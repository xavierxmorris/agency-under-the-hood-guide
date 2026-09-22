from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate  # noqa: E402


class RepositoryValidationTests(unittest.TestCase):
    def test_required_files(self) -> None:
        self.assertEqual([], validate.validate_required_files())

    def test_claim_ledger(self) -> None:
        self.assertEqual([], validate.validate_claims())

    def test_architecture_data(self) -> None:
        self.assertEqual([], validate.validate_architecture())

    def test_maturity_data(self) -> None:
        self.assertEqual([], validate.validate_maturity())

    def test_scorecards(self) -> None:
        self.assertEqual([], validate.validate_scorecards())

    def test_local_markdown_links(self) -> None:
        self.assertEqual([], validate.validate_markdown_links())

    def test_claim_references(self) -> None:
        self.assertEqual([], validate.validate_claim_references())

    def test_batch_example(self) -> None:
        self.assertEqual([], validate.validate_batch_example())

    def test_lab_contracts(self) -> None:
        self.assertEqual([], validate.validate_labs())

    def test_public_safety(self) -> None:
        self.assertEqual([], validate.validate_public_safety())

    def test_public_safety_detects_common_leaks(self) -> None:
        samples = [
            "C:" + "\\\\" + "Users" + "\\\\" + "someone" + "\\\\" + "repo",
            "/" + "home" + "/" + "someone" + "/" + "repo",
            "gh" + "p_" + "abcdefghijklmnopqrstuvwxyz123456",
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertTrue(validate.public_safety_findings(sample))

    def test_claim_cycle_is_rejected(self) -> None:
        bad = """
        {
          "schema_version": 1,
          "agency_release": "test",
          "claims": [
            {"id": "I-001", "kind": "interpretation", "category": "test",
             "status": "released", "statement": "cycle",
             "derived_from": ["I-001"]}
          ]
        }
        """
        original = validate.load_json
        try:
            validate.load_json = lambda _: __import__("json").loads(bad)
            self.assertTrue(validate.validate_claims())
        finally:
            validate.load_json = original

    def test_windows_evidence_traversal_is_rejected(self) -> None:
        bad = """
        {
          "schema_version": 1,
          "agency_release": "test",
          "claims": [
            {"id": "F-001", "kind": "fact", "category": "test",
             "status": "released", "statement": "bad path",
             "evidence": [
               {"path": "docs/agency/..\\\\..\\\\README.md", "section": "Title"}
             ]}
          ]
        }
        """
        original = validate.load_json
        try:
            validate.load_json = lambda _: __import__("json").loads(bad)
            errors = validate.validate_claims()
            self.assertTrue(any("invalid evidence path" in error for error in errors))
        finally:
            validate.load_json = original

    def test_invalid_batch_validation_is_rejected(self) -> None:
        invalid = """
batch:
  id: broken
job:
  iterations: "{{iterations}}"
validation:
  expectedExitCode: 0
"""
        self.assertTrue(validate.batch_example_errors(invalid))

    def test_generated_site_is_current(self) -> None:
        self.assertEqual([], validate.validate_generated_site())


if __name__ == "__main__":
    unittest.main()
