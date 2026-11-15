# AraHaul link and weather

*Active approach: links built for the experiment* · `arahaul`

| | |
|---|---|
| Sensor | CML (research link) + weather |
| Region | Ames, Iowa, USA |
| Period | 4-5 Jul 2023 (link runs), 48 h weather |
| Resolution | 1 s |
| Content | one Aviat link at 11 and 80 GHz; RSL, SNR, modulation, capacity, BER at both ends; iperf/ping; Davis stations, Parsivel2 (raw size-velocity matrix), Lufft WS100 |
| Licence | CC BY 4.0 |
| Paper | Zu et al. (2023), IEEE FNWF, [doi:10.1109/FNWF58287.2023.10520543](https://doi.org/10.1109/FNWF58287.2023.10520543) |
| Data | [https://doi.org/10.21227/6ncx-rs20](https://doi.org/10.21227/6ncx-rs20) |

## Download (by hand)

No automatic download: IEEE DataPort needs a (free) IEEE account; download by hand into the data folder.

Page: <https://ieee-dataport.org/documents/arahaul-outdoor-wireless-backhaul-link-performance-weather-measurements>

Put the files in `$OISAC_DATA/arahaul/` (default `~/data/oisac-datasets/arahaul/`) and `python -m oisac_datasets describe arahaul` will describe them.

