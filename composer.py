"""Render THE WORLD HERALD v2, the one-page front page for 23 Nov 2026.

Follows the winning pattern of the 19 November edition: masthead with a
big date, a THE DAY IN UTC strip, a region-count bar, three big leads
with flat drawn illustrations, ten medium grid stories, a world map with
numbered pins, twenty-five one-line briefs, and a DATE CHECK footer.

Thirty-eight stories in all, every one named with its source, from the
stories in stories.py. All illustrations are drawn flat with PIL — no
photographs. No network, no clock, no randomness except a fixed-seed
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
# Flat illustrations, drawn with PIL. Each takes (draw, x, y, w, h).
# ---------------------------------------------------------------------------

def _flames(draw, cx, base, scale=1.0):
    """Three flat flame tongues above (cx, base)."""
    s = scale
    for dx, fh, col in ((-16, 34, (230, 110, 30)), (0, 46, (240, 170, 40)),
                        (16, 30, (230, 110, 30))):
        x0 = cx + dx * s
        draw.polygon([(x0 - 10 * s, base), (x0, base - fh * s),
                      (x0 + 10 * s, base)], fill=col)


def _smoke(draw, x, y, r, col=(120, 116, 106)):
    """A small puff of smoke: three overlapping circles."""
    draw.ellipse([x - r, y - r, x + r, y + r], fill=col)
    draw.ellipse([x - r // 2, y - r - 4, x + r, y - r + 6], fill=col)
    draw.ellipse([x + r // 2, y - r // 2, x + 2 * r, y + r // 2], fill=col)


def art_tanker(draw, x, y, w, h):
    """A burning tanker in the strait, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    draw.line([x, y + h * 0.62, x + w, y + h * 0.62], fill=(120, 150, 175))
    # Distant tanker, already burning.
    draw.rectangle([x + w * 0.68, y + h * 0.42, x + w * 0.92, y + h * 0.62],
                   fill=(40, 40, 44))
    _flames(draw, x + w * 0.80, y + h * 0.44, scale=0.55)
    _smoke(draw, x + w * 0.80, y + h * 0.26, 9)
    # Main tanker.
    draw.rectangle([x + w * 0.08, y + h * 0.50, x + w * 0.62, y + h * 0.78],
                   fill=(28, 28, 32))
    draw.rectangle([x + w * 0.08, y + h * 0.50, x + w * 0.62, y + h * 0.56],
                   fill=(163, 30, 30))
    draw.rectangle([x + w * 0.50, y + h * 0.34, x + w * 0.60, y + h * 0.50],
                   fill=(60, 60, 66))
    _flames(draw, x + w * 0.30, y + h * 0.52, scale=0.9)
    _flames(draw, x + w * 0.46, y + h * 0.52, scale=0.7)
    _smoke(draw, x + w * 0.30, y + h * 0.24, 12)
    _smoke(draw, x + w * 0.48, y + h * 0.30, 9)
    # A naval mine, floating.
    draw.ellipse([x + w * 0.86, y + h * 0.80, x + w * 0.92, y + h * 0.88],
                 fill=(20, 20, 22))
    draw.line([x + w * 0.89, y + h * 0.78, x + w * 0.89, y + h * 0.72],
              fill=(20, 20, 22), width=2)


def art_cop(draw, x, y, w, h):
    """A conference hall with fossil fuels crossed out, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x + w * 0.10, y + h * 0.42, x + w * 0.90, y + h],
                   fill=(96, 110, 128))
    draw.polygon([(x + w * 0.10, y + h * 0.42), (x + w * 0.50, y + h * 0.22),
                  (x + w * 0.90, y + h * 0.42)], fill=(72, 86, 104))
    for i in range(5):
        cx = x + w * (0.18 + i * 0.16)
        draw.rectangle([cx, y + h * 0.58, cx + w * 0.07, y + h * 0.94],
                       fill=(232, 226, 208))
    # Flags of the deadlocked parties.
    for i, col in enumerate(((163, 30, 30), (64, 96, 140), (196, 120, 40),
                             (90, 130, 90), (120, 120, 60))):
        fx = x + w * (0.14 + i * 0.17)
        draw.line([fx, y + h * 0.30, fx, y + h * 0.46], fill=INK, width=2)
        draw.rectangle([fx, y + h * 0.30, fx + 14, y + h * 0.40], fill=col)
    label = "FOSSIL FUELS"
    fnt = font("sans_bold", 15)
    tw = draw.textlength(label, font=fnt)
    lx, ly = x + (w - tw) / 2, y + h * 0.10
    draw.text((lx, ly), label, font=fnt, fill=RED)
    draw.line([lx - 4, ly + 8, lx + tw + 4, ly + 8], fill=RED, width=3)


def art_block(draw, x, y, w, h):
    """A damaged apartment block under a smoke plume, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # The block, top corner torn away by the strike.
    draw.polygon([(x + w * 0.22, y + h * 0.98), (x + w * 0.22, y + h * 0.18),
                  (x + w * 0.38, y + h * 0.18), (x + w * 0.44, y + h * 0.34),
                  (x + w * 0.52, y + h * 0.26), (x + w * 0.60, y + h * 0.40),
                  (x + w * 0.78, y + h * 0.24),
                  (x + w * 0.78, y + h * 0.98)], fill=(120, 118, 110))
    # Scorch marks around the torn corner.
    draw.polygon([(x + w * 0.40, y + h * 0.20), (x + w * 0.46, y + h * 0.32),
                  (x + w * 0.52, y + h * 0.28)], fill=(60, 58, 54))
    for r in range(4):
        for c in range(4):
            wx = x + w * (0.28 + c * 0.12)
            wy = y + h * (0.34 + r * 0.16)
            if r == 0 and c < 2:
                continue  # the torn corner has no windows
            draw.rectangle([wx, wy, wx + 12, wy + 14], fill=(52, 52, 56))
    _smoke(draw, x + w * 0.45, y + h * 0.14, 12)
    _smoke(draw, x + w * 0.62, y + h * 0.10, 9)
    # Rubble at the base.
    for i, (dx, s) in enumerate(((0.30, 10), (0.44, 14), (0.62, 9))):
        draw.polygon([(x + w * dx, y + h * 0.98),
                      (x + w * dx + s, y + h * 0.98 - s * 0.7),
                      (x + w * dx + 2 * s, y + h * 0.98)],
                     fill=(90, 88, 82))
    # A rescue ladder against the block.
    draw.line([x + w * 0.84, y + h * 0.98, x + w * 0.80, y + h * 0.40],
              fill=RED, width=3)


def art_missile(draw, x, y, w, h):
    """A cruise missile over a field, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + w * 0.70, y + h * 0.08, x + w * 0.98, y + h * 0.32],
                 fill=(240, 200, 90))
    # Missile body, diagonal and thick enough to read at card size.
    draw.polygon([(x + w * 0.14, y + h * 0.66), (x + w * 0.62, y + h * 0.28),
                  (x + w * 0.72, y + h * 0.40), (x + w * 0.24, y + h * 0.78)],
                 fill=(235, 233, 226))
    draw.polygon([(x + w * 0.62, y + h * 0.28), (x + w * 0.76, y + h * 0.22),
                  (x + w * 0.72, y + h * 0.40)], fill=(163, 30, 30))
    draw.polygon([(x + w * 0.14, y + h * 0.66), (x + w * 0.08, y + h * 0.60),
                  (x + w * 0.18, y + h * 0.58), (x + w * 0.24, y + h * 0.78)],
                 fill=(120, 118, 112))
    # Flame and smoke at the tail.
    draw.polygon([(x + w * 0.14, y + h * 0.66), (x + w * 0.04, y + h * 0.72),
                  (x + w * 0.10, y + h * 0.80)], fill=(240, 170, 40))
    _smoke(draw, x + w * 0.06, y + h * 0.62, 5)
    # Field below, with an impact burst.
    draw.rectangle([x, y + h * 0.80, x + w, y + h], fill=(120, 130, 80))
    draw.ellipse([x + w * 0.78, y + h * 0.78, x + w * 0.92, y + h * 0.94],
                 fill=(90, 100, 60))
    draw.polygon([(x + w * 0.85, y + h * 0.76), (x + w * 0.88, y + h * 0.66),
                  (x + w * 0.91, y + h * 0.76)], fill=(230, 110, 30))


def art_chart(draw, x, y, w, h):
    """The Friday plunge, in red, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=LIGHT_RULE)
    for gy in (y + h // 3, y + 2 * h // 3):
        draw.line([x + 3, gy, x + w - 3, gy], fill=(226, 220, 204))
    pts = [(x + 6, y + 8), (x + 34, y + 14), (x + 62, y + 12),
           (x + 90, y + 24), (x + 118, y + 22), (x + 146, y + 34),
           (x + w - 6, y + h - 10)]
    draw.line(pts, fill=RED, width=3, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    draw.text((x + 6, y + 1), "S&P \u22123.7%", font=font("sans_bold", 10),
              fill=RED)
    draw.text((x + 6, y + h - 13), "Nasdaq \u22125.3%",
              font=font("sans", 9), fill=GREY)


def art_ship(draw, x, y, w, h):
    """A warship capsizing after a drone strike, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h * 0.64, x + w, y + h], fill=SEA)
    # The corvette, heeling over.
    draw.polygon([(x + w * 0.12, y + h * 0.60), (x + w * 0.72, y + h * 0.44),
                  (x + w * 0.80, y + h * 0.58), (x + w * 0.30, y + h * 0.72)],
                 fill=(80, 84, 90))
    draw.rectangle([x + w * 0.42, y + h * 0.34, x + w * 0.56, y + h * 0.48],
                   fill=(60, 64, 70))
    _flames(draw, x + w * 0.55, y + h * 0.46, scale=0.5)
    _smoke(draw, x + w * 0.55, y + h * 0.28, 8)
    # A sea drone, low over the water.
    dx, dy = x + w * 0.82, y + h * 0.30
    draw.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(20, 20, 22))
    draw.line([dx - 12, dy - 6, dx + 12, dy - 6], fill=(20, 20, 22), width=2)
    draw.line([dx - 12, dy + 6, dx + 12, dy + 6], fill=(20, 20, 22), width=2)


def art_badge(draw, x, y, w, h):
    """A police badge on navy, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=(36, 52, 78))
    cx, cy = x + w / 2, y + h / 2
    draw.polygon([(cx, cy - 18), (cx + 16, cy - 8), (cx + 12, cy + 12),
                  (cx, cy + 20), (cx - 12, cy + 12), (cx - 16, cy - 8)],
                 fill=(216, 170, 60), outline=(240, 200, 90))
    draw.ellipse([cx - 5, cy - 7, cx + 5, cy + 3], fill=(36, 52, 78))
    draw.text((x + 6, y + h - 12), "FBI MOST WANTED", font=font("sans_bold", 8),
              fill=(240, 200, 90))


def art_factory(draw, x, y, w, h):
    """A factory on fire, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x + w * 0.08, y + h * 0.48, x + w * 0.92, y + h],
                   fill=(110, 108, 100))
    draw.polygon([(x + w * 0.08, y + h * 0.48), (x + w * 0.25, y + h * 0.30),
                  (x + w * 0.42, y + h * 0.48), (x + w * 0.59, y + h * 0.30),
                  (x + w * 0.76, y + h * 0.48), (x + w * 0.92, y + h * 0.48)],
                 fill=(88, 86, 80))
    draw.rectangle([x + w * 0.80, y + h * 0.18, x + w * 0.88, y + h * 0.48],
                   fill=(96, 94, 88))
    _flames(draw, x + w * 0.50, y + h * 0.50, scale=0.55)
    _smoke(draw, x + w * 0.84, y + h * 0.12, 8)
    for i in range(3):
        wx = x + w * (0.16 + i * 0.28)
        draw.rectangle([wx, y + h * 0.62, wx + 16, y + h * 0.78],
                       fill=(240, 170, 40))


def art_school(draw, x, y, w, h):
    """An exam paper with red marks and a pencil, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 220, 204))
    draw.rectangle([x + w * 0.24, y + h * 0.08, x + w * 0.72, y + h * 0.92],
                   fill=(255, 253, 246), outline=INK)
    for i in range(4):
        ly = y + h * (0.28 + i * 0.16)
        draw.line([x + w * 0.30, ly, x + w * 0.66, ly], fill=GREY, width=1)
    draw.text((x + w * 0.30, y + h * 0.10), "EXAM", font=font("sans_bold", 10),
              fill=INK)
    # Two red crosses over the answers.
    for cx, cy in ((0.62, 0.34), (0.62, 0.50)):
        px, py = x + w * cx, y + h * cy
        draw.line([px - 5, py - 5, px + 5, py + 5], fill=RED, width=2)
        draw.line([px - 5, py + 5, px + 5, py - 5], fill=RED, width=2)
    draw.polygon([(x + w * 0.80, y + h * 0.70), (x + w * 0.88, y + h * 0.62),
                  (x + w * 0.94, y + h * 0.86), (x + w * 0.86, y + h * 0.94)],
                 fill=(240, 170, 40))
    draw.polygon([(x + w * 0.88, y + h * 0.62), (x + w * 0.90, y + h * 0.58),
                  (x + w * 0.94, y + h * 0.66)], fill=(163, 30, 30))


def art_globe(draw, x, y, w, h):
    """A globe with an orbit ring, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 228, 220))
    cx, cy, r = x + w * 0.42, y + h * 0.52, min(w, h) * 0.34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 110, 160))
    draw.ellipse([cx - r * 0.45, cy - r * 0.7, cx + r * 0.3, cy - r * 0.1],
                 fill=(90, 140, 80))
    draw.ellipse([cx - r * 0.2, cy + r * 0.25, cx + r * 0.75, cy + r * 0.8],
                 fill=(90, 140, 80))
    draw.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6],
                 outline=(163, 30, 30), width=2)
    draw.text((x + w * 0.74, y + h * 0.12), "128", font=font("sans_bold", 14),
              fill=RED)
    draw.text((x + w * 0.74, y + h * 0.40), "STATES", font=font("sans_bold", 8),
              fill=INK)


def art_trophy(draw, x, y, w, h):
    """A gold trophy and a football, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 234, 214))
    cx = x + w * 0.38
    draw.polygon([(cx - 18, y + h * 0.10), (cx + 18, y + h * 0.10),
                  (cx + 12, y + h * 0.52), (cx - 12, y + h * 0.52)],
                 fill=(216, 170, 60))
    draw.arc([cx - 26, y + h * 0.12, cx - 8, y + h * 0.40], 90, 270,
             fill=(216, 170, 60), width=4)
    draw.arc([cx + 8, y + h * 0.12, cx + 26, y + h * 0.40], -90, 90,
             fill=(216, 170, 60), width=4)
    draw.rectangle([cx - 4, y + h * 0.52, cx + 4, y + h * 0.68],
                   fill=(216, 170, 60))
    draw.rectangle([cx - 16, y + h * 0.68, cx + 16, y + h * 0.76],
                   fill=(216, 170, 60))
    bx, by = x + w * 0.76, y + h * 0.68
    draw.ellipse([bx - 14, by - 14, bx + 14, by + 14], fill=(255, 253, 246),
                 outline=INK)
    draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=INK)
    for dx, dy in ((-9, -8), (9, -8), (-11, 6), (11, 6)):
        draw.ellipse([bx + dx - 2, by + dy - 2, bx + dx + 2, by + dy + 2],
                     fill=INK)


def art_mercury(draw, x, y, w, h):
    """Mercury and the BepiColombo probe, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    for sx, sy in ((0.12, 0.16), (0.30, 0.10), (0.86, 0.14), (0.92, 0.60),
                   (0.08, 0.70)):
        draw.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2],
                     fill=(255, 253, 246))
    cx, cy, r = x + w * 0.38, y + h * 0.52, min(w, h) * 0.30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 146, 138))
    for dx, dy, cr in ((-0.4, -0.3, 4), (0.3, 0.1, 5), (-0.1, 0.45, 3),
                       (0.5, -0.4, 3)):
        draw.ellipse([cx + dx * r - cr, cy + dy * r - cr,
                      cx + dx * r + cr, cy + dy * r + cr],
                     fill=(120, 116, 108))
    # The probe, with solar panels.
    px, py = x + w * 0.78, y + h * 0.30
    draw.rectangle([px - 10, py - 3, px - 2, py + 3], fill=(64, 110, 160))
    draw.rectangle([px + 2, py - 3, px + 10, py + 3], fill=(64, 110, 160))
    draw.rectangle([px - 3, py - 5, px + 3, py + 5], fill=(220, 218, 210))


def art_smog(draw, x, y, w, h):
    """A city skyline under a smog haze, flat."""
    draw.rectangle([x, y, x + w, y + h], fill=(222, 200, 160))
    draw.ellipse([x + w * 0.76, y + h * 0.10, x + w * 0.94, y + h * 0.34],
                 fill=(230, 120, 40))
    for bx, bw, bh in ((0.06, 0.16, 0.52), (0.26, 0.20, 0.68),
                       (0.50, 0.16, 0.44), (0.70, 0.20, 0.60)):
        draw.rectangle([x + w * bx, y + h * (1 - bh), x + w * (bx + bw), y + h],
                       fill=(110, 104, 92))
    draw.rectangle([x, y + h * 0.62, x + w, y + h * 0.78],
                   fill=(196, 168, 120))
    draw.text((x + 6, y + 4), "AQI 538", font=font("sans_bold", 13),
              fill=RED)


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

# Simplified world map, in a 290 x 172 box: lon -170..190, lat 75..-55.
CONTINENTS = [
    [(14, 42), (40, 26), (72, 20), (96, 30), (104, 44), (98, 58), (86, 66),
     (70, 58), (58, 66), (34, 60), (18, 52)],
    [(72, 8), (92, 6), (96, 16), (78, 18)],
    [(82, 88), (104, 82), (118, 96), (112, 120), (100, 142), (90, 124),
     (82, 104)],
    [(136, 34), (158, 26), (176, 34), (170, 50), (152, 52), (140, 44)],
    [(140, 68), (168, 64), (186, 78), (178, 104), (160, 122), (146, 104),
     (138, 84)],
    [(176, 30), (220, 20), (262, 28), (276, 44), (262, 62), (236, 72),
     (212, 66), (192, 52), (178, 44)],
    [(232, 84), (246, 88), (258, 92)],
    [(238, 124), (268, 122), (274, 140), (246, 146), (234, 134)],
]
# Story number -> pin position in the map box.
PINS = {
    1: (183, 64), 2: (162, 50), 3: (168, 32), 4: (152, 24),
    5: (234, 68), 6: (153, 57), 7: (50, 65), 8: (222, 107),
    9: (239, 50), 10: (140, 46), 11: (132, 28), 13: (197, 58),
}

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
    stories.validate()
    img = Image.new("RGB", (W, H), PAPER)
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
    sub = font("serif_italic", 13)
    tw = draw.textlength(stories.SUBTITLE, font=sub)
    draw.text(((W - tw) / 2, 114), stories.SUBTITLE, font=sub, fill=RED)
    rule(draw, 128, 3)
    rule(draw, 133, 1)

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
    mx, my, mw, mh = MARGIN, 784, 290, 166
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
