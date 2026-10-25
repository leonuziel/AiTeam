#!/usr/bin/env python3
"""
Documentation Compaction & Lifecycle Assistant
Scans documentation for historical revision bloat in Section 4,
squashes accumulated revisions into clean baseline specifications,
and archives superseded Architecture Decision Records (ADRs).
"""
import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Ensure UTF-8 output across platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DOCS_DIR = Path("docs")
DECISIONS_DIR = DOCS_DIR / "decisions"
ARCHIVE_DIR = DECISIONS_DIR / "archive"

SECTION_4_RE = re.compile(
    r"(##\s+4\.\s+Decisions\s+&\s+Revisions.*?\n)(.*)",
    re.DOTALL | re.IGNORECASE
)

def extract_section_4_revisions(content: str) -> Tuple[Optional[str], List[str]]:
    """Extracts lines and individual revision bullets from Section 4."""
    match = SECTION_4_RE.search(content)
    if not match:
        return None, []
    sec4_text = match.group(2)
    bullets = []
    for line in sec4_text.splitlines():
        trimmed = line.strip()
        if trimmed.startswith(("-", "*")):
            bullets.append(trimmed)
    return sec4_text, bullets

def audit_docs(threshold: int = 8) -> Tuple[List[Dict], List[Path]]:
    """Audits docs for revision bloat and superseded ADRs."""
    bloated_docs = []
    all_markdown = sorted(list(DOCS_DIR.glob("**/*.md")))

    for md_file in all_markdown:
        # Skip archive directory
        if "archive" in md_file.parts:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        _, bullets = extract_section_4_revisions(content)
        if len(bullets) > threshold:
            bloated_docs.append({
                "path": md_file,
                "count": len(bullets),
                "bullets": bullets
            })

    # Scan for superseded ADRs
    superseded_adrs = []
    if DECISIONS_DIR.exists():
        for adr in sorted(DECISIONS_DIR.glob("ADR-*.md")):
            try:
                content = adr.read_text(encoding="utf-8")
                # Look for Status: Superseded or Status: Deprecated
                if re.search(r"Status:\s*(Superseded|Deprecated)", content, re.IGNORECASE):
                    superseded_adrs.append(adr)
            except Exception:
                continue

    return bloated_docs, superseded_adrs

def squash_file_revisions(file_path: Path, keep_recent: int = 2) -> bool:
    """Squashes historical Section 4 revisions into a single consolidated baseline entry."""
    if not file_path.exists():
        print(f"❌ Error: File '{file_path}' does not exist.")
        return False

    content = file_path.read_text(encoding="utf-8")
    match = SECTION_4_RE.search(content)
    if not match:
        print(f"⚠️ File '{file_path}' does not have a recognizable '## 4. Decisions & Revisions' section.")
        return False

    header = match.group(1)
    sec4_text = match.group(2)
    lines = sec4_text.splitlines()

    bullets = []
    other_lines = []
    for line in lines:
        if line.strip().startswith(("-", "*")):
            bullets.append(line.strip())
        else:
            if line.strip():
                other_lines.append(line)

    if len(bullets) <= keep_recent:
        print(f"ℹ️ File '{file_path}' only has {len(bullets)} revision(s). Nothing to squash.")
        return False

    older_bullets = bullets[:-keep_recent]
    recent_bullets = bullets[-keep_recent:]

    today_str = datetime.now().strftime("%Y-%m-%d")
    baseline_entry = (
        f"- {today_str}: [CONSOLIDATED-BASELINE] Consolidated {len(older_bullets)} historical revisions "
        f"into living specifications. Full architectural provenance preserved in Git history."
    )

    new_sec4_lines = []
    if other_lines:
        new_sec4_lines.extend(other_lines)
        new_sec4_lines.append("")
    new_sec4_lines.append(baseline_entry)
    for b in recent_bullets:
        new_sec4_lines.append(b)

    new_sec4_content = "\n".join(new_sec4_lines) + "\n"
    new_full_content = content[:match.start(2)] + new_sec4_content

    file_path.write_text(new_full_content, encoding="utf-8")
    print(f"✨ Squashed {len(older_bullets)} historical revision(s) in '{file_path}'. Kept {len(recent_bullets)} recent entries.")
    return True

def archive_superseded_adrs(superseded: List[Path]) -> int:
    """Moves superseded or deprecated ADRs into docs/decisions/archive/."""
    if not superseded:
        print("ℹ️ No superseded ADRs found to archive.")
        return 0

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    moved_count = 0
    for adr in superseded:
        dest = ARCHIVE_DIR / adr.name
        adr.rename(dest)
        print(f"📦 Archived: '{adr}' -> '{dest}'")
        moved_count += 1
    return moved_count

def run_audit_report(threshold: int = 8, strict: bool = False) -> int:
    print(f"🔍 Auditing documentation lifecycle & revision bloat (Threshold: >{threshold} entries)...")
    bloated, superseded = audit_docs(threshold=threshold)

    has_issues = False

    if bloated:
        print(f"\n⚠️ Detected {len(bloated)} document(s) exceeding revision threshold:")
        for item in bloated:
            print(f"  - [{item['path'].as_posix()}]: {item['count']} revisions (Threshold: {threshold})")
        has_issues = True
    else:
        print("✨ All document revision logs are lean and within healthy thresholds.")

    if superseded:
        print(f"\n📦 Detected {len(superseded)} superseded/deprecated ADR(s) awaiting archiving:")
        for adr in superseded:
            print(f"  - {adr.as_posix()}")
        has_issues = True
    else:
        print("✨ Zero unarchived superseded ADRs detected.")

    print("-" * 65)
    if has_issues:
        print("💡 Recommendation:")
        if bloated:
            print("   Run: python scripts/harness.py compact --squash <path>  (or --squash-all)")
        if superseded:
            print("   Run: python scripts/harness.py compact --archive-adrs")
        if strict:
            return 1
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Documentation Compaction & Lifecycle Assistant"
    )
    parser.add_argument("--audit", action="store_true", help="Audit docs for revision bloat and superseded ADRs")
    parser.add_argument("--threshold", type=int, default=8, help="Revision count threshold before flagging bloat (default: 8)")
    parser.add_argument("--squash", help="Target document path to squash historical Section 4 revisions")
    parser.add_argument("--squash-all", action="store_true", help="Batch squash all documents exceeding threshold")
    parser.add_argument("--archive-adrs", action="store_true", help="Move superseded/deprecated ADRs to archive/")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero code if bloat is detected during audit")

    args = parser.parse_args()

    if args.squash:
        success = squash_file_revisions(Path(args.squash))
        sys.exit(0 if success else 1)

    if args.archive_adrs:
        _, superseded = audit_docs(threshold=args.threshold)
        archive_superseded_adrs(superseded)
        sys.exit(0)

    if args.squash_all:
        bloated, _ = audit_docs(threshold=args.threshold)
        if not bloated:
            print("✨ No bloated documents found to squash.")
            sys.exit(0)
        for item in bloated:
            squash_file_revisions(item["path"])
        sys.exit(0)

    # Default to audit
    sys.exit(run_audit_report(threshold=args.threshold, strict=args.strict))

if __name__ == "__main__":
    main()
