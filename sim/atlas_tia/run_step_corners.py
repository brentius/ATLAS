"""Run TI-model step checks at the AC sweep's minimum BW/PM corners."""

from __future__ import annotations

import csv
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
LTSPICE = Path(os.environ.get(
    "ATLAS_LTSPICE",
    Path.home() / "AppData/Local/Programs/ADI/LTspice/LTspice.exe",
))
CASES = [
    ("c02_min_bw", "0.2p", "0p", "1p", "1000p", "100k"),
    ("c02_min_pm", "0.2p", "85p", "0p", "1000p", "1T"),
    ("c05_min_bw", "0.5p", "0p", "1p", "1000p", "100k"),
    ("c05_min_pm", "0.5p", "0p", "1p", "100p", "1T"),
]

DECK = """ATLAS TIA - step response at {name} with TI OPAx828
.include ../vendor/OPAx828.LIB
VPLUS VPLUS_IN 0 15
VMINUS VMINUS_IN 0 -15
R3 VPLUS_IN VP 10
R4 VMINUS_IN VN 10
C2 VP 0 100n
C3 VN 0 100n
C4 VP 0 10u
C5 VN 0 10u
IIN 0 TIP PULSE(0 1n 100u 1n 1n 1m 2m)
Cexternal TIP 0 {cextra}
R1 TIP RAW 100Meg
C1 TIP RAW {cfit}
Cfeedback_stray TIP RAW {cstray}
XU1 0 TIP VP VN RAW OPAx828
R2 RAW OUT 220
Rload OUT 0 {rreceiver}
Cload OUT 0 {ccable}
.tran 0 1.3m 0 20n
.meas tran before AVG V(out) FROM=50u TO=90u
.meas tran during AVG V(out) FROM=900u TO=1000u
.meas tran final FIND V(out) AT=1099u
.meas tran minimum MIN V(out) FROM=100u TO=1099u
.meas tran late_pp PP V(out) FROM=900u TO=1000u
.save V(OUT)
.end
"""


def measurement(log: str, name: str) -> float:
    match = re.search(rf"(?m)^\s*{name}:.*?=(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)", log)
    if not match:
        raise ValueError(f"Missing {name} measurement")
    return float(match.group(1))


def main() -> None:
    generated = HERE / "generated"
    generated.mkdir(exist_ok=True)
    output = []
    for name, cfit, cextra, cstray, ccable, rreceiver in CASES:
        deck = generated / f"{name}.cir"
        deck.write_text(DECK.format(name=name, cfit=cfit, cextra=cextra,
                                    cstray=cstray, ccable=ccable,
                                    rreceiver=rreceiver))
        completed = subprocess.run([str(LTSPICE), "-b", str(deck)],
                                   cwd=generated, timeout=120, check=False,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        if completed.returncode:
            raise RuntimeError(f"LTspice failed for {name}: {completed.returncode}")
        log = deck.with_suffix(".log").read_text(errors="replace")
        if "Total elapsed time:" not in log or "Error" in log:
            raise RuntimeError(f"Incomplete or erroneous simulation: {name}")
        before = measurement(log, "before")
        during = measurement(log, "during")
        final = measurement(log, "final")
        minimum = measurement(log, "minimum")
        late_pp = measurement(log, "late_pp")
        output.append({
            "case": name, "cfit_pf": float(cfit[:-1]), "cextra_pf": float(cextra[:-1]),
            "cstray_pf": float(cstray[:-1]), "ccable_pf": float(ccable[:-1]),
            "rreceiver": rreceiver, "step_change_mv": 1000 * (during - before),
            "undershoot_mv": 1000 * max(0, final - minimum),
            "late_pp_mv": 1000 * late_pp,
        })
    destination = HERE / "results/transient_corners.csv"
    destination.parent.mkdir(exist_ok=True)
    with destination.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    for row in output:
        print(row)
    print(destination)


if __name__ == "__main__":
    main()
