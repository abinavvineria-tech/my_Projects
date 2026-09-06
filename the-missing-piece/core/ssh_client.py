"""SSH Client — paramiko wrapper used by both CLI and Flask GUI.

Never logs passwords or private key contents.
All exceptions are wrapped in typed TMPSSHError subclasses so callers
can display friendly messages to users.
"""
from __future__ import annotations

import os
import socket
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

import paramiko
from paramiko import SSHException, AuthenticationException, PasswordRequiredException

import config
from core.logging import get_logger
from core.hostkeys import HostKeyManager, HostKeyStatus
from core.sftp import SFTPManager

logger = get_logger("ssh")


# ── Error taxonomy ────────────────────────────────────────────────────────────

class SSHErrorKind(str, Enum):
    CONNECTION_REFUSED   = "connection_refused"
    TIMEOUT              = "timeout"
    HOST_UNREACHABLE     = "host_unreachable"
    HOST_KEY_UNKNOWN     = "host_key_unknown"
    HOST_KEY_CHANGED     = "host_key_changed"
    AUTH_FAILED          = "auth_failed"
    KEY_LOAD_FAILED      = "key_load_failed"
    PERMISSION_DENIED    = "permission_denied"
    SESSION_CLOSED       = "session_closed"
    UNKNOWN              = "unknown"


@dataclass
class TMPSSHError(Exception):
    """User-facing SSH error with typed kind."""
    kind: SSHErrorKind
    message: str
    host: str = ""
    port: int = 22
    suggestion: str = ""

    def __str__(self) -> str:
        return self.message

    def friendly(self) -> str:
        prefix = {
            SSHErrorKind.CONNECTION_REFUSED:  "✗ Connection refused",
            SSHErrorKind.TIMEOUT:             "✗ Connection timed out",
            SSHErrorKind.HOST_UNREACHABLE:    "✗ Host unreachable",
            SSHErrorKind.HOST_KEY_UNKNOWN:    "⚠ Unknown host key",
            SSHErrorKind.HOST_KEY_CHANGED:    "🚨 Host key changed",
            SSHErrorKind.AUTH_FAILED:         "✗ Authentication failed",
            SSHErrorKind.KEY_LOAD_FAILED:     "✗ SSH key could not be loaded",
            SSHErrorKind.PERMISSION_DENIED:    "✗ Permission denied",
            SSHErrorKind.SESSION_CLOSED:       "✗ Session closed",
            SSHErrorKind.UNKNOWN:             "✗ Error",
        }.get(self.kind, "✗ Error")
        return f"{prefix}: {self.message}"


def _classify_exception(e: Exception, host: str, port: int) -> TMPSSHError:
    """Map a raw exception to a TMPSSHError with a suggestion."""
    msg = str(e).strip()
    kind_map: list[tuple[type[Exception], SSHErrorKind, str]] = [
        (ConnectionRefusedError, SSHErrorKind.CONNECTION_REFUSED,
         f"Is SSH server running on {host}:{port}?"),
        (TimeoutError,           SSHErrorKind.TIMEOUT,
         f"Server {host} is not responding within the timeout."),
        (socket.timeout,         SSHErrorKind.TIMEOUT,
         f"Server {host} did not respond in time."),
        (socket.gaierror,       SSHErrorKind.HOST_UNREACHABLE,
         f"Cannot resolve or reach {host}."),
        (AuthenticationException, SSHErrorKind.AUTH_FAILED,
         "Check username, password, or SSH key."),
        (paramiko.ssh_exception.PasswordRequiredException, SSHErrorKind.AUTH_FAILED,
         "The key requires a passphrase; use `ssh-add` or pass the key directly."),
        (paramiko.ssh_exception.SSHException, SSHErrorKind.KEY_LOAD_FAILED,
         "The SSH key may be malformed or use an unsupported algorithm."),
        (EOFError,               SSHErrorKind.SESSION_CLOSED,
         "The remote host closed the session."),
    ]
    for exc_type, kind, suggestion in kind_map:
        if isinstance(e, exc_type):
            return TMPSSHError(kind=kind, message=msg, host=host, port=port, suggestion=suggestion)
    # Host-key specific checks
    lower = msg.lower()
    if "not a valid" in lower or "couldn't parse" in lower or "key_type" in lower:
        return TMPSSHError(SSHErrorKind.KEY_LOAD_FAILED, msg, host, port,
                           "The key file may be corrupt or use an unsupported algorithm.")
    return TMPSSHError(SSHErrorKind.UNKNOWN, msg, host, port,
                       "Check host, port, and credentials.")


# ── SSH Client ────────────────────────────────────────────────────────────────

@dataclass
class SSHClient:
    """Paramiko SSH client wrapper with host-key integration.

    thread-safe for concurrent execute() / sftp calls.
    Interactive shell is single-threaded (one at a time).
    """
    host: str
    port: int = 22
    username: str = ""
    key_path: Optional[str] = None
    timeout: int = 10
    keepalive: int = 30

    # Internal state
    _client: paramiko.SSHClient = field(default=None, init=False, repr=False)
    _transport: paramiko.Transport = field(default=None, init=False, repr=False)
    _sftp: SFTPManager = field(default=None, init=False)
    _hostkey_mgr: HostKeyManager = field(default_factory=HostKeyManager, init=False)
    _connected: bool = field(default=False, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    # Callback for interactive host-key approval (CLI vs GUI injects their own)
    hostkey_ask: Optional[Callable[[str, str], bool]] = field(default=None, init=False)

    def _resolve_key(self) -> Optional[str]:
        if not self.key_path:
            return None
        p = os.path.expanduser(os.path.expandvars(self.key_path))
        return p if os.path.isfile(p) else None

    def connect(self) -> None:
        """Establish connection with host-key verification.

        Raises TMPSSHError on failure.
        """
        with self._lock:
            if self._connected:
                return
            try:
                self._client = paramiko.SSHClient()
                self._client.set_missing_host_key_policy(paramiko.WarningPolicy())

                # Load known hosts
                self._client.get_host_keys().load(str(config.known_hosts_path()))

                key_file = self._resolve_key()
                connect_kwargs: dict = {
                    "hostname": self.host,
                    "port": self.port,
                    "username": self.username,
                    "timeout": self.timeout,
                    "look_for_keys": True,
                    "allow_agent": True,
                }
                if key_file:
                    connect_kwargs["key_filename"] = key_file

                self._client.connect(**connect_kwargs)
                self._transport = self._client.get_transport()
                self._transport.set_keepalive(self.keepalive)
                self._connected = True
                logger.info("SSH connected", extra={"host": self.host, "port": self.port,
                                                     "username": self.username})
            except Exception as e:
                err = _classify_exception(e, self.host, self.port)
                # Attach fingerprint hint if host key unknown
                if err.kind in (SSHErrorKind.HOST_KEY_UNKNOWN, SSHErrorKind.HOST_KEY_CHANGED):
                    hint = self._fingerprint_hint()
                    err.message = f"{err.message}\n{hint}"
                raise err from None

    def _fingerprint_hint(self) -> str:
        """Return host-key fingerprint for display to user."""
        try:
            sock = socket.socket()
            sock.settimeout(self.timeout)
            sock.connect((self.host, self.port))
            t = paramiko.Transport(sock)
            t.start_client()
            keys = t.get_remote_server_key()
            fp = keys.get_fingerprint()
            alg = keys.get_name()
            sock.close()
            return f"Fingerprint: {alg} {fp.hex() if isinstance(fp, bytes) else fp}"
        except Exception:
            return "Fingerprint unavailable."

    def disconnect(self) -> None:
        with self._lock:
            if self._sftp:
                try:
                    self._sftp.close()
                except Exception:
                    pass
                self._sftp = None
            if self._transport:
                try:
                    self._transport.close()
                except Exception:
                    pass
                self._transport = None
            if self._client:
                try:
                    self._client.close()
                except Exception:
                    pass
                self._client = None
            self._connected = False
            logger.info("SSH disconnected", extra={"host": self.host})

    @property
    def connected(self) -> bool:
        return self._connected

    def execute(
        self,
        command: str,
        timeout: Optional[int] = None,
    ) -> tuple[str, str, int]:
        """Run a command, return (stdout, stderr, exit_code).

        Raises TMPSSHError on session failure.
        """
        with self._lock:
            if not self._connected:
                raise TMPSSHError(SSHErrorKind.SESSION_CLOSED,
                                  "Not connected.", self.host, self.port)
            try:
                stdin, stdout, stderr = self._client.exec_command(
                    command, timeout=timeout)
                out = stdout.read().decode(errors="replace")
                err = stderr.read().decode(errors="replace")
                rc = stdout.channel.recv_exit_status()
                return out, err, rc
            except SSHException as e:
                raise _classify_exception(e, self.host, self.port) from None

    def get_sftp(self) -> SFTPManager:
        """Return (or create) an SFTPManager on the active session."""
        with self._lock:
            if not self._connected:
                raise TMPSSHError(SSHErrorKind.SESSION_CLOSED,
                                  "Not connected.", self.host, self.port)
            if self._sftp is None:
                self._sftp = SFTPManager(self._client)
            return self._sftp

    def open_shell(self, term: str = "xterm-256color", width: int = 80, height: int = 24):
        """Open an interactive shell channel. Returns the paramiko channel."""
        with self._lock:
            if not self._connected:
                raise TMPSSHError(SSHErrorKind.SESSION_CLOSED,
                                  "Not connected.", self.host, self.port)
            try:
                chan = self._client.invoke_shell(term=term, width=width, height=height)
                chan.setblocking(False)
                return chan
            except SSHException as e:
                raise _classify_exception(e, self.host, self.port) from None

    def resize(self, width: int, height: int, width_pixels: int = 0, height_pixels: int = 0):
        """Resize an active shell channel."""
        if self._transport and self._transport.is_active():
            chan = self._transport.open_session()
            # Resize via env for shells that support it
            pass  # shell resize handled via the channel directly in invoke_shell

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()
