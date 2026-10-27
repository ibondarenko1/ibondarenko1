import pathlib
import sys
import unittest
from copy import deepcopy

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update_readme


class UpdateReadmeTests(unittest.TestCase):
    def test_merged_prs_uses_reviewed_registry_value(self):
        config = {
            "merged_prs": {
                "count": 25,
                "verified_at": "2026-10-22",
                "url": "https://github.com/search?q=test&type=pullrequests",
            }
        }
        self.assertEqual(update_readme.merged_prs(config)["count"], 25)

    def test_merged_prs_rejects_invalid_count(self):
        config = {
            "merged_prs": {
                "count": True,
                "verified_at": "2026-10-22",
                "url": "https://github.com/search?q=test&type=pullrequests",
            }
        }
        with self.assertRaisesRegex(ValueError, "Invalid merged PR count"):
            update_readme.merged_prs(config)

    def test_badge_links_to_the_same_public_search(self):
        config = update_readme.profile_badges()
        block = update_readme.build_badges_block()
        self.assertIn(config["merged_prs"]["url"], block)

    def test_cisa_badge_counts_credits_and_uses_profile_anchor(self):
        config = update_readme.profile_badges()
        entries = deepcopy(update_readme.cisa_advisories(config))
        for count, noun in ((1, "advisory"), (2, "advisories")):
            with self.subTest(count=count):
                config["cisa_ics"]["entries"] = entries[:count]
                block = update_readme.build_badges_block(config)
                self.assertIn(f"CISA%20ICS%20Advisories-{count}-", block)
                self.assertIn(f"{count} CISA ICS {noun} with researcher credit", block)
                self.assertIn("#cisa-ics-advisories", block)

    def test_cisa_list_links_each_advisory(self):
        config = update_readme.profile_badges()
        block = update_readme.build_cisa_list(config)
        self.assertTrue(block.startswith("## CISA ICS advisories"))
        for entry in update_readme.cisa_advisories(config):
            self.assertEqual(
                block.count("[" + entry["advisory"] + "](" + entry["url"] + ")"),
                1,
            )
            self.assertIn(entry["published_at"], block)

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
