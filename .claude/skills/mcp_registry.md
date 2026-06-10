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

### Firecrawl — REMOVED (2026-06-10)

| Field | Value |
|---|---|
| **Status** | REMOVED — no longer used |
| Server name | `firecrawl-mcp-server` (de-registered) |
| Removed | 2026-06-10 |
| Reason | No longer needed; its API key was exposed on GitHub, revoked, and purged from git history. |
| Cleanup | `.mcp.json` entry removed; dropped from `enabledMcpjsonServers`; `firecrawl_mcp_setup_report.md` deleted; literal key scrubbed from all history via `git filter-repo`. |

To re-add Firecrawl (or any keyed MCP) in future: store the key in a **gitignored** `.env` and reference it as `${FIRECRAWL_API_KEY}` in `.mcp.json` — never a literal in any tracked file.

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

### API Key Security

`C:\Bari` **is** a git repository. API keys for MCP servers must **never** be written as a literal into any tracked file. Instead:
- Store the key in a **gitignored** `.env` (the `.env` / `.env.*` patterns are in `.gitignore`).
- Reference it in `.mcp.json` via env-var expansion: `"FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"`.

Never store API keys in:
- `C:\Bari\.mcp.json` as a literal (use `${ENV_VAR}` expansion only)
- `C:\Bari\.claude\settings.json` (this file is reviewed and should be clean)
- Any file that is tracked, shared, or version-controlled
