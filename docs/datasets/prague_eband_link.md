# Prague E-band link (water vapour)

*More open link datasets* · `prague_eband_link`

| | |
|---|---|
| Sensor | CML (E-band) |
| Region | Prague, Czech Republic |
| Period | 7 months |
| Resolution | 5 min |
| Content | one 4.87 km link at 73.5/83.5 GHz with temperature and humidity, for water vapour retrieval |
| Licence | CC BY 4.0 |
| Paper | Fencl et al. (2021) |
| Data | [https://doi.org/10.5281/zenodo.5013463](https://doi.org/10.5281/zenodo.5013463) |

## Get it

```bash
python -m oisac_datasets fetch prague_eband_link            # the small split below
python -m oisac_datasets fetch prague_eband_link --all      # the whole record
```

Split: the whole record (6 MB).

## Files in the record

| file | size |
|---|---:|
| `Dataset_1.0.0.zip` | 6.2 MB |
| **total** | **6.2 MB** |

## What the split holds

**`Dataset_1.0.0.zip`** (6.2 MB)

- 29 files, 29.3 MB unpacked; 14 x .csv, 4 x .txt, 4 x .html, 4 x .rmd, 3 x .pdf
- `data_metedata/commercial_microwave_link_total_loss/cml_total_loss.csv` (1.8 MB)
- `data_metedata/commercial_microwave_link_total_loss/metadata_commercial_microwave_link.txt` (953 B)
- `data_metedata/meteo_observations/datasheet_MR3(H)XX_2017_CES1.pdf` (561.0 kB)
- `data_metedata/meteo_observations/datasheet_rvt12-13-v2_Czech_language.pdf` (318.8 kB)
- `data_metedata/meteo_observations/datasheet_rvt_10-11_0_Czech_language.pdf` (210.8 kB)
- `data_metedata/meteo_observations/metadata_meteo.txt` (1.1 kB)
- `data_metedata/meteo_observations/site_1_humidity.csv` (1.5 MB)
- `data_metedata/meteo_observations/site_1_temperature.csv` (1.5 MB)
- `data_metedata/meteo_observations/site_2_humidity.csv` (1.6 MB)
- `data_metedata/meteo_observations/site_2_temperature.csv` (1.5 MB)
- `data_metedata/meteo_observations/wet_weather_classifier.csv` (1.5 MB)
- `data_metedata/synthetic_gaseous_attenuation/k_theor_site1.csv` (2.1 MB)
- ... 17 more

*inside:* `data_metedata/synthetic_gaseous_attenuation/k_wvd_model_parameters.csv`

```
"f";"epsilon";"gamma";"delta";"kT0";"kT20"
73.5;0.0175;19.5015;0.751;0.14;0.112
83.5;0.0179;16.0967;0.7496;0.046;0.035
```

*inside:* `data_metedata/commercial_microwave_link_total_loss/metadata_commercial_microwave_link.txt`

```
Commercial microwave link (CML) operated by T-Mobile CZ on Ericsson MINILINK platform.
Total loss is obtained as the difference between transmitted (tx) and received (rx) signal powers. Original data obtained at irregular time step (dt ~ 10 s) are

CML metadata:
```

*inside:* `data_metedata/meteo_observations/metadata_meteo.txt`

```
Meteorological observations are collected at two sites using tipping bucket rain gauges for wet weathr classification (MR3, METEOSERVIS v.o.s., catch area 500 c


Site_1 position (lattitude-longitude):;50.0302N;14.5291E;
```

