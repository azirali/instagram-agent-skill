---
name: aziral-instagram-caption
description: Draft and review Instagram captions, alt text and RU/EN/KK localizations from verified source material. Includes a local non-destructive text checker for previews, placeholders and editorial budgets.
---

# Caption and localization

Use the supplied post, brief and evidence. Open with the specific takeaway or useful detail the audience can evaluate. Keep the writer's voice, remove needless preamble and give the post one relevant next action when an action is needed.

Preserve uncertainty and feature status. Never turn a prototype into a launched service, a goal into a measured outcome, or an example into a customer testimonial. If a needed fact is missing, ask for it or return a clearly marked draft with `{{verify: fact}}`. A draft with unresolved placeholders is not ready to publish.

## Language and accessibility

Produce separate RU/EN/KK variants when requested. Compare names, prices, currencies, dates, promises and URLs against the source. Translate the meaning and tone naturally; retain Kazakh letters and valid emoji sequences. Do not remove all invisible Unicode characters indiscriminately because joiners can be meaningful.

Provide useful alt text for the supplied image when appropriate: the relevant visible content and message, without inventing details that are not shown. Do not treat hashtags as alt text or add unsupported demographic descriptions of people.

## Local review

```bash
python3 scripts/caption_check.py caption.txt --language kk --preview 125 --hashtag-budget 5
```

Resolve the script path relative to this skill directory. It reads UTF-8, emits JSON and never edits the input. Python 3.10+ is sufficient. `--preview` and `--hashtag-budget` are adjustable editorial settings. The preview uses Unicode code points, not actual feed layout or grapheme clusters. For a verified account-specific length constraint, pass `--max-characters N`; no platform maximum is assumed by default.

The report flags unresolved placeholders, selected control characters, and exceeded budgets. `--strict` exits with status 1 on findings. A clean report does not verify facts, language quality, rights, accessibility or platform acceptance. Re-read those manually; this is not an AI detector or a reach predictor.

Deliver copy-ready variants only after resolving factual gaps, plus alt text and a brief explanation of any deliberate language differences. Publishing, outreach and scheduling require the user's authorization for the actual destination and action; do not request it again when already provided.
