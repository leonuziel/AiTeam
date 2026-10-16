# Technical Architecture Overview

Scope: Global Technology Stack & Engineering Conventions
Related: docs/ARCHITECTURE.md, docs/product/overview.md

## 1. Responsibilities & Boundaries
- **Owns:** Baseline technology stack selection, cross-cutting architectural patterns, coding conventions, and global technical invariants.
- **Does NOT Own:** Product domain definitions (owned by `docs/product/`) or environment-specific deployment workflows (owned by `docs/operations/`).

## 2. Invariants (Hard Rules)
- Code must strictly adhere to the technical patterns and invariants defined in this documentation tree.
- Dependencies and core frameworks must be documented prior to introduction in the codebase.
- No direct implementation code may violate data contracts (`docs/tech/data/`) or API contracts (`docs/tech/api/`).

## 3. Specifications & Interfaces
### Stack Conventions
- Application code is placed under `src/`.
- Automated tests are placed under `tests/`.
- Utility automation and repository health scripts reside in `scripts/`.
- Concrete documentation blueprints reside in `templates/`.

### Subsystem Technical Specs
- Detailed data contracts and persistence models belong in `docs/tech/data/`.
- Public/internal API protocols and error contracts belong in `docs/tech/api/`.
- Subsystem module designs belong in `docs/tech/modules/<module>/`.

## 4. Decisions & Revisions
- 2026-10-10: Initial technical overview established for template repository.
