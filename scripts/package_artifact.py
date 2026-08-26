#!/usr/bin/env python3
"""Package the built binary into the platform-specific release artifact.

Usage: package_artifact.py <type>
  type = windows | macos | linux
Produces the artifact(s) under dist/.

All platforms ship a portable single-file binary:
  - windows -> netconnect-windows-x86_64.zip  (contains netconnect.exe)
  - macos   -> netconnect-macos-x86_64         (extensionless portable)
  - linux   -> netconnect-linux-x86_64         (extensionless portable)
"""
import sys
import shutil
import zipfile
from pathlib import Path

DIST = Path("dist")

NAMES = {
    "windows": "netconnect-windows-x86_64.zip",
    "macos": "netconnect-macos-x86_64",
    "linux": "netconnect-linux-x86_64",
}


def main():
    if len(sys.argv) != 2:
        print("Usage: package_artifact.py <windows|macos|linux>")
        sys.exit(1)
    t = sys.argv[1]
    if t not in NAMES:
        raise SystemExit(f"unknown type: {t}")

    exe = DIST / "netconnect.exe" if (DIST / "netconnect.exe").exists() else DIST / "netconnect"
    if not exe.exists():
        raise SystemExit(f"binary not found: {exe}")

    out = DIST / NAMES[t]
    if t == "windows":
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(exe, "netconnect.exe")
    else:
        shutil.move(str(exe), str(out))
    print(f"PKG={out.name}")


if __name__ == "__main__":
    main()
