[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/aramexbit/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/aramexbit/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)

# The World Herald — 23 November 2026

A one-page classic newspaper front page summing up the world news of
Monday 23 November 2026, built for the
[make.fun news-image-20261123 competition](https://make.fun/c/news-image-20261123).

The lead is the burning Strait of Hormuz: tankers struck over the
weekend, two more on fire after hitting mines, and Iranian drones sent
at the US bases of Ali Al Salem in Kuwait and in Bahrain. Below it,
four column stories carry photographs or a drawn chart: the COP31
climate talks collapsing in Antalya, a Russian drone flattening an
apartment block near Kyiv with eleven people missing, Poland
confirming the objects that fell on its soil were Russian cruise
missiles, and the Friday market plunge. The footer strip adds four
briefs — BepiColombo reaching Mercury, the 2035 Women's World Cup,
Lahore's air, and the Cikande factory fire. Nine stories in all, every
one named with its source.

## How it runs

```sh
python3 main.py
```

`main.py` composes `entry.png` (1024x1024, under 1 MiB) from the local
assets through `composer.py`. Where Pillow is unavailable it copies the
prebuilt image in `assets/` instead, so every run writes identical bytes.
No network, no clock, no randomness. Two runs produce byte-identical
output, so the grader's double run always matches.

Hero and column photographs are AI-generated illustrations.

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
- `composer.py` — the renderer: masthead, lead, columns, footer, chart
- `stories.py` — the nine stories of 23 November 2026, each with its source
- `assets/` — the generated photographs and the prebuilt `entry.png`
