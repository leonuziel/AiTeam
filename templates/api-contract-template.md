# API Contract: [Endpoint / Resource Name]

Scope: Technical Architecture - API Route Contract
Related: docs/tech/api/contracts.md, docs/tech/api/error-handling.md

## 1. Responsibilities & Boundaries
- **Owns:** Route definition, request parameter validation, authorization requirements, and response payload specification for [Endpoint / Resource Name].
- **Does NOT Own:** Underlying database persistence schemas (owned by `docs/tech/data/schemas.md`).

## 2. Invariants (Hard Rules)
- [Route Invariant 1: e.g., Requires Bearer JWT token with 'scope:read'].
- [Route Invariant 2: e.g., Request rate cannot exceed 60 requests per minute per IP].

## 3. Specifications & Interfaces
### HTTP Method & URI
- **Method:** `POST`
- **Path:** `/api/v1/[resource]`
- **Content-Type:** `application/json`

### Request Schema
```json
{
  "property_a": "string (required)",
  "property_b": "number (optional)"
}
```

### Success Response (HTTP 200 / 201)
```json
{
  "success": true,
  "data": {
    "id": "res_123",
    "created_at": "2026-10-10T12:00:00Z"
  }
}
```

## 4. Decisions & Revisions
- YYYY-MM-DD: Initial API route contract established.
