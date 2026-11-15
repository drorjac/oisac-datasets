"""The dataset catalogue (catalog.yaml) and the file listings of each data host."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import requests
import yaml

from .remote import UA

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.yaml"
GROUPS = {
    "main": "The six networks of the lecture",
    "more": "More open link datasets",
    "active": "Active approach: links built for the experiment",
    "upcoming": "Not open yet",
}


def data_dir() -> Path:
    """Where downloads go: $OISAC_DATA, else ~/data/oisac-datasets (never inside the repo)."""
    return Path(os.environ.get("OISAC_DATA", Path.home() / "data" / "oisac-datasets")).expanduser()


@dataclass
class RemoteFile:
    name: str
    size: int
    url: str
    checksum: str = ""


@dataclass
class Dataset:
    id: str
    name: str
    group: str
    source: dict
    sample: list = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    def __getattr__(self, k):
        try:
            return self.__dict__["extra"][k]
        except KeyError:
            raise AttributeError(k) from None

    def get(self, k, default=""):
        return self.extra.get(k, default)

    @property
    def is_open(self) -> bool:
        return self.source["type"] in ("zenodo", "4tu")

    @property
    def landing(self) -> str:
        s = self.source
        if self.get("data_doi"):
            return "https://doi.org/" + self.extra["data_doi"]
        return s.get("url", "")

    def files(self) -> list[RemoteFile]:
        """The files of the record, from the host's API (Zenodo or 4TU)."""
        s, t = self.source, self.source["type"]
        if t == "zenodo":
            j = requests.get(f"https://zenodo.org/api/records/{s['record']}", headers=UA, timeout=60).json()
            return [RemoteFile(f["key"], f["size"], f["links"]["self"], f.get("checksum", ""))
                    for f in j["files"]]
        if t == "4tu":
            j = requests.get(f"https://data.4tu.nl/v2/articles/{s['article']}/files", headers=UA, timeout=60).json()
            if isinstance(j, dict):
                j = j.get("files", [])
            return [RemoteFile(f["name"], f.get("size", 0), f["download_url"],
                               "md5:" + f["computed_md5"] if f.get("computed_md5") else "")
                    for f in j if not f.get("is_link_only")]
        return []

    def zenodo_latest(self) -> str | None:
        """The record id the DOI resolves to today (Zenodo versions move on)."""
        if self.source["type"] != "zenodo":
            return None
        j = requests.get(f"https://zenodo.org/api/records/{self.source['record']}", headers=UA, timeout=60).json()
        return str(j["id"])


def load() -> list[Dataset]:
    raw = yaml.safe_load(CATALOG.read_text())["datasets"]
    out = []
    for d in raw:
        d = dict(d)
        out.append(Dataset(d.pop("id"), d.pop("name"), d.pop("group"), d.pop("source"),
                           d.pop("sample", []), d))
    return out


def get(ds_id: str) -> Dataset:
    for d in load():
        if d.id == ds_id:
            return d
    raise KeyError(f"no dataset {ds_id!r}; try: " + ", ".join(d.id for d in load()))
