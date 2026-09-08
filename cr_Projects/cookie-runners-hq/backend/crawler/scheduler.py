"""Crawl scheduler — periodically crawls all enabled sources.

Uses APScheduler to run a single background job.  The scheduler is
intentionally lightweight so it can run inside the Flask process for
single-user deployments; for production scale, run a separate worker.
"""
from __future__ import annotations

import logging
import re
import threading
import time
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from backend import database as db
from backend.crawler.firecrawl_client import CrawlResult, FirecrawlClient
from backend.detector.update_detector import UpdateDetector

logger = logging.getLogger("cookie_runners_hq.scheduler")

_scheduler: BackgroundScheduler | None = None
_scheduler_lock = threading.Lock()


def _parse_schedule(schedule: str) -> int:
    """Parse a schedule string like '30m', '1h', '90s' to seconds.

    Falls back to 30 minutes for unparseable values.
    """
    m = re.match(r"^(\d+)\s*([smhd])$", schedule.strip().lower())
    if not m:
        return 30 * 60
    value, unit = int(m.group(1)), m.group(2)
    return value * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]


def run_crawl_for_source(source: dict[str, Any]) -> dict[str, Any]:
    """Crawl a single source, detect updates, and record history.

    Returns a result dict suitable for returning from the API.
    """
    source_id = source.get("id")
    if not source_id:
        return {"success": False, "error": "source missing id"}

    start = time.time()
    client = FirecrawlClient()
    result: CrawlResult = client.scrape_url(source["url"])
    duration = time.time() - start

    detector = UpdateDetector()
    new_announcements: list[int] = []
    try:
        if result.success:
            detected = detector.process_scrape_result(result, source)
            for ann in detected:
                if not db.get_announcement_by_hash(ann["content_hash"]):
                    new_id = db.insert_announcement(
                        ann["game_id"], ann["title"], ann["content_hash"],
                        ann["source_url"], ann["source_name"], ann.get("published_date"),
                        ann.get("category", "general"), ann.get("official_status", "unknown"),
                        float(ann.get("confidence", 0.5)),
                        ann.get("summary", ""), ann.get("raw_content", "")[:5000],
                        ann.get("change_status", "NEW"),
                    )
                    new_announcements.append(new_id)
            db.touch_source_last_checked(source_id)
            db.insert_crawl_history(
                source_id, "success",
                f"new_announcements={len(new_announcements)}",
                "", duration,
            )
            return {
                "success": True,
                "method": result.method,
                "duration": round(duration, 2),
                "new_announcements": len(new_announcements),
                "announcement_ids": new_announcements,
            }
        else:
            db.insert_crawl_history(
                source_id, "failed", "", result.error or "scrape failed", duration,
            )
            return {"success": False, "error": result.error, "duration": round(duration, 2)}
    except Exception as exc:  # noqa: BLE001
        logger.exception("Crawl failed for source %s: %s", source_id, exc)
        db.insert_crawl_history(
            source_id, "error", "", str(exc), time.time() - start,
        )
        return {"success": False, "error": str(exc)}


def run_full_crawl() -> dict[str, int]:
    """Crawl all enabled sources. Returns aggregate stats."""
    sources = db.get_all_sources(enabled_only=True)
    total_new = 0
    failures = 0
    for source in sources:
        result = run_crawl_for_source(source)
        if result.get("success"):
            total_new += int(result.get("new_announcements", 0))
        else:
            failures += 1
    return {"sources_crawled": len(sources), "new_announcements": total_new, "failures": failures}


def start_scheduler(schedule: str = "30m") -> BackgroundScheduler:
    """Start the background scheduler if not already running."""
    global _scheduler
    with _scheduler_lock:
        if _scheduler is not None and _scheduler.running:
            return _scheduler
        interval = _parse_schedule(schedule)
        _scheduler = BackgroundScheduler(daemon=True)
        _scheduler.add_job(
            run_full_crawl,
            trigger=IntervalTrigger(seconds=interval),
            id="cookie_runners_full_crawl",
            name="Cookie Runners HQ — Full Crawl",
            replace_existing=True,
        )
        _scheduler.start()
        logger.info("Crawl scheduler started — running every %ds", interval)
        return _scheduler


def stop_scheduler() -> None:
    """Stop the background scheduler."""
    global _scheduler
    with _scheduler_lock:
        if _scheduler is not None and _scheduler.running:
            _scheduler.shutdown(wait=False)
            logger.info("Crawl scheduler stopped")
        _scheduler = None


def is_scheduler_running() -> bool:
    """True if the background scheduler is running."""
    return _scheduler is not None and _scheduler.running
