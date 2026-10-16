# Meta-Generator Guide: Bootstrapping Agentic Repositories

This document defines how this repository operates as a **reusable template** (meta-generator) rather than an application-specific codebase. 

## 1. Core Purpose of the Meta-Repo
This repository contains zero application code (`src/` is empty or reserved entirely for agentic scaffolding). Instead, it provides the pure **agent harness and knowledge topology** required to bootstrap any new software project.

## 2. What This Template Provides
- **Master Agent Directives (`agent_system_prompt.md`):** Defines the roles (Orchestrator, Doc-Sync, Implementer) and the strict escalation loops.
- **Agent Extensions & Utilities (`agent_extensions.md`):** Contains concrete leaf templates and project health linters.
- **Documentation Topology (`docs/`):** A pre-structured markdown hierarchy ready to receive product requirements, architecture specs, and operational guides.

## 3. How to Use This Template for a New Project
1. **Use as Template:** On GitHub, click **"Use this template"** to spin up a fresh repository for your new software project.
2. **Bootstrap Architecture:** Open the new repo in Antigravity or your agent environment and feed it the master prompt to begin the discovery and design cycle.
3. **Run Health Audits:** Use the built-in linter (`scripts/lint_docs.py`) to verify that all newly created documentation leaf nodes conform to the required layout and invariants before code writing begins.