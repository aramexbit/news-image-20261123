"""Render THE WORLD HERALD, the one-page front page for 23 November 2026.

Draws the masthead, one lead story with a full-width photograph, four
column stories and a four-brief footer strip onto a 1024x1024 sheet of
newsprint, from the stories in stories.py. No network, no clock, no
randomness except a fixed-seed grain, so two runs write identical bytes.

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
MARGIN = 30
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


def center_crop(im, target_w, target_h):
    """Crop the image to the target aspect, centred, then resize."""
    sw, sh = im.size
    target_ratio = target_w / target_h
    ratio = sw / sh
    if ratio > target_ratio:
        new_w = int(sh * target_ratio)
        left = (sw - new_w) // 2
        im = im.crop((left, 0, left + new_w, sh))
    else:
        new_h = int(sw / target_ratio)
        top = (sh - new_h) // 2
        im = im.crop((0, top, sw, top + new_h))
    return im.resize((target_w, target_h), Image.LANCZOS)


def photo(name, target_w, target_h):
    """A generated photograph from assets/, cropped to the slot."""
    path = os.path.join(ASSETS, name)
    with Image.open(path) as im:
        return center_crop(im.convert("RGB"), target_w, target_h)


def grain(img):
    """Fixed-seed newsprint speckle; deterministic across runs."""
    rng = random.Random(20261123)
    px = img.load()
    for _ in range(1400):
        x = rng.randrange(W)
        y = rng.randrange(H)
        px[x, y] = PAPER_DARK if rng.random() < 0.5 else PAPER_LIGHT
    return img


def markets_chart(draw, x, y, w, h):
    """A small drawn markets panel: the Friday plunge, in red."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=LIGHT_RULE)
    for gy in (y + h // 3, y + 2 * h // 3):
        draw.line([x + 4, gy, x + w - 4, gy], fill=(226, 220, 204))
    pts = [
        (x + 8, y + 16), (x + 34, y + 26), (x + 58, y + 22),
        (x + 84, y + 40), (x + 108, y + 38), (x + 132, y + 58),
        (x + 158, y + 54), (x + 182, y + 74), (x + 206, y + 70),
        (x + w - 8, y + h - 14),
    ]
    draw.line(pts, fill=RED, width=3, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    small = font("sans_bold", 13)
    draw.text((x + 8, y + 4), "S&P 500 \u22123.7%", font=small, fill=RED)
    draw.text((x + 8, y + h - 20), "Nasdaq \u22125.3%  \u00b7  Taiwan \u221217.5%",
              font=font("sans", 11), fill=GREY)


def rule(draw, y, weight=1, x0=None, x1=None):
    """A horizontal rule across the content width."""
    draw.line([x0 or MARGIN, y, x1 or (W - MARGIN), y], fill=RULE, width=weight)
    return y + weight


def render(out_path):
    """Compose the front page and write it to out_path. Returns info."""
    stories.validate()
    img = Image.new("RGB", (W, H), PAPER)
    grain(img)
    draw = ImageDraw.Draw(img)

    # Outer frame.
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # Masthead.
    mast = font("serif_bold", 60)
    tw = draw.textlength(stories.MASTHEAD, font=mast)
    draw.text(((W - tw) / 2, 20), stories.MASTHEAD, font=mast, fill=INK)
    rule(draw, 90, 3)
    rule(draw, 95, 1)
    date_fnt = font("sans_bold", 15)
    tw = draw.textlength(stories.DATELINE, font=date_fnt)
    draw.text(((W - tw) / 2, 102), stories.DATELINE, font=date_fnt, fill=INK)
    rule(draw, 124, 1)

    # Lead story.
    lead = stories.LEAD
    y = 134
    kick = font("sans_bold", 14)
    draw.text((MARGIN, y), lead["kicker"], font=kick, fill=RED)
    y += 22
    head_fnt, head_lines = fit_lines(draw, lead["headline"], "serif_bold",
                                     44, CW, 2, min_size=36)
    y = draw_lines(draw, MARGIN, y, head_lines, head_fnt, INK, 50)
    y += 8
    hero = photo(lead["image"], CW, 232)
    img.paste(hero, (MARGIN, y))
    draw.rectangle([MARGIN, y, MARGIN + CW, y + 232], outline=INK, width=1)
    y += 232 + 10
    body_fnt, body_lines = fit_lines(draw, lead["body"], "serif", 19, CW, 4)
    y = draw_lines(draw, MARGIN, y, body_lines, body_fnt, INK, 24)
    y += 4
    src = font("serif_italic", 14)
    draw.text((MARGIN, y), "Sources: " + lead["source"], font=src, fill=GREY)
    y += 20
    rule(draw, y, 1)
    y += 10

    # Four column stories.
    col_w = 232
    gap = (CW - 4 * col_w) // 3
    col_top = y
    col_bottom = col_top
    for i, col in enumerate(stories.COLUMNS):
        x = MARGIN + i * (col_w + gap)
        cy = col_top
        if col.get("chart"):
            markets_chart(draw, x, cy, col_w, 96)
        else:
            thumb = photo(col["image"], col_w, 96)
            img.paste(thumb, (x, cy))
            draw.rectangle([x, cy, x + col_w, cy + 96], outline=INK, width=1)
        cy += 96 + 8
        draw.text((x, cy), col["kicker"], font=font("sans_bold", 12), fill=RED)
        cy += 18
        hf, hl = fit_lines(draw, col["headline"], "serif_bold", 22, col_w, 2)
        cy = draw_lines(draw, x, cy, hl, hf, INK, 24)
        cy += 2
        bf, bl = fit_lines(draw, col["body"], "serif", 14, col_w, 4, min_size=12)
        cy = draw_lines(draw, x, cy, bl, bf, INK, 18)
        cy += 3
        draw.text((x, cy), col["source"], font=font("serif_italic", 12), fill=GREY)
        cy += 16
        col_bottom = max(col_bottom, cy)
    y = col_bottom + 2
    rule(draw, y, 1)
    y += 10

    # Footer strip: four briefs.
    for i, brief in enumerate(stories.FOOTER):
        x = MARGIN + i * (col_w + gap)
        text = brief["lead"] + " \u2014 " + brief["text"] + " (" + brief["source"] + ")"
        ff, fl = fit_lines(draw, text, "serif", 13, col_w, 3, min_size=11)
        draw_lines(draw, x, y, fl, ff, INK, 16)
    y += 3 * 16 + 8
    foot = font("sans", 11)
    tw = draw.textlength(stories.FOOTLINE, font=foot)
    draw.text(((W - tw) / 2, y), stories.FOOTLINE, font=foot, fill=GREY)

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
