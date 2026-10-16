# Domain: [Domain Name]

Scope: Product Domain - [Domain Name]
Related: docs/product/overview.md, docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** Core domain user stories, business rules, acceptance criteria, and workflow states for [Domain Name].
- **Does NOT Own:** Technical database schemas or infrastructure configuration (owned by `docs/tech/` and `docs/operations/`).

## 2. Invariants (Hard Rules)
- [Domain Invariant 1: e.g., A user cannot initiate an order without a confirmed payment source.]
- [Domain Invariant 2: e.g., All status transitions must be recorded in an audit trail.]

## 3. Specifications & Interfaces
### User Stories & Acceptance Criteria
- **Story 1:** As a [Role], I want [Feature], so that [Benefit].
  - *Criteria:* Given [Context], When [Action], Then [Expected Result].

### State Transitions & Flows
```text
[State A] ---> (Trigger 1) ---> [State B]
              ---> (Trigger 2) ---> [State C]
```

## 4. Decisions & Revisions
- YYYY-MM-DD: Initial domain specification established.
