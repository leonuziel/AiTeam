#!/usr/bin/env python3
"""
Doc-Sync Custodian Decision Recorder
Appends atomic, date-stamped decision entries to the '## 4. Decisions & Revisions' section
of target documentation files or generates a new Architecture Decision Record (ADR).
"""
import sys
import argparse
import re
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

TODAY = datetime.utcnow().strftime("%Y-%m-%d")

ADR_TEMPLATE = """# ADR-{number:03d}: {title}

Scope: Architecture Decision Record - {title}
Related: docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** Architectural decision record, evaluation criteria, and consequences for {title}.
- **Does NOT Own:** Implementation files directly.

## 2. Invariants (Hard Rules)
- Once accepted, this decision is binding on all agent implementations until formally superseded.
- Superseding decisions must reference this record directly.

## 3. Specifications & Interfaces
### Decision Context
- **Status:** Accepted
- **Date:** {date}
- **Context:** {context}

### Evaluated Alternatives
- Option A: Baseline approach
- Option B: Alternative approach

### Consequences
- **Positive:** Standardized convention and consistency across agents.
- **Negative / Trade-offs:** Initial overhead in specification alignment.

## 4. Decisions & Revisions
- {date}: Initial decision recorded and marked as Accepted.
"""

def append_decision(file_path_str: str, decision_text: str):
    target = Path(file_path_str)
    if not target.exists():
        print(f"❌ Error: File '{target}' does not exist.")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    
    # Locate Decisions & Revisions heading
    match = re.search(r'(##\s*4\.\s*Decisions\s*&\s*Revisions|##\s*Decisions\s*&\s*Revisions)', content, re.IGNORECASE)
    if not match:
        print(f"❌ Error: Could not locate '## Decisions & Revisions' section in '{target}'.")
        sys.exit(1)

    new_entry = f"- {TODAY}: {decision_text}\n"
    
    # Find insertion point: directly below the header or at the end of the section
    header_end = match.end()
    # Check if there's trailing content after the header
    rest = content[header_end:]
    
    # If the file already ends with newline
    updated_content = content[:header_end] + "\n" + new_entry + rest.lstrip("\n")
    target.write_text(updated_content, encoding="utf-8")
    print(f"✅ Appended decision to '{target}':\n   {new_entry.strip()}")

def create_adr(title: str, context: str = "Standardized baseline decision"):
    decisions_dir = Path("docs/decisions")
    decisions_dir.mkdir(parents=True, exist_ok=True)
    
    # Count existing ADRs
    existing_adrs = list(decisions_dir.glob("ADR-*.md"))
    next_number = len(existing_adrs) + 1
    
    slug = title.lower().replace(" ", "-").replace("_", "-")
    filename = f"ADR-{next_number:03d}-{slug}.md"
    file_path = decisions_dir / filename

    content = ADR_TEMPLATE.format(
        number=next_number,
        title=title,
        date=TODAY,
        context=context
    )

    file_path.write_text(content, encoding="utf-8")
    print(f"✅ Created ADR: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Record decisions in docs or create ADRs.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--append", nargs=2, metavar=("FILE", "DECISION"), help="Append a decision entry to target doc")
    group.add_argument("--adr", type=str, metavar="TITLE", help="Create a new ADR record")

    parser.add_argument("--context", type=str, default="Baseline decision context", help="Context for new ADR")

    args = parser.parse_args()

    if args.append:
        append_decision(args.append[0], args.append[1])
    elif args.adr:
        create_adr(args.adr, args.context)

if __name__ == "__main__":
    main()
