#!/usr/bin/env python3
"""
Living Documentation Index Generator
Scans all specification documents under docs/ and generates a comprehensive,
searchable catalog and dependency map at docs/INDEX.md.
"""
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DOCS_DIR = Path("docs")
DEFAULT_OUTPUT = DOCS_DIR / "INDEX.md"

TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
SCOPE_RE = re.compile(r"^Scope:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
RELATED_RE = re.compile(r"^Related:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
SECTION_1_RE = re.compile(r"^##\s+1\.\s+Responsibilities.*?\n(.*?)(?=\n##\s+|$)", re.DOTALL | re.MULTILINE)


def parse_doc(doc_path: Path) -> Dict[str, Any]:
    try:
        text = doc_path.read_text(encoding="utf-8")
    except Exception:
        return {}

    title_match = TITLE_RE.search(text)
    title = title_match.group(1).strip() if title_match else doc_path.stem

    scope_match = SCOPE_RE.search(text)
    scope = scope_match.group(1).strip() if scope_match else "General"

    related_match = RELATED_RE.search(text)
    related = related_match.group(1).strip() if related_match else "None"

    # Extract first sentence or bullet from section 1
    summary = "Specification leaf."
    sec1_match = SECTION_1_RE.search(text)
    if sec1_match:
        sec1_text = sec1_match.group(1).strip()
        # Find first non-empty line that isn't a subheader
        for line in sec1_text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                # Clean bullet or markdown
                clean = re.sub(r"^[-*]\s+", "", line)
                clean = re.sub(r"[*_`]", "", clean)
                summary = clean[:120] + ("..." if len(clean) > 120 else "")
                break

    return {
        "path": doc_path,
        "rel_path": doc_path.as_posix(),
        "title": title,
        "scope": scope,
        "related": related,
        "summary": summary
    }


def generate_index_content(docs: List[Dict[str, Any]]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        "# Documentation System Index & Dependency Map",
        "",
        "Scope: Documentation Topology",
        "Related: [System Architecture](ARCHITECTURE.md)",
        "",
        "## 1. Responsibilities & Boundaries",
        "This document serves as the single living index and navigation hub for all specifications across the repository.",
        "It catalogs all domain, technical, operational, and architectural documentation leaves to ensure complete discovery and eliminate orphaned specifications.",
        "",
        "## 2. Invariants (Hard Rules)",
        "- Every specification file under `docs/` must be cataloged within this index.",
        "- All documentation links within this index must remain valid, relative, and verified.",
        "- This document is maintained programmatically via `python scripts/harness.py index`.",
        "- Manual edits must adhere strictly to the 4-section documentation invariant.",
        "",
        "## 3. Specifications & Interfaces",
        "",
        "### Documentation Hierarchy",
        "",
        "```mermaid",
        "graph TD",
        "    Architecture[\"docs/ARCHITECTURE.md<br/>(Master System Blueprint)\"]",
        "    Product[\"docs/product/<br/>(Business & Domain Specs)\"]",
        "    Tech[\"docs/tech/<br/>(API, Data & Module Contracts)\"]",
        "    Ops[\"docs/operations/<br/>(Deployment & Telemetry)\"]",
        "    Decisions[\"docs/decisions/<br/>(Architecture Decision Records)\"]",
        "",
        "    Architecture --> Product",
        "    Architecture --> Tech",
        "    Product --> Tech",
        "    Tech --> Ops",
        "    Decisions -.-> Architecture",
        "    Decisions -.-> Tech",
        "```",
        "",
        "### Specification Catalog",
        "",
        "| Specification | Scope | Summary | Related Links |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for d in docs:
        if d["path"].name == "INDEX.md":
            continue
        rel_to_docs = d["path"].relative_to(DOCS_DIR).as_posix()
        link = f"[{d['title']}]({rel_to_docs})"
        scope = d["scope"]
        summary = d["summary"].replace("|", "/")
        related = d["related"].replace("|", "/")
        lines.append(f"| {link} | {scope} | {summary} | {related} |")

    lines.extend([
        "",
        "## 4. Decisions & Revisions",
        f"- {today}: Auto-generated living documentation index cataloging {len(docs) - 1} specification leaves."
    ])

    return "\n".join(lines) + "\n"


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Living Documentation Index Generator")
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUTPUT), help="Output index path")
    parser.add_argument("--check", action="store_true", help="Check if index is complete and up to date")
    args = parser.parse_args()

    if not DOCS_DIR.exists():
        print("❌ Error: 'docs/' directory does not exist.")
        return 1

    all_md = sorted(DOCS_DIR.rglob("*.md"))
    doc_infos = [parse_doc(p) for p in all_md if p.is_file()]

    output_path = Path(args.output)
    new_content = generate_index_content(doc_infos)

    if args.check:
        if not output_path.exists():
            print(f"❌ Index file '{output_path}' does not exist! Run without --check to generate.")
            return 1
        existing_content = output_path.read_text(encoding="utf-8")
        missing_entries = []
        for d in doc_infos:
            if d["path"].name == "INDEX.md":
                continue
            rel_to_docs = d["path"].relative_to(DOCS_DIR).as_posix()
            if rel_to_docs not in existing_content:
                missing_entries.append(rel_to_docs)
        if missing_entries:
            print(f"⚠️  Index is out of date: {len(missing_entries)} document(s) missing from catalog:")
            for m in missing_entries:
                print(f"    - {m}")
            return 1
        print("✨ Documentation index is completely up to date!")
        return 0

    output_path.write_text(new_content, encoding="utf-8")
    print(f"✨ Living documentation index generated at '{output_path.as_posix()}' ({len(doc_infos) - 1} documents indexed)!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
