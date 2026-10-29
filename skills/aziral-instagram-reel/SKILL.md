---
name: aziral-instagram-reel
description: Write evidence-backed Instagram Reel scripts and product-demo storyboards, with RU/EN/KK variants and a local Unicode-aware spoken timing estimate. Use for scripting and video-production handoff.
---

# Reel script and production handoff

Work from the supplied brief, actual product behavior and available footage. Choose one audience problem and one visible payoff. If no recording or runnable product is available, deliver a proposed shot list and label unavailable shots; do not imply a render exists.

Offer a few opening lines with different angles when useful. Select on clarity, factual support and fit to the footage. A text-only score cannot predict reach, retention or virality, so do not manufacture one.

## Storyboard

Keep spoken lines separate from visual directions and on-screen text. For each beat, specify the claim, supporting screen or action, spoken line, concise on-screen label, and transition. Use a natural ending and one appropriate next step. Do not force a loop or a sales pitch into every Reel.

Write separate RU/EN/KK variants when requested, preserving names, amounts, dates and feature status. Adapt phrasing for speech instead of matching word counts. Keep the founder's actual experience distinct from a hypothetical example.

## Estimate speaking time

Save only spoken lines as `role | text`, one beat per line. Roles such as `hook`, `demo`, `proof` and `cta` are descriptive labels.

```bash
python3 scripts/beat_sheet.py spoken.txt --wpm 145 --target 30
```

Resolve `scripts/beat_sheet.py` relative to this skill directory. The tool runs locally with Python 3.10+ and no packages or network. It counts Unicode words, including Cyrillic and Kazakh. WPM and pause are editable assumptions, not measured speech or platform rules. Emoji and visual directions are not speech. Verify the final pacing with a recorded read; the script does not align audio, generate captions or render video.

If a line is too long, shorten it or add a meaningful visual change. Keep the result readable with the sound off: provide subtitles or a clear text equivalent and avoid essential information only in audio.

## Handoff

Deliver the selected script, storyboard, estimated timing, asset list and unresolved evidence gaps. For production, use the user's chosen renderer. If available, AZIRAL HyperFrames workflows suit HTML video and AZIRAL Remotion workflows suit React video; otherwise provide a renderer-neutral storyboard. Check current dimensions, overlays and music rights for the intended publishing surface when producing the actual asset.

Do not start paid generation, cloud rendering, account access or publishing merely because a script was requested. Existing explicit authorization remains valid within its scope.
