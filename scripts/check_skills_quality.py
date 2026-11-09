#!/usr/bin/env python3
"""技能入库 QC：扫描 skills/*/SKILL.md，硬检查 + 质量评分。

硬检查（任一失败则退出码 1，进 CI）：
  H1 SKILL.md 存在且非空
  H2 frontmatter 存在（--- 包围）
  H3 frontmatter 含 name，且与目录名一致
  H4 frontmatter 含 description，且 ≤1024 字符
  H5 正文（frontmatter 之后）≥200 字符

质量评分（仅报告，不卡 CI；借鉴 24 分制 rubric 思路，见 docs/LESSONS_FROM_OTHERS.md）：
  Q1 frontmatter 含 license 字段            +2
  Q2 frontmatter 含 version 字段            +1
  Q3 frontmatter 含 tags 或 dependencies    +1
  Q4 正文含 ≥3 个 markdown 标题             +2
  Q5 正文 ≥1000 字符                        +2
  满分 8；仓库均分与最低分技能打印在末尾。
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
            failures.append(f"{d.name}: H1 SKILL.md 缺失或为空")
            continue
        text = f.read_text(encoding="utf-8").lstrip("\ufeff")
        fm, body = parse_frontmatter(text)
        if fm is None:
            failures.append(f"{d.name}: H2 frontmatter 缺失或未闭合")
            continue
        name = fm.get("name", "").strip("'\"")
        if not name:
            failures.append(f"{d.name}: H3 缺 name")
        elif name != d.name:
            failures.append(f"{d.name}: H3 name 与目录名不一致 (name={name})")
        desc = fm.get("description", "")
        if not desc:
            failures.append(f"{d.name}: H4 缺 description")
        elif len(desc) > 1024:
            failures.append(f"{d.name}: H4 description 超长 ({len(desc)} > 1024)")
        if len(body.strip()) < 200:
            failures.append(f"{d.name}: H5 正文过短 ({len(body.strip())} < 200)")
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
