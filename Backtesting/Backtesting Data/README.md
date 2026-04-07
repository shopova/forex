# Backtesting Data Guide

## Requirements
- `Python 3.9+`
- No external packages required (standard library only)
- CSV files with OHLC data

## CSV Format (Required)
- Required columns:
  - `time` (or `timestamp`)
  - `open`
  - `high`
  - `low`
  - `close`
- Optional columns:
  - `Volume` (or `volume`)

Timestamp format:
- Preferred: UTC ISO format, e.g. `2025-07-28T04:00:00Z`

## Run Backtest Commands
Pine-aligned defaults (`Big Shadow` uses `Profile Mode = Balanced` and `Pair Preset Mode = MT5 Per-Pair >=2R (2020-2026)`):

```bash
python3 backtesting/run_indicator_backtests.py \
  --csv "Backtesting Data/FX_USDJPY, 60.csv" \
  --output-dir "Backtesting Data/results_usdjpy_balanced"
```

Run Big Shadow in strict profile (`Profile Mode = A+ Strict`):

```bash
python3 backtesting/run_indicator_backtests.py \
  --csv "Backtesting Data/FX_USDJPY, 60.csv" \
  --output-dir "Backtesting Data/results_usdjpy_strict" \
  --bs-profile "A+ Strict"
```

Disable pair preset mode and use manual Big Shadow inputs only:

```bash
python3 backtesting/run_indicator_backtests.py \
  --csv "Backtesting Data/FX_USDJPY, 60.csv" \
  --output-dir "Backtesting Data/results_usdjpy_manual" \
  --bs-pair-preset-mode "Off (Manual Inputs)"
```

Disable trend filter:

```bash
python3 backtesting/run_indicator_backtests.py \
  --csv "Backtesting Data/FX_USDJPY, 60.csv" \
  --output-dir "Backtesting Data/results_usdjpy_no_trend" \
  --disable-trend-filter
```

Disable trend + session filters:

```bash
python3 backtesting/run_indicator_backtests.py \
  --csv "Backtesting Data/FX_USDJPY, 60.csv" \
  --output-dir "Backtesting Data/results_usdjpy_no_trend_no_session" \
  --disable-trend-filter \
  --disable-session-filter
```

Optional:
- Override tick size: `--mintick 0.001`
- Set Big Shadow profile mode: `--bs-profile "Balanced"|"A+ Strict"|"Custom"`
- Set Big Shadow pair preset mode: `--bs-pair-preset-mode "MT5 Per-Pair >=2R (2020-2026)"|"Off (Manual Inputs)"`

Outputs:
- `summary.json` (performance summary)
- `trades.csv` (trade-by-trade results)

## Export From TradingView
1. Open the pair and timeframe you want (for example `USDJPY`, `1H`).
2. Set chart timezone to UTC.
3. Open chart menu and choose `Export chart data`.
4. Save CSV into `Backtesting Data/` (example: `FX_USDJPY, 60.csv`).
5. Repeat for each pair/timeframe.

Notes:
- TradingView exports extra indicator columns too; this runner ignores extra columns.
- Keep the OHLC/time columns intact.

## Export From Benchmark
1. Open historical data export/download in Benchmark.
2. Select instrument, timeframe, and date range.
3. Export as `CSV`.
4. Ensure CSV includes time + OHLC columns.
5. Save the file to `Backtesting Data/`.

If Benchmark uses different names:
- `timestamp` is accepted instead of `time`
- `volume` is accepted instead of `Volume`

If your file uses other names, rename headers to match this guide before running.
