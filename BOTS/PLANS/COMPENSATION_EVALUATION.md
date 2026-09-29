# ATLAS TIA compensation simulation — 24 September 2026

## Decision

The nominal 0.2 pF and 0.5 pF C1 populations both satisfy the planned
**≥1 kHz bandwidth, ≥60° phase margin, and ≤1 dB peaking** limits in all
160 declared capacitance/load combinations for each value. **0.5 pF has only
61 Hz of minimum-bandwidth margin.** An illustrative +0.1 pF fitted-capacitor
shift makes its worst corner miss 1 kHz, especially with R1 at +1%. The
0.2 pF population retains at least 212 Hz margin at the corresponding
illustrative +0.1 pF, +1% R1 corner. Prefer **0.2 pF for the first prototype
population**, with 0.5 pF assembled as a comparison if practical. Final C1
selection requires physical bandwidth/noise tests. The KiCad first-prototype
population is now YAGEO `CQ0603BRNPO9BNR20` (0.2 pF, ±0.1 pF, 50 V,
C0G/NP0, 0603). The 0.5 pF option remains a comparison population.

## Model and circuit

- LTspice 26.1.1, TI `OPAx828.LIB` model Final 1.3 from `SBOMAJ0D.ZIP`.
  Top-level model order: `IN+ IN- VCC VEE OUT`. The model includes input
  impedance, so only external capacitance is added at `TIP`.
- KiCad design values: OPA828, R1=100 MΩ, R2=220 Ω, ±15 V feeds each through
  10 Ω, 100 nF and nominal 10 µF local rail capacitors. The output load is
  after R2.
- Additional input capacitance: 0, 5, 15, 35, 85 pF. Feedback stray
  capacitance: 0, 0.1, 0.3, 1 pF. Cable capacitance after R2: 0, 100, 500,
  1000 pF. Receiver: 100 kΩ or approximately open (1 TΩ). Fitted C1: 0.2,
  0.5, 1, 5 pF. This is 640 cases in each AC and loop-gain run.
- AC bandwidth is the first -3 dB crossing relative to the 1 Hz output
  magnitude for a 1 pA input current. Peaking is the maximum magnitude from
  1 Hz to 10 MHz relative to that 1 Hz value. Loop margin uses a 0 V DC / 1 V
  AC series source between the amplifier output and feedback branch;
  return ratio is `-V(AMP)/V(FB)`, with other AC inputs zero. Phase margin
  is 180° plus return-ratio phase at its 0 dB crossing. All cases had one
  bandwidth crossing and one loop-gain unity crossing.

## Full matrix results

| Fitted C1 | Cases meeting all three limits | -3 dB bandwidth range | Phase-margin range | Maximum peaking |
|---:|---:|---:|---:|---:|
| 0.2 pF | 160/160 | 1.327–8.716 kHz | 84.5–89.5° | 0.00 dB |
| 0.5 pF | 160/160 | 1.061–3.228 kHz | 86.2–89.5° | 0.00 dB |
| 1 pF | 120/160 | 0.796–1.597 kHz | 85.4–89.5° | 0.00 dB |
| 5 pF | 0/160 | 0.265–0.318 kHz | 81.2–88.7° | 0.00 dB |

The minimum bandwidth for each fitted value occurred with 0 pF additional
input, 1 pF feedback stray, 1000 pF cable and a 100 kΩ receiver. Failure
of the 1 pF and 5 pF options is due to bandwidth, not simulated phase margin
or peaking. The full per-case results are in
[`compensation_sweep.csv`](../../sim/atlas_tia/results/compensation_sweep.csv).

## Tolerance and transient checks

The selected [YAGEO Hi-Q NP0 series datasheet](https://yageogroup.com/content/datasheet/asset/file/UPY-HIGH_Q_NP0_16V-TO-500V)
defines the `B` tolerance code as ±0.1 pF, and the
[part listing](https://www.digikey.in/en/products/detail/yageo/CQ0603BRNPO9BNR20/11497278)
confirms the selected 0603 part's 0.2 pF, 50 V and C0G ratings. The
±0.1 pF corners below therefore match its stated tolerance, but remain
illustrative for the assembled circuit because actual pad and trace
capacitance are unmeasured. At the minimum-bandwidth load above:

| Nominal C1 and tolerance corner | R1 | Bandwidth | Phase margin |
|---|---:|---:|---:|
| 0.2 pF nominal, C1=0.3 pF | 101 MΩ | 1.213 kHz | 87.3° |
| 0.5 pF nominal, C1=0.6 pF | 100 MΩ | 0.995 kHz | 87.0° |
| 0.5 pF nominal, C1=0.6 pF | 101 MΩ | 0.985 kHz | 87.0° |

At the high-input-capacitance phase corner (85 pF extra input, 0 pF feedback
stray, 1000 pF cable, open receiver), C1=0.1 pF with R1=99–101 MΩ gave
71.2–71.5° phase margin. This tests the low side of an illustrative
selected 0.2 ±0.1 pF C1 population.

Four 1 nA step checks covered the minimum-bandwidth and minimum-phase-margin
corners for 0.2 and 0.5 pF. The measured change at 0.9–1.0 ms was -99.43
to -100.00 mV; no undershoot beyond the value at 1.099 ms was detected.
The last 100 µs before that point varied by at most 0.235 mV, consistent
with continuing settling at the slow corners. See
[`transient_corners.csv`](../../sim/atlas_tia/results/transient_corners.csv).

Replacing each nominal 10 µF local bulk capacitor with 1 or 3 µF changed
the minimum-bandwidth results by less than the printed 0.001 Hz and phase
margin by about 0.001° in this ideal-source model. This **does not**
validate supply decoupling against actual PSU/cable impedance or rail noise.

## Limits before PCB release

### Feedback stray headroom update — 29 September 2026

A targeted high-side tolerance study (C1 = 0.3 pF, R1 = 101 MΩ) found the
modeled 1 kHz bandwidth crossing at about 1.276 pF additional feedback
capacitance, or 1.576 pF fitted-plus-stray. The prior 1 pF stray envelope
therefore has about 0.276 pF of model headroom at that tolerance corner. An
80-case input/output-load check gave 40/40 passing at 1.27 pF stray and 0/40
passing at 1.28 pF. The reproducible decks, derived results and physical
test recommendation are in
[`sim/atlas_tia/FEEDBACK_STRAY_BUDGET.md`](../../sim/atlas_tia/FEEDBACK_STRAY_BUDGET.md).
This diagnostic estimate does not change C1 population or qualify the
assembled PCB. Measure the board's actual bandwidth with its harness and
receiver before release.

- The TI macromodel and ideal parasitic elements do not predict PCB leakage,
  contamination, the actual 0603 pad/guard capacitance, feedback-resistor
  excess noise, or mechanically induced current. The 1 pF feedback-stray
  value is an assumed envelope, not a measurement of the routed board.
- C1's first-prototype part and absolute tolerance are now recorded in
  KiCad. Confirm procurement and assembly availability before ordering;
  the 0.5 pF comparison part remains to be selected. Verify the assembled
  board's effective feedback capacitance and bandwidth.
- Receiver impedance and cable capacitance are provisional until the
  converter and harness are designed. Rail filtering needs a realistic
  source-impedance/noise model and bench measurement.
- Bench qualification still needs bipolar current injection, bandwidth,
  noise spectra, leakage, overload recovery, cable-load response and warm-up
  drift. Simulated phase margin does not replace these checks.

Reproduce the sweep with `LTspice.exe -b tia_opa828_ac_sweep.cir` and
`LTspice.exe -b tia_opa828_loop_sweep.cir` from the parent `sim/atlas_tia`
directory, then run
`summarize_sweep.py` against the two base paths. The raw and log outputs are
ignored by Git; the result CSV is retained.
