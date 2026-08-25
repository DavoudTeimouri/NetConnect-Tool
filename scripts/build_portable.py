#!/usr/bin/env python3
"""Build script for portable NetConnect executables using PyInstaller."""

import sys
import os
import subprocess
import platform
import shutil
from pathlib import Path

# Force UTF-8 output on Windows (cp1252 can't encode checkmarks)
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def run_cmd(cmd, cwd=None, check=True):
    """Run command and return result, streaming output live."""
    print(f"Running: {' '.join(cmd)}")
    # Stream live to avoid pipe deadlock on Windows (PyInstaller subprocess)
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def main():
    """Build portable executables."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"

    # Clean previous builds
    for d in [dist_dir, build_dir]:
        if d.exists():
            shutil.rmtree(d)

    # PyInstaller options
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--clean",
        "--noconfirm",
        "--name", "netconnect",
        "--console",
        # Hidden imports for runtime
        "--hidden-import", "yaml",
        "--hidden-import", "platformdirs",
        "--hidden-import", "tabulate",
        # Entry point
        str(src_dir / "netconnect" / "cli.py"),
    ]

    # --strip only works on Unix (no strip.exe on Windows)
    system = platform.system().lower()
    if system != "windows":
        pyinstaller_args.append("--strip")

    if system == "windows":
        icon_path = project_root / "packaging" / "windows" / "icon.ico"
        if icon_path.exists():
            pyinstaller_args.extend(["--icon", str(icon_path)])
    elif system == "darwin":
        pyinstaller_args.extend([
            "--osx-bundle-identifier", "com.netconnect.tool",
        ])

    print(f"Building for {system} ({platform.machine()})...")
    run_cmd(pyinstaller_args, cwd=project_root)

    # Find built executable
    exe_name = "netconnect.exe" if system == "windows" else "netconnect"
    exe_path = dist_dir / exe_name

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n[OK] Built successfully: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB")

        # Test the executable
        print("\nTesting executable...")
        test_result = run_cmd([str(exe_path), "--version"], check=False)
        if test_result.returncode == 0:
            print("[OK] Version test passed")
        else:
            print("[FAIL] Version test failed")
    else:
        print(f"\n[FAIL] Executable not found at {exe_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
