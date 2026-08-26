#!/usr/bin/env python3
"""Package the built binary into the platform-specific release artifact.

Usage: package_artifact.py <type>
  type = zip | bin | deb
Produces the artifact(s) under dist/.
"""
import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path

DIST = Path("dist")


def main():
    if len(sys.argv) != 2:
        print("Usage: package_artifact.py <zip|bin|deb>")
        sys.exit(1)
    t = sys.argv[1]

    exe = DIST / "netconnect.exe" if (DIST / "netconnect.exe").exists() else DIST / "netconnect"
    if not exe.exists():
        raise SystemExit(f"binary not found: {exe}")

    if t == "zip":
        out = DIST / "netconnect-windows-x86_64.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(exe, "netconnect.exe")
        print(f"PKG={out.name}")

    elif t == "bin":
        out = DIST / "netconnect-macos-x86_64.bin"
        shutil.move(str(exe), str(out))
        print(f"PKG={out.name}")

    elif t == "deb":
        bin_out = DIST / "netconnect-linux-x86_64.bin"
        shutil.copy(str(exe), str(bin_out))
        deb_out = DIST / "netconnect-linux-x86_64.deb"
        subprocess.run([sys.executable, "scripts/build_deb.py", str(exe), str(deb_out)], check=True)
        print(f"PKG={deb_out.name}")

    else:
        raise SystemExit(f"unknown type: {t}")


if __name__ == "__main__":
    main()
