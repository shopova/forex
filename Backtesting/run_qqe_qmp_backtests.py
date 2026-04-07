#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from run_indicator_backtests import (
    Bar,
    Trade,
    atr,
    ema,
    infer_mintick,
    load_bars,
    map_previous_htf_series,
    map_previous_period_close,
    rolling_sma,
    rsi,
    summarize,
    write_trades,
)


@dataclass
class QqeConfig:
    require_trend_stack: bool = True
    qqe_wp: float = 3.0
    use_macro_trend_filter: bool = True
    daily_sma_len: int = 200
    h4_ema_len: int = 50
    use_session_filter: bool = True
    stop_atr_len: int = 14
    stop_atr_mult: float = 1.0
    swing_lookback: int = 5
    target_r: float = 2.0
    min_required_r: float = 2.0
    enable_breakeven: bool = True
    breakeven_at_r: float = 1.0
    exit_on_opposite_qmp: bool = True
    exit_on_macd_zero_cross: bool = False


@dataclass
class PendingEntry:
    direction: int
    signal_index: int
    stop_price: float


@dataclass
class ActiveTrade:
    direction: int
    entry_index: int
    entry_time: object
    entry: float
    stop: float
    target: float
    risk: float
    breakeven_armed: bool = False


def wma(vals: List[Optional[float]], length: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    if length <= 0:
        return out
    denom = length * (length + 1) / 2.0
    for i in range(length - 1, len(vals)):
        window = vals[i - length + 1 : i + 1]
        if any(v is None for v in window):
            continue
        total = 0.0
        weight = 1
        for v in window:
            total += float(v) * weight
            weight += 1
        out[i] = total / denom
    return out


def crossover(curr_a: Optional[float], prev_a: Optional[float], curr_b: Optional[float], prev_b: Optional[float]) -> bool:
    if None in (curr_a, prev_a, curr_b, prev_b):
        return False
    return prev_a <= prev_b and curr_a > curr_b


def crossunder(curr_a: Optional[float], prev_a: Optional[float], curr_b: Optional[float], prev_b: Optional[float]) -> bool:
    if None in (curr_a, prev_a, curr_b, prev_b):
        return False
    return prev_a >= prev_b and curr_a < curr_b


def cross(curr_a: Optional[float], prev_a: Optional[float], curr_b: Optional[float], prev_b: Optional[float]) -> bool:
    return crossover(curr_a, prev_a, curr_b, prev_b) or crossunder(curr_a, prev_a, curr_b, prev_b)


def true_range(bars: List[Bar]) -> List[float]:
    out: List[float] = [0.0] * len(bars)
    for i, bar in enumerate(bars):
        if i == 0:
            out[i] = bar.h - bar.l
        else:
            prev_close = bars[i - 1].c
            out[i] = max(bar.h - bar.l, abs(bar.h - prev_close), abs(bar.l - prev_close))
    return out


def period_key_for_timeframe(ts, timeframe: str) -> Tuple[int, ...]:
    if timeframe == "D":
        return (ts.year, ts.month, ts.day)
    raise ValueError(f"Unsupported higher timeframe: {timeframe}")


def calc_long_stop(cfg: QqeConfig, bars: List[Bar], atr_vals: List[Optional[float]], lows: List[float], index: int) -> Optional[float]:
    atr_value = atr_vals[index]
    if atr_value is None:
        return None
    return lows[index] - (atr_value * cfg.stop_atr_mult)


def calc_short_stop(cfg: QqeConfig, bars: List[Bar], atr_vals: List[Optional[float]], highs: List[float], index: int) -> Optional[float]:
    atr_value = atr_vals[index]
    if atr_value is None:
        return None
    return highs[index] + (atr_value * cfg.stop_atr_mult)


def close_trade(trades: List[Trade], indicator: str, active: ActiveTrade, bars: List[Bar], exit_index: int, exit_price: float) -> None:
    r = ((exit_price - active.entry) / active.risk) if active.direction == 1 else ((active.entry - exit_price) / active.risk)
    eps = 1e-9
    if r > eps:
        outcome = "win"
    elif r < -eps:
        outcome = "loss"
    else:
        outcome = "be"
    trades.append(
        Trade(
            indicator=indicator,
            direction=active.direction,
            entry_time=active.entry_time,
            exit_time=bars[exit_index].ts,
            entry=active.entry,
            stop=active.stop,
            target=active.target,
            exit_price=exit_price,
            outcome=outcome,
            r=round(r, 3),
        )
    )


def run_qqe_qmp(bars: List[Bar], mintick: float, cfg: Optional[QqeConfig] = None) -> Tuple[Dict[str, object], List[Trade]]:
    cfg = cfg or QqeConfig()
    if len(bars) < 400:
        raise ValueError("Not enough bars for QQE/QMP trend-filtered backtests. Need at least ~400 bars.")

    closes = [b.c for b in bars]
    highs = [b.h for b in bars]
    lows = [b.l for b in bars]

    ema12 = ema(closes, 12)
    ema12x2 = ema(ema12, 12)
    ema26 = ema(closes, 26)
    ema26x2 = ema(ema26, 26)

    blue_macd: List[Optional[float]] = [None] * len(bars)
    for i in range(len(bars)):
        if None in (ema12[i], ema12x2[i], ema26[i], ema26x2[i]):
            continue
        zerolag_fast = 2.0 * float(ema12[i]) - float(ema12x2[i])
        zerolag_slow = 2.0 * float(ema26[i]) - float(ema26x2[i])
        blue_macd[i] = zerolag_fast - zerolag_slow

    macd_sig_1 = ema(blue_macd, 9)
    macd_sig_2 = ema(macd_sig_1, 9)
    org_macd: List[Optional[float]] = [None] * len(bars)
    for i in range(len(bars)):
        if None in (macd_sig_1[i], macd_sig_2[i]):
            continue
        org_macd[i] = 2.0 * float(macd_sig_1[i]) - float(macd_sig_2[i])

    macd_bull_trigger = [False] * len(bars)
    macd_bear_trigger = [False] * len(bars)
    macd_long_bias = [False] * len(bars)
    macd_short_bias = [False] * len(bars)
    last_bull = -100000
    last_bear = -100000
    for i in range(len(bars)):
        bull_dot = crossover(blue_macd[i], blue_macd[i - 1] if i > 0 else None, org_macd[i], org_macd[i - 1] if i > 0 else None)
        bear_dot = crossunder(blue_macd[i], blue_macd[i - 1] if i > 0 else None, org_macd[i], org_macd[i - 1] if i > 0 else None)
        macd_bull_trigger[i] = bull_dot and org_macd[i] is not None and float(org_macd[i]) < 0.0
        macd_bear_trigger[i] = bear_dot and org_macd[i] is not None and float(org_macd[i]) > 0.0
        if macd_bull_trigger[i]:
            last_bull = i
        if macd_bear_trigger[i]:
            last_bear = i
        macd_long_bias[i] = (i - last_bull) < (i - last_bear)
        macd_short_bias[i] = (i - last_bear) < (i - last_bull)

    rsi_vals = rsi(closes, 8)
    rsi_ma = ema(rsi_vals, 1)
    atr_rsi: List[Optional[float]] = [None] * len(bars)
    for i in range(1, len(bars)):
        if None in (rsi_ma[i], rsi_ma[i - 1]):
            continue
        atr_rsi[i] = abs(float(rsi_ma[i - 1]) - float(rsi_ma[i]))
    ma_atr_rsi = ema(atr_rsi, 15)
    dar_base = ema(ma_atr_rsi, 15)
    dar: List[Optional[float]] = [None] * len(bars)
    for i in range(len(bars)):
        if dar_base[i] is not None:
            dar[i] = float(dar_base[i]) * cfg.qqe_wp

    rsi0: List[Optional[float]] = [None] * len(bars)
    rsi1: List[Optional[float]] = [None] * len(bars)
    for i in range(len(bars)):
        if None in (rsi_ma[i], dar[i]):
            continue
        new_short_band = float(rsi_ma[i]) + float(dar[i])
        new_long_band = float(rsi_ma[i]) - float(dar[i])
        prev_rsi0 = rsi0[i - 1] if i > 0 else None
        prev_rsi1 = rsi1[i - 1] if i > 0 else None
        prev_rsi_ma = rsi_ma[i - 1] if i > 0 else None

        if None not in (prev_rsi_ma, prev_rsi0) and float(prev_rsi_ma) < float(prev_rsi0) and float(rsi_ma[i]) < float(prev_rsi0):
            rsi0[i] = min(float(prev_rsi0), new_short_band)
        else:
            rsi0[i] = new_short_band

        if None not in (prev_rsi_ma, prev_rsi1) and float(prev_rsi_ma) > float(prev_rsi1) and float(rsi_ma[i]) > float(prev_rsi1):
            rsi1[i] = max(float(prev_rsi1), new_long_band)
        else:
            rsi1[i] = new_long_band

    qqe_trend: List[float] = [1.0] * len(bars)
    second_rsi_line: List[Optional[float]] = [None] * len(bars)
    qqe_bull_cross = [False] * len(bars)
    qqe_bear_cross = [False] * len(bars)
    qqe_long_bias = [False] * len(bars)
    qqe_short_bias = [False] * len(bars)
    for i in range(len(bars)):
        rsi0_shift_curr = rsi0[i - 1] if i >= 1 else None
        rsi0_shift_prev = rsi0[i - 2] if i >= 2 else None
        rsi1_shift_curr = rsi1[i - 1] if i >= 1 else None
        rsi1_shift_prev = rsi1[i - 2] if i >= 2 else None
        prev_rsi_ma = rsi_ma[i - 1] if i > 0 else None
        cross_rsi0 = cross(rsi_ma[i], prev_rsi_ma, rsi0_shift_curr, rsi0_shift_prev)
        cross_rsi1 = cross(rsi_ma[i], prev_rsi_ma, rsi1_shift_curr, rsi1_shift_prev)
        if cross_rsi0:
            qqe_trend[i] = 1.0
        elif cross_rsi1:
            qqe_trend[i] = -1.0
        elif i > 0:
            qqe_trend[i] = qqe_trend[i - 1]

        second_rsi_line[i] = rsi1[i] if qqe_trend[i] == 1.0 else rsi0[i]
        qqe_bull_cross[i] = crossover(rsi_ma[i], prev_rsi_ma, second_rsi_line[i], second_rsi_line[i - 1] if i > 0 else None)
        qqe_bear_cross[i] = crossunder(rsi_ma[i], prev_rsi_ma, second_rsi_line[i], second_rsi_line[i - 1] if i > 0 else None)
        if None not in (rsi_ma[i], second_rsi_line[i]):
            qqe_long_bias[i] = float(rsi_ma[i]) > float(second_rsi_line[i])
            qqe_short_bias[i] = float(rsi_ma[i]) < float(second_rsi_line[i])

    raw_long_switch = [macd_long_bias[i] and qqe_bull_cross[i] for i in range(len(bars))]
    raw_short_switch = [macd_short_bias[i] and qqe_bear_cross[i] for i in range(len(bars))]

    ema50 = ema(closes, 50)
    ema100 = ema(closes, 100)
    wma240 = wma(closes, 240)

    trend_allows_long = [False] * len(bars)
    trend_allows_short = [False] * len(bars)
    for i in range(len(bars)):
        bullish_stack = None not in (ema50[i], ema100[i], wma240[i]) and float(ema50[i]) > float(ema100[i]) > float(wma240[i])
        bearish_stack = None not in (ema50[i], ema100[i], wma240[i]) and float(ema50[i]) < float(ema100[i]) < float(wma240[i])
        trend_allows_long[i] = (not cfg.require_trend_stack) or bullish_stack
        trend_allows_short[i] = (not cfg.require_trend_stack) or bearish_stack

    d_close = map_previous_period_close(bars, lambda ts: (ts.year, ts.month, ts.day))
    d_sma = map_previous_htf_series(
        bars,
        lambda ts: (ts.year, ts.month, ts.day),
        lambda bucket: bucket[-1].c,
        lambda vals: rolling_sma(vals, cfg.daily_sma_len),
    )
    h4_close = map_previous_period_close(bars, lambda ts: (ts.year, ts.month, ts.day, ts.hour // 4))
    h4_ema = map_previous_htf_series(
        bars,
        lambda ts: (ts.year, ts.month, ts.day, ts.hour // 4),
        lambda bucket: bucket[-1].c,
        lambda vals: ema(vals, cfg.h4_ema_len),
    )

    raw_long_signal = [raw_long_switch[i] and trend_allows_long[i] for i in range(len(bars))]
    raw_short_signal = [raw_short_switch[i] and trend_allows_short[i] for i in range(len(bars))]
    long_setup = [False] * len(bars)
    short_setup = [False] * len(bars)
    for i in range(len(bars)):
        macro_allows_long = (not cfg.use_macro_trend_filter) or (
            None not in (d_close[i], d_sma[i], h4_close[i], h4_ema[i])
            and float(d_close[i]) > float(d_sma[i])
            and float(h4_close[i]) > float(h4_ema[i])
        )
        macro_allows_short = (not cfg.use_macro_trend_filter) or (
            None not in (d_close[i], d_sma[i], h4_close[i], h4_ema[i])
            and float(d_close[i]) < float(d_sma[i])
            and float(h4_close[i]) < float(h4_ema[i])
        )
        session_allows = (not cfg.use_session_filter) or (7 <= bars[i].ts.hour < 17)
        reward_risk_allowed = cfg.target_r >= cfg.min_required_r
        long_setup[i] = raw_long_signal[i] and macro_allows_long and session_allows and reward_risk_allowed
        short_setup[i] = raw_short_signal[i] and macro_allows_short and session_allows and reward_risk_allowed

    atr_vals = atr(bars, cfg.stop_atr_len)

    trades: List[Trade] = []
    setups = 0
    entries = 0
    canceled = 0
    pending_entry: Optional[PendingEntry] = None
    active: Optional[ActiveTrade] = None
    pending_close = False

    for i, bar in enumerate(bars):
        if pending_close and active is not None:
            close_trade(trades, "QQE/QMP", active, bars, i, bar.o)
            active = None
            pending_close = False

        if pending_entry is not None and pending_entry.signal_index + 1 == i and active is None:
            entry = bar.o
            stop = pending_entry.stop_price
            if pending_entry.direction == 1 and stop >= entry:
                stop = entry - mintick
            if pending_entry.direction == -1 and stop <= entry:
                stop = entry + mintick
            risk = abs(entry - stop)
            if risk > 0:
                target = entry + (risk * cfg.target_r) if pending_entry.direction == 1 else entry - (risk * cfg.target_r)
                active = ActiveTrade(
                    direction=pending_entry.direction,
                    entry_index=i,
                    entry_time=bar.ts,
                    entry=entry,
                    stop=stop,
                    target=target,
                    risk=risk,
                )
                entries += 1
            else:
                canceled += 1
            pending_entry = None

        if active is not None:
            stop_hit = False
            target_hit = False
            if active.direction == 1:
                stop_hit = bar.l <= active.stop
                target_hit = bar.h >= active.target
            else:
                stop_hit = bar.h >= active.stop
                target_hit = bar.l <= active.target

            if stop_hit:
                close_trade(trades, "QQE/QMP", active, bars, i, active.stop)
                active = None
                pending_close = False
            elif target_hit:
                close_trade(trades, "QQE/QMP", active, bars, i, active.target)
                active = None
                pending_close = False
            else:
                if cfg.enable_breakeven and not active.breakeven_armed:
                    if active.direction == 1 and bar.h >= active.entry + (active.risk * cfg.breakeven_at_r):
                        active.breakeven_armed = True
                    elif active.direction == -1 and bar.l <= active.entry - (active.risk * cfg.breakeven_at_r):
                        active.breakeven_armed = True

                if active.breakeven_armed:
                    if active.direction == 1:
                        active.stop = max(active.stop, active.entry)
                    else:
                        active.stop = min(active.stop, active.entry)

                if cfg.exit_on_opposite_qmp:
                    if active.direction == 1 and raw_short_signal[i]:
                        pending_close = True
                    if active.direction == -1 and raw_long_signal[i]:
                        pending_close = True

                if cfg.exit_on_macd_zero_cross and i > 0 and org_macd[i] is not None and org_macd[i - 1] is not None:
                    long_zero_exit = active.direction == 1 and crossunder(org_macd[i], org_macd[i - 1], 0.0, 0.0)
                    short_zero_exit = active.direction == -1 and crossover(org_macd[i], org_macd[i - 1], 0.0, 0.0)
                    if long_zero_exit or short_zero_exit:
                        pending_close = True

                if pending_close and i == len(bars) - 1:
                    close_trade(trades, "QQE/QMP", active, bars, i, bar.c)
                    active = None
                    pending_close = False

        if active is None and pending_entry is None and i + 1 < len(bars):
            if long_setup[i]:
                stop = calc_long_stop(cfg, bars, atr_vals, lows, i)
                if stop is not None and stop < bar.c:
                    pending_entry = PendingEntry(direction=1, signal_index=i, stop_price=stop)
                    setups += 1
            elif short_setup[i]:
                stop = calc_short_stop(cfg, bars, atr_vals, highs, i)
                if stop is not None and stop > bar.c:
                    pending_entry = PendingEntry(direction=-1, signal_index=i, stop_price=stop)
                    setups += 1

    return summarize("QQE/QMP", trades, setups, entries, canceled), trades


def find_default_csvs() -> List[Path]:
    root = Path("Backtesting Data")
    return sorted(root.glob("*_H1_*.csv"))


def pair_from_path(path: Path) -> str:
    return path.name.split("_", 1)[0].upper()
def main() -> int:
    parser = argparse.ArgumentParser(description="Backtest QQE/QMP strategy defaults on MT5 CSV data.")
    parser.add_argument(
        "--csv",
        action="append",
        dest="csvs",
        help="CSV path to backtest. Repeat for multiple files. Defaults to all MT5 H1 CSVs in Backtesting Data/.",
    )
    parser.add_argument(
        "--output-dir",
        default="Backtesting Data/results_qqe_qmp_mt5_2026-02-27",
        help="Directory for per-pair output files.",
    )
    args = parser.parse_args()

    csv_paths = [Path(p) for p in args.csvs] if args.csvs else find_default_csvs()
    if not csv_paths:
        raise FileNotFoundError("No MT5 H1 CSV files found.")

    out_root = Path(args.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    aggregated: List[Dict[str, object]] = []
    for csv_path in csv_paths:
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV not found: {csv_path}")
        bars = load_bars(csv_path)
        mintick = infer_mintick(csv_path)
        summary, trades = run_qqe_qmp(bars, mintick)
        pair = pair_from_path(csv_path)
        pair_dir = out_root / pair
        pair_dir.mkdir(parents=True, exist_ok=True)
        with (pair_dir / "summary.json").open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "source_csv": str(csv_path),
                    "bars": len(bars),
                    "start": bars[0].ts.isoformat(),
                    "end": bars[-1].ts.isoformat(),
                    "mintick": mintick,
                    "result": summary,
                },
                f,
                indent=2,
            )
        write_trades(pair_dir / "trades.csv", trades)

        aggregated.append(
            {
                "pair": pair,
                "source_csv": str(csv_path),
                "bars": len(bars),
                "start": bars[0].ts.isoformat(),
                "end": bars[-1].ts.isoformat(),
                "mintick": mintick,
                "result": summary,
            }
        )

        print(
            f"{pair}: setups={summary['setups']} entries={summary['entries']} "
            f"closed={summary['closed_trades']} win%={summary['win_rate_pct']} "
            f"netR={summary['net_r']} avgR={summary['avg_r']}"
        )

    with (out_root / "summary.json").open("w", encoding="utf-8") as f:
        json.dump({"results": aggregated}, f, indent=2)
    print(f"Wrote: {out_root / 'summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
