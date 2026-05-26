# Clean Slate FX Strategy v2 - Session Model

## Strategic Decision

This version replaces the lower-frequency swing-only model with a professional part-time session model.

Reason:

- you are not trading full time
- you want to trade a few focused hours a day
- you need enough repetition to learn
- you do not want a system that depends on rare `1H` candles
- `QQE / QMP` is removed completely

This does not mean becoming a scalper.

It means becoming a structured session trader.

## Strategic Premise

The model is built around three repeatable sources of intraday opportunity:

1. session timing and liquidity concentration
2. interaction with pre-marked higher-timeframe levels
3. simple confirmation after rejection or re-acceptance

The edge is not "a magical candle pattern."

The edge should come from:

1. where price is
2. when price gets there
3. whether behavior changes cleanly
4. whether risk is small and controlled

Important clarification:

- this is not a pure microstructure or order-flow scalping model
- on `30m`, you are trading session flow around structure
- the trigger must stay simple because the hard part is still location, patience, and discipline

## Trading Identity

You should trade as:

- a part-time professional FX session trader

Not as:

- a full-day discretionary trader
- a signal collector
- a pattern hunter

## Market and Pair Scope

Primary pairs:

- `EURUSD`
- `GBPUSD`
- `USDJPY`

Secondary pair:

- `USDCAD` only if your available session overlaps New York enough

Why:

- these are the most practical liquid majors for a level-and-structure trader
- they generally offer cleaner execution conditions than spreading attention across many pairs
- they fit a professional watchlist better than constantly rotating symbols

## Session Commitment

Trade one fixed session block only.

Default recommendation:

- first `2-3` hours of London

Alternative:

- first `2-3` hours of New York, but only if that is the block you can trade consistently

Rules:

- do not switch session by mood
- commit to one session block for a meaningful sample before reviewing results
- if you change session, restart the sample instead of mixing stats

Professionals build routine around repeatable conditions.

## Timeframe Structure

- `Daily`: directional map, weekly context, and major levels
- `4H`: market condition, structural zones, and confirmed swings
- `30m`: execution chart
- `5m`: optional refinement only after competence is proven

Do not start on `5m`.

Your current behavioral profile does not need more noise.

## Meaningful Level Definition

A level is tradable only if it comes from one of these families:

- prior day high
- prior day low
- prior day close
- weekly high or low
- Asia session high or low before London
- one of the last two confirmed `4H` swing highs or swing lows
- a clear `Daily` or `4H` supply or demand zone created by obvious displacement
- a `00` or `50` round number only if it overlaps with one of the higher-timeframe references above

Rules:

- levels must be marked before the session starts
- do not add random intraday lines to justify a trade
- if price is not interacting with a pre-defined level family, there is no setup

## Market Condition Framework

Every trade must begin with one of two contexts.

### Context 1: Trend Continuation

Valid only if:

- `Daily` and `4H` still support the same directional bias
- there is a clear prior impulse in that direction
- the pullback is corrective, not aggressive
- price is pulling into a meaningful level or zone
- there is still at least `2R` available to the first logical opposing structure

Working definition of corrective pullback:

- candles overlap more than they displace
- the pullback travels slower than the prior impulse
- the pullback does not close through the higher-timeframe level that defines the idea

### Context 2: Liquidity Sweep Reversal

Valid only if:

- price is at a clear `Daily` or `4H` extreme or important level
- the move into the level is stretched, one-sided, or climactic
- session liquidity sweeps the level and fails
- price re-accepts back through the level or breaks structure away from it
- there is still at least `2R` available to the first logical opposing structure

### Invalid Context

No trade if market is:

- mid-range
- overlapping and directionless
- in transition without a clear level
- already extended far away from your level before a trigger appears

## Event-Risk Protocol

News risk is part of the model, not an optional afterthought.

Baseline rules:

- no new entry if a Tier-1 release for either currency is due within the next `30` minutes
- no new entry until the first full `30m` candle after the release has closed
- if a major central bank decision, CPI, NFP, or similar release lands inside your trading block, treat the day as reduced quality
- do not widen stops or cancel targets because of news

If the calendar makes the session structurally unstable:

- skip the session

## The Trigger Model

Use the same trigger logic in both contexts.

This is important.

More setups should not mean more random triggers.

Use only these two triggers:

### Trigger A: Level Reclaim

Definition:

- price trades through a meaningful level
- then closes back through it
- entry is taken only after the market shows re-acceptance

Long:

- price trades below support or into demand
- the reclaim candle closes back above the level on `30m`
- buy stop goes above the reclaim candle high

Short:

- price trades above resistance or into supply
- the reclaim candle closes back below the level on `30m`
- sell stop goes below the reclaim candle low

Minimum quality standard:

- the reclaim close must finish in the top third of the candle range for longs
- the reclaim close must finish in the bottom third of the candle range for shorts
- the close must finish clearly back through the level, not just by a tiny drift
- no more than `2` of the last `4` closed `30m` candles may straddle both sides of the level

Valid only if:

- the level is meaningful on `Daily` or `4H`
- the reclaim candle closes clearly back through the level
- there is room for at least `2R`
- the reclaim is not just random chop around the level
- entry is taken only after the reclaim candle has closed

Do not use this trigger if:

- only a wick pierced the level but the close is weak
- price keeps closing on both sides of the level
- the market is still in the middle of a range
- the reclaim candle is so large that the trade is already late

### Trigger B: Micro Structure Break

Definition:

- price reacts at a meaningful level
- then breaks the last meaningful local pivot in the intended direction
- entry is taken on the break or on the first controlled retest

Meaningful pivot definition:

- the pivot must be obvious on `30m`
- it must be the last swing high or swing low that caused at least one full `30m` candle close in the opposite direction before being broken
- wick-only breaks do not count

Long:

- after the pullback or sweep, price breaks the last meaningful `30m` lower high
- buy stop goes above the break candle high or on the first controlled retest

Short:

- after the pullback or sweep, price breaks the last meaningful `30m` higher low
- sell stop goes below the break candle low or on the first controlled retest

Valid only if:

- the pivot being broken is meaningful, not tiny noise
- the level reaction happened first
- the break shows real change of behavior
- the break candle closes through the pivot
- the market still offers at least `2R`
- the trigger happens within `3` closed `30m` candles of the original level reaction

Do not use this trigger if:

- there is no clear pivot to break
- the market is still overlapping and messy
- the broken pivot is too minor to matter
- you are calling it a break only because one candle looks dramatic
- price has already traveled too far from the invalidation point before entry

## Trigger Decision Tree

Use this every time:

1. Is price at a meaningful pre-marked `Daily` or `4H` level?
   If no:
   no trade
2. Is the session active and free of immediate Tier-1 event risk?
   If no:
   no trade
3. Is the context either `Trend continuation` or `Liquidity sweep reversal`?
   If no:
   no trade
4. Did price either reclaim the level or break a meaningful `30m` pivot after reacting there?
   If no:
   no trigger
5. Is invalidation clear and structural?
   If no:
   no trade
6. Is projected reward at least `2R` after spread and realistic execution cost?
   If no:
   no trade

## What Does Not Count As A Trigger

- hesitation at a level
- one dramatic wick without confirmation
- "momentum looks weaker"
- "it feels tired"
- a pretty candle in the middle of a range

If behavior has not changed, there is no trigger.

## Setup Library

You only need two playbooks.

### Playbook 1: Pullback Continuation

Use when:

- `Daily` and `4H` trend are aligned
- session pulls price into a pre-marked continuation zone

Entry:

- `30m` reclaim or micro structure break in trend direction

Target:

- next intraday or `1H` structure
- minimum `2R`

### Playbook 2: Sweep and Reversal

Use when:

- price reaches a major `Daily` or `4H` level
- session sweeps that level
- reclaim or structure shift confirms rejection

Entry:

- `30m` reclaim or micro structure break away from the swept level

Target:

- opposing intraday structure first
- extended target only if reversal has room

## What Happens to the Old Named Patterns

- `Last Kiss` becomes one subtype of continuation reclaim
- `Big Shadow` becomes one subtype of exhaustion rejection
- `Wammie / Moolah` becomes one subtype of sweep-and-reversal logic
- `QQE / QMP` is dropped

This is cleaner.

You keep the useful market ideas and remove the clutter.

## Entry Rules

Enter only if all are true:

- pair is on watchlist
- session is active
- no immediate Tier-1 event window is active
- price is at a pre-marked level
- trade fits either continuation or sweep/reversal context
- one of the two triggers prints cleanly
- entry is taken with a stop order after confirmation, not by chasing market
- stop can be placed at structural invalidation
- target offers at least `2R`

No entry:

- in the middle of the move
- after the candle has already expanded too far
- because of fear of missing out
- because you redrew the level after the fact

Operational rule:

- if you cannot point to the exact level and the exact trigger candle, you are not allowed to enter

## Risk Rules

Use current rebuild rules until proven otherwise:

- `0.25%` risk per trade
- maximum `2` trades per day
- maximum `1` open position at a time

Use your stricter actual caps:

- daily max loss: `0.50%`
- weekly max loss: `1.50%`

If first trade is rule-broken:

- stop for the day

If first trade is a clean loss:

- one more trade maximum

If session conditions are abnormal:

- reduce activity by skipping trades, not by changing risk rules

## Stop Placement

Stop goes:

- beyond the reclaim extreme
- beyond the sweep extreme
- beyond the invalidating swing point

Default volatility buffer:

- `0.5 x ATR(14)` on `30m`

Rules:

- use the same default buffer unless you later validate a different standard in testing
- if the structural stop plus default buffer is too wide for acceptable size, skip the trade
- if spread or volatility is abnormal, skip the trade rather than widening the stop

Operational stop rules:

- for `Level reclaim` longs:
  stop goes below the reclaim low plus buffer
- for `Level reclaim` shorts:
  stop goes above the reclaim high plus buffer
- for `Micro structure break` longs:
  stop goes below the defended swing low plus buffer
- for `Micro structure break` shorts:
  stop goes above the defended swing high plus buffer

Never:

- widen the stop after entry
- move the stop farther because price is "almost coming back"
- compress the stop so much that the structure no longer makes sense

## Profit Model

Default:

- full target at `2R`

Why:

- simple
- measurable
- suits backtesting
- avoids over-management

Break-even reminder:

- with a fixed `+2R / -1R` model, the strategy must win above roughly `33%` before costs to have positive expectancy
- that means journaling must track realistic net `R`, not just chart-perfect outcomes

Optional later:

- partial at `1.5R`
- trail remainder behind `30m` or `1H` structure

Do not add this now.

First prove you can execute the simple version.

## Exit Rules

Use only four exit types:

### 1. Hard Stop

- if price hits structural invalidation, exit
- no widening
- no second guessing

### 2. Fixed Target

- default target is full exit at `2R`
- this remains the baseline for replay, demo, and record keeping

### 3. Early Premise-Failure Exit

This exit is allowed only if the original trade thesis is objectively broken before stop is hit.

Examples:

- breakout trade closes back inside the range
- reclaim trade immediately loses the reclaimed level
- micro structure break trade breaks, then reverses back through the broken pivot
- price starts accepting the opposite side of the level

This exit is not allowed for:

- normal pullbacks
- fear after entry
- boredom
- wanting to avoid taking a full `-1R`

If you exit early, you must be able to state:

- what specific condition failed

### 4. Time Stop

If after `3-5` closed `30m` candles:

- price has made no meaningful progress
- the trade is stale
- the original premise is weakening

then a flat or reduced-risk exit is allowed.

## Trade Management Rules

For now, manage trades simply:

- place entry, stop, and target immediately
- do not scale in
- do not add to losers
- do not take partials by default

Break-even rule:

- move to break-even only after price reaches at least `+1R`
- do not move to break-even too early just to feel safe
- if structure still needs room, leave the original stop

Early exit rule:

- if the reason for entry is gone, exit
- if the reason is still valid, stay in

Default rule for first-time execution:

- unless premise failure is obvious, let the trade hit either stop or `2R`

## Breakout-Specific Failure Rules

If you entered because of breakout logic, exit early if:

- price closes back inside the broken range
- the breakout level is lost immediately
- follow-through disappears and the market accepts back inside prior structure

If those things do not happen, do not panic-exit only because price hesitates.

## First-Time Trader Rules

If you were starting today, your exact operating rules would be:

1. Trade only `EURUSD`, `GBPUSD`, and `USDJPY`
2. Mark only approved `Daily` and `4H` level families before the session
3. Check the economic calendar before the session starts
4. Wait for price to reach a pre-marked level
5. Trade only `Trend continuation` or `Liquidity sweep reversal`
6. Trigger must be either `Level reclaim` or `Micro structure break`
7. Use `30m` only for trigger and management
8. Place structural stop plus default `0.5 x ATR(14)` buffer
9. Take full profit at `2R` by default
10. Move to break-even only after `+1R`
11. Exit early only if the premise is objectively broken
12. Maximum `2` trades per day
13. Maximum `1` open position at a time
14. Stop for the day after `0.50%` loss

If any one of those rules is not met:

- no trade

## What Sustainable Means for You

For your profile, sustainable does not mean:

- catching every move
- high win rate alone
- trading many times a day

It means:

- enough opportunities each week to learn and compound skill
- low enough complexity to stay disciplined
- positive expectancy after costs and mistakes
- no single bad day destroying progress

## Professional Mentoring Guidance

If I were coaching you directly, I would insist on the following:

### Rule 1

Stop searching for a magical trigger.

There is no candle that will rescue bad location.

### Rule 2

Choose your lane.

If you can trade only a few hours a day, build a session model.

Do not use a full-day swing trigger framework and then complain that you miss moves.

That is a mismatch, not a strategy failure.

### Rule 3

Trade one repeated behavior, not many named setups.

You need repetition.

Repetition builds pattern recognition, confidence, and data.

### Rule 4

Win rate is not the first question.

The first question is:

- does the strategy produce positive expectancy after your actual execution behavior?

That said, for your psychology, a very low win-rate system is not ideal at this stage.

You likely need a model that can realistically live in the roughly `40%` to `55%` win-rate area with `2R` style asymmetry or mixed management.

### Rule 5

Your real enemy is not missing trades.

Your real enemy is:

- forcing trades
- widening risk
- re-entering emotionally
- changing style every two weeks

## Daily Workflow

### Before Session

1. Mark `Daily` bias.
2. Mark approved `4H` structure levels and zones.
3. Mark prior day and relevant session reference levels.
4. Check the economic calendar for Tier-1 releases affecting your pairs.
5. Write only two scenarios per pair:
   - continuation from zone
   - sweep and reversal from extreme
6. Set alerts.

### During Session

1. Wait for price to reach level.
2. Watch only for reclaim or micro structure break.
3. Use stop orders only after the trigger candle closes.
4. Place stop, target, and invalidation immediately.
5. Do not invent a third setup.

### After Session

1. Screenshot the trade or missed setup.
2. Journal:
   - pair
   - session
   - context
   - level family
   - trigger
   - grade
   - `R`
   - news tag
   - emotional state
3. End the workday.

## Study and Backtesting Plan

Backtest by pair and session, not just by pattern name.

Test separately:

- `EURUSD` London
- `GBPUSD` London
- `USDJPY` London
- `USDCAD` New York only if relevant

For each pair, track:

- opportunities per week
- win rate
- average win
- average loss
- net `R`
- max losing streak
- missed valid setup count
- hours held
- event-risk tag
- spread or execution notes when relevant

Do not optimize for frequency alone.

Optimize for:

- repeatability
- clarity
- behavioral fit
- positive results after realistic costs

## Tooling Principle

If you build TradingView tools for this model, use them as execution infrastructure, not black-box signal generators.

Useful tooling should focus on:

- session window shading
- pre-marked level display
- event-risk warning
- reclaim and micro-break validation markers
- journal and screenshot prompts

The tool should help enforce the process.

It should not encourage random extra trades.

## Recommendation

If you want my professional guidance in one sentence:

- become a session-based level-and-structure trader with only two playbooks and two triggers, then master that before adding anything else.

## Next Build Steps

The logical next deliverables are:

1. a one-page execution checklist for this session model
2. a chart-marking template for pre-session planning
3. a TradingView indicator specification for:
   - session windows
   - approved level families
   - event-risk blocking
   - `30m` reclaim and micro-break triggers
4. a backtesting sheet template aligned to this model
