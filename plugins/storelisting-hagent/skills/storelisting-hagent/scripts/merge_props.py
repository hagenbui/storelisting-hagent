#!/usr/bin/env python3
"""Merge a props-in-context edit back into the composed shot, keeping the phone and the real screen untouched.

usage: merge_props.py shot.png edited.png out.png crop.json
  shot.png    the composed shot from compose_phone.py (scene + phone + staged screen)
  edited.png  the image generator's edit of the crop (any size; it is scaled back onto the crop area)
  crop.json   written by compose_phone.py --edit-crop

Only pixels the edit really changed (the new props, their shadows) are taken, as whole objects with soft edges.
The screen interior always comes from shot.png; props may reach the screen's outer side margin only.
Exit 0 = done. Exit 2 = the edit drew onto the screen (the prop would be cut there): redo the edit and say so in
the prompt. Exit 3 = the edit added nothing, or changed the whole picture: redo it.
"""
import json, sys
import numpy as np
from PIL import Image
from scipy import ndimage

shot_p, edit_p, out_p, meta_p = sys.argv[1:5]
m = json.load(open(meta_p)); W, H = m["canvas"]; cy, ch = m["crop_y"], m["crop_h"]
orig = np.asarray(Image.open(shot_p).convert("RGB")).astype(float)
ed = orig.copy(); ed[cy:cy + ch] = np.asarray(Image.open(edit_p).convert("RGB").resize((W, ch), Image.LANCZOS)).astype(float)
# the generator can shift the picture by a pixel or two: line it up on the phone, but never by more than 8 px
X, Y, BW, BH = m["phone"]; y0 = max(Y, cy)
g = lambda a: a[y0:Y + BH, X:X + BW].mean(2)
F = np.fft.fft2(g(orig)) * np.conj(np.fft.fft2(g(ed))); r = np.abs(np.fft.ifft2(F / (np.abs(F) + 1e-9)))
dy, dx = np.unravel_index(r.argmax(), r.shape)
dy = dy - r.shape[0] if dy > r.shape[0] // 2 else dy; dx = dx - r.shape[1] if dx > r.shape[1] // 2 else dx
if max(abs(dy), abs(dx)) > 8: dy = dx = 0
ed = np.roll(ed, (dy, dx), (0, 1))
k = W / 1080  # sizes below were tuned on a 1080 px wide shot
d = np.abs(orig - ed).mean(2) > 26
lab, n = ndimage.label(ndimage.binary_dilation(ndimage.binary_opening(d, iterations=2), iterations=round(12 * k)))
keep = [i for i in range(1, n + 1) if (lab == i).sum() > 1500 * k * k]  # whole objects, no specks
mask = ndimage.binary_dilation(ndimage.binary_fill_holes(np.isin(lab, keep)), iterations=round(18 * k))
sx0, sy0, sx1, sy1 = m["screen"]; s = m["safe"]; inner = (slice(sy0, sy1), slice(sx0 + s, sx1 - s))
mf = ndimage.gaussian_filter(mask.astype(float), 14 * k); mf[inner] = 0
out = orig * (1 - mf[..., None]) + ed * mf[..., None]
Image.fromarray(out.round().clip(0, 255).astype(np.uint8)).save(out_p)
on_screen = ndimage.binary_opening(d, iterations=4)[inner].mean() * 100  # solid blobs only; re-drawn text edges are noise
cover = 100 * (mf > 0.5).mean()
print(f"aligned by ({dx}, {dy}) px; props cover {cover:.1f}% of the shot")
if on_screen > 0.3: print("REDO: the edit drew onto the app screen; ask for the prop just outside the phone"); sys.exit(2)
if not 0.5 < cover < 40: print("REDO: the edit added nothing, or changed the whole picture"); sys.exit(3)
