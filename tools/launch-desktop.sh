#!/bin/bash
# ==============================================================================
# Agent Hub 2.0 Native macOS Desktop App Launcher
# Launches local Python server in background and opens an isolated Chrome App window
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PORT=8765
URL="http://127.0.0.1:${PORT}"

echo "🚀 Starting Agent Hub Control Server..."
# Check if server is already running
if ! lsof -i :${PORT} > /dev/null 2>&1; then
    python3 "${DIR}/agent-hub/server.py" > /tmp/agent-hub.log 2>&1 &
    sleep 0.8
fi

echo "🖥️  Launching Native App Window..."
# Open in Google Chrome App Mode (borderless, no URL bar, standalone window)
if [ -d "/Applications/Google Chrome.app" ]; then
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --app="${URL}" --window-size=1440,900 --user-data-dir="/tmp/agent-hub-chrome-profile" > /dev/null 2>&1 &
elif [ -d "/Applications/Brave Browser.app" ]; then
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" --app="${URL}" --window-size=1440,900 > /dev/null 2>&1 &
else
    # Fallback to default browser
    open "${URL}"
fi

echo "✨ Agent Hub 2.0 is now running as a desktop app!"
