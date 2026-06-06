# Agent Coverage Map v1

**Status:** Authoritative · **Effective:** 2026-06-04  
**Maintained by:** CC Agent (update on every agent addition/removal/lane change)  
**Validator:** `05_command_center/validate_agents.py`

---

## Purpose

Answers two questions at a glance:
1. **What domains does the agent fleet cover?** (no silent gaps)
2. **For ambiguous queries, which agent owns the call?** (no phantom routing)

---

## Domain → Owner map

| Domain | Primary Agent | Secondary (escalation) | Gap? |
|---|---|---|---|
| Product strategy, MVP scoping, roadmap, build/pause/cut | `product-agent` | — | COVERED |
| Nutrition logic, BSIP scoring philosophy, category science | `nutrition-agent` | — | COVERED |
| Research, literature, evidence synthesis, competitor analysis | `research-agent` | — | COVERED |
| Data pipeline: BSIP0/1/2 execution, corpus, JSON generation | `data-agent` | — | COVERED |
| Frontend implementation: Next.js, React, routes, components | `frontend-agent` | — | COVERED |
| UX, visual hierarchy, information architecture, design | `design-agent` | — | COVERED |
| QA: score propagation, regression, build verification, launch gate | `qa-agent` | — | COVERED |
| Consumer copy, Hebrew editorial, category page content | `content-agent` | — | COVERED |
| Marketing, SEO, growth, content strategy | `marketing-agent` | — | COVERED |
| Registry health, task lifecycle, dashboard, closing authority | `cc-agent` | — | COVERED |
| Independent challenge, adversarial review, red-team scoring | `red-team-agent` | — | COVERED |

---

## Routing disambiguation — ambiguous-query resolution table

Some queries match multiple agents. This table is the tiebreaker.

| Query pattern | Routes to | Not to | Reason |
|---|---|---|---|
| "is the score correct?" | `qa-agent` | `nutrition-agent` | QA verifies propagation; Nutrition owns philosophy |
| "should we change the scoring rule?" | `nutrition-agent` + `product-agent` (D7 co-sign) | `data-agent` | Rule proposals = Nutrition; approval = both |
| "implement the scoring rule change" | `data-agent` | `nutrition-agent` | Implementation after co-sign |
| "is the comparison page layout right?" | `design-agent` | `frontend-agent` | Design owns UX decisions; Frontend implements |
| "fix the layout bug" | `frontend-agent` | `design-agent` | Frontend owns implementation |
| "write the insight line for product X" | `content-agent` | `nutrition-agent` | Content authors; Nutrition science-checks on request |
| "is the insight line scientifically accurate?" | `nutrition-agent` | `content-agent` | Science review = Nutrition |
| "what categories should we launch next?" | `product-agent` | `research-agent` | Sequencing = Product; research informs, not decides |
| "what does the evidence say about X ingredient?" | `research-agent` | `nutrition-agent` | Evidence gathering = Research; interpretation = Nutrition |
| "challenge this score / stress-test this category" | `red-team-agent` | `qa-agent` | Adversarial challenge = Red-team; pass/fail verification = QA |
| "are we on track?" / "what's left?" | `cc-agent` | `product-agent` | Registry map = CC; roadmap decisions = Product |
| "close this task" | `cc-agent` | any other | Closing authority is CC-only |
| "what are the SEO implications?" | `marketing-agent` | `content-agent` | SEO strategy = Marketing; Hebrew copy = Content |

---

## Uncovered domains (known gaps)

| Domain | Gap type | Proposed resolution |
|---|---|---|
| Legal / regulatory review | Intentional (no agent) | Route to owner if a wire-4 tripwire fires |
| External partnerships / vendor eval | Intentional (no agent) | Owner-only decision (wire-4) |
| User research / moderated sessions | Partial — Design handles instrumentation | Owned by owner / external researcher |
| Infrastructure / hosting / DevOps | Not modeled | Route to owner |

---

## Agent fleet health checks

Run `python 05_command_center/validate_agents.py` to verify:
- All required frontmatter fields present (name, description, version, changelog)
- All required body sections present (Mission, Responsibilities, Does Not Own, Hard Rules, Autonomy Mandate, Escalation Rules, Inputs, Outputs)
- No coverage gaps vs. this map

**Validation is advisory in CI, blocking in the CC close-readiness gate for any task that adds or changes an agent.**

---

## Change log

| Date | Change | Author |
|---|---|---|
| 2026-06-04 | v1 created; 11-agent fleet; red-team-agent added; routing disambiguation table | CC Agent |
