#!/usr/bin/env python3
"""Check every PNG/JPEG in a pack folder against store specs.

Files are matched by name prefix:
  play_screenshot_*  1080x1920 (or any 9:16 / 16:9, 320-3840px), no alpha, <= 8 MB
  play_icon*         512x512, RGBA PNG, <= 1 MB
  play_feature*      1024x500, no alpha, <= 15 MB
  ios_screenshot_*   1320x2868 or 1290x2796 (6.9"), or 1242x2688 / 1284x2778 (6.5"), no alpha
  ipad_screenshot_*  2064x2752 or 2048x2732, no alpha
  ios_icon*          1024x1024, no alpha
usage: check_pack.py PACK_DIR
"""
import os, sys
from PIL import Image

MB = 1024 * 1024
RULES = [
    ("play_screenshot", lambda w, h: 320 <= min(w, h) and max(w, h) <= 3840 and
        round(max(w, h) / min(w, h), 3) == round(16 / 9, 3), False, 8 * MB, "9:16, 320-3840px"),
    ("play_icon", lambda w, h: (w, h) == (512, 512), True, 1 * MB, "512x512 32-bit"),
    ("play_feature", lambda w, h: (w, h) == (1024, 500), False, 15 * MB, "1024x500"),
    ("ios_screenshot", lambda w, h: (w, h) in [(1320, 2868), (1290, 2796), (1242, 2688), (1284, 2778)],
        False, 10 * MB, "iPhone 6.9\" or 6.5\" portrait"),
    ("ipad_screenshot", lambda w, h: (w, h) in [(2064, 2752), (2048, 2732)], False, 10 * MB, "iPad 13\" portrait"),
    ("ios_icon", lambda w, h: (w, h) == (1024, 1024), False, 10 * MB, "1024x1024, no alpha"),
]

def main(d):
    bad = 0
    files = sorted(f for f in os.listdir(d) if f.lower().endswith((".png", ".jpg", ".jpeg")))
    for f in files:
        rule = next((r for r in RULES if f.startswith(r[0])), None)
        if not rule:
            continue
        p = os.path.join(d, f)
        im = Image.open(p)
        w, h = im.size
        has_alpha = im.mode in ("RGBA", "LA", "P")
        prefix, size_ok, want_alpha, max_bytes, label = rule
        problems = []
        if not size_ok(w, h):
            problems.append(f"size {w}x{h}, want {label}")
        if want_alpha and im.mode != "RGBA":
            problems.append(f"mode {im.mode}, want RGBA")
        if not want_alpha and has_alpha:
            problems.append(f"has alpha ({im.mode})")
        if os.path.getsize(p) > max_bytes:
            problems.append(f"{os.path.getsize(p) // 1024} KB over limit")
        print(("FAIL " if problems else "ok   ") + f"{f} {w}x{h} {im.mode}" + (": " + "; ".join(problems) if problems else ""))
        bad += bool(problems)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
