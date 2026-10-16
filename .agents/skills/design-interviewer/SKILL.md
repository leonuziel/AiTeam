---
name: design-interviewer
description: Interactive design decision escalation interviewer. Guides agents and users in formulating structured decision packages (Option A vs Option B) when hitting forks in the road and recording ADRs.
---

# Design Interviewer Skill

This skill governs how agents interact with the user or lead architect when encountering an architectural fork in the road, an ambiguous product requirement, or an unhandled edge case.

## Protocol: The Structured Decision Package

When an unresolvable trade-off is reached:
1. **Never guess or invent business logic silently in code.**
2. **Halt code generation immediately.**
3. **Formulate a structured Decision Package:**

```markdown
### ❓ [DESIGN QUESTION]: <Concise Title>
- **Target Specification:** [e.g. `docs/tech/api/contracts.md`]
- **Context & Dilemma:** <Why a fork exists and what triggered it>
- **Impacted Invariants:** <Existing rules affected>

#### Options Considered:
- **Option A: <Title>**
  - *Pros:* <Advantages>
  - *Cons / Trade-offs:* <Costs or limitations>
- **Option B: <Title>**
  - *Pros:* <Advantages>
  - *Cons / Trade-offs:* <Costs or limitations>

#### 💡 Agent Recommendation:
<Recommended Option> &mdash; *Rationale:* <Why this aligns with system invariants and scalability>
```

## Recording the Human Decision

Once the human selects an option (e.g. via chat or interactive CLI):
1. **Log the ADR:**
   ```bash
   python scripts/harness.py adr "<Decision Title>"
   ```
2. **Update the Target Specification:**
   - Update `## 2. Invariants` or `## 3. Specifications` in the target doc.
   - Append an entry to `## 4. Decisions & Revisions`:
     ```bash
     python scripts/harness.py append <target_doc> "Resolved design fork: adopted Option <X> (<Title>)"
     ```
3. **Resume Implementation:**
   Implement code and test assertions in lockstep with the documented decision.
