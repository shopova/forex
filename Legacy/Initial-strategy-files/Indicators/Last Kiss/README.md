# Last Kiss Indicator Project Summary

## Objective
Build a TradingView Pine Script (v6) **Last Kiss (Retouch)** indicator aligned with:
- `Trading handbook.md`
- `Legacy/Initial-strategy-files/Dual-Methodology Strategy for Major Pairs.md`
- `Trade Execution Checklist.md`
- `Trader Profile Context.md`

## Current Main Script
- `last_kiss_indicator_v6.pine`
- `last_kiss_indicator_mt5.mq5`

## Rule Mapping Implemented
- Consolidation-box detection with minimum touch count on both boundaries.
- Consolidation-box detection now uses an adaptive window (`Min Consolidation Bars` to `Max Consolidation Bars`) and selects the longest valid active range.
- Range qualification requires both boundaries to be actively respected, not just historical touches.
- Fixed box boundaries after detection (no moving top/bottom once the setup box is accepted).
- Volatility penetration buffer for range interaction checks (ATR + ticks based).
- Consolidation quality filters to avoid trend phases being labeled as boxes:
  - max net drift as % of box height
  - max outside closes during consolidation window
- Breakout validation:
  - close-or-wick mode
  - ATR breakout buffer
  - minimum breakout body
  - optional volume expansion filter
- Retouch detection on broken box edge.
- Catalyst quality filter (body size, close near extreme, rejection wick/body ratio).
- Execution via stop orders only:
  - bullish: Buy Stop above catalyst high
  - bearish: Sell Stop below catalyst low
- Emergency stop options:
  - midpoint of box (default)
  - opposite box edge
  - opposite edge + ATR buffer
- Target engine:
  - `R Multiple` mode
  - `Nearest Zone` mode using pivot-based support/resistance
  - target-zone buffer in ticks
  - fallback to `R Multiple` if nearest-zone target is unavailable
- Setup-quality gate:
  - setup is accepted only if projected reward-to-risk is at least `Minimum Setup R` (default `2.0R`)
- Fake-breakout control:
  - timeout invalidation from breakout to retest
  - box dropped after too many fake breakouts (default max `2`)
- Dynamic box invalidation:
  - box is invalidated if one boundary is not touched for too long (`maxBoundaryStaleBars`)
  - candidate box requires recent touches on both boundaries (`recentTouchWindow`)
  - box is invalidated if closes remain outside the range for too many consecutive bars (`maxOutsideCloseRun`)
  - invalidated boxes can be force-deleted from chart objects (toggle)
  - box boundaries are drawn as line objects (not historical `plot` traces), so deletion behaves as expected
  - invalidation deletion is toggleable (`Delete Invalidated Boxes`)
- Pending-order expiry:
  - cancel setup if stop entry is not triggered within configured bars (default `5`)
- Optional strategy filters:
  - D1 200 SMA + H4 50 EMA trend filter
  - session filter
- Pair preset workflow:
  - `Pair Preset Mode` supports `Off (Manual Inputs)` and `Synced Per-Pair (MT5 2020-2026, 2026-02-26)`
  - synced mode auto-applies pair-specific tuned settings for `EURUSD`, `GBPUSD`, `USDCAD`, `USDJPY`
  - non-matching symbols keep manual inputs
- Alerts:
  - breakout, retest, setup-ready, entry-triggered, setup-canceled

## Default Settings Snapshot (Current)
- `pairPresetMode`: `Off (Manual Inputs)`
- `targetMode`: `R Multiple`
- `targetRR`: `2.0` (minimum allowed)
- `minSetupRR`: `2.0` (minimum allowed)
- `stopMode`: `Midpoint of Box`
- `maxFakeBreakouts`: `2`
- `rangeVolBufAtr`: `0.10`
- `rangeVolBufTicks`: `5`
- `minConsolBars`: `20`
- `maxConsolBars`: `80`
- `recentTouchWindow`: `12`
- `minRecentBoundaryTouches`: `2`
- `maxBoundaryStaleBars`: `30`
- `maxConsolDriftPct`: `25`
- `maxOutsideCloses`: `1`
- `maxOutsideCloseRun`: `2`
- `entryExpiryBars`: `5`
- `useTrendFilter`: `true`
- `useSessionFilter`: `true`
- `keepHistoricalRectangles`: `true`
- `deleteInvalidatedBoxes`: `false`
- `showTargetZones`: `false`

## Synced Per-Pair Presets (2026-02-26)
- `EURUSD`: `minConsolBars=16`, `maxConsolBars=60`, `stopMode=Opposite Box Edge`, `targetRR=2.0`, `minSetupRR=2.0`, `win_rate_pct=41.79`, `net_r=17.0`
- `GBPUSD`: `minConsolBars=16`, `maxConsolBars=50`, `stopMode=Midpoint of Box`, `targetRR=2.5`, `minSetupRR=2.5`, `win_rate_pct=55.56`, `net_r=17.0`
- `USDCAD`: `minConsolBars=16`, `maxConsolBars=60`, `stopMode=Midpoint of Box`, `targetRR=3.0`, `minSetupRR=2.5`, `win_rate_pct=28.57`, `net_r=6.0`
- `USDJPY`: `minConsolBars=30`, `maxConsolBars=50`, `stopMode=Midpoint of Box`, `targetRR=3.0`, `minSetupRR=2.0`, `win_rate_pct=33.87`, `net_r=19.46`

## Notes
- Auto target zones are pivot-based approximations; discretionary zone review can still be superior.
- The script is an indicator with setup/management logic and alerts, not a broker-executing strategy.
- If `Target Mode = Nearest Zone` and no valid zone exists in trade direction, target falls back to R-multiple logic.

## MT5 Port Notes
- `last_kiss_indicator_mt5.mq5` ports the same four-state Last Kiss workflow to a MetaTrader 5 custom indicator.
- The MT5 version evaluates confirmed bars only, then extends active box and pending levels onto the current live bar for visibility.
- The MT5 version keeps one active chart rectangle for the current box; historical setup/entry/cancel markers are preserved via indicator buffers rather than persistent historical rectangles.
- Session filtering in MT5 uses broker server time.
