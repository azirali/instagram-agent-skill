# Instagram Agent Skill by AZIRAL

![Instagram Agent Skill by AZIRAL](assets/cover.svg)

**Five focused agent skills for founder and product content in English, Russian and Kazakh.**

Turn verified product material into a content plan, a Reel script, a caption or a carousel. Review your own post metrics with local Python tools. Keep facts consistent across languages and keep publication under your control.

[Русский](README.ru.md) · [Қазақша](README.kk.md) · [MIT](LICENSE) · [Examples](examples)

Independent work by **Olzhas Azirali / AZIRAL**, inspired by [Jake Schincariol's project](https://github.com/Jakeschincariol/instagram-agent-skill). Original instructions and implementations; no affiliation with the upstream author, Instagram or Meta. See [origin and scope](NOTICE.md).

## Install

With the Skills CLI, choose the coding agent and installation scope you use:

```sh
npx skills add azirali/instagram-agent-skill
```

Or select one workflow:

```sh
npx skills add azirali/instagram-agent-skill --skill aziral-instagram-reel
```

The skill folders are self-contained. Each includes `SKILL.md` and Codex UI metadata; the reel, caption and insights skills also include local tools. No Meta app, Instagram credentials or paid service is needed for these workflows. Your coding agent may have its own usage costs. This repository does not include a publishing integration or Claude plugin manifest.

## Choose a skill

| Skill | Useful output |
| --- | --- |
| [`aziral-instagram-plan`](skills/aziral-instagram-plan/SKILL.md) | Positioning, evidence brief and a feasible content calendar |
| [`aziral-instagram-reel`](skills/aziral-instagram-reel/SKILL.md) | Spoken script, visual storyboard, timing estimate and renderer handoff |
| [`aziral-instagram-caption`](skills/aziral-instagram-caption/SKILL.md) | Natural RU/EN/KK captions, alt text and a non-destructive text report |
| [`aziral-instagram-carousel`](skills/aziral-instagram-carousel/SKILL.md) | Concise carousel or Story sequence with visual directions and sources |
| [`aziral-instagram-insights`](skills/aziral-instagram-insights/SKILL.md) | Format-specific CSV comparisons with missing data kept visible |

## Try a real task

```text
Use $aziral-instagram-reel with this recording of my app prototype.
Show one working action. Prepare separate RU, EN and KK versions,
keep demo data clearly labeled and do not invent customers or revenue.
Deliver a storyboard and a spoken-time estimate for a 30-second Reel.
```

```text
Use $aziral-instagram-insights to review this CSV from one account.
Compare saves and shares per reach within each format. Explain missing
observations, then suggest one experiment. Do not schedule or publish.
```

For rendered video, supply footage and specify your renderer. These workflows can hand off to [AZIRAL HyperFrames](https://github.com/azirali/hyperframes) or [AZIRAL Remotion](https://github.com/azirali/remotion) when installed; those are optional, separately configured tools.

## Run the tools without an agent

Python **3.10+**, standard library only. No installation, network requests or API keys. From the repository root:

```sh
python3 skills/aziral-instagram-caption/scripts/caption_check.py examples/caption.kk.txt --language kk --strict
python3 skills/aziral-instagram-reel/scripts/beat_sheet.py examples/reel.ru.txt --wpm 145 --target 30
python3 skills/aziral-instagram-insights/scripts/insights.py examples/insights.csv
```

All three print JSON and leave their input untouched. The caption tool uses configurable editorial budgets; it does not claim to reproduce feed layout or know current account limits. The beat sheet estimates timing from Unicode words and a chosen speaking rate; record a read-through before editing. Analytics use actions per 1000 reach and same-format sample medians, not causal attribution or predictions.

The CSV in `examples/` is **synthetic test data**, including zero and missing observations. It is not AZIRAL account performance. The multilingual captions and scripts demonstrate this toolkit's features; they are text examples, not rendered media or evidence of marketing results.

## What this collection emphasizes

- **Evidence before claims.** Prototype status, unknown numbers and missing footage stay explicit.
- **RU / EN / KK as separate adaptations.** Preserve names, amounts and meaning; review Cyrillic and Kazakh text at phone size.
- **Unicode-aware local tools.** Cyrillic words are counted and valid emoji joiners are preserved. The text checker does not silently rewrite your voice.
- **Readable mobile content.** Keep speech, on-screen labels, visual directions and alt text separate.
- **Descriptive analytics.** Blank is unknown, zero is observed zero, and a zero denominator produces `null`.

No virality guarantee, AI-detection score, engagement bot, scraping system or automatic publishing is included. External actions follow the user's actual authorization; requesting a draft does not authorize outreach, account changes or paid production. Platform constraints change, so verify them for the intended account and surface when publishing.

## Demo and walkthrough

Watch the [36-second silent demo](https://aziral.com/media/instagram-agent-skill/demo.mp4), or use the [vertical version](https://aziral.com/media/instagram-agent-skill/demo-vertical.mp4). The AI-assisted animation uses actual CLI output; the analytics data are synthetic examples and speech timing is an estimate.

- [English technical walkthrough on Medium](https://medium.com/@olzasazirali/unicode-safe-content-tools-for-english-russian-and-kazakh-769024c567f3)
- [Russian case study by Olzhas Azirali](https://aziral.com/blog/instagram-agent-skill-aziral-unicode-ru-en-kk)

## Unicode regression fixtures

[Twenty reproducible fixtures](examples/unicode-regression) cover RU/EN/KK text, emoji joiners, combining accents, flags, modifiers and line endings. Offline Python and JavaScript verifiers identify their count units and runtime versions. Removing a joiner or changing an encoding expectation fails the check; input is preserved. This is a focused regression pack, not a complete Unicode conformance suite.

```sh
python3 examples/unicode-regression/verify.py
node examples/unicode-regression/verify.mjs
```

Try the [free browser checker by Olzhas Azirali / AZIRAL](https://aziral.com/en/tools/unicode-text-checker). It inspects text locally; the repository pack lets developers reproduce the examples without a browser.

## Development

```sh
python3 -m unittest discover -s tests -v
```

Tests cover multilingual timing, input preservation, editorial findings and analytics edge cases. They do not measure audience response or verify Instagram UI behavior. No GitHub Actions workflow is bundled; run checks locally before contributing.

Useful contributions include language corrections, reproducible script bugs and concrete workflow improvements. Do not submit private account exports, tokens or customer records. Use synthetic data for examples.

## License and author

[MIT](LICENSE), Copyright (c) 2026 Olzhas Azirali / AZIRAL. The linked inspiration and external tools retain their own authorship and licenses. [NOTICE.md](NOTICE.md) records the source of inspiration and the scope of the original work.

Created by [Olzhas Azirali](https://aziral.com/olzhas-azirali) · [AZIRAL](https://aziral.com) · [GitHub](https://github.com/azirali)

[Product video](https://github.com/azirali/hyperframes) · [React promos](https://github.com/azirali/remotion) · [Brand frontend](https://github.com/azirali/taste-skill) · [UI review](https://github.com/azirali/impeccable)

If the toolkit is useful in your work, a star helps others discover it.

