import datetime as dt
import io
import json
import pathlib
import sys
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import discover_cves


def record(cve_id="CVE-2026-12345", state="PUBLISHED", credit_type="finder", name="Ievgen Bondarenko"):
    return {
        "cveMetadata": {"cveId": cve_id, "state": state},
        "containers": {"cna": {"credits": [{"type": credit_type, "value": name}]}},
    }


def archive(*records):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as output:
        for item in records:
            cve_id = item["cveMetadata"]["cveId"]
            output.writestr("deltaCves/" + cve_id + ".json", json.dumps(item))
    return stream.getvalue()


class DiscoverCvesTests(unittest.TestCase):
    def test_credited_requires_published_structured_finder_credit(self):
        self.assertTrue(discover_cves.credited(record()))
        self.assertFalse(discover_cves.credited(record(state="REJECTED")))
        self.assertFalse(discover_cves.credited(record(credit_type="reporter")))
        self.assertFalse(discover_cves.credited(record(name="Someone Else")))

    def test_latest_delta_asset_is_selected_for_every_day(self):
        releases = []
        fixtures = (
            ("2026-10-20T01:00:00Z", "2026-10-20_delta_CVEs_at_0100Z.zip"),
            ("2026-10-21T00:30:00Z", "2026-10-20_delta_CVEs_at_end_of_day.zip"),
            ("2026-10-21T12:00:00Z", "2026-10-21_delta_CVEs_at_1200Z.zip"),
        )
        for stamp, asset_name in fixtures:
            day = asset_name[:10]
            hour = stamp[11:13]
            releases.append(
                {
                    "tag_name": "cve_" + day + "_" + hour + "00Z",
                    "published_at": stamp,
                    "assets": [
                        {
                            "name": asset_name,
                            "browser_download_url": "https://example.test/" + stamp,
                        }
                    ],
                }
            )
        selected = discover_cves.latest_delta_assets(
            releases, dt.date(2026, 10, 20), dt.date(2026, 10, 21)
        )
        self.assertEqual([item["name"] for item in selected], [
            "2026-10-20_delta_CVEs_at_end_of_day.zip",
            "2026-10-21_delta_CVEs_at_1200Z.zip",
        ])

    def test_missing_day_fails_instead_of_silently_skipping_records(self):
        releases = [
            {
                "tag_name": "cve_2026-10-21_1200Z",
                "published_at": "2026-10-21T12:00:00Z",
                "assets": [
                    {
                        "name": "2026-10-21_delta_CVEs_at_1200Z.zip",
                        "browser_download_url": "https://example.test/delta.zip",
                    }
                ],
            }
        ]
        with self.assertRaisesRegex(RuntimeError, "2026-10-20"):
            discover_cves.latest_delta_assets(
                releases, dt.date(2026, 10, 20), dt.date(2026, 10, 21)
            )

    def test_archive_record_and_metadata_ids_must_match(self):
        payload = archive(record())
        [(cve_id, raw)] = list(discover_cves.archive_records(payload))
        self.assertEqual(cve_id, "CVE-2026-12345")
        self.assertEqual(discover_cves.inspect_record(cve_id, raw)["id"], cve_id)
        mismatched = json.dumps(record(cve_id="CVE-2026-99999")).encode()
        with self.assertRaisesRegex(ValueError, "Record ID mismatch"):
            discover_cves.inspect_record("CVE-2026-12345", mismatched)

    def test_unexpected_archive_member_is_rejected(self):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as output:
            output.writestr("unexpected.txt", "not a CVE record")
        with self.assertRaisesRegex(ValueError, "Unexpected CVE delta archive member"):
            list(discover_cves.archive_records(stream.getvalue()))


if __name__ == "__main__":
    unittest.main()
