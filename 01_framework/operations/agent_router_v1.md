# Agent Router v1 — Dispatch Disambiguation

**Status:** Authoritative · **Effective:** 2026-06-04  
**Maintained by:** CC Agent  
**Coverage map:** `agent_coverage_map_v1.md`

---

## Purpose

The orchestrator dispatches agents via the `Agent` tool using the agent's `description:` frontmatter slug. When a query matches multiple agents, this document is the tiebreaker. It makes routing deterministic — the orchestrator checks this table before spawning rather than relying on prose-match intuition.

---

## Routing rules (ordered — first match wins)

### Rule 1: Keyword triggers (unambiguous)

| If the query contains… | Dispatch to |
|---|---|
| "close this task" / "mark CLOSED" / "registry" / "drift" / "dashboard" | `cc-agent` |
| "score correct?" / "propagation" / "build pass?" / "lint" / "regression check" | `qa-agent` |
| "write copy" / "insight line" / "prologue" / "Hebrew" / "editorial" | `content-agent` |
| "implement" / "component" / "route" / "Next.js" / "bari-web" | `frontend-agent` |
| "layout" / "spacing" / "UX" / "mobile hierarchy" / "design critique" | `design-agent` |
| "run pipeline" / "BSIP0" / "BSIP1" / "BSIP2 run" / "generate JSON" | `data-agent` |
| "scoring rule" / "methodology" / "food science" / "BSIP philosophy" | `nutrition-agent` |
| "evidence" / "literature" / "PubMed" / "competitor" / "market research" | `research-agent` |
| "SEO" / "marketing" / "growth" / "campaign" / "content pillar" | `marketing-agent` |
| "prioritize" / "roadmap" / "MVP" / "build or cut" / "go-live decision" | `product-agent` |
| "challenge" / "stress-test" / "red-team" / "adversarial" | `red-team-agent` |

### Rule 2: Ownership boundary tiebreakers

When Rule 1 fires on two agents, the boundary table resolves it:

| Boundary | Owner | Escalation |
|---|---|---|
| Is the score *value* correct (propagation)? | `qa-agent` | — |
| Is the score *methodology* correct (philosophy)? | `nutrition-agent` | — |
| Should the *rule* change (proposal)? | `nutrition-agent` | — |
| Should the *rule* change (approval)? | `nutrition-agent` + `product-agent` (D7) | — |
| Who *implements* an approved rule? | `data-agent` | — |
| Is the *layout* correct (UX decision)? | `design-agent` | — |
| *Fix* the layout bug? | `frontend-agent` | — |
| *Author* the copy? | `content-agent` | — |
| Is the copy *scientifically accurate*? | `nutrition-agent` | — |
| *Challenge* the entire category? | `red-team-agent` | — |
| Pass/fail *verification* of category? | `qa-agent` | — |

### Rule 3: Multi-domain — split ownership

When a task genuinely spans two domains, split file ownership and dispatch in parallel:

```
PATTERN: [Domain A files] → Agent A  ||  [Domain B files] → Agent B
No agent touches the other's file set. Return blocks separated by owner.
```

Common parallel patterns:
- Score rule change: `nutrition-agent` (rule spec) ‖ `data-agent` (implementation) — sequential, not parallel (Data waits for Nutrition co-sign)
- Category launch: `qa-agent` (QA pass) ‖ `content-agent` (copy) — parallel
- Glass Box wave: `research-agent` (evidence) ‖ `nutrition-agent` (tiers) ‖ `data-agent` (engine) — parallel with clear file boundaries

### Rule 4: Default (no rule matched)

Route to `product-agent` for strategy ambiguity; `cc-agent` for registry ambiguity; `qa-agent` for verification ambiguity.

---

## Versioning policy for agent files

Every change to a `.claude/agents/*.md` file **must** include a `changelog:` entry in the YAML frontmatter with:

```yaml
changelog:
  - version: "X.Y"
    date: "YYYY-MM-DD"
    summary: "One sentence: what changed and why."
```

- Bump minor version (`1.0 → 1.1`) for: added sections, updated hard rules, new skills.
- Bump major version (`1.X → 2.0`) for: lane changes, ownership transfers, new authority grants.
- Run `python 05_command_center/validate_agents.py` after any agent change.
- Open a tracked task (`work_type: coordination`) for any agent file change that shifts decision rights or adds/removes a lane.

---

## Adding a new agent

1. Create `.claude/agents/<slug>.md` from this template:

```markdown
---
name: <Name> Agent
description: <50-150 word dispatch trigger — what it owns and use-case keywords>
version: 1.0
successor-to: <previous-skill.md or "none (agent-native)">
changelog:
  - version: "1.0"
    date: "YYYY-MM-DD"
    summary: "Initial definition."
---

## Mission
## Workspace
## Responsibilities
## Does Not Own
## Decision Rights
## Inputs
## Outputs
## Hard Rules
## Autonomy Mandate
## Escalation Rules
```

2. Add an entry to `agent_coverage_map_v1.md` (Domain → Owner table + coverage gap resolved).
3. Add the slug to `VALID_OWNERS` in `validate_agents.py`.
4. Update the routing disambiguation table if the new agent creates any boundary ambiguity.
5. Run `python validate_agents.py` — must pass clean before the agent is dispatched.

---

## Change log

| Date | Change |
|---|---|
| 2026-06-04 | v1 created — 4-rule router, versioning policy, new-agent checklist |
