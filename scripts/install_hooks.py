#!/usr/bin/env python3
"""
Git Pre-Commit Hook Installer
Configures Git to use the repository's version-controlled .githooks directory.
"""
import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def install_hooks():
    hooks_dir = Path(".githooks")
    if not hooks_dir.exists():
        print("❌ Error: '.githooks' directory does not exist.")
        sys.exit(1)

    print("🔧 Installing Doc-to-Code Git pre-commit hooks...")
    try:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True)
        print("✅ Configured git 'core.hooksPath' to '.githooks'.")
        print("✨ Pre-commit compliance hooks successfully activated!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to configure git hooks: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_hooks()
