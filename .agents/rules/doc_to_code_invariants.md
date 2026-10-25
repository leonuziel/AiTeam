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

5. **Continuous Auto-Advancement (Turbo Mode & Exhaustion Gate):**
   - When an active roadmap or backlog is assigned, **never halt prematurely to ask for conversational confirmation** ("Should I proceed?", "Would you like me to continue?").
   - Before yielding a turn, verify task completion via `python scripts/harness.py next`. If incomplete tasks or audit issues remain and no blocking design question exists, **immediately execute the next task autonomously in the same turn**.

6. **Pragmatic SOLID & Clean Code Standards:**
   - **SRP:** Classes have one reason to change; functions do one thing. Keep files < 300–400 lines; functions < 30–50 lines. Isolate pure logic from I/O (*Functional Core, Imperative Shell*).
   - **OCP:** Use registries, strategy patterns, or dispatch maps rather than sprawling switch/if-else blocks.
   - **LSP:** Adapter implementations must honor base contracts without throwing unexpected runtime exceptions.
   - **ISP:** Keep interfaces lean. Do not force callers to provide unused dummy arguments.
   - **DIP:** Invert dependencies via constructor injection (storage, network, clock, PRNG seeds) with default parameters. Never hardcode global singletons (`localStorage`, `window`, `Math.random`) inside core domain logic.
   - **KISS & YAGNI:** Avoid speculative abstractions. Do not create an interface/factory without multiple concrete implementations or an explicit requirement.
