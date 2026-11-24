---
name: storelisting-hagent
description: Build Google Play and/or Apple App Store listing packs from a Figma app design, including screenshots, icon, Play feature graphic and optional listing text, with visuals made by the OpenAI image generator from the real screens. Use whenever the user asks for store listing assets, ASO screenshots, a Play or App Store pack, a feature graphic or store icon, even if they only paste a Figma link and name a store.
---

# Store listing pack from a Figma design

The user hands over a Figma link to an app design and wants store-ready assets. Two standing preferences shape everything here:

- **The visuals are generated, not laid out.** Use the OpenAI image generator (the `omniroute-images` plugin, `model: gpt`, `quality: high`) and pass the real Figma screen as the reference, so each phone shows the actual UI inside a polished marketing scene. Plain frame-plus-text layouts are not what they want.
- **The words come from Figma, and they live in Figma.** Headlines and sublines are taken from the design's own copy (onboarding titles and bodies, feature labels, button text) rather than invented. Small grammar fixes are fine if you mention them.
- **Rule: never bake marketing text into a generated image.** Headlines, sublines, the app name or wordmark, taglines and badges are always added as live text layers in Figma, on top of text-free generated art. Generated text gets misspelled, can't be edited, and can't be translated; live Figma text can be fixed in seconds and reused for every language with the same art. The only text allowed in the generated image is the app's own UI inside the phone screen, copied from the reference screen.

- **Rule: show each feature at its best, never in a default or empty state.** A store screenshot sells the result. If the screen is about colors, the swatches are visibly colorful and one is selected. If it creates something, show the finished, attractive output: a colorful styled QR inside and out, a filled-in form, a populated list. Props around the phone must match what the screen shows. For example, a colored QR on screen means a colored QR on the floating card, not a plain black one. Black placeholder swatches, "Tap to add image" boxes, empty lists and lorem ipsum count as failures.
- **Rule: no real or confidential information, ever.** Design files are full of real data: the studio's own company name, client brands, real URLs and domains, emails, phone numbers, addresses, GPS coordinates, Wi-Fi network names, people's names and photos, account IDs. None of it may appear in store assets, whether in the phone UI, on props, or in the text. Replace each item with believable fictional data of the same kind: a made-up brand ("Bloom Café", "Northwind Studio"), a domain on example.com, a fictional number in the right local format (for example 555 in the US), a city-center location that isn't anyone's home, a network name like "Bloom_Guest". Keep one consistent fictional persona across the whole pack so the screens tell one story.

Specs per store are in `references/store-specs.md`, and the prompt patterns are in `references/prompt-templates.md`. Read both before generating.

## Step 0: Ask first, in one message

Before reading the file or generating anything, ask these together and wait for the answer (image generation is billed, so the scope should be agreed first):

1. **Stores:** Google Play, Apple App Store, or both?
2. **Assets:** the default is 5 phone screenshots, the icon, and the feature graphic (Play only). Add iPad / tablet screenshots? Skip the icon if the app already has a final one?
3. **Listing text:** also write the store text (Play: title, short and full description. App Store: name, subtitle, promotional text, description, keywords)?
4. **Languages:** English only, or others too (for example Vietnamese)? Each language multiplies the screenshots, so confirm.
5. **Where to save:** a folder on their Mac. The text is always added in their Figma file, so confirm which page the Store Pack section should go on.

Offer sensible defaults in the question ("If you just say go: both stores, 5 screenshots each, icon, feature graphic, English, no listing text") so a one-word reply works. Save the answers in project memory if the same app is likely to come back.

## Step 1: Read the design

- Get the fileKey and node-id from the URL and call Figma `create_session`. If access fails, call `whoami` and tell the user which account needs the file shared with it.
- `get_metadata` on the page: the output is large, so save it and extract the screen frames (phone-sized, for example 390-430 wide) with jq or grep.
- Run one read-only `use_figma` script that returns, per screen, its name, id and the visible text (deduped, skipping status-bar time digits), plus the solid fill colors and font families of a main screen. This gives the copy, the brand color and the screen list in one call.
- Check for existing marketing frames (names like "GF", "Feature", "Store", or 1024x500 frames). If you find one, screenshot it and use it as the style reference.
- Pick about 5 hero screens covering: the core action, creation or customization, results or detail, history or library, and the trust/onboarding promise. Pair each with a headline and subline from the copy.

## Step 1b: Stage the reference screens

The generator copies whatever the reference shows, so fix the content in Figma before taking any screenshots. Don't count on the prompt to fix it.

- In one `use_figma` call (load the figma-use skill first), duplicate the chosen screens into a scratch section named "Store Pack / staged refs", next to the Store Pack section. Never edit the originals.
- In the copies, replace every real or confidential item (rule above) with the fictional persona's data, and put each screen in its best state: pick real colors for color swatches and select one, give the QR or other output a colorful style, add a center image or logo where the feature offers it, and fill empty lists and history with varied, realistic fictional entries. Use the app's own components and variants where they exist.
- Return a list of every swap you made (real, then fictional) and include it in the final reply, so the user can check that nothing slipped through.
- Screenshot the staged copies, not the originals, in Step 2. Read them back once to confirm that no real names, domains, numbers or coordinates remain.

## Step 2: Get reference images onto the Mac

The generator's `reference_image` must be a path on the user's Mac.

- Screenshot each chosen screen with Figma `get_screenshot` and `enableBase64Response: true`. The PNG lands in the session's tool-results folder. (Direct figma.com asset URLs are usually blocked by the cloud proxy.)
- Copy them to `/mnt/project-files/<app>-store/refs/`, then `device_commit_files` them into the agreed Mac folder under `refs/`. Request folder access once if needed.
- For the icon, crop the app icon out of the splash or home screen.

## Step 3: Generate text-free art

- Screenshots: 1024x1536. Icon: 1024x1024. Feature graphic: 1536x1024.
- Every prompt says the art has no text outside the phone screen, and leaves clean, calm background where the text will go: the top ~30% of each screenshot, and the left ~45% of the feature graphic. See `references/prompt-templates.md`. Don't put the headline into the prompt at all, because generators tend to draw any quoted words.
- Play shots show an Android phone and App Store shots show an iPhone. Do the two stores as separate generations, because the device frame differs.
- Submit two jobs at a time (the plugin runs two concurrently), poll `fetch_image` about every 30 seconds, and never resubmit a job that is still running.
- Copy each finished image from tool-results to `/mnt/project-files/<app>-store/raw/` straight away.
- Look at every image. Regenerate if it has any text outside the phone (stray words, fake logos, labels on props), a busy or dark text area, invented UI labels, or a cut-off phone. Also regenerate if it has anything real or confidential (the generator sometimes brings back brand names or domains from memory), a feature shown in a dull default state, or props that don't match the screen. Name the problem in the new prompt.

## Step 4: Fit the art to exact sizes

```
python3 scripts/fit_asset.py play-shot raw/01.png art/play_screenshot_01_<topic>.png
python3 scripts/fit_asset.py ios-shot  raw/01_ios.png art/ios_screenshot_01_<topic>.png
python3 scripts/fit_asset.py play-icon raw/icon.png final/play_icon_512.png
python3 scripts/fit_asset.py ios-icon  raw/icon.png final/ios_icon_1024.png
python3 scripts/fit_asset.py play-fg   raw/feature.png art/play_feature_graphic_1024x500.png
```

The fit script trims a little from the sides and extends the background for the rest, because the generator's 2:3 output doesn't match 9:16 or the iPhone ratio. With `--anchor top`, all the extension goes above the phone, which gives the headline more room. Icons have no text, so they go straight to `final/`. Screenshots and the feature graphic go to `art/`, because they still need their text.

## Step 5: Add the text in Figma

Load the figma-use skill before any `use_figma` call.

1. **Frames.** On the design's page, below the existing content, create a section named "Store Pack". In it, create one frame per screenshot and one for the feature graphic, at exact store size (for example 1080x1920 or 1320x2868), named after the output file (`play_screenshot_01_scan`). Return the frame ids.
2. **Art as background.** Call `upload_assets` with those frame ids as `nodeIds` and `scaleMode: FILL`, to get single-use POST URLs (mcp.figma.com, valid for 10 minutes). The cloud container and the Cowork VM can't reach that host, so run the curl POSTs (`-H "Content-Type: image/png" --data-binary @file`) from the user's Mac through a Remote Control session in a folder they've approved. Create the URLs right before starting that session. Upload the real app icon the same way, into an image frame inside the feature graphic.
3. **Text layers.** In one `use_figma` call, add to each frame a vertical auto-layout "Copy" group, centered in the empty top area: a "Headline" text (the app's display font from Step 1, bold, near-black or the brand's dark color, about 6 to 7% of the frame width per line, at most 2 lines) and a "Subline" text (regular weight, dark gray, about 3.5%). For the feature graphic, put the icon, the app name and the tagline as text in the empty left area. Load each font with `listAvailableFontsAsync` / `loadFontAsync` first. Keep the text inside the store-safe margins, and make sure it doesn't overlap the phone.
4. **Check.** Screenshot the section (`get_screenshot`) and look for clipped or overlapping text and poor contrast on the art. Fix those before export.
5. **Other languages.** Duplicate the frames and replace only the text. The art is shared, which is the point of keeping text out of it. Name the copies with a locale suffix (`play_screenshot_01_scan_vi`).

## Step 6: Export and check

- Export each frame with `download_assets` (`defaultFormat: png`, `defaultScale: 1`), so the output is exactly the frame size. The returned URLs are on figma.com, which the cloud container can't reach. Download them on the user's Mac (Remote Control `curl -L -o`) into the pack's `final/` folder. Alternatively, ask the user to select the section in Figma and export at 1x.
- Run `python3 scripts/check_pack.py final/`. Keep the file-name prefixes, because the checker matches on them.
- Make a contact sheet of all the screenshots for the user.

## Step 7: Listing text (if requested)

Write it from the Figma copy and the screens, in a `listing.json` shaped like `{"app": "QR Tap", "locales": {"en-US": {"ios": {...}, "play": {...}}, "vi": {...}}}`. The field names and limits are in `scripts/check_listing.py` (`LIMITS`), and the store rules are in `references/store-specs.md`. Then run:

```
python3 scripts/check_listing.py listing.json           # limits, required fields, banned claims
python3 scripts/check_listing.py listing.json --write   # also writes fastlane/metadata/... text files
```

Fix every failure before delivering. The checker counts characters the way the store consoles do and flags phrases like "#1", "best" or "free" that Play and Apple reject.

## Step 8: Deliver

- Make sure `final/` is in the agreed Mac folder.
- In the reply, attach the contact sheet, the icon and the feature graphic (6 attachments at most per message), and link the Figma section where the text can be edited. Then list what each store got, the specs checked, where the copy came from, and any trade-offs, such as a copy fix.
