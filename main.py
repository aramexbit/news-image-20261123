"""THE WORLD HERALD — 23 November 2026: write the front page to the output.

Standard library only at the top level, so the run never fails on a
missing third-party package: the page is composed through composer.py
when Pillow is available, and the prebuilt image in assets/ is copied
instead when it is not. No network, no clock, no randomness — two runs
write identical bytes.

Usage:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576
PAGE = (1024, 1024)


def output_dir():
    """The grader writes to /output; local runs use MAKEFUN_OUTPUT_DIR."""
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    if os.path.isdir("/output"):
        return "/output"
    return "out"


def clear_contents(path):
    """Empty the output folder; the folder itself is never removed."""
    os.makedirs(path, exist_ok=True)
    for name in os.listdir(path):
        target = os.path.join(path, name)
        if os.path.isdir(target) and not os.path.islink(target):
            shutil.rmtree(target)
        else:
            os.remove(target)


def copy_prebuilt(target):
    """Fallback: the prebuilt page bundled in assets/."""
    root = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(root, "assets", "entry.png")
    shutil.copyfile(source, target)
    return "prebuilt"


def read_png_size(path):
    """Image dimensions from the PNG header; None when it is not a PNG."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return (width, height)


def read_jpeg_size(data):
    """Image dimensions from a JPEG SOF marker; None when not found."""
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return (width, height)
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + length
    return None


def verify(target):
    """The gate's own checks, here: whole file, size, and dimensions."""
    with open(target, "rb") as fh:
        data = fh.read()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        kind = "PNG"
    elif data[:2] == b"\xff\xd8":
        kind = "JPEG"
    else:
        raise SystemExit("output is neither PNG nor JPEG")
    if len(data) > MAX_BYTES:
        raise SystemExit("output is over the 1 MiB gate: %d bytes" % len(data))
    if kind == "PNG":
        size = read_png_size(target)
    else:
        size = read_jpeg_size(data)
    if size is not None and size != PAGE:
        raise SystemExit("%s is %s, the page must be 1024x1024" % (kind, size))
    return kind, len(data), hashlib.sha256(data).hexdigest()


def main():
    out_dir = output_dir()
    clear_contents(out_dir)
    target = os.path.join(out_dir, "entry.png")
    if os.environ.get("MAKEFUN_FORCE_FALLBACK"):
        # Forced fallback: used by the local test, never by the grader.
        mode = copy_prebuilt(target)
    else:
        try:
            import composer
        except ImportError:
            mode = copy_prebuilt(target)
        else:
            composer.render(target)
            mode = "composed"
    kind, size, digest = verify(target)
    print("WROTE %s %s %d bytes sha256=%s mode=%s" % (target, kind, size, digest, mode))
    return 0


if __name__ == "__main__":
    sys.exit(main())
