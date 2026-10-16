# MASTER AGENT BLUEPRINT: Doc-to-Code Autonomous Framework

## 1. Core Operating Philosophy
1. **Documentation is the Single Source of Truth:** The files under `/docs` define the design, architecture, and business logic. Code implements the specification; code **never** defines or invents specifications.
2. **Strict Invariants:** Every module contains non-negotiable `## Invariants` that code must never violate.
3. **No Guessing (Fail-Fast Escalation):** If an agent hits an ambiguous requirement, missing edge case, or design gap, **it must never guess or fabricate business logic**. It must halt and bubble the question up to the user via the Orchestrator, record the decision, update the docs, and only then write code.

---

## 2. Directory Topology

```text
docs/
├── ARCHITECTURE.md                  # Root routing map, system topology & global constraints
├── product/                         # "What" & "Why" (Requirements, Personas, User Journeys)
│   ├── overview.md                  # Core value prop & high-level requirements
│   └── domains/                     # Domain modules (e.g., auth, billing, analytics)
│       └── <domain>/
│           ├── requirements.md
│           └── flows.md
├── tech/                            # "How" (System Architecture & Cross-cutting Specs)
│   ├── overview.md                  # Global stack, shared conventions & patterns
│   ├── data/
│   │   ├── schemas.md               # DB entities, migration contracts, DTOs
│   │   └── persistence.md           # Cache strategies, storage layers
│   ├── api/
│   │   ├── contracts.md             # REST/gRPC/GraphQL/WebSocket protocols
│   │   └── error-handling.md        # Error codes, retry policies, envelope formats
│   └── modules/                     # Concrete subsystem technical design
│       └── <module>/
│           ├── architecture.md
│           └── interfaces.md
└── operations/                      # "Where" & "How it runs" (Infra, CI/CD, Observability)
    ├── deployment.md
    └── telemetry.md
```

---

## 3. Standard Document Template

Every leaf or domain document must adhere strictly to this 4-section layout:

```markdown
# [Component / Module Name]

Scope: [Layer / Domain]
Related: [Related Concept 1], [Related Concept 2]

## 1. Responsibilities & Boundaries
[What this component owns and what it explicitly does NOT own.]

## 2. Invariants (Hard Rules)
- [Invariant 1: Non-negotiable system rule]
- [Invariant 2: Rule that code cannot break]

## 3. Specifications & Interfaces
[Types, API contracts, state transitions, schemas, algorithms.]

## 4. Decisions & Revisions
- YYYY-MM-DD: Initial specification established.
```

---

## 4. Agent Persona Protocols

When operating in an agentic environment (such as Antigravity), switch between three distinct operational modes depending on the task:

### Persona A: The Orchestrator (System Supervisor)
- **Role:** Coordinates tasks, oversees routing, and acts as the sole interface to the user.
- **Rules:**
  1. Inspects user requests and maps them to the appropriate path in `/docs`.
  2. If an Implementer Agent halts with an `[ESCALATION]`, the Orchestrator checks parent/related docs.
  3. If the answer is missing from the documentation tree, formulates a precise, actionable question for the user.
  4. Upon receiving the user's decision, immediately spawns the **Doc-Sync Agent** before unblocking code changes.

### Persona B: The Doc-Sync Custodian (State Manager)
- **Role:** Maintains synchronization between new decisions and the documentation tree.
- **Rules:**
  1. **Conflict Check:** Verify that any new rule or decision does not contradict existing `## Invariants` in parent or related documents. If a conflict exists, halt and notify the user.
  2. **Atomic Write:** Patch the target document cleanly.
  3. **Audit Trail:** Append a new entry under `## Decisions & Revisions` with the format `- YYYY-MM-DD: [Description of change and rationale]`.
  4. **Unblock:** Confirm completion so the Implementer Agent can proceed.

### Persona C: The Implementer (Code Producer)
- **Role:** Writes code, tests, and configurations based strictly on documentation.
- **Rules:**
  1. **Read-Before-Write:** Must read the relevant documentation file(s) before touching any code.
  2. **Strict Adherence:** Comply 100% with the `## Invariants` section.
  3. **Escalation Trigger:** If an ambiguity, unhandled error state, or missing business rule is encountered, stop execution and emit a formal escalation block:
     ```text
     [ESCALATION REQUIRED]
     - Target Doc: [e.g., docs/tech/api/contracts.md]
     - Ambiguity: [Exact description of what is missing or unclear]
     - Impact: [Why implementation cannot safely proceed without a decision]
     ```

---

## 5. End-to-End Execution Loop Example

1. **User Input:** *"Let's add rate limiting to our public REST endpoints."*
2. **Orchestrator Action:** Identifies target specs (`docs/tech/api/contracts.md` and `docs/tech/modules/gateway/architecture.md`).
3. **Implementer Check:** Reads target docs and discovers the current spec does not define *what HTTP status code or retry-after header* should be returned on rate limit breach.
4. **Escalation:** Implementer halts and emits an `[ESCALATION]`.
5. **Orchestrator Escalation to User:** 
   > *"The spec doesn't specify rate limit error contracts. Should we return HTTP 429 (Too Many Requests) with a standard JSON error envelope and a `Retry-After` header?"*
6. **User Response:** *"Yes, use HTTP 429 with standard JSON and Retry-After."*
7. **Doc-Sync Action:** 
   - Updates `docs/tech/api/contracts.md` with the 429 specification.
   - Appends a log under `## Decisions & Revisions`.
8. **Implementer Execution:** Reads the updated spec and writes the middleware code and unit tests matching the exact documented contract.