# Sri Lanka CML rain maps

*Rain products from opportunistic sensors* · `srilanka`

| | |
|---|---|
| Sensor | CML product (maps) |
| Region | Sri Lanka |
| Period | Sep-Dec 2019 |
| Resolution | 15 min, 0.02 deg grid |
| Content | rainfall maps from the links; the link data themselves are not open |
| Licence | CC BY 4.0 |
| Paper | Overeem et al. (2021), ERL 16, 074058, [doi:10.1088/1748-9326/ac0fa6](https://doi.org/10.1088/1748-9326/ac0fa6) |
| Data | [https://doi.org/10.4121/14166539](https://doi.org/10.4121/14166539) |

## Get it

```bash
python -m oisac_datasets fetch srilanka            # the small split below
python -m oisac_datasets fetch srilanka --all      # the whole record
```

Split: the readme, the interpolation grid and the smallest map file.

## Files in the record

| file | size |
|---|---:|
| `CMLInterpolationGridSriLanka.dat` | 427.2 kB |
| `CMLRainMapsSriLanka15min.zip` | 420.4 MB |
| `readme.txt` | 5.0 kB |
| **total** | **420.8 MB** |

## What the split holds

**`CMLInterpolationGridSriLanka.dat`** (427.2 kB)

```
# Longitude[degrees],Latitude[degrees],ColumnNumber,RowNumber,CMLAntennaWithin5km[0=no;1=yes]
79.66,5.9,0,0,0
79.66,5.92,0,1,0
79.66,5.94,0,2,0
79.66,5.96,0,3,0
79.66,5.98,0,4,0
```

**`readme.txt`** (5.0 kB)

```
# Description:
Gridded dataset of rainfall intensities (mm/h) covering Sri Lanka over the period 12 September 2019 through 31 December 2019. Commercial microwave link (CML) da


# References

```

