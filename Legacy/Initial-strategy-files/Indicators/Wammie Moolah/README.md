# Wammie / Moolah Indicator Project Summary

## Objective
Build a TradingView Pine Script (v6) indicator for **Wammies** and **Moolahs** aligned with:
- `Trading handbook.md`
- `Legacy/Initial-strategy-files/Dual-Methodology Strategy for Major Pairs.md`
- `Trade Execution Checklist.md`
- `Trader Profile Context.md`

## Current Main Script
- `wammie_moolah_indicator_v6.pine`
- `wammie_moolah_indicator_mt5.mq5`

## Rule Mapping Implemented
- Two-touch reversal framework at support/resistance.
- Zone confluence modes:
  - auto pivot zones (dynamic)
  - manual static support/resistance
  - zone filter fully off (pivot swing structure mode using confirmed swing highs/lows)
- Optional auto-zone freeze after first detection.
- In `Manual Static` mode, set explicit support/resistance values; `0` means "not set".
- **Wammie** logic:
  - first touch at support
  - second touch must be a **higher low**
  - second touch must stay within a configurable **max distance** from the first touch (default: 80 ticks / 0.80 ATR)
  - minimum candles between touches (default 4)
  - optional A+ spacing marker (default 20+)
- **Moolah** logic:
  - first touch at resistance
  - second touch must be a **lower high**
  - second touch must stay within a configurable **max distance** from the first touch (default: 80 ticks / 0.80 ATR)
  - minimum candles between touches (default 4)
- First-touch extreme filter (optional).
- Bounce-away-between-touches filter (optional).
- Chop filter using maximum interim zone retests.
- Catalyst candle quality:
  - body size filter (ATR-based)
  - close near extreme
  - rejection wick/body ratio
  - optional bull/bear candle color requirement
- Stop-entry execution:
  - Wammie: Buy Stop above bullish catalyst
  - Moolah: Sell Stop below bearish catalyst
- Stop-loss placement:
  - Wammie: below first (lower) touch + buffer
  - Moolah: above first (higher) touch + buffer
- Trigger window control:
  - `Within N Candles (3-5)` (default)
  - `Next Candle (A+)`
- Target modes:
  - `R Multiple` (default)
  - `Nearest Zone`
- Optional breakeven event at +R.

## Additional Strategy Filters Included
- Daily 200 SMA + H4 50 EMA trend filter (optional, enabled by default).
- Session filter (optional, enabled by default).
- MACD direction filter (optional).
- RSI overbought/oversold filter (optional).
- Room-to-the-left filter (optional, disabled by default).

## Current Default Profile (Best Strict, No-Zone)
- `Require Zone Confluence = false` (manual zone discretion outside script).
- Trend filter ON (`Daily 200 SMA + H4 50 EMA`) and session filter ON.
- `Target Mode = R Multiple`, `R Multiple Target = 2.0`.
- `Min Candles Between Touches = 4`.
- `Max Second-Touch Distance = 80 ticks / 0.80 ATR`.
- `Require First Touch at Local Extreme = true`.
- Catalyst defaults tuned for more throughput:
  - `Require Bull/Bear Candle Color = false`
  - `Min Body (ATR) = 0.08`
  - `Min Rejection Wick / Body = 0.10`

## Marker & Line Meanings
- `W1` / `M1` (candidate markers) = potential first-touch baselines while structure is building.
- `W1*` / `M1*` labels = the exact first touch that was actually used by a confirmed setup.
- `Wammie First Touch` / `Moolah First Touch` horizontal lines are the first-touch reference levels used for structure and stop placement.
- First-touch lines are drawn as active line objects (not persistent historical plot lines), so old lines are removed when a new baseline replaces them.
- Optional dashed connector line (toggle in visuals) links the exact first touch to the detected second touch used for confirmation.
- `W BUY` / `M SELL` are setup-ready markers (second touch + catalyst + filters confirmed).

## Visual Defaults (Current)
- Candidate first-touch markers (`W1` / `M1`) are hidden by default to reduce historical clutter.
- Linked first-touch labels (`W1*` / `M1*`) are enabled by default.
- First-to-second touch dashed connector is enabled by default.
- Active first-touch horizontal reference line is enabled by default.

## Recommended Presets
- **Walter-style static zones**
  - `Require Zone Confluence = true`
  - `Zone Source = Manual Static`
  - Enter `Manual Support Zone` and `Manual Resistance Zone`
  - Keep candidate markers off; keep linked labels + connector on
- **Structure-only discovery mode (more historical signals)**
  - `Require Zone Confluence = false`
  - Keep trend/session filters on initially, then relax if needed
  - Use linked labels to identify the exact first touch used
- **A+ stricter mode**
  - Keep `Min Candles Between Touches >= 6`
  - Keep `A+ Candles Between Touches = 20`
  - Prefer `Next Candle (A+)` trigger mode

## Alerts Included
- First touch recorded (Wammie / Moolah path).
- Setup ready (Wammie / Moolah).
- A+ setup ready (20+ spacing).
- Entry triggered.
- Setup canceled (invalid/expired).
- Breakeven reached.
- Target hit.
- Stop hit.

## Notes
- Auto zones are pivot-based approximations; discretionary manual zones can still be more precise.
- The script is an indicator with setup/trade-management guidance and alerts, not a broker-executing strategy.
- If nearest valid target zone is unavailable, target falls back to R-multiple.
- In manual-zone mode, a value of `0` means the zone is not set.

## MT5 Port Notes
- `wammie_moolah_indicator_mt5.mq5` ports the same Wammie/Moolah structure detection, pending-order, and trade-management workflow to a MetaTrader 5 custom indicator.
- The MT5 version keeps the active first-touch references and all actionable levels visible via indicator buffers on the chart.
- TradingView-specific linked first-touch labels and connector lines are simplified to buffer-based markers/levels in the MT5 version.
- Session filtering in MT5 uses broker server time.
