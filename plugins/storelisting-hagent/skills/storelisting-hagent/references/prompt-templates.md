# Image-generator prompt templates

Use `model: gpt`, `quality: high`, and always pass the matching Figma screen as `reference_image` (an absolute path on the Mac). Fill in the {braces}. Keep the shared style block identical across a pack so the set looks consistent.

## Shared style block (only where the visual direction is silent; the direction always wins)
Background: {light brand tint} to {lighter tint} gradient with large smooth flowing {brand color hex} wave shapes, premium, polished, bright and clean. Keep the phone and props well inside the canvas with generous side margins (at least {12 for Play, 16 for iPhone}% left and right), nothing important near the left or right edges. NO text, letters, numbers, logos or watermarks anywhere outside the phone screen. Props carry icons only, never words.

## Screenshot scene (layered method, the default; no phone, no props)
{Store} screenshot BACKGROUND ART, tall 9:16 portrait, for {app type}. Do NOT draw any phone, device, screen, UI or objects. No text, letters, numbers, logos or watermarks.
Background only: {light brand tint} blending into {second tint} toward the bottom, a faint {texture, e.g. dot grid} across the upper half, and two broad, softly rounded {brand color hex} waves across the lower 40%, the front wave slightly deeper and sweeping toward the {left|right}; soft studio light from the upper left, gentle depth. Only {brand colors} and warm neutrals. The top 26% is calm, empty background. Premium, polished, bright and clean.

## Props in context (the default; an edit of the composed shot's bottom 2:3 from compose_phone.py --edit-crop)
This is the lower part of a mobile app-store screenshot for '{app}', {app type}. Keep the phone, its frame, the screen and everything on it, and the background exactly as they are, at the same position and size; keep the whole picture inside the image borders, nothing cut off. Add: exactly one {hero prop that echoes this screen, e.g. a chunky alarm clock} (one only); {up to two small accents, e.g. tiny stars, soft clouds low at the corners}. All props in one consistent look: {how the visual direction draws props, e.g. soft glossy 3D toys | flat round stickers with a thin dark outline}. Main prop placement: just outside the phone next to its lower {left|right} corner, touching the outer frame at most. {3D: Light them like the scene, with natural contact shadows on the ground and on the phone frame and soft ambient occlusion, so they look photographed together with the phone. | Flat: Draw them in the same flat graphic style as the background (no 3D, no realistic shading; at most a soft flat drop shadow).} The phone frame is thin, so props stay beside the phone: nothing may cover any part of the screen. Props use only these colors: {brand colors}. No text, letters or numbers anywhere outside the screen.

## Decor kit sheet (fallback only; cut with scripts/cut_kit.py)
A clean product sticker sheet of six separate glossy, rounded, toy-like 3D objects for {app type}, in a loose 3x2 grid with generous empty space between them (no object touches another or the edge), on a perfectly flat, uniform pure magenta (#FF00FF) background with no shadows on the background. All in {brand colors} and warm neutrals, soft studio light from the upper left, consistent style and scale: 1. {hero prop for screen 1} 2. {hero prop for screen 2} ... 5. a small cluster of three glossy spheres 6. a small cluster of three four-point sparkles. No text, letters, numbers or logos. Square image.

## Screenshot with a generated phone (old method; only for one-off single images)
{Store} promotional screenshot background art, portrait, for {app type}. Use the attached app screen as the exact UI shown on the phone: {list the key UI elements and their visible labels, so the generator keeps them}.

Composition: the top 30% of the canvas is calm, clean, empty background with no objects and no text, reserved for a headline that will be added later. The lower 70%: a modern slim {Android phone with thin bezels and punch-hole camera | iPhone with Dynamic Island} showing the app screen, {upright | slightly tilted 6 degrees}, soft realistic shadow. {1 or 2 props that echo the feature and match exactly what the screen shows (same colors, same styled output): floating glossy 3D tiles in the brand color with white icons, spheres, a printed QR card, swatches...}, subtle depth of field.

{Shared style block}

Describe the staged screen's content as it is: colorful swatches, the styled output, the fictional brand. Add: "Every object, including anything visible inside the phone's camera view, uses only {brand color} tones and warm neutrals; no other strong colors. The screen shows the feature in a finished, colorful state. Do not show any real company names, real websites, phone numbers or personal data."

Device matters. Play shots use an Android phone and App Store shots use an iPhone, because each store rejects or flags the other platform's hardware. Never quote the headline in this prompt.

## App icon
App icon for "{App Name}", recreated as a polished high-resolution store icon based on the attached icon. Keep the same concept exactly: {describe the mark, colors and gradient}.

Format rules: full-bleed square artwork filling the entire 1:1 canvas edge to edge. NO rounded corners, NO outer shadow, NO border, NO transparent areas, NO device frame, NO text or letters. Keep the mark centered inside the middle 66% of the canvas so it survives circular and squircle masks.

## Play feature graphic (text-free art; icon, name and tagline are added later in Figma)
Google Play feature graphic background art (wide banner) for {app type}. {If the file has an existing banner: "Use the attached banner as the style reference, but remove all text and the logo from it."}

Layout: the left 45% is calm, clean, empty background with no objects and no text, reserved for the app icon, name and tagline that will be added later. Right side: a slim Android phone, tilted slightly, showing {hero screen}, with floating props. Keep the important content inside the central horizontal band (16% to 84% of the height).

{Shared style block}
