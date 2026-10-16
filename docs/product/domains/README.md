# Product Domain Specifications Guide

Scope: Product Strategy - Domain Module Layout
Related: docs/product/overview.md, docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** Directory topology and structural guidance for all functional domain modules placed under `docs/product/domains/<domain>/`.
- **Does NOT Own:** Technical implementation contracts (owned by `docs/tech/modules/`).

## 2. Invariants (Hard Rules)
- Every new product capability must reside in its own folder: `docs/product/domains/<domain_name>/`.
- Each domain folder must contain at least `requirements.md` and `flows.md` modeled after `templates/domain-template.md`.
- No code in `src/` may implement business logic without a corresponding domain specification in this tree.

## 3. Specifications & Interfaces
### Domain Subfolder Hierarchy
```text
docs/product/domains/<domain>/
├── requirements.md     # User stories, acceptance criteria, invariant constraints
└── flows.md            # Interaction sequence diagrams, user journeys, edge cases
```

### Scaffolding Command
Use the automated bootstrapper utility:
```bash
python scripts/scaffold_module.py --domain <name>
```

## 4. Decisions & Revisions
- 2026-10-10: Baseline domain organization guide established for template repository.
