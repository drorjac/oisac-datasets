"""Offline checks of catalog.yaml (no network)."""
from oisac_datasets import catalog


def test_ids_unique_and_groups_known():
    ds = catalog.load()
    ids = [d.id for d in ds]
    assert len(ids) == len(set(ids))
    assert {d.group for d in ds} <= set(catalog.GROUPS)


def test_sources_complete():
    for d in catalog.load():
        t = d.source["type"]
        assert t in ("zenodo", "4tu", "github", "manual", "closed"), d.id
        if t == "zenodo":
            assert d.source["record"].isdigit(), d.id
        if t == "4tu":
            assert d.source["article"], d.id
        if t in ("manual", "closed", "github"):
            assert d.source["url"].startswith("https://"), d.id
        if t in ("zenodo", "4tu", "github"):
            assert d.sample, f"{d.id}: open dataset without a split"


def test_closed_not_open():
    for d in catalog.load():
        if d.group == "closed":
            assert not d.is_open and "not open" in d.get("licence")
