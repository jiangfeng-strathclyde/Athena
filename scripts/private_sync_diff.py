#!/usr/bin/env python3
"""私有分身手册 ↔ 公开蒸馏手册 的漂移检查（只报计数与归属侧，不落盘私有内容）。

用法：python scripts/private_sync_diff.py [--private PATH]
默认私有路径：D:\\Max分身\\docs\\MAX_DISTILLED.md
输出仅到 stdout；是否把某条“可迁移红线/方法论”同步进公开版，由人工判定后编辑公开版。
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "docs" / "DISTILLED_PUBLIC.md"
DEFAULT_PRIVATE = Path("D:/Max分身/docs/MAX_DISTILLED.md")

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
        print(f"私有手册不存在：{priv}（跳过漂移检查）")
        return 0
    pb, ub = bullets(priv), bullets(PUBLIC)
    only_priv = [t for t in pb if t not in ub]
    only_pub = [t for t in ub if t not in pb]
    common = [t for t in pb if t in ub]
    print(f"private sha : {sha(priv)}  ({priv})")
    print(f"public  sha : {sha(PUBLIC)}")
    print(f"common      : {len(common)}")
    print(f"only-private: {len(only_priv)}  -> 逐条判定是否可迁移（项目事实永不迁移）")
    print(f"only-public : {len(only_pub)}  -> 检查是否已被私有版废弃")
    for t in only_priv:
        print(f"  [priv-only §{pb[t]}] {t[:60]}")
    for t in only_pub:
        print(f"  [pub-only  §{ub[t]}] {t[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
