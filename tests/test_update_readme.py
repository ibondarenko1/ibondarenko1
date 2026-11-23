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
    def test_profile_evidence_counts_published_activity_independently(self):
        config = update_readme.profile_badges()
        original_counts = [len(config["published_cves"]["entries"]),
                           config["merged_prs"]["count"],
                           len(config["cisa_ics"]["entries"])]
        labels = ("published CVEs", "merged pull requests", "published CISA ICS advisories")
        targets = ("published-cves", "merged-pull-requests", "cisa-ics-advisories")
        for changed in range(3):
            with self.subTest(changed=targets[changed]):
                varied = deepcopy(config)
                counts = original_counts.copy()
                counts[changed] -= 1
                if changed == 0:
                    varied["published_cves"]["entries"].pop()
                elif changed == 1:
                    varied["merged_prs"]["entries"].pop()
                    varied["merged_prs"]["count"] -= 1
                else:
                    varied["cisa_ics"]["entries"].pop()
                block = update_readme.build_profile_evidence(varied)
                expected = " · ".join(
                    f"**[{count} {label}](RESEARCH.md#{target})**"
                    for count, label, target in zip(counts, labels, targets))
                self.assertEqual(block, expected)
                self.assertNotIn("verified", block.lower())
        original = update_readme.build_profile_evidence(config)
        config["published_advisories"]["entries"] = []
        self.assertEqual(update_readme.build_profile_evidence(config), original)

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
        new_pr = {"repository": "example/project", "title": "Synthetic contribution",
                  "url": "https://github.com/example/project/pull/123"}
        config["merged_prs"]["entries"].append(new_pr)
        config["merged_prs"]["count"] += 1
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
                expected_readme = update_readme.replace_block(
                    original_readme, "PROFILE_EVIDENCE",
                    update_readme.build_profile_evidence(config))
                self.assertEqual(generated_readme, expected_readme)
                for entry in (new_cve, new_advisory):
                    link = f"[{entry['id']}]({entry['source']})"
                    self.assertEqual(generated_research.count(link), 1)
                    self.assertNotIn(link, generated_readme)
                self.assertEqual(generated_research.count(
                    "[example/project#123](" + new_pr["url"] + ")"), 1)
                self.assertNotIn(new_pr["url"], generated_readme)
                published = len(config["cisa_ics"]["entries"])
                self.assertIn(f"Researcher credit in {published} published CISA ICS advisories.", generated_research)
                self.assertNotIn("img.shields.io", generated_readme)
                update_readme.main()
                self.assertEqual(readme.read_text(encoding="utf-8"), generated_readme)
                self.assertEqual(research.read_text(encoding="utf-8"), generated_research)

    def test_invalid_markers_fail_before_any_document_write(self):
        config = update_readme.profile_badges()
        config["published_cves"]["entries"].append(
            {"id": "CVE-2099-10000", "source": "https://example.test/cve"})
        good_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        good_research = (ROOT / "RESEARCH.md").read_text(encoding="utf-8")
        start, end = "<!-- PROFILE_EVIDENCE:START -->", "<!-- PROFILE_EVIDENCE:END -->"
        cisa_end = "<!-- CISA_LIST:END -->"
        pr_start, pr_end = "<!-- PR_LIST:START -->", "<!-- PR_LIST:END -->"
        reversed_readme = good_readme.replace(start, "TEMP_MARKER").replace(
            end, start).replace("TEMP_MARKER", end)
        crossed_research = good_research.replace(cisa_end, "").replace(
            pr_start, pr_start + "\n" + cisa_end)
        nested_research = good_research.replace(cisa_end, "").replace(
            pr_end, pr_end + "\n" + cisa_end)
        cases = [
            ("missing", good_readme.replace(end, ""), good_research, "PROFILE_EVIDENCE"),
            ("duplicate", good_readme + start + end, good_research, "PROFILE_EVIDENCE"),
            ("reversed", reversed_readme, good_research, "PROFILE_EVIDENCE"),
            ("crossed", good_readme, crossed_research, "overlap"),
            ("nested", good_readme, nested_research, "overlap"),
            ("appendix", good_readme, good_research.replace(
                "<!-- PR_LIST:END -->", ""), "PR_LIST"),
        ]
        for case, original_readme, original_research, error in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                readme, research, registry = (root / name for name in (
                    "README.md", "RESEARCH.md", "profile_badges.json"))
                readme.write_text(original_readme, encoding="utf-8")
                research.write_text(original_research, encoding="utf-8")
                registry.write_text(json.dumps(config), encoding="utf-8")
                with patch.multiple(update_readme, README=str(readme),
                                    RESEARCH=str(research), PROFILE_BADGES=str(registry)), \
                        patch("builtins.open", wraps=open) as opened:
                    with self.assertRaisesRegex(SystemExit, error):
                        update_readme.main()
                    for call in opened.call_args_list:
                        mode = call.args[1] if len(call.args) > 1 else call.kwargs.get("mode", "r")
                        self.assertFalse(any(flag in mode for flag in "wax+"))
                self.assertEqual(readme.read_text(encoding="utf-8"), original_readme)
                self.assertEqual(research.read_text(encoding="utf-8"), original_research)

    def test_complete_indexes_contain_every_entry(self):
        config = update_readme.profile_badges()
        config["merged_prs"]["entries"][0]["title"] = "Fix [bounds] <input> | `test`"
        for section, builder in (("published_cves", update_readme.build_cve_list),
                                 ("published_advisories", update_readme.build_advisory_list)):
            block = builder(config)
            for entry in config[section]["entries"]:
                self.assertEqual(block.count(f"[{entry['id']}]({entry['source']})"), 1)
        record = update_readme.build_merged_pr_list(config)
        self.assertTrue(record.startswith("## Merged pull requests"))
        self.assertNotIn("<!--", record)
        self.assertIn(r"Fix \[bounds\] &lt;input&gt; \| \`test\`", record)
        self.assertIn("code, tests, documentation, detection queries, resource entries, and workflow experiments", record)
        for entry in config["merged_prs"]["entries"]:
            self.assertEqual(record.count(f"({entry['url']})"), 1)
            self.assertIn(entry.get("merged_at", "")[:10], record)
        self.assertEqual(record.count("(company workflow experiment)"), sum(
            entry.get("workflow_experiment", False) for entry in config["merged_prs"]["entries"]))

    def test_merged_pr_registry_rejects_incomplete_or_invalid_records(self):
        config = update_readme.profile_badges()
        cases = []
        incomplete = deepcopy(config)
        incomplete["merged_prs"]["entries"].pop()
        cases.append(incomplete)
        duplicate = deepcopy(config)
        duplicate["merged_prs"]["entries"][1] = deepcopy(duplicate["merged_prs"]["entries"][0])
        cases.append(duplicate)
        for field, value in (("verified_at", "2026-02-30"), ("count", True)):
            invalid = deepcopy(config)
            invalid["merged_prs"][field] = value
            cases.append(invalid)
        for field, value in (("url", "https://github.com/other/repo/pull/1"),
                             ("title", ""), ("merged_at", "2026-02-30T00:00:00Z")):
            invalid = deepcopy(config)
            invalid["merged_prs"]["entries"][0][field] = value
            cases.append(invalid)
        for index, invalid in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(ValueError):
                update_readme.merged_prs(invalid)

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

    def test_private_coordination_is_rejected_and_never_rendered(self):
        config = update_readme.profile_badges()
        self.assertNotIn("cisa_coordination", config)
        legacy = deepcopy(config)
        legacy["cisa_coordination"] = {
            "active_cases": 999999,
            "last_verified": "2099-12-31",
            "source": "PRIVATE_TEST_SENTINEL",
        }
        for builder in (update_readme.build_profile_evidence,
                        update_readme.build_merged_pr_list,
                        update_readme.build_cve_list,
                        update_readme.build_advisory_list,
                        update_readme.build_cisa_list):
            with self.subTest(builder=builder.__name__):
                output = builder(legacy)
                self.assertEqual(output, builder(config))
                for private_value in ("999999", "2099-12-31", "PRIVATE_TEST_SENTINEL"):
                    self.assertNotIn(private_value, output)
        with tempfile.TemporaryDirectory() as directory:
            registry = pathlib.Path(directory) / "profile_badges.json"
            registry.write_text(json.dumps(legacy), encoding="utf-8")
            with patch.object(update_readme, "PROFILE_BADGES", str(registry)):
                with self.assertRaisesRegex(ValueError, "Private coordination data"):
                    update_readme.profile_badges()

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
