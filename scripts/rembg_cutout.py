#!/usr/bin/env python3
"""rembg_cutout.py — remove background from a product image using rembg (local, no API).

Usage:
  python3 scripts/rembg_cutout.py <input> <output.png>

The output is a PNG with a transparent background (alpha channel).
Feed the output into composite_white.py to produce a pure-white-background main image.

Exit codes:
  0  success
  1  input not found, rembg failed, or output write error
  2  bad arguments
"""

import sys
import os

def main():
    if len(sys.argv) != 3:
        print("usage: rembg_cutout.py <input> <output.png>", file=sys.stderr)
        sys.exit(2)

    src_path = sys.argv[1]
    dst_path = sys.argv[2]

    if not os.path.exists(src_path):
        print(f"error: input not found: {src_path}", file=sys.stderr)
        sys.exit(1)

    try:
        from rembg import remove
        from PIL import Image
    except ImportError as e:
        print(f"error: missing dependency — {e}. Run: pip install rembg Pillow", file=sys.stderr)
        sys.exit(1)

    try:
        with open(src_path, "rb") as f:
            input_data = f.read()
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        output_data = remove(input_data)
    except Exception as e:
        print(f"error: rembg failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Verify output has real transparency
    from io import BytesIO
    img = Image.open(BytesIO(output_data))
    if img.mode != "RGBA":
        print(f"error: rembg output has no alpha channel (mode={img.mode})", file=sys.stderr)
        sys.exit(1)

    import numpy as np
    alpha = np.array(img.split()[3])
    if alpha.min() == 255:
        print("warning: rembg output has no transparent pixels — background may not have been removed", file=sys.stderr)

    os.makedirs(os.path.dirname(os.path.abspath(dst_path)), exist_ok=True)
    try:
        with open(dst_path, "wb") as f:
            f.write(output_data)
    except OSError as e:
        print(f"error: cannot write output: {e}", file=sys.stderr)
        sys.exit(1)

    w, h = img.size
    transparent_pct = round((alpha < 255).sum() / alpha.size * 100, 1)
    print(f"ok: {src_path} → {dst_path} ({w}x{h}, {transparent_pct}% transparent)")

if __name__ == "__main__":
    main()
