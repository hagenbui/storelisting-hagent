# storelisting-hagent

A Claude skill (packaged as a Claude Code plugin) that builds store listing packs for mobile apps from a Figma design:

- **Google Play:** phone screenshots (1080x1920), 512x512 icon, 1024x500 feature graphic, and optional title, short and full description
- **Apple App Store:** iPhone 6.9" screenshots (1320x2868), optional iPad 13" (2064x2752), 1024x1024 icon, and optional name, subtitle, promo text, description and keywords

The visuals are generated with the OpenAI image generator (the omniroute-images plugin), with the real Figma screens passed in as references. Copy comes from the design. Before it starts, the skill asks which stores, which assets and which languages you want.

## Layout

```
.claude-plugin/plugin.json              plugin manifest
skills/storelisting-hagent/
  SKILL.md                              the workflow
  references/store-specs.md             current asset and text limits per store
  references/prompt-templates.md        image-generator prompt patterns
  scripts/fit_asset.py                  resize/extend generated images to exact store sizes
  scripts/check_pack.py                 verify a finished pack against the specs
  scripts/check_listing.py              check listing text limits, write fastlane metadata
```

## Install

Claude Code: `claude plugin install /path/to/storelisting-hagent` (or add the folder as a local marketplace).
Claude.ai: upload `skills/storelisting-hagent` as a skill.

## Scripts

```
python3 scripts/fit_asset.py play-shot  in.png out.png
python3 scripts/fit_asset.py ios-shot   in.png out.png
python3 scripts/fit_asset.py ipad-shot  in.png out.png
python3 scripts/fit_asset.py play-icon  in.png out.png
python3 scripts/fit_asset.py ios-icon   in.png out.png
python3 scripts/fit_asset.py play-fg    in.png out.png
python3 scripts/check_pack.py path/to/pack/
python3 scripts/check_listing.py listing.json [--write]
```

Requires Python 3 with Pillow and numpy.
