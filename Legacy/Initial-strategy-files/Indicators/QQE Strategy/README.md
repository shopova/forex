# QQE / QMP Strategy

This folder now includes a standalone Pine Script v6 strategy for the lower-risk `Method No. 1` version of the QQE / QMP workflow:

- Strategy file: `QQE Strategy/qqe_qmp_strategy_v6.pine`
- Supporting indicators: `QMP-indicator.pine`, `QQE-adv.pine`, `Macd-platinum.pine`
- Python backtest mirror: `backtesting/run_qqe_qmp_backtests.py`

## What It Implements

- Reuses the existing `QMP Filter` signal semantics already coded in `QMP-indicator.pine`.
- Keeps the book-aligned signal sequence:
  - `MACD Platinum` bullish dot below zero, then bullish `QQE Adv` sync for longs.
  - `MACD Platinum` bearish dot above zero, then bearish `QQE Adv` sync for shorts.
  - Signals confirm on candle close.
- Defaults to the lower-risk `Method No. 1` model:
  - single position only
  - hard stop on every trade
  - fixed `R Multiple` target
  - optional move to breakeven at `+1R`
  - optional early exit on opposite QMP signal

## Default Risk / Filter Bias

To stay aligned with the stricter repository rules, the strategy defaults are intentionally tighter than the source book:

- `Risk Per Trade (% of Equity) = 0.50`
- `Use Daily 200 SMA + H4 50 EMA Filter = true`
- `Use Session Filter = true`
- `Trading Session = 0700-1700`
- `R Multiple Target = 2.0`
- `Minimum Allowed Target R = 2.0`

The original book-style internal QMP filter is still preserved:

- `Require 50/100/240 Trend Stack = true`
- `Use Higher Time Frame QMP Filter = false` by default

## Entry / Stop Behavior

- `Entry Mode = Next Bar Open (Book)` is the default and submits the order after the signal closes, so TradingView backtests fill it on the next bar open.
- `Signal Candle Break Stop` is available if you want the strategy to match your broader stop-order-only execution preference.
- Stop placement can be chosen from:
  - signal candle extreme plus ATR buffer
  - recent swing plus ATR buffer
  - 50 EMA / 100 EMA / 240 LWMA plus ATR buffer

## How The Scripts Work

### `QMP-indicator.pine`

This is the signal-layer script. It does not place trades. It marks when the QQE / QMP setup is present and whether that setup is tradable or blocked.

The internal flow is:

- `MACD Platinum` builds directional bias using the zero-lag `12/26/9` MACD logic.
- A bullish MACD trigger is only accepted when the bullish crossover happens below the zero line.
- A bearish MACD trigger is only accepted when the bearish crossover happens above the zero line.
- The most recent accepted MACD trigger defines the active bias: long bias or short bias.
- `QQE Adv (1, 8, 3)` then provides the timing trigger using `RSI(8)` and its adaptive QQE band.
- A raw long sync happens when MACD is already in long bias and QQE prints a fresh bullish cross.
- A raw short sync happens when MACD is already in short bias and QQE prints a fresh bearish cross.
- The raw sync is then filtered by the `50 EMA / 100 EMA / 240 LWMA` trend stack.
- If enabled, the raw sync is also filtered by higher-time-frame QMP state via `request.security`.
- The script always plots the raw sync dot, but changes the color depending on whether the signal passes the filters.

In practice:

- Green buy dot = raw long sync passed the filter stack and is tradable.
- Red sell dot = raw short sync passed the filter stack and is tradable.
- Yellow dot = raw sync happened, but the filter stack blocked it.

This is why the indicator is useful even when it blocks signals: you can still see the raw momentum events, but the script distinguishes them from the setups you would actually trade.

### `QQE-adv.pine` and `Macd-platinum.pine`

These scripts are the component references behind the QMP logic.

- `QQE-adv.pine` provides the QQE band and cross behavior used for timing.
- `Macd-platinum.pine` provides the MACD dot logic used for directional bias.
- `QMP-indicator.pine` combines the two into a single chart-level confirmation model.

They are useful when you want to inspect the source calculations separately, but the actual QMP signal decision is made by `QMP-indicator.pine`.

### `qqe_qmp_strategy_v6.pine`

This is the execution-layer script. It takes the QMP signal logic and converts it into an actual strategy with entries, stops, exits, and risk handling.

The strategy flow is:

- It reuses the same QMP signal sequence as the indicator.
- It then adds stricter repo-level filters.
- Daily `200 SMA` plus H4 `50 EMA` macro trend confirmation keeps trades aligned with the broader trend.
- `0700-1700` trading-session restriction removes out-of-session entries.
- A minimum allowed target threshold keeps the configured target at or above the required `R`.
- When a valid setup closes, the default entry is submitted for the next bar open.
- Position size is calculated from `Risk Per Trade (% of Equity)` and the distance between entry and stop.
- The default stop is based on the signal candle extreme plus an ATR buffer, although other stop modes are available.
- The target is set at a fixed `R Multiple`, default `2R`.
- If price reaches `+1R`, the script can move the stop to breakeven.
- If an opposite raw QMP signal appears, the script can close the trade early.
- A MACD zero-line exit is available as an optional additional exit rule.

The strategy is intentionally conservative:

- single position only
- hard stop always present
- no basket logic
- no scale-in logic

That keeps it aligned with the lower-risk `Method No. 1` workflow rather than the higher-risk book variants.

### `run_qqe_qmp_backtests.py`

This is the Python mirror used to test the default QQE / QMP behavior on local MT5 CSV files outside TradingView.

The runner:

- reads MT5 OHLC data from `Backtesting Data/*.csv`
- rebuilds the QMP signal sequence from the Pine logic
- applies the default strategy execution rules from `qqe_qmp_strategy_v6.pine`
- uses next-bar-open entries by default
- tracks stop, target, breakeven, and opposite-signal exits
- writes `summary.json` and `trades.csv` for each pair separately

The goal of the Python runner is not to replace TradingView. Its purpose is to make per-pair validation faster and reproducible on your local data so you can compare pairs, tune rules, and inspect trade-by-trade `R` outcomes.

## Indicator Alerts

`QQE Strategy/QMP-indicator.pine` now exposes these alertconditions:

- `QMP Signal`: combined tradable alert for any valid long or short QMP signal
- `QMP Buy`: tradable long signal only
- `QMP Sell`: tradable short signal only
- `QMP Buy Blocked`: raw long sync detected, but blocked by the filter stack
- `QMP Sell Blocked`: raw short sync detected, but blocked by the filter stack

This keeps raw syncs visible while still allowing a single TradingView alert to be attached for any tradable QMP setup.

## Important Constraints

- This script is a lower-risk automation layer only. It does **not** implement the book’s `Method No. 2` basket / no-hard-stop behavior.
- It is intentionally single-position (`pyramiding = 0`) to stay conservative and avoid sequence stacking risk.
- News filtering is not automated in Pine here; that remains discretionary.

## Python Backtest Mirror

`backtesting/run_qqe_qmp_backtests.py` mirrors the default `Method No. 1` execution profile on local MT5 CSV data:

- QMP signal timing follows `QMP-indicator.pine`
- execution defaults follow `qqe_qmp_strategy_v6.pine`
- default target is `2R`
- breakeven moves to entry at `+1R`
- opposite QMP signals can force an early exit
- results are written per pair, not as a single aggregate

Current default MT5 per-pair baseline from the local runner:

- `EURUSD`: `272` closed trades, `24.63%` win rate, `-18.00R`
- `GBPUSD`: `289` closed trades, `23.88%` win rate, `-26.00R`
- `USDCAD`: `268` closed trades, `25.00%` win rate, `-8.00R`
- `USDJPY`: `238` closed trades, `28.57%` win rate, `+17.72R`

## When To Tune It

The first parameters worth tuning are:

- `Entry Mode`
- `Stop Mode`
- `ATR Stop Buffer`
- `Use Higher Time Frame QMP Filter`
- `Use Daily 200 SMA + H4 50 EMA Filter`
- `Trading Session`
