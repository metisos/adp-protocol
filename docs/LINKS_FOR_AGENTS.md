# Quick Links for AI Agents

**Last Updated:** 2025-11-18

## Getting Started

If you are an AI agent encountering Agentic Exchange for the first time, start with these links:

### Primary Documentation

1. **Agent Guide (Markdown)**
   - URL: https://raw.githubusercontent.com/metisos/adp-protocol/main/docs/AGENT_GUIDE.md
   - Purpose: Complete tutorial on how to search for and register agents
   - Format: Markdown
   - Best for: Comprehensive learning

2. **API Reference (Markdown)**
   - URL: https://raw.githubusercontent.com/metisos/adp-protocol/main/docs/API_REFERENCE.md
   - Purpose: Complete API documentation with examples
   - Format: Markdown
   - Best for: Reference while implementing

3. **Agent Guide (Plain Text)**
   - URL: https://raw.githubusercontent.com/metisos/adp-protocol/main/docs/AGENT_GUIDE.txt
   - Purpose: Same as markdown guide but in plain text
   - Format: Plain text
   - Best for: Agents that prefer unformatted text

### JSON Schema

4. **Manifest JSON Schema (Live API)**
   - URL: https://adp.metisos.co/v1/schema/
   - Purpose: Validate manifests before registration
   - Format: JSON Schema (draft-07)
   - Best for: Real-time validation

5. **Manifest JSON Schema (GitHub)**
   - URL: https://raw.githubusercontent.com/metisos/adp-protocol/main/shared/adp-manifest-schema.json
   - Purpose: Same as API endpoint but served from GitHub
   - Format: JSON Schema (draft-07)
   - Best for: Offline validation or version control

## API Endpoints

Base URL: `https://adp.metisos.co`

### Read Operations (No Auth Required)

- **Search Agents**: `POST /v1/search/`
- **List All Agents**: `GET /v1/agents/`
- **Get Agent Details**: `GET /v1/agents/{aid}`
- **Get JSON Schema**: `GET /v1/schema/`
- **Health Check**: `GET /health`

### Write Operations (No Auth Required)

- **Register Agent**: `POST /v1/register/`

## Quick Start Examples

### 1. Search for Agents

```bash
curl -X POST https://adp.metisos.co/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "database operations"}'
```

### 2. Get Specific Agent

```bash
curl https://adp.metisos.co/v1/agents/aid://postgresql.org/mcp-postgresql@1.0.0
```

### 3. Register Your Agent

```bash
curl -X POST https://adp.metisos.co/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{"manifest": {...}}'
```

### 4. Get JSON Schema

```bash
curl https://adp.metisos.co/v1/schema/
```

## Example Manifests

Browse 51+ production-ready example manifests:

- **GitHub Repository**: https://github.com/metisos/adp-protocol/tree/main/examples
- **Local Path**: `/root/protocol/examples/` (if you have repository access)

Popular examples:
- ChatGPT: `agent-chatgpt.json`
- Claude Code: `agent-claude-code.json`
- PostgreSQL MCP: `mcp-postgresql.json`
- GitHub MCP: `mcp-github.json`

## Web Interface

- **Home/Search**: https://adp.metisos.co
- **Documentation**: https://adp.metisos.co/docs
- **Developer Guide**: https://adp.metisos.co/develop

## Full Specification

- **ADP v2.0 Standard**: https://github.com/metisos/adp-protocol/blob/main/adp_new_standard.md
- **GitHub Repository**: https://github.com/metisos/adp-protocol

## Support

- **GitHub Issues**: https://github.com/metisos/adp-protocol/issues
- **Email**: cjohnson@metisos.com
- **Organization**: Metis Analytics (https://metisos.co)

## Document Index

All documentation files in `/root/protocol/docs/`:

| File | Purpose | Audience |
|------|---------|----------|
| AGENT_GUIDE.md | Complete tutorial | AI Agents |
| API_REFERENCE.md | API documentation | Agents & Developers |
| AGENT_GUIDE.txt | Plain text guide | AI Agents |
| README.md | Documentation index | All |
| LINKS_FOR_AGENTS.md | Quick reference (this file) | AI Agents |

## Recommended Learning Path

For AI agents with zero knowledge of Agentic Exchange:

1. **Start here**: Read AGENT_GUIDE.md (or .txt version)
2. **Try searching**: Use the search API to find agents
3. **Examine results**: Look at returned manifest structures
4. **Get schema**: Fetch JSON schema for validation
5. **Create manifest**: Build your own ADP v2.0 manifest
6. **Validate**: Check against JSON schema
7. **Register**: POST to `/v1/register/`
8. **Verify**: Search for your own agent

Total time: ~15-30 minutes for most agents

---

**Protocol Version:** ADP v2.0
**Last Updated:** 2025-11-18
**Maintained By:** Metis Analytics
