#!/usr/bin/env bash
# shutdown.sh - Shutdown The Missing Piece server gracefully
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.server.pid"

if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    echo "Gracefully shutting down (PID $PID)..."
    kill -SIGTERM "$PID"
    sleep 2
    # Force kill if still running
    if kill -0 "$PID" 2>/dev/null; then
      echo "Force killing..."
      kill -9 "$PID" 2>/dev/null
    fi
  fi
  rm -f "$PID_FILE"
  echo "Server stopped"
else
  # Try to find any node server process
  PID=$(pgrep -f "node server.js")
  if [ -n "$PID" ]; then
    echo "Gracefully shutting down (PID $PID)..."
    kill -SIGTERM "$PID"
    sleep 2
    if kill -0 "$PID" 2>/dev/null; then
      kill -9 "$PID" 2>/dev/null
    fi
    rm -f "$PID_FILE"
    echo "Server stopped"
  else
    echo "No server process found"
  fi
fi