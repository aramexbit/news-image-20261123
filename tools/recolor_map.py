"""Keep the real NASA Blue Marble colours for the front-page world map.

Build-time tool for THE WORLD HERALD (news-image-20261123 v7). It
turns the NASA Blue Marble Next Generation world map (public domain)
into the small map the front page pastes under WHERE IT HAPPENED —
with the satellite's own colours kept: deep blue ocean, green and
brown land, white ice, real texture. v6 flattened the same source
into one cream land colour and one pale-blue sea colour, and the map
read as a flat cartoon; v7 keeps the photograph.

Source (downloaded once, kept outside the repo in /tmp):
    NASA Blue Marble: Next Generation + topography + bathymetry,
    August 2004, 3600x1800 JPEG, equirectangular (Plate Carree),
    lon -180..180, lat 90..-90. Produced by Reto Stoeckli, NASA Earth
    Observatory (NASA Goddard Space Flight Center). NASA imagery is
    public domain; the same file is mirrored on Wikimedia Commons as
    "Blue Marble Next Generation + topography + bathymetry.jpg".
    Direct file: https://upload.wikimedia.org/wikipedia/commons/5/56/
    Blue_Marble_Next_Generation_%2B_topography_%2B_bathymetry.jpg
    The repo asset is the PNG this script writes
    (assets/world-map.png). The entry program only ever reads that
    PNG, so the render needs no network.

Method (no data file is read in: the picture itself is the map):
    1. Crop the latitude window lat 83..-60 — the same window the
       front-page pins use — so the picture and the pins share one
       equirectangular projection.
    2. Resize to the 432x172 map box with LANCZOS. 360 degrees of
       longitude over 143 degrees of latitude is an aspect of 2.52,
       and 432/172 is 2.51, so the continents keep their true
       proportions instead of the 1.58x vertical stretch of v6.
       (v11 widened the v7 box from 320x127; the stored asset was
       upscaled from that picture because the source was lost.)
    3. Light touches only, so it sits on newsprint without shouting:
       desaturate to 0.88, contrast 1.06, then blend 10% toward the
       paper colour. Land is never flattened to one colour.

Usage:
    python3 tools/recolor_map.py /tmp/bluemarble.jpg assets/world-map.png
"""

import hashlib
import sys

from PIL import Image, ImageEnhance

# Map box on the front page: lon -180..180, lat 83..-60, 432x172 px.
# True equirectangular aspect: 360/143 = 2.52; box aspect 432/172 =
# 2.51. v6 used 290x166 for 360x130 degrees (aspect 1.75 against a
# true 2.77), which stretched every continent 1.58x vertically. v11
# widens the v7 box (320x127) to 432x172 so the pins and the HOW TO
# READ text read neatly; the stored asset was upscaled from the
# 320x127 picture with LANCZOS because the 3600x1800 source was lost
# when /tmp was wiped — re-running this tool with a fresh source
# rebuilds the asset at the same 432x172 box.
MAP_W, MAP_H = 432, 172
LAT_N, LAT_S = 83, -60

PAPER = (248, 242, 227)


def natural_map(source, target):
    """Build the true-colour map PNG and return its stats."""
    img = Image.open(source).convert("RGB")
    width, height = img.size
    if width != 2 * height:
        raise SystemExit("source is not 2:1 equirectangular: %s" % (img.size,))
    # Latitude window of the front-page map box. lat 83..-60 keeps
    # Greenland and Svalbard in frame while cutting Antarctica (its
    # white mass would eat the bottom fifth of the box) and the empty
    # polar ocean above 83N, so the inhabited continents fill the box.
    y0 = int((90 - LAT_N) / 180 * height)
    y1 = int((90 - LAT_S) / 180 * height)
    img = img.crop((0, y0, width, y1)).resize((MAP_W, MAP_H), Image.LANCZOS)
    if img.size != (MAP_W, MAP_H):
        raise SystemExit("resized map is %s, the box is %s"
                         % (img.size, (MAP_W, MAP_H)))
    # Light touches only: a little less saturation, a little more
    # contrast, then a whisper of the paper colour so the satellite
    # photograph sits on the newsprint instead of shouting off it.
    img = ImageEnhance.Color(img).enhance(0.88)
    img = ImageEnhance.Contrast(img).enhance(1.06)
    paper = Image.new("RGB", (MAP_W, MAP_H), PAPER)
    img = Image.blend(img, paper, 0.10)
    img.save(target, format="PNG", optimize=True)
    with open(target, "rb") as fh:
        data = fh.read()
    px = list(img.getdata())
    n = len(px)
    mean = tuple(round(sum(c[i] for c in px) / n) for i in range(3))
    return {
        "target": target,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": (MAP_W, MAP_H),
        "mean_rgb": mean,
    }


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: recolor_map.py <source.jpg> <world-map.png>")
    info = natural_map(argv[1], argv[2])
    print(info)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
