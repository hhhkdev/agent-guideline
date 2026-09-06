#!/bin/bash
# Generate high-res ICNS icon for Agent Hub 2.0
ICONSET_DIR="/tmp/AgentHub.iconset"
mkdir -p "$ICONSET_DIR"

# Generate 512x512 PNG using Python PIL or Swift/sips
python3 - << 'PYEOF'
import os
from PIL import Image, ImageDraw, ImageFont

# 512x512 canvas
img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Rounded rectangle gradient-like background
margin = 24
draw.rounded_rectangle([margin, margin, 512 - margin, 512 - margin], radius=110, fill=(24, 18, 48, 255), outline=(99, 102, 241, 200), width=8)

# Glowing inner circle
draw.ellipse([100, 100, 412, 412], fill=(49, 46, 129, 255), outline=(129, 140, 248, 255), width=6)

# Text or Symbol
# Draw lightning and text
draw.text((156, 170), "AH", fill=(255, 255, 255, 255), font_size=180)
draw.text((160, 360), "AGENT HUB", fill=(165, 180, 252, 255), font_size=32)

img.save("/tmp/AgentHub_512.png")
PYEOF

if [ -f "/tmp/AgentHub_512.png" ]; then
    sips -z 16 16     /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_16x16.png" > /dev/null
    sips -z 32 32     /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_16x16@2x.png" > /dev/null
    sips -z 32 32     /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_32x32.png" > /dev/null
    sips -z 64 64     /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_32x32@2x.png" > /dev/null
    sips -z 128 128   /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_128x128.png" > /dev/null
    sips -z 256 256   /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_128x128@2x.png" > /dev/null
    sips -z 256 256   /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_256x256.png" > /dev/null
    sips -z 512 512   /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_256x256@2x.png" > /dev/null
    sips -z 512 512   /tmp/AgentHub_512.png --out "${ICONSET_DIR}/icon_512x512.png" > /dev/null

    mkdir -p "/Users/hhhk/dev/agent-guideline/tools/assets"
    iconutil -c icns "$ICONSET_DIR" -o "/Users/hhhk/dev/agent-guideline/tools/assets/AgentHub.icns"
    cp /tmp/AgentHub_512.png "/Users/hhhk/dev/agent-guideline/tools/assets/AgentHub.png"
    echo "✓ App icon successfully generated at tools/assets/AgentHub.icns"
fi
