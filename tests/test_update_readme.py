import pathlib
import sys
import unittest

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


if __name__ == "__main__":
    unittest.main()
