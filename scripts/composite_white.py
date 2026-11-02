#!/usr/bin/env python3
"""composite_white.py — place a transparent-background PNG onto a pure white canvas.

Usage:
  python3 scripts/composite_white.py <input.png> <output.png> [--size 1000]

The input must be a PNG with an alpha channel (transparent background).
The product is scaled to fit inside the canvas with 5% margin on each side,
centered, and composited onto RGB(255,255,255).

Exit codes:
  0  success
  1  input file not found or not a valid image
  2  bad arguments
"""

import sys
import os
import argparse

try:
    from PIL import Image
except ImportError:
    print("error: Pillow not installed — run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

def composite_onto_white(src_path: str, dst_path: str, canvas_size: int = 1000) -> None:
    if not os.path.exists(src_path):
        print(f"error: input not found: {src_path}", file=sys.stderr)
        sys.exit(1)

    try:
        src = Image.open(src_path).convert("RGBA")
    except Exception as e:
        print(f"error: cannot open image: {e}", file=sys.stderr)
        sys.exit(1)

    # Scale product to fit within (canvas * 0.90) keeping aspect ratio
    max_side = int(canvas_size * 0.90)
    src.thumbnail((max_side, max_side), Image.LANCZOS)

    canvas = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))

    # Center the product
    x = (canvas_size - src.width) // 2
    y = (canvas_size - src.height) // 2
    canvas.paste(src, (x, y), mask=src.split()[3])  # alpha as mask

    os.makedirs(os.path.dirname(os.path.abspath(dst_path)), exist_ok=True)
    canvas.save(dst_path, "PNG")
    print(f"ok: composited → {dst_path} ({canvas_size}x{canvas_size} white background)")


def main():
    parser = argparse.ArgumentParser(description="Composite transparent PNG onto white background")
    parser.add_argument("input", help="Input PNG with transparency")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--size", type=int, default=1000, help="Canvas size in px (default: 1000)")
    args = parser.parse_args()

    if args.size < 100 or args.size > 4096:
        print("error: --size must be 100–4096", file=sys.stderr)
        sys.exit(2)

    composite_onto_white(args.input, args.output, args.size)


if __name__ == "__main__":
    main()
