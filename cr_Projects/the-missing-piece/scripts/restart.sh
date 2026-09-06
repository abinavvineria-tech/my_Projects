#!/usr/bin/env bash
# restart.sh - Restart The Missing Piece server
bash "$(dirname "$0")/stop.sh"
sleep 1
bash "$(dirname "$0")/start.sh"