#!/usr/bin/env python3
"""Check store listing text against App Store and Google Play limits, then write fastlane metadata files.

Usage: python3 check_listing.py listing.json            # check only
       python3 check_listing.py listing.json --write    # check, then write fastlane/metadata/...
       python3 check_listing.py --selftest

listing.json: {"app": "QR Tap", "locales": {"en-US": {"ios": {...}, "play": {...}}, "vi": {...}}}
Field names and limits are in LIMITS. Leave out a store a locale doesn't ship to.
"""
import json, os, re, sys, tempfile, unicodedata

LIMITS = {  # characters, as App Store Connect and Play Console count them
    "ios": {"name": 30, "subtitle": 30, "keywords": 100, "promotional_text": 170,
            "description": 4000, "release_notes": 4000},
    "play": {"title": 30, "short_description": 80, "full_description": 4000, "release_notes": 500},
}
REQUIRED = {"ios": ["name", "description", "keywords"], "play": ["title", "short_description", "full_description"]}
# Play rejects these in title, icon and short description; Apple rejects price and ranking claims in metadata.
BANNED = re.compile(r"\b(#1|no\.? ?1|top|best|free|sale|discount|download now|install now)\b|[★☆✓✔]", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def words(s):
    return {w for w in re.split(r"[\s,]+", s.lower()) if w}


def check(listing):
    problems = []
    for loc, stores in listing["locales"].items():
        for store, fields in stores.items():
            if store not in LIMITS:
                problems.append(f"{loc}: unknown store '{store}' (use ios or play)")
                continue
            for f in REQUIRED[store]:
                if not fields.get(f, "").strip():
                    problems.append(f"{loc} {store}: missing {f}")
            for f, text in fields.items():
                where = f"{loc} {store} {f}"
                if f not in LIMITS[store]:
                    problems.append(f"{where}: unknown field")
                    continue
                n = len(unicodedata.normalize("NFC", text))
                if n > LIMITS[store][f]:
                    problems.append(f"{where}: {n} chars, limit {LIMITS[store][f]}")
                if f in ("name", "subtitle", "title", "short_description"):
                    if BANNED.search(text):
                        problems.append(f"{where}: promo or ranking word '{BANNED.search(text).group(0)}'")
                    if EMOJI.search(text):
                        problems.append(f"{where}: emoji")
                    if sum(w.isupper() and len(w) > 4 for w in text.split()) > 0:
                        problems.append(f"{where}: all-caps word")
            if store == "ios" and "keywords" in fields:
                kw = fields["keywords"]
                if ", " in kw:
                    problems.append(f"{loc} ios keywords: spaces after commas waste characters")
                repeated = words(kw) & (words(fields.get("name", "")) | words(fields.get("subtitle", "")))
                if repeated:
                    problems.append(f"{loc} ios keywords: repeat words already in name or subtitle: {', '.join(sorted(repeated))}")
    return problems


IOS_FILES = {"name": "name.txt", "subtitle": "subtitle.txt", "keywords": "keywords.txt",
             "promotional_text": "promotional_text.txt", "description": "description.txt",
             "release_notes": "release_notes.txt"}
PLAY_FILES = {"title": "title.txt", "short_description": "short_description.txt",
              "full_description": "full_description.txt", "release_notes": "changelogs/default.txt"}


def write(listing, root):
    out = []
    for loc, stores in listing["locales"].items():
        for store, fields in stores.items():
            base, names = ((f"fastlane/metadata/{loc}", IOS_FILES) if store == "ios"
                           else (f"fastlane/metadata/android/{loc}", PLAY_FILES))
            for f, text in fields.items():
                path = os.path.join(root, base, names[f])
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, "w").write(unicodedata.normalize("NFC", text).strip() + "\n")
                out.append(path)
    return out


def run(path, do_write):
    listing = json.load(open(path))
    problems = check(listing)
    for p in problems:
        print("FIX ", p)
    if problems:
        sys.exit(f"{len(problems)} problem(s)")
    for loc, stores in listing["locales"].items():
        for store, fields in stores.items():
            print(f"ok  {loc} {store}: " + ", ".join(f"{f} {len(t)}/{LIMITS[store][f]}" for f, t in fields.items()))
    if do_write:
        for p in write(listing, os.path.dirname(os.path.abspath(path))):
            print("wrote", p)


def selftest():
    good = {"app": "Test", "locales": {
        "en-US": {"ios": {"name": "QR Tap: Scan & Create", "subtitle": "Read any code in a second",
                          "keywords": "qrcode,barcode,reader,wifi,generator", "description": "Scan codes."},
                  "play": {"title": "QR Tap: Scan & Create", "short_description": "Scan any QR or barcode.",
                           "full_description": "Scan codes."}},
        "vi": {"play": {"title": "QR Tap: Quét mã nhanh", "short_description": "Quét mọi mã QR và mã vạch.",
                        "full_description": "Quét mã."}}}}
    assert check(good) == [], check(good)
    bad = {"app": "Test", "locales": {"en-US": {
        "ios": {"name": "Best QR Scanner app SCANS ever made for you", "keywords": "qr, scanner", "description": "x"},
        "play": {"title": "QR 🔥", "short_description": "x", "full_description": "x"}}}}
    found = "\n".join(check(bad))
    for expect in ["limit 30", "promo or ranking word", "all-caps", "spaces after commas", "repeat words", "emoji"]:
        assert expect in found, f"missed: {expect}\n{found}"
    d = tempfile.mkdtemp()
    files = write(good, d)
    assert os.path.exists(f"{d}/fastlane/metadata/android/vi/title.txt") and len(files) == 10, files
    print("selftest passed")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    selftest() if sys.argv[1] == "--selftest" else run(sys.argv[1], "--write" in sys.argv)
