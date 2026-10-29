#!/usr/bin/env python3
"""A small, public demonstration of the estimation used by the model.

The private research repository holds the market data. This script shows the
method without any market data: it generates a synthetic panel with a known
scarcity coefficient, estimates the same regression with Newey-West (HAC)
standard errors, and prints the recovery.

    python3 scripts/estimate.py --demo
    python3 scripts/estimate.py --demo --beta 0.17 --seed 7 --json

The point is not the synthetic number. The point is that the estimator is
readable, testable, and recovers a coefficient it was not told.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from typing import List, Sequence, Tuple

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def solve(matrix: List[List[float]], vector: List[float]) -> List[float]:
    """Gaussian elimination with partial pivoting, for a small dense system."""
    n = len(matrix)
    a = [row[:] + [vector[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError("singular design matrix")
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        for j in range(col, n + 1):
            a[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            if factor == 0:
                continue
            for j in range(col, n + 1):
                a[row][j] -= factor * a[col][j]
    return [a[i][n] for i in range(n)]


def transpose_product(x: Sequence[Sequence[float]]) -> List[List[float]]:
    k = len(x[0])
    out = [[0.0] * k for _ in range(k)]
    for row in x:
        for i in range(k):
            for j in range(k):
                out[i][j] += row[i] * row[j]
    return out


def inverse(matrix: List[List[float]]) -> List[List[float]]:
    n = len(matrix)
    columns = []
    for col in range(n):
        unit = [1.0 if i == col else 0.0 for i in range(n)]
        columns.append(solve(matrix, unit))
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def ols(y: Sequence[float], x: Sequence[Sequence[float]]) -> dict:
    k = len(x[0])
    xtx = transpose_product(x)
    xty = [sum(row[i] * target for row, target in zip(x, y)) for i in range(k)]
    beta = solve(xtx, xty)
    fitted = [sum(b * v for b, v in zip(beta, row)) for row in x]
    residuals = [target - fit for target, fit in zip(y, fitted)]
    mean = sum(y) / len(y)
    total = sum((target - mean) ** 2 for target in y)
    residual = sum(error ** 2 for error in residuals)
    return {"beta": beta, "residuals": residuals, "xtx_inv": inverse(xtx),
            "r2": 1.0 - residual / total if total else 0.0}


def hac_se(x: Sequence[Sequence[float]], residuals: Sequence[float],
           xtx_inv: List[List[float]], lags: int = 4) -> List[float]:
    """Newey-West standard errors with a Bartlett kernel."""
    n, k = len(x), len(x[0])
    meat = [[0.0] * k for _ in range(k)]
    for t in range(n):
        for i in range(k):
            for j in range(k):
                meat[i][j] += residuals[t] ** 2 * x[t][i] * x[t][j]
    for lag in range(1, lags + 1):
        weight = 1.0 - lag / (lags + 1.0)
        for t in range(lag, n):
            for i in range(k):
                for j in range(k):
                    meat[i][j] += weight * residuals[t] * residuals[t - lag] \
                        * (x[t][i] * x[t - lag][j] + x[t - lag][i] * x[t][j])
    cov = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            cov[i][j] = sum(xtx_inv[i][a] * meat[a][b] * xtx_inv[b][j]
                            for a in range(k) for b in range(k))
    return [math.sqrt(max(cov[i][i], 0.0)) for i in range(k)]


def synthetic(n: int = 520, beta: float = 0.17, seed: int = 7) -> Tuple[List[float], List[List[float]]]:
    """A weekly panel with a known scarcity coefficient and a seasonal curve."""
    rng = random.Random(seed)
    month_effect = [0.010, 0.014, 0.006, -0.004, -0.010, -0.008,
                    -0.002, 0.000, 0.004, 0.006, 0.010, 0.014]
    y, x = [], []
    scarcity = 0.0
    rate = 2.0
    dollar = 100.0
    for t in range(n):
        scarcity = 0.85 * scarcity + rng.gauss(0.0, 0.55)
        rate += 0.03 * (2.0 - rate) + rng.gauss(0.0, 0.08)
        dollar += 0.02 * (100.0 - dollar) + rng.gauss(0.0, 0.9)
        month = (t // 4) % 12
        carry = (0.005 + beta * scarcity + 0.0020 * rate - 0.0003 * dollar
                 + month_effect[month] + rng.gauss(0.0, 0.100))
        row = [1.0, scarcity, rate, dollar] + [1.0 if month == m else 0.0 for m in range(11)]
        y.append(carry)
        x.append(row)
    return y, x


def fit_demo(beta: float = 0.17, seed: int = 7, n: int = 520) -> dict:
    y, x = synthetic(n=n, beta=beta, seed=seed)
    result = ols(y, x)
    se = hac_se(x, result["residuals"], result["xtx_inv"], lags=4)
    return {"true_beta": beta, "beta": result["beta"][1], "t": result["beta"][1] / se[1],
            "n": n, "r2": result["r2"], "seed": seed}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="run the synthetic demonstration")
    parser.add_argument("--beta", type=float, default=0.17, help="the true synthetic coefficient")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--n", type=int, default=520)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.demo:
        parser.error("pass --demo; this script never reads market data")
    result = fit_demo(beta=args.beta, seed=args.seed, n=args.n)
    if args.json:
        print(json.dumps(result, sort_keys=True))
        return 0
    print("synthetic demonstration, no market data")
    print("true beta      %.4f" % result["true_beta"])
    print("estimated beta %.4f" % result["beta"])
    print("HAC t          %.2f" % result["t"])
    print("observations   %d" % result["n"])
    print("R2             %.3f" % result["r2"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())