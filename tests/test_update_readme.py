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
                self.assertIn(f"CISA%20ICS%20Published-{count}-", block)
                self.assertIn(f"{count} published CISA ICS {noun} with researcher credit", block)
                self.assertIn("#cisa-ics-advisories", block)

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
                badges = update_readme.build_badges_block(config)
                section = update_readme.build_cisa_list(config)
                self.assertIn(f"CISA%20Active%20Cases-{active_count}-", badges)
                self.assertIn(f"CISA%20ICS%20Published-{published_count}-", badges)
                self.assertIn("#cisa-coordination", badges)
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
