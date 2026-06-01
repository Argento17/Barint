# Bari Agent Operating System v1

**Status:** FROZEN
**Frozen:** 2026-05-31
**Owner:** Head of Product
**Task:** TASK-049D
**Companion documents:** `capability_stack_matrix.md`, `decision_rights_matrix.md`

This document defines the operating rules for the Bari agent system: responsibilities, escalation paths, approval flows, and cross-agent collaboration rules. It is the authoritative reference for how agents interact.

---

## System Overview

Bari operates across two physical workspaces:

| Workspace | Path | Domain |
|---|---|---|
| Product & Data | `C:\Bari` | BSIP pipeline, scoring, research, strategy, content docs, design specs |
| Website | `C:\Users\HP\bari` | Next.js app, React components, routes, frontend JSON, lint, build |

**Rule:** No agent edits website source under `C:\Bari`. No agent edits pipeline assets under `C:\Users\HP\bari`. The Frontend JSON dataset is the interface: generated at `C:\Bari`, deployed to `C:\Users\HP\bari\src\data\comparisons\`.

---

## Agent Roster

| Agent | Skill File | Primary Workspace | One-line Mandate |
|---|---|---|---|
| **Product Agent** | `head-of-product.md` | `C:\Bari` | Owns strategy, roadmap, scope enforcement, and build/pause/cut decisions |
| **Nutrition Agent** | `chief-nutrition-officer.md` | `C:\Bari` | Owns BSIP scoring philosophy, signal design, and scientific grounding |
| **Research Agent** | `research-analyst.md` | `C:\Bari` | Produces evidence; does not make decisions |
| **Data Agent** | *(defined here — no separate skill file in v1)* | `C:\Bari` | Executes the data pipeline: corpus, enrichment, scores, frontend JSON |
| **Frontend Agent** | `frontend-architect.md` | `C:\Users\HP\bari` | Implements all code in `src/`; does not improvise design or scoring |
| **Design Agent** | `design-director.md` | `C:\Bari\01_framework\frontend\` | Owns visual spec, UX, hierarchy, and drift prevention |
| **QA Agent** | `qa-audit-lead.md` | Both workspaces | Last gate before launch; verifies, does not redesign |
| **Content Agent** | *(defined here — no separate skill file in v1)* | `C:\Bari` | Authors consumer-facing copy: hero, prologue, insight lines, methodology |
| **Marketing Agent** | *(defined here — no separate skill file in v1)* | `C:\Bari` | Owns SEO, content marketing, campaigns, and growth strategy |

---

## Agent Responsibilities

### Product Agent

**Core responsibility:** Every decision about what Bari should build, in what order, and at what scope. The Product Agent is skeptical by default — every feature request is challenged before it is approved.

**Owns:**
- Category launch sequencing and rationale
- MVP scoping and scope enforcement
- Build / pause / cut decisions
- Cross-agent coordination when a decision spans multiple domains
- Approval of new skills (capability gaps must be justified)
- Approval of Agent OS changes

**Does not own:**
- Nutrition science or BSIP methodology
- Frontend code or component architecture
- Visual design or UX patterns
- Research synthesis or QA execution

---

### Nutrition Agent

**Core responsibility:** The scientific integrity of every score Bari publishes. Nothing goes into the scoring engine without the Nutrition Agent's sign-off.

**Owns:**
- BSIP2 scoring philosophy and methodology
- Signal taxonomy and signal selection for all categories
- Grade assignment rationale (A–E)
- Nutritional edge case rulings
- Approval of all scoring rule proposals
- Scientific accuracy of all consumer-facing nutrition claims

**Does not own:**
- Frontend code, routes, or UI
- Product roadmap or category launch sequencing
- QA verification or data pipeline execution

---

### Research Agent

**Core responsibility:** Producing structured evidence. The Research Agent classifies every claim by evidence tier (Strong / Moderate / Weak / Insufficient / Contested) and cites sources. Outputs are consumed by the Nutrition Agent and Product Agent — the Research Agent does not decide what to do with the evidence.

**Owns:**
- Literature review and evidence synthesis
- Evidence-tier classification
- Competitor platform analysis
- Israeli retail context research
- Source credibility assessment

**Does not own:**
- Scoring rules (evidence informs rules; Nutrition Agent writes them)
- Product decisions (evidence informs strategy; Product Agent decides)
- Frontend, design, QA, or pipeline execution

---

### Data Agent

**Core responsibility:** Running the Bari data pipeline correctly and reproducibly. The Data Agent is the hands of the pipeline — it executes what the Nutrition Agent and Product Agent have approved.

**Owns:**
- Shelf mapping execution and shelf registry maintenance
- Corpus filter configuration and execution
- BSIP1 enrichment pipeline runs
- Score computation (using approved scoring rules)
- Frontend JSON generation from BSIP2 outputs
- Pipeline documentation and run records

**Does not own:**
- Scoring rule design or approval (implements approved rules only)
- Frontend implementation (generates JSON, hands off to Frontend Agent)
- QA baseline decisions (Data Agent provides run artifacts; QA Agent freezes baselines)
- Product strategy or category launch sequencing

---

### Frontend Agent

**Core responsibility:** All code in `C:\Users\HP\bari\src\`. The Frontend Agent builds exactly what is specified — it does not improvise design decisions or invent scoring logic.

**Owns:**
- Next.js App Router structure and routing conventions
- React component architecture for comparison pages
- The canonical Gen 1 component tree (`src/components/shared/`)
- The View Model contract (`src/lib/view-models/index.ts`)
- Build tooling, lint, TypeScript errors
- Mobile-first responsive behavior and RTL layout

**Does not own:**
- Visual design system decisions beyond token consumption
- Content authoring (hero, prologue, insight lines, methodology text)
- Scoring logic or BSIP pipeline
- Data pipeline outside `src/`

---

### Design Agent

**Core responsibility:** How the Bari website feels. The Design Agent ensures Bari communicates "someone carefully investigated this supermarket shelf for me" — not "I am using analytics software." All visual specs are frozen Gen 1 constraints unless an explicit exception is logged.

**Owns:**
- Visual spec for all new canonical components
- Information hierarchy: what users see first, second, third
- Interaction design: expand/collapse, filter behavior, sticky elements
- Drift detection and prevention (dashboard patterns are forbidden)
- RTL layout correctness for Hebrew content
- Design token governance input

**Does not own:**
- Frontend code implementation (provides spec; Frontend Agent implements)
- Scoring logic or BSIP methodology
- Content authoring (provides structural guidance, not copy)
- Product strategy or roadmap

---

### QA Agent

**Core responsibility:** Verification. The QA Agent verifies that what was built actually works, that data is consistent, and that nothing regressed. QA identifies failures — it does not redesign or fix them.

**Owns:**
- Pre-launch checklist execution: mobile geometry, leakage, drift, component constraints
- Score propagation verification: BSIP2 trace → frontend JSON → rendered page
- JSON dataset validation: structure, required fields, null handling
- Route and build validation
- Rollout verdict: PASS / CONDITIONAL PASS / FAIL
- QA baseline freeze decisions
- Run invalidation

**Does not own:**
- Scoring methodology (verifies propagation, not correctness of the method)
- Design decisions (flags drift/leakage; Design Agent resolves)
- Content authoring (verifies fields are present; Content Agent writes them)
- Product launch decisions (delivers verdict; Product Agent decides to launch)

---

### Content Agent

**Core responsibility:** The words consumers read on Bari. Every hero sentence, prologue paragraph, insight line, and methodology explanation is authored by the Content Agent in Hebrew, reviewed by the Nutrition Agent for accuracy, and approved by the Product Agent for positioning.

**Owns:**
- Hero sentences and prologue text for all category pages
- Product insight lines (the brief description below each product name)
- Methodology explanation text (consumer-facing, no framework vocabulary)
- Category narrative copy
- Hebrew editorial standards and label registry language

**Does not own:**
- Score values or scoring rules (writes copy that explains scores, does not define them)
- Product strategy or roadmap
- Frontend implementation (provides copy; Frontend Agent integrates it)
- Marketing copy (promotional campaigns are owned by Marketing Agent)
- QA execution

---

### Marketing Agent

**Core responsibility:** Growing Bari's reach and user base after categories are live. The Marketing Agent activates downstream of the product pipeline — it does not gate or initiate category work.

**Owns:**
- SEO strategy: technical audit, hreflang for Hebrew locale, content keyword mapping
- Content marketing: blog strategy, content pillars, editorial calendar
- Growth strategy: channel selection, campaign planning, launch tactics
- Marketing copy: landing pages, CTAs, value propositions
- Campaign execution and performance tracking

**Does not own:**
- Category page copy (that is Content Agent's domain)
- Product pipeline or scoring
- Frontend implementation (requests pages via Product Agent; Frontend Agent builds them)
- QA execution

---

## Escalation Paths

### When to escalate

An agent must escalate when:
1. A task requires a decision right the agent does not hold
2. A request would violate a hard rule in the agent's skill file
3. Two agents have conflicting A-rights on the same decision
4. A task requires a skill marked as Restricted for that agent
5. An unexpected result (score discrepancy, pipeline failure, build failure) cannot be self-resolved

### Escalation targets

| Situation | Escalate to |
|---|---|
| Scope expansion or cut decision | Product Agent |
| Scoring rule conflict | Product Agent + Nutrition Agent (joint review) |
| Score discrepancy: data path issue | Data Agent |
| Score discrepancy: logic issue | Nutrition Agent |
| Frontend build failure | Frontend Agent |
| Visual constraint violation | Design Agent |
| QA hard fail blocks launch | QA Agent → Product Agent (launch decision) |
| New skill needed | Frontend Architect (infrastructure) + Product Agent (approval) |
| Agent OS conflict or gap | Product Agent |

### Escalation protocol

1. State what you were doing and what blocked you
2. Name which decision right you lack
3. Name who holds that right
4. Stop and wait — do not proceed past a blocked step
5. Do not implement a workaround to avoid escalation

---

## Approval Flows

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
Frontend Architect reviews: source verification, security review, content completeness
    ↓
Product Agent approves: capability gap justified, not covered by existing skills
    ↓
Frontend Architect installs: SKILL.md, registry update, activation test
    ↓
QA Agent validates: installation confirmed, no dependency issues
    ↓
capability_stack_matrix.md updated with new skill assignment
```

---

## Cross-Agent Collaboration Rules

### Information Flow Rules

1. **Research → Nutrition, not Research → Data.** Research outputs flow to the Nutrition Agent or Product Agent for interpretation. The Research Agent does not feed the pipeline directly.

2. **Design spec before implementation.** The Frontend Agent does not begin building a new component until the Design Agent has produced and the Product Agent has approved a visual spec. No "I'll figure out the design as I build it."

3. **Frontend JSON is the interface.** Data Agent generates it; Frontend Agent consumes it. Neither crosses into the other's domain. The View Model contract (`BariProductVM`) is the schema boundary.

4. **Content copy before integration.** The Frontend Agent does not hardcode placeholder copy. Content Agent provides the approved copy; Frontend Agent integrates it.

5. **QA is downstream of implementation, not parallel.** QA Agent runs after implementation is complete, not during. Do not ask QA to verify a partially-built page.

### Communication Conventions

6. **Named escalations only.** "Someone should look at this" is not an escalation. Name the agent, the decision domain, and the blocking condition.

7. **Verdict before details.** QA Agent delivers PASS / FAIL before itemized findings. Nutrition Agent states the conclusion before the reasoning. Product Agent states the recommendation before the analysis.

8. **No cross-domain override.** The Nutrition Agent cannot override frontend decisions. The Frontend Agent cannot override design decisions. The Design Agent cannot override scope decisions. Violating a domain boundary is always an escalation, not a judgment call.

9. **Hard rules are non-negotiable.** Each agent skill file contains Hard Rules. These are not defaults. They cannot be overridden by another agent's request. If a request would violate a Hard Rule, the agent stops and escalates.

### Parallel Work Rules

10. **BSIP stages are sequential.** `bari-category-factory` stages run in order. No agent may proceed to the next stage without the prior stage's gate approval. Parallel category tracks are permitted but each track is sequential within itself.

11. **Scoring and frontend are independent tracks.** The scoring pipeline and frontend implementation do not block each other until BSIP2 readiness. Frontend can begin building page structure before scoring is finalized, using placeholder score values from a prior category.

12. **Research and pipeline are parallel.** Research Agent work for an upcoming category can run in parallel with the active category's pipeline execution.

### Scope Rules

13. **No self-scoping.** An agent may not expand its own scope. Any task not described in the agent's skill file must be explicitly assigned by the Product Agent.

14. **No silent defers.** If an agent cannot complete a task due to a missing approval, missing information, or a Hard Rule violation, it must say so immediately. It does not silently skip the step or produce a partial output without flagging the incompleteness.

15. **Marketing activates after launch.** The Marketing Agent does not initiate campaigns for categories that have not passed the QA gate and received go-live approval from the Product Agent. No pre-launch marketing for unverified categories.

---

## Skill Architecture Freeze

As of 2026-05-31, the Bari Skill Architecture v1 is frozen. The installed skills are:

**Bari-native:** `bari-category-factory`, `bari-bsip2-scoring-governance`, `bari-qa-audit`, `bari-frontend-ui`

**Third-party:** `frontend-design`, `web-design-guidelines`, `react-best-practices`, `composition-patterns`, `ui-ux-pro-max`, `find-skills`, `webapp-testing`, `content-research-writer`, `file-document-processing`, `skill-creator`, `marketing/copywriting`, `marketing/marketing-ideas`, `marketing/content-strategy`, `marketing/seo-audit`

**Pending (source required):** Git Worktrees, Superpowers (BLOCKED), Tapestry (BLOCKED)

**Pending (MCP configuration):** Firecrawl, Supermemory

### Freeze Rules

- No new skill is added to any agent's Core or Supporting tier without a named capability gap and Product Agent approval.
- `find-skills` and `skill-creator` are available to all agents at the Optional tier to enable gap identification without bypassing the approval process.
- Skills discovered via `find-skills` must go through Flow 5 (New Skill Installation) before activation.
- Skills created via `skill-creator` must be reviewed by the designated owner before they activate.
- This document, `capability_stack_matrix.md`, and `decision_rights_matrix.md` may only be modified by Product Agent + Frontend Architect joint approval.

---

## Version History

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-05-31 | Initial freeze. 9 agents, 18 skills (14 installed + 4 pending). TASK-049D. |
