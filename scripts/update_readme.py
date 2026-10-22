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
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

USER = "ibondarenko1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
PROFILE_BADGES = os.path.join(ROOT, "data", "profile_badges.json")


class EmbeddedSearchDataParser(HTMLParser):
    """Extract GitHub's public search result payload from its HTML page."""

    def __init__(self):
        super().__init__()
        self._capture = False
        self._chunks = []
        self.payload = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if (
            tag == "script"
            and attributes.get("type") == "application/json"
            and attributes.get("data-target") == "react-app.embeddedData"
        ):
            self._capture = True
            self._chunks = []

    def handle_data(self, data):
        if self._capture:
            self._chunks.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._capture:
            self.payload = "".join(self._chunks)
            self._capture = False


def public_search_page(url, attempts=3):
    """Fetch a GitHub public search page without repository or user tokens."""
    req = urllib.request.Request(url)
    req.add_header("Accept", "text/html")
    req.add_header("User-Agent", USER + "-readme-bot")
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            if error.code != 429 and not 500 <= error.code < 600:
                raise
            if attempt + 1 == attempts:
                raise
            time.sleep(2 ** attempt)


def merged_prs_search_url():
    query = "type:pr author:%s is:merged -user:%s" % (USER, USER)
    return "https://github.com/search?" + urllib.parse.urlencode(
        {"q": query, "type": "pullrequests"}
    )


def merged_prs_count():
    """Count merged PRs authored by USER in repositories USER does not own.

    Parse the count that GitHub shows to anonymous profile visitors. The REST
    Search API is unsuitable here: a repository-scoped Actions token sees only
    its own repository, while an anonymous API request from an Actions runner
    can return an empty result set. The public HTML search page carries the
    displayed count in a structured JSON payload.
    """
    parser = EmbeddedSearchDataParser()
    parser.feed(public_search_page(merged_prs_search_url()))
    if not parser.payload:
        raise ValueError("GitHub public search payload was not found")

    route = json.loads(parser.payload)["payload"]["blackbirdSearchRoute"]
    if route.get("errors") or route.get("warn_limited_results"):
        raise ValueError("GitHub public search returned incomplete results")
    count = route.get("result_count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValueError("GitHub public search returned an invalid result count")
    return count


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
    prs_url = merged_prs_search_url()
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
