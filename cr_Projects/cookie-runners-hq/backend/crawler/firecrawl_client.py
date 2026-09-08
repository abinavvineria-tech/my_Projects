"""Firecrawl client with BeautifulSoup fallback.

Primary mode: Firecrawl API (https://api.firecrawl.dev) — handles JS rendering,
structured extraction, and crawling at scale.

Fallback mode: requests + BeautifulSoup when FIRECRAWL_API_KEY is missing,
returns a fallback marker so callers can flag uncertain results.
"""
from __future__ import annotations

import hashlib
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup

from backend.crawler.rate_limiter import get_rate_limiter

logger = logging.getLogger("cookie_runners_hq.crawler")

FIRECRAWL_BASE = "https://api.firecrawl.dev/v1"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


@dataclass
class CrawlResult:
    """Result of a crawl/scrape operation."""

    url: str
    success: bool
    method: str  # "firecrawl" or "fallback"
    markdown: str = ""
    html: str = ""
    title: str = ""
    content_hash: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    duration: float = 0.0


class FirecrawlClient:
    """Client for the Firecrawl API with BeautifulSoup fallback."""

    def __init__(self, api_key: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.api_key = api_key or os.environ.get("FIRECRAWL_API_KEY", "")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "CookieRunnersHQ/1.0 (+https://github.com/cookie-runners-hq)",
            "Accept": "application/json",
        })
        if self.api_key and self.api_key != "your_firecrawl_api_key_here":
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
            self._available = True
        else:
            self._available = False
        self._rate_limiter = get_rate_limiter()

    @property
    def is_available(self) -> bool:
        """True if Firecrawl is configured and ready."""
        return self._available

    def _request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """HTTP request with exponential backoff retries."""
        last_exc: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
                if resp.status_code == 429 or resp.status_code >= 500:
                    wait = RETRY_BACKOFF ** attempt
                    logger.warning("HTTP %d on %s, retrying in %.1fs", resp.status_code, url, wait)
                    time.sleep(wait)
                    continue
                return resp
            except requests.RequestException as exc:
                last_exc = exc
                wait = RETRY_BACKOFF ** attempt
                logger.warning("Request error on %s (%s), retrying in %.1fs", url, exc, wait)
                time.sleep(wait)
        if last_exc:
            raise last_exc
        raise RuntimeError(f"Max retries exceeded for {url}")

    def scrape_url(self, url: str, formats: Optional[list[str]] = None) -> CrawlResult:
        """Scrape a single URL and return structured content.

        Parameters
        ----------
        url : str
            The URL to scrape.
        formats : list[str] | None
            Desired output formats (default: ["markdown", "html"]).
        """
        start = time.time()
        formats = formats or ["markdown", "html"]
        if self._available:
            result = self._scrape_firecrawl(url, formats)
        else:
            result = self._scrape_fallback(url)
        result.duration = time.time() - start
        result.content_hash = hashlib.sha256((result.markdown or result.html).encode("utf-8")).hexdigest()
        return result

    def crawl_url(self, url: str, limit: int = 5) -> list[CrawlResult]:
        """Crawl a URL and follow links (returns multiple results)."""
        if not self._available:
            logger.info("Firecrawl unavailable — falling back to single-page scrape")
            return [self.scrape_url(url)]
        start = time.time()
        try:
            resp = self._request_with_retry(
                "POST", f"{FIRECRAWL_BASE}/crawl",
                json={"url": url, "limit": limit, "scrapeOptions": {"formats": ["markdown", "html"]}},
            )
            if resp.status_code != 200:
                return [CrawlResult(url=url, success=False, method="firecrawl", error=resp.text)]
            data = resp.json()
            results: list[CrawlResult] = []
            for item in data.get("data", []):
                md = item.get("markdown", "")
                html = item.get("html", "")
                results.append(CrawlResult(
                    url=item.get("url", url),
                    success=True,
                    method="firecrawl",
                    markdown=md,
                    html=html,
                    title=(item.get("metadata", {}) or {}).get("title", ""),
                    content_hash=hashlib.sha256((md or html).encode("utf-8")).hexdigest(),
                    metadata=item.get("metadata", {}) or {},
                ))
            return results
        except Exception as exc:  # noqa: BLE001
            logger.error("Firecrawl crawl failed for %s: %s", url, exc)
            return [CrawlResult(url=url, success=False, method="firecrawl", error=str(exc))]

    def extract_structured(self, url: str, schema: dict[str, Any]) -> dict[str, Any]:
        """Extract structured data using a JSON schema (Firecrawl only)."""
        if not self._available:
            logger.warning("Structured extraction requires Firecrawl — returning empty result")
            return {"_warning": "firecrawl_unavailable", "url": url}
        try:
            resp = self._request_with_retry(
                "POST", f"{FIRECRAWL_BASE}/extract",
                json={"urls": [url], "schema": schema},
            )
            if resp.status_code != 200:
                return {"_error": resp.text, "url": url}
            return resp.json()
        except Exception as exc:  # noqa: BLE001
            logger.error("Firecrawl extract failed for %s: %s", url, exc)
            return {"_error": str(exc), "url": url}

    # ─── Private helpers ──────────────────────────────────────────────────────

    def _scrape_firecrawl(self, url: str, formats: list[str]) -> CrawlResult:
        """Scrape using the Firecrawl API."""
        try:
            resp = self._request_with_retry(
                "POST", f"{FIRECRAWL_BASE}/scrape",
                json={"url": url, "formats": formats},
            )
            if resp.status_code != 200:
                return CrawlResult(url=url, success=False, method="firecrawl", error=resp.text)
            data = resp.json().get("data", {})
            return CrawlResult(
                url=url,
                success=True,
                method="firecrawl",
                markdown=data.get("markdown", ""),
                html=data.get("html", ""),
                title=(data.get("metadata", {}) or {}).get("title", ""),
                metadata=data.get("metadata", {}) or {},
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("Firecrawl scrape failed for %s: %s", url, exc)
            return CrawlResult(url=url, success=False, method="firecrawl", error=str(exc))

    def _scrape_fallback(self, url: str) -> CrawlResult:
        """Fallback: requests + BeautifulSoup when Firecrawl is unavailable."""
        try:
            self._rate_limiter.acquire_blocking(source_id=hash(url) % 10000, timeout=15)
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            html = resp.text
            soup = BeautifulSoup(html, "lxml")
            # Remove noisy elements
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            title = soup.title.string if soup.title else ""
            text = soup.get_text(separator="\n", strip=True)
            markdown = text[:50000]  # cap to avoid huge payloads
            return CrawlResult(
                url=url, success=True, method="fallback",
                markdown=markdown, html=html[:50000], title= title or "",
                metadata={"_fallback": True, "_note": "extracted without firecrawl"},
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("Fallback scrape failed for %s: %s", url, exc)
            return CrawlResult(url=url, success=False, method="fallback", error=str(exc))
