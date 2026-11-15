# Prague collocated CMLs

*More open link datasets* · `prague_collocated`

| | |
|---|---|
| Sensor | CML (processed) |
| Region | Prague, Czech Republic |
| Period | 2014-2016, non-winter |
| Resolution | 1 min |
| Content | pairs of links on the same path at 12 sites, 22-38 GHz, 33 rain events; rain-induced attenuation and rain rate |
| Licence | CC BY 4.0 |
| Paper | Spackova et al. (2023) |
| Data | [https://doi.org/10.5281/zenodo.8009877](https://doi.org/10.5281/zenodo.8009877) |

## Get it

```bash
python -m oisac_datasets fetch prague_collocated            # the small split below
python -m oisac_datasets fetch prague_collocated --all      # the whole record
```

Split: the whole record (2 MB).

## Files in the record

| file | size |
|---|---:|
| `dataset.zip` | 1.9 MB |
| **total** | **1.9 MB** |

## What the split holds

**`dataset.zip`** (1.9 MB)

- 23 files, 18.7 MB unpacked; 23 x .txt
- `Rain_induced_attenuation/Rain_induced_attenuation_data_10a.txt` (676.7 kB)
- `Rain_induced_attenuation/Rain_induced_attenuation_data_1a.txt` (676.7 kB)
- `Rain_induced_attenuation/Rain_induced_attenuation_data_2a.txt` (676.7 kB)
- `Rain_induced_attenuation/Rain_induced_attenuation_data_3a.txt` (676.7 kB)
- `Rain_induced_attenuation/Rain_induced_attenuation_data_6a.txt` (676.7 kB)
- `Rain_induced_attenuation/Rain_induced_attenuation_data_7a.txt` (676.7 kB)
- `Rain_induced_attenuation/Rain_induced_attenuation_data_8a.txt` (676.7 kB)
- `Rain_induced_attenuation/Rain_induced_attenuation_data_9a.txt` (676.7 kB)
- `Rainfall_intensity/Rainfall_intensity_data_10a.txt` (951.0 kB)
- `Rainfall_intensity/Rainfall_intensity_data_11b.txt` (951.0 kB)
- `Rainfall_intensity/Rainfall_intensity_data_12b.txt` (951.0 kB)
- `Rainfall_intensity/Rainfall_intensity_data_1a.txt` (951.0 kB)
- ... 11 more

*inside:* `Read_me.txt`

```
Data for the paper Evaluation of error components in rainfall retrieval from collocated commercial microwave links
by Špačková, A., Fencl, M. and Bareš, V.


```

*inside:* `Rain_induced_attenuation/Rain_induced_attenuation_data_10a.txt`

```
"time_utc" "link1_attenuation" "link2_attenuation"
2014-07-08 09:40:00 "-0.50" "-0.21"
2014-07-08 09:41:00 "-0.62" "-0.21"
2014-07-08 09:42:00 "-0.43" "-0.30"
```

*inside:* `Rain_induced_attenuation/Rain_induced_attenuation_data_1a.txt`

```
"time_utc" "link1_attenuation" "link2_attenuation"
2014-07-08 09:40:00 "-0.03" " 0.01"
2014-07-08 09:41:00 "-0.14" "-0.12"
2014-07-08 09:42:00 " 0.20" "-0.26"
```

