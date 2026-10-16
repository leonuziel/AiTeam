## 🛡️ Doc-to-Code Compliance Gate

> **Single Source of Truth Invariant:**  
> Code implements specifications; code never invents specifications.

### 📋 Pre-Merge Checklist
Please confirm that your changes adhere to repository invariants before requesting review:

- [ ] **1. Specification Synchronization:** Relevant documentation files under `docs/` have been created or updated.
- [ ] **2. Invariant Compliance:** No non-negotiable rules under `## 2. Invariants (Hard Rules)` have been violated.
- [ ] **3. Decisions & Revisions:** All changes are accompanied by a date-stamped revision log under `## 4. Decisions & Revisions` or a new ADR in `docs/decisions/`.
- [ ] **4. Parity & Test Suite:** Application code in `src/` matches specifications 1:1, and test suites in `tests/` pass.
- [ ] **5. Master Audit:** `python scripts/harness.py audit` passes with a **100% health score**.

---

### 📝 Summary of Changes
- **Target Specification(s):** [e.g., `docs/tech/api/contracts.md`]
- **Core Changes:** [Brief summary of architectural and code modifications]
- **ADR Reference (if applicable):** [e.g., `docs/decisions/ADR-001-...`]
