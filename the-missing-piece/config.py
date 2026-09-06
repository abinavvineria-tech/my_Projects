"""Configuration, paths, defaults. Termux-aware."""
from __future__ import annotations

import os
import socket
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


APP_NAME = "tmpssh"
APP_FULL = "The Missing Piece SSH"
TAGLINE = "🧩 Connect. Manage. Complete the missing piece."
VERSION = "1.0.0"

DEFAULT_PORT = 22
DEFAULT_TIMEOUT = 10
DEFAULT_KEEPALIVE = 30
BANNER = r"""
╔══════════════════════════════════════╗
║        🧩 THE MISSING PIECE SSH     ║
║          SSH CLIENT FOR TERMUX      ║
╚══════════════════════════════════════╝
"""


def is_termux() -> bool:
    """Return True if we appear to be running inside Termux on Android."""
    return (
        "com.termux" in os.environ.get("PREFIX", "")
        or os.path.exists("/data/data/com.termux")
        or os.environ.get("TERMUX_VERSION") is not None
    )


def data_dir() -> Path:
    """Project-local data directory (relative to project root)."""
    env = os.environ.get("TMPSSH_DATA_DIR")
    if env:
        p = Path(env)
    else:
        p = Path(__file__).resolve().parent.parent / "data"
    p.mkdir(parents=True, exist_ok=True)
    return p


def user_dir() -> Path:
    """Per-user runtime directory (logs, known_hosts cache)."""
    p = Path(os.environ.get("TMPSSH_HOME", str(Path.home() / ".tmpssh")))
    (p / "logs").mkdir(parents=True, exist_ok=True)
    return p


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def hosts_file() -> Path:
    return data_dir() / "hosts.json"


def settings_file() -> Path:
    return data_dir() / "settings.json"


def known_hosts_path() -> Path:
    p = user_dir() / "known_hosts"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


@dataclass
class Settings:
    """Engine + UI settings. Never contains credentials."""
    default_port: int = DEFAULT_PORT
    timeout: int = DEFAULT_TIMEOUT
    keepalive_interval: int = DEFAULT_KEEPALIVE
    font_size: int = 14
    theme: str = "dark"   # dark | light
    auto_reconnect: bool = True
    sftp_confirm: bool = True
    cli_banner: bool = True
    terminal_theme: str = "plum"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Settings":
        path = path or settings_file()
        if not path.exists():
            return cls()
        try:
            import json
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return cls()
        s = cls()
        for k, v in raw.items():
            if hasattr(s, k):
                setattr(s, k, v)
        return s

    def save(self, path: Optional[Path] = None) -> None:
        import json
        path = path or settings_file()
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")


def hostname_local() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "localhost"


def sys_info() -> dict:
    import platform
    return {
        "app": APP_FULL,
        "version": VERSION,
        "termux": is_termux(),
        "hostname": hostname_local(),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }