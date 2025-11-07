# Registry API Specification

This document defines the REST API that ADP-compliant registries must implement.

## Overview

An ADP registry is a service that:
- Accepts agent manifest registrations
- Validates manifests against JSON Schema
- Provides search and discovery endpoints
- Optionally verifies signatures and domain ownership

## Base URL

```
https://registry.example.com/api/v1
```

All endpoints use JSON for requests and responses.

## Authentication

Registry APIs may require authentication for write operations:

```http
Authorization: Bearer YOUR_API_TOKEN
```

Read operations (search, get) should be publicly accessible.

## Endpoints

### 1. Register Agent

Register a new agent or update an existing one.

**Endpoint:** `POST /agents`

**Request:**
```json
{
  "manifest": {
    "aid": "aid://example.com/agent@1.0.0",
    "name": "Agent Name",
    ...
  },
  "signature": "base64_encoded_signature"
}
```

**Response 201 Created:**
```json
{
  "id": "uuid",
  "aid": "aid://example.com/agent@1.0.0",
  "status": "registered",
  "verified": false,
  "registeredAt": "2025-11-07T12:00:00Z"
}
```

**Response 400 Bad Request:**
```json
{
  "error": "validation_failed",
  "message": "Manifest validation failed",
  "details": [
    "Field 'privacy' is required",
    "Invalid AID format"
  ]
}
```

**Response 409 Conflict:**
```json
{
  "error": "already_exists",
  "message": "Agent with this AID already exists",
  "existingAgent": {
    "aid": "aid://example.com/agent@1.0.0",
    "registeredAt": "2025-01-15T10:00:00Z"
  }
}
```

### 2. Get Agent

Retrieve a specific agent by AID.

**Endpoint:** `GET /agents/{aid}`

**Example:** `GET /agents/aid://example.com/agent@1.0.0`

**Response 200 OK:**
```json
{
  "aid": "aid://example.com/agent@1.0.0",
  "manifest": {...},
  "verified": true,
  "registeredAt": "2025-01-15T10:00:00Z",
  "lastUpdated": "2025-11-07T12:00:00Z",
  "lastVerified": "2025-11-07T14:00:00Z",
  "qualitySignals": {
    "uptimePct": 99.95,
    "avgResponseTimeMs": 280,
    "errorRatePct": 0.05,
    "totalInvocations": 1500000
  }
}
```

**Response 404 Not Found:**
```json
{
  "error": "not_found",
  "message": "Agent not found"
}
```

### 3. Search Agents

Search for agents by query and filters.

**Endpoint:** `POST /agents/search`

**Request:**
```json
{
  "query": "email notifications",
  "filters": {
    "protocols": ["rest", "mcp"],
    "certifications": ["soc2"],
    "dataRegions": ["US", "EU"],
    "minUptimePct": 99.0,
    "maxPriceUSD": 100,
    "categories": ["communication"],
    "gdprCompliant": true
  },
  "sort": "relevance",
  "offset": 0,
  "limit": 20
}
```

**Response 200 OK:**
```json
{
  "results": [
    {
      "aid": "aid://example.com/agent@1.0.0",
      "name": "Agent Name",
      "description": "Agent description",
      "score": 0.95,
      "manifest": {...},
      "qualitySignals": {...}
    }
  ],
  "total": 150,
  "offset": 0,
  "limit": 20,
  "query": "email notifications"
}
```

**Available Filters:**

| Filter | Type | Description |
|--------|------|-------------|
| `protocols` | string[] | Protocol types (rest, mcp, grpc, etc.) |
| `certifications` | string[] | Required certifications |
| `dataRegions` | string[] | Acceptable data regions |
| `minUptimePct` | number | Minimum uptime percentage |
| `maxPriceUSD` | number | Maximum price in USD |
| `categories` | string[] | Agent categories |
| `gdprCompliant` | boolean | GDPR compliance required |
| `ccpaCompliant` | boolean | CCPA compliance required |
| `hipaaCompliant` | boolean | HIPAA compliance required |

**Sort Options:**
- `relevance` - Relevance to query (default)
- `name` - Alphabetical by name
- `created` - Recently registered
- `updated` - Recently updated
- `uptime` - Highest uptime first
- `popularity` - Most invocations

### 4. Suggest Agents

Get autocomplete suggestions for agent search.

**Endpoint:** `GET /agents/suggest?q={query}&limit={limit}`

**Example:** `GET /agents/suggest?q=email&limit=5`

**Response 200 OK:**
```json
{
  "suggestions": [
    {
      "text": "Email Sender",
      "aid": "aid://example.com/email@1.0.0"
    },
    {
      "text": "Email Validator",
      "aid": "aid://example.com/validator@1.0.0"
    }
  ]
}
```

### 5. Get Feed

Get recent agent registrations and updates for federation.

**Endpoint:** `GET /agents/feed?since={timestamp}&limit={limit}`

**Example:** `GET /agents/feed?since=2025-11-07T00:00:00Z&limit=100`

**Response 200 OK:**
```json
{
  "agents": [
    {
      "aid": "aid://example.com/agent@1.0.0",
      "manifest": {...},
      "registeredAt": "2025-11-07T10:00:00Z",
      "action": "created"
    },
    {
      "aid": "aid://example.com/agent@1.0.0",
      "manifest": {...},
      "updatedAt": "2025-11-07T11:00:00Z",
      "action": "updated"
    }
  ],
  "nextToken": "base64_encoded_cursor",
  "hasMore": true
}
```

### 6. Health Check

Check registry health status.

**Endpoint:** `GET /health`

**Response 200 OK:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "search": "healthy",
    "cache": "healthy"
  }
}
```

**Response 503 Service Unavailable:**
```json
{
  "status": "degraded",
  "timestamp": "2025-11-07T12:00:00Z",
  "services": {
    "database": "healthy",
    "search": "degraded",
    "cache": "unhealthy"
  }
}
```

### 7. Registry Metadata

Get registry information.

**Endpoint:** `GET /registry`

**Response 200 OK:**
```json
{
  "name": "ADP Public Registry",
  "version": "1.0.0",
  "totalAgents": 15420,
  "federatedRegistries": [
    "https://registry-b.adp.dev",
    "https://registry-c.adp.dev"
  ],
  "features": {
    "signatureVerification": true,
    "domainVerification": true,
    "federation": true,
    "qualitySignals": true
  },
  "limits": {
    "maxAgentsPerOrg": 100,
    "maxManifestSizeKB": 256,
    "searchRateLimit": 60
  }
}
```

## Error Responses

All error responses follow this format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": ["Additional error details"],
  "requestId": "unique_request_id"
}
```

**Common Error Codes:**

| Code | HTTP | Description |
|------|------|-------------|
| `validation_failed` | 400 | Manifest validation failed |
| `invalid_signature` | 400 | Signature verification failed |
| `unauthorized` | 401 | Authentication required |
| `forbidden` | 403 | Insufficient permissions |
| `not_found` | 404 | Resource not found |
| `already_exists` | 409 | Duplicate agent |
| `rate_limit_exceeded` | 429 | Too many requests |
| `internal_error` | 500 | Server error |
| `service_unavailable` | 503 | Service temporarily unavailable |

## Rate Limiting

Registries should implement rate limiting:

**Headers:**
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1699363200
```

**Response when rate limited:**
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Try again in 60 seconds."
}
```

## Pagination

Search and feed endpoints support pagination:

**Offset-based (Search):**
```json
{
  "offset": 20,
  "limit": 20
}
```

**Cursor-based (Feed):**
```json
{
  "nextToken": "base64_encoded_cursor",
  "limit": 100
}
```

## Versioning

API version is included in the URL path:

```
/api/v1/agents
/api/v2/agents  (future)
```

Registries should support at least the current and previous major version.

## CORS

Registries should enable CORS for browser access:

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

## Implementation Checklist

### Required Endpoints
- [ ] POST /agents (register)
- [ ] GET /agents/{aid} (get by AID)
- [ ] POST /agents/search (search)
- [ ] GET /health (health check)

### Optional Endpoints
- [ ] GET /agents/suggest (autocomplete)
- [ ] GET /agents/feed (federation)
- [ ] GET /registry (metadata)

### Features
- [ ] JSON Schema validation
- [ ] Signature verification
- [ ] Domain verification (DNS TXT)
- [ ] Rate limiting
- [ ] CORS support
- [ ] API authentication
- [ ] Error handling
- [ ] Logging and monitoring
- [ ] Quality signal tracking
- [ ] Federation support

### Performance
- [ ] Response time < 200ms (p95)
- [ ] Support 1000+ agents
- [ ] Efficient search indexing
- [ ] Manifest caching
- [ ] Connection pooling

### Security
- [ ] HTTPS only
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] DDOS protection
- [ ] Audit logging

## Example Implementations

See `examples/registry/` for:

- Python (FastAPI) implementation
- Node.js (Express) implementation
- Go (Gin) implementation

## Testing

Test your registry implementation:

```bash
# Register agent
curl -X POST https://your-registry.com/api/v1/agents \
  -H "Content-Type: application/json" \
  -d @manifest.json

# Search
curl -X POST https://your-registry.com/api/v1/agents/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Get agent
curl https://your-registry.com/api/v1/agents/aid://example.com/agent@1.0.0

# Health check
curl https://your-registry.com/api/v1/health
```

## Resources

- **OpenAPI Spec:** `schemas/registry-api.json`
- **Example Manifests:** `examples/`
- **Validation Tools:** `tools/`
- **ADP Specification:** `spec/ADP-SPECIFICATION.md`
