# Deployment & Environment Topology

Scope: Operations & Infrastructure - Deployment Lifecycle
Related: docs/ARCHITECTURE.md, docs/operations/telemetry.md

## 1. Responsibilities & Boundaries
- **Owns:** Target environments (local, staging, production), containerization contracts, CI/CD pipeline stages, and secret management conventions.
- **Does NOT Own:** Subsystem application code logic (owned by `src/` and `docs/tech/modules/`).

## 2. Invariants (Hard Rules)
- Production secrets must never be committed to repository files; environment variables or secret vaults must be used exclusively.
- All deployments must be automated, reproducible, and verifiable via automated integration/health checks.
- Container images or build artifacts must be immutable and version-tagged.

## 3. Specifications & Interfaces
### Environment Tiers
- **Development / Local:** Fast feedback, mocked external services where applicable.
- **Staging / QA:** Mirror of production infrastructure; used for pre-release validation.
- **Production:** High availability, redundant infrastructure, least-privilege security scoping.

### Baseline CI/CD Pipeline Gates
1. Code formatting & static analysis.
2. Documentation structural linting (`scripts/lint_docs.py`).
3. Automated unit and contract test suites.
4. Containerization and artifact registry publishing.

## 4. Decisions & Revisions
- 2026-10-10: Baseline deployment lifecycle and environment topology established for template repository.
