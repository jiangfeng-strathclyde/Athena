#!/usr/bin/env python3
"""Check external HTTP(S) links in the README, docs, and clone kit.

Run with: ``python scripts/check_external_links.py``
The weekly workflow runs this separately from push checks because network
requests can be slow or flaky. A confirmed 404/5xx response exits with status
1. Known dynamic endpoints and badge services are skipped.
"""
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [ROOT / "README.md"] + sorted((ROOT / "docs").glob("*.md")) + sorted((ROOT / "clone-kit").glob("*.md"))
SKIP = (
    "img.shields.io",
    "/discussions",
    "users.noreply.github.com",
)
TIMEOUT = 12


def collect():
    links = {}
    for f in TARGETS:
        for m in re.finditer(r"\[[^\]]*\]\((https?://[^)\s]+)\)", f.read_text(encoding="utf-8")):
            links.setdefault(m.group(1), f.name)
    return links


def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link-check)"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.status


def main():
    links = collect()
    bad = []
    for url, src in sorted(links.items()):
        if any(s in url for s in SKIP):
            print(f"SKIP  {url}  ({src})")
            continue
        status = None
        for attempt in (1, 2):
            try:
                status = probe(url)
                break
            except urllib.error.HTTPError as e:
                status = e.code
                if e.code < 500 and e.code != 429:
                    break
            except Exception:
                status = None
            time.sleep(2)
        if status and 200 <= status < 400:
            print(f"OK    {status}  {url}")
        else:
            print(f"FAIL  {status}  {url}  ({src})")
            bad.append(url)
    if bad:
        print(f"\n{len(bad)} external link(s) failed:")
        for u in bad:
            print("  -", u)
        return 1
    print("\nAll checked external links are reachable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
