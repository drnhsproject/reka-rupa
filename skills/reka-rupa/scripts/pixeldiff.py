#!/usr/bin/env python3
"""Compare a source screenshot with a build screenshot, overall and by region.

Usage: pixeldiff.py <source.png> <build.png> [x0,y0,x1,y1 ...]
Needs Pillow and numpy. Both images must have the same pixel size, so capture
both at the same viewport width and device pixel ratio.
Each region is "x0,y0,x1,y1" in pixels. Without regions, the image is split
into horizontal bands of 80 px so you can see where the difference lives.
Reports the share of pixels whose largest channel difference exceeds 32.
Use it to attribute each remaining difference to a region, then look at that
region before naming a cause.
"""
import sys

try:
    import numpy as np
    from PIL import Image, ImageChops
except ImportError:
    print("needs Pillow and numpy (pip install pillow numpy)")
    sys.exit(2)

LIMIT = 32


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    a = Image.open(argv[1]).convert("RGB")
    b = Image.open(argv[2]).convert("RGB")
    if a.size != b.size:
        print(f"size mismatch: source {a.size}, build {b.size}")
        return 2
    diff = np.asarray(ImageChops.difference(a, b)).max(axis=2)
    width, height = a.size
    print(f"overall: {np.count_nonzero(diff > LIMIT) / diff.size * 100:.3f}% of pixels differ by more than {LIMIT}; max {diff.max()}")
    if len(argv) > 3:
        regions = [tuple(int(v) for v in arg.split(",")) for arg in argv[3:]]
    else:
        regions = [(0, y, width, min(y + 80, height)) for y in range(0, height, 80)]
    for x0, y0, x1, y1 in regions:
        part = diff[y0:y1, x0:x1]
        count = int(np.count_nonzero(part > LIMIT))
        if count or len(argv) > 3:
            ys, xs = np.nonzero(part > LIMIT)
            where = f" (at x {xs.min() + x0}-{xs.max() + x0}, y {ys.min() + y0}-{ys.max() + y0})" if count else ""
            print(f"  region {x0},{y0},{x1},{y1}: {count} px differ{where}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
