#!/usr/bin/env python3
"""上游 ARIS 月度 diff：列出新增/删除/语义可能变更的技能，供策展决策。

用法：python scripts/upstream_diff.py [--cache DIR] [--save-snapshot]
默认缓存：仓库外 ../.aris-upstream（不进入仓库）。仅浅克隆，无写仓库行为；
--save-snapshot 才更新 clone-kit/UPSTREAM_SNAPSHOT.json（策展完成后执行）。
哈希前统一 LF 行尾、剥离本仓库追加段、去掉结尾空行，避免噪声。
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = "https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep"
SNAPSHOT = ROOT / "clone-kit" / "UPSTREAM_SNAPSHOT.json"
MARKERS = ("## 镜像说明", "## 环境适配")
CRLF = "\r\n"
LF = "\n"


def norm(text: str) -> str:
    return text.replace(CRLF, LF).rstrip(LF)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def norm_hash(p: Path) -> str:
    return digest(norm(p.read_text(encoding="utf-8")))


def git(cache: Path, *args):
    return subprocess.run(["git", "-C", str(cache), *args],
                          capture_output=True, text=True)


def upstream_skills(cache: Path):
    base = cache
    for cand in (base / "skills", base):
        if cand.is_dir() and any(p.is_dir() for p in cand.iterdir()):
            base = cand
            break
    out = {}
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        f = d / "SKILL.md"
        if f.is_file():
            out[d.name] = norm_hash(f)
    return out


def mirrored_skills():
    out = {}
    skills = ROOT / "skills"
    for d in sorted(p for p in skills.iterdir() if p.is_dir()):
        f = d / "SKILL.md"
        if f.is_file():
            text = norm(f.read_text(encoding="utf-8"))
            cut = min([len(text)] + [text.index(m) for m in MARKERS if m in text])
            out[d.name] = digest(text[:cut].rstrip(LF))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=str(ROOT.parent / ".aris-upstream"))
    ap.add_argument("--save-snapshot", action="store_true")
    a = ap.parse_args()
    cache = Path(a.cache)
    if not (cache / ".git").is_dir():
        cache.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "clone", "--depth", "1", UPSTREAM, str(cache)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("clone 失败：", r.stderr.strip()[:300])
            return 1
    else:
        git(cache, "fetch", "--depth", "1", "origin")
        git(cache, "reset", "--hard", "FETCH_HEAD")

    up = upstream_skills(cache)
    mine = mirrored_skills()
    head = git(cache, "rev-parse", "--short", "HEAD").stdout.strip()

    added = sorted(set(up) - set(mine))
    removed = sorted(set(mine) - set(up))
    changed = sorted(k for k in set(up) & set(mine) if up[k] != mine[k])

    print(f"upstream head : {head}")
    print(f"upstream skills: {len(up)}   mirrored: {len(mine)}")
    print(f"added upstream : {len(added)}")
    for n in added:
        print("  +", n)
    print(f"removed upstream: {len(removed)}  (本仓库非 ARIS 镜像项会列在这里，属预期)")
    for n in removed:
        print("  -", n)
    print(f"content differs : {len(changed)}  (已剥离追加段/行尾/结尾空行，仍需人工判语义)")
    for n in changed:
        print("  ~", n)

    if a.save_snapshot:
        SNAPSHOT.write_text(json.dumps(
            {"upstream": UPSTREAM, "head": head, "skills": up},
            ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"snapshot saved -> {SNAPSHOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
