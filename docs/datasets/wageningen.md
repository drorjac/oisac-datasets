# Wageningen campaign

*More open link datasets* · `wageningen`

| | |
|---|---|
| Sensor | CML (research links) |
| Region | Wageningen, the Netherlands |
| Period | Aug 2014 - Jan 2016 |
| Resolution | 20 Hz |
| Content | three co-located 2.2 km rooftop links (38 GHz ex-commercial, 26 and 38 GHz dual-pol. research); 5 disdrometers, gauge, scintillometer, cameras |
| Licence | CC0 |
| Paper | van Leth et al. (2018), AMT 11, 4645-4669, [doi:10.5194/amt-11-4645-2018](https://doi.org/10.5194/amt-11-4645-2018) |
| Data | [https://doi.org/10.4121/uuid:1dd45123-c732-4390-9fe4-6e09b578d4ff](https://doi.org/10.4121/uuid:1dd45123-c732-4390-9fe4-6e09b578d4ff) |

## Get it

```bash
python -m oisac_datasets fetch wageningen            # the small split below
python -m oisac_datasets fetch wageningen --all      # the whole record
```

Split: the three smallest files of the record (README and site file).

## Files in the record

| file | size |
|---|---:|
| `README.yaml` | 23.9 kB |
| `Wageningen Urban Rainfall experiment site.kml` | 1.5 kB |
| `data.zip` | 7.0 GB |
| **total** | **7.0 GB** |

## What the split holds

**`README.yaml`** (23.9 kB)

```
---
set_id: WURex14
description: |
    Data collected with collocated microwave (and optical) links and laser disdrometers from August 2014 untill January 2016 in the town of Wageningen. Transmit

    This dataset is formatted as an HDF5 file and was encoded using the h5py python library. Gaps in the data were filled up to get regular time series. Fill va
```

**`Wageningen Urban Rainfall experiment site.kml`** (1.5 kB)

```

<kml xmlns="http://www.opengis.net/kml/2.2">
                <Document>
                    <name>Wageningen Urban Rainfall experiment site</name>
                    <Placemark>
                        <name>Forum_2</name>
```

