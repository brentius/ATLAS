"""Check the selected C1's modeled feedback-stray bandwidth budget.

Run both tia_opa828_stray_budget_*.cir decks with LTspice batch mode first.
The ignored .raw/.log files are required inputs; the CSV is a derived result.
"""

from __future__ import annotations

import csv
from pathlib import Path

from analyze_raw import read_ac, summarize_closed
from summarize_sweep import labels


HERE = Path(__file__).resolve().parent
LIMIT_HZ = 1000.0


def cases(stem: str, expected: int) -> list[dict[str, float]]:
    base = HERE / stem
    case_labels = labels(base.with_suffix(".log"))
    names, steps = read_ac(base.with_suffix(".raw"))
    if len(case_labels) != expected or len(steps) != expected:
        raise ValueError(f"{stem}: expected {expected} steps, got "
                         f"{len(case_labels)} labels and {len(steps)} waveforms")
    result = []
    for label, step in zip(case_labels, steps):
        metric = summarize_closed(names, step)
        if metric["bandwidth_crossings"] != 1 or metric["bandwidth_hz"] is None:
            raise ValueError(f"{stem}: ambiguous -3 dB crossing for {label}")
        result.append({**label, **metric})
    return result


def main() -> None:
    fine = cases("tia_opa828_stray_budget_ac", 8)
    envelope = cases("tia_opa828_stray_budget_envelope", 80)
    fine_by_stray = {round(row["cstray"] * 1e12, 6): row for row in fine}
    expected_fine = {1.0, 1.2, 1.25, 1.27, 1.275, 1.28, 1.3, 1.5}
    if set(fine_by_stray) != expected_fine:
        raise ValueError("Missing, duplicate, or unexpected fine-sweep steps")
    expected_grid = {
        (stray, cextra, ccable, receiver)
        for stray in (1.27, 1.28)
        for cextra in (0, 5, 15, 35, 85)
        for ccable in (0, 100, 500, 1000)
        for receiver in (100000.0, 1e12)
    }
    observed_grid = [
        (round(row["cstray"] * 1e12, 6), round(row["cextra"] * 1e12, 6),
         round(row["ccable"] * 1e12, 6), row["rreceiver"])
        for row in envelope
    ]
    if len(set(observed_grid)) != 80 or set(observed_grid) != expected_grid:
        raise ValueError("Envelope grid has missing, duplicate, or unexpected cases")
    worst: dict[float, dict[str, float]] = {}
    for row in envelope:
        stray_pf = round(row["cstray"] * 1e12, 6)
        if stray_pf not in (1.27, 1.28):
            raise ValueError(f"Unexpected envelope Cstray: {stray_pf} pF")
        if stray_pf not in worst or row["bandwidth_hz"] < worst[stray_pf]["bandwidth_hz"]:
            worst[stray_pf] = row
    if len(worst) != 2:
        raise ValueError("Missing one envelope Cstray value")
    for stray_pf, row in worst.items():
        reference = fine_by_stray[stray_pf]["bandwidth_hz"]
        if abs(reference - row["bandwidth_hz"]) > 0.001:
            raise ValueError(f"Fine/envelope disagreement at {stray_pf} pF")

    low = fine_by_stray[1.275]["bandwidth_hz"]
    high = fine_by_stray[1.28]["bandwidth_hz"]
    if not low >= LIMIT_HZ > high:
        raise ValueError("The 1 kHz crossing is not bracketed")
    estimate_pf = 1.275 + (LIMIT_HZ - low) * (1.28 - 1.275) / (high - low)

    output = HERE / "results/feedback_stray_budget.csv"
    output.parent.mkdir(exist_ok=True)
    fields = ["cstray_pf", "cextra_pf", "ccable_pf", "rreceiver_ohm",
              "bandwidth_hz", "peaking_db", "bandwidth_crossings", "passes_1khz"]
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in envelope:
            writer.writerow({
                "cstray_pf": row["cstray"] * 1e12,
                "cextra_pf": row["cextra"] * 1e12,
                "ccable_pf": row["ccable"] * 1e12,
                "rreceiver_ohm": row["rreceiver"],
                "bandwidth_hz": row["bandwidth_hz"],
                "peaking_db": row["peaking_db"],
                "bandwidth_crossings": row["bandwidth_crossings"],
                "passes_1khz": row["bandwidth_hz"] >= LIMIT_HZ,
            })
    for stray_pf in (1.27, 1.28):
        subset = [row for row in envelope if round(row["cstray"] * 1e12, 6) == stray_pf]
        row = worst[stray_pf]
        print(f"Cstray={stray_pf:.2f} pF: {sum(r['bandwidth_hz'] >= LIMIT_HZ for r in subset)}/"
              f"{len(subset)} pass; minimum {row['bandwidth_hz']:.3f} Hz at "
              f"Cextra={row['cextra'] * 1e12:g} pF, "
              f"Ccable={row['ccable'] * 1e12:g} pF, "
              f"Rreceiver={row['rreceiver']:g} ohm")
    print(f"Interpolated model crossing: Cstray={estimate_pf:.6f} pF "
          f"(C1+stray={estimate_pf + 0.3:.6f} pF)")
    print(f"Results: {output}")


if __name__ == "__main__":
    main()
