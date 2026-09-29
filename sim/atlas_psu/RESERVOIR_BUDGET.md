# PSU reservoir and transformer envelope — 29 September 2026

## Provisional circuit update

C1/C2 in the PSU schematic now use **4700 µF, 50 V** Nichicon
`LGY1H472MELB30`, matching the exact part and 30 mm / 10 mm snap-in
footprints already on the PSU PCB. The [Nichicon LGY series datasheet](https://www.nichicon.com/getmedia/6716b3c6-abcc-4da1-80b0-b33e29e5a195/e-lgy-DB.pdf)
lists this part as 30 × 30 mm, ±20%, with 2.1 A RMS rated ripple at
105°C/120 Hz. Its 50–120 Hz frequency coefficient is 0.88–1.00. Check
assembly sourcing and the actual capacitor current waveform before release.

This restores schematic/PCB part parity and improves the calculated
low-line trough. In the simplified case below, 4700 µF leaves +2.49 V
idealized headroom at 216.2 V input, or +0.70 V at 200 V input, during
the hypothetical additional 0.5 A / 10 ms pulse. The 200 V margin is
small before winding, ESR and wiring losses. **The circuit is a
prototype population, not a validated PSU rating.** Larger capacitance
raises stored energy, inrush and discharge time: each nominal 4700 µF
reservoir holds about 2.56 J at 33 V and takes about 89 s to fall from
33 V to 5 V through a 10 kΩ bleeder alone (about 112 s at +20% C and
+5% R). The enclosure and bench procedure must treat the rails as live
until measured discharged.

## Finding

An earlier PSU schematic candidate used **2200 µF, 50 V** Ymin
`LKMJ2501H222MF` for both raw reservoirs, while the board still carried
4700 µF Nichicon parts. The analysis below preserves that comparison and
uses the existing plan assumptions; it does not qualify either population.

The former 2200 µF low-line example has about **2.80 V** of idealized raw-rail
headroom beyond a 15.1 V output plus a provisional 3.0 V regulator
differential. A hypothetical **additional 0.5 A for 10 ms** consumes
`0.5 A × 10 ms / 1760 µF = 2.84 V` at the capacitor's -20% tolerance;
the calculated headroom becomes **-0.04 V** even before winding, wiring,
ESR and regulator transient losses. The earlier plan's 2.3 V pulse estimate
used the nominal 2200 µF rather than the minimum 1760 µF. This pulse is an
illustrative stack demand, not a measured load or fixed requirement.

The candidate Vigortronix `VTX-146-030-218` specifies a **200–264 V**
series-primary input range, 2 × 18 V, 0.83 A, 30 VA and **14% typical**
regulation in its [manufacturer datasheet](https://www.vigortronix.com/wp-content/uploads/2021/09/VTX-146-xxxx-2-Series-Dual-Primary-Toroida-D0008.pdf).
The plan's 216.2 V (-6%) case is therefore only one possible low-line
scenario. At the datasheet's 200 V input limit, the same idealized estimate
has only **1.00 V** headroom without a pulse and **-1.84 V** with the pulse.
Whether ATLAS must operate throughout 200–264 V is a project requirement
decision; this review does not silently extend it.

| Primary input | Capacitor | No-pulse headroom | Headroom with +0.5 A for 10 ms |
|---:|---:|---:|---:|
| 216.2 V | 2200 µF | +2.80 V | -0.04 V |
| 216.2 V | 3300 µF | +3.44 V | +1.55 V |
| 216.2 V | 4700 µF | +3.82 V | +2.49 V |
| 200.0 V | 2200 µF | +1.00 V | -1.84 V |
| 200.0 V | 3300 µF | +1.65 V | -0.25 V |
| 200.0 V | 4700 µF | +2.03 V | +0.70 V |

The 4700 µF row is the selected provisional prototype population; 2200
and 3300 µF are comparisons. Larger capacitance also affects inrush,
charging-current RMS, bleeder time, package/footprint and cost. The table
cannot establish a release rating until the stack current waveform and
required primary-voltage range are established.

## Reproducible method and limits

`reservoir_budget.py` writes the full derived table to
`results/reservoir_budget.csv`. It uses:

`Vpeak = 18 Vrms × (Vprimary / 230 V) × √2 − 1.1 V`

`Vtrough = Vpeak − (0.34 A × 10 ms + Ipulse × 10 ms) / (0.8 × Cnominal)`

`headroom = Vtrough − 15.1 V − 3.0 V`

The 18 Vrms at 230 V and 0.34 A positive-rail average draw come from the
local PSU plan; 1.1 V one-diode drop and 3.0 V regulator differential are
its provisional assumptions. Both the selected
[Nichicon LGY](https://www.nichicon.com/getmedia/6716b3c6-abcc-4da1-80b0-b33e29e5a195/e-lgy-DB.pdf)
and former [Ymin LKM](https://www.ymin.cn/lead-type-miniature-type-aluminum-electrolytic-capacitor-lkm-product/)
series list **±20%** capacitance tolerance at 120 Hz.
The 10 ms no-recharge interval is a simple upper-bound discharge model at
100 Hz. It does not account for capacitor-input transformer loading, winding
resistance/regulation under pulsed charge, rectifier conduction angle,
capacitor ESR, capacitance versus temperature/frequency/age, wiring drop,
regulator current limits, recovery, or regenerated stack energy. The actual
raw trough can differ in either direction; this estimate is insufficient
for release.

## Ripple-current correction and high-line ceiling

The [Ymin LKM page](https://www.ymin.cn/lead-type-miniature-type-aluminum-electrolytic-capacitor-lkm-product/)
lists this part at 3.57 A RMS rated ripple current and gives frequency
coefficients of **0.4 at 50 Hz, 0.5 at 120 Hz and 1 at 100 kHz**. Thus the
plan's provisional `0.65 × 3.57 ≈ 2.3 A at 100 Hz` is not supported by the
manufacturer's coefficients. Direct multiplication gives 1.43 A at 50 Hz
and 1.79 A at 120 Hz at the table's reference temperature. The actual
capacitor charging waveform contains harmonics, so its heating must be
checked using measured/simulated current RMS and spectral content, not a
single 100 Hz multiplier. No capacitor ripple-current margin is claimed.

At the datasheet's 264 V upper input and **typical** 14% no-load regulation,
the ideal secondary peak before rectifier drop is
`18 × (264/230) × 1.14 × √2 = 33.31 V`. At light load the diode drop can be
small, so the plan's provisional **33 V raw ceiling** is not a guaranteed
upper bound over the transformer's full input range. The 14% is typical,
not a guaranteed maximum. Device-voltage, reservoir-energy and thermal
checks need a justified system high-line limit and transformer tolerance.

## Required discriminator

Define the maximum *additional* stack pulse current, duration, repetition
rate and which rail it loads; define ATLAS's intended AC input range.
Then model the exact transformer with measured or guaranteed winding
impedance, rectifier and capacitor ESR, and test the built supply under
combined/asymmetric loads. Record both raw troughs, regulator outputs,
capacitor current RMS, rail-valid behavior and temperature. Retain 2200 µF
as an alternative only if the measured/revised model margins and thermal
limits meet the agreed operating envelope. No mains wiring was changed.

## KiCad verification

KiCad 10.0.6 ERC on the revised schematic found **no errors** and one
warning for the intentionally isolated `CHASSIS` contact. DRC with
schematic parity found **zero parity issues** after matching C1/C2 fields
between schematic and board. The unfinished PSU PCB still reports
**106 design-rule violations**, **118 unconnected items** and no valid
`Edge.Cuts` outline. Generated JSON reports are kept locally under the
ignored `pcb/atlas_psu/routing_review/` directory. These results verify
part-field consistency, not layout or electrical readiness.
