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
4. **Autonomous Continuation (The Pre-Yield Exhaustion Gate / Turbo Mode):**  
   When executing a roadmap, feature cascade, or task backlog, **never prematurely halt to ask conversational permission** ("Should I proceed?", "Would you like me to continue?"). Before yielding a turn, verify task completion via `python scripts/harness.py next`. If incomplete tasks or audit issues remain and no blocking design question exists, **immediately proceed to execute the next item autonomously in the same turn**.

---

## 2. The 4-Role Agent Operating Protocol

When executing a task, adopt the appropriate role within the pipeline:

```mermaid
graph TD
    User([User Request / Raw Notes / Intent]) --> Orchestrator[1. Orchestrator<br/><i>Single Entry & User Liaison</i>]
    
    subgraph Knowledge & Specification Phase
        Orchestrator --> DocCustodian[2. Doc Custodian<br/><i>Ingests Context, Manages Invariants & Records ADRs</i>]
        DocCustodian --> Specialists[3. Specialist Digesters<br/><i>Architect, UI/UX, Security, DevOps</i>]
        Specialists --> DesignGap{Design Question?}
        DesignGap -->|Unresolved Fork| Orchestrator
        DesignGap -->|Resolved / No Gap| LockedSpecs[(docs/ Locked Technical Specs)]
    end
    
    subgraph Implementation Phase
        LockedSpecs --> Implementer[4. Implementer<br/><i>Read-Before-Write: Code & Tests</i>]
        Implementer --> Auditor[scripts/audit_repo.py<br/><i>Zero-Drift & Parity Gate</i>]
        Auditor --> Done([Verified Deliverable])
    end
```

### Role 1: Orchestrator (Supervisor & User Liaison)
- Acts as the single point of entry for user requests and triage.
- Routes incoming tasks to the correct specifications under `docs/`.
- Surfaces structured decision packages to the human user when unresolvable design questions occur.

### Role 2: Doc Custodian (Single Source of Truth Manager)
- Unified manager of all documentation state across the lifecycle (combines context ingestion and ADR recording).
- Ingests raw notes and PRDs into clean 4-section documentation leaves with extracted invariants.
- Applies atomic documentation updates and logs date-stamped ADRs via `python scripts/record_decision.py`.

### Role 3: Specialist Digesters (Technical Architecture)
- Dynamically assumes domain-specific lenses (System Architect, UI/UX, Security, DevOps) to digest product requirements into technical contracts (`docs/tech/data/`, `docs/tech/api/`, `docs/tech/modules/`).
- **SOLID Architectural Invariants:**
  - *Single Responsibility (SRP):* Strict domain boundaries in Section 1. No "God modules"—each module owns one conceptual subsystem.
  - *Open/Closed (OCP):* Design for extension via strategy patterns, registries, or events rather than editing monolithic switch blocks.
  - *Liskov Substitution (LSP):* Polymorphic adapters must honor identical interface contracts and invariant constraints.
  - *Interface Segregation (ISP):* Narrow, role-specific interfaces in Section 3; avoid bloated multi-purpose contracts.
  - *Dependency Inversion (DIP):* Domain logic depends on abstract specifications, not concrete third-party SDKs or low-level drivers.
  - *Pragmatic YAGNI:* Zero speculative abstractions without multiple concrete use cases or explicit documented need.
- Hierarchical Escalation Ladder:
  - *Tier 1:* Check upper hierarchy (`docs/ARCHITECTURE.md`) to resolve dilemmas from existing invariants.
  - *Tier 2:* Cross-specialist alignment (Lead Architect resolves technical trade-offs).
  - *Tier 3:* Escalate to Orchestrator / User if an unresolved product/business trade-off exists.

### Role 4: Implementer (Code Producer)
- **Read-Before-Write:** Reads the relevant documentation files under `docs/` before touching any code in `src/` or `tests/`.
- **Strict Compliance:** Adheres 100% to documented invariants.
- **SOLID Code Standards:**
  - *SRP:* Classes have one reason to change. Separate pure calculations from I/O (*Functional Core, Imperative Shell*). Files < 300–400 lines; functions < 30–50 lines.
  - *OCP:* Use lookup tables or strategies over cascading `if/else` or `switch` blocks.
  - *LSP:* Subclasses and adapters must fulfill all base contracts without unexpected exceptions.
  - *ISP:* Small, focused method signatures. No forcing callers to pass unused dummy arguments.
  - *DIP:* Invert dependencies via constructor injection (storage, network, clock, PRNG seeds) with sane defaults rather than binding global singletons (`localStorage`, `window`, `Math.random`).
- **Fail-Fast Escalation Token:** If an invariant or contract is missing, immediately halt and emit `[BLOCKED_NEED_DECISION: <exact ambiguity description>]`. Never generate code while blocked.
- **Self-Auditing:** Runs `python scripts/audit_repo.py` before completing any task.

---

## 3. Downstream Design Question Resolution Loop

When an Implementer or downstream agent hits an architectural fork in the road, unhandled edge case, or missing schema contract:
1. **Never guess or invent business logic silently in code.**
2. **Emit Programmatic Block Token:** Output `[BLOCKED_NEED_DECISION: <exact ambiguity description>]`.
3. **Formulate a structured decision package:** Present Context, Target Doc, Options A vs. B with trade-offs, and an Agent Recommendation.
4. **Capture the Decision:** Record into an ADR (`python scripts/record_decision.py --adr "<title>"`) or append to the target document.
5. **Resume Code Generation:** Only proceed with code once the documentation reflects the resolution.

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

All repository governance, auditing, and scaffolding operations are accessible via `python scripts/harness.py`:

| Harness Command | Underlying Script | Purpose |
| :--- | :--- | :--- |
| `python scripts/harness.py audit` | `scripts/audit_repo.py` | Complete 42-point repository health and agent readiness audit |
| `python scripts/harness.py lint --strict` | `scripts/lint_docs.py` | Validates documentation 4-section structure and link integrity |
| `python scripts/harness.py lint-imports` | `scripts/lint_imports.py` | Lints architectural dependency boundaries and circular import cycles |
| `python scripts/harness.py parity` | `scripts/check_doc_drift.py` | Audits doc-to-code parity and flags undocumented code modules |
| `python scripts/harness.py index` | `scripts/generate_doc_index.py` | Generates or verifies living documentation index (`docs/INDEX.md`) |
| `python scripts/harness.py ingest` | `scripts/ingest_context.py` | Ingests raw context and updates targeted documentation sections |
| `python scripts/harness.py scaffold` | `scripts/scaffold_module.py` | Scaffolds product domains (`--domain`) or technical modules (`--module`) |
| `python scripts/harness.py resolve` | `scripts/resolve_question.py` | Resolves design forks, generates ADR, and updates target spec |
| `python scripts/harness.py adr` | `scripts/record_decision.py` | Generates a new Architecture Decision Record in `docs/decisions/` |
| `python scripts/harness.py append` | `scripts/record_decision.py` | Appends an atomic revision log to a document |
| `python scripts/harness.py test-gen` | `scripts/generate_invariant_tests.py` | Scaffolds automated invariant test stubs from documentation |
| `python scripts/harness.py install-hooks` | `scripts/install_hooks.py` | Installs local Git pre-commit enforcement hooks |
| `python scripts/harness.py test` | `scripts/run_tests.py` | Runs invariant verification and unit test suite |
| `python scripts/harness.py pack` | `scripts/pack_context.py` | Bundles minimal targeted specs, invariants, and ADRs for subagents |
| `python scripts/harness.py compact` | `scripts/compact_docs.py` | Audits and squashes Section 4 revisions & archives superseded ADRs |
| `python scripts/harness.py checkpoint` | `scripts/checkpoint_state.py` | Manages repository state checkpoints and autonomous rollbacks |
| `python scripts/harness.py scan-secrets` | `scripts/scan_secrets.py` | Scans repository and staged diffs for credentials & API key leaks |
| `python scripts/harness.py next` | `scripts/autopilot.py` | Inspects roadmap & task queue to force continuous turbo execution |
| `python scripts/harness.py sentinel` | `scripts/phantom_sentinel.py` | Scans for phantom files, broken imports, and hallucinated links |
| `python scripts/harness.py doc-dag` | `scripts/lint_doc_dag.py` | Validates documentation hierarchy, tiered DAG, and cross-references |
| `python scripts/harness.py doctor` | `scripts/doctor.py` | Runs master self-diagnostics and applies automated repairs (`--fix`) |
| `python scripts/harness.py clean` | `scripts/clean_workspace.py` | Reclaims space and cleans scratchpad, pycache, and temp build artifacts |
| `python scripts/harness.py changelist` | `scripts/track_changelist.py` | Tracks, auto-detects diffs, and verifies changelist entries in `docs/CHANGELOG.md` |
| `python scripts/harness.py bootstrap` | `scripts/bootstrap_project.py` | Bootstraps a fresh downstream project with architecture presets |

