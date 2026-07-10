# ZORTEX ROM Knowledge Database

ZORTEX v0.8 compares a working SCORE 7T reference architecture with the target
tablet profile.

The comparison distinguishes:

1. User-installable applications
2. Privileged Android applications
3. Framework components
4. Boot components
5. Vendor-dependent components

A package name visible on a working tablet does not prove that the same APK can
be installed independently. SystemUI, PermissionController, PackageInstaller,
SettingsProvider, PHH integration, and Lineage framework components depend on
the complete ROM architecture.

## Commands

```bash
python scripts/rom_knowledge.py build-profiles
python scripts/rom_knowledge.py sources
python scripts/rom_knowledge.py compare
python scripts/rom_knowledge.py report
python scripts/rom_knowledge.py deploy-checkMD
