"""Rebuild the generated parts of README.md from catalog.yaml: the dataset tables and the gallery."""
from __future__ import annotations

from . import catalog
from .catalog import GROUPS

START, END = "<!-- TABLE START (python -m oisac_datasets docs) -->", "<!-- TABLE END -->"
GSTART, GEND = "<!-- GALLERY START -->", "<!-- GALLERY END -->"
ACCESS = {"zenodo": "download", "4tu": "download", "github": "download", "manual": "by hand", "closed": "not open"}


def _access(d):
    t = d.source["type"]
    host = {"zenodo": "Zenodo", "4tu": "4TU", "github": "GitHub"}.get(t, "")
    label = ACCESS[t] + (f" ({host})" if host else "")
    return f"[{label}]({d.landing})" if d.landing else label


def tables() -> str:
    L = []
    for g, title in GROUPS.items():
        ds = [d for d in catalog.load() if d.group == g]
        L += [f"### {title}", "", "| dataset | sensor | where | when | sampling | access | licence |",
              "|---|---|---|---|---|---|---|"]
        for d in ds:
            L.append(f"| [**{d.name}**](docs/datasets/{d.id}.md) | {d.get('sensor')} | {d.get('region')} | "
                     f"{d.get('period')} | {d.get('resolution')} | {_access(d)} | {d.get('licence')} |")
        L.append("")
    return "\n".join(L)


def gallery(per_row=3) -> str:
    figs = [d for d in catalog.load() if (catalog.ROOT / "docs" / "fig" / "datasets" / f"{d.id}.png").exists()]
    cells = [f'<a href="docs/datasets/{d.id}.md"><img src="docs/fig/datasets/{d.id}.png" width="100%"></a>'
             f"<br><sub><b>{d.name}</b></sub>" for d in figs]
    rows = ["<table>"]
    for i in range(0, len(cells), per_row):
        rows.append("<tr>" + "".join(f'<td width="33%" valign="top">{c}</td>' for c in cells[i:i + per_row]) + "</tr>")
    rows.append("</table>")
    return "\n".join(rows)


def _replace(s, a, b, body):
    i, j = s.index(a) + len(a), s.index(b)
    return s[:i] + "\n" + body + "\n" + s[j:]


def write_readme():
    p = catalog.ROOT / "README.md"
    s = p.read_text()
    s = _replace(s, START, END, tables())
    s = _replace(s, GSTART, GEND, gallery())
    p.write_text(s)
    print("wrote README.md tables and gallery")
