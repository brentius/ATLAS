"""Idealized positive raw-rail trough budget for the proposed ATLAS PSU.

This intentionally omits winding resistance, capacitor ESR, wiring loss,
rectifier conduction angle, and regulator dynamics. It cannot qualify a PSU.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
NOMINAL_PRIMARY_V = 230.0
SECONDARY_RMS_V = 18.0  # assumed at nominal primary and rated winding load
DIODE_DROP_V = 1.1  # plan assumption, one conducting bridge diode per rail
BASE_CURRENT_A = 0.34  # positive reservoir, including auxiliary and bleeder
CAP_MIN_FRACTION = 0.8  # -20% tolerance for both compared reservoir parts
DISCHARGE_S = 0.010  # one 100 Hz interval, conservatively no recharge
OUTPUT_REQUIRED_V = 15.1
DROPOUT_ALLOWANCE_V = 3.0
EXTRA_PULSE_A = 0.5  # illustrative additional positive-rail current
PULSE_S = 0.010


def row(primary_v: float, nominal_cap_uf: int, pulse_a: float) -> dict[str, float]:
    cap_f = nominal_cap_uf * 1e-6 * CAP_MIN_FRACTION
    peak_v = SECONDARY_RMS_V * primary_v / NOMINAL_PRIMARY_V * math.sqrt(2) - DIODE_DROP_V
    base_drop_v = BASE_CURRENT_A * DISCHARGE_S / cap_f
    pulse_drop_v = pulse_a * PULSE_S / cap_f
    trough_v = peak_v - base_drop_v - pulse_drop_v
    return {
        "primary_v": primary_v,
        "nominal_cap_uf": nominal_cap_uf,
        "minimum_cap_uf": cap_f * 1e6,
        "extra_pulse_a": pulse_a,
        "pulse_ms": PULSE_S * 1e3 if pulse_a else 0,
        "ideal_peak_v": peak_v,
        "base_drop_v": base_drop_v,
        "pulse_drop_v": pulse_drop_v,
        "raw_trough_v": trough_v,
        "headroom_after_3v_allowance_v": trough_v - OUTPUT_REQUIRED_V - DROPOUT_ALLOWANCE_V,
    }


def main() -> None:
    rows = [row(primary, cap, pulse)
            for primary in (NOMINAL_PRIMARY_V * 0.94, 200.0)
            for cap in (2200, 3300, 4700)
            for pulse in (0.0, EXTRA_PULSE_A)]
    # Reproduce the plan's rounded baseline at -6% line, -20% capacitance.
    assert 20.8 < rows[0]["raw_trough_v"] < 21.0
    assert rows[0]["headroom_after_3v_allowance_v"] > 0
    assert rows[1]["headroom_after_3v_allowance_v"] < 0
    assert all(r["base_drop_v"] > 0 and r["ideal_peak_v"] > r["raw_trough_v"] for r in rows)

    output = HERE / "results/reservoir_budget.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for r in rows:
        print(f"{r['primary_v']:.1f} V, {r['nominal_cap_uf']} uF, "
              f"+{r['extra_pulse_a']:.1f} A pulse: trough {r['raw_trough_v']:.3f} V, "
              f"headroom {r['headroom_after_3v_allowance_v']:+.3f} V")
    print(f"Results: {output}")


if __name__ == "__main__":
    main()
