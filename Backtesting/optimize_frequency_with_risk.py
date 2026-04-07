#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from run_indicator_backtests import (
    Trade,
    infer_mintick,
    load_bars,
    run_big_shadow,
    run_wammie_moolah,
)


@dataclass
class Scenario:
    id: str
    indicator: str
    disable_trend_filter: bool
    disable_session_filter: bool
    overrides: Dict[str, object]


@dataclass
class SimResult:
    executed_trades: int
    skipped_by_pause: int
    skipped_by_frequency: int
    hard_stops: int
    capital_preservation_activations: int
    max_drawdown_pct: float
    total_return_pct: float
    ending_equity: float


def build_scenarios() -> List[Scenario]:
    return [
        Scenario("bs_balanced", "Big Shadow", False, False, {}),
        Scenario("bs_balanced_no_session", "Big Shadow", False, True, {}),
        Scenario("bs_strict", "Big Shadow", False, False, {"profileMode": "A+ Strict"}),
        Scenario("bs_no_trend", "Big Shadow", True, False, {"profileMode": "A+ Strict"}),
        Scenario("bs_no_trend_no_session", "Big Shadow", True, True, {"profileMode": "A+ Strict"}),
        Scenario(
            "bs_relaxed_a",
            "Big Shadow",
            True,
            True,
            {
                "profileMode": "Custom",
                "requireOutsideBar": False,
                "dominanceMode": "Previous 5 Candles",
                "requireExtreme": False,
            },
        ),
        Scenario(
            "bs_relaxed_b",
            "Big Shadow",
            True,
            True,
            {
                "profileMode": "Custom",
                "requireOutsideBar": False,
                "dominanceMode": "Previous 5 Candles",
                "requireExtreme": False,
                "useRoomLeftFilter": False,
            },
        ),
        Scenario(
            "bs_relaxed_c",
            "Big Shadow",
            True,
            True,
            {
                "profileMode": "Custom",
                "requireOutsideBar": False,
                "dominanceMode": "Previous 5 Candles",
                "requireExtreme": False,
                "useRoomLeftFilter": False,
                "useZoneFilter": False,
            },
        ),
        Scenario(
            "bs_relaxed_d",
            "Big Shadow",
            True,
            True,
            {
                "profileMode": "Custom",
                "requireOutsideBar": False,
                "dominanceMode": "Previous 5 Candles",
                "requireExtreme": False,
                "useRoomLeftFilter": False,
                "useZoneFilter": False,
                "minRangeVsPrev": 1.05,
                "minRangeAtr": 0.70,
                "closeExtremeTicks": 20,
                "closeExtremeAtr": 0.08,
                "triggerMode": "Within N Candles",
                "entryExpiryBars": 5,
            },
        ),
        Scenario("wm_strict", "Wammie/Moolah", False, False, {}),
        Scenario("wm_no_trend", "Wammie/Moolah", True, False, {}),
        Scenario("wm_no_trend_no_session", "Wammie/Moolah", True, True, {}),
        Scenario(
            "wm_relaxed_a",
            "Wammie/Moolah",
            True,
            True,
            {
                "requireFirstTouchExtreme": False,
                "requireBounceBetweenTouches": False,
                "useRoomLeftFilter": False,
                "maxInterimRetests": 2,
                "minBarsBetweenTouches": 4,
            },
        ),
        Scenario(
            "wm_relaxed_b",
            "Wammie/Moolah",
            True,
            True,
            {
                "requireFirstTouchExtreme": False,
                "requireBounceBetweenTouches": False,
                "useRoomLeftFilter": False,
                "maxInterimRetests": 2,
                "minBarsBetweenTouches": 4,
                "minBodyAtr": 0.12,
            },
        ),
        Scenario(
            "wm_relaxed_c",
            "Wammie/Moolah",
            True,
            True,
            {
                "requireFirstTouchExtreme": False,
                "requireBounceBetweenTouches": False,
                "useRoomLeftFilter": False,
                "maxInterimRetests": 3,
                "minBarsBetweenTouches": 4,
                "useZoneFilter": False,
            },
        ),
        Scenario(
            "wm_relaxed_d",
            "Wammie/Moolah",
            True,
            True,
            {
                "requireFirstTouchExtreme": False,
                "requireBounceBetweenTouches": False,
                "useRoomLeftFilter": False,
                "maxInterimRetests": 3,
                "minBarsBetweenTouches": 3,
                "useZoneFilter": False,
                "minBodyAtr": 0.10,
                "minSecondTouchTicks": 1,
                "minSecondTouchAtr": 0.0,
                "requireCandleColor": False,
            },
        ),
    ]


def simulate_risk_rules(trades: List[Trade]) -> SimResult:
    # From uploaded docs:
    # - Base risk 1%
    # - Capital preservation trigger at >=6% DD or 3 consecutive losses -> risk 0.5%
    # - Hard stop at >=10% DD or 4 consecutive losses -> 48h pause
    # - After 2 losses reduce frequency
    # - Capital preservation minimum 10 trades before restore
    equity = 100.0
    peak = 100.0
    max_dd = 0.0

    loss_streak = 0
    cp_mode = False
    cp_trades = 0

    cooldown_until: Optional[datetime] = None
    reduce_frequency_toggle = False

    executed = 0
    skipped_pause = 0
    skipped_freq = 0
    hard_stops = 0
    cp_activations = 0

    for t in sorted(trades, key=lambda x: x.entry_time):
        if cooldown_until is not None and t.entry_time < cooldown_until:
            skipped_pause += 1
            continue

        if loss_streak >= 2:
            reduce_frequency_toggle = not reduce_frequency_toggle
            if not reduce_frequency_toggle:
                skipped_freq += 1
                continue

        dd_now = (peak - equity) / peak * 100.0 if peak > 0 else 0.0
        if (loss_streak >= 3 or dd_now >= 6.0) and not cp_mode:
            cp_mode = True
            cp_trades = 0
            cp_activations += 1

        risk_pct = 0.5 if cp_mode else 1.0
        trade_ret_pct = risk_pct * t.r

        equity *= 1.0 + trade_ret_pct / 100.0
        peak = max(peak, equity)
        dd_now = (peak - equity) / peak * 100.0 if peak > 0 else 0.0
        max_dd = max(max_dd, dd_now)

        executed += 1

        if t.r < 0:
            loss_streak += 1
        else:
            loss_streak = 0
            reduce_frequency_toggle = False

        if cp_mode:
            cp_trades += 1
            if cp_trades >= 10 and dd_now < 6.0 and loss_streak < 3:
                cp_mode = False
                cp_trades = 0

        if dd_now >= 10.0 or loss_streak >= 4:
            hard_stops += 1
            cooldown_until = t.exit_time + timedelta(hours=48)
            loss_streak = 0
            reduce_frequency_toggle = False
            cp_mode = True
            cp_trades = 0

    return SimResult(
        executed_trades=executed,
        skipped_by_pause=skipped_pause,
        skipped_by_frequency=skipped_freq,
        hard_stops=hard_stops,
        capital_preservation_activations=cp_activations,
        max_drawdown_pct=round(max_dd, 2),
        total_return_pct=round(equity - 100.0, 2),
        ending_equity=round(equity, 2),
    )


def evaluate_scenario(files: List[Path], scenario: Scenario) -> Dict[str, object]:
    all_trades: List[Trade] = []
    raw_entries = 0
    raw_setups = 0
    raw_net_r = 0.0
    per_pair = []

    for fp in files:
        bars = load_bars(fp)
        mintick = infer_mintick(fp)

        if scenario.indicator == "Big Shadow":
            summary, trades = run_big_shadow(
                bars,
                mintick,
                disable_trend_filter=scenario.disable_trend_filter,
                disable_session_filter=scenario.disable_session_filter,
                overrides=scenario.overrides,
                pair_name=fp.name,
            )
        else:
            summary, trades = run_wammie_moolah(
                bars,
                mintick,
                disable_trend_filter=scenario.disable_trend_filter,
                disable_session_filter=scenario.disable_session_filter,
                overrides=scenario.overrides,
            )

        raw_entries += int(summary["entries"])
        raw_setups += int(summary["setups"])
        raw_net_r += float(summary["net_r"])
        all_trades.extend(trades)

        per_pair.append(
            {
                "pair_file": fp.name,
                "entries": summary["entries"],
                "setups": summary["setups"],
                "net_r": summary["net_r"],
            }
        )

    sim = simulate_risk_rules(all_trades)

    return {
        "scenario_id": scenario.id,
        "indicator": scenario.indicator,
        "disable_trend_filter": scenario.disable_trend_filter,
        "disable_session_filter": scenario.disable_session_filter,
        "overrides": scenario.overrides,
        "raw_entries": raw_entries,
        "raw_setups": raw_setups,
        "raw_net_r": round(raw_net_r, 2),
        "risk_adjusted": {
            "executed_trades": sim.executed_trades,
            "skipped_by_pause": sim.skipped_by_pause,
            "skipped_by_frequency": sim.skipped_by_frequency,
            "hard_stops": sim.hard_stops,
            "capital_preservation_activations": sim.capital_preservation_activations,
            "max_drawdown_pct": sim.max_drawdown_pct,
            "total_return_pct": sim.total_return_pct,
            "ending_equity": sim.ending_equity,
        },
        "per_pair": per_pair,
    }


def rank_results(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    # Optimization target: increase executable frequency while protecting drawdown.
    # Feasible set: max DD <= 10% and non-negative return.
    feasible = [
        r
        for r in rows
        if r["risk_adjusted"]["max_drawdown_pct"] <= 10.0 and r["risk_adjusted"]["total_return_pct"] >= 0.0
    ]

    feasible.sort(
        key=lambda r: (
            r["risk_adjusted"]["executed_trades"],
            -r["risk_adjusted"]["hard_stops"],
            r["risk_adjusted"]["total_return_pct"],
        ),
        reverse=True,
    )

    if feasible:
        return feasible

    # Fallback if no feasible set: prioritize lower drawdown then frequency.
    rows.sort(
        key=lambda r: (
            -r["risk_adjusted"]["max_drawdown_pct"],
            r["risk_adjusted"]["executed_trades"],
            r["risk_adjusted"]["total_return_pct"],
        ),
        reverse=True,
    )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize frequency with risk/drawdown controls from strategy docs.")
    parser.add_argument("--data-glob", default="Backtesting Data/*_H1_*.csv")
    parser.add_argument("--output-dir", default="Backtesting Data/results_mt5_risk_optimized")
    args = parser.parse_args()

    files = [Path(p) for p in sorted(glob.glob(args.data_glob)) if Path(p).is_file()]
    if not files:
        raise ValueError(f"No files matched: {args.data_glob}")

    scenarios = build_scenarios()

    all_rows = []
    for s in scenarios:
        all_rows.append(evaluate_scenario(files, s))

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for indicator in ["Big Shadow", "Wammie/Moolah"]:
        subset = [r for r in all_rows if r["indicator"] == indicator]
        for r in subset:
            rr = r["risk_adjusted"]
            r["feasible"] = rr["max_drawdown_pct"] <= 10.0 and rr["total_return_pct"] >= 0.0
        ranked = rank_results(subset)

        out = {
            "indicator": indicator,
            "data_files": [p.name for p in files],
            "ranking_logic": "feasible: max_drawdown<=10 and total_return>=0, ranked by executed_trades desc then fewer hard stops then return",
            "ranked_results": ranked,
            "all_results": subset,
        }

        path = out_dir / ("big_shadow_risk_opt.json" if indicator == "Big Shadow" else "wammie_moolah_risk_opt.json")
        with path.open("w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)

        print(f"\n=== {indicator} risk-aware top configs ===")
        for i, r in enumerate(ranked[:5], start=1):
            rr = r["risk_adjusted"]
            print(
                f"{i}. {r['scenario_id']} | executed={rr['executed_trades']} raw={r['raw_entries']} "
                f"maxDD={rr['max_drawdown_pct']}% return={rr['total_return_pct']}% hardStops={rr['hard_stops']}"
            )
        print(f"Wrote: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
