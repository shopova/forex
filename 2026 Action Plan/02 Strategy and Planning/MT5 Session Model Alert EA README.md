# MT5 Session Model Alert EA README

## Purpose

This note explains how to install, compile, attach, and use the `v1` semi-automatic MT5 expert built for the current `2026` session-trading model.

The EA is:

- for the current FTMO-style demo workflow
- default allowed symbols: `EURUSD`, `GBPUSD`, `USDJPY`, `USDCAD`
- `30m` only
- alert-only in `v1`
- based on the current clean-slate session model
- intended to work with manually marked executable zones

It is not a fully automatic trade-finding bot.

It is a structured execution assistant.

## EA Source File

Repository source file:

- `Initial-strategy-files/Indicators/Combined Strategy/session_model_alert_ea_mt5.mq5`

Installed MT5 file on this Mac:

- `/Users/rositsashopova/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Experts/session_model_alert_ea_mt5.mq5`

## What The EA Does

The EA monitors only manually marked executable zones and checks whether a valid `30m` trigger appears inside those zones.

It then:

- checks higher-time-frame bias
- checks session timing
- checks FTMO-style percentage risk
- suggests a lot size from stop distance and account equity
- checks room for a fixed `2R` target
- sends an alert when the setup is valid
- shows a dashboard on the chart

It does **not** place trades automatically in `v1`.

## Strategy Alignment

This EA is aligned with:

- `2026 Action Plan/02 Strategy and Planning/Six Month Trading Plan 2026.md`
- `2026 Action Plan/02 Strategy and Planning/Clean Slate FX Strategy v2 - Session Model.md`
- `2026 Action Plan/03 Journal and Trade Reviews/Daily Journal.md`

Main logic:

- `Daily` bias
- `4H` condition
- `30m` execution
- continuation from meaningful level
- accepted breakout retest / `Last Kiss`
- strict reversal reclaim

Legacy note:

- the older small-account planning files now live under `Legacy/2026 Action Plan/` and are no longer the active execution reference for this EA workflow

## Install On Mac

### 1. MT5 Experts Folder

Exact MT5 `Experts` folder path on this Mac:

`/Users/rositsashopova/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Experts`

### 2. Copy The EA

Copy:

- `Initial-strategy-files/Indicators/Combined Strategy/session_model_alert_ea_mt5.mq5`

into:

- `/Users/rositsashopova/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Experts`

This has already been done on this machine.

### 3. Compile The EA

In MetaTrader 5:

1. Open `MetaEditor`
2. Open `session_model_alert_ea_mt5.mq5`
3. Press `F7`
4. Confirm compile output shows no errors

If there are compile errors, fix those before using the EA.

### 4. Attach The EA

In MT5:

1. Open one allowed symbol chart such as `EURUSD`, `GBPUSD`, `USDJPY`, or `USDCAD`
2. Change chart to `M30`
3. Enable `Algo Trading`
4. In `Navigator`, locate `session_model_alert_ea_mt5`
5. Drag it onto the chosen allowed-symbol `M30` chart

## First Input Setup

Check these first:

- `InpAllowedSymbols = EURUSD,GBPUSD,USDJPY,USDCAD`
- `InpAllowedTimeframe = PERIOD_M30`
- `InpSessionStartHourSofia = 10`
- `InpSessionStartMinuteSofia = 0`
- `InpSessionEndHourSofia = 18`
- `InpSessionEndMinuteSofia = 0`
- `InpRiskPerTradePct = 0.25`
- `InpFTMOStartBalance = 100000`
- `InpMaxDailyLossPct = 5.0`
- `InpMaxTotalLossPct = 10.0`

## Important Time Setting

The EA session filter is based on Sofia time.

You must set:

- `InpServerToSofiaOffsetMinutes`

Formula:

- `Sofia time = broker server time + offset`

Examples:

- broker is `1` hour behind Sofia -> `60`
- broker is `2` hours behind Sofia -> `120`
- broker is `1` hour ahead of Sofia -> `-60`

If this input is wrong, the session filter will be wrong.

## Chart Markup Workflow

### Horizontal Lines

Keep the current discretionary line workflow:

- `red` horizontal lines = `Daily` levels
- `orange` horizontal lines = `4H` levels
- `blue` horizontal lines = `30m` levels

The EA does not read line color.

The colors are for trader workflow only.

The EA uses horizontal lines only as optional room-to-target references.

### Executable Zones

The EA requires **rectangles** for executable zones.

Use one rectangle per live setup area.

Required naming:

- `ZEURUSD_CONT_01`
- `ZEURUSD_LK_01`
- `ZEURUSD_REV_01`
- `ZGBPUSD_CONT_01`
- `ZUSDJPY_CONT_01`
- `ZUSDCAD_CONT_01`

Meaning:

- `CONT` = continuation zone
- `LK` = accepted breakout retest / `Last Kiss`
- `REV` = reversal zone

Rules:

- name must start with `Z`
- name must include the current chart symbol token, for example `EURUSD`, `GBPUSD`, `USDJPY`, or `USDCAD`
- name must include one of `CONT`, `LK`, or `REV`
- rectangle must cover the actual price zone
- rectangle must remain active in time while you want the EA to monitor it

If the rectangle name is wrong, the EA ignores it.

## How To Draw The First Test Zone

Recommended first test:

- one continuation zone only

Steps:

1. Open an allowed symbol on `M30`
2. Insert `Rectangle`
3. Draw it around the continuation reaction area
4. Right-click rectangle -> `Properties`
5. Rename it to match the chart symbol, for example `ZEURUSD_CONT_01` on `EURUSD` or `ZGBPUSD_CONT_01` on `GBPUSD`
6. Make sure the time span stretches far enough to stay active during the session

Do not draw the rectangle in the middle of a range.

For continuation, the rectangle should mark the actual executable reaction area.

## Trigger Logic In v1

### Continuation

Valid only when price interacts with the zone edge and then shows:

- rejection from the edge, or
- false-break reclaim back through the edge

### Last Kiss

Valid only when the pattern behaves like:

- breakout
- retest
- acceptance outside the box or clean reclaim confirmation

### Reversal

Valid only when price shows:

- sweep beyond the level
- reclaim back through the level

Reversal in `v1` is reclaim-only, not generic fading.

## What Blocks A Signal

The EA blocks alerts if:

- wrong symbol
- wrong timeframe
- outside session window
- HTF bias is neutral for continuation / `Last Kiss`
- repeated tests weakened the zone
- open-position limit is reached
- daily trade limit is reached
- weekly trade limit is reached
- FTMO daily loss limit is reached
- FTMO total loss limit is reached
- projected risk is above the configured percentage risk limit
- there is no clean `2R` room to the next marked horizontal line

## Trade Planning Model

If a signal is valid, the EA calculates:

- direction
- suggested entry
- structural stop plus ATR buffer
- fixed `2R` target
- suggested lot size
- projected cash risk at the suggested lot size

The EA does not compress stops to fit the account.

If risk is too large, the setup is blocked.

## Dashboard

When attached, the EA shows a chart dashboard with:

- symbol / timeframe
- session status
- auto bias
- effective bias
- nearest zone
- zone state
- planned direction
- entry / stop / target
- cash risk
- reason for waiting or blocking

Common dashboard messages:

- `Waiting for reclaim confirmation`
- `HTF bias is neutral`
- `Outside session window`
- `Projected risk exceeds per-trade FTMO limit`
- `No clean 2R room to next marked line`
- `Alert sent`

## Recommended First Test

For the first test:

1. Use only one zone: `ZEURUSD_CONT_01`
2. Keep horizontal lines on chart
3. Attach the EA to one allowed-symbol `M30` chart
4. Set the correct broker-to-Sofia time offset
5. Watch the dashboard update on closed candles

Optional first-test simplification:

- temporarily set `InpUseLineRoomFilter = false`

That makes it easier to verify the trigger engine before turning the room filter back on.

## Practical Notes

- The EA runs on closed `30m` candles
- The EA is alert-only in `v1`
- This is a semi-automatic execution assistant, not a standalone strategy engine
- Manual zone quality still matters more than trigger speed
- The EA enforces account-wide FTMO-style drawdown limits using account equity
- The EA checks trade counts across the full allowed-symbol list, not just the current chart

## If The EA Does Not Work

Check these in order:

1. `EURUSD` chart?
   Or another symbol from `InpAllowedSymbols`?
2. `M30` timeframe?
3. `Algo Trading` enabled?
4. EA compiled successfully?
5. Correct rectangle name for that chart symbol?
6. Rectangle still active in time?
7. Correct `InpServerToSofiaOffsetMinutes`?
8. Any message in MT5 `Experts` or `Journal` tab?

## Current v1 Limits

This EA does not yet:

- auto-detect zones
- place trades
- read news
- manage partial profits
- move stops to breakeven
- distinguish line color

Those can be added in later versions if needed.
