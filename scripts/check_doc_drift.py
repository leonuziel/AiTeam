#!/usr/bin/env python3
"""
Doc-to-Code Parity & Drift Detector
Ensures that no code is written without a corresponding specification,
and flags orphaned specifications or undocumented implementations.
"""
import sys
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_DIR = Path("src")
DOCS_MODULES_DIR = Path("docs/tech/modules")
TESTS_DIR = Path("tests")

def check_drift() -> int:
    issues = 0
    print("🔍 Auditing doc-to-code parity & drift...")

    # 1. Inspect src/ modules
    src_modules = [p for p in SRC_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")] if SRC_DIR.exists() else []
    doc_modules = [p for p in DOCS_MODULES_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")] if DOCS_MODULES_DIR.exists() else []

    src_names = {p.name for p in src_modules}
    doc_names = {p.name for p in doc_modules}

    # Check for un-documented code modules
    for name in src_names:
        if name not in doc_names:
            print(f"  ❌ Undocumented code module: 'src/{name}' has no matching spec in 'docs/tech/modules/{name}'!")
            issues += 1

    # Check for module docs without implementation scaffolding
    for name in doc_names:
        if name not in src_names:
            print(f"  ℹ️  Spec awaiting implementation: 'docs/tech/modules/{name}' (no code under 'src/{name}' yet).")

    # Check for code without tests
    if TESTS_DIR.exists():
        test_names = {p.name for p in TESTS_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")}
        for name in src_names:
            if name not in test_names:
                print(f"  ⚠️  Missing test folder: 'src/{name}' has no corresponding 'tests/{name}'!")

    print("-" * 60)
    if issues > 0:
        print(f"❌ Parity audit FAILED with {issues} drift violation(s).")
        return 1
    else:
        print("✨ Doc-to-code parity audit PASSED! Zero undocumented modules detected.")
        return 0

if __name__ == "__main__":
    sys.exit(check_drift())
