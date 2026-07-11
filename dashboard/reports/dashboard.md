# ZORTEX SCORE 7T ROM Dashboard

Generated: `2026-07-11T03:45:25.844980+00:00`

## Decision

BLOCKED: dashboard analysis does not authorize firmware deployment.

## Metrics

- Reference components: 15
- Verified target components: 0
- Missing or unverified: 15
- Public source repositories: 6

## User-installable applications

- `app.lawnchair`
- `de.szalkowski.activitylauncher`

## Privileged, framework, vendor or boot components

- `com.android.launcher3`
- `com.android.localtransport`
- `com.android.packageinstaller`
- `com.android.permissioncontroller`
- `com.android.providers.settings`
- `com.android.providers.telephony`
- `com.android.systemui`
- `com.topjohnwu.magisk`
- `lineageos.platform`
- `me.phh.treble.app`
- `org.lineageos.customization`
- `org.lineageos.lineageparts`
- `org.lineageos.lineagesettings`

## Missing or unverified on target

- `app.lawnchair`
- `com.android.launcher3`
- `com.android.localtransport`
- `com.android.packageinstaller`
- `com.android.permissioncontroller`
- `com.android.providers.settings`
- `com.android.providers.telephony`
- `com.android.systemui`
- `com.topjohnwu.magisk`
- `de.szalkowski.activitylauncher`
- `lineageos.platform`
- `me.phh.treble.app`
- `org.lineageos.customization`
- `org.lineageos.lineageparts`
- `org.lineageos.lineagesettings`

## Platform mismatches

- No confirmed mismatch; unresolved fields remain.

## Interpretation

Package names alone do not recreate a ROM.
System components require matching framework, vendor, kernel,
device-tree, partition and verified-boot architecture.
