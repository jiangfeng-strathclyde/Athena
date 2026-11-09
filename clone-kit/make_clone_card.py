#!/usr/bin/env python3
"""Generate a clone card (SVG + markdown badge line) for this repo or your own clone.

Usage:
  python make_clone_card.py [--name NAME] [--direction TEXT] [--out PREFIX]

Reads clone-kit/MANIFEST.json for skill counts and git metadata for the snapshot
date. Outputs <PREFIX>.svg and <PREFIX>.md next to this script. No network calls.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=HERE, capture_output=True,
                              text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="Athena Cyber Clone")
    ap.add_argument("--direction", default="remote sensing & ML / earth observation")
    ap.add_argument("--out", default=str(HERE / "clone-card"))
    ap.add_argument("--protocol", default="v1")
    ap.add_argument("--integrity", default="triple-audit ON")
    a = ap.parse_args()

    manifest = json.loads((HERE / "MANIFEST.json").read_text(encoding="utf-8"))
    listed_only = sum(1 for x in manifest if x.get("mirrored") is False)
    no_local_text = sum(1 for x in manifest
                        if x.get("source") in ("template-preset", "built-in"))
    skills_dir = HERE.parent / "skills"
    n_skills = sum(1 for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() \
        else len(manifest)
    snap = git("log", "-1", "--format=%ad", "--date=short") or date.today().isoformat()
    commit = (git("rev-parse", "--short", "HEAD") or "unknown")[:7]

    md = (
        f"![license](https://img.shields.io/badge/License-MIT-yellow) "
        f"![skills](https://img.shields.io/badge/skills-{n_skills}-blue) "
        f"![protocol](https://img.shields.io/badge/clone%20protocol-{a.protocol}-green) "
        f"![integrity](https://img.shields.io/badge/integrity-{a.integrity.replace(' ', '%20')}-orange) "
        f"![snapshot](https://img.shields.io/badge/snapshot-{snap}-lightgrey)\n"
    )

    w, h = 640, 300
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Georgia, 'Songti SC', serif">
  <rect width="{w}" height="{h}" fill="#fbfaf7" stroke="#d9d2c7"/>
  <rect x="0" y="0" width="{w}" height="64" fill="#31687e"/>
  <text x="24" y="40" fill="#ffffff" font-size="24">{a.name}</text>
  <text x="24" y="92" fill="#1c1c1c" font-size="15">direction: {a.direction}</text>
  <text x="24" y="120" fill="#1c1c1c" font-size="15">skills mirrored: {n_skills} · listed-only: {listed_only} · platform presets w/o local text: {no_local_text}</text>
  <text x="24" y="148" fill="#1c1c1c" font-size="15">clone protocol: {a.protocol} · integrity: {a.integrity}</text>
  <text x="24" y="176" fill="#1c1c1c" font-size="15">snapshot: {snap} · commit: {commit}</text>
  <line x1="24" y1="196" x2="{w-24}" y2="196" stroke="#8c4a00" stroke-width="2"/>
  <text x="24" y="224" fill="#6b6b6b" font-size="13">red lines: never fabricate · costed change lists · unified counting ·</text>
  <text x="24" y="244" fill="#6b6b6b" font-size="13">honest trichotomy (verified / mathematical / candidate) · no bypassing scanners</text>
  <text x="24" y="276" fill="#8c4a00" font-size="13">github.com/jiangfeng-strathclyde/Athena · MIT · skill texts mirrored from ARIS (MIT)</text>
</svg>
"""
    Path(a.out + ".svg").write_text(svg, encoding="utf-8")
    Path(a.out + ".md").write_text(md, encoding="utf-8")
    print(f"wrote {a.out}.svg and {a.out}.md (skills={n_skills}, snapshot={snap})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
