#!/usr/bin/env python3
"""Regenerate the dynamic badges block of the GitHub profile README.

One section is kept in sync automatically:

  * BADGES - two clickable shields.io counter badges near the top of
    the README:
      - CVEs Published -> GitHub Advisory Database, credit:USER filter.
                          Counts entries in data/advisories.json. Only
                          GHSAs where USER is credited as reporter
                          belong in that file - the badge link goes
                          straight to the canonical GitHub credit list,
                          so anything on the badge needs to also appear
                          there. Update the file when one of your
                          submitted advisories publishes with credit.
      - Merged PRs     -> GitHub pull-request search (`is:pr is:merged
                          author:USER -user:USER`). Count comes from
                          the search API's total_count, so new merged
                          PRs auto-bump the badge.

The block lives between HTML marker comments in README.md:

  <!-- BADGES:START --> ... <!-- BADGES:END -->

Run locally with a token in GITHUB_TOKEN; the workflow passes one in CI.
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
ADVISORIES = os.path.join(ROOT, "data", "advisories.json")


def api(path):
    url = path if path.startswith("http") else API + path
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", USER + "-readme-bot")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    token = os.environ.get("GITHUB_TOKEN", "")
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
    return int(api(url).get("total_count", 0))


def cves_credited_count():
    """Count CVEs published with USER credited as reporter.

    Source of truth is data/advisories.json - a curated GHSA-id list.
    The companion badge link uses GitHub's `credit:USER` filter on the
    Advisory Database; only entries that show up there belong in this
    file. (GitHub's `credits[]` listing has been observed to drop
    `user.login` for some published advisories, so the search filter
    can under-count even when the operator is genuinely the reporter -
    keeping the curated list keeps the badge honest if that recurs.)
    """
    with open(ADVISORIES, encoding="utf-8") as handle:
        return len(json.load(handle))


def build_badges_block():
    cve_count = cves_credited_count()
    pr_count = merged_prs_count()
    cves_url = "https://github.com/advisories?query=credit%3A" + USER
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
    return (
        "<p>\n"
        '  <a href="' + cves_url + '">'
        '<img alt="' + str(cve_count) + ' CVE'
        + ('' if cve_count == 1 else 's') + ' published" '
        'src="' + cve_badge + '"></a>\n'
        '  <a href="' + prs_url + '">'
        '<img alt="' + str(pr_count) + ' merged PR'
        + ('' if pr_count == 1 else 's') + '" '
        'src="' + pr_badge + '"></a>\n'
        "</p>"
    )


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
    if updated == original:
        print("README.md already up to date.")
        return
    with open(README, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(updated)
    print("README.md updated.")


if __name__ == "__main__":
    main()
