#!/usr/bin/env python3
"""
Unified Agentic Harness CLI
The single entry point for all repository governance, linting, scaffolding,
context ingestion, and audit operations.
"""
import sys
import subprocess
import argparse
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPTS_DIR = Path("scripts")

def run_script(script_name: str, args: list) -> int:
    target = SCRIPTS_DIR / script_name
    if not target.exists():
        print(f"❌ Error: Script '{target}' not found.")
        return 1
    cmd = [sys.executable, str(target)] + args
    result = subprocess.run(cmd)
    return result.returncode

def main():
    parser = argparse.ArgumentParser(
        prog="harness",
        description="Unified Doc-to-Code Autonomous Harness CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available harness commands")

    # Audit command
    subparsers.add_parser("audit", help="Run master 29-point repository health and parity audit")

    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Lint documentation structure, 4 sections, and links")
    lint_parser.add_argument("--strict", action="store_true", help="Fail on warnings or broken links")

    # Parity command
    subparsers.add_parser("parity", help="Check doc-to-code parity and detect architectural drift")

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest structured context into a document leaf")
    ingest_parser.add_argument("--target", required=True, help="Target markdown file")
    ingest_parser.add_argument("--section", required=True, help="Target section name")
    ingest_parser.add_argument("--content", required=True, help="Content to append")
    ingest_parser.add_argument("--summary", default="Context ingested into specification", help="Revision summary")

    # Scaffold command
    scaffold_parser = subparsers.add_parser("scaffold", help="Scaffold a new domain or technical module")
    scaffold_group = scaffold_parser.add_mutually_exclusive_group(required=True)
    scaffold_group.add_argument("--domain", help="Scaffold a product domain")
    scaffold_group.add_argument("--module", help="Scaffold a technical module")

    # Decision / ADR commands
    adr_parser = subparsers.add_parser("adr", help="Generate a formal Architecture Decision Record (ADR)")
    adr_parser.add_argument("title", help="Title of the architecture decision")
    adr_parser.add_argument("--context", default="Baseline decision context", help="Context for the decision")

    append_parser = subparsers.add_parser("append", help="Append an atomic decision log to target doc")
    append_parser.add_argument("target", help="Target documentation file")
    append_parser.add_argument("decision", help="Decision log text")

    # Bootstrap command
    bootstrap_parser = subparsers.add_parser("bootstrap", help="Bootstrap a new downstream project")
    bootstrap_parser.add_argument("--name", required=True, help="Project name")
    bootstrap_parser.add_argument("--description", default="New project bootstrapped from agentic template", help="Project description")

    # Install hooks command
    subparsers.add_parser("install-hooks", help="Install local Git pre-commit hooks")

    args, unknown = parser.parse_known_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "audit":
        sys.exit(run_script("audit_repo.py", unknown))
    elif args.command == "lint":
        cli_args = ["--strict"] if args.strict else []
        sys.exit(run_script("lint_docs.py", cli_args + unknown))
    elif args.command == "parity":
        sys.exit(run_script("check_doc_drift.py", unknown))
    elif args.command == "ingest":
        sys.exit(run_script("ingest_context.py", [
            "--target", args.target,
            "--section", args.section,
            "--content", args.content,
            "--summary", args.summary
        ] + unknown))
    elif args.command == "scaffold":
        cli_args = ["--domain", args.domain] if args.domain else ["--module", args.module]
        sys.exit(run_script("scaffold_module.py", cli_args + unknown))
    elif args.command == "adr":
        sys.exit(run_script("record_decision.py", ["--adr", args.title, "--context", args.context] + unknown))
    elif args.command == "append":
        sys.exit(run_script("record_decision.py", ["--append", args.target, args.decision] + unknown))
    elif args.command == "bootstrap":
        sys.exit(run_script("bootstrap_project.py", ["--name", args.name, "--description", args.description] + unknown))
    elif args.command == "install-hooks":
        sys.exit(run_script("install_hooks.py", unknown))

if __name__ == "__main__":
    main()
