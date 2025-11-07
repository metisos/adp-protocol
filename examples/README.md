# ADP Manifest Examples

This directory contains production-ready example manifests demonstrating various ADP v2.0 features.

## Basic Examples

### notify.json
Multi-channel notification service supporting email, SMS, Slack, webhooks, and push notifications.

**Features:**
- Multiple invocation protocols (REST, MCP)
- Detailed capability definitions with rate limits
- Privacy disclosures and compliance flags
- Security attestations
- Pricing tiers

### atlas.json
Order tracking agent providing multi-system visibility.

**Features:**
- Simple capability structure
- Single REST protocol
- Basic privacy and security configuration
- Minimal required fields

## Industry-Specific Examples

### analytics.json
Enterprise business intelligence and analytics platform.

**Features:**
- Multiple protocols (REST, MCP, WebSocket)
- Complex capability definitions
- Data analysis and forecasting
- SLA commitments

### calendar.json
Intelligent scheduling assistant with conflict detection.

**Features:**
- Natural language processing
- Multi-timezone support
- External calendar sync
- OAuth2 authentication

### payment.json
Payment processing gateway with PCI DSS compliance.

**Features:**
- Multiple payment methods
- Security certifications (PCI DSS, SOC 2)
- Fraud detection capabilities
- Transaction handling

### email.json
Email service with deliverability tracking.

**Features:**
- Template management
- Bounce handling
- Delivery analytics
- SMTP protocol support

### crm.json
Customer relationship management agent.

**Features:**
- Contact management
- Lead tracking
- Integration capabilities
- Data export functionality

### document.json
Document processing and analysis service.

**Features:**
- Multiple file format support
- OCR capabilities
- Content extraction
- Document generation

### translate.json
Multi-language translation service.

**Features:**
- 100+ language support
- Batch translation
- Terminology management
- Quality scoring

### weather.json
Weather data and forecasting service.

**Features:**
- Real-time conditions
- Multi-day forecasts
- Historical data access
- Alert notifications

## Validation

Validate any manifest using the provided tool:

```bash
python ../tools/validate.py manifest.json
```

## Usage

Use these manifests as templates for your own agents:

1. Copy an example that matches your use case
2. Update the AID with your domain
3. Modify capabilities to match your agent
4. Update owner information
5. Configure invocation protocols
6. Set privacy and security parameters
7. Validate against JSON Schema
8. Publish at well-known URI

## Compliance Levels

### Bronze Compliance
All examples meet Bronze requirements:
- Valid manifest with required fields
- Proper AID format
- Complete capability definitions
- Privacy disclosures
- Security configuration

### Silver Compliance
Examples with Silver features:
- notify.json (health check + signing key)
- atlas.json (domain verification)
- payment.json (certificate validation)

### Gold Compliance
Examples with Gold features:
- notify.json (attestations + SLA + privacy policy)
- payment.json (certifications + audit trail)
- analytics.json (comprehensive monitoring)

## Common Patterns

### Multiple Protocols
See: notify.json, analytics.json
Shows how to support REST, MCP, and other protocols simultaneously.

### Complex Capabilities
See: analytics.json, email.json
Demonstrates detailed input/output schemas, error definitions, and rate limits.

### Security & Compliance
See: payment.json, email.json
Examples of certifications, attestations, and compliance flags.

### Pricing Models
All examples show different pricing approaches:
- Free tier with limits
- Usage-based pricing
- Subscription models
- Enterprise custom pricing

## Resources

- JSON Schema: ../schemas/manifest-v2.0.json
- Validation Tool: ../tools/validate.py
- Documentation: ../docs/MANIFEST_GUIDE.md
- Specification: ../spec/ADP-SPECIFICATION.md
