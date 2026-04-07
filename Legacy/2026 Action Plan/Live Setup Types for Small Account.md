# Live Setup Types for Small Account

## Purpose

This file defines which setups are suitable for the current live account and which should stay in demo, replay, or study.

It is built around:

- `Initial-strategy-files/Clean Slate FX Strategy v2 - Session Model.md`
- `Legacy/2026 Action Plan/MT5 Live Trading Plan - 387.50 EUR.md`
- journal notes from `The Art and Science of Technical Analysis`
- the broader reading direction of the current book stack

## Core Idea

The account is small, so the best live setup is not the most exciting setup.

The best live setup is the one that combines:

1. clear market phase
2. clear structure
3. compact invalidation
4. realistic `2R`
5. low decision stress

The journal notes point to the same conclusion repeatedly:

- classify the market phase first
- favor trend continuation over early termination
- trade level failure only after real acceptance
- treat transition and complex pullbacks with suspicion

## Market Phase Priority

Based on the Grimes notes, every setup should be assigned to one of these states first:

- `trend`
- `range`
- `transition / uncertain`

For this account:

- `trend` is the best environment for live trading
- `range` is acceptable only at the edge, never in the middle
- `transition / uncertain` is usually not a live-trading environment

## Live Setup Tier 1

These are the best-fit live setups for the current account.

### 1. Trend Continuation After Healthy Pullback

Why it is preferred:

- it is the clearest trade category from the journal notes
- continuation is more repeatable than early reversal
- it usually allows tighter, cleaner invalidation

What must be true:

- `Daily` and `4H` show a clear trend
- prior impulse is real, not weak drift
- pullback is corrective, not aggressive
- with-trend structure is still intact
- no climax or obvious late-stage exhaustion
- entry comes from a meaningful level
- stop fits the live-account cap at `0.01` lot

Good live examples:

- `EURUSD` pullback continuation with `7-10` pip stop
- `USDJPY` continuation with `10-16` pip stop

Best trigger types:

- level reclaim in trend direction
- micro structure break after the pullback stalls

### 2. Breakout Acceptance and Retest

This is the clean live version of a `support / resistance failing` trade from the Grimes notes.

Why it is preferred:

- the structure is easier to explain
- the invalidation can be compact
- it fits the idea that a break matters only if price is accepted beyond the level

What must be true:

- a meaningful level breaks
- price holds outside the level
- retest shows acceptance, not immediate rejection back into range
- the retest is not occurring in messy transition structure
- reward remains at least `2R`
- stop fits the live-account cap

Pattern translation:

- `Last Kiss` belongs here when the break is real and the retest is clean

### 3. Compact Sweep Reversal at a Major Extreme

This is the only reversal-type live setup that should stay on the list for now.

Why it is secondary, not primary:

- reversal trades are harder
- many need wider stops
- many happen in transition, which the notes repeatedly treat as deceptive

What must be true:

- price is at a real `Daily` or `4H` extreme
- the move into the level looks stretched, climactic, or vulnerable
- the sweep fails quickly
- reclaim or structure shift appears fast
- stop is still compact enough for the live account

Pattern translation:

- selective `Wammie / Moolah`
- selective `Big Shadow`

This setup is live-eligible only when it is unusually clean.

## Demo / Replay Tier

These setups can still be useful for study, but they are not good default live setups for this account.

### 1. Trend Termination Trades

Why they move to demo:

- the journal notes explicitly frame termination as harder and less forgiving
- they are easy to label too early
- they often need more interpretation and more room

Examples:

- shorting the first stall after a strong uptrend
- buying the first bounce after heavy markdown

### 2. Complex Pullback Setups

Why they move to demo:

- the notes warn that complex pullbacks often look tradable before they fail
- the first failed continuation attempt is a major warning sign
- they are exactly the kind of chart that creates emotional overtrading

Examples:

- second-entry continuation in messy overlap
- continuation after a failed first push

### 3. Wide-Stop Rejection Setups

Why they move to demo:

- the live account cannot absorb wide invalidation
- forcing a narrow stop on a wide pattern destroys the setup logic

Examples:

- `Big Shadow` with a large candle range
- `Last Kiss` where the true invalidation is too far away
- `Wammie / Moolah` where first-touch to second-touch distance is too large

## Avoid Completely

These should not be traded live and should rarely even be simulated as serious candidates.

### 1. Middle-of-Range Trades

Reason:

- the notes are explicit that the middle of the box has no edge

### 2. Transition / Uncertain Structure

Reason:

- this is where false continuation and false reversal are both common
- the notes repeatedly warn against forcing clean labels onto uncertain structure

### 3. First Breakout Spike Without Acceptance

Reason:

- a break is not a failure trade until price is accepted beyond the level
- a wick beyond a level is not enough

### 4. Trades That Need Stop Compression

Reason:

- if the setup needs a `15`-pip stop but the account allows only `10`, the solution is not to cheat the stop

### 5. Trades With Conflicting Higher-Timeframe Context

Reason:

- your notes already extracted this rule: when current timeframe conflicts with higher timeframe, the higher timeframe is likely to take control

## Pattern Ranking for the Current Live Account

### Best Live Fit

1. `Continuation reclaim`
2. `Continuation micro structure break`
3. `Accepted breakout retest / Last Kiss`

### Secondary Live Fit

1. `Compact liquidity sweep reversal`
2. `Small and clean rejection candle at major extreme`

### Mostly Demo / Replay

1. `Big Shadow`
2. `Wammie / Moolah`
3. `early reversal / termination`

This does not mean those patterns are bad.

It means they are a weaker fit for:

- this account size
- this stage of development
- this need for clean repetition

## Pair Fit

For the live account:

- `EURUSD`: best overall
- `USDJPY`: strong second choice
- `GBPUSD`: conditional, only if stop is compact and spread is normal
- `USDCAD`: better for study and demo than live for now

## Daily Selection Order

Use this order every day:

1. classify the market phase
2. decide whether the pair is trend, range edge, or transition
3. choose the trade category:
   - continuation
   - level failing
   - holding
   - termination
4. reject anything in `transition / uncertain`
5. measure the real stop at `0.01` lot
6. reject anything too large for the account
7. only then consider the trigger

This order matters.

The books and your notes both point to the same mistake:

- traders focus on the candle first and the market context second

## Journal Labels

To make review easier, label every setup with one of these:

- `Tier 1 live continuation`
- `Tier 1 live breakout retest`
- `Tier 1 live compact sweep`
- `demo-only termination`
- `demo-only complex pullback`
- `demo-only wide stop`
- `invalid transition`
- `invalid middle of range`

## Bottom Line

For the current live account, you are not trying to prove that you can trade every pattern.

You are trying to prove that you can:

- read phase correctly
- choose the simplest trade category
- take only setups that fit the account
- skip attractive but oversized or ambiguous trades

That is the professional path for a small real account.
