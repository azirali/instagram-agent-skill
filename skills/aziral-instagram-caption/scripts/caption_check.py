#!/usr/bin/env python3
"""Non-destructive editorial checks. No network or third-party packages."""

import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata


def positive(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def nonnegative(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return number


def review(text, language="en", preview=125, hashtag_budget=5, max_characters=None):
    if language not in {"en", "ru", "kk"}:
        raise ValueError("language must be en, ru or kk")
    if preview <= 0 or hashtag_budget < 0 or (max_characters is not None and max_characters <= 0):
        raise ValueError("invalid editorial budget")
    hashtags = re.findall(r"(?<![\w/#])#[\w]+", text, flags=re.UNICODE)
    findings = []
    if not text.strip():
        findings.append({"code": "empty", "message": "Caption is empty."})
    placeholders = re.findall(r"\{\{[^{}]*\}\}|\[(?:VERIFY|TODO|TBD)(?:[^\]]*)\]", text, re.I)
    if placeholders:
        findings.append({"code": "placeholders", "values": placeholders,
                         "message": "Resolve placeholders before publication."})
    if len(hashtags) > hashtag_budget:
        findings.append({"code": "hashtag_budget", "message": "Editorial hashtag budget exceeded."})
    if max_characters is not None and len(text) > max_characters:
        findings.append({"code": "length_budget", "message": "Configured character budget exceeded."})
    suspicious = sorted({f"U+{ord(char):04X}" for char in text
                         if (unicodedata.category(char) == "Cc" and char not in "\n\r\t")
                         or char in "\u200b\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069\ufeff"})
    if suspicious:
        findings.append({"code": "review_controls", "values": suspicious,
                         "message": "Review these characters in context; input was not modified."})
    return {
        "language": language,
        "characters": len(text),
        "count_unit": "Unicode code points, not grapheme clusters or rendered width",
        "preview": text[:preview],
        "preview_budget": preview,
        "preview_is_truncated": len(text) > preview,
        "hashtags": hashtags,
        "hashtag_budget": hashtag_budget,
        "max_characters": max_characters,
        "findings": findings,
        "limitations": "Editorial checks only. Facts, translation quality and current platform constraints require review.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="UTF-8 caption file")
    parser.add_argument("--language", choices=("en", "ru", "kk"), default="en")
    parser.add_argument("--preview", type=positive, default=125, help="editorial preview in Unicode code points")
    parser.add_argument("--hashtag-budget", type=nonnegative, default=5, help="editorial budget, not a platform rule")
    parser.add_argument("--max-characters", type=positive, help="optional verified or editorial limit")
    parser.add_argument("--strict", action="store_true", help="exit 1 when findings exist")
    args = parser.parse_args()
    try:
        text = args.path.read_text(encoding="utf-8-sig")
        report = review(text, args.language, args.preview, args.hashtag_budget, args.max_characters)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 1 if args.strict and report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
