#!/usr/bin/env python3
"""
Agent Hallucination Trap & Phantom File Sentinel
Scans source code imports and documentation path references to detect
hallucinated modules, non-existent relative imports, and phantom file paths
before they cause runtime exceptions or architectural drift.
"""
import sys
import os
import re
import ast
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_DIR = Path("src")
DOCS_DIR = Path("docs")

IGNORE_DIRS = {".git", ".agent", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}

def check_python_phantom_imports(py_file: Path) -> List[Dict]:
    """Inspects Python AST to ensure relative and internal imports resolve to real files."""
    phantoms = []
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return phantoms

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                # Relative import e.g. from .helpers import foo
                base_dir = py_file.parent
                for _ in range(node.level - 1):
                    base_dir = base_dir.parent
                rel_mod = node.module.replace(".", "/") if node.module else ""
                target_cand_py = base_dir / f"{rel_mod}.py"
                target_cand_init = base_dir / rel_mod / "__init__.py"
                target_cand_dir = base_dir / rel_mod

                if not (target_cand_py.exists() or target_cand_init.exists() or target_cand_dir.exists()):
                    phantoms.append({
                        "source": py_file.as_posix(),
                        "line": getattr(node, "lineno", 0),
                        "target": f"level={node.level} {node.module}",
                        "type": "Phantom Relative Python Import"
                    })
    return phantoms

def check_js_phantom_imports(js_file: Path) -> List[Dict]:
    """Inspects JS/TS relative imports to verify target files exist."""
    phantoms = []
    try:
        text = js_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return phantoms

    lines = text.splitlines()
    for line_idx, line in enumerate(lines, start=1):
        # Match relative imports: from './...' or require('./...')
        matches = re.findall(r'''(?:import|from|require)\s*\(?['"](\.[^'"]+)['"]\)?''', line)
        for rel_path in matches:
            # Strip query params or hash
            clean_rel = rel_path.split("?")[0].split("#")[0]
            resolved = (js_file.parent / clean_rel).resolve()

            # Candidate extensions
            candidates = [
                resolved,
                resolved.with_suffix(".ts"),
                resolved.with_suffix(".tsx"),
                resolved.with_suffix(".js"),
                resolved.with_suffix(".jsx"),
                resolved / "index.ts",
                resolved / "index.tsx",
                resolved / "index.js"
            ]

            if not any(cand.exists() for cand in candidates):
                phantoms.append({
                    "source": js_file.as_posix(),
                    "line": line_idx,
                    "target": rel_path,
                    "type": "Phantom Relative JS/TS Import"
                })
    return phantoms

def audit_workspace_phantoms() -> Tuple[List[Dict], List[Dict]]:
    """Audits entire workspace for phantom imports and hallucinated links."""
    code_phantoms = []
    doc_phantoms = []

    # 1. Audit src/ imports
    if SRC_DIR.exists():
        for f in SRC_DIR.rglob("*"):
            if f.is_file():
                if any(ign in f.parts for ign in IGNORE_DIRS):
                    continue
                if f.suffix == ".py":
                    code_phantoms.extend(check_python_phantom_imports(f))
                elif f.suffix in {".ts", ".tsx", ".js", ".jsx"}:
                    code_phantoms.extend(check_js_phantom_imports(f))

    # 2. Audit docs/ internal markdown links
    if DOCS_DIR.exists():
        for doc in DOCS_DIR.rglob("*.md"):
            try:
                content = doc.read_text(encoding="utf-8", errors="ignore")
                # Find markdown links: [text](path)
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                for text, target in links:
                    if target.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    clean_target = target.split("#")[0]
                    if not clean_target:
                        continue
                    if clean_target.startswith("file://"):
                        clean_target = clean_target.replace("file://", "").lstrip("/\\")

                    resolved_root = Path(clean_target)
                    resolved_src = doc.parent / clean_target

                    if not resolved_root.exists() and not resolved_src.exists():
                        doc_phantoms.append({
                            "source": doc.as_posix(),
                            "line": 0,
                            "target": target,
                            "type": "Phantom Documentation Link"
                        })
            except Exception:
                pass

    return code_phantoms, doc_phantoms

def run_sentinel(strict: bool = False) -> int:
    print("🔍 Running Phantom File Sentinel & Hallucination Trap...")

    code_phantoms, doc_phantoms = audit_workspace_phantoms()
    total_phantoms = len(code_phantoms) + len(doc_phantoms)

    if total_phantoms == 0:
        print("✨ Sentinel PASSED! Zero phantom files, broken imports, or hallucinated paths detected.")
        print("-" * 65)
        return 0

    print(f"\n❌ DETECTED {total_phantoms} PHANTOM / HALLUCINATED REFERENCES:")
    print("-" * 65)

    for p in code_phantoms:
        print(f"  🚨 [{p['source']}:{p['line']}] {p['type']}: '{p['target']}' does not exist on disk!")

    for d in doc_phantoms:
        print(f"  🔗 [{d['source']}] {d['type']}: '{d['target']}' does not resolve to any real file!")

    print("-" * 65)
    print("💡 Fix or remove phantom references before proceeding.")
    return 1

def main():
    parser = argparse.ArgumentParser(description="Agent Hallucination Trap & Phantom File Sentinel")
    parser.add_argument("--strict", action="store_true", help="Fail with non-zero exit code on any phantom reference")
    args = parser.parse_args()

    sys.exit(run_sentinel(strict=args.strict))

if __name__ == "__main__":
    main()
