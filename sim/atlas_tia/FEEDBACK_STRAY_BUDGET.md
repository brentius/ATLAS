# TIA feedback-capacitance budget — 29 September 2026

## Result and interpretation

**Simulated, not measured.** With the selected C1 at its stated high tolerance
end (0.3 pF), R1 at the schematic's assumed +1% end (101 MΩ), and the
existing TI OPAx828 macromodel, the 1 kHz closed-loop bandwidth boundary is
approximately **1.276 pF of additional feedback capacitance**. That is
approximately 1.576 pF total fitted-plus-stray feedback capacitance. The
previous 1 pF stray assumption leaves about 0.276 pF of model headroom. No
assembled-board stray capacitance has been measured.

| Additional feedback C | Worst -3 dB bandwidth | Cases ≥1 kHz |
|---:|---:|---:|
| 1.00 pF | 1212.481 Hz | targeted load only |
| 1.20 pF | 1050.752 Hz | targeted load only |
| 1.27 pF | 1003.881 Hz | 40/40 |
| 1.28 pF | 997.530 Hz | 0/40 |
| 1.30 pF | 985.039 Hz | targeted load only |

The 40 cases at each bracket value cover 0/5/15/35/85 pF external input
capacitance, 0/100/500/1000 pF output cable capacitance, and 100 kΩ/1 TΩ
receivers. The minimum occurred at 0 pF added input, 1000 pF cable, and
100 kΩ receiver, as in the earlier sweep. All 80 cases had one -3 dB
crossing and 0 dB reported peaking over the simulated frequency range.

The interpolated 1.276 pF crossing is a **diagnostic model estimate**, not a
manufacturing tolerance or physical pass criterion. In particular, the
macromodel, ideal parasitic capacitors, unknown cover/lead geometry, and
unverified receiver prevent sub-0.01 pF predictions for a real board. The
simple RC estimate, `1/(2π × 101 MΩ × 1 kHz) = 1.57579 pF` total feedback
capacitance, independently agrees with the simulated 1.576 pF threshold but
cannot establish phase margin, peaking or noise. The prior sweep remains the
evidence for those other simulated limits inside its declared 0–1 pF stray
envelope.

## Physical acceptance check

For the assembled preamp, inject a calibrated small-signal current through a
known injection capacitor or other characterized current source without
permanently loading the tip node. Record its amplitude and uncertainty versus
frequency. With the intended harness and receiver connected, measure the
output transimpedance at a low reference frequency and the first -3 dB
crossing. Also repeat with the declared worst-case 1000 pF cable and 100 kΩ
receiver if that envelope remains the project requirement. The existing
≥1 kHz bandwidth and ≤1 dB peaking criteria apply to the **measured**
response. Record C1 population, R1 measurement, harness, receiver, source
calibration, and test conditions. The effective feedback capacitance may be
estimated from the response for diagnosis, but the measured frequency
response determines acceptance. Noise, leakage and overload recovery remain
separate checks.

## Reproduction and provenance

- Design inputs: `pcb/atlas_tia/atlas_tia.kicad_sch` records C1 = 0.2 pF,
  ±0.1 pF, and R1 = 100 MΩ, 1%; `tia_opa828_stray_budget_*.cir` record the
  analyzed high-side values and all loads.
- Model: local TI `OPAx828.LIB` Final 1.3 from `SBOMAJ0D.ZIP`, used by
  LTspice 26.1.1. Its licensed copy is deliberately excluded from Git.
- Run `LTspice.exe -b tia_opa828_stray_budget_ac.cir` and
  `LTspice.exe -b tia_opa828_stray_budget_envelope.cir` from `sim/atlas_tia`.
  Wait for `Total elapsed time:` in each log, then run
  `python summarize_stray_budget.py`. The derived 80-case table is
  `results/feedback_stray_budget.csv`; original local waveform/log files
  remain untouched and ignored by Git.
- The summary script checks step counts, unique crossings, the 1 kHz
  bracket, and agreement between the targeted and envelope runs.
