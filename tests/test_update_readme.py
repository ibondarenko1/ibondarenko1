import pathlib
import sys
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import update_readme


class UpdateReadmeTests(unittest.TestCase):
    def test_merged_pr_count_uses_the_public_search_view(self):
        with mock.patch.object(
            update_readme, "api", return_value={"total_count": 25}
        ) as request:
            self.assertEqual(update_readme.merged_prs_count(), 25)
        request.assert_called_once()
        self.assertFalse(request.call_args.kwargs["use_token"])


if __name__ == "__main__":
    unittest.main()
