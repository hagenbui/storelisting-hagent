#!/usr/bin/env python3
"""Cut the props out of a decor kit sheet into separate transparent PNGs.
usage: cut_kit.py sheet.png outdir/      -> outdir/prop_0.png, prop_1.png, ...

The sheet is one generated image of 4 to 9 separate props laid out in a loose grid with clear gaps. If the generator
returned it with transparency, the alpha is used; otherwise the background must be flat magenta (#FF00FF), which is
keyed out. Props are found by cutting along empty rows and columns (no extra dependencies), specks are dropped.
Look at every cut before using it: two props that touch come out as one piece."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def mask_of(src):
    rgba = np.asarray(src.convert("RGBA")).astype(int); a = rgba[..., 3]
    if (a < 10).mean() > 0.2: return a > 128
    r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    return ~((r > 170) & (b > 150) & (g < 110) & (abs(r - b) < 90))


def runs(v, min_px=4, min_gap=12):
    on = v > min_px; out = []; s = None; gap = 0
    for i, x in enumerate(on):
        if x:
            if s is None: s = i
            gap = 0
        elif s is not None:
            gap += 1
            if gap >= min_gap: out.append((s, i - gap + 1)); s = None; gap = 0
    if s is not None: out.append((s, len(on)))
    return out


def cut(m, y0, x0, depth=0):
    boxes = []
    for r0, r1 in runs(m.sum(1)):
        sub = m[r0:r1]
        for c0, c1 in runs(sub.sum(0)):
            cell = sub[:, c0:c1]; rr = runs(cell.sum(1))
            if depth < 3 and len(rr) > 1: boxes += cut(cell, y0 + r0, x0 + c0, depth + 1)
            else: boxes.append((y0 + r0, x0 + c0, cell))
    return boxes


if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    src = Image.open(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    m = mask_of(src); rgb = np.asarray(src.convert("RGB")); k = 0
    for y, x, cell in cut(m, 0, 0):
        ys, xs = np.nonzero(cell)
        if len(ys) < 3000: continue                       # speck
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        alpha = Image.fromarray((cell[y0:y1, x0:x1] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1))
        piece = Image.fromarray(rgb[y + y0:y + y1, x + x0:x + x1]).convert("RGBA"); piece.putalpha(alpha)
        piece.save(out / f"prop_{k}.png"); print(f"prop_{k}", int(x + x0), int(y + y0), int(x1 - x0), int(y1 - y0)); k += 1
