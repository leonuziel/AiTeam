---
name: doc-harness
description: Unified Doc-to-Code harness commands for auditing, ingesting context, scaffolding modules, recording ADRs, and running health checks.
---

# Doc-to-Code Harness Skill

This skill guides agents and developers when operating within the Doc-to-Code Autonomous Harness repository.

## When to Use This Skill
- Running audits, linter checks, and parity verifications.
- Ingesting raw product context or PRDs into structured documentation.
- Scaffolding new product domains or technical modules.
- Recording Architecture Decision Records (ADRs) or appending atomic revision logs.
- Bootstrapping a fresh downstream project.

## Harness CLI Reference

All repository operations are managed through the unified CLI: `python scripts/harness.py`.

### 1. Repository Health & Gating
```bash
# Run the complete master health audit (must score 100%)
python scripts/harness.py audit

# Run documentation structural & link linter
python scripts/harness.py lint

# Run doc-to-code parity and drift audit
python scripts/harness.py parity

# Install git pre-commit hooks
python scripts/harness.py install-hooks
```

### 2. Context Ingestion & Documentation
```bash
# Ingest notes into a documentation file
python scripts/harness.py ingest --target docs/product/overview.md --notes "We are building a multi-tenant payment service."

# Append an atomic revision log
python scripts/harness.py append docs/tech/api/contracts.md "Added rate limit header contracts"
```

### 3. Architecture Decision Records (ADR)
```bash
# Record a new Architecture Decision Record
python scripts/harness.py adr "Adopt EdDSA for Token Signatures"
```

### 4. Module & Domain Scaffolding
```bash
# Scaffold a new product domain leaf
python scripts/harness.py scaffold --domain billing

# Scaffold a new technical module (docs + src/ + tests/)
python scripts/harness.py scaffold --module auth
```

### 5. Diagnostics, Hygiene & Verification
```bash
# Run comprehensive template self-diagnostics and auto-repair
python scripts/harness.py doctor --fix

# Reclaim space and clean compiler caches & scratchpad
python scripts/harness.py clean

# Scan for phantom files, broken imports, or hallucinated links
python scripts/harness.py sentinel --strict

# Validate documentation hierarchy and DAG cross-references
python scripts/harness.py doc-dag --strict

# Scan for exposed credentials or API keys
python scripts/harness.py scan-secrets

# Continuous turbo autopilot task advancement
python scripts/harness.py next
```

### 6. Project Bootstrapping
```bash
# Clean out template examples and re-brand for a new project with architecture presets
python scripts/harness.py bootstrap --name "MyPaymentGateway" --preset backend
```

## Agent Directives Checklist
1. **Read-Before-Write:** Always read the corresponding `docs/` specifications before editing `src/` or `tests/`.
2. **Strict Invariants:** Never violate `## 2. Invariants (Hard Rules)` in any document.
3. **No Code Without Docs:** If functionality is needed, document it first under `docs/` with all 4 required sections.
4. **Zero Drift:** Run `python scripts/harness.py audit` before completing any task.
