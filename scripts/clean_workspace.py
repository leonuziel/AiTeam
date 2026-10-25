#!/usr/bin/env python3
"""
Workspace Hygiene & Garbage Collector
Cleans temporary scratch files, compiler caches, and stale agent artifacts.
"""
import sys
import shutil
from pathlib import Path
import argparse

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

TEMP_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.tmp",
    "*~",
    ".coverage",
    ".coverage.*",
    "coverage.xml",
    ".DS_Store",
    "Thumbs.db",
]

TEMP_DIRS = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
    "*.egg-info",
    "htmlcov",
]

def clean_workspace(dry_run=False, clean_checkpoints=False, verbose=False):
    repo_root = Path(__file__).resolve().parent.parent
    print(f"🧹 Running Workspace Hygiene & Garbage Collector on '{repo_root.name}'...")
    if dry_run:
        print("  ℹ️  [DRY-RUN MODE] No files will be permanently deleted.")

    deleted_files = 0
    deleted_dirs = 0
    bytes_freed = 0

    # 1. Clean matching files
    for pattern in TEMP_PATTERNS:
        for file_path in repo_root.rglob(pattern):
            # Never touch .git
            if ".git" in file_path.parts:
                continue
            try:
                size = file_path.stat().st_size
                if not dry_run:
                    file_path.unlink()
                deleted_files += 1
                bytes_freed += size
                if verbose:
                    print(f"  🗑️  Removed file: {file_path.relative_to(repo_root)} ({size} bytes)")
            except Exception as e:
                if verbose:
                    print(f"  ⚠️  Could not remove {file_path}: {e}")

    # 2. Clean matching directories
    for dir_pattern in TEMP_DIRS:
        for dir_path in repo_root.rglob(dir_pattern):
            if ".git" in dir_path.parts:
                continue
            if dir_path.is_dir():
                try:
                    dir_size = sum(f.stat().st_size for f in dir_path.rglob("*") if f.is_file())
                    if not dry_run:
                        shutil.rmtree(dir_path, ignore_errors=True)
                    deleted_dirs += 1
                    bytes_freed += dir_size
                    if verbose:
                        print(f"  📁 Removed dir: {dir_path.relative_to(repo_root)} ({dir_size} bytes)")
                except Exception as e:
                    if verbose:
                        print(f"  ⚠️  Could not remove {dir_path}: {e}")

    # 3. Optional: Clean older checkpoints (keep last 5)
    checkpoints_dir = repo_root / ".agent" / "checkpoints"
    if clean_checkpoints and checkpoints_dir.exists():
        metadata_files = sorted(checkpoints_dir.glob("checkpoint_*.json"))
        if len(metadata_files) > 5:
            stale_files = metadata_files[:-5]
            for mf in stale_files:
                archive_name = mf.stem.replace("checkpoint_", "state_") + ".tar.gz"
                af = checkpoints_dir / archive_name
                try:
                    if mf.exists():
                        bytes_freed += mf.stat().st_size
                        if not dry_run:
                            mf.unlink()
                        deleted_files += 1
                    if af.exists():
                        bytes_freed += af.stat().st_size
                        if not dry_run:
                            af.unlink()
                        deleted_files += 1
                    if verbose:
                        print(f"  🗄️  Pruned stale checkpoint: {mf.name}")
                except Exception as e:
                    if verbose:
                        print(f"  ⚠️  Could not prune checkpoint {mf}: {e}")

    mb_freed = bytes_freed / (1024 * 1024)
    status_prefix = "[DRY-RUN] Would clean" if dry_run else "Cleaned"
    print(f"✨ {status_prefix} {deleted_files} temporary file(s) and {deleted_dirs} cache directory(ies).")
    print(f"💾 Total space reclaimed: {bytes_freed:,} bytes ({mb_freed:.2f} MB).")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Workspace hygiene and temporary cache garbage collector")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview deletions without deleting")
    parser.add_argument("--clean-checkpoints", action="store_true", help="Prune older checkpoints (retain last 5)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print each deleted file and directory")
    args = parser.parse_args()

    sys.exit(clean_workspace(dry_run=args.dry_run, clean_checkpoints=args.clean_checkpoints, verbose=args.verbose))

if __name__ == "__main__":
    main()
