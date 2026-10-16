# Product Overview & Core Requirements

Scope: Product Vision & High-Level Requirements
Related: docs/ARCHITECTURE.md, docs/tech/overview.md

## 1. Responsibilities & Boundaries
- **Owns:** High-level product definition, user personas, core value propositions, and overarching product requirements.
- **Does NOT Own:** Technical stack choices, database schemas, or infrastructure specifications (owned by `docs/tech/` and `docs/operations/`).

## 2. Invariants (Hard Rules)
- All product requirements must define acceptance criteria before technical design begins.
- Breaking behavioral changes to user flows must be explicitly reviewed and documented.
- Domain-specific product workflows must be maintained in dedicated subfolders under `docs/product/domains/`.

## 3. Specifications & Interfaces
### Core Product Capabilities (Baseline Template)
- Baseline empty template prepared to receive application-specific requirements.
- Domain modules should be introduced under `docs/product/domains/<domain>/` with `requirements.md` and `flows.md`.

### Product Domain Structure
- `docs/product/domains/` will house functional feature sets as the application is defined.

## 4. Decisions & Revisions
- 2026-10-10: Initial product baseline specification established for template repository.
