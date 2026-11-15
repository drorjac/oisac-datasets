"""Figures for the README and the dataset pages.

    overview_map()   where every dataset is (world + Europe)
    timeline()       when each was recorded
    landscape()      sampling interval vs number of sensors
    quicklook(id)    a map and a time series from the downloaded split

All figures go to docs/fig/. Colours: one fixed categorical slot per catalogue group
(the reference palette of the dataviz method, in its fixed order), plus a marker shape
per group, so group identity never rests on colour alone.
"""
from __future__ import annotations

import glob
import gzip
import json
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import requests  # noqa: E402
import xarray as xr  # noqa: E402

from . import catalog  # noqa: E402
from .catalog import GROUPS, data_dir  # noqa: E402

warnings.filterwarnings("ignore")
FIG = catalog.ROOT / "docs" / "fig"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
GROUP_COLOR = dict(zip(GROUPS, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6"]))
GROUP_MARK = dict(zip(GROUPS, ["o", "s", "D", "^", "v", "P", "X"]))
SEQ = "Blues"  # magnitude: one hue, light to dark

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.titlecolor": INK, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "font.size": 9, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "lines.linewidth": 1.2, "font.family": "DejaVu Sans",
})


def _save(fig, name):
    p = FIG / name
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {p.relative_to(catalog.ROOT)}")
    return p


def _points(d):
    lat, lon = d.get("lat", None), d.get("lon", None)
    if lat in (None, ""):
        return []
    return list(zip(lat, lon)) if isinstance(lat, list) else [(lat, lon)]


# ------------------------------------------------------------------ base layers
def _land():
    cache = data_dir() / "_cache" / "ne_110m_land.geojson"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson"
        cache.write_bytes(requests.get(url, timeout=60).content)
    return json.loads(cache.read_text())


def _draw_land(ax):
    for f in _land()["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = np.asarray(poly[0])
            ax.fill(ring[:, 0], ring[:, 1], color="#ecebe7", ec="#d6d5d0", lw=0.4, zorder=0)


def _basemap(ax):
    """Light grey Esri tiles under a lon/lat axis; silently skipped offline."""
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(4))
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.tick_params(labelsize=7)
    try:
        import contextily as ctx
        ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.Esri.WorldGrayCanvas,
                        attribution_size=5, zorder=0)
    except Exception:  # noqa: BLE001
        pass


def _timeaxis(ax):
    import matplotlib.dates as mdates
    loc = mdates.AutoDateLocator(minticks=4, maxticks=8)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))


def _layout_map_ts2():
    """Map on the left over two rows; signal top right, reference bottom right."""
    fig = plt.figure(figsize=(12, 4.8))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.6], height_ratios=[2.2, 1], hspace=0.12, wspace=0.18)
    a = fig.add_subplot(gs[:, 0])
    b = fig.add_subplot(gs[0, 1])
    c = fig.add_subplot(gs[1, 1], sharex=b)
    plt.setp(b.get_xticklabels(), visible=False)
    return fig, a, b, c


def _links(ax, lon0, lat0, lon1, lat1, color="#2a78d6", lw=0.9, label=None):
    for i, (a, b, c, d) in enumerate(zip(lon0, lat0, lon1, lat1)):
        ax.plot([a, c], [b, d], color=color, lw=lw, solid_capstyle="round", label=label if i == 0 else None)


def _square(ax, lon, lat, pad=0.08):
    lon, lat = np.asarray(lon, float), np.asarray(lat, float)
    lon, lat = lon[np.isfinite(lon)], lat[np.isfinite(lat)]
    cx, cy = (lon.min() + lon.max()) / 2, (lat.min() + lat.max()) / 2
    k = np.cos(np.radians(cy))
    h = max(lat.max() - lat.min(), (lon.max() - lon.min()) * k) * (0.5 + pad) + 1e-3
    ax.set_xlim(cx - h / k, cx + h / k)
    ax.set_ylim(cy - h, cy + h)
    ax.set_aspect(1 / k)


# ------------------------------------------------------------------ overview figures
PLACES = [("Gothenburg", 57.70, 11.97), ("the Netherlands", 52.15, 5.1), ("Prague", 50.05, 14.5),
          ("Emilia-Romagna", 44.5, 11.0), ("Milan", 45.46, 9.19), ("southern France", 43.7, 5.0),
          ("Dubendorf", 47.40, 8.61), ("Germany", 51.0, 10.4), ("Czechia", 49.8, 15.5),
          ("southern Germany", 47.8, 11.5)]
PLACE_POS = {"Gothenburg": (4.5, 58.6, "left"), "the Netherlands": (-2.6, 54.2, "left"),
             "Prague": (15.6, 51.6, "left"), "Emilia-Romagna": (13.2, 43.0, "left"),
             "Milan": (3.0, 46.4, "left"), "southern France": (-2.6, 41.6, "left"),
             "Dubendorf": (-2.6, 48.6, "left"), "Germany": (12.6, 54.6, "left"), "Czechia": (16.4, 48.6, "left"),
             "southern Germany": (13.0, 45.7, "left")}


def _short(d):
    return SHORT.get(d.id, d.name.split(" (")[0])


SHORT = {"netherlands": "NL CML 2011-15", "nl_2011_12": "NL CML 2011-12", "radar_cml_merged": "radar+CML merged",
         "opera_netatmo": "OPERA + Netatmo (Europe)", "opensense_example": "OpenSense example data",
         "openmrg2_pws": "OpenMRG2 PWS", "prague_eband_link": "Prague E-band link", "germany_cml": "Germany CML (closed)",
         "israel_tau": "Israel CML (not open yet)", "rehovot_scwn": "Rehovot smart city (not open yet)",
         "telcorain_cz": "TelcoRain maps", "pycomlink_example": "pycomlink example", "rainlink_example": "RAINLINK example",
         "common_dubendorf": "CoMMon", "radarcnr": "RADARCNR", "wageningen": "Wageningen",
         "prague_collocated": "Prague collocated", "prague_eband": "Prague E-band", "amsterdam_pws": "Amsterdam PWS"}


def _frame(ax, box, title):
    x0, x1, y0, y1 = box
    _draw_land(ax)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect(1 / np.cos(np.radians((y0 + y1) / 2)))
    ax.set_title(title)
    ax.set_xticks([]), ax.set_yticks([])
    ax.grid(False)
    for sp in ax.spines.values():
        sp.set_color(GRID)


def _dots(ax, ds, box):
    x0, x1, y0, y1 = box
    for d in ds:
        for lat, lon in _points(d):
            if x0 <= lon <= x1 and y0 <= lat <= y1:
                ax.scatter(lon, lat, s=64, color=GROUP_COLOR[d.group], marker=GROUP_MARK[d.group],
                           ec=SURF, lw=1.5, zorder=3)


def overview_map():
    ds = catalog.load()
    fig = plt.figure(figsize=(14, 6.4))
    a = fig.add_axes([0.0, 0.12, 0.56, 0.8])
    b = fig.add_axes([0.58, 0.08, 0.42, 0.88])
    world, eu = (-115, 95, -12, 66), (-3, 21, 40, 60)
    _frame(a, world, "Where the datasets are")
    _frame(b, eu, "Europe (most of the open data)")
    _dots(a, ds, world)
    _dots(b, ds, eu)
    a.add_patch(plt.Rectangle((eu[0], eu[2]), eu[1] - eu[0], eu[3] - eu[2], fill=False, ec=INK2, lw=0.7, zorder=4))
    outside = {"New York": ("openmesh", "openmesh_v1", "cosmos", "opensense_example"), "Ames, Iowa": ("arahaul",),
               "Ouagadougou": ("ouagadougou",), "Sri Lanka": ("srilanka",), "Israel": ("israel_tau", "rehovot_scwn")}
    pos = {"New York": (-112, 52), "Ames, Iowa": (-112, 30), "Ouagadougou": (-40, 2), "Sri Lanka": (60, -5),
           "Israel": (45, 45)}
    names = {d.id: _short(d) for d in ds}
    names.update({"openmesh": "OpenMesh v2", "openmesh_v1": "OpenMesh v1", "cosmos": "COSMOS",
                  "opensense_example": "OpenSense example", "arahaul": "AraHaul", "ouagadougou": "CML rain maps",
                  "srilanka": "CML rain maps"})
    anchor = {"New York": (-73.95, 40.7), "Ames, Iowa": (-93.6, 42.0), "Ouagadougou": (-1.5, 12.4),
              "Sri Lanka": (80.7, 7.5), "Israel": (34.9, 31.6)}
    for place, ids in outside.items():
        txt = place + "\n" + "\n".join("  " + names[i] for i in ids)
        a.annotate(txt, anchor[place], pos[place], fontsize=7.5, color=INK2, va="center",
                   arrowprops=dict(arrowstyle="-", color=INK2, lw=0.5),
                   bbox=dict(boxstyle="round,pad=0.25", fc=SURF, ec=GRID, lw=0.5))
    # Europe: one stacked label per place
    groups = {p: [] for p, _, _ in PLACES}
    for d in ds:
        for lat, lon in _points(d):
            if not (eu[0] <= lon <= eu[1] and eu[2] <= lat <= eu[3]) or d.id == "opera_netatmo":
                continue
            p = min(PLACES, key=lambda pl: (pl[1] - lat) ** 2 + (pl[2] - lon) ** 2)
            if (p[1] - lat) ** 2 + (p[2] - lon) ** 2 < 2.5 and d.id not in groups[p[0]]:
                groups[p[0]].append(d.id)
    for p, lat, lon in PLACES:
        ids = groups[p]
        if not ids:
            continue
        x, y, ha = PLACE_POS[p]
        txt = p + "\n" + "\n".join("  " + names[i] for i in ids)
        b.annotate(txt, (lon, lat), (x, y), fontsize=7.2, color=INK2, va="center", ha=ha,
                   arrowprops=dict(arrowstyle="-", color=INK2, lw=0.5),
                   bbox=dict(boxstyle="round,pad=0.25", fc=SURF, ec=GRID, lw=0.5))
    b.text(eu[1] - 0.3, eu[2] + 0.4, "OPERA + Netatmo covers 78% of Europe", ha="right", fontsize=7, color=INK2)
    handles = [plt.Line2D([], [], marker=GROUP_MARK[g], color=GROUP_COLOR[g], ls="", ms=8, mec=SURF) for g in GROUPS]
    fig.legend(handles, list(GROUPS.values()), loc="lower left", ncol=2, fontsize=8.5, bbox_to_anchor=(0.01, 0.0))
    return _save(fig, "overview_map.png")


def _ym(s):
    return pd.Timestamp(str(s) + "-01") if s else None


def timeline():
    ds = [d for d in catalog.load() if d.get("start")]
    ds.sort(key=lambda d: (list(GROUPS).index(d.group), _ym(d.start)))
    fig, ax = plt.subplots(figsize=(10, 0.28 * len(ds) + 1.2))
    for i, d in enumerate(ds):
        a, b = _ym(d.start), _ym(d.end) + pd.offsets.MonthEnd(0)
        c = GROUP_COLOR[d.group]
        ax.barh(i, (b - a).days, left=a, height=0.62, color=c, ec=SURF, lw=0)
        ax.text(b + pd.Timedelta(days=40), i, d.get("resolution").split(",")[0].split(" (")[0],
                va="center", fontsize=7, color=INK2)
    ax.set_yticks(range(len(ds)), [d.name for d in ds], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(pd.Timestamp("2004-06-01"), pd.Timestamp("2028-06-01"))
    ax.grid(axis="y", visible=False)
    ax.set_title("When each dataset was recorded (label: sampling interval)")
    used = [g for g in GROUPS if any(d.group == g for d in ds)]
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=GROUP_COLOR[g]) for g in used], [GROUPS[g] for g in used],
              loc="upper center", bbox_to_anchor=(0.45, -0.06), fontsize=8, ncol=3)
    return _save(fig, "timeline.png")


def landscape():
    ds = [d for d in catalog.load() if d.get("res_s") and d.get("n")]
    fig, ax = plt.subplots(figsize=(8.5, 5.4))
    for d in ds:
        ax.scatter(d.res_s, d.n, s=70, color=GROUP_COLOR[d.group], marker=GROUP_MARK[d.group], ec=SURF, lw=1.5, zorder=3)
        dx, dy = LAND_OFF.get(d.id, (6, 4))
        ax.annotate(_short(d), (d.res_s, d.n), (dx, dy), textcoords="offset points", fontsize=7.5, color=INK2,
                    ha="right" if dx < 0 else "left")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ticks = [0.05, 1, 10, 60, 300, 900, 3600]
    ax.set_xticks(ticks, ["20 Hz", "1 s", "10 s", "1 min", "5 min", "15 min", "1 h"])
    ax.set_xlim(0.03, 9000)
    ax.set_ylim(0.6, 40000)
    ax.set_xlabel("sampling interval")
    ax.set_ylabel("number of sensors (links or stations)")
    ax.set_title("Few links sampled fast, or many links sampled slowly")
    used = [g for g in GROUPS if any(d.group == g for d in ds)]
    ax.legend([plt.Line2D([], [], marker=GROUP_MARK[g], color=GROUP_COLOR[g], ls="", ms=8, mec=SURF) for g in used],
              [GROUPS[g] for g in used], loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    return _save(fig, "landscape.png")


LAND_OFF = {"netherlands": (6, -9), "nl_2011_12": (6, 4), "opensat4weather": (6, 2), "openrainer": (6, -4),
            "openmesh_v1": (-6, -2), "pycomlink_example": (6, -8), "rehovot_scwn": (-6, 4), "common_dubendorf": (6, 6),
            "arahaul": (-6, 6), "wageningen": (6, 4), "prague_collocated": (6, -4), "openmrg2_pws": (6, 4),
            "openmesh": (6, 2), "amsterdam_pws": (6, 2)}


# ------------------------------------------------------------------ quicklooks
def _f(ds_id, pattern):
    hits = sorted(glob.glob(str(data_dir() / ds_id / "**" / pattern), recursive=True))
    if not hits:
        raise FileNotFoundError(f"{ds_id}: no {pattern} in the split; run `fetch {ds_id}` first")
    return hits[0]


def _wettest(da, dim="time"):
    """Index of the wettest step of a (cml or station x time) rain/attenuation field."""
    return int(np.nanargmax(np.asarray(da)))


def _cml_quicklook(d, path, s0="site_0", s1="site_1", title_ts=None, la="lat", lo="lon"):
    ds = xr.open_dataset(path)
    lat0, lon0 = ds[f"{s0}_{la}"].values, ds[f"{s0}_{lo}"].values
    lat1, lon1 = ds[f"{s1}_{la}"].values, ds[f"{s1}_{lo}"].values
    rsl = ds["rsl"]
    other = [x for x in rsl.dims if x not in ("time", "cml_id")]
    r = rsl.isel({other[0]: 0}) if other else rsl
    r = r.transpose("cml_id", "time")
    sm = r.rolling(time=max(3, r.sizes["time"] // 500), center=True).median()   # smooth out spikes
    base = sm.median("time")
    drop = (base - sm.min("time")).values                   # the deepest sustained fade
    drop[~np.isfinite(drop)] = -1
    drop[drop > 40] = -1                                    # skip outages
    k = int(np.argmax(drop))
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1, 1.6]})
    _links(a, lon0, lat0, lon1, lat1, color=GROUP_COLOR[d.group])
    _links(a, [lon0[k]], [lat0[k]], [lon1[k]], [lat1[k]], color=INK, lw=2.2)
    _square(a, np.r_[lon0, lon1], np.r_[lat0, lat1])
    _basemap(a)
    a.set_title(f"{ds.sizes['cml_id']} links (black: the one on the right)")
    a.tick_params(labelsize=7)
    t = pd.to_datetime(r["time"].values)
    b.plot(t, r.isel(cml_id=k).values, color=INK, lw=0.9)
    b.set_ylabel("RSL (dBm)")
    cid = ds["cml_id"].values[k]
    f = ds["frequency"].values
    fr = f[k] if f.ndim == 1 else np.nanmean(f[..., k]) if f.shape[-1] == len(lon0) else np.nanmean(f)
    fr = fr / 1000 if fr > 1000 else fr
    b.set_title(title_ts or f"Link {cid}: received signal level ({fr:.1f} GHz)")
    _timeaxis(b)
    ds.close()
    return fig


def _grid_sum_map(ax, lon, lat, total, label="rain total (mm)", cmap=SEQ):
    m = ax.pcolormesh(lon, lat, np.where(total > 0, total, np.nan), cmap=cmap, shading="auto", alpha=0.85, zorder=1)
    plt.colorbar(m, ax=ax, label=label, shrink=0.8)


def ql_openmrg(d):
    fig = _cml_quicklook(d, _f("openmrg", "openmrg_cml_8d.nc"))
    return fig


def ql_openrainer(d):
    return _cml_quicklook(d, _f("openrainer", "openrainer_cml_8d.nc"))


def ql_opensense_example(d):
    return _cml_quicklook(d, _f("opensense_example", "openmesh_cml_20d.nc"))


def ql_pycomlink_example(d):
    return _cml_quicklook(d, _f("pycomlink_example", "example_cml_data.nc"), "site_a", "site_b", la="latitude", lo="longitude")


def ql_netherlands(d):
    frames = [pd.read_csv(gzip.open(p, "rt")) for p in
              sorted(glob.glob(str(data_dir() / "netherlands" / "**" / "*.csv.gz"), recursive=True))]
    df = max(frames, key=len)
    for c in ["SITE_LAT_SECS", "SITE_LON_SECS", "FAR_END_LAT_SECS", "FAR_END_LON_SECS"]:
        df[c] = df[c] / 3.6e6
    meta = df.drop_duplicates("LINK_ID")
    df["t"] = pd.to_datetime(df["YYYYMMDDHHMMSS"].astype(str), format="%Y%m%d%H%M%S")
    ok = df[(df.RF_INPUT_LEVEL_MIN < -10) & (df.RF_INPUT_LEVEL_MIN > -95)]
    full = ok.groupby("LINK_ID").size()
    ok = ok[ok.LINK_ID.isin(full[full >= 0.9 * full.max()].index)]       # links reporting all day
    rng = ok.groupby("LINK_ID")["RF_INPUT_LEVEL_MIN"].agg(lambda s: s.median() - s.min())
    k = rng[rng < 35].idxmax()
    df = df[(df.RF_INPUT_LEVEL_MIN < -10) & (df.RF_INPUT_LEVEL_MIN > -95)]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1, 1.6]})
    _links(a, meta.SITE_LON_SECS, meta.SITE_LAT_SECS, meta.FAR_END_LON_SECS, meta.FAR_END_LAT_SECS,
           color=GROUP_COLOR[d.group], lw=0.5)
    m = meta[meta.LINK_ID == k].iloc[0]
    _links(a, [m.SITE_LON_SECS], [m.SITE_LAT_SECS], [m.FAR_END_LON_SECS], [m.FAR_END_LAT_SECS], color=INK, lw=2.2)
    _square(a, np.r_[meta.SITE_LON_SECS, meta.FAR_END_LON_SECS], np.r_[meta.SITE_LAT_SECS, meta.FAR_END_LAT_SECS])
    _basemap(a)
    a.set_title(f"{len(meta)} links, {df.t.dt.date.iloc[0]} (one daily file)")
    s = df[df.LINK_ID == k].sort_values("t")
    b.fill_between(s.t, s.RF_INPUT_LEVEL_MIN, s.RF_INPUT_LEVEL_MAX, step="mid", color=GROUP_COLOR[d.group], alpha=0.35, lw=0)
    b.step(s.t, s.RF_INPUT_LEVEL_MIN, where="mid", color=INK, lw=0.9, label="min")
    b.step(s.t, s.RF_INPUT_LEVEL_MAX, where="mid", color=INK2, lw=0.9, ls="--", label="max")
    b.set_ylabel("RSL (dBm)")
    b.legend(loc="lower left")
    b.set_title(f"Link {k}: 15-min min and max received level ({m.FREQ / 1e6:.1f} GHz)")
    _timeaxis(b)
    return fig


def ql_nl_2011_12(d):
    df = pd.read_csv(_f("nl_2011_12", "*.head"), sep=r"\s+")
    meta = df.drop_duplicates("ID")
    fig, a = plt.subplots(figsize=(6, 5.5))
    _links(a, meta.XStart, meta.YStart, meta.XEnd, meta.YEnd, color=GROUP_COLOR[d.group], lw=0.5)
    _square(a, np.r_[meta.XStart, meta.XEnd], np.r_[meta.YStart, meta.YEnd])
    _basemap(a)
    t = pd.to_datetime(df.DateTime.astype(str), format="%Y%m%d%H%M")
    a.set_title(f"{len(meta)} links in the first 5 MB ({t.min():%d %b %Y %H:%M} - {t.max():%H:%M})")
    return fig


def ql_opensat4weather(d):
    import zipfile
    import tempfile
    z = zipfile.ZipFile(_f("opensat4weather", "OpenSat4Weather_data.zip"))
    with tempfile.TemporaryDirectory() as td:
        for n in ("sml_data_2022.nc", "radar_along_sml_data_2022.nc"):
            z.extract(n, td)
        s = xr.open_dataset(Path(td) / "sml_data_2022.nc").load()
        r = xr.open_dataset(Path(td) / "radar_along_sml_data_2022.nc").load()
    tot = r.rainfall_amount.sum("time")
    k = int(np.argmax(tot.values))
    ev = r.rainfall_amount.isel(sml_id=k).rolling(time=12 * 24, center=True).sum()
    t0 = pd.Timestamp(ev.time.values[int(np.nanargmax(ev.values))])
    win = slice(t0 - pd.Timedelta("18h"), t0 + pd.Timedelta("18h"))
    fig, a, b, b2 = _layout_map_ts2()
    a.scatter(s.site_0_lon, s.site_0_lat, s=10, color=GROUP_COLOR[d.group], ec="none", zorder=2)
    a.scatter(s.site_0_lon[k], s.site_0_lat[k], s=50, color=INK, zorder=3)
    _square(a, s.site_0_lon.values, s.site_0_lat.values)
    _basemap(a)
    a.set_title(f"{s.sizes['sml_id']} satellite-link receivers (black: right)")
    b.plot(pd.to_datetime(s.time.sel(time=win).values), s.rsl.isel(sml_id=k).sel(time=win), color=INK, lw=0.8)
    b.set_ylabel("RSL (dBm)")
    rr = r.rainfall_amount.isel(sml_id=k).sel(time=win)
    b2.bar(pd.to_datetime(rr.time.values), rr.values, width=0.003, color=GROUP_COLOR[d.group])
    b2.set_ylabel("radar\n(mm / 5 min)", fontsize=8)
    b.set_title(f"Ku-band link {s.sml_id.values[k]}: the signal drops in rain, {t0:%d %b %Y}")
    _timeaxis(b2)
    return fig


def ql_amsterdam_pws(d):
    ds = xr.open_dataset(_f("amsterdam_pws", "ams_pws_full_period.nc")).load()
    daily = ds.rainfall.resample(time="1D").sum(min_count=200)
    day = daily.median("id").idxmax("time").values
    tot = daily.sel(time=day)
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1, 1.6]})
    m = a.scatter(ds.lon, ds.lat, c=tot, s=28, cmap=SEQ, ec=INK2, lw=0.3, zorder=2)
    plt.colorbar(m, ax=a, label="rain that day (mm)", shrink=0.8)
    _square(a, ds.lon.values, ds.lat.values)
    _basemap(a)
    a.set_title(f"{ds.sizes['id']} Netatmo stations, {pd.Timestamp(day):%d %b %Y}")
    win = ds.rainfall.sel(time=slice(pd.Timestamp(day), pd.Timestamp(day) + pd.Timedelta("1D"))).cumsum("time")
    t = pd.to_datetime(win.time.values)
    q = win.quantile([0.1, 0.5, 0.9], dim="id")
    b.fill_between(t, q.sel(quantile=0.1), q.sel(quantile=0.9), color=GROUP_COLOR[d.group], alpha=0.3, lw=0, label="10-90% of stations")
    b.plot(t, q.sel(quantile=0.5), color=INK, label="median station")
    b.set_ylabel("accumulated rain (mm)")
    b.legend(loc="upper left")
    b.set_title("The wettest day in the record, station by station")
    _timeaxis(b)
    return fig


def ql_openmesh(d):
    meta = pd.read_csv(_f("openmesh", "links_metadata.csv"))
    rad = xr.open_dataset(_f("openmesh", "openmesh_radar_rain_2023-11-22.nc"))
    tot = rad.rainfall_amount_1h.sum("time_1h")
    fig, a = plt.subplots(figsize=(7, 6))
    _grid_sum_map(a, rad.lon, rad.lat, tot.values, "MRMS rain, 22 Nov 2023 (mm)")
    for f, c in [(5, "#1baf7a"), (24, "#eb6834"), (60, "#6250d6")]:
        g = meta[(meta.frequency / 1000).round().between(f - 3, f + 15)]
        _links(a, g.site_0_lon, g.site_0_lat, g.site_1_lon, g.site_1_lat, color=c, lw=1.4, label=f"~{f} GHz")
    _square(a, np.r_[meta.site_0_lon, meta.site_1_lon], np.r_[meta.site_0_lat, meta.site_1_lat], pad=0.25)
    _basemap(a)
    a.legend(loc="upper left")
    a.set_title(f"NYC Mesh: {meta.cml_id.nunique()} links over a radar rain day")
    return fig


def ql_openmesh_v1(d):
    import zipfile
    z = zipfile.ZipFile(_f("openmesh_v1", "OpenMesh.zip"))
    meta = pd.read_csv(z.open("dataset/links/links_metadata.csv"))
    fig, a = plt.subplots(figsize=(6, 5.5))
    _links(a, meta.site_0_lon, meta.site_0_lat, meta.site_1_lon, meta.site_1_lat, color=GROUP_COLOR[d.group], lw=1.4)
    _square(a, np.r_[meta.site_0_lon, meta.site_1_lon], np.r_[meta.site_0_lat, meta.site_1_lat], pad=0.2)
    _basemap(a)
    a.set_title(f"OpenMesh v1: {meta.cml_id.nunique()} links")
    return fig


def ql_prague_eband(d):
    meta = pd.read_csv(_f("prague_eband", "metadata_table_commercial_microwave_links.csv"), sep=";")
    loss = pd.read_csv(_f("prague_eband", "1a.csv"), sep=";", parse_dates=["time"], na_values="NA").set_index("time")
    rain = pd.read_csv(_f("prague_eband", "site_1_rainfall_intensity.csv"), sep=";", parse_dates=[0], na_values="NA")
    rain = rain.set_index(rain.columns[0]).iloc[:, 0]
    day = rain.resample("1D").sum().idxmax()
    win = slice(day - pd.Timedelta("6h"), day + pd.Timedelta("30h"))
    fig, a, b, b2 = _layout_map_ts2()
    _links(a, meta.lonA, meta.latA, meta.lonB, meta.latB, color=GROUP_COLOR[d.group], lw=2)
    a.scatter(meta.lonA.iloc[0], meta.latA.iloc[0], s=40, color=INK, zorder=3)
    a.text(0.02, 0.02, "\n".join(f"link {m.id}: {m.length / 1000:.1f} km, {m.freqA} GHz" for _, m in meta.iterrows()),
           transform=a.transAxes, fontsize=7, color=INK2, va="bottom",
           bbox=dict(boxstyle="round,pad=0.3", fc=SURF, ec=GRID, lw=0.5), zorder=5)
    _square(a, np.r_[meta.lonA, meta.lonB], np.r_[meta.latA, meta.latB], pad=0.4)
    _basemap(a)
    a.set_title("Six E-band links from one hub")
    l = loss["total_loss"].loc[win]
    b.plot(l.index, l.values, color=INK, lw=0.8)
    b.set_ylabel("link 1a total loss (dB)")
    r = rain.loc[win]
    b2.fill_between(r.index, 0, r.values, color=GROUP_COLOR[d.group], lw=0, step="mid")
    b2.set_ylabel("gauge\n(mm/h)", fontsize=8)
    _timeaxis(b2)
    b.set_title(f"73.5 GHz, 4.9 km: loss follows the rain, {day:%d %b %Y}")
    return fig


def ql_ouagadougou(d):
    ds = xr.open_dataset(_f("ouagadougou", "CML_rainfall_maps_Ougadougou.nc"))
    tot = (ds.rain_rate.sum("time") * 5 / 60).values
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.8))
    _grid_sum_map(a, ds.longitude, ds.latitude, tot, "season total (mm)")
    _basemap(a)
    a.set_aspect(1 / np.cos(np.radians(12.36)))
    a.set_title("Rain from CMLs, 29 Jun - 10 Oct 2020")
    mean = ds.rain_rate.mean(["x", "y"])
    k = int(np.nanargmax(mean.values))
    one = ds.rain_rate.isel(time=k).values
    m = b.pcolormesh(ds.longitude, ds.latitude, np.where(one > 0.1, one, np.nan), cmap=SEQ, shading="auto", zorder=1)
    plt.colorbar(m, ax=b, label="rain rate (mm/h)", shrink=0.8)
    _basemap(b)
    b.set_aspect(1 / np.cos(np.radians(12.36)))
    b.set_title(f"One 5-min map: {pd.Timestamp(ds.time.values[k]):%d %b %Y %H:%M} UTC")
    return fig


def ql_radar_cml_merged(d):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    for ax, pat, name in zip(axs, ["OpenMRG_rainfall_add_IDW.nc", "OpenMRG_rainfall_pked.nc"],
                             ["additive IDW", "kriging with external drift"]):
        ds = xr.open_dataset(_f("radar_cml_merged", pat))
        tot = ds.rainfall.sum("time").values
        _grid_sum_map(ax, ds.lon, ds.lat, tot, "Jun-Aug 2015 total (mm)")
        _basemap(ax)
        ax.set_aspect(1 / np.cos(np.radians(57.7)))
        ax.set_title(f"OpenMRG radar + CMLs: {name}")
    return fig


def ql_opera_netatmo(d):
    import h5py
    f = h5py.File(_f("opera_netatmo", "*.h5"))
    x = f["dataset1/data1/data"][()].astype(float)
    x[x < 0] = np.nan
    fig, a = plt.subplots(figsize=(7, 7.5))
    m = a.imshow(np.where(x > 0.1, x, np.nan), cmap=SEQ, vmax=np.nanpercentile(x, 99.5), interpolation="nearest")
    a.imshow(np.where(np.isnan(x), 1.0, np.nan), cmap="Greys", vmin=0, vmax=4, interpolation="nearest")
    plt.colorbar(m, ax=a, label="1-h rain (mm)", shrink=0.7)
    a.set_xticks([]), a.set_yticks([])
    a.grid(False)
    a.set_title("OPERA + Netatmo, 13 Apr 2020 06-07 UTC (grey: no radar)")
    return fig


def ql_telcorain_cz(d):
    from PIL import Image
    files = sorted(glob.glob(str(data_dir() / "telcorain_cz" / "**" / "*.png"), recursive=True))
    pick = files[:: max(1, len(files) // 6)][:6]
    fig, axs = plt.subplots(2, 3, figsize=(12, 5.4))
    for ax, p in zip(axs.flat, pick):
        ax.imshow(Image.open(p))
        n = Path(p).stem.split("_")
        ax.set_title(f"{n[0]} {n[1][:2]}:{n[1][2:]} UTC  (median {float(n[2]):.2f} mm/h)", fontsize=8, fontweight="normal")
        ax.axis("off")
    fig.suptitle("TelcoRain: CML rain over Czechia, 21 July 2025", x=0.02, ha="left", fontweight="bold")
    return fig


QUICKLOOKS = {k[3:]: v for k, v in globals().items() if k.startswith("ql_")}


def quicklook(ds_id):
    d = catalog.get(ds_id)
    fig = QUICKLOOKS[ds_id](d)
    return _save(fig, f"datasets/{ds_id}.png")


def all_figures():
    overview_map()
    timeline()
    landscape()
    for k in QUICKLOOKS:
        try:
            quicklook(k)
        except Exception as e:  # noqa: BLE001
            print(f"skip {k}: {e}")
