# Architecture Decision Records (ADRs) Guide

Scope: Architecture Decision Log & Governance
Related: docs/ARCHITECTURE.md, docs/tech/overview.md

## 1. Responsibilities & Boundaries
- **Owns:** Historical repository for all binding architectural, technical, and operational decisions recorded across project lifecycles.
- **Does NOT Own:** Living code files or active API contracts (owned by `src/` and `docs/tech/`).

## 2. Invariants (Hard Rules)
- Once an ADR is marked as Accepted, it is binding across all agents and human contributors.
- ADRs are immutable historical records; modifying an established architectural direction requires creating a new ADR that explicitly supersedes the predecessor.
- Every ADR filename must adhere to the pattern `ADR-XXX-<kebab-case-title>.md` (e.g., `ADR-001-use-postgresql.md`).

## 3. Specifications & Interfaces
### Generating an ADR via Agentic Tooling
```bash
python scripts/record_decision.py --adr "Use Redis for Distributed Token Revocation" --context "Stateless JWT authentication requiring real-time session invalidation"
```

### ADR Lifecycle States
- `Proposed`: Open for review and evaluation of trade-offs.
- `Accepted`: Approved and active binding contract for implementation.
- `Superseded`: Replaced by a subsequent ADR (must cite replacement ADR link).
- `Deprecated`: Decommissioned without direct replacement.

## 4. Decisions & Revisions
- 2026-10-10: Baseline Architecture Decision Records governance established for template repository.
