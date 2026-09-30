# ATLAS isolation architecture comparison — 30 September 2026

## Recommendation for the next prototype

Use the existing spring-frame concept as a **modular test platform**, with
the total suspended mass adjustable. Compare (A) the bare suspended stage,
(B) the same stage with a conductive plate moving past frame-fixed magnets
for non-contact eddy-current damping, and (C) a short, two- or three-plate
metal/elastomer stack on the stage if the first two configurations leave
high-frequency coupling. This is a test sequence, **not** a selected slab
weight, spring, magnet gap or fabrication release. Keep the scanner, sample
and preamplifier on the same compact upper assembly; do not split the
tip/sample mechanical loop across stages. Fit, magnetic compatibility and
performance must be checked before adding a damper near the instrument.

Do not substitute passive permanent-magnet levitation for the springs at
this stage. The cited STM examples use magnets for **eddy-current damping**
of a mechanically supported mass, not as the vertical support. Static
permanent-magnet support of an ordinary ferromagnetic stage is not stable
in all directions without additional constraints or active control; a
levitation system would also introduce a new control/fault path. This is
an engineering recommendation based on the sources below, not a measured
comparison on ATLAS.

## Evidence from other STM builds

| Source and implementation | What it establishes | Limit for ATLAS |
|---|---|---|
| [OpenSTM build paper, section 5.1](https://arxiv.org/pdf/2310.05413) | Its reported build suspended a 10 kg stone from four springs, each listed at 408 N/m, and placed three 20 × 20 × 1 cm aluminium plates separated by fluoro-rubber rings on it. The paper says other isolation methods can be used. | It does not measure ATLAS's spring rate, mode frequencies or vibration transfer. Its four-spring value cannot be copied into an eight-spring design without recalculation. |
| [Dan Berard's build account](https://dberard.com/home-built-stm/vibration-isolation/) | Three long springs support an aluminium/MDF stage with a three-steel-plate Viton stack; fixed magnets near the moving aluminium plate provide eddy-current damping. The builder reports about 1 Hz **horizontal pendulum** and 2 Hz **vertical spring** resonances and uses fine 40 AWG wiring. | His 1 Hz number is not a vertical-spring specification and his site does not provide an ATLAS transfer measurement. |
| [J. Herkenhoff's STM repository](https://github.com/jherkenhoff/STM) | Uses steel plates separated by Viton pieces and describes optional spring/elastic-rope suspension and aluminium-base eddy-current damping. | Build description, not an ATLAS head/fixture qualification. |
| [Le's STM isolation thesis](https://digitalcommons.calpoly.edu/theses/2272/) | Develops a six-spring suspended copper stage with neodymium-magnet eddy-current damping and Viton at contacts. | Different geometry and environment; magnet position and damping remain to be engineered for ATLAS. |
| [Schmid and Varga, *Ultramicroscopy* (1992)](https://www.sciencedirect.com/science/article/pii/0304399192904934) | Their analysis finds spring/eddy-current and elastomer plate stages complementary. It also notes plate stacks can amplify some 10–100 Hz vibration and suggests only a few plates. | Do not add a plate stack on the assumption that more layers always improve isolation; compare transfer measurements. |
| [University of Virginia magnetic-levitation note](https://galileo.phys.virginia.edu/classes/317.gbh.fall05/mag-lev/mag-lev.html) | Explains why ordinary static permanent-magnet levitation is unstable without special materials or feedback. | Does not rule out every magnetic bearing, but does not justify a passive levitated ATLAS stage. |

The build accounts report their own configurations. They are not controlled
A/B measurements on one STM. In particular, OpenSTM's HOPG imaging is
evidence for its whole build, not proof that one isolation element alone
would outperform another element on ATLAS.

| ATLAS option | Main advantage | Main unresolved cost or failure mode | Trial role |
|---|---|---|---|
| Spring-supported mass alone | Reuses the present frame; mass and stiffness can be measured directly | Resonant amplification and cable bypass | Baseline first |
| Springs plus eddy-current plate/magnets | Adds adjustable non-contact damping without magnetic support | Magnetic interaction, extra moving mass and gap/clearance control | Reversible second configuration |
| Short metal/elastomer plate stack | Additional high-frequency attenuation may be possible | Creep, load/temperature dependence and possible 10–100 Hz amplification | Compare only if baseline/damper data justify it |
| Passive permanent-magnet levitation | Could remove a direct mechanical support path in a specialized design | Ordinary static magnets do not give stable unconstrained support; requires a different architecture | Not selected |
| Actively stabilized magnetic stage | Stability can be controlled in principle | Sensors, actuator power, control noise and fault behavior become part of the STM | Outside this prototype comparison |

## Mass and spring-rate implications

The [earlier suspension budget](SUSPENSION_BUDGET.md) correctly found that,
for **vertical, linear, zero-preload springs retuned to maintain exactly
1 Hz**, `mg/k = g/(2πf)² = 248 mm`, regardless of mass. The user's ability
to change slab mass matters when the **installed spring stiffness stays
fixed**: `f = sqrt(k/m)/(2π)` decreases and `mg/k` increases as mass is
added. Initial spring tension, angled mounts, geometric stiffness and
load-dependent rate invalidate the simple stretch interpretation; use the
loaded effective stiffness and measured free decay.

The following are **calculated illustrations**, assuming the OpenSTM
paper's 408 N/m rate for *each* spring, vertical equal load sharing, no
preload and no other moving mass. These are **not** ATLAS spring data.

| Example | Combined `k` | Moving mass | Ideal vertical `f` | `mg/k` |
|---|---:|---:|---:|---:|
| Four OpenSTM-rate springs, 12 lb slab | 1632 N/m | 5.443 kg | 2.76 Hz | 32.7 mm |
| Four OpenSTM-rate springs, 10 kg stone | 1632 N/m | 10.0 kg | 2.03 Hz | 60.1 mm |
| Eight OpenSTM-rate springs, 12 lb slab | 3264 N/m | 5.443 kg | 3.90 Hz | 16.4 mm |
| Eight OpenSTM-rate springs, 10 kg stone | 3264 N/m | 10.0 kg | 2.88 Hz | 30.0 mm |

At 3264 N/m, an eight-spring stage would need **20.67 kg total moving
mass** for an ideal 2 Hz vertical mode, before accounting for the head,
cables and elastomer compliance. That is not a recommended weight: frame
capacity, spring extension, handling and floor loading have not been
checked. Four 408 N/m springs with 10 kg alone yield 2.03 Hz; added
plates/head would lower that low-frequency estimate. Berard's reported
1 Hz horizontal pendulum and 2 Hz vertical mode are consistent with these
being distinct degrees of freedom, not interchangeable design targets.

Run `suspension_sizing.py` with the **measured total moving mass and
loaded effective spring rate** when available. Example (illustrative
OpenSTM-rate springs, not ATLAS measurements):

```text
python sim/atlas_mechanics/suspension_sizing.py --mass-kg 5.44310844 --spring-count 8 --spring-rate-n-m 408 --target-hz 2
```

The tool reports the frequency, `mg/k` and mass needed for the requested
target at fixed stiffness. It cannot choose a safe slab or predict damping.

## Reversible comparison and acceptance gate

1. Record actual frame geometry, support capacity, spring count, loaded
   tangent stiffness, clearance and total moving mass. Check all mounts,
   cables and possible bottoming before adding mass. Obtain vertical,
   lateral, pitch and roll free-decay records with the intended cable loom.
2. Establish a baseline with the existing slab and spring arrangement.
   Record simultaneous frame and stage motion during a quiet interval and
   a repeatable small excitation, with a dummy head in place of a live
   tip/sample. Resolve the vertical mode and transfer over at least
   0.5–100 Hz if the sensors permit; retain the raw traces, sensor
   calibration, locations, added sensor mass, sample rate and uncertainty.
   Repeat each configuration at least three times.
3. If resonance ring-down is excessive, test a detachable conductor plate
   on the moving stage and magnets fixed to the frame. Change only the
   magnet gap between runs. Compare magnets near/far at the same moving
   mass and cable routing; use nonmagnetic dummy ballast if removing the
   conductor otherwise changes mass. Keep mechanical clearance and check
   whether fields affect scanner magnets, approach mechanics or
   electronics. A magnet is not an acceptable mechanical stop or
   structural support.
4. If high-frequency transfer remains problematic, compare a two- or
   three-plate elastomer stack using the same head position and cables.
   Record pad geometry, compression, temperature and creep. Look for
   amplification in the 10–100 Hz band as well as attenuation.
5. Select the lowest-complexity configuration that measurably reduces
   tip–sample disturbance without unacceptable resonance, drift, cable
   coupling, clearance or approach-motion penalties. Repeat scans or
   tunnelling-current noise checks only after the mechanical comparison
   and electrical baseline exist. The pass criterion is a reproducible
   reduction in stage/frame transfer or junction-noise spectrum under
   matched conditions, with no new amplified band or clearance failure;
   numerical limits require the measured site and head noise budget.
   No imaging result is claimed here.

The next physical input is the **actual loaded spring rate and complete
moving mass**. Without those two values, changing slab weight is a tuning
experiment rather than a justified design selection.
