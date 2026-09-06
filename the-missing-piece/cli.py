#!/usr/bin/env python3
"""tmpssh — The Missing Piece SSH CLI.

Run from the project directory:
    python cli.py version
    python cli.py hosts
    python cli.py connect user@host
    python cli.py web
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
import time
from pathlib import Path

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from core.logging import get_logger, get_log_path, secure_log_event
from core.profiles import ProfileManager, HostSpec, parse_user_host, is_valid_hostname, is_valid_port, is_valid_key_path
from core.hostkeys import HostKeyManager
from core.ssh_client import SSHClient, TMPSSHError

logger = get_logger("cli")


BANNER = config.BANNER
TAGLINE = config.TAGLINE


def banner() -> None:
    print(BANNER)
    print(f"   {config.APP_FULL} v{config.VERSION}")
    print(f"   {TAGLINE}")
    print(f"   {'Termux' if config.is_termux() else 'Generic'} | "
          f"Python {sys.version.split()[0]} | {config.hostname_local()}")
    print("   ─" * 24)
    print("   ✓ SSH Engine ready")
    print("   ✓ Host-key verification ready")
    print("   ✓ SFTP ready")
    print("   ✓ Profiles ready")
    print(f"   ✓ Logs at {get_log_path()}")
    print()


def confirm(prompt: str, default: bool = False) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        a = input(f"{prompt} {suffix}: ").strip().lower()
        if not a:
            return default
        if a in ("y", "yes"):
            return True
        if a in ("n", "no"):
            return False


def cmd_version(_: argparse.Namespace) -> int:
    banner()
    print(f"tmpssh version: {config.VERSION}")
    print(f"termux: {config.is_termux()}")
    print(f"python: {sys.version.split()[0]}")
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    print("⚙ tmpssh status")
    print(f"  version: {config.VERSION}")
    print(f"  known_hosts: {config.known_hosts_path()}")
    print(f"  data_dir: {config.data_dir()}")
    print(f"  log_file: {get_log_path()}")
    print(f"  termux: {config.is_termux()}")
    pm = ProfileManager()
    print(f"  profiles: {len(pm.list_names())}")
    hkm = HostKeyManager()
    print(f"  known hosts: {len(hkm.list_known())}")
    return 0


def cmd_config(args: argparse.Namespace) -> int:
    s = config.Settings.load()
    if args.set:
        for kv in args.set:
            k, _, v = kv.partition("=")
            if not hasattr(s, k):
                print(f"✗ unknown setting: {k}")
                return 1
            try:
                # type cast by existing attribute
                cur = getattr(s, k)
                cast = type(cur)
                setattr(s, k, cast(v))
            except Exception as e:
                print(f"✗ {k}: {e}")
                return 1
        s.save()
    s = config.Settings.load()
    print(json.dumps(s.to_dict(), indent=2))
    return 0


def cmd_hosts(args: argparse.Namespace) -> int:
    pm = ProfileManager()
    names = pm.list_names()
    if args.raw:
        print(json.dumps(pm.all(), indent=2))
        return 0
    if not names:
        print("⚠ No saved hosts. Use `tmpssh add-host` to add one.")
        return 0
    print(f"{'NAME':<24} {'HOST':<32} {'PORT':<6} {'USER':<16}")
    print("─" * 80)
    for n in names:
        h = pm.get(n)
        print(f"{h.name:<24} {h.hostname:<32} {h.port:<6} {h.username:<16}")
    return 0


def cmd_add_host(_: argparse.Namespace) -> int:
    print("📝 Add SSH host profile (leave blank to abort)")
    try:
        name = input("  Name (e.g. my-server): ").strip()
        if not name:
            print("✗ aborted")
            return 1
        hostname = input("  Hostname / IP: ").strip()
        port = input(f"  Port [{config.DEFAULT_PORT}]: ").strip() or str(config.DEFAULT_PORT)
        username = input("  Username: ").strip()
        key_path = input("  SSH key path (optional, e.g. ~/.ssh/id_ed25519): ").strip()
        label = input("  Label / note (optional): ").strip()
        try:
            host = HostSpec(
                name=name,
                hostname=hostname,
                port=int(port),
                username=username,
                identity_file=key_path or None,
                label=label,
            )
        except ValueError as e:
            print(f"✗ {e}")
            return 1
        pm = ProfileManager()
        pm.add(host.to_dict())
        print(f"✓ Saved profile '{name}'")
        return 0
    except KeyboardInterrupt:
        print("\n✗ aborted")
        return 1


def cmd_remove_host(args: argparse.Namespace) -> int:
    pm = ProfileManager()
    name = args.name
    if pm.get(name) is None:
        print(f"✗ profile '{name}' not found")
        return 1
    if not args.yes and not confirm(f"Remove profile '{name}'?"):
        print("✗ cancelled")
        return 1
    pm.remove(name)
    print(f"✓ removed '{name}'")
    return 0


def _prompt_password(prompt: str) -> str:
    """Prompt without echo. Empty input raises EOFError."""
    return getpass.getpass(prompt)


def _hostkey_ask(host: str, fingerprint: str) -> bool:
    """CLI callback to confirm a new host key."""
    print()
    print("⚠ UNKNOWN SSH HOST")
    print(f"   Host:       {host}")
    print(f"   Fingerprint: {fingerprint}")
    return confirm("   Trust this host?", default=False)


def cmd_connect(args: argparse.Namespace) -> int:
    """Connect to a host and either run a single command or open an interactive shell."""
    user, host, port = parse_user_host(args.target, default_port=args.port)
    port = int(port or config.DEFAULT_PORT)

    if not is_valid_hostname(host):
        print(f"✗ invalid hostname: {host!r}")
        return 1
    if not is_valid_port(port):
        print(f"✗ invalid port: {port}")
        return 1

    key_path = args.key or ""
    if key_path and not is_valid_key_path(key_path):
        print(f"⚠ key not found: {key_path}")
        print("  falling back to password authentication")

    timeout = int(args.timeout or config.DEFAULT_TIMEOUT)
    keepalive = int(args.keepalive or config.DEFAULT_KEEPALIVE)

    cli = SSHClient(host=host, port=port, username=user,
                    key_path=key_path or None,
                    timeout=timeout, keepalive=keepalive)

    print(f"→ connecting to {user}@{host}:{port} ...")
    try:
        cli.connect()
    except TMPSSHError as e:
        if e.kind == SSHErrorKind.HOST_KEY_CHANGED:
            print("🚨 HOST KEY CHANGED — connection blocked.")
            print(e.message)
            return 2
        if e.kind == SSHErrorKind.HOST_KEY_UNKNOWN:
            print("⚠ Unknown host key.")
            print(e.message)
            print()
            if _hostkey_ask(host, e.message):
                HostKeyManager().trust(host, port)
                try:
                    cli.connect()
                except TMPSSHError as e2:
                    print(e2.friendly())
                    return 2
            else:
                print("✗ connection refused (host not trusted)")
                return 2
        else:
            print(e.friendly())
            if e.suggestion:
                print(f"  → {e.suggestion}")
            return 2
    except Exception as e:
        print(f"✗ unexpected error: {e}")
        return 2

    print("✓ Connected")
    secure_log_event(logger, "info", "CLI connected", host=host, port=port, user=user)

    if args.command:
        out, err, rc = cli.execute(args.command, timeout=timeout)
        if out: print(out, end="" if out.endswith("\n") else "\n")
        if err: print(err, end="" if err.endswith("\n") else "\n", file=sys.stderr)
        cli.disconnect()
        return rc

    # Interactive shell
    print(f"   shell: {user}@{host}:{port}  (Ctrl+D to exit, Ctrl+C to interrupt)")
    chan = cli.open_shell(term=os.environ.get("TERM", "xterm-256color"))
    try:
        import select
        import termios
        import tty
        old = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        try:
            while True:
                r, _, _ = select.select([sys.stdin, chan], [], [], 0.5)
                if sys.stdin in r:
                    try:
                        b = os.read(sys.stdin.fileno(), 4096)
                    except OSError:
                        break
                    if not b:
                        break
                    if b == b"\x04":  # Ctrl+D
                        break
                    chan.send(b)
                if chan in r:
                    try:
                        data = chan.recv(65536)
                    except Exception:
                        break
                    if not data:
                        break
                    sys.stdout.write(data.decode(errors="replace"))
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)
    except KeyboardInterrupt:
        pass
    finally:
        cli.disconnect()
        print("\n✓ disconnected")
    return 0


def cmd_sftp(args: argparse.Namespace) -> int:
    """Open an interactive SFTP REPL on the remote."""
    user, host, port = parse_user_host(args.target, default_port=args.port)
    port = int(port or config.DEFAULT_PORT)
    cli = SSHClient(host=host, port=port, username=user,
                    key_path=args.key or None,
                    timeout=int(args.timeout or config.DEFAULT_TIMEOUT))
    try:
        cli.connect()
    except TMPSSHError as e:
        print(e.friendly())
        return 2

    sftp = cli.get_sftp()
    print(f"📁 SFTP on {user}@{host}:{port}")
    print("   commands: ls [path] | cd <path> | get <path> | put <local> <remote> | mkdir <path> | rm <path> | rename <old> <new> | exit")
    cwd = args.path or "/"
    try:
        while True:
            try:
                line = input(f"sftp:{cwd}> ").strip()
            except EOFError:
                break
            if not line:
                continue
            parts = line.split()
            cmd = parts[0]
            args_ = parts[1:]
            try:
                if cmd in ("exit", "quit"):
                    break
                if cmd == "ls":
                    p = args_[0] if args_ else cwd
                    for it in sftp.list(p):
                        print(it)
                elif cmd == "cd":
                    cwd = args_[0]
                    sftp.list(cwd)
                elif cmd == "get":
                    remote = args_[0]
                    local = args_[1] if len(args_) > 1 else os.path.basename(remote)
                    sftp.download(remote, open(local, "wb"))
                    print(f"✓ saved {local}")
                elif cmd == "put":
                    local, remote = args_[0], args_[1]
                    sftp.upload(open(local, "rb"), remote)
                    print(f"✓ uploaded {remote}")
                elif cmd == "mkdir":
                    sftp.mkdir(args_[0]); print("✓ ok")
                elif cmd == "rm":
                    if not confirm(f"Delete {args_[0]}?"): continue
                    sftp.delete(args_[0]); print("✓ ok")
                elif cmd == "rename":
                    sftp.rename(args_[0], args_[1]); print("✓ ok")
                elif cmd == "pwd":
                    print(cwd)
                elif cmd == "help":
                    print("   ls [path] | cd <path> | get <path> [local] | put <local> <remote> | mkdir <path> | rm <path> | rename <old> <new> | exit")
                else:
                    print(f"✗ unknown: {cmd}")
            except TMPSSHError as e:
                print(e.friendly())
    except KeyboardInterrupt:
        pass
    finally:
        cli.disconnect()
        print("✓ disconnected")
    return 0


def cmd_web(args: argparse.Namespace) -> int:
    print(f"→ starting web GUI on http://{args.host}:{args.port}")
    from app import run
    run(args.host, args.port, debug=args.debug)
    return 0


def main(argv=None) -> int:
    banner()
    p = argparse.ArgumentParser(prog="tmpssh", add_help=False)
    sub = p.add_subparsers(dest="cmd")

    p_conn = sub.add_parser("connect"); p_conn.add_argument("target", help="user@host[:port]")
    p_conn.add_argument("-p", "--port", default=None); p_conn.add_argument("-k", "--key", default="")
    p_conn.add_argument("-t", "--timeout", default=None); p_conn.add_argument("--keepalive", default=None)
    p_conn.add_argument("-c", "--command", default="", help="run a single command and exit")
    p_conn.set_defaults(func=cmd_connect)

    p_hosts = sub.add_parser("hosts"); p_hosts.add_argument("--raw", action="store_true")
    p_hosts.set_defaults(func=cmd_hosts)

    p_add = sub.add_parser("add-host"); p_add.set_defaults(func=cmd_add_host)

    p_rm = sub.add_parser("remove-host"); p_rm.add_argument("name"); p_rm.add_argument("-y", "--yes", action="store_true")
    p_rm.set_defaults(func=cmd_remove_host)

    p_sftp = sub.add_parser("sftp"); p_sftp.add_argument("target"); p_sftp.add_argument("-p", "--port", default=None)
    p_sftp.add_argument("-k", "--key", default=""); p_sftp.add_argument("-t", "--timeout", default=None)
    p_sftp.add_argument("--path", default="/")
    p_sftp.set_defaults(func=cmd_sftp)

    p_status = sub.add_parser("status"); p_status.set_defaults(func=cmd_status)

    p_cfg = sub.add_parser("config"); p_cfg.add_argument("--set", nargs="*", default=[],
        help="key=value pairs, e.g. --set timeout=15")
    p_cfg.set_defaults(func=cmd_config)

    p_web = sub.add_parser("web"); p_web.add_argument("--host", default="127.0.0.1")
    p_web.add_argument("--port", type=int, default=5000); p_web.add_argument("--debug", action="store_true")
    p_web.set_defaults(func=cmd_web)

    p_ver = sub.add_parser("version"); p_ver.set_defaults(func=cmd_version)
    p_help = sub.add_parser("help"); p_help.set_defaults(func=lambda a: p.print_help())

    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] in ("help", "-h", "--help"):
        p.print_help()
        return 0
    args = p.parse_args(argv)
    if not hasattr(args, "func"):
        p.print_help(); return 0
    return int(args.func(args) or 0)


if __name__ == "__main__":
    sys.exit(main())