#!/usr/bin/env python3
"""
Autonomous Rollback & State Checkpoint Manager
Creates lightweight, deterministic repository checkpoints prior to cascading agent turns.
Allows one-command atomic rollback if downstream agent edits fail invariant or audit gates.
"""
import sys
import os
import subprocess
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CHECKPOINTS_DIR = Path(".agent/checkpoints")

def run_git(args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

def create_checkpoint(name: str, description: str = "") -> Optional[str]:
    """Creates a local Git checkpoint ref and records metadata."""
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    checkpoint_id = f"ckpt_{timestamp}_{clean_name}"

    # Get git status and diff stats
    status_res = run_git(["status", "--porcelain"])
    modified_files = [line.strip().split()[-1] for line in status_res.stdout.splitlines() if line.strip()]

    head_res = run_git(["rev-parse", "HEAD"])
    head_commit = head_res.stdout.strip() if head_res.returncode == 0 else "UNKNOWN"

    # Create stash with message containing checkpoint_id
    stash_msg = f"[AGENT-CHECKPOINT] {checkpoint_id}: {name}"
    run_git(["stash", "push", "--include-untracked", "-m", stash_msg])
    
    # Immediately apply stash back so working tree remains intact, but stash is saved!
    run_git(["stash", "apply", "--quiet"])

    metadata = {
        "id": checkpoint_id,
        "name": name,
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "head_commit": head_commit,
        "modified_files": modified_files,
        "stash_message": stash_msg
    }

    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    meta_file = CHECKPOINTS_DIR / f"{checkpoint_id}.json"
    meta_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"🔒 Checkpoint '{checkpoint_id}' successfully created ({len(modified_files)} file(s) tracked).")
    return checkpoint_id

def list_checkpoints() -> List[Dict]:
    """Lists all available checkpoints."""
    if not CHECKPOINTS_DIR.exists():
        print("ℹ️ No checkpoints found.")
        return []

    checkpoints = []
    for f in sorted(CHECKPOINTS_DIR.glob("ckpt_*.json"), reverse=True):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            checkpoints.append(data)
        except Exception:
            continue

    if not checkpoints:
        print("ℹ️ No saved checkpoints found.")
        return []

    print("\n📦 AVAILABLE REPOSITORY CHECKPOINTS:")
    print("-" * 65)
    for ckpt in checkpoints:
        print(f"  • {ckpt['id']}")
        print(f"    Name: {ckpt['name']} | Created: {ckpt['timestamp']}")
        print(f"    Head: {ckpt['head_commit'][:8]} | Files: {len(ckpt['modified_files'])}")
    print("-" * 65)
    return checkpoints

def restore_checkpoint(checkpoint_id: Optional[str] = None) -> bool:
    """Restores repository working tree to the specified checkpoint (or latest)."""
    checkpoints = list_checkpoints()
    if not checkpoints:
        print("❌ Error: No checkpoints available to restore.")
        return False

    target_ckpt = None
    if checkpoint_id:
        for c in checkpoints:
            if c["id"] == checkpoint_id or c["name"] == checkpoint_id:
                target_ckpt = c
                break
        if not target_ckpt:
            print(f"❌ Error: Checkpoint '{checkpoint_id}' not found.")
            return False
    else:
        target_ckpt = checkpoints[0]

    print(f"⏪ Restoring repository to checkpoint: '{target_ckpt['id']}' ({target_ckpt['name']})...")

    # Hard reset working directory and clean untracked files
    run_git(["reset", "--hard", target_ckpt["head_commit"]])
    run_git(["clean", "-fd"])

    # Find matching stash
    stash_list = run_git(["stash", "list"]).stdout
    target_stash_ref = None
    for line in stash_list.splitlines():
        if target_ckpt["stash_message"] in line:
            target_stash_ref = line.split(":")[0].strip()
            break

    if target_stash_ref:
        res = run_git(["stash", "apply", target_stash_ref, "--quiet"])
        if res.returncode == 0:
            print(f"✨ Successfully restored working state from stash '{target_stash_ref}'.")
        else:
            print(f"⚠️ Stash apply had conflicts or warnings: {res.stderr.strip()}")
    else:
        print(f"✨ Clean commit state restored to HEAD ({target_ckpt['head_commit'][:8]}).")

    return True

def drop_checkpoint(checkpoint_id: str) -> bool:
    """Removes a checkpoint record."""
    meta_file = CHECKPOINTS_DIR / f"{checkpoint_id}.json"
    if meta_file.exists():
        meta_file.unlink()
        print(f"🗑️ Checkpoint '{checkpoint_id}' dropped.")
        return True
    print(f"❌ Checkpoint '{checkpoint_id}' not found.")
    return False

def main():
    parser = argparse.ArgumentParser(description="Autonomous Rollback & State Checkpoint Manager")
    subparsers = parser.add_subparsers(dest="action", help="Checkpoint actions")

    create_parser = subparsers.add_parser("create", help="Create a repository checkpoint")
    create_parser.add_argument("name", help="Human-readable checkpoint name")
    create_parser.add_argument("--description", "-d", default="", help="Optional description")

    restore_parser = subparsers.add_parser("restore", help="Restore repository to a checkpoint")
    restore_parser.add_argument("id", nargs="?", help="Checkpoint ID or name (defaults to latest)")

    subparsers.add_parser("list", help="List all saved checkpoints")

    drop_parser = subparsers.add_parser("drop", help="Delete a checkpoint")
    drop_parser.add_argument("id", help="Checkpoint ID to delete")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(0)

    if args.action == "create":
        create_checkpoint(args.name, args.description)
    elif args.action == "restore":
        success = restore_checkpoint(args.id)
        sys.exit(0 if success else 1)
    elif args.action == "list":
        list_checkpoints()
    elif args.action == "drop":
        drop_checkpoint(args.id)

if __name__ == "__main__":
    main()
