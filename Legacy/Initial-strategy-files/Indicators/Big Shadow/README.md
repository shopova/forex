# Big Shadow Indicator Project Summary

## Objective
Build a TradingView Pine Script (v6) Big Shadow indicator aligned with:
- Naked Forex Big Shadow rules
- `The big shadow.md`
- repository strategy and execution documents

## Source Documents Used
- `The big shadow.md`
- `Trading handbook.md`
- `Trade Execution Checklist.md`
- `Legacy/Initial-strategy-files/Dual-Methodology Strategy for Major Pairs.md`
- `Trader Profile Context.md`

## Current Main Script
- `big_shadow_indicator_v6.pine`
- `big_shadow_indicator_mt5.mq5`

## Rule Mapping Implemented
- Profile mode switch:
  - `Balanced` (default): relaxed gating for better frequency
  - `A+ Strict`: strict checklist gating
  - `Custom`: uses manual toggle inputs
- Pair preset mode:
  - `MT5 Per-Pair >=2R (2020-2026)` (default): auto-applies tested per-pair settings for `EURUSD`, `GBPUSD`, `USDCAD`, `USDJPY`
  - `Off (Manual Inputs)`: uses input values directly
- Two-candle Big Shadow structure with second candle as the signal.
- Optional strict outside-bar rule (`higher high + lower low` vs previous candle).
- Dominance rule (largest range vs previous 5 or previous 10 candles).
- Close quality filter:
  - bullish close must be near high
  - bearish close must be near low
  - tolerance configurable in ticks and ATR
- Zone confluence filter using auto pivots (support/resistance).
- Extreme-location filter (signal at local extreme, default OFF).
- Room-to-the-left filter (default 7 bars, default OFF).
- Stop-entry execution:
  - bullish: Buy Stop above Big Shadow high
  - bearish: Sell Stop below Big Shadow low
- Stop-loss beyond opposite Big Shadow extreme with buffer.
- Trigger window modes:
  - `Next Candle (A+)`
  - `Within N Candles`
- Target modes:
  - `Nearest Zone`
  - `R Multiple` (default, minimum `2.0R`)
- Setup validation gate:
  - setup is accepted only if projected reward-to-risk is at least `Minimum Setup R` (default `2.0R`)
- Optional breakeven event at +R.
- Alerts for setup ready, entry triggered, setup canceled, breakeven, target hit, and stop hit.

## Default Settings Snapshot
- `profileMode`: `Balanced`
- `pairPresetMode`: `MT5 Per-Pair >=2R (2020-2026)`
- `triggerMode`: `Next Candle (A+)` (manual value; per-pair preset may override)
- `dominanceMode`: `Previous 10 Candles (A+)` (manual value; per-pair preset may override)
- `useZoneFilter`: `false` (manual value; per-pair preset keeps this OFF for supported pairs)
- `requireExtreme`: `false` (manual value; per-pair preset enables only for EURUSD)
- `useRoomLeftFilter`: `false` (manual value; per-pair preset keeps this OFF for supported pairs)
- `roomLeftBars`: `7` (manual value)
- `targetMode`: `R Multiple`
- `targetRR`: `2.0` (minimum allowed)
- `minSetupRR`: `2.0` (minimum allowed)
- `useTrendFilter`: `true` (manual value; per-pair preset disables trend filter for supported pairs)
- `useSessionFilter`: `false`

## Profile Behavior
- `Balanced` enforces:
  - `requireExtreme = false`
  - `useRoomLeftFilter = false`
  - `useSessionFilter = false`
- `A+ Strict` enforces:
  - `requireExtreme = true`
  - `useRoomLeftFilter = true`
  - `useSessionFilter = true`
- `Custom`:
  - Uses the manual values of those three inputs directly.

## MT5 Per-Pair Preset (Updated 2026-02-25)
- Backtest scope used for calibration:
  - Pair files: `EURUSD_H1_2020-2026-02-23.csv`, `GBPUSD_H1_2020-2026-02-23.csv`, `USDCAD_H1_2020-2026-02-23.csv`, `USDJPY_H1_2020-2026-02-23.csv`
  - Full period: `2020-01-02` to `2026-02-23` (1H bars)
  - Constraint: `targetRR >= 2.0` and `minSetupRR >= 2.0`
- Result:
  - No single universal configuration achieved `>= +2R` net on all 4 pairs simultaneously.
  - Per-pair preset mode was added to enforce settings that each reach at least `+2R` net on their own pair.
  - Python backtest runner mirrors this via `--bs-pair-preset-mode "MT5 Per-Pair >=2R (2020-2026)"`.
- Per-pair outcomes (net R):
  - `EURUSD`: `+2.0R`
  - `GBPUSD`: `+15.0R`
  - `USDCAD`: `+7.0R`
  - `USDJPY`: `+15.0R`
- Execution defaults still enforce minimum `+2R` setup quality:
  - `targetMode = R Multiple`
  - `targetRR >= 2.0`
  - `minSetupRR >= 2.0`

## Important Notes
- Auto zones are pivot-based approximations. Manual zone marking can still be superior in discretionary review.
- The script is an indicator with setup/management logic and alerts, not a broker-executing strategy.
- If `Target Mode` is switched to `Nearest Zone` and no valid zone exists, target falls back to R-multiple logic.
- Pair preset mode is calibrated only for `EURUSD/GBPUSD/USDCAD/USDJPY` on the backtest period above; use `Off (Manual Inputs)` for other symbols.

## MT5 Port Notes
- `big_shadow_indicator_mt5.mq5` ports the same Big Shadow trigger, preset, pending-order, and trade-management workflow to a MetaTrader 5 custom indicator.
- The MT5 version evaluates confirmed bars, then extends the active pending/trade levels onto the live bar for chart visibility.
- Event markers and alerts are preserved; session filtering uses broker server time.

## Suggested Validation Workflow
1. Paste script into TradingView and confirm compile.
2. Test on your execution timeframe (primarily 1H) using replay.
3. Compare generated setups against checklist A+ criteria.
4. Tune close tolerance and zone tolerance per pair volatility.
