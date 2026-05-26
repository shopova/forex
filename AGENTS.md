# Initial prompt

I am a forex trader. I will provide you with documents describing my profile and strategy. What I want for you as a result is to create Pine Script indicators. Make sure to ask questions and require specifications if anything is lacking. I would like to create a Last Kiss (retouch) indicator to use in TradingView which is in synergy with the provided documents and knowledge you have.

# Strategy Repository Guide

This directory is a strategy knowledge base for designing, validating, and automating a complete forex trading framework. It includes trader context, rule documentation, execution controls, indicator implementations, research notes, and performance records.

## Core Documents
- `Legacy/Initial-strategy-files/Trader Profile Context.md`  
  Defines trader constraints, strengths, risk tolerance, and operational boundaries.

- `Legacy/Initial-strategy-files/Trading handbook.md`  
  Master rulebook for discretionary and systemized decision-making.

- `Legacy/Initial-strategy-files/Trade Execution Checklist.md`  
  Structured process controls before, during, and after trade execution.

- `Legacy/Initial-strategy-files/Trade Journal - Journal.csv`  
  Historical results for validation, error analysis, and rule refinement.

- `2026 Action Plan/01 Trading Desk/Daily Forex Trading Routine.md`  
  Session-by-session operating routine for preparation, execution, and review.

- `2026 Action Plan/02 Strategy and Planning/Six Month Trading Plan 2026.md`  
  Six-month roadmap for the current rebuild phase, covering study, backtesting, forward testing, and progression criteria.

- `2026 Action Plan/02 Strategy and Planning/MT5 Session Model Alert EA README.md`  
  Installation, chart-markup, and usage guide for the current `EURUSD 30m` MT5 session-model alert EA.

- `Legacy/Initial-strategy-files/Drawdown & Psychology Rules.pdf`  
  Hard behavioral and drawdown controls that override setup discretion when needed.

- `2026 Action Plan/02 Strategy and Planning/Clean Slate FX Strategy v2 - Session Model.md`  
  Current clean-slate strategy direction for the part-time session-trading model.

- `2026 Action Plan/03 Journal and Trade Reviews/Daily Journal.md`  
  Current day-by-day market-observation and planning journal for the active 2026 process.

## Legacy Documents
- `Legacy/2026 Action Plan/MT5 Live Trading Plan - 387.50 EUR.md`  
  Old small-account live plan tied to the `EUR 387.50` MT5 rebuild phase; no longer the active path.

- `Legacy/2026 Action Plan/Live Setup Types for Small Account.md`  
  Small-account setup filter built around the `0.01` lot constraint; retained for historical reference only.

- `Legacy/2026 Action Plan/Clean Slate FX Strategy v1.md`  
  Earlier clean-slate draft superseded by the active session-model strategy.

- `Legacy/Initial-strategy-files/Dual-Methodology Strategy for Major Pairs.md`  
  Older Elliott/Naked hybrid methodology retained as a historical reference, not as the active framework.

- `Legacy/Initial-strategy-files/Risk Scaling Plan.md`  
  Older live-account scaling plan tied to the pre-demo phase.

- `Legacy/Forex xp/`  
  Archive of prior live-account rebuild docs, statements, FTMO readiness notes, and behavior review material.

## Reference Materials
- `Legacy/Initial-strategy-files/Indicators/QQE Strategy/MT4_MT5 High Probability Forex Trading Method.md`  
  Detailed rule source for the QMP / QQE high-probability trend-following method.

- `Reading Materials/The big shadow.md`  
  Detailed Big Shadow reference text (Naked Forex chapter extraction).

- `Reading Materials/Correction Quality Guide.md`  
  Context aid for evaluating pullbacks and continuation quality.

- `Reading Materials/Impulse Identification Guide.md`  
  Context aid for distinguishing impulse vs correction behavior.

- `Legacy/Initial-strategy-files/Manual Backtest Journaling/codex_thread_summary.md`  
  Compact summary of prior strategy-development discussions and clarified setup definitions.

## Study Framework
- `Book Notes/Guidelines/reading_first_roadmap_2026.md`  
  Current book-selection and reading-priority guide; use this instead of older note-index/source-map files.

- `Book Notes/Guidelines/12_week_edge_curriculum_2026.md`  
  Main reading-heavy study framework for improving edge, chart judgment, and strategy design.

- `Book Notes/Guidelines/art_and_science_foundation_plan_2026.md`  
  Book-specific extraction plan for `The Art and Science of Technical Analysis`, aligned with the first four weeks of the study curriculum.

- `Book Notes/Guidelines/art_and_science_5_day_daily_template.md`  
  Current daily note template for extracting practical chart-reading rules from the Grimes book.

## Indicator Implementations

### Last Kiss
- `Legacy/Initial-strategy-files/Indicators/Last Kiss/last_kiss_indicator_v6.pine`  
  Current TradingView Pine Script v6 implementation.

- `Legacy/Initial-strategy-files/Indicators/Last Kiss/last_kiss_indicator_mt5.mq5`  
  Current MetaTrader 5 custom indicator port.

- `Legacy/Initial-strategy-files/Indicators/Last Kiss/README.md`  
  Implementation summary, defaults, preset notes, and workflow coverage.

### Big Shadow
- `Legacy/Initial-strategy-files/Indicators/Big Shadow/big_shadow_indicator_v6.pine`  
  Current TradingView Pine Script v6 implementation.

- `Legacy/Initial-strategy-files/Indicators/Big Shadow/README.md`  
  Implementation summary, defaults, and validation notes.

### Wammie / Moolah
- `Legacy/Initial-strategy-files/Indicators/Wammie Moolah/wammie_moolah_indicator_v6.pine`  
  Current TradingView Pine Script v6 implementation.

- `Legacy/Initial-strategy-files/Indicators/Wammie Moolah/README.md`  
  Implementation summary, defaults, and optimization notes.

### QQE / QMP
- `Legacy/Initial-strategy-files/Indicators/QQE Strategy/QMP-indicator.pine`  
  Price-chart QMP Filter implementation with tradable and blocked alert variants.

- `Legacy/Initial-strategy-files/Indicators/QQE Strategy/QQE-adv.pine`  
  QQE Advanced source used by the QMP filter logic.

- `Legacy/Initial-strategy-files/Indicators/QQE Strategy/Macd-platinum.pine`  
  MACD Platinum source used by the QMP filter logic.

- `Legacy/Initial-strategy-files/Indicators/QQE Strategy/qqe_qmp_strategy_v6.pine`  
  Standalone Pine Script v6 strategy for lower-risk `Method No. 1`.

- `Legacy/Initial-strategy-files/Indicators/QQE Strategy/README.md`  
  QQE / QMP implementation summary and default execution model.

### Combined Strategy
- `Legacy/Initial-strategy-files/Indicators/Combined Strategy/three_setups_strategy_v6.pine`  
  Unified Pine strategy combining Last Kiss, Big Shadow, and Wammie/Moolah with shared risk controls.

- `Legacy/Initial-strategy-files/Indicators/Combined Strategy/session_model_alert_ea_mt5.mq5`  
  Semi-automatic MetaTrader 5 alert EA for the current `EURUSD 30m` session model using manual executable zones.

## Backtesting Data
- `Backtesting/Backtesting Data/README.md`  
  Format requirements, export workflow, and example commands for local backtests.

- `Backtesting/Backtesting Data/*.csv`  
  Source OHLC datasets for pair-level validation and reproduction of Pine defaults.

- `Backtesting/Backtesting Data/results_*`  
  Generated backtest outputs and comparison runs; use these for validation, not as rule sources.

## Utilities
- `Legacy/news_risk_monitor/README.md`  
  Archived overview of the live-session news-risk monitor and its usage.

- `Legacy/news_risk_monitor/run_news_monitor.py`  
  Archived macro-calendar and headline-risk monitor utility.

- `Legacy/news_risk_monitor/config.json`  
  Local configuration for the archived news-risk monitor.

- `Backtesting/run_indicator_backtests.py`  
  Python backtest runner for Last Kiss, Big Shadow, and Wammie/Moolah logic mirrored from Pine defaults.

- `Backtesting/run_qqe_qmp_backtests.py`  
  Python backtest runner that mirrors the default QQE / QMP `Method No. 1` execution model and reports results per pair.

- `Backtesting/optimize_last_kiss_mt5.py`  
  Last Kiss MT5-oriented optimization helper.

- `Backtesting/optimize_frequency_with_risk.py`  
  Utility for signal-frequency / risk tradeoff experiments.

- `Backtesting/run_signal_frequency_sweep.py`  
  Utility for signal-frequency sweeps across configuration variants.

## How to Use This Repository
1. Read the profile, handbook, routine, drawdown, and checklist documents under `Legacy/Initial-strategy-files/` first, and the active planning documents under `2026 Action Plan/`, to anchor decisions in trader-specific constraints.
2. Extract objective entry, exit, invalidation, and risk rules from the methodology and checklist documents before coding.
3. Use `Legacy/Initial-strategy-files/Trade Journal - Journal.csv` and files in `Backtesting/Backtesting Data/` to verify assumptions, tune parameters, and detect recurring mistakes.
4. For Last Kiss work, review `Legacy/Initial-strategy-files/Indicators/Last Kiss/README.md` before modifying implementation logic; there is no standalone active Last Kiss note file in the current workspace.
5. For Big Shadow work, review `Legacy/Initial-strategy-files/Indicators/Big Shadow/README.md` and `Reading Materials/The big shadow.md` before modifying implementation logic.
6. For Wammie/Moolah work, review `Legacy/Initial-strategy-files/Indicators/Wammie Moolah/README.md` before modifying implementation logic.
7. For strategy-design or study-work requests, prioritize `2026 Action Plan/02 Strategy and Planning/Clean Slate FX Strategy v2 - Session Model.md`, `Book Notes/Guidelines/reading_first_roadmap_2026.md`, and `Book Notes/Guidelines/12_week_edge_curriculum_2026.md`.
8. For QQE / QMP work, read `Legacy/Initial-strategy-files/Indicators/QQE Strategy/MT4_MT5 High Probability Forex Trading Method.md` first and treat it as the detailed rule source for that method.
9. Keep Python backtest defaults aligned with the Pine defaults they are intended to mirror.
10. If changing cross-setup execution or shared risk logic, review `Legacy/Initial-strategy-files/Indicators/Combined Strategy/three_setups_strategy_v6.pine` and keep its shared behavior consistent with the individual setup modules.
11. For archived live-session execution support or risk-blocking automation, review `Legacy/news_risk_monitor/README.md` and keep any changes aligned with its local config and archived workflow.
12. For the current MT5 session-model EA workflow, review `2026 Action Plan/02 Strategy and Planning/MT5 Session Model Alert EA README.md` and `Legacy/Initial-strategy-files/Indicators/Combined Strategy/session_model_alert_ea_mt5.mq5` before changing live alert logic, chart-markup rules, or session defaults.

## Strategy-to-Indicator Scope
Automation work (for example Pine Script) should represent the full strategy stack:
- market condition and pair filters
- setup detection
- confirmation and invalidation logic
- risk management levels and alert workflow
- optional journaling outputs for post-trade review

Current implementation status:
- Last Kiss retouch logic is implemented in Pine Script v6 in `Legacy/Initial-strategy-files/Indicators/Last Kiss/last_kiss_indicator_v6.pine`.
- Last Kiss retouch logic is also implemented for MetaTrader 5 in `Legacy/Initial-strategy-files/Indicators/Last Kiss/last_kiss_indicator_mt5.mq5`.
- Big Shadow trigger logic is implemented in Pine Script v6 in `Legacy/Initial-strategy-files/Indicators/Big Shadow/big_shadow_indicator_v6.pine`.
- Wammie/Moolah trigger logic is implemented in Pine Script v6 in `Legacy/Initial-strategy-files/Indicators/Wammie Moolah/wammie_moolah_indicator_v6.pine`.
- QQE / QMP source indicators are present in `Legacy/Initial-strategy-files/Indicators/QQE Strategy/`.
- QMP alertconditions include a combined tradable signal (`QMP Signal`) in addition to directional and blocked alerts.
- A standalone QQE / QMP Pine strategy is implemented in `Legacy/Initial-strategy-files/Indicators/QQE Strategy/qqe_qmp_strategy_v6.pine`.
- A combined execution model for all three setups is implemented in `Legacy/Initial-strategy-files/Indicators/Combined Strategy/three_setups_strategy_v6.pine`.
- A semi-automatic MT5 alert EA for the current clean-slate session model is implemented in `Legacy/Initial-strategy-files/Indicators/Combined Strategy/session_model_alert_ea_mt5.mq5`.
- Python backtesting mirrors exist in `Backtesting/run_indicator_backtests.py` and `Backtesting/run_qqe_qmp_backtests.py`.
- Big Shadow and Wammie/Moolah README files mention MT5 ports, but those MT5 source files are not present in the current workspace; do not assume they exist unless they are added.
- An archived live-session news-risk utility is present in `Legacy/news_risk_monitor/`; treat it as a reference utility rather than the active execution path.
- The current MT5 session-model EA is alert-only in `v1`, runs on `30m`, supports the FTMO/demo allowed-symbol shortlist (`EURUSD`, `GBPUSD`, `USDJPY`, `USDCAD` by default), and uses manually named rectangles as executable zones.
- The current MT5 session-model EA uses percentage-based risk and suggested lot sizing rather than the older small-account fixed `0.01` lot model.

Current Last Kiss baseline (from current README and synced presets):
- Execution uses stop orders only after breakout and retouch confirmation.
- Default target mode is `R Multiple` with minimum `2R`.
- Default setup-quality gate requires projected reward-to-risk >= `2.0R`.
- Trend and session filters are enabled by default.
- `Pair Preset Mode` supports `Off (Manual Inputs)` and `Synced Per-Pair (MT5 2020-2026, 2026-02-26)` for `EURUSD`, `GBPUSD`, `USDCAD`, and `USDJPY`.

Current Wammie/Moolah baseline:
- Use no zone confluence by default (`Require Zone Confluence = false`); zone selection is discretionary/manual.
- Keep trend and session filters enabled by default.
- Use `R Multiple` target mode with minimum `2R`.
- Keep Moolah (short-side reversed logic) enabled and validated alongside Wammie.

Current Big Shadow baseline (updated 2026-02-26 in repo notes):
- Use no zone confluence by default (`Require Zone Confluence = false`).
- Use `R Multiple` target mode by default with minimum `2R` (`R Multiple Target >= 2.0`).
- Enforce setup-quality gate: only accept setups with projected reward-to-risk >= `2.0R` (`Minimum Setup R >= 2.0`).
- Use per-pair MT5 preset mode by default in Pine (`Pair Preset Mode = MT5 Per-Pair >=2R (2020-2026)`) for `EURUSD`, `GBPUSD`, `USDCAD`, and `USDJPY`.
- Keep manual override available (`Pair Preset Mode = Off (Manual Inputs)`).

Current QQE / QMP baseline (book-aligned, repo-constrained):
- Default to the lower-risk trend-following workflow (`Method No. 1`) for automation unless the user explicitly requests the higher-risk basket / no-hard-stop variant.
- Use stacked `50 EMA`, `100 EMA`, and `240 LMA` as the default trend filter inside the QMP logic.
- Treat `QMP Filter` confirmation as the sync condition between `QQE Adv (1,8,3)` and `MACD Platinum (12,26,9)`.
- In an uptrend, look for blue `MACD Platinum` dots below zero, then a confirmed blue `QMP Filter` dot; in a downtrend, look for red `MACD Platinum` dots above zero, then a confirmed red `QMP Filter` dot.
- Treat QMP dots as candle-close confirmations only; default execution in the strategy is at the open of the next candle after confirmation.
- Keep raw `QMP Filter` dots visible whenever the `MACD Platinum` bias and the `QQE Adv` cross are in sync; stricter filters may mark a signal as blocked, but must not suppress the raw dot entirely.
- In the indicator, keep both raw directional alerts and the combined tradable alert available; blocked raw syncs should remain distinguishable from tradable signals.
- Treat `Method No. 2` (scale-in / catastrophe-stop / basket logic) as high risk and only implement it when the user explicitly requests that behavior.
- For Python QQE / QMP validation, report results per pair rather than as a single aggregate and include at minimum closed trades, win rate, and net `R`.

Current strategic priority:
- The active strategy-design direction is the clean-slate part-time session model in `2026 Action Plan/02 Strategy and Planning/Clean Slate FX Strategy v2 - Session Model.md`.
- Current MT5 automation priority is the semi-automatic FTMO/demo session-model alert EA for the allowed major-pair shortlist, not full autonomous trade discovery.
- QQE / QMP materials remain in the repo, but they are no longer a default focus unless the user explicitly asks for them.

Micro trend-line policy:
- Treat `One- to Three-Bar Trend Lines` from `The Art and Science of Technical Analysis` as an optional micro-confirmation tool only.
- They may be used to refine timing inside already-valid continuation contexts such as `Last Kiss`, `break + retest`, `EMA bounce`, or `breaker candle at retest`.
- Do not treat them as a standalone setup family, primary trigger, or default indicator requirement.
- They must not override higher-time-frame structure, fib location, invalidation, or the existing 1H trigger hierarchy.
- If the user asks to automate them, frame them as an optional filter/entry refinement rather than a separate strategy.

Big Shadow backtesting policy:
- Do not rely on aggregate-only optimization/ranking when assessing whether the strategy meets return targets.
- Validate performance per pair using full available MT5 history.
- In Python runner, default to pair-aware reproduction via:
  - `--bs-pair-preset-mode "MT5 Per-Pair >=2R (2020-2026)"`
- If target constraints are requested (for example, `>= +2R`), report pair-level outcomes explicitly.

## Notes
- `.DS_Store` files are system metadata and not strategy content.
- Current strategy source documents and indicator implementations now live under `Legacy/Initial-strategy-files/`; use those paths unless a future reorganization moves them back into a non-legacy location.
- The active planning documents now live under `2026 Action Plan/`.
- Older small-account and rebuild-phase planning documents were moved under `Legacy/`.
- The former `Initial-strategy-files/Forex xp/` archive was moved to `Legacy/Forex xp/`.
- The old `Book Notes/00_index.md` and `Book Notes/01_source_map.md` files were removed; use the study-framework files above instead.
- When rules conflict across documents, prioritize explicit checklist constraints and documented risk limits.
- When QQE / QMP book guidance conflicts with the checklist, risk plan, or drawdown rules, keep the stricter operational and risk-control rule.
- `Legacy/Initial-strategy-files/Manual Backtest Journaling/` contains manual journaling references and prior thread summaries.
- Indicator implementations live under `Legacy/Initial-strategy-files/Indicators/`.
- Backtesting datasets and generated results live under `Backtesting/Backtesting Data/`.
- `Backtesting/Backtesting Data/results_*` folders are generated outputs; do not treat them as canonical rule definitions.
- Keep Last Kiss-related files inside `Legacy/Initial-strategy-files/Indicators/Last Kiss/`.
- Keep Big Shadow-related files inside `Legacy/Initial-strategy-files/Indicators/Big Shadow/`.
- Keep Wammie/Moolah-related files inside `Legacy/Initial-strategy-files/Indicators/Wammie Moolah/`.
- Keep QQE / QMP-related files inside `Legacy/Initial-strategy-files/Indicators/QQE Strategy/`.
- Keep combined execution logic inside `Legacy/Initial-strategy-files/Indicators/Combined Strategy/`.
- Keep the MT5 session-model alert EA and closely related docs aligned between `Legacy/Initial-strategy-files/Indicators/Combined Strategy/session_model_alert_ea_mt5.mq5` and `2026 Action Plan/02 Strategy and Planning/MT5 Session Model Alert EA README.md`.
- Keep archived news-risk monitoring files inside `Legacy/news_risk_monitor/`.
