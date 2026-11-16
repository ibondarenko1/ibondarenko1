import pathlib
import sys
import unittest
from copy import deepcopy
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import discover_advisories as discovery
import update_readme


def github_record():
    return {
        "ghsa_id": "GHSA-mr9f-g8qf-4w4j", "cve_id": "CVE-2026-118628",
        "state": "published", "published_at": "2026-11-13T02:52:27Z",
        "withdrawn_at": None,
        "html_url": "https://github.com/mlflow/mlflow/security/advisories/GHSA-mr9f-g8qf-4w4j",
        "summary": "SSRF through client-supplied artifact URIs.",
        "vulnerabilities": [{"package": {"name": "mlflow"}}],
        "credits_detailed": [{"user": {"login": "ibondarenko1"},
                              "type": "reporter", "state": "accepted"}],
    }


def opc_record():
    return {
        "document": {"distribution": {"tlp": {"label": "WHITE"}},
                     "tracking": {"status": "final", "initial_release_date": "2026-11-13T00:00:00Z"}},
        "product_tree": {"branches": [{"name": "OPC UA .NET Standard Stack"}]},
        "vulnerabilities": [{
            "ids": [{"system_name": "GCVE", "text": "GCVE-105-2026-011"}],
            "title": "Sessionless Call reads another session's result file.",
            "acknowledgments": [{"names": ["Ievgen Bondarenko"]}],
        }],
    }


OPC_PATH = "csaf/2026/011/gcve-105-2026-011.json"


class DiscoverAdvisoriesTests(unittest.TestCase):
    def test_mlflow_reporter_credit_is_preserved(self):
        entry = discovery.github_entry(github_record(), "mlflow/mlflow")
        self.assertEqual(entry["cve"], "CVE-2026-118628")
        self.assertEqual(entry["credit"], "reporter")

    def test_private_withdrawn_unaccepted_or_unrelated_credits_are_ignored(self):
        for field, value in (("state", "draft"), ("withdrawn_at", "2026-11-14T00:00:00Z")):
            record = github_record()
            record[field] = value
            self.assertIsNone(discovery.github_entry(record, "mlflow/mlflow"))
        for change in ({"state": "pending"}, {"type": "remediation_developer"},
                       {"user": {"login": "someone-else"}}):
            record = github_record()
            record["credits_detailed"][0].update(change)
            self.assertIsNone(discovery.github_entry(record, "mlflow/mlflow"))
        record = github_record()
        record["credits_detailed"] = []
        record["description"] = "Ievgen Bondarenko is mentioned here."
        self.assertIsNone(discovery.github_entry(record, "mlflow/mlflow"))

    def test_published_list_follows_cursor_pagination_without_authentication(self):
        prefix = "https://api.github.com/repos/mlflow/mlflow/security-advisories"
        next_url = prefix + "?after=cursor&state=published"
        responses = [(b'[1]', {"Link": '<' + next_url + '>; rel="next"'}), (b'[2]', {})]
        with patch.object(discovery, "get", side_effect=responses) as fetch:
            self.assertEqual(list(discovery.github_advisories("mlflow/mlflow")), [1, 2])
        self.assertTrue(all(call.kwargs["authenticated"] is False for call in fetch.call_args_list))

    def test_opc_gcve_requires_final_public_direct_credit(self):
        self.assertEqual(discovery.opc_entries(opc_record(), OPC_PATH)[0]["id"], "GCVE-105-2026-011")
        record = opc_record()
        record["document"]["tracking"]["status"] = "draft"
        self.assertEqual(discovery.opc_entries(record, OPC_PATH), [])
        record = opc_record()
        record["document"]["distribution"]["tlp"]["label"] = "AMBER"
        self.assertEqual(discovery.opc_entries(record, OPC_PATH), [])
        record = opc_record()
        record["vulnerabilities"][0]["acknowledgments"][0]["names"] = ["Someone Else"]
        self.assertEqual(discovery.opc_entries(record, OPC_PATH), [])

    def test_merge_is_idempotent_and_gcve_does_not_inflate_cve_count(self):
        config = {"published_cves": {"entries": []}}
        ghsa = discovery.github_entry(github_record(), "mlflow/mlflow")
        gcve = discovery.opc_entries(opc_record(), OPC_PATH)[0]
        discovery.merge_entries(config, [ghsa, gcve], lambda _: True)
        expected = deepcopy(config)
        discovery.merge_entries(config, [ghsa, gcve], lambda _: True)
        self.assertEqual(config, expected)
        self.assertEqual([item["id"] for item in config["published_cves"]["entries"]], ["CVE-2026-118628"])
        self.assertEqual([item["id"] for item in config["published_advisories"]["entries"]], ["GCVE-105-2026-011"])
        self.assertIn("GCVE-105-2026-011", update_readme.build_advisory_list(config))

    def test_reserved_cve_stays_out_of_count_then_promotes_once(self):
        config = {"published_cves": {"entries": []}}
        ghsa = discovery.github_entry(github_record(), "mlflow/mlflow")
        discovery.merge_entries(config, [ghsa], lambda _: False)
        self.assertEqual(config["published_cves"]["entries"], [])
        self.assertEqual(len(config["published_advisories"]["entries"]), 1)
        discovery.merge_entries(config, [ghsa], lambda _: True)
        self.assertEqual(len(config["published_cves"]["entries"]), 1)
        self.assertEqual(config["published_advisories"]["entries"], [])

    def test_existing_editorial_cve_metadata_is_not_overwritten(self):
        entry = {"id": "CVE-2026-118628", "source": "https://example.test/reviewed",
                 "product": "MLflow", "summary": "Reviewed description."}
        config = {"published_cves": {"entries": [entry.copy()]}}
        ghsa = discovery.github_entry(github_record(), "mlflow/mlflow")
        discovery.merge_entries(config, [ghsa], lambda _: True)
        self.assertEqual(config["published_cves"]["entries"], [entry])


if __name__ == "__main__":
    unittest.main()
