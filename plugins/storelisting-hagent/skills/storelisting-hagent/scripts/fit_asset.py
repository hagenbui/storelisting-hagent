#!/usr/bin/env python3
"""Fit an AI-generated image to an exact store asset size.

The image generator only outputs 1024x1536, 1536x1024 or 1024x1024. Plain
cropping to the store ratio tends to cut headlines, so this script trims a
little from the long side and extends the background (using smoothed edge
colors, blended at the seam) for the rest.

usage: fit_asset.py KIND in.png out.png [--crop 0.04] [--anchor center|top]
KIND: play-shot ios-shot ipad-shot play-icon ios-icon play-fg
"""
import argparse
import numpy as np
from PIL import Image

KINDS = {
    #  kind        size          max trim per side (fraction)  mode
    "play-shot": ((1080, 1920), 0.04, "RGB"),
    "ios-shot":  ((1320, 2868), 0.08, "RGB"),
    "ipad-shot": ((2064, 2752), 0.06, "RGB"),
    "play-icon": ((512, 512),   0.0,  "RGBA"),  # Play wants 32-bit PNG
    "ios-icon":  ((1024, 1024), 0.0,  "RGB"),   # App Store icon must have no alpha
    "play-fg":   ((1024, 500),  0.5,  "RGB"),   # feature graphic: crop freely
}

def _smooth(row, k=61):
    pad = np.pad(row, ((k // 2, k // 2), (0, 0)), mode="edge")
    ker = np.ones(k) / k
    return np.stack([np.convolve(pad[:, c], ker, mode="valid") for c in range(3)], axis=1)

def _extend(a, before, after, axis, blend=24):
    """Extend array a along axis (0 = vertical, 1 = horizontal) using edge colors."""
    if axis == 1:
        return _extend(a.transpose(1, 0, 2), before, after, 0, blend).transpose(1, 0, 2)
    h = a.shape[0]
    top = _smooth(a[:6].mean(axis=0))
    bot = _smooth(a[-6:].mean(axis=0))
    out = np.concatenate([np.repeat(top[None], before, 0), a, np.repeat(bot[None], after, 0)], 0)
    b = min(blend, h // 4)
    for i in range(b):
        t = i / b
        if before:
            out[before + i] = (1 - t) * top + t * a[i]
        if after:
            out[before + h - 1 - i] = (1 - t) * bot + t * a[h - 1 - i]
    return out

def fit(src, dst, kind, crop=None, anchor="center"):
    (W, H), max_trim, mode = KINDS[kind]
    if crop is not None:
        max_trim = crop
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    target = W / H
    if abs(w / h - target) > 1e-3:
        if w / h > target:  # too wide: trim sides, then extend top/bottom
            need_w = h * target
            trim = int(min((w - need_w) / 2, max_trim * w))
            a = a[:, trim:w - trim]
            w = a.shape[1]
            new_h = round(w / target)
            if new_h > h:
                extra = new_h - h
                before = 0 if anchor == "top" else extra // 2
                a = _extend(a, before, extra - before, 0)
            else:  # trimming alone was enough; center-crop height
                y = (h - new_h) // 2
                a = a[y:y + new_h]
        else:  # too tall: trim top/bottom, then extend sides
            need_h = w / target
            trim = int(min((h - need_h) / 2, max_trim * h))
            a = a[trim:h - trim]
            h = a.shape[0]
            new_w = round(h * target)
            if new_w > w:
                extra = new_w - w
                a = _extend(a, extra // 2, extra - extra // 2, 1)
            else:
                x = (w - new_w) // 2
                a = a[:, x:x + new_w]
    out = Image.fromarray(a.clip(0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS).convert(mode)
    out.save(dst, "PNG")
    return out.size, out.mode

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=KINDS)
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--crop", type=float, help="max fraction trimmed from each side of the long axis")
    p.add_argument("--anchor", choices=["center", "top"], default="center",
                   help="where to add background when extending vertically")
    a = p.parse_args()
    size, mode = fit(a.src, a.dst, a.kind, a.crop, a.anchor)
    print(f"{a.dst} {size[0]}x{size[1]} {mode}")
