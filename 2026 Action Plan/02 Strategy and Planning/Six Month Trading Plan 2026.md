# Six Month Trading Plan 2026

## Purpose

This plan covers the next six months:

- start: `2026-03-24`
- end: `2026-09-24`

The key change is this:

- the training environment is now a `100K` demo account

That removes the old micro-account constraint.

This plan is no longer built around:

- the `EUR 387.50` live-account balance
- the `0.01` minimum-lot problem
- the need to filter trades mainly by account size

It is now built around:

- professional process simulation
- strategy development under realistic risk
- higher-quality forward testing
- building FTMO-style readiness without paying for a challenge yet

For the current path, treat these older `2026 Action Plan` files as legacy reference only, not active execution documents:

- `Legacy/2026 Action Plan/MT5 Live Trading Plan - 387.50 EUR.md`
- `Legacy/2026 Action Plan/Live Setup Types for Small Account.md`

## Strategic Shift

The strategy logic does not need to change dramatically.

The execution framework does.

What stays:

- `Daily` and `4H` define context
- `30m` defines execution
- only two contexts are traded:
  - continuation from a meaningful level
  - liquidity sweep reversal from a meaningful level
- only two trigger families are used:
  - level reclaim
  - micro structure break

What changes:

- you no longer need to reject good setups only because the stop is too wide for a tiny live account
- you can train proper structural stops and realistic position sizing
- the account should be treated as a professional simulation account, not as a toy

## Identity For This Period

Trade as:

- a part-time professional trader in training

Do not trade as:

- a recovery trader
- a gambler because the money is not real
- a full-time chart watcher
- a pattern collector

The purpose of the demo is not to make fake money.

The purpose is to prove:

- quality of judgment
- quality of routine
- quality of execution
- quality of risk behavior

## Account Model

Use the `100K` demo as if it were funded capital.

Account assumption:

- balance: `100,000` in account currency

Base simulation risk:

- standard risk per trade: `0.25%`
- maximum daily loss: `0.75%`
- maximum weekly loss: `2.0%`
- maximum open positions: `1`
- maximum trades per day: `2`
- maximum trades per week: `8`

This means:

- `0.25%` risk = `250` in account currency
- `0.75%` daily stop = `750`
- `2.0%` weekly stop = `2,000`

These are training limits, not broker limits.

They are intentionally tighter than what many traders would use, because the goal is clean process.

## Why The Strategy Changes Under 100K Demo

With the small live account, the strategy had to be filtered heavily by stop width.

With a `100K` demo, the main filter should be:

- market condition
- level quality
- trigger quality
- rule clarity

Not:

- whether `0.01` lot can physically fit the stop

This means the strategy can now be trained in its more natural form:

- clean structural stops
- cleaner `2R` logic
- better pair comparison
- more honest forward testing

## Core Strategy Framework

### Timeframes

- `Daily`: major bias and major levels
- `4H`: market condition, swing integrity, and zone quality
- `30m`: trigger and execution

### Allowed Contexts

1. `Trend continuation`
   - valid only when `Daily` and `4H` still support the same directional bias
   - requires a real prior impulse and a corrective pullback

2. `Liquidity sweep reversal`
   - valid only at major `Daily` or `4H` levels
   - requires a stretched move, failed sweep, and lower-timeframe shift

### Invalid Contexts

No trade if market is:

- mid-range
- overlapping and messy
- clearly uncertain / transition without a level edge
- too close to major scheduled news

## Pair Scope

Primary pairs:

- `EURUSD`
- `GBPUSD`
- `USDJPY`

Secondary pair:

- `USDCAD` once the first three are being handled cleanly

This is wider than the small-account model, but still narrow enough to stay professional.

## Trigger Model

Use only these trigger families:

### Trigger A: Level Reclaim

- price breaks beyond a meaningful level
- closes back through it
- entry is placed beyond the reclaim candle in the intended direction

### Trigger B: Micro Structure Break

- pullback or sweep stalls at a valid level
- `30m` structure breaks back in the intended direction
- entry is taken on stop beyond the break candle or on first controlled retest

The strategy should not drift back into:

- random candle trading
- indicator dependency
- setup collecting

## Risk Rules

### Base Mode

Use this by default for the first three months:

- `0.25%` risk per trade
- `2` trades per day maximum
- `1` open trade at a time
- stop after `0.75%` daily loss
- stop after `2.0%` weekly loss

### Progression Mode

Only after at least `30` rule-clean demo trades and positive expectancy:

- allow `0.35%` risk on `A+` setups only

`A+` means all of these are true:

- higher-timeframe context is clear
- level is pre-marked and important
- trigger is obvious
- invalidation is clean
- projected target is at least `2R`
- no nearby news conflict

If discipline slips:

- immediately go back to `0.25%`

## Trade Management Model

Default model:

- full target at `2R`

Why this stays:

- easier to test
- easier to review
- reduces management noise

Optional review later:

- partial at `1R`, runner to `2R+`

Do not introduce that variation until you have enough clean demo data to compare it.

## What The Demo Account Allows You To Train Properly

Under the old small-account model, some structurally valid trades had to be skipped because the account was too small.

Under this model, you should now train:

- proper stop placement beyond structural invalidation
- realistic pair comparison
- honest `R` measurement
- professional risk sizing
- behavior under a larger nominal account

This is important.

A trader can look disciplined on a tiny account for the wrong reason:

- because the account physically prevents normal execution

The `100K` demo removes that excuse.

## Time Allocation

For the next six months, use this approximate split:

- `35%` reading and note extraction
- `25%` chart analysis and replay
- `30%` live-market forward testing on demo
- `10%` review and rule refinement

Reading still matters, but the demo should now carry more weight than before.

## Phase 1: Weeks 1-4 (`2026-03-24` to `2026-04-21`)

### Objective

Re-anchor the strategy in structure and begin demo execution without pressure.

### Main Work

- continue the reading curriculum
- finalize definitions for:
  - trend
  - range
  - transition
  - healthy pullback
  - failed pullback
  - valid level
- mark charts daily on `EURUSD`, `GBPUSD`, and `USDJPY`

### Demo Trading Activity

- take only the cleanest setups
- maximum `4` demo trades per week
- use full pre-trade journaling

### End-Phase Deliverables

- market-condition definitions
- healthy pullback checklist
- failed pullback checklist
- first version of the trade scorecard

## Phase 2: Weeks 5-8 (`2026-04-22` to `2026-05-19`)

### Objective

Turn reading into a sharper opportunity filter.

### Main Work

- compare valid vs invalid setups
- define no-trade conditions more aggressively
- classify setups by context:
  - continuation
  - sweep reversal

### Demo Trading Activity

- increase to a maximum of `6` demo trades per week
- no trade unless it is preplanned before the session
- record skipped trades that were correctly rejected

### End-Phase Deliverables

- valid-opportunity scorecard v2
- no-trade checklist
- first formal strategy checklist
- pair preference ranking

## Phase 3: Weeks 9-12 (`2026-05-20` to `2026-06-16`)

### Objective

Refine execution quality.

### Main Work

- standardize the exact trigger rules
- define when reclaim is valid
- define when micro structure break is valid
- eliminate borderline trigger interpretations

### Demo Trading Activity

- forward test in the real trading windows consistently
- maximum `8` demo trades per week
- only one variable may be adjusted at a time

### End-Phase Deliverables

- trigger quality checklist
- example library of clean setups
- updated journal template
- stable entry checklist

## Phase 4: Weeks 13-16 (`2026-06-17` to `2026-07-14`)

### Objective

Operate the strategy as a repeatable professional routine.

### Main Work

- forward test as if accountable to external capital
- track rule compliance as seriously as results
- reduce chart noise and interpretation drift

### Demo Trading Activity

- keep watchlist narrow
- take only trades that can be explained in one paragraph before entry
- review all missed trades, but do not chase them

### End-Phase Deliverables

- at least `20` well-documented demo trades
- weekly review archive
- clear list of top error patterns

## Phase 5: Weeks 17-20 (`2026-07-15` to `2026-08-11`)

### Objective

Test consistency under repetition.

### Main Work

- continue forward testing
- compare pair-level results
- compare continuation vs sweep-reversal results
- stop casual changes to the strategy

### Demo Trading Activity

- maintain base risk unless progression criteria are met
- if progression criteria are met, allow limited `A+` testing at `0.35%`
- if results degrade, return immediately to base mode

### End-Phase Deliverables

- `30-40` documented demo trades
- pair-level performance summary
- context-level performance summary
- list of vague rules still needing cleanup

## Phase 6: Weeks 21-26 (`2026-08-12` to `2026-09-24`)

### Objective

Finish with a strategy that is testable, explainable, and ready for the next stage.

### Main Work

- finalize the written strategy
- finalize the daily routine
- finalize the trade checklist
- compare backtest assumptions with demo behavior
- decide whether the strategy is ready for funded-account preparation

### Demo Trading Activity

- keep execution controlled
- no challenge-style overtrading
- no artificial pressure to hit performance numbers

### End-Phase Deliverables

- final strategy draft
- final trade checklist
- final journal format
- six-month review summary
- decision on next phase

## Daily Operating Rules

Use this structure on trading days:

1. pre-session preparation before `10:30`
2. primary decision window `10:30-12:00`
3. secondary management / preplanned execution window `15:00-16:00`
4. daily study block
5. daily journal and review

## Monthly Focus

### March 24 - April 23

- structure, levels, and market condition

### April 24 - May 23

- pullback quality, invalid setup filtering, and no-trade discipline

### May 24 - June 23

- trigger clarity and execution standardization

### June 24 - July 23

- professional demo routine and accountability

### July 24 - August 23

- consistency and pair-by-pair review

### August 24 - September 24

- consolidation and next-stage decision

## Weekly Review Questions

Answer these every week:

1. Did I follow the session rules?
2. Did I trade only the two approved contexts?
3. Did I reject weak setups fast enough?
4. Which pair was clearest?
5. Which setups were structurally valid but poorly executed?
6. What rule became clearer this week?
7. What still feels vague?

## What Counts As Progress

Progress is:

- clearer chart reading
- cleaner risk behavior
- fewer forced trades
- more accurate no-trade decisions
- better journaling
- more consistent demo execution

Progress is not:

- demo profit spikes from loose risk
- taking extra trades because the money is not real
- changing rules after a few losses
- collecting more setup names

## End-Of-Period Decision

At the end of six months, advance only if most of these are true:

- at least `30` high-quality demo trades are documented
- rules are stable and understandable
- pair focus is clear
- expectancy is positive or close to stable with clean execution
- no recurring risk-rule violations
- no recurring emotional blowups

If these are not true:

- extend the demo phase
- do not escalate to a paid challenge yet

## Bottom Line

The `100K` demo account should make you more honest, not more aggressive.

It removes the distortions of the tiny live account.

That means the strategy should now be trained in its proper form:

- structure first
- triggers second
- risk fixed
- journaling serious
- execution selective

This is the correct bridge between reading and funded-account readiness.
