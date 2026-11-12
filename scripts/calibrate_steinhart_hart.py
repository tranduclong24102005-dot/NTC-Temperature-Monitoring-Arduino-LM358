#!/usr/bin/env python3
"""Fit Steinhart-Hart A/B/C from 3 (temperature C, resistance ohm) points.

Usage:
    python scripts/calibrate_steinhart_hart.py data/calibration_points_from_report.csv

No third-party dependencies. Only for educational, 3-point calibration.
"""
import csv
import math
import sys
from pathlib import Path


def solve_linear_3x3(matrix, values):
    """Gaussian elimination with partial pivoting (3 equations / 3 unknowns)."""
    a = [list(row) + [value] for row, value in zip(matrix, values)]
    for column in range(3):
        pivot = max(range(column, 3), key=lambda row: abs(a[row][column]))
        if abs(a[pivot][column]) < 1e-18:
            raise ValueError("Singular or ill-conditioned three-point calibration")
        a[column], a[pivot] = a[pivot], a[column]
        scale = a[column][column]
        for k in range(column, 4):
            a[column][k] /= scale
        for row in range(3):
            if row == column:
                continue
            multiplier = a[row][column]
            for k in range(column, 4):
                a[row][k] -= multiplier * a[column][k]
    return [a[i][3] for i in range(3)]


def sh_temp_c(r_ohm, a, b, c):
    ln_r = math.log(r_ohm)
    inv_kelvin = a + b * ln_r + c * ln_r ** 3
    if inv_kelvin <= 0:
        raise ValueError("Invalid inverse temperature; check coefficients")
    return 1.0 / inv_kelvin - 273.15


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/calibrate_steinhart_hart.py PATH_TO_3_POINTS.csv")
        return 2

    file_path = Path(sys.argv[1])
    try:
        with file_path.open("r", encoding="utf-8-sig", newline="") as fp:
            reader = csv.DictReader(fp)
            points = [(float(r["temp_c"]), float(r["resistance_ohm"])) for r in reader]
        if len(points) != 3:
            raise ValueError("Expected exactly 3 rows of data")
        if any(r <= 0 or t <= -273.15 for t, r in points):
            raise ValueError("Resistance must be positive; temperature above absolute zero")
        matrix = [[1.0, math.log(r), math.log(r) ** 3] for t, r in points]
        right = [1.0 / (t + 273.15) for t, r in points]
        a, b, c = solve_linear_3x3(matrix, right)
        print("Steinhart-Hart coefficients fitted to YOUR input points:")
        print(f"SH_A = {a:.15g}f;")
        print(f"SH_B = {b:.15g}f;")
        print(f"SH_C = {c:.15g}f;")
        print("\nFit check (not independent validation):")
        for t, r in points:
            computed = sh_temp_c(r, a, b, c)
            print(f"R={r:10.1f} ohm | reference={t:7.3f} C | fitted={computed:7.3f} C")
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
