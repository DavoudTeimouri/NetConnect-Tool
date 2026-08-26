#!/usr/bin/env python3
"""Build a .deb package from the already-built portable binary.

Usage: build_deb.py <binary_path> <output_deb_path>
"""
import sys
import os
import shutil
import subprocess
from pathlib import Path

PKG_NAME = "netconnect"
VERSION = "2.0.0"
MAINTAINER = "Davoud Teimouri <davoud.teimouri@gmail.com>"
ARCH = "amd64"


def build_deb(binary_path: str, output_deb: str):
    binary = Path(binary_path)
    if not binary.exists():
        raise SystemExit(f"Binary not found: {binary}")

    staging = Path("deb_staging")
    if staging.exists():
        shutil.rmtree(staging)

    bin_dir = staging / "usr" / "bin"
    bin_dir.mkdir(parents=True)
    shutil.copy(binary, bin_dir / "netconnect")
    os.chmod(bin_dir / "netconnect", 0o755)

    doc_dir = staging / "usr" / "share" / "doc" / PKG_NAME
    doc_dir.mkdir(parents=True)
    (doc_dir / "copyright").write_text(
        "netconnect\nCopyright (c) Davoud Teimouri\nLicensed under the MIT License.\n"
    )

    control_dir = staging / "DEBIAN"
    control_dir.mkdir()
    control = (
        f"Package: {PKG_NAME}\n"
        f"Version: {VERSION}\n"
        f"Section: net\n"
        f"Priority: optional\n"
        f"Architecture: {ARCH}\n"
        f"Maintainer: {MAINTAINER}\n"
        f"Description: NetConnect - cross-platform network connectivity testing tool\n"
        f" Listen on TCP/UDP ports, test connections to IP ranges, and measure\n"
        f" latency. Single-file portable executable built with PyInstaller.\n"
    )
    (control_dir / "control").write_text(control)

    subprocess.run(["dpkg-deb", "--build", str(staging), output_deb], check=True)
    print(f"Built deb: {output_deb}")
    shutil.rmtree(staging)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: build_deb.py <binary_path> <output_deb_path>")
        sys.exit(1)
    build_deb(sys.argv[1], sys.argv[2])
