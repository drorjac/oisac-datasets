# OpenMesh v1

*The six networks of the lecture* · `openmesh_v1`

| | |
|---|---|
| Sensor | CML (community mesh) |
| Region | New York City, USA |
| Period | Oct 2023 - Jun 2024 |
| Resolution | 1 min |
| Content | the first release, 103 links (links only on this record) |
| Operator / source | NYC Mesh (community network) |
| Licence | CC BY 4.0 |
| Paper | Jacoby et al. (2026), ESSD 18, 5817-5836, [doi:10.5194/essd-18-5817-2026](https://doi.org/10.5194/essd-18-5817-2026) |
| Data | [https://doi.org/10.5281/zenodo.15287692](https://doi.org/10.5281/zenodo.15287692) |

## Get it

```bash
python -m oisac_datasets fetch openmesh_v1            # the small split below
python -m oisac_datasets fetch openmesh_v1 --all      # the whole record
```

Split: the whole record (14 MB).

## Files in the record

| file | size |
|---|---:|
| `OpenMesh.zip` | 13.7 MB |
| **total** | **13.7 MB** |

## What the split holds

**`OpenMesh.zip`** (13.7 MB)

- 10 files, 332.7 MB unpacked; 3 x .csv, 2 x .html, 2 x .ipynb, 2 x .nc, 1 x .txt
- `dataset/maps/frequency_map.html` (486.3 kB)
- `dataset/maps/directional_map.html` (476.8 kB)
- `dataset/weather stations/read_pws_sample.ipynb` (1.0 MB)
- `dataset/weather stations/pws_opensense_sample_jan.nc` (9.8 MB)
- `dataset/weather stations/pws_metadata.csv` (1.8 kB)
- `dataset/weather stations/ASOS_stations.csv` (147 B)
- `dataset/links/ds_openmesh.nc` (320.3 MB)
- `dataset/links/links_metadata.csv` (7.3 kB)
- `dataset/links/openmesh_dataset_example.ipynb` (591.2 kB)
- `dataset/README.txt` (8.8 kB)

*inside:* `dataset/weather stations/ASOS_stations.csv`

```
Station ID,Latitude,Longitude,Elevation,Description
KNYC,40.779,-73.969,27,NY ASOS
KJFK,40.6386,-73.7622,7,NY ASOS
KLGA,40.7794,-73.8803,9,NY ASOS
```

*inside:* `dataset/links/links_metadata.csv`

```
,cml_id,sublink_id,site_0_lat,site_0_lon,site_1_lat,site_1_lon,frequency,length,polarization
0,1,sublink_1,40.696093,-73.939749,40.686198,-73.9175,68040,2178.1,v
1,1,sublink_2,40.686139,-73.917512,40.696096,-73.93978,68040,2183.0,v
2,1,sublink_3,40.685983,-73.917588,40.696,-73.9398,5765,2178.9,v
```

*inside:* `dataset/README.txt`

```
-------
The OpenMesh Sample Dataset
-------
Version: 1.0 (Sample Package)
```

