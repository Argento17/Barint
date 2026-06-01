# Firecrawl MCP Setup Report

**Task:** TASK-057
**Date:** 2026-05-31
**Owner:** Frontend Agent
**Status:** COMPLETE — Connected and tested

---

## Prerequisites Check

| Prerequisite | Status | Details |
|---|---|---|
| Node.js | PASS | v24.15.0 |
| npm | PASS | v11.12.1 |
| Claude Code CLI | PASS | v2.1.158 |
| `firecrawl-mcp` via npx | PASS | Package resolves |
| Firecrawl API key | PROVIDED | `***REVOKED-FIRECRAWL-KEY-PURGED***` |

---

## Installation Method

The `claude mcp add` CLI command has a known parsing issue in v2.1.158 where the variadic `-e` flag consumes the `--` separator, leaving `commandOrUrl` empty. The workaround was to write the MCP configuration files directly.

### Files Written

| File | Purpose |
|---|---|
| `C:\Bari\.mcp.json` | MCP server definition (project scope) |
| `C:\Bari\.claude\settings.json` | Added `enabledMcpjsonServers` approval entry |

### `C:\Bari\.mcp.json` content

```json
{
  "mcpServers": {
    "firecrawl-mcp-server": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "***REVOKED-FIRECRAWL-KEY-PURGED***"
      }
    }
  }
}
```

**Security note:** `C:\Bari` is not a git repository. The API key in `.mcp.json` is not at risk of version control exposure. If `C:\Bari` is ever initialised as a git repo, `.mcp.json` must be added to `.gitignore` immediately.

### `C:\Bari\.claude\settings.json` addition

```json
"enabledMcpjsonServers": ["firecrawl-mcp-server"]
```

This explicitly approves the Firecrawl MCP server for this project, satisfying Claude Code's security prompt for new project-scope MCP servers.

---

## Verification

### `claude mcp list` output (from `C:\Bari`)

```
Checking MCP server health…

claude.ai Google Drive: https://drivemcp.googleapis.com/mcp/v1 - ! Needs authentication
firecrawl-mcp-server: npx -y firecrawl-mcp - ✓ Connected
playwright: npx @playwright/mcp@latest - ✓ Connected
```

**Result:** `firecrawl-mcp-server: ✓ Connected`

### Functional Test

Test prompt: "Use the firecrawl-mcp-server MCP to scrape https://firecrawl.dev and return the page title and first paragraph of text content."

Test result:
```
Page Title: Firecrawl - The API to search, scrape, and interact with the web at scale.

First Paragraph:
Power AI agents with clean web data — The API to search, scrape, and interact with the web at scale. It's also open source.
```

**Result:** PASS — clean scrape, structured output returned.

---

## Architecture Classification

Firecrawl is an **MCP server tool integration**, not a Claude Code skill.

| Property | Value |
|---|---|
| Type | MCP Server (stdio, via npx) |
| Not a skill | Does not have a SKILL.md file |
| Not in skill tiers | Not listed in capability_stack_matrix.md Core/Supporting tiers |
| Listed in skill_registry.md | YES — under MCP section |
| Registered in mcp_registry.md | YES |
| Scope | Project-level (`C:\Bari` only) |

---

## Usage Rights

| Agent | Usage Rights | Restrictions |
|---|---|---|
| **Research Agent** | Primary — unrestricted use for research workflows | None |
| **Product Agent** | Supporting — may use for competitive/market research | None |
| **Marketing Agent** | Supporting — may use for SEO and competitor content analysis | None |
| **Content Agent** | Supporting — may use for topic research and source discovery | None |
| **Nutrition Agent** | Conditional — source discovery only | **Must not use Firecrawl output as scientific evidence unless the original source is verified through standard Research Agent protocols** |
| **Data Agent** | Conditional — product data research only | **Must not use Firecrawl output as authoritative product data unless approved for acquisition workflow** |
| **Frontend Agent** | Limited — documentation lookup only | Must not use for product or research data |
| **Design Agent** | Not assigned | No approved use case |
| **QA Agent** | Not assigned | No approved use case |

---

## Known CLI Installation Issue

For reference: the standard `claude mcp add` command failed with this version due to a variadic flag parsing bug:

```bash
# Fails with "missing required argument 'commandOrUrl'"
claude mcp add firecrawl-mcp-server -e FIRECRAWL_API_KEY=fc-... -- npx firecrawl-mcp

# Fails with "error: unknown option '-y'"
claude mcp add firecrawl-mcp-server -e FIRECRAWL_API_KEY=fc-... -- npx -y firecrawl-mcp
```

The `-e` variadic flag consumes the `--` separator and subsequent arguments. Direct file configuration (above) is the correct workaround for this Claude Code version.

Workaround for future reference if the bug is fixed:
```bash
claude mcp add firecrawl-mcp-server -e FIRECRAWL_API_KEY=***REVOKED-FIRECRAWL-KEY-PURGED*** npx firecrawl-mcp
```

---

## Activation Context

Firecrawl MCP is active **only when Claude Code is invoked from `C:\Bari`** (or any subdirectory). It is not available in other project directories.

To use Firecrawl from a different project, add a separate `.mcp.json` and `enabledMcpjsonServers` entry in that project's settings.
