# ATLAS engineering decisions

## 2026-09-29 — Provisional PSU reservoir population

**Decision:** Populate C1 and C2 with Nichicon `LGY1H472MELB30`
(4700 µF, ±20%, 50 V) for the next PSU prototype. The existing PCB already
uses its 30 mm, 10 mm pitch snap-in footprint; the schematic now matches
it. This is a prototype choice, **not** fabrication or electrical-safety
approval. The exact part's [manufacturer datasheet](https://www.nichicon.com/getmedia/6716b3c6-abcc-4da1-80b0-b33e29e5a195/e-lgy-DB.pdf)
lists 2.1 A RMS at 105°C/120 Hz. Assembly availability still needs a
current quote.

**Reasoning:** The preceding 2200 µF schematic option did not match the
4700 µF PCB. In the simplified low-line calculation at -20% capacitor
tolerance, 0.34 A baseline draw and an illustrative additional 0.5 A for
10 ms, the 2200 µF option leaves -0.04 V of provisional regulator
headroom at 216.2 V primary; 4700 µF leaves +2.49 V. At the candidate
transformer's [200 V lower input rating](https://www.vigortronix.com/wp-content/uploads/2021/09/VTX-146-xxxx-2-Series-Dual-Primary-Toroida-D0008.pdf),
4700 µF leaves only +0.70 V in this idealized case. Winding impedance,
rectifier conduction, capacitor ESR, temperature, wiring loss and the
actual stack pulse are not included. See
[`sim/atlas_psu/RESERVOIR_BUDGET.md`](sim/atlas_psu/RESERVOIR_BUDGET.md).

**Trade-offs and alternatives:** The larger part increases inrush,
charging-current RMS, stored energy and bleeder time. 3300 µF improves
the 2200 µF trough but needs a different exact part and footprint review;
its idealized headroom at 200 V with that pulse is still negative.
Remaining at 2200 µF would require proving the stack pulse and line
envelope are sufficiently smaller. Changing to a different transformer
or separate actuator energy source is a system architecture decision.

**Before release:** Define ATLAS's AC input range and stack-driver peak
current, duration, repetition and rail path. Model or measure the exact
transformer and capacitor current waveform, then test raw trough,
regulated rails, inrush, reservoir discharge, temperature and fault
response under combined and asymmetric loads. The PCB also needs a valid
outline, routing and design-rule review.
