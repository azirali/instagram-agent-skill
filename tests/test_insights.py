"""Behavioral checks for missing data, fair comparisons and local CSV errors."""
import csv
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/aziral-instagram-insights/scripts/insights.py"
spec = importlib.util.spec_from_file_location("aziral_insights", SCRIPT)
insights = importlib.util.module_from_spec(spec)
spec.loader.exec_module(insights)


def report(text):
    return insights.analyze(insights.read_rows(io.StringIO(text)))


class InsightsTests(unittest.TestCase):
    def test_missing_and_observed_zero_are_distinct(self):
        result = report("post_id,format,reach,saves,shares\na,reel,100,0,\nb,reel,,4,0\nc,reel,0,2,1\n")
        posts = {post["post_id"]: post for post in result["posts"]}
        self.assertEqual(posts["a"]["per_1000_reach"]["saves"], 0)
        self.assertIsNone(posts["a"]["per_1000_reach"]["shares"])
        self.assertIsNone(posts["b"]["per_1000_reach"]["saves"])
        self.assertIsNone(posts["c"]["per_1000_reach"]["shares"])
        self.assertEqual(result["formats"][0]["observed_posts"]["views"], 0)
        self.assertEqual(result["formats"][0]["observed_posts"]["reach"], 2)

    def test_same_format_median_includes_focal_post(self):
        result = report("post_id,format,reach,views,saves\na,reel,100,100,3\nb,reel,200,300,4\nc,carousel,1000,10000,8\n")
        groups = {group["format"]: group for group in result["formats"]}
        posts = {post["post_id"]: post for post in result["posts"]}
        self.assertEqual(groups["reel"]["median_views"], 200)
        self.assertEqual(groups["carousel"]["median_views"], 10000)
        self.assertEqual(posts["b"]["views_vs_format_median"], 1.5)
        self.assertEqual(posts["a"]["per_1000_reach"]["saves"], 30)
        self.assertTrue(groups["reel"]["warnings"])

    def test_observed_zero_views_included_in_baseline(self):
        result = report("post_id,format,views\na,reel,0\nb,reel,0\nc,reel,90\n")
        self.assertEqual(result["formats"][0]["median_views"], 0)
        self.assertTrue(all(post["views_vs_format_median"] is None for post in result["posts"]))
        json.dumps(result, allow_nan=False)

    def test_invalid_counts_fail_instead_of_becoming_zero(self):
        for value in ("-1", "NaN", "Infinity", "1.5", "not-a-number", "9007199254740992"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                report(f"post_id,format,reach\na,reel,{value}\n")

    def test_bad_rows_and_duplicates_rejected(self):
        cases = [
            "post_id,format\na,reel\na,story\n",
            "post_id,format\n,reel\n",
            "post_id,format\na,\n",
            "post_id,format\na,reel,extra\n",
            "post_id,format,reach\na,reel\n",
            "post_id,format,reach,reach\na,reel,1,2\n",
            "format,reach\nreel,1\n",
            "post_id,format\n",
        ]
        for text in cases:
            with self.subTest(text=text), self.assertRaises(ValueError):
                report(text)

    def test_unterminated_csv_quote_is_an_error(self):
        with self.assertRaises(csv.Error):
            report('post_id,format\na,"reel\n')

    def test_cli_accepts_bom_and_unicode_and_leaves_input_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "посттар.csv"
            original = "\ufeffpost_id,format,reach,views\nқазақша,Reel,100,250\n".encode("utf-8")
            source.write_bytes(original)
            proc = subprocess.run([sys.executable, str(SCRIPT), str(source)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["posts"][0]["post_id"], "қазақша")
            self.assertEqual(source.read_bytes(), original)

    def test_cli_error_is_nonzero_and_no_partial_json(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.csv"
            source.write_text("post_id,format,reach\na,reel,NaN\n", encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPT), str(source)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(proc.stdout, "")
            self.assertIn("Error:", proc.stderr)


if __name__ == "__main__":
    unittest.main()
