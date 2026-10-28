#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
APP="build/大水桌宠.app"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
swiftc -O -target arm64-apple-macosx14.0 -framework AppKit -framework AVFoundation Sources/main.swift Sources/SharedDance.swift -o "$APP/Contents/MacOS/DashuiPet"
cp -R Assets/. "$APP/Contents/Resources/"
cp LICENSE-GoodThing "$APP/Contents/Resources/"
cp LICENSE-SunPet "$APP/Contents/Resources/"
cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleExecutable</key><string>DashuiPet</string>
<key>CFBundleIdentifier</key><string>local.dashui.desktop-pet</string>
<key>CFBundleName</key><string>大水桌宠</string>
<key>CFBundleDisplayName</key><string>大水桌宠</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleShortVersionString</key><string>1.2</string>
<key>CFBundleVersion</key><string>2</string>
<key>LSMinimumSystemVersion</key><string>14.0</string>
<key>LSUIElement</key><true/>
<key>NSHighResolutionCapable</key><true/>
<key>CFBundleIconFile</key><string>AppIcon</string>
</dict></plist>
PLIST
codesign --force --sign - "$APP"
printf '已构建：%s\n' "$APP"
