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

- **Rule: the UI on the phone must look correct and polished.** The screen inside the phone is the product, so layout bugs read as a buggy app. Primary buttons are full width (or exactly as the design system specifies) and centered. Elements are aligned to the same margins, nothing is clipped, and there are no large dead white areas. Placeholder values like "WiFi SSID", "Label" or "example" count as unfinished. Fix these in the staged copy (Step 1b) even if the original design has them, then check the generated phone screen for the same problems. Generators often shrink, shift or invent controls, so compare each one against the staged reference.

- **Rule: everything in the frame is on-brand.** Every visible object uses the app's brand colors (from Step 1) or warm neutrals (white, cream, wood, soft gray). That includes photos and products inside the phone screen, such as a camera viewfinder's subject, plus props and backgrounds. A strong off-brand color, like a purple package in an orange app, pulls the eye away from the product and makes the set look unplanned. If the design's own mock photo is off-brand, swap it in the staged copy, or tell the generator exactly which on-brand subject to show (for example "a cream coffee bag with an orange label").

- **Rule: the art always covers the whole frame.** The background art layer must reach every edge of the frame, with no strip of bare frame color showing at the top, bottom or sides. When you move or scale an art layer to tighten the layout, keep x <= 0, y <= 0, x + width >= frame width and y + height >= frame height, and check it in code after every change. To move the scene up or down, re-fit the art image itself (crop on one side, extend the other) rather than sliding the layer and leaving a gap. Also check that scaling hasn't cut off a prop or phone at the frame's edge.

- **Rule: vary the composition across the set.** Eight screenshots with the same centered phone under the same top headline read as monotone. Plan a different layout for each before generating: a hero shot with a big tilted phone bleeding off the edge, a close-up of the screen, a flat-lay scene, a prop-led shot where the result (for example the QR tile) is the hero, a diagonal arc of feature icons, a map or world scene. Alternate where the empty text zone sits (top, bottom, top-left) and match the text alignment to it. Keep the palette, lighting and type consistent so it still reads as one set.

- **Rule: headlines are short, one line, and have some life.** Write each headline to fit on one line (about 2 to 4 words), all at the same size across the set, with the key word in a brand-color gradient and a soft brand-colored glow or shadow. Pick a display font with character for the headline (not necessarily the app's UI font) and keep it consistent across the set. Always pair it with a readable subtitle: one line, about 4% of the frame width, semibold, in a dark warm color, never light gray. Keep the headline block close to the phone, without a large empty band in between.

- **Rule: headline sits in the top golden area.** Put the top edge of the copy block at about 6% of the canvas height (5 to 7%, about 115 px on a 1920 px screenshot), centered horizontally. Never center the copy vertically in the empty space above the phone; that pushes it too far from the top edge.

- **Rule: never crop.** No container may clip its content: copy groups, auto-layout frames and text with outlines or shadows must have clip content turned off, and nothing may be hidden by a parent's bounds. Fit generated art without trimming the sides (`--crop 0`), so no prop, card or device is cut at the canvas edge. Before delivery, audit every frame for clipped children (compare each node's absoluteRenderBounds with any clipping ancestor) and look for props touching the edges.

- **Rule: no repeated images, no IP.** Every screenshot shows a different subject (different drawings, photos and props across the whole pack, including thumbnails inside the phone). No copyrighted or brand characters or look-alikes, and no anime-style people, even if the app's own templates use them; swap in original, neutral subjects (animals, objects, places).

- **Hard rule: phone mockups have correct anatomy and aspect ratio.** A wrong phone is an automatic reject. The phone body must match a real device for the app's screen ratio: a 360x800 (9:20) screen sits in a body of about 1:2.05 to 1:2.15 (width:height), with thin even bezels, rounded corners matching the screen corners, one centered punch-hole camera and side buttons on one edge only. The screen UI must lie on the same plane as the body: every UI row stays parallel to the bezel edges, and nothing is wider, shorter or skewed differently from the glass. Image generators get this wrong in tilted or perspective shots (they paste the UI as a flat texture, so the bezel tilts one way while the text and cards tilt another, and the body comes out too wide or too short). So: (1) by default ask for the phone upright and facing the viewer, with "correct real phone proportions, 9:20 screen"; (2) use a tilted or perspective phone only if the screen is put on afterwards with a real perspective transform (Figma or PIL corner-pin onto the glass), never generator-drawn; (3) after every generation, measure the phone's bounding box (height / width must be within 5% of the target ratio, using the full phone, not a cropped part) and check that UI rows run parallel to the bezel; reject and regenerate anything that fails. Close-ups that crop the phone still need correct corners, bezel width and UI scale. (4) Every phone in a set must be the identical device: same body color, corner radius, bezel, camera and button side, at the same size. A generator draws a different phone each time, so never ship generator-drawn phones as a set. Generate each scene without a phone (props placed beside, not over, the phone area), then composite one standard phone frame with the polished screen inside it, at the same position and size in every shot.

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
- Replace any off-brand photo or mock content in the copies (camera subjects, product shots, avatars) with on-brand material, or note the subject to describe in the prompt.
- Also fix layout problems in the copies: make the primary call-to-action full width and centered, align elements to the screen margins, and fill dead space with relevant content.
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
- Look at every image. Regenerate if it has any text outside the phone (stray words, fake logos, labels on props), a busy or dark text area, invented UI labels, or a cut-off phone. Also regenerate if any object in the scene uses a strong off-brand color, if the phone UI drifts from the staged reference (a shrunken or off-center button, missing or extra tabs, invented controls), if it has anything real or confidential (the generator sometimes brings back brand names or domains from memory), a feature shown in a dull default state, or props that don't match the screen. Name the problem in the new prompt.

## Step 4: Fit the art to exact sizes

```
python3 scripts/fit_asset.py play-shot raw/01.png art/play_screenshot_01_<topic>.png --crop 0 --anchor top
python3 scripts/fit_asset.py ios-shot  raw/01_ios.png art/ios_screenshot_01_<topic>.png --crop 0 --anchor top
python3 scripts/fit_asset.py play-icon raw/icon.png final/play_icon_512.png
python3 scripts/fit_asset.py ios-icon  raw/icon.png final/ios_icon_1024.png
python3 scripts/fit_asset.py play-fg   raw/feature.png art/play_feature_graphic_1024x500.png
```

The fit script trims a little from the sides and extends the background for the rest, because the generator's 2:3 output doesn't match 9:16 or the iPhone ratio. With `--anchor top`, all the extension goes above the phone, which gives the headline more room. Icons have no text, so they go straight to `final/`. Screenshots and the feature graphic go to `art/`, because they still need their text.

## Step 5: Add the text in Figma

Load the figma-use skill before any `use_figma` call.

1. **Frames.** On the design's page, below the existing content, create a section named "Store Pack". In it, create one frame per screenshot and one for the feature graphic, at exact store size (for example 1080x1920 or 1320x2868), named after the output file (`play_screenshot_01_scan`). Return the frame ids.
2. **Art as background.** Call `upload_assets` with those frame ids as `nodeIds` and `scaleMode: FILL`, to get single-use POST URLs (mcp.figma.com, valid for 10 minutes). The cloud container and the Cowork VM can't reach that host, so run the curl POSTs (`-H "Content-Type: image/png" --data-binary @file`) from the user's Mac through a Remote Control session in a folder they've approved. Create the URLs right before starting that session. Upload the real app icon the same way, into an image frame inside the feature graphic.
3. **Text layers.** In one `use_figma` call, add to each frame a vertical auto-layout "Copy" group with clip content off, its top edge at about 6% of the frame height (the golden area rule above): a "Headline" text (one line, a display font with character, about 9% of the frame width, near-black with the key word in a brand gradient and a soft glow; see the headline rule) and a "Subline" text (one line, semibold, dark warm color, about 4%). For the feature graphic, put the icon, the app name and the tagline as text in the empty left area. Load each font with `listAvailableFontsAsync` / `loadFontAsync` first. Keep the text inside the store-safe margins, and make sure it doesn't overlap the phone.
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

- Before delivering, audit every asset against each rule at the top (no baked text, best state, no real data, polished UI, on-brand colors), and fix any failures. Include a one-line pass note per asset in the reply.

- Make sure `final/` is in the agreed Mac folder.
- In the reply, attach the contact sheet, the icon and the feature graphic (6 attachments at most per message), and link the Figma section where the text can be edited. Then list what each store got, the specs checked, where the copy came from, and any trade-offs, such as a copy fix.
