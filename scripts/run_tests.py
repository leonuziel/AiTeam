#!/usr/bin/env python3
"""
Unified Invariant & Unit Test Runner
Runs the full test suite and verifies 100% test coverage for documented invariants.
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

SCRIPTS_DIR = Path("scripts")
TESTS_DIR = Path("tests")

def run_tests() -> int:
    print("=" * 65)
    print("🧪 DOC-TO-CODE INVARIANT & TEST RUNNER")
    print("=" * 65)

    # 1. Audit Invariant Test Coverage
    print("\n▶ Verifying invariant test coverage against docs/...")
    gen_script = SCRIPTS_DIR / "generate_invariant_tests.py"
    if gen_script.exists():
        res = subprocess.run([sys.executable, str(gen_script), "--check"], capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            print("  ⚠️  Invariant test suite is out of date. Auto-generating fresh invariant tests...")
            subprocess.run([sys.executable, str(gen_script)], check=True)
        else:
            print(res.stdout.strip())
    else:
        print("  ⚠️  generate_invariant_tests.py not found.")

    # 2. Run Test Suite
    print("\n▶ Executing test suite in 'tests/'...")
    # Check if pytest is available
    use_pytest = False
    try:
        chk = subprocess.run(["pytest", "--version"], capture_output=True)
        if chk.returncode == 0:
            use_pytest = True
    except Exception:
        use_pytest = False

    if use_pytest:
        print("  ℹ️  Running with pytest...")
        cmd = ["pytest", "tests"]
    else:
        print("  ℹ️  Running with built-in unittest discovery...")
        cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests"]

    result = subprocess.run(cmd)
    
    print("\n" + "=" * 65)
    if result.returncode == 0:
        print("✨ All unit and invariant verification tests PASSED!")
    else:
        print("❌ Test execution FAILED. Check test failures above.")
    print("=" * 65)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
