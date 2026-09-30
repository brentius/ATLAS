# ATLAS suspension frequency check — 30 September 2026

## Finding

The [README](../../README.md#damping) describes an eight-spring suspension
carrying a 12 lb granite slab and states a 1 Hz natural frequency. No spring
rate, total moving mass, geometry, damping measurement or free-decay record
is available in this repository. **The 1 Hz value is unverified here.**
This calculation does not select a spring or change the head design.

For an ideal vertical, linear, zero-preload spring set carrying only the
stated slab mass, a 1 Hz vertical mode requires **215 N/m combined tangent
stiffness**, or **26.9 N/m per spring** if eight springs share the load
equally. The corresponding static stretch from the unloaded length is
**248 mm**. A suspension with initial tension, preload, angled springs or
nonlinear stiffness can have a different unloaded-to-loaded stretch; its
frequency must be established from the loaded tangent stiffness or measured
motion. The clearance and available extension of the actual frame are not
documented.

## Inputs and equations

| Quantity | Value | Origin |
|---|---:|---|
| Granite slab | 12 lb = 5.4431 kg | README claim; mass not independently weighed |
| Spring count | 8 | README claim; geometry and load sharing unknown |
| Gravity | 9.80665 m/s² | Calculation convention |
| Target vertical frequency | 1 Hz | README claim; not a measured result in this repository |

For a single vertical degree of freedom with total moving mass `m` and
effective vertical tangent stiffness `k`, `f_n = sqrt(k/m)/(2π)`. Thus
`k = m(2πf_n)²`. For eight equal vertical springs in parallel,
`k_each = k/8`. If they are linear and have no preload, force balance gives
`Δ = mg/k = g/(2πf_n)²`. This idealized `Δ` is independent of mass at a
fixed target frequency, but required spring stiffness rises with mass.

| Target `f_n` | Total `k` for 5.4431 kg | Equal-spring `k_each` | Zero-preload static stretch |
|---:|---:|---:|---:|
| 1 Hz | 214.9 N/m | 26.9 N/m | 248.4 mm |
| 1.5 Hz | 483.5 N/m | 60.4 N/m | 110.4 mm |
| 2 Hz | 859.5 N/m | 107.4 N/m | 62.1 mm |
| 3 Hz | 1934.0 N/m | 241.7 N/m | 27.6 mm |

At 1 Hz with the slab alone, each equally loaded spring carries 6.67 N.
If the actual suspended head, fixtures and cables add 1.0 kg while the
combined stiffness stays 214.9 N/m, the ideal vertical frequency falls to
0.919 Hz. This is a sensitivity example, not an estimate of the head mass.
For an angled axial spring, its small-motion vertical contribution is
approximately `k_axial cos²θ`; load sharing and geometric stiffness need
the actual mounting coordinates and tension. Flexible cables may add both
stiffness and a direct disturbance path.

Isolation is frequency-dependent. In a simple base-excited, single-mode
model, displacement transmissibility is
`T = sqrt(1 + (2ζr)²) / sqrt((1-r²)² + (2ζr)²)`, where `r` is forcing
frequency divided by natural frequency and `ζ` is damping ratio. For an
*illustrative*, unmeasured `ζ = 0.10`, this model gives `T = 5.10` at
resonance, `0.356` at twice the natural frequency and `0.0589` at five
times it. A 1 Hz mode therefore does not imply immunity to wind, sound,
direct cable force, or excitation near 1 Hz. Damping, lateral/tilt modes
and acoustic coupling have not been measured.

## Physical check before treating 1 Hz as a design result

1. Weigh the entire moving assembly with its actual cables in place.
   Record slab, head, fixtures and any attached cable mass separately.
2. Record unloaded and loaded spring lengths, mount angles, vertical travel
   and minimum clearance to the frame. Check for coil bind and contact at
   both static position and expected motion extremes.
3. With the assembly safely restrained, add and remove a known small mass
   near its centre and measure the incremental vertical displacement. In a
   locally linear suspension, `k_eff = Δm g / Δx`. At the calculated 1 Hz
   slab-only stiffness, a 0.5 kg increment would move it about 22.8 mm;
   this is a predicted diagnostic scale, not a load instruction for an
   unverified frame. Repeat at several loads to reveal nonlinearity and
   unequal spring sharing.
4. Record at least three small-amplitude free decays of the fully assembled
   suspension. From successive peak times obtain the vertical period and
   frequency; from peak ratios estimate damping. Repeat with cables in
   their intended restrained configuration. Check lateral, pitch and roll
   modes separately, as one vertical number cannot qualify the head.
5. Record the measurement method, sensor calibration, load and cable state,
   amplitudes, uncertainty and raw time series. Compare the measured modes
   with disturbances at the bench and with the head's own mounted modes.

Do not use this model alone to release the suspension or assert imaging
stability. It only identifies the stiffness and travel scale that the
stated 1 Hz claim would require under explicit assumptions.
