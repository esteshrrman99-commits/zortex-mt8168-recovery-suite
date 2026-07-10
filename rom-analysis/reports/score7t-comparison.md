# ZORTEX SCORE 7T ROM Comparison

- Reference profile: `score7t-working-reference`
- Target profile: `score7t-locked-target`
- Deployment authorized: `False`

## Decision

BLOCKED: comparison evidence does not authorize firmware deployment.

## Matching packages

- None recorded

## Missing from target

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

## Extra on target

- None

## Platform mismatches

- No confirmed mismatch; unresolved fields may remain.

## Interpretation

Missing ROM-level packages cannot be reproduced by copying APKs.
They require a compatible system image, framework, vendor layer,
kernel, partition layout, and authorized installation route.
