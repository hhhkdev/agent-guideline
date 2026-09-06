#!/bin/bash
# ==============================================================================
# Builds a standalone macOS .app bundle "Agent Hub.app"
# With custom AgentHub.icns icon, native desktop wrapper, and status bar monitor
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_NAME="Agent Hub.app"
APP_DIR="${DIR}/${APP_NAME}"
CONTENTS="${APP_DIR}/Contents"
MACOS="${CONTENTS}/MacOS"
RESOURCES="${CONTENTS}/Resources"

echo "📦 Creating macOS Application Bundle: ${APP_DIR}..."
rm -rf "${APP_DIR}"
mkdir -p "${MACOS}"
mkdir -p "${RESOURCES}"

# Copy custom ICNS icon
cp "${DIR}/assets/AgentHub.icns" "${RESOURCES}/AppIcon.icns"

# Create Info.plist
cat << 'PLIST' > "${CONTENTS}/Info.plist"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>AgentHub</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.hhhk.agenthub</string>
    <key>CFBundleName</key>
    <string>Agent Hub</string>
    <key>CFBundleDisplayName</key>
    <string>Agent Hub</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>12.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
PLIST

# Create Executable Launcher Script
cat << 'LAUNCHER' > "${MACOS}/AgentHub"
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." >/dev/null 2>&1 && pwd )"
PORT=8765
URL="http://127.0.0.1:${PORT}"

# 1. Start Server if not running
if ! lsof -i :${PORT} > /dev/null 2>&1; then
    python3 "${DIR}/tools/agent-hub/server.py" > /tmp/agent-hub-server.log 2>&1 &
    sleep 0.8
fi

# 2. Start Status Bar Monitor if not running
if ! pgrep -f "agent-hub-menubar" > /dev/null 2>&1; then
    "${DIR}/tools/status-bar/agent-hub-menubar" > /dev/null 2>&1 &
fi

# 3. Launch App Window with custom title
if [ -d "/Applications/Google Chrome.app" ]; then
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      --app="${URL}" \
      --window-size=1440,920 \
      --user-data-dir="/tmp/agent-hub-app-profile" \
      --no-first-run \
      --no-default-browser-check > /dev/null 2>&1 &
elif [ -d "/Applications/Brave Browser.app" ]; then
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
      --app="${URL}" \
      --window-size=1440,920 \
      --user-data-dir="/tmp/agent-hub-app-profile" > /dev/null 2>&1 &
else
    open "${URL}"
fi
LAUNCHER

chmod +x "${MACOS}/AgentHub"

echo "🎉 Successfully built 'Agent Hub.app' with custom icon and status bar integration!"
