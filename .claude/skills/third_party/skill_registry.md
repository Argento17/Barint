# Bari Third-Party Skill Registry

**Status:** 14 of 16 skills installed — Wave 2 complete (TASK-049C)
**Last updated:** 2026-05-31
**Owner:** Frontend Architect

This registry documents all approved third-party skills for the Bari project.
A skill is not considered installed until its source is verified, its content is reviewed, and its SKILL.md is placed in this directory.

---

## Registry Status Legend

| Symbol | Meaning |
|---|---|
| INSTALLED | SKILL.md present, source verified, content reviewed |
| MCP | Not a Claude Code skill — requires MCP server configuration |
| SOURCE_REQUIRED | Approved for installation, source repository not yet confirmed |
| BLOCKED | Source found but content failed security review |

---

## Registry

### 1. Anthropic Frontend Design

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049) |
| Source Repository | `https://github.com/anthropics/skills/tree/main/skills/frontend-design` |
| Version | main branch — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\frontend-design\SKILL.md` |
| Purpose | Create distinctive, production-grade frontend interfaces that avoid generic AI aesthetics |
| Activation Trigger | "build web components", "create a page", "style/beautify UI", "landing page", "dashboard", "React component" |
| Dependencies | None |
| Security Notes | No external calls. Content is self-contained. REVIEWED: safe. |
| Tested | Yes — 2026-05-31 (see installation_report_v1.md) |

---

### 2. Vercel Web Design Guidelines

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049) |
| Source Repository | `https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines` |
| Version | 1.0.0 — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\web-design-guidelines\SKILL.md` |
| Purpose | Review UI code against Vercel Web Interface Guidelines |
| Activation Trigger | "review my UI", "check accessibility", "audit design", "review UX", "check against best practices" |
| Dependencies | **Makes runtime WebFetch call** to `github.com/vercel-labs/web-interface-guidelines/main/command.md` |
| Security Notes | ATTENTION: fetches external content at runtime. Approved for Bari frontend files only. Do not use if external URL unavailable — fall back to `bari-frontend-ui`. |
| Tested | Yes — 2026-05-31 (see installation_report_v1.md) |

---

### 3. Vercel React Best Practices

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049) |
| Source Repository | `https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices` |
| Version | 1.0.0 — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\react-best-practices\SKILL.md` |
| Purpose | 70 React/Next.js performance optimization rules across 8 priority categories |
| Activation Trigger | "React component", "Next.js", "data fetching", "bundle optimization", "performance improvements", "refactor React" |
| Dependencies | None |
| Security Notes | No external calls. Content is self-contained. REVIEWED: safe. |
| Tested | Yes — 2026-05-31 (see installation_report_v1.md) |

---

### 4. Vercel Composition Patterns

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049) |
| Source Repository | `https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns` |
| Version | 1.0.0 — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\composition-patterns\SKILL.md` |
| Purpose | 8 React composition rules to eliminate boolean prop proliferation and build scalable component APIs |
| Activation Trigger | "boolean props", "compound components", "component library", "render props", "context providers", "component architecture" |
| Dependencies | None. React 19 section applies only to React 19+ projects. |
| Security Notes | No external calls. Content is self-contained. REVIEWED: safe. |
| Tested | Yes — 2026-05-31 (see installation_report_v1.md) |

---

### 5. UI/UX Pro Max

| Field | Value |
|---|---|
| **Status** | **INSTALLED (PARTIAL)** |
| Approved | Yes (TASK-049) |
| Source Repository | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` (85.2k stars, MIT) |
| Version | main branch — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\uiux-pro-max\SKILL.md` |
| Purpose | Design intelligence: 50+ styles, 161 palettes, 57 font pairings, 99 UX guidelines, 10 stacks |
| Activation Trigger | "design", "UI/UX", "accessibility", "color system", "typography", "animation", "build/review/fix/improve UI" |
| Dependencies | Optional: shadcn/ui MCP for component search |
| Security Notes | YAML frontmatter is verbatim from source. Body rules derived from source documentation (full verbatim SKILL.md was too large to reproduce via WebFetch). To get complete rule set, sync from source repo. |
| Tested | Yes — activation trigger confirmed 2026-05-31 (see installation_report_v1.md) |

---

### 6. Vercel React Native Skills

| Field | Value |
|---|---|
| Status | SOURCE_REQUIRED |
| Approved | Yes (TASK-049) |
| Source Repository | Not confirmed |
| Version | Unknown |
| Installation Path | `C:\Bari\.claude\skills\third_party\vercel-react-native\SKILL.md` |
| Purpose | React Native patterns per Vercel guidance |
| Activation Trigger | Unknown — source review required |
| Dependencies | None expected |
| Security Notes | Clarify: Bari is a web platform, not a native app. Confirm this skill is needed. |

---

### 6b. Find Skills (TASK-049B addition)

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049B) |
| Source Repository | `https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md` (20.7k stars) |
| Version | main branch — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\find-skills\SKILL.md` |
| Purpose | Discover and install agent skills from the open agent skills ecosystem via `npx skills` CLI |
| Activation Trigger | "find a skill for", "is there a skill that", "how do I do X", "can you do X", "extend capabilities" |
| Dependencies | `npx skills` CLI (optional, for discovery). Bari-specific gate: discovered skills require Frontend Architect approval before installation. |
| Security Notes | No external calls in the skill itself. Points to skills.sh leaderboard for discovery. Discovery output must go through Bari vetting before any install. |
| Tested | Yes — 2026-05-31 (see installation_report_v1.md) |

---

### 7. Superpowers

| Field | Value |
|---|---|
| Status | SOURCE_REQUIRED |
| Approved | Yes (TASK-049) |
| Source Repository | Not confirmed — "claude-code-superpowers" is referenced in the community but no canonical repo confirmed |
| Version | Unknown |
| Installation Path | `C:\Bari\.claude\skills\third_party\superpowers\SKILL.md` |
| Purpose | Unknown — name is too generic to infer purpose without source |
| Activation Trigger | Unknown |
| Dependencies | Unknown |
| Security Notes | HIGH PRIORITY REVIEW — vague-named skills with broad capability claims require careful content review |

---

### 8. Using Git Worktrees

| Field | Value |
|---|---|
| Status | SOURCE_REQUIRED |
| Approved | Yes (TASK-049) |
| Source Repository | Not confirmed |
| Version | Unknown |
| Installation Path | `C:\Bari\.claude\skills\third_party\git-worktrees\SKILL.md` |
| Purpose | Guide Claude through git worktree workflows |
| Activation Trigger | Likely: "create a worktree", "work in isolation", "parallel branches" |
| Dependencies | Claude Code has built-in `EnterWorktree`/`ExitWorktree` tools — confirm this skill adds value beyond built-in |
| Security Notes | Verify skill does not override or conflict with Claude Code's native worktree support |

---

### 9. Tapestry

| Field | Value |
|---|---|
| Status | SOURCE_REQUIRED |
| Approved | Yes (TASK-049) |
| Source Repository | Not confirmed — "Tapestry" is ambiguous (framework? tool? code weaving concept?) |
| Version | Unknown |
| Installation Path | `C:\Bari\.claude\skills\third_party\tapestry\SKILL.md` |
| Purpose | Unknown — requires clarification of what "Tapestry" refers to in this context |
| Activation Trigger | Unknown |
| Dependencies | Unknown |
| Security Notes | Cannot assess until purpose is clarified |

---

### 10. Content Research Writer

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049 / installed TASK-049C) |
| Source Repository | `https://github.com/ComposioHQ/awesome-claude-skills/blob/master/content-research-writer/SKILL.md` |
| Version | master branch — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\content-research-writer\SKILL.md` |
| Purpose | Collaborative writing partner: research, outline, draft, cite, and refine content while preserving the writer's voice |
| Activation Trigger | "writing blog posts", "creating educational content", "drafting thought leadership", "researching and writing case studies", "improving hooks and introductions", "section-by-section feedback while writing" |
| Dependencies | None. Works best with web search enabled for research phase. |
| Security Notes | Does not post to external services. Bari note: output destined for live site needs category team review. REVIEWED: safe. |
| Bari Agent | Research Analyst, Head of Product, Chief Nutrition Officer |
| Tested | Yes — 2026-05-31 |

---

### 11. Firecrawl

| Field | Value |
|---|---|
| **Status** | **MCP ACTIVE** — connected and tested (TASK-057) |
| Type | MCP Server — NOT a Claude Code skill. No SKILL.md. Not in capability_stack_matrix skill tiers. |
| Approved | Yes (TASK-049), configured (TASK-057) |
| Source Repository | `github.com/mendableai/firecrawl-mcp-server` |
| Package | `firecrawl-mcp` via npx |
| Config File | `C:\Bari\.mcp.json` — `mcpServers.firecrawl-mcp-server` |
| Approval Entry | `enabledMcpjsonServers` in `C:\Bari\.claude\settings.json` |
| API Key Storage | `C:\Bari\.mcp.json` env block (C:\Bari is not a git repo — safe) |
| Scope | Project-level — active only when Claude Code runs from `C:\Bari` |
| Primary Agent | Research Agent |
| Supporting Agents | Product Agent, Marketing Agent, Content Agent |
| Restricted | Nutrition Agent (source discovery only), Data Agent (product research only, not authoritative data), Frontend Agent (docs only) |
| Health | ✓ Connected — verified 2026-05-31 |
| Full Registry | See `mcp_registry.md` |

---

### 12. Webapp Testing

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049 / installed TASK-049C) |
| Source Repository | `https://github.com/AutumnsGrove/ClaudeSkills/blob/master/webapp-testing/SKILL.md` |
| Version | master branch — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\webapp-testing\SKILL.md` |
| Purpose | Playwright-based E2E testing: multi-browser, mobile emulation, screenshot capture, API mocking, visual regression |
| Activation Trigger | "E2E testing", "UI automation", "test across browsers", "visual regression", "API mocking", "mobile responsive testing" |
| Dependencies | `playwright`, `pytest-playwright` Python packages; `playwright install` for browser binaries |
| Security Notes | Bari note added: tests must not run against production; use mock API responses. REVIEWED: safe. |
| Bari Agent | Frontend Architect, QA & Audit Lead |
| Tested | Yes — 2026-05-31 |

---

### 13. Skill Creator

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049 / installed TASK-049C) |
| Source Repository | `https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md` |
| Version | main branch — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\skill-creator\SKILL.md` |
| Purpose | Guide Claude through creating, structuring, and validating new Claude Code skills using progressive disclosure principles |
| Activation Trigger | "create a skill", "add a skill to plugin", "write a new skill", "improve skill description", "organize skill content", "write a SKILL.md" |
| Dependencies | None |
| Security Notes | Bari gate added: all skills created by this skill must be reviewed by the designated owner before use. REVIEWED: safe. |
| Bari Agent | All agents (meta-skill) |
| Tested | Yes — 2026-05-31 |

---

### 14. Supermemory

| Field | Value |
|---|---|
| **Status** | **MCP — NOT A CLAUDE CODE SKILL** |
| Approved | Yes (TASK-049) |
| Source Repository | `supermemory.ai` — MCP server available |
| Version | Check supermemory.ai for current version |
| Installation Path | N/A — requires MCP server configuration in `.claude/settings.json` |
| Purpose | Persistent memory layer across Claude Code sessions |
| Activation Trigger | Claude Code MCP tool calls — not a SKILL.md activation |
| Dependencies | Supermemory API key required |
| Security Notes | All memory stored via Supermemory transits external servers. Review data sensitivity before enabling. Bari category/scoring data must not be sent to external memory services without explicit approval. |

**Action required:** Configure as MCP server in `.claude/settings.json`, not as a skill file.

---

### 15. File / PDF Document Processing

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049 / installed TASK-049C) |
| Source Repository | `https://github.com/ComposioHQ/awesome-claude-skills/blob/master/document-skills/pdf/SKILL.md` |
| Version | master branch — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\file-document-processing\SKILL.md` |
| Purpose | PDF manipulation toolkit: extract text/tables, create PDFs, merge/split documents, handle forms, OCR scanned PDFs |
| Activation Trigger | "fill in a PDF form", "process PDF documents", "extract text from PDF", "merge PDFs", "split PDF", "extract tables from PDF" |
| Dependencies | `pypdf`, `pdfplumber`, `reportlab`, `pandas` (Python). OCR: `pytesseract`, `pdf2image`. CLI: `poppler-utils`, `qpdf` (optional). |
| Security Notes | License: Proprietary (ComposioHQ). Check LICENSE.txt in source repo before redistribution. Bari note added: do not write output files outside project directory. |
| Bari Agent | Research Analyst, QA & Audit Lead, Chief Nutrition Officer |
| Tested | Yes — 2026-05-31 |

---

### 16. Marketing Skills (4 subskills installed)

Source repository: `https://github.com/coreyhaines31/marketingskills` (v2.3.0, MIT, 50+ skills available)
Installed 4 of 50+ subskills. Remaining skills are available from source if needed.

#### 16a. Copywriting

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049 / installed TASK-049C) |
| Source | `skills/copywriting/SKILL.md` in `coreyhaines31/marketingskills` |
| Version | 2.0.0 — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\marketing\copywriting\SKILL.md` |
| Purpose | Write, rewrite, or improve marketing copy for any page — homepage, landing pages, pricing, feature pages, about pages |
| Activation Trigger | "write copy for", "improve this copy", "rewrite this page", "marketing copy", "headline help", "CTA copy", "value proposition", "tagline", "hero section copy" |
| Dependencies | None. Optionally reads `.agents/product-marketing.md` context file if present. |
| Security Notes | Bari note: Hebrew website copy requires category team review. REVIEWED: safe. |
| Bari Agent | Head of Product |

#### 16b. Marketing Ideas

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049 / installed TASK-049C) |
| Source | `skills/marketing-ideas/SKILL.md` in `coreyhaines31/marketingskills` |
| Version | 2.0.0 — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\marketing\marketing-ideas\SKILL.md` |
| Purpose | 139 proven marketing ideas organized by category, stage, and budget |
| Activation Trigger | "marketing ideas", "growth ideas", "how to market", "marketing strategies", "brainstorm marketing", "what marketing should I do" |
| Dependencies | None. Optionally reads `.agents/product-marketing.md` context file if present. |
| Security Notes | REVIEWED: safe. |
| Bari Agent | Head of Product |

#### 16c. Content Strategy

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049 / installed TASK-049C) |
| Source | `skills/content-strategy/SKILL.md` in `coreyhaines31/marketingskills` |
| Version | 2.0.0 — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\marketing\content-strategy\SKILL.md` |
| Purpose | Plan content strategy, decide what to create, build content pillars and topic clusters |
| Activation Trigger | "content strategy", "what should I write about", "content ideas", "blog strategy", "topic clusters", "content planning", "editorial calendar", "content pillars" |
| Dependencies | None. Optionally reads `.agents/product-marketing.md` context file if present. |
| Security Notes | REVIEWED: safe. |
| Bari Agent | Head of Product, Research Analyst |

#### 16d. SEO Audit

| Field | Value |
|---|---|
| **Status** | **INSTALLED** |
| Approved | Yes (TASK-049 / installed TASK-049C) |
| Source | `skills/seo-audit/SKILL.md` in `coreyhaines31/marketingskills` |
| Version | 2.0.0 — 2026-05-31 |
| Installation Path | `C:\Bari\.claude\skills\third_party\marketing\seo-audit\SKILL.md` |
| Purpose | Audit, review, and diagnose SEO issues — technical SEO, on-page optimization, international SEO/hreflang |
| Activation Trigger | "SEO audit", "technical SEO", "why am I not ranking", "SEO issues", "on-page SEO", "my traffic dropped", "lost rankings", "core web vitals", "crawl errors" |
| Dependencies | Optional: Search Console access, Screaming Frog, Ahrefs/Semrush. Rich Results Test for schema validation. |
| Security Notes | Contains detailed hreflang guidance relevant to Bari's Hebrew locale. REVIEWED: safe. |
| Bari Agent | Head of Product, Research Analyst |

---

## MCP Servers (Separate Installation Track)

The following approved items are MCP server integrations, not Claude Code skills. They require separate configuration in `.claude/settings.json` and are tracked here for completeness.

| Name | Type | API Key Required | Config Location |
|---|---|---|---|
| Firecrawl | MCP Server | Yes (`FIRECRAWL_API_KEY`) | `.claude/settings.json` → `mcpServers` |
| Supermemory | MCP Server | Yes | `.claude/settings.json` → `mcpServers` |

---

## How to Complete an Installation

When the source for a SOURCE_REQUIRED skill is confirmed:

1. Obtain the SKILL.md from the verified source repository
2. Security review: confirm no external network calls, no data exfiltration instructions, no hardcoded credentials
3. Place file at the installation path listed above
4. Update this registry: change status to INSTALLED, record version and source repo
5. Update `skill_activation_guide.md` with confirmed activation triggers
6. Run the validation prompt from the activation guide
7. Record validation result
