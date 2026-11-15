# Prague E-band CMLs

*More open link datasets* · `prague_eband`

| | |
|---|---|
| Sensor | CML (E-band) |
| Region | Prague, Czech Republic |
| Period | one season |
| Resolution | 1 and 5 min |
| Content | E-band (71-86 GHz) CML losses with rain gauges, temperature and humidity; raw and regular series, R code |
| Licence | CC BY 4.0 |
| Paper | Fencl et al. (2020), AMT 13, 6559-6578, [doi:10.5194/amt-13-6559-2020](https://doi.org/10.5194/amt-13-6559-2020) |
| Data | [https://doi.org/10.5281/zenodo.4090953](https://doi.org/10.5281/zenodo.4090953) |

## Get it

```bash
python -m oisac_datasets fetch prague_eband            # the small split below
python -m oisac_datasets fetch prague_eband --all      # the whole record
```

Split: one preprocessed link, the link and station metadata and one gauge, from inside the 85 MB zip (read over HTTP).

## Files in the record

| file | size |
|---|---:|
| `dataset.zip` | 85.3 MB |
| **total** | **85.3 MB** |

## Inside `dataset.zip` (read over HTTP)

54 members, 1.0 GB unpacked; 49 x .csv, 2 x .html, 2 x .rmd, 1 x .txt
- `CML_weather_retrieval.nb.html` (5.2 MB)
- `CML_weather_retrieval.Rmd` (48.0 kB)
- `Data_Preprocessing.nb.html` (836.5 kB)
- `Data_Preprocessing.Rmd` (11.9 kB)
- `preprocessed/commercial_microwave_links_total_loss/1a.csv` (4.4 MB)
- `preprocessed/commercial_microwave_links_total_loss/1b.csv` (4.4 MB)
- `preprocessed/commercial_microwave_links_total_loss/2a.csv` (4.4 MB)
- `preprocessed/commercial_microwave_links_total_loss/2b.csv` (4.4 MB)
- `preprocessed/commercial_microwave_links_total_loss/3a.csv` (4.4 MB)
- `preprocessed/commercial_microwave_links_total_loss/3b.csv` (4.4 MB)
- `preprocessed/commercial_microwave_links_total_loss/4a.csv` (4.4 MB)
- `preprocessed/commercial_microwave_links_total_loss/4b.csv` (4.4 MB)
- ... 42 more (full list: `_zip_contents.tsv` after a fetch)

## What the split holds

**`dataset/preprocessed/commercial_microwave_links_total_loss/1a.csv`** (4.4 MB)

```
time;total_loss
2018-08-20 00:00:00;NA
2018-08-20 00:01:00;50.6
2018-08-20 00:02:00;50.6
2018-08-20 00:03:00;50.4
2018-08-20 00:04:00;50.5
```

**`dataset/preprocessed/commercial_microwave_links_total_loss/metadata_table_commercial_microwave_links.csv`** (601 B)

```
id;lonA;latA;lonB;latB;freqA;freqB;polA;polB;length;idglob;manufacturer;type;id_old
1;14.53;50.03;14.6;50.03;73.5;83.5;V;V;4866;52206_52205;Ericsson;MINILINK;1147_1148
2;14.53;50.03;14.51;50.02;73.75;83.75;V;V;1409;51808_51814;Ericsson;MINILINK;3004_3005
3;14.53;50.03;14.51;50.03;72.75;82.75;V;V;1164;51928_51927;Ericsson;MINILINK;3050_3051
4;14.53;50.03;14.52;50.03;74.25;84.25;H;H;765;51895_51896;Ericsson;MINILINK;3010_3011
5;14.53;50.04;14.53;50.03;73;83;V;V;573;51759_51758;Ericsson;MINILINK;3007_3006
```

**`dataset/preprocessed/meteo_data/metadata_meteo.csv`** (895 B)

```
Atmospheric observations are collected at four sites using tipping bucket rain gauges (MR3, METEOSERVIS v.o.s., catch area 500 cm^2, resolution 0.1 mm). Two rai
;;;
name:;site_1;;
observations:;rainfall tips (pulse);air temperature (air temperature (°C); air relative humidity (%)
position (lattitude-longitude):;50.0302N;14.5291E;
;;;
```

**`dataset/preprocessed/meteo_data/metadata_meteo_table.csv`** (226 B)

```
Name;lat;lon;rainfall intensity (mm h^-1);air temperature (degrees of Celsius);air relative humidity (%)
site_1;50.0302;14.5291;T;T;T
site_2;50.0296;14.5458;T;T;T
site_3;50.0315;14.5982;T;F;F
site_4;50.0231;14.4984;T;F;F
```

**`dataset/preprocessed/meteo_data/site_1_rainfall_intensity.csv`** (3.9 MB)

```
time;rainfall_intensity
2018-08-20 00:00:00;0
2018-08-20 00:01:00;0
2018-08-20 00:02:00;0
2018-08-20 00:03:00;0
2018-08-20 00:04:00;0
```

