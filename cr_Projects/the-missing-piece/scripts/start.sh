#!/usr/bin/env bash
# start.sh - Start The Missing Piece server
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/backend"
if [ ! -d "node_modules" ]; then
  echo "Installing backend dependencies..."
  npm install --silent
fi
node server.js
