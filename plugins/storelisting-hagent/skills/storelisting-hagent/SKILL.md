---
name: storelisting-hagent
description: Build Google Play and/or Apple App Store listing packs from a Figma app design, including screenshots, icon, Play feature graphic and optional listing text, with visuals made by the OpenAI image generator from the real screens. Use whenever the user asks for store listing assets, ASO screenshots, a Play or App Store pack, a feature graphic or store icon, even if they only paste a Figma link and name a store.
---

# Store listing pack from a Figma design

The user hands over a Figma link to an app design and wants store-ready assets. Two standing preferences shape everything here:

- **The visuals are generated, not laid out.** Use the OpenAI image generator (the `omniroute-images` plugin, `model: gpt`, `quality: high`) and pass the real Figma screen as the reference, so each phone shows the actual UI inside a polished marketing scene. Plain frame-plus-text layouts are not what they want.
- **The words come from Figma, and they live in Figma.** Headlines are taken from the design's own copy (onboarding titles and bodies, feature labels, button text) rather than invented. Small grammar fixes are fine if you mention them.
- **Hard rule: the user's concrete preferences win; this skill only fills the gaps.** The point of this skill is to use what the user has already decided instead of guessing. Those decisions live in the file (pages or frames like "Visual Concept", "App Visual", "Visual direction", "Style tile", "Moodboard", "Art direction", "Brand", "Character style lock", or the user's link), in the brief, in what they say in chat, and in memory of past feedback on this app. Read all of them in Step 1, before writing any prompt, and follow them for the background, the palette (exact hex values), the fonts, the props and characters (who appears, the cast, and how they are drawn: 3D, flat, risograph, illustration, photo), the light, the mood and everything they rule out. They win over a dataset pack, the templates and every default rule in this skill (including the headline colors and pill, prop style and "neutral subjects instead of people"), and over your own taste and over earlier packs. If a rule below conflicts with a stated preference, follow the preference and tell the user which rule you set aside. If the file has no direction, ask for it or for a few words before generating. If you can't open the file, stop and ask; never generate from a brief or a pack alone. When the user asks for something new mid-run (for example "add characters"), look for that element in the direction first (a cast or character page) before drawing it any other way.

- **Rule: never bake marketing text into a generated image.** Headlines, the app name or wordmark, taglines and badges are always added as live text layers in Figma, on top of text-free generated art. Generated text gets misspelled, can't be edited, and can't be translated; live Figma text can be fixed in seconds and reused for every language with the same art. The only text allowed in the generated image is the app's own UI inside the phone screen, copied from the reference screen.

- **Rule: show each feature at its best, never in a default or empty state.** A store screenshot sells the result. If the screen is about colors, the swatches are visibly colorful and one is selected. If it creates something, show the finished, attractive output: a colorful styled QR inside and out, a filled-in form, a populated list. Props around the phone must match what the screen shows. For example, a colored QR on screen means a colored QR on the floating card, not a plain black one. Black placeholder swatches, "Tap to add image" boxes, empty lists and lorem ipsum count as failures.
- **Rule: no real or confidential information, ever.** Design files are full of real data: the studio's own company name, client brands, real URLs and domains, emails, phone numbers, addresses, GPS coordinates, Wi-Fi network names, people's names and photos, account IDs. None of it may appear in store assets, whether in the phone UI, on props, or in the text. Replace each item with believable fictional data of the same kind: a made-up brand ("Bloom Café", "Northwind Studio"), a domain on example.com, a fictional number in the right local format (for example 555 in the US), a city-center location that isn't anyone's home, a network name like "Bloom_Guest". Keep one consistent fictional persona across the whole pack so the screens tell one story.

- **Rule: the UI on the phone must look correct and polished.** The screen inside the phone is the product, so layout bugs read as a buggy app. Primary buttons are full width (or exactly as the design system specifies) and centered. Elements are aligned to the same margins, nothing is clipped, and there are no large dead white areas. Placeholder values like "WiFi SSID", "Label" or "example" count as unfinished. Fix these in the staged copy (Step 1b) even if the original design has them, then check the generated phone screen for the same problems. Generators often shrink, shift or invent controls, so compare each one against the staged reference.

- **Rule: everything in the frame is on-brand.** Every visible object uses the app's brand colors or warm neutrals (white, cream, wood, soft gray). When the file defines a palette (App Color variables or listed hex values), use exactly those values, not colors sampled from the screens or taken from a dataset brief. That includes photos and products inside the phone screen, such as a camera viewfinder's subject, plus props and backgrounds. A strong off-brand color, like a purple package in an orange app, pulls the eye away from the product and makes the set look unplanned. If the design's own mock photo is off-brand, swap it in the staged copy, or tell the generator exactly which on-brand subject to show (for example "a cream coffee bag with an orange label").

- **Rule: the art always covers the whole frame.** The background art layer must reach every edge of the frame, with no strip of bare frame color showing at the top, bottom or sides. When you move or scale an art layer to tighten the layout, keep x <= 0, y <= 0, x + width >= frame width and y + height >= frame height, and check it in code after every change. To move the scene up or down, re-fit the art image itself (crop on one side, extend the other) rather than sliding the layer and leaving a gap. Also check that scaling hasn't cut off a prop or phone at the frame's edge.

- **Rule: vary the composition across the set.** Eight screenshots with the same centered phone under the same top headline read as monotone. Plan a different layout for each before generating: a hero shot with a big tilted phone bleeding off the edge, a close-up of the screen, a flat-lay scene, a prop-led shot where the result (for example the QR tile) is the hero, a diagonal arc of feature icons, a map or world scene. Alternate where the empty text zone sits (top, bottom, top-left) and match the text alignment to it. Keep the palette, lighting and type consistent so it still reads as one set. Mix in **freestyle slides** with no phone: big characters or a scene with floating live-UI bubbles and cards (an avatar with a name, a star count, a notification card) built in Figma. About one slide in three works well. Take layouts from varied dataset packs; tilts stay gentle (6° or less), and the screen always stays fully inside the frame.

- **Rule: scenes tell small stories.** When the app has people or characters (its own cast, see the IP rule), show them using the feature: a parent and child following steps, a high-five at the school gate, a grandparent setting a reminder. Vary the scenes across the set (indoor and outdoor, morning and night, different ages and settings), and make each headline match its scene.

- **Rule: no subline; a two-line headline that explains itself.** There is no subtitle. The headline alone must say what the feature does for the user, in two short lines (a feature noun plus its benefit, about 4 to 7 words, for example "Steps kids can / follow alone" or "Set a reminder / for any step"), with a manual line break so the lines are balanced. Use the heading font the file sets (only when it sets none, pick a display font with character), at about 9% of the frame width, the same size on every slide. By default the text is the palette's dark cool color (navy, not warm brown: brown on a warm peach background reads muddy even at high contrast), and the key word sits on a high-contrast pill in the file's accent color (for example cream text on a terracotta pill tilted about −3°). No gradient and no glow unless the preferences ask for them.

- **Rule: an icon from the app's own set next to the headline.** Put one instance of the app's own icon components (for example `Icon/...` in its Figma file) next to the shorter headline line, chosen to match the slide (an alarm clock for a timer, a trophy for rewards), about 11 to 13% of the frame width, tilted 10 to 14°, at least 45 px from the frame edges. Never draw or generate a substitute icon.

- **Rule: keep every element on its own Figma layer.** Each screenshot frame holds separate layers: the background scene (text-free and phone-free), the phone as a Figma object (Body, Rim and a clipped Screen with the staged screen as an image fill), floating live-UI bubbles, the live headline text and the icon instance. Never bake the phone, the UI bubbles or the text into the background image, so each one can be moved, resized or swapped later.

- **Rule: headline sits in the top golden area.** Put the top edge of the copy block at about 6% of the canvas height (5 to 7%, about 115 px on a 1920 px screenshot), centered horizontally. Never center the copy vertically in the empty space above the phone; that pushes it too far from the top edge.
- **Rule: no dead space above or below the scene.** The phone (or first key prop or bubble) starts about 50 to 80 px below the headline's second line (content top at about 20% of a 1920 px canvas), and the scene reaches the bottom edge: no empty band of plain background, table or waves at the bottom either. With the layered method `compose_phone.py` already places the phone this way. Only for a one-off image with a generator-drawn phone: a 9:16 frame needs a big phone, so ask the generator (editing a 9:16 reference, it returns about 941x1672) for "a tall 9:16 portrait; the phone spans about 60 to 64% of the image width, top edge at about 22% and bottom edge at about 96% of the image height, body about 2.1 times as tall as wide; props smaller, tucked beside the phone and fully inside the image; top 20% plain background". Then scale to 1080 wide, put the content top just under the headline, and only stretch a few rows of plain background if a small gap (under about 100 px) is left. Never fill a big gap with stretched or flat background, and never cut a prop. Measure the phone body ratio after every edit; these edits often break it.

- **Rule: never crop.** No container may clip its content: copy groups, auto-layout frames and text with outlines or shadows must have clip content turned off, and nothing may be hidden by a parent's bounds. Fit generated art without trimming the sides (`--crop 0`), so no prop, card or device is cut at the canvas edge. Before delivery, audit every frame for clipped children (compare each node's absoluteRenderBounds with any clipping ancestor) and look for props touching the edges.

- **Rule: no repeated images, no IP.** Every screenshot shows a different subject (different drawings, photos and props across the whole pack, including thumbnails inside the phone). No copyrighted or brand characters or look-alikes, and no anime-style people, even if the app's own templates use them; swap in original, neutral subjects (animals, objects, places). If the file defines its own original cast (a character page or style lock), use only those characters, drawn in that style, and never invent new people.

- **Hard rule: phone mockups have correct anatomy and aspect ratio.** A wrong phone is an automatic reject. The phone body must match a real device for the app's screen ratio: a 360x800 (9:20) screen sits in a body of about 1:2.05 to 1:2.15 (width:height), with thin even bezels, rounded corners matching the screen corners, one centered punch-hole camera and side buttons on one edge only. The screen UI must lie on the same plane as the body: every UI row stays parallel to the bezel edges, and nothing is wider, shorter or skewed differently from the glass. Image generators get this wrong in tilted or perspective shots (they paste the UI as a flat texture, so the bezel tilts one way while the text and cards tilt another, and the body comes out too wide or too short). So: (1) by default ask for the phone upright and facing the viewer, with "correct real phone proportions, 9:20 screen"; (2) use a tilted or perspective phone only if the screen is put on afterwards with a real perspective transform (Figma or PIL corner-pin onto the glass), never generator-drawn; (3) after every generation, measure the phone's bounding box (height / width must be within 5% of the target ratio, using the full phone, not a cropped part) and check that UI rows run parallel to the bezel; reject and regenerate anything that fails. Close-ups that crop the phone still need correct corners, bezel width and UI scale. (4) Every phone in a set must be the identical device: same body color, corner radius, bezel, camera and button side, at the same size. A generator draws a different phone each time, so never ship generator-drawn phones as a set. Generate each scene without a phone (props placed beside, not over, the phone area), then add one standard phone with the polished screen inside it, at the same size in every shot. Use `scripts/compose_phone.py` (Step 4) for the geometry and the preview; in Figma the phone is rebuilt as its own object at that geometry (layer rule above), so the set can't drift.

Specs per store are in `references/store-specs.md`, and the prompt patterns are in `references/prompt-templates.md`. Read both before generating.

## Step 0: Ask first, in one message

Before reading the file or generating anything, ask these together and wait for the answer (image generation is billed, so the scope should be agreed first):

1. **Stores:** Google Play, Apple App Store, or both?
2. **Assets:** the default is 5 phone screenshots, the icon, and the feature graphic (Play only). Add iPad / tablet screenshots? Skip the icon if the app already has a final one?
3. **Listing text:** also write the store text (Play: title, short and full description. App Store: name, subtitle, promotional text, description, keywords)?
4. **Languages:** English only, or others too (for example Vietnamese)? Each language multiplies the screenshots, so confirm.
5. **Where to save:** a folder on their Mac. The text is always added in their Figma file, so confirm which page the Store Pack section should go on.
6. **Visual direction:** which page or frame in the file sets the look for the art (link)? If there is none yet, a few words are enough (for example "soft 3D toys, cream and butter yellow, calm").

Offer sensible defaults in the question ("If you just say go: both stores, 5 screenshots each, icon, feature graphic, English, no listing text") so a one-word reply works. Save the answers in project memory if the same app is likely to come back.

## Step 1: Read the design

- Get the fileKey and node-id from the URL and call Figma `create_session`. If access fails, call `whoami` and tell the user which account needs the file shared with it.
- `get_metadata` on the page: the output is large, so save it and extract the screen frames (phone-sized, for example 390-430 wide) with jq or grep.
- Run one read-only `use_figma` script that returns, per screen, its name, id and the visible text (deduped, skipping status-bar time digits), plus the solid fill colors and font families of a main screen. This gives the copy, the brand color and the screen list in one call.
- Read the visual direction (hard rule above): list the file's pages (`get_metadata` without a node id) and look for a page or frame named like "Visual Concept", "App Visual", "Visual direction", "Style tile", "Moodboard", "Art direction" or "Character style lock", or use the one the user linked. Dump all of its text with one read-only `use_figma` call (notes are often in another language; read them all) and screenshot it into `refs/visual_direction.png`.
- Write `refs/preferences.md`: a checklist of every concrete preference, copied word for word, not summarized: exact palette hex values and their roles, fonts, background, how props and characters are drawn, the allowed cast (names, looks, details such as glasses, hearing aids, wheelchairs), light, mood, and a "Banned" list (for example glow, sparkles, floating objects, outlines, clothes in the background's colors). Add what the user said in chat and past feedback from memory, and mark which skill defaults it overrides. A one-line summary is not enough: it loses the details, and they are what the user cares about.
- Re-read `refs/preferences.md` before each batch of prompts (also after a context reset), and paste its palette hex values, style words and bans into every prompt in Steps 3 and 4.
- Check for existing marketing frames (names like "GF", "Feature", "Store", or 1024x500 frames). If you find one, screenshot it and use it as the style reference.
- Pick about 5 hero screens covering: the core action, creation or customization, results or detail, history or library, and the trust/onboarding promise. Pair each with a two-line headline from the copy and decide which slides are freestyle (no phone).
- List the app's own icon components (names like `Icon/...`) with their ids, and pick one per slide for the headline icon.

## Step 1b: Stage the reference screens

The generator copies whatever the reference shows, so fix the content in Figma before taking any screenshots. Don't count on the prompt to fix it.

- In one `use_figma` call (load the figma-use skill first), duplicate the chosen screens into a scratch section named "Store Pack / staged refs", next to the Store Pack section. Never edit the originals.
- In the copies, replace every real or confidential item (rule above) with the fictional persona's data, and put each screen in its best state: pick real colors for color swatches and select one, give the QR or other output a colorful style, add a center image or logo where the feature offers it, and fill empty lists and history with varied, realistic fictional entries. Use the app's own components and variants where they exist.
- Return a list of every swap you made (real, then fictional) and include it in the final reply, so the user can check that nothing slipped through.
- Replace any off-brand photo or mock content in the copies (camera subjects, product shots, avatars) with on-brand material, or note the subject to describe in the prompt.
- Also fix layout problems in the copies: make the primary call-to-action full width and centered, align elements to the screen margins, and fill dead space with relevant content.
- Screenshot the staged copies, not the originals, in Step 2. Read them back once to confirm that no real names, domains, numbers or coordinates remain.

## Step 1c: Pick a style from the private pattern dataset (optional)

Only when the user has a private pattern dataset on their Mac and the env var `STORELISTING_DATASET` (or the user's message) points to its folder. The dataset is never copied into this plugin or its repo: only the folder path is read, at run time. Without it, skip this step and use `references/prompt-templates.md`.

1. Write a brief JSON from Step 1 (app name, 3 brand colors taken from `refs/preferences.md` when the file defines a palette, otherwise from the design, 3 to 4 moods, `needs_screen: true`, `platform`, `slides`, `slide_roles`, optional `archetype`). Take the moods, `slide_bg` (main background color per slide) and `slide_props` (simple original props, no characters) from the visual direction whenever it sets them; leave them out only where it is silent, and the pack fills those in.
2. Run `python3 $STORELISTING_DATASET/scripts/retrieve.py brief.json -k 6`. Show the user the top 3 with their strip (`dataset/packs/<id>/strip.png`) and let them pick, or use the user's shortlist from `picker.html`. A pack marked `ip_sensitive` is a spec source only.
3. Run `python3 $STORELISTING_DATASET/scripts/compile.py brief.json --pack <id> [--style-from A --layout-from B] --no-device -o compiled.json`. Per slide it writes `gpt_prompt` (the scene: no phone, no props, the phone area left plain where `scripts/compose_phone.py` puts the phone on a Play shot) and `prop_prompt` (the props edit for Step 4).
4. Use each `gpt_prompt` in Step 3 and each `prop_prompt` in Step 4 in place of the template prompts. Check both against the visual direction first and change anything that contradicts it (for example a pack's flat sticker props when the direction asks for soft 3D toys, or a solid saturated background when it asks for calm tints). Also remove words that don't fit the app.
5. Build a moodboard for the brief: `python3 $STORELISTING_DATASET/scripts/moodboard.py brief.json -o moodboard/ [-k 6] [--extra refs/visual_direction.png]`. It weights the best-fitting packs (impact %), skips `ip_sensitive` packs, and writes `moodboard_labeled.png` (show this one to the user) and `moodboard_ref.png` (no labels, for the generator). Pass `--extra` with the app's own cast sheet or style sample so the app's look stays in charge.
6. The only dataset image that may go to the generator is `moodboard_ref.png` (owner decision, 2026-11-26), as the style reference for the scenes. The prompt must say to borrow composition, energy and color balance only, and never copy a template's characters, logos, text, UI or exact layout. Never attach the strips or single pack screenshots. Record the pack ids and their impact % in the final reply.

## Step 2: Get reference images onto the Mac

The generator's `reference_image` must be a path on the user's Mac.

- Screenshot each chosen screen with Figma `get_screenshot` and `enableBase64Response: true`. The PNG lands in the session's tool-results folder. (Direct figma.com asset URLs are usually blocked by the cloud proxy.)
- Copy them to `/mnt/project-files/<app>-store/refs/`, then `device_commit_files` them into the agreed Mac folder under `refs/`. Request folder access once if needed.
- For the icon, crop the app icon out of the splash or home screen.

## Step 3: Generate text-free art

Screenshots use the layered method: the generator makes the scenes and later draws the props into the finished shot, and the phone is never generator-drawn (hard rule 4). Per pack:

1. **One scene per screenshot, with no phone and no props.** Follow the visual direction. A scene is a `generate_image` call with no screen in it (the real screen goes in later, as the Figma phone); its only reference image is the moodboard from Step 1c when there is one. Characters from the app's cast are drawn into the scene, acting out the slide's story. Freestyle slides get a scene with no phone area, leaving room for the floating UI bubbles instead. One shared style block for the whole set (same background family, never a flat fill: a soft tonal gradient, a faint texture such as a dot grid, broad brand-color waves or shapes in the lower part, studio light), and vary only the layout of the shapes (waves sweeping left or right, a different environment per slide if the app suits it). Keep the top ~26% calm and empty, and the phone column (x 20 to 80%, y 26 to 98%) plain.
2. **Props come in Step 4**, drawn by the generator into the composed shot (scene plus phone plus real screen), so they share its light and cast real shadows on the ground and the phone. Pick one hero prop per screen that echoes what the screen does (an alarm clock for a routine list, a stopwatch for a timer, a link or Wi-Fi tile for a QR result), drawn the way the visual direction says. A cut-out decor kit sheet (`references/prompt-templates.md`, `scripts/cut_kit.py`) is only a fallback, for the icon and feature graphic or when the in-context edit keeps failing: pasted cut-outs look stuck on, with flat shadows and mismatched light.
3. Save every prompt with its reference and size in `prompts.json` next to `raw/`, so any shot can be reproduced.

- Sizes: scenes 1024x1536 (they often come back 941x1672; the compositor cover-fits either). Icon: 1024x1024. Feature graphic: 1536x1024.
- Every prompt says the art has no text outside the phone screen, and leaves clean, calm background where the text will go: the top ~30% of each screenshot, and the left ~45% of the feature graphic. See `references/prompt-templates.md`. Don't put the headline into the prompt at all, because generators tend to draw any quoted words.
- Play shots show an Android phone and App Store shots show an iPhone. Do the two stores as separate generations, because the device frame differs.
- Submit two jobs at a time (the plugin runs two concurrently), poll `fetch_image` about every 30 seconds, and never resubmit a job that is still running.
- Copy each finished image from tool-results to `/mnt/project-files/<app>-store/raw/` straight away.
- Look at every image. Regenerate if it has any text outside the phone (stray words, fake logos, labels on props), a busy or dark text area, invented UI labels, or a cut-off phone. Also regenerate if any object in the scene uses a strong off-brand color, if the phone UI drifts from the staged reference (a shrunken or off-center button, missing or extra tabs, invented controls), if it has anything real or confidential (the generator sometimes brings back brand names or domains from memory), a feature shown in a dull default state, or props that don't match the screen. Name the problem in the new prompt.

## Step 4: Compose the screenshots, fit the rest

Screenshots (layered method):

```
python3 scripts/compose_phone.py play-shot raw/01_scene.png refs/01_staged.png art/01_play_shot.png --body "#6A3E1E" --edit-crop art/01_play_crop.png
#   then edit_reference_image: reference art/01_play_crop.png, the "Props in context" prompt, 1024x1536 -> raw/01_play_props.png
python3 scripts/merge_props.py art/01_play_shot.png raw/01_play_props.png art/play_screenshot_01_<topic>.png art/01_play_crop.json
```

- The phone is the same on every shot of a store: centered, from 26.3% to 97.5% of the height (60% of the width on Play; on the taller iOS canvas it is capped at 70% and starts lower). `--body` is the bezel color, usually a dark brand neutral. `--edit-crop` also writes the bottom 2:3 of the shot (the size the generator edits) and a `.json` saying where it and the screen sit.
- The props prompt asks for exactly one hero prop plus up to two small accents, placed just outside the phone next to a lower corner and touching the outer frame at most. The frame is only a few pixels wide, so "overlap the frame" makes the generator put props on the screen. 3D props get contact shadows on the ground and the frame; flat sticker or illustration props stay flat, as the visual direction says.
- `merge_props.py` keeps only what the edit added (the props and their shadows) and leaves the phone and the real screen exactly as composed. Exit 2 means a prop landed on the screen, exit 3 means nothing usable was added: redo that edit and name the problem in the prompt. After two failed tries, use the kit fallback for that shot.
- Do the crop, edit and merge once per store, because the iPhone is bigger and sits lower.
- Kit fallback: `python3 scripts/cut_kit.py raw/kit.png kit/`, then `compose_phone.py ... --props layout.json`, where the layout places props as fractions of the canvas (`[{"img": "kit/prop_0.png", "cx": 0.116, "by": 0.956, "w": 0.222, "layer": "front"}]`; front props may cover the bezel and the screen's outer margin only, and the script refuses anything further in or cut at the canvas edge).
- Look at the composed set side by side against the visual direction before Step 5: one background family, matching props, nothing on the screen.
- The composed PNG is a preview and the source of the geometry. What goes to Figma is the scene (or, when props were drawn in context, the merged image, since the Figma phone sits exactly over its composited phone) plus the phone geometry: write each slide's phone size, tilt and center to `layers/geo.json` for Step 5.

Icon and feature graphic:

```
python3 scripts/fit_asset.py play-shot raw/01.png art/play_screenshot_01_<topic>.png --crop 0 --anchor top
python3 scripts/fit_asset.py ios-shot  raw/01_ios.png art/ios_screenshot_01_<topic>.png --crop 0 --anchor top
python3 scripts/fit_asset.py play-icon raw/icon.png final/play_icon_512.png
python3 scripts/fit_asset.py ios-icon  raw/icon.png final/ios_icon_1024.png
python3 scripts/fit_asset.py play-fg   raw/feature.png art/play_feature_graphic_1024x500.png
```

The fit script trims a little from the sides and extends the background for the rest, because the generator's 2:3 output doesn't match 9:16 or the iPhone ratio. With `--anchor top`, all the extension goes above the phone, which gives the headline more room. Use it for the icon, the feature graphic, and any single-image screenshot made the old way. Icons have no text, so they go straight to `final/`. Screenshots and the feature graphic go to `art/`, because they still need their text.

## Step 5: Add the text in Figma

Load the figma-use skill before any `use_figma` call.

1. **Frames.** On the design's page, below the existing content, create a section named "Store Pack". In it, create one frame per screenshot and one for the feature graphic, at exact store size (for example 1080x1920 or 1320x2868), named after the output file (`play_screenshot_01_scan`). Return the frame ids.
2. **Art as background.** Call `upload_assets` with those frame ids as `nodeIds` and `scaleMode: FILL`, to get single-use POST URLs (mcp.figma.com, valid for 10 minutes). The cloud container and the Cowork VM can't reach that host, so run the curl POSTs (`-H "Content-Type: image/png" --data-binary @file`) from the user's Mac through a Remote Control session in a folder they've approved. Create the URLs right before starting that session. Upload the real app icon the same way, into an image frame inside the feature graphic.
3. **Phone and UI layers.** On phone slides, build the phone from `layers/geo.json` as a Figma object: a "Body" (bezel color, rounded corners, drop shadow), a "Rim" (inner stroke) and a clipped "Screen" with the staged screen as an image fill, at the same size on every slide. On freestyle slides, build the floating bubbles and cards as live Figma layers, using the app's components where they exist.
4. **Text and icon layers.** In one `use_figma` call, add to each frame a "Copy" group with clip content off, its top edge at about 5 to 7% of the frame height (the golden area rule above): a "Headline" text in two lines (the file's heading font, about 9% of the frame width, styled as the headline rule and `refs/preferences.md` say, with the key word on its own pill shape behind it) and an instance of the slide's icon component next to the shorter line (see the icon rule). No subline. For the feature graphic, put the icon, the app name and the tagline as text in the empty left area. Load each font with `listAvailableFontsAsync` / `loadFontAsync` first. Keep the text inside the store-safe margins, and make sure it doesn't overlap the phone.
5. **Check.** Screenshot the section (`get_screenshot`) and look for clipped or overlapping text and poor contrast on the art. Fix those before export.
6. **Other languages.** Duplicate the frames and replace only the text. The art is shared, which is the point of keeping text out of it. Name the copies with a locale suffix (`play_screenshot_01_scan_vi`).

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

- Before delivering, first audit every asset against `refs/preferences.md`, item by item (palette, style, cast, bans), then against each rule at the top (no baked text, best state, no real data, polished UI, on-brand colors, two-line headline with no subline, app icon, separate layers, gentle tilts, a mix of phone and freestyle slides), and fix any failures. Include a one-line pass note per asset in the reply, and list any rule you set aside because a preference overrode it.

- Make sure `final/` is in the agreed Mac folder.
- In the reply, attach the contact sheet, the icon and the feature graphic (6 attachments at most per message), and link the Figma section where the text can be edited. Then list what each store got, the specs checked, where the copy came from, and any trade-offs, such as a copy fix.
