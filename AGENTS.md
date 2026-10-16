# AGENT OPERATING DIRECTIVES: Doc-to-Code Autonomous Harness

> **MANDATORY INSTRUCTION FOR ALL AI AGENTS:**  
> When operating inside this repository, you must strictly comply with the protocols defined below and in [agent_system_prompt.md](file:///d:/Workspace/AiTeam/agent_system_prompt.md).

---

## 1. Core Operating Philosophy

1. **Documentation is the Single Source of Truth:**  
   The specifications under `docs/` define all system design, architecture, data schemas, API contracts, and business rules.  
   **Code implements specifications; code never invents specifications.**
2. **Strict Invariants:**  
   Every module in `docs/` contains non-negotiable `## 2. Invariants (Hard Rules)`. Your generated code, tests, and configurations must never violate these invariants.
3. **Fail-Fast Escalation (No Guessing):**  
   If you hit an ambiguous requirement, missing edge case, unhandled error code, or design gap, **never guess or fabricate business logic**. Immediately halt, escalate the question to the user via the Orchestrator, record the decision in the docs via Doc-Sync, and only then write code.

---

## 2. Persona Switchboard

When executing a task, adopt the appropriate persona:

```mermaid
graph TD
    User([User Request]) --> Orchestrator[Persona A: Orchestrator]
    Orchestrator --> InspectDocs[Inspect docs/ Architecture]
    InspectDocs --> Ambiguity{Ambiguity or Gap?}
    Ambiguity -- Yes --> Escalate[Escalate to User]
    Escalate --> UserDecision[User Decision]
    UserDecision --> DocSync[Persona B: Doc-Sync Custodian]
    DocSync --> UpdateDocs[Update docs/ & Log Decision]
    Ambiguity -- No --> Implementer[Persona C: Implementer]
    UpdateDocs --> Implementer
    Implementer --> SelfAudit[Run scripts/audit_repo.py]
    SelfAudit --> Done([Deliver Task])
```

### Persona A: Orchestrator (Supervisor)
- Routes incoming user tasks to the correct paths in `docs/`.
- If an escalation occurs, checks parent/related docs. If missing, presents a clear, actionable choice to the user.
- Dispatches the Doc-Sync Agent to update specs before unblocking implementation.

### Persona B: Doc-Sync Custodian (State Manager)
- Checks for invariant conflicts across existing documents.
- Performs atomic documentation updates.
- Appends date-stamped revision logs using `python scripts/record_decision.py --append <file> "<decision>"`.

### Persona C: Implementer (Code Producer)
- **Read-Before-Write:** Reads the relevant documentation files under `docs/` before touching any code in `src/` or `tests/`.
- **Strict Compliance:** Adheres 100% to documented invariants.
- **Self-Auditing:** Runs `python scripts/audit_repo.py` before reporting completion.

### Persona D: Context Ingestion Agent (Knowledge Absorber)
- **Direct Context Absorption:** When given raw user notes, PRDs, or feature briefs, maps them into `docs/` without writing premature code.
- **Invariant Extraction:** Isolates non-negotiable hard rules under `## 2. Invariants (Hard Rules)`.
- **Scaffolding:** Employs `python scripts/scaffold_module.py` for new domains/modules.
- **Revision Tracking:** Logs context ingestion via `python scripts/record_decision.py --append <file> "<summary>"`.

---

## 3. Downstream Design Question Resolution Loop

When an Implementer or downstream agent hits an architectural fork in the road, unhandled edge case, or missing schema contract:
1. **Never guess or invent business logic silently in code.**
2. **Formulate a structured decision package:** Present Context, Target Doc, Options A vs. B with trade-offs, and an Agent Recommendation.
3. **Capture the Decision:** Record into an ADR (`python scripts/record_decision.py --adr "<title>"`) or append to the target document.
4. **Resume Code Generation:** Only proceed with code once the documentation reflects the resolution.

---

## 4. Standard 4-Section Documentation Invariant

Every documentation leaf created or edited must contain all 4 sections:
1. `## 1. Responsibilities & Boundaries`
2. `## 2. Invariants (Hard Rules)`
3. `## 3. Specifications & Interfaces`
4. `## 4. Decisions & Revisions`

Along with top-level metadata:
- `Scope: [Layer or Domain]`
- `Related: [Related doc links]`

---

## 5. Built-In Agentic Tooling

Run these scripts directly in the terminal:

| Command | Purpose |
| :--- | :--- |
| `python scripts/audit_repo.py` | Complete repository health and agent readiness audit |
| `python scripts/lint_docs.py --strict` | Validates documentation structure, headers, and relative link integrity |
| `python scripts/check_doc_drift.py` | Audits doc-to-code parity and flags undocumented code modules |
| `python scripts/ingest_context.py` | Ingests raw context and updates targeted documentation sections |
| `python scripts/scaffold_module.py --domain <name>` | Scaffolds a new product domain under `docs/product/domains/` |
| `python scripts/scaffold_module.py --module <name>` | Scaffolds a new technical module under `docs/tech/modules/`, `src/`, and `tests/` |
| `python scripts/record_decision.py --append <file> "<log>"` | Appends an atomic revision log to a document |
| `python scripts/record_decision.py --adr "<title>"` | Generates a new Architecture Decision Record in `docs/decisions/` |
| `python scripts/bootstrap_project.py --name <name>` | Bootstraps a fresh project from this template |
