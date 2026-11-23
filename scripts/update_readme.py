#!/usr/bin/env python3
"""Refresh the profile's results and complete public research records.

README.md includes compact linked counts for published work.
RESEARCH.md retains complete indexes of published CVEs, advisories, and PRs.
Only marked sections are regenerated; the surrounding text is preserved.
"""
from datetime import date, datetime
from html import escape
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
RESEARCH = os.path.join(ROOT, "RESEARCH.md")
PROFILE_BADGES = os.path.join(ROOT, "data", "profile_badges.json")
CISA_ADVISORY_RE = re.compile(r"ICSA-[0-9]{2}-[0-9]{3}-[0-9]{2}")


def validate_cisa_advisories(entries):
    """Validate the reviewed list of current CISA researcher credits."""
    if not isinstance(entries, list) or not entries:
        raise ValueError("CISA advisory list must not be empty")
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Invalid CISA advisory entry")
        advisory = entry.get("advisory")
        if not isinstance(advisory, str) or not CISA_ADVISORY_RE.fullmatch(advisory):
            raise ValueError("Invalid CISA advisory ID: " + str(advisory))
        if advisory in seen:
            raise ValueError("Duplicate CISA advisory ID: " + advisory)
        seen.add(advisory)
        product = entry.get("product")
        if not isinstance(product, str) or not product.strip():
            raise ValueError("Missing CISA product for " + advisory)
        published_at = entry.get("published_at")
        if not isinstance(published_at, str) or not re.fullmatch(
                r"[0-9]{4}-[0-9]{2}-[0-9]{2}", published_at):
            raise ValueError("Invalid CISA publication date for " + advisory)
        try:
            date.fromisoformat(published_at)
        except ValueError as exc:
            raise ValueError("Invalid CISA publication date for " + advisory) from exc
        expected_url = (
            "https://www.cisa.gov/news-events/ics-advisories/"
            + advisory.lower()
        )
        if entry.get("url") != expected_url:
            raise ValueError("Unexpected CISA URL for " + advisory)
    return entries


def profile_badges():
    """Load verified published CVE entries, rejecting duplicate or invalid IDs.

    Entries are reviewed against their linked public CVE/vendor/CISA/GHSA
    sources before inclusion. This is not a claim that every existing
    CVE record is discoverable automatically via a single API.
    """
    with open(PROFILE_BADGES, encoding="utf-8") as handle:
        config = json.load(handle)
    if "cisa_coordination" in config:
        raise ValueError("Private coordination data does not belong in the public registry")
    cisa_config = config.get("cisa_ics")
    if not isinstance(cisa_config, dict):
        raise ValueError("Missing CISA advisory registry")
    validate_cisa_advisories(cisa_config.get("entries"))
    merged_prs(config)
    entries = config["published_cves"]["entries"]
    ids = set()
    for entry in entries:
        cve = entry["id"]
        if not re.fullmatch(r"CVE-[0-9]{4}-[0-9]{4,}", cve):
            raise ValueError("Invalid CVE ID: " + cve)
        if cve in ids:
            raise ValueError("Duplicate CVE ID: " + cve)
        if not entry["source"].startswith("https://"):
            raise ValueError("Missing HTTPS attribution source for " + cve)
        has_product = "product" in entry
        has_summary = "summary" in entry
        if has_product != has_summary:
            raise ValueError("Product and summary must be supplied together for " + cve)
        if has_product:
            if not all(isinstance(entry[field], str) and entry[field].strip()
                       for field in ("product", "summary")):
                raise ValueError("Empty product or summary for " + cve)
        ids.add(cve)
    for entry in config.get("published_advisories", {}).get("entries", []):
        advisory = entry["id"]
        if not re.fullmatch(r"(?:GCVE-[0-9]+-[0-9]{4}-[0-9]+|GHSA-[a-z0-9-]+)", advisory):
            raise ValueError("Invalid vendor advisory ID: " + advisory)
        if advisory in ids:
            raise ValueError("Duplicate vendor advisory ID: " + advisory)
        ids.add(advisory)
        if not entry["source"].startswith("https://"):
            raise ValueError("Missing HTTPS advisory source")
        if not all(isinstance(entry.get(field), str) and entry[field].strip()
                   for field in ("product", "summary", "published_at")):
            raise ValueError("Missing vendor advisory metadata")
        date.fromisoformat(entry["published_at"])
    return config


def cisa_advisories(config=None):
    """Return validated CISA advisories from a registry configuration."""
    config = config or profile_badges()
    return validate_cisa_advisories(config["cisa_ics"]["entries"])



def merged_prs(config=None):
    """Validate the complete, dated inventory behind the merged PR count."""
    registry = (config or profile_badges()).get("merged_prs")
    if not isinstance(registry, dict):
        raise ValueError("Missing merged PR registry")
    count = registry.get("count")
    entries = registry.get("entries")
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValueError("Invalid merged PR count")
    if not isinstance(entries, list) or count != len(entries):
        raise ValueError("Merged PR count must match the complete entries list")
    verified = registry.get("verified_at")
    if not isinstance(verified, str) or not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}", verified):
        raise ValueError("Invalid merged PR verification date")
    try:
        date.fromisoformat(verified)
    except ValueError as exc:
        raise ValueError("Invalid merged PR verification date") from exc
    if not isinstance(registry.get("url"), str) or not registry["url"].startswith(
            "https://github.com/search?"):
        raise ValueError("Missing merged PR source query")
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Invalid merged PR entry")
        repository = entry.get("repository")
        if not isinstance(repository, str) or not re.fullmatch(
                r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("Invalid merged PR repository")
        if repository.split("/", 1)[0].lower() == "ibondarenko1":
            raise ValueError("Merged PR inventory excludes personal repositories")
        url = entry.get("url")
        if not isinstance(url, str) or not re.fullmatch(
                re.escape("https://github.com/" + repository + "/pull/")
                + r"[1-9][0-9]*", url):
            raise ValueError("Unexpected merged PR URL for " + repository)
        if url.lower() in seen:
            raise ValueError("Duplicate merged PR URL: " + url)
        seen.add(url.lower())
        if not isinstance(entry.get("title"), str) or not entry["title"].strip():
            raise ValueError("Missing merged PR title")
        if "merged_at" in entry:
            try:
                datetime.strptime(entry["merged_at"], "%Y-%m-%dT%H:%M:%SZ")
            except (TypeError, ValueError) as exc:
                raise ValueError("Invalid merged PR date") from exc
        if "workflow_experiment" in entry and not isinstance(
                entry["workflow_experiment"], bool):
            raise ValueError("Invalid merged PR workflow experiment label")
    return registry


def markdown_text(value):
    """Keep external titles readable without introducing Markdown or HTML."""
    value = escape(" ".join(value.split()), quote=False)
    return re.sub(r"([\\`*_\[\]|])", r"\\\1", value)


def build_profile_evidence(config=None):
    """Show compact counts linking to complete public records."""
    config = config or profile_badges()
    cve_count = len(config["published_cves"]["entries"])
    prs = merged_prs(config)
    cisa_count = len(cisa_advisories(config))
    return (
        f"**[{cve_count} published CVEs](RESEARCH.md#published-cves)** · "
        f"**[{prs['count']} merged pull requests](RESEARCH.md#merged-pull-requests)** · "
        f"**[{cisa_count} published CISA ICS advisories](RESEARCH.md#cisa-ics-advisories)**"
    )


def build_cve_list(config=None):
    """Build the clickable, descriptive CVE index from the reviewed registry.

    Automatically discovered entries remain valid before optional editorial
    metadata is reviewed and added to the registry.
    """
    config = config or profile_badges()
    entries = config["published_cves"]["entries"]
    rows = ["## Published CVEs", "",
            "Published CVEs with public researcher credit. Listed roles follow the source advisory.", ""]
    for item in sorted(entries, key=lambda row: row["id"]):
        line = "- [" + item["id"] + "](" + item["source"] + ")"
        if item.get("product") and item.get("summary"):
            line += " · **" + item["product"] + "**: " + item["summary"]
        if item.get("credit"):
            line += " Credit: " + item["credit"] + "."
        rows.append(line)
    return "\n".join(rows)


def build_advisory_list(config=None):
    """Show credited vendor publications independently of the CVE count."""
    config = config or profile_badges()
    rows = ["## Published vendor advisories", "",
            "Public advisories acknowledging my research.", ""]
    for item in config.get("published_advisories", {}).get("entries", []):
        line = ("- [" + item["id"] + "](" + item["source"] + ") · **"
                + item["product"] + "**: " + item["summary"]
                + " Published " + item["published_at"] + ".")
        if item.get("cve"):
            line += " Associated CVE: " + item["cve"] + "."
        rows.append(line)
    return "\n".join(rows)


def build_merged_pr_list(config=None):
    """List every reviewed merged PR without treating every entry as a fix."""
    registry = merged_prs(config)
    rows = ["## Merged pull requests", "",
            f"{registry['count']} merged pull requests authored by ibondarenko1 "
            "outside personal repositories. Includes code, tests, documentation, "
            "detection queries, resource entries, and workflow experiments. "
            "Company workflow experiments are labelled below.", "",
            "[Source query](" + registry["url"] + "). Verified "
            + registry["verified_at"] + ".", "",
            "| Pull request | Contribution | Merged |",
            "| --- | --- | --- |"]
    for entry in registry["entries"]:
        number = entry["url"].rsplit("/", 1)[1]
        link = ("[" + markdown_text(entry["repository"]) + "#" + number
                + "](" + entry["url"] + ")")
        title = markdown_text(entry["title"])
        if entry.get("workflow_experiment"):
            title += " (company workflow experiment)"
        rows.append("| " + link + " | " + title + " | "
                    + entry.get("merged_at", "")[:10] + " |")
    return "\n".join(rows)



def build_cisa_list(config=None):
    """Show only published CISA ICS advisories with researcher credit."""
    config = config or profile_badges()
    advisories = cisa_advisories(config)
    rows = ["## CISA ICS advisories", "",
            f"Researcher credit in {len(advisories)} published CISA ICS "
            + ("advisory" if len(advisories) == 1 else "advisories") + ".", "",
            "| Product | Advisory | Published |",
            "| --- | --- | --- |"]
    for item in advisories:
        advisory = "[" + item["advisory"] + "](" + item["url"] + ")"
        rows.append("| " + item["product"] + " | " + advisory +
                    " | " + item["published_at"] + " |")
    return "\n".join(rows)


def validate_blocks(text, names):
    """Require unique, ordered, non-overlapping generated sections."""
    spans = []
    for name in names:
        start, end = "<!-- %s:START -->" % name, "<!-- %s:END -->" % name
        if text.count(start) != 1 or text.count(end) != 1:
            sys.exit("marker pair %s must occur exactly once" % name)
        left, right = text.index(start), text.index(end)
        if left >= right:
            sys.exit("marker pair %s is out of order" % name)
        spans.append((left, right + len(end), name))
    spans.sort()
    for previous, current in zip(spans, spans[1:]):
        if current[0] < previous[1]:
            sys.exit("marker pairs %s and %s overlap" % (previous[2], current[2]))


def replace_block(text, name, content):
    validate_blocks(text, (name,))
    start, end = "<!-- %s:START -->" % name, "<!-- %s:END -->" % name
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.DOTALL)
    return pattern.sub(lambda _m: start + "\n" + content + "\n" + end, text)


def main():
    config = profile_badges()
    with open(README, encoding="utf-8") as handle:
        original_readme = handle.read()
    with open(RESEARCH, encoding="utf-8") as handle:
        original_research = handle.read()
    validate_blocks(original_readme, ("PROFILE_EVIDENCE",))
    validate_blocks(original_research, ("CISA_LIST", "CVE_LIST", "ADVISORY_LIST", "PR_LIST"))
    updated_readme = replace_block(
        original_readme, "PROFILE_EVIDENCE", build_profile_evidence(config))
    updated_research = replace_block(
        original_research, "CISA_LIST", build_cisa_list(config))
    updated_research = replace_block(
        updated_research, "CVE_LIST", build_cve_list(config))
    updated_research = replace_block(
        updated_research, "ADVISORY_LIST", build_advisory_list(config))
    updated_research = replace_block(
        updated_research, "PR_LIST", build_merged_pr_list(config))
    # Validate every generated section before writing either document.
    for path, original, updated in (
            (README, original_readme, updated_readme),
            (RESEARCH, original_research, updated_research)):
        name = os.path.basename(path)
        if updated == original:
            print(name + " already up to date.")
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(updated)
        print(name + " updated.")


if __name__ == "__main__":
    main()
