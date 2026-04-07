# MT5 Live Trading Plan - 387.50 EUR

## Purpose

This file is the live-account operating plan for the current MetaTrader account.

It is built for:

- account balance: `EUR 387.50`
- minimum order size: `0.01` lot
- current goal: rebuild discipline, confidence, and process on real money

This is not an aggressive growth plan.

It is a capital-preservation and process-building plan.

Related implementation note:

- see `2026 Action Plan/MT5 Session Model Alert EA README.md` for the current `EURUSD 15m` MT5 alert-EA installation, chart-markup, and usage workflow for this account phase

## Core Principle

At this account size, the `0.01` minimum lot is the main practical constraint.

That means:

- many structurally valid trades will still be too large for the account
- percentage risk rules must be translated into stop-size limits
- skipping oversized setups is part of the plan

The rule is simple:

If the smallest tradable size risks too much, the setup is not a live trade.

## Account Risk Numbers

Balance reference:

- `EUR 387.50`

Live-account limits:

- standard risk per trade: `0.25% = EUR 0.97`
- maximum daily loss: `0.50% = EUR 1.94`
- maximum weekly loss: `1.50% = EUR 5.81`
- maximum open positions: `1`
- maximum trades per day: `2`
- maximum trades per week: `6`

For this account, there is no need to size above `0.01` lot during the current rebuild phase.

## Lot-Based Risk Reality

Because `0.01` lot is the minimum size, live risk is controlled mainly by stop distance.

General formula:

`live risk in EUR = stop in pips x pip value in EUR at 0.01 lot`

If that result is above `EUR 0.97`, skip the trade in the real account.

## Approximate Pip Value at 0.01 Lot

These are approximate values for a `EUR` account using ECB euro reference rates from `2026-03-13`:

- `EURUSD`: about `EUR 0.0871` per pip at `0.01` lot
- `GBPUSD`: about `EUR 0.0871` per pip at `0.01` lot
- `USDJPY`: about `EUR 0.0547` per pip at `0.01` lot
- `USDCAD`: about `EUR 0.0636` per pip at `0.01` lot

Use these as planning values.

Before entering, still confirm the actual cash risk in the MT5 order window or calculator because pip value changes with price.

## Maximum Stop Size at 0.01 Lot

Using the `EUR 0.97` risk cap:

- `EURUSD`: about `11.1` pips maximum stop
- `GBPUSD`: about `11.1` pips maximum stop
- `USDJPY`: about `17.7` pips maximum stop
- `USDCAD`: about `15.2` pips maximum stop

These are mathematical maximums, not practical maximums.

For live trading, use slightly tighter operational caps to leave room for spread and slippage:

- `EURUSD`: `10` pips
- `GBPUSD`: `10` pips
- `USDJPY`: `16` pips
- `USDCAD`: `14` pips

If the required stop is wider than that, the trade is:

- valid for study, replay, or demo
- not valid for this live account

## Pair Selection for This Account

Default live pairs:

- `EURUSD`
- `USDJPY`

Conditional live pair:

- `GBPUSD` only if spread is normal and stop is within the live cap

Study / demo pair for now:

- `USDCAD`

Reason:

- `EURUSD` and `USDJPY` are the most practical for the current balance and time windows
- `GBPUSD` can still work, but stop-size tolerance is tighter
- `USDCAD` is better kept for study until New York observation becomes more consistent

## Live Entry Filter

A trade is live-eligible only if all of these are true:

1. it fits one of the two strategy contexts:
   - continuation from a meaningful level
   - liquidity sweep reversal from a meaningful level
2. the level was marked before the decision window
3. `Daily` and `4H` structure are clear
4. the `15m` trigger is clean
5. the stop is at true structural invalidation
6. the planned target is at least `2R`
7. `0.01` lot keeps the cash risk at or below `EUR 0.97`

If item `7` fails:

- do not reduce the stop artificially
- do not ignore the invalidation level
- do not trade live

## Position Sizing Rule

For this phase:

- trade only `0.01` lot live

Decision rule:

1. mark the setup
2. calculate the real stop distance in pips, including spread buffer
3. compare the stop distance to the pair cap
4. if it fits, live trade at `0.01`
5. if it does not fit, skip live and record it in the journal as:
   - `valid setup, too large for account`

## Examples

### Example 1: EURUSD continuation

- entry stop above reclaim candle
- structural stop: `8.5` pips
- lot size: `0.01`
- estimated cash risk: `8.5 x EUR 0.0871 = about EUR 0.74`

This is allowed.

### Example 2: EURUSD continuation with wider stop

- structural stop: `15` pips
- lot size: `0.01`
- estimated cash risk: `15 x EUR 0.0871 = about EUR 1.31`

This is not allowed live.

It may still be:

- a valid setup
- a valid demo trade
- a valid replay example

### Example 3: USDJPY sweep reversal

- structural stop: `14` pips
- lot size: `0.01`
- estimated cash risk: `14 x EUR 0.0547 = about EUR 0.77`

This is allowed.

## What This Means for the Strategy

The account size forces you toward:

- tighter, cleaner intraday structures
- fewer trades
- stronger selectivity
- better patience

It also means:

- not every good-looking `15m` setup is tradable live
- wide-stop reversal attempts will usually belong in demo, not live

That is acceptable.

The live account is for process validation, not for catching everything.

## Allowed Trade Types on This Account

Highest priority:

- `15m` continuation setups with compact invalidation
- `15m` sweep reversals only when the invalidation remains compact

Lower priority:

- trades that need a large box midpoint stop
- trades that need a very wide candle stop
- trades near major news

If a setup needs a wide stop to be valid, it is not suited to this account.

## Six-Month Live Trading Rules

For the next six months:

- no live position larger than `0.01` lot
- no more than `1` live trade open at any time
- no more than `2` live trades in one day
- no more than `6` live trades in one week
- no live trade if the setup was not planned before the session
- no phone entries
- no widening stops
- no same-session revenge re-entry

## Session Routine

Bulgarian time:

- primary decision window: `10:30-12:00`
- secondary management / preplanned execution window: `15:00-16:00`

Outside these windows:

- alerts are allowed
- management is allowed if already planned
- fresh discretionary live entries are not allowed

## When To Skip Live Trading Completely

Do not place a live trade if any of these are true:

- account risk at `0.01` lot is above `EUR 0.97`
- daily loss limit has been hit
- weekly loss limit has been hit
- you are emotionally urgent
- the setup is not clearly preplanned
- the chart is mid-range or messy
- major news is too close

## Journal Categories

Every watched setup should be labeled as one of these:

- `live taken`
- `valid but too large for account`
- `valid but missed`
- `invalid and correctly skipped`
- `invalid and wrongly considered`

This matters because the account size will force many correct skips.

You need data on that.

## Progression Rules

You do not move to `0.02` lot because of impatience.

For this rebuild phase, `0.02` lot is not allowed.

Review the rule only if all of these are true:

- balance is materially higher
- at least `40` live trades are complete
- risk behavior is clean
- expectancy is positive
- no major emotional slip is present

Even then, the increase must be written and justified before use.

## Bottom Line

This account should be traded as a precision account.

Your real edge right now is:

- selecting only the cleanest opportunities
- respecting the `0.01` lot constraint
- proving you can trade small without emotional distortion

That is the correct base for later FTMO trading.

## Source Note

Approximate pip-value planning uses ECB euro reference rates published on `2026-03-13`:

- USD: `1.1476` per EUR
- JPY: `182.85` per EUR
- CAD: `1.5726` per EUR

Source:

- https://www.ecb.europa.eu/stats/shared/pdf/eurofxref.pdf
