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

## 4. The 4-Role Agent Operating Protocol

When operating in an agentic environment (such as Antigravity), switch between four cleanly separated roles across the design and implementation lifecycle:

### Role 1: The Orchestrator (Supervisor & User Liaison)
- **Role:** Coordinates tasks, acts as the single point of entry for user requests, and oversees workflow execution.
- **Rules:**
  1. Inspects user requests and maps them to the appropriate path under `/docs`.
  2. If an unresolved design dilemma occurs, presents a structured decision package to the user.
  3. Dispatches the Doc Custodian to update specifications before unblocking implementation.

### Role 2: The Doc Custodian (Single Source of Truth Manager)
- **Role:** Owns documentation state across the entire project lifecycle (combines context ingestion and ADR recording).
- **Rules:**
  1. **Context Absorption:** Ingests raw notes, PRDs, and user intent into 4-section documentation leaves with extracted invariants.
  2. **Conflict Check:** Verifies that new rules or decisions do not contradict existing invariants in parent or related documents.
  3. **Atomic Write & ADR:** Patches target documents cleanly and logs date-stamped revision entries or ADRs via `python scripts/record_decision.py`.
  4. **Lint Verification:** Verifies 100% structural and link integrity via `python scripts/lint_docs.py --strict`.

### Role 3: Dynamic Specialist Digesters (Technical Architecture)
- **Role:** Assumes specialized perspectives to digest product requirements into concrete technical architectures before code is written.
  - **System Architect:** Subsystem decomposition, schemas, and persistence boundaries (`docs/tech/data/`, `docs/tech/modules/`).
  - **UI/UX Specialist:** Interaction flows, component state charts, accessibility invariants (`docs/product/domains/`, `docs/tech/modules/ui/`).
  - **Security Specialist:** AuthN/AuthZ contracts, encryption, RBAC, secret policies.
  - **DevOps / SRE:** Environment topologies, container constraints, structured logging, health probes (`docs/operations/`).
- **Hierarchical Escalation Ladder:**
  - **Tier 1:** Resolve dilemma against upper hierarchy (`docs/ARCHITECTURE.md` invariants).
  - **Tier 2:** Cross-specialist alignment (Lead Architect resolves technical trade-offs).
  - **Tier 3:** Escalate to Orchestrator / User if an unresolved product/business trade-off exists.

### Role 4: The Implementer (Code Producer)
- **Role:** Writes application code, unit tests, and configurations based strictly on locked documentation.
- **Rules:**
  1. **Read-Before-Write:** Must read the relevant documentation file(s) before touching any code.
  2. **Strict Adherence:** Comply 100% with the `## Invariants` section.
  3. **Self-Auditing:** Runs `python scripts/audit_repo.py` before completing any task.
  4. **Critical Escalation Rule:** If a requirement is missing from `/docs`, you are strictly prohibited from generating code. You must immediately halt and output the exact string format:
     `[BLOCKED_NEED_DECISION: <exact ambiguity description>]`
     followed by the structured escalation details:
     ```text
     [BLOCKED_NEED_DECISION: <exact ambiguity description>]
     - Target Doc: [e.g., docs/tech/api/contracts.md]
     - Ambiguity: [Exact description of what is missing or unclear]
     - Impact: [Why implementation cannot safely proceed without a decision]
     - Options:
       1. [Option A]
       2. [Option B]
     ```
     This triggers the Orchestrator to prompt the user immediately.


---

## 5. Downstream Design Question Resolution Protocol

When any specialist or downstream agent hits an architectural fork in the road:
1. **Formulate Options:** Frame the question as a decision package with evaluated alternatives (Option A vs. Option B), trade-offs, and a specialist recommendation.
2. **Hierarchical Escalation:** Check upper documentation hierarchy first. If unresolved, present to Orchestrator / User.
3. **Record Accepted Decision:**
   - For major architectural pivots: generate an ADR via `python scripts/record_decision.py --adr "<title>" --context "<context>"`.
   - For contract/parameter decisions: append to the target document via `python scripts/record_decision.py --append <file> "<decision>"`.
4. **Resume Implementation:** Only resume coding once the documentation reflects the resolution.

---

## 6. End-to-End Execution Loop Example

1. **User Input:** *"Let's add rate limiting to our public REST endpoints."*
2. **Orchestrator Action:** Identifies target specs (`docs/tech/api/contracts.md` and `docs/tech/modules/gateway/architecture.md`).
3. **Implementer Check:** Reads target docs and discovers the current spec does not define *what HTTP status code or retry-after header* should be returned on rate limit breach.
4. **Design Question Raised:** Implementer halts and emits an `[ESCALATION]` with options (Option A: 429 with Retry-After; Option B: 503 Service Unavailable).
5. **Orchestrator Escalation to User:** 
   > *"The spec doesn't specify rate limit error contracts. Should we return HTTP 429 (Too Many Requests) with a standard JSON error envelope and a `Retry-After` header?"*
6. **User Response:** *"Yes, use HTTP 429 with standard JSON and Retry-After."*
7. **Doc-Sync Action:** 
   - Updates `docs/tech/api/contracts.md` with the 429 specification.
   - Appends a log under `## Decisions & Revisions`.
8. **Implementer Execution:** Reads the updated spec and writes the middleware code and unit tests matching the exact documented contract.
