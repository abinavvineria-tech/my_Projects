"""The Missing Piece SSH — Flask GUI.

Binds to 127.0.0.1 by default for safety. No public-network exposure
unless --host 0.0.0.0 is explicitly passed to start.sh.

Routes (UI):
    /            Dashboard
    /connect     Connect form
    /terminal    Web terminal (xterm.js + WebSocket)
    /sftp        File manager
    /hosts       Profile manager
    /settings    Settings
    /about       About

API endpoints (used by the UI JS):
    POST /api/connect          {host, port, username, key_path, hostkey_action}
    POST /api/disconnect
    GET  /api/status
    POST /api/command          {command}
    POST /api/hostkey/approve  {host, port, action: accept|reject|once}
    GET  /api/sftp/list        ?path=
    POST /api/sftp/upload
    POST /api/sftp/mkdir       {path}
    POST /api/sftp/rename      {old, new}
    POST /api/sftp/download    {path}
    DELETE /api/sftp/delete    {path}
    GET  /api/hosts
    POST /api/hosts            {name, hostname, port, username, identity_file}
    PUT  /api/hosts/<name>
    DELETE /api/hosts/<name>
    GET  /api/settings
    POST /api/settings         {settings}
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from pathlib import Path
from typing import Optional

# Ensure package paths are resolvable when invoked as a script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import (
    Flask, render_template, request, jsonify, send_from_directory,
    abort, Response,
)
from flask_cors import CORS

import config
from core.logging import get_logger, secure_log_event
from core.profiles import ProfileManager, HostProfile
from core.hostkeys import HostKeyManager
from core.ssh_client import SSHClient, TMPSSHError, SSHErrorKind
from core.sftp import SFTPManager

logger = get_logger("web")

# ── Session state ─────────────────────────────────────────────────────────────

class WebSession:
    """Holds the user's current SSH session in memory."""
    def __init__(self):
        self.client: Optional[SSHClient] = None
        self.lock = threading.Lock()
        self.hostkey_pending: Optional[dict] = None

    def status(self) -> dict:
        if self.client and self.client.connected:
            return {"connected": True, "host": self.client.host,
                    "port": self.client.port, "username": self.client.username,
                    "since": getattr(self, "_since", 0)}
        return {"connected": False}

    def require(self) -> SSHClient:
        if not self.client or not self.client.connected:
            abort(409, description="not connected")
        return self.client

SESSION = WebSession()

# ── Flask app ─────────────────────────────────────────────────────────────────

app = Flask(
    __name__,
    template_folder=str(config.project_root() / "templates"),
    static_folder=str(config.project_root() / "static"),
)
CORS(app)

@app.errorhandler(TMPSSHError)
def _tmpssh_error(e: TMPSSHError):
    secure_log_event(logger, "warning", e.message, kind=e.kind.value,
                     host=e.host, port=e.port)
    return jsonify({
        "ok": False,
        "kind": e.kind.value,
        "message": e.friendly(),
        "suggestion": e.suggestion,
    }), 400

@app.errorhandler(404)
def _not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "message": "not found"}), 404
    return render_template("index.html"), 200

@app.errorhandler(500)
def _server_error(e):
    logger.exception("internal error")
    return jsonify({"ok": False, "message": "internal server error"}), 500

# ── UI routes ─────────────────────────────────────────────────────────────────

@app.get("/")
def page_index():
    return render_template(
        "index.html",
        app_name=config.APP_FULL,
        version=config.VERSION,
        termux=config.is_termux(),
    )

@app.get("/connect")
def page_connect():
    return render_template("connect.html",
                           app_name=config.APP_FULL, version=config.VERSION)

@app.get("/terminal")
def page_terminal():
    return render_template("terminal.html",
                           app_name=config.APP_FULL, version=config.VERSION)

@app.get("/sftp")
def page_sftp():
    return render_template("sftp.html",
                           app_name=config.APP_FULL, version=config.VERSION)

@app.get("/hosts")
def page_hosts():
    return render_template("hosts.html",
                           app_name=config.APP_FULL, version=config.VERSION)

@app.get("/settings")
def page_settings():
    return render_template("settings.html",
                           app_name=config.APP_FULL, version=config.VERSION)

@app.get("/about")
def page_about():
    return render_template("about.html",
                           app_name=config.APP_FULL, version=config.VERSION,
                           info=config.sys_info())

# ── API: connection ───────────────────────────────────────────────────────────

@app.post("/api/connect")
def api_connect():
    """Connect to an SSH host.

    If the host is unknown, we DO NOT auto-accept. We return a
    "hostkey_pending" payload so the UI can prompt the user to accept/reject.
    """
    data = request.get_json(force=True, silent=True) or {}
    host = (data.get("host") or "").strip()
    if not host:
        return jsonify({"ok": False, "message": "host is required"}), 400
    port = int(data.get("port") or 22)
    username = (data.get("username") or "").strip()
    key_path = data.get("key_path") or ""
    if not username:
        return jsonify({"ok": False, "message": "username is required"}), 400

    # Validate hostname/port
    from core.profiles import is_valid_hostname, is_valid_port
    if not is_valid_hostname(host):
        return jsonify({"ok": False, "message": "invalid hostname"}), 400
    if not is_valid_port(port):
        return jsonify({"ok": False, "message": "invalid port"}), 400

    if key_path:
        from core.profiles import is_valid_key_path
        if not is_valid_key_path(key_path):
            return jsonify({"ok": False, "message": "ssh key not found"}), 400

    SESSION.lock.acquire()
    try:
        # Disconnect any prior session
        if SESSION.client:
            try: SESSION.client.disconnect()
            except Exception: pass
            SESSION.client = None

        # Host-key preflight: check if the host is known.
        hkm = HostKeyManager()
        status, fp = hkm.check(host, port)
        if status.name == "CHANGED":
            return jsonify({
                "ok": False,
                "kind": "host_key_changed",
                "message": "🚨 HOST KEY CHANGED",
                "detail": ("The server's identity does not match the previously trusted "
                          "identity. Connection blocked. Verify out-of-band before re-accepting."),
                "fingerprint": fp,
            }), 409
        if status.name == "UNKNOWN":
            # Compute fingerprint without accepting
            new_fp = hkm.compute_fingerprint(host, port) if hasattr(hkm, "compute_fingerprint") else fp
            return jsonify({
                "ok": False,
                "kind": "host_key_unknown",
                "message": "⚠ Unknown SSH host",
                "fingerprint": new_fp,
                "host": host,
                "port": port,
            }), 409

        cli = SSHClient(host=host, port=port, username=username,
                        key_path=key_path or None,
                        timeout=int(data.get("timeout") or 10))
        try:
            cli.connect()
        except TMPSSHError as e:
            return jsonify({
                "ok": False,
                "kind": e.kind.value,
                "message": e.friendly(),
                "suggestion": e.suggestion,
            }), 400
        SESSION.client = cli
        SESSION._since = int(time.time())
        hkm.mark_trusted(host, port)
    finally:
        SESSION.lock.release()
    return jsonify({"ok": True, "status": SESSION.status()})

@app.post("/api/hostkey/approve")
def api_hostkey_approve():
    """Approve a previously-unknown host key. Then caller can retry connect."""
    data = request.get_json(force=True, silent=True) or {}
    host = (data.get("host") or "").strip()
    port = int(data.get("port") or 22)
    action = (data.get("action") or "").strip().lower()
    if not host or action not in {"accept", "reject"}:
        return jsonify({"ok": False, "message": "bad request"}), 400
    hkm = HostKeyManager()
    if action == "reject":
        return jsonify({"ok": True, "rejected": True})
    hkm.trust(host, port)
    return jsonify({"ok": True, "trusted": True})

@app.post("/api/disconnect")
def api_disconnect():
    with SESSION.lock:
        if SESSION.client:
            try: SESSION.client.disconnect()
            except Exception: pass
            SESSION.client = None
    return jsonify({"ok": True, "status": SESSION.status()})

@app.get("/api/status")
def api_status():
    return jsonify({"ok": True, "status": SESSION.status(),
                    "app": config.APP_FULL, "version": config.VERSION,
                    "termux": config.is_termux(),
                    "info": config.sys_info()})

@app.post("/api/command")
def api_command():
    data = request.get_json(force=True, silent=True) or {}
    cmd = (data.get("command") or "").strip()
    if not cmd:
        return jsonify({"ok": False, "message": "command is required"}), 400
    cli = SESSION.require()
    out, err, rc = cli.execute(cmd)
    return jsonify({"ok": True, "stdout": out, "stderr": err, "exit_code": rc})

# ── API: SFTP ─────────────────────────────────────────────────────────────────

@app.get("/api/sftp/list")
def api_sftp_list():
    path = request.args.get("path", "/")
    sftp = SESSION.require().get_sftp()
    items = sftp.list(path)
    return jsonify({"ok": True, "path": path, "items": [vars(i) for i in items]})

@app.post("/api/sftp/mkdir")
def api_sftp_mkdir():
    data = request.get_json(force=True, silent=True) or {}
    path = (data.get("path") or "").strip()
    if not path:
        return jsonify({"ok": False, "message": "path required"}), 400
    SESSION.require().get_sftp().mkdir(path)
    return jsonify({"ok": True})

@app.post("/api/sftp/rename")
def api_sftp_rename():
    data = request.get_json(force=True, silent=True) or {}
    old = (data.get("old") or "").strip()
    new = (data.get("new") or "").strip()
    if not old or not new:
        return jsonify({"ok": False, "message": "old and new required"}), 400
    SESSION.require().get_sftp().rename(old, new)
    return jsonify({"ok": True})

@app.delete("/api/sftp/delete")
def api_sftp_delete():
    data = request.get_json(force=True, silent=True) or {}
    path = (data.get("path") or "").strip()
    if not path:
        return jsonify({"ok": False, "message": "path required"}), 400
    SESSION.require().get_sftp().delete(path)
    return jsonify({"ok": True})

@app.post("/api/sftp/upload")
def api_sftp_upload():
    """Upload a local file to a remote path.

    Body (multipart/form-data): file=<file>, path=<remote path>
    """
    if "file" not in request.files:
        return jsonify({"ok": False, "message": "file field required"}), 400
    f = request.files["file"]
    remote_path = request.form.get("path", "").strip()
    if not remote_path:
        return jsonify({"ok": False, "message": "path required"}), 400
    sftp = SESSION.require().get_sftp()
    sftp.upload(f.stream, remote_path)
    return jsonify({"ok": True})

@app.post("/api/sftp/download")
def api_sftp_download():
    data = request.get_json(force=True, silent=True) or {}
    path = (data.get("path") or "").strip()
    if not path:
        return jsonify({"ok": False, "message": "path required"}), 400
    from io import BytesIO
    sftp = SESSION.require().get_sftp()
    buf = BytesIO()
    sftp.download(path, buf)
    buf.seek(0)
    return Response(
        buf.getvalue(),
        mimetype="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{Path(path).name}"'},
    )

# ── API: hosts / settings ─────────────────────────────────────────────────────

@app.get("/api/hosts")
def api_hosts_list():
    pm = ProfileManager()
    return jsonify({"ok": True, "hosts": pm.list_names()})

@app.get("/api/hosts/<name>")
def api_hosts_get(name):
    pm = ProfileManager()
    h = pm.get(name)
    if h is None:
        abort(404)
    return jsonify({"ok": True, "host": vars(h)})

@app.post("/api/hosts")
def api_hosts_create():
    data = request.get_json(force=True, silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"ok": False, "message": "name required"}), 400
    pm = ProfileManager()
    try:
        h = pm.add(data)
    except ValueError as e:
        return jsonify({"ok": False, "message": str(e)}), 400
    return jsonify({"ok": True, "host": vars(h)})

@app.put("/api/hosts/<name>")
def api_hosts_update(name):
    data = request.get_json(force=True, silent=True) or {}
    pm = ProfileManager()
    try:
        h = pm.update(name, data)
    except KeyError:
        abort(404)
    except ValueError as e:
        return jsonify({"ok": False, "message": str(e)}), 400
    return jsonify({"ok": True, "host": vars(h)})

@app.delete("/api/hosts/<name>")
def api_hosts_delete(name):
    pm = ProfileManager()
    pm.remove(name)
    return jsonify({"ok": True})

@app.get("/api/settings")
def api_settings_get():
    return jsonify({"ok": True, "settings": config.Settings.load().to_dict()})

@app.post("/api/settings")
def api_settings_set():
    data = request.get_json(force=True, silent=True) or {}
    s = config.Settings.load()
    # Reject any attempt to write password / key / secret fields
    forbidden = {"password", "passwd", "secret", "token", "key",
                 "private_key", "passphrase"}
    for k in list(data.keys()):
        if k.lower() in forbidden:
            return jsonify({"ok": False, "message": f"{k} is forbidden"}), 400
        if hasattr(s, k):
            setattr(s, k, data[k])
    s.save()
    return jsonify({"ok": True, "settings": s.to_dict()})

# ── Run ───────────────────────────────────────────────────────────────────────

def run(host: str = "127.0.0.1", port: int = 5000, debug: bool = False):
    print(config.BANNER)
    print(f"🧩 {config.APP_FULL} v{config.VERSION}")
    print(f"   bound: http://{host}:{port}  (debug={debug})")
    print(f"   termux: {config.is_termux()}")
    print(f"   logs:   {__import__('core.logging', fromlist=['get_log_path']).get_log_path()}")
    print(f"   data:   {config.data_dir()}")
    print("   type Ctrl+C to stop\n")
    app.run(host=host, port=port, debug=debug, threaded=True)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--host", default=os.environ.get("TMPSSH_HOST", "127.0.0.1"))
    p.add_argument("--port", type=int, default=int(os.environ.get("TMPSSH_PORT", "5000")))
    p.add_argument("--debug", action="store_true")
    args = p.parse_args()
    run(args.host, args.port, args.debug)