"""Command line: python -m oisac_datasets {list,info,files,contents,fetch,describe,docs}"""
from __future__ import annotations

import argparse

from . import catalog
from .catalog import GROUPS, data_dir
from .describe import markdown
from .fetch import _human, fetch, zip_contents


def main(argv=None):
    ap = argparse.ArgumentParser(prog="oisac_datasets", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="all datasets")
    for c, h in [("info", "catalogue entry"), ("files", "files in the record, with sizes"),
                 ("describe", "write docs/datasets/<id>.md from the record and the local split")]:
        sub.add_parser(c, help=h).add_argument("id")
    p = sub.add_parser("contents", help="list the members of a zip in the record, over HTTP")
    p.add_argument("id"); p.add_argument("zip")
    p = sub.add_parser("fetch", help="download the split (default) or more")
    p.add_argument("id", nargs="+", help="dataset ids, or 'open' for every open dataset")
    p.add_argument("--all", action="store_true", help="every file of the record")
    p.add_argument("--file", action="append", help="one file of the record (repeatable)")
    p.add_argument("--zip", help="with --member: the zip to read")
    p.add_argument("--member", action="append", help="member name or glob inside --zip (repeatable)")
    p.add_argument("--max-mb", type=float, default=150, help="skip split files larger than this")
    sub.add_parser("docs", help="describe every dataset and rebuild the README table")
    a = ap.parse_args(argv)

    if a.cmd == "list":
        for g, title in GROUPS.items():
            print(f"\n{title}")
            for d in catalog.load():
                if d.group == g:
                    print(f"  {d.id:<18} {d.name:<34} {d.get('sensor'):<26} {d.get('licence')}")
        print(f"\ndata folder: {data_dir()}  (set OISAC_DATA to change)")
    elif a.cmd == "info":
        d = catalog.get(a.id)
        for k, v in {"name": d.name, "group": d.group, **d.extra, "data": d.landing}.items():
            print(f"{k:>12}: {v}")
    elif a.cmd == "files":
        fs = catalog.get(a.id).files()
        for f in fs:
            print(f"{_human(f.size):>10}  {f.name}")
        print(f"{_human(sum(f.size for f in fs)):>10}  total")
    elif a.cmd == "contents":
        rf = {f.name: f for f in catalog.get(a.id).files()}[a.zip]
        _, members = zip_contents(rf)
        for n, s in members:
            print(f"{_human(s):>10}  {n}")
        print(f"{len(members)} members")
    elif a.cmd == "fetch":
        ids = [d.id for d in catalog.load() if d.is_open] if a.id == ["open"] else a.id
        for i in ids:
            d = catalog.get(i)
            print(f"== {d.id}: {d.name}")
            got = fetch(d, mode="all" if a.all else "sample", files=a.file, members=a.member,
                        zip_name=a.zip, max_mb=a.max_mb)
            print(f"   {len(got)} files in {data_dir() / d.id}")
    elif a.cmd == "describe":
        _write_doc(catalog.get(a.id))
    elif a.cmd == "docs":
        for d in catalog.load():
            _write_doc(d)
        from .readme import write_readme
        write_readme()


def _write_doc(d):
    p = catalog.ROOT / "docs" / "datasets" / f"{d.id}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(markdown(d) + "\n")
    print(f"wrote {p.relative_to(catalog.ROOT)}")


if __name__ == "__main__":
    main()
