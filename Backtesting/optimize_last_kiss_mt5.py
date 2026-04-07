#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
import random
import time
from pathlib import Path
from typing import Dict, List, Tuple

from run_indicator_backtests import infer_mintick, load_bars, run_last_kiss


PARAM_SPACE: Dict[str, List[object]] = {
    "minConsolBars": [16, 20, 24, 30],
    "maxConsolBars": [50, 60, 80, 100],
    "minTouches": [2, 3],
    "touchTolPct": [6.0, 8.0, 10.0],
    "rangeVolBufAtr": [0.05, 0.10, 0.15],
    "rangeVolBufTicks": [3, 5, 8],
    "recentTouchWindow": [8, 12, 16],
    "minRecentBoundaryTouches": [1, 2],
    "maxBoundaryStaleBars": [20, 30, 40],
    "maxConsolDriftPct": [20.0, 25.0, 35.0],
    "maxOutsideCloses": [0, 1, 2],
    "maxOutsideCloseRun": [1, 2, 3],
    "minBoxAtr": [0.8, 1.0, 1.2, 1.4],
    "maxBoxAtr": [4.0, 6.0],
    "breakoutBufferAtr": [0.05, 0.10, 0.15],
    "minBreakoutBodyAtr": [0.15, 0.25, 0.35],
    "useVolumeFilter": [True, False],
    "volMult": [1.0, 1.1, 1.2],
    "maxRetestBars": [8, 12, 15, 20],
    "retestTolPct": [10.0, 12.0, 15.0],
    "minCatalystBodyAtr": [0.12, 0.20, 0.30],
    "closeNearExtremePct": [20.0, 25.0, 30.0],
    "minWickBodyRatio": [0.1, 0.2, 0.3],
    "entryExpiryBars": [3, 5],
    "stopMode": ["Midpoint of Box", "Opposite Box Edge"],
    "targetRR": [2.0, 2.5, 3.0],
    "minSetupRR": [2.0, 2.5],
    "useTrendFilter": [True, False],
    "useSessionFilter": [True, False],
    "maxNoZoneTouchBars": [60, 120, 240],
}

BASELINE: Dict[str, object] = {
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


def sample_configs(samples: int, seed: int) -> List[Dict[str, object]]:
    rnd = random.Random(seed)
    configs: List[Dict[str, object]] = [dict(BASELINE)]
    seen = {json.dumps(BASELINE, sort_keys=True)}
    keys = list(PARAM_SPACE.keys())

    while len(configs) < samples:
        cfg = dict(BASELINE)
        for k in keys:
            cfg[k] = rnd.choice(PARAM_SPACE[k])

        # Safety: max consolidation bars should exceed/equal min consolidation bars.
        if int(cfg["maxConsolBars"]) < int(cfg["minConsolBars"]):
            continue

        # Safety: max box atr should exceed min box atr.
        if float(cfg["maxBoxAtr"]) <= float(cfg["minBoxAtr"]):
            continue

        sig = json.dumps(cfg, sort_keys=True)
        if sig in seen:
            continue
        seen.add(sig)
        configs.append(cfg)
    return configs


def evaluate_config(
    cfg: Dict[str, object],
    pair_data: Dict[str, Tuple[List[object], float]],
) -> Dict[str, object]:
    per_pair: Dict[str, Dict[str, object]] = {}
    net_sum = 0.0
    min_net = 10**9

    for pair, (bars, mintick) in pair_data.items():
        summary, _ = run_last_kiss(bars, mintick, overrides=cfg)
        pair_res = {
            "net_r": float(summary["net_r"]),
            "entries": int(summary["entries"]),
            "setups": int(summary["setups"]),
            "closed_trades": int(summary["closed_trades"]),
            "win_rate_pct": float(summary["win_rate_pct"]),
            "max_drawdown_r": float(summary["max_drawdown_r"]),
        }
        per_pair[pair] = pair_res
        net = pair_res["net_r"]
        net_sum += net
        min_net = min(min_net, net)

    return {
        "config": cfg,
        "per_pair": per_pair,
        "net_r_sum": round(net_sum, 2),
        "min_pair_net_r": round(min_net, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize Last Kiss on MT5 pair set.")
    parser.add_argument("--data-glob", default="Backtesting Data/*_H1_2020-2026-02-23.csv")
    parser.add_argument("--samples", type=int, default=220)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--min-net-r", type=float, default=2.0)
    parser.add_argument("--output", default="Backtesting Data/results_mt5_allpairs_2026-02-26_rerun/last_kiss_opt_mt5.json")
    args = parser.parse_args()

    files = [Path(p) for p in sorted(glob.glob(args.data_glob)) if Path(p).is_file()]
    if not files:
        raise ValueError(f"No data files matched: {args.data_glob}")

    pair_data: Dict[str, Tuple[List[object], float]] = {}
    for f in files:
        pair = f.name.split("_")[0]
        pair_data[pair] = (load_bars(f), infer_mintick(f))

    configs = sample_configs(args.samples, args.seed)

    t0 = time.time()
    results: List[Dict[str, object]] = []
    best_per_pair: Dict[str, Dict[str, object]] = {
        pair: {"net_r": float("-inf"), "result": None} for pair in pair_data.keys()
    }

    for idx, cfg in enumerate(configs, start=1):
        r = evaluate_config(cfg, pair_data)
        results.append(r)
        for pair, pr in r["per_pair"].items():
            if pr["net_r"] > best_per_pair[pair]["net_r"]:
                best_per_pair[pair] = {"net_r": pr["net_r"], "result": r}

        if idx % 5 == 0 or idx == len(configs):
            print(f"[{idx}/{len(configs)}] best-min-pair-netR={max(x['min_pair_net_r'] for x in results):.2f}")

    universal = [
        r
        for r in results
        if all(pr["net_r"] >= args.min_net_r for pr in r["per_pair"].values())
    ]
    universal.sort(key=lambda x: (x["min_pair_net_r"], x["net_r_sum"]), reverse=True)

    per_pair_at_least = {}
    for pair, rec in best_per_pair.items():
        best = rec["result"]
        if best is None:
            continue
        per_pair_at_least[pair] = {
            "best_net_r": rec["net_r"],
            "meets_min_target": rec["net_r"] >= args.min_net_r,
            "config": best["config"],
            "metrics": best["per_pair"][pair],
        }

    payload = {
        "data_files": [f.name for f in files],
        "samples": len(configs),
        "seed": args.seed,
        "min_net_r_target": args.min_net_r,
        "elapsed_sec": round(time.time() - t0, 2),
        "universal_count": len(universal),
        "best_universal": universal[:10],
        "best_per_pair": per_pair_at_least,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Completed in {payload['elapsed_sec']}s")
    print(f"Universal configs meeting >= {args.min_net_r}R on all pairs: {len(universal)}")
    for pair, rec in per_pair_at_least.items():
        print(f"{pair}: best_net_r={rec['best_net_r']} meets_target={rec['meets_min_target']}")
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
