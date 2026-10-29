# The research

The public record of what was asked, what was found, and what would change the conclusion.

## The question

Oil and gas are physical markets. When the stock is low relative to the same week in prior years,
the nearby barrel should be worth more than the deferred one. The curve should backwardate.

Three questions follow:

1. Is the relation in the data once the obvious alternatives are controlled for?
2. How strong is it, and where is it strongest?
3. Can it frame a trade idea without confusing a story with an edge?

## The four claims

| Claim | Test | Result |
|---|---|---|
| Scarce stock means backwardation | Controlled regression of annualised carry on seasonal scarcity | **Confirmed** in oil and gas |
| Gas obeys the same idea more tightly | Same regression, gas sample | **Confirmed**; gas R² 0.739 against 0.140 |
| The state changes the relation | 2020 split; tight-storage dummy | **Confirmed**; tight storage is a level shift, post-2020 a slope change |
| The weekly build adds little | Horse race against the level; build coefficient | **No edge** in oil and gas |
| Liquids move together, gas separately | First-component share against a null | **Confirmed**; median 0.561 vs 0.243 |
| Gas convexity at high scarcity | Squared scarcity term | **Falsified** in gas |

The scorecard is **12 confirmed, 2 no-edge, 1 falsified**.

## What the evidence says

- Oil scarcity coefficient: **0.0311** (HAC t 3.49), n 742, R² 0.140.
- Gas scarcity coefficient: **0.1724** (HAC t 6.86), n 481, R² 0.739.
- Common-factor share: **0.561** median against a null of **0.243**; **0.667** ex-gas against 0.260.
- Walk-forward: **28.3%** lower error than a seasonal naive for oil, **53.2%** for gas.
- Against a random walk: worse (oil 0.120 vs 0.042; gas 0.173 vs 0.100).
- Direction accuracy: 48.7% oil, 53.7% gas.

## What the state variable looks like

The seasonal z-score is not identically distributed across the two markets.

| Measure | Oil (WTI) | Gas (Henry Hub) |
|---|---|---|
| Observations | 742 | 481 |
| Median | -0.46 | -0.07 |
| 10th percentile | -4.71 | -1.53 |
| 90th percentile | 0.68 | 1.04 |
| Share beyond one standard deviation | 44.7% | 34.9% |

Oil's left tail is the 2020 storage build. A model that treated "one z-score" as the same event in
both markets would miss that. The public figures show the aggregate distribution and a synthetic
construction, not dated observations.

## What the research cannot say

- It explains the **level** of carry relative to seasonality. It does not time week-to-week moves.
- The measured curve ends **2024-04-05**, when the EIA stopped republishing NYMEX settlements.
  The live curve is a separate integration.
- The energy block has **no registered holdout**. The out-of-sample test is a walk-forward.
- The scarcity term is linear. A storage-capacity ceiling is researched, not implemented.
- The power leg is out of scope because no free forward curve was found.
- The event layer is curated by hand; there is no automated news feed yet.
- The model has no live track record.

## What would change the conclusion

- A negative or insignificant scarcity coefficient in a larger sample.
- A common-factor share no higher than the null in a wider panel.
- A walk-forward that stops beating the seasonal naive after the live curve is joined.
- A gas event study showing the carry effect is entirely an event effect.

## How to read the evidence

| Document | What it covers |
|---|---|
| [The visual explainer](explainer.md) | The theory and the evidence, chart by chart |
| [Method](methodology.md) | The equations, the sample, the tests |
| [Roadmap](roadmap.md) | Built, in progress, researched |
| [Reproducing](reproducing.md) | How to run the public estimator and the checks |
| [Data and licences](data-and-licences.md) | What is not published, and why |

[Back to the landing page](../README.md)