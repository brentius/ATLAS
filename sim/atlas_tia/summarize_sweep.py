"""Combine LTspice AC and loop-gain sweeps into a reproducible CSV summary."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from analyze_raw import read_ac, summarize_closed, summarize_loop


STEP = re.compile(r"^\.step\s+(.+)$", re.MULTILINE)


def labels(log_path: Path) -> list[dict[str, float]]:
    text = log_path.read_text(errors="replace")
    if "Total elapsed time:" not in text:
        raise ValueError(f"LTspice run is incomplete: {log_path}")
    output = []
    for match in STEP.finditer(text):
        output.append({item.split("=", 1)[0]: float(item.split("=", 1)[1])
                       for item in match.group(1).split()})
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ac", type=Path, required=True, help="AC sweep base path without extension")
    parser.add_argument("--loop", type=Path, required=True, help="Loop sweep base path without extension")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    ac_labels = labels(args.ac.with_suffix(".log"))
    loop_labels = labels(args.loop.with_suffix(".log"))
    ac_names, ac_steps = read_ac(args.ac.with_suffix(".raw"))
    loop_names, loop_steps = read_ac(args.loop.with_suffix(".raw"))
    n = len(ac_labels)
    if n != 640 or not (len(ac_steps) == len(loop_steps) == len(loop_labels) == n):
        raise ValueError(f"Incomplete or mismatched sweep: {n}, {len(ac_steps)}, "
                         f"{len(loop_labels)}, {len(loop_steps)}")
    if ac_labels != loop_labels:
        raise ValueError("AC and loop-gain case order does not agree")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["step", "cfit_pf", "cextra_pf", "cstray_pf", "ccable_pf",
                  "rreceiver_ohm", "transimpedance_ohm", "bandwidth_hz",
                  "peaking_db", "unity_hz", "phase_margin_deg",
                  "bandwidth_crossings", "unity_crossings", "passes"]
    rows = []
    for i, (case, ac, loop) in enumerate(zip(ac_labels, ac_steps, loop_steps), 1):
        closed = summarize_closed(ac_names, ac)
        stability = summarize_loop(loop_names, loop)
        row = {
            "step": i,
            "cfit_pf": case["cfit"] * 1e12,
            "cextra_pf": case["cextra"] * 1e12,
            "cstray_pf": case["cstray"] * 1e12,
            "ccable_pf": case["ccable"] * 1e12,
            "rreceiver_ohm": case["rreceiver"],
            **{key: closed[key] for key in ("transimpedance_ohm", "bandwidth_hz", "peaking_db", "bandwidth_crossings")},
            **{key: stability[key] for key in ("unity_hz", "phase_margin_deg", "unity_crossings")},
        }
        row["passes"] = (closed["bandwidth_hz"] is not None and closed["bandwidth_hz"] >= 1000
                         and closed["peaking_db"] <= 1
                         and stability["phase_margin_deg"] is not None
                         and stability["phase_margin_deg"] >= 60
                         and closed["bandwidth_crossings"] == 1
                         and stability["unity_crossings"] == 1)
        rows.append(row)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    for cf in (0.2, 0.5, 1.0, 5.0):
        subset = [row for row in rows if abs(row["cfit_pf"] - cf) < 1e-8]
        print(f"C1={cf:g}pF: pass {sum(row['passes'] for row in subset)}/{len(subset)}, "
              f"BW {min(row['bandwidth_hz'] for row in subset):.1f}.."
              f"{max(row['bandwidth_hz'] for row in subset):.1f} Hz, "
              f"PM {min(row['phase_margin_deg'] for row in subset):.1f}.."
              f"{max(row['phase_margin_deg'] for row in subset):.1f} deg, "
              f"peak max {max(row['peaking_db'] for row in subset):.2f} dB")
    print(f"Results: {args.output}")


if __name__ == "__main__":
    main()
