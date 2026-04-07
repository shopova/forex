# Clean Slate FX Strategy v1

## Purpose

This document defines a clean-slate trading framework built from:

- the trader profile and behavioral constraints in this repository
- the practical lessons captured in `some-investment-books/INVESTMENT_BOOKS_SUMMARY.md`
- market-structure notes from `The Art and Science of Technical Analysis`
- risk and psychology principles reflected across `Trading in the Zone`, `The Disciplined Trader`, `Trade Your Way to Financial Freedom`, and `The New Trading for a Living`
- external market-structure, FX-market, and prop-firm reference points

It is not a pattern-first strategy.

It is a structure-first, risk-first, process-first strategy.

## Why This Version Exists

The current repository already contains several trigger families:

- Last Kiss
- Big Shadow
- Wammie / Moolah
- QQE / QMP

The problem is not that these patterns are useless.

The problem is that the trigger layer has become too important relative to:

- market regime
- location
- structure quality
- risk asymmetry
- behavioral stability

This clean-slate version fixes that by making the trigger a secondary filter.

## Core Thesis

The durable edge should come from five things:

1. Trading only liquid major FX pairs.
2. Trading in the direction of higher-timeframe structure.
3. Entering after a healthy correction into meaningful price.
4. Requiring objective proof that the correction has ended.
5. Keeping losses small and standardized while targeting asymmetric outcomes.

## Strategy Identity

Name:

- `Major-Pair Structure Continuation`

Primary style:

- swing / short-term swing continuation

Primary market:

- spot FX majors

Primary holding profile:

- same day to multi-day

Primary objective:

- positive expectancy with low behavioral complexity

## Instrument Scope

Trade only:

- `EURUSD`
- `USDJPY`
- `GBPUSD`
- `USDCAD`

Start with:

- `EURUSD`
- `USDJPY`

Reason:

- they are liquid
- they align with your London-session operating model
- they reduce unnecessary symbol sprawl

Do not trade more than one open macro idea at a time.

If two pairs express the same USD theme, treat them as one trade idea.

## Session Scope

Execution session:

- London session into early New York only

Operating rule:

- analysis once
- alerts only afterward
- no chart babysitting all day

No new positions:

- within 60 minutes before high-impact news on either currency in the pair
- within 15 minutes after the event if volatility is still abnormal

## Timeframe Model

- `Daily`: bias and major location
- `4H`: regime, impulse, and correction structure
- `1H`: entry confirmation and execution

The sequence never changes:

1. `Daily` bias
2. `4H` structure
3. `1H` trigger

If the first two are unclear, the third does not matter.

## Regime Classification

Every pair must be classified as one of three states:

- `Trend`
- `Range`
- `Transition`

### Trend

Trade only if all are true:

- `Daily` price is clearly above or below the `200 SMA`
- `4H` structure shows `HH + HL` for longs or `LH + LL` for shorts
- with-trend swings are still larger or cleaner than countertrend swings
- the pullback has not broken the key opposite-side `4H` pivot

### Range

No continuation trades.

### Transition

No continuation trades.

Transition includes:

- failed continuation attempts
- first abnormal countertrend swing
- mixed `HH + LL` or `LH + HL`
- climax behavior

## Setup Type

Use only one core setup:

- `trend continuation after a healthy pullback`

This is the actual setup.

The candle pattern is only the trigger.

## What Counts as a Valid Pullback

The pullback must satisfy most of the following:

- it follows a clear `4H` impulse, not drift
- it retraces into a logical area:
  - prior structure
  - broken level
  - `4H 50 EMA`
  - fib zone, usually `0.38` to `0.62`
- it is corrective in character:
  - overlapping bars
  - lower volatility than the impulse leg
  - no strong opposite-side expansion
- it does not break the key `4H` invalidation point
- it still leaves at least `2R` to the next meaningful target

Invalid pullback:

- too deep
- too sharp
- directly news-driven
- countertrend leg larger than the prior with-trend leg
- forms into major opposing daily structure

## Trigger Logic

Use only two approved trigger families.

Both must be placed by stop order, never by chasing market price.

### Trigger A: Reclaim / Acceptance Trigger

For longs:

- price pulls back into a valid continuation zone
- `1H` probes below or into the zone
- `1H` closes back above the local level with bullish intent
- buy stop goes above the trigger candle high

For shorts:

- price pulls back into a valid continuation zone
- `1H` probes above or into the zone
- `1H` closes back below the local level with bearish intent
- sell stop goes below the trigger candle low

### Trigger B: Micro-Structure Shift Trigger

For longs:

- pullback forms lower highs on `1H`
- price breaks the last lower high or the pullback trendline
- buy stop goes above the breakout / confirmation candle

For shorts:

- pullback forms higher lows on `1H`
- price breaks the last higher low or the pullback trendline
- sell stop goes below the breakout / confirmation candle

## How Existing Patterns Fit

Existing patterns are demoted to confirmation only.

- `Last Kiss` is valid only if it also satisfies the continuation setup and reclaim logic.
- `Big Shadow` is valid only if it appears at a meaningful correction endpoint or true exhaustion extreme.
- `Wammie / Moolah` is not a core continuation trigger and should not be used inside trend continuation unless it also resolves through structure.
- `QQE / QMP` is timing confirmation only, never primary decision logic.

This means the strategy can still use familiar tools without depending on them.

## Entry Rules

Enter only if all are true:

- pair is in approved universe
- regime = `Trend`
- `Daily` and `4H` are aligned
- pullback is healthy
- one of the two approved triggers prints
- planned target is at least `2R`
- trade does not violate daily or weekly risk cap

Order type:

- stop order only

No entry:

- inside the trigger candle
- in the middle of a range
- after the move has already expanded away from the zone

## Stop Placement

Stop goes beyond structural invalidation, not at an arbitrary pip distance.

Approved stop locations:

- beyond the `1H` trigger extreme plus buffer
- beyond the pullback swing point plus buffer
- beyond the `4H` invalidation if size still allows acceptable risk

Buffer:

- `0.5` to `1.0 x ATR(14)` on `1H`, depending on pair volatility

Never:

- widen the stop after entry
- move the stop because of emotion

## Profit Taking

Default management:

- full target at `2R`

Optional advanced management, only after positive sample:

- partial at `2R`
- trail remainder behind new `1H` swing structure

For now, default to the simpler model:

- one entry
- one stop
- one target

This is less exciting and more stable.

## Position Sizing

Current live rebuild sizing:

- `0.25%` risk per trade

Current hard caps:

- daily max loss: `0.50%`
- weekly max loss: `1.50%`
- max one open position at a time
- max two trades per day
- max six trades per week

Risk may scale only after:

- at least `30-50` clean trades
- positive expectancy
- no oversized losses
- no rule-breaking cluster

## Trade Grading

Every trade is graded before entry.

### A+

- clean daily bias
- clean `4H` trend
- pullback into strong location
- trigger prints cleanly
- no nearby opposing structure
- `2.5R+` space available

### A

- all core conditions present
- some minor imperfection
- still `2R+`

### B

- technically valid but not clean enough

Allowed live:

- `A+`
- `A`

Skip:

- `B`

## Hard Disqualifiers

Skip the trade if any are true:

- market is in `Range` or `Transition`
- no clear `4H` impulse exists
- pullback is too aggressive
- target is below `2R`
- trade is near major news
- trade requires narrative or hope
- you feel urgency to recover prior losses
- broker sizing forces you above planned risk

## Journaling Metrics

Track these, not just win rate:

- setup grade
- pair
- regime
- trigger family
- planned `R`
- realized `R`
- average win
- average loss
- net `R`
- rule compliance
- emotional state before entry

If expectancy is positive but only because of a few outliers, note that explicitly.

## Utilization Paths

### 1. Discretionary Manual Use

Use a fixed workflow:

1. Mark daily bias.
2. Mark `4H` regime and invalidation.
3. Draw the pullback zone.
4. Set alerts at the zone.
5. Wait for one of the two approved `1H` triggers.
6. Place stop order, stop loss, and target immediately.

### 2. TradingView Indicator Stack

The most useful automation is not a pattern detector alone.

Build tools in this order:

1. `Regime Filter`
   - classifies `Trend / Range / Transition`
2. `Pullback Quality Tool`
   - highlights valid continuation zones on `4H`
3. `Trigger Tool`
   - marks reclaim / micro-structure shift triggers on `1H`
4. `Risk Planner`
   - entry, stop, target, position size, and live `R`

### 3. Backtesting Use

Test separately by:

- pair
- year
- regime
- trigger family

Do not accept aggregate-only results.

Minimum useful outputs:

- trade count
- win rate
- average win
- average loss
- net `R`
- max drawdown in `R`
- expectancy

### 4. FTMO Use

This strategy is better suited to the `2-Step` FTMO model than the `1-Step` model.

Reason:

- `2-Step` allows a `5%` maximum daily loss and `10%` maximum loss
- `1-Step` uses a `3%` daily loss limit, a trailing maximum loss, and a `Best Day Rule`
- your local records show that behavioral volatility is currently the bigger risk than idea generation

## What This Strategy Explicitly Rejects

- high-frequency signal collecting
- indicator-first entries
- trading in transition just because a candle looks strong
- revenge re-entry
- multiple correlated positions
- phone execution
- trying to recover losses quickly

## Expected Strengths

- simpler decision tree
- easier journaling
- lower trigger controversy
- better fit with your existing structure-first beliefs
- stronger alignment with prop-style risk limits

## Expected Weaknesses

- lower trade frequency
- more missed moves
- requires patience around pullbacks
- will underperform in fast breakout conditions without retests

These are acceptable trade-offs.

## Review Standard

After the first `30` trades, review:

- Which pair performs best?
- Does reclaim or micro-structure trigger perform better?
- Are stop buffers too tight or too loose?
- Are you skipping valid trades or forcing weak ones?
- Is `2R` the right default target, or should some pairs use a slightly different model?

Do not expand setup variety before this review is complete.

## Version Rule

This is `v1`.

For now:

- one core setup
- two trigger families
- four pairs maximum
- one session
- one open idea at a time

Complexity can be added later only if the simpler version proves profitable and behaviorally stable first.

## External Reference Anchors

These are not trade signals.

They are the external reasons this framework is shaped the way it is:

- `BIS Triennial Survey (30 September 2025)`:
  - global FX turnover reached `USD 9.6 trillion` per day in April 2025
  - the `USD` was on one side of `89%` of all FX trades
  - the `EUR` and `JPY` remained among the most traded currencies
  - the `United Kingdom` remained the most important FX trading location globally
- `AQR / Hurst, Ooi, Pedersen (2017)`:
  - trend-following evidence remains robust across long historical samples
- `Moskowitz, Ooi, Pedersen (2012)`:
  - time-series momentum was documented across multiple asset classes, including currency instruments
- `FX Global Code (December 2024)`:
  - supports process discipline around ethics, governance, execution, risk management, and compliance
- `FTMO official objective pages checked on 11 March 2026`:
  - `2-Step`: `10%` challenge target, `5%` verification target, `5%` max daily loss, `10%` max loss, minimum `4` trading days
  - `1-Step`: `10%` target, `3%` max daily loss, `10%` end-of-day trailing max loss, `50%` Best Day Rule

Inference from those sources:

- focus on major USD pairs
- keep execution centered on London-led liquidity
- use a trend / continuation framework rather than frequent reversal guessing
- prefer simple, rules-based governance over discretionary trigger proliferation
