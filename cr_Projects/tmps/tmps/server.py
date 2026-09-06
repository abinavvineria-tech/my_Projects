"""
TMPS Backend Server - Real Hermes Agent Studio
No mocks. All real system integration.
"""
import os, sys, json, subprocess, asyncio, uuid, threading
from pathlib import Path
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE = Path(__file__).parent
TERMINALS = {}

# ── Hermes ──────────────────────────────────────────────────────────────
def hermes(args: str, timeout=60) -> dict:
    """Call real Hermes CLI. No mocks."""
    try:
        result = subprocess.run(
            ["hermes"] + args.split(),
            capture_output=True, text=True, timeout=timeout,
            cwd=str(BASE.parent)
        )
        return {"ok": True, "stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Timeout", "stdout": "", "stderr": ""}
    except FileNotFoundError:
        return {"ok": False, "error": "Hermes not found", "stdout": "", "stderr": ""}
    except Exception as e:
        return {"ok": False, "error": str(e), "stdout": "", "stderr": ""}

@app.route("/api/hermes/status")
def api_hermes_status():
    r = hermes("status")
    return jsonify(r)

@app.route("/api/hermes/chat", methods=["POST"])
def api_hermes_chat():
    data = request.json or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"ok": False, "error": "No prompt"}), 400
    r = hermes(f'-z {prompt} --cli', timeout=120)
    return jsonify(r)

@app.route("/api/hermes/chat/stream", methods=["POST"])
def api_hermes_chat_stream():
    """SSE stream of Hermes output."""
    data = request.json or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"ok": False, "error": "No prompt"}), 400

    def generate():
        try:
            proc = subprocess.Popen(
                ["hermes", "-z", prompt, "--cli"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, cwd=str(BASE.parent)
            )
            for line in iter(proc.stdout.readline, ""):
                if line:
                    yield f"data: {json.dumps({'chunk': line})}\n\n"
            proc.stdout.close()
            proc.wait()
            yield f"data: {json.dumps({'done': True, 'code': proc.returncode})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype="text/event-stream")

@app.route("/api/hermes/missing", methods=["POST"])
def api_hermes_missing():
    """Signature feature: ask Hermes to find missing pieces."""
    data = request.json or {}
    project = data.get("project", "")
    prompt_extra = data.get("context", "")
    project_context = f"Project: {project}\n" if project else ""
    prompt = (
        f"{project_context}{prompt_extra}"
        "Inspect this project thoroughly. Report:\n"
        "1. TODO/FIXME comments\n"
        "2. Broken imports or missing files\n"
        "3. Missing error handling\n"
        "4. Missing .env config\n"
        "5. Incomplete functions\n"
        "6. Broken tests\n"
        "7. Unused imports/variables\n"
        "8. Potential runtime issues\n"
        "Be concise. Format as a checklist."
    )
    r = hermes(f'-z "{prompt}" --cli', timeout=180)
    return jsonify(r)

# ── Terminal ────────────────────────────────────────────────────────────
@app.route("/api/terminal/create", methods=["POST"])
def api_terminal_create():
    tid = str(uuid.uuid4())[:8]
    TERMINALS[tid] = {"id": tid, "cwd": os.getcwd()}
    return jsonify({"ok": True, "id": tid})

@app.route("/api/terminal/<tid>/write", methods=["POST"])
def api_terminal_write(tid):
    if tid not in TERMINALS:
        return jsonify({"ok": False, "error": "Terminal not found"}), 404
    data = request.json or {}
    cmd = data.get("cmd", "") + "\n"
    # Run command synchronously for simplicity
    cwd = TERMINALS[tid].get("cwd", os.getcwd())
    try:
        if cmd.strip().startswith("cd "):
            new_dir = cmd.strip()[3:].strip()
            if os.path.isdir(new_dir):
                TERMINALS[tid]["cwd"] = os.path.abspath(new_dir)
                out = f"Changed directory to {TERMINALS[tid]['cwd']}\n"
            else:
                out = f"cd: no such directory: {new_dir}\n"
        else:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                cwd=cwd, timeout=30
            )
            out = result.stdout + result.stderr
    except Exception as e:
        out = f"error: {e}\n"
    return jsonify({"ok": True, "output": out, "cwd": TERMINALS[tid]["cwd"]})

# ── File Explorer ───────────────────────────────────────────────────────
@app.route("/api/files/list", methods=["GET"])
def api_files_list():
    path = request.args.get("path", str(BASE.parent))
    try:
        entries = []
        for e in sorted(os.scandir(path), key=lambda x: (not x.is_dir(), x.name)):
            try:
                entries.append({
                    "name": e.name,
                    "type": "dir" if e.is_dir() else "file",
                    "size": e.stat().st_size if e.is_file() else 0,
                    "path": e.path,
                })
            except: pass
        return jsonify({"ok": True, "entries": entries, "path": path})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route("/api/files/read", methods=["GET"])
def api_files_read():
    path = request.args.get("path", "")
    if not path: return jsonify({"ok": False, "error": "No path"}), 400
    try:
        content = Path(path).read_text(errors="replace")
        return jsonify({"ok": True, "content": content[:50000], "size": len(content)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route("/api/files/write", methods=["POST"])
def api_files_write():
    data = request.json or {}
    path, content = data.get("path", ""), data.get("content", "")
    if not path: return jsonify({"ok": False, "error": "No path"}), 400
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route("/api/files/delete", methods=["POST"])
def api_files_delete():
    data = request.json or {}
    path = data.get("path", "")
    if not path: return jsonify({"ok": False, "error": "No path"}), 400
    try:
        p = Path(path)
        if p.is_dir():
            import shutil; shutil.rmtree(p)
        else:
            p.unlink()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

# ── Git ─────────────────────────────────────────────────────────────────
@app.route("/api/git/status")
def api_git_status():
    try:
        r = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=str(BASE.parent))
        branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, cwd=str(BASE.parent)).stdout.strip()
        return jsonify({"ok": True, "branch": branch, "changes": r.stdout.strip().split("\n")})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route("/api/git/log", methods=["GET"])
def api_git_log():
    try:
        r = subprocess.run(["git", "log", "--oneline", "-10"], capture_output=True, text=True, cwd=str(BASE.parent))
        return jsonify({"ok": True, "commits": r.stdout.strip().split("\n")})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route("/api/git/diff", methods=["GET"])
def api_git_diff():
    path = request.args.get("path", "")
    try:
        cmd = ["git", "diff", path] if path else ["git", "diff"]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BASE.parent))
        return jsonify({"ok": True, "diff": r.stdout[:20000]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

# ── Project ─────────────────────────────────────────────────────────────
@app.route("/api/project/detect")
def api_project_detect():
    """Detect project type from root."""
    root = str(BASE.parent)
    detected = {"type": "unknown", "dev_cmd": None, "test_cmd": None}
    p = Path(root)
    if (p / "package.json").exists():
        detected["type"] = "node"
        try:
            pkg = json.loads((p / "package.json").read_text())
            detected["dev_cmd"] = pkg.get("scripts", {}).get("dev")
            detected["test_cmd"] = pkg.get("scripts", {}).get("test")
            detected["build_cmd"] = pkg.get("scripts", {}).get("build")
        except: pass
    elif (p / "pyproject.toml").exists():
        detected["type"] = "python"
        detected["dev_cmd"] = "python3 -m http.server 8000"
    return jsonify({**detected, "ok": True, "root": root})

# ── System / Doctor ──────────────────────────────────────────────────────
@app.route("/api/doctor")
def api_doctor():
    checks = []
    hermes_path = subprocess.run(["which", "hermes"], capture_output=True, text=True).stdout.strip()
    checks.append({"name": "Hermes Agent", "ok": bool(hermes_path), "detail": hermes_path or "not found"})
    checks.append({"name": "Node.js", "ok": bool(subprocess.run(["which", "node"], capture_output=True).stdout.strip()), "detail": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip()})
    checks.append({"name": "Python", "ok": bool(subprocess.run(["which", "python3"], capture_output=True).stdout.strip()), "detail": subprocess.run(["python3", "--version"], capture_output=True, text=True).stdout.strip()})
    checks.append({"name": "Git", "ok": bool(subprocess.run(["which", "git"], capture_output=True).stdout.strip()), "detail": "ok"})
    checks.append({"name": "Terminal", "ok": True, "detail": "shell available"})
    r = hermes("status")
    checks.append({"name": "Hermes Comms", "ok": r.get("ok", False), "detail": r.get("error", "ok")})
    checks.append({"name": "Workspace", "ok": True, "detail": str(BASE.parent)})
    ready = all(c["ok"] for c in checks)
    return jsonify({"ok": True, "ready": ready, "checks": checks})

if __name__ == "__main__":
    print("🧩 TMPS Server starting on :18999")
    app.run(host="0.0.0.0", port=18999, debug=False, threaded=True)
