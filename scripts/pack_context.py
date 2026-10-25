#!/usr/bin/env python3
"""
Context Bundler & Subagent Prompt Packer
Extracts and bundles the minimal, token-efficient slice of documentation, invariants,
API contracts, and ADRs needed for a specific implementation or design task.
Features intelligent token pruning: filters out archived/superseded ADRs and prunes
historical Section 4 revision churn to maximize LLM context efficiency.
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

SECTION_4_RE = re.compile(
    r"(##\s+4\.\s+Decisions\s+&\s+Revisions.*?\n)(.*)",
    re.DOTALL | re.IGNORECASE
)

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
        if path_str.startswith("file://"):
            path_str = path_str.replace("file://", "").lstrip("/\\")
        cand = Path(path_str)
        try:
            if cand.exists():
                resolved.append(cand)
            elif (DOCS_DIR / path_str).exists():
                resolved.append(DOCS_DIR / path_str)
        except OSError:
            pass
    return resolved

def is_active_adr(adr_path: Path) -> bool:
    """Checks whether an ADR is active (not superseded, deprecated, or archived)."""
    if "archive" in adr_path.parts:
        return False
    try:
        text = adr_path.read_text(encoding="utf-8")
        if re.search(r"Status:\s*(Superseded|Deprecated)", text, re.IGNORECASE):
            return False
        return True
    except Exception:
        return True

def prune_section_4_for_context(content: str, max_revisions: int = 3) -> str:
    """Prunes older Section 4 revisions to conserve LLM context tokens."""
    match = SECTION_4_RE.search(content)
    if not match:
        return content

    header = match.group(1)
    sec4_text = match.group(2)
    lines = sec4_text.splitlines()

    bullets = []
    other_lines = []
    for line in lines:
        trimmed = line.strip()
        if trimmed.startswith(("-", "*")):
            bullets.append(trimmed)
        else:
            if trimmed:
                other_lines.append(line)

    if len(bullets) <= max_revisions:
        return content

    recent_bullets = bullets[-max_revisions:]
    omitted_count = len(bullets) - max_revisions

    pruned_sec4 = []
    if other_lines:
        pruned_sec4.extend(other_lines)
        pruned_sec4.append("")
    pruned_sec4.append(f"- ... [{omitted_count} older historical revision(s) omitted for subagent context efficiency] ...")
    for b in recent_bullets:
        pruned_sec4.append(b)

    return content[:match.start(2)] + "\n".join(pruned_sec4) + "\n"

def pack_context(
    domain: Optional[str] = None,
    module: Optional[str] = None,
    target: Optional[str] = None,
    include_adrs: bool = True,
    full_history: bool = False,
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

    # 4. Optional ADRs (Only active, non-archived ADRs)
    if include_adrs:
        adrs_dir = DOCS_DIR / "decisions"
        if adrs_dir.exists():
            for adr in sorted(adrs_dir.glob("ADR-*.md")):
                if is_active_adr(adr):
                    targets_to_read.add(adr)

    # Build the bundle
    sections: List[str] = []

    # Header
    sections.append("# AGENT CONTEXT PACK: DOC-TO-CODE HARNESS")
    sections.append("> Generated for targeted autonomous agent execution.")
    sections.append("")

    # Agent Blueprint Excerpt
    if AGENT_SYSTEM_PROMPT.exists():
        sections.append("## 0. AGENT CORE DIRECTIVES & ESCALATION RULE")
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
            if not full_history:
                content = prune_section_4_for_context(content, max_revisions=3)
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
    parser.add_argument("--full-history", action="store_true", help="Include full Section 4 revision history without pruning")

    args = parser.parse_args()

    pack = pack_context(
        domain=args.domain,
        module=args.module,
        target=args.target,
        include_adrs=not args.no_adrs,
        full_history=args.full_history,
        output_path=args.output
    )

    if not args.output:
        print("\n" + "=" * 65)
        print(pack[:1500] + ("\n... [truncated preview, use -o to save full pack] ..." if len(pack) > 1500 else ""))
        print("=" * 65)

if __name__ == "__main__":
    main()
