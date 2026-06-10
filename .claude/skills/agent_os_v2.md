# Bari Agent Operating System v2

**Status:** ACTIVE
**Version:** 2.0
**Supersedes:** `agent_os_v1.md` (archived — do not use for new work)
**Published:** 2026-05-31
**Owner:** Product Agent
**Task:** TASK-049E

Agent OS v2 completes the migration from persona architecture to agent architecture. All six legacy persona files are deprecated. Agent definition files in `C:\Bari\.claude\agents\` are now the single source of truth for all agent behavior.

---

## What Changed from v1

| Area | v1 | v2 |
|---|---|---|
| Agent definitions | Persona files (`head-of-product.md`, etc.) | Agent files (`product-agent.md`, etc.) |
| Definition location | `C:\Bari\.claude\skills\` | `C:\Bari\.claude\agents\` |
| Agents covered | 6 (persona-based) + 3 (OS-only) | 9 (all have dedicated agent files) |
| Architecture model | Hybrid (persona + OS) | Agent-native (OS only) |
| Skill assignments | In OS + activation guide only | In each agent's definition file |
| Decision rights | In `decision_rights_matrix.md` only | In each agent's definition file |

All approval flows, escalation paths, cross-agent collaboration rules, and skill assignments are **unchanged**. v2 is a structural migration, not a policy change.

---

## Agent Roster

| Agent | Definition File | Primary Workspace | Successor to |
|---|---|---|---|
| **Product Agent** | `agents/product-agent.md` | `C:\Bari` | `head-of-product.md` |
| **Nutrition Agent** | `agents/nutrition-agent.md` | `C:\Bari` | `chief-nutrition-officer.md` |
| **Research Agent** | `agents/research-agent.md` | `C:\Bari` | `research-analyst.md` |
| **Data Agent** | `agents/data-agent.md` | `C:\Bari` | *(agent-native)* |
| **Frontend Agent** | `agents/frontend-agent.md` | `C:\bari\bari-web` | `frontend-architect.md` |
| **Design Agent** | `agents/design-agent.md` | `C:\Bari\01_framework\frontend\` | `design-director.md` |
| **QA Agent** | `agents/qa-agent.md` | Both workspaces | `qa-audit-lead.md` |
| **Content Agent** | `agents/content-agent.md` | `C:\Bari` | *(agent-native)* |
| **Marketing Agent** | `agents/marketing-agent.md` | `C:\Bari` | *(agent-native)* |

---

## System Overview

Bari operates across two physical workspaces:

| Workspace | Path | Domain |
|---|---|---|
| Product & Data | `C:\Bari` | BSIP pipeline, scoring, research, strategy, content docs, design specs |
| Website | `C:\bari\bari-web` | Next.js app, React components, routes, frontend JSON, lint, build |

**Invariant:** No agent edits website source under `C:\Bari`. No agent edits pipeline assets under `C:\bari\bari-web`. The Frontend JSON dataset is the interface: generated at `C:\Bari`, deployed to `C:\bari\bari-web\src\data\comparisons\`.

---

## Approval Flows

*Unchanged from v1. Agent names updated.*

### Flow 1: New Category Launch

```
Product Agent initiates
    ↓
Research Agent produces market landscape
    ↓
Nutrition Agent confirms scoring approach exists
    ↓
Product Agent approves launch brief
    ↓
Data Agent: Shelf Mapping → [Product Agent approval]
    ↓
Data Agent: Corpus Filter → [Product Agent approval]
    ↓
Data Agent: BSIP0 Gate → [Product Agent approval] + QA Agent verification
    ↓
Data Agent: BSIP1 Enrichment → [Nutrition Agent approval]
    ↓
QA Agent: QA Gate → hard fails block; warnings reviewed
    ↓
Data Agent: BSIP2 Readiness → [Nutrition Agent + Product Agent approval]
    ↓
Data Agent: Frontend JSON generation
    ↓
Frontend Agent: Page implementation → [Design Agent spec approval first]
    ↓
Content Agent: Copy authoring → [Nutrition Agent + Product Agent approval]
    ↓
QA Agent: Pre-launch checklist → PASS / FAIL verdict
    ↓
Product Agent: Go-live decision
    ↓
Marketing Agent: Launch campaign
```

### Flow 2: Scoring Rule Change

```
Nutrition Agent proposes rule (with evidence registry reference)
    ↓
Data Agent reviews implementability
    ↓
bari-bsip2-scoring-governance checklist:
    - Evidence registry reference ✓
    - Label observability ✓
    - Category activation scope ✓
    - Rollback plan ✓
    - Rule accumulation check ✓
    ↓
Nutrition Agent approves (scientific validity)
    ↓
Product Agent approves (scope and business impact)
    [Both approvals required — either can block]
    ↓
Data Agent implements
    ↓
Nutrition Agent verifies implementation matches spec
    ↓
QA Agent verifies score propagation
```

### Flow 3: New Frontend Component

```
Product Agent approves scope
    ↓
Design Agent produces visual spec
    ↓
Product Agent approves spec (if it affects page structure or scope)
    ↓
Frontend Agent implements
    ↓
QA Agent verifies: geometry, leakage, drift, build pass
    ↓
Design Agent visual review
    ↓
Product Agent launch approval
```

### Flow 4: Content Publication

```
Content Agent drafts copy
    ↓
Nutrition Agent approves (accuracy of all nutrition-facing claims)
    ↓
Product Agent approves (positioning, product-level claims)
    ↓
Frontend Agent integrates copy into frontend JSON
    ↓
QA Agent verifies copy fields present in rendered page
```

### Flow 5: New Skill Installation

```
Any agent identifies capability gap
    ↓
Agent documents: gap description, proposed skill, source URL
    ↓
Frontend Agent reviews: source verification, security review, content completeness
    ↓
Product Agent approves: capability gap justified, not covered by existing skills
    ↓
Frontend Agent installs: SKILL.md, registry update, activation test
    ↓
QA Agent validates: installation confirmed, no dependency issues
    ↓
capability_stack_matrix.md updated with new skill assignment
```

---

## Escalation Paths

| Situation | Escalate to |
|---|---|
| Scope expansion or cut decision | Product Agent |
| Scoring rule conflict | Product Agent + Nutrition Agent (joint review) |
| Score discrepancy: data path issue | Data Agent |
| Score discrepancy: logic issue | Nutrition Agent |
| Frontend build failure | Frontend Agent |
| Visual constraint violation | Design Agent |
| QA hard fail blocks launch | QA Agent → Product Agent (launch decision) |
| New skill needed | Frontend Agent (infrastructure) + Product Agent (approval) |
| Agent OS conflict or gap | Product Agent |

### Escalation Protocol

1. State what you were doing and what blocked you
2. Name which decision right you lack
3. Name who holds that right
4. Stop and wait — do not proceed past a blocked step
5. Do not implement a workaround to avoid escalation

---

## Cross-Agent Collaboration Rules

1. **Research → Nutrition or Product, not Research → Data.** Research outputs are interpreted by Nutrition Agent or Product Agent before feeding the pipeline.
2. **Design spec before implementation.** Frontend Agent does not begin a new component without Design Agent's approved spec.
3. **Frontend JSON is the interface.** Data Agent generates it; Frontend Agent consumes it. The `BariProductVM` contract is the schema boundary.
4. **Content copy before integration.** Frontend Agent does not hardcode placeholder copy. Content Agent provides approved copy; Frontend Agent integrates it.
5. **QA is downstream of implementation.** QA Agent runs after implementation is complete, not during.
6. **Named escalations only.** "Someone should look at this" is not an escalation. Name the agent, decision domain, and blocking condition.
7. **Verdict before details.** QA Agent delivers PASS/FAIL before itemized findings. Nutrition Agent states conclusion before reasoning. Product Agent states recommendation before analysis.
8. **No cross-domain override.** Nutrition Agent cannot override frontend decisions. Frontend Agent cannot override design decisions. Design Agent cannot override scope decisions.
9. **Hard rules are non-negotiable.** Each agent definition file contains Hard Rules that cannot be overridden by another agent's request.
10. **BSIP stages are sequential.** `bari-category-factory` stages run in order. No stage begins without the prior stage's gate approval.
11. **Scoring and frontend are independent tracks.** They do not block each other until BSIP2 readiness.
12. **Research and pipeline are parallel.** Research Agent work for an upcoming category can run in parallel with the active category's pipeline.
13. **No self-scoping.** An agent may not expand its own scope without Product Agent approval.
14. **No silent defers.** Incomplete outputs must be explicitly flagged as incomplete.
15. **Marketing activates after launch.** Marketing Agent does not run campaigns for unverified categories.

---

## Companion Documents

| Document | Location | Purpose |
|---|---|---|
| `capability_stack_matrix.md` | `C:\Bari\.claude\skills\` | Agent skill tiers (Core/Supporting/Optional/Restricted) |
| `decision_rights_matrix.md` | `C:\Bari\.claude\skills\` | Decision domains with per-agent rights |
| `ownership_matrix_v2.md` | `C:\Bari\.claude\skills\` | Domain, artifact, and process ownership |
| `migration_report.md` | `C:\Bari\.claude\skills\` | TASK-049E migration audit trail |
| `deprecated_personas.md` | `C:\Bari\.claude\skills\` | Retirement plan for legacy persona files |
| `agent_os_v1.md` | `C:\Bari\.claude\skills\` | Archived — do not use for new work |

---

## Skill Architecture Freeze

*Status unchanged from v1. Reproduced here for completeness.*

As of 2026-05-31, the Bari Skill Architecture v1 is frozen.

**Bari-native:** `bari-category-factory`, `bari-bsip2-scoring-governance`, `bari-qa-audit`, `bari-frontend-ui`

**Third-party (installed):** `frontend-design`, `web-design-guidelines`, `react-best-practices`, `composition-patterns`, `ui-ux-pro-max`, `find-skills`, `webapp-testing`, `content-research-writer`, `file-document-processing`, `skill-creator`, `marketing/copywriting`, `marketing/marketing-ideas`, `marketing/content-strategy`, `marketing/seo-audit`

**Pending (source required):** Git Worktrees, Superpowers (BLOCKED), Tapestry (BLOCKED)

**MCP Servers (active):** none (Firecrawl removed 2026-06-10 — see `mcp_registry.md`)

**Pending (MCP configuration):** Supermemory (blocked pending data residency policy review)

No new skill is added to any agent's Core or Supporting tier without a named capability gap and Product Agent approval.

---

## Version History

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-05-31 | Initial freeze. 9 agents, 18 skills (14 installed + 4 pending). TASK-049D. |
| v2.0 | 2026-05-31 | Migration to agent-native architecture. 9 dedicated agent definition files. Legacy persona files deprecated. TASK-049E. |
| v2.1 | 2026-05-31 | Firecrawl MCP server installed and activated. `mcp_registry.md` created. TASK-057. |
