# Store specs (checked November 2026)

Re-check the official pages if a spec looks off: Play Console help "Add preview assets", and App Store Connect help "Screenshot specifications" / "App information".

## Google Play

| Asset | Size | Format | Notes |
|---|---|---|---|
| Phone screenshots | 1080x1920 (9:16) recommended; any side 320-3840px, long side at most 2x short side | JPEG or 24-bit PNG, no alpha, at most 8 MB | 2 to 8 per device type. At least 4 at 1080px+ in 9:16 makes the app eligible for promotion in recommendations. |
| 7"/10" tablet screenshots | e.g. 1200x1920 / 1600x2560 | same | Optional, only if the app supports tablets |
| App icon | 512x512 | 32-bit PNG with alpha, at most 1 MB | Full-bleed square. Google applies the mask (rounded corners, about 20% radius) and the shadow, so don't bake them in. Keep the mark in the central ~70%. |
| Feature graphic | 1024x500 | JPEG or 24-bit PNG, no alpha, at most 15 MB | Shown behind the promo video and in some placements. Keep text and key art away from the edges, because it can be cropped. |

Text limits: app name 30 chars, short description 80, full description 4000. No emoji or ALL CAPS in the title, and no ranking or price claims ("#1", "free", "best") in the title, icon or screenshots.

## Apple App Store

| Asset | Size (portrait) | Format | Notes |
|---|---|---|---|
| iPhone 6.9" screenshots (required) | 1320x2868 (also accepted: 1290x2796) | PNG or JPEG, no alpha | 1 to 10. Smaller iPhone sizes are scaled down from this one automatically. |
| iPhone 6.5" (optional fallback) | 1242x2688 or 1284x2778 | same | Only needed if 6.9" isn't provided |
| iPad 13" (required if the app runs on iPad) | 2064x2752 (also accepted: 2048x2732) | same | 1 to 10 |
| App icon | 1024x1024 | PNG, **no alpha**, no rounded corners | Supplied in the app binary / asset catalog. Apple applies the mask. |

There is no feature graphic on the App Store. The optional App Preview video is out of scope for this skill.

Text limits: app name 30 chars, subtitle 30, promotional text 170 (can change without a new version), description 4000, keywords 100 bytes (comma-separated, no spaces after commas, don't repeat words already in the name). "What's New" is 4000.

## Generator output, mapped to stores

| Target | Generate at | Fit with `scripts/fit_asset.py` |
|---|---|---|
| Play screenshot | 1024x1536 | `play-shot` (trims about 4% per side, extends the top and bottom) |
| iPhone screenshot | 1024x1536 | `ios-shot` (trims about 8% per side, extends the top and bottom). Ask for 16% side margins in the prompt. |
| iPad screenshot | 1024x1536 | `ipad-shot` (trims about 6% top and bottom, extends the sides). Keep the top and bottom 8% clear. |
| Play icon | 1024x1024 | `play-icon` |
| iOS icon | 1024x1024 | `ios-icon` |
| Feature graphic | 1536x1024 | `play-fg` (center crop). Keep content in the middle 70% of the height. |
