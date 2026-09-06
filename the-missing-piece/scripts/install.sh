#!/bin/bash
# 🧩 The Missing Piece SSH — install (Termux-safe)
echo "🧩 THE MISSING PIECE SSH — install"
echo "Detecting Termux..."
if [ -n "$PREFIX" ] || [ -f "/data/data/com.termux/files/usr/bin/python" ]; then
    echo "  ✓ Termux detected"
else
    echo "  ⚠ Not Termux — continuing anyway"
fi
python3 --version || { echo "✗ python3 required"; exit 1; }
# Create venv with system-site-packages to reuse Termux cryptography
if [ ! -d ".venv" ]; then
    python3 -m venv .venv --system-site-packages
fi
source .venv/bin/activate
pip install -q -r requirements.txt --no-build-isolation 2>/dev/null || pip install -q paramiko flask flask-cors python-dotenv --no-build-isolation
mkdir -p data templates static/css static/js static/icons scripts tests
chmod +x cli.py
cp cli.py tmpssh 2>/dev/null || echo '#!/usr/bin/env python3\nexec(open("cli.py").read())' > tmpssh && chmod +x tmpssh
echo "✅ Installed. Use: python cli.py  |  python -m cli  |  tmpssh  |  python app.py"
echo "   Web:  python -c \"from app import run; run()\""
echo "   URL:  http://127.0.0.1:5000"
