#!/usr/bin/env python3
"""Discover newly credited published CVEs in CVEProject's official rolling delta."""
import concurrent.futures
import datetime as dt
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "data", "profile_badges.json")
DELTA = "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/deltaLog.json"
OFFICIAL = "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/"
IDENTITY = re.compile(r"^Ievgen(?:\s+\(Jack\))?\s+Bondarenko$", re.I)
CVE = re.compile(r"^CVE-(\d{4})-(\d{4,})$")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ibondarenko1-cve-monitor"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def candidate(item):
    cve_id = item.get("cveId", "")
    if not CVE.fullmatch(cve_id):
        return None
    url = item.get("githubLink", "")
    # Never visit an untrusted URL from the feed.
    if not url.startswith(OFFICIAL) or not url.endswith("/" + cve_id + ".json"):
        return None
    return cve_id, url


def credited(record):
    meta = record.get("cveMetadata", {})
    if meta.get("state") != "PUBLISHED":
        return False
    containers = record.get("containers", {})
    # Only structured direct finder credits, not free-text name mentions.
    credits = containers.get("cna", {}).get("credits", [])
    for credit in credits:
        if credit.get("type", "").lower() == "finder" and IDENTITY.fullmatch(credit.get("value", "").strip()):
            return True
    return False


def inspect(pair):
    cve_id, url = pair
    payload = get(url)
    if b"Ievgen" not in payload and b"Bondarenko" not in payload:
        return None
    record = json.loads(payload)
    if record.get("cveMetadata", {}).get("cveId") != cve_id:
        raise ValueError("Record ID mismatch for " + cve_id)
    if credited(record):
        return {"id": cve_id, "source": "https://www.cve.org/CVERecord?id=" + cve_id}
    return None


def main():
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=3)
    delta = json.loads(get(DELTA))
    if not isinstance(delta, list):
        raise ValueError("Unexpected CVE delta format")
    with open(MANIFEST, encoding="utf-8") as stream:
        data = json.load(stream)
    entries = data["published_cves"]["entries"]
    existing = {entry["id"] for entry in entries}
    pending = {}
    seen_recent = False
    for batch in delta:
        stamp = dt.datetime.fromisoformat(batch["fetchTime"].replace("Z", "+00:00"))
        if stamp < cutoff:
            continue
        seen_recent = True
        for item in batch.get("new", []) + batch.get("updated", []):
            pair = candidate(item)
            if pair and pair[0] not in existing:
                pending[pair[0]] = pair
    if not seen_recent:
        raise RuntimeError("CVE delta feed contains no updates in the past 72 hours")
    print("Inspecting", len(pending), "new or updated records")
    discovered = []
    # A failed request must fail the job: never silently skip records.
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for entry in executor.map(inspect, pending.values()):
            if entry is not None:
                discovered.append(entry)
    if discovered:
        entries.extend(sorted(discovered, key=lambda x: x["id"]))
        entries.sort(key=lambda x: x["id"])
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    print("Added", len(discovered), "new CVEs; total", len(entries))


if __name__ == "__main__":
    main()
