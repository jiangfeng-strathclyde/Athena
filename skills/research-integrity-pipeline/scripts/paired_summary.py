#!/usr/bin/env python3
"""Summarize paired runs from a long-format CSV without changing any files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import statistics
from pathlib import Path


def summarize(path: Path, *, metric: str, baseline: str, candidate: str,
              unit: str, pair_column: str = "seed", method_column: str = "method") -> dict:
    if not baseline.strip() or not candidate.strip() or baseline == candidate:
        raise ValueError("Baseline and candidate must be distinct, nonempty method names.")
    if not unit.strip():
        raise ValueError("Specify the metric's stored unit; no rescaling is performed.")
    required = [pair_column, method_column, metric]
    if len(set(required)) != 3 or not all(required):
        raise ValueError("Pair, method, and metric columns must have distinct, nonempty names.")
    raw = path.read_bytes()
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    fields = reader.fieldnames or []
    if len(fields) != len(set(fields)) or not set(required).issubset(fields):
        raise ValueError("CSV needs unique headers including: " + ", ".join(required))
    pairs: dict[str, dict[str, dict]] = {}
    ignored = 0
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"Malformed field count at CSV line {reader.line_num}.")
        method = row[method_column]
        if not method.strip():
            raise ValueError(f"Missing method at CSV line {reader.line_num}.")
        if method not in {baseline, candidate}:
            ignored += 1
            continue
        pair = row[pair_column]
        if not pair.strip():
            raise ValueError(f"Missing pair ID at CSV line {reader.line_num}.")
        bucket = pairs.setdefault(pair, {})
        if method in bucket:
            raise ValueError(f"Duplicate method {method!r} for pair {pair!r}; no rows were averaged or dropped.")
        try:
            value = float(row[metric])
        except ValueError as exc:
            raise ValueError(f"Invalid metric at CSV line {reader.line_num}.") from exc
        if not math.isfinite(value):
            raise ValueError(f"Non-finite metric at CSV line {reader.line_num}.")
        bucket[method] = {"value": value, "csv_line_end": reader.line_num}
    if not pairs:
        raise ValueError("No rows match the requested methods.")
    incomplete = [pair for pair, values in pairs.items() if len(values) != 2]
    if incomplete:
        raise ValueError("Incomplete pairs; supply the missing runs or document a separate exclusion: "
                         + ", ".join(incomplete))
    records = [{"pair_id": pair, "baseline": values[baseline], "candidate": values[candidate],
                "difference": values[candidate]["value"] - values[baseline]["value"]}
               for pair, values in pairs.items()]
    deltas = [record["difference"] for record in records]
    if not all(math.isfinite(value) for value in deltas):
        raise ValueError("Paired difference exceeds the supported numeric range.")
    mean = statistics.mean(deltas)
    std = statistics.stdev(deltas) if len(deltas) > 1 else None
    if not math.isfinite(mean) or (std is not None and not math.isfinite(std)):
        raise ValueError("Summary exceeds the supported numeric range.")
    return {
        "source": {"path": str(path.resolve()), "sha256": hashlib.sha256(raw).hexdigest()},
        "metric": metric, "unit": unit, "pair_column": pair_column,
        "method_column": method_column, "baseline_method": baseline, "candidate_method": candidate,
        "difference_definition": "candidate minus baseline; original units; no rounding before aggregation",
        "n_pairs": len(deltas), "mean_difference": mean, "sample_std_difference": std,
        "std_definition": "sample standard deviation (n-1); null when n=1",
        "ignored_other_method_rows": ignored, "pairs": records,
        "scope": "Descriptive arithmetic only. Pair validity, independence, completeness of the supplied "
                 "dataset, scientific significance, and direction of improvement require separate review.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--metric", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--unit", required=True, help="Stored units, e.g. percentage-points or seconds.")
    parser.add_argument("--pair-column", default="seed")
    parser.add_argument("--method-column", default="method")
    args = parser.parse_args(argv)
    try:
        result = summarize(args.csv, metric=args.metric, baseline=args.baseline,
                           candidate=args.candidate, unit=args.unit,
                           pair_column=args.pair_column, method_column=args.method_column)
        print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, csv.Error, OverflowError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
