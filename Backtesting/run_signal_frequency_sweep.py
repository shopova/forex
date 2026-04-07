#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from run_indicator_backtests import (
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


def build_scenarios() -> List[Scenario]:
    big_shadow = [
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
    ]

    wammie = [
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
                "maxInterimRetests": 3,
                "minBarsBetweenTouches": 4,
                "useZoneFilter": False,
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
                "minBarsBetweenTouches": 3,
                "useZoneFilter": False,
                "minBodyAtr": 0.10,
                "minSecondTouchTicks": 1,
                "minSecondTouchAtr": 0.0,
                "requireCandleColor": False,
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
                "maxInterimRetests": 4,
                "minBarsBetweenTouches": 3,
                "useZoneFilter": False,
                "minBodyAtr": 0.08,
                "minSecondTouchTicks": 0,
                "minSecondTouchAtr": 0.0,
                "requireCandleColor": False,
                "minRejectionWickBody": 0.10,
                "closeNearExtremeTicks": 20,
                "closeNearExtremeAtr": 0.10,
            },
        ),
    ]

    return big_shadow + wammie


def evaluate_pair_scenario(csv_path: Path, scenario: Scenario) -> Dict[str, object]:
    bars = load_bars(csv_path)
    mintick = infer_mintick(csv_path)

    if scenario.indicator == "Big Shadow":
        summary, _trades = run_big_shadow(
            bars,
            mintick,
            disable_trend_filter=scenario.disable_trend_filter,
            disable_session_filter=scenario.disable_session_filter,
            overrides=scenario.overrides,
            pair_name=csv_path.name,
        )
    else:
        summary, _trades = run_wammie_moolah(
            bars,
            mintick,
            disable_trend_filter=scenario.disable_trend_filter,
            disable_session_filter=scenario.disable_session_filter,
            overrides=scenario.overrides,
        )

    return {
        "pair_file": csv_path.name,
        "bars": len(bars),
        "entries": summary["entries"],
        "setups": summary["setups"],
        "closed_trades": summary["closed_trades"],
        "win_rate_pct": summary["win_rate_pct"],
        "net_r": summary["net_r"],
        "avg_r": summary["avg_r"],
        "max_drawdown_r": summary["max_drawdown_r"],
    }


def aggregate(scenario: Scenario, per_pair: List[Dict[str, object]]) -> Dict[str, object]:
    total_entries = sum(int(x["entries"]) for x in per_pair)
    total_setups = sum(int(x["setups"]) for x in per_pair)
    total_closed = sum(int(x["closed_trades"]) for x in per_pair)
    total_net_r = round(sum(float(x["net_r"]) for x in per_pair), 2)
    return {
        "scenario_id": scenario.id,
        "indicator": scenario.indicator,
        "disable_trend_filter": scenario.disable_trend_filter,
        "disable_session_filter": scenario.disable_session_filter,
        "overrides": scenario.overrides,
        "total_entries": total_entries,
        "total_setups": total_setups,
        "total_closed_trades": total_closed,
        "total_net_r": total_net_r,
        "per_pair": per_pair,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep Big Shadow and Wammie/Moolah configs for signal frequency.")
    parser.add_argument(
        "--data-glob",
        default="Backtesting Data/*_H1_*.csv",
        help="Glob for input CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        default="Backtesting Data/results_mt5_sweep",
        help="Output folder for sweep artifacts.",
    )
    args = parser.parse_args()

    files = [Path(p) for p in sorted(glob.glob(args.data_glob)) if Path(p).is_file()]
    if not files:
        raise ValueError(f"No files matched: {args.data_glob}")

    scenarios = build_scenarios()
    all_results: List[Dict[str, object]] = []

    for s in scenarios:
        per_pair = [evaluate_pair_scenario(fp, s) for fp in files]
        all_results.append(aggregate(s, per_pair))

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for indicator in ["Big Shadow", "Wammie/Moolah"]:
        subset = [x for x in all_results if x["indicator"] == indicator]
        subset.sort(key=lambda x: (x["total_entries"], x["total_net_r"]), reverse=True)

        path = out_dir / ("big_shadow_sweep.json" if indicator == "Big Shadow" else "wammie_moolah_sweep.json")
        with path.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "indicator": indicator,
                    "data_files": [p.name for p in files],
                    "ranked_results": subset,
                },
                f,
                indent=2,
            )

        print(f"\n=== {indicator} top configs ===")
        for i, row in enumerate(subset[:5], start=1):
            print(
                f"{i}. {row['scenario_id']} | entries={row['total_entries']} setups={row['total_setups']} "
                f"closed={row['total_closed_trades']} netR={row['total_net_r']}"
            )
        print(f"Wrote: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
