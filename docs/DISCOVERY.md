# Agent Discovery Methods

This guide explains how to discover agents using the Agent Discovery Protocol.

## Overview

ADP supports three discovery methods:

1. **Direct Discovery** - Fetch manifest from agent's domain
2. **Registry-Based Discovery** - Search via ADP registries
3. **Federated Discovery** - Query across multiple registries

## Method 1: Direct Discovery

Fetch an agent manifest directly from its domain without using a registry.

### Well-Known URI

Agents publish manifests at a standardized location:

```
https://{domain}/.well-known/agents/{agent-name}-{version}.json
```

**Example:**
```bash
curl https://metisos.co/.well-known/agents/notify-2.0.0.json
```

**Response:**
```json
{
  "aid": "aid://metisos.co/notify@2.0.0",
  "name": "Notify",
  "capabilities": [...],
  ...
}
```

### DNS Verification

Optionally verify domain ownership via DNS TXT record:

```bash
dig TXT _adp.metisos.co
```

**Expected Response:**
```
_adp.metisos.co. 3600 IN TXT "adp=v2;key=sha256:abc123..."
```

### Direct Discovery Flow

```
1. Consumer knows AID: aid://domain.com/agent@1.0.0
2. Extract domain from AID
3. Construct URL: https://domain.com/.well-known/agents/agent-1.0.0.json
4. Fetch manifest via HTTPS GET
5. Validate JSON schema
6. Verify signature (optional)
7. Use manifest to invoke agent
```

### Code Example

```python
import httpx
import json

async def discover_agent_direct(aid: str):
    # Parse AID
    parts = aid.split("://")[1].split("/")
    domain = parts[0]
    agent_version = parts[1]  # agent@version
    agent_name, version = agent_version.split("@")

    # Construct manifest URL
    url = f"https://{domain}/.well-known/agents/{agent_name}-{version}.json"

    # Fetch manifest
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        manifest = response.json()

    return manifest

# Usage
manifest = await discover_agent_direct("aid://metisos.co/notify@2.0.0")
```

## Method 2: Registry-Based Discovery

Search for agents using an ADP registry.

### Search by Query

**Request:**
```bash
curl -X POST https://registry.adp.dev/api/v1/agents/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "email notifications",
    "limit": 10
  }'
```

**Response:**
```json
{
  "results": [
    {
      "aid": "aid://metisos.co/notify@2.0.0",
      "name": "Notify",
      "description": "Multi-channel notification service...",
      "score": 0.95,
      "manifest": {...}
    }
  ],
  "total": 15,
  "offset": 0,
  "limit": 10
}
```

### Search with Filters

**Request:**
```bash
curl -X POST https://registry.adp.dev/api/v1/agents/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "payment processing",
    "filters": {
      "protocols": ["rest", "mcp"],
      "certifications": ["soc2", "pci-dss"],
      "dataRegions": ["US", "EU"],
      "minUptimePct": 99.0,
      "maxPriceUSD": 100
    },
    "sort": "relevance",
    "limit": 20
  }'
```

### Available Filters

| Filter | Type | Description |
|--------|------|-------------|
| `protocols` | array | Protocol types (rest, mcp, grpc) |
| `certifications` | array | Required certifications |
| `dataRegions` | array | Acceptable data regions |
| `minUptimePct` | number | Minimum uptime percentage |
| `maxPriceUSD` | number | Maximum price in USD |
| `categories` | array | Agent categories |
| `gdprCompliant` | boolean | GDPR compliance required |

### Get Agent by AID

**Request:**
```bash
curl https://registry.adp.dev/api/v1/agents/aid://metisos.co/notify@2.0.0
```

**Response:**
```json
{
  "manifest": {...},
  "registeredAt": "2025-01-15T10:00:00Z",
  "lastVerified": "2025-11-07T14:00:00Z",
  "qualitySignals": {
    "uptimePct": 99.95,
    "avgResponseTimeMs": 280,
    "totalInvocations": 1500000
  }
}
```

### Code Example

```python
import httpx

async def search_agents(query: str, filters: dict = None):
    url = "https://registry.adp.dev/api/v1/agents/search"

    payload = {"query": query}
    if filters:
        payload["filters"] = filters

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

# Usage
results = await search_agents(
    query="email",
    filters={"protocols": ["mcp"], "certifications": ["soc2"]}
)

for agent in results["results"]:
    print(f"{agent['name']}: {agent['aid']}")
```

## Method 3: Federated Discovery

Query multiple registries simultaneously for broader coverage.

### Federated Search Flow

```
1. Consumer queries Registry A
2. Registry A searches local database
3. Registry A forwards query to Registry B, C, D
4. Registries return results to Registry A
5. Registry A aggregates and ranks results
6. Consumer receives combined results
```

### Federated Query

**Request to Primary Registry:**
```bash
curl -X POST https://registry-a.adp.dev/api/v1/agents/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "data analysis",
    "federate": true,
    "maxDepth": 2,
    "timeout": 5000
  }'
```

**Response with Federated Results:**
```json
{
  "results": [
    {
      "aid": "aid://example-a.com/agent@1.0.0",
      "name": "Agent A",
      "registry": "https://registry-a.adp.dev",
      "score": 0.95
    },
    {
      "aid": "aid://example-b.com/agent@1.0.0",
      "name": "Agent B",
      "registry": "https://registry-b.adp.dev",
      "score": 0.92
    }
  ],
  "sources": {
    "https://registry-a.adp.dev": 15,
    "https://registry-b.adp.dev": 8,
    "https://registry-c.adp.dev": 12
  },
  "total": 35
}
```

## Discovery Best Practices

### 1. Cache Results

Cache manifest lookups to reduce latency:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_manifest_cached(aid: str):
    return fetch_manifest(aid)
```

### 2. Verify Signatures

Always verify manifest signatures:

```python
def verify_manifest_signature(manifest: dict, signature: str) -> bool:
    public_key = manifest["security"]["signingKeys"]["current"]
    # Verify Ed25519 signature
    return verify_ed25519(manifest, signature, public_key)
```

### 3. Check Health Before Invoking

Verify agent is healthy before invocation:

```python
async def check_agent_health(manifest: dict) -> bool:
    for protocol in manifest["invocation"]["protocols"]:
        if protocol.get("healthCheck"):
            try:
                response = await httpx.get(protocol["healthCheck"])
                return response.status_code == 200
            except:
                continue
    return False
```

### 4. Handle Multiple Protocols

Choose optimal protocol based on requirements:

```python
def select_protocol(manifest: dict, preferred: list) -> dict:
    for protocol_type in preferred:
        for protocol in manifest["invocation"]["protocols"]:
            if protocol["type"] == protocol_type:
                return protocol
    return manifest["invocation"]["protocols"][0]

# Usage
protocol = select_protocol(manifest, preferred=["mcp", "grpc", "rest"])
```

### 5. Monitor Quality Signals

Track agent performance over time:

```python
def should_use_agent(manifest: dict, quality_signals: dict) -> bool:
    if quality_signals.get("uptimePct", 0) < 99.0:
        return False
    if quality_signals.get("avgResponseTimeMs", 9999) > 1000:
        return False
    return True
```

## Discovery Patterns

### Pattern 1: Direct Lookup

Use when you know the exact AID:

```python
aid = "aid://metisos.co/notify@2.0.0"
manifest = await discover_agent_direct(aid)
```

### Pattern 2: Capability Search

Search by specific capability:

```python
results = await search_agents(
    query="email.send",
    filters={"capabilities": ["email.send"]}
)
```

### Pattern 3: Multi-Registry Failover

Try multiple registries for reliability:

```python
registries = [
    "https://registry-a.adp.dev",
    "https://registry-b.adp.dev",
    "https://registry-c.adp.dev"
]

for registry in registries:
    try:
        results = await search_registry(registry, query)
        if results:
            return results
    except:
        continue
```

### Pattern 4: Hybrid Discovery

Combine registry search with direct verification:

```python
# Search via registry
results = await search_agents(query="payment")

# Verify via direct discovery
for agent in results["results"]:
    try:
        direct_manifest = await discover_agent_direct(agent["aid"])
        if verify_signature(direct_manifest):
            # Use direct manifest (most authoritative)
            use_manifest(direct_manifest)
    except:
        # Fallback to registry manifest
        use_manifest(agent["manifest"])
```

## Troubleshooting

### Agent Not Found

**Problem:** 404 when fetching manifest

**Solutions:**
1. Check AID format is correct
2. Verify domain is accessible
3. Ensure manifest is published at correct path
4. Try registry search instead

### Invalid Manifest

**Problem:** JSON schema validation fails

**Solutions:**
1. Validate manifest against schema
2. Check required fields are present
3. Verify field formats (AIDs, dates, etc.)
4. Report to agent owner

### Signature Verification Fails

**Problem:** Cryptographic signature doesn't match

**Solutions:**
1. Check public key matches manifest
2. Verify manifest hasn't been modified
3. Check signature format
4. Contact agent owner

## Resources

- **Discovery Tools:** `tools/`
- **Code Examples:** `examples/`
- **Specification:** `spec/ADP-SPECIFICATION.md`
- **Contact:** cjohnson@metisos.com
