# 🧩 The Missing Piece SSH (tmpssh)

Modern SSH Client — CLI + Flask GUI for Termux.
Two interfaces sharing a single Python SSH engine.

| Symbol | Meaning |
|---|---|
| ✅ | verified |
| ⚠ | known limitation |
| 🧩 | "the missing piece" feature |

## What it does

- **CLI** — `tmpssh connect user@host`, `hosts`, `add-host`, `sftp`, `web`, `status`, `version`, `help`.
- **GUI** — Flask + xterm.js browser terminal, SFTP file manager, host profiles, settings.
- **Engine** — `paramiko`-based core used by both interfaces. Host-key verification required. Passwords never stored. Logs redact secrets.

## Layout

```
the-missing-piece-ssh/
├── app.py            Flask GUI (xterm.js + SFTP)
├── cli.py            tmpssh CLI
├── config.py         Paths, defaults, Termux detection
├── requirements.txt
├── README.md
├── LICENSE
├── core/             Shared SSH engine
│   ├── __init__.py
│   ├── ssh_client.py
│   ├── connection.py
│   ├── hostkeys.py
│   ├── profiles.py
│   ├── sftp.py
│   └── logging.py
├── templates/        Flask Jinja2 templates
├── static/           CSS / JS / icons
├── data/             hosts.json + settings.json
├── scripts/          install.sh + start.sh
└── tests/            pytest unit tests
```

## Install (Termux)

```bash
cd ~/Projects/the-missing-piece-ssh
bash scripts/install.sh
```

The installer:
1. Detects Termux (`$PREFIX` + `/data/data/...`).
2. Checks Python 3.8+.
3. Creates a venv in `.venv` (uses `--system-site-packages` so Termux-built `cryptography` is reused).
4. Installs requirements with `--no-build-isolation`.
5. Creates `data/`, `~/.tmpssh/logs/`.
6. Prints usage.

## CLI usage

```bash
tmpssh connect user@example.com           # SSH key auth
tmpssh connect user@example.com -p 2222
tmpssh connect my-profile                 # saved profile
tmpssh hosts
tmpssh add-host                           # interactive
tmpssh remove-host NAME
tmpssh sftp user@example.com
tmpssh status
tmpssh web                                # http://127.0.0.1:5000
tmpssh web --port 8080
tmpssh config                             # show config
tmpssh version
tmpssh help
```

Equivalent module invocation:
```bash
python -m tmpssh
```

## GUI usage

```bash
tmpssh web
# open http://127.0.0.1:5000 in Termux browser
```

Pages:
- `/` Dashboard — connection status, recent hosts, quick connect.
- `/connect` Connect form (hostname, port, user, key path).
- `/terminal` xterm.js WebSocket terminal.
- `/sftp` Remote file manager.
- `/hosts` Profile CRUD.
- `/settings` UI + engine settings.
- `/about` Version + credits.

## Host profiles

`data/hosts.json`:

```json
{
  "name": "my-server",
  "hostname": "example.com",
  "port": 22,
  "username": "user",
  "identity_file": "~/.ssh/id_ed25519"
}
```

Passwords are never stored. Auth uses SSH key (preferred) or interactive secure prompt.

## SSH key setup

```bash
ssh-keygen -t ed25519 -C "tmpssh-termux"
ssh-copy-id user@example.com
tmpssh connect user@example.com
```

## Host-key security

First connection: fingerprint prompt. **No silent bypass.**
Changed key: connection blocked. Verify out-of-band before re-accepting.

## Settings

Stored in `data/settings.json`:

```json
{
  "default_port": 22,
  "timeout": 10,
  "font_size": 14,
  "theme": "dark",
  "auto_reconnect": true,
  "sftp_confirm": true,
  "known_hosts_path": "~/.tmpssh/known_hosts",
  "cli_banner": true
}
```

## Tests

```bash
python -m pytest tests/ -v
```

Tests cover config, profile validation, hostname/port validation, host-key logic, SFTP path handling, Flask routes, and connection error mapping. They **do not require a real SSH server** — paramiko transport is mocked.

## Security notes

- Host-key verification is mandatory. First-time prompts are explicit.
- Passwords are not echoed and never persisted.
- Private keys are not logged.
- GUI runs on `127.0.0.1` by default. External bind requires explicit `--host 0.0.0.0`.
- API endpoints cannot execute commands on the local Termux host from a browser request — only on the SSH target selected by the user.
- Logs redact `password|passwd|pwd|secret|token|key`, SSH key blobs, and `ssh-rsa/...` strings.

## Troubleshooting

| Problem | Fix |
|---|---|
| `paramiko ImportError` on Termux | `pip install --no-build-isolation paramiko` |
| `cryptography` ABI mismatch | Reuse system site-packages: venv created with `--system-site-packages` |
| `Port 5000 in use` | `tmpssh web --port 8080` |
| Host-key mismatch | `rm data/known_hosts.json` line for that host, then re-trust after verifying out-of-band |
| SFTP `Permission denied` | remote account lacks `sftp-server`; check `/etc/ssh/sshd_config` |
| xterm.js blank screen | HTTP not HTTPS — fine for local. WS works on plain HTTP. |

## Architecture

```
           ┌──────────────────┐
           │   cli.py         │
           │  tmpssh CLI      │
           └────────┬─────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │       core/            │
        │ ssh_client · connection│
        │ hostkeys · sftp        │
        │ profiles · logging      │
        └────────┬───────────────┘
                 │
                 ▼
           paramiko / OpenSSH
                 ▲
                 │
        ┌────────┴─────────┐
        │     app.py        │
        │   Flask GUI       │
        │  (xterm.js+WS)    │
        └───────────────────┘
```

## License

MIT — see `LICENSE`.