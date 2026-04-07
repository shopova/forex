# News Risk Monitor

This folder contains a first-pass news-risk monitor for the live `15m` session.

It is built around the current live rotation:

- `EURUSD`
- `USDJPY`
- `GBPUSD`

`USDCAD` is intentionally excluded because the current live-account plan keeps it in study / demo.

## What It Does

The monitor combines two layers:

1. scheduled macro risk from Forex Factory's weekly JSON export
2. unscheduled headline risk from configurable RSS feeds

It then:

- maps risk to the relevant pair(s)
- marks each pair as `GREEN`, `AMBER`, or `RED`
- prints new alerts directly in the terminal
- prints a compact pair-status board each cycle with active reasons, headlines, and sources
- writes the latest state to:
  - `news_risk_monitor/latest_status.json`
  - `news_risk_monitor/latest_status.md`

This is a `trade-permission filter`.

It is not a direction predictor.

## Default Topic Coverage

The default config watches these unscheduled themes:

- `Iran / Hormuz / shipping / energy shock`: all allowed pairs
- `Trump policy / Truth Social / tariff headlines`: all allowed pairs
- `Ukraine / Russia escalation`: all allowed pairs
- `Central bank surprise / intervention / emergency policy`: all allowed pairs
- `Oil / OPEC shock`: all allowed pairs
- `China / Taiwan / PBOC / Asia risk`: `USDJPY`
- `EU political / sovereign stress`: `EURUSD`
- `UK political / gilt stress`: `GBPUSD`
- `Banking / liquidity / credit stress`: all allowed pairs

The scheduled calendar layer already covers normal `USD`, `EUR`, `GBP`, and `JPY` releases. The headline layer is for unscheduled shocks that can distort the `15m` chart.

## Files

- `run_news_monitor.py`: main runner
- `config.example.json`: example config
- `state.json`: created after first run
- `latest_status.json`: created after first run
- `latest_status.md`: created after first run

## Setup

1. Copy the example config and adjust it if needed:

```bash
cp news_risk_monitor/config.example.json news_risk_monitor/config.json
```

If you already copied `config.json` earlier, either replace it with the updated example or merge the new headline feeds manually.

## Run Once

```bash
python3 news_risk_monitor/run_news_monitor.py --config news_risk_monitor/config.json --once
```

## Run Continuously

Default poll interval is `300` seconds.

```bash
python3 news_risk_monitor/run_news_monitor.py --config news_risk_monitor/config.json
```

Or with a custom poll interval:

```bash
python3 news_risk_monitor/run_news_monitor.py --config news_risk_monitor/config.json --poll-seconds 180
```

## Scheduling

Two practical options:

1. Run it continuously during your trading windows.
2. Run it every `5` minutes through `cron` or a macOS LaunchAgent.

For your current routine, the most useful windows are:

- before the `10:30-12:00` Sofia session
- before the `15:00-16:00` Sofia management window

## Notes

- Google News RSS is usable for a first version, but still noisy.
- Tighten `trusted_sources` if you want fewer alerts.
- Scheduled events are more reliable than headlines; use them as the hard block.
- Headline alerts should be treated conservatively: when in doubt, the bot should block trading, not encourage it.
