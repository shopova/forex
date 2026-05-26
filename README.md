# Forex Strategy Repository Map

This repository is a working knowledge base for a discretionary-to-systematic forex trading framework. It combines trader context, active trading process documents, Pine Script and MT5 indicator code, backtesting utilities, study material, and legacy archives.

If you are new to this repo, treat it as a guided workspace, not a flat document dump. The most important distinction is:

- `2026 Action Plan/` = active operating documents
- `Legacy/` = older strategy material, archived execution docs, and current indicator source locations
- `Backtesting/` = validation utilities and historical data
- `Book Notes/` and `Reading Materials/` = study and reference support

## What This Repo Is For

Use this repo to:

- understand the trader's current operating model
- design or refine setup rules
- build or modify Pine Script and MT5 indicators
- validate logic with backtests
- support journaling, review, and study

Do not assume every document here is current. Some files are intentionally kept for historical context or reference only.

## Current Strategic Priority

The active strategy direction is the part-time session-trading model centered on:

- [Clean Slate FX Strategy v2 - Session Model.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/02 Strategy and Planning/Clean Slate FX Strategy v2 - Session Model.md>)
- [Daily Forex Trading Routine.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Daily Forex Trading Routine.md>)
- [Pre-Trade Entry Filter.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Pre-Trade Entry Filter.md>)
- [Trigger Types and Definitions.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Trigger Types and Definitions.md>)
- [Daily Journal.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/03 Journal and Trade Reviews/Daily Journal.md>)

The current MT5 automation priority is the semi-automatic alert EA, not fully autonomous trade discovery:

- [MT5 Session Model Alert EA README.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/02 Strategy and Planning/MT5 Session Model Alert EA README.md>)
- [session_model_alert_ea_mt5.mq5](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Combined%20Strategy/session_model_alert_ea_mt5.mq5>)

## Repo Layout

### `2026 Action Plan/`

This is the active operational layer.

- `01 Trading Desk/`: live workflow, trigger definitions, chart-reading rules, checklists
- `02 Strategy and Planning/`: active strategy model, planning, risk scaling, MT5 session-model docs
- `03 Journal and Trade Reviews/`: daily planning, post-trade review, coaching templates
- `04 Study Plans/`: current study tracks and study checklists

If you need to understand how the trader currently works day to day, start here.

### `Legacy/`

This folder contains both archived material and still-relevant implementation assets.

- `Legacy/Initial-strategy-files/`: foundational trader context, handbook, checklist, journal history
- `Legacy/Initial-strategy-files/Indicators/`: Pine Script and MT5 indicator source code
- `Legacy/Forex xp/`: old live-trading and rebuild archive
- `Legacy/news_risk_monitor/`: archived utility, reference only
- `Legacy/2026 Action Plan/`: superseded planning documents

Important: indicator source files still live under `Legacy/Initial-strategy-files/Indicators/`. `Legacy` does not mean "ignore everything inside it."

### `Backtesting/`

This folder contains the code and data used to validate strategy logic.

- Python runners for Last Kiss, Big Shadow, Wammie/Moolah, and QQE/QMP
- OHLC CSV data in `Backtesting/Backtesting Data/`
- generated result folders under `Backtesting/Backtesting Data/results_*`

Use result folders for comparison and validation, not as canonical rule definitions.

### `Book Notes/`

This is the study system.

- `Guidelines/`: reading roadmaps, extraction plans, study frameworks
- `Journal notes/`: book-by-book notes and concept extraction

Use this area for improving judgment, pattern quality, and execution thinking. Do not treat it as the active rulebook unless a concept has been moved into strategy docs.

### `Reading Materials/`

Reference texts, excerpts, and supporting material for specific concepts such as Big Shadow, pullback quality, and impulse identification.

This is context support, not the primary operating layer.

## Read This First

If you are an outsider trying to understand the repo before making changes, read in this order:

1. [Trader Profile Context.md](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Trader%20Profile%20Context.md>)
2. [Trading handbook.md](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Trading%20handbook.md>)
3. [Trade Execution Checklist.md](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Trade%20Execution%20Checklist.md>)
4. [Drawdown & Psychology Rules.pdf](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Drawdown%20&%20Psychology%20Rules.pdf>)
5. [Clean Slate FX Strategy v2 - Session Model.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/02 Strategy and Planning/Clean Slate FX Strategy v2 - Session Model.md>)
6. [Daily Forex Trading Routine.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Daily Forex Trading Routine.md>)
7. [Pre-Trade Entry Filter.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Pre-Trade Entry Filter.md>)
8. [Trigger Types and Definitions.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Trigger Types and Definitions.md>)

That sequence gives you trader constraints first, then active execution logic.

## If You Are Working On Indicators

Start with the setup README before touching code.

### Last Kiss

- [README.md](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Last%20Kiss/README.md>)
- [last_kiss_indicator_v6.pine](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Last%20Kiss/last_kiss_indicator_v6.pine>)
- [last_kiss_indicator_mt5.mq5](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Last%20Kiss/last_kiss_indicator_mt5.mq5>)

Current baseline:

- stop-order execution after breakout and retouch confirmation
- `R Multiple` target mode by default
- minimum setup quality of `2.0R`
- trend and session filters enabled by default

### Big Shadow

- [README.md](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Big%20Shadow/README.md>)
- [big_shadow_indicator_v6.pine](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Big%20Shadow/big_shadow_indicator_v6.pine>)
- [The big shadow.md](</Users/rositsashopova/Documents/Projects/forex/Reading%20Materials/The%20big%20shadow.md>)

Current baseline:

- no zone confluence required by default
- `R Multiple` target mode by default
- minimum projected reward-to-risk of `2.0R`

### Wammie / Moolah

- [README.md](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Wammie%20Moolah/README.md>)
- [wammie_moolah_indicator_v6.pine](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Wammie%20Moolah/wammie_moolah_indicator_v6.pine>)

Current baseline:

- no zone confluence required by default
- trend and session filters enabled
- `R Multiple` target mode with minimum `2R`

### QQE / QMP

- [MT4_MT5 High Probability Forex Trading Method.md](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/QQE%20Strategy/MT4_MT5%20High%20Probability%20Forex%20Trading%20Method.md>)
- [README.md](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/QQE%20Strategy/README.md>)
- [QMP-indicator.pine](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/QQE%20Strategy/QMP-indicator.pine>)
- [qqe_qmp_strategy_v6.pine](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/QQE%20Strategy/qqe_qmp_strategy_v6.pine>)

Current default automation stance:

- use lower-risk `Method No. 1`
- keep raw sync dots visible even when a stricter filter blocks tradability
- report validation per pair, not only aggregate

### Combined Execution Logic

- [three_setups_strategy_v6.pine](</Users/rositsashopova/Documents/Projects/forex/Legacy/Initial-strategy-files/Indicators/Combined%20Strategy/three_setups_strategy_v6.pine>)

Review this file before changing cross-setup execution, shared risk logic, or behavior that should remain consistent across modules.

## If You Are Working On Backtesting

Read these first:

- [Backtesting Data/README.md](</Users/rositsashopova/Documents/Projects/forex/Backtesting/Backtesting%20Data/README.md>)
- [run_indicator_backtests.py](</Users/rositsashopova/Documents/Projects/forex/Backtesting/run_indicator_backtests.py>)
- [run_qqe_qmp_backtests.py](</Users/rositsashopova/Documents/Projects/forex/Backtesting/run_qqe_qmp_backtests.py>)

Working rules:

- keep Python defaults aligned with the Pine defaults they mirror
- validate performance per pair when assessing strategy quality
- do not treat generated `results_*` folders as rule definitions

## If You Are Working On The Current Live Workflow

Stay inside `2026 Action Plan/` first.

Open these:

- [Daily Forex Trading Routine.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Daily Forex Trading Routine.md>)
- [How I Read Daily 4H 30m Before A Trade.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/How%20I%20Read%20Daily%204H%2030m%20Before%20A%20Trade.md>)
- [What To Look For On 30m.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/What%20To%20Look%20For%20On%2030m.md>)
- [Pre-Trade Entry Filter.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Pre-Trade%20Entry%20Filter.md>)
- [Trigger Types and Definitions.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Trigger%20Types%20and%20Definitions.md>)
- [Key Level Maintenance Rules.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/01 Trading Desk/Key%20Level%20Maintenance%20Rules.md>)

For journaling and review:

- [Daily Journal.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/03 Journal and Trade Reviews/Daily Journal.md>)
- [Trade Coaching Log Template.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/03 Journal and Trade Reviews/Trade%20Coaching%20Log%20Template.md>)
- [Edge Review and Setup Definitions.md](</Users/rositsashopova/Documents/Projects/forex/2026 Action Plan/03 Journal and Trade Reviews/Edge%20Review%20and%20Setup%20Definitions.md>)

## Active Vs Legacy

Use this rule of thumb:

- if a document exists in `2026 Action Plan/`, prefer it for current process
- if a document under `Legacy/` defines trader profile, hard risk rules, or current indicator code, it may still be authoritative
- if a document is explicitly archived, superseded, or tied to older small-account workflows, use it only for historical context

Examples of clearly non-primary material:

- `Legacy/2026 Action Plan/`
- `Legacy/Forex xp/`
- `Legacy/news_risk_monitor/`

Examples of legacy paths that still matter:

- `Legacy/Initial-strategy-files/Trader Profile Context.md`
- `Legacy/Initial-strategy-files/Trading handbook.md`
- `Legacy/Initial-strategy-files/Trade Execution Checklist.md`
- `Legacy/Initial-strategy-files/Indicators/`

## Practical Working Rules

- Do not change indicator defaults without checking the setup README and any matching Python backtest logic.
- Do not assume legacy means obsolete; several live code assets still live there.
- Do not rely on a single aggregate backtest when pair-level behavior matters.
- Keep the trader's risk, psychology, and checklist rules above setup discretion.
- When documents conflict, prefer stricter operational and risk-control rules.

## Short Version

If you only need the minimum mental model:

1. Read trader constraints in `Legacy/Initial-strategy-files/`.
2. Read the active operating model in `2026 Action Plan/`.
3. Read setup-specific README files before editing indicator code in `Legacy/Initial-strategy-files/Indicators/`.
4. Use `Backtesting/` to validate logic, not to define it.
5. Treat `Book Notes/` and `Reading Materials/` as support material unless a rule has been promoted into the active strategy docs.
