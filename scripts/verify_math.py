#!/usr/bin/env python3
"""Numeric smoke checks based on the documented divider, amplifier and NTC model.

No hardware is connected. Passing these tests does not certify measurement accuracy.
"""
import math
import unittest

R25 = 10000.0
BETA = 3950.0
DIVIDER_V = 3.3
VREF_V = 1.65
R1, R2, R3 = 10000.0, 10000.0, 5600.0
SH_A, SH_B, SH_C = 0.001129148, 0.000234125, 0.0000000876741


def ntc_from_beta(temp_c):
    return R25 * math.exp(BETA * (1 / (temp_c + 273.15) - 1 / 298.15))


def vin_from_ntc(resistance_ohm):
    return DIVIDER_V * R1 / (R1 + resistance_ohm)


def vout_from_vin(vin):
    ratio = R3 / R2
    return vin * (1 + ratio) - VREF_V * ratio


def steinhart_temp_c(resistance_ohm):
    lnr = math.log(resistance_ohm)
    return 1 / (SH_A + SH_B * lnr + SH_C * lnr ** 3) - 273.15


def inverse_recovery(vout):
    ratio = R3 / R2
    vin = (vout + VREF_V * ratio) / (1 + ratio)
    ntc_resistance = R1 * (DIVIDER_V / vin - 1)
    return steinhart_temp_c(ntc_resistance)


class FormulaChecks(unittest.TestCase):
    def test_at_25_degrees(self):
        ntc = ntc_from_beta(25)
        self.assertAlmostEqual(ntc, 10000, places=5)
        self.assertAlmostEqual(vin_from_ntc(ntc), 1.65, places=5)
        self.assertAlmostEqual(vout_from_vin(1.65), 1.65, places=5)
        self.assertAlmostEqual(steinhart_temp_c(10000), 25.0, delta=0.2)

    def test_reported_calibration_points_approximate(self):
        points = [(8, 21916), (29, 8395), (52, 3345)]
        for temperature, resistance in points:
            with self.subTest(reference_c=temperature):
                self.assertAlmostEqual(steinhart_temp_c(resistance), temperature, delta=0.1)

    def test_ideal_temperature_voltage_increases(self):
        temps = [-3.35, 25, 60]
        values = [vout_from_vin(vin_from_ntc(ntc_from_beta(t))) for t in temps]
        self.assertTrue(values[0] < values[1] < values[2])
        self.assertAlmostEqual(values[0], 0.101, delta=0.01)
        self.assertAlmostEqual(values[2], 3.199, delta=0.01)

    def test_mathematical_reverse_path(self):
        for t in (8, 25, 29, 52, 60):
            with self.subTest(temp_c=t):
                vout = vout_from_vin(vin_from_ntc(ntc_from_beta(t)))
                reconstructed = inverse_recovery(vout)
                self.assertAlmostEqual(reconstructed, t, delta=0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
