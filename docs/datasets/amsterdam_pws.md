# Amsterdam PWS

*The six networks of the lecture* · `amsterdam_pws`

| | |
|---|---|
| Sensor | PWS |
| Region | Amsterdam, the Netherlands |
| Period | May 2016 - May 2018 |
| Resolution | 5 min |
| Content | 134 Netatmo personal weather stations; KNMI gauge-adjusted radar at the station points |
| Operator / source | Netatmo (citizens) |
| Licence | CC BY 4.0 |
| Paper | de Vos et al. (2019), GRL 46, 8820-8829, [doi:10.1029/2019GL083731](https://doi.org/10.1029/2019GL083731) |
| Data | [https://doi.org/10.4121/uuid:6e6a9788-49fc-4635-a43d-a2fa164d37ec](https://doi.org/10.4121/uuid:6e6a9788-49fc-4635-a43d-a2fa164d37ec) |

## Get it

```bash
python -m oisac_datasets fetch amsterdam_pws            # the small split below
python -m oisac_datasets fetch amsterdam_pws --all      # the whole record
```

Split: the full period in the OpenSense format (6 MB).

## Files in the record

| file | size |
|---|---:|
| `Amsterdam metropolitan area.kml` | 593 B |
| `data.zip` | 7.6 MB |
| **total** | **7.6 MB** |

## What the split holds

**`example/ams_gauges_full_period.nc`** (293.4 kB)

- dims: id=20, time=18263
- time: 2016-05-01T01:00:00 .. 2018-05-31T23:00:00
- `rainfall` ('id', 'time') mm - rainfall amount per time unit
- coords: elevation, lat, lon

**`example/ams_pws_full_period.nc`** (5.8 MB)

- dims: id=134, time=219168
- time: 2016-05-01T00:05:00 .. 2018-06-01T00:00:00
- `rainfall` ('id', 'time') mm - rainfall amount per time unit
- coords: elevation, lat, lon

