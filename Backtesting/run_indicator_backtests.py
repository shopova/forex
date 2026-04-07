#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Bar:
    ts: datetime
    o: float
    h: float
    l: float
    c: float
    v: float


@dataclass
class Trade:
    indicator: str
    direction: int  # 1 long, -1 short
    entry_time: datetime
    exit_time: datetime
    entry: float
    stop: float
    target: float
    exit_price: float
    outcome: str  # win/loss/be
    r: float


def parse_time(s: str) -> datetime:
    s = s.strip()
    if s.endswith("Z"):
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        dt = None
    if dt is None:
        fmts = [
            "%Y.%m.%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y.%m.%d",
            "%Y-%m-%d",
        ]
        for fmt in fmts:
            try:
                dt = datetime.strptime(s, fmt)
                break
            except ValueError:
                continue
    if dt is None:
        raise ValueError(f"Unsupported datetime format: {s}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def load_bars(csv_path: Path) -> List[Bar]:
    def _norm(k: str) -> str:
        return k.strip().lstrip("\ufeff").replace("<", "").replace(">", "").strip().lower()

    def _pick(field_map: Dict[str, str], keys: List[str]) -> Optional[str]:
        for k in keys:
            if k in field_map:
                return field_map[k]
        return None

    bars: List[Bar] = []
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = "\t" if "\t" in sample else ","

        reader = csv.DictReader(f, delimiter=delimiter)
        if not reader.fieldnames:
            raise ValueError(f"No headers found in {csv_path}")

        field_map: Dict[str, str] = {_norm(h): h for h in reader.fieldnames if h is not None}

        time_key = _pick(field_map, ["time", "timestamp"])
        date_key = _pick(field_map, ["date"])
        open_key = _pick(field_map, ["open"])
        high_key = _pick(field_map, ["high"])
        low_key = _pick(field_map, ["low"])
        close_key = _pick(field_map, ["close"])
        vol_key = _pick(field_map, ["volume", "tickvol", "vol"])

        if not (open_key and high_key and low_key and close_key):
            raise ValueError(f"Missing OHLC columns in {csv_path}. Found headers: {reader.fieldnames}")
        if time_key is None and date_key is None:
            raise ValueError(f"Missing time/date columns in {csv_path}. Found headers: {reader.fieldnames}")

        for row in reader:
            if time_key and date_key and time_key != date_key and row.get(date_key) and row.get(time_key):
                ts = parse_time(f"{row[date_key].strip()} {row[time_key].strip()}")
            elif time_key and row.get(time_key):
                ts = parse_time(row[time_key])
            elif date_key and row.get(date_key):
                ts = parse_time(row[date_key])
            else:
                continue

            bars.append(
                Bar(
                    ts=ts,
                    o=float(row[open_key]),
                    h=float(row[high_key]),
                    l=float(row[low_key]),
                    c=float(row[close_key]),
                    v=float(row[vol_key]) if vol_key and row.get(vol_key) not in (None, "") else 0.0,
                )
            )
    return bars


def infer_mintick(csv_path: Path) -> float:
    name = csv_path.name.upper()
    if "JPY" in name:
        return 0.001
    return 0.00001


def infer_pair_key(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    raw = re.sub(r"[^A-Z]", "", name.upper())
    for pair in ("EURUSD", "GBPUSD", "USDCAD", "USDJPY"):
        if pair in raw:
            return pair
    return None


def rolling_sma(vals: List[Optional[float]], length: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    if length <= 0:
        return out
    q: List[float] = []
    s = 0.0
    for i, v in enumerate(vals):
        if v is None:
            q.append(0.0)
        else:
            q.append(v)
            s += v
        if len(q) > length:
            old = q.pop(0)
            s -= old
        if len(q) == length:
            out[i] = s / length
    return out


def ema(vals: List[Optional[float]], length: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    alpha = 2.0 / (length + 1.0)
    prev: Optional[float] = None
    for i, v in enumerate(vals):
        if v is None:
            out[i] = prev
            continue
        if prev is None:
            prev = v
        else:
            prev = alpha * v + (1.0 - alpha) * prev
        out[i] = prev
    return out


def rma(vals: List[Optional[float]], length: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    if length <= 0:
        return out
    seed: List[float] = []
    prev: Optional[float] = None
    for i, v in enumerate(vals):
        if v is None:
            out[i] = prev
            continue
        if prev is None:
            seed.append(v)
            if len(seed) == length:
                prev = sum(seed) / length
                out[i] = prev
            else:
                out[i] = None
        else:
            prev = (prev * (length - 1) + v) / length
            out[i] = prev
    return out


def atr(bars: List[Bar], length: int) -> List[Optional[float]]:
    trs: List[Optional[float]] = [None] * len(bars)
    for i, b in enumerate(bars):
        if i == 0:
            trs[i] = b.h - b.l
        else:
            pc = bars[i - 1].c
            trs[i] = max(b.h - b.l, abs(b.h - pc), abs(b.l - pc))
    return rma(trs, length)


def rsi(closes: List[float], length: int) -> List[Optional[float]]:
    gains: List[Optional[float]] = [None] * len(closes)
    losses: List[Optional[float]] = [None] * len(closes)
    for i in range(1, len(closes)):
        ch = closes[i] - closes[i - 1]
        gains[i] = max(ch, 0.0)
        losses[i] = max(-ch, 0.0)
    rg = rma(gains, length)
    rl = rma(losses, length)
    out: List[Optional[float]] = [None] * len(closes)
    for i in range(len(closes)):
        if rg[i] is None or rl[i] is None:
            out[i] = None
        elif rl[i] == 0:
            out[i] = 100.0
        else:
            rs = rg[i] / rl[i]
            out[i] = 100.0 - (100.0 / (1.0 + rs))
    return out


def highest(vals: List[float], start: int, end: int) -> Optional[float]:
    if start < 0 or end < start:
        return None
    return max(vals[start : end + 1])


def lowest(vals: List[float], start: int, end: int) -> Optional[float]:
    if start < 0 or end < start:
        return None
    return min(vals[start : end + 1])


def pivot_low(vals: List[float], left: int, right: int) -> List[Optional[float]]:
    n = len(vals)
    out: List[Optional[float]] = [None] * n
    for i in range(n):
        c = i - right
        if c - left < 0 or c + right >= n:
            continue
        w = vals[c - left : c + right + 1]
        if vals[c] == min(w):
            out[i] = vals[c]
    return out


def pivot_high(vals: List[float], left: int, right: int) -> List[Optional[float]]:
    n = len(vals)
    out: List[Optional[float]] = [None] * n
    for i in range(n):
        c = i - right
        if c - left < 0 or c + right >= n:
            continue
        w = vals[c - left : c + right + 1]
        if vals[c] == max(w):
            out[i] = vals[c]
    return out


def map_previous_htf_series(
    bars: List[Bar],
    period_key_fn,
    period_close_fn,
    period_metric_fn,
) -> List[Optional[float]]:
    period_to_close: Dict[Tuple[int, ...], float] = {}
    last_key: Optional[Tuple[int, ...]] = None
    bucket: List[Bar] = []

    for b in bars:
        key = period_key_fn(b.ts)
        if last_key is None:
            last_key = key
        if key != last_key:
            period_to_close[last_key] = period_close_fn(bucket)
            bucket = []
            last_key = key
        bucket.append(b)
    if last_key is not None and bucket:
        period_to_close[last_key] = period_close_fn(bucket)

    sorted_keys = sorted(period_to_close.keys())
    metric_vals = period_metric_fn([period_to_close[k] for k in sorted_keys])

    prev_metric: Dict[Tuple[int, ...], Optional[float]] = {}
    prev = None
    for k, mv in zip(sorted_keys, metric_vals):
        prev_metric[k] = prev
        prev = mv

    out: List[Optional[float]] = [None] * len(bars)
    for i, b in enumerate(bars):
        key = period_key_fn(b.ts)
        out[i] = prev_metric.get(key)
    return out


def map_previous_period_close(bars: List[Bar], period_key_fn) -> List[Optional[float]]:
    period_close: Dict[Tuple[int, ...], float] = {}
    last_key: Optional[Tuple[int, ...]] = None
    bucket: List[Bar] = []

    for b in bars:
        key = period_key_fn(b.ts)
        if last_key is None:
            last_key = key
        if key != last_key:
            period_close[last_key] = bucket[-1].c
            bucket = []
            last_key = key
        bucket.append(b)
    if last_key is not None and bucket:
        period_close[last_key] = bucket[-1].c

    keys = sorted(period_close.keys())
    prev_close_map: Dict[Tuple[int, ...], Optional[float]] = {}
    prev = None
    for k in keys:
        prev_close_map[k] = prev
        prev = period_close[k]

    out: List[Optional[float]] = [None] * len(bars)
    for i, b in enumerate(bars):
        out[i] = prev_close_map.get(period_key_fn(b.ts))
    return out


def summarize(indicator: str, trades: List[Trade], setups: int, entries: int, canceled: int) -> Dict[str, object]:
    wins = sum(1 for t in trades if t.outcome == "win")
    losses = sum(1 for t in trades if t.outcome == "loss")
    bes = sum(1 for t in trades if t.outcome == "be")
    total_r = sum(t.r for t in trades)
    win_rate = (wins / len(trades) * 100.0) if trades else 0.0

    eq = 0.0
    peak = 0.0
    max_dd = 0.0
    for t in trades:
        eq += t.r
        peak = max(peak, eq)
        max_dd = max(max_dd, peak - eq)

    return {
        "indicator": indicator,
        "setups": setups,
        "entries": entries,
        "canceled_setups": canceled,
        "closed_trades": len(trades),
        "wins": wins,
        "losses": losses,
        "breakeven": bes,
        "win_rate_pct": round(win_rate, 2),
        "net_r": round(total_r, 2),
        "avg_r": round((total_r / len(trades)) if trades else 0.0, 3),
        "max_drawdown_r": round(max_dd, 2),
    }


def in_session_0700_1700(ts: datetime) -> bool:
    h = ts.hour
    return 7 <= h < 17


def run_last_kiss(
    bars: List[Bar],
    mintick: float,
    disable_trend_filter: bool = False,
    disable_session_filter: bool = False,
    overrides: Optional[Dict[str, object]] = None,
) -> Tuple[Dict[str, object], List[Trade]]:
    cfg: Dict[str, object] = {
        "minConsolBars": 20,
        "maxConsolBars": 80,
        "minTouches": 2,
        "touchTolPct": 8.0,
        "touchTolTicks": 8,
        "rangeVolBufAtr": 0.10,
        "rangeVolBufTicks": 5,
        "recentTouchWindow": 12,
        "minRecentBoundaryTouches": 2,
        "maxBoundaryStaleBars": 30,
        "maxConsolDriftPct": 25.0,
        "maxOutsideCloses": 1,
        "maxOutsideCloseRun": 2,
        "atrLen": 14,
        "minBoxAtr": 1.2,
        "maxBoxAtr": 6.0,
        "breakoutCloseOnly": True,
        "breakoutBufferAtr": 0.10,
        "minBreakoutBodyAtr": 0.25,
        "useVolumeFilter": True,
        "volLen": 20,
        "volMult": 1.1,
        "maxFakeBreakouts": 2,
        "maxRetestBars": 15,
        "retestTolPct": 12.0,
        "retestTolTicks": 10,
        "minCatalystBodyAtr": 0.20,
        "closeNearExtremePct": 25.0,
        "minWickBodyRatio": 0.20,
        "entryOffsetTicks": 2,
        "entryExpiryBars": 5,
        "stopMode": "Midpoint of Box",
        "stopAtrMult": 1.0,
        "targetMode": "R Multiple",
        "targetRR": 2.0,
        "minSetupRR": 2.0,
        "targetPivotLen": 3,
        "targetZoneBufferTicks": 2,
        "useTrendFilter": True,
        "dailySmaLen": 200,
        "h4EmaLen": 50,
        "useSessionFilter": True,
        "maxNoZoneTouchBars": 120,
    }
    if overrides:
        cfg.update(overrides)

    if "boxLookback" in cfg:
        if "minConsolBars" not in cfg:
            cfg["minConsolBars"] = cfg["boxLookback"]
        if "maxConsolBars" not in cfg:
            cfg["maxConsolBars"] = cfg["boxLookback"]

    minConsolBars = int(cfg["minConsolBars"])
    maxConsolBars = int(cfg["maxConsolBars"])
    minTouches = int(cfg["minTouches"])
    touchTolPct = float(cfg["touchTolPct"])
    touchTolTicks = int(cfg["touchTolTicks"])
    rangeVolBufAtr = float(cfg["rangeVolBufAtr"])
    rangeVolBufTicks = int(cfg["rangeVolBufTicks"])
    recentTouchWindow = int(cfg["recentTouchWindow"])
    minRecentBoundaryTouches = int(cfg["minRecentBoundaryTouches"])
    maxBoundaryStaleBars = int(cfg["maxBoundaryStaleBars"])
    maxConsolDriftPct = float(cfg["maxConsolDriftPct"])
    maxOutsideCloses = int(cfg["maxOutsideCloses"])
    maxOutsideCloseRun = int(cfg["maxOutsideCloseRun"])
    atrLen = int(cfg["atrLen"])
    minBoxAtr = float(cfg["minBoxAtr"])
    maxBoxAtr = float(cfg["maxBoxAtr"])

    breakoutCloseOnly = bool(cfg["breakoutCloseOnly"])
    breakoutBufferAtr = float(cfg["breakoutBufferAtr"])
    minBreakoutBodyAtr = float(cfg["minBreakoutBodyAtr"])
    useVolumeFilter = bool(cfg["useVolumeFilter"])
    volLen = int(cfg["volLen"])
    volMult = float(cfg["volMult"])
    maxFakeBreakouts = int(cfg["maxFakeBreakouts"])

    maxRetestBars = int(cfg["maxRetestBars"])
    retestTolPct = float(cfg["retestTolPct"])
    retestTolTicks = int(cfg["retestTolTicks"])
    minCatalystBodyAtr = float(cfg["minCatalystBodyAtr"])
    closeNearExtremePct = float(cfg["closeNearExtremePct"])
    minWickBodyRatio = float(cfg["minWickBodyRatio"])

    entryOffsetTicks = int(cfg["entryOffsetTicks"])
    entryExpiryBars = int(cfg["entryExpiryBars"])
    stopMode = str(cfg["stopMode"])
    stopAtrMult = float(cfg["stopAtrMult"])
    targetMode = str(cfg["targetMode"])
    targetRR = float(cfg["targetRR"])
    minSetupRR = float(cfg["minSetupRR"])
    targetPivotLen = int(cfg["targetPivotLen"])
    targetZoneBufferTicks = int(cfg["targetZoneBufferTicks"])

    useTrendFilter = bool(cfg["useTrendFilter"])
    dailySmaLen = int(cfg["dailySmaLen"])
    h4EmaLen = int(cfg["h4EmaLen"])
    useSessionFilter = bool(cfg["useSessionFilter"])
    maxNoZoneTouchBars = int(cfg["maxNoZoneTouchBars"])

    searchMinBars = min(minConsolBars, maxConsolBars)
    searchMaxBars = max(minConsolBars, maxConsolBars)

    if disable_trend_filter:
        useTrendFilter = False
    if disable_session_filter:
        useSessionFilter = False

    closes = [b.c for b in bars]
    highs = [b.h for b in bars]
    lows = [b.l for b in bars]
    opens = [b.o for b in bars]
    volumes = [b.v for b in bars]

    atr_vals = atr(bars, atrLen)
    vol_ma = rolling_sma([v for v in volumes], volLen)
    pLow = pivot_low(lows, targetPivotLen, targetPivotLen)
    pHigh = pivot_high(highs, targetPivotLen, targetPivotLen)

    d_close = map_previous_period_close(bars, lambda t: (t.year, t.month, t.day))
    d_sma = map_previous_htf_series(
        bars,
        lambda t: (t.year, t.month, t.day),
        lambda bucket: bucket[-1].c,
        lambda seq: rolling_sma([v for v in seq], dailySmaLen),
    )
    h4_close = map_previous_period_close(bars, lambda t: (t.year, t.month, t.day, t.hour // 4))
    h4_ema = map_previous_htf_series(
        bars,
        lambda t: (t.year, t.month, t.day, t.hour // 4),
        lambda bucket: bucket[-1].c,
        lambda seq: ema([v for v in seq], h4EmaLen),
    )

    supportZone: Optional[float] = None
    resistanceZone: Optional[float] = None

    state = 0
    boxTop: Optional[float] = None
    boxBottom: Optional[float] = None
    boxStartBar: Optional[int] = None
    breakoutBar: Optional[int] = None
    direction = 0
    fakeBreakouts = 0
    entryPrice: Optional[float] = None
    stopPrice: Optional[float] = None
    targetPrice: Optional[float] = None
    setupBar: Optional[int] = None
    outsideCloseRun = 0
    lastZoneTouchBar: Optional[int] = None
    lastTopTouchBar: Optional[int] = None
    lastBottomTouchBar: Optional[int] = None

    active_trade = None
    trades: List[Trade] = []
    setups = 0
    entries = 0
    canceled = 0

    def box_tol(height: float) -> float:
        return max(mintick * touchTolTicks, height * touchTolPct * 0.01)

    def range_vol_buf(a: float) -> float:
        return max(mintick * rangeVolBufTicks, a * rangeVolBufAtr)

    def retest_tol(height: float) -> float:
        return max(mintick * retestTolTicks, height * retestTolPct * 0.01)

    def reset_box():
        nonlocal state, boxTop, boxBottom, boxStartBar, breakoutBar, direction, fakeBreakouts, entryPrice, stopPrice, targetPrice, setupBar
        nonlocal outsideCloseRun, lastZoneTouchBar, lastTopTouchBar, lastBottomTouchBar
        state = 0
        boxTop = None
        boxBottom = None
        boxStartBar = None
        breakoutBar = None
        direction = 0
        fakeBreakouts = 0
        entryPrice = None
        stopPrice = None
        targetPrice = None
        setupBar = None
        outsideCloseRun = 0
        lastZoneTouchBar = None
        lastTopTouchBar = None
        lastBottomTouchBar = None

    for i, b in enumerate(bars):
        a = atr_vals[i]
        if a is None:
            continue

        if pLow[i] is not None:
            supportZone = pLow[i]
        if pHigh[i] is not None:
            resistanceZone = pHigh[i]

        # Manage active trade first (this extension is required for backtest PnL)
        if active_trade is not None:
            adir = active_trade["dir"]
            ent = active_trade["entry"]
            stp = active_trade["stop"]
            tgt = active_trade["target"]
            rrisk = max(abs(ent - stp), mintick)
            if adir == 1:
                stop_touched = b.l <= stp
                target_touched = b.h >= tgt
            else:
                stop_touched = b.h >= stp
                target_touched = b.l <= tgt

            if stop_touched or target_touched:
                if stop_touched:
                    outcome = "loss"
                    exit_px = stp
                    r = -1.0
                else:
                    outcome = "win"
                    exit_px = tgt
                    r = (tgt - ent) / rrisk if adir == 1 else (ent - tgt) / rrisk
                trades.append(
                    Trade(
                        indicator="Last Kiss",
                        direction=adir,
                        entry_time=active_trade["entry_time"],
                        exit_time=b.ts,
                        entry=ent,
                        stop=stp,
                        target=tgt,
                        exit_price=exit_px,
                        outcome=outcome,
                        r=round(r, 3),
                    )
                )
                active_trade = None

        candLen: Optional[int] = None
        candTop: Optional[float] = None
        candBottom: Optional[float] = None
        candidateValid = False
        if state == 0:
            enoughData = i >= searchMaxBars
            if enoughData:
                for length in range(searchMinBars, searchMaxBars + 1):
                    start = i - length + 1
                    if start < 0:
                        continue
                    t = max(highs[start : i + 1])
                    bot = min(lows[start : i + 1])
                    h = t - bot
                    tol = box_tol(h) + range_vol_buf(a)
                    recentLen = min(recentTouchWindow, length)
                    recentStart = i - recentLen + 1

                    topTouches = sum(1 for x in highs[start : i + 1] if x >= t - tol)
                    bottomTouches = sum(1 for x in lows[start : i + 1] if x <= bot + tol)
                    topTouchesRecent = sum(1 for x in highs[recentStart : i + 1] if x >= t - tol)
                    bottomTouchesRecent = sum(1 for x in lows[recentStart : i + 1] if x <= bot + tol)
                    outsideCloses = sum(1 for x in closes[start : i + 1] if (x > t + tol or x < bot - tol))
                    drift = abs(closes[i] - closes[start])

                    heightOk = h >= a * minBoxAtr and h <= a * maxBoxAtr
                    touchesOk = topTouches >= minTouches and bottomTouches >= minTouches
                    recentBoundaryActive = (
                        topTouchesRecent >= minRecentBoundaryTouches and bottomTouchesRecent >= minRecentBoundaryTouches
                    )
                    driftOk = h > 0 and drift <= h * maxConsolDriftPct * 0.01
                    outsideOk = outsideCloses <= maxOutsideCloses
                    valid = heightOk and touchesOk and recentBoundaryActive and driftOk and outsideOk

                    if valid and (candLen is None or length > candLen):
                        candLen = length
                        candTop = t
                        candBottom = bot
            candidateValid = candLen is not None

        trendLong = (
            d_close[i] is not None
            and d_sma[i] is not None
            and h4_close[i] is not None
            and h4_ema[i] is not None
            and d_close[i] > d_sma[i]
            and h4_close[i] > h4_ema[i]
        )
        trendShort = (
            d_close[i] is not None
            and d_sma[i] is not None
            and h4_close[i] is not None
            and h4_ema[i] is not None
            and d_close[i] < d_sma[i]
            and h4_close[i] < h4_ema[i]
        )
        inSession = in_session_0700_1700(b.ts)

        if state == 0 and candidateValid and candTop is not None and candBottom is not None and candLen is not None:
            boxTop = candTop
            boxBottom = candBottom
            boxStartBar = i - candLen + 1
            breakoutBar = None
            direction = 0
            fakeBreakouts = 0
            entryPrice = None
            stopPrice = None
            targetPrice = None
            setupBar = None
            outsideCloseRun = 0
            lastZoneTouchBar = i
            lastTopTouchBar = i
            lastBottomTouchBar = i
            state = 1

        if state == 1 and boxTop is not None and boxBottom is not None:
            activeHeight = boxTop - boxBottom
            activeTouchTol = box_tol(activeHeight) + range_vol_buf(a)
            inBoxNow = b.h >= boxBottom - activeTouchTol and b.l <= boxTop + activeTouchTol
            topTouchedNow = b.h >= boxTop - activeTouchTol
            bottomTouchedNow = b.l <= boxBottom + activeTouchTol
            closeOutsideNow = b.c > boxTop + activeTouchTol or b.c < boxBottom - activeTouchTol

            if inBoxNow:
                lastZoneTouchBar = i
            if topTouchedNow:
                lastTopTouchBar = i
            if bottomTouchedNow:
                lastBottomTouchBar = i
            outsideCloseRun = (outsideCloseRun + 1) if closeOutsideNow else 0

            inactiveTooLong = lastZoneTouchBar is not None and (i - lastZoneTouchBar > maxNoZoneTouchBars)
            topStale = lastTopTouchBar is not None and (i - lastTopTouchBar > maxBoundaryStaleBars)
            bottomStale = lastBottomTouchBar is not None and (i - lastBottomTouchBar > maxBoundaryStaleBars)
            staleBoundary = topStale or bottomStale
            outsideRunInvalid = outsideCloseRun > maxOutsideCloseRun

            if inactiveTooLong or staleBoundary or outsideRunInvalid:
                canceled += 1
                reset_box()
            else:
                breakBuf = a * breakoutBufferAtr
                breakoutBodyOk = abs(b.c - b.o) >= a * minBreakoutBodyAtr
                breakoutVolumeOk = (not useVolumeFilter) or (
                    vol_ma[i] is not None and b.v > vol_ma[i] * volMult
                )
                prev_close = bars[i - 1].c if i > 0 else b.c
                longBreakRaw = b.c > boxTop + breakBuf if breakoutCloseOnly else b.h > boxTop + breakBuf
                shortBreakRaw = b.c < boxBottom - breakBuf if breakoutCloseOnly else b.l < boxBottom - breakBuf
                longBreak = longBreakRaw and prev_close <= boxTop and breakoutBodyOk and breakoutVolumeOk
                shortBreak = shortBreakRaw and prev_close >= boxBottom and breakoutBodyOk and breakoutVolumeOk

                if longBreak:
                    direction = 1
                    breakoutBar = i
                    state = 2
                    lastTopTouchBar = i
                    outsideCloseRun = 0
                elif shortBreak:
                    direction = -1
                    breakoutBar = i
                    state = 2
                    lastBottomTouchBar = i
                    outsideCloseRun = 0

        if state == 2 and boxTop is not None and boxBottom is not None and breakoutBar is not None:
            barsFromBreak = i - breakoutBar
            bHeight = boxTop - boxBottom
            rTol = retest_tol(bHeight)
            edge = boxTop if direction == 1 else boxBottom
            touchedEdge = b.h >= edge - rTol and b.l <= edge + rTol

            rng = max(b.h - b.l, mintick)
            body = abs(b.c - b.o)
            bodyOk = body >= a * minCatalystBodyAtr
            closeNearHigh = (b.h - b.c) <= rng * closeNearExtremePct * 0.01
            closeNearLow = (b.c - b.l) <= rng * closeNearExtremePct * 0.01
            lowerWick = min(b.o, b.c) - b.l
            upperWick = b.h - max(b.o, b.c)
            bullWickOk = lowerWick >= body * minWickBodyRatio
            bearWickOk = upperWick >= body * minWickBodyRatio

            bullCatalyst = direction == 1 and touchedEdge and b.c > b.o and bodyOk and closeNearHigh and bullWickOk
            bearCatalyst = direction == -1 and touchedEdge and b.c < b.o and bodyOk and closeNearLow and bearWickOk

            trendOk = (not useTrendFilter) or (trendLong if direction == 1 else trendShort)
            sessionOk = (not useSessionFilter) or inSession

            if (bullCatalyst or bearCatalyst) and trendOk and sessionOk:
                entryPrice = b.h + mintick * entryOffsetTicks if direction == 1 else b.l - mintick * entryOffsetTicks
                boxMid = (boxTop + boxBottom) * 0.5
                if stopMode == "Midpoint of Box":
                    stopPrice = boxMid
                elif stopMode == "Opposite Box Edge":
                    stopPrice = boxBottom if direction == 1 else boxTop
                else:
                    stopPrice = (boxBottom - a * stopAtrMult) if direction == 1 else (boxTop + a * stopAtrMult)
                risk = max(abs(entryPrice - stopPrice), mintick)
                rrTarget = entryPrice + direction * risk * targetRR
                targetZoneBuffer = mintick * targetZoneBufferTicks
                zoneTargetLong = (
                    (resistanceZone - targetZoneBuffer)
                    if (resistanceZone is not None and resistanceZone > entryPrice)
                    else None
                )
                zoneTargetShort = (
                    (supportZone + targetZoneBuffer)
                    if (supportZone is not None and supportZone < entryPrice)
                    else None
                )
                zoneTarget = zoneTargetLong if direction == 1 else zoneTargetShort
                targetPrice = rrTarget
                if targetMode == "Nearest Zone" and zoneTarget is not None:
                    targetPrice = zoneTarget
                setupRR = (
                    (targetPrice - entryPrice) / risk if direction == 1 else (entryPrice - targetPrice) / risk
                )

                if setupRR >= minSetupRR:
                    setupBar = i
                    state = 3
                    setups += 1
                else:
                    entryPrice = None
                    stopPrice = None
                    targetPrice = None
            else:
                failedBreak = b.c < boxTop if direction == 1 else b.c > boxBottom
                timedOut = barsFromBreak > maxRetestBars
                if failedBreak or timedOut:
                    fakeBreakouts += 1
                    canceled += 1
                    prevDirection = direction
                    direction = 0
                    breakoutBar = None
                    entryPrice = None
                    stopPrice = None
                    targetPrice = None
                    setupBar = None
                    if fakeBreakouts >= maxFakeBreakouts:
                        reset_box()
                    else:
                        state = 1
                        lastZoneTouchBar = i
                        if prevDirection == 1:
                            lastTopTouchBar = i
                        elif prevDirection == -1:
                            lastBottomTouchBar = i
                        outsideCloseRun = 0

        if state == 3 and setupBar is not None and entryPrice is not None and stopPrice is not None and targetPrice is not None:
            barsSinceSetup = i - setupBar
            entryTriggered = b.h >= entryPrice if direction == 1 else b.l <= entryPrice
            invalidBeforeTrigger = b.l <= stopPrice if direction == 1 else b.h >= stopPrice
            expired = barsSinceSetup > entryExpiryBars

            if entryTriggered:
                entries += 1
                active_trade = {
                    "dir": direction,
                    "entry": entryPrice,
                    "stop": stopPrice,
                    "target": targetPrice,
                    "entry_time": b.ts,
                }
                reset_box()
            elif invalidBeforeTrigger or expired:
                canceled += 1
                reset_box()

    if active_trade is not None:
        # Forced close at last bar for reporting consistency.
        last = bars[-1]
        adir = active_trade["dir"]
        e = active_trade["entry"]
        stp = active_trade["stop"]
        tgt = active_trade["target"]
        rrisk = max(abs(e - stp), mintick)
        r = (last.c - e) / rrisk if adir == 1 else (e - last.c) / rrisk
        outcome = "be" if abs(r) < 0.05 else ("win" if r > 0 else "loss")
        trades.append(
            Trade(
                indicator="Last Kiss",
                direction=adir,
                entry_time=active_trade["entry_time"],
                exit_time=last.ts,
                entry=e,
                stop=stp,
                target=tgt,
                exit_price=last.c,
                outcome=outcome,
                r=round(r, 3),
            )
        )

    return summarize("Last Kiss", trades, setups, entries, canceled), trades


def run_big_shadow(
    bars: List[Bar],
    mintick: float,
    disable_trend_filter: bool = False,
    disable_session_filter: bool = False,
    overrides: Optional[Dict[str, object]] = None,
    pair_name: Optional[str] = None,
) -> Tuple[Dict[str, object], List[Trade]]:
    cfg: Dict[str, object] = {
        "profileMode": "Balanced",
        "pairPresetMode": "Off (Manual Inputs)",
        "atrLen": 14,
        "requireOutsideBar": True,
        "dominanceMode": "Previous 10 Candles (A+)",
        "minRangeVsPrev": 1.20,
        "minRangeAtr": 1.0,
        "closeExtremeTicks": 10,
        "closeExtremeAtr": 0.03,
        "useZoneFilter": False,
        "pivotLen": 3,
        "zoneTolTicks": 8,
        "zoneTolAtr": 0.10,
        "requireExtreme": False,
        "extremeLookback": 20,
        "useRoomLeftFilter": False,
        "roomLeftBars": 7,
        "entryOffsetTicks": 2,
        "stopOffsetTicks": 2,
        "stopOffsetAtr": 0.05,
        "triggerMode": "Next Candle (A+)",
        "entryExpiryBars": 5,
        "targetMode": "R Multiple",
        "targetRR": 2.0,
        "minSetupRR": 2.0,
        "targetZoneBufferTicks": 2,
        "breakevenAtR": 1.0,
        "useTrendFilter": True,
        "dailySmaLen": 200,
        "h4EmaLen": 50,
        "useSessionFilter": False,
    }
    if overrides:
        cfg.update(overrides)

    profileMode = str(cfg["profileMode"])
    pairPresetMode = str(cfg["pairPresetMode"])
    atrLen = int(cfg["atrLen"])
    requireOutsideBar = bool(cfg["requireOutsideBar"])
    dominanceMode = str(cfg["dominanceMode"])
    minRangeVsPrev = float(cfg["minRangeVsPrev"])
    minRangeAtr = float(cfg["minRangeAtr"])
    closeExtremeTicks = int(cfg["closeExtremeTicks"])
    closeExtremeAtr = float(cfg["closeExtremeAtr"])

    useZoneFilter = bool(cfg["useZoneFilter"])
    pivotLen = int(cfg["pivotLen"])
    zoneTolTicks = int(cfg["zoneTolTicks"])
    zoneTolAtr = float(cfg["zoneTolAtr"])
    requireExtreme = bool(cfg["requireExtreme"])
    extremeLookback = int(cfg["extremeLookback"])
    useRoomLeftFilter = bool(cfg["useRoomLeftFilter"])
    roomLeftBars = int(cfg["roomLeftBars"])

    entryOffsetTicks = int(cfg["entryOffsetTicks"])
    stopOffsetTicks = int(cfg["stopOffsetTicks"])
    stopOffsetAtr = float(cfg["stopOffsetAtr"])
    triggerMode = str(cfg["triggerMode"])
    entryExpiryBars = int(cfg["entryExpiryBars"])
    targetMode = str(cfg["targetMode"])
    targetRR = float(cfg["targetRR"])
    minSetupRR = float(cfg["minSetupRR"])
    targetZoneBufferTicks = int(cfg["targetZoneBufferTicks"])
    breakevenAtR = float(cfg["breakevenAtR"])

    useTrendFilter = bool(cfg["useTrendFilter"])
    dailySmaLen = int(cfg["dailySmaLen"])
    h4EmaLen = int(cfg["h4EmaLen"])
    useSessionFilter = bool(cfg["useSessionFilter"])

    strictProfile = profileMode == "A+ Strict"
    customProfile = profileMode == "Custom"
    pair_key_override = cfg.get("pairKey")
    pairKey = str(pair_key_override).upper() if pair_key_override is not None else infer_pair_key(pair_name)
    usePairPreset = pairPresetMode == "MT5 Per-Pair >=2R (2020-2026)"
    presetEURUSD = usePairPreset and pairKey == "EURUSD"
    presetGBPUSD = usePairPreset and pairKey == "GBPUSD"
    presetUSDJPY = usePairPreset and pairKey == "USDJPY"
    presetUSDCAD = usePairPreset and pairKey == "USDCAD"
    presetMajor = presetEURUSD or presetGBPUSD or presetUSDJPY or presetUSDCAD
    presetGBPUSDJPY = presetGBPUSD or presetUSDJPY

    effectiveUseZoneFilter = False if presetMajor else useZoneFilter
    effectiveRequireOutsideBar = True if presetUSDCAD else (False if presetMajor else requireOutsideBar)
    effectiveDominanceMode = (
        "Previous 10 Candles (A+)"
        if presetGBPUSDJPY
        else ("Previous 5 Candles" if presetMajor else dominanceMode)
    )
    effectiveMinRangeVsPrev = 1.2 if (presetEURUSD or presetUSDCAD) else (1.1 if presetGBPUSDJPY else minRangeVsPrev)
    effectiveMinRangeAtr = 0.9 if presetEURUSD else (0.5 if presetUSDCAD else (0.7 if presetGBPUSDJPY else minRangeAtr))
    effectiveCloseExtremeTicks = 20 if (presetEURUSD or presetGBPUSDJPY) else (15 if presetUSDCAD else closeExtremeTicks)
    effectiveCloseExtremeAtr = 0.02 if presetEURUSD else (0.05 if (presetUSDCAD or presetGBPUSDJPY) else closeExtremeAtr)
    effectiveEntryOffsetTicks = 1 if presetEURUSD else (2 if (presetUSDCAD or presetGBPUSDJPY) else entryOffsetTicks)
    effectiveStopOffsetTicks = 1 if (presetEURUSD or presetGBPUSDJPY) else (3 if presetUSDCAD else stopOffsetTicks)
    effectiveStopOffsetAtr = 0.10 if presetEURUSD else (0.02 if presetUSDCAD else (0.05 if presetGBPUSDJPY else stopOffsetAtr))
    effectiveTriggerMode = "Within N Candles" if presetUSDCAD else ("Next Candle (A+)" if presetMajor else triggerMode)
    effectiveEntryExpiryBars = 3 if presetUSDCAD else (7 if presetGBPUSDJPY else (5 if presetEURUSD else entryExpiryBars))
    effectiveBreakevenAtR = 1.2 if presetEURUSD else (1.5 if (presetUSDCAD or presetGBPUSDJPY) else breakevenAtR)
    effectiveRequireExtreme = True if presetEURUSD else (False if presetMajor else (requireExtreme if customProfile else strictProfile))
    effectiveUseRoomLeftFilter = False if presetMajor else (useRoomLeftFilter if customProfile else strictProfile)
    effectiveUseSessionFilter = False if presetMajor else (useSessionFilter if customProfile else strictProfile)
    effectiveUseTrendFilter = False if presetMajor else useTrendFilter
    dominanceLookback = 10 if effectiveDominanceMode == "Previous 10 Candles (A+)" else 5

    if disable_trend_filter:
        effectiveUseTrendFilter = False
    if disable_session_filter:
        effectiveUseSessionFilter = False

    highs = [b.h for b in bars]
    lows = [b.l for b in bars]
    opens = [b.o for b in bars]
    closes = [b.c for b in bars]

    atr_vals = atr(bars, atrLen)

    d_close = map_previous_period_close(bars, lambda t: (t.year, t.month, t.day))
    d_sma = map_previous_htf_series(
        bars,
        lambda t: (t.year, t.month, t.day),
        lambda bucket: bucket[-1].c,
        lambda seq: rolling_sma([v for v in seq], dailySmaLen),
    )
    h4_close = map_previous_period_close(bars, lambda t: (t.year, t.month, t.day, t.hour // 4))
    h4_ema = map_previous_htf_series(
        bars,
        lambda t: (t.year, t.month, t.day, t.hour // 4),
        lambda bucket: bucket[-1].c,
        lambda seq: ema([v for v in seq], h4EmaLen),
    )

    pLow = pivot_low(lows, pivotLen, pivotLen)
    pHigh = pivot_high(highs, pivotLen, pivotLen)

    supportZone: Optional[float] = None
    resistanceZone: Optional[float] = None

    pendingDir = 0
    pendingEntry = None
    pendingStop = None
    pendingTarget = None
    pendingBE = None
    pendingBar = None

    tradeDir = 0
    tradeEntry = None
    tradeStop = None
    tradeTarget = None
    tradeBE = None
    movedToBE = False
    current_entry_time: Optional[datetime] = None

    trades: List[Trade] = []
    setups = 0
    entries = 0
    canceled = 0

    for i, b in enumerate(bars):
        a = atr_vals[i]
        if a is None or i < 2:
            continue

        if pLow[i] is not None:
            supportZone = pLow[i]
        if pHigh[i] is not None:
            resistanceZone = pHigh[i]

        zoneTol = max(mintick * zoneTolTicks, a * zoneTolAtr)
        closeTol = max(mintick * effectiveCloseExtremeTicks, a * effectiveCloseExtremeAtr)
        stopBuf = max(mintick * effectiveStopOffsetTicks, a * effectiveStopOffsetAtr)
        targetZoneBuffer = mintick * targetZoneBufferTicks

        trendLong = (
            d_close[i] is not None
            and d_sma[i] is not None
            and h4_close[i] is not None
            and h4_ema[i] is not None
            and d_close[i] > d_sma[i]
            and h4_close[i] > h4_ema[i]
        )
        trendShort = (
            d_close[i] is not None
            and d_sma[i] is not None
            and h4_close[i] is not None
            and h4_ema[i] is not None
            and d_close[i] < d_sma[i]
            and h4_close[i] < h4_ema[i]
        )
        inSession = in_session_0700_1700(b.ts)

        atSupport = supportZone is not None and b.l <= supportZone + zoneTol and b.l >= supportZone - zoneTol
        atResistance = resistanceZone is not None and b.h >= resistanceZone - zoneTol and b.h <= resistanceZone + zoneTol

        enoughBars = i > max(max(dominanceLookback, roomLeftBars), extremeLookback) + 2
        candleRange = max(b.h - b.l, mintick)
        prevRange = max(highs[i - 1] - lows[i - 1], mintick)
        prevRanges = [highs[j] - lows[j] for j in range(max(0, i - dominanceLookback), i)]
        prevMaxRange = max(prevRanges) if len(prevRanges) >= dominanceLookback else None

        outsideBar = b.h > highs[i - 1] and b.l < lows[i - 1]
        dominantRange = (
            prevMaxRange is not None
            and candleRange > prevMaxRange
            and candleRange >= prevRange * effectiveMinRangeVsPrev
            and candleRange >= a * effectiveMinRangeAtr
        )

        bullCloseOk = (b.h - b.c) <= closeTol and b.c > b.o
        bearCloseOk = (b.c - b.l) <= closeTol and b.c < b.o

        lo_ext = min(lows[i - extremeLookback + 1 : i + 1]) if i - extremeLookback + 1 >= 0 else None
        hi_ext = max(highs[i - extremeLookback + 1 : i + 1]) if i - extremeLookback + 1 >= 0 else None
        bullExtreme = lo_ext is not None and b.l <= lo_ext
        bearExtreme = hi_ext is not None and b.h >= hi_ext

        lleft = lows[i - roomLeftBars : i] if i - roomLeftBars >= 0 else []
        hleft = highs[i - roomLeftBars : i] if i - roomLeftBars >= 0 else []
        bullRoomLeftZone = supportZone is not None and lleft and min(lleft) > supportZone + zoneTol
        bearRoomLeftZone = resistanceZone is not None and hleft and max(hleft) < resistanceZone - zoneTol
        bullRoomLeftExtreme = lleft and min(lleft) > b.l + zoneTol
        bearRoomLeftExtreme = hleft and max(hleft) < b.h - zoneTol
        bullRoomLeft = bullRoomLeftZone if effectiveUseZoneFilter else bool(bullRoomLeftExtreme)
        bearRoomLeft = bearRoomLeftZone if effectiveUseZoneFilter else bool(bearRoomLeftExtreme)

        bullPattern = enoughBars and dominantRange and ((not effectiveRequireOutsideBar) or outsideBar) and bullCloseOk
        bearPattern = enoughBars and dominantRange and ((not effectiveRequireOutsideBar) or outsideBar) and bearCloseOk

        bullLocationOk = (
            ((not effectiveUseZoneFilter) or atSupport)
            and ((not effectiveRequireExtreme) or bullExtreme)
            and ((not effectiveUseRoomLeftFilter) or bullRoomLeft)
        )
        bearLocationOk = (
            ((not effectiveUseZoneFilter) or atResistance)
            and ((not effectiveRequireExtreme) or bearExtreme)
            and ((not effectiveUseRoomLeftFilter) or bearRoomLeft)
        )

        bullFilterOk = ((not effectiveUseTrendFilter) or trendLong) and ((not effectiveUseSessionFilter) or inSession)
        bearFilterOk = ((not effectiveUseTrendFilter) or trendShort) and ((not effectiveUseSessionFilter) or inSession)

        bullSignal = bullPattern and bullLocationOk and bullFilterOk
        bearSignal = bearPattern and bearLocationOk and bearFilterOk

        if pendingDir == 0 and tradeDir == 0:
            if bullSignal and not bearSignal:
                e = b.h + mintick * effectiveEntryOffsetTicks
                s = b.l - stopBuf
                r = max(e - s, mintick)
                zoneT = resistanceZone - targetZoneBuffer if (resistanceZone is not None and resistanceZone > e) else None
                rrT = e + r * targetRR
                t = zoneT if targetMode == "Nearest Zone" and zoneT is not None else rrT
                setupRR = (t - e) / r

                if setupRR >= minSetupRR:
                    pendingDir = 1
                    pendingEntry = e
                    pendingStop = s
                    pendingTarget = t
                    pendingBE = e + r * effectiveBreakevenAtR
                    pendingBar = i
                    setups += 1
            elif bearSignal and not bullSignal:
                e = b.l - mintick * effectiveEntryOffsetTicks
                s = b.h + stopBuf
                r = max(s - e, mintick)
                zoneT = supportZone + targetZoneBuffer if (supportZone is not None and supportZone < e) else None
                rrT = e - r * targetRR
                t = zoneT if targetMode == "Nearest Zone" and zoneT is not None else rrT
                setupRR = (e - t) / r

                if setupRR >= minSetupRR:
                    pendingDir = -1
                    pendingEntry = e
                    pendingStop = s
                    pendingTarget = t
                    pendingBE = e - r * effectiveBreakevenAtR
                    pendingBar = i
                    setups += 1

        if pendingDir != 0:
            barsSince = i - pendingBar
            canTrigger = barsSince == 1 if effectiveTriggerMode == "Next Candle (A+)" else barsSince >= 1
            expired = barsSince > 1 if effectiveTriggerMode == "Next Candle (A+)" else barsSince > effectiveEntryExpiryBars

            invalidBefore = canTrigger and (b.l <= pendingStop if pendingDir == 1 else b.h >= pendingStop)
            triggered = canTrigger and (b.h >= pendingEntry if pendingDir == 1 else b.l <= pendingEntry)

            if invalidBefore:
                canceled += 1
                pendingDir = 0
                pendingEntry = pendingStop = pendingTarget = pendingBE = pendingBar = None
            elif triggered:
                entries += 1
                tradeDir = pendingDir
                tradeEntry = pendingEntry
                tradeStop = pendingStop
                tradeTarget = pendingTarget
                tradeBE = pendingBE
                movedToBE = False
                current_entry_time = b.ts

                pendingDir = 0
                pendingEntry = pendingStop = pendingTarget = pendingBE = pendingBar = None
            elif expired:
                canceled += 1
                pendingDir = 0
                pendingEntry = pendingStop = pendingTarget = pendingBE = pendingBar = None

        if tradeDir != 0:
            activeStop = tradeEntry if movedToBE else tradeStop
            beReached = (not movedToBE) and ((b.h >= tradeBE) if tradeDir == 1 else (b.l <= tradeBE))
            if beReached:
                movedToBE = True
                activeStop = tradeEntry

            stopTouched = (b.l <= activeStop) if tradeDir == 1 else (b.h >= activeStop)
            targetTouched = (b.h >= tradeTarget) if tradeDir == 1 else (b.l <= tradeTarget)

            if stopTouched or targetTouched:
                if stopTouched:
                    exit_px = activeStop
                    r = 0.0 if movedToBE else -1.0
                    outcome = "be" if movedToBE else "loss"
                else:
                    exit_px = tradeTarget
                    rrisk = (tradeEntry - tradeStop) if tradeDir == 1 else (tradeStop - tradeEntry)
                    r = ((tradeTarget - tradeEntry) / rrisk) if tradeDir == 1 else ((tradeEntry - tradeTarget) / rrisk)
                    outcome = "win"
                trades.append(
                    Trade(
                        indicator="Big Shadow",
                        direction=tradeDir,
                        entry_time=current_entry_time or b.ts,
                        exit_time=b.ts,
                        entry=tradeEntry,
                        stop=tradeStop,
                        target=tradeTarget,
                        exit_price=exit_px,
                        outcome=outcome,
                        r=round(r, 3),
                    )
                )

                tradeDir = 0
                tradeEntry = tradeStop = tradeTarget = tradeBE = None
                movedToBE = False
                current_entry_time = None

    if tradeDir != 0:
        last = bars[-1]
        rrisk = (tradeEntry - tradeStop) if tradeDir == 1 else (tradeStop - tradeEntry)
        r = ((last.c - tradeEntry) / rrisk) if tradeDir == 1 else ((tradeEntry - last.c) / rrisk)
        outcome = "be" if abs(r) < 0.05 else ("win" if r > 0 else "loss")
        trades.append(
            Trade(
                indicator="Big Shadow",
                direction=tradeDir,
                entry_time=current_entry_time or last.ts,
                exit_time=last.ts,
                entry=tradeEntry,
                stop=tradeStop,
                target=tradeTarget,
                exit_price=last.c,
                outcome=outcome,
                r=round(r, 3),
            )
        )

    return summarize("Big Shadow", trades, setups, entries, canceled), trades


def run_wammie_moolah(
    bars: List[Bar],
    mintick: float,
    disable_trend_filter: bool = False,
    disable_session_filter: bool = False,
    overrides: Optional[Dict[str, object]] = None,
) -> Tuple[Dict[str, object], List[Trade]]:
    MAX_SCAN_BARS = 200

    cfg: Dict[str, object] = {
        "atrLen": 14,
        "pivotLen": 3,
        "useZoneFilter": False,
        "zoneSource": "Auto Pivot (Dynamic)",
        "freezeAutoZones": False,
        "zoneTolTicks": 8,
        "zoneTolAtr": 0.10,
        "minBarsBetweenTouches": 4,
        "idealBarsBetweenTouches": 20,
        "maxBarsBetweenTouches": 80,
        "minSecondTouchTicks": 0,
        "minSecondTouchAtr": 0.0,
        "maxSecondTouchTicks": 80,
        "maxSecondTouchAtr": 0.80,
        "maxInterimRetests": 1,
        "requireFirstTouchExtreme": True,
        "extremeLookback": 20,
        "requireBounceBetweenTouches": False,
        "minBounceAtr": 0.5,
        "requireCandleColor": False,
        "minBodyAtr": 0.08,
        "closeNearExtremeTicks": 10,
        "closeNearExtremeAtr": 0.05,
        "minRejectionWickBody": 0.10,
        "entryOffsetTicks": 2,
        "stopOffsetTicks": 2,
        "stopOffsetAtr": 0.05,
        "triggerMode": "Within N Candles (3-5)",
        "entryExpiryBars": 5,
        "targetMode": "R Multiple",
        "targetRR": 2.0,
        "targetZoneBufferTicks": 2,
        "breakevenAtR": 1.0,
        "useTrendFilter": True,
        "dailySmaLen": 200,
        "h4EmaLen": 50,
        "useSessionFilter": True,
        "useMacdFilter": False,
        "macdFast": 12,
        "macdSlow": 26,
        "macdSignalLen": 9,
        "useRsiFilter": False,
        "rsiLen": 14,
        "rsiLongMax": 35.0,
        "rsiShortMin": 65.0,
        "useRoomLeftFilter": False,
        "roomLeftBars": 7,
    }
    if overrides:
        cfg.update(overrides)

    atrLen = int(cfg["atrLen"])
    pivotLen = int(cfg["pivotLen"])
    useZoneFilter = bool(cfg["useZoneFilter"])
    zoneSource = str(cfg["zoneSource"])
    freezeAutoZones = bool(cfg["freezeAutoZones"])
    zoneTolTicks = int(cfg["zoneTolTicks"])
    zoneTolAtr = float(cfg["zoneTolAtr"])
    minBarsBetweenTouches = int(cfg["minBarsBetweenTouches"])
    idealBarsBetweenTouches = int(cfg["idealBarsBetweenTouches"])
    maxBarsBetweenTouches = int(cfg["maxBarsBetweenTouches"])
    minSecondTouchTicks = int(cfg["minSecondTouchTicks"])
    minSecondTouchAtr = float(cfg["minSecondTouchAtr"])
    maxSecondTouchTicks = int(cfg["maxSecondTouchTicks"])
    maxSecondTouchAtr = float(cfg["maxSecondTouchAtr"])
    maxInterimRetests = int(cfg["maxInterimRetests"])
    requireFirstTouchExtreme = bool(cfg["requireFirstTouchExtreme"])
    extremeLookback = int(cfg["extremeLookback"])
    requireBounceBetweenTouches = bool(cfg["requireBounceBetweenTouches"])
    minBounceAtr = float(cfg["minBounceAtr"])

    requireCandleColor = bool(cfg["requireCandleColor"])
    minBodyAtr = float(cfg["minBodyAtr"])
    closeNearExtremeTicks = int(cfg["closeNearExtremeTicks"])
    closeNearExtremeAtr = float(cfg["closeNearExtremeAtr"])
    minRejectionWickBody = float(cfg["minRejectionWickBody"])

    entryOffsetTicks = int(cfg["entryOffsetTicks"])
    stopOffsetTicks = int(cfg["stopOffsetTicks"])
    stopOffsetAtr = float(cfg["stopOffsetAtr"])
    triggerMode = str(cfg["triggerMode"])
    entryExpiryBars = int(cfg["entryExpiryBars"])
    targetMode = str(cfg["targetMode"])
    targetRR = float(cfg["targetRR"])
    targetZoneBufferTicks = int(cfg["targetZoneBufferTicks"])
    breakevenAtR = float(cfg["breakevenAtR"])

    useTrendFilter = bool(cfg["useTrendFilter"])
    dailySmaLen = int(cfg["dailySmaLen"])
    h4EmaLen = int(cfg["h4EmaLen"])
    useSessionFilter = bool(cfg["useSessionFilter"])
    if disable_trend_filter:
        useTrendFilter = False
    if disable_session_filter:
        useSessionFilter = False
    useMacdFilter = bool(cfg["useMacdFilter"])
    macdFast = int(cfg["macdFast"])
    macdSlow = int(cfg["macdSlow"])
    macdSignalLen = int(cfg["macdSignalLen"])
    useRsiFilter = bool(cfg["useRsiFilter"])
    rsiLen = int(cfg["rsiLen"])
    rsiLongMax = float(cfg["rsiLongMax"])
    rsiShortMin = float(cfg["rsiShortMin"])
    useRoomLeftFilter = bool(cfg["useRoomLeftFilter"])
    roomLeftBars = int(cfg["roomLeftBars"])

    highs = [b.h for b in bars]
    lows = [b.l for b in bars]
    opens = [b.o for b in bars]
    closes = [b.c for b in bars]

    atr_vals = atr(bars, atrLen)

    d_close = map_previous_period_close(bars, lambda t: (t.year, t.month, t.day))
    d_sma = map_previous_htf_series(
        bars,
        lambda t: (t.year, t.month, t.day),
        lambda bucket: bucket[-1].c,
        lambda seq: rolling_sma([v for v in seq], dailySmaLen),
    )
    h4_close = map_previous_period_close(bars, lambda t: (t.year, t.month, t.day, t.hour // 4))
    h4_ema = map_previous_htf_series(
        bars,
        lambda t: (t.year, t.month, t.day, t.hour // 4),
        lambda bucket: bucket[-1].c,
        lambda seq: ema([v for v in seq], h4EmaLen),
    )

    ema_fast = ema([float(c) for c in closes], macdFast)
    ema_slow = ema([float(c) for c in closes], macdSlow)
    macd_raw: List[Optional[float]] = [None] * len(closes)
    for i in range(len(closes)):
        if ema_fast[i] is not None and ema_slow[i] is not None:
            macd_raw[i] = ema_fast[i] - ema_slow[i]
    macd_signal = ema(macd_raw, macdSignalLen)
    macd_hist: List[Optional[float]] = [None] * len(closes)
    for i in range(len(closes)):
        if macd_raw[i] is not None and macd_signal[i] is not None:
            macd_hist[i] = macd_raw[i] - macd_signal[i]

    rsi_vals = rsi(closes, rsiLen)

    pLow = pivot_low(lows, pivotLen, pivotLen)
    pHigh = pivot_high(highs, pivotLen, pivotLen)

    autoSupportZone: Optional[float] = None
    autoResistanceZone: Optional[float] = None

    wFirstBar: Optional[int] = None
    wFirstLow: Optional[float] = None
    wFirstZone: Optional[float] = None

    mFirstBar: Optional[int] = None
    mFirstHigh: Optional[float] = None
    mFirstZone: Optional[float] = None

    pendingDir = 0
    pendingEntry = None
    pendingStop = None
    pendingTarget = None
    pendingBE = None
    pendingBar = None

    tradeDir = 0
    tradeEntry = None
    tradeStop = None
    tradeTarget = None
    tradeBE = None
    movedToBE = False
    current_entry_time: Optional[datetime] = None

    trades: List[Trade] = []
    setups = 0
    entries = 0
    canceled = 0

    def count_interim_touches(i: int, bars_between: int, zone: float, tol: float, support_side: bool) -> int:
        cnt = 0
        upper = min(MAX_SCAN_BARS, bars_between - 1)
        for k in range(1, upper + 1):
            idx = i - k
            if idx < 0:
                break
            touched = (lows[idx] <= zone + tol and lows[idx] >= zone - tol) if support_side else (highs[idx] >= zone - tol and highs[idx] <= zone + tol)
            cnt += 1 if touched else 0
        return cnt

    def max_high_between(i: int, bars_between: int) -> Optional[float]:
        vals = []
        upper = min(MAX_SCAN_BARS, bars_between - 1)
        for k in range(1, upper + 1):
            idx = i - k
            if idx < 0:
                break
            vals.append(highs[idx])
        return max(vals) if vals else None

    def min_low_between(i: int, bars_between: int) -> Optional[float]:
        vals = []
        upper = min(MAX_SCAN_BARS, bars_between - 1)
        for k in range(1, upper + 1):
            idx = i - k
            if idx < 0:
                break
            vals.append(lows[idx])
        return min(vals) if vals else None

    for i, b in enumerate(bars):
        a = atr_vals[i]
        if a is None:
            continue

        if pLow[i] is not None:
            autoSupportZone = autoSupportZone if (freezeAutoZones and autoSupportZone is not None) else pLow[i]
        if pHigh[i] is not None:
            autoResistanceZone = autoResistanceZone if (freezeAutoZones and autoResistanceZone is not None) else pHigh[i]

        supportZone = autoSupportZone if zoneSource == "Auto Pivot (Dynamic)" else None
        resistanceZone = autoResistanceZone if zoneSource == "Auto Pivot (Dynamic)" else None

        zoneTol = max(mintick * zoneTolTicks, a * zoneTolAtr)
        secondTouchDeltaMin = max(mintick * minSecondTouchTicks, a * minSecondTouchAtr)
        secondTouchDeltaMax = max(secondTouchDeltaMin, max(mintick * maxSecondTouchTicks, a * maxSecondTouchAtr))
        closeTol = max(mintick * closeNearExtremeTicks, a * closeNearExtremeAtr)
        stopBuf = max(mintick * stopOffsetTicks, a * stopOffsetAtr)
        targetZoneBuffer = mintick * targetZoneBufferTicks

        trendLong = (
            d_close[i] is not None
            and d_sma[i] is not None
            and h4_close[i] is not None
            and h4_ema[i] is not None
            and d_close[i] > d_sma[i]
            and h4_close[i] > h4_ema[i]
        )
        trendShort = (
            d_close[i] is not None
            and d_sma[i] is not None
            and h4_close[i] is not None
            and h4_ema[i] is not None
            and d_close[i] < d_sma[i]
            and h4_close[i] < h4_ema[i]
        )
        inSession = in_session_0700_1700(b.ts)

        ml = macd_raw[i]
        ms = macd_signal[i]
        mh = macd_hist[i]
        macdLongOk = ml is not None and ms is not None and mh is not None and ml > ms and mh > 0
        macdShortOk = ml is not None and ms is not None and mh is not None and ml < ms and mh < 0
        rv = rsi_vals[i]
        rsiLongOk = rv is not None and rv <= rsiLongMax
        rsiShortOk = rv is not None and rv >= rsiShortMin

        rng = max(b.h - b.l, mintick)
        body = abs(b.c - b.o)
        bodyOk = body >= a * minBodyAtr
        bullCloseStrong = (b.h - b.c) <= closeTol
        bearCloseStrong = (b.c - b.l) <= closeTol
        lowerWick = min(b.o, b.c) - b.l
        upperWick = b.h - max(b.o, b.c)
        bullWickOk = lowerWick >= body * minRejectionWickBody
        bearWickOk = upperWick >= body * minRejectionWickBody
        bullCatalyst = bodyOk and bullCloseStrong and bullWickOk and ((not requireCandleColor) or b.c > b.o)
        bearCatalyst = bodyOk and bearCloseStrong and bearWickOk and ((not requireCandleColor) or b.c < b.o)

        commonLongFilter = ((not useTrendFilter) or trendLong) and ((not useSessionFilter) or inSession) and ((not useMacdFilter) or macdLongOk) and ((not useRsiFilter) or rsiLongOk)
        commonShortFilter = ((not useTrendFilter) or trendShort) and ((not useSessionFilter) or inSession) and ((not useMacdFilter) or macdShortOk) and ((not useRsiFilter) or rsiShortOk)

        bullSignal = False
        bearSignal = False
        bullBarsBetween = None
        bearBarsBetween = None
        bullFirstRef = None
        bearFirstRef = None

        if pendingDir == 0 and tradeDir == 0:
            if wFirstBar is not None and i - wFirstBar > maxBarsBetweenTouches:
                wFirstBar = None
                wFirstLow = None
                wFirstZone = None
            if mFirstBar is not None and i - mFirstBar > maxBarsBetweenTouches:
                mFirstBar = None
                mFirstHigh = None
                mFirstZone = None

            if wFirstBar is None:
                zoneTouch = useZoneFilter and (supportZone is not None and b.l <= supportZone + zoneTol and b.l >= supportZone - zoneTol)
                pivotTouch = (not useZoneFilter) and (pLow[i] is not None)
                firstExtremeOkZone = (not requireFirstTouchExtreme) or (i > extremeLookback and b.l <= min(lows[i - extremeLookback + 1 : i + 1]))
                pivotIdx = i - pivotLen
                firstExtremeOkPivot = (not requireFirstTouchExtreme) or (
                    pivotIdx >= extremeLookback - 1
                    and lows[pivotIdx] <= min(lows[pivotIdx - extremeLookback + 1 : pivotIdx + 1])
                )
                if zoneTouch and firstExtremeOkZone:
                    wFirstBar = i
                    wFirstLow = b.l
                    wFirstZone = supportZone
                elif pivotTouch and firstExtremeOkPivot and pivotIdx >= 0:
                    wFirstBar = pivotIdx
                    wFirstLow = lows[pivotIdx]
                    wFirstZone = lows[pivotIdx]

            if mFirstBar is None:
                zoneTouch = useZoneFilter and (resistanceZone is not None and b.h >= resistanceZone - zoneTol and b.h <= resistanceZone + zoneTol)
                pivotTouch = (not useZoneFilter) and (pHigh[i] is not None)
                firstExtremeOkZone = (not requireFirstTouchExtreme) or (i > extremeLookback and b.h >= max(highs[i - extremeLookback + 1 : i + 1]))
                pivotIdx = i - pivotLen
                firstExtremeOkPivot = (not requireFirstTouchExtreme) or (
                    pivotIdx >= extremeLookback - 1
                    and highs[pivotIdx] >= max(highs[pivotIdx - extremeLookback + 1 : pivotIdx + 1])
                )
                if zoneTouch and firstExtremeOkZone:
                    mFirstBar = i
                    mFirstHigh = b.h
                    mFirstZone = resistanceZone
                elif pivotTouch and firstExtremeOkPivot and pivotIdx >= 0:
                    mFirstBar = pivotIdx
                    mFirstHigh = highs[pivotIdx]
                    mFirstZone = highs[pivotIdx]

            if wFirstBar is not None and wFirstLow is not None and wFirstZone is not None:
                secondTouchCandidate = False
                secondLow = b.l
                secondBar = i
                if useZoneFilter:
                    secondTouchCandidate = supportZone is not None and b.l <= wFirstZone + zoneTol and b.l >= wFirstZone - zoneTol
                    secondLow = b.l
                    secondBar = i
                elif pLow[i] is not None and i >= pivotLen:
                    secondTouchCandidate = True
                    secondLow = lows[i - pivotLen]
                    secondBar = i - pivotLen

                if secondTouchCandidate and secondBar > wFirstBar:
                    barsFromFirst = secondBar - wFirstBar
                    if secondLow < wFirstLow:
                        wFirstBar = secondBar
                        wFirstLow = secondLow
                        wFirstZone = supportZone if supportZone is not None else secondLow
                    elif minBarsBetweenTouches <= barsFromFirst <= maxBarsBetweenTouches:
                        secondHigher = secondLow >= wFirstLow + secondTouchDeltaMin
                        secondWithinMax = secondLow <= wFirstLow + secondTouchDeltaMax
                        interimTouches = count_interim_touches(i, barsFromFirst, wFirstZone, zoneTol, True) if useZoneFilter else 0
                        interimOk = (interimTouches <= maxInterimRetests) if useZoneFilter else True
                        mhb = max_high_between(i, barsFromFirst) if useZoneFilter else None
                        bounceOk = ((not requireBounceBetweenTouches) or (mhb is not None and mhb >= wFirstZone + a * minBounceAtr)) if useZoneFilter else True
                        lleft = lows[i - roomLeftBars : i] if i - roomLeftBars >= 0 else []
                        roomLeftPad = zoneTol if useZoneFilter else secondTouchDeltaMin
                        roomLeftOk = (not useRoomLeftFilter) or (i > roomLeftBars and lleft and min(lleft) > wFirstZone + roomLeftPad)
                        filterOk = commonLongFilter and roomLeftOk

                        if secondHigher and secondWithinMax and interimOk and bounceOk and bullCatalyst and filterOk:
                            bullSignal = True
                            bullBarsBetween = barsFromFirst
                            bullFirstRef = wFirstLow
                            wFirstBar = None
                            wFirstLow = None
                            wFirstZone = None
                        elif (not secondHigher) or (not secondWithinMax) or (not interimOk):
                            wFirstBar = secondBar
                            wFirstLow = secondLow
                            wFirstZone = supportZone if (useZoneFilter and supportZone is not None) else secondLow

            if mFirstBar is not None and mFirstHigh is not None and mFirstZone is not None:
                secondTouchCandidate = False
                secondHigh = b.h
                secondBar = i
                if useZoneFilter:
                    secondTouchCandidate = resistanceZone is not None and b.h >= mFirstZone - zoneTol and b.h <= mFirstZone + zoneTol
                    secondHigh = b.h
                    secondBar = i
                elif pHigh[i] is not None and i >= pivotLen:
                    secondTouchCandidate = True
                    secondHigh = highs[i - pivotLen]
                    secondBar = i - pivotLen

                if secondTouchCandidate and secondBar > mFirstBar:
                    barsFromFirst = secondBar - mFirstBar
                    if secondHigh > mFirstHigh:
                        mFirstBar = secondBar
                        mFirstHigh = secondHigh
                        mFirstZone = resistanceZone if resistanceZone is not None else secondHigh
                    elif minBarsBetweenTouches <= barsFromFirst <= maxBarsBetweenTouches:
                        secondLower = secondHigh <= mFirstHigh - secondTouchDeltaMin
                        secondWithinMax = secondHigh >= mFirstHigh - secondTouchDeltaMax
                        interimTouches = count_interim_touches(i, barsFromFirst, mFirstZone, zoneTol, False) if useZoneFilter else 0
                        interimOk = (interimTouches <= maxInterimRetests) if useZoneFilter else True
                        mlb = min_low_between(i, barsFromFirst) if useZoneFilter else None
                        bounceOk = ((not requireBounceBetweenTouches) or (mlb is not None and mlb <= mFirstZone - a * minBounceAtr)) if useZoneFilter else True
                        hleft = highs[i - roomLeftBars : i] if i - roomLeftBars >= 0 else []
                        roomLeftPad = zoneTol if useZoneFilter else secondTouchDeltaMin
                        roomLeftOk = (not useRoomLeftFilter) or (i > roomLeftBars and hleft and max(hleft) < mFirstZone - roomLeftPad)
                        filterOk = commonShortFilter and roomLeftOk

                        if secondLower and secondWithinMax and interimOk and bounceOk and bearCatalyst and filterOk:
                            bearSignal = True
                            bearBarsBetween = barsFromFirst
                            bearFirstRef = mFirstHigh
                            mFirstBar = None
                            mFirstHigh = None
                            mFirstZone = None
                        elif (not secondLower) or (not secondWithinMax) or (not interimOk):
                            mFirstBar = secondBar
                            mFirstHigh = secondHigh
                            mFirstZone = resistanceZone if (useZoneFilter and resistanceZone is not None) else secondHigh

        if bullSignal and bearSignal:
            bullSignal = False
            bearSignal = False

        if pendingDir == 0 and tradeDir == 0:
            if bullSignal and not bearSignal and bullFirstRef is not None:
                e = b.h + mintick * entryOffsetTicks
                s = bullFirstRef - stopBuf
                r = max(e - s, mintick)
                zoneT = resistanceZone - targetZoneBuffer if (resistanceZone is not None and resistanceZone > e) else None
                rrT = e + r * targetRR
                t = zoneT if targetMode == "Nearest Zone" and zoneT is not None else rrT

                pendingDir = 1
                pendingEntry = e
                pendingStop = s
                pendingTarget = t
                pendingBE = e + r * breakevenAtR
                pendingBar = i
                setups += 1
            elif bearSignal and not bullSignal and bearFirstRef is not None:
                e = b.l - mintick * entryOffsetTicks
                s = bearFirstRef + stopBuf
                r = max(s - e, mintick)
                zoneT = supportZone + targetZoneBuffer if (supportZone is not None and supportZone < e) else None
                rrT = e - r * targetRR
                t = zoneT if targetMode == "Nearest Zone" and zoneT is not None else rrT

                pendingDir = -1
                pendingEntry = e
                pendingStop = s
                pendingTarget = t
                pendingBE = e - r * breakevenAtR
                pendingBar = i
                setups += 1

                wFirstBar = None
                wFirstLow = None
                wFirstZone = None
                mFirstBar = None
                mFirstHigh = None
                mFirstZone = None

        if pendingDir != 0:
            barsSince = i - pendingBar
            canTrigger = barsSince == 1 if triggerMode == "Next Candle (A+)" else barsSince >= 1
            expired = barsSince > 1 if triggerMode == "Next Candle (A+)" else barsSince > entryExpiryBars

            invalidBefore = canTrigger and (b.l <= pendingStop if pendingDir == 1 else b.h >= pendingStop)
            triggered = canTrigger and (b.h >= pendingEntry if pendingDir == 1 else b.l <= pendingEntry)

            if invalidBefore:
                canceled += 1
                pendingDir = 0
                pendingEntry = pendingStop = pendingTarget = pendingBE = pendingBar = None
            elif triggered:
                entries += 1
                tradeDir = pendingDir
                tradeEntry = pendingEntry
                tradeStop = pendingStop
                tradeTarget = pendingTarget
                tradeBE = pendingBE
                movedToBE = False
                current_entry_time = b.ts

                pendingDir = 0
                pendingEntry = pendingStop = pendingTarget = pendingBE = pendingBar = None
            elif expired:
                canceled += 1
                pendingDir = 0
                pendingEntry = pendingStop = pendingTarget = pendingBE = pendingBar = None

        if tradeDir != 0:
            activeStop = tradeEntry if movedToBE else tradeStop
            beReached = (not movedToBE) and ((b.h >= tradeBE) if tradeDir == 1 else (b.l <= tradeBE))
            if beReached:
                movedToBE = True
                activeStop = tradeEntry

            stopTouched = (b.l <= activeStop) if tradeDir == 1 else (b.h >= activeStop)
            targetTouched = (b.h >= tradeTarget) if tradeDir == 1 else (b.l <= tradeTarget)

            if stopTouched or targetTouched:
                if stopTouched:
                    exit_px = activeStop
                    r = 0.0 if movedToBE else -1.0
                    outcome = "be" if movedToBE else "loss"
                else:
                    exit_px = tradeTarget
                    rrisk = (tradeEntry - tradeStop) if tradeDir == 1 else (tradeStop - tradeEntry)
                    r = ((tradeTarget - tradeEntry) / rrisk) if tradeDir == 1 else ((tradeEntry - tradeTarget) / rrisk)
                    outcome = "win"

                trades.append(
                    Trade(
                        indicator="Wammie/Moolah",
                        direction=tradeDir,
                        entry_time=current_entry_time or b.ts,
                        exit_time=b.ts,
                        entry=tradeEntry,
                        stop=tradeStop,
                        target=tradeTarget,
                        exit_price=exit_px,
                        outcome=outcome,
                        r=round(r, 3),
                    )
                )

                tradeDir = 0
                tradeEntry = tradeStop = tradeTarget = tradeBE = None
                movedToBE = False
                current_entry_time = None

    if tradeDir != 0:
        last = bars[-1]
        rrisk = (tradeEntry - tradeStop) if tradeDir == 1 else (tradeStop - tradeEntry)
        r = ((last.c - tradeEntry) / rrisk) if tradeDir == 1 else ((tradeEntry - last.c) / rrisk)
        outcome = "be" if abs(r) < 0.05 else ("win" if r > 0 else "loss")
        trades.append(
            Trade(
                indicator="Wammie/Moolah",
                direction=tradeDir,
                entry_time=current_entry_time or last.ts,
                exit_time=last.ts,
                entry=tradeEntry,
                stop=tradeStop,
                target=tradeTarget,
                exit_price=last.c,
                outcome=outcome,
                r=round(r, 3),
            )
        )

    return summarize("Wammie/Moolah", trades, setups, entries, canceled), trades


def write_trades(path: Path, trades: List[Trade]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["indicator", "direction", "entry_time", "exit_time", "entry", "stop", "target", "exit_price", "outcome", "r"])
        for t in trades:
            w.writerow(
                [
                    t.indicator,
                    "long" if t.direction == 1 else "short",
                    t.entry_time.isoformat(),
                    t.exit_time.isoformat(),
                    f"{t.entry:.6f}",
                    f"{t.stop:.6f}",
                    f"{t.target:.6f}",
                    f"{t.exit_price:.6f}",
                    t.outcome,
                    f"{t.r:.3f}",
                ]
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Backtest TradingView Pine indicators on CSV OHLCV data.")
    parser.add_argument("--csv", required=True, help="Path to OHLCV CSV (TradingView export).")
    parser.add_argument("--output-dir", default="Backtesting Data/results", help="Directory for output files.")
    parser.add_argument("--mintick", type=float, default=None, help="Override symbol tick size.")
    parser.add_argument("--disable-trend-filter", action="store_true", help="Disable D1/H4 trend filters for all indicators.")
    parser.add_argument("--disable-session-filter", action="store_true", help="Disable 07:00-17:00 session filter for all indicators.")
    parser.add_argument(
        "--bs-profile",
        default="Balanced",
        choices=["Balanced", "A+ Strict", "Custom"],
        help="Big Shadow profile mode. Matches Pine Profile Mode input.",
    )
    parser.add_argument(
        "--bs-pair-preset-mode",
        default="MT5 Per-Pair >=2R (2020-2026)",
        choices=["MT5 Per-Pair >=2R (2020-2026)", "Off (Manual Inputs)"],
        help="Big Shadow pair preset mode. Use MT5 per-pair mode to auto-apply tested settings per supported major pair.",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    bars = load_bars(csv_path)
    if len(bars) < 400:
        raise ValueError("Not enough bars for trend-filtered backtests. Need at least ~400 bars.")

    mintick = args.mintick if args.mintick is not None else infer_mintick(csv_path)

    lk_summary, lk_trades = run_last_kiss(
        bars,
        mintick,
        disable_trend_filter=args.disable_trend_filter,
        disable_session_filter=args.disable_session_filter,
    )
    bs_summary, bs_trades = run_big_shadow(
        bars,
        mintick,
        disable_trend_filter=args.disable_trend_filter,
        disable_session_filter=args.disable_session_filter,
        overrides={
            "profileMode": args.bs_profile,
            "pairPresetMode": args.bs_pair_preset_mode,
        },
        pair_name=csv_path.name,
    )
    wm_summary, wm_trades = run_wammie_moolah(
        bars,
        mintick,
        disable_trend_filter=args.disable_trend_filter,
        disable_session_filter=args.disable_session_filter,
    )

    all_trades = lk_trades + bs_trades + wm_trades
    summaries = [lk_summary, bs_summary, wm_summary]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_path = out_dir / "summary.json"
    trades_path = out_dir / "trades.csv"

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "source_csv": str(csv_path),
                "bars": len(bars),
                "start": bars[0].ts.isoformat(),
                "end": bars[-1].ts.isoformat(),
                "mintick": mintick,
                "disable_trend_filter": args.disable_trend_filter,
                "disable_session_filter": args.disable_session_filter,
                "big_shadow_profile": args.bs_profile,
                "big_shadow_pair_preset_mode": args.bs_pair_preset_mode,
                "results": summaries,
            },
            f,
            indent=2,
        )

    write_trades(trades_path, all_trades)

    print(f"Source: {csv_path}")
    print(f"Bars: {len(bars)} | Range: {bars[0].ts.isoformat()} -> {bars[-1].ts.isoformat()} | mintick={mintick}")
    print(f"Big Shadow profile: {args.bs_profile}")
    print(f"Big Shadow pair preset mode: {args.bs_pair_preset_mode}")
    for s in summaries:
        print(
            f"{s['indicator']}: setups={s['setups']} entries={s['entries']} closed={s['closed_trades']} "
            f"win%={s['win_rate_pct']} netR={s['net_r']}"
        )
    print(f"Wrote: {summary_path}")
    print(f"Wrote: {trades_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
