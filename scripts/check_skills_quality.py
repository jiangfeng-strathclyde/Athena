#!/usr/bin/env python3
"""Run structural checks and a non-blocking quality score for every skill.

Hard checks fail CI:
  H1 ``SKILL.md`` exists and is not empty.
  H2 YAML-like frontmatter is present and closed.
  H3 ``name`` is present and matches the directory name.
  H4 ``description`` is present and no longer than 1,024 characters.
  H5 The body contains at least 200 characters.

The quality score is informational and follows the rubric in
``docs/LESSONS_FROM_OTHERS.md``:
  Q1 ``license`` field                         +2
  Q2 ``version`` field                         +1
  Q3 ``tags`` or ``dependencies`` field        +1
  Q4 At least three Markdown headings          +2
  Q5 Body contains at least 1,000 characters   +2
  Maximum: 8 points.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return None, text
    fm_raw, body = m.group(1), text[m.end():]
    fm = {}
    key = None
    for line in fm_raw.splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            key = km.group(1).lower()
            fm[key] = km.group(2).strip()
        elif key and (line.startswith((" ", "\t")) or not line.strip()):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm, body


def score(fm, body):
    s = 0
    if fm.get("license"):
        s += 2
    if fm.get("version"):
        s += 1
    if fm.get("tags") or fm.get("dependencies"):
        s += 1
    if len(re.findall(r"^#{1,6}\s", body, re.M)) >= 3:
        s += 2
    if len(body) >= 1000:
        s += 2
    return s


def main():
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    failures, scores = [], []
    for d in dirs:
        f = d / "SKILL.md"
        if not f.is_file() or f.stat().st_size == 0:
            failures.append(f"{d.name}: H1 SKILL.md is missing or empty")
            continue
        text = f.read_text(encoding="utf-8").lstrip("\ufeff")
        fm, body = parse_frontmatter(text)
        if fm is None:
            failures.append(f"{d.name}: H2 frontmatter is missing or unclosed")
            continue
        name = fm.get("name", "").strip("'\"")
        if not name:
            failures.append(f"{d.name}: H3 name is missing")
        elif name != d.name:
            failures.append(f"{d.name}: H3 name does not match the directory (name={name})")
        desc = fm.get("description", "")
        if not desc:
            failures.append(f"{d.name}: H4 description is missing")
        elif len(desc) > 1024:
            failures.append(f"{d.name}: H4 description is too long ({len(desc)} > 1024)")
        if len(body.strip()) < 200:
            failures.append(f"{d.name}: H5 body is too short ({len(body.strip())} < 200)")
        scores.append((score(fm, body), d.name))

    print(f"scanned: {len(dirs)} skill dirs, {len(scores)} parsed")
    if scores:
        avg = sum(s for s, _ in scores) / len(scores)
        lowest = sorted(scores)[:5]
        print(f"quality score: avg {avg:.2f}/8  lowest: " +
              ", ".join(f"{n}={s}" for s, n in lowest))
    if failures:
        print(f"\nFAIL {len(failures)} hard check(s):")
        for x in failures:
            print("  -", x)
        return 1
    print("PASS  all hard checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
