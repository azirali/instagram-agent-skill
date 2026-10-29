"""Behavioral checks for Unicode text preservation and spoken timing."""
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CAPTION_SCRIPT = ROOT / "skills/aziral-instagram-caption/scripts/caption_check.py"
BEAT_SCRIPT = ROOT / "skills/aziral-instagram-reel/scripts/beat_sheet.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


caption = load("aziral_caption_test", CAPTION_SCRIPT)
beats = load("aziral_beats_test", BEAT_SCRIPT)


class CaptionTests(unittest.TestCase):
    def test_unicode_emoji_and_urls_are_preserved(self):
        text = "Ә Ғ Қ Ң Ө Ұ Ү Һ І 👩‍💻 https://aziral.com/?lang=kk #қазақша"
        result = caption.review(text, language="kk", preview=1000)
        self.assertEqual(result["preview"], text)
        self.assertEqual(result["hashtags"], ["#қазақша"])
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["characters"], len(text))

    def test_unknown_facts_are_reported(self):
        result = caption.review("Result: {{verify: sales increase}}. [TODO: obtain evidence]")
        finding = next(item for item in result["findings"] if item["code"] == "placeholders")
        self.assertEqual(len(finding["values"]), 2)

    def test_budgets_are_configurable_editorial_checks(self):
        text = "Прототип #бір #екі"
        result = caption.review(text, language="ru", preview=5, hashtag_budget=1, max_characters=10)
        self.assertEqual(result["preview"], text[:5])
        self.assertTrue(result["preview_is_truncated"])
        self.assertEqual({item["code"] for item in result["findings"]}, {"length_budget", "hashtag_budget"})
        self.assertEqual(caption.review(text, preview=100, hashtag_budget=2)["findings"], [])

    def test_controls_are_flagged_without_rewriting(self):
        text = "Demo\u200b text 👨‍👩‍👧‍👦"
        result = caption.review(text)
        self.assertEqual(result["preview"], text)
        finding = next(item for item in result["findings"] if item["code"] == "review_controls")
        self.assertEqual(finding["values"], ["U+200B"])

    def test_cli_strict_status_and_input_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "мәтін.txt"
            original = "\ufeffПрототип 👩‍💻 {{verify: факт}}".encode("utf-8")
            path.write_bytes(original)
            proc = subprocess.run([sys.executable, str(CAPTION_SCRIPT), str(path), "--language", "kk", "--strict"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1, proc.stderr)
            self.assertIn("👩‍💻", json.loads(proc.stdout)["preview"])
            self.assertEqual(path.read_bytes(), original)


class BeatTests(unittest.TestCase):
    def test_three_languages_have_positive_spoken_timing(self):
        texts = {
            "en": "I build apps for local businesses.",
            "ru": "Я создаю приложения для местного бизнеса.",
            "kk": "Мен жергілікті бизнеске қосымша жасаймын.",
        }
        for language, text in texts.items():
            with self.subTest(language=language):
                result = beats.make_sheet("hook | " + text)
                self.assertGreater(result["words"], 0)
                self.assertGreater(result["estimated_seconds"], 0)
                self.assertEqual(result["beats"][0]["text"], text)

    def test_pause_is_between_beats_not_after_final(self):
        result = beats.make_sheet("hook | One two\ndemo | Three four", wpm=120, pause=0.5, target=3)
        self.assertEqual(result["words"], 4)
        self.assertEqual(result["estimated_seconds"], 2.5)
        self.assertEqual(result["difference_from_target_seconds"], -0.5)
        self.assertEqual(result["beats"][1]["start_seconds"], 1.5)

    def test_role_metadata_emoji_and_comments_are_not_spoken_words(self):
        result = beats.make_sheet("# shot instruction\nhook | Прототип 👩‍💻\ndemo | Қосымша дайын", wpm=60, pause=0)
        self.assertEqual(result["words"], 3)
        self.assertEqual(result["estimated_seconds"], 3)
        self.assertEqual(beats.word_count("don't co-founder"), 2)

    def test_invalid_or_nonfinite_timings_are_rejected(self):
        for kwargs in ({"wpm": 0}, {"wpm": math.nan}, {"wpm": math.inf}, {"pause": -1}, {"pause": math.inf}, {"target": 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                beats.make_sheet("hook | Demo", **kwargs)
        for text in ("", "missing separator", "| Empty role", "hook | 👩‍💻"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                beats.make_sheet(text)

    def test_cli_bom_unicode_and_input_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "сценарий.txt"
            original = "\ufeffhook | Ә Ғ Қ Ң Ө Ұ Ү Һ І 👩‍💻".encode("utf-8")
            path.write_bytes(original)
            proc = subprocess.run([sys.executable, str(BEAT_SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads(proc.stdout)
            self.assertEqual(result["words"], 9)
            self.assertIn("👩‍💻", result["beats"][0]["text"])
            self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
