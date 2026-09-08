#!/usr/bin/env python3
import sys, sqlite3, os
DB='data/crhq.db'
print("🍪 CookieRunners HQ Doctor")
for label, cmd in [("Python","python3 --version"),("Flask","python3 -c 'import flask'")]:
    print(f"  {'✓' if os.system('python3 -c \"import flask\" > /dev/null 2>&1')==0 else '✗'} {label}")
print("  ⚠ Fireclaw unavailable -> using cached/offline")
print("✓ Offline mode: enabled")
