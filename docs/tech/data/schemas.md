# Data Schemas & Entities Contract

Scope: Technical Architecture - Data Layer & Persistence Models
Related: docs/tech/overview.md, docs/tech/data/persistence.md

## 1. Responsibilities & Boundaries
- **Owns:** Global entity definitions, canonical schema structures, database migration rules, and data transfer object (DTO) contracts.
- **Does NOT Own:** Physical database provisioning or storage connection configuration (owned by `docs/tech/data/persistence.md` and `docs/operations/deployment.md`).

## 2. Invariants (Hard Rules)
- Every persisted entity must possess a unique immutable identifier and audit timestamps (`created_at`, `updated_at`).
- Breaking schema changes must provide an explicit forward-migration path and backward-compatible fallback window.
- Application code must never bypass defined schema validation when accepting or persisting external data.

## 3. Specifications & Interfaces
### Canonical Schema Blueprint
```typescript
interface BaseEntity {
  id: string; // UUID v4 or KSUID
  created_at: string; // ISO 8601 UTC
  updated_at: string; // ISO 8601 UTC
}
```

### Migration Policy
- Database migrations are sequential, version-controlled, and deterministic.
- Schema definitions must be verified with automated test suites before committing.

## 4. Decisions & Revisions
- 2026-10-10: Baseline data schemas contract established for template repository.
