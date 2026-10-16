# Rule: Doc-to-Code Operating Invariants

Always adhere to these rules when working in this workspace:

1. **Documentation is the Single Source of Truth:**
   - Always read relevant files in `docs/` before writing or modifying code in `src/`.
   - Never implement business rules or APIs that are not documented in `docs/`.

2. **Strict Invariant Adherence:**
   - Comply 100% with the `## 2. Invariants` section in target docs.
   - If an invariant cannot be satisfied, do not hack a workaround; escalate to the user.

3. **Fail-Fast Escalation:**
   - If a requirement, edge case, or contract is missing or ambiguous, halt immediately and ask the user for clarification.
   - Update the documentation with the user's decision before writing implementation code.

4. **Self-Auditing:**
   - Run `python scripts/audit_repo.py` and `python scripts/lint_docs.py --strict` to verify changes before marking any task as complete.
