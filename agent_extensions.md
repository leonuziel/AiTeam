# AGENT EXTENSIONS & UTILITIES: Doc-to-Code Framework

This document provides the supplementary blueprints, validation scripts, and configuration guidelines to support the Antigravity agent in maintaining strict documentation hygiene.

---

## 1. Concrete Leaf Template (`templates/leaf-template.md`)

Whenever the agent creates a new documentation leaf file, it must strictly follow this structural blueprint:

```markdown
# [Module / Component Name]

Scope: [Product Domain / Tech Layer]
Related: [Concept A], [Concept B]

## 1. Responsibilities & Boundaries
- **Owns:** [What this component handles]
- **Does NOT Own:** [Explicit boundaries and exclusions]

## 2. Invariants (Hard Rules)
- [Non-negotiable rule 1: e.g., All inputs must be sanitized before persistence]
- [Non-negotiable rule 2: e.g., Maximum payload size cannot exceed 5MB]

## 3. Specifications & Interfaces
[Insert data schemas, state machines, API contracts, sequence descriptions, or core algorithms here.]

## 4. Decisions & Revisions
- YYYY-MM-DD: Initial specification established.
```

---

## 2. Programmatic Linter Script (`scripts/lint_docs.py`)

To ensure documentation files never drift or lose structural integrity, use this Python script. The agent can run this script to self-audit its changes before completing a task.

```python
import os
import sys
from pathlib import Path

# Ensure UTF-8 output across platforms and Windows console code pages
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DOCS_DIR = Path("docs")
REQUIRED_SECTIONS = [
    "Responsibilities & Boundaries",
    "Invariants",
    "Specifications & Interfaces",
    "Decisions & Revisions"
]

def lint_docs():
    errors = 0
    markdown_files = list(DOCS_DIR.glob("**/*.md"))
    print(f"🔍 Linting {len(markdown_files)} documentation files...")

    for file_path in markdown_files:
        content = file_path.read_text(encoding="utf-8")
        
        # Check for required sections
        for section in REQUIRED_SECTIONS:
            if section.lower() not in content.lower():
                print(f"  ❌ [{file_path}] Missing required section: '## {section}'")
                errors += 1

        # Check for metadata headers
        if "Scope:" not in content:
            print(f"  ⚠️ [{file_path}] Missing 'Scope:' metadata line.")
        if "Related:" not in content:
            print(f"  ⚠️ [{file_path}] Missing 'Related:' metadata line.")

    if errors > 0:
        print(f"\n❌ Lint failed with {errors} structural errors.")
        exit(1)
    else:
        print("\n✨ All documentation files passed structural linting!")
        exit(0)

if __name__ == "__main__":
    lint_docs()
```

---

## 3. Antigravity Environment Config (`.agent/config.json`)

If your workspace supports configuration rules, place this file under `.agent/config.json` to scope write permissions and enforce execution flow:

```json
{
  "workspace": {
    "name": "Doc-to-Code Autonomous System",
    "allowed_write_paths": [
      "docs/",
      "src/",
      "tests/",
      "scripts/",
      "templates/"
    ],
    "protected_paths": [
      ".git/",
      "agent_system_prompt.md",
      "agent_extensions.md"
    ]
  },
  "behavior": {
    "require_spec_before_code": true,
    "escalate_on_ambiguity": true
  }
}
```

---

## 4. Built-In Utilities & Workflows Catalog

### Helper Scripts (`scripts/`)
- `scripts/audit_repo.py`: Master health checker running 26-point verification.
- `scripts/lint_docs.py`: Validates 4-section documentation structure and link integrity.
- `scripts/check_doc_drift.py`: Audits doc-to-code parity and flags undocumented modules.
- `scripts/ingest_context.py`: Ingests raw context and updates targeted documentation sections.
- `scripts/scaffold_module.py`: Scaffolds new domains (`--domain`) and modules (`--module`).
- `scripts/record_decision.py`: Appends revision logs (`--append`) or creates ADRs (`--adr`).
- `scripts/bootstrap_project.py`: Configures metadata and initializes a new downstream project.

### Core Agent Workflows (`.agent/workflows/`)
- `context_ingestion_loop.md`: Standard loop for absorbing raw notes into `docs/`.
- `design_resolution_loop.md`: Standard loop for bubbling up downstream design questions.
- `escalation_loop.md`: Protocol for halting and escalating on ambiguity.
- `doc_sync_loop.md`: Protocol for atomic document updates and ADR logging.
- `code_review_loop.md`: Gate checking invariants, parity, and tests.
- `continuous_cleanliness_loop.md`: Repository hygiene checklist.
