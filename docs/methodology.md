# Method in one page

The model is deliberately small. The object of interest is one coefficient, and every other choice
is there to stop that coefficient being an artefact.

## 1. The two measurements

**Scarcity.** For each market, take the weekly inventory level and compute a z-score against the
same ISO week in the prior five years:

```text
scarcity_t = (inventory_t - mean(inventory_same_week)) / sd(inventory_same_week)
```

A high value means the stock is tight. The seasonal comparison is what removes the winter/summer
shape that would otherwise dominate.

**Carry.** Take the first and fourth contract for the same market and compute:

```text
carry_t = 4 × ln(M1_t / M4_t)
```

The multiplier annualises a three-month slope. Positive is backwardation.

## 2. The regression

```text
carry_t = a + b × scarcity_t + c' × controls_t + month dummies + error_t
```

The coefficient `b` is the result. The controls are:

- the policy buffer (OPEC+ spare capacity, SPR, LNG capacity, as available);
- the short rate;
- industrial production;
- the trade-weighted dollar;
- realised volatility.

Standard errors are Newey-West (HAC) with a lag long enough to cover the overlap in weekly data.
The model reports the coefficient, the t-statistic, the number of observations and R². It does not
report a p-value as if it were a probability that the theory is true.

## 3. The sample

| Market | Observations | First week | Last week |
|---|---|---|---|
| WTI | 742 | 2010-01-08 | 2024-04-05 |
| Henry Hub | 481 | 2015-01-09 | 2024-04-05 |

The carry sample ends on 2024-04-05 because the EIA stopped republishing NYMEX settlements on that
date. The weekly stocks continue beyond it; the model says so rather than splicing a different
curve into the same series.

## 4. The tests

| Test | What it asks | What would make it fail |
|---|---|---|
| Controlled regression | Is `b` positive after the controls? | A negative or insignificant coefficient |
| Convexity | Does the slope change at high scarcity? | The wrong sign, or no improvement |
| State split | Is the relation different after 2020? | The same slope in both windows |
| Tight-storage dummy | Does tight storage shift the level? | An insignificant or negative dummy |
| Common factor | Is the co-movement real? | A share no higher than the null |
| Factor localisation | Is the factor liquids or global energy? | A null-sized increment from adding gas |
| Walk-forward | Does it beat a naive forecast? | Worse error than the naive |
| Scorecard | Do the registered rules hold? | A rule changes sign or misses its bar |

The common-factor null is built by applying the same estimator to independent series with the same
shape. That is the comparison that turns a principal component into evidence.

## 5. The out-of-sample rule

The walk-forward re-estimates the model on the expanding past and predicts the next period. It
compares three forecasts:

1. the model;
2. a seasonal naive (the same week last year);
3. a random walk (the last value).

The model beats the seasonal naive and loses to the random walk. Both results are reported. A
result that only appears against the weaker benchmark is not a timing model.

## 6. What is registered and what is exploratory

Each claim has a rule written before the result is seen, a sample, and a stated outcome. The
scorecard is **12 confirmed, 2 no-edge, 1 falsified**. The two no-edge rules are the weekly build
in oil and gas. The falsified rule is the gas convexity term.

The energy block has no registered holdout. The rates block does. The difference is stated in the
explainer and is not hidden.

## 7. Reproduction

The public repository contains the aggregate numbers and the figure generator, not the data. A
reader can reproduce every figure with:

```bash
python3 scripts/make_figures.py
python3 tests/check_public.py
```

The private research repository holds the declarations, the manifest, the data catalog and the
retrieval receipts. The public repository links to the published documents, not to the bytes.

## 8. Limits

- The model is a **level** model. It does not forecast the price.
- The carry sample is historical. The live curve is a separate integration.
- The scarcity measure uses a five-year seasonal window. A structural change in storage capacity
  is not in the linear term.
- The common factor is measured on nine prices. A wider panel could change the share.
- The scorecard is a record of tests, not a guarantee of future performance.
- The model has no live track record.

[Back to the landing page](../README.md) · [Explainer](explainer.md) · [Roadmap](roadmap.md) ·
[Data and licences](data-and-licences.md)