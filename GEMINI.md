# Antigravity & Gemini Workspace Instructions

This repository operates under the **Doc-to-Code Autonomous Harness**.
All AI agents and assistants working in this codebase must adhere strictly to:

- [AGENTS.md](file:///d:/Workspace/AiTeam/AGENTS.md) &mdash; Universal Agent Operating Directives.
- [agent_system_prompt.md](file:///d:/Workspace/AiTeam/agent_system_prompt.md) &mdash; Master Agent Blueprint (Orchestrator, Doc-Sync, Implementer).
- [agent_extensions.md](file:///d:/Workspace/AiTeam/agent_extensions.md) &mdash; Standards, Linters, and Templates.

### Key Workflows
- **Context Ingestion Loop:** [.agent/workflows/context_ingestion_loop.md](file:///d:/Workspace/AiTeam/.agent/workflows/context_ingestion_loop.md) &mdash; Ingest raw context/PRDs into docs.
- **Design Resolution Loop:** [.agent/workflows/design_resolution_loop.md](file:///d:/Workspace/AiTeam/.agent/workflows/design_resolution_loop.md) &mdash; Bubble up and record design decisions.
- **Escalation Protocol:** [.agent/workflows/escalation_loop.md](file:///d:/Workspace/AiTeam/.agent/workflows/escalation_loop.md) &mdash; Fail-fast on ambiguity.
- **Doc-Sync Loop:** [.agent/workflows/doc_sync_loop.md](file:///d:/Workspace/AiTeam/.agent/workflows/doc_sync_loop.md) &mdash; Atomic doc updates & revision logging.
- **Continuous Cleanliness:** [.agent/workflows/continuous_cleanliness_loop.md](file:///d:/Workspace/AiTeam/.agent/workflows/continuous_cleanliness_loop.md) &mdash; Hygiene checks.

### Verification Commands
Before completing any task, execute:
```bash
python scripts/audit_repo.py
```
Ensure 100% health score.
