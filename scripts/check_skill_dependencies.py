#!/usr/bin/env python3
"""Report static packaging gaps; this is not a runtime or security certification."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^\n)]+)\)")


def inspect_skill(folder: Path) -> dict:
    document = folder / "SKILL.md"
    text = document.read_text(encoding="utf-8")
    missing = set()
    outside = set()
    for match in LINK.finditer(text):
        raw = match.group(1).strip()
        if not raw:
            continue
        target = raw[1:raw.index(">")] if raw.startswith("<") and ">" in raw else raw.split()[0]
        if urlsplit(target).scheme or target.startswith(("#", "//")):
            continue
        relative = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not relative:
            continue
        resource = (folder / relative).resolve()
        if not resource.exists():
            missing.add(relative)
        if resource != folder.resolve() and folder.resolve() not in resource.parents:
            outside.add(relative)
    return {
        "skill": folder.name,
        "missing_local_references": sorted(missing),
        "references_outside_skill": sorted(outside),
        "declares_unbundled_support": bool(re.search(
            r"support(?:ing)? (?:files|documentation|documents)[^\n]*(?:not distributed|not included)",
            text, re.IGNORECASE)),
        "mentions_shared_references": "shared-references/" in text,
        "mentions_host_tools": bool(re.search(r"mcp__|Bash\(", text)),
    }


def needs_attention(report: dict) -> bool:
    return bool(report["missing_local_references"] or report["references_outside_skill"]
                or report["declares_unbundled_support"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", help="Inspect only this skill; repeat as needed.")
    parser.add_argument("--json", action="store_true", help="Print full machine-readable findings.")
    parser.add_argument("--strict", action="store_true", help="Fail on detected packaging gaps.")
    args = parser.parse_args(argv)
    catalog = {p.name: p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()}
    names = sorted(set(args.skill) if args.skill else catalog)
    if set(names) - set(catalog):
        parser.error("Unknown skill(s): " + ", ".join(sorted(set(names) - set(catalog))))
    reports = [inspect_skill(catalog[name]) for name in names]
    attention = [r for r in reports if needs_attention(r)]
    summary = {
        "skills_scanned": len(reports),
        "skills_with_packaging_findings": len(attention),
        "skills_declaring_unbundled_support": sum(r["declares_unbundled_support"] for r in reports),
        "skills_mentioning_shared_references": sum(r["mentions_shared_references"] for r in reports),
        "skills_mentioning_host_tools": sum(r["mentions_host_tools"] for r in reports),
    }
    if args.json:
        print(json.dumps({"summary": summary, "skills": reports}, ensure_ascii=True, indent=2))
    else:
        for key, value in summary.items():
            print(f"{key}: {value}")
        for report in attention[:10]:
            print(f"CHECK {report['skill']}: {len(report['missing_local_references'])} missing links; "
                  f"unbundled support={report['declares_unbundled_support']}")
        print("Use --json for all findings. This scan checks inline Markdown links and known "
              "mirror notices, not code references, credentials, tool availability, or agent behavior. "
              "Outside-folder links need packaging review even if they resolve in this checkout.")
    return int(args.strict and bool(attention))


if __name__ == "__main__":
    raise SystemExit(main())
