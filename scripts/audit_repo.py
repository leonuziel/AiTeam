#!/usr/bin/env python3
"""
Master Repository Health & Agentic Readiness Auditor
Performs end-to-end checks across docs structure, parity, configuration, and templates.
"""
import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CORE_FILES = [
    "ARCHITECTURE.md",
    "meta_generator_guide.md",
    "agent_system_prompt.md",
    "agent_extensions.md",
    "README.md",
    "AGENTS.md",
    "GEMINI.md",
    ".agent/config.json",
    ".agent/workflows/context_ingestion_loop.md",
    ".agent/workflows/requirement_digestion_loop.md",
    ".agent/workflows/design_resolution_loop.md",
    ".agent/workflows/autonomous_pipeline_loop.md",
    ".agent/workflows/doc_sync_loop.md",
    ".agent/workflows/escalation_loop.md",
    ".agent/workflows/code_review_loop.md",
    ".agent/workflows/continuous_cleanliness_loop.md",
    ".agent/workflows/doc_compaction_loop.md",
    "scripts/harness.py",
    "scripts/compact_docs.py",
    "scripts/checkpoint_state.py",
    "scripts/scan_secrets.py",
    "scripts/autopilot.py",
    "scripts/lint_imports.py",
    "scripts/lint_docs.py",
    "scripts/scaffold_module.py",
    "scripts/record_decision.py",
    "scripts/ingest_context.py",
    "scripts/check_doc_drift.py",
    "scripts/bootstrap_project.py",
    "scripts/install_hooks.py",
    ".githooks/pre-commit",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "templates/leaf-template.md",
    "templates/domain-template.md",
    "templates/module-template.md",
    "templates/api-contract-template.md",
    "templates/decision-record-template.md",
    "docs/decisions/README.md",
    ".agents/skills/doc-harness/SKILL.md",
    ".agents/skills/design-interviewer/SKILL.md",
    "scripts/generate_invariant_tests.py",
    ".devcontainer/devcontainer.json",
    "scripts/resolve_question.py",
    "scripts/generate_doc_index.py",
    "docs/INDEX.md",
    "CHANGELOG.md",
    "docs/CHANGELOG.md",
    "docs/operations/changelist.md",
    ".agent/workflows/changelist_tracking_loop.md",
    "scripts/track_changelist.py",
    "scripts/pack_context.py",
    "scripts/run_tests.py",
    "LICENSE",
    "SECURITY.md",
    "mcp_config.json"
]

def run_step(title: str, command: list) -> bool:
    print(f"\n▶ Running: {title}...")
    result = subprocess.run([sys.executable] + command, capture_output=True, text=True, encoding="utf-8")
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip())
        print(f"❌ {title} FAILED with return code {result.returncode}")
        return False
    return True

def audit():
    total_checks = 0
    passed_checks = 0

    print("=" * 65)
    print("🛡️  MASTER REPOSITORY HEALTH & AGENTIC READINESS AUDIT")
    print("=" * 65)

    # 1. Core Files Verification
    print("\n▶ Verifying core harness files...")
    all_files_present = True
    for file_str in CORE_FILES:
        total_checks += 1
        path = Path(file_str)
        if path.exists():
            passed_checks += 1
            print(f"  ✅ {file_str}")
        else:
            print(f"  ❌ Missing required file: {file_str}")
            all_files_present = False

    # 2. Doc Linting Check
    total_checks += 1
    if run_step("Structural Documentation Linting", ["scripts/lint_docs.py", "--strict"]):
        passed_checks += 1

    # 3. Doc-to-Code Parity Check
    total_checks += 1
    if run_step("Doc-to-Code Parity & Drift Check", ["scripts/check_doc_drift.py"]):
        passed_checks += 1

    # 4. Living Documentation Index Check
    total_checks += 1
    if run_step("Living Documentation Index Completeness", ["scripts/generate_doc_index.py", "--check"]):
        passed_checks += 1

    # 5. Changelist Tracking Integrity Check
    total_checks += 1
    if run_step("Changelist Tracking Integrity", ["scripts/track_changelist.py", "verify"]):
        passed_checks += 1

    # 6. Automated Invariant & Unit Test Suite
    total_checks += 1
    if run_step("Automated Invariant & Unit Test Suite", ["scripts/run_tests.py"]):
        passed_checks += 1

    # 7. Documentation Lifecycle & Compaction Health
    total_checks += 1
    if run_step("Documentation Lifecycle & Compaction Health", ["scripts/compact_docs.py", "--audit", "--strict"]):
        passed_checks += 1

    # 8. Secret & Credential Leakage Audit
    total_checks += 1
    if run_step("Secret & Credential Leakage Audit", ["scripts/scan_secrets.py"]):
        passed_checks += 1

    # 9. Architectural Dependency Boundary & Import Audit
    total_checks += 1
    if run_step("Architectural Dependency Boundary & Import Audit", ["scripts/lint_imports.py", "--strict"]):
        passed_checks += 1

    # Summary
    score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    print("\n" + "=" * 65)
    print(f"📊 Audit Summary: {passed_checks}/{total_checks} checks passed ({score:.1f}% health score)")
    print("=" * 65)

    if score == 100.0:
        print("🚀 Template is in PRISTINE condition and ready for project bootstrapping!")
        return 0
    else:
        print(f"⚠️  Template has {total_checks - passed_checks} unresolved audit issue(s).")
        return 1

if __name__ == "__main__":
    sys.exit(audit())
