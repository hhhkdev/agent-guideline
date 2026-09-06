#!/bin/bash
# ==============================================================================
# Agent Hub 2.0 All-In-One Unified Launcher
# 1. Background Control Server (Port 8765)
# 2. Native macOS Menu Bar Token Monitor (⚡ C:% G:% O:%)
# 3. Standalone Desktop App Window (Custom Icon & Dedicated Process)
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_PATH="${DIR}/tools/Agent Hub.app"

echo "=================================================="
echo "🚀 Agent Hub 2.0 올인원 원클릭 실행 (All-in-One)"
echo "=================================================="

# Check & build app bundle if not yet built
if [ ! -d "${APP_PATH}" ]; then
    echo "📦 Initializing macOS App bundle..."
    "${DIR}/tools/create-macos-app.sh" > /dev/null 2>&1
fi

echo "1️⃣  백그라운드 컨트롤 서버 가동..."
echo "2️⃣  맥북 상단 상태바 토큰 모니터 등록..."
echo "3️⃣  독립 데스크톱 앱 창 구동..."

# Open macOS Application Bundle (handles server + menubar + window all together)
open "${APP_PATH}"

echo "=================================================="
echo "✨ 실행 완료!"
echo "• 맥북 상단 메뉴바: ⚡ C:% G:% O:% 실시간 표시"
echo "• 화면: Agent Hub 2.0 데스크톱 앱 창 오픈"
echo "=================================================="
