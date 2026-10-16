# Persistence & Caching Strategy

Scope: Technical Architecture - Storage & Caching Layers
Related: docs/tech/overview.md, docs/tech/data/schemas.md

## 1. Responsibilities & Boundaries
- **Owns:** Storage adapters, database connection pooling policies, transaction demarcation, caching strategies, and cache invalidation policies.
- **Does NOT Own:** Business validation rules (owned by domain modules) or schema contracts (owned by `docs/tech/data/schemas.md`).

## 2. Invariants (Hard Rules)
- All multi-entity modifications requiring consistency must be executed within transactional boundaries.
- Cache invalidation or expiration times (TTL) must be explicitly defined for every cached entity; unbounded cache entries are forbidden.
- Storage failures must be caught, translated to domain-safe errors, and never leak raw database credentials or low-level connection strings.

## 3. Specifications & Interfaces
### Storage Layer Boundaries
- Persistence access must always be abstracted behind repository or data access interfaces.
- Cache layer sits between application services and relational/document persistence layers.

### Transaction Interface Contract
```typescript
interface TransactionManager {
  executeInTransaction<T>(work: () => Promise<T>): Promise<T>;
}
```

## 4. Decisions & Revisions
- 2026-10-10: Baseline persistence and caching strategy established for template repository.
