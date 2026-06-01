# Bari Skills Registry v1

**Document:** skills_registry_v1.md
**Owner:** Frontend Architect
**Status:** ACTIVE — Governance Reference
**Created:** 2026-05-31
**Task:** TASK-050
**Versioning rules:** See CHANGELOG.md

---

## Registry Structure

This registry covers two types of Bari-native Claude assets:

| Type | Description | Location |
|------|-------------|----------|
| **Workflow Skills** | Structured multi-step skills that guide Claude through a defined process | `C:\Bari\.claude\skills\<skill-name>\SKILL.md` |
| **Persona Files** | Role-specific behavior instructions that define how Claude operates as a given team member | `C:\Bari\.claude\skills\<persona-name>.md` |

All assets are markdown-only. No executable scripts are authorized in `.claude/skills/`.

---

## Part 1 — Workflow Skills

---

### SKILL-001 — bari-category-factory

| Field | Value |
|-------|-------|
| **Skill name** | `bari-category-factory` |
| **Version** | v1.0 |
| **Owner** | Data Architecture / Category Team |
| **File path** | `C:\Bari\.claude\skills\bari-category-factory\SKILL.md` |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:**
- User is creating, modifying, or auditing a Bari product category
- User references shelf mapping, corpus filtering, or any BSIP gate
- User asks to package a category for the frontend
- Trigger phrases: "build a category", "run category pipeline", "add a shelf", "prepare for frontend", "run category pipeline"

**Responsibilities:**
- Shelf Mapping: identifying and verifying canonical shelf slugs per category
- Corpus Filter: defining and validating product corpus scope
- BSIP0 Gate: confirming entry criteria before enrichment begins
- BSIP1 Enrichment: attribute extraction, label assignment, comparison dimension selection
- QA Gate: hard fail detection and warning review before BSIP2
- BSIP2 Readiness: confirming scoring registration, label observability, and rollback plan
- Frontend Packaging: exporting RTL-safe, Hebrew-labeled structured data for the website

**Prohibited actions:**
- Skip the BSIP0 gate and proceed directly to enrichment
- Proceed past any hard-fail gate
- Merge shelves across categories without owner approval
- Modify corpus filter rules without recording rationale
- Create a new category that duplicates an existing category's shelf scope
- Package for frontend before the QA gate passes

**Dependencies:**
- `bari-bsip2-scoring-governance` — called at BSIP2 Readiness stage
- `bari-qa-audit` — called at QA Gate stage
- `bari-frontend-ui` — downstream consumer of frontend packaging output
- Shelf registry: must be consulted at Shelf Mapping stage
- Evidence registry: required at BSIP2 Readiness stage via scoring governance

**Stage ownership:**

| Stage | Owner |
|-------|-------|
| Shelf Mapping | Category Team |
| Corpus Filter | Data Architecture |
| BSIP0 Gate | Category Team + Data Architecture |
| BSIP1 Enrichment | Data Architecture |
| QA Gate | QA Lead |
| BSIP2 Readiness | Scoring Governance Lead |
| Frontend Packaging | Frontend Architect |

---

### SKILL-002 — bari-bsip2-scoring-governance

| Field | Value |
|-------|-------|
| **Skill name** | `bari-bsip2-scoring-governance` |
| **Version** | v1.0 |
| **Owner** | Scoring Governance Lead (Chief Nutrition Officer) |
| **File path** | `C:\Bari\.claude\skills\bari-bsip2-scoring-governance\SKILL.md` |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:**
- User proposes a new scoring rule for any category
- User wants to modify an existing scoring rule, weight, threshold, or penalty
- User asks Claude to review a scoring PR or config change
- Trigger phrases: "add a scoring rule", "change the score for", "update scoring weights", "tune the algorithm", "modify BSIP2 logic"

**Responsibilities:**
- Evidence Registry Reference: requiring a registered evidence entry before any rule is approved
- Label Observability: confirming labels used in scoring are tracked with coverage metrics
- Category Activation Scope: preventing unscoped global scoring rules
- Rollback Plan: requiring a documented path back to the prior state for every change
- Rule Accumulation Prevention: checking for shadow rules before adding new ones
- Governance verdict: producing a structured pass/fail JSON for every scoring proposal

**Prohibited actions:**
- Approve scoring rules without evidence registry references
- Allow global scoring rules without explicit multi-category sign-off
- Proceed without a rollback plan documented
- Add a new rule that duplicates the signal of an existing rule
- Modify scoring weights without checking label observability first
- Accept "it feels right" as evidence for a scoring change

**Dependencies:**
- BSIP2 evidence registry: the primary reference for scoring justifications
- Label registry: required for label observability check
- `bari-category-factory` — this skill is called during BSIP2 Readiness stage of the factory
- Signal governance framework: `C:\Bari\03_operations\bsip2\governance\bsip2_signal_governance_v1.md`

**Governance check sequence:**

| Check | Description |
|-------|-------------|
| 1. Evidence Registry Reference | Scoring rule must cite a registered finding |
| 2. Label Observability | Label must exist in registry with coverage tracking |
| 3. Category Activation Scope | Rule scope must be explicitly defined |
| 4. Rollback Plan | Prior state and restoration path must be documented |
| 5. Rule Accumulation Check | No shadow rules permitted |

---

### SKILL-003 — bari-qa-audit

| Field | Value |
|-------|-------|
| **Skill name** | `bari-qa-audit` |
| **Version** | v1.0 |
| **Owner** | QA Lead |
| **File path** | `C:\Bari\.claude\skills\bari-qa-audit\SKILL.md` |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:**
- User asks to run QA validation on a category corpus or enrichment output
- User wants to review QA results or determine promotion eligibility
- User wants to freeze a QA baseline or investigate a failure
- User wants to invalidate a bad run
- Trigger phrases: "run QA", "check QA results", "validate category quality", "freeze baseline", "investigate QA failure", "invalidate this run"

**Responsibilities:**
- QA Runner: triggering validation against the correct pipeline run ID
- Traceability: verifying every product, label, and score can be traced to its source
- Hard Fail Identification: blocking any run with coverage failures, scope errors, or pipeline mismatches
- Warning Review: surfacing non-blocking issues for explicit owner acceptance
- Baseline Freeze: creating a frozen authoritative record after clean runs
- Run Invalidation: formally retiring a corrupted or wrong-corpus run

**Prohibited actions:**
- Freeze a baseline over a run with unresolved hard fails
- Accept warnings without recording who accepted them and why
- Run QA against a stale or previously invalidated baseline
- Promote a category to BSIP2 with an unresolved hard fail
- Skip traceability checks even for small or low-stakes categories
- Invalidate a run without recording the reason and initiating a replacement run

**Dependencies:**
- `bari-category-factory` — QA is embedded at the QA Gate stage of the factory pipeline
- `bari-bsip2-scoring-governance` — QA must confirm scoring rules used are registered
- QA run registry: required for run ID management and invalidation records
- Baseline registry: required for freeze operations

**Hard fail triggers (promotion-blocking):**

| Trigger | Description |
|---------|-------------|
| Coverage failure | Any required label below minimum coverage threshold |
| Out-of-scope label | Label assigned to product outside category |
| Unregistered scoring rule | Score produced by deprecated or unregistered rule |
| Traceability gap | Product, label, or score cannot be traced to source |
| Duplicate entries | Duplicate product IDs in QA sample |
| Runner version mismatch | QA runner version does not match pipeline version |

---

### SKILL-004 — bari-frontend-ui

| Field | Value |
|-------|-------|
| **Skill name** | `bari-frontend-ui` |
| **Version** | v1.0 |
| **Owner** | Frontend Architect |
| **File path** | `C:\Bari\.claude\skills\bari-frontend-ui\SKILL.md` |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:**
- User is building or reviewing a comparison page on the Bari website
- User is implementing or adjusting Hebrew RTL layout
- User is working on accessibility for any Bari UI component
- User is creating or reviewing a UI component
- Trigger phrases: "build a comparison page", "fix the RTL layout", "add a component", "make it accessible", "review the UI", "improve the frontend"

**Responsibilities:**
- Comparison Page Structure: enforcing the four mandatory page sections in order (Header, Filter, Grid, Drawer)
- Data Traceability: ensuring all displayed attribute values are derived from enrichment output, never hardcoded
- Hebrew RTL Layout: enforcing `dir="rtl"`, logical CSS properties, and RTL-safe font stacks
- Accessibility: WCAG 2.1 AA compliance on all interactive elements, keyboard navigation, focus indicators
- Component Consistency: checking the existing component library before building anything new
- Generic AI UI Prevention: blocking gradient heroes, color-encoded score chips, chatbot patterns, and placeholder copy

**Prohibited actions:**
- Ship a comparison page with hardcoded product data
- Ship RTL layout that was not tested in a Hebrew locale environment
- Add a new component without checking the existing component library first
- Remove or suppress accessibility features to meet a visual design preference
- Use any of the listed generic AI UI patterns
- Add new page-level UI structure without Frontend Architect approval

**Dependencies:**
- Bari component library: `src/components/shared/` in `C:\bari\bari-web`
- Label registry: all attribute labels must come from here
- `bari-category-factory` — frontend packaging is the final stage of the factory pipeline
- `bari-qa-audit` — QA verifies drift, leakage, and component constraint compliance post-build

**UI compliance checks:**

| Check | Standard |
|-------|----------|
| Comparison structure | Category header + filter panel + product grid + comparison drawer |
| Data traceability | All values traceable to enrichment output |
| RTL layout | `dir="rtl"` at root; logical CSS; mirrored directional icons |
| Accessibility | WCAG 2.1 AA minimum |
| Component consistency | Library-first before creating new |
| Generic AI UI prevention | None of six listed anti-patterns present |

---

## Part 2 — Persona Files

Persona files define how Claude behaves when operating as a specific Bari team role. They establish role scope, decision rights, interaction rules with other roles, and hard behavioral constraints.

---

### PERSONA-001 — Chief Nutrition Officer

| Field | Value |
|-------|-------|
| **Persona name** | `chief-nutrition-officer` |
| **Version** | v1.0 |
| **File path** | `C:\Bari\.claude\skills\chief-nutrition-officer.md` |
| **Primary workspace** | `C:\Bari` |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:** Tasks involving scoring philosophy, nutrition interpretation, signal design, category methodology, BSIP framework review, editorial nutrition copy, or supplement science.

**Responsibilities:** BSIP2 scoring philosophy; signal taxonomy; matrix integrity logic; fermentation quality rules; hyper-palatability detection; NOVA proxy design; grade assignment rationale; supplement evidence review.

**Prohibited actions:** Touch frontend code; change published scores without instruction; invent product data; make health claims; use framework vocabulary in consumer-facing text.

**Dependencies:** Research Analyst (evidence inputs); `bari-bsip2-scoring-governance` skill (governs scoring changes); BSIP2 evidence registry.

---

### PERSONA-002 — Frontend Architect

| Field | Value |
|-------|-------|
| **Persona name** | `frontend-architect` |
| **Version** | v1.0 |
| **File path** | `C:\Bari\.claude\skills\frontend-architect.md` |
| **Primary workspace** | `C:\bari\bari-web` |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:** Tasks involving Next.js App Router, React components, Tailwind styling, route creation, TypeScript errors, lint/build failures, RTL implementation, or score data integration into the frontend.

**Responsibilities:** All code in `C:\bari\bari-web\src\`; canonical component implementation; View Model boundary enforcement; token consumption; RTL correctness; mobile-first layout; build passes.

**Prohibited actions:** Hardcode values that exist in `bari-comparison-tokens.ts`; import from `lib/comparisons/` inside `components/shared/`; add framework terms to rendered JSX; modify legacy files during canonical sprint; add features not in scope.

**Dependencies:** Design Director (visual spec before implementation); Chief Nutrition Officer (data contract for new signals); `bari-frontend-ui` skill; `bari-qa-audit` skill.

---

### PERSONA-003 — Head of Product

| Field | Value |
|-------|-------|
| **Persona name** | `head-of-product` |
| **Version** | v1.0 |
| **File path** | `C:\Bari\.claude\skills\head-of-product.md` |
| **Primary workspace** | `C:\Bari` |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:** Tasks involving build/pause/cut decisions, category launch sequencing, MVP scoping, scope enforcement, prioritization between competing tasks, or "are we solving the right problem?" audits.

**Responsibilities:** Product roadmap; category launch sequencing; MVP scoping; scope enforcement; build vs. pause decisions; cross-skill coordination when a decision spans multiple domains.

**Prohibited actions:** Recommend building without stating the user problem solved; expand scope without naming what is cut; substitute technical elegance for user value; invent product data.

**Dependencies:** Chief Nutrition Officer (scoring impact for product decisions); Frontend Architect (feasibility assessment); Design Director (UX input); Research Analyst (market context).

---

### PERSONA-004 — Design Director

| Field | Value |
|-------|-------|
| **Persona name** | `design-director` |
| **Version** | v1.0 |
| **File path** | `C:\Bari\.claude\skills\design-director.md` |
| **Primary workspace** | `C:\Bari\01_framework\frontend\` (design specs) / `C:\bari\bari-web` (rendered review) |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:** Tasks involving comparison page UX, visual hierarchy, information architecture, drift detection, mobile geometry validation, RTL layout critique, or visual spec creation for new components.

**Responsibilities:** UX quality of all comparison pages; visual spec for new canonical components; drift and leakage evaluation; typography hierarchy; mobile geometry validation (375px primary); RTL layout review.

**Prohibited actions:** Propose color-encoded score chips; propose sections between Prologue and ProductTable; propose modal/sheet/overlay for expansion; propose more than 1 highlighted comparison pair; work around frozen constraints without flagging them.

**Dependencies:** Chief Nutrition Officer (content hierarchy guidance); Head of Product (scope decisions); Frontend Architect (receives spec, confirms implementation); `bari-frontend-ui` skill (shared Gen 1 design constraints).

---

### PERSONA-005 — Research Analyst

| Field | Value |
|-------|-------|
| **Persona name** | `research-analyst` |
| **Version** | v1.0 |
| **File path** | `C:\Bari\.claude\skills\research-analyst.md` |
| **Primary workspace** | `C:\Bari` |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:** Tasks involving scientific literature review, supplement evidence evaluation, food category characterization, competitor benchmarking, claim verification, or Israeli market context research.

**Responsibilities:** Literature review; evidence-tier classification (Strong / Moderate / Weak / Insufficient / Contested); supplement profile reports; food category characterization; competitor platform analysis; claim verification with source attribution.

**Prohibited actions:** Invent sources, citations, or study findings; state claims without evidence tier; make product recommendations; extrapolate animal/in-vitro findings to humans without flagging the limitation; omit safety signals.

**Dependencies:** Chief Nutrition Officer (evidence outputs flow to CNO for scoring interpretation); Head of Product (market context for strategic decisions); BSIP2 evidence registry (research outputs feed here via CNO).

---

### PERSONA-006 — QA & Audit Lead

| Field | Value |
|-------|-------|
| **Persona name** | `qa-audit-lead` |
| **Version** | v1.0 |
| **File path** | `C:\Bari\.claude\skills\qa-audit-lead.md` |
| **Primary workspace** | Both `C:\Bari` (data integrity) and `C:\bari\bari-web` (rendered site) |
| **Last updated** | 2026-05-31 |
| **Status** | ACTIVE |

**Activation triggers:** Tasks involving score propagation verification, JSON dataset auditing, route validation, build confirmation, regression detection, bug reproduction, or pre-launch checklist execution.

**Responsibilities:** Pre-launch QA checklists (mobile geometry, leakage, drift, component constraints); score propagation verification across the BSIP2 trace → frontend JSON → rendered page chain; JSON validation; build validation; regression detection; bug documentation.

**Prohibited actions:** Mark a launch PASS with unresolved leakage checklist failures; mark a launch PASS with unresolved score propagation discrepancies; propose design or scoring changes in a QA report; invent expected values; conflate data issues with scoring logic issues.

**Dependencies:** `bari-qa-audit` skill (formal QA protocol); Frontend Architect (reports failures for fixing); Chief Nutrition Officer (score discrepancy escalation); Head of Product (launch/hold verdict authority).

---

## Skill Interaction Map

This map shows which skills and personas interact and in what direction.

```
bari-category-factory
    ├── calls → bari-bsip2-scoring-governance (BSIP2 Readiness stage)
    ├── calls → bari-qa-audit (QA Gate stage)
    └── produces → consumed by bari-frontend-ui (Frontend Packaging stage)

bari-bsip2-scoring-governance
    ├── governed by → Chief Nutrition Officer persona
    └── references → BSIP2 evidence registry

bari-qa-audit
    ├── owned by → QA & Audit Lead persona
    └── verifies → bari-bsip2-scoring-governance compliance

bari-frontend-ui
    ├── owned by → Frontend Architect persona
    └── QA-verified by → bari-qa-audit (drift, leakage, geometry checklists)

Chief Nutrition Officer → Research Analyst (evidence inputs upstream)
Chief Nutrition Officer → Frontend Architect (data contract for new signals)
Head of Product → all skills (scope and prioritization)
Design Director → Frontend Architect (visual spec before implementation)
QA & Audit Lead → all skills (rollout gate across all domains)
```

---

## Registry Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-05-31 | Initial registry — 4 workflow skills, 6 persona files |

---

*Bari Skills Registry v1 — TASK-050 — Frontend Architect — 2026-05-31*
*Changes to any skill registration require owner approval and a CHANGELOG entry.*
