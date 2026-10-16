#!/usr/bin/env python3
"""
New Project Bootstrap Wizard
Initializes a new software project created from this meta-generator template.
"""
import sys
import argparse
import subprocess
import json
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def bootstrap(name: str, description: str):
    print("=" * 65)
    print(f"🚀 BOOTSTRAPPING NEW PROJECT: '{name}'")
    print("=" * 65)

    # 1. Update .agent/config.json
    config_path = Path(".agent/config.json")
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["workspace"]["name"] = name
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
            print(f"  ✅ Updated .agent/config.json with project name: '{name}'")
        except Exception as e:
            print(f"  ⚠️  Could not update .agent/config.json: {e}")

    # 2. Update docs/product/overview.md
    product_overview = Path("docs/product/overview.md")
    if product_overview.exists():
        content = product_overview.read_text(encoding="utf-8")
        # Update title line
        lines = content.splitlines()
        if lines and lines[0].startswith("# "):
            lines[0] = f"# Product Overview: {name}"
        updated_content = "\n".join(lines)
        product_overview.write_text(updated_content, encoding="utf-8")
        print(f"  ✅ Updated docs/product/overview.md title")

    # 3. Check / Initialize Git
    git_dir = Path(".git")
    if not git_dir.exists():
        try:
            subprocess.run(["git", "init"], check=True, capture_output=True)
            print("  ✅ Initialized fresh Git repository (.git/)")
        except Exception:
            print("  ℹ️  Git initialization skipped (git command not available or already managed)")
    else:
        print("  ℹ️  Git repository already initialized.")

    # 4. Run full health audit
    print("\n▶ Running health audit on fresh project...")
    audit_script = Path("scripts/audit_repo.py")
    if audit_script.exists():
        result = subprocess.run([sys.executable, str(audit_script)], capture_output=True, text=True, encoding="utf-8")
        print(result.stdout.strip())
        if result.returncode != 0:
            print("❌ Initial health audit failed. Check warnings above.")
            sys.exit(1)

    print("\n" + "=" * 65)
    print(f"✨ Project '{name}' successfully bootstrapped and ready for development!")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Bootstrap a new software project from this template.")
    parser.add_argument("--name", required=True, type=str, help="Name of the new software project")
    parser.add_argument("--description", default="New software project bootstrapped from agentic template", type=str, help="Project summary description")

    args = parser.parse_args()
    bootstrap(args.name, args.description)

if __name__ == "__main__":
    main()
