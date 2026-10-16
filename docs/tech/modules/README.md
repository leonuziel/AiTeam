# Subsystem Modules Architecture Guide

Scope: Technical Architecture - Subsystem Modules Topology
Related: docs/tech/overview.md, docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** Structural guidance and conventions for technical subsystem designs placed under `docs/tech/modules/<module>/`.
- **Does NOT Own:** Product domain definitions (owned by `docs/product/domains/`).

## 2. Invariants (Hard Rules)
- Every subsystem module in `src/<module>/` must have a corresponding specification in `docs/tech/modules/<module>/`.
- Each technical module folder must contain `architecture.md` and `interfaces.md`.
- Circular dependencies between modules are strictly forbidden.

## 3. Specifications & Interfaces
### Module Subfolder Topology
```text
docs/tech/modules/<module>/
├── architecture.md     # Component layout, dependencies, internal state flow
└── interfaces.md       # Exported functions, classes, types, and method signatures
```

### Scaffolding Command
Use the automated bootstrapper utility:
```bash
python scripts/scaffold_module.py --module <name>
```

## 4. Decisions & Revisions
- 2026-10-10: Baseline subsystem modules guide established for template repository.
