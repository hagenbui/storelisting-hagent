#!/usr/bin/env python3
"""Composite ONE identical phone (same size, position, bezel on every shot) with the real app screen onto a
phone-free scene, with optional cut-out props behind and in front of it.

usage:
  compose_phone.py play-shot scene.png screen.png out.png [--props props.json] [--body "#6A3E1E"]
  compose_phone.py ios-shot  scene.png screen.png out.png ...
  add --edit-crop crop.png to also write the bottom 2:3 of the shot (the props-in-context edit input) and crop.json
  (where the crop and the screen sit), which scripts/merge_props.py reads.

Geometry (fractions of the canvas): the phone is centered and runs from 26.3% to 97.5% of the height (about 60% of
the width on a 9:16 Play shot); width is capped at 70%, so on the taller iOS canvas it is anchored at 97.5% and starts
lower, leaving more headline room and no dead space. Height follows the screen's own ratio. The scene is
cover-fitted to the canvas (no stretching).

props.json, coordinates as fractions of the canvas:
  [{"img": "kit/prop_2.png", "cx": 0.115, "by": 0.955, "w": 0.22, "layer": "front"}, ...]
  cx = center x, by = bottom y, w = width; layer "back" (behind the phone) or "front".
Front props may cover the bezel and the screen's outer margin only (SAFE, about 3.7% of the phone width); the
script refuses a layout that reaches further into the screen, so no button or label is ever hidden.
"""
import json, sys
from PIL import Image, ImageDraw, ImageFilter

SIZES = {"play-shot": (1080, 1920), "ios-shot": (1320, 2868)}


def hex_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cover(scene, W, H):
    k = max(W / scene.width, H / scene.height)
    scene = scene.resize((round(scene.width * k), round(scene.height * k)), Image.LANCZOS)
    return scene.crop(((scene.width - W) // 2, 0, (scene.width - W) // 2 + W, H)).convert("RGBA")


def place(canvas, p, W, H, sbox, safe):
    im = Image.open(p["img"]).convert("RGBA")
    w = round(p["w"] * W); h = round(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    x, y = round(p["cx"] * W - w / 2), round(p["by"] * H) - h
    if x < 0 or y < 0 or x + w > W or y + h > H:
        sys.exit(f"refused: {p['img']} would be cut at the canvas edge (never-crop rule)")
    if p.get("layer") == "front":
        sx0, sy0, sx1, sy1 = sbox; a = im.split()[3].load()
        bad = sum(1 for yy in range(0, h, 4) for xx in range(0, w, 4)
                  if a[xx, yy] > 40 and sx0 + safe < x + xx < sx1 - safe and sy0 < y + yy < sy1)
        if bad:
            sys.exit(f"refused: front prop {p['img']} covers the app screen ({bad} sample points); move or shrink it")
    al = im.split()[3].point(lambda v: min(90, v)); sh = Image.new("RGBA", im.size, (60, 40, 20, 0)); sh.putalpha(al)
    pad = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); pad.alpha_composite(sh, (40, 58))
    canvas.alpha_composite(pad.filter(ImageFilter.GaussianBlur(18)), (x - 40, y - 40)); canvas.alpha_composite(im, (x, y))


def compose(kind, scene_p, screen_p, out_p, props=(), body="#2B2B2E"):
    W, H = SIZES[kind]; canvas = cover(Image.open(scene_p), W, H); screen = Image.open(screen_p).convert("RGB")
    # Size the phone to run from the top line (26.3%) to 97.5% of the height (no dead space below), capped at 70% of
    # the width; on taller canvases (iOS) the cap wins and the phone is anchored at the bottom instead.
    ratio = (screen.height / screen.width) * (1 - 2 * 0.0216) + 2 * 0.0216
    BW = round(min(W * 0.70, H * (0.975 - 0.263) / ratio)); BEZEL = round(BW * 0.0216); SW = BW - 2 * BEZEL
    SH = round(SW * screen.height / screen.width); BH = SH + 2 * BEZEL
    X, Y = (W - BW) // 2, max(round(H * 0.263), round(H * 0.975) - BH); R = round(BW * 0.117); safe = round(BW * 0.037)
    sbox = (X + BEZEL, Y + BEZEL, X + BEZEL + SW, Y + BEZEL + SH)
    if Y + BH > H: sys.exit("refused: phone would run off the bottom; use a taller canvas or a shorter screen")
    for p in props:
        if p.get("layer") != "front": place(canvas, p, W, H, sbox, safe)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((X, Y + BW // 27, X + BW, Y + BH + BW // 27), R, fill=(40, 30, 20, 110))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(BW // 23)))
    c = hex_rgb(body); light = tuple(min(255, v + 45) for v in c)
    phone = Image.new("RGBA", (BW, BH), (0, 0, 0, 0)); d = ImageDraw.Draw(phone)
    d.rounded_rectangle((0, 0, BW - 1, BH - 1), R, fill=c + (255,))
    d.rounded_rectangle((3, 3, BW - 4, BH - 4), R - 3, outline=light + (255,), width=3)
    canvas.alpha_composite(phone, (X, Y))
    m = Image.new("L", (SW, SH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), R - BEZEL, fill=255)
    canvas.paste(screen.resize((SW, SH), Image.LANCZOS), sbox[:2], m)
    for p in props:
        if p.get("layer") == "front": place(canvas, p, W, H, sbox, safe)
    canvas.convert("RGB").save(out_p)
    return {"canvas": (W, H), "phone": (X, Y, BW, BH), "body_ratio": round(BH / BW, 2), "top_pct": round(100 * Y / H, 1),
            "bottom_pct": round(100 * (Y + BH) / H, 1), "screen": sbox, "safe": safe}


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 4 or a[0] not in SIZES: sys.exit(__doc__)
    props = json.load(open(a[a.index("--props") + 1])) if "--props" in a else []
    body = a[a.index("--body") + 1] if "--body" in a else "#2B2B2E"
    r = compose(a[0], a[1], a[2], a[3], props, body); print(r)
    if "--edit-crop" in a:  # the image generator edits at 2:3, so hand it the bottom 2:3, where the phone and props are
        crop_p = a[a.index("--edit-crop") + 1]; W, H = r["canvas"]; ch = min(H, round(W * 1.5))
        Image.open(a[3]).crop((0, H - ch, W, H)).save(crop_p)
        json.dump({"crop_y": H - ch, "crop_h": ch, **{k: r[k] for k in ("canvas", "phone", "screen", "safe")}}, open(crop_p.rsplit(".", 1)[0] + ".json", "w"))
