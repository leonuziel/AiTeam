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

import shutil

def install_hooks():
    hooks_dir = Path(".githooks")
    if not hooks_dir.exists():
        print("❌ Error: '.githooks' directory does not exist.")
        sys.exit(1)

    print("🔧 Installing Doc-to-Code Git pre-commit hooks...")
    
    # 1. Configure git core.hooksPath
    try:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True)
        print("✅ Configured git 'core.hooksPath' to '.githooks'.")
    except Exception as e:
        print(f"⚠️  Could not set core.hooksPath via git config: {e}")

    # 2. Also copy directly to .git/hooks/pre-commit if .git/hooks exists
    git_hooks_dir = Path(".git/hooks")
    if git_hooks_dir.exists():
        src_hook = hooks_dir / "pre-commit"
        dest_hook = git_hooks_dir / "pre-commit"
        if src_hook.exists():
            shutil.copy2(src_hook, dest_hook)
            try:
                dest_hook.chmod(0o755)
            except Exception:
                pass
            print("✅ Copied pre-commit hook directly to '.git/hooks/pre-commit'.")

    print("✨ Pre-commit compliance hooks successfully activated!")

if __name__ == "__main__":
    install_hooks()

