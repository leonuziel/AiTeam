# Module: [Module Name]

Scope: Technical Architecture - Subsystem [Module Name]
Related: docs/tech/overview.md, docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** Internal module architecture, component cohesion, algorithmic implementation, and internal interfaces for [Module Name].
- **Does NOT Own:** Cross-cutting authentication contracts (owned by `docs/tech/api/`) or persistence adapters directly (unless encapsulated).

## 2. Invariants (Hard Rules)
- [Module Invariant 1: e.g., All incoming parameters must be validated at the boundary.]
- [Module Invariant 2: e.g., No blocking I/O calls on the event loop thread.]

## 3. Specifications & Interfaces
### Exported Types & Signatures
```typescript
export interface [ModuleName]Service {
  execute(command: [CommandType]): Promise<[ResultType]>;
}
```

### Component Architecture & Dependency Graph
```text
[Public API / Controller]
        |
        v
[Service Layer] ---> [Domain Model]
        |
        v
[Data Adapter / Repository]
```

## 4. Decisions & Revisions
- YYYY-MM-DD: Initial module specification established.
