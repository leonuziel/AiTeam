#!/usr/bin/env python3
"""
Doc-to-Code Changelist Tracker & Generator
Records atomic changelist entries, auto-detects diffs across docs and code,
and verifies traceability in docs/CHANGELOG.md.
"""
import sys
import re
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CHANGELOG_PATH = Path("docs/CHANGELOG.md")
CATEGORIES = ["Added", "Changed", "Fixed", "Invariants", "Security", "Deprecated", "Removed"]

def get_git_changed_files() -> Dict[str, List[str]]:
    """Inspects Git status to group changed files into docs, src, tests, scripts."""
    result = {"docs": [], "src": [], "tests": [], "scripts": [], "other": []}
    try:
        proc = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            # Git status porcelain: XY <path> or XY <path1> -> <path2>
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                continue
            path_str = parts[1].split("->")[-1].strip().strip('"')
            p = Path(path_str)
            if p.parts and p.parts[0] == "docs":
                result["docs"].append(path_str)
            elif p.parts and p.parts[0] == "src":
                result["src"].append(path_str)
            elif p.parts and p.parts[0] == "tests":
                result["tests"].append(path_str)
            elif p.parts and p.parts[0] in ("scripts", ".githooks", ".agent"):
                result["scripts"].append(path_str)
            else:
                result["other"].append(path_str)
    except Exception as e:
        print(f"⚠️  Git inspection warning: {e}")
    return result

def format_entry(title: str, category: str, summary: str, specs: str, modules: str, ref: str) -> str:
    """Formats a canonical changelist entry markdown block."""
    entry = f"- **{title}:**\n"
    entry += f"  - **Category:** {category}\n"
    entry += f"  - **Summary:** {summary}\n"
    entry += f"  - **Affected Specs:** {specs if specs else 'None'}\n"
    entry += f"  - **Affected Modules:** {modules if modules else 'None'}\n"
    entry += f"  - **Decision Ref:** {ref if ref else 'N/A'}\n"
    return entry

def record_entry(title: str, category: str, summary: str, specs: str, modules: str, ref: str, version: str = "Unreleased") -> bool:
    """Appends a structured changelist entry to docs/CHANGELOG.md."""
    if not CHANGELOG_PATH.exists():
        print(f"❌ Error: Changelog file '{CHANGELOG_PATH}' not found.")
        return False

    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    
    # Locate version header (e.g. ### [Unreleased])
    version_header_pattern = rf"(###\s+\[{re.escape(version)}\][^\n]*)"
    match = re.search(version_header_pattern, content)
    if not match:
        print(f"❌ Error: Section for version '[{version}]' not found in {CHANGELOG_PATH}.")
        return False

    version_header = match.group(1)
    version_idx = match.end()

    # Look for the category header (e.g. #### Added) under this version section
    # Find next section or end of version block
    next_version_match = re.search(r"\n###\s+\[", content[version_idx:])
    version_block_end = version_idx + next_version_match.start() if next_version_match else len(content)

    category_header = f"#### {category}"
    category_pattern = rf"({re.escape(category_header)}\s*\n)"
    sub_block = content[version_idx:version_block_end]
    cat_match = re.search(category_pattern, sub_block)

    entry_text = format_entry(title, category, summary, specs, modules, ref)

    if cat_match:
        # Insert after category header
        insert_pos = version_idx + cat_match.end()
        new_content = content[:insert_pos] + entry_text + content[insert_pos:]
    else:
        # Category header does not exist under this version yet; create it right under version header
        new_block = f"\n\n{category_header}\n" + entry_text
        new_content = content[:version_idx] + new_block + content[version_idx:]

    CHANGELOG_PATH.write_text(new_content, encoding="utf-8")
    print(f"✅ Successfully recorded changelist entry: '{title}' under [{version}] -> {category}")
    return True

def generate_entry_proposal(category: str = "Changed", ref: str = "N/A", apply: bool = False) -> str:
    """Auto-generates a changelist draft based on current Git working directory changes."""
    files = get_git_changed_files()
    all_changed = files["docs"] + files["src"] + files["tests"] + files["scripts"] + files["other"]
    
    if not all_changed:
        print("ℹ️  No uncommitted changes detected in repository.")
        return ""

    specs_str = ", ".join(f"`{f}`" for f in files["docs"]) if files["docs"] else "None"
    modules_str = ", ".join(f"`{f}`" for f in (files["src"] + files["tests"] + files["scripts"])) if (files["src"] + files["tests"] + files["scripts"]) else "None"

    # Suggest category
    detected_cat = category
    if any("invariants" in f.lower() for f in files["docs"]):
        detected_cat = "Invariants"
    elif files["src"] and not files["docs"]:
        detected_cat = "Fixed"
    elif files["docs"] and not files["src"]:
        detected_cat = "Added"

    title_proposal = "Automated Work Iteration"
    summary_proposal = f"Updated {len(all_changed)} repository file(s) across specifications and implementations."

    draft = format_entry(
        title=title_proposal,
        category=detected_cat,
        summary=summary_proposal,
        specs=specs_str,
        modules=modules_str,
        ref=ref
    )

    print("\n🔍 DETECTED CHANGELIST DRAFT FROM GIT DIFF:")
    print("-" * 60)
    print(draft.strip())
    print("-" * 60)

    if apply:
        record_entry(title_proposal, detected_cat, summary_proposal, specs_str, modules_str, ref)
    else:
        print("💡 Use '--apply' or pass arguments to '--record' to commit this entry to docs/CHANGELOG.md.")

    return draft

def release_version(version: str, tag: bool = False) -> bool:
    """Cuts a new release in docs/CHANGELOG.md by converting [Unreleased] to a versioned block."""
    if not CHANGELOG_PATH.exists():
        print(f"❌ Error: Changelog file '{CHANGELOG_PATH}' not found.")
        return False

    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    unreleased_pattern = r"###\s+\[Unreleased\]"
    match = re.search(unreleased_pattern, content)
    if not match:
        print("❌ Error: '### [Unreleased]' section not found in changelog.")
        return False

    today = datetime.utcnow().strftime("%Y-%m-%d")
    clean_version = version.lstrip("v")
    new_release_header = f"### [Unreleased]\n\n### [{clean_version}] - {today}"

    # Replace first occurrence of ### [Unreleased] with new block
    updated_content = content[:match.start()] + new_release_header + content[match.end():]
    CHANGELOG_PATH.write_text(updated_content, encoding="utf-8")
    print(f"🎉 Successfully cut release [{clean_version}] dated {today} in '{CHANGELOG_PATH}'!")

    if tag:
        tag_name = f"v{clean_version}"
        try:
            subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {clean_version}"], check=True)
            print(f"🏷️  Created Git tag '{tag_name}'.")
        except Exception as e:
            print(f"⚠️  Could not create Git tag: {e}")

    return True

def verify_changelog() -> int:
    """Verifies docs/CHANGELOG.md structure and traceability requirements."""
    print("🔍 Auditing changelist tracking integrity...")
    if not CHANGELOG_PATH.exists():
        print(f"  ❌ Missing changelog ledger: '{CHANGELOG_PATH}' does not exist.")
        return 1

    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    errors = 0

    if "### [Unreleased]" not in content:
        print("  ❌ Missing '### [Unreleased]' section in docs/CHANGELOG.md.")
        errors += 1

    if "## 1. Responsibilities & Boundaries" not in content or "## 2. Invariants (Hard Rules)" not in content:
        print("  ❌ docs/CHANGELOG.md does not adhere to the 4-section documentation invariant.")
        errors += 1

    if errors == 0:
        print("✨ Changelist tracking ledger is healthy and compliant with invariants!")
        return 0
    else:
        print(f"❌ Changelist verification failed with {errors} error(s).")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Doc-to-Code Changelist Tracker & Generator")
    subparsers = parser.add_subparsers(dest="subcommand", help="Changelist commands")

    # Record command
    record_parser = subparsers.add_parser("record", help="Record a structured changelist entry")
    record_parser.add_argument("--title", required=True, help="Title of the change")
    record_parser.add_argument("--category", choices=CATEGORIES, default="Changed", help="Change category")
    record_parser.add_argument("--summary", required=True, help="Description of change and rationale")
    record_parser.add_argument("--specs", default="", help="Comma-separated affected spec paths under docs/")
    record_parser.add_argument("--modules", default="", help="Comma-separated affected modules/tests paths")
    record_parser.add_argument("--ref", default="", help="ADR link, commit hash, or issue reference")
    record_parser.add_argument("--version", default="Unreleased", help="Target version header (default: Unreleased)")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate changelist draft from Git diff")
    gen_parser.add_argument("--category", choices=CATEGORIES, default="Changed", help="Default category")
    gen_parser.add_argument("--ref", default="", help="Decision or issue reference")
    gen_parser.add_argument("--apply", action="store_true", help="Automatically record generated draft to docs/CHANGELOG.md")

    # Release command
    release_parser = subparsers.add_parser("release", help="Cut a release by converting [Unreleased] to a versioned release")
    release_parser.add_argument("--version", required=True, help="New release version (e.g. 1.1.0)")
    release_parser.add_argument("--tag", action="store_true", help="Create a Git tag for this release")

    # Verify command
    subparsers.add_parser("verify", help="Verify changelog structure and invariants")

    args = parser.parse_args()

    if not args.subcommand or args.subcommand == "verify":
        sys.exit(verify_changelog())
    elif args.subcommand == "record":
        success = record_entry(args.title, args.category, args.summary, args.specs, args.modules, args.ref, args.version)
        sys.exit(0 if success else 1)
    elif args.subcommand == "generate":
        generate_entry_proposal(category=args.category, ref=args.ref, apply=args.apply)
        sys.exit(0)
    elif args.subcommand == "release":
        success = release_version(args.version, args.tag)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
