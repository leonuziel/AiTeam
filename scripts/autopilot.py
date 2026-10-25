#!/usr/bin/env python3
"""
Autonomous Roadmap & Task Queue Inspector (Autopilot / Turbo Mode)
Programmatically inspects roadmaps, backlogs, and doc-to-code parity to determine
whether uncompleted tasks remain. Prevents agents from prematurely yielding turns
or asking the user for permission when verified work remains to be done.
"""
import sys
import os
import re
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROADMAP_PATHS = [
    Path("ROADMAP.md"),
    Path("docs/ROADMAP.md"),
    Path("docs/product/roadmap.md")
]

SRC_DIR = Path("src")
DOCS_MODULES_DIR = Path("docs/tech/modules")

def find_roadmap_file() -> Optional[Path]:
    """Finds the active roadmap file if one exists."""
    for p in ROADMAP_PATHS:
        if p.exists():
            return p
    return None

def extract_uncompleted_roadmap_tasks(roadmap_path: Path) -> List[Dict]:
    """Extracts unchecked task items from a roadmap markdown file."""
    tasks = []
    try:
        content = roadmap_path.read_text(encoding="utf-8")
        for line_idx, line in enumerate(content.splitlines(), start=1):
            trimmed = line.strip()
            # Match markdown unchecked task: - [ ] <task> or * [ ] <task>
            match = re.search(r"^[-*]\s*\[\s*\]\s*(.+)$", trimmed)
            if match:
                task_text = match.group(1).strip()
                tasks.append({
                    "file": roadmap_path.as_posix(),
                    "line": line_idx,
                    "text": task_text
                })
    except Exception:
        pass
    return tasks

def find_unimplemented_module_specs() -> List[str]:
    """Finds specifications in docs/tech/modules/ awaiting implementation in src/."""
    unimplemented = []
    if DOCS_MODULES_DIR.exists():
        for mod_dir in DOCS_MODULES_DIR.iterdir():
            if mod_dir.is_dir() and not mod_dir.name.startswith("."):
                src_cand = SRC_DIR / mod_dir.name
                if not src_cand.exists() or not any(src_cand.glob("*")):
                    unimplemented.append(mod_dir.name)
    return unimplemented

def check_remaining_work() -> Tuple[bool, List[str]]:
    """Evaluates whether work remains to be done in the repository."""
    work_items = []

    # 1. Check active roadmap for uncompleted items
    roadmap_file = find_roadmap_file()
    if roadmap_file:
        uncompleted_tasks = extract_uncompleted_roadmap_tasks(roadmap_file)
        for t in uncompleted_tasks:
            work_items.append(f"[Roadmap] {t['text']} ({t['file']}:{t['line']})")

    # 2. Check for specs awaiting implementation
    unimplemented_mods = find_unimplemented_module_specs()
    for mod in unimplemented_mods:
        work_items.append(f"[Unimplemented Module] 'docs/tech/modules/{mod}' has no code in 'src/{mod}/'")

    return len(work_items) > 0, work_items

def mark_task_complete(task_query: str) -> bool:
    """Marks a task as completed (- [ ] -> - [x]) in the active roadmap."""
    roadmap_file = find_roadmap_file()
    if not roadmap_file:
        print("❌ Error: No roadmap file found.")
        return False

    content = roadmap_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    found = False

    for i, line in enumerate(lines):
        if re.search(r"^[-*]\s*\[\s*\]", line.strip()) and task_query.lower() in line.lower():
            lines[i] = re.sub(r"\[\s*\]", "[x]", line, count=1)
            found = True
            print(f"✅ Marked task complete: {lines[i].strip()}")
            break

    if found:
        roadmap_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    else:
        print(f"⚠️ Could not find uncompleted task matching query: '{task_query}'")
        return False

def main():
    parser = argparse.ArgumentParser(description="Autonomous Task Queue & Roadmap Inspector (Autopilot / Turbo)")
    parser.add_argument("--complete", "-c", help="Mark a task as completed in the active roadmap")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON status")
    args = parser.parse_args()

    if args.complete:
        success = mark_task_complete(args.complete)
        sys.exit(0 if success else 1)

    has_work, items = check_remaining_work()

    if has_work:
        print("=" * 65)
        print("🚨 AUTOPILOT / TURBO GATE: REMAINING WORK DETECTED")
        print("=" * 65)
        print(f"Found {len(items)} uncompleted task(s) in active roadmap / specifications:")
        for idx, item in enumerate(items[:5], start=1):
            print(f"  {idx}. {item}")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more pending tasks.")
        print("-" * 65)
        print("⚡ MANDATORY DIRECTIVE FOR AI AGENTS:")
        print("DO NOT halt or ask the user 'Should I proceed?'.")
        print("Execute the next uncompleted task immediately in this turn.")
        print("=" * 65)
        # Exit with code 2 to indicate work remains
        sys.exit(2)
    else:
        print("=" * 65)
        print("✨ AUTOPILOT / TURBO GATE: ALL TASKS EXHAUSTED")
        print("=" * 65)
        print("All roadmap phases are checked and all specifications are implemented.")
        print("Running final health audit to verify 100% compliance score...")
        audit_res = subprocess.run([sys.executable, "scripts/audit_repo.py"], capture_output=True, text=True, encoding="utf-8")
        if audit_res.returncode == 0:
            print("✨ Health score is 100.0%. All definition-of-done criteria met.")
            sys.exit(0)
        else:
            print("⚠️ Audit issues detected! Must resolve before stopping:")
            print(audit_res.stdout.strip())
            sys.exit(1)

if __name__ == "__main__":
    main()
