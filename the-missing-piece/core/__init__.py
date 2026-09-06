"""The Missing Piece SSH — core package."""
__version__ = "1.0.0"
__app_name__ = "tmpssh"
__tagline__ = "🧩 Connect. Manage. Complete the missing piece."

from core.ssh_client import SSHClient
from core.connection import ConnectionManager
from core.hostkeys import HostKeyManager, HostKeyStatus
from core.profiles import ProfileManager, HostProfile, HostSpec
from core.sftp import SFTPManager
from core.logging import get_logger, get_log_path, secure_log_event

__all__ = [
    "SSHClient",
    "ConnectionManager",
    "HostKeyManager",
    "HostKeyStatus",
    "ProfileManager",
    "HostProfile",
    "HostSpec",
    "SFTPManager",
    "get_logger",
    "get_log_path",
    "secure_log_event",
]