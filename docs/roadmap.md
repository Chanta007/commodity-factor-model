# Roadmap

What is built, what is in progress, and what has been researched. Each item names the next test,
so the roadmap is a set of questions rather than a wish list.

## Built

| Item | What it does | Where it is shown |
|---|---|---|
| Data layer | Declares the EIA and FRED series, fetches them, verifies checksums and dates, and records a manifest | Private repository; aggregate coverage in the figures |
| Scarcity and carry | Seasonal z-score and annualised slope | [Method](methodology.md) |
| Controlled regression | HAC standard errors, policy buffer, rates, demand, dollar, volatility and month dummies | [Explainer §3](explainer.md#3-scarcity-moves-the-curve) |
| Common-factor null | Compares the observed share with independent series of the same shape | [Explainer §7](explainer.md#7-one-factor-but-not-one-market) |
| State tests | 2020 split and tight-storage dummy | [Explainer §5](explainer.md#5-the-state-matters-in-two-different-ways) |
| Walk-forward | Expanding-window out-of-sample against seasonal naive and random walk | [Explainer §4](explainer.md#4-gas-is-the-stronger-market) |
| Scorecard | 12 confirmed, 2 no-edge, 1 falsified | [Explainer §8](explainer.md#8-the-scorecard) |
| Deterministic figures | Six SVGs generated from aggregate numbers | [`figures/`](figures/) |

## In progress

| Item | Why it matters | Next test |
|---|---|---|
| Live curve integration | The measured baseline ends 2024-04-05 | Join Databento or ICE settlements to the existing stocks and re-run the same regression; report the splice explicitly |
| Gas event study | Weather and outages are events, not weekly columns | Pre-register event windows for polar vortexes, hurricanes, LNG outages and pipeline closures; measure abnormal front-month returns, volatility and basis |
| News and event feed | The event list is curated by hand | Add dated EIA, OPEC+, NOAA and LNG/pipeline notices with a source and a timestamp; measure whether a dated event closes a measured gap |

## Researched

| Item | Finding | Why it is parked |
|---|---|---|
| Gas storage-capacity ceiling | A linear scarcity term may miss the physical ceiling | No clean public capacity series at the required frequency; test a piecewise term once the series is found |
| Power leg | A forward curve is needed for the same carry object | No free forward curve; day-ahead indices have zero tenor and are not a substitute |
| A second holdout | The rates block has one; the energy block does not | The walk-forward is the current out-of-sample test; a holdout is a later, separate registration |
| Wider commodity panel | The common factor is measured on nine energy prices | A wider panel is a new question and a new multiple-comparison count |

## What would change the conclusion

- A negative or insignificant scarcity coefficient in a larger sample.
- A common-factor share no higher than the null in a wider panel.
- A walk-forward that stops beating the seasonal naive after the live curve is joined.
- A gas event study that shows the carry effect is entirely an event effect.

These are the results that would reopen the claims. They are listed so the model can be wrong in
public.

[Back to the landing page](../README.md) · [Explainer](explainer.md) · [Method](methodology.md) ·
[Data and licences](data-and-licences.md)