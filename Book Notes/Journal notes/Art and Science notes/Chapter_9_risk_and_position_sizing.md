# Section Note: Art and Science of Technical Analysis

Source:
- `Reading-materials/some-investment-books/New Folder/The Art and Science of Technical Analysis - Market Structure, Price Action, and Trading Strategies 2012 - annotated.pdf`

Parent chapter:
- `Chapter 9: Risk Management`

Section focus:
- `Risk and Position Sizing`

## Core Idea

- The first practical job of risk management is simple:
  - know where the trade is wrong
  - know how much money that loss represents
  - size the position so the loss fits the account
- The stop defines the per-unit risk.
- The position size converts that structural risk into an acceptable account risk.

## Key Points

- `Always know the loss before entry`
  - Grimes treats this as the one rule that cannot be broken.
  - A trade is not ready until the invalidation point is defined in advance.

- `Stops must sit outside noise`
  - Very tight stops often sit inside normal fluctuation.
  - If the stop is closer than roughly one average bar range, it is often just noise management, not thesis invalidation.

- `Size from the stop, do not move the stop for convenience`
  - You do not get to choose the stop based on how much you want to lose.
  - The pattern dictates the stop.
  - The trader controls the money risk by changing the position size.

- `Fixed fractional is robust`
  - Risking a consistent percent of equity is not optimized, but it is practical.
  - It helps control:
    - single bad losses
    - losing streaks
    - account-level damage
    - scaling as equity changes

- `Aggressive sizing looks better on paper than it feels in real life`
  - More risk per trade can produce more profit.
  - But volatility, deep drawdowns, and bankruptcy risk rise faster than most traders expect.
  - The drawdown recovery math becomes brutal very quickly.

- `Think in R`
  - The initial risk creates the base unit for the trade.
  - This helps evaluate performance without getting emotionally attached to nominal money swings.

## What This Changes For Me

- A tighter stop is not automatically a lower-risk trade.
- If structure needs a wider stop, the answer is smaller size, not a forced tighter stop.
- Per-trade risk must be chosen with losing streaks and rare larger-than-expected losses in mind, not only best-case expectancy.

## Rule Extracted

- `The market sets the stop through structure; I set the account risk through position size.`

## Practical Forex Translation

- For FX, the stop should usually sit beyond:
  - the pullback low/high
  - the retest failure point
  - the liquidity sweep extreme
  - or the structure level that invalidates the setup
- Then calculate lot size from:
  - account risk
  - stop distance in pips
  - pair-specific pip value
- This directly supports your current process:
  - structural stop first
  - fixed percent risk second
  - reject the trade if the required stop destroys the setup `R`
