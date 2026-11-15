# RADARCNR (Milan)

*Simulations and method data* · `radarcnr`

| | |
|---|---|
| Sensor | radar + CML configuration |
| Region | Milan, Italy |
| Period | rain events |
| Resolution | radar scans |
| Content | weather radar data and the configuration of a terrestrial CML network, with MATLAB code for tomographic 2-D rain field reconstruction |
| Licence | CC BY 4.0 |
| Paper | D'Amico et al., AMT (tomographic reconstruction from CMLs) |
| Data | [https://doi.org/10.5281/zenodo.3975497](https://doi.org/10.5281/zenodo.3975497) |

## Get it

```bash
python -m oisac_datasets fetch radarcnr            # the small split below
python -m oisac_datasets fetch radarcnr --all      # the whole record
```

Split: the whole record (0.6 MB). Note that the zip on Zenodo is AES-encrypted (checked Nov 2026), so its files cannot be opened without a password from the authors.

## Files in the record

| file | size |
|---|---:|
| `radarCNR.zip` | 620.3 kB |
| **total** | **620.3 kB** |

## What the split holds

**`radarCNR.zip`** (620.3 kB)

- 5 files, 4.3 MB unpacked; 2 x .m, 1 x .txt, 1 x (none), 1 x .docx
- `readnpc2.m` (7.6 kB)
- `link_cfg1.txt` (2.2 kB)
- `npcpar.m` (6.2 kB)
- `NPC380` (4.2 MB)
- `readme.docx` (18.6 kB)

- (the zip members are password-protected; they cannot be previewed)

