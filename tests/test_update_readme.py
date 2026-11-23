import io
import json
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update_readme


class UpdateReadmeTests(unittest.TestCase):
    def test_profile_evidence_counts_cves_independently_of_other_activity(self):
        config = update_readme.profile_badges()
        count = len(config["published_cves"]["entries"])
        expected = (
            f"Public records credit my work in {count} published CVEs. "
            "[Research record and sources](RESEARCH.md)."
        )
        self.assertEqual(update_readme.build_profile_evidence(config), expected)
        config["cisa_coordination"]["active_cases"] = 99
        config["published_advisories"]["entries"] = []
        self.assertEqual(update_readme.build_profile_evidence(config), expected)

    def test_generation_updates_both_documents_and_preserves_editorial_text(self):
        config = update_readme.profile_badges()
        new_cve = {"id": "CVE-2099-10000", "source": "https://example.test/cve"}
        new_advisory = {
            "id": "GHSA-test-test-test",
            "source": "https://example.test/advisory",
            "product": "Test product",
            "summary": "Synthetic test advisory.",
            "published_at": "2099-01-01",
        }
        config["published_cves"]["entries"].append(new_cve)
        config["published_advisories"]["entries"].append(new_advisory)
        original_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        original_research = (ROOT / "RESEARCH.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            readme, research, registry = (root / name for name in (
                "README.md", "RESEARCH.md", "profile_badges.json"))
            readme.write_text(original_readme, encoding="utf-8")
            research.write_text(original_research, encoding="utf-8")
            registry.write_text(json.dumps(config), encoding="utf-8")
            with patch.multiple(update_readme, README=str(readme),
                                RESEARCH=str(research), PROFILE_BADGES=str(registry)), \
                    redirect_stdout(io.StringIO()):
                update_readme.main()
                generated_readme = readme.read_text(encoding="utf-8")
                generated_research = research.read_text(encoding="utf-8")
                self.assertEqual(generated_readme, update_readme.replace_block(
                    original_readme, "PROFILE_EVIDENCE",
                    update_readme.build_profile_evidence(config)))
                for entry in (new_cve, new_advisory):
                    self.assertIn(f"[{entry['id']}]({entry['source']})", generated_research)
                    self.assertNotIn(entry["id"], generated_readme)
                active = config["cisa_coordination"]["active_cases"]
                published = len(config["cisa_ics"]["entries"])
                self.assertIn(f"{active} active vulnerability coordination cases", generated_research)
                self.assertIn(f"Researcher credit in {published} published CISA ICS advisories.", generated_research)
                self.assertNotIn("img.shields.io", generated_readme)
                update_readme.main()
                self.assertEqual(readme.read_text(encoding="utf-8"), generated_readme)
                self.assertEqual(research.read_text(encoding="utf-8"), generated_research)

    def test_missing_appendix_marker_does_not_partially_update_profile(self):
        config = update_readme.profile_badges()
        config["published_cves"]["entries"].append(
            {"id": "CVE-2099-10000", "source": "https://example.test/cve"})
        original_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        original_research = (ROOT / "RESEARCH.md").read_text(encoding="utf-8").replace(
            "<!-- ADVISORY_LIST:END -->", "")
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            readme, research, registry = (root / name for name in (
                "README.md", "RESEARCH.md", "profile_badges.json"))
            readme.write_text(original_readme, encoding="utf-8")
            research.write_text(original_research, encoding="utf-8")
            registry.write_text(json.dumps(config), encoding="utf-8")
            with patch.multiple(update_readme, README=str(readme),
                                RESEARCH=str(research), PROFILE_BADGES=str(registry)):
                with self.assertRaisesRegex(SystemExit, "ADVISORY_LIST"):
                    update_readme.main()
            self.assertEqual(readme.read_text(encoding="utf-8"), original_readme)
            self.assertEqual(research.read_text(encoding="utf-8"), original_research)

    def test_cisa_list_links_each_advisory(self):
        config = update_readme.profile_badges()
        block = update_readme.build_cisa_list(config)
        self.assertTrue(block.startswith("## CISA coordination"))
        self.assertIn("### CISA ICS advisories", block)
        for entry in update_readme.cisa_advisories(config):
            self.assertEqual(
                block.count("[" + entry["advisory"] + "](" + entry["url"] + ")"),
                1,
            )
            self.assertIn(entry["published_at"], block)

    def test_active_coordination_count_is_independent_of_public_advisories(self):
        config = deepcopy(update_readme.profile_badges())
        published_count = len(config["cisa_ics"]["entries"])
        for active_count in (7, 3):
            with self.subTest(active_count=active_count):
                config["cisa_coordination"]["active_cases"] = active_count
                section = update_readme.build_cisa_list(config)
                self.assertIn(f"{active_count} active vulnerability coordination cases", section)
                self.assertIn(f"Researcher credit in {published_count} published CISA ICS advisories.", section)
                self.assertIn(config["cisa_coordination"]["last_verified"], section)

    def test_coordination_rejects_invalid_counts_and_review_dates(self):
        config = deepcopy(update_readme.profile_badges())
        for field, value in (("active_cases", True), ("active_cases", -1),
                             ("last_verified", "2026-02-30"),
                             ("last_verified", "not a date")):
            with self.subTest(field=field, value=value):
                invalid = deepcopy(config)
                invalid["cisa_coordination"][field] = value
                with self.assertRaises(ValueError):
                    update_readme.cisa_coordination(invalid)

    def test_cisa_registry_rejects_duplicate_ids(self):
        config = update_readme.profile_badges()
        entries = update_readme.cisa_advisories(config)
        duplicate = entries + [deepcopy(entries[0])]
        with self.assertRaisesRegex(ValueError, "Duplicate CISA advisory ID"):
            update_readme.validate_cisa_advisories(duplicate)

    def test_cisa_registry_rejects_impossible_dates_and_urls(self):
        config = update_readme.profile_badges()
        entries = deepcopy(update_readme.cisa_advisories(config))
        entries[0]["published_at"] = "2026-02-30"
        with self.assertRaisesRegex(ValueError, "Invalid CISA publication date"):
            update_readme.validate_cisa_advisories(entries)
        entries[0]["published_at"] = "2026-09-29"
        entries[0]["url"] = entries[1]["url"]
        with self.assertRaisesRegex(ValueError, "Unexpected CISA URL"):
            update_readme.validate_cisa_advisories(entries)


if __name__ == "__main__":
    unittest.main()
