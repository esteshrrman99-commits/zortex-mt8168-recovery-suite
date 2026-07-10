# ZORTEX SCORE 7T Reference Stack Laboratory

This module models the open-source architecture visible on a reference SCORE 7T.

It does not copy APKs, vendor blobs, cryptographic keys, or proprietary firmware.

## Important distinction

Ordinary applications:
- Lawnchair
- Activity Launcher

ROM/system components:
- LineageOS Settings and framework
- PHH/TrebleDroid integration
- SystemUI
- PackageInstaller
- PermissionController
- SettingsProvider
- TelephonyProvider
- Trebuchet system integration
- Magisk boot integration

The complete reference result requires a board-compatible Android system image,
vendor implementation, kernel/device tree, verified boot arrangement, and an
authorized installation path. Installing the visible APK names alone cannot
reproduce the reference tablet.
