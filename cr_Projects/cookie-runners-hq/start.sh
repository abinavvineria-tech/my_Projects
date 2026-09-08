#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
export $(grep -v '^#' .env 2>/dev/null | xargs) || true
mkdir -p data logs
python3 -m flask --app backend/app:app run --host=0.0.0.0 --port=${FLASK_PORT:-5000}
