# Trigger Types and Definitions

Use this as the quick reference for what counts as a trigger in your current framework.

Core rule:

- context decides whether the setup matters
- trigger decides when to act
- no trigger is valid without a meaningful level and structural invalidation

Current execution stack:

- `Daily`: bias
- `4H`: market condition and key level
- `30m`: trigger

## Core Trigger Families

### 1. Level Reclaim

Definition:

- price trades through a meaningful level
- then closes back through it
- entry is taken only after the market shows re-acceptance

What it looks like:

- failed break of support, then close back above
- failed break of resistance, then close back below
- breakout retest that holds and re-accepts

Use it for:

- `Liquidity sweep reversal`
- `Last Kiss breakout retest`
- `Failed breakout response`

Not enough by itself:

- one wick through the level without a convincing close
- multiple weak closes around the level
- chop with no clear acceptance

Books / notes:

- [Chapter_6_failure_test.md](/Users/rositsashopova/Documents/Projects/forex/Book%20Notes/Journal%20notes/Art%20and%20Science%20notes/Chapter_6_failure_test.md)
- [Chapter_6_failed_breakouts.md](/Users/rositsashopova/Documents/Projects/forex/Book%20Notes/Journal%20notes/Art%20and%20Science%20notes/Chapter_6_failed_breakouts.md)
- [Chapter_5_breakout_trade_trading_range_to_trend.md](/Users/rositsashopova/Documents/Projects/forex/Book%20Notes/Journal%20notes/Art%20and%20Science%20notes/Chapter_5_breakout_trade_trading_range_to_trend.md)
- [last_kiss.md](/Users/rositsashopova/Documents/Projects/forex/Reading%20Materials/some-investment-books/books/last_kiss.md)

### 2. Micro Structure Break

Definition:

- price reacts at a meaningful level
- then breaks the last meaningful local pivot in the intended direction
- entry is taken on the break or first controlled retest

What it looks like:

- bullish: support holds, then price breaks the last `30m` lower high
- bearish: resistance holds, then price breaks the last `30m` higher low

Use it for:

- `Trend continuation`
- `Countertrend support reaction`
- `Countertrend resistance reaction`
- selective reversal work only after real change of behavior

Not enough by itself:

- candle looks strong but no actual pivot break exists
- market is still inside noisy overlap
- the pivot broken is too minor to matter

Books / notes:

- [Chapter_6_pullback_entering_lower_time_frame_breakout.md](/Users/rositsashopova/Documents/Projects/forex/Book%20Notes/Journal%20notes/Art%20and%20Science%20notes/Chapter_6_pullback_entering_lower_time_frame_breakout.md)
- [Chapter_6_pullback_buying_support_or_shorting_resistance.md](/Users/rositsashopova/Documents/Projects/forex/Book%20Notes/Journal%20notes/Art%20and%20Science%20notes/Chapter_6_pullback_buying_support_or_shorting_resistance.md)
- [Chapter_3_trend_analysis.md](/Users/rositsashopova/Documents/Projects/forex/Book%20Notes/Journal%20notes/Art%20and%20Science%20notes/Chapter_3_trend_analysis.md)
- [Chapter_3_on_trends.md](/Users/rositsashopova/Documents/Projects/forex/Book%20Notes/Journal%20notes/Art%20and%20Science%20notes/Chapter_3_on_trends.md)

## Secondary Visual Forms

These are not separate trigger families. They are visual subtypes that must resolve into `Level Reclaim` or `Micro Structure Break`.

- `Last Kiss`
- `Big Shadow`
- `Wammie / Moolah`
- `Breakout retest`
- `Failed breakout`

Useful references:

- [big_shadow.md](/Users/rositsashopova/Documents/Projects/forex/Reading%20Materials/some-investment-books/books/big_shadow.md)
- [naked_forex.md](/Users/rositsashopova/Documents/Projects/forex/Reading%20Materials/some-investment-books/books/naked_forex.md)
- [Correction Quality Guide.md](/Users/rositsashopova/Documents/Projects/forex/Reading%20Materials/Correction%20Quality%20Guide.md)
- [Impulse Identification Guide.md](/Users/rositsashopova/Documents/Projects/forex/Reading%20Materials/Impulse%20Identification%20Guide.md)

## What Is Not a Trigger

- hesitation at a level
- a dramatic wick with no confirmation
- a nice candle in the middle of a range
- “it feels tired”
- “momentum looks weaker” without a reclaim or pivot break

If behavior has not changed, there is no trigger.

## Trigger Checklist

Before entry, confirm:

1. meaningful `Daily` or `4H` level
2. context is clear
3. trigger on `30m` is complete, not anticipated
4. invalidation is structural
5. target still offers at least `2R`

## Simple Journal Language

Use these phrases:

- `Level reclaim above support`
- `Level reclaim below resistance`
- `Break above last 30m lower high`
- `Break below last 30m higher low`
- `No trigger`

Avoid these vague phrases:

- `momentum weakened`
- `looked tired`
- `nice rejection`
- `probably reversing`

## Default Mentoring Rule

- if there is no reclaim and no real micro structure break, the trade is not confirmed
- if the setup is still interesting, label it `Pattern study only`
