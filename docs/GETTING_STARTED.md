# Getting Started with ADP

This guide will walk you through creating your first ADP-compliant agent manifest and publishing it for discovery.

## Prerequisites

- A domain you control (for agent identifier)
- Web server with HTTPS
- Understanding of your agent's capabilities

## Step 1: Define Your Agent

Start by identifying:

1. **Agent Name** - Short, descriptive name (lowercase, hyphens allowed)
2. **Version** - Semantic version (e.g., 1.0.0)
3. **Capabilities** - What actions your agent can perform
4. **Protocols** - How consumers will invoke your agent (REST, MCP, etc.)

## Step 2: Create the Manifest

Create a JSON file with the minimum required fields:

```json
{
  "aid": "aid://yourdomain.com/agent-name@1.0.0",
  "name": "Your Agent Name",
  "description": "Brief description of what your agent does",
  "owner": {
    "org": "Your Organization",
    "site": "https://yourdomain.com",
    "contact": "support@yourdomain.com"
  },
  "capabilities": [
    {
      "id": "action.perform",
      "description": "Description of this capability (minimum 10 characters)"
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
    "dataRegions": ["US"],
    "dataSharing": "none",
    "privacyPolicy": "https://yourdomain.com/privacy"
  },
  "security": {
    "signingKeys": {
      "current": "ed25519:YOUR_PUBLIC_KEY_HERE"
    }
  },
  "updatedAt": "2025-11-07T00:00:00Z"
}
```

## Step 3: Validate Your Manifest

Use the ADP validator to ensure your manifest is correct:

```bash
python tools/validate.py your-manifest.json
```

The validator checks:
- JSON syntax
- Required fields
- Field formats and patterns
- Schema compliance

## Step 4: Generate Signing Keys

Generate an Ed25519 key pair for signing your manifest:

```bash
# Using OpenSSL
openssl genpkey -algorithm Ed25519 -out private.pem
openssl pkey -in private.pem -pubout -out public.pem
```

Extract the public key and add it to your manifest:

```json
"security": {
  "signingKeys": {
    "current": "ed25519:BASE64_ENCODED_PUBLIC_KEY"
  }
}
```

## Step 5: Publish Your Manifest

### Option A: Well-Known URI (Recommended)

Publish your manifest at:

```
https://yourdomain.com/.well-known/agents/agent-name-1.0.0.json
```

**Example Directory Structure:**
```
yourdomain.com/
  .well-known/
    agents/
      agent-name-1.0.0.json
```

**Web Server Configuration (nginx):**
```nginx
location /.well-known/agents/ {
    add_header Content-Type application/json;
    add_header Access-Control-Allow-Origin *;
}
```

### Option B: DNS TXT Record (Optional)

Add a DNS TXT record for additional verification:

```
_adp.yourdomain.com IN TXT "adp=v2;key=sha256:HASH_OF_PUBLIC_KEY"
```

## Step 6: Register with Registries (Optional)

Register your agent with ADP-compatible registries:

```bash
curl -X POST https://registry.adp.dev/api/v1/agents \
  -H "Content-Type: application/json" \
  -d @your-manifest.json
```

## Step 7: Test Discovery

Verify your agent can be discovered:

### Direct Discovery
```bash
curl https://yourdomain.com/.well-known/agents/agent-name-1.0.0.json
```

### Registry Search
```bash
curl -X POST https://registry.adp.dev/api/v1/agents/search \
  -H "Content-Type: application/json" \
  -d '{"query": "your agent name"}'
```

## Step 8: Implement Health Check

Ensure your health check endpoint returns proper status:

```json
GET /health

Response 200 OK:
{
  "status": "healthy",
  "timestamp": "2025-11-07T12:00:00Z",
  "version": "1.0.0"
}
```

## Next Steps

- **Add capabilities** - Define input/output schemas for your capabilities
- **Implement authentication** - Set up API keys or OAuth2
- **Monitor health** - Track uptime and performance
- **Version management** - Plan for updates and deprecations
- **Upgrade compliance** - Work toward Silver or Gold certification

## Common Issues

### Manifest Validation Fails

**Problem:** JSON Schema validation errors

**Solution:** Check required fields, field formats, and patterns

### Agent Not Discoverable

**Problem:** Well-known URI returns 404

**Solution:** Verify file path and web server configuration

### Health Check Fails

**Problem:** Health endpoint unreachable

**Solution:** Check endpoint URL, SSL certificate, and server status

## Resources

- **JSON Schema:** `schemas/manifest-v2.0.json`
- **Examples:** `examples/`
- **Validation Tool:** `tools/validate.py`
- **Full Specification:** `spec/ADP-SPECIFICATION.md`

## Support

- GitHub Issues: https://github.com/metisos/adp-protocol/issues
- Email: cjohnson@metisos.com
- Organization: Metis Analytics
