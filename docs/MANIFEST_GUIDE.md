# Manifest Creation Guide

Complete guide to creating valid ADP v2.0 agent manifests.

## Manifest Structure

An ADP manifest is a JSON document that describes an agent's identity, capabilities, and service parameters.

### Required Fields

All manifests MUST include:

```json
{
  "aid": "Agent Identifier",
  "name": "Human-readable name",
  "owner": {/* Owner information */},
  "capabilities": [/* List of capabilities */],
  "invocation": {/* How to invoke the agent */},
  "privacy": {/* Data handling policies */},
  "security": {/* Cryptographic keys */},
  "updatedAt": "ISO 8601 timestamp"
}
```

## Agent Identifier (AID)

Format: `aid://{domain}/{agent-name}@{version}`

**Rules:**
- Domain must be DNS-resolvable
- Agent name must match pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Version must follow semantic versioning

**Examples:**
```json
"aid": "aid://anthropic.com/claude-analyst@1.0.0"
"aid": "aid://api.example.com/data-processor@2.1.0"
"aid": "aid://metisos.co/notify@1.5.0-beta.1"
```

## Owner Information

Identifies the organization responsible for the agent.

**Minimum Required:**
```json
"owner": {
  "org": "Organization Name"
}
```

**Recommended:**
```json
"owner": {
  "org": "Organization Name",
  "site": "https://example.com",
  "contact": "support@example.com",
  "support": "https://docs.example.com"
}
```

## Capabilities

Each capability represents a specific action the agent can perform.

**Basic Capability:**
```json
{
  "id": "capability.action",
  "description": "What this capability does (minimum 10 characters)"
}
```

**Full Capability with Schemas:**
```json
{
  "id": "email.send",
  "description": "Send email messages with attachments and tracking",
  "inputs": {
    "type": "object",
    "properties": {
      "to": {"type": "string", "format": "email"},
      "subject": {"type": "string", "maxLength": 200},
      "body": {"type": "string"},
      "attachments": {
        "type": "array",
        "items": {"type": "string", "format": "uri"}
      }
    },
    "required": ["to", "subject", "body"]
  },
  "outputs": {
    "type": "object",
    "properties": {
      "messageId": {"type": "string"},
      "status": {"type": "string", "enum": ["sent", "queued", "failed"]}
    }
  },
  "errors": [
    {
      "code": "invalid_email",
      "httpStatus": 400,
      "description": "Email address format is invalid",
      "retryable": false
    },
    {
      "code": "rate_limit_exceeded",
      "httpStatus": 429,
      "description": "Too many requests",
      "retryable": true,
      "retryAfterSeconds": 60
    }
  ],
  "rateLimit": {
    "requestsPerMinute": 60,
    "requestsPerHour": 1000,
    "burstLimit": 100
  },
  "sla": {
    "responseTimeMs": 500,
    "concurrency": 10
  }
}
```

**Capability ID Naming:**
- Use dot notation: `category.action`
- Lowercase only
- Hyphens allowed: `data-analysis.process`
- Examples: `email.send`, `payment.process`, `image.generate`

## Invocation

Defines how consumers can invoke your agent.

**Single Protocol:**
```json
"invocation": {
  "protocols": [
    {
      "type": "rest",
      "endpoint": "https://api.example.com/v1",
      "version": "1.0.0",
      "spec": "https://api.example.com/openapi.json",
      "healthCheck": "https://api.example.com/health"
    }
  ],
  "authentication": ["api_key"]
}
```

**Multiple Protocols:**
```json
"invocation": {
  "protocols": [
    {
      "type": "rest",
      "endpoint": "https://api.example.com/v1",
      "healthCheck": "https://api.example.com/health"
    },
    {
      "type": "mcp",
      "endpoint": "https://api.example.com/mcp",
      "version": "1.0"
    },
    {
      "type": "grpc",
      "endpoint": "grpc://api.example.com:443",
      "spec": "https://api.example.com/proto/service.proto"
    }
  ],
  "authentication": ["oauth2", "api_key", "jwt"]
}
```

**Protocol Types:**
- `rest` - RESTful HTTP API
- `mcp` - Model Context Protocol
- `grpc` - Google RPC
- `graphql` - GraphQL endpoint
- `websocket` - WebSocket connection

**Authentication Methods:**
- `oauth2` - OAuth 2.0 flow
- `api_key` - API key in header
- `jwt` - JSON Web Token
- `mtls` - Mutual TLS
- `none` - No authentication required

## Privacy

Required data handling disclosures.

**Minimum Required:**
```json
"privacy": {
  "dataRetentionDays": 90,
  "dataRegions": ["US"],
  "dataSharing": "none"
}
```

**Complete Privacy Section:**
```json
"privacy": {
  "dataRetentionDays": 90,
  "dataRegions": ["US", "EU", "AP"],
  "dataSharing": "none",
  "privacyPolicy": "https://example.com/privacy",
  "gdprCompliant": true,
  "ccpaCompliant": true,
  "hipaaCompliant": false
}
```

**Data Retention:**
- `0` - No data retained (ephemeral processing)
- Positive integer - Days data is kept
- `-1` - Indefinite retention

**Data Regions:**
- Use ISO 3166-1 alpha-2 country codes
- Examples: `US`, `EU`, `GB`, `JP`, `AU`

**Data Sharing:**
- `none` - No sharing with third parties
- `anonymized` - Aggregated analytics only
- `partners` - Shared with named partners
- `public` - Public dataset

## Security

Cryptographic keys and certifications.

**Minimum Required:**
```json
"security": {
  "signingKeys": {
    "current": "ed25519:MCowBQYDK2VwAyEAn1QT3nD8FqPzVZ+7K5mYvN9wX2rH8jL3pQ4sT6uV8wY="
  }
}
```

**With Key Rotation:**
```json
"security": {
  "signingKeys": {
    "current": "ed25519:CURRENT_KEY",
    "next": "ed25519:NEXT_KEY",
    "rotationDate": "2025-12-01T00:00:00Z",
    "previous": ["ed25519:OLD_KEY_1", "ed25519:OLD_KEY_2"]
  },
  "attestations": [
    {
      "type": "domain_control",
      "value": "example.com",
      "attestor": "Organization Name",
      "validUntil": "2026-01-01T00:00:00Z"
    }
  ],
  "certifications": ["soc2", "iso27001"],
  "vulnerabilityDisclosure": "https://example.com/security"
}
```

**Supported Certifications:**
- `soc2` - SOC 2 Type II
- `iso27001` - ISO/IEC 27001
- `pci-dss` - PCI DSS
- `fedramp` - FedRAMP
- `hipaa` - HIPAA compliant

## Optional Fields

### Description

```json
"description": "Detailed description of your agent (up to 2000 characters)"
```

### SLA

```json
"sla": {
  "uptimePct": 99.9,
  "responseTimeMs": 500,
  "errorRatePct": 0.1,
  "supportResponseHours": 24
}
```

### Pricing

```json
"pricing": [
  {
    "plan": "Free",
    "currency": "USD",
    "price": 0,
    "unit": "month",
    "rateLimit": {
      "requestsPerMonth": 1000
    },
    "features": ["Basic features", "Community support"]
  },
  {
    "plan": "Pro",
    "currency": "USD",
    "price": 29,
    "unit": "month",
    "rateLimit": {
      "requestsPerMonth": 50000
    },
    "features": ["All features", "Priority support", "SLA guarantee"]
  }
]
```

**Pricing Units:**
- `request` - Per API request
- `hour` - Per hour of usage
- `day` - Per day
- `month` - Per month
- `year` - Per year
- `token` - Per token processed
- `user` - Per user

### Metadata

```json
"metadata": {
  "category": ["communication", "automation"],
  "tags": ["email", "notifications", "alerts"],
  "statusPage": "https://status.example.com",
  "documentation": "https://docs.example.com",
  "repository": "https://github.com/org/repo",
  "license": "MIT"
}
```

**Categories:**
- `communication` - Email, messaging, notifications
- `data-analysis` - Analytics, reporting, insights
- `automation` - Workflow, task automation
- `security` - Auth, encryption, compliance
- `productivity` - Calendars, tasks, collaboration
- `development` - Code generation, testing
- `other` - Other categories

## Validation

Use the provided validator to check your manifest:

```bash
python tools/validate.py manifest.json
```

The validator checks:
1. JSON syntax
2. Required fields present
3. Field format compliance
4. Pattern matching (AID, emails, URIs)
5. Enum values
6. Array constraints

## Best Practices

1. **Keep descriptions clear and concise**
2. **Define input/output schemas** for all capabilities
3. **Specify error conditions** with clear codes
4. **Include rate limits** to set expectations
5. **Provide health check endpoint** for monitoring
6. **Update timestamp** whenever manifest changes
7. **Version appropriately** using semantic versioning
8. **Document privacy practices** thoroughly
9. **Rotate keys regularly** (at least annually)
10. **Test manifest validation** before publishing

## Examples

See `examples/` directory for complete manifest examples:

- `notify.json` - Notification service (multi-channel)
- `atlas.json` - Order tracking agent
- `analytics.json` - Business intelligence platform
- `calendar.json` - Scheduling assistant
- `payment.json` - Payment processing gateway

## Resources

- **JSON Schema:** `schemas/manifest-v2.0.json`
- **Specification:** `spec/ADP-SPECIFICATION.md`
- **Validator:** `tools/validate.py`
- **Examples:** `examples/`
