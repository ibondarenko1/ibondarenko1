#!/usr/bin/env python3
"""Refresh the profile's evidence sentence and the separate research record.

README.md keeps an editorial profile and one generated CVE count. RESEARCH.md
holds the public CVE/advisory indexes and a dated coordination aggregate.
Only marked sections are regenerated; the surrounding text is preserved.
"""
from datetime import date
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


def build_profile_evidence(config=None):
    """Keep one source-linked publication count in the editorial profile."""
    config = config or profile_badges()
    cve_count = len(config["published_cves"]["entries"])
    return (
        "Public records credit my work in " + str(cve_count) + " published CVE"
        + ("" if cve_count == 1 else "s")
        + ". [Research record and sources](RESEARCH.md)."
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
        sys.exit("marker pair %s not found" % name)
    return pattern.sub(lambda _m: start + "\n" + content + "\n" + end, text)


def main():
    config = profile_badges()
    with open(README, encoding="utf-8") as handle:
        original_readme = handle.read()
    with open(RESEARCH, encoding="utf-8") as handle:
        original_research = handle.read()
    updated_readme = replace_block(
        original_readme, "PROFILE_EVIDENCE", build_profile_evidence(config))
    updated_research = replace_block(
        original_research, "CISA_LIST", build_cisa_list(config))
    updated_research = replace_block(
        updated_research, "CVE_LIST", build_cve_list(config))
    updated_research = replace_block(
        updated_research, "ADVISORY_LIST", build_advisory_list(config))
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
