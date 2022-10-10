#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/Kodiak.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/Kodiak.dmg" && rm "dist/Kodiak.dmg"
create-dmg \
  --volname "Kodiak" \
  --volicon "kodiak.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Kodiak.app" 175 120 \
  --hide-extension "Kodiak.app" \
  --app-drop-link 425 120 \
  "dist/Kodiak.dmg" \
  "dist/dmg/"