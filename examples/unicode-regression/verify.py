#!/usr/bin/env python3
"""Verify scalar counts and encoding sizes without rewriting the fixture file."""

import argparse
import json
from pathlib import Path
import platform
import re
import sys
import unicodedata


METRICS = ("codePoints", "utf8Bytes", "utf16CodeUnits", "graphemeClusters")


def verify(data):
    if not isinstance(data, dict) or type(data.get("schemaVersion")) is not int or data["schemaVersion"] != 1:
        raise ValueError("expected schemaVersion 1")
    fixtures = data.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise ValueError("fixtures must be a nonempty list")
    ids = set()
    checks = []
    for fixture in fixtures:
        if not isinstance(fixture, dict):
            raise ValueError("each fixture must be an object")
        name = fixture.get("id")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in ids:
            raise ValueError("fixture IDs must be unique lowercase ASCII identifiers")
        ids.add(name)
        text = fixture.get("text")
        if not isinstance(text, str):
            raise ValueError(f"{name}: text must be a string")
        if any(0xD800 <= ord(char) <= 0xDFFF for char in text):
            raise ValueError(f"{name}: unpaired surrogate outside scalar-value scope")
        expected = fixture.get("expected")
        if not isinstance(expected, dict) or any(type(expected.get(key)) is not int or expected[key] < 0 for key in METRICS):
            raise ValueError(f"{name}: expected metrics must be nonnegative integers")
        points = [f"U+{ord(char):04X}" for char in text]
        if fixture.get("codePointsHex") != points:
            raise ValueError(f"{name}: source text differs from codePointsHex; inspect transport or editing")
        actual = {
            "codePoints": len(text),
            "utf8Bytes": len(text.encode("utf-8")),
            "utf16CodeUnits": len(text.encode("utf-16-le")) // 2,
        }
        for metric, value in actual.items():
            if value != expected[metric]:
                raise ValueError(f"{name}: {metric}: expected {expected[metric]}, got {value}")
        checks.append({"id": name, "actual": actual, "status": "passed"})
    return {
        "status": "passed",
        "fixturesChecked": len(checks),
        "runtime": {"python": platform.python_version(), "unicodeDatabase": unicodedata.unidata_version},
        "graphemes": {"status": "not_measured", "reason": "Run verify.mjs for recorded Intl.Segmenter expectations."},
        "checks": checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path(__file__).with_name("fixtures.json"))
    args = parser.parse_args()
    try:
        report = verify(json.loads(args.path.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
