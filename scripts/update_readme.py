#!/usr/bin/env python3
"""Regenerate the dynamic sections of the GitHub profile README.

Two sections are kept in sync automatically:

  * Upstream Contributions - every merged pull request authored by USER in
    repositories USER does not own, discovered via the GitHub search API.
  * Published CVEs & Advisories - the advisories listed in data/advisories.json
    by GHSA id. The advisory listing API does not expose credited users, so the
    id list is maintained by hand; the CVE id and severity of each are fetched.

Each section lives between HTML marker comments in README.md:

  <!-- PRS:START -->  ...  <!-- PRS:END -->
  <!-- CVES:START --> ...  <!-- CVES:END -->

To add a CVE, append one object to data/advisories.json. To add a merged PR,
do nothing - the next run picks it up. Run locally with a token in
GITHUB_TOKEN; the workflow passes one in CI.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

USER = "ibondarenko1"
API = "https://api.github.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
ADVISORIES = os.path.join(ROOT, "data", "advisories.json")

# Curated one-line repository descriptions. A repository not listed here
# falls back to the description published by the repository itself.
REPO_NOTES = {
    "google/gvisor": "container runtime / application kernel",
    "google/bumble": "Bluetooth protocol stack",
    "swiftlang/swift-package-manager": "Apple, Swift toolchain",
    "tink-crypto/tink-py": "Google cryptography library",
    "google/osv-scanner": "vulnerability scanner",
}

# GitHub stores a truncated title for a few early PRs. Override with the
# intended full title here, keyed by "owner/repo#number".
PR_TITLE_OVERRIDES = {
    "google/bumble#912":
        "fix: add input validation to prevent remote crash "
        "from empty/malformed input",
}


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


def merged_prs():
    """Every merged PR authored by USER in a repository USER does not own."""
    query = "type:pr author:%s is:merged -user:%s" % (USER, USER)
    items, page = [], 1
    while True:
        url = "%s/search/issues?q=%s&per_page=100&page=%d" % (
            API, urllib.parse.quote(query), page)
        data = api(url)
        batch = data.get("items", [])
        items.extend(batch)
        if not batch or len(items) >= data.get("total_count", 0):
            break
        page += 1
    return items


def repo_description(full_name):
    if full_name in REPO_NOTES:
        return REPO_NOTES[full_name]
    try:
        return (api("/repos/" + full_name).get("description") or "").strip()
    except urllib.error.HTTPError:
        return ""


def build_prs_block():
    repos = {}
    for item in merged_prs():
        full = item["repository_url"].split("/repos/", 1)[1]
        repos.setdefault(full, []).append(
            (item["number"], item["title"].strip(), item["html_url"]))
    for prs in repos.values():
        prs.sort(key=lambda pr: pr[0], reverse=True)
    order = sorted(repos, key=lambda name: (-len(repos[name]), name))
    total = sum(len(prs) for prs in repos.values())

    lines = ["**%d** merged pull requests across **%d** open-source projects."
             % (total, len(repos)), ""]
    for full in order:
        description = repo_description(full)
        header = "**[%s](https://github.com/%s)**" % (full, full)
        if description:
            header += " - " + description
        lines.append(header)
        for number, title, url in repos[full]:
            title = PR_TITLE_OVERRIDES.get("%s#%d" % (full, number), title)
            lines.append("- [#%d](%s) - %s" % (number, url, title))
        lines.append("")
    return "\n".join(lines).rstrip()


def build_cves_block():
    with open(ADVISORIES, encoding="utf-8") as handle:
        entries = json.load(handle)
    lines = ["| CVE | Severity | Vulnerability |",
             "|-----|----------|---------------|"]
    for entry in entries:
        ghsa = entry["ghsa"]
        advisory = api("/advisories/" + ghsa)
        cve = advisory.get("cve_id") or ghsa
        severity = (advisory.get("severity") or "").capitalize()
        url = advisory.get("html_url") or "https://github.com/advisories/" + ghsa
        note = entry.get("note") or (advisory.get("summary") or "").strip()
        lines.append("| [%s](%s) | %s | %s |" % (cve, url, severity, note))
    return "\n".join(lines)


def replace_block(text, name, content):
    start, end = "<!-- %s:START -->" % name, "<!-- %s:END -->" % name
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        sys.exit("marker pair %s not found in README.md" % name)
    return pattern.sub(lambda _m: start + "\n" + content + "\n" + end, text)


def main():
    with open(README, encoding="utf-8") as handle:
        original = handle.read()
    updated = replace_block(original, "PRS", build_prs_block())
    updated = replace_block(updated, "CVES", build_cves_block())
    if updated == original:
        print("README.md already up to date.")
        return
    with open(README, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(updated)
    print("README.md updated.")


if __name__ == "__main__":
    main()
