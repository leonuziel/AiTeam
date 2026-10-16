# System Architecture & Routing Map

Scope: Global System Topology & Routing
Related: docs/product/overview.md, docs/tech/overview.md

## 1. Responsibilities & Boundaries
- **Owns:** Root documentation routing map, global architectural topology, cross-domain coordination rules, and overarching system constraints.
- **Does NOT Own:** Specific product domain business logic (owned by `docs/product/`) or detailed subsystem technical contracts and implementations (owned by `docs/tech/`).

## 2. Invariants (Hard Rules)
- All new features and domains must establish specifications in `docs/` before code implementation begins.
- Documentation under `docs/` is the single source of truth; code never fabricates specifications.
- Ambiguities or missing requirements must trigger an escalation rather than speculative implementation.
- Every documentation leaf must adhere to the 4-section standard (`Responsibilities & Boundaries`, `Invariants`, `Specifications & Interfaces`, `Decisions & Revisions`).

## 3. Specifications & Interfaces
### Documentation Tree Topology
```text
docs/
├── ARCHITECTURE.md                  # Root routing map, system topology & global constraints
├── product/                         # "What" & "Why" (Requirements, Personas, User Journeys)
│   ├── overview.md                  # Core value prop & high-level requirements
│   └── domains/                     # Domain modules (e.g., auth, billing, analytics)
├── tech/                            # "How" (System Architecture & Cross-cutting Specs)
│   ├── overview.md                  # Global stack, shared conventions & patterns
│   ├── data/                        # DB entities, migration contracts, DTOs, persistence
│   ├── api/                         # REST/gRPC/GraphQL/WebSocket protocols, error contracts
│   └── modules/                     # Concrete subsystem technical design
└── operations/                      # "Where" & "How it runs" (Infra, CI/CD, Observability)
    ├── deployment.md
    └── telemetry.md
```

### Agent Roles & Routing Protocol
- **Orchestrator:** High-level task delegation, documentation routing, escalation routing to the user.
- **Doc-Sync Custodian:** Conflict verification, atomic doc updates, audit logging under Decisions & Revisions.
- **Implementer:** Read-before-write validation, strict invariant compliance, code & test authoring.

## 4. Decisions & Revisions
- 2026-10-10: Baseline architecture routing map established for template repository.
