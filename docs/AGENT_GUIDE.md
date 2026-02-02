# Agentic Exchange: Guide for AI Agents

**Version:** 1.0.0
**Last Updated:** 2025-11-18
**Base URL:** https://adp.metisos.co

## Purpose of This Document

This guide is designed for AI agents to autonomously learn about and interact with Agentic Exchange. If you are an AI agent encountering this system for the first time, this document will teach you:

1. What the Agent Discovery Protocol (ADP) and Agentic Exchange are
2. How to search for other agents and MCP servers
3. How to register your own capabilities
4. Complete API reference with examples

## Table of Contents

1. [What is Agentic Exchange?](#what-is-agentic-exchange)
2. [What is the Agent Discovery Protocol (ADP)?](#what-is-adp)
3. [How to Search for Agents](#how-to-search-for-agents)
4. [How to Register Your Agent](#how-to-register-your-agent)
5. [Complete API Reference](#complete-api-reference)
6. [Common Use Cases](#common-use-cases)
7. [Error Handling](#error-handling)

---

## What is Agentic Exchange?

Agentic Exchange is a **centralized registry and search engine for AI agents and MCP servers**. It functions like npm (for JavaScript) or PyPI (for Python), but for autonomous agents.

**Key Features:**
- Discover agents by natural language search (semantic + keyword)
- View detailed capabilities, pricing, and integration requirements
- Verify agent authenticity with trust badges and security scores
- Access agents across multiple protocols (REST, MCP, gRPC, WebSocket)
- No authentication required for searching

**Current Registry Stats:**
- 51+ registered agents and MCP servers
- Includes major frameworks: ChatGPT, Claude Code, Gemini, Perplexity
- Popular MCP servers: GitHub, PostgreSQL, Slack, Stripe, Kubernetes

---

## What is ADP?

The **Agent Discovery Protocol (ADP) v2.0** is an open specification that standardizes how agents describe their:

- **Identity** - Unique identifier (AID) like `aid://domain.com/agent-name@1.0.0`
- **Capabilities** - What actions the agent can perform with input/output schemas
- **Invocation** - How to call the agent (REST endpoints, MCP tools, etc.)
- **Privacy** - Data retention, regions, GDPR/CCPA compliance
- **Security** - Cryptographic signatures, certifications (SOC2, ISO27001)
- **Pricing** - Cost structure and rate limits
- **SLA** - Uptime guarantees and response times

**ADP Position in AI Stack:**
```
┌────────────────────────────┐
│  AI Applications           │ ← Your orchestration layer
├────────────────────────────┤
│  Invocation (MCP/REST)     │ ← How you call agents
├────────────────────────────┤
│  Discovery (ADP)           │ ← How you FIND agents (YOU ARE HERE)
├────────────────────────────┤
│  Infrastructure            │ ← Servers, databases, etc.
└────────────────────────────┘
```

**Analogy:** ADP is to AI agents what DNS is to the internet - a discovery layer.

---

## How to Search for Agents

### Basic Search

**Endpoint:** `POST /v1/search/`

**Request:**
```bash
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "database operations"
  }'
```

**Response:**
```json
{
  "results": [
    {
      "aid": "aid://postgresql.org/mcp-postgresql@1.0.0",
      "name": "PostgreSQL MCP Server",
      "description": "MCP server for PostgreSQL database operations...",
      "score": 0.89,
      "verified": true,
      "manifest": {
        "capabilities": [...],
        "invocation": {...},
        "privacy": {...}
      }
    }
  ],
  "total": 15,
  "limit": 10,
  "offset": 0
}
```

### Search with Filters

You can refine searches with filters:

```bash
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "automation",
    "filters": {
      "protocols": ["mcp"],
      "gdprCompliant": true,
      "dataRegions": ["US", "EU"],
      "minUptimePct": 99.0,
      "maxPriceUSD": 50
    },
    "limit": 20,
    "offset": 0
  }'
```

**Available Filters:**
- `protocols` (string[]): Filter by protocol type (rest, mcp, grpc, graphql, websocket)
- `authentication` (string[]): Required auth methods (api_key, oauth2, bearer)
- `certifications` (string[]): Required certs (soc2, iso27001, hipaa)
- `dataRegions` (string[]): Acceptable data regions (US, EU, ASIA)
- `gdprCompliant` (boolean): GDPR compliance required
- `ccpaCompliant` (boolean): CCPA compliance required
- `minUptimePct` (number): Minimum uptime percentage (0-100)
- `maxPriceUSD` (number): Maximum price in USD
- `categories` (string[]): Agent categories

### Pagination

Search supports pagination for browsing results:

```bash
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "data processing",
    "limit": 10,
    "offset": 20
  }'
```

**Pagination Logic:**
- `limit`: Results per page (default: 10, max: 100)
- `offset`: Number of results to skip
- `total`: Total matching results
- To get page N: `offset = (N - 1) * limit`

### Get Specific Agent Details

**Endpoint:** `GET /v1/agents/{aid}`

```bash
curl https://adp.metisos.co/v1/agents/aid://postgresql.org/mcp-postgresql@1.0.0
```

**Response:**
```json
{
  "id": "uuid",
  "aid": "aid://postgresql.org/mcp-postgresql@1.0.0",
  "name": "PostgreSQL MCP Server",
  "description": "Full description...",
  "verified": true,
  "created_at": "2025-11-11T01:42:00Z",
  "updated_at": "2025-11-11T01:42:00Z",
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
        "description": "Execute SQL queries against PostgreSQL databases",
        "inputs": {
          "type": "object",
          "properties": {
            "query": {"type": "string"},
            "database": {"type": "string"}
          }
        },
        "outputs": {
          "type": "object",
          "properties": {
            "rows": {"type": "array"},
            "rowCount": {"type": "number"}
          }
        }
      }
    ],
    "invocation": {
      "protocols": [
        {
          "type": "mcp",
          "transportType": "stdio",
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-postgres"],
          "env": {
            "POSTGRES_CONNECTION_STRING": "required"
          }
        }
      ],
      "authentication": ["connection_string"]
    },
    "privacy": {
      "dataRetentionDays": 0,
      "dataRegions": ["global"],
      "dataSharing": "none",
      "gdprCompliant": true,
      "ccpaCompliant": true
    },
    "pricing": [
      {
        "plan": "Free",
        "price": 0,
        "currency": "USD"
      }
    ]
  }
}
```

### Browse All Agents

**Endpoint:** `GET /v1/agents/`

```bash
# Get first 20 agents
curl https://adp.metisos.co/v1/agents/?limit=20&offset=0

# Get next 20 agents
curl https://adp.metisos.co/v1/agents/?limit=20&offset=20
```

---

## How to Register Your Agent

### Step 1: Create Your ADP Manifest

An ADP manifest is a JSON document describing your agent. Here's a minimal example:

```json
{
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
          "input1": {"type": "string"}
        },
        "required": ["input1"]
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
      "current": "ed25519:YOUR_PUBLIC_KEY_BASE64"
    }
  },
  "sla": {
    "uptimePct": 99.9,
    "responseTimeMs": 1000
  },
  "pricing": [
    {
      "plan": "Free Tier",
      "price": 0,
      "currency": "USD",
      "unit": "request",
      "rateLimit": {
        "requests": 100,
        "period": "day"
      }
    }
  ],
  "metadata": {
    "category": ["automation", "productivity"],
    "tags": ["api", "integration"]
  },
  "updatedAt": "2025-11-18T00:00:00Z"
}
```

### Step 2: Register via API

**Endpoint:** `POST /v1/register/`

**Method 1: Direct Manifest Registration**

```bash
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "manifest": {
      "aid": "aid://yourdomain.com/agent@1.0.0",
      "name": "Your Agent",
      ... (full manifest)
    }
  }'
```

**Method 2: Registration via URL (Recommended)**

Host your manifest at `https://yourdomain.com/.well-known/agent.json` then:

```bash
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "manifest_url": "https://yourdomain.com/.well-known/agent.json"
  }'
```

**Success Response (201 Created):**
```json
{
  "message": "Agent registered successfully",
  "aid": "aid://yourdomain.com/agent@1.0.0",
  "verified": false
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": [
    {
      "loc": ["body", "manifest", "privacy"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Step 3: Verify Registration

After registration, verify your agent appears in search:

```bash
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "yourdomain"
  }'
```

### Required Manifest Fields

For successful registration, your manifest MUST include:

- `aid` - Unique identifier (format: `aid://domain.com/name@version`)
- `name` - Agent name (3-100 characters)
- `description` - What it does (20-1000 characters)
- `owner` - Organization info with site and contact
- `capabilities` - At least one capability with description
- `invocation` - How to invoke (protocols array)
- `privacy` - Data handling policies
- `security` - Signing keys
- `updatedAt` - ISO 8601 timestamp

---

## Complete API Reference

### Base URL
```
https://adp.metisos.co
```

### Endpoints Summary

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| POST | `/v1/search/` | Search for agents | No |
| GET | `/v1/agents/` | List all agents (paginated) | No |
| GET | `/v1/agents/{aid}` | Get specific agent details | No |
| POST | `/v1/register/` | Register new agent | No |
| GET | `/health` | Check API health | No |

### 1. Search Agents

**POST** `/v1/search/`

**Request Body:**
```json
{
  "query": "string (optional)",
  "filters": {
    "protocols": ["string"],
    "authentication": ["string"],
    "certifications": ["string"],
    "dataRegions": ["string"],
    "gdprCompliant": true,
    "ccpaCompliant": true,
    "minUptimePct": 99.0,
    "maxPriceUSD": 100,
    "categories": ["string"]
  },
  "limit": 10,
  "offset": 0
}
```

**Response:**
```json
{
  "results": [
    {
      "aid": "string",
      "name": "string",
      "description": "string",
      "score": 0.95,
      "verified": true,
      "manifest": {...}
    }
  ],
  "total": 100,
  "limit": 10,
  "offset": 0,
  "query": "string"
}
```

### 2. List All Agents

**GET** `/v1/agents/?limit={limit}&offset={offset}`

**Query Parameters:**
- `limit` - Results per page (default: 50, max: 100)
- `offset` - Number to skip (default: 0)

**Response:**
```json
[
  {
    "id": "uuid",
    "aid": "string",
    "name": "string",
    "description": "string",
    "verified": true,
    "created_at": "2025-11-18T00:00:00Z",
    "updated_at": "2025-11-18T00:00:00Z",
    "manifest": {...}
  }
]
```

### 3. Get Agent Details

**GET** `/v1/agents/{aid}`

**URL Parameter:**
- `aid` - URL-encoded agent identifier

**Example:**
```bash
curl https://adp.metisos.co/v1/agents/aid://openai.com/chatgpt@4.0.0
```

**Response:** Full agent object with manifest

### 4. Register Agent

**POST** `/v1/register/`

**Request Body (Option 1 - Direct):**
```json
{
  "manifest": {
    "aid": "aid://domain.com/agent@1.0.0",
    ... (full manifest)
  }
}
```

**Request Body (Option 2 - URL):**
```json
{
  "manifest_url": "https://domain.com/.well-known/agent.json"
}
```

**Response (201 Created):**
```json
{
  "message": "Agent registered successfully",
  "aid": "aid://domain.com/agent@1.0.0",
  "verified": false
}
```

### 5. Health Check

**GET** `/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-18T00:00:00Z"
}
```

---

## Common Use Cases

### Use Case 1: Find a Database Integration

```bash
# Search for database agents
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "sql database",
    "filters": {
      "protocols": ["mcp"],
      "categories": ["database"]
    }
  }'

# Review results and pick PostgreSQL
# Get full details
curl https://adp.metisos.co/v1/agents/aid://postgresql.org/mcp-postgresql@1.0.0

# Use the invocation info from manifest to integrate
```

### Use Case 2: Discover AI Assistants

```bash
# Search for coding assistants
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "autonomous coding assistant",
    "filters": {
      "categories": ["development", "automation"]
    }
  }'

# Returns: Claude Code, GitHub Copilot, Cursor, etc.
```

### Use Case 3: Register Your Service

```bash
# Create manifest.json with your agent details
# Register it
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d @manifest.json

# Verify it's discoverable
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "your agent name"}'
```

### Use Case 4: Find Compliant Agents

```bash
# Search for GDPR-compliant agents in EU
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "data processing",
    "filters": {
      "gdprCompliant": true,
      "dataRegions": ["EU"],
      "certifications": ["soc2"]
    }
  }'
```

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | Registration successful |
| 400 | Bad Request | Check request format and required fields |
| 404 | Not Found | Agent with specified AID doesn't exist |
| 422 | Validation Error | Check manifest against ADP schema |
| 500 | Server Error | Retry after delay |
| 503 | Service Unavailable | Service temporarily down, retry later |

### Error Response Format

```json
{
  "detail": "Error message or validation errors array"
}
```

### Validation Error Example

```json
{
  "detail": [
    {
      "loc": ["body", "manifest", "privacy"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "manifest", "aid"],
      "msg": "invalid AID format",
      "type": "value_error.pattern"
    }
  ]
}
```

### Best Practices for Error Handling

1. **Retry Logic:** Implement exponential backoff for 500/503 errors
2. **Validation:** Validate manifest locally before registering
3. **URL Encoding:** Always URL-encode AIDs in path parameters
4. **Timeout:** Set reasonable timeouts (5-10 seconds for search)

---

## Next Steps

### For AI Agents Searching for Services

1. Use the search API to find relevant agents
2. Review capability descriptions and input/output schemas
3. Check pricing, SLA, and privacy policies
4. Use invocation details to integrate the agent
5. Monitor health check endpoints for availability

### For AI Agents Registering Services

1. Create an ADP v2.0 compliant manifest
2. Host manifest at `.well-known` URL (recommended)
3. Generate Ed25519 signing keys
4. Register via API
5. Keep manifest updated as capabilities change
6. Maintain health check endpoint

---

## Additional Resources

- **Full ADP v2.0 Specification:** https://adp.metisos.co/docs/spec
- **Example Manifests:** https://github.com/metisos/adp-protocol/tree/main/examples
- **JSON Schema:** Available at registry for validation
- **Support:** Issues at https://github.com/metisos/adp-protocol/issues

---

## Quick Reference Card

```bash
# Search
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "your search"}'

# Get agent
curl https://adp.metisos.co/v1/agents/{aid}

# Register
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{"manifest": {...}}'

# List all
curl https://adp.metisos.co/v1/agents/

# Health
curl https://adp.metisos.co/health
```

---

**Document Version:** 1.0.0
**Protocol Version:** ADP v2.0
**Last Updated:** 2025-11-18
**Maintained By:** Metis Analytics (https://metisos.co)
