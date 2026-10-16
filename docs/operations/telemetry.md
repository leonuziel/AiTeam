# Telemetry, Observability & Health Monitoring

Scope: Operations & Observability - Logging, Metrics, Tracing & Health
Related: docs/ARCHITECTURE.md, docs/operations/deployment.md

## 1. Responsibilities & Boundaries
- **Owns:** Structured logging conventions, application metrics collection, distributed tracing propagation, and health check endpoints.
- **Does NOT Own:** Business logic calculations that emit events (owned by domain modules).

## 2. Invariants (Hard Rules)
- All log output must be machine-parsable JSON containing timestamp, severity level, message, and `request_id` or `trace_id`.
- Personally Identifiable Information (PII) and secret credentials must be automatically redacted before writing to log streams.
- Services must provide unauthenticated `/healthz` (liveness) and `/ready` (readiness) probe endpoints for orchestrators.

## 3. Specifications & Interfaces
### Canonical Structured Log Schema
```json
{
  "timestamp": "2026-10-10T12:00:00.000Z",
  "level": "INFO",
  "message": "User authenticated successfully",
  "context": {
    "user_id": "usr_123",
    "request_id": "req_abc123"
  }
}
```

### Health Probe Contracts
- `GET /healthz`: Returns `200 OK` if the process is responsive.
- `GET /ready`: Returns `200 OK` if dependencies (DB, cache) are reachable and healthy.

## 4. Decisions & Revisions
- 2026-10-10: Baseline telemetry and observability standards established for template repository.
