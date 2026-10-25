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

    # Test-gen / invariants command
    testgen_parser = subparsers.add_parser("test-gen", help="Generate invariant test stubs from documentation")
    testgen_parser.add_argument("--output", "-o", default="tests/test_invariants.py", help="Output test file path")
    testgen_parser.add_argument("--check", action="store_true", help="Audit if test file covers all invariants")

    # Resolve command
    resolve_parser = subparsers.add_parser("resolve", help="Resolve a design fork and sync docs & ADRs")
    resolve_parser.add_argument("--title", help="Decision title")
    resolve_parser.add_argument("--target", help="Target document path")
    resolve_parser.add_argument("--choice", help="Selected option summary")
    resolve_parser.add_argument("--context", default="", help="Context & trade-off rationale")
    resolve_parser.add_argument("--interactive", action="store_true", help="Launch interactive prompt")

    # Index command
    index_parser = subparsers.add_parser("index", help="Generate or audit living documentation index")
    index_parser.add_argument("--check", action="store_true", help="Audit if index covers all documents")
    index_parser.add_argument("--output", "-o", default="docs/INDEX.md", help="Output index path")

    # Install hooks command
    subparsers.add_parser("install-hooks", help="Install local Git pre-commit hooks")

    # Changelist command
    changelist_parser = subparsers.add_parser("changelist", help="Track, generate, release, or verify changelist entries")
    changelist_parser.add_argument("action", nargs="?", default="verify", help="Changelist action (verify, record, generate, release)")

    # Test runner command
    subparsers.add_parser("test", help="Run full unit and invariant verification test suite")

    # Pack context command
    pack_parser = subparsers.add_parser("pack", help="Pack targeted context, specs, and invariants for subagents")
    pack_parser.add_argument("--domain", help="Product domain to include")
    pack_parser.add_argument("--module", help="Technical module to include")
    pack_parser.add_argument("--target", help="Specific document to pack")
    pack_parser.add_argument("--output", "-o", help="Output path for context pack")
    pack_parser.add_argument("--no-adrs", action="store_true", help="Exclude architecture decision records")

    # Compact command
    compact_parser = subparsers.add_parser("compact", help="Audit and compact historical Section 4 revisions and archive superseded ADRs")
    compact_parser.add_argument("--audit", action="store_true", help="Audit docs for revision bloat")
    compact_parser.add_argument("--threshold", type=int, default=8, help="Revision count threshold before flagging bloat")
    compact_parser.add_argument("--squash", help="Target document path to squash historical Section 4 revisions")
    compact_parser.add_argument("--squash-all", action="store_true", help="Batch squash all documents exceeding threshold")
    compact_parser.add_argument("--archive-adrs", action="store_true", help="Move superseded/deprecated ADRs to archive/")
    compact_parser.add_argument("--strict", action="store_true", help="Fail if bloat is detected")

    # Checkpoint command
    checkpoint_parser = subparsers.add_parser("checkpoint", help="Manage repository state checkpoints and autonomous rollbacks")
    checkpoint_parser.add_argument("action", nargs="?", default="list", choices=["create", "restore", "list", "drop"], help="Checkpoint action")
    checkpoint_parser.add_argument("name", nargs="?", default="", help="Checkpoint name or ID")

    # Scan-secrets command
    scan_secrets_parser = subparsers.add_parser("scan-secrets", help="Scan repository or staged changes for exposed credentials and API keys")
    scan_secrets_parser.add_argument("--staged", action="store_true", help="Scan only git staged files")
    scan_secrets_parser.add_argument("--path", help="Scan a specific file or directory")

    # Autopilot / Turbo command
    autopilot_parser = subparsers.add_parser("autopilot", aliases=["next"], help="Inspect active roadmap & task queue for continuous turbo execution")
    autopilot_parser.add_argument("--complete", "-c", help="Mark a task as completed in active roadmap")
    autopilot_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

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
    elif args.command == "resolve":
        cli_args = []
        if args.title:
            cli_args += ["--title", args.title]
        if args.target:
            cli_args += ["--target", args.target]
        if args.choice:
            cli_args += ["--choice", args.choice]
        if args.context:
            cli_args += ["--context", args.context]
        if args.interactive:
            cli_args += ["--interactive"]
        sys.exit(run_script("resolve_question.py", cli_args + unknown))
    elif args.command == "index":
        cli_args = ["--output", args.output]
        if args.check:
            cli_args.append("--check")
        sys.exit(run_script("generate_doc_index.py", cli_args + unknown))
    elif args.command == "test-gen":
        cli_args = ["--output", args.output]
        if args.check:
            cli_args.append("--check")
        sys.exit(run_script("generate_invariant_tests.py", cli_args + unknown))
    elif args.command == "bootstrap":
        sys.exit(run_script("bootstrap_project.py", ["--name", args.name, "--description", args.description] + unknown))
    elif args.command == "install-hooks":
        sys.exit(run_script("install_hooks.py", unknown))
    elif args.command == "changelist":
        cli_args = [args.action] if args.action else []
        sys.exit(run_script("track_changelist.py", cli_args + unknown))
    elif args.command == "test":
        sys.exit(run_script("run_tests.py", unknown))
    elif args.command == "pack":
        cli_args = []
        if args.domain:
            cli_args += ["--domain", args.domain]
        if args.module:
            cli_args += ["--module", args.module]
        if args.target:
            cli_args += ["--target", args.target]
        if args.output:
            cli_args += ["-o", args.output]
        if args.no_adrs:
            cli_args += ["--no-adrs"]
        sys.exit(run_script("pack_context.py", cli_args + unknown))
    elif args.command == "compact":
        cli_args = []
        if args.audit:
            cli_args.append("--audit")
        if args.threshold != 8:
            cli_args += ["--threshold", str(args.threshold)]
        if args.squash:
            cli_args += ["--squash", args.squash]
        if args.squash_all:
            cli_args.append("--squash-all")
        if args.archive_adrs:
            cli_args.append("--archive-adrs")
        if args.strict:
            cli_args.append("--strict")
        sys.exit(run_script("compact_docs.py", cli_args + unknown))
    elif args.command == "checkpoint":
        cli_args = [args.action]
        if args.name:
            cli_args.append(args.name)
        sys.exit(run_script("checkpoint_state.py", cli_args + unknown))
    elif args.command == "scan-secrets":
        cli_args = []
        if args.staged:
            cli_args.append("--staged")
        if args.path:
            cli_args += ["--path", args.path]
        sys.exit(run_script("scan_secrets.py", cli_args + unknown))
    elif args.command in ("autopilot", "next"):
        cli_args = []
        if args.complete:
            cli_args += ["--complete", args.complete]
        if args.json:
            cli_args.append("--json")
        sys.exit(run_script("autopilot.py", cli_args + unknown))

if __name__ == "__main__":
    main()
