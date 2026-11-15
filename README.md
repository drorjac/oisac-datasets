# oisac-datasets

Every dataset in the OISAC lecture **"Open datasets for opportunistic sensing"**, in one place:
where each one lives, what is in it, and a small tool that downloads it, or only a small
split of it, and describes what came down.

Opportunistic sensing reads weather from radio links built for something else: cellular
backhaul (CML), community and smart-city mesh networks, satellite TV links (SML), and
citizen weather stations (PWS). The lecture uses six open networks and points to a dozen
more; they are all listed below, each with its own page in [`docs/datasets/`](docs/datasets).

## Quick start

```bash
git clone git@github.com:drorjac/oisac-datasets.git && cd oisac-datasets
pip install -e .                       # requests, pyyaml, xarray, netCDF4

python -m oisac_datasets list          # the catalogue
python -m oisac_datasets files netherlands         # files in the record and their sizes
python -m oisac_datasets contents openmesh openmesh-2.0.0.zip   # inside a zip, over HTTP
python -m oisac_datasets fetch openmrg             # the small split (default)
python -m oisac_datasets fetch open                # the split of every open dataset (~200 MB)
python -m oisac_datasets fetch opensat4weather --all              # the whole record
python -m oisac_datasets fetch netherlands --zip RawCMLdata.zip --member "*2012*"  # chosen members
python -m oisac_datasets docs          # rebuild docs/datasets/*.md and the tables below
```

Data go to `~/data/oisac-datasets/<id>/` (set `OISAC_DATA` to move it), never into the
repository.

### The split, and reading big archives without downloading them

Most records are one large zip (OpenMRG 318 MB, OpenMesh 606 MB, the Netherlands 12.6 GB).
Zenodo and 4TU.ResearchData answer HTTP range requests, so the tool opens such a zip
**remotely**: it reads the zip's table of contents and pulls out single members with a
few small requests. `fetch` uses this for the default split, which keeps every split
small: the record's README and metadata, one or a few data files, or the OpenSense
8-day example subsets (OpenMRG, OpenRainER, Amsterdam PWS), which are already in the
[OpenSense data format](https://github.com/OpenSenseAction/OS_data_format_conventions).
`--all` downloads the full record, with resume and an md5 check.

## The datasets

<!-- TABLE START (python -m oisac_datasets docs) -->
### The six networks of the lecture

| dataset | sensor | region, period | resolution | licence | data |
|---|---|---|---|---|---|
| [**OpenMRG**](docs/datasets/openmrg.md) | CML | Gothenburg, Sweden; Jun-Aug 2015 | 10 s | CC BY-SA 4.0 | [zenodo](https://doi.org/10.5281/zenodo.7107689) |
| [**OpenRainER**](docs/datasets/openrainer.md) | CML | Emilia-Romagna, Italy; 2021-2022 | 1 min | CC BY 4.0 | [zenodo](https://doi.org/10.5281/zenodo.10593848) |
| [**Netherlands CML (2011-2015)**](docs/datasets/netherlands.md) | CML | the Netherlands; Jan 2011 - Mar 2015 | 15 min (min/max RSL) | CC BY 4.0 | [4tu](https://doi.org/10.4121/be252844-b672-471e-8d69-27269a862ec1.v1) |
| [**OpenSat4Weather**](docs/datasets/opensat4weather.md) | SML | southern France; Aug-Dec 2022 | 1 min | CC BY 4.0 | [zenodo](https://doi.org/10.5281/zenodo.16530166) |
| [**Amsterdam PWS**](docs/datasets/amsterdam_pws.md) | PWS | Amsterdam, the Netherlands; May 2016 - May 2018 | 5 min | CC BY 4.0 | [4tu](https://doi.org/10.4121/uuid:6e6a9788-49fc-4635-a43d-a2fa164d37ec) |
| [**OpenMesh v2**](docs/datasets/openmesh.md) | CML (community mesh) | New York City, USA; Oct 2023 - Nov 2026, yearly updates | 1 min, later 6 min | CC BY 4.0 | [zenodo](https://doi.org/10.5281/zenodo.23283445) |
| [**OpenMesh v1**](docs/datasets/openmesh_v1.md) | CML (community mesh) | New York City, USA; Oct 2023 - Jun 2024 | 1 min | CC BY 4.0 | [zenodo](https://doi.org/10.5281/zenodo.15287692) |

### More open link datasets

| dataset | sensor | region, period | resolution | licence | data |
|---|---|---|---|---|---|
| [**Wageningen campaign**](docs/datasets/wageningen.md) | CML (research links) | Wageningen, the Netherlands; Aug 2014 - Jan 2016 | 20 Hz | CC0 | [4tu](https://doi.org/10.4121/uuid:1dd45123-c732-4390-9fe4-6e09b578d4ff) |
| [**Prague collocated CMLs**](docs/datasets/prague_collocated.md) | CML (processed) | Prague, Czech Republic; 2014-2016, non-winter | 1 min | CC BY 4.0 | [zenodo](https://doi.org/10.5281/zenodo.8009877) |
| [**Prague E-band CMLs**](docs/datasets/prague_eband.md) | CML (E-band) | Prague, Czech Republic; one season | 1 and 5 min | CC BY 4.0 | [zenodo](https://doi.org/10.5281/zenodo.4090953) |
| [**Prague E-band link (water vapour)**](docs/datasets/prague_eband_link.md) | CML (E-band) | Prague, Czech Republic; 7 months | 5 min | CC BY 4.0 | [zenodo](https://doi.org/10.5281/zenodo.5013463) |
| [**CoMMon (Dubendorf)**](docs/datasets/common_dubendorf.md) | CML (dual-pol.) | Dubendorf, Switzerland; Mar 2011 - Mar 2012 | 4 s | CC BY 4.0 | [zenodo](https://doi.org/10.5281/zenodo.4923125) |
| [**Netherlands CML (2011-2012)**](docs/datasets/nl_2011_12.md) | CML | the Netherlands; Jun 2011 - Sep 2012 | 15 min (min/max RSL) | CC BY 4.0 | [4tu](https://doi.org/10.4121/7a692e36-c32f-4916-813b-c62d2566e8d8) |
| [**Sri Lanka rainfall maps**](docs/datasets/srilanka.md) | CML product (maps only) | Sri Lanka; Sep-Dec 2019 | 15 min, 0.02 deg grid | CC BY 4.0 | [4tu](https://doi.org/10.4121/14166539) |

### Active approach: links built for the experiment

| dataset | sensor | region, period | resolution | licence | data |
|---|---|---|---|---|---|
| [**COSMOS 28 GHz measurements**](docs/datasets/cosmos.md) | mmWave channel measurements (testbed) | West Harlem, New York City, USA; 2019 (street level), 2022-2024 (outdoor to indoor) | campaign | see the source | [manual](https://wiki.cosmos-lab.org/wiki/Datasets) |
| [**AraHaul link and weather**](docs/datasets/arahaul.md) | CML (research link) + weather | Ames, Iowa, USA; 4-5 Jul 2023 (link runs), 48 h weather | 1 s | CC BY 4.0 | [manual](https://doi.org/10.21227/6ncx-rs20) |

### Not open yet

| dataset | sensor | region, period | resolution | licence | data |
|---|---|---|---|---|---|
| [**Israel CML network (TAU CellEnMon)**](docs/datasets/israel_tau.md) | CML | Israel; 2005- | 15 min to 1/day (five protocols) | not open yet (being prepared for release) | [upcoming](https://cellenmonlab.tau.ac.il) |
| [**Rehovot smart-city E-band network**](docs/datasets/rehovot_scwn.md) | CML (smart-city x-haul) | Rehovot, Israel; 2020 | 30 s | not open yet | [upcoming](https://cellenmonlab.tau.ac.il) |
<!-- TABLE END -->

## Cite the data you use

Each dataset page gives the paper and the data DOI. Please cite both, and respect each
record's licence (most are CC BY 4.0; OpenMRG is CC BY-SA 4.0; Wageningen is CC0).

## Related

- OpenSense COST Action CA20136: <https://opensenseaction.eu>, code and conventions at
  <https://github.com/OpenSenseAction>, its dataset list at <https://opensenseaction.eu/outputs/datasets/>
- OpenSense example data (the 8-day subsets): <https://github.com/OpenSenseAction/opensense_example_data>
- OpenMesh: <https://github.com/drorjac/OpenMesh>
- TAU CellEnMon lab: <https://cellenmonlab.tau.ac.il>

Code: MIT licence. The data are not in this repository and keep their own licences.
