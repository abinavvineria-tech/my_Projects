#!/usr/bin/env bash
set -euo pipefail
echo "Starting CookieRunners: Update Nexus (CRUN)..."
python -m app || echo "Dashboard requires web server; try: python -m http.server --directory web 8080"
