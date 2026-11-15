"""Describe what a dataset holds: catalogue facts, the record's files, and what is inside the
downloaded split (netCDF dimensions and variables, table columns, zip members)."""
from __future__ import annotations

import zipfile
from pathlib import Path

from .catalog import GROUPS, Dataset, data_dir
from .fetch import _human

TEXT = {".csv", ".txt", ".dat", ".tsv", ".asc", ".yaml", ".yml", ".r", ".md", ".kml", ".json"}


def describe_netcdf(p: Path) -> list[str]:
    import xarray as xr
    try:
        ds = xr.open_dataset(p)
    except Exception as e:  # noqa: BLE001
        return [f"(could not open with xarray: {e})"]
    out = ["dims: " + ", ".join(f"{k}={v}" for k, v in ds.sizes.items())]
    if "time" in ds.coords and ds.sizes.get("time", 0):
        t = ds["time"].values
        out.append(f"time: {str(t[0])[:19]} .. {str(t[-1])[:19]}")
    for name, v in list(ds.data_vars.items())[:14]:
        unit = v.attrs.get("units", "")
        ln = v.attrs.get("long_name", "")
        out.append(f"`{name}` {tuple(v.dims)} {unit} {('- ' + ln) if ln else ''}".rstrip())
    if len(ds.data_vars) > 14:
        out.append(f"... and {len(ds.data_vars) - 14} more variables")
    coords = [c for c in ds.coords if c not in ds.dims]
    if coords:
        out.append("coords: " + ", ".join(coords[:12]))
    ds.close()
    return out


def describe_text(p: Path, n=6) -> list[str]:
    try:
        with open(p, errors="replace") as f:
            lines = [ln.rstrip()[:160] for _, ln in zip(range(n), f)]
    except Exception as e:  # noqa: BLE001
        return [f"(unreadable: {e})"]
    return ["```", *lines, "```"]


def describe_gz(p: Path, n=6) -> list[str]:
    import gzip
    with gzip.open(p, "rt", errors="replace") as f:
        lines = [ln.rstrip()[:160] for _, ln in zip(range(n), f)]
    return ["```", *lines, "```"]


def _peek_members(p: Path, info, limit=3, max_bytes=80e6, skip=()) -> list[str]:
    """Open the first few netCDF/CSV members of a local zip and describe them."""
    import fnmatch
    import tempfile
    out, done = [], 0
    for i in info:
        suf = Path(i.filename).suffix.lower()
        if suf not in (".nc", ".csv", ".txt") or i.file_size > max_bytes or done >= limit:
            continue
        if any(fnmatch.fnmatch(i.filename.lower(), pat) for pat in skip):
            continue
        with zipfile.ZipFile(p) as z, tempfile.TemporaryDirectory() as td:
            t = Path(td) / Path(i.filename).name
            t.write_bytes(z.read(i))
            d = describe_netcdf(t) if suf == ".nc" else describe_text(t, 4)
        out += ["", f"*inside:* `{i.filename}`", ""]
        out += d if d and d[0] == "```" else [f"- {x}" for x in d]
        done += 1
    return out


def describe_zip(p: Path, n=12, skip=()) -> list[str]:
    with zipfile.ZipFile(p) as z:
        info = [i for i in z.infolist() if not i.is_dir()]
    exts: dict[str, int] = {}
    for i in info:
        exts[Path(i.filename).suffix.lower() or "(none)"] = exts.get(Path(i.filename).suffix.lower() or "(none)", 0) + 1
    out = [f"{len(info)} files, {_human(sum(i.file_size for i in info))} unpacked; "
           + ", ".join(f"{v} x {k}" for k, v in sorted(exts.items(), key=lambda kv: -kv[1]))]
    out += [f"- `{i.filename}` ({_human(i.file_size)})" for i in info[:n]]
    if len(info) > n:
        out.append(f"- ... {len(info) - n} more")
    nc_first = sorted(info, key=lambda i: (Path(i.filename).suffix.lower() != ".nc", i.file_size))
    return out + _peek_members(p, nc_first, skip=skip)


def describe_file(p: Path, skip=()) -> list[str]:
    import fnmatch
    if any(fnmatch.fnmatch(str(p).lower(), pat) for pat in skip):
        return ["(no preview: excluded for this dataset)"]
    s = p.suffix.lower()
    if s in (".nc", ".nc4", ".netcdf"):
        return describe_netcdf(p)
    if s == ".zip":
        return describe_zip(p, skip=skip)
    if s == ".gz":
        return describe_gz(p)
    if s in TEXT:
        return describe_text(p)
    return []


def zip_listing_summary(tsv: Path, n=12) -> list[str]:
    rows = [ln.split("\t") for ln in tsv.read_text().splitlines()[1:] if ln]
    total = sum(int(b) for _, b in rows)
    exts: dict[str, int] = {}
    for m, _ in rows:
        e = Path(m).suffix.lower() or "(none)"
        exts[e] = exts.get(e, 0) + 1
    out = [f"{len(rows)} members, {_human(total)} unpacked; "
           + ", ".join(f"{v} x {k}" for k, v in sorted(exts.items(), key=lambda kv: -kv[1])[:6])]
    out += [f"- `{m}` ({_human(int(b))})" for m, b in rows[:n]]
    if len(rows) > n:
        out.append(f"- ... {len(rows) - n} more (full list: `{tsv.name}` after a fetch)")
    return out


def markdown(ds: Dataset, online=True) -> str:
    g = ds.get
    L = [f"# {ds.name}", "", f"*{GROUPS[ds.group]}* · `{ds.id}`", ""]
    rows = [("Sensor", g("sensor")), ("Region", g("region")), ("Period", g("period")),
            ("Resolution", g("resolution")), ("Content", g("content")), ("Operator / source", g("operator")),
            ("Licence", g("licence")),
            ("Paper", f"{g('paper')}" + (f", [doi:{g('paper_doi')}](https://doi.org/{g('paper_doi')})" if g("paper_doi") else "")),
            ("Data", f"[{ds.landing}]({ds.landing})" if ds.landing else "")]
    L += ["| | |", "|---|---|"] + [f"| {k} | {v} |" for k, v in rows if v] + [""]
    if ds.group == "upcoming":
        L += ["**Not open yet.** The data are in the TAU CellEnMon lab database and are being prepared "
              "for a public release. This page will get a download once they are out.", ""]
        return "\n".join(L)
    if ds.source["type"] == "manual":
        L += ["## Download", "", f"No automatic download: {ds.source.get('note', '')}.", "",
              f"Page: <{ds.source['url']}>", ""]
        return "\n".join(L)

    L += ["## Get it", "", "```bash",
          f"python -m oisac_datasets fetch {ds.id}            # the small split below",
          f"python -m oisac_datasets fetch {ds.id} --all      # the whole record",
          "```", "", f"Split: {g('sample_note')}.", ""]
    if online and ds.is_open:
        try:
            files = ds.files()
            L += ["## Files in the record", "", "| file | size |", "|---|---:|"]
            L += [f"| `{f.name}` | {_human(f.size)} |" for f in files]
            L += [f"| **total** | **{_human(sum(f.size for f in files))}** |", ""]
            latest = ds.zenodo_latest()
            if latest and latest != ds.source["record"]:
                L += [f"The DOI now resolves to Zenodo record {latest} (a newer version); the tool follows it.", ""]
        except Exception as e:  # noqa: BLE001
            L += [f"(file list unavailable: {e})", ""]

    out = data_dir() / ds.id
    tsvs = sorted(out.glob("*/_zip_contents.tsv")) if out.exists() else []
    for t in tsvs:
        L += [f"## Inside `{t.parent.name}.zip` (read over HTTP)", ""] + zip_listing_summary(t) + [""]
    local = [p for p in sorted(out.rglob("*")) if p.is_file() and p.name not in ("MANIFEST.json", "_zip_contents.tsv")
             and not p.name.endswith(".part")] if out.exists() else []
    if local:
        L += ["## What the split holds", ""]
        for p in local:
            L += [f"**`{p.relative_to(out)}`** ({_human(p.stat().st_size)})", ""]
            d = describe_file(p, skip=ds.get("no_preview", []) or ())
            code = False
            for x in d:
                if x.startswith("```"):
                    code = not code
                L.append(x if code or x.startswith(("- ", "*inside", "```")) or not x else f"- {x}")
            if d:
                L.append("")
    return "\n".join(L)
