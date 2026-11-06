#!/usr/bin/env python3
"""外链周报：抽取 README 与 docs/*.md 的 http(s) 链接做存活探测。

用法：python scripts/check_external_links.py
仅在周 cron 中运行（push 时跑会拖慢且易抖动）。硬 404/5xx 且重试仍失败 → 退出 1。
SKIP 列表里的模式不做判定（如未启用的 Discussions 页、 shields 徽章端点）。
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
        print(f"\n{len(bad)} 个外链失效：")
        for u in bad:
            print("  -", u)
        return 1
    print("\n外链全部存活。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
