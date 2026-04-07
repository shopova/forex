#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from zoneinfo import ZoneInfo


SEVERITY_ORDER = {"GREEN": 0, "AMBER": 1, "RED": 2}
DEFAULT_USER_AGENT = "forex-news-risk-monitor/1.0"


@dataclass
class ScheduledEvent:
    key: str
    title: str
    currency: str
    impact: str
    severity: str
    event_time_utc: datetime
    pairs: List[str]
    blocked_until_utc: datetime
    reason: str
    alert_needed: bool


@dataclass
class HeadlineAlert:
    key: str
    feed_name: str
    title: str
    source: str
    link: str
    severity: str
    pairs: List[str]
    published_at_utc: datetime
    detected_at_utc: datetime
    blocked_until_utc: datetime
    reason: str
    alert_needed: bool


def expand_env(value: Any) -> Any:
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    return value


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(path: Path) -> Dict[str, Any]:
    config = expand_env(load_json(path))
    config.setdefault("timezone", "Europe/Sofia")
    config.setdefault("allowed_pairs", ["EURUSD", "USDJPY", "GBPUSD"])
    config.setdefault("currency_to_pairs", {})
    config.setdefault(
        "scheduled_windows",
        {
            "High": {"lookahead_minutes": 90, "cooldown_minutes": 60, "severity": "RED"},
            "Medium": {"lookahead_minutes": 30, "cooldown_minutes": 30, "severity": "AMBER"},
            "Low": {"lookahead_minutes": 0, "cooldown_minutes": 0, "severity": "GREEN"},
        },
    )
    config.setdefault("state_path", "state.json")
    config.setdefault("status_path", "latest_status.json")
    config.setdefault("markdown_path", "latest_status.md")
    config.setdefault("forex_factory_url", "https://nfs.faireconomy.media/ff_calendar_thisweek.json")
    config.setdefault("forex_factory_currencies", ["USD", "EUR", "GBP", "JPY"])
    config.setdefault("headline_feeds", [])
    return config


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def resolve_path(base_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def read_source(source: str, timeout_seconds: int = 20) -> bytes:
    if source.startswith("http://") or source.startswith("https://"):
        req = urllib.request.Request(
            source,
            headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "*/*"},
        )
        with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
            return response.read()
    return Path(source).read_bytes()


def load_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {
            "sent_scheduled_alerts": {},
            "sent_headline_alerts": {},
            "headline_blocks": {},
        }
    try:
        state = load_json(path)
    except json.JSONDecodeError:
        state = {}
    state.setdefault("sent_scheduled_alerts", {})
    state.setdefault("sent_headline_alerts", {})
    state.setdefault("headline_blocks", {})
    return state


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def prune_state(state: Dict[str, Any], now_utc: datetime) -> None:
    cutoff = now_utc - timedelta(days=7)

    for bucket_name in ("sent_scheduled_alerts", "sent_headline_alerts"):
        bucket = state.get(bucket_name, {})
        stale = []
        for key, value in bucket.items():
            try:
                ts = datetime.fromisoformat(value)
            except ValueError:
                stale.append(key)
                continue
            if ts < cutoff:
                stale.append(key)
        for key in stale:
            bucket.pop(key, None)

    blocks = state.get("headline_blocks", {})
    expired = []
    for key, value in blocks.items():
        try:
            until = datetime.fromisoformat(value["blocked_until_utc"])
        except (ValueError, KeyError):
            expired.append(key)
            continue
        if until <= now_utc:
            expired.append(key)
    for key in expired:
        blocks.pop(key, None)


def hash_key(*parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return digest[:20]


def normalize_severity(value: str) -> str:
    upper = value.upper()
    if upper not in SEVERITY_ORDER:
        raise ValueError(f"Unsupported severity: {value}")
    return upper


def local_fmt(dt_utc: datetime, tz_name: str) -> str:
    tz = ZoneInfo(tz_name)
    return dt_utc.astimezone(tz).strftime("%Y-%m-%d %H:%M %Z")


def event_pairs_for_currency(config: Dict[str, Any], currency: str) -> List[str]:
    pairs = config["currency_to_pairs"].get(currency, [])
    allowed = set(config["allowed_pairs"])
    return [pair for pair in pairs if pair in allowed]


def fetch_scheduled_events(config: Dict[str, Any], state: Dict[str, Any], now_utc: datetime) -> List[ScheduledEvent]:
    payload = json.loads(read_source(config["forex_factory_url"]).decode("utf-8"))
    relevant_currencies = set(config["forex_factory_currencies"])
    scheduled_events: List[ScheduledEvent] = []

    for item in payload:
        currency = item.get("country", "").upper()
        impact = item.get("impact", "")
        if currency not in relevant_currencies:
            continue
        window = config["scheduled_windows"].get(impact)
        if not window:
            continue
        pairs = event_pairs_for_currency(config, currency)
        if not pairs:
            continue

        lookahead = timedelta(minutes=int(window.get("lookahead_minutes", 0)))
        cooldown = timedelta(minutes=int(window.get("cooldown_minutes", 0)))
        if lookahead == timedelta(0) and cooldown == timedelta(0):
            continue

        event_time = datetime.fromisoformat(item["date"]).astimezone(timezone.utc)
        active_from = event_time - lookahead
        blocked_until = event_time + cooldown
        if now_utc < active_from or now_utc > blocked_until:
            continue

        severity = normalize_severity(window["severity"])
        title = item.get("title", "").strip()
        event_key = hash_key("scheduled", currency, impact, title, event_time.isoformat())
        alert_needed = event_key not in state["sent_scheduled_alerts"]
        if now_utc < event_time:
            mins = int((event_time - now_utc).total_seconds() // 60)
            reason = f"{impact} {currency} event in {mins}m: {title}"
        else:
            reason = f"{impact} {currency} event cooldown: {title}"

        scheduled_events.append(
            ScheduledEvent(
                key=event_key,
                title=title,
                currency=currency,
                impact=impact,
                severity=severity,
                event_time_utc=event_time,
                pairs=pairs,
                blocked_until_utc=blocked_until,
                reason=reason,
                alert_needed=alert_needed,
            )
        )

    scheduled_events.sort(key=lambda item: item.event_time_utc)
    return scheduled_events


def parse_rss_datetime(raw: str) -> datetime:
    dt = parsedate_to_datetime(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def host_matches(url: str, candidates: Iterable[str]) -> bool:
    host = urllib.parse.urlparse(url).netloc.lower()
    if not host:
        return False
    for candidate in candidates:
        normalized = candidate.lower()
        if host == normalized or host.endswith("." + normalized):
            return True
    return False


def text_matches_keywords(text: str, keywords: Iterable[str]) -> bool:
    haystack = text.lower()
    return any(keyword.lower() in haystack for keyword in keywords)


def parse_rss_feed(feed_config: Dict[str, Any], state: Dict[str, Any], now_utc: datetime) -> List[HeadlineAlert]:
    xml_payload = read_source(feed_config["url"]).decode("utf-8", errors="replace")
    root = ET.fromstring(xml_payload)
    alerts: List[HeadlineAlert] = []

    trusted_sources = feed_config.get("trusted_sources", [])
    keywords_any = feed_config.get("keywords_any", [])
    max_age_hours = int(feed_config.get("max_age_hours", 24))
    max_age = timedelta(hours=max_age_hours)
    severity = normalize_severity(feed_config.get("severity", "RED"))
    cooldown = timedelta(minutes=int(feed_config.get("cooldown_minutes", 60)))
    max_items = int(feed_config.get("max_items", 3))
    pairs = feed_config.get("pairs", [])
    feed_name = feed_config["name"]

    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or link or title).strip()
        raw_pub_date = (item.findtext("pubDate") or "").strip()
        if not raw_pub_date:
            continue
        pub_date = parse_rss_datetime(raw_pub_date)
        if now_utc - pub_date > max_age:
            continue

        description = html.unescape((item.findtext("description") or "").strip())
        source_elem = item.find("source")
        source_name = (source_elem.text or "").strip() if source_elem is not None and source_elem.text else ""
        source_url = source_elem.attrib.get("url", "") if source_elem is not None else ""

        combined_text = " ".join(part for part in (title, description, source_name) if part)
        if keywords_any and not text_matches_keywords(combined_text, keywords_any):
            continue
        if trusted_sources:
            matches = host_matches(link, trusted_sources) or host_matches(source_url, trusted_sources)
            if not matches:
                continue

        alert_key = hash_key("headline", feed_name, guid)
        alert_needed = alert_key not in state["sent_headline_alerts"]
        alerts.append(
            HeadlineAlert(
                key=alert_key,
                feed_name=feed_name,
                title=title,
                source=source_name or source_url or feed_name,
                link=link,
                severity=severity,
                pairs=pairs,
                published_at_utc=pub_date,
                detected_at_utc=now_utc,
                blocked_until_utc=now_utc + cooldown,
                reason=f"{feed_name} / {source_name or source_url or feed_name}: {title}",
                alert_needed=alert_needed,
            )
        )

    alerts.sort(key=lambda item: item.published_at_utc, reverse=True)
    if max_items > 0:
        alerts = alerts[:max_items]
    return alerts


def merge_pair_status(
    allowed_pairs: List[str],
    scheduled_events: List[ScheduledEvent],
    headline_blocks: List[HeadlineAlert],
) -> Dict[str, Dict[str, Any]]:
    pair_status = {
        pair: {
            "state": "GREEN",
            "blocked_until_utc": None,
            "reasons": [],
        }
        for pair in allowed_pairs
    }

    def apply(pair: str, severity: str, blocked_until_utc: datetime, reason: str) -> None:
        entry = pair_status[pair]
        if SEVERITY_ORDER[severity] > SEVERITY_ORDER[entry["state"]]:
            entry["state"] = severity
        if entry["blocked_until_utc"] is None or blocked_until_utc > entry["blocked_until_utc"]:
            entry["blocked_until_utc"] = blocked_until_utc
        entry["reasons"].append(reason)

    for event in scheduled_events:
        for pair in event.pairs:
            apply(pair, event.severity, event.blocked_until_utc, event.reason)

    for alert in headline_blocks:
        for pair in alert.pairs:
            apply(pair, alert.severity, alert.blocked_until_utc, alert.reason)

    return pair_status


def format_pair_status_markdown(pair_status: Dict[str, Dict[str, Any]], timezone_name: str) -> str:
    lines = ["# News Risk Status", ""]
    for pair, entry in pair_status.items():
        lines.append(f"## {pair}: {entry['state']}")
        blocked_until_utc = entry["blocked_until_utc"]
        if isinstance(blocked_until_utc, str):
            blocked_until_utc = datetime.fromisoformat(blocked_until_utc)
        if blocked_until_utc is not None:
            lines.append(f"- Blocked until: {local_fmt(blocked_until_utc, timezone_name)}")
        else:
            lines.append("- Blocked until: n/a")
        if entry["reasons"]:
            for reason in entry["reasons"]:
                lines.append(f"- {reason}")
        else:
            lines.append("- No active blocks")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_alert_message(
    item_type: str,
    severity: str,
    title: str,
    pairs: List[str],
    blocked_until_utc: datetime,
    timezone_name: str,
    source: Optional[str] = None,
    link: Optional[str] = None,
) -> str:
    lines = [f"{severity} {item_type}", title]
    lines.append(f"Pairs: {', '.join(pairs)}")
    lines.append(f"Blocked until: {local_fmt(blocked_until_utc, timezone_name)}")
    if source:
        lines.append(f"Source: {source}")
    if link:
        lines.append(link)
    return "\n".join(lines)


def format_headline_digest(alerts: List[HeadlineAlert], timezone_name: str) -> str:
    first = alerts[0]
    latest_block = max(item.blocked_until_utc for item in alerts)
    pairs = sorted({pair for item in alerts for pair in item.pairs})
    lines = [f"{first.severity} headline risk digest", first.feed_name]
    lines.append(f"Pairs: {', '.join(pairs)}")
    lines.append(f"Blocked until: {local_fmt(latest_block, timezone_name)}")
    for item in alerts:
        lines.append(f"- {item.source}: {item.title}")
    return "\n".join(lines)


def emit_alert_message(message: str) -> None:
    print(message)
    print()


def format_terminal_status_summary(status_payload: Dict[str, Any]) -> str:
    generated_at = datetime.fromisoformat(status_payload["generated_at_utc"])
    timezone_name = status_payload["timezone"]
    lines = [f"[{local_fmt(generated_at, timezone_name)}] Current pair states"]
    for pair, entry in status_payload["pairs"].items():
        blocked_until = entry["blocked_until_utc"]
        blocked_text = local_fmt(datetime.fromisoformat(blocked_until), timezone_name) if blocked_until else "n/a"
        lines.append(f"- {pair}: {entry['state']} until {blocked_text}")
        reasons = entry.get("reasons", [])
        if reasons:
            for reason in reasons[:2]:
                lines.append(f"  {reason}")
            extra = len(reasons) - 2
            if extra > 0:
                lines.append(f"  +{extra} more")
    return "\n".join(lines)


def serialise_pair_status(pair_status: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    for pair, entry in pair_status.items():
        payload[pair] = {
            "state": entry["state"],
            "blocked_until_utc": entry["blocked_until_utc"].isoformat() if entry["blocked_until_utc"] else None,
            "reasons": entry["reasons"],
        }
    return payload


def run_once(config: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    now_utc = utc_now()
    prune_state(state, now_utc)

    scheduled_events = fetch_scheduled_events(config, state, now_utc)
    new_headlines: List[HeadlineAlert] = []
    for feed in config["headline_feeds"]:
        new_headlines.extend(parse_rss_feed(feed, state, now_utc))

    headline_blocks: List[HeadlineAlert] = []
    for alert in new_headlines:
        if alert.alert_needed:
            state["headline_blocks"][alert.key] = {
                "feed_name": alert.feed_name,
                "title": alert.title,
                "source": alert.source,
                "link": alert.link,
                "severity": alert.severity,
                "pairs": alert.pairs,
                "blocked_until_utc": alert.blocked_until_utc.isoformat(),
                "reason": alert.reason,
            }
            state["sent_headline_alerts"][alert.key] = now_utc.isoformat()
        headline_blocks.append(alert)

    active_headline_blocks: List[HeadlineAlert] = []
    for key, block in state["headline_blocks"].items():
        blocked_until_utc = datetime.fromisoformat(block["blocked_until_utc"])
        if blocked_until_utc <= now_utc:
            continue
        reason = f"{block['feed_name']} / {block['source']}: {block['title']}"
        active_headline_blocks.append(
            HeadlineAlert(
                key=key,
                feed_name=block["feed_name"],
                title=block["title"],
                source=block["source"],
                link=block["link"],
                severity=block["severity"],
                pairs=block["pairs"],
                published_at_utc=now_utc,
                detected_at_utc=now_utc,
                blocked_until_utc=blocked_until_utc,
                reason=reason,
                alert_needed=False,
            )
        )

    pair_status = merge_pair_status(config["allowed_pairs"], scheduled_events, active_headline_blocks)

    timezone_name = config["timezone"]
    for event in scheduled_events:
        if event.alert_needed:
            message = format_alert_message(
                item_type="scheduled risk",
                severity=event.severity,
                title=f"{event.currency} {event.impact}: {event.title}",
                pairs=event.pairs,
                blocked_until_utc=event.blocked_until_utc,
                timezone_name=timezone_name,
            )
            emit_alert_message(message)
            state["sent_scheduled_alerts"][event.key] = now_utc.isoformat()

    digest_groups: Dict[str, List[HeadlineAlert]] = {}
    for alert in new_headlines:
        if alert.alert_needed:
            digest_groups.setdefault(alert.feed_name, []).append(alert)

    for feed_name in sorted(digest_groups):
        message = format_headline_digest(digest_groups[feed_name], timezone_name=timezone_name)
        emit_alert_message(message)

    status_payload = {
        "generated_at_utc": now_utc.isoformat(),
        "timezone": timezone_name,
        "pairs": serialise_pair_status(pair_status),
        "scheduled_events": [
            {
                "title": item.title,
                "currency": item.currency,
                "impact": item.impact,
                "severity": item.severity,
                "event_time_utc": item.event_time_utc.isoformat(),
                "blocked_until_utc": item.blocked_until_utc.isoformat(),
                "pairs": item.pairs,
                "reason": item.reason,
            }
            for item in scheduled_events
        ],
        "headline_blocks": [
            {
                "feed_name": item.feed_name,
                "title": item.title,
                "source": item.source,
                "link": item.link,
                "severity": item.severity,
                "blocked_until_utc": item.blocked_until_utc.isoformat(),
                "pairs": item.pairs,
                "reason": item.reason,
            }
            for item in active_headline_blocks
        ],
    }
    return state, status_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="FX news risk monitor with terminal alerts.")
    parser.add_argument("--config", required=True, help="Path to the JSON config file.")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit.")
    parser.add_argument("--poll-seconds", type=int, default=300, help="Loop delay when not using --once.")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    base_dir = config_path.parent
    state_path = resolve_path(base_dir, config["state_path"])
    status_path = resolve_path(base_dir, config["status_path"])
    markdown_path = resolve_path(base_dir, config["markdown_path"])
    state = load_state(state_path)

    while True:
        try:
            state, status_payload = run_once(config, state)
            write_json(state_path, state)
            write_json(status_path, status_payload)
            ensure_parent(markdown_path)
            markdown_path.write_text(
                format_pair_status_markdown(status_payload["pairs"], config["timezone"]),
                encoding="utf-8",
            )
            print(format_terminal_status_summary(status_payload))
            print()
        except KeyboardInterrupt:
            return 130
        except Exception as exc:
            print(f"news_risk_monitor error: {exc}", file=sys.stderr)
            if args.once:
                return 1
        if args.once:
            return 0
        time.sleep(max(args.poll_seconds, 5))


if __name__ == "__main__":
    raise SystemExit(main())
