# ATLAS project status — 29 September 2026

ATLAS aims to build a low-cost STM that can image the HOPG carbon lattice.
The root README uses an intentionally aspirational tense; no physical
imaging result is documented in this repository.

## Current engineering state

- **TIA:** Routed KiCad board and TI-model compensation study exist. The
  selected 0.2 pF C1 population passed the 160 declared nominal
  parasitic/load simulation cases. The
  [feedback-capacitance analysis](sim/atlas_tia/FEEDBACK_STRAY_BUDGET.md)
  quantifies limited model headroom. Assembled bandwidth, leakage, noise,
  overload recovery, head fit and the actual receiver remain unmeasured.
- **PSU:** Populated schematic and an unfinished, unrouted PCB exist. C1/C2
  are provisionally 4700 µF Nichicon in both. The
  [reservoir budget](sim/atlas_psu/RESERVOIR_BUDGET.md) compares the former
  2200 µF candidate, and [DECISIONS.md](DECISIONS.md) records the trade-off.
  KiCad 10.0.6 ERC has no errors and one explained isolated-CHASSIS warning.
  The PCB DRC finds an absent board outline, 118 unconnected items and
  silkscreen violations; it is not ready for fabrication. Loaded rail,
  capacitor RMS current, thermal, startup, fault and mains/enclosure
  behavior are unqualified.
- **Converter, mechanics and control:** No converter KiCad project or
  tracked `cad/` or `code/` implementation is present. Scanner motion and
  load, head geometry, harness and receiver contracts remain undefined by
  measured evidence here.
- **Local records:** `BOTS/` contains detailed plans and role guidance but
  is intentionally ignored by Git. This file and DECISIONS.md are the
  portable project-state summary.

## Highest-value next action

Define the required AC input range and measure or specify the stack
driver's additional current waveform (peak, width, duty and rail). Then
qualify the PSU's raw troughs, capacitor current, thermal and fault
behavior under those conditions before releasing a board or energizing
the scanner.
