"""Recolor a real equirectangular world map into the page palette.

Build-time tool for THE WORLD HERALD (news-image-20261123 v6). It turns
the NASA Blue Marble Next Generation world map (public domain) into the
small flat-colour map the front page pastes under WHERE IT HAPPENED.

Source (downloaded once, kept outside the repo):
    NASA Blue Marble: Next Generation + topography + bathymetry,
    August 2004, 3600x1800 JPEG, equirectangular (Plate Carree),
    lon -180..180, lat 90..-90. Produced by Reto Stoeckli, NASA Earth
    Observatory (NASA Goddard Space Flight Center). NASA imagery is
    public domain; the same file is mirrored on Wikimedia Commons as
    "Blue Marble Next Generation + topography + bathymetry.jpg".
    Direct file: https://upload.wikimedia.org/wikipedia/commons/5/56/
    Blue_Marble_Next_Generation_%2B_topography_%2B_bathymetry.jpg
    The source is a JPEG; the repo asset is the recolored PNG this
    script writes (assets/world-map.png). The entry program only ever
    reads that PNG, so the render needs no network.

Method (no data file is read in: the land/ocean split is computed here
from the picture itself):
    1. A pixel is ocean when its blue channel beats red by more than 12
       and green by more than 8. Deep ocean, shallow turquoise water and
       the Persian Gulf all pass; green forest, tan desert, brown rock
       and white ice all fail, so they read as land.
    2. A 3x3 median filter clears single-pixel speckle (JPEG noise and
       tiny islands too small to draw).
    3. The latitude window lat 75..-55 is cropped (the same window the
       front page pins use), then the mask is resized to the 290x166 map
       box with LANCZOS, which anti-aliases the coastlines.
    4. Land is painted cream (250, 244, 228), ocean pale blue
       (214, 226, 232), and the one-pixel coastline edge is painted a
       muted tan (150, 140, 120), all in the page palette.

Usage:
    python3 tools/recolor_map.py /tmp/bluemarble.jpg assets/world-map.png
"""

import hashlib
import sys

from PIL import Image, ImageChops, ImageFilter

# Map box on the front page: lon -180..180, lat 75..-55, 290x166 px.
MAP_W, MAP_H = 290, 166
LAT_N, LAT_S = 75, -55

OCEAN = (214, 226, 232)
LAND = (250, 244, 228)
COAST = (150, 140, 120)


def ocean_mask(img):
    """Binary mask (255 = ocean) from the blue-dominance test."""
    r, g, b = img.split()
    over_red = ImageChops.subtract(b, r).point(lambda v: 255 if v > 12 else 0)
    over_green = ImageChops.subtract(b, g).point(lambda v: 255 if v > 8 else 0)
    ocean = ImageChops.multiply(over_red, over_green)
    return ocean.filter(ImageFilter.MedianFilter(3))


def recolor(source, target):
    """Build the flat-colour map PNG and return its stats."""
    img = Image.open(source).convert("RGB")
    width, height = img.size
    if width != 2 * height:
        raise SystemExit("source is not 2:1 equirectangular: %s" % (img.size,))
    land = ImageChops.invert(ocean_mask(img))
    # Latitude window of the front-page map box.
    y0 = int((90 - LAT_N) / 180 * height)
    y1 = int((90 - LAT_S) / 180 * height)
    land = land.crop((0, y0, width, y1)).resize((MAP_W, MAP_H), Image.LANCZOS)
    ocean_img = Image.new("RGB", (MAP_W, MAP_H), OCEAN)
    land_img = Image.new("RGB", (MAP_W, MAP_H), LAND)
    page = Image.composite(land_img, ocean_img, land)
    # Coastline: land pixels next to ocean, painted muted tan.
    eroded = land.filter(ImageFilter.MinFilter(3))
    edge = ImageChops.subtract(land, eroded)
    coast_img = Image.new("RGB", (MAP_W, MAP_H), COAST)
    page = Image.composite(coast_img, page, edge)
    page.save(target, format="PNG", optimize=True)
    hist = land.histogram()
    total = sum(hist)
    land_frac = sum(hist[128:]) / total
    with open(target, "rb") as fh:
        data = fh.read()
    return {
        "target": target,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "land_fraction": round(land_frac, 3),
    }


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: recolor_map.py <source.jpg> <world-map.png>")
    info = recolor(argv[1], argv[2])
    print(info)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
