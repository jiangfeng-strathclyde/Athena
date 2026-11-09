#!/usr/bin/env python3
"""仓库自校验：README/题图里的计数与目录、清单、演示数据必须互相咬合。

用法：python scripts/check_repo_consistency.py
任一检查失败退出码为 1。仅用标准库。
"""
import csv
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
MANIFEST = ROOT / "clone-kit" / "MANIFEST.json"
DEMO_CSV = ROOT / "docs" / "demo_assets" / "demo_results.csv"
TRANSPARENCY = ROOT / "docs" / "TRANSPARENCY_LOG.md"

EXPECTED_SKILL_DIRS = 108
EXPECTED_MANIFEST_ENTRIES = 198
TRIPLE = ["citation-audit", "paper-claim-audit", "experiment-audit"]
BLOCKED = ["deepxiv", "paper-compile", "paper-poster-html"]

failures = []


def check(label, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (f"  [{detail}]" if detail else ""))
    if not ok:
        failures.append(label)


def declares_skill_count(text):
    return (f"{EXPECTED_SKILL_DIRS} 个科研技能" in text
            or f"{EXPECTED_SKILL_DIRS} research skills" in text)


def main():
    readme = README.read_text(encoding="utf-8")
    skill_dirs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())

    n = len(skill_dirs)
    check(f"skills/ 目录数 == {EXPECTED_SKILL_DIRS}", n == EXPECTED_SKILL_DIRS, f"actual={n}")
    check("README 声明 108 个技能（中/英文任一）", declares_skill_count(readme))
    for svg in ["assets/hero.svg", "assets/social-preview.svg"]:
        text = (ROOT / svg).read_text(encoding="utf-8")
        check(f"{svg} 声明 108 个技能（中/英文任一）", declares_skill_count(text))

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    m = len(manifest)
    check(f"MANIFEST 条目 == {EXPECTED_MANIFEST_ENTRIES}", m == EXPECTED_MANIFEST_ENTRIES, f"actual={m}")

    for name in TRIPLE:
        check(f"最小可信集技能存在: {name}", (SKILLS / name / "SKILL.md").is_file())
        check(f"README 提到 {name}", f"`{name}`" in readme)

    for name in BLOCKED:
        check(f"被拦截技能仍镜像: {name}", (SKILLS / name / "SKILL.md").is_file())
        check(f"TRANSPARENCY_LOG 记录 {name}", name in TRANSPARENCY.read_text(encoding="utf-8"))

    deltas = {}
    with DEMO_CSV.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            deltas.setdefault(int(row["seed"]), {})[row["method"]] = float(row["miou"])
    seq = [round(d["ours"] - d["baseline"], 4) for _, d in sorted(deltas.items())]
    mean, std = statistics.mean(seq), statistics.stdev(seq)
    claim = f"{mean:.2f} ± {std:.2f}"
    check(f"README 数字与 demo CSV 重算一致 ({claim})", readme.count(claim) >= 2, f"occurrences={readme.count(claim)}")

    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", readme):
        link = match.group(1)
        if link.startswith(("http", "#", "mailto")):
            continue
        target = (README.parent / link.split("#")[0]).resolve()
        check(f"README 链接有效: {link}", target.exists())

    if failures:
        print(f"\n{len(failures)} 项不一致：")
        for f in failures:
            print("  -", f)
        return 1
    print("\n全部一致。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
