"""Transport and runtime checks for the complete Unicode regression fixture pack."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "examples/unicode-regression"
spec = importlib.util.spec_from_file_location("unicode_regression_verify", PACK / "verify.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class UnicodeRegressionTests(unittest.TestCase):
    def setUp(self):
        self.original = (PACK / "fixtures.json").read_bytes()
        self.data = json.loads(self.original)

    def test_complete_pack_matches_encoding_counts_and_remains_untouched(self):
        report = verifier.verify(self.data)
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["fixturesChecked"], 20)
        self.assertEqual((PACK / "fixtures.json").read_bytes(), self.original)
        accent = {row["id"]: row for row in self.data["fixtures"]}
        self.assertNotEqual(accent["accent-composed"]["text"], accent["accent-decomposed"]["text"])
        self.assertEqual(accent["accent-composed"]["expected"]["graphemeClusters"], accent["accent-decomposed"]["expected"]["graphemeClusters"])

    def test_transport_that_removes_a_joiner_is_detected(self):
        fixture = next(row for row in self.data["fixtures"] if row["id"] == "emoji-zwj")
        fixture["text"] = fixture["text"].replace("\u200d", "")
        with self.assertRaisesRegex(ValueError, "source text differs"):
            verifier.verify(self.data)

    def test_encoding_regression_and_non_scalar_input_are_rejected(self):
        fixture = next(row for row in self.data["fixtures"] if row["id"] == "kazakh-word")
        fixture["expected"]["utf8Bytes"] -= 1
        with self.assertRaisesRegex(ValueError, "utf8Bytes"):
            verifier.verify(self.data)
        fixture["text"] = "\ud800"
        with self.assertRaisesRegex(ValueError, "surrogate"):
            verifier.verify(self.data)

    @unittest.skipUnless(shutil.which("node"), "Node is optional for Python tests; run verify.mjs to check segmentation")
    def test_javascript_checks_reference_and_detects_changed_segmentation(self):
        proc = subprocess.run(["node", str(PACK / "verify.mjs")], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report["fixturesChecked"], 20)
        self.assertEqual(report["graphemes"]["status"], "checked_against_reference")
        self.assertEqual((PACK / "fixtures.json").read_bytes(), self.original)
        fixture = next(row for row in self.data["fixtures"] if row["id"] == "emoji-zwj")
        fixture["expected"]["graphemeClusters"] = 2
        with tempfile.TemporaryDirectory() as directory:
            altered = Path(directory) / "altered.json"
            altered.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
            bad = subprocess.run(["node", str(PACK / "verify.mjs"), str(altered)], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("graphemeClusters", bad.stderr)

    @unittest.skipUnless(shutil.which("node"), "Node is optional for Python tests; run verify.mjs to check segmentation")
    def test_missing_segmenter_does_not_become_a_code_point_approximation(self):
        code = """
import { readFileSync } from 'node:fs';
const { verify } = await import(process.argv[1]);
const data = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify(verify(data, { segmenter: null })));
"""
        proc = subprocess.run(["node", "--input-type=module", "-e", code, (PACK / "verify.mjs").as_uri(), str(PACK / "fixtures.json")], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report["status"], "partial_no_segmenter")
        self.assertEqual(report["graphemes"]["status"], "not_measured")
        self.assertTrue(all(row["actual"]["graphemeClusters"] is None for row in report["checks"]))


if __name__ == "__main__":
    unittest.main()
