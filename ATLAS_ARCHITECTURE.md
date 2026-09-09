# ATLAS architecture and board design plan

Revision: 9 September 2026
Status: approved architecture direction and prototype design plan; not a fabrication-ready schematic or a claim of measured performance.

This document supersedes the previous architecture plan. It covers all three custom boards, their interfaces, component requirements, implementation order and validation. The first custom board to design is the TIA, followed by the converter/driver board and PSU. PCB assembly will use an assembly service. Component quantities below are planning allocations; the released schematic determines the final purchasing BOM.

## 1. Objective and fixed design choices

Build an ambient scanning tunnelling microscope that produces repeatable HOPG lattice images, using OpenSTM's compact head and piezo stick-slip approach, with FPGA acquisition and feedback.

The planning budget is approximately **£1,500 including a newly purchased FPGA board**, excluding the computer, labour and general workshop/test equipment. No FPGA is assumed already owned. UHV, cryogenics, spectroscopy and high-voltage scanner amplifiers are outside this first build.

| Function | Selected architecture |
|---|---|
| Head current amplifier | OPA828IDR, fixed 100 MΩ feedback |
| Current ADC | ADS8685, with downstream ×1/×10 gain and filtering |
| Fine Z conversion | One AD5791, B grade |
| Other analog commands | One AD5676, B grade, TSSOP, external reference |
| Scanner | Quartered PUI AB1290B; analog quadrant mixing |
| Coarse approach | OpenSTM piezo slider; conservative step/search first |
| Controller | Arty S7-25, to purchase; Verilog real-time controller |
| Scanner ranges | Fixed analog full-scale spans; software-variable field, centre and speed |
| Power | External isolated UK 230 V, 50 Hz linear supply |
| Custom board count | Three: TIA, converter/driver and PSU |
| Assembly | Factory-assembled SMD boards; connector/mechanical finishing as needed |

Existing KiCad project files are starting files, not evidence of a completed circuit. The older README narrative is historical and is not the component specification.

## 2. Physical partition and interfaces

| Assembly | Contents | Placement |
|---|---|---|
| Board 1: TIA | Current amplifier, feedback network, output isolation, supply filtering and decoupling | Immediately beside the tip, inside a conductive cover |
| Board 2: converter/driver | Current receiver, gain/filtering, ADC, DACs, references, axis mixing, bias, stack driver and hardware fault handling | Away from the head, close to the FPGA |
| Board 3: PSU | Isolated-secondary rectification, smoothing, regulation, distribution and rail monitoring | External enclosure with the transformer and enclosed mains connections |
| Arty S7-25 | Timing, feedback, approach, raster and host communication | Beside the converter board |

Functional loop:

**Junction current → TIA → receiver/gain/filter → ADS8685 → FPGA PI → AD5791 Z → quadrant mixer/drivers → scanner → junction.**

The AD5676 supplies lateral offsets/raster, sample bias and the coarse-stack waveform. DAC outputs never directly drive piezo loads.

### Inter-board electrical contracts

These are signal allocations, not numbered connector pinouts. Freeze connector orientation, pin numbering, cable construction and mating parts before PCB routing.

| Connection | Signals and requirements |
|---|---|
| TIA to converter | TIA_OUT and TIA_SENSE_0V as a signal pair; +15 V, -15 V and a separate power-return conductor |
| PSU to converter | +15 V analog, -15 V analog, nominal +7.5 V auxiliary, return conductors and supply-valid indication |
| Converter to FPGA | 3.3 V-compatible SPI/control, converter reset/update signals, arm/enable, heartbeat and fault/status |
| Converter to scanner | Four quadrant outputs and brass-electrode return |
| Converter to sample | Filtered sample bias and defined return arrangement |
| Converter to stack | Separate drive/return connection, routed away from current sensing |
| FPGA to host | USB-UART commands, data, configuration and status |

TIA_SENSE_0V connects to local TIA analog ground but feeds a high-impedance differential receiver at the converter. It must not become the normal return for amplifier supply current. Route stack current through a separate supply-return branch. Keep reference voltages local to the converter PCB.

For the first build, the Arty uses its normal USB power connection. The custom PSU is not sized to power the FPGA board. Account explicitly for the resulting USB-ground connection when defining the system's signal-to-chassis bond.

## 3. Board 1: TIA

### 3.1 Reference circuit and transfer function

OpenSTM's inspected EasyEDA source specifies OPA627AU, a 100 MΩ feedback resistor, 5 pF parallel compensation and a 220 Ω output resistor. The project also provides a preamplifier BOM and Gerbers. ATLAS retains the basic transimpedance topology while changing the amplifier and evaluating compensation.

Reference source snapshot: commit `f418005b7db2896f61c39863710af142641fe801`, including the PreAmp sheet in the [OpenSTM EasyEDA project](https://github.com/Dimsmary/OpenSTM/tree/f418005b7db2896f61c39863710af142641fe801/PCB). The [earlier preamplifier design notes](https://github.com/Dimsmary/OpenSTM/blob/f418005b7db2896f61c39863710af142641fe801/Docs_V2.0%28old%29/1-1-PreampDesign.md) explain the basic current-injection test.

Ground the non-inverting input. Connect the tip to the inverting input and return feedback from the amplifier output before the output isolation resistor.

For positive current defined as flowing into the input:

**VOUT = -ITIP × 100 MΩ.**

| Injected current | Ideal TIA output |
|---:|---:|
| 100 pA | -10 mV |
| 1 nA | -100 mV |
| 10 nA | -1 V |

### 3.2 Component requirements

| Item | Quantity | Prototype specification |
|---|---:|---|
| Amplifier | 1 | OPA828IDR, SOIC-8 |
| Feedback resistor | 1 | 100 MΩ high-value SMD resistor; prefer 1% where practical; specify temperature/voltage coefficients and measure excess noise |
| Feedback capacitor | 1 footprint | C0G/NP0; evaluate 0.2, 0.5, 1 and 5 pF using interchangeable parts |
| Output resistor | 1 | 220 Ω, 1%, outside the feedback loop |
| Supply-filter resistors | 2 | 10 Ω initial value, one per rail |
| Local bypass capacitors | 2 | 100 nF, 50 V, one per rail, close to the amplifier |
| Bulk capacitors | 2 | 10 µF, at least 35 V, one per rail; verify effective capacitance and leakage |
| Tip input | 1 | Small direct solder/contact connection |
| Power/signal connector | 1 | Five signal positions as allocated in Section 2, plus shield provision |
| Test points | As needed | Output and rails; no large test pad on the current input |
| Conductive cover and attachment | 1 set | Fit the head geometry and preserve tip clearance |

Do not substitute an arbitrary high-value resistor merely because its resistance matches. Record the exact part, tolerance, noise information and fitted footprint in the released BOM. Assembly-service availability and the input-capacitance budget jointly determine the resistor package.

### 3.3 Compensation, noise and heat

Start simulation with 0.5 pF feedback capacitance. With 100 MΩ, its RC pole is approximately 3.18 kHz; 5 pF gives approximately 318 Hz. Include feedback-resistor capacitance, pads, input capacitance and the tip connection. A capacitor marking alone does not establish actual bandwidth.

Select the prototype population through simulation, then confirm by measurement. Use a single compact compensation footprint rather than a bank of long selectable feedback branches. No gain switch or leaky protection device belongs on the sensitive input.

OPA828 has 45 MHz gain-bandwidth and approximately 5.5 mA typical quiescent current. At ±15 V, calculated unloaded dissipation is 165 mW. OPA140 remains a lower-power fallback if measured head heating matters and its bandwidth is adequate. [OPA828 datasheet](https://www.ti.com/lit/ds/symlink/opa828.pdf), [OPA140 datasheet](https://www.ti.com/lit/ds/symlink/opa140.pdf).

A 100 MΩ resistor contributes approximately 12.9 fA/√Hz Johnson-current noise at 300 K. Include amplifier voltage noise acting through input capacitance, resistor excess noise, pickup and downstream electronics in the complete budget. This theoretical resistor value is not a measured instrument noise floor.

### 3.4 Layout and acceptance

Keep the input and feedback loop short. Guard the input near its virtual-ground potential, and clear copper beneath the high-impedance node where needed to control capacitance. Keep power/output routing away from it. Specify cleaning, drying and inspection after assembly.

Test gain and polarity with a characterised injection resistor at 100 pA, 1 nA and 10 nA in both directions. Measure bandwidth, peaking, noise spectrum, integrated noise in a stated bandwidth, overload recovery, cable-load sensitivity and warm-up drift. Do not short the input to ground when claiming the open-input current-noise performance.

Deliverables: KiCad schematic and PCB, simulation and assumptions, BOM, assembly/position files, fabrication files, connector definition and a bench-test record.

## 4. Board 2: converter and driver

### 4.1 Functional zones and supplies

Partition the board into current acquisition, Z/reference circuitry, lateral/bias generation, quadrant outputs, stack drive and digital entry/fault logic.

Use continuous ground planes with deliberate return-current routing. Place digital interfaces at an edge. Keep stack-drive heat and current loops away from the ADC/reference zones; make the stack output independently disconnectable.

Receive ±15 V for analog stages and nominal +7.5 V auxiliary. Generate local +5 V analog and +3.3 V logic using separate TPS7A4901 regulators. Budget the total auxiliary load within the PSU allowance. The 7.5 V feed provides useful dropout/PSRR headroom for the 5 V regulator; do not assume its advertised rejection under inadequate headroom. [TPS7A49 datasheet](https://www.ti.com/lit/ds/symlink/tps7a49.pdf).

Feed REF5050 from a filtered rail with sufficient input headroom, such as the auxiliary rail. Do not attempt to obtain a regulated 5 V reference from a 5 V supply. Feed REF5025 from the clean 5 V rail.

### 4.2 Main component allocation

| Item | Planning quantity | Function / release check |
|---|---:|---|
| ADS8685 | 1 | Current acquisition; prefer TSSOP for inspection |
| AD5791, B grade | 1 | Dedicated 20-bit Z DAC |
| AD5676, B grade, TSSOP | 1 | Eight-channel command DAC with external reference |
| REF5050 | 1 | 5 V source for the Z reference circuit |
| REF5025 | 1 | 2.5 V reference for AD5676 and bipolar mappings |
| AD8676 | 2 dual packages | Generate ±10 V references and provide separate force-sense reference buffers |
| AD8675 | 1 | AD5791 output buffer |
| OPA4192 | 4 quad packages | Current receiver/gain/filter, lateral mappings, axis summing, midpoint/bias generation and four quadrant outputs |
| OPA2192 | 1 dual package | Final bias buffer and retract-command buffer |
| ADG1419 | 3 initially | Downstream current gain, bias range and Z-command override |
| Additional startup/stack-inhibit switching | As required by the completed circuit | Hold defined outputs during startup and faults; select ratings against actual signals |
| OPA551 | 1 evaluation candidate | Stack power amplifier; not approved for ordering until load/edge checks pass |
| TPS7A4901 | 2 | Local 5 V and 3.3 V regulation |
| Precision matched resistor networks | Per completed schematic | Receiver CMRR, Z reference/scaling, bipolar mappings and quadrant ratios |
| C0G/film filter capacitors | Per completed filters | Signal/reference paths, chosen for leakage and stability |
| Supply bypass/bulk capacitors | Per IC and load zone | Follow individual datasheets; budget effective capacitance |
| Hardware current-window detection | 1 circuit | Independent detection at a buffered current-signal node |
| Independent watchdog and rail-valid logic | 1 circuit | Remove arm/override Z when timing or power validity fails |
| Interface resistors, pull resistors and connectors | Per pin allocation | Defined inactive states and controlled digital edges |

This is a design BOM, not a parts order. Part grades, packages, assembly stock, matched networks, switch population and every passive value must be resolved in the schematic/BOM release.

The four OPA4192 packages allocate 16 amplifier channels: three for current receiver/gain/filter; four for X/Y coarse/fine mappings; two for X/Y sums; one for the 1.25 V midpoint; one for wide bias generation; four for quadrants; one spare. The OPA2192 supplies bias output and fault-retract buffering. Terminate the spare amplifier in a stable defined configuration. The Z/reference amplifiers and stack power stage are separate.

The OPAx192 family is the starting precision-amplifier choice; capacitive-load claims do not qualify the actual piezos and cables. [OPAx192 datasheet](https://www.ti.com/lit/ds/symlink/opa4192.pdf).

### 4.3 Current receiver, gain and ADC

Use a unity-gain differential receiver for TIA_OUT minus TIA_SENSE_0V, with a matched resistor network. Its input impedance must be high enough to keep loading through the TIA's 220 Ω output resistor small; account for remaining attenuation in gain calibration. Begin receiver-network design around 100 kΩ, then verify noise, CMRR and amplifier input/common-mode behaviour.

Follow it with a non-inverting stage selectable between ×1 and ×10. A starting arrangement uses a permanent 90 kΩ feedback resistor and a 10 kΩ gain leg whose lower end switches between ground (×10) and the stage output (×1). This preserves feedback during switching. Include switch on-resistance in calibration.

Use an ADG1419 on this buffered voltage path. Its digital control is compatible with 3.3 V logic when supplied appropriately for the analog signals. [ADG1419 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ADG1419.pdf).

Add a two-pole low-pass filter, initially designed around 10 kHz with a well-damped response. Verify ADC input-drive requirements, settling and the complete transfer function. This filter precedes 100 ksample/s acquisition; a separate digital anti-alias filter is required before reducing the sample rate for feedback.

Use ADS8685's internal 4.096 V reference and its required reference-pin capacitors. Do not connect REF5050 to its reference input. Initial imaging range is ±2.56 V. [ADS8685 datasheet](https://www.ti.com/lit/ds/symlink/ads8685.pdf).

| Downstream gain | Nominal current span at ±2.56 V ADC input | Calculated current increment |
|---|---:|---:|
| ×1 | ±25.6 nA | 781.25 fA/code |
| ×10 | ±2.56 nA | 78.125 fA/code |

These figures ignore receiver loading and calibration errors and are quantisation increments, not effective resolution. Select wider ADC spans when needed for diagnosis. Mark samples invalid during configuration changes and settling.

### 4.4 Z conversion and reference circuit

Use AD5791 at a native ±10 V span. A REF5050 source, filtering, one AD8676 for reference generation, a second AD8676 for force-sense buffers, and an AD8675 output buffer follow the structure of ADI's CN0191. Use precision low-drift resistor ratios in reference generation. [CN0191 circuit](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0191.html).

Scale the buffered output by 0.5 to produce the nominal ±5 V Z command. Include divider loading and downstream mixer impedance in the ratio; avoid treating an unloaded divider calculation as the final circuit. Place the hardware Z override before a shared bounded-slew conditioning stage so both normal and retract commands have controlled transitions.

At this 10 V command span, 20-bit code spacing is 9.54 µV. At the same span, 16 bits gives 152.59 µV, a factor of 16 larger. The AD5791 is selected for continuous fine Z travel without coarse/fine range transfers during feedback. AD5764 could also feed an analog mixer; analog mixing and DAC bit depth are separate choices. Evaluate noise at the quadrant outputs, including reference, buffer, resistor and driver contributions. [AD5791 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/AD5791.pdf), [AD5764 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/AD5764.pdf).

### 4.5 Lateral commands and quadrant outputs

Run AD5676 from 5 V with a 2.5 V external reference and gain-one native outputs. Derive a buffered 1.25 V midpoint from that reference. For native DAC voltage D, use the following nominal mappings:

| Channel | Mapping | Function |
|---|---|---|
| A | 6.4 × (D - 1.25 V) | X offset, ±8 V |
| B | 6.4 × (D - 1.25 V) | Y offset, ±8 V |
| C | 0.2 × (D - 1.25 V) | X fine raster, ±0.25 V |
| D | 0.2 × (D - 1.25 V) | Y fine raster, ±0.25 V |
| E | 8 × (D - 1.25 V), followed by range selection | Sample bias |
| F | Load-specific mapping to validated stack limits | Coarse waveform |
| G, H | Defined static codes | Unconnected spares |

Here D is a voltage variable, independent of the channel letter. Implement the affine mappings with appropriate differential/summing networks; in particular, attenuation below unity cannot be obtained from a simple non-inverting gain stage.

Use independent filtering by function. Strongly filter lateral offsets and hold them unchanged throughout each frame. Keep fine raster and stack paths out of the slow offset filters. Select TSSOP midscale reset and load all channels to known codes before arming. [AD5676 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/AD5676.pdf).

Form X = Xoffset + Xfine and Y = Yoffset + Yfine, then:

**V1 = Z + X; V2 = Z - X; V3 = Z + Y; V4 = Z - Y.**

Ground the buzzer brass electrode through its intended return. The four output stages must meet measured capacitive-load requirements. Allocate series isolation/compensation footprints per electrode; choose populated values from loop/load testing.

Software must enforce **|Z| + max(|X|, |Y|) ≤ 10 V**, with additional operating margin. Reject commands that would clip. The advertised maximum ranges are not simultaneously available.

The fine X/Y increment is 7.63 µV/code. Physical travel follows measured sensitivity; 100 nm/V is an illustration, not a scanner specification. Scan width, centre and speed remain programmable within fixed analog spans. Smaller code excursions do not create smaller voltage increments.

### 4.6 Sample bias

Generate a nominal ±10 V wide command. Derive the imaging range using a precision 50:1 attenuation network, select wide or attenuated voltage with an ADG1419, and buffer/filter the selected output. Nominal imaging span is ±200 mV.

Include switch leakage, on-resistance, divider loading, buffer offset and output filtering in calibration. Keep the switch on low-impedance circuitry. Add the required startup clamp/inhibit so range-control or supply transitions cannot apply an uncontrolled sample voltage.

Change bias range only after retracting, mark data invalid through settling, then reacquire with fine Z. Keep the coarse stack still unless the sample is outside fine-Z travel. Initial imaging settings are around 50–100 mV and 0.5–1 nA; the wide range is a development capability, not the default approach voltage.

### 4.7 Stack driver

The paper's AL1.65 × 1.65 × 5D-4F is the actuator; BSP715 is the slide. Obtain the actuator specification and measure capacitance before finalising voltage range, amplifier and pulse shape.

Evaluate OPA551 as a unity-gain-stable power-amplifier candidate. It is a 200 mA-class device, but available current, thermal limits, output swing and stability depend on conditions. Its inclusion does not approve an arbitrary stack waveform. [OPA55x datasheet](https://www.ti.com/lit/ds/symlink/opa551.pdf).

Calculate required peak current from **I = C × dV/dt**, then test both sourcing and sinking into a representative load. For illustration, 100 nF moved through 10 V in 10 µs requires approximately 100 mA.

Select the waveform within the actual stack's voltage and reverse-voltage limits, amplifier capability and PSU average-current budget. If the candidate cannot meet the required edge, revise the driver before PCB release; do not silently slow the edge and assume stick-slip behaviour is preserved. Include current limiting, damping/compensation, local energy storage and a defined hold command.

### 4.8 Startup, fault handling and digital interface

Use separate chip selects and suitable update/reset signals for the ADC and DACs. Keep outputs inhibited until supplies, references, converter configuration and all actuator codes are valid. Review every device's serial timing, logic rails and power-up sequence.

| State | Required analog behaviour |
|---|---|
| Power-up / FPGA unconfigured | Defined startup commands; stack stepping inhibited; no uncontrolled bias |
| Initialisation | Read back available configuration; establish range and motion polarity; wait for settling |
| Armed imaging | Normal Z control; fixed lateral offsets; stack held static |
| Range change | Retract, switch, wait, invalidate transient samples, then reacquire |
| Watchdog / overcurrent | Override Z with the verified retract command; inhibit stack activity and further raster updates |
| Rail loss | Assert fault early enough for tested withdrawal where energy remains; block re-arming until reinitialised |
| Complete power loss | No claim of active retraction; characterise final discharge behaviour |

Use an independent watchdog and hardware current-window detection at a buffered signal node. Translate comparator inputs/outputs correctly for their supply and FPGA logic domains. Do not connect a negative analog signal or a comparator output referenced to a negative rail directly to 3.3 V logic.

ADG1419 Z override selects a buffered, hardware-configured retract command when not armed. Define power-on logic with pull resistors. The actual retract sign, magnitude and slew follow measured scanner direction/travel. Fault action must preserve lateral commands where valid while withdrawing Z; resetting every DAC immediately is not a substitute for withdrawal.

### 4.9 Converter-board tests and outputs

- Verify all local rails, reference levels and startup sequences before enabling outputs.
- Test receiver CMRR/loading, both gains, ADC ranges, polarity, settling and calibration.
- Sweep DAC endpoints and midscale; verify Z scaling, coarse/fine mappings and bias ranges.
- Measure static output noise and step settling at references, command nodes and quadrant outputs.
- Check cross-coupling while changing lateral codes, operating digital interfaces and exercising the stack driver.
- Test each output against measured or representative cable/piezo capacitance, including overload and short recovery.
- Scope startup, reset, configuration loss, gain/range changes, watchdog, overcurrent and rail dropout at every actuator output.
- Confirm that inhibited/invalid data are flagged and clipped rasters are rejected.

Deliverables: zoned schematic, amplifier-channel allocation, noise/latency/current budgets, complete BOM, PCB/assembly/fabrication outputs, FPGA pin allocation, register configuration list, calibration procedure and bench results.

## 5. Board 3: PSU

### 5.1 Power architecture and design envelope

Use **230 V, 50 Hz mains → isolating transformer → secondary bridge/reservoirs → linear regulators → distribution**. UK supply voltage is nominally 230 V; a 100 V-only transformer is unsuitable. Keep mains enclosed, fused and appropriately earthed. The custom PCB contains isolated-secondary circuitry. [UK supply characteristics](https://library.ukpowernetworks.co.uk/library/en/Connectionsquotations/worksinformation/4.2-supply-characteristics-LVmetered-unmetered-customers/).

| Output | Initial continuous design allowance | Loads |
|---|---:|---|
| +15 V | 200 mA aggregate | TIA, analog amplifiers/references and average stack-driver demand |
| -15 V | 200 mA aggregate | TIA, analog amplifiers/references and stack-driver return/sink demand |
| Nominal +7.5 V | 100 mA aggregate | Converter-board local 5 V and 3.3 V regulators, reference/monitoring loads |

These are design targets requiring thermal/load validation, not completed supply ratings. Include regulator programming currents and monitor circuitry in the internal load budget. Account separately for stack peak current and duty cycle. Arty USB power is outside these allocations.

Use a provisional 30 VA transformer with two 18 V secondaries, wired in series with the correct phase. The winding junction forms secondary 0 V; the outer ends feed the bridge AC terminals. Reservoir capacitors connect from each bridge DC rail to secondary 0 V. Verify this complete split-supply topology, winding phase, current imbalance and polarity in the schematic.

Derive the auxiliary output from the positive raw reservoir through its own LM317. This avoids needing an additional transformer winding for the modest converter load, at the cost of explicitly budgeted regulator heat. The auxiliary load adds to positive winding/rectifier demand.

### 5.2 Component requirements

| Item | Planning quantity | Prototype specification / constraint |
|---|---:|---|
| Isolating transformer, off PCB | 1 | UK 230 V, 50 Hz primary; provisional 2 × 18 V, 30 VA; finalise from load, regulation and thermal calculations |
| Main bridge rectifier | 1 | At least 2 A and 200 V class; qualify surge current, dissipation and chosen split-supply wiring |
| Raw reservoir capacitors | 2 | 4700 µF, 50 V, 105°C initial choice; verify ripple-current rating and service life |
| LM317 | 2 | +15 V and nominal +7.5 V regulators, heatsink-compatible packages |
| LM337 | 1 | -15 V regulator, heatsink-compatible package |
| Output-to-adjust resistors | 3 | 110 Ω, 0.1%, initial design to provide minimum-load margin |
| Adjust-to-ground networks | 3 | Nominal 1.21 kΩ for ±15 V; 549 Ω for approximately +7.5 V; include reference/adjust-current tolerances |
| Regulator input bypass capacitors | At least 3 | 100 nF, 50 V close to regulator inputs; add bulk where wiring/loop length requires it |
| Regulator output capacitors | At least 3 | Start with 10 µF electrolytic plus suitable local bypass; verify each regulator's stability requirements |
| Adjustment bypass capacitors | Up to 3 | 10 µF initial value; datasheet-compatible polarity, voltage rating and discharge protection |
| Protection diodes | Budget 6 footprints | Output/input and adjustment discharge paths where required; orientations differ for positive and negative regulators |
| Reservoir bleeders | 2 | 10 kΩ, 0.5 W initial value; calculate actual decay and account for loading |
| Heatsinks / insulating hardware | 3 sets or validated shared assembly | Size for worst-case enclosure temperature and regulator power |
| Rail-valid monitor | 1 circuit | Scaled ±15 V and auxiliary supervision; defined inactive/fault state |
| Secondary protection | Per winding/branch design | Fuse/current ratings based on transformer and wiring |
| Secondary input connector | 1 | Separate, labelled winding inputs and centre connection |
| Output distribution connectors | As allocated | Keyed outputs, current-rated contacts and separate sensitive/stack returns |
| Bench-input selection | 1 arrangement | Mutually exclusive normal/bench feeds; no backfeeding |
| Mains inlet, fuse, switch, PE hardware and enclosure | 1 set, off PCB | Transformer/inrush appropriate; enclosed mains terminations |

Use exact datasheet pinouts: LM317 and LM337 are not interchangeable pin-for-pin. Their tabs can sit at different electrical potentials, so a shared conductive heatsink requires correctly specified isolation.

The LM317/LM337 setting relation includes reference tolerance and adjustment current; the nominal resistor arithmetic is not a precision rail calibration. The proposed 110 Ω programming resistor gives more minimum-load margin than copying a generic divider without checking load. Follow manufacturer capacitor and protection-diode guidance. [LM317 datasheet](https://www.ti.com/lit/ds/symlink/lm317.pdf), [LM337 datasheet](https://www.ti.com/lit/ds/symlink/lm337.pdf).

### 5.3 Ripple, dropout and thermal calculations

Calculate each rail's minimum reservoir trough from mains variation, transformer load regulation, rectifier conduction drop and ripple. Calculate maximum raw voltage at high line and light load, including transformer regulation. Retain the proposed secondary/capacitor ratings only if both cases pass.

For a first approximation at 50 Hz mains:

**ΔV ≈ I / (100 × C)** for full-wave reservoir ripple.

At 0.30 A positive-rail draw and 4700 µF, the estimated ripple is approximately 0.64 V before adding programming/monitoring loads. Transformer RMS current is higher than average DC load with capacitor-input rectification; do not select VA from regulated output watts alone.

Regulator dissipation is approximately **(VRAW - VOUT) × I** for a positive rail, with the corresponding magnitude expression for the negative rail. As an illustrative nominal case at 25 V raw, +15 V at 0.20 A dissipates about 2 W, and +7.5 V at 0.10 A about 1.75 W. High-line dissipation will be greater. Include the negative regulator, bridge, bleeders and transformer losses.

Use the actual package thermal resistances, interface materials, heatsinks and enclosure temperature. Prefer a fanless supply enclosure located away from the head; do not rely on the regulator's headline current rating without thermal derating.

Check local converter LDO headroom at the lowest auxiliary voltage and highest wiring drop. Any final output capacitors must satisfy stability and discharge conditions during asymmetric supply loss.

### 5.4 Distribution, grounding and startup

Keep bridge-to-reservoir charging loops short and separate from regulated-output returns. Use the reservoir midpoint as the secondary reference/distribution origin, with deliberately routed branches.

Provide separate branches for sensitive analog/TIA loads and the stack stage. The grounds remain electrically related; the objective is to keep charging and actuator currents out of sensitive reference paths. Keep chassis/protective earth bonding explicit and never remove PE to diagnose a ground loop.

Provide a rail-valid signal with a defined failure state if the PSU or monitor loses power. Account for monitor thresholds, hysteresis and propagation time, converter reset limits and available stored energy before promising retract-on-dropout behaviour.

Default to inhibited actuators until the converter completes initialisation. A supply-valid signal alone does not establish valid DAC codes or references. Scope actual rail sequencing and output transients under startup, shutdown and loss of one rail.

### 5.5 Development input

Use a removable harness or selector that disconnects the normal supply before connecting a bench source. Supply +15 V, 0 V, -15 V and the auxiliary feed as required by the completed system. A single 0–30 V bench channel is not automatically a split supply.

Route bench power through the same intended downstream distribution and local decoupling. Prevent current flowing into inactive regulators or the alternate source. Document the bench supply's permitted series/grounding arrangement and its relationship to USB and oscilloscope ground.

### 5.6 PSU tests and outputs

- Check transformer secondary phase, bridge wiring, capacitor polarity and regulator/tab pinouts before power.
- Test no-load operation and each output individually, then combined loads up to the design envelope.
- Include asymmetric loading and stack-like load pulses; measure ripple and transients at the PSU and at the converter connector.
- Verify dropout margin, maximum capacitor/device voltage, thermal equilibrium and shutdown/recovery.
- Measure reservoir discharge; bleeders do not imply immediate discharge.
- Test rail-valid timing, one-rail loss, normal/bench selection and reverse-current paths.
- Compare TIA and quadrant noise with the dedicated supply and a suitable bench reference.
- Record measured output ratings, limits and temperatures before connecting the microscope.

Deliverables: power-tree and load budget, secondary-side schematic, transformer/rectifier/reservoir calculations, thermal design, PCB and assembly files, off-board wiring diagram, connector/polarity labels and loaded test results.

## 6. Head mechanics and environmental stability

Retain the quartered AB1290B, short ceramic/sapphire-insulated tip mount, cut 0.25 mm Pt–Ir tip and HOPG sample. Measure actual X/Y/Z sensitivity, usable travel and mounted resonance; the bare-disc resonance is not the assembled scanner bandwidth. [PUI AB1290B](https://puiaudio.com/product/benders/ab1290b).

Retain OpenSTM's slide/stack/magnet arrangement. Obtain the exact actuator limits and matching mechanical dimensions before ordering substitutes. The [OpenSTM paper](https://arxiv.org/pdf/2310.05413) demonstrates feasibility, not a guaranteed approach time or frame rate for ATLAS.

| Coarse mechanism consideration | Selected piezo slider | Screw/lever fallback |
|---|---|---|
| Head reuse | Preserves OpenSTM's compact arrangement | Requires mechanical redesign |
| Heat | No motor winding; dynamic piezo/driver losses still exist | Motor should be de-energised during imaging; thermal settling still required |
| Motion | Depends on waveform, friction, load and contacts | Depends on pitch, reduction, backlash and elastic compliance |
| Qualification | Measure missed steps, peak excursion and stationary drift | Measure backlash, compliance and motion on power removal |

Start with retract–step–settle–fine-search. Near the sample, target worst-case forward excursion below one quarter of usable fine-Z search travel. Test repeated tunnelling acquisition and post-step settling. Switch to the screw fallback only if the slider cannot meet motion/holding requirements after reasonable waveform/contact correction or cannot be sourced within budget. Failure of the proximity proxy alone calls for slower search.

Use a damped suspension, flexible restrained cables, conductive head cover and an acoustic/draft enclosure. Measure suspension and head modes. Keep transformer fields, FPGA activity and heat away from the head, and correlate Z drift with time and recent actuator activity.

## 7. FPGA, host and data

Purchase Arty S7-25 and synthesise the timing/feedback core before committing its final pin allocation. Use Verilog, on-chip FIFOs and line buffers first. Its 80 DSP slices and 202.5 KB block RAM provide a starting resource envelope, not a proof of fit. USB-UART is the initial host link. [Arty S7 reference manual](https://digilent.com/reference/_media/reference/programmable-logic/arty-s7/arty-s7_rm.pdf).

Initial rates are 100 ksample/s ADC acquisition and 10 kHz PI updates. Design filtering/decimation to prevent aliasing, account for total delay, and tune the physical loop against the measured analog and mechanical response. These rates do not imply 10 kHz mechanical feedback bandwidth.

Implement fixed-point linear-current PI with saturation and anti-windup. Verify numeric widths and overflow behaviour. Add logarithmic error only after defining current sign, zero and saturation handling. Do not add derivative action by default.

Approach states: initialise, retract, bounded coarse step, settle, fine search, capture, stabilise/image and fault/retract. Initialise the integrator for a continuous transfer into feedback. Final acquisition requires valid correctly signed tunnelling current, not a motion-induced spike. Proximity-based acceleration is a later calibrated option.

Support constant-current imaging and explicitly labelled slow-feedback current imaging. Begin around 5–10 nm fields and 256 × 256 samples after calibration; keep dimensions, direction and dwell configurable.

The host sets parameters, displays data and stores records; it does not schedule feedback iterations. Define framed commands/data with integrity and sequence checking. Budget link throughput before fixing continuous record rates. Use finite full-rate diagnostic captures when continuous streaming would exceed the link. Mark overruns and never silently discard data.

Store acquired current, Z/DAC codes, timing, bias/range, gain, filters, PI settings, scan direction/dwell, approach history, calibration version and validity/fault flags. Preserve unprocessed acquired records and the exact acquisition/filter settings; save processed images as derivatives.

## 8. Implementation order and release gates

1. **TIA electrical design:** schematic, selected packages, current/noise model, input-capacitance sweep, compensation comparison and connector contract.
2. **TIA prototype:** factory assembly, cleaning and complete bench characterisation.
3. **Mechanical/stack qualification:** verify actual parts and load; measure motion and waveform requirements before driver/machining release.
4. **Converter electrical design:** implement the channel allocation, reference circuits, mappings, gain/bias switching, digital interfaces and hardware fault paths. Complete noise, latency and current budgets.
5. **PSU electrical design:** use the converter/stack load budget to finalise transformer, reservoir, regulator, monitoring and heatsink choices.
6. **Converter/PSU prototypes:** bench loads and simulated current first; validate startup and faults before actuator connection.
7. **FPGA integration:** test simulated inputs, PI limits, dropped data, communication stalls, watchdog, saturation and exhausted travel; then close the physical loop conservatively.
8. **Junction and imaging:** demonstrate repeated acquisition/withdrawal, stable holding, larger features and then repeatable lattice contrast.

Each board release requires an electrical-rule check, footprint/pinout review, board-rule check, complete exact-part BOM, assembly/position-file review and a defined bench procedure. Keep assembly variants and fitted calibration values traceable.

Compensation, stack-drive voltage/current/edges, output-load stability, calibrated scanner gains, independent fault action and PSU thermal/dropout limits are required engineering checks before their respective release. Their successful measurement is not assumed by this document.

## 9. Imaging success criteria

Require repeatable real-space HOPG lattice contrast across separate frames, directions and speeds. Inspect forward/reverse scans, current error and saturation flags. Use spatial analysis to support, rather than create, the observed periodicity.

For a triangular lattice with a = 0.246 nm, the first reciprocal shell is 2/(sqrt(3) × a), approximately 4.69 cycles/nm. Check both lattice vectors. Preserve original images and document detrending/windowing; selecting a few FFT peaks is not proof of atomic imaging. [Gwyddion lattice measurement](https://gwyddion.net/documentation/user-guide-en/feature-measurement.html).

Calibrate and verify on separate data. If HOPG is used to set the scale, agreement on the same corrected frame is not independent validation. Explicitly label affine correction. Moiré patterns and Au(111) reconstruction are optional later targets, not prerequisites. [Gwyddion distortion correction](https://gwyddion.net/documentation/user-guide-en/edit-extended.html).

## 10. Budget and procurement

| Category | Planning allowance |
|---|---:|
| Arty S7-25 and cable | £120 |
| Analog electronics, references, drivers, PCBs and assembly | £500 |
| Head machining, slide, stack, magnets and mounting parts | £300 |
| PSU and distribution | £150 |
| Isolation, shielding and enclosure | £150 |
| HOPG, Pt–Ir and consumables | £100 |
| Shipping, revisions and contingency | £180 |
| **Total** | **£1,500** |

These are allocations, not current quotations. Count retained purchases at their purchase cost. Obtain landed quotations including assembly setup, extended/consigned parts, tax and shipping before ordering. The £500 electronics allowance includes the AD5791 support circuit and all three-board assembly costs other than PSU components assigned to its own row; do not double-count or omit setup costs.

The hardware allocation is £1,320 before contingency. Preserve the revision reserve. If quotations exceed the budget, revisit sourcing, assembly and machining first; a coarse/fine 16-bit Z design is a possible separately agreed cost revision, not the selected architecture.

The next concrete milestone is a tested TIA, followed by converter and PSU prototypes that satisfy the interfaces and release gates above.
