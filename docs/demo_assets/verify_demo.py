#!/usr/bin/env python3
"""Independently recompute the statistics shown in the README demo.

Run with: ``python docs/demo_assets/verify_demo.py``
Exit status 0 means the CSV and README agree; status 1 blocks the check.
The data is synthetic and documented in this directory's README.
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
        raise SystemExit(f"FAIL: seed(s) {missing} lack a complete baseline/ours pair")
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
        failures.append(f"mean {mean:.2f} != README claim {CLAIMED_MEAN}")
    if round(std, 2) != CLAIMED_STD:
        failures.append(f"std {std:.2f} != README claim {CLAIMED_STD}")

    readme = README_PATH.read_text(encoding="utf-8")
    claim = f"{CLAIMED_MEAN} ± {CLAIMED_STD}"
    if readme.count(claim) < 2:
        failures.append(f"README contains '{claim}' {readme.count(claim)} time(s); expected at least 2")
    if "cherry-pick" not in readme:
        failures.append("README does not label the single-seed maximum as cherry-picking")

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        return 1
    print("PASS: README statistics match the independent CSV recomputation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
