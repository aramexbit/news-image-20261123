"""Brighten the too-dark grid photographs (v6 blind-test fix).

Build-time tool for THE WORLD HERALD (news-image-20261123 v6). The
blind test of v4 found the ten grid thumbnails thin and dark: the
markets screen (mean luminance 31) and the Cikande fire (35) read as
black strips, the stadium (60) nearly so, and the dusk scenes in
Mexico, Korea and Lahore (87-90) were hard to read at thumbnail size.
The three lead photographs are NOT touched.

Method: a gamma lift (shadows rise more than highlights, so flames and
floodlights do not blow out) plus a small brightness lift, applied with
PIL only. The factors below were set from the measured mean luminance
of each file (see the --check output). The files are rewritten in
place; keep a backup of the originals outside the repo before running.
Measured result (23 Nov 2026): markets 30.7 -> 65.4, Cikande
34.8 -> 76.3, stadium 59.9 -> 87.9, Mexico 87.1 -> 108.6, Korea
89.5 -> 107.8, Lahore 89.7 -> 111.6.

Mercury is deliberately left alone: it is a space photograph, and its
black sky is correct. Its thumbnail was dark because the crop missed
the planet, so v6 fixes it with a new focus point in composer.py
instead of brightening it.

Usage:
    python3 tools/brighten_grid.py --check      # measure only
    python3 tools/brighten_grid.py              # brighten in place
"""

import argparse
import os
import sys

from PIL import Image, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

# art -> (gamma, brightness): darker originals get a stronger lift.
BRIGHTEN = {
    "chart": (0.62, 1.18),    # markets screen, mean L 31
    "factory": (0.62, 1.18),  # Cikande fire at night, mean L 35
    "trophy": (0.75, 1.12),   # stadium at night, mean L 60
    "badge": (0.85, 1.08),    # Mexico at dusk, mean L 87
    "school": (0.85, 1.08),   # Korea exam hall, mean L 90
    "smog": (0.85, 1.08),     # Lahore smog, mean L 90
}

NAMES = {
    "chart": "photo-grid-markets.webp",
    "factory": "photo-grid-cikande.webp",
    "trophy": "photo-grid-stadium.webp",
    "badge": "photo-grid-mexico.webp",
    "school": "photo-grid-korea.webp",
    "smog": "photo-grid-lahore.webp",
}


def mean_luminance(img):
    """Mean grey level of the image, 0..255."""
    grey = img.convert("L")
    hist = grey.histogram()
    total = sum(hist)
    return sum(i * c for i, c in enumerate(hist)) / total


def gamma_lut(gamma):
    """Lookup table for the gamma lift: out = 255 * (in/255) ** gamma."""
    return [int(255 * (i / 255) ** gamma + 0.5) for i in range(256)]


def brighten(path, gamma, brightness):
    """Gamma-lift then brighten the file in place; returns (before, after)."""
    img = Image.open(path).convert("RGB")
    before = mean_luminance(img)
    # RGB needs one 256-entry table per channel: repeat the table 3x.
    img = img.point(gamma_lut(gamma) * 3)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img.save(path, format="WEBP", quality=90)
    after = mean_luminance(Image.open(path).convert("RGB"))
    return before, after


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="measure only, change nothing")
    args = parser.parse_args(argv)
    for art, (gamma, brightness) in BRIGHTEN.items():
        path = os.path.join(ASSETS, NAMES[art])
        if args.check:
            mean = mean_luminance(Image.open(path).convert("RGB"))
            print("%-8s mean L %.1f (gamma %.2f, brightness %.2f)"
                  % (art, mean, gamma, brightness))
        else:
            before, after = brighten(path, gamma, brightness)
            print("%-8s mean L %.1f -> %.1f (gamma %.2f, brightness %.2f)"
                  % (art, before, after, gamma, brightness))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
