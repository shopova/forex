# Clean Slate FX Strategy v2 Session Model Deep Review

## What this strategy is really trying to do

Clean Slate FX Strategy v2 is a rules-first attempt to extract repeatable intraday opportunities from three structural sources of FX price behavior: (i) time-of-day liquidity/volatility effects, (ii) order clustering around widely observed “levels” (support/resistance, highs/lows, round numbers), and (iii) directional continuation vs exhaustion/reversal around higher-timeframe structure. citeturn5view0turn26search1turn9search4

That “where + when + risk” framing is directionally aligned with what market microstructure research says matters most at short horizons: order flow and liquidity conditions can dominate short-run moves, and those conditions vary sharply across the 24-hour day. citeturn14view0turn5view0

The strategy’s most defensible thesis is not “a magical candle pattern works,” but rather:

- **The same few hours, every day, have systematically different market conditions than the rest of the day**, creating a more stable learning environment and a potentially more stable distribution of outcomes (better spread/liquidity, more decisive moves, more frequent interaction with key reference points). citeturn19view1turn5view0  
- **Order clustering near obvious levels can generate both reversals and accelerations**—which matches your two contexts (continuation vs sweep/reversal) and your two triggers (reclaim vs structure break). citeturn26search1turn9search4  

That said: a coherent story is not the same as a proven edge. The academic evidence on technical-rule profitability in FX is mixed and often time-varying; several well-known “edges” weaken or disappear as markets adapt or once realistic costs are included. citeturn18search0turn10search16

## Market reality check: liquidity, sessions, and why this “session model” is plausible

The global OTC FX market is extremely liquid in aggregate, but activity is still highly concentrated in major centers and time windows. The entity["organization","Bank for International Settlements","basel-based intl bank"] 2025 Triennial Survey release reports global OTC FX turnover around **$9.6 trillion per day** (April 2025, net-net basis), and it emphasizes the continued concentration of activity in top jurisdictions—especially the **United Kingdom (~38%)** and the **United States (~19%)** on a net-gross basis. citeturn4view0

This matters because your “first 2–3 hours of entity["city","London","england, uk"]” (or first 2–3 hours of entity["city","New York City","new york, us"]) is essentially a bet that the hourly microstructure is materially different in those windows—and that the difference is stable enough to train on. Research supports that basic premise:

- The entity["organization","Reserve Bank of Australia","central bank of australia"] documented **broad, persistent intraday volatility patterns** in FX and found volatility tends to be higher in “offshore” hours, with especially elevated activity during the **London–New York overlap**, plus identifiable spikes around **market opens/closes**, **major data releases**, and the **London fix**. citeturn19view1  
- entity["organization","Swiss National Bank","central bank of switzerland"] research also finds a statistically and economically significant “time-of-day phenomenon” in FX returns, arguing it is persistent enough to contradict simple random-walk/market-efficiency expectations at intraday horizons and may remain profitable under simple rules even after transaction costs (within the assumptions of that study). citeturn5view0  

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["forex trading sessions overlap chart London New York Tokyo Sydney","London session opening forex trading floor","New York forex trading session overlap diagram"],"num_per_query":1}

### Pair focus: your watchlist is consistent with venue/liquidity evidence

Focusing on EURUSD, GBPUSD, USDJPY (and optionally USDCAD) is consistent with how electronic interdealer liquidity has historically organized itself:

- A entity["organization","Bank for International Settlements","bis paper series"] working paper on FX market evolution notes that **EBS** became the main venue for pairs like EURUSD and USDJPY, while **Reuters Matching** became the main venue for “commonwealth” pairs such as GBPUSD and USDCAD. citeturn24view1  
- A entity["organization","Norges Bank","central bank of norway"] working paper (using EBS-linked data and related estimates) reports materially lower average bid-ask spreads for EURUSD and USDJPY than GBPUSD in its sample and shows that EBS coverage is far higher for EURUSD and USDJPY than for GBPUSD. citeturn25view0  

This is not a guarantee of “clean charts,” but it does support your “professional watchlist” idea: fewer pairs where spreads and execution conditions are generally more favorable is a rational constraint for a part-time discretionary trader. citeturn25view0turn24view1

## Your “liquidity sweep + reclaim” logic maps to known order clustering effects

A key question is whether your two trade contexts and two triggers correspond to *real*, recurring mechanisms in FX—rather than story-telling after the fact.

### Why “sweeps” happen at all

A large body of microstructure work argues that **order flow and liquidity provision mechanics** are central to short-run price formation. In that framework, a “liquidity sweep” is a retail-trading term that often describes a real phenomenon: clustered conditional orders (especially stop-loss orders) can be triggered when price pushes through widely watched levels, leading to fast moves, overshoots, and sometimes reversals. citeturn26search1turn9search4

The most directly relevant evidence comes from entity["people","Carol L. Osler","fx microstructure economist"] and the entity["organization","Federal Reserve Bank of New York","us federal reserve district 2"] staff report literature:

- Osler’s work provides empirical evidence that stop-loss orders can contribute to **rapid, self-reinforcing “price cascades,”** particularly when prices reach levels where stop-loss orders are documented to cluster (often near round numbers). citeturn9search4turn9search2  
- A related New York Fed staff report argues that clustering of stop-loss and take-profit orders can explain two very “technical-analysis-like” behaviors: (1) **reversals at predictable support/resistance**, and (2) **acceleration after level breaks**—which is strikingly close to your “reclaim” and “break + follow-through” framing. citeturn26search1  

### What this implies for your Trigger A and Trigger B

**Trigger A (Level reclaim)** is essentially a conservative version of “probe beyond a level → rejection → re-acceptance.” That is coherent with a market where (a) stops cluster near obvious reference points and (b) intraday liquidity is uneven—so price can overshoot and then mean-revert once the burst of conditional market orders is absorbed. citeturn9search4turn26search1

**Trigger B (Micro structure break)** is essentially a “behavioral regime shift” proxy: instead of predicting the reversal, you wait for a local pivot break that suggests the flow has flipped. That is directionally aligned with microstructure intuition: order-flow pressure can push prices, and when that pressure changes, the local structure tends to change too. citeturn24view0turn5view0

However, there is an important tension: the more your “micro structure” concept is truly microstructure-driven (order flow / very short-horizon predictability), the more you should be skeptical that a **30-minute trigger** is always timely. Ito & Hashimoto’s EBS-based analysis finds predictability and price impact from deal imbalances at very short horizons (1–5 minutes) and that significance can disappear at longer horizons like 30 minutes in their setup. citeturn24view0

That does *not* mean “30m can’t work,” but it does mean your 30m trigger is likely capturing a **different phenomenon** (broader discretionary structure and session flow), not the short-lived micro-predictability found at ultra-short horizons. You should be explicit about that, because it affects how you define pivots, how wide your stops need to be, and how you manage “late” entries. citeturn24view0turn5view0

## Strengths of the model, especially for a part-time discretionary trader

The best part of this strategy is not any single trigger; it’s the **operating system**.

### It is designed for skill acquisition, not just signal-hunting

Constraining yourself to one session block, a small watchlist, and two triggers will increase the quantity and comparability of reps. That matters because the research record strongly suggests that if technical/behavioral edges exist, they can be **episodic and adaptive**—meaning you need clean records and consistent execution to tell whether your edge is real or whether the market regime changed. citeturn18search0turn5view0

The entity["people","Christopher J. Neely","frb st louis economist"] / entity["people","Paul A. Weller","finance professor"] / entity["people","Joshua M. Ulrich","coauthor fx AMH study"] line of work is particularly relevant: it finds technical trading rule returns were genuinely present in earlier decades in some forms, but **profits for common rules (e.g., moving average/filter rules) largely disappeared by the early 1990s**, and returns to other rule types declined as well—consistent with markets adapting and crowding out simple patterns. citeturn18search0

### The risk architecture is unusually sane for “rebuild mode”

A few specific design choices stand out as “professional risk hygiene” in a retail context:

- **0.25% risk per trade** with **0.50% daily max loss** and **1.50% weekly max loss** creates a strong brake against the most common account-killers (revenge trading, doubling down, or letting one day dominate the week).  
- **Max 2 trades/day** and **1 open position** reduces correlated decision error (you avoid stacking trades that are effectively the same bet).  
- A simple, testable default profit model (**2R full exit**) supports clean stats and reduces discretionary “death by a thousand management decisions.”

These are not “alpha,” but they help prevent negative expectancy from execution mistakes overwhelming any edge that might exist. (This matters because even academically documented technical-rule returns can be fragile once costs and real execution are incorporated.) citeturn10search16turn18search0

### Your session + major-pairs constraint is a practical cost-control lever

Major pairs generally have tighter spreads and deeper liquidity than less-traded crosses, and electronic venue dominance differs by pair (eg, EBS vs Reuters Matching). Your restricted watchlist aligns with that structure, which is a reasonable way to reduce “strategy drag” from costs and poor fills. citeturn25view0turn24view1

## The biggest weaknesses and likely failure modes

This strategy is coherent, but several parts are “soft,” and the soft parts are where discretionary systems usually break.

### The definitions are not yet operational enough to ensure repeatability

The strategy depends on non-trivial subjective judgments:

- “meaningful” Daily/4H levels  
- “corrective vs aggressive” pullbacks  
- “climactic, stretched” moves  
- “meaningful” 30m pivot breaks  
- “not just random chop”

Those are expertise-laden concepts. If you cannot turn them into **consistent, pre-defined tagging rules**, your backtest will be contaminated by hindsight selection, and your live execution will drift over time. This is especially dangerous because research suggests technical edges can be time-varying; without stable definitions, you won’t know whether performance shifts came from the market or from you moving the goalposts. citeturn18search0

### The “sweep and reversal” idea is real, but it can seduce you into catching knives

Osler’s evidence supports the reality of stop clusters and cascades, but it also implies the opposite of what many traders intuit: when stops cascade, the move can **extend further than seems rational** before mean reversion appears. citeturn9search4turn26search12

Your rules try to manage this by requiring reclaim/structure shift (good), but you still need a **hard filter** for “this is likely trend continuation after a break” vs “this is a sweep that will fail.” Osler’s work explicitly links both reversal-at-level and acceleration-after-crossing to the same underlying clustering mechanics. In other words: the same level can produce both outcomes; your job is not to predict, but to force empirical confirmation and accept that confirmation will sometimes come “late.” citeturn26search1

### News-and-event risk is not optional in a session strategy

The highest-probability time windows (London morning, New York morning, overlaps) coincide disproportionately with scheduled macro releases and benchmark fixing flows.

The Reserve Bank of Australia bulletin does not just claim “news matters”—it shows identifiable **volatility spikes around US data releases and the London fix**, and it notes these effects appear even when averaging across many days. citeturn19view1

Your current spec does not clearly say whether you will:
- stand down around high-impact releases,
- widen stops,
- accept slippage risk,
- or skip the day if a release lands in your 2–3 hour block.

Without a rule here, you will tend to “make it up” live, which is where performance and discipline usually degrade. citeturn19view1turn5view0

### The “2R fixed target” is clean, but the math can punish you if your true win rate is low

This is not a criticism of 2R; it is a reminder of what you are implicitly committing to.

With a fixed **+2R / -1R** payoff, break-even win rate (ignoring costs) is **33.3%**. If your real win rate after spreads/slippage is, say, 30%, the system loses money even if you “feel” like you’re getting good entries. Conversely, at 45% wins, expectancy is strong:  
EV = 0.45·2R − 0.55·1R = +0.35R per trade (before costs).

This is exactly why your journaling/backtesting plan (track net R, streaks, missed setups) is structurally correct—but it becomes critical that your definitions and trade logging are objective enough to measure honestly. citeturn18search0

### Academic caution flag: intraday “rules” often die once realistic costs are applied

In the intraday domain, one recurring theme in the literature is: patterns can be detectable, but monetizing them after costs is hard.

Neely & Weller’s work on intraday technical strategies reports that when realistic transaction costs and trading hours are considered, they find **no evidence of excess returns** for the rule-generation approaches they test (even while noting the rules can uncover stable patterns). citeturn10search16turn10search8

This does not refute your strategy (it’s a different rule family and era), but it strongly argues for a conservative stance: **assume you have no edge until your own, costed, rule-consistent sample proves otherwise.** citeturn10search16turn18search0

## How I would tighten this strategy to make it testable and “professionally executable”

Your “next build steps” (checklist, marking template, indicator spec, backtesting sheet) are exactly the right direction. citeturn4view0turn19view1  
Below are the changes that would most improve robustness without expanding complexity.

### Make “meaningful level” mechanically defensible

Right now, “meaningful” is a judgment call. You can keep discretion, but you need an objective backbone. Examples of ruleable level families (choose a small subset):

- Prior day high/low and close  
- Weekly high/low  
- Session high/low (Asia range highs/lows before London)  
- Clearly defined swing points on 4H (eg, last two confirmed swing highs/lows)  
- Round-number grid (e.g., 00/50 levels) **only if** they align with a 4H/Daily swing

The reason to include round-number logic is not superstition; it is consistent with evidence that stop-loss clustering can occur near round numbers and that behavior around those thresholds can be unusually fast. citeturn9search4turn26search1

### Add a strict “event risk” protocol

Given the documented volatility spikes around key releases and fixes, specify one of these policies (and then never improvise):

- **Stand-down rule:** no new entries from X minutes before to Y minutes after Tier-1 releases (and consider the London fix).  
- **Only-with-confirmation rule:** trade only after the release, only if your trigger prints, and require larger “clearance” (more room to 2R) to compensate for whipsaw risk.

This is justified by the documented clustering of volatility around data releases and around the fix. citeturn19view1turn5view0

### Reduce “trigger ambiguity” with one quantification per trigger

You don’t need to over-engineer; you need one clear standard that prevents “I kinda see it.”

Examples:

- **Reclaim candle quality rule:** reclaim close must finish in the top/bottom X% of its range *and* close at least N pips beyond the level (or beyond a fraction of 30m ATR).  
- **Chop filter:** forbid reclaim entries if the last K 30m closes straddle the level more than M times.  
- **Pivot definition:** “meaningful pivot” = last swing high/low that caused at least one full 30m candle close in the opposite direction (a structural criterion, not a visual one).

This is the single most important step for making your replay/backtest honest and repeatable. citeturn18search0

### Align stop buffers with what you’re actually trading

Using an ATR-based buffer makes conceptual sense as a volatility normalization tool, but your current range (0.3–0.7× ATR(14) on 30m) is wide enough to create inconsistent effective risk if you choose it discretionarily.

Given that you aim for professional routine, I would set:
- one default buffer (e.g., 0.5× 30m ATR),
- one override condition (e.g., “if spread/volatility is unusually elevated, skip trade rather than widening”).

This helps prevent the classic discretionary trap: changing the stop to “make the trade fit,” rather than filtering the trade out. citeturn10search16turn19view1

### Treat platform/tooling as execution infrastructure, not as “an indicator”

You mention optional entity["company","TradingView","charting platform"] indicator specs. If you build tooling, focus it on **process enforcement**, not signal generation:

- session window shading + “no trade outside window” alerts  
- pre-marked level display that locks after session starts  
- a rule-based “valid reclaim” marker (based only on the definitions you set)  
- automatic screenshot + journal prompt after trade close

This improves compliance and data quality—your two biggest performance multipliers if the edge is subtle. citeturn18search0

### Put retail-risk realities in the strategy’s preface

If you trade FX via leveraged retail products (often CFDs/rolling spot), regulators explicitly warn that **a high proportion of retail clients lose money**, and leverage limits (eg, 30:1 on major FX pairs in EU/UK-style frameworks) exist because of the loss profile. citeturn15search0turn15search1turn15search7

This does not invalidate the strategy—it reinforces why your risk controls are not “conservative,” they are *structurally necessary*.

## Bottom-line opinion

As written, Clean Slate FX Strategy v2 is a **strong trading operating system** (routine, constraints, risk caps, replay-friendly simplicity) wrapped around a **plausible microstructure story** (session effects + level/order clustering). citeturn4view0turn19view1turn26search1turn9search4

Its main vulnerability is that several key concepts (“meaningful,” “corrective,” “climactic,” “not chop”) are still discretionary enough that you could “win the argument but lose the account”—ie, take trades that seem compliant in the moment but cannot be evaluated consistently afterward. That is exactly the environment where apparent technical edges often vanish under costs, regime changes, and execution drift. citeturn10search16turn18search0

If you convert the soft parts into a small set of objective definitions and add an explicit event-risk protocol, this framework becomes a legitimately testable, professional-grade part-time model: not because it guarantees profit, but because it creates the conditions under which you can *truthfully discover* whether you have an edge—and keep it when markets adapt. citeturn18search0turn19view1