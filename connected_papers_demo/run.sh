#!/bin/bash

# Connected Papers Demo - Quick Start Script

echo "🚀 Starting Connected Papers Demo..."
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Installing Flask..."
    python3 -m pip install -q Flask
    echo "✅ Flask installed successfully!"
    echo ""
fi

# Navigate to the demo directory
cd "$(dirname "$0")"

echo "🌐 Starting server..."
echo ""
echo "============================================================"
echo "  Open your browser to: http://127.0.0.1:5001"
echo "============================================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
python3 server.py
