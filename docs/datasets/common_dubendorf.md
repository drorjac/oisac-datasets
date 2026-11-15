# CoMMon (Dubendorf)

*More open link datasets* · `common_dubendorf`

| | |
|---|---|
| Sensor | CML (dual-pol.) |
| Region | Dubendorf, Switzerland |
| Period | Mar 2011 - Mar 2012 |
| Resolution | 4 s |
| Content | one 1.85 km dual-polarised 38 GHz link, radomes shielded at times (wet antenna); 5 disdrometers, 3 gauges |
| Licence | CC BY 4.0 |
| Paper | Spackova et al. (2021), ESSD |
| Data | [https://doi.org/10.5281/zenodo.4923125](https://doi.org/10.5281/zenodo.4923125) |

## Get it

```bash
python -m oisac_datasets fetch common_dubendorf            # the small split below
python -m oisac_datasets fetch common_dubendorf --all      # the whole record
```

Split: the readme, the site file and the record's own one-day example.

## Files in the record

| file | size |
|---|---:|
| `Metadata_sheets.pdf` | 1.6 MB |
| `Documentation.zip` | 781.8 kB |
| `Sites.kml` | 2.7 kB |
| `Common_dataset.zip` | 342.9 MB |
| `Readme.txt` | 8.6 kB |
| `HTML_viewer.zip` | 182.4 MB |
| `Data_example_of_one_day.zip` | 1.1 MB |
| **total** | **528.8 MB** |

## What the split holds

**`Data_example_of_one_day.zip`** (1.1 MB)

- 14 files, 72.0 MB unpacked; 14 x .dat
- `Data_example_of_one_day/20_ascii_20110427.dat` (14.0 MB)
- `Data_example_of_one_day/21_ascii_20110427.dat` (14.0 MB)
- `Data_example_of_one_day/22_ascii_20110427.dat` (14.0 MB)
- `Data_example_of_one_day/40_ascii_20110427.dat` (14.0 MB)
- `Data_example_of_one_day/41_ascii_20110427.dat` (14.0 MB)
- `Data_example_of_one_day/Affoltern_2011-04-27.dat` (12.0 kB)
- `Data_example_of_one_day/CML_20110427.dat` (1.6 MB)
- `Data_example_of_one_day/Fluntern_2011-04-27.dat` (12.0 kB)
- `Data_example_of_one_day/Kloten_2011-04-27.dat` (12.0 kB)
- `Data_example_of_one_day/RG02_2011-04-27.dat` (49.1 kB)
- `Data_example_of_one_day/RG03_2011-04-27.dat` (48.2 kB)
- `Data_example_of_one_day/RG04_2011-04-27.dat` (49.1 kB)
- ... 2 more

**`Readme.txt`** (8.6 kB)

```
Common dataset

A data paper, by Špačková, A., Bareš, V., Fencl, M., Schleiss, M., Jaffrain, J., Berne, A., and Rieckermann, J. entitled “One year of attenuation data from a co

Measurement campaign:
	- 9 March 2011 - 21 March 2012; Dübendorf, Switzerland
```

**`Sites.kml`** (2.7 kB)

```
<?xml version="1.0" encoding="utf-8" ?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document id="root_doc">
<Schema name="altitude" id="altitude">
	<SimpleField name="site" type="int"></SimpleField>
	<SimpleField name="altitude" type="string"></SimpleField>
```

