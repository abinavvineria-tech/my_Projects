"""Safe logging — never log passwords, keys, or secrets.

Pattern-based redaction at the formatter level is intentionally aggressive:
if a log line *could* contain a key blob, password, token, or SSH key
fingerprint string longer than a normal hostname, it is masked.

All log records also flow through a custom filter that strips args
matching common secret names (password, passwd, pwd, secret, token,
key, private_key, private, auth, credential).
"""
from __future__ import annotations

import logging
import os
import re
import sys
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

# Names that should never be logged
_SECRET_KEYS = frozenset({
    "password", "passwd", "pwd", "secret", "token", "key",
    "private_key", "private", "auth", "credential", "credentials",
    "passphrase", "auth_token", "session_token", "access_token",
    "refresh_token", "api_key", "secret_key", "ssh_key",
})

# Patterns redacted from any log line
_REDACT_PATTERNS = [
    re.compile(r"(?i)(password|passwd|pwd|secret|token|api[-_]?key)[\s:=]+\S+"),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+PRIVATE KEY-----"),
    re.compile(r"-----BEGIN [A-Z ]+KEY-----[\s\S]+?-----END [A-Z ]+KEY-----"),
    re.compile(r"\bssh-(rsa|dss|ed25519|ecdsa-sha2-[a-z0-9-]+)\s+[A-Za-z0-9+/=]{40,}"),
    re.compile(r"(?i)(passphrase)[\s:=]+\S+"),
]


class _SecureFilter(logging.Filter):
    """Filter that redacts known-secret kwargs from log records."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        # Mask secret kwargs in args
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: ("[REDACTED]" if k.lower().replace("-", "_") in _SECRET_KEYS else v)
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, tuple):
                # tuple-style args cannot reliably map secrets; drop via msg rewrite
                record.args = tuple("[REDACTED]" if i == 0 else a for i, a in enumerate(record.args))

        # Redact patterns in the formatted message
        msg = record.getMessage()
        for pat in _REDACT_PATTERNS:
            msg = pat.sub("[REDACTED]", msg)
        record.msg = msg
        record.args = ()
        return True


_LOCK = threading.Lock()
_LOGGERS: dict[str, logging.Logger] = {}


def _log_dir() -> Path:
    base = Path(os.environ.get("TMPSSH_DATA_DIR", str(Path.home() / ".tmpssh")))
    (base / "logs").mkdir(parents=True, exist_ok=True)
    return base / "logs"


def get_logger(name: str = "tmpssh") -> logging.Logger:
    """Return a process-wide logger with safe filters."""
    with _LOCK:
        existing = _LOGGERS.get(name)
        if existing is not None:
            return existing

        logger = logging.getLogger(name)
        if logger.handlers:  # already configured
            _LOGGERS[name] = logger
            return logger

        logger.setLevel(os.environ.get("TMPSSH_LOG_LEVEL", "INFO").upper())
        logger.propagate = False

        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Rotating file
        fh = RotatingFileHandler(
            _log_dir() / "tmpssh.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        fh.addFilter(_SecureFilter())

        # Console (stderr)
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.WARNING)
        ch.setFormatter(logging.Formatter("%(levelname)-7s %(message)s"))
        ch.addFilter(_SecureFilter())

        logger.addHandler(fh)
        logger.addHandler(ch)
        _LOGGERS[name] = logger
        return logger


def get_log_path() -> str:
    """Absolute path to the active log file."""
    return str(_log_dir() / "tmpssh.log")


def secure_log_event(
    logger: logging.Logger,
    level: str,
    message: str,
    **fields: Any,
) -> None:
    """Log a structured event, dropping any field whose name looks secret."""
    safe = {k: v for k, v in fields.items() if k.lower() not in _SECRET_KEYS}
    getattr(logger, level.lower())(message, extra=safe) if safe else getattr(logger, level.lower())(message)


def clear_old_logs(days: int = 7) -> int:
    """Remove rotated log backups older than `days`. Returns count removed."""
    import time as _t
    removed = 0
    cutoff = _t.time() - days * 86400
    for f in _log_dir().glob("*.log*"):
        try:
            if f.stat().st_mtime < cutoff:
                f.unlink()
                removed += 1
        except OSError:
            pass
    return removed