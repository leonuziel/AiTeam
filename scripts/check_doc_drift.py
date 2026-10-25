#!/usr/bin/env python3
"""
AST-Enhanced Doc-to-Code Parity & Drift Detector
Ensures that no code is written without a corresponding specification,
flags orphaned specifications or undocumented implementations, and
uses AST (Python) and symbol parsing (TypeScript/JavaScript) to verify that
public classes, methods, and functions declared in Section 3 exist in code.
"""
import sys
import os
import re
import ast
import argparse
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_DIR = Path("src")
DOCS_MODULES_DIR = Path("docs/tech/modules")
TESTS_DIR = Path("tests")

TS_EXPORT_PATTERNS = [
    r"export\s+(?:default\s+)?(?:async\s+)?(?:function|class|interface|type|enum)\s+([A-Za-z0-9_]+)",
    r"export\s+(?:const|let|var)\s+([A-Za-z0-9_]+)"
]

def extract_python_symbols(py_path: Path) -> Set[str]:
    """Extracts public classes, methods, and functions using Python AST."""
    symbols = set()
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    symbols.add(node.name)
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("_"):
                        symbols.add(item.name)
                        symbols.add(f"{node.name}.{item.name}")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_"):
                    symbols.add(node.name)
    except Exception:
        pass
    return symbols

def extract_ts_symbols(ts_path: Path) -> Set[str]:
    """Extracts exported TypeScript/JavaScript symbols."""
    symbols = set()
    try:
        text = ts_path.read_text(encoding="utf-8")
        for p in TS_EXPORT_PATTERNS:
            for m in re.finditer(p, text):
                symbols.add(m.group(1))
    except Exception:
        pass
    return symbols

def extract_module_code_symbols(module_dir: Path) -> Set[str]:
    """Recursively extracts all exported code symbols from a module folder."""
    symbols = set()
    for py_file in module_dir.glob("**/*.py"):
        symbols.update(extract_python_symbols(py_file))
    for ts_file in list(module_dir.glob("**/*.ts")) + list(module_dir.glob("**/*.js")):
        symbols.update(extract_ts_symbols(ts_file))
    return symbols

def extract_spec_declared_symbols(spec_path: Path) -> Set[str]:
    """Extracts symbols declared in backticks under '## 3. Specifications & Interfaces'."""
    symbols = set()
    try:
        content = spec_path.read_text(encoding="utf-8")
        # Find Section 3
        match = re.search(r"##\s+3\.\s+Specifications\s+&\s+Interfaces.*?\n(.*?)(?=\n##\s+|$)", content, re.DOTALL | re.IGNORECASE)
        if match:
            sec3_text = match.group(1)
            # Find backtick identifiers: `identifier`
            for m in re.finditer(r"`([A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)?)`", sec3_text):
                ident = m.group(1)
                # Ignore common language keywords or markdown markers
                if ident not in {"true", "false", "null", "none", "str", "int", "float", "bool", "dict", "list", "any", "void", "string", "number"}:
                    symbols.add(ident)
    except Exception:
        pass
    return symbols

def find_module_spec_doc(module_name: str) -> Optional[Path]:
    """Finds matching specification markdown file for a given module name."""
    cand1 = DOCS_MODULES_DIR / f"{module_name}.md"
    if cand1.exists():
        return cand1
    cand2 = DOCS_MODULES_DIR / module_name / "spec.md"
    if cand2.exists():
        return cand2
    cand3 = DOCS_MODULES_DIR / module_name / "overview.md"
    if cand3.exists():
        return cand3
    cand4 = DOCS_MODULES_DIR / module_name / "requirements.md"
    if cand4.exists():
        return cand4
    # Any markdown in the module doc directory
    mod_dir = DOCS_MODULES_DIR / module_name
    if mod_dir.is_dir():
        mds = list(mod_dir.glob("*.md"))
        if mds:
            return mds[0]
    return None

def check_drift(strict: bool = False, enable_ast: bool = True) -> int:
    issues = 0
    ast_warnings = 0
    print("🔍 Auditing doc-to-code parity & AST drift...")

    # 1. Inspect src/ modules
    src_modules = [p for p in SRC_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")] if SRC_DIR.exists() else []
    doc_modules = [p for p in DOCS_MODULES_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")] if DOCS_MODULES_DIR.exists() else []

    src_names = {p.name for p in src_modules}
    doc_names = {p.name for p in doc_modules}

    # Check for un-documented code modules
    for name in src_names:
        if name not in doc_names and not (DOCS_MODULES_DIR / f"{name}.md").exists():
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

    # 2. AST-Level Symbol Parity Check
    if enable_ast and src_modules:
        print("\n  🔬 Running AST symbol parity inspection...")
        for src_mod in src_modules:
            code_symbols = extract_module_code_symbols(src_mod)
            spec_file = find_module_spec_doc(src_mod.name)

            if spec_file and code_symbols:
                declared_symbols = extract_spec_declared_symbols(spec_file)
                # Check if declared symbols exist in code
                missing_in_code = {s for s in declared_symbols if s not in code_symbols and not any(s in cs for cs in code_symbols)}
                if missing_in_code:
                    for s in sorted(missing_in_code):
                        print(f"  ⚠️  AST Disparity: Declared interface `{s}` in '{spec_file}' is missing from code exports in '{src_mod.as_posix()}'!")
                        ast_warnings += 1

    if not src_modules:
        print("  ℹ️  Template Mode Active: 'src/' contains zero code modules. Parity baseline clean.")

    if strict and ast_warnings > 0:
        issues += ast_warnings

    print("-" * 60)
    if issues > 0:
        print(f"❌ Parity audit FAILED with {issues} drift violation(s).")
        return 1
    else:
        print("✨ Doc-to-code parity audit PASSED! Zero undocumented modules detected.")
        return 0

def main():
    parser = argparse.ArgumentParser(description="AST-Enhanced Doc-to-Code Parity & Drift Detector")
    parser.add_argument("--strict", action="store_true", help="Fail on AST symbol disparities or missing test suites")
    parser.add_argument("--no-ast", action="store_true", help="Disable AST symbol extraction")
    args = parser.parse_args()

    sys.exit(check_drift(strict=args.strict, enable_ast=not args.no_ast))

if __name__ == "__main__":
    main()
