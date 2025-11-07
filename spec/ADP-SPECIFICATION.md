# Agent Discovery Protocol (ADP) v2.0 Specification

**Version:** 2.0.0
**Status:** Production Standard
**Published:** 2025-11-07
**Authors:** Metis Analytics
**License:** CC BY 4.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Core Concepts](#2-core-concepts)
3. [Agent Identifier (AID)](#3-agent-identifier-aid)
4. [Manifest Format](#4-manifest-format)
5. [Discovery Mechanisms](#5-discovery-mechanisms)
6. [Invocation Protocols](#6-invocation-protocols)
7. [Security & Trust](#7-security--trust)
8. [Privacy Requirements](#8-privacy-requirements)
9. [Registry Specification](#9-registry-specification)
10. [Compliance Levels](#10-compliance-levels)

---

## 1. Introduction

### 1.1 Purpose

The Agent Discovery Protocol (ADP) is an open standard that enables AI agents to be discovered, trusted, and invoked across the AI ecosystem. ADP provides the discovery and metadata layer while remaining neutral about invocation mechanisms.

### 1.2 Design Principles

1. **Simplicity First** - Minimal required fields; optional complexity
2. **Security by Default** - Cryptographic signatures required
3. **Privacy Conscious** - Data handling disclosures mandatory
4. **Protocol Neutral** - Support any invocation method
5. **Decentralized** - No single point of control
6. **Extensible** - Room for future capabilities

### 1.3 Positioning in the AI Stack

```
+-------------------------------------+
|  AI Applications & Orchestrators    | <-- Business Logic
+-------------------------------------+
|     Invocation Layer                | <-- MCP, API, gRPC, etc.
+-------------------------------------+
|  Discovery Layer (ADP)              | <-- Agent Discovery & Metadata
+-------------------------------------+
|     Infrastructure Layer            | <-- Kubernetes, Cloud, etc.
+-------------------------------------+
```

ADP is to AI agents what DNS is to the internet: a decentralized discovery mechanism.

---

## 2. Core Concepts

### 2.1 Agents

An **agent** is an autonomous AI service that provides one or more capabilities. Agents can be:

- Language models with tool-calling abilities
- Specialized AI services (image generation, data analysis)
- Workflow orchestrators
- API wrappers with AI enhancements

### 2.2 Capabilities

A **capability** is a specific action or service an agent provides. Each capability has:

- Unique identifier (dot notation)
- Description
- Input/output schemas
- Error definitions
- Rate limits and SLAs

### 2.3 Discovery

**Discovery** is the process of finding agents that match specific criteria:

- Direct discovery via domain lookup
- Registry-based search
- Federated query across multiple registries

### 2.4 Trust

**Trust** is established through multiple layers:

1. Cryptographic signatures (Ed25519)
2. Domain verification (DNS TXT records)
3. Third-party attestations
4. Community reputation

---

## 3. Agent Identifier (AID)

### 3.1 Format

**Syntax:** `aid://{domain}/{agent-name}@{version}`

**Components:**
- `aid://` - Protocol prefix (required)
- `{domain}` - DNS domain (required)
- `{agent-name}` - Agent identifier (required)
- `@{version}` - Semantic version (required)

### 3.2 Examples

```
aid://anthropic.com/claude-analyst@1.0.0
aid://metisos.co/notify@2.0.0
aid://api.example.com/data-processor@1.5.2
```

### 3.3 Naming Rules

**Agent Name Pattern:** `^[a-z0-9]+(-[a-z0-9]+)*$`

**Valid:**
- `atlas`
- `email-sender`
- `data-analyzer`

**Invalid:**
- `Atlas` (uppercase not allowed)
- `email_sender` (underscore not allowed)
- `agent.name` (dot notation reserved for capabilities)

### 3.4 Versioning

Follow Semantic Versioning 2.0.0:

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
1.0.0          - Initial stable release
1.2.0          - New capabilities added
2.0.0          - Breaking changes
2.1.0-beta.1   - Pre-release version
```

**Versioning Rules:**
- **MAJOR:** Breaking changes to capability contracts
- **MINOR:** New capabilities, backward-compatible changes
- **PATCH:** Bug fixes, performance improvements

---

## 4. Manifest Format

### 4.1 Required Fields

```json
{
  "aid": "aid://domain.com/agent@1.0.0",
  "name": "Agent Name",
  "owner": {
    "org": "Organization Name"
  },
  "capabilities": [...],
  "invocation": {...},
  "privacy": {...},
  "security": {...},
  "updatedAt": "2025-11-07T00:00:00Z"
}
```

### 4.2 Owner

```json
"owner": {
  "org": "Organization Name",        // Required
  "site": "https://example.com",     // Optional
  "contact": "support@example.com",  // Optional
  "support": "https://help.example.com" // Optional
}
```

### 4.3 Capabilities

```json
"capabilities": [
  {
    "id": "capability.action",
    "description": "What this capability does (minimum 10 characters)",
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
    },
    "errors": [...],       // Optional
    "rateLimit": {...},    // Optional
    "sla": {...}           // Optional
  }
]
```

### 4.4 Invocation

```json
"invocation": {
  "protocols": [
    {
      "type": "rest",     // rest | mcp | grpc | graphql | websocket
      "endpoint": "https://api.example.com/v1",
      "version": "1.0.0",
      "spec": "https://api.example.com/openapi.json",
      "healthCheck": "https://api.example.com/health"
    }
  ],
  "authentication": ["api_key", "oauth2", "jwt"]
}
```

### 4.5 Privacy

```json
"privacy": {
  "dataRetentionDays": 90,     // 0 = none, -1 = indefinite
  "dataRegions": ["US", "EU"], // ISO 3166-1 alpha-2 codes
  "dataSharing": "none",       // none | anonymized | partners | public
  "privacyPolicy": "https://example.com/privacy",
  "gdprCompliant": true,
  "ccpaCompliant": true,
  "hipaaCompliant": false
}
```

### 4.6 Security

```json
"security": {
  "signingKeys": {
    "current": "ed25519:MCowBQYDK2VwAyEA...",
    "next": "ed25519:...",           // Optional, for rotation
    "rotationDate": "2025-12-01T00:00:00Z" // Optional
  },
  "attestations": [...],             // Optional
  "certifications": ["soc2", "iso27001"], // Optional
  "vulnerabilityDisclosure": "https://example.com/security" // Optional
}
```

### 4.7 Optional Fields

```json
"description": "Detailed description",
"sla": {
  "uptimePct": 99.9,
  "responseTimeMs": 500,
  "errorRatePct": 0.1,
  "supportResponseHours": 24
},
"pricing": [...],
"metadata": {
  "category": ["communication", "automation"],
  "tags": ["email", "notifications"],
  "documentation": "https://docs.example.com",
  "repository": "https://github.com/org/repo",
  "license": "MIT"
}
```

---

## 5. Discovery Mechanisms

### 5.1 Well-Known URI Discovery

Agents MUST publish manifests at:

```
https://{domain}/.well-known/agents/{agent-name}-{version}.json
```

**Example:**
```
https://metisos.co/.well-known/agents/notify-2.0.0.json
```

### 5.2 DNS-Based Discovery

Optional DNS TXT record at `_adp.{domain}`:

```
_adp.metisos.co IN TXT "adp=v2;key=sha256:abc123...;registry=https://registry.adp.dev"
```

### 5.3 Registry-Based Discovery

**Search Request:**
```http
POST /api/v1/agents/search
Content-Type: application/json

{
  "query": "email notifications",
  "filters": {
    "protocols": ["mcp"],
    "certifications": ["soc2"],
    "dataRegions": ["US", "EU"]
  },
  "limit": 20
}
```

**Response:**
```json
{
  "results": [
    {
      "aid": "aid://example.com/agent@1.0.0",
      "name": "Agent Name",
      "manifest": {...},
      "score": 0.95
    }
  ],
  "total": 47
}
```

---

## 6. Invocation Protocols

### 6.1 Supported Protocols

ADP supports any invocation protocol. Common protocols:

- **REST** - RESTful HTTP APIs
- **MCP** - Model Context Protocol
- **gRPC** - Google RPC
- **GraphQL** - Query language
- **WebSocket** - Bidirectional communication

### 6.2 Protocol Specifications

Each protocol entry includes:

```json
{
  "type": "rest",
  "endpoint": "https://api.example.com/v1",
  "version": "1.0.0",
  "spec": "https://api.example.com/openapi.json",
  "healthCheck": "https://api.example.com/health"
}
```

### 6.3 Multi-Protocol Support

Agents MAY support multiple protocols:

```json
"protocols": [
  {"type": "mcp", "endpoint": "https://api.example.com/mcp"},
  {"type": "rest", "endpoint": "https://api.example.com/v1"},
  {"type": "grpc", "endpoint": "grpc://api.example.com:443"}
]
```

---

## 7. Security & Trust

### 7.1 Cryptographic Signatures

**Algorithm:** Ed25519 (RFC 8032)

**Signing Process:**
1. Canonicalize manifest JSON (sorted keys, no whitespace)
2. Sign with Ed25519 private key
3. Publish signature alongside manifest

**Verification:**
1. Extract public key from `security.signingKeys.current`
2. Canonicalize manifest (excluding signature)
3. Verify signature using Ed25519

### 7.2 Key Rotation

**Process:**
1. Announce new key 30+ days in advance
2. Publish in `signingKeys.next` with `rotationDate`
3. On rotation date, move `next` to `current`
4. Keep old key in `previous` array for grace period
5. After grace period, remove from `previous`

### 7.3 Attestations

Third-party attestations provide additional trust signals:

```json
"attestations": [
  {
    "type": "domain_control",
    "value": "example.com",
    "attestor": "Organization Name",
    "signature": "eyJhbGciOiJFZDI1NTE5...",
    "validUntil": "2026-01-01T00:00:00Z"
  }
]
```

**Attestation Types:**
- `domain_control` - Proves domain ownership
- `ssl_cert` - Valid SSL certificate
- `organization` - Legal entity verification
- `third_party_audit` - Security audit

---

## 8. Privacy Requirements

### 8.1 Required Disclosures

All manifests MUST include:

```json
"privacy": {
  "dataRetentionDays": 90,
  "dataRegions": ["US"],
  "dataSharing": "none"
}
```

### 8.2 Data Retention

- `0` - No data retained (ephemeral processing)
- Positive integer - Days retained
- `-1` - Indefinite retention

### 8.3 Data Sharing

- `none` - No data sharing
- `anonymized` - Aggregated analytics only
- `partners` - Shared with named partners
- `public` - Public dataset

### 8.4 Compliance Flags

```json
"gdprCompliant": true,
"ccpaCompliant": true,
"hipaaCompliant": false
```

---

## 9. Registry Specification

### 9.1 Registry Responsibilities

A compliant ADP registry MUST:

1. Accept agent manifests via API
2. Validate manifests against JSON Schema
3. Verify cryptographic signatures
4. Provide search functionality
5. Return manifests on request

### 9.2 Registry API

**Register Agent:**
```http
POST /api/v1/agents
Content-Type: application/json

{
  "manifest": {...}
}
```

**Search Agents:**
```http
POST /api/v1/agents/search
{
  "query": "search terms",
  "filters": {...}
}
```

**Get Agent:**
```http
GET /api/v1/agents/{aid}
```

### 9.3 Quality Signals

Registries SHOULD track:

```json
"qualitySignals": {
  "uptimePct": 99.95,
  "avgResponseTimeMs": 280,
  "errorRatePct": 0.05,
  "totalInvocations": 1500000,
  "userRating": 4.8
}
```

---

## 10. Compliance Levels

### 10.1 Bronze Compliance

**Requirements:**
- Valid manifest with all required fields
- Published at well-known URI
- Passes JSON Schema validation

### 10.2 Silver Compliance

**Requirements:**
- All Bronze requirements
- Valid Ed25519 signing key
- Signed manifest
- Health check endpoint returning 200 OK

### 10.3 Gold Compliance

**Requirements:**
- All Silver requirements
- At least one verified attestation
- Privacy policy published and accessible
- 99%+ uptime over 30 days
- SLA commitments defined

---

## Appendix A: JSON Schema

See `schemas/manifest-v2.0.json` for the complete JSON Schema.

## Appendix B: Error Codes

Standard error codes for agent invocation:

| Code | HTTP | Description | Retryable |
|------|------|-------------|-----------|
| `invalid_capability` | 400 | Capability not found | No |
| `invalid_input` | 400 | Input validation failed | No |
| `authentication_required` | 401 | Missing/invalid auth | No |
| `rate_limit_exceeded` | 429 | Too many requests | Yes |
| `internal_error` | 500 | Server error | Yes |
| `service_unavailable` | 503 | Temporarily unavailable | Yes |

## Appendix C: Changelog

**v2.0.0 (2025-11-07)**
- Added required `privacy` field
- Enhanced security with key rotation
- Merged invocation protocols
- Added compliance levels

**v1.0.0 (2025-01-01)**
- Initial specification release

---

**Agent Discovery Protocol v2.0 Specification**
Copyright 2025 ADP Standards Working Group
Licensed under CC BY 4.0
