#!/usr/bin/env python3
"""
Interactive & Scriptable Decision Resolver
Enables agents and human architects to resolve design question forks,
automatically generate Architecture Decision Records (ADRs), and append
atomic revision logs to the target specification document.
"""
import sys
import argparse
import subprocess
from pathlib import Path

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


def interactive_resolve():
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

    print("\n▶ Executing ADR generation & revision logging...")
    
    # 1. Create ADR
    rc1 = run_record_decision(["--adr", title, "--context", f"{context} (Decision: {choice})"])
    if rc1 != 0:
        return rc1

    # 2. Append revision to target doc
    rev_log = f"Resolved design fork: adopted '{choice}'. See ADR for full context."
    rc2 = run_record_decision(["--append", target, rev_log])
    if rc2 != 0:
        return rc2

    print(f"\n✨ Decision successfully locked! Updated '{target}' and generated ADR.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a design fork and sync docs & ADRs")
    parser.add_argument("--title", help="Decision title")
    parser.add_argument("--target", help="Target document path")
    parser.add_argument("--choice", help="Selected option summary")
    parser.add_argument("--context", default="", help="Context & trade-off rationale")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive prompt")
    args = parser.parse_args()

    # If interactive flag or no arguments provided and stdin is a TTY
    if args.interactive or (not args.title and not args.target and sys.stdin.isatty()):
        return interactive_resolve()

    if not args.title or not args.target or not args.choice:
        parser.print_help()
        print("\n❌ Error: --title, --target, and --choice are required for non-interactive execution.")
        return 1

    target_path = Path(args.target)
    if not target_path.exists():
        print(f"❌ Error: Target specification '{args.target}' does not exist.")
        return 1

    context = args.context or f"Adopted '{args.choice}' after evaluating architectural trade-offs."

    # 1. Create ADR
    rc1 = run_record_decision(["--adr", args.title, "--context", f"{context} (Decision: {args.choice})"])
    if rc1 != 0:
        return rc1

    # 2. Append to target doc
    rev_log = f"Resolved design fork: adopted '{args.choice}'. See ADR for rationale."
    rc2 = run_record_decision(["--append", args.target, rev_log])
    if rc2 != 0:
        return rc2

    print(f"✨ Decision '{args.title}' successfully recorded and synced to '{args.target}'!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
