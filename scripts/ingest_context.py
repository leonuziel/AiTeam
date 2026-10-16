#!/usr/bin/env python3
"""
Context Ingestion Assistant
Appends or updates specifications in target documentation files and logs the revision,
ensuring the 4-section documentation layout is maintained.
"""
import sys
import argparse
import re
from datetime import datetime
from pathlib import Path
import subprocess

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

TODAY = datetime.utcnow().strftime("%Y-%m-%d")

def ingest_context(target_file_str: str, section_title: str, content_to_add: str, summary: str = None):
    target = Path(target_file_str)
    if not target.exists():
        print(f"❌ Error: File '{target}' does not exist.")
        sys.exit(1)

    file_text = target.read_text(encoding="utf-8")
    
    # Locate target section header (e.g. ## 2. Invariants or ## 3. Specifications & Interfaces)
    pattern = rf'(##\s*(?:\d\.\s*)?{re.escape(section_title)}[^\n]*)'
    match = re.search(pattern, file_text, re.IGNORECASE)
    
    if not match:
        print(f"❌ Error: Could not locate section '{section_title}' in '{target}'.")
        sys.exit(1)

    # Insert content right below the section heading
    header_end = match.end()
    insertion = f"\n\n{content_to_add.strip()}\n"
    
    updated_text = file_text[:header_end] + insertion + file_text[header_end:]
    
    # If summary provided, append to Decisions & Revisions
    if summary:
        rev_match = re.search(r'(##\s*(?:\d\.\s*)?Decisions\s*&\s*Revisions[^\n]*)', updated_text, re.IGNORECASE)
        if rev_match:
            rev_header_end = rev_match.end()
            rev_entry = f"\n- {TODAY}: {summary.strip()}\n"
            updated_text = updated_text[:rev_header_end] + rev_entry + updated_text[rev_header_end:]
            
    target.write_text(updated_text, encoding="utf-8")
    print(f"✅ Context ingested into '{target}' under section '{section_title}'.")
    if summary:
        print(f"   Logged revision: {summary.strip()}")

    # Run linter verification
    print("▶ Running lint verification on updated documentation...")
    linter = Path("scripts/lint_docs.py")
    if linter.exists():
        res = subprocess.run([sys.executable, str(linter), "--strict"], capture_output=True, text=True, encoding="utf-8")
        if res.returncode == 0:
            print("✨ Documentation linter passed cleanly.")
        else:
            print(f"⚠️  Linter warnings/errors:\n{res.stdout}")

def main():
    parser = argparse.ArgumentParser(description="Ingest structured context into documentation leaves.")
    parser.add_argument("--target", required=True, type=str, help="Target markdown file (e.g., docs/tech/api/contracts.md)")
    parser.add_argument("--section", required=True, type=str, help="Section name (e.g., 'Invariants', 'Specifications & Interfaces')")
    parser.add_argument("--content", required=True, type=str, help="Content to append under the section")
    parser.add_argument("--summary", type=str, default="Context ingested into specification", help="Brief summary for Decisions & Revisions log")

    args = parser.parse_args()
    ingest_context(args.target, args.section, args.content, args.summary)

if __name__ == "__main__":
    main()
