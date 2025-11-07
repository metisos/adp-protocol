# Agent Discovery Protocol (ADP)

**Version:** 2.0.0
**Status:** Production Ready
**License:** MIT

An open standard for discovering, trusting, and invoking AI agents across the ecosystem.

## Overview

The Agent Discovery Protocol (ADP) provides a standardized way for AI agents to publish their capabilities, for consumers to discover relevant agents, and for systems to verify agent authenticity and trust.

**ADP solves three fundamental problems:**

1. **Discovery** - How do agents and humans find relevant AI services?
2. **Trust** - How do consumers verify agent authenticity and capabilities?
3. **Interoperability** - How do agents work across different platforms and protocols?

## Key Features

- **Protocol-Agnostic Invocation** - Supports MCP, REST, gRPC, GraphQL, WebSocket
- **Decentralized Discovery** - No single registry required; federated architecture
- **Cryptographic Trust** - Ed25519 signatures and multi-party attestations
- **Privacy-First Design** - Required data handling disclosures
- **Version Management** - Semantic versioning with deprecation support
- **Enterprise-Ready** - SLA commitments, compliance signals, audit trails

## Quick Start

### For Agent Developers

1. Create your agent manifest following the ADP v2.0 specification
2. Publish your manifest at `https://yourdomain.com/.well-known/agents/{name}-{version}.json`
3. Register with ADP-compatible registries (optional)

```json
{
  "aid": "aid://yourdomain.com/agent-name@1.0.0",
  "name": "Your Agent Name",
  "description": "What your agent does",
  "owner": {
    "org": "Your Organization",
    "site": "https://yourdomain.com",
    "contact": "support@yourdomain.com"
  },
  "capabilities": [
    {
      "id": "capability.action",
      "description": "Description of what this capability does"
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
    "dataSharing": "none"
  },
  "security": {
    "signingKeys": {
      "current": "ed25519:YOUR_PUBLIC_KEY_HERE"
    }
  },
  "updatedAt": "2025-11-07T00:00:00Z"
}
```

### For Agent Consumers

1. Search for agents via ADP registry or direct discovery
2. Verify agent manifest signature
3. Invoke agent using specified protocol (MCP, REST, etc.)

### For Registry Operators

1. Implement the ADP registry API specification
2. Validate incoming manifests against JSON Schema
3. Verify cryptographic signatures
4. Provide search and discovery services

## Documentation

- **[Specification](./spec/ADP-SPECIFICATION.md)** - Complete ADP v2.0 standard
- **[Getting Started](./docs/GETTING_STARTED.md)** - Step-by-step guide
- **[Manifest Guide](./docs/MANIFEST_GUIDE.md)** - Creating valid manifests
- **[Discovery Methods](./docs/DISCOVERY.md)** - How to discover agents
- **[Security](./docs/SECURITY.md)** - Signatures, attestations, and trust
- **[Registry API](./docs/REGISTRY_API.md)** - Building ADP registries
- **[Migration Guide](./docs/MIGRATION.md)** - Upgrading from v1.0 to v2.0

## Repository Structure

```
adp-public/
├── README.md              # This file
├── spec/                  # Formal specifications
│   ├── ADP-SPECIFICATION.md
│   └── CHANGELOG.md
├── schemas/               # JSON Schemas
│   ├── manifest-v2.0.json
│   └── registry-api.json
├── examples/              # Reference implementations
│   ├── manifests/         # Example agent manifests
│   ├── clients/           # Client code examples
│   └── validators/        # Validation tools
├── docs/                  # Documentation
│   ├── GETTING_STARTED.md
│   ├── MANIFEST_GUIDE.md
│   ├── DISCOVERY.md
│   ├── SECURITY.md
│   ├── REGISTRY_API.md
│   └── MIGRATION.md
└── tools/                 # Utilities
    ├── validate.py        # Manifest validator
    └── migrate.py         # v1.0 to v2.0 migration
```

## Examples

See the `examples/` directory for:

- **Complete agent manifests** - Production-ready examples
- **Client implementations** - Python, Node.js, Go examples
- **Registry integration** - How to register and discover agents
- **Validation tools** - Schema validation utilities

## Compliance Levels

ADP defines three compliance tiers:

**Bronze** - Basic manifest with required fields
**Silver** - Bronze + signing key verification + health endpoint
**Gold** - Silver + attestations + SLA monitoring + privacy policy

Agents can start at Bronze and upgrade over time.

## Contributing

We welcome contributions to the ADP specification and tooling.

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description
4. Follow the contribution guidelines

## Governance

ADP is governed by the Agent Discovery Protocol Standards Working Group (ADP-SWG), a multi-stakeholder organization committed to open standards.

**Specification Changes:**
1. Anyone can submit an RFC (Request for Comments)
2. Community feedback period (30+ days)
3. Working group review and vote
4. Publication with migration guide

## License

The ADP specification is licensed under CC BY 4.0.
Reference implementations and tools are licensed under MIT.

## Support

- **Specification Issues:** [GitHub Issues](https://github.com/adp-protocol/adp-spec/issues)
- **Documentation:** [Full documentation](./docs/)
- **Community:** [Discord](https://discord.gg/adp-protocol)
- **Email:** standards@adp.dev

## Related Standards

- **MCP (Model Context Protocol)** - Agent invocation protocol
- **OpenAPI** - REST API description
- **JSON Schema** - Data validation
- **OAuth 2.0** - Authentication
- **W3C DID** - Decentralized identity

ADP complements these standards by providing the discovery and metadata layer.

## Version History

- **v2.0.0** (2025-11-07) - Production release with privacy and security enhancements
- **v1.0.0** (2025-01-01) - Initial specification

## Acknowledgments

The ADP specification was developed with input from the AI agent community, including contributions from agent developers, registry operators, and standards organizations.

---

**Agent Discovery Protocol v2.0**
Making AI agents discoverable, trustable, and invocable at scale.
