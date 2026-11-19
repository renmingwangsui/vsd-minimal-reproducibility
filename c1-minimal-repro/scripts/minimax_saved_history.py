#!/usr/bin/env python3
"""Finite saved-history sup-norm diameter and midpoint minimax calculation."""
import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

REQUIRED = {"descriptor_class", "history_id", "output", "node", "time_s", "value"}

def calculate(path):
    data = defaultdict(lambda: defaultdict(dict))
    clocks = defaultdict(dict)
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        for row in reader:
            key = (row["descriptor_class"], row["output"])
            hid, node = row["history_id"], int(row["node"])
            t, value = float(row["time_s"]), float(row["value"])
            if not (math.isfinite(t) and math.isfinite(value)):
                raise ValueError(f"non-finite value at {key}/{hid}/{node}")
            if node in data[key][hid]:
                raise ValueError(f"duplicate node {node} at {key}/{hid}")
            if node in clocks[key] and clocks[key][node] != t:
                raise ValueError(f"clock mismatch at {key}/{node}")
            data[key][hid][node] = value
            clocks[key][node] = t

    result = []
    for (cls, output), histories in sorted(data.items()):
        ids = sorted(histories)
        nodes = sorted(clocks[(cls, output)])
        expected = set(nodes)
        for hid in ids:
            if set(histories[hid]) != expected:
                raise ValueError(f"saved-grid mismatch: {cls}/{output}/{hid}")
        ranges = []
        for node in nodes:
            vals = [histories[hid][node] for hid in ids]
            ranges.append(max(vals) - min(vals))
        diameter = max(ranges, default=0.0)
        radius = diameter / 2.0
        worst = 0.0
        for hid in ids:
            err = max(abs(histories[hid][node] -
                          (max(histories[h][node] for h in ids) +
                           min(histories[h][node] for h in ids)) / 2.0)
                      for node in nodes)
            worst = max(worst, err)
        result.append({
            "descriptor_class": cls, "output": output,
            "n_histories": len(ids), "n_nodes": len(nodes),
            "diameter_sup": format(diameter, ".17g"),
            "half_diameter": format(radius, ".17g"),
            "midpoint_worst_error": format(worst, ".17g"),
            "absolute_identity_residual": format(abs(worst-radius), ".17g"),
            "scope": "finite_saved_grid_unrestricted_prediction"
        })
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    rows = calculate(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["descriptor_class", "output"]
    with args.output.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"classes={len(rows)} output={args.output}")

if __name__ == "__main__":
    main()
