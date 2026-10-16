# Workflow: Fail-Fast Escalation Protocol

## Purpose
Enforces the core rule: **Agents must never guess, invent, or fabricate business logic, schemas, or API contracts.**

---

## Trigger Conditions
- Missing acceptance criteria or ambiguous requirements in `docs/product/`.
- Unspecified HTTP error status codes, headers, or payloads in `docs/tech/api/`.
- Undefined failure modes, retries, or timeouts in `docs/tech/modules/`.
- Conflicting invariants between two documents.

---

## Escalation Sequence

```mermaid
sequenceDiagram
    participant Implementer as Implementer Agent
    participant Orchestrator as Orchestrator Agent
    participant User as Human User
    participant DocSync as Doc-Sync Custodian

    Implementer->>Implementer: Encounters ambiguous requirement or missing contract
    Implementer->>Orchestrator: Emit [ESCALATION REQUIRED] block & Halt code edits
    Orchestrator->>Orchestrator: Inspect docs/ tree for existing resolution
    alt Resolution Found in Parent Spec
        Orchestrator->>Implementer: Provide documented spec link & unblock
    else Resolution Not in Docs
        Orchestrator->>User: Formulate precise question with options
        User->>Orchestrator: Selects option / decides rule
        Orchestrator->>DocSync: Trigger Doc-Sync Loop with user decision
        DocSync->>Implementer: Spec updated & verified; unblock code production
    end
```

### Escalation Block Format
When halting, the Implementer must output this exact structure:

```text
[ESCALATION REQUIRED]
- Target Specification: docs/tech/api/contracts.md
- Context: Implementing public user registration endpoint
- Missing Decision: Password complexity minimum requirements and lockout threshold
- Impact: Cannot implement validation logic or write unit tests without formal specification
- Recommended Options:
  1. Minimum 12 characters, 5 failed attempts locks for 15 minutes (OWASP recommended)
  2. Minimum 8 characters, exponential backoff without account lockout
```

### Escalation Resolution Invariant
**No code may be written until the Doc-Sync loop has updated the target document and recorded the decision.**
