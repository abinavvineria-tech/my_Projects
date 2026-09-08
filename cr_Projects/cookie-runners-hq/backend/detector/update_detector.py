"""Update detector — classifies announcements from crawled content."""
from __future__ import annotations

from typing import Any

from backend.detector.change_hasher import hash_content
from backend.models import ChangeStatus, OfficialStatus


class UpdateDetector:
    """Detect new/changed announcements from crawl results."""

    def detect_new(self, content: str, source: dict[str, Any]) -> dict[str, Any]:
        return {
            "game_id": source.get("game", "ALL"),
            "title": content[:120],
            "content_hash": hash_content(content),
            "source_url": source.get("url", ""),
            "source_name": source.get("name", ""),
            "category": "general",
            "official_status": OfficialStatus.UNKNOWN,
            "confidence": 0.7,
            "summary": content[:500],
            "raw_content": content[:10000],
            "change_status": ChangeStatus.NEW,
        }

    def detect_change(self, old_hash: str, new_content: str) -> dict[str, Any] | None:
        new_hash = hash_content(new_content)
        if new_hash == old_hash:
            return None
        return {
            "change_status": ChangeStatus.UPDATED,
            "content_hash": new_hash,
            "summary": f"Content changed (hash {old_hash[:8]} -> {new_hash[:8]})",
        }

    def categorize(self, content: str) -> str:
        low = content.lower()
        if any(w in low for w in ["maintenance", "down", "update", "patch"]): return "maintenance"
        if any(w in low for w in ["cookie", "character", "new cookie"]): return "cookie"
        if any(w in low for w in ["event", "festival", "season", "challenge"]): return "event"
        return "general"

    def determine_status(self, content: str) -> ChangeStatus:
        low = content.lower()
        if "upcoming" in low or "coming" in low: return ChangeStatus.UPCOMING
        if "ended" in low or "concluded" in low: return ChangeStatus.ENDED
        if "started" in low or "live" in low: return ChangeStatus.LIVE
        return ChangeStatus.NEW

    def process_scrape_result(self, result: Any, source: dict[str, Any]) -> list[dict[str, Any]]:
        if not result.success:
            return []
        announcements: list[dict[str, Any]] = []
        content = result.markdown or result.html or ""
        ann = self.detect_new(content, source)
        ann["category"] = self.categorize(content)
        ann["change_status"] = self.determine_status(content)
        announcements.append(ann)
        return announcements
