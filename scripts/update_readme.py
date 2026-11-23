#!/usr/bin/env python3
"""Regenerate the GitHub profile README's badges and public research indexes.

BADGES shows published CVEs, active CISA coordination cases, published CISA
advisories, and merged upstream PRs. Coordination uses a dated, manually reviewed
aggregate; public research indexes use the public-source registry.
These indexes are delimited by markers in README.md and updated together.
"""
from datetime import date
import json
import os
import re
import sys

USER = "ibondarenko1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
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


def merged_prs(config=None):
    """Count merged PRs authored by USER in repositories USER does not own.

    GitHub's repository-scoped Actions token cannot search other repositories,
    and anonymous searches from Actions runners have returned false zeroes.
    Keep the manually verified public count and its exact query together in the
    reviewed profile registry instead of letting the workflow corrupt the badge.
    """
    entry = (config or profile_badges())["merged_prs"]
    count = entry.get("count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValueError("Invalid merged PR count")
    if not entry.get("url", "").startswith("https://github.com/search?"):
        raise ValueError("Invalid merged PR public search URL")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", entry.get("verified_at", "")):
        raise ValueError("Invalid merged PR verification date")
    return entry


def profile_badges():
    """Load verified published CVE entries, rejecting duplicate or invalid IDs.

    Entries are reviewed against their linked public CVE/vendor/CISA/GHSA
    sources before inclusion. This is not a claim that every existing
    CVE record is discoverable automatically via a single API.
    """
    with open(PROFILE_BADGES, encoding="utf-8") as handle:
        config = json.load(handle)
    cisa_config = config.get("cisa_ics")
    if not isinstance(cisa_config, dict):
        raise ValueError("Missing CISA advisory registry")
    validate_cisa_advisories(cisa_config.get("entries"))
    cisa_coordination(config)
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


def cisa_coordination(config=None):
    """Return the reviewed aggregate without exposing private case details."""
    entry = (config or profile_badges()).get("cisa_coordination")
    if not isinstance(entry, dict):
        raise ValueError("Missing CISA coordination aggregate")
    count = entry.get("active_cases")
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValueError("Invalid active CISA case count")
    verified = entry.get("last_verified")
    if not isinstance(verified, str) or not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}", verified):
        raise ValueError("Invalid CISA coordination verification date")
    try:
        date.fromisoformat(verified)
    except ValueError as exc:
        raise ValueError("Invalid CISA coordination verification date") from exc
    if not isinstance(entry.get("source"), str) or not entry["source"].strip():
        raise ValueError("Missing CISA coordination review source")
    return entry


def build_badges_block(config=None):
    config = config or profile_badges()
    cve_count = len(config["published_cves"]["entries"])
    merged = merged_prs(config)
    pr_count = merged["count"]
    cves_url = "https://github.com/" + USER + "/" + USER + "#published-cves"
    cisa = cisa_advisories(config)
    active_cases = cisa_coordination(config)["active_cases"]
    prs_url = merged["url"]
    cve_badge = ("https://img.shields.io/badge/CVEs%20Published-"
                 + str(cve_count)
                 + "-c0392b?style=flat-square&logo=cve"
                 + "&logoColor=white&labelColor=222")
    pr_badge = ("https://img.shields.io/badge/Merged%20PRs-"
                + str(pr_count)
                + "-2da44e?style=flat-square&logo=github"
                + "&logoColor=white&labelColor=222")
    cisa_badge = ("https://img.shields.io/badge/CISA%20ICS%20Published-"
                  + str(len(cisa))
                  + "-005ea2?style=flat-square&labelColor=222")
    coordination_badge = ("https://img.shields.io/badge/CISA%20Active%20Cases-"
                          + str(active_cases)
                          + "-005ea2?style=flat-square&labelColor=222")
    cisa_url = cves_url.rsplit("#", 1)[0] + "#cisa-ics-advisories"
    coordination_url = cves_url.rsplit("#", 1)[0] + "#cisa-coordination"
    return (
        "<p>\n"
        '  <a href="' + cves_url + '">'
        '<img alt="' + str(cve_count) + ' CVE'
        + ('' if cve_count == 1 else 's') + ' published" '
        'src="' + cve_badge + '"></a>\n'
        '  <a href="' + coordination_url + '">'
        '<img alt="' + str(active_cases) + ' active CISA coordination '
        + ('case' if active_cases == 1 else 'cases') + '" '
        'src="' + coordination_badge + '"></a>\n'
        '  <a href="' + cisa_url + '">'
        '<img alt="' + str(len(cisa))
        + ' published CISA ICS ' + ("advisory" if len(cisa) == 1 else "advisories")
        + ' with researcher credit" '
        'src="' + cisa_badge + '"></a>\n'
        '  <a href="' + prs_url + '">'
        '<img alt="' + str(pr_count) + ' merged PR'
        + ('' if pr_count == 1 else 's') + '" '
        'src="' + pr_badge + '"></a>\n'
        "</p>"
    )


def build_cve_list():
    """Build the clickable, descriptive CVE index from the badge registry.

    Automatically discovered entries remain valid before optional editorial
    metadata is reviewed and added to the registry.
    """
    entries = profile_badges()["published_cves"]["entries"]
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


def build_cisa_list(config=None):
    """Show active coordination separately from published researcher credits."""
    config = config or profile_badges()
    coordination = cisa_coordination(config)
    active_cases = coordination["active_cases"]
    advisories = cisa_advisories(config)
    rows = ["## CISA coordination", "",
            f"{active_cases} active vulnerability coordination "
            + ("case" if active_cases == 1 else "cases")
            + " through CISA VINCE-NT. Last verified "
            + coordination["last_verified"] + ".", "",
            "### CISA ICS advisories", "",
            f"Researcher credit in {len(advisories)} published CISA ICS "
            + ("advisory" if len(advisories) == 1 else "advisories") + ".", "",
            "| Product | Advisory | Published |",
            "| --- | --- | --- |"]
    for item in advisories:
        advisory = "[" + item["advisory"] + "](" + item["url"] + ")"
        rows.append("| " + item["product"] + " | " + advisory +
                    " | " + item["published_at"] + " |")
    return "\n".join(rows)


def replace_block(text, name, content):
    start, end = "<!-- %s:START -->" % name, "<!-- %s:END -->" % name
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        sys.exit("marker pair %s not found in README.md" % name)
    return pattern.sub(lambda _m: start + "\n" + content + "\n" + end, text)


def main():
    with open(README, encoding="utf-8") as handle:
        original = handle.read()
    updated = replace_block(original, "BADGES", build_badges_block())
    updated = replace_block(updated, "CISA_LIST", build_cisa_list())
    updated = replace_block(updated, "CVE_LIST", build_cve_list())
    updated = replace_block(updated, "ADVISORY_LIST", build_advisory_list())
    if updated == original:
        print("README.md already up to date.")
        return
    with open(README, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(updated)
    print("README.md updated.")


if __name__ == "__main__":
    main()
