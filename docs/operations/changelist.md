# Changelist & Revision Tracking

Scope: Operations & Lifecycle - Changelist Tracking & Traceability
Related: docs/ARCHITECTURE.md, docs/CHANGELOG.md, docs/operations/deployment.md

## 1. Responsibilities & Boundaries
- **Owns:** Standards, schema contracts, validation rules, and automation workflows for recording and maintaining atomic changelists across code and specifications.
- **Does NOT Own:** Raw Git version control history (managed by Git) or domain-specific business features (managed by `docs/product/`).

## 2. Invariants (Hard Rules)
- Every atomic release, milestone, or multi-file code change must append an entry to the changelist ledger in `docs/CHANGELOG.md`.
- Every changelist entry must specify:
  1. Change category (`Added`, `Changed`, `Fixed`, `Invariants`, `Security`, `Deprecated`, `Removed`).
  2. Targeted specification document(s) under `docs/`.
  3. Targeted implementation or test paths under `src/` and `tests/`.
  4. Traceability link (ADR reference or formal decision ID).
- Code changes in `src/` must never be released or promoted to main without a verified changelist entry.
- Changelist entries must be immutable once published in a release tag.

## 3. Specifications & Interfaces
### Canonical Changelist Entry Schema
```markdown
### [Version / Date / Identifier] - YYYY-MM-DD
- **Category:** Added | Changed | Fixed | Invariants | Security | Deprecated | Removed
- **Summary:** Concise description of the change and business rationale.
- **Affected Specs:** [docs/path/to/spec.md]
- **Affected Modules:** [src/module_name/], [tests/module_name/]
- **Decision Ref:** ADR-001 (or commit/issue reference)
```

### Automation & Tooling Integration
- CLI command: `python scripts/harness.py changelist`
- Verification script: `scripts/track_changelist.py`
  - `--record`: Record a new entry with metadata validation.
  - `--generate`: Inspect git diff and auto-populate affected specs and source paths.
  - `--verify`: Validate that all recent changes have corresponding changelist entries.

## 4. Decisions & Revisions
- 2026-10-24: Baseline changelist tracking specification and invariant rules established.
