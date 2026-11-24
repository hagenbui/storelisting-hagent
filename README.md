# storelisting-hagent

A Claude skill (packaged as a Claude Code plugin) that builds store listing packs for mobile apps from a Figma design:

- **Google Play:** phone screenshots (1080x1920), 512x512 icon, 1024x500 feature graphic, and optional title, short and full description
- **Apple App Store:** iPhone 6.9" screenshots (1320x2868), optional iPad 13" (2064x2752), 1024x1024 icon, and optional name, subtitle, promo text, description and keywords

The visuals are generated with the OpenAI image generator (the omniroute-images plugin), with the real Figma screens passed in as references. Copy comes from the design. Before it starts, the skill asks which stores, which assets and which languages you want.

## Layout

This repo is both a plugin marketplace and the plugin it lists.

```
.claude-plugin/marketplace.json                 marketplace catalog (lists the plugin below)
plugins/storelisting-hagent/
  .claude-plugin/plugin.json                    plugin manifest
  skills/storelisting-hagent/
    SKILL.md                                    the workflow
    references/store-specs.md                   current asset and text limits per store
    references/prompt-templates.md              image-generator prompt patterns
    scripts/fit_asset.py                        resize/extend generated images to exact store sizes
    scripts/check_pack.py                       verify a finished pack against the specs
    scripts/check_listing.py                    check listing text limits, write fastlane metadata
```

## Install with auto-update

**From GitHub (recommended, works on any machine):** push this repo to GitHub, then in Claude Code:

```
claude plugin marketplace add <github-user>/storelisting-hagent
claude plugin install storelisting-hagent@storelisting-hagent
```

Then turn on auto-update once: run `/plugin`, open **Marketplaces**, select `storelisting-hagent`, and choose **Enable auto-update**. Or add it to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "storelisting-hagent": {
      "source": { "source": "github", "repo": "<github-user>/storelisting-hagent" },
      "autoUpdate": true
    }
  }
}
```

No `version` field is set, so every pushed commit counts as a new version. Claude Code picks it up within about 10 minutes of starting a session and shows "Plugin updated · Run /reload-plugins to apply". If you'd rather release on purpose, add `"version": "x.y.z"` to `plugin.json` and bump it for each release.

**From this folder (this Mac only):**

```
claude plugin marketplace add ~/Coding/storelisting-hagent
claude plugin install storelisting-hagent@storelisting-hagent
```

A local marketplace loads the plugin in place, so edits apply at the next session start or after `/reload-plugins`, with no update step.

## Scripts

```
python3 plugins/storelisting-hagent/skills/storelisting-hagent/scripts/fit_asset.py play-shot  in.png out.png
python3 plugins/storelisting-hagent/skills/storelisting-hagent/scripts/fit_asset.py ios-shot   in.png out.png
python3 plugins/storelisting-hagent/skills/storelisting-hagent/scripts/fit_asset.py ipad-shot  in.png out.png
python3 plugins/storelisting-hagent/skills/storelisting-hagent/scripts/fit_asset.py play-icon  in.png out.png
python3 plugins/storelisting-hagent/skills/storelisting-hagent/scripts/fit_asset.py ios-icon   in.png out.png
python3 plugins/storelisting-hagent/skills/storelisting-hagent/scripts/fit_asset.py play-fg    in.png out.png
python3 plugins/storelisting-hagent/skills/storelisting-hagent/scripts/check_pack.py path/to/pack/
python3 plugins/storelisting-hagent/skills/storelisting-hagent/scripts/check_listing.py listing.json [--write]
```

Requires Python 3 with Pillow and numpy.
