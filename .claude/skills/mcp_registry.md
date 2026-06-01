# Bari MCP Registry

**Version:** 1.0
**Published:** 2026-05-31
**Owner:** Frontend Agent
**Task:** TASK-057

This registry tracks all MCP (Model Context Protocol) server integrations for the Bari project. MCP servers are tool integrations — they are distinct from Claude Code skills. They are NOT listed in `capability_stack_matrix.md` skill tiers.

---

## What is an MCP Server (vs. a Skill)

| Property | Claude Skill | MCP Server |
|---|---|---|
| Format | `SKILL.md` markdown file | `.mcp.json` config entry |
| Mechanism | Loads instructions into Claude's context | Provides tools Claude can call |
| Activation | Triggered by description match | Available as callable tools in every session |
| Location | `C:\Bari\.claude\skills\` | `C:\Bari\.mcp.json` |
| Has API key | No | Often yes |

---

## Registered MCP Servers

### Firecrawl

| Field | Value |
|---|---|
| **Status** | ACTIVE |
| Server name | `firecrawl-mcp-server` |
| Package | `firecrawl-mcp` (via npx) |
| Source | `github.com/mendableai/firecrawl-mcp-server` |
| Installed | 2026-05-31 |
| Task | TASK-057 |
| Config file | `C:\Bari\.mcp.json` |
| Approval | `enabledMcpjsonServers` in `C:\Bari\.claude\settings.json` |
| API key storage | `C:\Bari\.mcp.json` env block (not version controlled) |
| Scope | Project-level (`C:\Bari` only) |
| Health | ✓ Connected (verified 2026-05-31) |

**Purpose:** Web scraping and crawling — fetches structured content from URLs for use in Bari research workflows.

**Primary tools exposed:**
- `firecrawl_scrape` — scrape a single URL, returns clean markdown
- `firecrawl_crawl` — crawl a site and return multiple pages
- `firecrawl_search` — search the web and return structured results
- `firecrawl_map` — map all URLs on a domain

**Usage rights:**

| Agent | Rights | Restrictions |
|---|---|---|
| Research Agent | Primary | None |
| Product Agent | Supporting | None |
| Marketing Agent | Supporting | None |
| Content Agent | Supporting | None |
| Nutrition Agent | Conditional | Source discovery only — not scientific evidence |
| Data Agent | Conditional | Product research only — not authoritative product data without acquisition workflow approval |
| Frontend Agent | Limited | Documentation lookup only |
| Design Agent | Not assigned | — |
| QA Agent | Not assigned | — |

---

## Pending MCP Servers

### Supermemory

| Field | Value |
|---|---|
| **Status** | PENDING — awaiting data residency policy review |
| Package | TBD — `supermemory.ai` MCP server |
| Blocker | Bari category/scoring data must not transit external memory services without explicit approval |
| Task | Originally approved in TASK-049 |

**Action required:** Data policy review before installation. Confirm what categories of Bari data are permitted to be sent to Supermemory's servers.

---

## Installation Notes

### CLI Bug (Claude Code v2.1.158)

The `claude mcp add` command has a variadic flag parsing bug that prevents standard installation. Use direct file configuration:

1. Write `C:\Bari\.mcp.json` with `mcpServers` block
2. Add server name to `enabledMcpjsonServers` in `C:\Bari\.claude\settings.json`
3. Verify with `claude mcp list` (from `C:\Bari`)

See `firecrawl_mcp_setup_report.md` for full details.

### API Key Security

API keys for MCP servers must be stored in:
- `C:\Bari\.mcp.json` — acceptable only because C:\Bari is not a git repo
- If C:\Bari is ever git-initialised, `.mcp.json` must be added to `.gitignore` before the first commit

Never store API keys in:
- `C:\Bari\.claude\settings.json` (this file is reviewed and should be clean)
- Any file that may be shared or version-controlled
