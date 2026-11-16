#!/usr/bin/env python3
"""Import public researcher credits absent from CVE List finder fields.

GitHub advisories are fetched anonymously and must have an accepted finder or
reporter credit. OPC Foundation CSAF documents must be final and TLP:WHITE/CLEAR.
GCVE/GHSA records remain separate from the CVE count until a CVE is PUBLISHED.
"""
import json
import re
import urllib.error
from pathlib import PurePosixPath

from discover_cves import CVE, IDENTITY, MANIFEST, get

USER = "ibondarenko1"
GHSA = re.compile(r"^GHSA-[23456789cfghjmpqrvwx]{4}(?:-[23456789cfghjmpqrvwx]{4}){2}$")
GCVE = re.compile(r"^GCVE-\d+-\d{4}-\d+$")
OPC_REPO = "OPCFoundation/OPC-SecurityAdvisories"
OPC_PATH = re.compile(r"^csaf/\d{4}/\d{3}/gcve-\d+-\d{4}-\d+\.json$")


def public_json(url):
    # An Actions token scoped to this profile cannot read another repository's
    # advisories. Anonymous reads also prevent private advisory disclosure.
    return json.loads(get(url, authenticated=False))


def github_advisories(repository):
    prefix = "https://api.github.com/repos/" + repository + "/security-advisories"
    url = prefix + "?state=published&sort=updated&direction=desc&per_page=100"
    visited = set()
    while url:
        if url in visited or not url.startswith(prefix + "?"):
            raise ValueError("Unexpected GitHub advisory pagination URL")
        visited.add(url)
        payload, headers = get(url, authenticated=False, with_headers=True)
        records = json.loads(payload)
        if not isinstance(records, list):
            raise ValueError("Unexpected GitHub advisory response")
        yield from records
        match = re.search(r'<([^>]+)>;\s*rel="next"', headers.get("Link", ""))
        url = match.group(1) if match else None


def github_entry(advisory, repository):
    if (advisory.get("state") != "published"
            or not advisory.get("published_at") or advisory.get("withdrawn_at")):
        return None
    role = next((credit.get("type") for credit in advisory.get("credits_detailed", [])
                 if credit.get("user", {}).get("login", "").lower() == USER
                 and credit.get("state") == "accepted"
                 and credit.get("type") in {"finder", "reporter"}), None)
    if role is None:
        return None
    ghsa = advisory.get("ghsa_id", "")
    if not GHSA.fullmatch(ghsa):
        raise ValueError("Invalid GitHub advisory ID")
    source = "https://github.com/" + repository + "/security/advisories/" + ghsa
    if advisory.get("html_url") != source:
        raise ValueError("GitHub advisory source mismatch")
    packages = sorted({item["package"]["name"]
                       for item in advisory.get("vulnerabilities", [])
                       if item.get("package", {}).get("name")})
    entry = {"id": ghsa, "source": source,
             "product": ", ".join(packages) or repository,
             "summary": advisory["summary"].strip(),
             "published_at": advisory["published_at"][:10], "credit": role}
    if advisory.get("cve_id"):
        if not CVE.fullmatch(advisory["cve_id"]):
            raise ValueError("Invalid advisory CVE ID")
        entry["cve"] = advisory["cve_id"]
    return entry


def opc_entries(document, path):
    doc = document.get("document", {})
    tracking = doc.get("tracking", {})
    tlp = doc.get("distribution", {}).get("tlp", {}).get("label", "").upper()
    if tracking.get("status") != "final" or tlp not in {"WHITE", "CLEAR"}:
        return []
    results = []
    for vulnerability in document.get("vulnerabilities", []):
        names = [name for credit in vulnerability.get("acknowledgments", [])
                 for name in credit.get("names", [])]
        if not any(IDENTITY.fullmatch(name.strip()) for name in names):
            continue
        gcve = next((item["text"] for item in vulnerability.get("ids", [])
                     if item.get("system_name") == "GCVE"), "")
        if not GCVE.fullmatch(gcve) or PurePosixPath(path).stem.upper() != gcve:
            raise ValueError("OPC advisory ID/path mismatch")
        entry = {"id": gcve,
                 "source": "https://github.com/" + OPC_REPO + "/blob/latest/"
                           + str(PurePosixPath(path).parent) + "/README.md",
                 "product": document["product_tree"]["branches"][0]["name"],
                 "summary": vulnerability["title"].strip(),
                 "published_at": tracking["initial_release_date"][:10]}
        cve = vulnerability.get("cve") or next(
            (item["text"] for item in vulnerability.get("ids", [])
             if item.get("system_name") == "CVE"), None)
        if cve:
            if not CVE.fullmatch(cve):
                raise ValueError("Invalid OPC advisory CVE ID")
            entry["cve"] = cve
        results.append(entry)
    return results


def discover_opc():
    tree = public_json("https://api.github.com/repos/" + OPC_REPO
                       + "/git/trees/latest?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("Incomplete OPC advisory tree")
    for item in tree["tree"]:
        path = item["path"]
        if item["type"] == "blob" and OPC_PATH.fullmatch(path):
            document = public_json("https://raw.githubusercontent.com/" + OPC_REPO
                                   + "/latest/" + path)
            yield from opc_entries(document, path)


def published_cve(cve):
    year, number = CVE.fullmatch(cve).groups()
    bucket = number[:-3] + "xxx"
    url = ("https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/"
           + year + "/" + bucket + "/" + cve + ".json")
    try:
        record = public_json(url)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return False
        raise
    meta = record.get("cveMetadata", {})
    if meta.get("cveId") != cve:
        raise ValueError("CVE source ID mismatch")
    return meta.get("state") == "PUBLISHED"


def merge_entries(config, discovered, is_published=published_cve):
    cves = config["published_cves"]["entries"]
    advisories = config.setdefault("published_advisories", {"entries": []})["entries"]
    cve_ids = {item["id"] for item in cves}
    advisory_ids = {item["id"] for item in advisories}
    for entry in discovered:
        cve = entry.get("cve")
        if cve and (cve in cve_ids or is_published(cve)):
            if cve not in cve_ids:
                cves.append({**{key: value for key, value in entry.items()
                                if key not in {"id", "cve", "published_at"}}, "id": cve})
                cve_ids.add(cve)
            # Retain a vendor GCVE as a separate identifier, while the numeric
            # CVE count comes only from the unique published_cves registry.
            if entry["id"].startswith("GHSA-"):
                advisories[:] = [item for item in advisories if item["id"] != entry["id"]]
                advisory_ids.discard(entry["id"])
                continue
        if entry["id"] not in advisory_ids:
            advisories.append(entry.copy())
            advisory_ids.add(entry["id"])
        elif cve:
            next(item for item in advisories if item["id"] == entry["id"])["cve"] = cve
    cves.sort(key=lambda item: item["id"])
    advisories.sort(key=lambda item: item["id"])


def main():
    with open(MANIFEST, encoding="utf-8") as stream:
        config = json.load(stream)
    before = json.dumps(config, sort_keys=True)
    discovered = []
    sources = config["advisory_sources"]
    for repository in sources["github_repositories"]:
        for advisory in github_advisories(repository):
            entry = github_entry(advisory, repository)
            if entry:
                discovered.append(entry)
    if sources.get("opc_foundation_csaf"):
        discovered.extend(discover_opc())
    merge_entries(config, discovered)
    if json.dumps(config, sort_keys=True) != before:
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(config, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    print("Verified", len(discovered), "public advisory credits; total",
          len(config["published_cves"]["entries"]), "CVEs and",
          len(config["published_advisories"]["entries"]), "other advisory records")


if __name__ == "__main__":
    main()
