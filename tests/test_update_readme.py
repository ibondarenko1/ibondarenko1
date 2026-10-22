import json
import pathlib
import sys
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update_readme


class UpdateReadmeTests(unittest.TestCase):
    @staticmethod
    def search_page(count=25, limited=False):
        data = {
            "payload": {
                "blackbirdSearchRoute": {
                    "errors": [],
                    "logged_in": False,
                    "result_count": count,
                    "type": "pullrequests",
                    "warn_limited_results": limited,
                }
            }
        }
        return (
            '<script type="application/json" '
            'data-target="react-app.embeddedData">'
            + json.dumps(data)
            + "</script>"
        )

    def test_merged_pr_count_uses_public_html_search_payload(self):
        with mock.patch.object(
            update_readme, "public_search_page", return_value=self.search_page()
        ) as request:
            self.assertEqual(update_readme.merged_prs_count(), 25)
        request.assert_called_once_with(update_readme.merged_prs_search_url())

    def test_merged_pr_count_rejects_limited_results(self):
        with mock.patch.object(
            update_readme,
            "public_search_page",
            return_value=self.search_page(limited=True),
        ):
            with self.assertRaisesRegex(ValueError, "incomplete results"):
                update_readme.merged_prs_count()

    def test_merged_pr_count_rejects_missing_payload(self):
        with mock.patch.object(
            update_readme, "public_search_page", return_value="<html></html>"
        ):
            with self.assertRaisesRegex(ValueError, "payload was not found"):
                update_readme.merged_prs_count()

    def test_badge_links_to_the_same_public_search(self):
        with mock.patch.object(update_readme, "merged_prs_count", return_value=25):
            block = update_readme.build_badges_block()
        self.assertIn(update_readme.merged_prs_search_url(), block)


if __name__ == "__main__":
    unittest.main()
