"""Ideal single-mode spring/mass sizing for an ATLAS isolation trial.

All mass is the *total* moving assembly. Spring rate is effective vertical
stiffness at the loaded position, not necessarily a catalogue axial rate.
This does not model preload, geometry, damping, plate-stack modes or cables.
"""

from __future__ import annotations

import argparse
import math


G = 9.80665  # m/s^2


def positive(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("value must be finite and positive")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mass-kg", type=positive, required=True,
                        help="total moving mass, including slab, plates, head and fixtures")
    stiffness = parser.add_mutually_exclusive_group(required=True)
    stiffness.add_argument("--total-k-n-m", type=positive,
                           help="measured combined effective vertical stiffness")
    stiffness.add_argument("--spring-rate-n-m", type=positive,
                           help="effective vertical rate of one equal spring")
    parser.add_argument("--spring-count", type=int,
                        help="required with --spring-rate-n-m")
    parser.add_argument("--target-hz", type=positive,
                        help="optional vertical-frequency target for mass comparison")
    parser.add_argument("--pendulum-length-m", type=positive,
                        help="optional effective length for horizontal pendulum estimate")
    args = parser.parse_args()

    if args.spring_rate_n_m is not None:
        if args.spring_count is None or args.spring_count <= 0:
            parser.error("--spring-rate-n-m requires a positive --spring-count")
        total_k = args.spring_rate_n_m * args.spring_count
    else:
        if args.spring_count is not None:
            parser.error("--spring-count is only used with --spring-rate-n-m")
        total_k = args.total_k_n_m

    vertical_hz = math.sqrt(total_k / args.mass_kg) / (2 * math.pi)
    equivalent_deflection_m = args.mass_kg * G / total_k
    print(f"total moving mass: {args.mass_kg:.4f} kg")
    print(f"effective vertical stiffness: {total_k:.3f} N/m")
    print(f"ideal vertical frequency: {vertical_hz:.4f} Hz")
    print(f"mg/k: {equivalent_deflection_m * 1000:.1f} mm "
          "(unloaded-to-loaded stretch only for vertical, linear, zero-preload springs)")

    if args.target_hz is not None:
        target_mass = total_k / (2 * math.pi * args.target_hz) ** 2
        delta_mass = target_mass - args.mass_kg
        print(f"total mass for {args.target_hz:.3f} Hz at fixed stiffness: "
              f"{target_mass:.4f} kg ({delta_mass:+.4f} kg relative to input)")

    if args.pendulum_length_m is not None:
        horizontal_hz = math.sqrt(G / args.pendulum_length_m) / (2 * math.pi)
        print(f"ideal small-angle horizontal pendulum frequency: {horizontal_hz:.4f} Hz")


if __name__ == "__main__":
    main()
