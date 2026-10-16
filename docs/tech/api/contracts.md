# API Protocols & Contracts

Scope: Technical Architecture - External & Internal API Layer
Related: docs/tech/overview.md, docs/tech/api/error-handling.md

## 1. Responsibilities & Boundaries
- **Owns:** API architectural styles (REST, gRPC, WebSocket), endpoint conventions, URI routing standards, serialization formats, and authentication header policies.
- **Does NOT Own:** Subsystem internal business operations (owned by `docs/tech/modules/`) or standard error payloads (owned by `docs/tech/api/error-handling.md`).

## 2. Invariants (Hard Rules)
- All public endpoints must enforce authenticated or explicit public authorization contracts.
- Breaking API contract changes require explicit versioning (`/api/v1/`, `/api/v2/`).
- Payloads must strictly validate against input DTO schemas; unvalidated payloads must be rejected immediately.

## 3. Specifications & Interfaces
### Standard Request / Response Envelope
```json
{
  "success": true,
  "data": {},
  "meta": {
    "timestamp": "2026-10-10T12:00:00Z",
    "request_id": "req_abc123"
  }
}
```

### Protocol Guidelines
- REST: Resource-oriented, lowercase hyphen-separated paths (e.g., `/api/v1/user-profiles`).
- HTTP Status Codes: Adhere to standard semantic definitions (200, 201, 204, 400, 401, 403, 404, 429, 500).

## 4. Decisions & Revisions
- 2026-10-10: Baseline API contracts and serialization established for template repository.
