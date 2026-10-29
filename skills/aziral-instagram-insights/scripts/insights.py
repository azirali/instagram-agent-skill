#!/usr/bin/env python3
"""Read an account's local post CSV and emit descriptive, format-specific metrics."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import statistics
import sys
from typing import TextIO

METRICS = ("reach", "views", "saves", "shares", "comments", "likes", "profile_visits", "follows")
RATE_METRICS = METRICS[2:]
MAX_COUNT = 2**53 - 1


def parse_count(raw: str | None, field: str, line: int) -> int | None:
    """A blank observation is unknown, never an observed zero."""
    if raw is None or not raw.strip():
        return None
    try:
        number = Decimal(raw.strip())
    except InvalidOperation as exc:
        raise ValueError(f"Line {line}: {field} must be a nonnegative integer or blank") from exc
    if not number.is_finite() or number < 0 or number != number.to_integral_value() or number > MAX_COUNT:
        raise ValueError(f"Line {line}: {field} must be an integer from 0 to {MAX_COUNT}, or blank")
    return int(number)


def read_rows(stream: TextIO) -> list[dict]:
    reader = csv.DictReader(stream, strict=True)
    fields = reader.fieldnames
    if not fields or len(fields) != len(set(fields)):
        raise ValueError("CSV needs unique column names and a header")
    missing = {"post_id", "format"} - set(fields)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    rows = []
    seen = set()
    for row in reader:
        line = reader.line_num
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"Line {line}: number of fields differs from the header")
        post_id = row["post_id"].strip()
        post_format = row["format"].strip().casefold()
        if not post_id or not post_format:
            raise ValueError(f"Line {line}: post_id and format cannot be blank")
        if post_id in seen:
            raise ValueError(f"Line {line}: duplicate post_id {post_id!r}")
        seen.add(post_id)
        rows.append({
            "post_id": post_id,
            "format": post_format,
            "metrics": {field: parse_count(row.get(field), field, line) for field in METRICS},
        })
    if not rows:
        raise ValueError("CSV contains no posts")
    return rows


def ratio(numerator: int | None, denominator: int | float | None, scale: int = 1) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return round(numerator / denominator * scale, 6)


def analyze(rows: list[dict]) -> dict:
    groups = []
    posts = []
    for post_format in sorted({row["format"] for row in rows}):
        members = sorted((row for row in rows if row["format"] == post_format), key=lambda row: row["post_id"])
        views = [row["metrics"]["views"] for row in members if row["metrics"]["views"] is not None]
        baseline = statistics.median(views) if views else None
        warnings = []
        if len(members) < 5:
            warnings.append("Fewer than 5 posts in this format; treat comparisons as exploratory")
        if len(views) < len(members):
            warnings.append("Some posts have no views observation; the median uses observed values only")
        if baseline == 0:
            warnings.append("Median views is zero; view multiples are unavailable")
        if any(row["metrics"]["reach"] is None or row["metrics"]["reach"] == 0 for row in members):
            warnings.append("Some reach observations are missing or zero; their rates are unavailable")
        groups.append({
            "format": post_format,
            "posts": len(members),
            "observed_posts": {field: sum(row["metrics"][field] is not None for row in members) for field in METRICS},
            "median_views": baseline,
            "views_baseline_posts": len(views),
            "warnings": warnings,
        })
        for row in members:
            metrics = row["metrics"]
            posts.append({
                **row,
                "per_1000_reach": {field: ratio(metrics[field], metrics["reach"], 1000) for field in RATE_METRICS},
                "views_vs_format_median": ratio(metrics["views"], baseline),
            })
    return {
        "schema_version": 1,
        "post_count": len(rows),
        "method": {
            "scope": "One account and a comparable observation window per CSV",
            "rate_denominator": "Reach of that post; rates are actions per 1000 reached accounts, not unique-person conversion probabilities",
            "views_baseline": "Median observed views in the supplied sample of the same format, including the focal post",
            "interpretation": "Descriptive comparisons only; no causal attribution, significance test, best-time inference, or prediction of future reach",
            "missing_values": "Blank cells and absent metric columns are null; observed zero remains zero",
        },
        "formats": groups,
        "posts": posts,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="UTF-8 CSV for one account; required columns: post_id, format")
    args = parser.parse_args(argv)
    try:
        with args.csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
            report = analyze(read_rows(stream))
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
