# ATLAS project status — 29 September 2026

ATLAS aims to build a low-cost STM that can image the HOPG carbon lattice.
The root README is aspirational; no physical imaging result is documented
in this repository.

## Current state

- **TIA:** Routed KiCad board and TI-model compensation studies exist. The
  selected 0.2 pF C1 population passed its 160 declared nominal
  parasitic/load cases within the 640-case sweep. The
  [compensation evaluation](COMPENSATION_EVALUATION.md) and
  [feedback-stray analysis](../../sim/atlas_tia/FEEDBACK_STRAY_BUDGET.md)
  document simulated results. Physical bandwidth, noise, leakage,
  overload recovery, head fit and cable loading remain unmeasured.
- **PSU:** Populated KiCad schematic exists, with C1/C2 now provisionally
  4700 µF Nichicon to match the existing PCB;
  the PCB and live hardware are not qualified. The 29 September independent
  [calculation](../../sim/atlas_psu/RESERVOIR_BUDGET.md) identifies the former
  2200 µF candidate's near-zero modeled positive-rail headroom for a
  hypothetical additional 0.5 A, 10 ms stack pulse at 216.2 V primary
  input and minimum reservoir capacitance. At 4700 µF, the same simplified
  case has +2.49 V idealized headroom. The capacitor maker's low-frequency
  ripple factors also supersede an optimistic factor in the earlier local
  plan. KiCad 10.0.6 ERC has zero errors and one reserved-CHASSIS warning.
  PCB DRC found 106 violations, including a missing outline and silkscreen
  issues, and 118 unconnected items. Exact part
  qualification, source behavior, loaded thermal and fault checks remain
  open.
- **Converter, mechanics and control:** No converter project or tracked
  `cad/` or `code/` implementation is present. Scanner motion/load, head
  geometry, receiver and harness contracts have no recorded physical
  qualification here.
- **Records:** This status, the [decision log](DECISIONS.md) and design
  plans in this directory are shared through Git. Role instructions in
  `BOTS/AGENTS` remain local.

## Open questions and next gate

1. Define the required AC input range for ATLAS and the stack driver's
   maximum **additional** current, pulse width, duty cycle and rail path.
2. For the PSU, use those inputs with measured or guaranteed transformer
   winding data, capacitor ESR/ripple current and exact regulator limits;
   test raw troughs, capacitor RMS current, rail-valid timing and temperature
   on the assembled supply before selecting reservoir size for release.
3. Characterize the assembled TIA with the actual head, harness and
   receiver against its gain, bandwidth, noise and recovery gates.

The most valuable immediate engineering action is item 1, because the
unmeasured stack pulse and unspecified system line range dominate the PSU
reservoir and regulator margins.
