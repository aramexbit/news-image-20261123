[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/aramexbit/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/aramexbit/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)

# The World Herald — 23 November 2026

A one-page classic newspaper front page summing up the world news of
Monday 23 November 2026, built for the
[make.fun news-image-20261123 competition](https://make.fun/c/news-image-20261123).

The layout follows the winning pattern of the 19 November edition:
three big photographic leads, ten medium grid stories, twenty-five
one-line briefs, a THE DAY IN UTC strip, a region-count bar, a world
map with numbered pins, and a DATE CHECK footer. Thirty-eight stories
in all, every one named with its source.

The leads are the burning Strait of Hormuz (tankers struck over the
weekend, two more on fire after hitting mines, and Iranian drones sent
at US bases in Kuwait and Bahrain), the COP31 climate talks collapsing
in Antalya over fossil fuels, and a Russian drone hitting an apartment
block in Dymer with eleven people missing. The grid carries Poland
confirming the fallen objects were Russian missiles, the Friday market
plunge, sea drones sinking a Russian warship off Libya, the capture of
cartel boss Chapo Isidro, the Cikande factory fire, South Korea's
education minister quitting, 128 states backing killer-robot rules,
the UK hosting the 2035 Women's World Cup, BepiColombo entering
Mercury orbit, and Lahore's air at AQI 538. Twenty-five one-line
briefs below the map cover the rest of the day, from Manipur to the
Baltic.

All thirteen pictures on the page are generated press photographs;
the world map is drawn from hand-written coastline polygons in lon/lat
(v4), projected equirectangular, so its continents are the real ones.

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
  grid, map (hand-written coastline polygons + numbered pins), briefs,
  DATE CHECK
- `stories.py` — the thirty-eight stories of 23 November 2026, each with
  its source
- `assets/` — the prebuilt `entry.png` plus the thirteen press
  photographs (`photo-*.webp`) and their provenance in `photos.json`
