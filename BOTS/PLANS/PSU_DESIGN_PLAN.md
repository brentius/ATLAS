# ATLAS PSU: schematic design and wiring plan

Revision: 29 September 2026 (provisional C1/C2 prototype population)

Status: a populated PSU schematic now exists in `pcb/atlas_psu/atlas_psu.kicad_sch`; this plan began as the earlier component-selection and wiring proposal and has not been fully reconciled with that live file. C1/C2 are currently 4700 µF Nichicon `LGY1H472MELB30`, matching the existing PCB population. The calculations below are preliminary and no loaded simulation, thermal test or assembly release is claimed. The 29 September reservoir analysis is in [`sim/atlas_psu/RESERVOIR_BUDGET.md`](../../sim/atlas_psu/RESERVOIR_BUDGET.md). KiCad 10.0.6 ERC found one documented CHASSIS warning and no errors; the unfinished PCB DRC still has an invalid outline and many unrouted items. This expands [Section 5 of the ATLAS architecture](ATLAS_ARCHITECTURE.md#5-board-3-psu), following the format of the [TIA design plan](TIA_DESIGN_PLAN.md).

## 1. Starting point and notation

Build the isolated-secondary part of a linear supply: two series-connected 18 V AC windings feed a bridge and split reservoirs; two LM317s generate +15 V and nominal +7.5 V, and an LM337 generates -15 V. A removable four-wire harness selects the normal supply or a bench supply. Distribution and the proposed undervoltage monitor are downstream of that selection, so they operate in either mode.

| Output | External continuous load allowance | Intended load |
|---|---:|---|
| +15 V | 200 mA aggregate | TIA, converter analog circuitry and average stack-driver demand |
| -15 V | 200 mA aggregate | Negative analog supply and stack-driver demand |
| Nominal +7.5 V | 100 mA aggregate | Converter local 5 V and 3.3 V regulators |

These allowances are shared between connectors, not available separately at every socket. Add the PSU's divider and monitor currents when sizing the transformer and regulators. The Arty remains USB-powered. Stack peak current, duty cycle, regenerated energy and the converter's finished load budget still determine the final rating.

**`U2.3` means pin 3 of U2.** A *net* is one electrically connected group of wires and pins. Rotation does not change pin numbers. `K` is a diode cathode and `A` is its anode. For the selected KiCad diode symbol, **pin 1 is K and pin 2 is A**. For `Device:C_Polarized`, **pin 1 is positive and pin 2 is negative**.

Your registered custom library, `atlas_parts_lib`, contains only `OPA828IDR`; it contains no PSU regulator, bridge or supervisor. All symbols proposed here already exist in your installed KiCad 10 libraries. Their exact identifiers and the footprint files below were checked locally. An existing footprint is a candidate land pattern, not proof that every manufacturer's similarly named package fits it.

The normal source uses `RAW_P`, `RAW_N` and `PSU_0V`. The selected output uses `SYS_P15`, `SYS_N15`, `SYS_AUX` and `SYS_0V`. Keep these distinct: the removable harness, not an identically named power symbol, must make the normal-to-system connection. Use ordinary attached net labels for these names.

## 2. Which library items are needed

The references below are allocations for the future drawing. Values such as `10u` and `1k21` are KiCad entry notation. Imperial package sizes are used throughout.

### 2.1 Power conversion and protection

| Reference | Purpose and value | Installed KiCad symbol | Proposed installed footprint |
|---|---|---|---|
| D10 | Bridge; Vishay `GBU4M-E3/51`, 4 A, 1000 V | `Diode_Bridge:GBU4M` | `Diode_THT:Diode_Bridge_Vishay_GBU` |
| U1, U3 | Positive regulators; HTC `LM317T` | `Regulator_Linear:LM317_TO-220` | `Package_TO_SOT_THT:TO-220-3_Vertical` |
| U2 | Negative regulator; onsemi `LM337T` | `Regulator_Linear:LM337_TO220` | `Package_TO_SOT_THT:TO-220-3_Vertical` |
| C1, C2 | Provisional raw reservoirs; `4700u`, 50 V, 105°C | `Device:C_Polarized` | `Capacitor_THT:CP_Radial_D30.0mm_P10.00mm_SnapIn` |
| C3, C5 | Positive-regulator input bypass; `100n`, 50 V, X7R | `Device:C` | `Capacitor_SMD:C_0603_1608Metric` |
| C4 | Negative-regulator input bypass; `10u`, 50 V, aluminum | `Device:C_Polarized` | `Capacitor_SMD:CP_Elec_6.3x5.4_Nichicon` |
| C6, C8 | Positive and auxiliary output capacitors; `10u`, 50 V | `Device:C_Polarized` | `Capacitor_SMD:CP_Elec_6.3x5.4_Nichicon` |
| C7 | Negative output capacitor; `47u`, 50 V, conventional wet aluminum | `Device:C_Polarized` | `Capacitor_SMD:CP_Elec_6.3x7.7` |
| C9, C10, C11 | Adjustment bypass; `10u`, 50 V | `Device:C_Polarized` | `Capacitor_SMD:CP_Elec_6.3x5.4_Nichicon` |
| C12, C13 | Positive and auxiliary output HF bypass; `100n`, 50 V, X7R | `Device:C` | `Capacitor_SMD:C_0603_1608Metric` |
| R1, R3, R5 | Output-to-adjust programming resistors; `110`, 0.1% | `Device:R` | `Resistor_SMD:R_0603_1608Metric` |
| R2, R4 | Adjust-to-return resistors; `1k21`, 0.1%, **0.25 W** | `Device:R` | `Resistor_SMD:R_0805_2012Metric` |
| R6 | Auxiliary adjust-to-return resistor; `549`, 0.1%, 0.125 W | `Device:R` | `Resistor_SMD:R_0805_2012Metric` |
| R7, R8 | Raw-rail bleeders; `10k`, 0.5 W | `Device:R` | `Resistor_SMD:R_2010_5025Metric` |
| D1–D6 | Regulator discharge protection; `M7`, 1 A silicon | `Device:D` | `Diode_SMD:D_SMA` |
| D7–D9 | Output reverse-polarity clamps; `M7` | `Device:D` | `Diode_SMD:D_SMA` |

**Do not accidentally select the LM317L or LM337L 100 mA versions.** Note the different spelling of the installed full-current symbols: `LM317_TO-220` includes a hyphen; `LM337_TO220` does not.

C4 follows the selected onsemi LM337's 10 µF aluminum input-bypass recommendation. C7 increases the architecture's 10 µF output starting allowance to 47 µF conventional aluminum. The manufacturer warns that reduced ESR can cause oscillation: assess the actual capacitor impedance over temperature, and do not substitute ceramic or polymer on capacitance alone. Do not add a ceramic directly across C7 by default. Include downstream capacitors and cable impedance in stability testing. [onsemi LM337, application information](https://www.onsemi.com/pdf/datasheet/lm337-d.pdf)

R2 and R4 each dissipate about **0.16 W**. Ordinary 0.125 W 0805 resistors are unsuitable even though the value and footprint match. The specific 0.25 W Panasonic part below provides initial margin; apply its temperature derating. R1/R3/R5 dissipate about 14 mW, and R6 about 72 mW.

### 2.2 Rail monitor and interfaces

The proposed monitor uses one TL431 and one optocoupler per rail. Each detector is powered by the rail it measures; the negative detector is referenced to `SYS_N15`. The three optocoupler outputs form a series permission path. This gives a practical undervoltage indication without connecting a negative-voltage signal to FPGA logic. It is a proposed circuit requiring threshold and timing qualification, not an overvoltage disconnect or a complete actuator safety controller.

| Reference | Purpose and value | Installed KiCad symbol | Proposed installed footprint |
|---|---|---|---|
| U4, U5, U6 | Positive, negative and auxiliary detectors; `TL431BIDBZR` | `Reference_Voltage:TL431DBZ` | `Package_TO_SOT_SMD:SOT-23` |
| U7, U8, U9 | Detector output coupling; `LTV-817S-TA1-D` | `Isolator:LTV-817S` | `Package_DIP:SMDIP-4_W9.53mm` |
| R9, R11 | ±15 V detector upper dividers; `45k3`, 0.1% | `Device:R` | `Resistor_SMD:R_0603_1608Metric` |
| R10, R12, R14 | Detector lower dividers; `10k`, 1% | `Device:R` | `Resistor_SMD:R_0603_1608Metric` |
| R13 | Auxiliary upper divider; `16k2`, 1% | `Device:R` | `Resistor_SMD:R_0603_1608Metric` |
| R15, R16 | ±15 V optocoupler LED resistors; `1k8`, 1%, 0.25 W | `Device:R` | `Resistor_SMD:R_1206_3216Metric` |
| R17 | Auxiliary LED resistor; `470`, 1%, 0.25 W | `Device:R` | `Resistor_SMD:R_1206_3216Metric` |
| R18 | PSU_VALID default-low resistor; `10k`, 1% | `Device:R` | `Resistor_SMD:R_0603_1608Metric` |
| R19 | Logic permission-feed resistor; `100`, 1% | `Device:R` | `Resistor_SMD:R_0603_1608Metric` |
| J1 | Four secondary wires; `SECONDARY_AC` | `Connector_Generic:Conn_01x04` | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal` |
| J2 | Normal regulated source; `NORMAL_SOURCE` | `Connector_Generic:Conn_01x04` | `Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical` |
| J3 | Selected supply input; `SYSTEM_FEED` | `Connector_Generic:Conn_01x04` | Same four-way JST XH footprint as J2 |
| J4 | Converter analog/TIA branch; `ANALOG_POWER` | `Connector_Generic:Conn_01x04` | Same four-way JST XH footprint as J2 |
| J5 | Separate stack-driver supply branch; `STACK_POWER` | `Connector_Generic:Conn_01x03` | `Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical` |
| J6 | Logic-side supply-valid interface; `PSU_STATUS` | `Connector_Generic:Conn_01x03` | `Connector_JST:JST_GH_SM03B-GHS-TB_1x03-1MP_P1.25mm_Horizontal` |
| J7 | Chassis/shield lead; `CHASSIS_CONTACT` | `Connector_Generic:Conn_01x01` | `Connector_Wire:SolderWirePad_1x01_SMD_1.5x3mm` |
| TP1–TP10 | Named test access, assigned below | `Connector:TestPoint` | `TestPoint:TestPoint_Pad_D1.0mm` |
| Power declarations | ERC declarations where needed | `power:PWR_FLAG` | None |

J7 and TP1–TP10 are PCB copper features: no purchased component and no assembly placement. The monitor's optocouplers do not make the entire PSU-to-converter connection galvanically isolated; its power returns still join the system. Their purpose here is level translation and a default-low permission path.

### 2.3 Exact parts and JLCPCB cross-reference

Catalogue checked on 11 September 2026 using public JLCPCB pages and indexed listings. **Listed** means the exact manufacturer/MPN/package has a catalogue match; it does not mean stock or a quoted assembly route has been secured. Stock observations can be cached and must be refreshed at order time. No parts have been purchased or reserved. Where stock was not exposed, the table says so rather than treating it as zero.

| References | Manufacturer and exact candidate MPN | JLCPCB catalogue | Sourcing or qualification status |
|---|---|---|---|
| U1, U3 | HTC Korea `LM317T` | [C39583120](https://jlcpcb.com/partdetail/HTC_Korea_TAEJINTech-LM317T/C39583120) | Extended; listing showed 9; TO-220, wave-solder route listed |
| U2 | onsemi `LM337T` | [C5345](https://jlcpcb.com/partdetail/onsemi-LM337T/C5345) | Extended; listing showed 0; procure/consign or review an exact replacement before release |
| D10 | Vishay `GBU4M-E3/51` | [C3008977](https://jlcpcb.com/partdetail/VishayIntertech-GBU4M_E351/C3008977) | Extended; GBU, wave solder; stock not exposed |
| C1, C2 | Nichicon `LGY1H472MELB30` | [C1582310](https://jlcpcb.com/partdetail/Nichicon-LGY1H472MELB30/C1582310) | Provisional prototype population matching the existing PCB footprint: 4700 µF, ±20%, 50 V, 30 × 30 mm, 10 mm pitch. The [Nichicon datasheet](https://www.nichicon.com/getmedia/6716b3c6-abcc-4da1-80b0-b33e29e5a195/e-lgy-DB.pdf) gives 2.1 A RMS at 105°C/120 Hz and 0.88 frequency factor at 50 Hz. Confirm assembly allocation, capacitor RMS current, inrush and discharge. The former Ymin 2200 µF option remains an unqualified comparison, not a drop-in for this footprint. |
| C3, C5, C12, C13 | Samsung `CL10B104KB8NNNC` | [C1591](https://jlcpcb.com/partdetail/CL10B104KB8NNNC/C1591) | Extended in inspected listing; stock shown; 100 nF, 50 V, X7R, 0603 |
| C4, C6, C8–C11 | Nichicon `UWT1H100MCL1GB` | [C445064](https://jlcpcb.com/partdetail/Nichicon-UWT1H100MCL1GB/C445064) | Extended; listing showed 3705; 10 µF, 50 V, 6.3 × 5.4 mm |
| C7 | Nichicon `UWT1H470MCL1GS` | [C445060](https://jlcpcb.com/partdetail/Nichicon-UWT1H470MCL1GS/C445060) | Extended; 47 µF, 50 V, 6.3 × 7.7 mm; stock not exposed; stability qualification required |
| R1, R3, R5 | KOA `RN73R1JTTD1100B25` | [C2508454](https://jlcpcb.com/partdetail/KOA_SpeerElec-RN73R1JTTD1100B25/C2508454) | Extended; 110 Ω, 0.1%, 100 mW, 0603; stock not exposed |
| R2, R4 | Panasonic `ERA-6VEB1211V` | [C3986344](https://jlcpcb.com/partdetail/PANASONIC-ERA6VEB1211V/C3986344) | Extended; 1.21 kΩ, 0.1%, **250 mW**, 0805; stock not exposed |
| R6 | Panasonic `ERA-6AEB5490V` | [C2087831](https://jlcpcb.com/partdetail/PANASONIC-ERA6AEB5490V/C2087831) | Extended; listing showed 0; 549 Ω, 0.1%, 125 mW, 0805 |
| R7, R8 | Uniroyal `2010W2J0103T4S` | [C20349](https://jlcpcb.com/partdetail/21060-2010W2J0103T4S/C20349) | Extended; listing showed 0; 10 kΩ, 5%, 0.5 W, 2010 |
| D1–D9 | MDD `M7` | [C95872](https://jlcpcb.com/partdetail/MDD_Microdiode_Semiconductor-M7/C95872) | Basic; 1 A, 1000 V, SMA; stock not exposed in inspected page |
| U4–U6 | Texas Instruments `TL431BIDBZR` | [C41283](https://jlcpcb.com/partdetail/TexasInstruments-TL431BIDBZR/C41283) | Extended; B grade, SOT-23; stock not exposed |
| U7–U9 | Lite-On `LTV-817S-TA1-D` | [C114603](https://jlcpcb.com/partdetail/LiteOn-LTV_817S_TA1D/C114603) | Extended; listing showed 6490; match gull-wing dimensions and CTR ordering code |
| R9, R11 | Panasonic `ERA-3AEB4532V` | [C3951453](https://jlcpcb.com/partdetail/PANASONIC-ERA3AEB4532V/C3951453) | Extended; listing showed 0; 45.3 kΩ, 0.1%, 0603 |
| R10, R12, R14, R18 | Uniroyal `0603WAF1002T5E` | [C25804](https://jlcpcb.com/partdetail/26547-0603WAF1002T5E/C25804) | Basic; 10 kΩ, 1%, 0603; stock not exposed |
| R13 | RALEC `RTT031622FTP` | [C103329](https://jlcpcb.com/partdetail/RALEC-RTT031622FTP/C103329) | Extended; 16.2 kΩ, 1%, 0603; stock not exposed |
| R15, R16 | Vishay `CRCW12061K80FKEBC` | [C4211031](https://jlcpcb.com/partdetail/VishayIntertech-CRCW12061K80FKEBC/C4211031) | Extended; 1.8 kΩ, 1%, 250 mW, 1206; stock not exposed |
| R17 | LIZ `CR1206F44700G` | [C102199](https://jlcpcb.com/partdetail/LIZElec-CR1206F44700G/C102199) | Extended; 470 Ω, 1%, 250 mW, 1206; stock not exposed |
| R19 | Uniroyal `0603WAF1000T5E` | [C22775](https://jlcpcb.com/partdetail/0603WAF1000T5E/C22775) | Basic; 100 Ω, 1%, 0603; stock not exposed |
| J1 | Phoenix Contact `MKDS 1,5/4-5,08` | No exact JLCPCB match verified | External purchase/consignment candidate; freeze exact order code and mechanical drawing before footprint approval |
| J2–J4 | JST `B4B-XH-A` | [C41422491](https://jlcpcb.com/partdetail/JST-B4B_XHA/C41422491) | Extended; four-way 2.5 mm through-hole; stock not exposed |
| J5 | JST `B3B-XH-A(LF)(SN)` | [C144394](https://jlcpcb.com/partdetail/Jst_SalesAmerica-B3B_XH_A_LF_SN/C144394) | Extended; three-way 2.5 mm through-hole; refresh stock and assembly quote |
| J6 | JST `SM03B-GHS-TB(LF)(SN)` | [C514175](https://jlcpcb.com/partdetail/SM03B-GHS-TB%28LF%29%28SN%29/C514175) | Extended; listing showed 3259; three-way 1.25 mm SMD |

The above is an electrically motivated candidate BOM, not an optimised purchasing quote. Several extended precision resistors have unfavourable pre-order minimums. Consolidate their sourcing or qualify equivalents before ordering; do not relax the regulator-setting tolerance or the resistor wattage silently. Do not substitute a `JLCPCB Assembly` service-placeholder listing for a verified component MPN. JLCPCB supports different [parts-sourcing routes](https://jlcpcb.com/help/article/pcba-parts-sourcing-instruction); catalogue presence and LCSC stock alone do not secure an assembly allocation.

### 2.4 Off-board parts and finishing

| Item | Quantity and requirement | Connection or procurement note |
|---|---|---|
| T1 transformer | 1; candidate Vigortronix `VTX-146-030-218`, 30 VA, 2 × 18 V, 0.83 A windings | Off PCB; [manufacturer listing](https://www.vigortronix.com/product/dual-primary-toroidal-2-x-115v-230v/); no JLCPCB order code verified |
| Secondary fuses and holders | 2; one series fuse in each winding's outer lead | Select time-current curve and rating from 0.83 A winding rating, measured charging inrush and wire capacity; final MPN/rating unresolved |
| Heatsinks and insulation | 3 sets; preliminary individual sink target at most 10°C/W | Electrical isolation pads, shoulder washers and suitable hardware required; validate package/interface thermal data and enclosure fit |
| Normal-source harness | 1; two XHP-4 housings and eight compatible XH contacts | J2 to J3, numbered pin-for-pin; removable in full |
| Analog and stack harnesses | One four-wire and one three-wire branch | XHP-4 and XHP-3 mating housings; size contacts/wire for aggregate and peak currents |
| Status harness | 1; three wires, GH mating housing `GHR-03V-S` | Use `SSHL-002T-P0.2` contacts with compatible wire size |
| Bench harness | 1; four-wire XHP-4 connection to J3 | Replaces the normal harness; bench supply must provide actual split rails and auxiliary output |
| Mains/enclosure assembly | 1 set | Enclosed 230 V primary wiring, inlet, primary fuse, switch, strain relief, PE stud/bonds and transformer mounting; exact rated parts remain a separate enclosure specification |

For XH harnesses, choose contacts such as `SXH-001T-P0.6` only with a supported wire/insulation size and correct crimp tooling. XH and GH are different connector families, so the three-way status plug cannot mate with the three-way stack-power header. Number the mating contacts using the manufacturer's drawing, not their apparent left-to-right order. [JST XH](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf), [JST GH](https://www.jst-mfg.com/product/pdf/eng/eGH.pdf)

The primary side stays off the custom PCB. PE bonds to the metal enclosure through dedicated hardware; it is not carried through J7 or a signal-ground trace. The transformer primary connection and fuse specification must follow the selected transformer's instructions. A toroidal mounting bolt must not form a closed conductive turn through the centre and around the outside of the core.

## 3. Exactly what connects to what

### 3.1 Transformer secondary and bridge

Call the first secondary ends **A1/A2** and the second **B1/B2**. These are descriptive wire names, not claimed transformer colour codes. Choose winding phase so connecting A2 to B1 produces approximately 36 V AC between A1 and B2, with approximately 18 V AC from either outer end to the junction.

| Connection | Destination |
|---|---|
| T1 A1 | Through off-board secondary fuse FSEC1 to J1.1 |
| T1 A2 | J1.2 |
| T1 B1 | J1.3 |
| T1 B2 | Through off-board secondary fuse FSEC2 to J1.4 |
| J1.1 | `AC_A`: D10.2 |
| J1.2 and J1.3 | Join together as `PSU_0V`; reservoir midpoint |
| J1.4 | `AC_B`: D10.3 |
| D10.1, positive terminal | `RAW_P`: C1.1 and positive regulator inputs |
| D10.4, negative terminal | `RAW_N`: C2.2 and negative regulator input |

**D10 negative is RAW_N, not ground.** C1 goes between RAW_P and the centre junction; C2 goes between the junction and RAW_N. Neither reservoir sees the whole rail-to-rail voltage. The centre junction is an actual transformer connection, not an artificial midpoint made only by two capacitors.

The installed GBU4M symbol inherits its pin map from GBU4A: **1 = +, 2/3 = AC, 4 = -**. Match that to the actual body markings and footprint. With the opposite winding phases, the outer-to-outer voltage can be near zero; never infer series phase solely from wire position. [Vishay bridge drawing](https://www.vishay.com/docs/88614/gbu4a.pdf)

### 3.2 Regulator pin map

| Component | Pin 1 | Pin 2 | Pin 3 | Metal tab |
|---|---|---|---|---|
| U1 LM317T | `ADJ_P` | `REG_P15` output | `RAW_P` input | `REG_P15` |
| U2 LM337T | `ADJ_N` | `RAW_N` input | `REG_N15` output | `RAW_N` |
| U3 LM317T | `ADJ_AUX` | `REG_AUX` output | `RAW_P` input | `REG_AUX` |

These tab voltages differ. Bare tabs must not share a conductive heatsink or touch an earthed case. U3 takes power from **RAW_P**, not from U1's +15 V output. [HTC LM317 pin definitions](https://www.htckorea.co.kr/Datasheet/Voltage%20Regulator/LM317.pdf), [onsemi LM337 pin definitions](https://www.onsemi.com/pdf/datasheet/lm337-d.pdf)

### 3.3 Every power resistor and capacitor terminal

| Component | Pin 1 connects to | Pin 2 connects to |
|---|---|---|
| R1 110 Ω | `REG_P15` | `ADJ_P` |
| R2 1.21 kΩ | `ADJ_P` | `PSU_0V` |
| R3 110 Ω | `REG_N15` | `ADJ_N` |
| R4 1.21 kΩ | `ADJ_N` | `PSU_0V` |
| R5 110 Ω | `REG_AUX` | `ADJ_AUX` |
| R6 549 Ω | `ADJ_AUX` | `PSU_0V` |
| R7 10 kΩ | `RAW_P` | `PSU_0V` |
| R8 10 kΩ | `PSU_0V` | `RAW_N` |
| C1 4700 µF | `RAW_P` positive | `PSU_0V` negative |
| C2 4700 µF | `PSU_0V` positive | `RAW_N` negative |
| C3 100 nF | `RAW_P` | `PSU_0V` |
| C4 10 µF | `PSU_0V` positive | `RAW_N` negative |
| C5 100 nF | `RAW_P` | `PSU_0V` |
| C6 10 µF | `REG_P15` positive | `PSU_0V` negative |
| C7 47 µF | `PSU_0V` positive | `REG_N15` negative |
| C8 10 µF | `REG_AUX` positive | `PSU_0V` negative |
| C9 10 µF | `ADJ_P` positive | `PSU_0V` negative |
| C10 10 µF | `PSU_0V` positive | `ADJ_N` negative |
| C11 10 µF | `ADJ_AUX` positive | `PSU_0V` negative |
| C12 100 nF | `REG_P15` | `PSU_0V` |
| C13 100 nF | `REG_AUX` | `PSU_0V` |

C2, C4, C7 and C10 have their **positive** terminals connected to PSU_0V. The 100 nF ceramics are non-polar. Every capacitor is a shunt connection between the named nodes, not a series element in the supply conductor.

### 3.4 Protection diode orientation

| Diode | Pin 1 cathode K | Pin 2 anode A | Purpose |
|---|---|---|---|
| D1 | `RAW_P` | `REG_P15` | U1 output discharges towards its input |
| D2 | `REG_P15` | `ADJ_P` | U1 adjustment-capacitor discharge |
| D3 | `REG_N15` | `RAW_N` | U2 protection, reversed relative to positive circuit |
| D4 | `ADJ_N` | `REG_N15` | U2 adjustment-capacitor protection |
| D5 | `RAW_P` | `REG_AUX` | U3 output-to-input protection |
| D6 | `REG_AUX` | `ADJ_AUX` | U3 adjustment-capacitor protection |
| D7 | `REG_P15` | `PSU_0V` | Clamps a positive output driven below return |
| D8 | `PSU_0V` | `REG_N15` | Clamps a negative output driven above return |
| D9 | `REG_AUX` | `PSU_0V` | Clamps auxiliary output driven below return |

D1–D6 implement capacitor-discharge paths. D7–D9 add reverse-output clamps for asymmetric rail loss; they do not protect against an arbitrary sustained wrong-voltage source. None of these diodes blocks normal-to-bench backfeeding. Source separation is provided by the removable harness. Check diode pulse current against all connected downstream capacitance. [Positive-regulator protection guidance](https://www.ti.com/lit/ds/symlink/lm317.pdf), [negative-regulator protection guidance](https://www.onsemi.com/pdf/datasheet/lm337-d.pdf)

### 3.5 Source selection and power outputs

| Pin | J2 NORMAL_SOURCE | J3 SYSTEM_FEED | J4 ANALOG_POWER |
|---|---|---|---|
| 1 | `REG_P15` | `SYS_P15` | `SYS_P15` |
| 2 | `PSU_0V` | `SYS_0V` | `SYS_0V` |
| 3 | `REG_N15` | `SYS_N15` | `SYS_N15` |
| 4 | `REG_AUX` | `SYS_AUX` | `SYS_AUX` |

In normal mode, the removable cable connects **J2.1 → J3.1, J2.2 → J3.2, J2.3 → J3.3 and J2.4 → J3.4**. There must be no PCB wire, copper link, shared ground symbol or parallel cable joining the normal and selected nets. In bench mode, remove that cable and plug the bench harness into J3: +15 V, 0 V, -15 V and nominal +7.5 V on pins 1–4 respectively. Use one source plug at a time and change it only with sources disabled and outputs discharged. The unused J2 stays disconnected and protected from accidental contact.

J5 feeds the stack driver on the converter board: **pin 1 = SYS_P15, pin 2 = SYS_0V, pin 3 = SYS_N15**. It is not an actuator-output socket. J4 and J5 share their supply rails but require separate cable return conductors and separate branch routes from J3.2. The converter must preserve that separation until its defined return junction; otherwise an extra low-impedance return can defeat the intended current paths.

The TIA is powered through the converter's TIA link. Do not connect a four-way PSU power plug directly to its five-way signal/power connector. The TIA's ground-sense conductor remains a receiver reference, not a PSU return.

### 3.6 Rail-detector connections

For the selected `TL431DBZ` symbol and TI DBZ package, **pin 1 = cathode K, pin 2 = REF, pin 3 = anode A**. U4 detects the positive rail; U5 detects the negative rail magnitude; U6 detects the auxiliary rail. Do not exchange TL431 and TL432: their SOT-23 pin allocations differ. The operating principle follows TI's comparator application. [TI TL431 comparator application and pinout](https://www.ti.com/lit/ds/symlink/tl431.pdf)

| Component | Pin 1 | Pin 2 | Pin 3 | Pin 4 |
|---|---|---|---|---|
| U4 TL431 | `DET_P_K` | `DET_P_REF` | `SYS_0V` | — |
| U5 TL431 | `DET_N_K` | `DET_N_REF` | `SYS_N15` | — |
| U6 TL431 | `DET_A_K` | `DET_A_REF` | `SYS_0V` | — |
| U7 optocoupler | `LED_P_A` anode | `DET_P_K` cathode | `OK_LINK_1` emitter | `OK_FEED` collector |
| U8 optocoupler | `LED_N_A` anode | `DET_N_K` cathode | `OK_LINK_2` emitter | `OK_LINK_1` collector |
| U9 optocoupler | `LED_A_A` anode | `DET_A_K` cathode | `PSU_VALID` emitter | `OK_LINK_2` collector |

| Component | Pin 1 connects to | Pin 2 connects to |
|---|---|---|
| R9 45.3 kΩ | `SYS_P15` | `DET_P_REF` |
| R10 10 kΩ | `DET_P_REF` | `SYS_0V` |
| R11 45.3 kΩ | `SYS_0V` | `DET_N_REF` |
| R12 10 kΩ | `DET_N_REF` | `SYS_N15` |
| R13 16.2 kΩ | `SYS_AUX` | `DET_A_REF` |
| R14 10 kΩ | `DET_A_REF` | `SYS_0V` |
| R15 1.8 kΩ | `SYS_P15` | `LED_P_A` |
| R16 1.8 kΩ | `SYS_0V` | `LED_N_A` |
| R17 470 Ω | `SYS_AUX` | `LED_A_A` |
| R18 10 kΩ | `PSU_VALID` | `STATUS_0V` |
| R19 100 Ω | `STATUS_3V3` | `OK_FEED` |

The negative LED current path is **SYS_0V → R16 → U8 LED → U5 cathode/anode → SYS_N15**. Its detector divider is also between SYS_0V and SYS_N15. U5's anode must not be grounded. This entire input-side circuit floats with the negative rail; only U8's light crosses to the logic-side permission path.

The positive path is SYS_P15 → R15 → U7 LED → U4 → SYS_0V. The auxiliary path is SYS_AUX → R17 → U9 LED → U6 → SYS_0V. Leave TL431 cathode-to-anode capacitors out of this comparator proposal; arbitrary capacitance can affect its response/stability.

Nominal detector thresholds, before reference-input current, tolerances and optical transfer, are `2.495 × (1 + Rupper/Rlower)`: **13.80 V** for the two main rail magnitudes and **6.54 V** for auxiliary. These are starting design thresholds, not measured trip voltages. Include TL431 reference current, temperature, resistor ratio, LED current and optocoupler CTR in the final threshold bounds.

### 3.7 Status connector and startup behaviour

| J6 pin | Function | Connection |
|---|---|---|
| 1 | `STATUS_3V3` | Current-limited 3.3 V from the converter/controller logic domain; R19.1 |
| 2 | `PSU_VALID` | U9.3, R18.1 and TP10.1; high permits further checks |
| 3 | `STATUS_0V` | Receiver's logic return; R18.2 |

When all three optocoupler LEDs are adequately driven, their series phototransistors conduct from J6.1 through R19 to J6.2. Loss of any measured rail opens that path; R18 pulls J6.2 low. Also require a **47 kΩ pulldown at the receiving end**, so an unplugged cable leaves the receiver low. That receiver resistor is a converter-board requirement, not an additional fitted PSU reference.

Do not pull PSU_VALID up at the receiver or directly connect it to a negative-referenced detector. Do not tie STATUS_0V to SYS_0V on this PSU drawing; its system relationship is established at the converter. The isolated transistor chain needs no such local bond.

Use a 3.3 V Schmitt-input receiver and verify measured high/low margins with all three transistor saturation drops, cable load and temperature. At 3.3 V the 10 kΩ local and 47 kΩ remote pulldowns demand less than 0.4 mA. Detector LED currents are approximately 6 mA on each main rail and 8 mA on auxiliary, depending on TL431 cathode voltage and LED drop. The optocoupler's actual CTR bin, saturation voltage and turn-off delay must be checked; catalogue CTR headline values are not a worst-case timing guarantee.

There is no deliberate analog hysteresis in this starting monitor. The converter must require **100 ms continuously valid before considering arming**, latch any rail-loss fault, and require reinitialisation and an explicit re-arm after recovery. Capture a falling PSU_VALID immediately; the 100 ms qualification applies only to becoming valid. This prevents automatic re-arming during threshold chatter, but detector propagation delay still has to be measured. PSU_VALID alone never overrides watchdog, DAC-initialisation or actuator-inhibit conditions.

This monitor detects undervoltage, not excessive voltage. It also senses at the PSU distribution input, so broken downstream load wires need local converter supervision. Do not promise withdrawal on power failure until the complete detector, logic, DAC and actuator chain has demonstrated sufficient response time and stored energy.

### 3.8 Ground, chassis and test points

`PSU_0V` is the transformer/reservoir origin. `SYS_0V` is the selected source return. In normal mode the harness connects them; in bench mode it does not. Keep bridge charging returns, regulator programming returns and load branches deliberate even when the nets are electrically connected through the cable. A shared net name alone does not control current flow in the eventual copper.

J7.1 is `CHASSIS` only. Do not fit a PSU_0V-to-chassis, SYS_0V-to-chassis or STATUS_0V-to-chassis link by default. Resolve the single intentional signal-to-chassis bond with the converter, Arty USB ground and earthed instruments before system release. PE remains permanently connected to the enclosure independently of any signal-bond decision.

| Test point | Net and value |
|---|---|
| TP1 | `RAW_P` |
| TP2 | `RAW_N` |
| TP3 | `PSU_0V` |
| TP4 | `REG_P15` |
| TP5 | `REG_N15` |
| TP6 | `REG_AUX` |
| TP7 | `SYS_P15` |
| TP8 | `SYS_N15` |
| TP9 | `SYS_AUX` |
| TP10 | `PSU_VALID` |

Measure raw/regulator voltages against PSU_0V, selected rails against SYS_0V, and status against STATUS_0V. J3.2 and J6.3 provide the latter return contacts. In particular, an earth-referenced oscilloscope ground clip must not be attached to RAW_N or SYS_N15.

For the later schematic, add PWR_FLAG declarations to RAW_P and RAW_N because the passive bridge does not declare them driven, and to any supply/return nets that actually contain power-input pins without a power-output source. U1/U2/U3 declare their regulated outputs. External flags on SYS rails, if needed, represent the selected source, not a second regulator. Use [KiCad's power-flag rules](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#_power_pins_and_power_flags); do not use flags to conceal an actual missing wire.

### 3.9 Complete net checklist

The following table lists each allocated physical PCB pin exactly once. It excludes off-board transformer/fuses, the removable harness, mechanical tabs and nonphysical power declarations. In normal mode the four harness connections in Section 3.5 join the corresponding net pairs externally.

| Net | All connected PCB pins |
|---|---|
| `AC_A` | `D10.2`, `J1.1` |
| `AC_B` | `D10.3`, `J1.4` |
| `RAW_P` | `D10.1`, `U1.3`, `U3.3`, `R7.1`, `C1.1`, `C3.1`, `C5.1`, `D1.1`, `D5.1`, `TP1.1` |
| `RAW_N` | `D10.4`, `U2.2`, `R8.2`, `C2.2`, `C4.2`, `D3.2`, `TP2.1` |
| `PSU_0V` | `R2.2`, `R4.2`, `R6.2`, `R7.2`, `R8.1`, `C1.2`, `C2.1`, `C3.2`, `C4.1`, `C5.2`, `C6.2`, `C7.1`, `C8.2`, `C9.2`, `C10.1`, `C11.2`, `C12.2`, `C13.2`, `D7.2`, `D8.1`, `D9.2`, `J1.2`, `J1.3`, `J2.2`, `TP3.1` |
| `REG_P15` | `U1.2`, `R1.1`, `C6.1`, `C12.1`, `D1.2`, `D2.1`, `D7.1`, `J2.1`, `TP4.1` |
| `ADJ_P` | `U1.1`, `R1.2`, `R2.1`, `C9.1`, `D2.2` |
| `REG_N15` | `U2.3`, `R3.1`, `C7.2`, `D3.1`, `D4.2`, `D8.2`, `J2.3`, `TP5.1` |
| `ADJ_N` | `U2.1`, `R3.2`, `R4.1`, `C10.2`, `D4.1` |
| `REG_AUX` | `U3.2`, `R5.1`, `C8.1`, `C13.1`, `D5.2`, `D6.1`, `D9.1`, `J2.4`, `TP6.1` |
| `ADJ_AUX` | `U3.1`, `R5.2`, `R6.1`, `C11.1`, `D6.2` |
| `SYS_P15` | `R9.1`, `R15.1`, `J3.1`, `J4.1`, `J5.1`, `TP7.1` |
| `SYS_0V` | `R10.2`, `R11.1`, `R14.2`, `R16.1`, `U4.3`, `U6.3`, `J3.2`, `J4.2`, `J5.2` |
| `SYS_N15` | `R12.2`, `U5.3`, `J3.3`, `J4.3`, `J5.3`, `TP8.1` |
| `SYS_AUX` | `R13.1`, `R17.1`, `J3.4`, `J4.4`, `TP9.1` |
| `DET_P_REF` | `R9.2`, `R10.1`, `U4.2` |
| `DET_P_K` | `U4.1`, `U7.2` |
| `LED_P_A` | `R15.2`, `U7.1` |
| `DET_N_REF` | `R11.2`, `R12.1`, `U5.2` |
| `DET_N_K` | `U5.1`, `U8.2` |
| `LED_N_A` | `R16.2`, `U8.1` |
| `DET_A_REF` | `R13.2`, `R14.1`, `U6.2` |
| `DET_A_K` | `U6.1`, `U9.2` |
| `LED_A_A` | `R17.2`, `U9.1` |
| `STATUS_3V3` | `R19.1`, `J6.1` |
| `OK_FEED` | `R19.2`, `U7.4` |
| `OK_LINK_1` | `U7.3`, `U8.4` |
| `OK_LINK_2` | `U8.3`, `U9.4` |
| `PSU_VALID` | `R18.1`, `U9.3`, `J6.2`, `TP10.1` |
| `STATUS_0V` | `R18.2`, `J6.3` |
| `CHASSIS` | `J7.1` |

## 4. Suggested drawing order

1. Draw J1 and its explicit J1.2-to-J1.3 centre connection. Add D10, C1/C2 and R7/R8, checking reservoir polarity first.
2. Draw U1, R1/R2, C3/C6/C9/C12 and D1/D2/D7. Check its input, output and adjustment nets against the tables.
3. Draw U2 independently using its own pin map, then R3/R4, C4/C7/C10 and D3/D4/D8. Check every polarized part against the negative-rail table.
4. Draw U3 from RAW_P with R5/R6, C5/C8/C11/C13 and D5/D6/D9.
5. Add J2 and the separate J3/J4/J5 distribution section. Describe the external normal harness in ordinary text; do not short the source groups inside the PCB schematic.
6. Add U4–U9 and R9–R19 from the detector tables. Keep the negative detector's reference distinction visible.
7. Add J6, J7 and TP1–TP10. Include the receiver pulldown, delayed arming and separate-current-return notes as interface requirements.
8. Check the complete net table, pin numbers, exact MPNs, capacitor polarities and footprints, then run ERC on the future drawing. Record unresolved sourcing and mechanical choices explicitly.

These are instructions for a later schematic session. They specify electrical relationships; no component coordinates or physical placement are prescribed here.

## 5. Simulation and electrical acceptance

### 5.1 Programming current and nominal output

Use `VOUT ≈ VREF × (1 + Rlower/Rprogram) + IADJ × Rlower`, with the corresponding negative sign for U2. With VREF = 1.25 V and the HTC typical IADJ = 50 µA, U1 gives approximately **+15.061 V** and U3 **+7.516 V**. Using the onsemi typical IADJ = 65 µA gives U2 approximately **-15.079 V**. The names ±15 V and +7.5 V are nominal.

The programming current is about **11.36 mA per regulator**. Even 1.20 V across a +0.1% 110 Ω resistor gives about 10.90 mA, above the 10 mA maximum minimum-load requirement used for the selected LM317 family. Include the selected LM337's corresponding requirement too. Evaluate reference/adjust-current limits and line/load regulation for the exact manufacturers; 0.1% resistors do not make these precision voltage references. [HTC LM317 electrical limits](https://www.htckorea.co.kr/Datasheet/Voltage%20Regulator/LM317.pdf)

### 5.2 Transformer, ripple and dissipation

For this centre-tapped split supply, each rail charges through **one bridge diode** from the active half-winding. Each reservoir is replenished at 100 Hz on 50 Hz mains. Use a circuit model with winding resistance, actual phasing, diode conduction and unequal loads; a generic single-output bridge model does not reproduce the centre-tap currents.

For preliminary budgeting, allow about 0.218 A through each main regulator and 0.120 A through U3, including dividers and detectors. With raw bleeders, use approximately **0.34 A positive** and **0.22 A negative** reservoir draw. Refine these values at the actual output extremes.

| Calculation | Preliminary result or required condition |
|---|---|
| Ripple `I/(100C)`, nominal 4700 µF | About 0.72 Vpp positive and 0.47 Vpp negative |
| Ripple with -20% capacitor tolerance | About 0.90 Vpp positive and 0.59 Vpp negative |
| Low-line example, 18 V winding × 0.94, 1.1 V diode drop, minimum positive capacitance | About 21.9 V positive raw trough before additional wiring/sag allowance (about 3.8 V above a 15.1 V output plus 3 V dropout allowance) |
| Dropout acceptance | Raw trough exceeds worst-case regulated output by at least the exact regulator's required differential; start with a 3 V allowance and retain additional wiring margin |
| High-line example, +10% line and assumed +15% no-load winding rise | About 32.2 V peak before diode drop; use 33 V as a provisional raw-voltage ceiling for calculations |
| C1/C2 rating | 50 V across each individual capacitor; validate tolerance/transients below rating |
| U1/U2 dissipation at 33 V raw and 0.218 A | About 3.9 W each at nominal 15 V output |
| U3 dissipation at 33 V raw and 0.120 A | About 3.1 W at nominal 7.5 V output |

C1/C2 were temporarily proposed at 2200 µF on 24 September 2026 to reduce size, inrush and discharge time. The 29 September prototype population is 4700 µF to match the already placed PCB parts and recover provisional low-line pulse headroom. Stack-driver current pulses remain unmeasured; do not interpret the larger capacitors as release qualification. The selected 4700 µF part increases energy and bleeder time, requiring the revised schematic note and physical measurement.

**29 September reservoir-envelope correction:** the former 2200 µF
candidate's 2.3 V illustrative 0.5 A / 10 ms pulse drop used nominal
capacitance; at -20% tolerance it becomes 2.84 V. That gave only 18.06 V
raw trough in the 216.2 V low-line case. At 4700 µF and -20%, the same
idealized case gives 20.59 V raw trough, leaving 2.49 V beyond the
provisional 15.1 V + 3.0 V regulation threshold. The candidate transformer's
[manufacturer datasheet](https://www.vigortronix.com/wp-content/uploads/2021/09/VTX-146-xxxx-2-Series-Dual-Primary-Toroida-D0008.pdf)
specifies a 200–264 V input range and 14% **typical** regulation. If ATLAS
must operate at 200 V input, the simplified 4700 µF estimate gives
20.13 V without and 18.80 V with the pulse, leaving only 0.70 V idealized
headroom before winding/wiring losses. At 264 V and typical no-load
regulation, the ideal pre-diode peak is 33.31 V, so the provisional 33 V
raw ceiling is not a guaranteed maximum over that full transformer range.
These are conditional calculations, not new operating requirements or
component choices. The reproducible comparison and limitations are in
[`RESERVOIR_BUDGET.md`](../../sim/atlas_psu/RESERVOIR_BUDGET.md).

The +15% transformer regulation figure is an explicit calculation assumption, not a verified specification for T1. Recalculate using the supplier's guaranteed tolerances, actual loading and winding measurements. The low-line and high-line examples are design cases, not promised supply limits. Capacitor-input RMS winding current, bridge surge current and reservoir ripple current must be evaluated separately from average DC current; the provisional 30 VA size does not settle these checks.

For a 40°C internal ambient and an initial junction-temperature target below 110°C, a 3.9 W regulator needs total junction-to-ambient thermal resistance below about 18°C/W. The proposed 10°C/W individual heatsink allowance leaves the remainder for junction-to-case and the electrically insulating interface. Use each exact package's data and the heatsink's installed orientation/ventilation; a nominal sink rating in open air does not establish the enclosed result. Verify U3's safe operating area at its larger input-output differential and all three devices under short circuit.

At 33 V, each 10 kΩ bleeder dissipates about 0.109 W. With provisional 4700 µF C1/C2, its nominal reservoir time constant is 47 s; with only that resistor discharging, 33 V to 5 V takes about **89 s**. With +20% capacitance and +5% resistance it is about **112 s**. Other loads usually accelerate discharge, but measure both reservoirs and treat voltage as present until verified.

### 5.3 Required electrical checks

- Sweep no load, individual full loads and combined loads. External load targets exclude internal programming/monitor currents. Include one winding fuse open and strongly asymmetric rail loading.
- Include the selected wet-electrolytic capacitor impedance versus frequency/temperature, long output wiring and all converter capacitors. Check U2 carefully for oscillation and all rails for startup overshoot and load-step recovery.
- Sweep detector thresholds slowly in both directions, then drop each rail abruptly with the others present. Check nominal 13.80/6.54 V thresholds against the converter's minimum usable rails and worst-case regulator output. Measure optical delays and validate logic levels across temperature and component variation.
- Verify that no supply-valid pulse can arm actuators during startup, missing rails, disconnected J6, absent STATUS_3V3 or brownout. Confirm the receiver's local pulldown and latched re-arm behaviour.
- Test the normal/bench transition with sources disabled. Check electrical separation before applying bench power; no current may enter U1/U2/U3 from the bench connection.
- Exercise representative stack pulses and returned charge. LM317/LM337 are not general-purpose four-quadrant supplies; if regenerated energy raises a rail beyond its allowed envelope, add a separately designed sink/clamp before actuator connection.
- Measure raw ripple, regulated ripple and noise at the PSU and converter. Compare TIA output noise with a suitable bench reference; this plan does not establish an STM noise floor.
- Run to thermal equilibrium with the enclosure closed. Record load, ambient, case/sink temperature, estimated junction temperature, output voltage and shutdown/recovery behaviour.

## 6. Completion criteria and remaining decisions

The component and net allocations are sufficient to draw the proposed circuit without inventing connections. They are not fabrication approval. Before release, resolve the out-of-stock regulator/reservoir/precision-resistor sourcing, J1's exact order code, transformer regulation, fuse curves, heatsinks, mating harness orientation and system chassis bond. Obtain a mixed SMD/through-hole assembly quote; bridge, reservoirs, TO-220 parts and XH headers need the appropriate assembly process or agreed finishing.

Release also requires successful ERC and footprint/pinout review on the completed schematic; dropout, capacitor-stability and thermal acceptance; qualified rail-monitor thresholds/timing and receiver fault handling; and verification of normal/bench separation. Final PCB work later needs its own DRC, routing/current-path review and assembly-file checks.

All designations in this document belong to the PSU. U1 on the TIA board remains its OPA828 amplifier. No KiCad source or library file was changed to produce this plan.
