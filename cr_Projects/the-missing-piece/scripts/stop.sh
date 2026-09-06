#!/usr/bin/env bash
# stop.sh - Stop The Missing Piece server
PID=$(pgrep -f "node server.js" | head -1)
if [ -z "$PID" ]; then
  echo "Server not running"
else
  kill "$PID"
  echo "Stopped (PID $PID)"
fi