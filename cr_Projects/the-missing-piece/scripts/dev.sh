#!/usr/bin/env bash
# dev.sh - Development mode - start server with file watching
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/backend"

echo "🧩 Starting The Missing Piece in DEV mode..."
echo "   Watching for changes in ../data/ and ./routes/"

# Install deps if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install --silent
fi

# Start server with nodemon if available, else node
if command -v nodemon &>/dev/null; then
  nodemon --watch ../data --watch ./routes server.js
else
  echo "nodemon not installed, using node"
  node server.js
fi