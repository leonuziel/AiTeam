# Template Master Map & Architecture

> **Doc-to-Code Autonomous Harness Master Map**  
> For the living, linted technical specification, see [docs/ARCHITECTURE.md](file:///d:/Workspace/AiTeam/docs/ARCHITECTURE.md).  
> For the full catalog of documentation leaves, see [docs/INDEX.md](file:///d:/Workspace/AiTeam/docs/INDEX.md).

---

## 1. Repository Topology

```text
AiTeam/
├── ARCHITECTURE.md                 # Template master map & routing index
├── CHANGELOG.md                    # Living release changelist pointer
├── LICENSE                         # Open-source MIT license
├── SECURITY.md                     # Security policies & invariant breach rules
├── agent_system_prompt.md          # Master agent directives & operating manual
├── agent_extensions.md             # Leaf templates, standards & linters
├── meta_generator_guide.md         # Template usage & generator guide
├── AGENTS.md                       # Universal multi-agent operational rules
├── GEMINI.md                       # Antigravity & IDE workspace instructions
├── .githooks/                      # Pre-commit automated enforcement gates
│   └── pre-commit                  # Runs lint_docs.py and check_doc_drift.py
├── scripts/                        # Harness toolchain & automated verification
│   ├── harness.py                  # Single-command unified harness CLI
│   ├── audit_repo.py               # Complete health & readiness audit
│   ├── lint_docs.py                # 4-section structural & link integrity linter
│   ├── check_doc_drift.py          # Doc-to-code parity and drift detection
│   ├── track_changelist.py         # Changelist tracker, diff detector & validator
│   ├── pack_context.py             # Context bundler & subagent prompt packer
│   ├── run_tests.py                # Invariant & unit test suite runner
│   ├── bootstrap_project.py        # Project bootstrap wizard with auto-hooks
│   ├── install_hooks.py            # Git hook configurator
│   ├── scaffold_module.py          # Domain & module spec generator
│   ├── record_decision.py          # ADR and atomic revision logger
│   └── resolve_question.py         # Design resolution & ADR workflow
├── templates/                      # Standard blueprint schemas
│   ├── leaf-template.md            # Standard 4-section document template
│   ├── domain-template.md          # Product domain requirements & flows
│   ├── module-template.md          # Tech module architecture & interfaces
│   ├── api-contract-template.md    # API contract specification template
│   └── decision-record-template.md # Architecture Decision Record (ADR)
├── docs/                           # Single Source of Truth specification tree
│   ├── ARCHITECTURE.md             # System topology & global invariants
│   ├── INDEX.md                    # Living documentation index
│   ├── CHANGELOG.md                # Living changelog & revision ledger
│   ├── product/                    # What & Why (Requirements & Journeys)
│   │   ├── overview.md             # Core product vision & capabilities
│   │   └── domains/                # Domain functional feature sets
│   ├── tech/                       # How (Architecture & Cross-cutting Specs)
│   │   ├── overview.md             # Stack conventions & shared rules
│   │   ├── data/                   # Schemas, persistence & migration contracts
│   │   ├── api/                    # REST/gRPC contracts & error codes
│   │   └── modules/                # Subsystem technical designs
│   ├── operations/                 # Where & How it runs (Infra, CI/CD)
│   │   ├── deployment.md           # Environment tiers & deployment gates
│   │   ├── telemetry.md            # Observability & logging contracts
│   │   └── changelist.md           # Changelist tracking & traceability spec
│   └── decisions/                  # Architecture Decision Records (ADRs)
│       └── README.md
├── src/                            # Implementation source code (.gitkeep)
└── tests/                          # Automated test suites (.gitkeep)
```

---

## 2. The 4 Autonomous Enforcement Gates

1. **Spec-First Gate (Orchestrator):**  
   All features must exist in [docs/](file:///d:/Workspace/AiTeam/docs) with non-negotiable `## 2. Invariants` before code is written. If missing, execution halts with `[BLOCKED_NEED_DECISION: <ambiguity>]`.
2. **Doc-Sync Gate (Custodian):**  
   Any accepted decision or requirement update is atomically patched into the documentation tree and logged under `## 4. Decisions & Revisions` or as an ADR via `python scripts/record_decision.py`.
3. **Implementation Gate (Implementer):**  
   Reads locked documentation (`Read-Before-Write`) and implements code and unit tests adhering 100% to documented invariants.
4. **Health & Lint Gate (Automated Guardrail):**  
   Enforced locally via Git pre-commit hook (`.githooks/pre-commit`) and globally via `python scripts/audit_repo.py`. Build or commit fails if markdown drift, broken links, or undocumented code modules are detected.
