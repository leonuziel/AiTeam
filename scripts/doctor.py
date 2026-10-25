#!/usr/bin/env python3
"""
Template Self-Diagnostic & Auto-Repair Sentinel (harness doctor)
Runs full repository diagnostics and optionally applies automated self-healing repairs.
"""
import sys
import subprocess
from pathlib import Path
import argparse

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_step(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, capture_output=True, encoding="utf-8", errors="replace", check=False)
        return res.returncode == 0, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def diagnose_repository(fix_mode=False, verbose=False):
    repo_root = Path(__file__).resolve().parent.parent
    print("🩺 =================================================================")
    print("🩺  TEMPLATE SELF-DIAGNOSTIC & AUTO-REPAIR SENTINEL")
    print("🩺 =================================================================")
    if fix_mode:
        print("  🔧 AUTO-REPAIR MODE ENABLED: Automated healing will be applied.")

    issues = []
    fixes_applied = []

    # 1. Python Runtime
    py_ver = sys.version_info
    if py_ver < (3, 8):
        issues.append(f"Python version {py_ver.major}.{py_ver.minor} is below minimum requirement 3.8")
    else:
        print(f"  ✅ Python Runtime: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")

    # 2. Git Hooks Configuration
    ok, out, _ = run_step(["git", "config", "core.hooksPath"], cwd=repo_root)
    git_hooks_path = out.strip()
    hooks_installed = (git_hooks_path == ".githooks") or (repo_root / ".git" / "hooks" / "pre-commit").exists()
    
    if not hooks_installed:
        issues.append("Git pre-commit hooks are not configured or inactive.")
        if fix_mode:
            print("  🔧 Auto-repairing Git hooks...")
            f_ok, f_out, _ = run_step([sys.executable, "scripts/install_hooks.py"], cwd=repo_root)
            if f_ok:
                fixes_applied.append("Activated Git pre-commit hooks via install_hooks.py")
                print("     -> Pre-commit hooks successfully installed.")
            else:
                print("     -> Failed to install Git hooks.")
    else:
        print("  ✅ Git Pre-Commit Hooks: Active")

    # 3. Essential Directory Hierarchy
    essential_dirs = [
        "docs",
        "docs/decisions",
        "docs/tech",
        "scripts",
        "templates",
        ".agent",
        ".githooks",
        "tests",
    ]
    missing_dirs = []
    for d in essential_dirs:
        dir_path = repo_root / d
        if not dir_path.is_dir():
            missing_dirs.append(d)
            if fix_mode:
                dir_path.mkdir(parents=True, exist_ok=True)
                fixes_applied.append(f"Created missing directory '{d}'")

    if missing_dirs and not fix_mode:
        issues.append(f"Missing essential directories: {', '.join(missing_dirs)}")
    else:
        print("  ✅ Directory Structure Invariants: Healthy")

    # 4. Living Documentation Index Check
    index_script = repo_root / "scripts" / "generate_doc_index.py"
    if index_script.exists():
        ok, out, _ = run_step([sys.executable, "scripts/generate_doc_index.py", "--check"], cwd=repo_root)
        if not ok:
            issues.append("Documentation index 'docs/INDEX.md' is stale or incomplete.")
            if fix_mode:
                print("  🔧 Auto-regenerating 'docs/INDEX.md'...")
                f_ok, _, _ = run_step([sys.executable, "scripts/generate_doc_index.py"], cwd=repo_root)
                if f_ok:
                    fixes_applied.append("Re-generated docs/INDEX.md")
                    print("     -> docs/INDEX.md updated.")
        else:
            print("  ✅ Living Documentation Index: Synchronized")

    # 5. Invariant Test Stubs Check
    testgen_script = repo_root / "scripts" / "generate_invariant_tests.py"
    if testgen_script.exists():
        ok, out, _ = run_step([sys.executable, "scripts/generate_invariant_tests.py", "--check"], cwd=repo_root)
        if not ok:
            issues.append("Invariant test coverage stubs in 'tests/invariants/' are missing or incomplete.")
            if fix_mode:
                print("  🔧 Auto-generating missing invariant test stubs...")
                f_ok, _, _ = run_step([sys.executable, "scripts/generate_invariant_tests.py"], cwd=repo_root)
                if f_ok:
                    fixes_applied.append("Generated missing invariant test stubs in tests/invariants/")
                    print("     -> Invariant test stubs generated.")
        else:
            print("  ✅ Invariant Verification Stubs: 100% Coverage")

    # 6. Phantom Sentinel Check
    sentinel_script = repo_root / "scripts" / "phantom_sentinel.py"
    if sentinel_script.exists():
        ok, out, _ = run_step([sys.executable, "scripts/phantom_sentinel.py", "--strict"], cwd=repo_root)
        if not ok:
            issues.append("Phantom files, broken imports, or hallucinated markdown links detected.")
        else:
            print("  ✅ Phantom File Sentinel: Clean")

    # 7. Documentation Hierarchy (DAG) Check
    dag_script = repo_root / "scripts" / "lint_doc_dag.py"
    if dag_script.exists():
        ok, out, _ = run_step([sys.executable, "scripts/lint_doc_dag.py", "--strict"], cwd=repo_root)
        if not ok:
            issues.append("Documentation tier inversions or broken cross-references detected.")
        else:
            print("  ✅ Documentation Hierarchy & DAG: Clean")

    # 8. Secret & Credential Leakage Check
    secret_script = repo_root / "scripts" / "scan_secrets.py"
    if secret_script.exists():
        ok, out, _ = run_step([sys.executable, "scripts/scan_secrets.py"], cwd=repo_root)
        if not ok:
            issues.append("Exposed secrets or credential leaks detected.")
        else:
            print("  ✅ Secret & Credential Leakage: Clean")

    # 9. Architectural Import Boundaries Check
    import_script = repo_root / "scripts" / "lint_imports.py"
    if import_script.exists():
        ok, out, _ = run_step([sys.executable, "scripts/lint_imports.py", "--strict"], cwd=repo_root)
        if not ok:
            issues.append("Architectural dependency boundary or circular import violations detected.")
        else:
            print("  ✅ Architectural Import Boundaries: Clean")

    # 10. Doc Compaction / Revision Bloat Check
    compaction_script = repo_root / "scripts" / "compact_docs.py"
    if compaction_script.exists():
        ok, out, _ = run_step([sys.executable, "scripts/compact_docs.py", "--audit", "--strict"], cwd=repo_root)
        if not ok:
            issues.append("Documentation revision bloat or unarchived superseded ADRs detected.")
            if fix_mode:
                print("  🔧 Auto-compacting documentation revision logs...")
                f_ok, _, _ = run_step([sys.executable, "scripts/compact_docs.py", "--squash-all", "--archive-adrs"], cwd=repo_root)
                if f_ok:
                    fixes_applied.append("Compacted bloated document revision histories & archived superseded ADRs")
                    print("     -> Documentation revisions squashed.")
        else:
            print("  ✅ Documentation Lifecycle & Revision Bloat: Healthy")

    # Summary
    print("\n🩺 =================================================================")
    if not issues or (fix_mode and len(fixes_applied) >= len(issues)):
        print("🎉 DIAGNOSTIC RESULT: ALL SYSTEMS OPERATIONAL (HEALTHY)")
        if fixes_applied:
            print("  ✨ Automated Repairs Applied:")
            for fix in fixes_applied:
                print(f"     - {fix}")
        print("🩺 =================================================================")
        return 0
    else:
        print(f"⚠️  DIAGNOSTIC RESULT: {len(issues)} ISSUE(S) DETECTED")
        for iss in issues:
            print(f"  ❌ {iss}")
        if not fix_mode:
            print("\n💡 TIP: Run 'python scripts/harness.py doctor --fix' to attempt automated repairs.")
        print("🩺 =================================================================")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Template Self-Diagnostic & Auto-Repair Sentinel")
    parser.add_argument("--fix", action="store_true", help="Automatically repair detected discrepancies")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose diagnostic output")
    args = parser.parse_args()

    sys.exit(diagnose_repository(fix_mode=args.fix, verbose=args.verbose))

if __name__ == "__main__":
    main()
