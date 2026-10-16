#!/usr/bin/env python3
"""
Automated Scaffolder for Agentic Repositories
Creates compliant documentation, src, and test directories for new domains or modules.
"""
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

TODAY = datetime.utcnow().strftime("%Y-%m-%d")

DOMAIN_REQUIREMENTS_TEMPLATE = """# Domain Requirements: {title}

Scope: Product Domain - {title}
Related: docs/product/overview.md, docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** Core business logic, acceptance criteria, and user workflows for {title}.
- **Does NOT Own:** Technical database schemas or physical infrastructure (owned by docs/tech/ and docs/operations/).

## 2. Invariants (Hard Rules)
- All user interactions must be authorized and validated before execution.
- Domain status transitions must be logged with audit timestamps.

## 3. Specifications & Interfaces
### User Stories & Acceptance Criteria
- **Story 1:** As a user, I want {name} capabilities, so that I can achieve expected outcomes.
  - *Criteria:* Given valid parameters, When requested, Then return success.

## 4. Decisions & Revisions
- {date}: Initial domain requirements established.
"""

DOMAIN_FLOWS_TEMPLATE = """# Domain Interaction Flows: {title}

Scope: Product Flows - {title}
Related: docs/product/domains/{name}/requirements.md, docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** End-to-end user journeys, sequence flows, and edge cases for {title}.
- **Does NOT Own:** Transport-level protocol serialization (owned by docs/tech/api/).

## 2. Invariants (Hard Rules)
- Every workflow must define an unrecoverable failure path and user feedback mechanism.
- Flow timeouts must terminate cleanly without hanging state.

## 3. Specifications & Interfaces
### Primary Workflow Sequence
```text
User / Client ---> [Initiate {title}] ---> [Validate Input]
                                           |
                    [Success Result] <--- [Process State]
```

## 4. Decisions & Revisions
- {date}: Initial interaction flows documented.
"""

MODULE_ARCHITECTURE_TEMPLATE = """# Subsystem Architecture: {title}

Scope: Technical Architecture - Subsystem {title}
Related: docs/tech/overview.md, docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** Internal module orchestration, domain state coordination, and business rule enforcement for {title}.
- **Does NOT Own:** Generic cross-cutting HTTP routing or global telemetry (owned by docs/tech/api/ and docs/operations/).

## 2. Invariants (Hard Rules)
- All public interfaces must strictly type input arguments and return contracts.
- In-memory state mutations must be synchronized and thread/async safe.

## 3. Specifications & Interfaces
### Subsystem Topology
```text
src/{name}/
├── index.py (or index.ts)
└── service.py
```

## 4. Decisions & Revisions
- {date}: Initial subsystem architecture established.
"""

MODULE_INTERFACES_TEMPLATE = """# Subsystem Interfaces: {title}

Scope: Technical Interfaces - Subsystem {title}
Related: docs/tech/modules/{name}/architecture.md, docs/tech/overview.md

## 1. Responsibilities & Boundaries
- **Owns:** Exported interface definitions, DTO signatures, and public contract declarations for {title}.
- **Does NOT Own:** Transport wire format envelopes (owned by docs/tech/api/contracts.md).

## 2. Invariants (Hard Rules)
- Modifications to existing public signatures require backward-compatible deprecation notices.
- Null or undefined arguments are rejected unless explicitly typed as optional.

## 3. Specifications & Interfaces
### Exported Signatures
```typescript
export interface {title}Service {{
  execute(params: Record<string, unknown>): Promise<boolean>;
}}
```

## 4. Decisions & Revisions
- {date}: Initial subsystem interfaces specified.
"""

def scaffold_domain(name: str):
    slug = name.lower().replace(" ", "_").replace("-", "_")
    title = slug.replace("_", " ").title()
    target_dir = Path("docs/product/domains") / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    req_file = target_dir / "requirements.md"
    flow_file = target_dir / "flows.md"

    if not req_file.exists():
        req_file.write_text(DOMAIN_REQUIREMENTS_TEMPLATE.format(title=title, name=slug, date=TODAY), encoding="utf-8")
        print(f"  ✅ Created: {req_file}")
    else:
        print(f"  ⚠️  Exists: {req_file}")

    if not flow_file.exists():
        flow_file.write_text(DOMAIN_FLOWS_TEMPLATE.format(title=title, name=slug, date=TODAY), encoding="utf-8")
        print(f"  ✅ Created: {flow_file}")
    else:
        print(f"  ⚠️  Exists: {flow_file}")

    print(f"\n✨ Product Domain '{slug}' scaffolded successfully.")

def scaffold_module(name: str):
    slug = name.lower().replace(" ", "_").replace("-", "_")
    title = slug.replace("_", " ").title()
    
    # Docs
    docs_dir = Path("docs/tech/modules") / slug
    docs_dir.mkdir(parents=True, exist_ok=True)
    arch_file = docs_dir / "architecture.md"
    intf_file = docs_dir / "interfaces.md"

    if not arch_file.exists():
        arch_file.write_text(MODULE_ARCHITECTURE_TEMPLATE.format(title=title, name=slug, date=TODAY), encoding="utf-8")
        print(f"  ✅ Created: {arch_file}")
    else:
        print(f"  ⚠️  Exists: {arch_file}")

    if not intf_file.exists():
        intf_file.write_text(MODULE_INTERFACES_TEMPLATE.format(title=title, name=slug, date=TODAY), encoding="utf-8")
        print(f"  ✅ Created: {intf_file}")
    else:
        print(f"  ⚠️  Exists: {intf_file}")

    # Code scaffold in src/ and tests/
    src_dir = Path("src") / slug
    src_dir.mkdir(parents=True, exist_ok=True)
    src_placeholder = src_dir / ".gitkeep"
    if not src_placeholder.exists():
        src_placeholder.write_text(f"# Placeholder for {slug} implementation\n", encoding="utf-8")
        print(f"  ✅ Created: {src_placeholder}")

    tests_dir = Path("tests") / slug
    tests_dir.mkdir(parents=True, exist_ok=True)
    test_placeholder = tests_dir / ".gitkeep"
    if not test_placeholder.exists():
        test_placeholder.write_text(f"# Placeholder for {slug} test suite\n", encoding="utf-8")
        print(f"  ✅ Created: {test_placeholder}")

    print(f"\n✨ Technical Module '{slug}' (docs, src, tests) scaffolded successfully.")

def main():
    parser = argparse.ArgumentParser(description="Scaffold compliant documentation and code structure.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--domain", type=str, help="Scaffold a new product domain (under docs/product/domains/)")
    group.add_argument("--module", type=str, help="Scaffold a new technical module (under docs/tech/modules/, src/, tests/)")

    args = parser.parse_args()

    if args.domain:
        scaffold_domain(args.domain)
    elif args.module:
        scaffold_module(args.module)

if __name__ == "__main__":
    main()
