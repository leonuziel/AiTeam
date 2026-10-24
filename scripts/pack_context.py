#!/usr/bin/env python3
"""
Context Bundler & Subagent Prompt Packer
Extracts and bundles the minimal, token-efficient slice of documentation, invariants,
API contracts, and ADRs needed for a specific implementation or design task.
"""
import sys
import re
import argparse
from pathlib import Path
from typing import List, Set, Optional

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DOCS_DIR = Path("docs")
AGENT_SYSTEM_PROMPT = Path("agent_system_prompt.md")
GLOBAL_ARCH = Path("docs/ARCHITECTURE.md")

def extract_related_paths(doc_path: Path) -> List[Path]:
    """Finds documents mentioned in the 'Related:' header of a file."""
    if not doc_path.exists():
        return []
    content = doc_path.read_text(encoding="utf-8")
    related_match = re.search(r"^Related:\s*(.+)$", content, re.MULTILINE | re.IGNORECASE)
    if not related_match:
        return []
    raw_paths = related_match.group(1).split(",")
    resolved = []
    for p in raw_paths:
        p = p.strip()
        if not p or p.lower() == "none":
            continue
        # Strip markdown links e.g. [name](path)
        link_match = re.search(r"\[.*?\]\((.*?)\)", p)
        path_str = link_match.group(1) if link_match else p
        cand = Path(path_str)
        if cand.exists():
            resolved.append(cand)
        elif (DOCS_DIR / path_str).exists():
            resolved.append(DOCS_DIR / path_str)
    return resolved

def pack_context(
    domain: Optional[str] = None,
    module: Optional[str] = None,
    target: Optional[str] = None,
    include_adrs: bool = True,
    output_path: Optional[str] = None
) -> str:
    """Compiles the structured context package for subagents or LLMs."""
    targets_to_read: Set[Path] = set()

    # Always include global architecture
    if GLOBAL_ARCH.exists():
        targets_to_read.add(GLOBAL_ARCH)

    # 1. Target by domain
    if domain:
        domain_dir = DOCS_DIR / "product" / "domains" / domain
        if domain_dir.exists():
            for p in domain_dir.glob("*.md"):
                targets_to_read.add(p)
        else:
            print(f"⚠️  Domain directory '{domain_dir}' does not exist.")

    # 2. Target by module
    if module:
        module_dir = DOCS_DIR / "tech" / "modules" / module
        if module_dir.exists():
            for p in module_dir.glob("*.md"):
                targets_to_read.add(p)
        else:
            print(f"⚠️  Module directory '{module_dir}' does not exist.")

    # 3. Direct target file
    if target:
        t_path = Path(target)
        if t_path.exists():
            targets_to_read.add(t_path)
            for rel in extract_related_paths(t_path):
                targets_to_read.add(rel)
        else:
            print(f"⚠️  Target file '{target}' does not exist.")

    # 4. Optional ADRs
    if include_adrs:
        adrs_dir = DOCS_DIR / "decisions"
        if adrs_dir.exists():
            for adr in sorted(adrs_dir.glob("ADR-*.md")):
                targets_to_read.add(adr)

    # Build the bundle
    sections: List[str] = []

    # Header
    sections.append("# AGENT CONTEXT PACK: DOC-TO-CODE HARNESS")
    sections.append("> Generated for targeted autonomous agent execution.")
    sections.append("")

    # Agent Blueprint Excerpt
    if AGENT_SYSTEM_PROMPT.exists():
        blueprint_content = AGENT_SYSTEM_PROMPT.read_text(encoding="utf-8")
        sections.append("## 0. AGENT CORE DIRECTIVES & ESCALATION RULE")
        # Extract Core Philosophy & Critical Escalation Rule
        sections.append("```text")
        sections.append("CRITICAL INVARIANT:")
        sections.append("Code implements specifications; code never invents specifications.")
        sections.append("If a requirement or invariant is missing, output:")
        sections.append("[BLOCKED_NEED_DECISION: <exact ambiguity description>]")
        sections.append("and halt code generation immediately.")
        sections.append("```\n")

    # Target Specifications
    sections.append("## 1. RELEVANT SPECIFICATIONS & CONTRACTS\n")
    for doc in sorted(targets_to_read):
        try:
            content = doc.read_text(encoding="utf-8")
            rel_path = doc.as_posix()
            sections.append(f"### File: `{rel_path}`\n")
            sections.append(content.strip())
            sections.append("\n---\n")
        except Exception as e:
            sections.append(f"⚠️ Could not read {doc}: {e}")

    bundle = "\n".join(sections)
    word_count = len(bundle.split())
    approx_tokens = int(word_count * 1.35)

    print(f"📦 Context Pack generated: {len(targets_to_read)} file(s) bundled (~{approx_tokens:,} tokens, {word_count:,} words).")

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(bundle, encoding="utf-8")
        print(f"💾 Saved context pack to '{out}'.")

    return bundle

def main():
    parser = argparse.ArgumentParser(description="Pack targeted context and invariants for subagents.")
    parser.add_argument("--domain", help="Product domain to include (e.g. auth, billing)")
    parser.add_argument("--module", help="Technical module to include (e.g. gateway, persistence)")
    parser.add_argument("--target", help="Specific document to pack (with auto-discovered related docs)")
    parser.add_argument("--output", "-o", help="File path to save the generated context pack")
    parser.add_argument("--no-adrs", action="store_true", help="Exclude architecture decision records")

    args = parser.parse_args()

    pack = pack_context(
        domain=args.domain,
        module=args.module,
        target=args.target,
        include_adrs=not args.no_adrs,
        output_path=args.output
    )

    if not args.output:
        print("\n" + "=" * 65)
        print(pack[:1500] + ("\n... [truncated preview, use -o to save full pack] ..." if len(pack) > 1500 else ""))
        print("=" * 65)

if __name__ == "__main__":
    main()
