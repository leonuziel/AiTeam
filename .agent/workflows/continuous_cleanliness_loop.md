# Workflow: Continuous Cleanliness & Health Maintenance Loop

## Purpose
Maintains zero architectural decay, prevents documentation bit rot, and verifies repository hygiene across all project iterations.

---

## Maintenance Trigger Points
- Before any Git commit or pull request.
- After merging major features or external dependency upgrades.
- Triggered by CI pipelines on push to `main`.

---

## 5-Point Cleanliness Checklist

### 1. Structural Invariants Check
```bash
python scripts/lint_docs.py --strict
```
Verifies that all documentation leaves contain all four mandatory sections (`Responsibilities & Boundaries`, `Invariants`, `Specifications & Interfaces`, `Decisions & Revisions`), valid `Scope:` / `Related:` metadata, and zero broken links.

### 2. Parity & Drift Check
```bash
python scripts/check_doc_drift.py
```
Ensures no ghost code resides under `src/` without matching specifications, and verifies test directory symmetry.

### 3. Decisions & Revisions Audit
Examines the target documentation files to ensure all architectural modifications made during the turn have a date-stamped log entry under `## 4. Decisions & Revisions`.

### 4. Zero Application Residue in Template Mode
If operating in template mode (prior to bootstrapping an application), confirms `src/` contains zero application code, maintaining clean template status.

### 5. Full Repository Health Sign-Off
```bash
python scripts/audit_repo.py
```
Validates 100% compliance score.
