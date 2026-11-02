#!/usr/bin/env python3
"""composite_white.py — place a transparent-background PNG onto a pure white canvas.

Usage:
  python3 scripts/composite_white.py <input.png> <output.png> [--size 1000]

The input must be a PNG with a real alpha channel (transparent background).
Run rembg_cutout.py first to produce a cutout PNG from a product photo.
The product is scaled to fit inside the canvas with 5% margin on each side,
centered, and composited onto RGB(255,255,255).

Exit codes:
  0  success
  1  input file not found, no alpha channel, or not a valid image
  2  bad arguments
"""

import sys
import os
import argparse

try:
    from PIL import Image
    import numpy as np
except ImportError as e:
    print(f"error: missing dependency — {e}. Run: pip install Pillow numpy", file=sys.stderr)
    sys.exit(1)

def composite_onto_white(src_path: str, dst_path: str, canvas_size: int = 1000) -> None:
    if not os.path.exists(src_path):
        print(f"error: input not found: {src_path}", file=sys.stderr)
        sys.exit(1)

    try:
        src_raw = Image.open(src_path)
    except Exception as e:
        print(f"error: cannot open image: {e}", file=sys.stderr)
        sys.exit(1)

    # Bug fix: validate alpha channel before converting
    if src_raw.mode not in ("RGBA", "LA") and "transparency" not in src_raw.info:
        print(
            f"error: input has no alpha channel (mode={src_raw.mode}) — "
            "run rembg_cutout.py first to produce a cutout PNG",
            file=sys.stderr,
        )
        sys.exit(1)

    src = src_raw.convert("RGBA")
    alpha = np.array(src.split()[3])
    if alpha.min() == 255:
        print(
            "error: input has no transparent pixels — background was not removed. "
            "Run rembg_cutout.py first.",
            file=sys.stderr,
        )
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

    # Bug fix: infer output format from extension, not hardcoded PNG
    ext = os.path.splitext(dst_path)[1].lower().lstrip(".")
    fmt_map = {"png": "PNG", "webp": "WEBP"}
    if ext not in fmt_map:
        print(f"error: output must be .png or .webp, got .{ext}", file=sys.stderr)
        sys.exit(2)
    canvas.save(dst_path, fmt_map[ext])
    print(f"ok: composited → {dst_path} ({canvas_size}x{canvas_size} white background)")


def main():
    parser = argparse.ArgumentParser(description="Composite transparent PNG onto white background")
    parser.add_argument("input", help="Input PNG with transparency (from rembg_cutout.py)")
    parser.add_argument("output", help="Output path (.png or .webp)")
    parser.add_argument("--size", type=int, default=1000, help="Canvas size in px (default: 1000)")
    args = parser.parse_args()

    if args.size < 100 or args.size > 4096:
        print("error: --size must be 100–4096", file=sys.stderr)
        sys.exit(2)

    composite_onto_white(args.input, args.output, args.size)


if __name__ == "__main__":
    main()
