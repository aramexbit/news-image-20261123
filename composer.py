"""Render THE WORLD HERALD v3, the one-page front page for 23 Nov 2026.

Follows the winning pattern of the 19 November edition: masthead with a
big date, a THE DAY IN UTC strip, a region-count bar, three big leads
with press photographs, ten medium grid stories, a world map with
numbered pins, twenty-five one-line briefs, and a DATE CHECK footer.
The map is drawn from hand-written coastline polygons in lon/lat
(v4), projected equirectangular, so its continents are the real ones.

Thirty-eight stories in all, every one named with its source, from the
stories in stories.py. All thirteen pictures are generated press
photographs, cropped into their boxes; the world map stays a drawn
diagram. No network, no clock, no randomness except a fixed-seed
grain, so two runs write identical bytes.

The page is saved as PNG; when the PNG would pass the 1 MiB gate it is
saved as JPEG instead (the file keeps the name entry.png either way).
"""

import hashlib
import io
import os
import random

from PIL import Image, ImageDraw, ImageFont

import stories

W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN
MAX_BYTES = 1048576

PAPER = (248, 242, 227)
PAPER_DARK = (238, 231, 212)
PAPER_LIGHT = (251, 246, 233)
INK = (20, 18, 16)
RED = (163, 30, 30)
GREY = (107, 101, 90)
RULE = (20, 18, 16)
LIGHT_RULE = (178, 170, 150)
PANEL = (255, 253, 246)
OCEAN = (214, 226, 232)
LAND = (250, 244, 228)
SKY = (233, 230, 212)
SEA = (38, 68, 96)

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")

_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
]
_SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
]
_SERIF_ITALIC = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf",
]
_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
]
_SANS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
]

_FONT_CACHE = {}


def font(kind, size):
    """First usable face for the kind, cached; bitmap fallback last."""
    key = (kind, size)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    paths = {
        "serif_bold": _SERIF_BOLD,
        "serif": _SERIF,
        "serif_italic": _SERIF_ITALIC,
        "sans_bold": _SANS_BOLD,
        "sans": _SANS,
    }[kind]
    face = None
    for path in paths:
        if os.path.exists(path):
            try:
                face = ImageFont.truetype(path, size)
                break
            except OSError:
                continue
    if face is None:
        face = ImageFont.load_default()
    _FONT_CACHE[key] = face
    return face


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit the width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top to bottom; returns the y below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_lines(draw, text, kind, size, width, max_lines, min_size=12):
    """Wrap the text, shrinking the face until it fits max_lines."""
    size_now = size
    while size_now > min_size:
        fnt = font(kind, size_now)
        lines = wrap(draw, text, fnt, width)
        if len(lines) <= max_lines:
            return fnt, lines
        size_now -= 1
    fnt = font(kind, min_size)
    return fnt, wrap(draw, text, fnt, width)[:max_lines]


def grain(img):
    """Fixed-seed newsprint speckle; deterministic across runs."""
    rng = random.Random(20261123)
    px = img.load()
    for _ in range(1400):
        x = rng.randrange(W)
        y = rng.randrange(H)
        px[x, y] = PAPER_DARK if rng.random() < 0.5 else PAPER_LIGHT
    return img


def rule(draw, y, weight=1, x0=None, x1=None):
    """A horizontal rule across the content width."""
    draw.line([x0 or MARGIN, y, x1 or (W - MARGIN), y], fill=RULE, width=weight)
    return y + weight


# ---------------------------------------------------------------------------
# Press photographs. Each art function takes (draw, x, y, w, h) and pastes
# a generated photojournalistic photo into the box, cropped to the box
# aspect around a focus point. No text inside any photo; the layout
# carries every headline and caption.
# ---------------------------------------------------------------------------

PHOTO_FILES = {
    "tanker": "photo-hero-hormuz.webp",
    "cop": "photo-hero-cop31.webp",
    "block": "photo-hero-dymer.webp",
    "missile": "photo-grid-poland.webp",
    "chart": "photo-grid-markets.webp",
    "ship": "photo-grid-libya.webp",
    "badge": "photo-grid-mexico.webp",
    "factory": "photo-grid-cikande.webp",
    "school": "photo-grid-korea.webp",
    "globe": "photo-grid-geneva.webp",
    "trophy": "photo-grid-stadium.webp",
    "mercury": "photo-grid-mercury.webp",
    "smog": "photo-grid-lahore.webp",
}

# Focus point (fx, fy) of each photo, 0..1: where the crop is centred.
PHOTO_FOCUS = {
    "tanker": (0.5, 0.68),
    "cop": (0.5, 0.62),
    "block": (0.5, 0.5),
    "missile": (0.5, 0.5),
    "chart": (0.5, 0.4),
    "ship": (0.5, 0.5),
    "badge": (0.5, 0.6),
    "factory": (0.5, 0.5),
    "school": (0.5, 0.5),
    "globe": (0.5, 0.55),
    "trophy": (0.5, 0.5),
    "mercury": (0.4, 0.5),
    "smog": (0.5, 0.5),
}

_PHOTO_CACHE = {}
_PAGE = None  # the page image, set by render(); photo() pastes into it.


def photo(name, x, y, w, h):
    """Paste the photo for `name` into the (x, y, w, h) box, cropped."""
    key = (name, w, h)
    if key not in _PHOTO_CACHE:
        src = Image.open(os.path.join(ASSETS, PHOTO_FILES[name]))
        src = src.convert("RGB")
        sw, sh = src.size
        fx, fy = PHOTO_FOCUS[name]
        target = w / h
        if sw / sh > target:
            cw = int(sh * target)
            cx = min(max(int((sw - cw) * fx), 0), sw - cw)
            box = (cx, 0, cx + cw, sh)
        else:
            ch = int(sw / target)
            cy = min(max(int((sh - ch) * fy), 0), sh - ch)
            box = (0, cy, sw, cy + ch)
        _PHOTO_CACHE[key] = src.crop(box).resize((w, h), Image.LANCZOS)
    _PAGE.paste(_PHOTO_CACHE[key], (x, y))


def art_tanker(draw, x, y, w, h):
    """A burning tanker in the strait, photographed at dusk."""
    photo("tanker", x, y, w, h)


def art_cop(draw, x, y, w, h):
    """A climate conference plenary hall, photographed."""
    photo("cop", x, y, w, h)


def art_block(draw, x, y, w, h):
    """A damaged apartment block, photographed with rescuers."""
    photo("block", x, y, w, h)


def art_missile(draw, x, y, w, h):
    """A smoking impact crater in a Polish field, photographed."""
    photo("missile", x, y, w, h)


def art_chart(draw, x, y, w, h):
    """A trading screen glowing red with the plunge, photographed."""
    photo("chart", x, y, w, h)


def art_ship(draw, x, y, w, h):
    """A warship listing in harbour, photographed."""
    photo("ship", x, y, w, h)


def art_badge(draw, x, y, w, h):
    """A cartel arrest at dusk, photographed from behind."""
    photo("badge", x, y, w, h)


def art_factory(draw, x, y, w, h):
    """A factory on fire at night, photographed."""
    photo("factory", x, y, w, h)


def art_school(draw, x, y, w, h):
    """An examination hall, photographed from the back."""
    photo("school", x, y, w, h)


def art_globe(draw, x, y, w, h):
    """A United Nations assembly hall, photographed."""
    photo("globe", x, y, w, h)


def art_trophy(draw, x, y, w, h):
    """A football stadium under floodlights, photographed."""
    photo("trophy", x, y, w, h)


def art_mercury(draw, x, y, w, h):
    """Mercury and a probe, photographed in space."""
    photo("mercury", x, y, w, h)


def art_smog(draw, x, y, w, h):
    """A city skyline under smog, photographed."""
    photo("smog", x, y, w, h)


ART = {
    "tanker": art_tanker,
    "cop": art_cop,
    "block": art_block,
    "missile": art_missile,
    "chart": art_chart,
    "ship": art_ship,
    "badge": art_badge,
    "factory": art_factory,
    "school": art_school,
    "globe": art_globe,
    "trophy": art_trophy,
    "mercury": art_mercury,
    "smog": art_smog,
}

# World map, in a 290 x 166 box: lon -170..190, lat 75..-55,
# equirectangular. Every coastline below is hand-written from the real
# geography -- each continent keeps its true shape and place, so the
# map reads as Earth, not blobs: North America with Florida, Baja and
# the Hudson Bay notch; South America wide in the north, tapering
# south; Europe with Iberia, the Italy boot and Greece; Africa as a
# triangle with the Horn; Asia with Kamchatka, Korea, the Malay
# peninsula, India and Arabia; Australia in its own shape; plus the
# larger islands (UK, Ireland, Iceland, Japan, Madagascar, New
# Zealand, Borneo, Sumatra, Java, New Guinea, the Philippines).
MAP_W, MAP_H = 290, 166
MAP_LON_W, MAP_LON_E = -170, 190
MAP_LAT_N, MAP_LAT_S = 75, -55


def lonlat_to_xy(lon, lat):
    """Equirectangular projection of (lon, lat) into the map box."""
    x = (lon - MAP_LON_W) / (MAP_LON_E - MAP_LON_W) * MAP_W
    y = (MAP_LAT_N - lat) / (MAP_LAT_N - MAP_LAT_S) * MAP_H
    return (round(x), round(y))


CONTINENTS_LONLAT = [
    # North America.
    [(-168, 66), (-160, 58), (-148, 60), (-126, 49), (-124, 41),
     (-120, 34), (-113, 28), (-109, 23), (-104, 20), (-96, 19),
     (-90, 20), (-86, 22), (-83, 29), (-81, 26), (-79, 33), (-71, 42),
     (-67, 45), (-62, 46), (-56, 50), (-66, 60), (-76, 63), (-86, 66),
     (-95, 69), (-122, 70), (-138, 70), (-153, 71), (-165, 69)],
    # Greenland.
    [(-55, 60), (-42, 60), (-32, 68), (-22, 72), (-28, 77), (-45, 77),
     (-56, 74), (-58, 68)],
    # South America.
    [(-77, 7), (-71, 12), (-60, 8), (-51, 4), (-43, -3), (-35, -8),
     (-40, -20), (-48, -28), (-57, -38), (-65, -45), (-69, -52),
     (-73, -50), (-73, -38), (-71, -25), (-76, -13), (-80, -4)],
    # Europe.
    [(-6, 36), (-9, 38), (-9, 43), (-3, 44), (-5, 48), (4, 53),
     (8, 56), (17, 61), (21, 65), (26, 69), (29, 71), (31, 68),
     (23, 52), (25, 46), (34, 41), (36, 38), (30, 36), (26, 38),
     (23, 37), (20, 40), (19, 44), (17, 42), (18, 40), (16, 38),
     (13, 42), (8, 44), (3, 43), (0, 39), (-2, 37)],
    # United Kingdom.
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 52), (0, 50)],
    # Ireland.
    [(-10, 52), (-9, 55), (-6, 55), (-6, 52)],
    # Iceland.
    [(-22, 64), (-17, 64), (-14, 65), (-16, 66), (-21, 66), (-24, 65)],
    # Africa.
    [(-6, 35), (-10, 31), (-17, 20), (-16, 14), (-7, 5), (6, 4), (9, 4),
     (13, -8), (15, -24), (18, -32), (20, -35), (32, -28), (40, -15),
     (40, -8), (48, 2), (51, 10), (43, 12), (39, 16), (34, 27), (32, 31),
     (19, 33), (12, 34), (10, 37), (-2, 35)],
    # Asia.
    [(28, 41), (51, 47), (68, 62), (75, 71), (95, 76), (112, 74),
     (135, 72), (158, 70), (173, 67), (178, 65), (164, 56), (150, 59),
     (139, 48), (129, 41), (127, 39), (126, 36), (124, 33), (117, 25),
     (109, 19), (104, 10), (100, 4), (89, 22), (81, 15), (76, 8),
     (71, 20), (63, 25), (53, 17), (45, 13), (35, 28), (31, 34)],
    # Sumatra.
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5),
     (100, -1), (97, 3)],
    # Borneo.
    [(109, 1), (113, 4), (117, 6), (119, 2), (117, -2), (113, -3),
     (109, -1)],
    # Java.
    [(105, -6), (110, -7), (114, -8), (112, -8), (107, -7)],
    # New Guinea.
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9),
     (142, -8), (137, -6), (132, -4)],
    # Philippines.
    [(120, 14), (122, 16), (122, 18), (120, 18), (119, 15)],
    # Japan.
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 40),
     (142, 43), (140, 44)],
    # Madagascar.
    [(44, -16), (47, -15), (50, -17), (49, -21), (46, -25), (44, -24),
     (43, -20), (43, -17)],
    # Australia.
    [(113, -22), (115, -32), (118, -35), (125, -33), (132, -32),
     (137, -35), (140, -38), (146, -39), (150, -37), (153, -31),
     (153, -27), (149, -22), (146, -19), (142, -11), (140, -17),
     (136, -15), (132, -12), (127, -14), (122, -17), (116, -20)],
    # Tasmania.
    [(145, -41), (148, -42), (148, -44), (146, -43), (144, -41)],
    # New Zealand.
    [(167, -45), (171, -43), (174, -41), (176, -38), (178, -38),
     (175, -40), (171, -43), (168, -46)],
    # Sri Lanka.
    [(80, 6), (81, 8), (80, 10), (79, 8)],
    # Taiwan.
    [(120, 22), (121, 24), (121, 25), (120, 23)],
    # Cuba.
    [(-85, 22), (-80, 23), (-75, 21), (-74, 20), (-78, 21), (-83, 22)],
]
CONTINENTS = [[lonlat_to_xy(lon, lat) for lon, lat in poly]
              for poly in CONTINENTS_LONLAT]

# Story number -> true (lon, lat) of the place it happened. Pins are
# projected with the same function as the coastlines, so each pin sits
# on the right spot of the map.
PINS_LATLON = {
    1: (56.0, 26.5), 2: (30.7, 36.9), 3: (30.5, 50.4), 4: (19.0, 52.0),
    5: (-74.0, 40.7), 6: (20.0, 32.1), 7: (-107.4, 25.6),
    8: (106.1, -6.1), 9: (127.0, 37.5), 10: (6.1, 46.2),
    11: (-0.1, 54.0), 13: (74.3, 31.5),
}
# Tiny spreads (a few pixels, in box coordinates) so no two pin
# circles in crowded Europe sit on top of each other; each nudge
# stays on the same country as the true position.
PIN_NUDGE = {4: (-4, -2), 6: (-3, 2), 10: (-2, 2), 11: (-3, -1)}
PINS = {}
for _num, (_lon, _lat) in PINS_LATLON.items():
    _px, _py = lonlat_to_xy(_lon, _lat)
    _dx, _dy = PIN_NUDGE.get(_num, (0, 0))
    PINS[_num] = (_px + _dx, _py + _dy)

REGION_COLORS = [
    (196, 80, 52), (196, 120, 40), (64, 96, 140), (120, 120, 60),
    (90, 130, 90), (80, 120, 120), (110, 110, 110),
]
REGION_LABELS = ["ASIA", "MID EAST", "EUROPE", "AFRICA", "AMERICAS",
                 "OC", "GLOBAL"]


def fit_brief(draw, text, source, width):
    """One brief on one line: shrink, then trim the text with an ellipsis."""
    size = 12
    while size > 10:
        fnt = font("serif", size)
        if draw.textlength(text + " (" + source + ")", font=fnt) <= width:
            return fnt, text
        size -= 1
    fnt = font("serif", 10)
    full = text + " (" + source + ")"
    while draw.textlength(full, font=fnt) > width and len(text) > 12:
        text = text.rsplit(" ", 1)[0]
        full = text + "\u2026 (" + source + ")"
    return fnt, full


def render(out_path):
    """Compose the front page and write it to out_path. Returns info."""
    global _PAGE
    stories.validate()
    img = Image.new("RGB", (W, H), PAPER)
    _PAGE = img
    grain(img)
    draw = ImageDraw.Draw(img)

    # Outer frame.
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # Kicker line.
    draw.text((MARGIN, 16), stories.KICKER_LEFT, font=font("sans_bold", 12),
              fill=RED)
    right = stories.KICKER_RIGHT
    tw = draw.textlength(right, font=font("sans_bold", 12))
    draw.text((W - MARGIN - tw, 16), right, font=font("sans_bold", 12),
              fill=INK)

    # Masthead, date, subtitle.
    mast = font("serif_bold", 52)
    tw = draw.textlength(stories.MASTHEAD, font=mast)
    draw.text(((W - tw) / 2, 34), stories.MASTHEAD, font=mast, fill=INK)
    date_fnt = font("serif_bold", 21)
    tw = draw.textlength(stories.DATELINE, font=date_fnt)
    draw.text(((W - tw) / 2, 90), stories.DATELINE, font=date_fnt, fill=INK)
    sub = font("serif_italic", 12)
    tw = draw.textlength(stories.SUBTITLE, font=sub)
    draw.text(((W - tw) / 2, 113), stories.SUBTITLE, font=sub, fill=RED)
    # v4: the 13 px subhead's descenders (y in Kyiv, p in collapses)
    # reached y=131 and the rule at y=128 struck through them. The
    # 12 px face at y=113 ends at y=129, and the rules now sit at
    # y=133 and y=138, so every letter clears the rules by 4 px while
    # the date's own descenders (ending y=114) clear the subhead.
    rule(draw, 133, 3)
    rule(draw, 138, 1)

    # THE DAY IN UTC strip: six slots, generic time labels.
    draw.text((MARGIN, 142), "THE DAY IN UTC", font=font("sans_bold", 11),
              fill=RED)
    slot_w = (CW - 5 * 8) // 6
    for i, (label, text) in enumerate(stories.UTC_STRIP):
        x = MARGIN + i * (slot_w + 8)
        draw.text((x, 156), label, font=font("sans_bold", 11), fill=RED)
        tf, tl = fit_lines(draw, text, "sans", 11, slot_w, 2, min_size=10)
        draw_lines(draw, x, 169, tl, tf, INK, 13)
    rule(draw, 196, 1)

    # Region-count bar, widths proportional to the counts.
    bx, by, bh = MARGIN, 202, 22
    total = sum(count for _, count in stories.REGIONS)
    used = 0
    for i, ((name, count), color, label) in enumerate(
            zip(stories.REGIONS, REGION_COLORS, REGION_LABELS)):
        if i == len(stories.REGIONS) - 1:
            seg = CW - used
        else:
            seg = round(CW * count / total)
        draw.rectangle([bx + used, by, bx + used + seg, by + bh], fill=color)
        txt = "%s %d" % (label, count)
        tf = font("sans_bold", 10)
        tw = draw.textlength(txt, font=tf)
        draw.text((bx + used + (seg - tw) / 2, by + 5), txt, font=tf,
                  fill=(255, 255, 255))
        used += seg

    # Three big leads.
    lead_w = 318
    lead_gap = (CW - 3 * lead_w) // 2
    for i, lead in enumerate(stories.LEADS):
        x = MARGIN + i * (lead_w + lead_gap)
        ART[lead["art"]](draw, x, 232, lead_w, 108)
        draw.rectangle([x, 232, x + lead_w, 232 + 108], outline=INK, width=1)
        draw.text((x, 344), "%d \u00b7 %s" % (lead["num"], lead["kicker"]),
                  font=font("sans_bold", 11), fill=RED)
        hf, hl = fit_lines(draw, lead["headline"], "serif_bold", 20, lead_w,
                           2, min_size=17)
        draw_lines(draw, x, 358, hl, hf, INK, 21)
        bf, bl = fit_lines(draw, lead["body"], "serif", 13, lead_w, 3,
                           min_size=11)
        draw_lines(draw, x, 402, bl, bf, INK, 15)
        draw.text((x, 449), lead["source"], font=font("serif_italic", 11),
                  fill=GREY)
    rule(draw, 466, 1)

    # Ten grid stories: five columns, two rows.
    card_w = 187
    card_gap = (CW - 5 * card_w) // 4
    for row in range(2):
        top = 474 + row * 144
        for col in range(5):
            story = stories.GRID[row * 5 + col]
            x = MARGIN + col * (card_w + card_gap)
            ART[story["art"]](draw, x, top, card_w, 46)
            draw.rectangle([x, top, x + card_w, top + 46], outline=INK,
                           width=1)
            draw.text((x, top + 50), "%d \u00b7 %s" % (story["num"],
                      story["kicker"]), font=font("sans_bold", 10), fill=RED)
            hf, hl = fit_lines(draw, story["headline"], "serif_bold", 15,
                               card_w, 2, min_size=13)
            draw_lines(draw, x, top + 62, hl, hf, INK, 16)
            bf, bl = fit_lines(draw, story["body"], "serif", 11, card_w, 2,
                               min_size=10)
            draw_lines(draw, x, top + 96, bl, bf, INK, 12)
            draw.text((x, top + 123), story["source"],
                      font=font("serif_italic", 9), fill=GREY)
    rule(draw, 760, 1)

    # Map + briefs.
    draw.text((MARGIN, 768), "WHERE IT HAPPENED",
              font=font("sans_bold", 12), fill=RED)
    draw.text((MARGIN + 302, 768), "ALSO ON MONDAY 23 NOVEMBER \u2014 25 MORE",
              font=font("sans_bold", 12), fill=RED)
    mx, my, mw, mh = MARGIN, 784, MAP_W, MAP_H
    draw.rectangle([mx, my, mx + mw, my + mh], fill=OCEAN, outline=INK,
                   width=1)
    for poly in CONTINENTS:
        draw.polygon([(mx + px, my + py) for px, py in poly], fill=LAND,
                     outline=GREY)
    for num, (px, py) in PINS.items():
        draw.ellipse([mx + px - 6, my + py - 6, mx + px + 6, my + py + 6],
                     fill=RED, outline=(255, 255, 255))
        nf = font("sans_bold", 8)
        tw = draw.textlength(str(num), font=nf)
        draw.text((mx + px - tw / 2, my + py - 5), str(num), font=nf,
                  fill=(255, 255, 255))
    # Briefs in two columns: 13 left, 12 right.
    brief_w = 332
    for col in range(2):
        bx = MARGIN + 302 + col * (brief_w + 10)
        chunk = stories.BRIEFS[col * 13:(col + 1) * 13]
        by = 784
        for num, text, source in chunk:
            nf = font("sans_bold", 11)
            draw.text((bx, by), num, font=nf, fill=RED)
            nw = draw.textlength(num + " ", font=nf)
            bf, shown = fit_brief(draw, text, source, brief_w - nw)
            draw.text((bx + nw, by), shown, font=bf, fill=INK)
            by += 13

    # DATE CHECK footer.
    dc = ("DATE CHECK \u2014 Left out on purpose, first reported before "
          "Monday: " + stories.DATE_CHECK_LEFT_OUT + ". Not yet: "
          + stories.DATE_CHECK_NOT_YET + ".")
    df, dl = fit_lines(draw, dc, "serif", 12, CW, 2, min_size=11)
    draw_lines(draw, MARGIN, 958, dl, df, INK, 14)
    foot = font("sans", 11)
    tw = draw.textlength(stories.FOOTLINE, font=foot)
    draw.text(((W - tw) / 2, 994), stories.FOOTLINE, font=foot, fill=GREY)

    # Save: PNG, or JPEG when the PNG would pass the 1 MiB gate.
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    data = buf.getvalue()
    fmt = "PNG"
    if len(data) > MAX_BYTES:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=88, optimize=True)
        data = buf.getvalue()
        fmt = "JPEG"
        if len(data) > MAX_BYTES:
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=80, optimize=True)
            data = buf.getvalue()
    with open(out_path, "wb") as fh:
        fh.write(data)
    return {
        "path": out_path,
        "format": fmt,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": (W, H),
    }


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png")
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    print(render(target))
