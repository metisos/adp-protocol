# Agentic Exchange API Reference

**Version:** 1.0.0
**Base URL:** `https://adp.metisos.co`
**Protocol:** ADP v2.0

## Overview

The Agentic Exchange API provides programmatic access to search and register AI agents and MCP servers. All endpoints return JSON and require no authentication for read operations.

## Quick Start

```bash
# Search for agents
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "database"}'

# Get specific agent
curl https://adp.metisos.co/v1/agents/aid://postgresql.org/mcp-postgresql@1.0.0

# Register new agent
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{"manifest": {...}}'
```

---

## Endpoints

### 1. Search Agents

Search for agents using natural language queries and filters.

**Endpoint:** `POST /v1/search/`

**Request:**
```json
{
  "query": "database operations",
  "filters": {
    "protocols": ["mcp", "rest"],
    "authentication": ["api_key"],
    "certifications": ["soc2"],
    "dataRegions": ["US", "EU"],
    "gdprCompliant": true,
    "ccpaCompliant": false,
    "minUptimePct": 99.0,
    "maxPriceUSD": 100,
    "categories": ["database", "integration"]
  },
  "limit": 10,
  "offset": 0
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | No | Natural language search query |
| filters | object | No | Structured filters (see below) |
| limit | integer | No | Results per page (default: 10, max: 100) |
| offset | integer | No | Number of results to skip (default: 0) |

**Filter Options:**

| Filter | Type | Description |
|--------|------|-------------|
| protocols | string[] | Protocol types: rest, mcp, grpc, graphql, websocket |
| authentication | string[] | Auth methods: api_key, oauth2, bearer, none |
| certifications | string[] | Certifications: soc2, iso27001, hipaa, pci_dss |
| dataRegions | string[] | Data regions: US, EU, ASIA, global |
| gdprCompliant | boolean | Requires GDPR compliance |
| ccpaCompliant | boolean | Requires CCPA compliance |
| minUptimePct | number | Minimum uptime percentage (0-100) |
| maxPriceUSD | number | Maximum price in USD |
| categories | string[] | Categories: database, automation, communication, etc. |

**Response (200 OK):**
```json
{
  "results": [
    {
      "aid": "aid://postgresql.org/mcp-postgresql@1.0.0",
      "name": "PostgreSQL MCP Server",
      "description": "MCP server for PostgreSQL database operations",
      "score": 0.89,
      "verified": true,
      "manifest": {
        "aid": "aid://postgresql.org/mcp-postgresql@1.0.0",
        "name": "PostgreSQL MCP Server",
        "owner": {
          "org": "PostgreSQL Community",
          "site": "https://www.postgresql.org",
          "contact": "community@postgresql.org"
        },
        "capabilities": [
          {
            "id": "postgresql.query",
            "description": "Execute SQL queries",
            "inputs": {...},
            "outputs": {...}
          }
        ],
        "invocation": {
          "protocols": [
            {
              "type": "mcp",
              "transportType": "stdio",
              "command": "npx",
              "args": ["-y", "@modelcontextprotocol/server-postgres"]
            }
          ],
          "authentication": ["connection_string"]
        },
        "privacy": {
          "dataRetentionDays": 0,
          "dataRegions": ["global"],
          "dataSharing": "none",
          "gdprCompliant": true
        },
        "pricing": [...],
        "metadata": {...}
      }
    }
  ],
  "total": 15,
  "limit": 10,
  "offset": 0,
  "query": "database operations"
}
```

**Example Requests:**

```bash
# Simple text search
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "email notifications"}'

# Search with filters
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "automation tools",
    "filters": {
      "protocols": ["mcp"],
      "gdprCompliant": true
    }
  }'

# Browse with pagination (page 2)
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "limit": 10,
    "offset": 10
  }'
```

---

### 2. List All Agents

Retrieve all registered agents with pagination.

**Endpoint:** `GET /v1/agents/`

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| limit | integer | No | 50 | Results per page (max: 100) |
| offset | integer | No | 0 | Number of results to skip |

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "aid": "aid://postgresql.org/mcp-postgresql@1.0.0",
    "name": "PostgreSQL MCP Server",
    "description": "MCP server for PostgreSQL database operations",
    "verified": true,
    "created_at": "2025-11-11T01:42:00.000Z",
    "updated_at": "2025-11-11T01:42:00.000Z",
    "manifest": {...}
  }
]
```

**Examples:**

```bash
# Get first 20 agents
curl https://adp.metisos.co/v1/agents/?limit=20

# Get next 20 agents (page 2)
curl https://adp.metisos.co/v1/agents/?limit=20&offset=20

# Get all agents (max 100 at a time)
curl https://adp.metisos.co/v1/agents/?limit=100
```

---

### 3. Get Agent Details

Retrieve detailed information about a specific agent by its AID.

**Endpoint:** `GET /v1/agents/{aid}`

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| aid | string | Yes | URL-encoded Agent ID |

**Response (200 OK):**
```json
{
  "id": "uuid",
  "aid": "aid://postgresql.org/mcp-postgresql@1.0.0",
  "name": "PostgreSQL MCP Server",
  "description": "Full description of the agent...",
  "verified": true,
  "created_at": "2025-11-11T01:42:00.000Z",
  "updated_at": "2025-11-11T01:42:00.000Z",
  "manifest": {
    "aid": "aid://postgresql.org/mcp-postgresql@1.0.0",
    "name": "PostgreSQL MCP Server",
    "owner": {...},
    "capabilities": [...],
    "invocation": {...},
    "privacy": {...},
    "security": {...},
    "sla": {...},
    "pricing": [...],
    "metadata": {...},
    "updatedAt": "2025-11-11T01:42:00Z"
  }
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Agent with AID 'aid://example.com/nonexistent@1.0.0' not found"
}
```

**Examples:**

```bash
# Get PostgreSQL MCP server
curl https://adp.metisos.co/v1/agents/aid://postgresql.org/mcp-postgresql@1.0.0

# Get ChatGPT agent
curl https://adp.metisos.co/v1/agents/aid://openai.com/chatgpt@4.0.0

# Get Claude Code agent
curl https://adp.metisos.co/v1/agents/aid://anthropic.com/claude-code@1.0.0

# Note: AIDs with special characters should be URL-encoded
# Example with URL encoding:
curl https://adp.metisos.co/v1/agents/aid%3A%2F%2Fexample.com%2Fagent%401.0.0
```

---

### 4. Register Agent

Register a new agent or update an existing one.

**Endpoint:** `POST /v1/register/`

**Method 1: Direct Manifest Registration**

Submit the complete manifest in the request body.

**Request:**
```json
{
  "manifest": {
    "aid": "aid://yourdomain.com/agent-name@1.0.0",
    "name": "Your Agent Name",
    "description": "What your agent does (minimum 20 characters)",
    "owner": {
      "org": "Your Organization",
      "site": "https://yourdomain.com",
      "contact": "contact@yourdomain.com"
    },
    "capabilities": [
      {
        "id": "agent.action",
        "description": "What this capability does",
        "inputs": {
          "type": "object",
          "properties": {
            "param1": {"type": "string"}
          }
        },
        "outputs": {
          "type": "object",
          "properties": {
            "result": {"type": "string"}
          }
        }
      }
    ],
    "invocation": {
      "protocols": [
        {
          "type": "rest",
          "endpoint": "https://api.yourdomain.com/v1",
          "healthCheck": "https://api.yourdomain.com/health"
        }
      ],
      "authentication": ["api_key"]
    },
    "privacy": {
      "dataRetentionDays": 90,
      "dataRegions": ["US", "EU"],
      "dataSharing": "none",
      "gdprCompliant": true,
      "ccpaCompliant": true
    },
    "security": {
      "signingKeys": {
        "current": "ed25519:BASE64_PUBLIC_KEY"
      }
    },
    "sla": {
      "uptimePct": 99.9,
      "responseTimeMs": 1000
    },
    "pricing": [
      {
        "plan": "Free",
        "price": 0,
        "currency": "USD",
        "unit": "request"
      }
    ],
    "metadata": {
      "category": ["automation"],
      "tags": ["api", "integration"]
    },
    "updatedAt": "2025-11-18T00:00:00Z"
  }
}
```

**Method 2: Registration via URL (Recommended)**

Host your manifest at a public URL and provide that URL.

**Request:**
```json
{
  "manifest_url": "https://yourdomain.com/.well-known/agent.json"
}
```

**Recommended URL structure:**
- `https://yourdomain.com/.well-known/agent.json` (single agent)
- `https://yourdomain.com/.well-known/agents/agent-name-1.0.0.json` (multiple versions)

**Response (201 Created):**
```json
{
  "message": "Agent registered successfully",
  "aid": "aid://yourdomain.com/agent-name@1.0.0",
  "verified": false
}
```

**Response (400 Bad Request) - Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "manifest", "privacy"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "manifest", "description"],
      "msg": "ensure this value has at least 20 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {"limit_value": 20}
    }
  ]
}
```

**Response (409 Conflict) - Agent Already Exists:**
```json
{
  "detail": "Agent with AID 'aid://yourdomain.com/agent-name@1.0.0' already exists"
}
```

**Examples:**

```bash
# Register via direct manifest
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d @manifest.json

# Register via URL
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "manifest_url": "https://example.com/.well-known/agent.json"
  }'
```

**Required Manifest Fields:**

| Field | Type | Description |
|-------|------|-------------|
| aid | string | Unique identifier (format: `aid://domain.com/name@version`) |
| name | string | Agent name (3-100 characters) |
| description | string | What it does (20-1000 characters) |
| owner | object | Organization info with site and contact |
| capabilities | array | At least one capability with description |
| invocation | object | How to invoke (protocols array) |
| privacy | object | Data handling policies (required fields below) |
| security | object | Signing keys |
| updatedAt | string | ISO 8601 timestamp |

**Required Privacy Fields:**

| Field | Type | Description |
|-------|------|-------------|
| dataRetentionDays | integer | Data retention period (0 = no retention) |
| dataRegions | string[] | Where data is stored (US, EU, ASIA, global) |
| dataSharing | string | Data sharing policy (none, anonymized, partners, public) |
| gdprCompliant | boolean | GDPR compliance status |
| ccpaCompliant | boolean | CCPA compliance status |

---

### 5. Health Check

Check the API health status.

**Endpoint:** `GET /health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-18T12:00:00.000Z"
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy",
  "timestamp": "2025-11-18T12:00:00.000Z",
  "error": "Database connection failed"
}
```

**Example:**

```bash
curl https://adp.metisos.co/health
```

---

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request format or parameters |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error occurred |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## Error Response Format

All errors return a consistent format:

```json
{
  "detail": "Error message or array of validation errors"
}
```

**Validation Error Example:**
```json
{
  "detail": [
    {
      "loc": ["body", "manifest", "privacy", "dataRetentionDays"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limits

- **No authentication required** for read operations (search, get)
- **No rate limits** currently enforced
- Recommended: Implement client-side caching and reasonable request intervals
- Search limit: 100 results maximum per request

---

## CORS

All endpoints support CORS:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

---

## Pagination

### Search Endpoint

Uses offset-based pagination:

```json
{
  "limit": 10,
  "offset": 0
}
```

**Calculate page:**
- Page 1: `offset = 0`
- Page 2: `offset = 10`
- Page N: `offset = (N - 1) * limit`

**Example:**
```bash
# Get page 3 with 20 results per page
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "automation",
    "limit": 20,
    "offset": 40
  }'
```

### List Endpoint

Uses query parameters:

```
GET /v1/agents/?limit=50&offset=0
```

---

## Data Types

### Agent ID (AID)

Format: `aid://domain.com/agent-name@version`

**Rules:**
- Must start with `aid://`
- Domain must be valid (you should control it)
- Agent name: lowercase, hyphens allowed, no spaces
- Version: Semantic versioning (e.g., 1.0.0)

**Examples:**
- `aid://openai.com/chatgpt@4.0.0`
- `aid://anthropic.com/claude-code@1.0.0`
- `aid://postgresql.org/mcp-postgresql@1.0.0`

### Timestamps

All timestamps use ISO 8601 format:

```
2025-11-18T12:00:00Z
2025-11-18T12:00:00.000Z
```

### Protocols

Supported protocol types:
- `rest` - REST API
- `mcp` - Model Context Protocol
- `grpc` - gRPC
- `graphql` - GraphQL
- `websocket` - WebSocket

---

## Complete Examples

### Example 1: Search and Integrate

```bash
# 1. Search for database agents
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "postgresql database",
    "filters": {"protocols": ["mcp"]}
  }' > search_results.json

# 2. Extract AID from results
# aid://postgresql.org/mcp-postgresql@1.0.0

# 3. Get full details
curl https://adp.metisos.co/v1/agents/aid://postgresql.org/mcp-postgresql@1.0.0 \
  > agent_details.json

# 4. Use invocation.protocols info to integrate
```

### Example 2: Register New Agent

```bash
# 1. Create manifest.json
cat > manifest.json <<EOF
{
  "aid": "aid://example.com/my-agent@1.0.0",
  "name": "My Agent",
  "description": "This is my custom agent that does amazing things",
  "owner": {
    "org": "My Company",
    "site": "https://example.com",
    "contact": "support@example.com"
  },
  "capabilities": [
    {
      "id": "myagent.process",
      "description": "Process data and return results",
      "inputs": {
        "type": "object",
        "properties": {
          "data": {"type": "string"}
        }
      },
      "outputs": {
        "type": "object",
        "properties": {
          "result": {"type": "string"}
        }
      }
    }
  ],
  "invocation": {
    "protocols": [
      {
        "type": "rest",
        "endpoint": "https://api.example.com/v1"
      }
    ],
    "authentication": ["api_key"]
  },
  "privacy": {
    "dataRetentionDays": 30,
    "dataRegions": ["US"],
    "dataSharing": "none",
    "gdprCompliant": true,
    "ccpaCompliant": true
  },
  "security": {
    "signingKeys": {
      "current": "ed25519:abc123..."
    }
  },
  "updatedAt": "2025-11-18T00:00:00Z"
}
EOF

# 2. Register
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d @manifest.json

# 3. Verify registration
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "my-agent"}'
```

### Example 3: Browse All Agents

```bash
# Get total count
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.total'

# Browse in batches of 20
for i in {0..2}; do
  offset=$((i * 20))
  curl https://adp.metisos.co/v1/agents/?limit=20&offset=$offset \
    > agents_page_$((i+1)).json
done
```

---

## SDKs and Tools

### Python Example

```python
import requests

BASE_URL = "https://adp.metisos.co"

def search_agents(query, filters=None):
    response = requests.post(
        f"{BASE_URL}/v1/search/",
        json={"query": query, "filters": filters or {}}
    )
    return response.json()

def get_agent(aid):
    response = requests.get(f"{BASE_URL}/v1/agents/{aid}")
    return response.json()

def register_agent(manifest):
    response = requests.post(
        f"{BASE_URL}/v1/register/",
        json={"manifest": manifest}
    )
    return response.json()

# Usage
results = search_agents("database", {"protocols": ["mcp"]})
agent = get_agent("aid://postgresql.org/mcp-postgresql@1.0.0")
```

### JavaScript Example

```javascript
const BASE_URL = "https://adp.metisos.co";

async function searchAgents(query, filters = {}) {
  const response = await fetch(`${BASE_URL}/v1/search/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, filters })
  });
  return response.json();
}

async function getAgent(aid) {
  const response = await fetch(`${BASE_URL}/v1/agents/${encodeURIComponent(aid)}`);
  return response.json();
}

async function registerAgent(manifest) {
  const response = await fetch(`${BASE_URL}/v1/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ manifest })
  });
  return response.json();
}

// Usage
const results = await searchAgents("database", { protocols: ["mcp"] });
const agent = await getAgent("aid://postgresql.org/mcp-postgresql@1.0.0");
```

---

## Support

- **Documentation:** https://adp.metisos.co/docs
- **GitHub:** https://github.com/metisos/adp-protocol
- **Issues:** https://github.com/metisos/adp-protocol/issues
- **Email:** cjohnson@metisos.com

---

**API Version:** 1.0.0
**Last Updated:** 2025-11-18
**Maintained By:** Metis Analytics
