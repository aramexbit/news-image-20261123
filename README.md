[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/aramexbit/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/aramexbit/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)

# The World Herald — 23 November 2026

A one-page classic newspaper front page summing up the world news of
Monday 23 November 2026, built for the
[make.fun news-image-20261123 competition](https://make.fun/c/news-image-20261123).

The layout follows the winning pattern of the 19 November edition,
plus the winners' four edges: a THE DAY IN NUMBERS strip, four big
photographic leads, nine bigger medium grid stories, a world map with
numbered pins and a HOW TO READ box, and thirty-three one-line
briefs, with a THE DAY IN UTC strip, a region-count bar, and a DATE
CHECK footer. Forty-six stories in all, every one named with its
source.

The leads are the burning Strait of Hormuz (tankers struck over the
weekend, two more on fire after hitting mines, and Iranian drones sent
at US bases), the COP31 climate talks collapsing in Antalya over
fossil fuels, a Russian drone hitting an apartment block in Dymer
with eleven people missing, and Poland confirming the fallen objects
were Russian missiles, with NATO meeting on Monday. The grid carries
the Friday market plunge, sea drones hitting a Russian warship off
Libya, the capture of cartel boss Chapo Isidro, the Cikande factory
fire, South Korea's education minister quitting, 128 states backing
killer-robot rules, the UK hosting the 2035 Women's World Cup,
BepiColombo entering Mercury orbit, and Lahore's air at AQI 538.
Thirty-three one-line briefs below the map cover the rest of the
day, from Manipur to the Baltic, including eight from the afternoon:
NATO meeting on Poland, US futures rebounding, Zelenskyy vowing
retaliation, the UN chief on COP31, Hormuz shipping counts, Kyiv's
EUR 70bn aid need, the US intelligence chief on Putin, and two
tankers hitting mines off Ghannam.

All thirteen pictures on the page are generated press photographs; the
world map is a real one. Its source is the NASA Blue Marble Next
Generation world map with topography and bathymetry (August 2004,
3600x1800, equirectangular, produced by Reto Stoeckli, NASA Earth
Observatory) — NASA imagery is public domain — kept in its true
satellite colours (deep blue ocean, green and brown land, white polar
ice) and true equirectangular proportions (320x127 for lon -180..180,
lat 83..-60) by `tools/recolor_map.py` (v7; v6 flattened the same
source to one cream land colour and stretched it 1.58x vertically,
which read as a flat cartoon). The map is stored as
`assets/world-map.png`; the entry program only ever reads that PNG,
so the render needs no network. The six darkest grid photographs
were gamma-lifted in place by `tools/brighten_grid.py` (v6), and
Mercury's thumbnail focus was moved onto the lit planet, so every
grid thumbnail reads at its small size.

## How it runs

```sh
python3 main.py
```

`main.py` composes `entry.png` (1024x1024, under 1 MiB) through
`composer.py`. Where Pillow is unavailable it copies the prebuilt image
in `assets/` instead, so every run writes identical bytes. No network,
no clock, no randomness. Two runs produce byte-identical output, so
the grader's double run always matches.

## Verification

Two runs must write identical bytes:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
sha256sum out/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
sha256sum out/entry.png
```

The fallback path can be tested without Pillow:

```sh
MAKEFUN_FORCE_FALLBACK=1 MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Contents

- `main.py` — the entrypoint: composes the page, or copies the prebuilt
  image when Pillow is missing
- `composer.py` — the renderer: masthead, UTC strip, region bar, leads,
  grid, map (real NASA world map + numbered pins), briefs,
  DATE CHECK
- `stories.py` — the forty-six stories of 23 November 2026, each with
  its source (v9: four leads, nine grid, thirty-three briefs; the
  numbers strip figures are all taken from stories on the page)
- `assets/` — the prebuilt `entry.png`, the recolored world map
  (`world-map.png`) plus the thirteen press photographs
  (`photo-*.webp`) and their provenance in `photos.json`
- `tools/` — `recolor_map.py` (NASA map in true satellite colours and
  proportions) and `brighten_grid.py` (gamma lift for the darkest
  grid photos)
