# RAINLINK example data

*Example data shipped with software* · `rainlink_example`

| | |
|---|---|
| Sensor | CML |
| Region | the Netherlands |
| Period | example days |
| Resolution | 15 min (min/max RSL) |
| Content | the Dutch example link data (R data file) and interpolation grid that come with RAINLINK |
| Licence | GPL-3 (RAINLINK package) |
| Paper | Overeem et al. (2016), AMT 9, 2425-2444, [doi:10.5194/amt-9-2425-2016](https://doi.org/10.5194/amt-9-2425-2016) |
| Data | [https://github.com/overeem11/RAINLINK](https://github.com/overeem11/RAINLINK) |

## Get it

```bash
python -m oisac_datasets fetch rainlink_example            # the small split below
python -m oisac_datasets fetch rainlink_example --all      # the whole record
```

Split: the example link data (R format) and the interpolation grid.

Source: <https://github.com/overeem11/RAINLINK>

## What the split holds

**`example/InterpolationGrid.dat`** (524.3 kB)

```
"X","Y"
6.471,53.555
6.485,53.554
6.455,53.547
6.469,53.546
6.484,53.546
```

**`example/Linkdata.RData`** (6.2 MB)

