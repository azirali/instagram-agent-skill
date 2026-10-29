#!/usr/bin/env python3
"""Estimate spoken timing from Unicode text, not from an audio recording."""

import argparse
import json
import math
from pathlib import Path
import re
import sys
import unicodedata


def word_count(text):
    normalized = unicodedata.normalize("NFC", text)
    return len(re.findall(r"[^\W_]+(?:['’\-][^\W_]+)*", normalized, re.UNICODE))


def make_sheet(text, wpm=145.0, pause=0.25, target=None):
    if not math.isfinite(wpm) or wpm <= 0:
        raise ValueError("wpm must be finite and greater than zero")
    if not math.isfinite(pause) or pause < 0:
        raise ValueError("pause must be finite and nonnegative")
    if target is not None and (not math.isfinite(target) or target <= 0):
        raise ValueError("target must be finite and greater than zero")
    beats = []
    cursor = 0.0
    for line_number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "|" not in line:
            raise ValueError(f"line {line_number}: expected role | spoken text")
        role, spoken = (part.strip() for part in line.split("|", 1))
        words = word_count(spoken)
        if not role or not spoken or words == 0:
            raise ValueError(f"line {line_number}: role and spoken words are required")
        if beats:
            cursor += pause
        duration = words * 60.0 / wpm
        beats.append({"role": role, "text": spoken, "words": words,
                      "start_seconds": round(cursor, 3), "end_seconds": round(cursor + duration, 3),
                      "spoken_seconds": round(duration, 3)})
        cursor += duration
    if not beats:
        raise ValueError("no spoken beats found")
    return {
        "assumptions": {"wpm": wpm, "pause_between_beats_seconds": pause,
                        "method": "Unicode word count; estimates only, not audio alignment"},
        "beats": beats,
        "words": sum(beat["words"] for beat in beats),
        "estimated_seconds": round(cursor, 3),
        "target_seconds": target,
        "difference_from_target_seconds": round(cursor - target, 3) if target is not None else None,
        "limitations": "Read aloud and time the recording. Numbers, abbreviations and language-specific delivery can change duration.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="UTF-8 lines in role | spoken text format")
    parser.add_argument("--wpm", type=float, default=145.0)
    parser.add_argument("--pause", type=float, default=0.25)
    parser.add_argument("--target", type=float)
    args = parser.parse_args()
    try:
        result = make_sheet(args.path.read_text(encoding="utf-8-sig"), args.wpm, args.pause, args.target)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
