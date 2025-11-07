# Security Guide

This guide covers security considerations for implementing and using the Agent Discovery Protocol.

## Overview

ADP security is built on three pillars:

1. **Cryptographic Signatures** - Ed25519 for manifest signing
2. **Domain Verification** - DNS-based ownership proof
3. **Attestations** - Third-party trust signals

## Cryptographic Signatures

### Key Generation

Generate an Ed25519 key pair:

**Using OpenSSL:**
```bash
# Generate private key
openssl genpkey -algorithm Ed25519 -out private.pem

# Extract public key
openssl pkey -in private.pem -pubout -out public.pem

# Convert to base64 for manifest
cat public.pem | grep -v "BEGIN\|END" | tr -d '\n' | base64 -w 0
```

**Using Python:**
```python
from cryptography.hazmat.primitives.asymmetric import ed25519
import base64

# Generate key pair
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Export public key
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)
public_key_b64 = base64.b64encode(public_bytes).decode()

print(f"ed25519:{public_key_b64}")
```

### Signing Manifests

Sign your manifest to prove authenticity:

```python
import json
from cryptography.hazmat.primitives.asymmetric import ed25519

def sign_manifest(manifest: dict, private_key: ed25519.Ed25519PrivateKey) -> str:
    # Canonicalize JSON (sorted keys, no whitespace)
    canonical = json.dumps(manifest, sort_keys=True, separators=(',', ':'))

    # Sign with private key
    signature = private_key.sign(canonical.encode())

    # Return base64-encoded signature
    return base64.b64encode(signature).decode()

# Usage
signature = sign_manifest(manifest, private_key)
```

### Verifying Signatures

Verify manifest signatures before trusting:

```python
def verify_signature(manifest: dict, signature: str) -> bool:
    # Extract public key from manifest
    key_string = manifest["security"]["signingKeys"]["current"]
    key_bytes = base64.b64decode(key_string.split(':')[1])
    public_key = ed25519.Ed25519PublicKey.from_public_bytes(key_bytes)

    # Canonicalize manifest (exclude signature field)
    manifest_copy = manifest.copy()
    if "signature" in manifest_copy:
        del manifest_copy["signature"]
    canonical = json.dumps(manifest_copy, sort_keys=True, separators=(',', ':'))

    # Verify signature
    try:
        public_key.verify(
            base64.b64decode(signature),
            canonical.encode()
        )
        return True
    except:
        return False
```

## Key Management

### Key Rotation

Rotate keys regularly (recommended: annually):

**Step 1:** Announce new key 30+ days in advance

```json
"security": {
  "signingKeys": {
    "current": "ed25519:CURRENT_KEY",
    "next": "ed25519:NEW_KEY",
    "rotationDate": "2025-12-01T00:00:00Z"
  }
}
```

**Step 2:** On rotation date, promote new key

```json
"security": {
  "signingKeys": {
    "current": "ed25519:NEW_KEY",
    "previous": ["ed25519:CURRENT_KEY"]
  }
}
```

**Step 3:** After grace period (30 days), remove old key

```json
"security": {
  "signingKeys": {
    "current": "ed25519:NEW_KEY"
  }
}
```

### Key Storage

**DO:**
- Store private keys in HSMs or secure key vaults
- Use environment variables or secrets managers
- Implement key access logging
- Rotate keys regularly

**DON'T:**
- Commit private keys to version control
- Share private keys between environments
- Store keys in application code
- Use same key for multiple agents

### Key Compromise

If a private key is compromised:

1. Generate new key pair immediately
2. Update manifest with new key
3. Revoke compromised key
4. Notify registry operators
5. Update all deployments
6. Publish security advisory

## Domain Verification

### DNS TXT Records

Prove domain ownership via DNS:

**Add TXT Record:**
```
_adp.yourdomain.com IN TXT "adp=v2;key=sha256:HASH_OF_PUBLIC_KEY"
```

**Verification Process:**
```python
import dns.resolver
import hashlib
import base64

def verify_domain_control(domain: str, manifest: dict) -> bool:
    # Get DNS TXT record
    try:
        answers = dns.resolver.resolve(f"_adp.{domain}", "TXT")
    except:
        return False

    # Extract public key from manifest
    public_key = manifest["security"]["signingKeys"]["current"]
    key_bytes = base64.b64decode(public_key.split(':')[1])
    key_hash = hashlib.sha256(key_bytes).hexdigest()

    # Check if TXT record matches
    for answer in answers:
        txt = str(answer).strip('"')
        if f"key=sha256:{key_hash}" in txt:
            return True

    return False
```

### Well-Known URI Verification

Verify manifest is published at correct location:

```python
async def verify_well_known_uri(aid: str) -> bool:
    # Parse AID
    domain = aid.split("://")[1].split("/")[0]
    agent_version = aid.split("/")[1]
    agent_name, version = agent_version.split("@")

    # Construct expected URL
    url = f"https://{domain}/.well-known/agents/{agent_name}-{version}.json"

    # Fetch and compare
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            published_manifest = response.json()

        # Verify AID matches
        return published_manifest["aid"] == aid
    except:
        return False
```

## Attestations

Third-party attestations provide additional trust signals.

### Attestation Structure

```json
"attestations": [
  {
    "type": "domain_control",
    "value": "example.com",
    "attestor": "Certificate Authority Name",
    "signature": "eyJhbGciOiJFZDI1NTE5...",
    "validUntil": "2026-01-01T00:00:00Z"
  },
  {
    "type": "third_party_audit",
    "value": "SOC 2 Type II",
    "attestor": "Audit Firm Name",
    "signature": "eyJhbGciOiJFZDI1NTE5...",
    "validUntil": "2025-12-31T00:00:00Z"
  }
]
```

### Creating Attestations

As an attestor:

```python
def create_attestation(
    attestation_type: str,
    value: str,
    attestor_name: str,
    private_key: ed25519.Ed25519PrivateKey,
    valid_until: str
) -> dict:
    attestation = {
        "type": attestation_type,
        "value": value,
        "attestor": attestor_name,
        "validUntil": valid_until
    }

    # Sign attestation
    canonical = json.dumps(attestation, sort_keys=True)
    signature = private_key.sign(canonical.encode())

    attestation["signature"] = base64.b64encode(signature).decode()
    return attestation
```

### Verifying Attestations

```python
def verify_attestation(
    attestation: dict,
    attestor_public_key: ed25519.Ed25519PublicKey
) -> bool:
    # Extract signature
    signature = attestation.pop("signature")

    # Verify signature
    try:
        canonical = json.dumps(attestation, sort_keys=True)
        attestor_public_key.verify(
            base64.b64decode(signature),
            canonical.encode()
        )
        return True
    except:
        return False
```

## Transport Security

### HTTPS Requirements

All ADP endpoints MUST use HTTPS:

- Well-known URIs: HTTPS only
- Health checks: HTTPS preferred
- API endpoints: HTTPS required

### TLS Best Practices

1. Use TLS 1.2 or higher
2. Strong cipher suites only
3. Valid SSL certificates (no self-signed)
4. Enable HSTS headers
5. Implement certificate pinning (optional)

### Example Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=31536000" always;

    location /.well-known/agents/ {
        alias /var/www/agents/;
        add_header Content-Type application/json;
        add_header Access-Control-Allow-Origin *;
    }
}
```

## Authentication

### API Key Authentication

Secure API key implementation:

```python
import secrets

def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

def verify_api_key(provided_key: str, stored_hash: str) -> bool:
    import hashlib
    provided_hash = hashlib.sha256(provided_key.encode()).hexdigest()
    return secrets.compare_digest(provided_hash, stored_hash)
```

### OAuth 2.0

Implement OAuth 2.0 for agent invocation:

1. Register client application
2. Obtain authorization code
3. Exchange for access token
4. Include token in API requests

### JWT Authentication

Use JSON Web Tokens for stateless auth:

```python
import jwt

def create_token(agent_id: str, secret: str) -> str:
    payload = {
        "sub": agent_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def verify_token(token: str, secret: str) -> dict:
    return jwt.decode(token, secret, algorithms=["HS256"])
```

## Rate Limiting

Implement rate limiting to prevent abuse:

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.limit = requests_per_minute
        self.requests = defaultdict(list)

    def allow_request(self, client_id: str) -> bool:
        now = time.time()
        minute_ago = now - 60

        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > minute_ago
        ]

        # Check limit
        if len(self.requests[client_id]) >= self.limit:
            return False

        # Record request
        self.requests[client_id].append(now)
        return True
```

## Security Checklist

### For Agent Developers

- [ ] Generate Ed25519 key pair securely
- [ ] Store private keys in secure vault
- [ ] Sign all manifests before publishing
- [ ] Publish manifest over HTTPS
- [ ] Add DNS TXT record for verification
- [ ] Implement health check endpoint
- [ ] Use strong authentication (OAuth2, JWT)
- [ ] Implement rate limiting
- [ ] Log security events
- [ ] Rotate keys annually
- [ ] Monitor for unauthorized access
- [ ] Have incident response plan

### For Agent Consumers

- [ ] Verify manifest signatures
- [ ] Check domain ownership (DNS)
- [ ] Validate well-known URI
- [ ] Check certificate validity
- [ ] Review attestations
- [ ] Check compliance flags
- [ ] Monitor agent health
- [ ] Implement request timeouts
- [ ] Log invocation attempts
- [ ] Handle rate limits gracefully

### For Registry Operators

- [ ] Validate incoming manifests
- [ ] Verify cryptographic signatures
- [ ] Check DNS TXT records
- [ ] Rate limit registration requests
- [ ] Implement DDOS protection
- [ ] Log all registry operations
- [ ] Monitor for malicious agents
- [ ] Implement manifest caching
- [ ] Provide secure API endpoints
- [ ] Regular security audits

## Vulnerability Disclosure

If you discover a security vulnerability:

1. **DO NOT** disclose publicly
2. Email cjohnson@metisos.com with details
3. Include proof of concept if possible
4. Allow 90 days for patch development
5. Coordinate public disclosure

## Resources

- **Ed25519 Spec:** RFC 8032
- **TLS Best Practices:** Mozilla SSL Configuration Generator
- **OAuth 2.0:** RFC 6749
- **JWT:** RFC 7519
- **DNS Security:** DNSSEC

## References

- ADP Specification: `spec/ADP-SPECIFICATION.md`
- Examples: `examples/`
- Validation Tools: `tools/`
