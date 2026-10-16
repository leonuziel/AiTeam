# API Error Handling & Resilience Protocols

Scope: Technical Architecture - Error Handling & Resilience Layer
Related: docs/tech/overview.md, docs/tech/api/contracts.md

## 1. Responsibilities & Boundaries
- **Owns:** Standardized error response envelopes, domain error code taxonomies, client retry policies, and circuit breaking contracts.
- **Does NOT Own:** Subsystem business rules that trigger errors (owned by individual domain modules).

## 2. Invariants (Hard Rules)
- Stack traces or internal system paths must NEVER be exposed in public API error responses.
- Every error response must include a unique machine-readable `error_code` and a traceable `request_id`.
- Rate limiting breaches must return HTTP 429 with standard JSON and a `Retry-After` header.

## 3. Specifications & Interfaces
### Standard Error Envelope Format
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource could not be found.",
    "details": []
  },
  "meta": {
    "timestamp": "2026-10-10T12:00:00Z",
    "request_id": "req_abc123"
  }
}
```

### Common Error Code Taxonomy
- `VALIDATION_ERROR`: Malformed input payload (HTTP 400)
- `UNAUTHORIZED`: Authentication missing or invalid (HTTP 401)
- `FORBIDDEN`: Insufficient role or access permissions (HTTP 403)
- `RESOURCE_NOT_FOUND`: Target entity does not exist (HTTP 404)
- `RATE_LIMIT_EXCEEDED`: Request frequency limit breached (HTTP 429)
- `INTERNAL_SERVER_ERROR`: Unhandled operational defect (HTTP 500)

## 4. Decisions & Revisions
- 2026-10-10: Baseline error taxonomy and envelope contract established for template repository.
