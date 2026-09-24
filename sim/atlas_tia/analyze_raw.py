"""Summarize LTspice complex AC raw files for the ATLAS TIA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def read_ac(path: Path) -> tuple[list[str], list[np.ndarray]]:
    payload = path.read_bytes()
    marker = "Binary:\n".encode("utf-16le")
    start = payload.find(marker)
    if start < 0:
        raise ValueError(f"No LTspice binary marker in {path}")
    header = payload[:start].decode("utf-16le")
    if "Plotname: AC Analysis" not in header or "Flags: complex" not in header:
        raise ValueError(f"Expected complex AC raw file: {path}")
    count = int(next(line.split(":", 1)[1] for line in header.splitlines()
                     if line.startswith("No. Variables:")))
    names = []
    in_variables = False
    for line in header.splitlines():
        if line == "Variables:":
            in_variables = True
            continue
        if in_variables and line.startswith("\t"):
            names.append(line.split("\t")[2].lower())
    if len(names) != count:
        raise ValueError(f"Expected {count} variables, found {names}")
    data = np.frombuffer(payload, dtype="<c16", offset=start + len(marker))
    if data.size % count:
        raise ValueError("Binary length is not a whole number of rows")
    data = data.reshape((-1, count))
    if data.shape[0] != int(next(line.split(":", 1)[1] for line in header.splitlines()
                                 if line.startswith("No. Points:"))):
        raise ValueError("Point count disagrees with header")
    cuts = np.flatnonzero(np.diff(data[:, 0].real) < 0) + 1
    return names, list(np.split(data, cuts))


def interpolate_crossing(freq: np.ndarray, values: np.ndarray, target: float) -> tuple[float, int, float] | None:
    indexes = np.flatnonzero((values[:-1] >= target) & (values[1:] < target))
    if len(indexes) == 0:
        return None
    i = int(indexes[0])
    fraction = (target - values[i]) / (values[i + 1] - values[i])
    hz = float(10 ** (np.log10(freq[i]) + fraction * (np.log10(freq[i + 1]) - np.log10(freq[i]))))
    return hz, i, float(fraction)


def summarize_closed(names: list[str], rows: np.ndarray) -> dict:
    freq = rows[:, 0].real
    out = rows[:, names.index("v(out)")]
    gain = np.abs(out)
    baseline = float(np.interp(1.0, freq, gain))
    mask = freq >= 1
    peak = float(np.max(gain[mask]))
    crossing = interpolate_crossing(freq, gain, baseline / np.sqrt(2))
    return {
        "transimpedance_ohm": baseline / 1e-12,
        "peaking_db": max(0.0, float(20 * np.log10(peak / baseline))),
        "bandwidth_hz": crossing[0] if crossing else None,
        "bandwidth_crossings": int(np.count_nonzero((gain[:-1] >= baseline / np.sqrt(2)) & (gain[1:] < baseline / np.sqrt(2)))),
    }


def summarize_loop(names: list[str], rows: np.ndarray) -> dict:
    freq = rows[:, 0].real
    amp = rows[:, names.index("v(amp)")]
    feedback = rows[:, names.index("v(fb)")]
    return_ratio = -amp / feedback
    magnitude = np.abs(return_ratio)
    phase = np.unwrap(np.angle(return_ratio)) * 180 / np.pi
    crossing = interpolate_crossing(freq, magnitude, 1.0)
    count = int(np.count_nonzero((magnitude[:-1] >= 1) & (magnitude[1:] < 1)))
    if not crossing:
        return {"unity_hz": None, "phase_margin_deg": None, "unity_crossings": count}
    hz, i, fraction = crossing
    phase_at_unity = float(phase[i] + fraction * (phase[i + 1] - phase[i]))
    phase_at_unity_wrapped = (phase_at_unity + 180) % 360 - 180
    return {
        "unity_hz": hz,
        "phase_margin_deg": 180 + phase_at_unity_wrapped,
        "phase_at_unity_deg": phase_at_unity_wrapped,
        "low_frequency_phase_deg": float(phase[0]),
        "unity_crossings": count,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("--mode", required=True, choices=("closed", "loop"))
    args = parser.parse_args()
    names, steps = read_ac(args.raw)
    summarize = summarize_closed if args.mode == "closed" else summarize_loop
    print(json.dumps([{"step": i + 1, **summarize(names, rows)}
                      for i, rows in enumerate(steps)], indent=2))


if __name__ == "__main__":
    main()
