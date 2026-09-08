"""
Environment configuration loader for Cookie Runners HQ.
Loads settings from environment variables and .env file.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

DEFAULT_DB_PATH = DATA_DIR / "cookie_runners.db"

# ---------------------------------------------------------------------------
# .env loading
# ---------------------------------------------------------------------------
_env_path = BASE_DIR / ".env"
if _DOTENV_AVAILABLE and _env_path.exists():
    load_dotenv(dotenv_path=_env_path, override=False)
elif _env_path.exists():
    # Minimal dotenv parser fallback (no third-party dep)
    with open(_env_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip("'\""))

# ---------------------------------------------------------------------------
# Core settings
# ---------------------------------------------------------------------------

class Settings:
    """Application-wide settings object. Access members as attributes."""

    # Flask
    FLASK_HOST: str = os.getenv("FLASK_HOST", "127.0.0.1")
    FLASK_PORT: int = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "yes")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cookie-runners-dev-secret")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")
    DATABASE_PATH: Path = DEFAULT_DB_PATH

    # Firecrawl crawler
    FIRECRAWL_API_KEY: str = os.getenv("FIRECRAWL_API_KEY", "")
    FIRECRAWL_BASE_URL: str = os.getenv(
        "FIRECRAWL_BASE_URL", "https://api.firecrawl.dev"
    )
    FIRECRAWL_TIMEOUT: int = int(os.getenv("FIRECRAWL_TIMEOUT", "60"))

    # Hermes orchestrator
    HERMES_API_KEY: str = os.getenv("HERMES_API_KEY", "")
    HERMES_BASE_URL: str = os.getenv("HERMES_BASE_URL", "http://localhost:8000")
    HERMES_MODEL: str = os.getenv("HERMES_MODEL", "auto")

    # Scheduler / crawl settings
    CRAWL_SCHEDULE: str = os.getenv("CRAWL_SCHEDULE", "30m")  # e.g. "5m", "1h"
    CRAWL_BATCH_SIZE: int = int(os.getenv("CRAWL_BATCH_SIZE", "10"))

    # Notification channels
    NOTIFY_DISCORD_WEBHOOK: Optional[str] = os.getenv("NOTIFY_DISCORD_WEBHOOK", "") or None
    NOTIFY_TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("NOTIFY_TELEGRAM_BOT_TOKEN", "") or None
    NOTIFY_TELEGRAM_CHAT_ID: Optional[str] = os.getenv("NOTIFY_TELEGRAM_CHAT_ID", "") or None
    NOTIFY_EMAIL_TO: Optional[str] = os.getenv("NOTIFY_EMAIL_TO", "") or None
    NOTIFY_SMTP_HOST: Optional[str] = os.getenv("NOTIFY_SMTP_HOST", "") or None
    NOTIFY_SMTP_PORT: int = int(os.getenv("NOTIFY_SMTP_PORT", "587"))
    NOTIFY_SMTP_USER: Optional[str] = os.getenv("NOTIFY_SMTP_USER", "") or None
    NOTIFY_SMTP_PASS: Optional[str] = os.getenv("NOTIFY_SMTP_PASS", "") or None

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Path = LOG_DIR / "cookie_runners.log"

    # Content hash algorithm
    HASH_ALGORITHM: str = os.getenv("HASH_ALGORITHM", "sha256")

    # Update detection sensitivity
    DETECT_TITLE_CHANGES: bool = os.getenv("DETECT_TITLE_CHANGES", "true").lower() in (
        "true", "1", "yes"
    )
    DETECT_BODY_CHANGES: bool = os.getenv("DETECT_BODY_CHANGES", "true").lower() in (
        "true", "1", "yes"
    )
    DETECT_META_CHANGES: bool = os.getenv("DETECT_META_CHANGES", "false").lower() in (
        "true", "1", "yes"
    )

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    def __repr__(self) -> str:
        safe = {k: v for k, v in self.__dict__.items() if "PASS" not in k and "KEY" not in k}
        return f"Settings({safe})"

    def __getitem__(self, key: str):
        return getattr(self, key)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
settings = Settings()
