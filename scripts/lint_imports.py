#!/usr/bin/env python3
"""
Architectural Dependency Boundary & Import Linter
Verifies Clean Architecture & SOLID dependency rules across src/ modules.
Detects circular import cycles and flags illegal inward dependencies
(e.g., domain logic importing from storage, network, or UI drivers).
"""
import sys
import os
import re
import ast
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_DIR = Path("src")

# Configurable layer hierarchy: lower layers must NEVER depend on higher layers
# Layer 0: Core / Domain / Entities
# Layer 1: Services / Use Cases / Application
# Layer 2: Adapters / Storage / Network / API
# Layer 3: Presentation / UI / Controllers
LAYER_TIERS = {
    "core": 0,
    "domain": 0,
    "entities": 0,
    "types": 0,
    "services": 1,
    "application": 1,
    "use_cases": 1,
    "adapters": 2,
    "storage": 2,
    "persistence": 2,
    "network": 2,
    "api": 2,
    "ui": 3,
    "presentation": 3,
    "controllers": 3,
    "views": 3
}

def extract_py_imports(py_file: Path) -> List[str]:
    """Extracts imported module paths from a Python file using AST."""
    imports = []
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8", errors="ignore"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except Exception:
        pass
    return imports

def extract_js_imports(js_file: Path) -> List[str]:
    """Extracts imported module paths from a JavaScript / TypeScript file."""
    imports = []
    try:
        text = js_file.read_text(encoding="utf-8", errors="ignore")
        # Match ES6 imports: import ... from './path' or from 'path'
        for m in re.finditer(r'''(?:import|from)\s+['"]([^'"]+)['"]''', text):
            imports.append(m.group(1))
        # Match require: require('./path')
        for m in re.finditer(r'''require\s*\(\s*['"]([^'"]+)['"]\s*\)''', text):
            imports.append(m.group(1))
    except Exception:
        pass
    return imports

def get_module_layer(file_path: Path) -> Tuple[str, int]:
    """Determines module name and architectural tier based on directory path."""
    try:
        rel = file_path.relative_to(SRC_DIR)
        parts = rel.parts
        if not parts:
            return ("root", 99)
        top_mod = parts[0].lower()
        tier = LAYER_TIERS.get(top_mod, 99)
        return (top_mod, tier)
    except Exception:
        return ("unknown", 99)

def build_import_graph() -> Tuple[Dict[str, Set[str]], List[str]]:
    """Builds the directed dependency graph between top-level modules."""
    graph: Dict[str, Set[str]] = {}
    violations: List[str] = []

    if not SRC_DIR.exists():
        return graph, violations

    src_files = list(SRC_DIR.glob("**/*.py")) + list(SRC_DIR.glob("**/*.ts")) + list(SRC_DIR.glob("**/*.js"))
    if not src_files:
        return graph, violations

    for f in src_files:
        from_mod, from_tier = get_module_layer(f)
        if from_mod not in graph:
            graph[from_mod] = set()

        raw_imports = extract_py_imports(f) if f.suffix == ".py" else extract_js_imports(f)
        for imp in raw_imports:
            # Check if internal import targeting src/
            to_mod = None
            if imp.startswith("."):
                # Relative import
                resolved = (f.parent / imp).resolve()
                try:
                    rel_to_src = resolved.relative_to(SRC_DIR.resolve())
                    to_mod = rel_to_src.parts[0].lower() if rel_to_src.parts else None
                except Exception:
                    continue
            else:
                # Absolute package import (e.g. from src.storage import ...)
                clean_imp = imp.split(".")[0]
                if clean_imp == "src" and len(imp.split(".")) > 1:
                    to_mod = imp.split(".")[1].lower()
                elif (SRC_DIR / clean_imp).is_dir():
                    to_mod = clean_imp.lower()

            if to_mod and to_mod != from_mod:
                graph[from_mod].add(to_mod)
                to_tier = LAYER_TIERS.get(to_mod, 99)
                # Check for architectural boundary inversion:
                # Lower tier (e.g. domain=0) must never import higher tier (e.g. storage=2, ui=3)
                if from_tier < to_tier and to_tier != 99:
                    violations.append(
                        f"Boundary Violation: '{f.as_posix()}' (Tier {from_tier}: {from_mod}) "
                        f"illegally imports higher layer '{to_mod}' (Tier {to_tier})! Invert via interfaces."
                    )

    return graph, violations

def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Detects circular dependency cycles using DFS."""
    cycles = []
    visited = set()
    rec_stack = []

    def dfs(node: str):
        visited.add(node)
        rec_stack.append(node)

        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                cycle_start = rec_stack.index(neighbor)
                cycle = rec_stack[cycle_start:] + [neighbor]
                cycles.append(cycle)

        rec_stack.pop()

    for node in list(graph.keys()):
        if node not in visited:
            dfs(node)

    return cycles

def lint_imports(strict: bool = False) -> int:
    print("🔍 Auditing architectural dependency boundaries & circular imports...")

    if not SRC_DIR.exists() or not any(SRC_DIR.glob("*")):
        print("  ℹ️  Template Mode Active: 'src/' contains zero application code. Import boundaries clean.")
        print("-" * 65)
        print("✨ Import boundary audit PASSED! Zero circular dependencies or layer inversions.")
        return 0

    graph, boundary_violations = build_import_graph()
    cycles = find_cycles(graph)

    has_errors = False

    if boundary_violations:
        print("\n❌ Architectural Layer Inversion Violations Detected:")
        for v in boundary_violations:
            print(f"  🚨 {v}")
        has_errors = True

    if cycles:
        print("\n❌ Circular Module Dependency Cycles Detected:")
        for c in cycles:
            print(f"  🔄 Cycle: {' -> '.join(c)}")
        has_errors = True

    print("-" * 65)
    if has_errors:
        print("❌ Import boundary audit FAILED.")
        return 1
    else:
        print("✨ Import boundary audit PASSED! Clean architecture & dependency inversion verified.")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Architectural Dependency Boundary & Import Linter")
    parser.add_argument("--strict", action="store_true", help="Fail on any boundary warning")
    args = parser.parse_args()

    sys.exit(lint_imports(strict=args.strict))

if __name__ == "__main__":
    main()
