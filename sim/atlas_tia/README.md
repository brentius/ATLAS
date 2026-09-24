# ATLAS TIA simulation

LTspice is suitable for the TIA compensation study. The `tia_opa828_*.cir`
files use TI's OPAx828 PSpice model. The `tia_proxy_*.cir` files are earlier
preliminary circuit checks using a deliberately simple 45 MHz gain-bandwidth
proxy. Open a `.cir` file in LTspice and click Run (or use LTspice batch mode).
For a `.cir` file, the working batch form is `LTspice.exe -b file.cir`.

## First TI-model run, 24 September 2026

LTspice 26.1.1 completed both TI-model netlists with exit code 0 and no logged
model errors. Baseline assumptions were 15 pF **external** input capacitance,
0.1 pF feedback stray capacitance, 100 pF output cable capacitance, and a
100 kΩ receiver. The 1 pA AC source gave about 99.8 MΩ low-frequency output
transimpedance. The 1 nA positive current step gave approximately -99.8 mV
output change (measured during the pulse, before it switched off).

| Fitted C1 | Simulated -3 dB bandwidth |
|---:|---:|
| 0.2 pF | 5.37 kHz |
| 0.5 pF | 2.66 kHz |
| 1 pF | 1.45 kHz |
| 5 pF | 0.312 kHz |

In this baseline, the maximum output magnitude from 1 Hz to 100 kHz occurred
at 1 Hz for all four values, so no gain peaking appeared in that interval.
The full 640-case parasitic/load and loop-gain sweep, tolerance corners,
step checks and evaluation are recorded in
[`results/COMPENSATION_EVALUATION.md`](results/COMPENSATION_EVALUATION.md).
The raw waveform and log files are local generated outputs and are ignored
by Git.

## Circuit represented

- 100 MΩ feedback resistor, stepped fitted C1 = 0.2, 0.5, 1, or 5 pF.
- Independent feedback stray capacitance, initially 0.1 pF.
- The proxy netlists add 15 pF for amplifier input capacitance. The TI-model
  netlists use the model's own input impedance and add only separately
  adjustable tip/PCB/cable capacitance.
- ±15 V incoming rails, 10 Ω series rail filters, 100 nF and 10 µF local
  capacitors on each rail.
- 220 Ω output resistor, provisional 100 kΩ receiver and output cable
  capacitance.

The AC files inject 1 pA AC into the tip. The transimpedance trace is
`-V(out)/1p`; nominal low-frequency magnitude is about 100 MΩ. Compare the
frequency response and peaking between C1 values. The step files apply
a 1 nA current step; the ideal settled output change is about -100 mV. The
proxy has only a single dominant pole and approximate output swing. It omits
the real amplifier's bias, noise, extra poles, overload behavior, and slew
limits. Consequently it cannot establish the planned 60° phase-margin gate.

## Remaining qualification

The 640-case AC and loop-gain sweeps are complete with the TI model. The
exact C1 part/tolerance, actual feedback stray capacitance, real cable and
receiver, supply impedance, noise, overload recovery and physical-board tests
remain open. The evaluation report states the population recommendation and
its limits.

The official TI archive `sbomaj0d.zip` and extracted `OPAx828.LIB` are in the
local `vendor/` directory, which is ignored by Git because the model is TI's
copyrighted evaluation material. The archive was downloaded from the OPA828
product page on 24 September 2026. Its top-level declaration is
`.SUBCKT OPAx828 IN+ IN- VCC VEE OUT`; the TI netlists connect `0 TIP VP VN RAW`
in that exact order. The model's usage notes list differential and common-mode
input impedance among the modeled parameters, so the TI netlists add only
external input capacitance. Model-specific results still require checking the
LTspice log and the physical board.
