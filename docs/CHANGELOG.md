# Repository Changelog & Revision Ledger

Scope: Global Project - Changelist History & Release Notes
Related: docs/ARCHITECTURE.md, docs/operations/changelist.md

## 1. Responsibilities & Boundaries
- **Owns:** The authoritative living ledger of all versioned changes, feature releases, invariant modifications, and bug fixes across the repository.
- **Does NOT Own:** Architectural design documents (owned by `docs/tech/`) or product roadmaps (owned by `docs/product/`).

## 2. Invariants (Hard Rules)
- All entries must adhere to the standard changelist entry schema defined in `docs/operations/changelist.md`.
- Changes affecting `## 2. Invariants (Hard Rules)` in any spec must be flagged under the `Invariants` category.
- Unreleased modifications must be tracked under `## [Unreleased]` until tagged for release.

## 3. Specifications & Interfaces

### [Unreleased]

#### Added
- **Changelist Tracking Framework:**
  - **Category:** Added
  - **Summary:** Introduced automated changelist tracking tooling (`scripts/track_changelist.py`, `harness changelist`), operational specification (`docs/operations/changelist.md`), and living ledger (`docs/CHANGELOG.md`).
  - **Affected Specs:** `docs/operations/changelist.md`, `docs/CHANGELOG.md`
  - **Affected Modules:** `scripts/track_changelist.py`, `scripts/harness.py`, `.agent/workflows/changelist_tracking_loop.md`
  - **Decision Ref:** Task: Add changelist tracking to the repo

- **Machine-Enforced Escalation Protocol:**
  - **Category:** Added
  - **Summary:** Added explicit `[BLOCKED_NEED_DECISION: <ambiguity>]` programmatic token to agent system directives and escalation workflow.
  - **Affected Specs:** `agent_system_prompt.md`, `instructions/master_system_prompt.md`, `AGENTS.md`, `.agent/workflows/escalation_loop.md`
  - **Affected Modules:** None (spec directives)
  - **Decision Ref:** Self-guardrailed Meta-Generator Framework enhancements

- **Dual-Wired Pre-Commit Health Hooks:**
  - **Category:** Added
  - **Summary:** Wired Git hooks to both `.githooks` and `.git/hooks/pre-commit` with automatic installation on project bootstrap.
  - **Affected Specs:** `ARCHITECTURE.md`, `docs/operations/deployment.md`
  - **Affected Modules:** `scripts/install_hooks.py`, `scripts/bootstrap_project.py`
  - **Decision Ref:** Automated verification gate implementation

- **Context Bundler & Subagent Prompt Packer:**
  - **Category:** Added
  - **Summary:** Added `scripts/pack_context.py` and `harness pack` command to slice minimal specifications, invariants, contracts, and ADRs for subagents.
  - **Affected Specs:** `ARCHITECTURE.md`, `AGENTS.md`
  - **Affected Modules:** `scripts/pack_context.py`, `scripts/harness.py`
  - **Decision Ref:** Autonomous agent context optimization

- **Unified Invariant & Unit Test Suite Runner:**
  - **Category:** Added
  - **Summary:** Added `scripts/run_tests.py` and `harness test` command; updated invariant test scaffolding to generate cross-platform `unittest.TestCase` suites.
  - **Affected Specs:** `ARCHITECTURE.md`, `AGENTS.md`, `.github/PULL_REQUEST_TEMPLATE.md`
  - **Affected Modules:** `scripts/run_tests.py`, `scripts/generate_invariant_tests.py`, `tests/test_invariants.py`
  - **Decision Ref:** Continuous invariant verification

- **Repository Governance Standards (LICENSE & SECURITY):**
  - **Category:** Added
  - **Summary:** Established open-source MIT License and formal Security Policy (`SECURITY.md`) with non-negotiable security invariants.
  - **Affected Specs:** `SECURITY.md`, `LICENSE`, `ARCHITECTURE.md`
  - **Affected Modules:** None
  - **Decision Ref:** Enterprise readiness & disclosure protocol


### [1.0.0] - 2026-10-10

#### Added
- **Core Doc-to-Code Framework:**
  - Baseline architecture, 4-section documentation standards, agent personas (Orchestrator, Doc-Sync, Specialist Digesters, Implementer).
  - Repository audit suite (`scripts/audit_repo.py`, `scripts/lint_docs.py`, `scripts/check_doc_drift.py`).
  - Living index generator (`scripts/generate_doc_index.py`).

## 4. Decisions & Revisions
- 2026-10-24: Initialized repository changelist tracking ledger.
- 2026-10-10: Template repository baseline release 1.0.0 established.
