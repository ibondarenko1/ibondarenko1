#!/usr/bin/env python3
"""Regenerate the GitHub profile README's badges and published CVE index.

BADGES shows published CVE count, CISA advisory, and merged upstream PRs.
CVE_LIST uses the same curated public-source registry. Entries discovered
automatically may initially lack optional product/issue descriptions.
Both sections are delimited by markers in README.md and updated together.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

USER = "ibondarenko1"
API = "https://api.github.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
PROFILE_BADGES = os.path.join(ROOT, "data", "profile_badges.json")


def api(path, use_token=True):
    url = path if path.startswith("http") else API + path
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", USER + "-readme-bot")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    token = os.environ.get("GITHUB_TOKEN", "") if use_token else ""
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def merged_prs_count():
    """Count merged PRs authored by USER in repositories USER does not own.

    Uses the search API's `total_count` field so we do not have to
    paginate just to count.
    """
    query = "type:pr author:%s is:merged -user:%s" % (USER, USER)
    url = "%s/search/issues?q=%s&per_page=1" % (
        API, urllib.parse.quote(query))
    # The profile badge links to the public search result. A repository-scoped
    # Actions token sees only its installation's repository, while a personal
    # token can include private pull requests. Use the anonymous public view so
    # the generated count matches what profile visitors can verify.
    return int(api(url, use_token=False).get("total_count", 0))


def profile_badges():
    """Load verified published CVE entries, rejecting duplicate or invalid IDs.

    Entries are reviewed against their linked public CVE/vendor/CISA/GHSA
    sources before inclusion. This is not a claim that every existing
    CVE record is discoverable automatically via a single API.
    """
    with open(PROFILE_BADGES, encoding="utf-8") as handle:
        config = json.load(handle)
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
    return config


def build_badges_block():
    config = profile_badges()
    cve_count = len(config["published_cves"]["entries"])
    pr_count = merged_prs_count()
    cves_url = "https://github.com/" + USER + "/" + USER + "#published-cves"
    cisa = config["cisa_ics"]
    prs_url = ("https://github.com/pulls?q=is%3Apr+author%3A" + USER
               + "+is%3Amerged+-user%3A" + USER)
    cve_badge = ("https://img.shields.io/badge/CVEs%20Published-"
                 + str(cve_count)
                 + "-c0392b?style=flat-square&logo=cve"
                 + "&logoColor=white&labelColor=222")
    pr_badge = ("https://img.shields.io/badge/Merged%20PRs-"
                + str(pr_count)
                + "-2da44e?style=flat-square&logo=github"
                + "&logoColor=white&labelColor=222")
    cisa_badge = ("https://img.shields.io/badge/CISA%20ICS-"
                  + cisa["advisory"].replace("-", "--")
                  + "-005ea2?style=flat-square&labelColor=222")
    return (
        "<p>\n"
        '  <a href="' + cves_url + '">'
        '<img alt="' + str(cve_count) + ' CVE'
        + ('' if cve_count == 1 else 's') + ' published" '
        'src="' + cve_badge + '"></a>\n'
        '  <a href="' + cisa["url"] + '">'
        '<img alt="CISA ICS Advisory ' + cisa["advisory"] + '" '
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
            "Verified public advisory links for each published CVE.", ""]
    for item in sorted(entries, key=lambda row: row["id"]):
        line = "- [" + item["id"] + "](" + item["source"] + ")"
        if item.get("product") and item.get("summary"):
            line += " · **" + item["product"] + "**: " + item["summary"]
        rows.append(line)
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
    updated = replace_block(updated, "CVE_LIST", build_cve_list())
    if updated == original:
        print("README.md already up to date.")
        return
    with open(README, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(updated)
    print("README.md updated.")


if __name__ == "__main__":
    main()
