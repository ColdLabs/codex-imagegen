#!/usr/bin/env python3
"""Make a contact sheet from several images so they can be compared at a glance.

Usage: uv run --with pillow scripts/contact_sheet.py OUT.jpg IMG1 IMG2 [IMG3 ...]
Works on macOS, Linux and Windows (no shell quoting involved).
"""
import sys
from pathlib import Path

from PIL import Image

ROW_HEIGHT = 400
GAP = 10


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    out = Path(argv[1]).expanduser()
    files = [Path(f).expanduser() for f in argv[2:]]
    images = []
    for f in files:
        im = Image.open(f).convert("RGB")
        images.append(im.resize((max(1, int(ROW_HEIGHT * im.width / im.height)), ROW_HEIGHT)))
    width = sum(im.width for im in images) + GAP * (len(images) - 1)
    sheet = Image.new("RGB", (width, ROW_HEIGHT), "white")
    x = 0
    for im in images:
        sheet.paste(im, (x, 0))
        x += im.width + GAP
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)
    print(out.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
