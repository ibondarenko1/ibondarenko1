#!/usr/bin/env python3
"""Discover newly credited CVEs from the official CVE List release deltas."""
import datetime as dt
import io
import json
import os
import re
import time
import urllib.error
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "data", "profile_badges.json")
RELEASES = "https://api.github.com/repos/CVEProject/cvelistV5/releases"
IDENTITY = re.compile(r"^Ievgen(?:\s+\(Jack\))?\s+Bondarenko$", re.I)
CVE = re.compile(r"^CVE-(\d{4})-(\d{4,})$")
DELTA_MEMBER = re.compile(r"^deltaCves/(CVE-\d{4}-\d{4,})\.json$")
DELTA_ASSET = re.compile(
    r"^(\d{4}-\d{2}-\d{2})_delta_CVEs_at_(?:\d{4}Z|end_of_day)\.zip$"
)
LOOKBACK_DAYS = 3
TRANSIENT_HTTP = {429, 500, 502, 503, 504}


def get(url, accept="application/vnd.github+json", attempts=5):
    """Fetch a URL, retrying bounded transient server and rate-limit errors."""
    for attempt in range(attempts):
        req = urllib.request.Request(
            url,
            headers={
                "Accept": accept,
                "User-Agent": "ibondarenko1-cve-monitor",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        token = os.environ.get("GITHUB_TOKEN", "")
        if token and url.startswith("https://api.github.com/"):
            req.add_header("Authorization", "Bearer " + token)
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code not in TRANSIENT_HTTP or attempt + 1 == attempts:
                raise
            retry_after = error.headers.get("Retry-After", "")
            delay = float(retry_after) if retry_after.isdigit() else min(2 ** attempt, 30)
            print("HTTP", error.code, "from", url, "- retrying in", delay, "seconds")
            time.sleep(delay)
    raise AssertionError("unreachable")


def credited(record):
    meta = record.get("cveMetadata", {})
    if meta.get("state") != "PUBLISHED":
        return False
    containers = record.get("containers", {})
    # Only structured direct finder credits, not free-text name mentions.
    credits = containers.get("cna", {}).get("credits", [])
    for credit in credits:
        if credit.get("type", "").lower() == "finder" and IDENTITY.fullmatch(
            credit.get("value", "").strip()
        ):
            return True
    return False


def latest_delta_assets(releases, start_date, end_date):
    """Select the newest cumulative delta asset for each UTC calendar day."""
    selected = {}
    for release in releases:
        stamp = dt.datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
        matched = [
            (DELTA_ASSET.fullmatch(asset.get("name", "")), asset)
            for asset in release.get("assets", [])
        ]
        assets = [(match, asset) for match, asset in matched if match]
        if not assets:
            continue
        if len(assets) != 1:
            raise ValueError("Expected one CVE delta asset in release " + release["tag_name"])
        match, asset = assets[0]
        day = dt.date.fromisoformat(match.group(1))
        if day < start_date or day > end_date:
            continue
        current = selected.get(day)
        if current is None or stamp > current[0]:
            selected[day] = (stamp, asset)
    expected = {
        start_date + dt.timedelta(days=offset)
        for offset in range((end_date - start_date).days + 1)
    }
    missing = sorted(expected - set(selected))
    if missing:
        raise RuntimeError(
            "No CVE delta release found for: " + ", ".join(day.isoformat() for day in missing)
        )
    return [selected[day][1] for day in sorted(selected)]


def discover_delta_assets(now):
    start_date = (now - dt.timedelta(days=LOOKBACK_DAYS)).date()
    end_date = now.date()
    releases = []
    page = 1
    while True:
        url = RELEASES + "?per_page=100&page=" + str(page)
        batch = json.loads(get(url))
        if not isinstance(batch, list):
            raise ValueError("Unexpected GitHub releases response")
        releases.extend(batch)
        if len(batch) < 100:
            break
        oldest = min(
            dt.datetime.fromisoformat(item["published_at"].replace("Z", "+00:00")).date()
            for item in batch
        )
        if oldest < start_date:
            break
        page += 1
        if page > 3:
            raise RuntimeError("CVE release pagination exceeded the expected lookback window")
    return latest_delta_assets(releases, start_date, end_date)


def archive_records(payload):
    """Yield validated CVE IDs and raw records from an official delta archive."""
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for item in archive.infolist():
            if item.is_dir():
                continue
            match = DELTA_MEMBER.fullmatch(item.filename)
            if not match:
                raise ValueError("Unexpected CVE delta archive member: " + item.filename)
            yield match.group(1), archive.read(item)


def inspect_record(cve_id, payload):
    record = json.loads(payload)
    if record.get("cveMetadata", {}).get("cveId") != cve_id:
        raise ValueError("Record ID mismatch for " + cve_id)
    if credited(record):
        return {"id": cve_id, "source": "https://www.cve.org/CVERecord?id=" + cve_id}
    return None


def main():
    now = dt.datetime.now(dt.timezone.utc)
    assets = discover_delta_assets(now)
    with open(MANIFEST, encoding="utf-8") as stream:
        data = json.load(stream)
    entries = data["published_cves"]["entries"]
    existing = {entry["id"] for entry in entries}

    # Each selected archive is cumulative from that day's baseline. Process the
    # days in order and retain only the newest form of a matching record.
    seen = set()
    possible = {}
    for asset in assets:
        name = asset["name"]
        print("Downloading", name)
        payload = get(asset["browser_download_url"], accept="application/octet-stream")
        for cve_id, record in archive_records(payload):
            if not CVE.fullmatch(cve_id):
                raise ValueError("Invalid CVE ID in delta archive: " + cve_id)
            if cve_id in existing:
                continue
            seen.add(cve_id)
            if b"Ievgen" in record or b"Bondarenko" in record:
                possible[cve_id] = record
            else:
                possible.pop(cve_id, None)

    print("Inspected", len(seen), "new or updated records from", len(assets), "archives")
    discovered = []
    for cve_id, payload in possible.items():
        entry = inspect_record(cve_id, payload)
        if entry is not None:
            discovered.append(entry)
    if discovered:
        entries.extend(sorted(discovered, key=lambda item: item["id"]))
        entries.sort(key=lambda item: item["id"])
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    print("Added", len(discovered), "new CVEs; total", len(entries))


if __name__ == "__main__":
    main()
