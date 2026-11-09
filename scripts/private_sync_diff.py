#!/usr/bin/env python3
"""Report drift between a private handbook and its public distillation.

Run with: ``python scripts/private_sync_diff.py [--private PATH]``
The default private path is ``D:\\MaxSeparation\\docs\\MAX_DISTILLED.md``.
Only counts, hashes, and short bullet previews are printed; the script never
writes private content into the repository.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "docs" / "DISTILLED_PUBLIC.md"
DEFAULT_PRIVATE = Path("D:/MaxSeparation/docs/MAX_DISTILLED.md")

SECTIONS = ("2", "3", "5")


def bullets(path: Path):
    out = {}
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s*(\d+)\.", line.strip())
        if m:
            cur = m.group(1)
            continue
        if cur in SECTIONS and line.strip().startswith(("- ", "* ")):
            text = re.sub(r"\*\*", "", line.strip()[2:]).strip()
            text = re.sub(r"\s+", " ", text)
            out[text] = cur
    return out


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--private", default=str(DEFAULT_PRIVATE))
    a = ap.parse_args()
    priv = Path(a.private)
    if not priv.is_file():
        print(f"Private handbook not found: {priv} (skipping drift check)")
        return 0
    pb, ub = bullets(priv), bullets(PUBLIC)
    only_priv = [t for t in pb if t not in ub]
    only_pub = [t for t in ub if t not in pb]
    common = [t for t in pb if t in ub]
    print(f"private sha : {sha(priv)}  ({priv})")
    print(f"public  sha : {sha(PUBLIC)}")
    print(f"common      : {len(common)}")
    print(f"only-private: {len(only_priv)}  -> review for safe public migration")
    print(f"only-public : {len(only_pub)}  -> check whether the private handbook is stale")
    for t in only_priv:
        print(f"  [priv-only §{pb[t]}] {t[:60]}")
    for t in only_pub:
        print(f"  [pub-only  §{ub[t]}] {t[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
