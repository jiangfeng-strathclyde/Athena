#!/usr/bin/env python3
"""Static preflight for a self-contained explorable-paper HTML artifact."""

from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ASSET_ATTRIBUTES = {
    "audio": ("src",),
    "embed": ("src",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "link": ("href",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "track": ("src",),
    "video": ("src", "poster"),
}
CONTROL_TAGS = {"button", "details", "dialog", "input", "select", "textarea"}


def is_remote(value: str) -> bool:
    cleaned = value.strip()
    parsed = urlparse(cleaned)
    return parsed.scheme.lower() in {"http", "https", "ws", "wss"} or cleaned.startswith("//")


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_depth = 0
        self.title_text: list[str] = []
        self.scripts = 0
        self.controls = 0
        self.remote_assets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        data = {key.lower(): value or "" for key, value in attrs}
        if tag == "title":
            self.title_depth += 1
        if tag == "script" and not data.get("src"):
            self.scripts += 1
        if tag in CONTROL_TAGS or data.get("role") in {"button", "slider", "tab"}:
            self.controls += 1
        for attr in ASSET_ATTRIBUTES.get(tag, ()):
            value = data.get(attr, "")
            if not value:
                continue
            candidates = value.split(",") if attr == "srcset" else [value]
            for candidate in candidates:
                url = candidate.strip().split()[0]
                if is_remote(url):
                    self.remote_assets.append(f"<{tag} {attr}={url!r}>")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)


def audit(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["file is not valid UTF-8"]

    parser = AuditParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:  # HTMLParser errors are rare but should be visible.
        return [f"HTML parser failed: {exc}"]

    if not "".join(parser.title_text).strip():
        problems.append("missing a non-empty <title>")
    if parser.scripts == 0:
        problems.append("no inline script found; the artifact has no inspectable interaction logic")
    if parser.controls == 0:
        problems.append("no native control or interactive ARIA role found")
    if parser.remote_assets:
        problems.append("remote runtime assets break offline packaging: " + ", ".join(parser.remote_assets[:8]))
    if "TODO" in text or "PLACEHOLDER" in text:
        problems.append("unresolved TODO or PLACEHOLDER marker found")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", type=Path, help="HTML artifact to inspect")
    args = ap.parse_args()
    if not args.html.is_file():
        print(f"FAIL: file not found: {args.html}", file=sys.stderr)
        return 2
    problems = audit(args.html)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        print(f"\nStatic preflight failed with {len(problems)} issue(s).")
        return 1
    print("PASS: static offline-artifact preflight")
    print("NOTE: source, numerical, browser, accessibility, and reproduction checks remain separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
