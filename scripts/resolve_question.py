#!/usr/bin/env python3
"""
Interactive & Machine-Readable Decision Resolver
Enables agents and human architects to resolve design question forks,
automatically generate Architecture Decision Records (ADRs), and append
atomic revision logs to the target specification document.
Supports structured JSON decision packages for machine-enforced escalation.
"""
import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPTS_DIR = Path("scripts")
RECORD_DECISION_SCRIPT = SCRIPTS_DIR / "record_decision.py"

def run_record_decision(args: list) -> int:
    cmd = [sys.executable, str(RECORD_DECISION_SCRIPT)] + args
    res = subprocess.run(cmd)
    return res.returncode

def resolve_from_package(data: Dict[str, Any]) -> int:
    """Resolves an architectural fork using a machine-readable JSON package."""
    title = data.get("title", "").strip()
    target = data.get("target_doc", "").strip()
    choice = data.get("selected_option", "").strip()
    ambiguity = data.get("ambiguity", "").strip()
    trade_offs = data.get("trade_offs", "").strip()
    alternatives = data.get("alternatives", [])

    if not title:
        print("❌ Error: Decision package missing required field: 'title'")
        return 1
    if not target:
        print("❌ Error: Decision package missing required field: 'target_doc'")
        return 1
    if not choice:
        print("❌ Error: Decision package missing required field: 'selected_option'")
        return 1

    target_path = Path(target)
    if not target_path.exists():
        print(f"❌ Error: Target specification '{target}' does not exist.")
        return 1

    context_lines = []
    if ambiguity:
        context_lines.append(f"Ambiguity / Context: {ambiguity}")
    if trade_offs:
        context_lines.append(f"Trade-offs: {trade_offs}")
    if alternatives:
        alts_str = ", ".join(alternatives)
        context_lines.append(f"Evaluated Alternatives: {alts_str}")
    context_lines.append(f"Decision: {choice}")

    full_context = " | ".join(context_lines)

    # 1. Create ADR
    rc1 = run_record_decision(["--adr", title, "--context", full_context])
    if rc1 != 0:
        return rc1

    # 2. Append revision to target doc
    rev_log = f"Resolved design fork: adopted '{choice}'. See ADR for trade-offs."
    rc2 = run_record_decision(["--append", target, rev_log])
    if rc2 != 0:
        return rc2

    print(f"\n✨ Decision Package '{title}' successfully locked and recorded to '{target}'!")
    return 0

def scaffold_blank_package() -> str:
    template = {
        "title": "Decision Title Here",
        "target_doc": "docs/tech/modules/example.md",
        "ambiguity": "Description of the unhandled edge case or design fork",
        "selected_option": "Option A: Description of adopted solution",
        "trade_offs": "Analysis of trade-offs, benefits, and architectural implications",
        "alternatives": [
            "Option B: Description of rejected alternative",
            "Option C: Description of another alternative"
        ]
    }
    return json.dumps(template, indent=2)

def interactive_resolve() -> int:
    print("=" * 65)
    print("🤝 Doc-to-Code Design Fork Resolver")
    print("=" * 65)
    print("Resolve an architectural fork and record it into the specification.\n")

    title = input("1. Decision Title (e.g., 'Adopt Redis for Token Denylist'): ").strip()
    if not title:
        print("❌ Error: Decision title cannot be empty.")
        return 1

    target = input("2. Target Spec Document (e.g., 'docs/tech/api/contracts.md'): ").strip()
    if not target or not Path(target).exists():
        print(f"❌ Error: Target specification '{target}' does not exist.")
        return 1

    choice = input("3. Selected Option / Decision Summary: ").strip()
    if not choice:
        print("❌ Error: Selected option cannot be empty.")
        return 1

    context = input("4. Rationale / Context (optional): ").strip()
    if not context:
        context = f"Adopted '{choice}' after evaluating architectural trade-offs."

    data = {
        "title": title,
        "target_doc": target,
        "selected_option": choice,
        "ambiguity": context
    }
    return resolve_from_package(data)

def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a design fork and sync docs & ADRs")
    parser.add_argument("--title", help="Decision title")
    parser.add_argument("--target", help="Target document path")
    parser.add_argument("--choice", help="Selected option summary")
    parser.add_argument("--context", default="", help="Context & trade-off rationale")
    parser.add_argument("--package", help="JSON string or path to JSON decision package file")
    parser.add_argument("--scaffold-package", action="store_true", help="Print a blank JSON escalation decision package")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive prompt")
    args = parser.parse_args()

    if args.scaffold_package:
        print(scaffold_blank_package())
        return 0

    if args.package:
        pkg_str = args.package.strip()
        pkg_path = Path(pkg_str)
        if pkg_path.exists() and pkg_path.is_file():
            try:
                data = json.loads(pkg_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"❌ Error: Failed to parse JSON package file '{pkg_path}': {e}")
                return 1
        else:
            try:
                data = json.loads(pkg_str)
            except Exception as e:
                print(f"❌ Error: Failed to parse JSON package string: {e}")
                return 1
        return resolve_from_package(data)

    if args.interactive or (not args.title and not args.target and sys.stdin.isatty()):
        return interactive_resolve()

    if not args.title or not args.target or not args.choice:
        parser.print_help()
        print("\n❌ Error: --title, --target, and --choice (or --package) are required for non-interactive execution.")
        return 1

    data = {
        "title": args.title,
        "target_doc": args.target,
        "selected_option": args.choice,
        "ambiguity": args.context
    }
    return resolve_from_package(data)

if __name__ == "__main__":
    sys.exit(main())
