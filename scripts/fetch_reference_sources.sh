#!/usr/bin/env bash
set -euo pipefail

DEST="reference-stack/sources"
mkdir -p "$DEST"

clone() {
  local name="$1"
  local url="$2"

  if [ -d "$DEST/$name/.git" ]; then
    echo "Already present: $name"
  else
    git clone --depth 1 "$url" "$DEST/$name"
  fi
}

clone activity-launcher https://github.com/ActivityLauncher/ActivityLauncher.git
clone lawnchair https://github.com/LawnchairLauncher/lawnchair.git
clone lineage-settings https://github.com/LineageOS/android_packages_apps_Settings.git
clone lineage-trebuchet https://github.com/LineageOS/android_packages_apps_Trebuchet.git
clone lineage-theme-picker https://github.com/LineageOS/android_packages_apps_ThemePicker.git
clone magisk https://github.com/topjohnwu/Magisk.git

echo
echo "Source references fetched."
echo "TrebleDroid is cataloged separately because it spans multiple repositories."
