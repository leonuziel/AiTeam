#!/usr/bin/env python3
"""
Structural Documentation Linter
Validates that all documentation nodes adhere strictly to the 4-section standard,
metadata headers, and internal link integrity.
"""
import os
import sys
import re
import argparse
from pathlib import Path

# Ensure UTF-8 output across platforms and Windows console code pages
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DOCS_DIR = Path("docs")
REQUIRED_SECTIONS = [
    "Responsibilities & Boundaries",
    "Invariants",
    "Specifications & Interfaces",
    "Decisions & Revisions"
]

def check_link_integrity(content: str, source_file: Path) -> list:
    """Checks markdown relative links to verify target existence."""
    broken_links = []
    # Match markdown links: [text](target) excluding web URLs and anchors
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    for text, target in links:
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # Strip anchor from target
        clean_target = target.split("#")[0]
        if not clean_target:
            continue
        
        target_path = Path(clean_target)
        # Check relative to repo root or relative to source file
        resolved_from_root = Path.cwd() / target_path
        resolved_from_source = source_file.parent / target_path
        
        if not resolved_from_root.exists() and not resolved_from_source.exists():
            broken_links.append(target)
            
    return broken_links

def lint_docs(strict: bool = False) -> int:
    errors = 0
    warnings = 0
    markdown_files = sorted(list(DOCS_DIR.glob("**/*.md")))
    print(f"🔍 Linting {len(markdown_files)} documentation files in '{DOCS_DIR}'...")

    for file_path in markdown_files:
        content = file_path.read_text(encoding="utf-8")
        file_errors = 0
        file_warnings = 0
        
        # Check required sections
        for section in REQUIRED_SECTIONS:
            if section.lower() not in content.lower():
                print(f"  ❌ [{file_path}] Missing required section: '## {section}'")
                file_errors += 1

        # Check metadata headers
        if "Scope:" not in content:
            print(f"  ⚠️  [{file_path}] Missing 'Scope:' metadata line.")
            file_warnings += 1
        if "Related:" not in content:
            print(f"  ⚠️  [{file_path}] Missing 'Related:' metadata line.")
            file_warnings += 1

        # Check internal links
        broken = check_link_integrity(content, file_path)
        for b in broken:
            print(f"  🔗 [{file_path}] Broken relative link detected: '{b}'")
            file_warnings += 1

        errors += file_errors
        warnings += file_warnings

    if strict and warnings > 0:
        errors += warnings

    print("-" * 60)
    if errors > 0:
        print(f"❌ Structural linting FAILED with {errors} error(s) and {warnings} warning(s).")
        return 1
    elif warnings > 0:
        print(f"⚠️  Documentation passed with {warnings} warning(s) (clean in non-strict mode).")
        return 0
    else:
        print("✨ All documentation files passed structural & link integrity checks!")
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint documentation structure and invariants.")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings (e.g., missing metadata or broken links)")
    args = parser.parse_args()
    
    sys.exit(lint_docs(strict=args.strict))