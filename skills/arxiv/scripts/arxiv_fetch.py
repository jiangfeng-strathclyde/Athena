#!/usr/bin/env python3
"""Standalone Athena adaptation of ARIS arxiv_fetch.py; see ../LICENSE.upstream."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ATOM = "{http://www.w3.org/2005/Atom}"
ID = re.compile(r"(?:\d{4}\.\d{4,5}|[A-Za-z][A-Za-z.-]*/\d{7})(?:v[1-9]\d*)?\Z")
API = "https://export.arxiv.org/api/query"
USER_AGENT = "Athena-arxiv/1.0 (+https://github.com/jiangfeng-strathclyde/Athena)"


def normalize_id(value: str) -> str:
    value = value.strip()
    if value.startswith(("https://", "http://")):
        url = urllib.parse.urlsplit(value)
        if url.hostname not in {"arxiv.org", "www.arxiv.org"} or url.query or url.fragment:
            raise ValueError("Expected an arxiv.org abstract or PDF URL")
        if url.path.startswith("/abs/"):
            value = url.path[5:]
        elif url.path.startswith("/pdf/"):
            value = url.path[5:].removesuffix(".pdf")
        else:
            raise ValueError("Expected /abs/ or /pdf/ in arXiv URL")
    value = value.removeprefix("id:")
    if not ID.fullmatch(value):
        raise ValueError("Invalid arXiv ID")
    return value


def api_url(query: str, max_results: int = 10, start: int = 0) -> str:
    if not 1 <= max_results <= 100 or start < 0 or not query.strip():
        raise ValueError("Use a nonempty query, --max 1..100 and --start >= 0")
    query = query.strip()
    if ID.fullmatch(query) or query.startswith(("id:", "https://", "http://")):
        params = {"id_list": normalize_id(query)}
    else:
        params = {"search_query": query, "start": start, "max_results": max_results,
                  "sortBy": "relevance", "sortOrder": "descending"}
    return API + "?" + urllib.parse.urlencode(params)


def fetch(url: str, limit: int) -> bytes:
    # Callers must also avoid concurrent invocations.
    time.sleep(3)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError(f"Response exceeds {limit} bytes; stopped without saving")
    return data


def parse_feed(data: bytes) -> list[dict]:
    root = ET.fromstring(data)
    if root.tag != ATOM + "feed":
        raise ValueError("Expected an arXiv Atom feed")
    papers = []
    for entry in root.findall(ATOM + "entry"):
        raw_id = entry.findtext(ATOM + "id", "")
        if "/api/errors" in raw_id:
            raise ValueError("arXiv API error: " + entry.findtext(ATOM + "summary", "unknown error"))
        paper_id = normalize_id(raw_id)
        clean = lambda name: " ".join(entry.findtext(ATOM + name, "").split())
        papers.append({
            "id": paper_id, "title": clean("title"), "abstract": clean("summary"),
            "authors": [a.findtext(ATOM + "name", "") for a in entry.findall(ATOM + "author")],
            "published": clean("published"), "updated": clean("updated"),
            "categories": [c.get("term", "") for c in entry.findall(ATOM + "category")],
            "abs_url": "https://arxiv.org/abs/" + paper_id,
            "pdf_url": "https://arxiv.org/pdf/" + paper_id,
        })
    return papers


def search(query: str, max_results: int = 10, start: int = 0) -> list[dict]:
    return parse_feed(fetch(api_url(query, max_results, start), 5 * 1024 * 1024))


def validate_pdf(data: bytes) -> None:
    if len(data) < 10240 or b"%PDF-" not in data[:1024]:
        raise ValueError("PDF header/size check failed; no existing file was changed")


def download(paper_id: str, output_dir: str = "papers") -> dict:
    paper_id = normalize_id(paper_id)
    folder = Path(output_dir).resolve()
    destination = folder / (paper_id.replace("/", "_") + ".pdf")
    if destination.is_symlink():
        raise ValueError("Refusing a symbolic-link destination")
    if destination.exists():
        with destination.open("rb") as handle:
            data = handle.read(50 * 1024 * 1024 + 1)
        if len(data) > 50 * 1024 * 1024:
            raise ValueError("Existing file exceeds validation size limit; left unchanged")
        validate_pdf(data)
        skipped = True
    else:
        data = fetch("https://arxiv.org/pdf/" + paper_id, 50 * 1024 * 1024)
        validate_pdf(data)
        folder.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also protects a file created during the request.
        with destination.open("xb") as handle:
            handle.write(data)
        skipped = False
    return {"id": paper_id, "path": str(destination), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "skipped": skipped,
            "validation": "header-and-size-only"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    find = sub.add_parser("search")
    find.add_argument("query")
    find.add_argument("--max", type=int, default=10)
    find.add_argument("--start", type=int, default=0)
    save = sub.add_parser("download")
    save.add_argument("id")
    save.add_argument("--dir", default="papers")
    args = parser.parse_args(argv)
    try:
        result = (search(args.query, args.max, args.start) if args.command == "search"
                  else download(args.id, args.dir))
    except (ValueError, OSError, urllib.error.URLError, ET.ParseError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
