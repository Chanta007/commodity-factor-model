"""Tests for the public synthetic estimator, no market data."""
from __future__ import annotations

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import estimate  # noqa: E402


class RecoveryTests(unittest.TestCase):
    def test_the_estimator_recovers_a_known_coefficient(self):
        result = estimate.fit_demo(beta=0.17, seed=7, n=520)
        self.assertAlmostEqual(result["beta"], 0.17, delta=0.02)
        self.assertGreater(result["t"], 3.0)
        self.assertEqual(result["n"], 520)

    def test_a_small_coefficient_is_also_recovered(self):
        result = estimate.fit_demo(beta=0.03, seed=11, n=520)
        self.assertAlmostEqual(result["beta"], 0.03, delta=0.02)

    def test_the_synthetic_panel_is_deterministic(self):
        first = estimate.synthetic(n=20, beta=0.1, seed=3)
        second = estimate.synthetic(n=20, beta=0.1, seed=3)
        third = estimate.synthetic(n=20, beta=0.1, seed=4)
        self.assertEqual(first, second)
        self.assertNotEqual(first, third)

    def test_the_ols_fit_is_exact_on_a_line(self):
        x = [[1.0, float(i)] for i in range(10)]
        y = [2.0 + 3.0 * i for i in range(10)]
        result = estimate.ols(y, x)
        self.assertAlmostEqual(result["beta"][0], 2.0, places=9)
        self.assertAlmostEqual(result["beta"][1], 3.0, places=9)
        self.assertAlmostEqual(result["r2"], 1.0, places=9)


if __name__ == "__main__":
    unittest.main()