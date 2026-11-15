"""Download a dataset, or just a small split of it.

    fetch(ds)                    the sample split from catalog.yaml (default)
    fetch(ds, mode="all")        every file of the record
    fetch(ds, files=["x.zip"])   chosen files of the record
    fetch(ds, members=["a/b.nc"], zip_name="x.zip")   chosen members of a remote zip
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import sys
import time
from pathlib import Path

import requests

from .catalog import Dataset, RemoteFile, data_dir
from .remote import UA, remote_zip

RAW = "https://raw.githubusercontent.com/{repo}/{ref}/{path}"


def _human(n: float) -> str:
    for u in ("B", "kB", "MB", "GB", "TB"):
        if n < 1000 or u == "TB":
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1000
    return ""


def download(url: str, dest: Path, size: int | None = None, checksum: str = "", quiet=False) -> Path:
    """Stream a file to disk; resumes a partial file; checks md5 when the host gives one."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and size and dest.stat().st_size == size:
        if not quiet:
            print(f"  have {dest.name} ({_human(size)})")
        return dest
    part = dest.with_suffix(dest.suffix + ".part")
    have = part.stat().st_size if part.exists() else 0
    headers = dict(UA)
    if have:
        headers["Range"] = f"bytes={have}-"
    with requests.get(url, headers=headers, stream=True, timeout=120) as r:
        r.raise_for_status()
        if have and r.status_code != 206:
            have = 0
        total = size or int(r.headers.get("Content-Length", 0)) + have
        t0, done = time.time(), have
        with open(part, "ab" if have else "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
                done += len(chunk)
                if not quiet and total:
                    rate = (done - have) / max(time.time() - t0, 1e-3)
                    sys.stdout.write(f"\r  {dest.name}: {_human(done)} / {_human(total)}  ({_human(rate)}/s)   ")
                    sys.stdout.flush()
    if not quiet:
        sys.stdout.write("\n")
    if checksum.startswith("md5:"):
        h = hashlib.md5()
        with open(part, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        if h.hexdigest() != checksum[4:]:
            raise OSError(f"md5 mismatch for {dest.name}; delete {part} and try again")
    part.rename(dest)
    return dest


def zip_contents(rf: RemoteFile):
    """List the members of a remote zip (name, size) without downloading it."""
    z = remote_zip(rf.url, rf.size)
    return z, [(i.filename, i.file_size) for i in z.infolist() if not i.is_dir()]


def extract_members(ds: Dataset, rf: RemoteFile, pick, out: Path, quiet=False,
                    head_mb: float | None = None) -> list[Path]:
    """Extract chosen members of a remote zip. `pick` is an int (the n smallest) or names/globs.
    With `head_mb`, keep only the first head_mb MB of each member, cut at a line end (text files)."""
    z, members = zip_contents(rf)
    stem = out / Path(rf.name).stem
    stem.mkdir(parents=True, exist_ok=True)
    (stem / "_zip_contents.tsv").write_text(
        "member\tbytes\n" + "".join(f"{n}\t{s}\n" for n, s in members))
    if isinstance(pick, int):
        names = [n for n, _ in sorted(members, key=lambda m: m[1])[:pick]]
    else:
        names = [n for n, _ in members if any(fnmatch.fnmatch(n, p) for p in pick)]
    got = []
    for n in names:
        dest = stem / n
        dest.parent.mkdir(parents=True, exist_ok=True)
        with z.open(n) as src:
            if head_mb:
                data = src.read(int(head_mb * 1e6))
                data = data[:data.rfind(b"\n") + 1] or data
                dest = dest.with_name(dest.name + ".head")
            else:
                data = src.read()
        with open(dest, "wb") as f:
            f.write(data)
        if not quiet:
            print(f"  {rf.name} -> {n} ({_human(dest.stat().st_size)})")
        got.append(dest)
    if not quiet:
        print(f"  ({len(members)} members listed in {stem.name}/_zip_contents.tsv, "
              f"{z.fp.requests} range requests, the zip itself was not downloaded)")
    return got


def fetch(ds: Dataset, mode: str = "sample", files: list[str] | None = None,
          members: list[str] | None = None, zip_name: str | None = None,
          max_mb: float = 150, quiet=False) -> list[Path]:
    if not ds.is_open:
        msg = ds.source.get("note") or ds.get("licence")
        print(f"{ds.id}: no automatic download ({ds.source['type']}). {msg}\n  {ds.landing}")
        return []
    out = data_dir() / ds.id
    out.mkdir(parents=True, exist_ok=True)
    record = {f.name: f for f in ds.files()}
    got: list[Path] = []

    if members:
        return extract_members(ds, record[zip_name], members, out, quiet)
    if files or mode == "all":
        for name in (files or list(record)):
            f = record[name]
            got.append(download(f.url, out / f.name, f.size, f.checksum, quiet))
        return got

    budget = max_mb * 1e6
    for spec in ds.sample:
        if "github" in spec:
            url = RAW.format(repo=spec["github"], ref=spec.get("ref", "main"), path=spec["path"])
            got.append(download(url, out / "example" / Path(spec["path"]).name, quiet=quiet))
        elif "smallest" in spec:
            for f in sorted(record.values(), key=lambda f: f.size)[:spec["smallest"]]:
                if f.size <= budget:
                    got.append(download(f.url, out / f.name, f.size, f.checksum, quiet))
        elif "members" in spec:
            got += extract_members(ds, record[spec["file"]], spec["members"], out, quiet, spec.get("head_mb"))
        else:
            f = record[spec["file"]]
            if f.size > budget:
                print(f"  skip {f.name} ({_human(f.size)} > {max_mb:.0f} MB); use --all or --max-mb")
                continue
            got.append(download(f.url, out / f.name, f.size, f.checksum, quiet))
    (out / "MANIFEST.json").write_text(json.dumps(
        {"dataset": ds.id, "landing": ds.landing, "mode": mode,
         "files": [str(p.relative_to(out)) for p in got]}, indent=1))
    return got
