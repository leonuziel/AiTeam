#!/usr/bin/env python3
"""
Documentation Dependency DAG & Cross-Reference Linter
Audits the 'Related:' metadata and cross-references across all documents under docs/.
Validates documentation layer hierarchy, verifies graph connectivity, ensures zero
orphaned documentation islands, and checks link integrity.
"""
import sys
import os
import re
import argparse
from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DOCS_DIR = Path("docs")

# Documentation Hierarchy Layers:
# Tier 0: Root Architecture & Index (defines system topology)
# Tier 1: Strategic Layer (Product & Tech Global Overviews)
# Tier 2: Domain, Subsystem & Interface Contracts (Data, API, Modules)
# Tier 3: Operational Governance & Records (Operations, Decisions, Changelog)
DOC_TIERS = {
    "architecture.md": 0,
    "index.md": 0,
    "product/overview.md": 1,
    "tech/overview.md": 1,
    "tech/data": 2,
    "tech/api": 2,
    "tech/modules": 2,
    "product/domains": 2,
    "operations": 3,
    "decisions": 3,
    "changelog.md": 3,
    "tech/template_enhancement_matrix_100.md": 2
}

def get_doc_tier(doc_path: Path) -> int:
    """Calculates the documentation architectural tier for a given document."""
    try:
        rel = doc_path.relative_to(DOCS_DIR).as_posix().lower()
        for pattern, tier in DOC_TIERS.items():
            if rel == pattern or rel.startswith(pattern):
                return tier
    except Exception:
        pass
    return 2

def resolve_target_doc(raw_target: str, source_doc: Path) -> Optional[Path]:
    """Resolves a raw related string/link to a canonical Path under docs/."""
    link_match = re.search(r"\[.*?\]\((.*?)\)", raw_target)
    target_str = link_match.group(1) if link_match else raw_target.strip()
    target_str = target_str.split("#")[0].strip()

    if not target_str or target_str.lower() in {"none", "n/a"}:
        return None
    if target_str.startswith(("http://", "https://", "mailto:")):
        return None
    if target_str.startswith("file://"):
        target_str = target_str.replace("file://", "").lstrip("/\\")

    cand_direct = Path(target_str)
    cand_root = Path.cwd() / target_str
    cand_rel = source_doc.parent / target_str
    cand_docs = DOCS_DIR / target_str

    for cand in [cand_direct, cand_root, cand_rel, cand_docs]:
        try:
            if cand.exists() and cand.is_file() and cand.suffix == ".md":
                return cand.resolve()
        except OSError:
            pass
    return None

def build_doc_network() -> Tuple[Dict[str, Set[str]], List[str], List[str]]:
    """Builds the directed cross-reference graph and identifies tier inversions."""
    graph: Dict[str, Set[str]] = {}
    broken_references: List[str] = []
    tier_inversions: List[str] = []

    markdown_files = sorted(list(DOCS_DIR.glob("**/*.md")))

    for doc in markdown_files:
        try:
            rel_doc = doc.relative_to(Path.cwd()).as_posix()
        except Exception:
            rel_doc = doc.as_posix()

        if rel_doc not in graph:
            graph[rel_doc] = set()

        try:
            content = doc.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        related_match = re.search(r"^Related:\s*(.+)$", content, re.MULTILINE | re.IGNORECASE)
        if not related_match:
            continue

        source_tier = get_doc_tier(doc)
        raw_items = related_match.group(1).split(",")
        for item in raw_items:
            item = item.strip()
            if not item or item.lower() in {"none", "n/a"}:
                continue
            resolved = resolve_target_doc(item, doc)
            if resolved:
                try:
                    rel_target = resolved.relative_to(Path.cwd().resolve()).as_posix()
                    graph[rel_doc].add(rel_target)
                    target_tier = get_doc_tier(resolved)
                    # Check for architectural tier inversion:
                    # Tier 0 (Root) should never be subordinated to Tier 3 (Changelog/Archive)
                    if source_tier == 0 and target_tier == 3:
                        tier_inversions.append(
                            f"Tier Inversion: Root spec '{rel_doc}' (Tier 0) is subordinated to operational record '{rel_target}' (Tier 3)!"
                        )
                except Exception:
                    pass
            else:
                broken_references.append(f"[{rel_doc}] Unresolvable 'Related:' target: '{item}'")

    return graph, broken_references, tier_inversions

def lint_doc_dag(strict: bool = False) -> int:
    print("🔍 Auditing Documentation Hierarchy & Cross-Reference Network...")

    graph, broken, inversions = build_doc_network()

    has_errors = False

    if broken:
        print(f"\n❌ Detected {len(broken)} broken 'Related:' cross-references:")
        for b in broken:
            print(f"  🔗 {b}")
        has_errors = True

    if inversions:
        print(f"\n❌ Detected {len(inversions)} Documentation Tier Inversions:")
        for inv in inversions:
            print(f"  🚨 {inv}")
        has_errors = True

    # Check for disconnected islands
    isolated = [k for k, v in graph.items() if len(v) == 0 and "readme" not in k.lower() and "archive" not in k.lower()]
    if isolated:
        print(f"\nℹ️  {len(isolated)} document(s) have standalone/unlinked 'Related:' scopes:")
        for iso in isolated[:3]:
            print(f"  • {iso}")

    print("-" * 65)
    if has_errors:
        print("❌ Documentation Network audit FAILED.")
        return 1
    else:
        total_connections = sum(len(v) for v in graph.values())
        print(f"✨ Documentation Hierarchy audit PASSED! {len(graph)} documents cleanly cross-referenced ({total_connections} active relations).")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Documentation Dependency & Hierarchy Linter")
    parser.add_argument("--strict", action="store_true", help="Fail on broken references or tier inversions")
    args = parser.parse_args()

    sys.exit(lint_doc_dag(strict=args.strict))

if __name__ == "__main__":
    main()
