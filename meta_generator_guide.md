# Meta-Generator Guide: Bootstrapping Agentic Repositories

This document defines how this repository operates as a **reusable template** (meta-generator) rather than an application-specific codebase. 

## 1. Core Purpose of the Meta-Repo
This repository contains zero application code (`src/` is empty or reserved entirely for agentic scaffolding). Instead, it provides the pure **agent harness and knowledge topology** required to bootstrap any new software project.

## 2. What This Template Provides
- **Master Agent Directives (`agent_system_prompt.md`):** Defines the roles (Orchestrator, Doc-Sync, Implementer, Context Ingestion) and the strict escalation loops.
- **Agent Extensions & Utilities (`agent_extensions.md`):** Contains concrete leaf templates and project health linters.
- **Agentic Workflows (`.agent/workflows/`):** Dedicated loops for Context Ingestion, Design Question Resolution, Doc-Sync, and Continuous Cleanliness.
- **Documentation Topology (`docs/`):** A pre-structured markdown hierarchy ready to receive product requirements, architecture specs, and operational guides.

## 3. How to Use This Template for a New Project
1. **Use as Template:** On GitHub, click **"Use this template"** to spin up a fresh repository for your new software project.
2. **Bootstrap Context:** Feed the agent raw project requirements or PRDs using the **Context Ingestion Loop** to populate `docs/` before writing any code.
3. **Resolve Design Questions:** As implementation progresses, downstream agents raise design questions with evaluated trade-offs, automatically logged to ADRs.
4. **Run Health Audits:** Use the built-in audit suite (`python scripts/audit_repo.py`) to verify that all documentation and code remain 100% compliant.
