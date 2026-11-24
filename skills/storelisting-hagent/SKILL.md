---
name: storelisting-hagent
description: Build Google Play and/or Apple App Store listing packs from a Figma app design, including screenshots, icon, Play feature graphic and optional listing text, with visuals made by the OpenAI image generator from the real screens. Use whenever the user asks for store listing assets, ASO screenshots, a Play or App Store pack, a feature graphic or store icon, even if they only paste a Figma link and name a store.
---

# Store listing pack from a Figma design

The user hands over a Figma link to an app design and wants store-ready assets. Two standing preferences shape everything here:

- **The visuals are generated, not laid out.** Use the OpenAI image generator (the `omniroute-images` plugin, `model: gpt`, `quality: high`) and pass the real Figma screen as the reference, so each phone shows the actual UI inside a polished marketing scene. Plain frame-plus-text layouts are not what they want.
- **The words come from Figma.** Headlines and sublines are taken from the design's own copy (onboarding titles and bodies, feature labels, button text) rather than invented. Small grammar fixes are fine if you mention them.

Specs per store are in `references/store-specs.md`, and the prompt patterns are in `references/prompt-templates.md`. Read both before generating.

## Step 0: Ask first, in one message

Before reading the file or generating anything, ask these together and wait for the answer (image generation is billed, so the scope should be agreed first):

1. **Stores:** Google Play, Apple App Store, or both?
2. **Assets:** the default is 5 phone screenshots, the icon, and the feature graphic (Play only). Add iPad / tablet screenshots? Skip the icon if the app already has a final one?
3. **Listing text:** also write the store text (Play: title, short and full description. App Store: name, subtitle, promotional text, description, keywords)?
4. **Languages:** English only, or others too (for example Vietnamese)? Each language multiplies the screenshots, so confirm.
5. **Where to save:** a folder on their Mac, and whether to place the results in the Figma file too.

Offer sensible defaults in the question ("If you just say go: both stores, 5 screenshots each, icon, feature graphic, English, no listing text") so a one-word reply works. Save the answers in project memory if the same app is likely to come back.

## Step 1: Read the design

- Get the fileKey and node-id from the URL and call Figma `create_session`. If access fails, call `whoami` and tell the user which account needs the file shared with it.
- `get_metadata` on the page: the output is large, so save it and extract the screen frames (phone-sized, for example 390-430 wide) with jq or grep.
- Run one read-only `use_figma` script that returns, per screen, its name, id and the visible text (deduped, skipping status-bar time digits), plus the solid fill colors and font families of a main screen. This gives the copy, the brand color and the screen list in one call.
- Check for existing marketing frames (names like "GF", "Feature", "Store", or 1024x500 frames). If you find one, screenshot it and use it as the style reference.
- Pick about 5 hero screens covering: the core action, creation or customization, results or detail, history or library, and the trust/onboarding promise. Pair each with a headline and subline from the copy.

## Step 2: Get reference images onto the Mac

The generator's `reference_image` must be a path on the user's Mac.

- Screenshot each chosen screen with Figma `get_screenshot` and `enableBase64Response: true`. The PNG lands in the session's tool-results folder. (Direct figma.com asset URLs are usually blocked by the cloud proxy.)
- Copy them to `/mnt/project-files/<app>-store/refs/`, then `device_commit_files` them into the agreed Mac folder under `refs/`. Request folder access once if needed.
- For the icon, crop the app icon out of the splash or home screen.

## Step 3: Generate

- Screenshots: 1024x1536. Icon: 1024x1024. Feature graphic: 1536x1024.
- Play shots show an Android phone and App Store shots show an iPhone. Do the two stores as separate generations, because the device frame differs.
- Submit two jobs at a time (the plugin runs two concurrently), poll `fetch_image` about every 30 seconds, and never resubmit a job that is still running.
- Copy each finished image from tool-results to `/mnt/project-files/<app>-store/raw/` straight away.
- Look at every image: misspelled headline, invented UI labels, a cut-off phone, text too close to the side edges. Regenerate only the failures, with the problem named in the prompt.

## Step 4: Fit to exact sizes and check

```
python3 scripts/fit_asset.py play-shot raw/01.png final/play_screenshot_01_<topic>.png
python3 scripts/fit_asset.py ios-shot  raw/01_ios.png final/ios_screenshot_01_<topic>.png
python3 scripts/fit_asset.py play-icon raw/icon.png final/play_icon_512.png
python3 scripts/fit_asset.py ios-icon  raw/icon.png final/ios_icon_1024.png
python3 scripts/fit_asset.py play-fg   raw/feature.png final/play_feature_graphic_1024x500.png
python3 scripts/check_pack.py final/
```

The fit script trims a little from the sides and extends the background for the rest, because the generator's 2:3 output doesn't match 9:16 or the iPhone ratio and plain cropping cuts headlines. Keep the file-name prefixes, because `check_pack.py` matches on them. View one fitted screenshot per store before moving on, and make a contact sheet of all the screenshots for the user.

## Step 5: Listing text (if requested)

Write it from the Figma copy and the screens, in a `listing.json` shaped like `{"app": "QR Tap", "locales": {"en-US": {"ios": {...}, "play": {...}}, "vi": {...}}}`. The field names and limits are in `scripts/check_listing.py` (`LIMITS`), and the store rules are in `references/store-specs.md`. Then run:

```
python3 scripts/check_listing.py listing.json           # limits, required fields, banned claims
python3 scripts/check_listing.py listing.json --write   # also writes fastlane/metadata/... text files
```

Fix every failure before delivering. The checker counts characters the way the store consoles do and flags phrases like "#1", "best" or "free" that Play and Apple reject.

## Step 6: Deliver

- Commit `final/` to the Mac folder.
- In the reply, attach the contact sheet, the icon and the feature graphic (6 attachments at most per message). Then list what each store got, the specs checked, where the copy came from, and any trade-offs, such as how the 9:16 fit was done or a copy fix.

## Step 7: Optional, place in Figma

- With one `use_figma` call (load the figma-use skill first), create a section named "Store Pack (AI generated)" below the existing content on the same page, with one frame per asset at its exact size. Return the frame ids.
- `upload_assets` with those `nodeIds` returns single-use POST URLs on mcp.figma.com that expire after 10 minutes. The cloud container and the Cowork VM can't reach that host, so run the curl POSTs (`-H "Content-Type: image/png" --data-binary @file`) from the user's Mac through a Remote Control session in a folder they've approved. Create the URLs right before starting that session.
- Confirm with `get_screenshot` of the section and share it.
