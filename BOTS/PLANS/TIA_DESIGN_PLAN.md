# ATLAS TIA: schematic design and wiring plan

Revision: 12 September 2026

Status: routing, test-pad rearrangement, 0603 C1 and the continuous exposed guard are complete as of 12 September 2026. All 18 physical components remain within the user's unchanged 35 × 12 mm board outline. The refilled saved board had zero unrouted connections, zero DRC violations (including silkscreen), and zero schematic-parity issues at that stage. Section 10 records the latest guard, local placement and separate ground-sense keepout. J2 retains its 1 × 2 mm solder-wire landing, moved 0.50 mm inward to accommodate the guard. Sections 7–9 record earlier layout stages. The TI-model compensation sweep was completed on 24 September 2026 (Section 11), but the exact C1 population and physical performance are not qualified. This expands [Section 3 of the ATLAS architecture](ATLAS_ARCHITECTURE.md#3-board-1-tia).

## 1. Starting point and notation

Keep the selected OPA828IDR, fixed 100 MΩ feedback, ±15 V input supplies and downstream 220 Ω output resistor. Start compensation at 0.5 pF and aim for at least 1 kHz bandwidth with a well-damped response. Use JLCPCB for assembly planning. Initial connector/contact footprints are now assigned for placement; board dimensions, mounting, head fit and cable clearance still require mechanical review.

Your custom library is `atlas_parts_lib`, stored in `pcb/atlas_parts_lib.kicad_sym`. The TIA schematic already contains its `OPA828IDR` symbol as **U1**. Use that existing U1; the designators below allocate the remaining parts.

**`U1.2` means pin 2 of component U1.** A *net* is one electrically connected group of wires and pins. Every pin listed on the same net must connect together. Pin numbers remain the same when a symbol is rotated or mirrored.

The library names below were checked against the installed KiCad 10 libraries. A **symbol** defines the schematic representation and pins; a **footprint** defines the PCB pads; a **manufacturer part number** identifies the component to order. Choosing `Device:R` and entering `100M` does not, by itself, select a suitable physical feedback resistor or a JLCPCB stock item.

## 2. Which library items to place

In the Schematic Editor, press **A** and search for the exact symbol identifier in this table. Set the reference, value and footprint in its properties. The table's dimensions use imperial package names: 0603, 1206 and 1210. The three `_Guard` footprints are project-local versions with standard copper pads and silkscreen gaps for the exposed guard.

| Reference | Purpose and value to enter | KiCad symbol | Footprint / selection status |
|---|---|---|---|
| U1 | Current amplifier; `OPA828IDR` | `atlas_parts_lib:OPA828IDR` | `atlas_parts_lib:SOIC-8_3.9x4.9mm_P1.27mm_Guard` |
| R1 | Feedback resistor; `100M` | `Device:R` | `atlas_parts_lib:R_1206_3216Metric_Guard`; initial RF candidate below |
| R2 | Output isolation; `220`, 1% | `Device:R` | `Resistor_SMD:R_0603_1608Metric` |
| R3, R4 | Positive/negative rail filters; `10`, 1% each | `Device:R` | `Resistor_SMD:R_0603_1608Metric` |
| C1 | Feedback compensation; `0.5p`, C0G/NP0, 50 V | `Device:C` | `atlas_parts_lib:C_0603_1608Metric_Guard` |
| C2, C3 | Positive/negative rail bypass; `100n`, X7R, 50 V each | `Device:C` | `Capacitor_SMD:C_0603_1608Metric` |
| C4, C5 | Positive/negative rail bulk; `10u`, X7R, 50 V each | `Device:C` | `Capacitor_SMD:C_1210_3225Metric`; starting package, subject to effective-capacitance and height checks |
| J1 | Five-contact power/signal connection; `TIA_LINK` | `Connector_Generic:Conn_01x05` | `Connector_JST:JST_GH_SM05B-GHS-TB_1x05-1MP_P1.25mm_Horizontal`; keyed side-entry SMD connector |
| J2 | Tip-lead solder connection; `TIP_CONTACT` | `Connector_Generic:Conn_01x01` | `Connector_Wire:SolderWirePad_1x01_SMD_1x2mm`; 1 × 2 mm landing for the flexible wire from the moving tip holder |
| J3 | Cover/shield attachment; `SHIELD_CONTACT` | `Connector_Generic:Conn_01x01` | `Connector_Wire:SolderWirePad_1x01_SMD_1.5x3mm`; solder pad for a shield/cover lead |
| TP1–TP5 | Output, rails and ground access; values listed below | `Connector:TestPoint` | `TestPoint:TestPoint_Pad_D1.0mm` |
| Ground symbols | Local analog ground, named **GNDA** | `power:GNDA` | No physical component or footprint |
| Five power flags | Declare the two incoming rails, two filtered rails and GNDA externally powered | `power:PWR_FLAG` | No physical component or footprint |

All physical components have assigned footprints. J2 now uses the installed standard `Connector_Wire:SolderWirePad_1x01_SMD_1x2mm` footprint, replacing the earlier custom 0.8 mm circular pad. Its single rounded rectangular pad uses front copper and solder mask, with no solder-paste opening. Pad 1 remains on `TIP_IN`. J2, J3 and TP1–TP5 are copper features, so they are excluded from the purchase BOM and component-placement output while remaining on the PCB. The tip holder is supported by the moving scanner; J2 terminates its short flexible lead on the fixed TIA. Provide strain relief at the fixed end and enough compliance for scanner motion. J1 is selected as the five-way JST GH harness interface; its fit must still be checked against the head and mated plug.

J1 uses JST `SM05B-GHS-TB`; the mating housing is `GHR-05V-S`, with `SSHL-002T-P0.2` contacts for a compatible wire size. The GH series is rated 50 V AC/DC, above the 30 V difference between the two supply rails. Check the manufacturer's mating-face numbering and cable exit during layout; its hold-down pads are mechanical and are not extra signal contacts. [JST GH catalogue](https://www.jst-mfg.com/product/pdf/eng/eGH.pdf)

The schematic contains the intended nine functional nets. U1 pins 5 and 8 remain unconnected; its internally unconnected pin 1 is now explicitly on GNDA for the PCB guard, as permitted by TI. Signal connectivity was preserved. R1–R4 had incorrectly inherited the amplifier's SOIC footprint; these were replaced with resistor footprints. Capacitors carry 50 V and dielectric requirements in their fields, but exact capacitor MPNs, DC-bias derating and JLCPCB availability remain purchasing checks.

### Physical-part selection

- **R1:** start with Vishay `CRHV1206AF100MFKE5`, 100 MΩ, 1%, ±100 ppm/°C. Its family lists a 25 ppm/V voltage coefficient for this resistance range. Verify sourcing and land-pattern suitability; its excess noise and feedback capacitance still need characterisation. [Vishay CRHV specification](https://www.vishay.com/docs/68002/crhv.pdf)
- **C1:** use one compact footprint. Obtain exact C0G/NP0 parts for 0.2, 0.5, 1 and 5 pF as alternative populations, recording absolute capacitance tolerance. Do not fit them as a selectable bank.
- **C4/C5:** the primary wiring tables below use **non-polar ceramic capacitors**. A nominal 10 µF ceramic can lose substantial capacitance under DC bias; use the selected manufacturer's data at 15 V and include tolerance/temperature effects in the rail-filter model. Keep mechanical sensitivity in the later bench checks.
- **All physical parts:** record exact manufacturer, part number, rating, footprint and verified JLCPCB sourcing route. Public stock, global sourcing and consignment are sourcing options, not proof of electrical suitability. [JLCPCB sourcing guidance](https://jlcpcb.com/help/article/pcba-parts-sourcing-instruction)

If a bulk capacitor later changes to a polarized electrolytic, change its symbol to `Device:C_Polarized` and assign the footprint of that exact part. Pin 1 is positive. **C4:** pin 1 to `VCC_TIA`, pin 2 to `GNDA`. **C5:** pin 1 to `GNDA`, pin 2 to `VEE_TIA`. The C5 pin assignment then differs from the ceramic baseline below; update the wiring table and netlist together.

### J2: direct contact or coax connection

The one-pin J2 represents the **tip's single electrical contact**, with the amplifier immediately beside it inside the conductive head cover. The cover connection is represented separately by J3. It does not represent a complete coax socket. The other electrode of the tunnelling junction is the sample, connected separately to the sample-bias driver; the tip must not be wired directly to GNDA.

If a cable is needed between the tip and amplifier, replace J2 with the installed **`Connector:Conn_Coaxial`** symbol and use a short shielded coax connection:

| Coax J2 pin | Conductor | Connect to |
|---|---|---|
| 1, `In` | Centre conductor | `TIP_IN`: U1.2, R1.1 and C1.1; the other end connects to the tip |
| 2, `Ext` | Outer conductor / shield | `GNDA` at the TIA end; keep the tip-end shield insulated from the tip, sample and chassis |

For this coax variant, **add J2.2 to the GNDA row of the complete net checklist**. J2.1 and every other circuit connection stay as specified. The coax shield screens the sensitive lead; it is not the sample connection. Do not add a 50 Ω termination across the current input.

Keep this GNDA-connected cable shield distinct from J3's `CHASSIS` net. A coax socket with a shell bonded to the metal cover would create a GNDA-to-chassis bond, so its mounting/insulation must be included in the system grounding decision before release. Match the eventual coax footprint's centre and shell pad numbers to the symbol; several physical shell pads may share pin number 2.

Retain the direct-contact baseline if the tip can sit immediately beside U1. If a cable is required, include its centre-to-shield capacitance and the connector capacitance in the input-capacitance model and repeat compensation checks. [TI transimpedance compensation guidance](https://www.ti.com/lit/an/sboa055a/sboa055a.pdf)

## 3. Exactly what connects to what

### 3.1 J1: provisional schematic pin allocation

Use these pin numbers to draw the schematic now. They are a proposed connector contract, not a verified physical cable pinout. Freeze the housing, mating-face orientation and numbering together before routing or making a harness.

| J1 pin | Cable function | Net on the TIA board | Connection |
|---|---|---|---|
| 1 | `TIA_OUT` | `TIA_OUT` | R2 pin 2 and TP2 pin 1 |
| 2 | `TIA_SENSE_0V` | `GNDA` | Separate sense route from the quiet local ground at U1 pin 3 |
| 3 | `PWR_RETURN` | `GNDA` | Dedicated power-return route; returns local bypass/bulk-capacitor currents |
| 4 | Incoming +15 V | `+15V_IN` | R3 pin 1 |
| 5 | Incoming −15 V | `-15V_IN` | R4 pin 1 |

J1 pins 1 and 2 form the output/sense signal pair. At the converter, pin 2 feeds the high-impedance receiver reference input; it must not be used as the converter's normal supply-return connection.

### 3.2 U1: amplifier pin map

| U1 pin | Function | Connect to |
|---|---|---|
| 1 | NC internally | Connect to GNDA as the endpoint of the PCB guard; exposed as a passive pin in the custom symbol |
| 2 | Inverting input, `−` | J2.1, R1.1 and C1.1; net `TIP_IN` |
| 3 | Non-inverting input, `+` | `GNDA` |
| 4 | Negative supply | R4.2, C3.1, C5.1 and TP4.1; net `VEE_TIA` |
| 5 | NC | Leave unwired |
| 6 | Amplifier output | R1.2, C1.2, R2.1 and TP1.1; net `TIA_RAW` |
| 7 | Positive supply | R3.2, C2.1, C4.1 and TP3.1; net `VCC_TIA` |
| 8 | NC | Leave unwired |

This is the **OPA828IDR SOIC-8** pinout. The custom symbol's output pin has no displayed text name, but its right-hand pin is pin 6. [TI OPA828 datasheet](https://www.ti.com/lit/ds/symlink/opa828.pdf)

### 3.3 Every resistor and capacitor terminal

| Component | Pin 1 connects to | Pin 2 connects to |
|---|---|---|
| R1 — 100 MΩ | `TIP_IN`: U1.2 | `TIA_RAW`: U1.6 |
| R2 — 220 Ω | `TIA_RAW`: U1.6 | `TIA_OUT`: J1.1 |
| R3 — 10 Ω | `+15V_IN`: J1.4 | `VCC_TIA`: U1.7 |
| R4 — 10 Ω | `-15V_IN`: J1.5 | `VEE_TIA`: U1.4 |
| C1 — 0.5 pF | `TIP_IN`: U1.2 | `TIA_RAW`: U1.6 |
| C2 — 100 nF ceramic | `VCC_TIA`: U1.7 | `GNDA` |
| C3 — 100 nF ceramic | `VEE_TIA`: U1.4 | `GNDA` |
| C4 — 10 µF ceramic | `VCC_TIA`: U1.7 | `GNDA` |
| C5 — 10 µF ceramic | `VEE_TIA`: U1.4 | `GNDA` |

R1 and C1 connect **in parallel**, between exactly the same two nodes. They return to **U1 pin 6 before R2**, not to J1 pin 1 after R2. The bypass and bulk capacitors connect **after** their respective 10 Ω rail resistors. Each capacitor connects between one rail and ground; none of these capacitors goes in series with a supply or signal.

Resistors and the selected ceramic capacitors are non-polar. Their pin assignments above establish a consistent drawing/netlist convention, rather than an electrical polarity requirement.

### 3.4 Complete net checklist

Use this table to check the finished drawing. It includes all physical component pins; the power flags and ground symbols are added as described below.

| Net | All physical pins that belong to this net |
|---|---|
| `TIP_IN` | J2.1, U1.2, R1.1, C1.1 |
| `TIA_RAW` | U1.6, R1.2, C1.2, R2.1, TP1.1 |
| `TIA_OUT` | R2.2, J1.1, TP2.1 |
| `+15V_IN` | J1.4, R3.1 |
| `-15V_IN` | J1.5, R4.1 |
| `VCC_TIA` | R3.2, U1.7, C2.1, C4.1, TP3.1 |
| `VEE_TIA` | R4.2, U1.4, C3.1, C5.1, TP4.1 |
| `GNDA` | U1.1, U1.3, C2.2, C3.2, C4.2, C5.2, J1.2, J1.3, TP5.1 |
| `CHASSIS` | J3.1 only at this stage; reserved for the external shield/cover connection |

U1 pins 5 and 8 intentionally belong to none of these nets. Pin 1 has no internal connection but is grounded externally for the guard. There is no test point on `TIP_IN`. Set the test-point values to `TIA_RAW`, `TIA_OUT`, `VCC_TIA`, `VEE_TIA` and `GNDA` for TP1 through TP5 respectively.

### 3.5 Ground, shield and power flags

Use **`GNDA` as the single schematic name for local TIA analog ground**; it is the ground called AGND/local analog ground in the architecture. `power:GNDA` symbols connect their attached wires together globally. Do not also create separate `AGND`, `GND` or `TIA_SENSE_0V` nets and assume their names make them connect.

`TIA_SENSE_0V` and `PWR_RETURN` are the **functions of J1 contacts 2 and 3**. For this simple schematic, both contacts electrically connect to `GNDA`. Add ordinary explanatory text beside the contacts, rather than giving the same ground wire conflicting net labels. In the layout handoff, explicitly require a separate sense trace from J1.2 to the quiet U1.3 reference point and a power-return route from J1.3 to the decoupling returns. A common net name does not enforce those physical routes; inspect them during PCB review.

J3 is a shield/cover interface only. Do not connect `CHASSIS` to `GNDA` in this schematic revision. The eventual chassis bond must be resolved with the converter, PSU and USB-ground arrangement. Its pending status blocks system/PCB release. A one-pin-label warning on this reserved contact should be documented specifically, rather than disabling that ERC check globally.

The drawn schematic uses `power:+15V` and `power:-15V` on the incoming rails, whose actual net names are **`+15V`** and **`-15V`**. These correspond to `+15V_IN` and `-15V_IN` in the wiring tables above; they remain electrically distinct from `VCC_TIA` and `VEE_TIA` after R3/R4.

Place one `power:PWR_FLAG` on each of **`+15V`**, **`-15V`**, **`VCC_TIA`**, **`VEE_TIA`** and **`GNDA`**. Five flags are required for this drawing because the incoming-rail power symbols also contain power-input pins. Flags on the incoming rails alone would not mark the nets after R3/R4 as powered. These flags are declarations for electrical-rule checking, not voltage sources or physical components. [KiCad power-pin and power-flag documentation](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#_power_pins_and_power_flags)

## 4. Suggested drawing order

1. Keep the existing U1 at the centre. Its `−` input is above its `+` input in the custom symbol.
2. Place J2 to the left and wire J2.1 to U1.2. Label the wire `TIP_IN`.
3. Draw R1 and C1 as separate parallel feedback branches from U1.6 back to U1.2. Add connection junctions where the branches meet; visual proximity is not a connection.
4. Connect U1.3 to `power:GNDA`.
5. Place R2 to the right of U1. Wire U1.6 → R2.1, then R2.2 → J1.1. Label the two sides `TIA_RAW` and `TIA_OUT` respectively.
6. Draw the positive supply block: J1.4 → R3.1; R3.2 → U1.7, C2.1 and C4.1. Connect C2.2 and C4.2 to GNDA.
7. Draw the negative supply block: J1.5 → R4.1; R4.2 → U1.4, C3.1 and C5.1. Connect C3.2 and C5.2 to GNDA. Label the incoming and filtered rail nets as in the checklist.
8. Connect J1.2 and J1.3 to GNDA and add the separate-sense/separate-return routing notes. Add J3 with its `CHASSIS` label and pending-bond note.
9. Add TP1–TP5 and the five power flags required by the drawn incoming/filtered supply symbols, then check every net against Section 3.4.
10. Run electrical-rule checking and review the component fields/footprints. Resolve real connection errors; record the intentionally deferred mechanical items.

Use wires or identically named attached labels to make connections. Schematic position does not determine PCB position: C2/C3 must eventually sit close to U1's supply pins, even if the supply blocks are drawn elsewhere on the page.

## 5. Simulation and electrical acceptance

### Baseline and assumptions

Use KiCad 10/ngspice with TI's OPA828 model, first validating compatibility and the model-terminal mapping. Symbol-to-footprint pin numbers are not automatically the model's terminal order. Verify which input capacitances and noise sources the model includes before adding external equivalents. [TI simulation models](https://www.ti.com/product/OPA828)

The datasheet lists 6 pF differential and 9 pF common-mode input capacitance. With the non-inverting input grounded, approximately 15 pF is a useful nominal device contribution; avoid counting it twice. Include the tip/contact, PCB and feedback-network parasitics separately. [TI datasheet](https://www.ti.com/lit/ds/symlink/opa828.pdf)

Initial sensitivity sweeps, pending actual head/cable data:

- Additional input capacitance: 0, 5, 15, 35 and 85 pF.
- Additional feedback capacitance: 0, 0.1, 0.3 and 1 pF.
- Output cable capacitance after R2: 0, 100, 500 and 1,000 pF.
- Receiver loading: open circuit and a provisional 100 kΩ load; replace the approximation with the converter's actual receiver network when designed.
- R1 tolerance, each C1 candidate's specified tolerance and effective bulk capacitance.

These are sensitivity cases, not measured capacitances or guaranteed operating limits.

### Compensation decision

| Fitted C1 | Ideal 100 MΩ–C1 pole, excluding parasitics |
|---|---:|
| 0.2 pF | 7.96 kHz |
| 0.5 pF | 3.18 kHz |
| 1 pF | 1.59 kHz |
| 5 pF | 318 Hz |

Evaluate signal bandwidth, loop gain/phase and transient response. The RC pole alone does not establish stability. Require at least **1 kHz bandwidth**, **60° simulated phase margin**, **no more than 1 dB peaking**, and no sustained oscillation across the declared capacitance/load envelope. [TI compensation guidance](https://www.ti.com/lit/an/sboa055a/sboa055a.pdf)

Retain 0.5 pF if it passes. Otherwise select the largest evaluated value that passes all criteria. Keep 5 pF as a slower diagnostic comparison. If none passes, revise the circuit or its justified operating envelope before handoff; do not silently relax the criteria.

### Gain, noise, power and recovery

- For current flowing into J2.1, the nominal unloaded transfer is `TIA_RAW = -ITIP × 100 MΩ`. Test ±100 pA, ±1 nA and ±10 nA; positive currents should give approximately −10 mV, −100 mV and −1 V. Separate zero-current offset from gain error and include R2/receiver attenuation at `TIA_OUT`.
- Check through ±25.6 nA for compatibility with the converter's nominal ×1 imaging span. Simulate current steps and ±200 nA overload pulses; record saturation and recovery limitations of the model.
- Calculate resistor thermal noise, amplifier voltage/current noise and output-network contributions. Report output noise and input-referred noise over 0.1–10 Hz and 1 Hz–1 kHz, stating the transfer function used for input referral. R1's calculated thermal-current noise at 300 K is approximately 12.9 fA/√Hz; it is not a measured system noise floor.
- Record the unmodelled contributions from excess resistor noise, leakage, contamination, interference and mechanical effects. Check DC offset separately, including amplifier bias current and plausible surface leakage.
- Approximately 5.5 mA nominal amplifier supply current implies about 55 mV drop across each 10 Ω filter resistor and roughly 165 mW amplifier dissipation. Check maximum current, output loading and warm-up implications before layout. [TI datasheet](https://www.ti.com/lit/ds/symlink/opa828.pdf)
- Review startup, shutdown and single-rail-loss behaviour. Numerical recovery results and the amplifier's datasheet settling figures do not qualify the assembled 100 MΩ TIA.

## 6. Handoff and completion criteria

The schematic-stage deliverables are the annotated KiCad schematic, a BOM with exact part identities/sourcing status, reproducible simulation files and results, and a PCB-layout handoff. Preserve the distinction between selected values, assumed parasitics and measured results.

The layout handoff must require a short input/feedback loop, local grounded guarding, deliberate copper clearance beneath the high-impedance node, separate sense/power-return routes, supply bypass placement, feedback takeoff before R2, and cleaning/drying/inspection. Do not add gain switching, ordinary protection diodes or a permanent injection network at the tip input.

The connection checklist and footprint/pin-number checks now pass, with no ERC errors and one explained warning for the one-pin CHASSIS net. PCB placement can begin with these footprints. Complete electrical qualification when the simulation criteria pass and sourcing/model limitations are documented. Before PCB release, verify J1/J2/J3 mechanical fit, head clearances, cable construction, effective capacitances and chassis bonding; their assigned footprints do not establish those results.

Later prototype qualification must include characterised external current injection in both directions, bandwidth/peaking, noise spectra, integrated noise, overload recovery, cable-load sensitivity and warm-up drift. Open-input noise testing uses a shielded open input, not an input shorted to ground. No physical performance is claimed by this document.

## 7. Initial PCB placement — 10 September 2026

**Historical placement study:** the following dimensions, positions and DRC results describe the 10 September version. The 11 September mechanical review supersedes that outline, and the user is undertaking the new placement and routing. J2's current footprint is listed in Section 2.

The working board is `atlas_tia.kicad_pcb`. All 18 footprints are placed on the front of a two-layer, 1.6 mm board with a **provisional 30 × 24 mm outline**. The outline is an initial placement envelope; mounting holes, tip attachment, strain relief, cover fit and cable clearance remain mechanical decisions.

J2's schematic already specified `atlas_parts_lib:TipContact_Pad_D0.8mm`, but the footprint was missing from the PCB. It has now been added, linked to the existing J2 symbol, with pad 1 on `TIP_IN`. This remains the direct-contact baseline described in Section 2.

| Group | Placement and reason |
|---|---|
| J2 and U1 | J2 sits left of U1 pin 2, with 2.725 mm between pad centres and approximately 1.35 mm between their nearest copper edges. Keep the eventual input route short. |
| R1 and C1 | Both sit above U1, with their pin-1/input pads aligned on the left and pin-2/output pads facing right. Keep the input branch compact and return feedback to U1 pin 6 before R2. |
| C2 and C3 | C2 sits beside U1 pin 7; C3 sits below U1 pin 4. Their rail pads face the corresponding supply pins. |
| R3/C4 and R4/C5 | Positive-rail filtering occupies the upper area; negative-rail filtering occupies the lower area. |
| R2 and J1 | R2 sits beside U1's output side. J1 is at the right edge with its cable exit facing outward. |
| TP1–TP5 and J3 | Test pads remain accessible on the output/power side. J3 sits near the lower-right edge and remains electrically separate from GNDA. |

Placement follows the short-input and close-bypass principles in [TI's OPA828 layout guidance, Section 8.4](https://www.ti.com/lit/ds/symlink/opa828.pdf). The saved PCB contains **zero tracks, zero vias and zero copper zones**. No guard or ground plane has been drawn yet.

The placement check reports **zero DRC violations and zero schematic-parity issues**, with **26 unconnected items expected at this unrouted stage**. Existing component pin/net assignments were preserved. These results establish placement and schematic consistency; they do not establish amplifier stability, leakage performance or production readiness.

At the routing stage, preserve the separate J1.2 ground-sense route to U1.3 and J1.3 power return described in Section 3.5. Their shared GNDA net currently does not enforce this separation. Resolve that routing constraint, input copper clearance and guarding before adding copper pours.

## 8. Placement and input routing update — 12 September 2026

The user's **35 × 12 mm outline is preserved exactly**, including its position, geometry and edge width. J1 and J2 also retain their positions and orientations. The board thickness remains 1.6 mm. No schematic connections, component values, footprints or project design rules were changed.

R1 and C1 now sit together above U1, with their input ends aligned and a shared compact branch to U1.2. J2 remains at the left edge. All input and feedback tracks stay on front copper. The total `TIP_IN` track centreline length, including all branches, was reduced from approximately 14.75 mm to 8.39 mm; this is a geometry comparison, not a measured capacitance or stability result. A B.Cu rule area named `TIP_IN_no_bottom_copper` prevents copper fills, tracks, pads and vias beneath the input and feedback region. The surrounding GNDA plane was refilled. U1.3 and the two bypass capacitors have their own local ground vias.

The remaining placement fits inside the existing outline:

- C4/R3 form the positive-rail filter group in the upper middle area.
- C5/R4 form the negative-rail filter group in the lower middle area.
- R2 sits beside U1's output; TP1 is connected to the output before R2.
- TP2 is toward J1 for the isolated output; TP3, TP4 and TP5 provide rail/ground access in the middle area.
- J3 is near the upper-right edge and remains on CHASSIS, separate from GNDA.

The direct track joining **J1.2 to J1.3 was removed**. J1.3 retains its power-return connection to the ground plane. **J1.2 is intentionally awaiting a separate sense route to the quiet U1.3 reference point.** Both pins still share the schematic GNDA net, so that physical separation must be maintained manually during routing. Do not resolve its unrouted connection by recreating the local bridge at J1.

At this earlier stage, the saved board had **14 unconnected items**, covering remaining power-filter/bulk-capacitor wiring, the output after R2, remaining test pads and the separate sense route. There were **zero non-silkscreen DRC violations and zero schematic-parity issues**. All 13 reported DRC warnings concerned silkscreen and were left unchanged at that stage. Section 9 supersedes this routing status; simulation, head fit and system grounding remain release checks.

## 9. Completed routing and test-pad arrangement — 12 September 2026

Historical completion stage: Section 10 supersedes the input-area placement, guard and sense-route coordinates below.

Finished the rail filters, bulk-capacitor returns, isolated output, all five test pads and the separate ground-sense connection. The actual starting file for this pass reported 11 unconnected items and 15 silkscreen warnings after refill, with no schematic-parity issues. The completed saved board passes KiCad 10.0.6 DRC with **zero violations, zero unconnected items and zero schematic-parity issues**, using the existing project rules and the all-track-errors option. No new DRC exclusions or relaxed rules were introduced.

The 35 × 12 mm outline, its coordinates and edge width, and the 1.6 mm board thickness are unchanged. J1, J2, J3, U1 and the other passive components retain their positions and orientations except R1, which moved 0.30 mm downward to make room for the upper grounded guard. All pad/net assignments, component values and footprint selections are preserved. Input and feedback connections remain entirely on F.Cu; the total TIP_IN track centreline length is now approximately **8.09 mm**.

TP1–TP5 form one row at y = 94.90 mm, with 2.70 mm centre spacing and the ground pad in the middle. Their original identities and nets are preserved:

| Left-to-right position | Reference | Signal | X position |
|---|---|---|---|
| 1 | TP1 | TIA_RAW, before R2 | 95.50 mm |
| 2 | TP2 | TIA_OUT, after R2 | 98.20 mm |
| 3 | TP5 | GNDA | 100.90 mm |
| 4 | TP3 | VCC_TIA, filtered positive rail | 103.60 mm |
| 5 | TP4 | VEE_TIA, filtered negative rail | 106.30 mm |

The 1 mm probe pads remain on the front, with references below them. Component-reference placements were adjusted to remove silkscreen collisions. No probe pad was added to TIP_IN.

J1.2 reaches a dedicated via at (110.90, 96.25) and then follows a 0.20 mm bottom-layer sense trace to the existing U1.3 reference via at (87.88, 96.685). The B.Cu rule area `TIA_SENSE_no_plane` excludes copper pours along this route, so it meets the GNDA plane only at the quiet-reference end. J1.3 retains its separate power-return via. The sense isolation was visually checked and sampled against the final filled plane, including its connector-end via; a shared net name alone is not relied on to enforce the separation.

The original `TIP_IN_no_bottom_copper` keepout is preserved. Grounded front-copper guard segments run above/left of the input network and below the tip landing, remaining open toward the tip connection at the board edge. The guards use GNDA-assigned copper graphics with explicit solder-mask openings; these open ends are intentional guard geometry. The upper guard returns through its own ground via, and the lower guard connects to U1.3. CHASSIS remains electrically separate from GNDA.

Local review files are in `routing_review/`: `before.kicad_pcb` preserves the input board, `final-drc.json` records the clean rule check, `layout-audit.json` records geometry/net and sense-plane checks, and `front-final.png` shows the actual KiCad front-copper/silkscreen plot. These review files follow the repository's existing ignore rules.

This completes PCB routing and pad rearrangement. It does not close the existing compensation simulation, exact-part sourcing, leakage/noise/cleaning qualification, connector/head mechanical-fit, or system chassis-bond release checks described above.

## 10. Continuous exposed guard and 0603 C1 — 12 September 2026

C1 now uses a standard 0603 copper/paste land pattern, retaining its 0.5 pF value, 50 V field and C0G/NP0 requirement. The front GNDA guard follows the user's specified path: **U1.3 → left edge → top → R1 pad gap → C1 pad gap → U1.1**. Copper width is 0.20 mm, with a continuous 0.30 mm F.Mask opening over every segment. No via fence was added.

TI lists pins 1, 5 and 8 as internally unconnected and permits grounding them. U1.1 is now a visible passive pin connected to GNDA in both the schematic and PCB; pins 5 and 8 remain unwired. The project symbol library carries the matching pin definition. [OPA828 datasheet, Table 5-1](https://www.ti.com/lit/ds/symlink/opa828.pdf#page=3)

The three local footprints listed in Section 2 retain the standard pad geometry and assembly courtyards. Their silkscreen is interrupted where the exposed guard passes through it. This avoids printing ink over the guard and keeps the board and footprint libraries consistent. The 0603 C1 pad gap provides 0.225 mm nominal copper clearance to each side of the 0.20 mm guard under the existing 0.20 mm net clearance rule.

Local placement changes relative to the user's saved board immediately before this revision:

| Part | Final position, mm | Change |
|---|---|---|
| J2 | (84.000, 95.000) | 0.500 mm inward, allowing the guard to pass between the solder landing and the left edge |
| R1 | (87.500, 90.800) | 0.250 mm upward |
| C1 | (87.500, 92.750) | Changed to 0603 and aligned its pad gap with R1's |
| U1 | (88.500, 96.275) | 0.225 mm downward for courtyard clearance |
| C3 | (86.805, 99.800) | 0.150 mm downward for courtyard clearance |

J1, J3, R2, all test pads and the remaining components retain their latest user-edited positions. The board outline and thickness are unchanged. Input and feedback tracks remain entirely on F.Cu; the total TIP_IN track centreline length is approximately 9.24 mm. Component values are unchanged. The only net-assignment change is U1.1 joining GNDA.

The B.Cu sense trace retains the user's bend near (95.48, 96.69) / (95.92, 96.25) and connector via at (110.17, 96.25). Its reference via is at (87.88, 96.685), connected to U1.3. `TIA_SENSE_no_plane` was redrawn as a corridor with a 0.40 mm centreline offset and an enlarged, chamfered area around the J1.2 via. It meets the ground plane only at the U1 reference end. The existing `TIP_IN_no_bottom_copper` area remains intact. The filled plane was inspected visually and checked at 2,652 sense-trace samples plus 360 points around the connector via.

Final KiCad 10.0.6 checks: **zero DRC violations, zero unrouted connections, zero schematic-parity issues and zero ERC errors**. The sole ERC warning is the previously documented one-pin CHASSIS label. Existing project rules and exclusions were not relaxed. `routing_review/guard-ring-drc.json`, `guard-ring-erc.json` and `guard-ring-audit.json` record the results; `guard-front.png` is the KiCad copper/silkscreen preview. The pre-edit PCB, schematic and symbol library are preserved under `routing_review/.history/guard-ring/`.

The larger C1 package and guard geometry remain subject to the existing compensation, parasitic-capacitance, cleaning, leakage/noise and mechanical qualification checks before release.

## 11. LTspice compensation sweep — 24 September 2026

The [simulation evaluation](COMPENSATION_EVALUATION.md) records a 640-case AC and loop-gain sweep using TI's OPAx828 PSpice model in LTspice 26.1.1. Nominal 0.2 pF and 0.5 pF populations met the ≥1 kHz bandwidth, ≥60° phase-margin and ≤1 dB peaking limits across all 160 capacitance/load cases each. Their minimum simulated bandwidths were 1.327 kHz and 1.061 kHz respectively. The 1 pF candidate failed bandwidth in 40/160 cases and 5 pF failed in all 160. Four extreme-corner 1 nA step simulations showed no undershoot beyond the late-pulse value.

The 0.5 pF population has little bandwidth margin. At the slowest declared corner, a 0.6 pF fitted value with 101 MΩ feedback gives 0.985 kHz. A 0.3 pF fitted value with 101 MΩ feedback gives 1.213 kHz. The first-prototype C1 value in both KiCad schematic and PCB is now **0.2 pF**, with YAGEO `CQ0603BRNPO9BNR20` (0603, 50 V, C0G/NP0, ±0.1 pF) recorded in the schematic. Its [manufacturer series datasheet](https://yageogroup.com/content/datasheet/asset/file/UPY-HIGH_Q_NP0_16V-TO-500V) defines the `B` tolerance code. The guarded footprint, routing and board outline are unchanged; 0.5 pF remains a comparison assembly option. Confirm procurement and assembly availability, measure actual PCB feedback capacitance and assembled-board frequency/noise response before release.

## 12. OpenSTM head-interface review — 24 September 2026

The five-contact connector at the right end is **J1**, not J2 in the KiCad schematic and board. J2 is the tip solder pad. This review checked the current 35 × 12 × 1.6 mm routed PCB in KiCad, including the footprints, actual pad positions, board edge and DRC. The board passed with zero violations, zero unconnected items and zero schematic-parity issues. No electrical layout, footprint, mounting-hole or thickness change was made: the available ATLAS head CAD does not yet define the clamp, cover, mating-plug opening or wire path.

| Interface | Decision and measured PCB facts | Required head-level provision |
|---|---|---|
| J2 tip | Retain the 1 × 2 mm no-paste SMD solder land at (84.0, 95.0). It is large enough to hand-solder a short fine enamelled scanner lead, while keeping the high-impedance input close to U1. It is not a socket or a structural anchor. | Fix the wire mechanically to the stationary head/cover near the PCB, with a compliant loop to the moving scanner. Keep adhesive and solder flux off the exposed guard and clean/inspect the input region after hand soldering. Do not let the moving scanner load the pad. |
| J1 five-way link | JST `SM05B-GHS-TB` is the **selected** ATLAS harness architecture. The mounted footprint spans about 10.75 mm across the 12 mm board and reaches x = 117.175 mm, only 0.325 mm inside the x = 117.5 mm right edge. The connector is 4.25 mm high. Its shrouded plug and cable leave the right board edge, so the footprint fitting on the PCB does not prove assembly clearance. | Make a dimensioned head-cover cutout and mated-plug/cable model. Reserve finger/tool access for unlatching, a cable bend, and a fixed harness anchor so insertion and cable force do not act on the SMD joints. Verify mating-face pin numbering and the J1.1 output/J1.2 sense pair in the actual harness. |
| Board retention | Keep the hole-free 35 × 12 mm outline provisionally. OpenSTM's actual PreAmp Gerber and native PCB show two 1.6 mm plated **GND-net** holes with 2.8 mm copper pads, spaced 5 mm apart, on its 24.5 × 8.5 mm board. This corrects the earlier inference that OpenSTM lacked preamp PCB holes. The board data does not label their mechanical purpose; check the head drawing before treating them as screw holes. | Define an ATLAS support/clamp or a hole pattern from the actual head CAD. Metal fasteners through grounded holes could bond the currently separate GNDA and CHASSIS nets, so do not copy OpenSTM's plated holes blindly. Verify 1.6 mm ATLAS PCB thickness against the head slot; OpenSTM's preamp is 1 mm thick. |
| Shield/guard | Keep J3 `CHASSIS` separate from `GNDA`. The front GNDA guard is intentionally exposed and approaches the left edge. | The conductive cover and any clamp must not touch the exposed guard or GNDA pads unless the system grounding plan intentionally bonds them. Use an insulating liner/standoffs and verify tip and moving-scanner clearance with the cover installed. |

The comparison is based on the [OpenSTM build paper](https://arxiv.org/pdf/2310.05413), the [OpenSTM native EasyEDA project](https://github.com/Dimsmary/OpenSTM/blob/main/PCB/ProProject_%E6%89%AB%E6%8F%8F%E9%9A%A7%E9%81%93%E6%98%BE%E5%BE%AE%E9%95%9COpenSTM_2023-09-09.epro), the [PreAmp Gerbers](https://github.com/Dimsmary/OpenSTM/blob/main/PCB/Gerber/Gerber_PreAmp_2023-08-25.zip), and the [JST GH manufacturer information](https://www.jst-mfg.com/product/index.php?lang=2&series=105). OpenSTM's FPC is a short internal head link; `ScannerConnector` has coaxial power and output connections to the remote electronics. The ATLAS circuit and connector wiring differ from OpenSTM, so the board is **inspired by** that head arrangement, not a drop-in mechanical replacement.

Before ordering the PCB, make a 3D head assembly with the exact J1 header, mating GHR-05V-S plug, wire bundle, fixed strain relief, J2 lead loop, cover, insulating support, and scanner travel. Measure the assembled feedback capacitance and noise because the exposed guard, pad, tip lead and cover are not captured by the LTspice circuit model.
