---
name: aziral-instagram-insights
description: Analyze supplied Instagram post metrics or a local CSV to compare saves, shares, follows and view multiples within each format. Use for content reviews and experiment planning from real observations.
---

# AZIRAL Instagram Insights

Use the supplied metrics, export or screenshots. This skill needs no Instagram login, network access or API token. It does not publish or contact people.

For CSV input, run the local helper with Python 3.10+:

```bash
python3 scripts/insights.py /path/to/posts.csv
```

Resolve the script relative to this skill directory. The helper reads the input and prints JSON; it never changes the source file.

CSV needs `post_id,format`. Optional columns are `reach,views,saves,shares,comments,likes,profile_visits,follows`. Use one account and comparable observation windows per file. Counts must be nonnegative integers no larger than 9007199254740991. Use UTF-8; a BOM is accepted. Blank values or absent columns mean unknown, while `0` means an observed zero. Duplicate IDs and malformed rows are errors. Unknown columns are ignored.

The report keeps formats separate. Action rates are per 1000 reach and remain null if the numerator is missing or reach is missing/zero. They are action counts, not probabilities of unique-person conversion. The view multiple uses the same-format sample median of observed views, including the focal post. It is not an independently measured account baseline. With fewer than five posts, or missing observations, keep the conclusion exploratory; five posts is a reporting caution threshold, not statistical validation.

Return the useful comparison for the user's goal, with the supporting counts and missing fields visible. Distinguish a post with high saves per reach from one with high total reach. Do not infer retention, sales, audience demographics or a best posting time from columns that do not measure them. Different publication ages, paid boosts and selective exports can make posts incomparable.

Propose a small next experiment with one changed variable and a metric to observe. Describe association rather than causation. For RU/EN/KK posts, only compare language performance if language labels and enough comparable observations are actually supplied; this helper does not infer language from IDs or formats.
