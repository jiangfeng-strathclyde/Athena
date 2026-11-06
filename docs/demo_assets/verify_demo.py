#!/usr/bin/env python3
"""独立第二实现：从原始 fold 级 CSV 重算 README 演示对话里的统计量。

用法：python docs/demo_assets/verify_demo.py
退出码 0 = 与 README 声明一致；1 = 不一致（按协议应停稿）。
仅用标准库。数据为合成示例，见同目录 README.md。
"""
import csv
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "demo_results.csv"
README_PATH = HERE.parent.parent / "README.md"

CLAIMED_MEAN = 1.17
CLAIMED_STD = 1.84


def load_deltas():
    per_seed = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            per_seed.setdefault(int(row["seed"]), {})[row["method"]] = float(row["miou"])
    seeds = sorted(per_seed)
    missing = [s for s in seeds if set(per_seed[s]) != {"baseline", "ours"}]
    if missing:
        raise SystemExit(f"FAIL: seed {missing} 缺少 baseline/ours 配对，口径不完整")
    return seeds, [round(per_seed[s]["ours"] - per_seed[s]["baseline"], 4) for s in seeds]


def main():
    seeds, deltas = load_deltas()
    mean = statistics.mean(deltas)
    std = statistics.stdev(deltas)
    print(f"seeds          : {seeds}")
    print(f"per-seed delta : {deltas}")
    print(f"mean +/- std   : {mean:.2f} +/- {std:.2f}  (sample std, n={len(deltas)})")

    failures = []
    if round(mean, 2) != CLAIMED_MEAN:
        failures.append(f"mean {mean:.2f} != README 声明 {CLAIMED_MEAN}")
    if round(std, 2) != CLAIMED_STD:
        failures.append(f"std {std:.2f} != README 声明 {CLAIMED_STD}")

    readme = README_PATH.read_text(encoding="utf-8")
    claim = f"{CLAIMED_MEAN} ± {CLAIMED_STD}"
    if readme.count(claim) < 2:
        failures.append(f"README 中 '{claim}' 出现 {readme.count(claim)} 次，期望 >= 2（中文对话 + 英文摘要）")
    if "cherry-pick" not in readme:
        failures.append("README 未把单 seed 最大值标注为 cherry-pick")

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        return 1
    print("PASS: README 的数字与原始 CSV 的独立重算一致。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
