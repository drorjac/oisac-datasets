"""Rebuild the dataset tables in README.md (between the TABLE markers) from catalog.yaml."""
from __future__ import annotations

from . import catalog
from .catalog import GROUPS

START, END = "<!-- TABLE START (python -m oisac_datasets docs) -->", "<!-- TABLE END -->"


def tables() -> str:
    L = []
    for g, title in GROUPS.items():
        ds = [d for d in catalog.load() if d.group == g]
        L += [f"### {title}", "", "| dataset | sensor | region, period | resolution | licence | data |",
              "|---|---|---|---|---|---|"]
        for d in ds:
            data = f"[{d.source['type']}]({d.landing})" if d.landing else ""
            L.append(f"| [**{d.name}**](docs/datasets/{d.id}.md) | {d.get('sensor')} | {d.get('region')}; "
                     f"{d.get('period')} | {d.get('resolution')} | {d.get('licence')} | {data} |")
        L.append("")
    return "\n".join(L)


def write_readme():
    p = catalog.ROOT / "README.md"
    s = p.read_text()
    a, b = s.index(START) + len(START), s.index(END)
    p.write_text(s[:a] + "\n" + tables() + s[b:])
    print("wrote README.md tables")
