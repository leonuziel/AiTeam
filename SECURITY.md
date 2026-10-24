# Security Policy

## Supported Versions

| Version | Supported          |
| :---    | :---               |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

---

## 1. Security Invariants (Non-Negotiable)

1. **Zero Secret Commit Invariant:**  
   Secret credentials, private keys, API tokens, and production environment values must NEVER be committed to the repository. All secrets must be injected via runtime environment variables or KMS / Secret Managers.
2. **Deterministic Authentication & Least Privilege:**  
   All endpoints and background tasks must define and adhere to the explicit authorization contracts specified under `docs/tech/api/` and `docs/operations/`.
3. **Escalate on Security Ambiguity:**  
   If an agent or engineer is unsure of the authentication, sanitization, or permission requirements for a feature, they are strictly prohibited from implementing speculative logic. They must emit `[BLOCKED_NEED_DECISION: <ambiguity>]` and escalate immediately.

---

## 2. Reporting a Vulnerability

If you discover a potential security vulnerability within this repository or a project bootstrapped from this template:

1. **Do NOT open a public GitHub issue.**
2. Send a detailed vulnerability report via private advisory on GitHub or email the repository maintainers.
3. Include:
   - Description of the vulnerability and its potential impact.
   - Exact steps or minimal proof of concept to reproduce.
   - Affected files and documentation specifications.
   - Any proposed invariant updates or remediation patches.

We will acknowledge receipt within 48 hours and work with you on a coordinated disclosure timeline.
