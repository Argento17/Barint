# Bari Agent Capability Stack Matrix v1

**Status:** FROZEN — Skill Architecture v1
**Frozen:** 2026-05-31
**Owner:** Frontend Architect (infrastructure), Head of Product (architecture governance)
**Task:** TASK-049D

This matrix defines the authoritative skill stack for each Bari agent. Skill assignments are frozen. A skill may not be added to an agent's stack without identifying a named capability gap and obtaining Head of Product approval.

---

## Legend

| Tier | Meaning |
|---|---|
| **Core** | Always loaded for this agent; governs default behavior on every task |
| **Supporting** | Available and expected on relevant tasks; not always active |
| **Optional** | Available situationally; agent may invoke at discretion |
| **Restricted** | Explicitly off-limits; agent must not invoke these skills |

---

## Skill Reference Index

### Bari-Native Skills
| Skill ID | Name | Owner |
|---|---|---|
| `B1` | `bari-category-factory` | Data Agent |
| `B2` | `bari-bsip2-scoring-governance` | Nutrition Agent |
| `B3` | `bari-qa-audit` | QA Agent |
| `B4` | `bari-frontend-ui` | Frontend Agent |

### Third-Party Skills
| Skill ID | Name | Source |
|---|---|---|
| `T1` | `frontend-design` | anthropics/skills |
| `T2` | `web-design-guidelines` | vercel-labs/agent-skills |
| `T3` | `react-best-practices` | vercel-labs/agent-skills |
| `T4` | `composition-patterns` | vercel-labs/agent-skills |
| `T5` | `ui-ux-pro-max` | nextlevelbuilder |
| `T6` | `find-skills` | vercel-labs/skills |
| `T7` | `webapp-testing` | AutumnsGrove/ClaudeSkills |
| `T8` | `content-research-writer` | ComposioHQ |
| `T9` | `file-document-processing` | ComposioHQ |
| `T10` | `skill-creator` | anthropics/claude-code |
| `T11` | `marketing/copywriting` | coreyhaines31/marketingskills |
| `T12` | `marketing/marketing-ideas` | coreyhaines31/marketingskills |
| `T13` | `marketing/content-strategy` | coreyhaines31/marketingskills |
| `T14` | `marketing/seo-audit` | coreyhaines31/marketingskills |

---

## 1. Product Agent

**Maps to:** Head of Product (`head-of-product.md`)
**Primary workspace:** `C:\Bari` (strategy, roadmap, rollout docs)
**Mandate:** Owns product strategy, category sequencing, scope enforcement, and build/pause/cut decisions.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `B1` bari-category-factory | Pipeline gating — Product Agent controls category launch decisions at each BSIP stage |
| **Core** | `B2` bari-bsip2-scoring-governance | Final approval authority on scoring rule changes |
| **Supporting** | `T12` marketing-ideas | Informs growth strategy per category |
| **Supporting** | `T13` content-strategy | Aligns content planning with roadmap |
| **Supporting** | `T8` content-research-writer | Strategic briefs and initiative documentation |
| **Optional** | `T6` find-skills | Discovering capability gaps in the skill stack |
| **Optional** | `T10` skill-creator | Encoding new product workflows as skills |
| **Restricted** | `B3` bari-qa-audit | QA Agent owns execution; Product Agent receives verdict, does not run QA |
| **Restricted** | `B4` bari-frontend-ui | No frontend implementation |
| **Restricted** | `T3` react-best-practices | No frontend implementation |
| **Restricted** | `T4` composition-patterns | No frontend implementation |
| **Restricted** | `T7` webapp-testing | No test execution |

---

## 2. Nutrition Agent

**Maps to:** Chief Nutrition Officer (`chief-nutrition-officer.md`)
**Primary workspace:** `C:\Bari` (scoring docs, BSIP assets, nutrition research)
**Mandate:** Owns BSIP scoring philosophy, signal design, grade assignment, and scientific grounding of all nutrition claims.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `B2` bari-bsip2-scoring-governance | Authority on all scoring rule proposals and modifications |
| **Supporting** | `T8` content-research-writer | Literature-backed scoring rationale docs; nutrition editorial review |
| **Supporting** | `T9` file-document-processing | Processing product spec sheets and nutrition data PDFs |
| **Optional** | `T6` find-skills | Discovering research-oriented skills |
| **Optional** | `T10` skill-creator | Encoding new scoring workflows as skills |
| **Restricted** | `B4` bari-frontend-ui | No frontend work |
| **Restricted** | `T1` frontend-design | No UI design |
| **Restricted** | `T2` web-design-guidelines | No UI review |
| **Restricted** | `T3` react-best-practices | No frontend implementation |
| **Restricted** | `T4` composition-patterns | No frontend implementation |
| **Restricted** | `T7` webapp-testing | No test execution |
| **Restricted** | `T11` marketing/copywriting | No marketing copy (editorial only via Content Agent) |
| **Restricted** | `T12` marketing/marketing-ideas | No marketing strategy |

---

## 3. Research Agent

**Maps to:** Research Analyst (`research-analyst.md`)
**Primary workspace:** `C:\Bari` (evidence summaries, category research, competitor analysis)
**Mandate:** Gathers evidence, evaluates sources, and produces structured research outputs. Produces evidence; does not make decisions.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `T8` content-research-writer | Primary output tool: literature review, evidence synthesis, category characterization |
| **Core** | `T9` file-document-processing | Ingesting research PDFs, spec sheets, and data exports |
| **Supporting** | `T13` content-strategy | Mapping research outputs to content opportunities |
| **Supporting** | `T14` marketing/seo-audit | Competitive SEO analysis in support of market research |
| **Optional** | `T6` find-skills | Discovering research-domain skills |
| **Optional** | `T10` skill-creator | Encoding research workflows |
| **Restricted** | `B1` bari-category-factory | No pipeline execution — research feeds Data Agent |
| **Restricted** | `B2` bari-bsip2-scoring-governance | Can surface evidence; cannot approve scoring rules |
| **Restricted** | `B4` bari-frontend-ui | No frontend work |
| **Restricted** | `T3` react-best-practices | No frontend implementation |
| **Restricted** | `T7` webapp-testing | No test execution |
| **Restricted** | `T11` marketing/copywriting | No marketing copy |
| **Restricted** | `T12` marketing/marketing-ideas | No growth strategy |

---

## 4. Data Agent

**Maps to:** Data Architecture / Category Team (no existing agent skill file — defined here)
**Primary workspace:** `C:\Bari` (Python pipelines, BSIP runners, generated JSON, corpus management)
**Mandate:** Executes the BSIP data pipeline: shelf mapping, corpus filtering, enrichment runs, score computation, and frontend JSON generation. Does not approve scoring rules; implements approved ones.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `B1` bari-category-factory | Pipeline execution authority — runs all 7 stages |
| **Core** | `T9` file-document-processing | Processing raw product data from PDFs, CSVs, exports |
| **Supporting** | `B3` bari-qa-audit | Data-side QA: traceability, corpus integrity, baseline management |
| **Supporting** | `T8` content-research-writer | Documenting pipeline decisions and corpus rationale |
| **Optional** | `T6` find-skills | Discovering data-processing skills |
| **Optional** | `T10` skill-creator | Encoding new pipeline stages as skills |
| **Restricted** | `B2` bari-bsip2-scoring-governance | Implements approved rules; cannot approve new rules |
| **Restricted** | `B4` bari-frontend-ui | No frontend work — generates JSON, hands off to Frontend Agent |
| **Restricted** | `T1` frontend-design | No UI design |
| **Restricted** | `T3` react-best-practices | No frontend implementation |
| **Restricted** | `T7` webapp-testing | No browser-based testing |
| **Restricted** | `T11` marketing/copywriting | No marketing |
| **Restricted** | `T12` marketing/marketing-ideas | No marketing |
| **Restricted** | `T13` content-strategy | No content strategy |
| **Restricted** | `T14` marketing/seo-audit | No SEO |

---

## 5. Frontend Agent

**Maps to:** Frontend Architect (`frontend-architect.md`)
**Primary workspace:** `C:\Users\HP\bari` (Next.js app, React components, routes, lint, build)
**Mandate:** Owns all code in `C:\Users\HP\bari\src\`. Implements specified components and pages. Does not improvise design or invent scoring logic.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `B4` bari-frontend-ui | Bari-specific frontend rules: comparison pages, RTL, accessibility, component registry |
| **Core** | `T3` react-best-practices | 70-rule performance guide for every React/Next.js task |
| **Core** | `T4` composition-patterns | Component API design — prevents boolean prop accumulation |
| **Core** | `T7` webapp-testing | E2E test coverage for every frontend change |
| **Supporting** | `T1` frontend-design | Aesthetic direction for distinctive UI (anti-generic-AI) |
| **Supporting** | `T2` web-design-guidelines | UI review against Vercel Web Interface Guidelines |
| **Optional** | `T5` ui-ux-pro-max | Deep UX/accessibility audit when requested |
| **Optional** | `T6` find-skills | Discovering frontend-domain skills |
| **Optional** | `T10` skill-creator | Encoding new frontend workflows |
| **Restricted** | `B1` bari-category-factory | No pipeline execution — receives frontend JSON, does not generate it |
| **Restricted** | `B2` bari-bsip2-scoring-governance | No scoring logic |
| **Restricted** | `B3` bari-qa-audit | QA Agent runs data-side QA; Frontend Agent fixes issues QA surfaces |
| **Restricted** | `T11` marketing/copywriting | No marketing copy |
| **Restricted** | `T12` marketing/marketing-ideas | No growth strategy |
| **Restricted** | `T13` content-strategy | No content strategy |
| **Restricted** | `T14` marketing/seo-audit | No SEO strategy |

---

## 6. Design Agent

**Maps to:** Design Director (`design-director.md`)
**Primary workspace:** `C:\Bari\01_framework\frontend\` (design specs, governance docs)
**Mandate:** Owns UX, visual hierarchy, information architecture, spacing, typography, and interaction patterns. Provides visual spec before Frontend Agent implements.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `T1` frontend-design | Bold, intentional aesthetic direction — anti-generic-AI design philosophy |
| **Core** | `T5` ui-ux-pro-max | Comprehensive UX standards, accessibility, interaction quality |
| **Core** | `T2` web-design-guidelines` | UI review standard for design critique |
| **Supporting** | `B4` bari-frontend-ui | Reference for Bari-specific component and RTL constraints during design review |
| **Supporting** | `T4` composition-patterns | Component API awareness during spec authoring |
| **Optional** | `T6` find-skills | Discovering design-domain skills |
| **Optional** | `T10` skill-creator | Encoding new design patterns as skills |
| **Restricted** | `B1` bari-category-factory | No pipeline work |
| **Restricted** | `B2` bari-bsip2-scoring-governance | No scoring |
| **Restricted** | `B3` bari-qa-audit | QA Agent runs QA; Design Agent resolves flagged design failures |
| **Restricted** | `T3` react-best-practices | No implementation |
| **Restricted** | `T7` webapp-testing | No test execution |
| **Restricted** | `T9` file-document-processing | No document processing |
| **Restricted** | `T11` marketing/copywriting | No marketing copy |
| **Restricted** | `T12` marketing/marketing-ideas | No growth strategy |
| **Restricted** | `T13` content-strategy | No content strategy |
| **Restricted** | `T14` marketing/seo-audit | No SEO |

---

## 7. QA Agent

**Maps to:** QA & Audit Lead (`qa-audit-lead.md`)
**Primary workspace:** Both `C:\Bari` (score traces, generated JSON) and `C:\Users\HP\bari` (rendered pages, routes, build)
**Mandate:** Verifies correctness across the full pipeline. Last gate before launch. Identifies failures; does not fix them.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `B3` bari-qa-audit | Data-side QA: traceability, hard fails, baseline freeze, run invalidation |
| **Core** | `T7` webapp-testing | Browser-side QA: E2E, visual regression, RTL layout verification |
| **Supporting** | `T9` file-document-processing | Auditing generated JSON files and pipeline output documents |
| **Supporting** | `T2` web-design-guidelines | UI compliance verification during visual QA |
| **Supporting** | `B4` bari-frontend-ui | Reference for Bari component constraints during checklist execution |
| **Optional** | `T6` find-skills | Discovering QA-domain skills |
| **Optional** | `T10` skill-creator | Encoding new QA checklists as skills |
| **Restricted** | `B1` bari-category-factory | Does not execute pipeline — verifies pipeline outputs |
| **Restricted** | `B2` bari-bsip2-scoring-governance | Does not approve scoring rules; escalates score discrepancies |
| **Restricted** | `T1` frontend-design | No design decisions |
| **Restricted** | `T3` react-best-practices | No implementation |
| **Restricted** | `T4` composition-patterns | No implementation |
| **Restricted** | `T5` ui-ux-pro-max | No design decisions — flags failures, Design Agent resolves |
| **Restricted** | `T11` marketing/copywriting | No marketing |
| **Restricted** | `T12` marketing/marketing-ideas | No marketing |
| **Restricted** | `T13` content-strategy | No content strategy |
| **Restricted** | `T14` marketing/seo-audit | No SEO |

---

## 8. Content Agent

**Maps to:** Editorial / Content Team (no existing agent skill file — defined here)
**Primary workspace:** `C:\Bari` (category copy docs, editorial standards, insight line library)
**Mandate:** Authors all consumer-facing copy for Bari: hero sentences, prologue text, insight lines, methodology explanations, category page copy. Works in Hebrew. Does not make product or scoring decisions.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `T8` content-research-writer | Research-backed writing: outlines, drafts, citations, voice preservation |
| **Supporting** | `T11` marketing/copywriting | Persuasive page copy when category pages need conversion-oriented language |
| **Supporting** | `T13` content-strategy | Content planning aligned with category pipeline |
| **Optional** | `T9` file-document-processing | Extracting content from product documents for copy research |
| **Optional** | `T6` find-skills | Discovering writing-domain skills |
| **Optional** | `T10` skill-creator | Encoding editorial style guides as skills |
| **Restricted** | `B1` bari-category-factory | No pipeline execution |
| **Restricted** | `B2` bari-bsip2-scoring-governance | No scoring rules — writes copy that explains scores, does not define them |
| **Restricted** | `B3` bari-qa-audit | No QA execution |
| **Restricted** | `B4` bari-frontend-ui | No frontend implementation |
| **Restricted** | `T3` react-best-practices | No frontend work |
| **Restricted** | `T4` composition-patterns | No frontend work |
| **Restricted** | `T7` webapp-testing | No test execution |
| **Restricted** | `T12` marketing/marketing-ideas | No growth strategy — Marketing Agent owns this |
| **Restricted** | `T14` marketing/seo-audit | No SEO strategy |

---

## 9. Marketing Agent

**Maps to:** Marketing Team (no existing agent skill file — defined here)
**Primary workspace:** `C:\Bari` (marketing strategy docs, campaign briefs, SEO plans)
**Mandate:** Owns marketing strategy, SEO, content marketing, and growth for the Bari platform. Operates outside the product pipeline. Works from approved category launches — does not initiate category work.

| Tier | Skills | Rationale |
|---|---|---|
| **Core** | `T11` marketing/copywriting | Page copy, CTAs, value propositions, conversion language |
| **Core** | `T12` marketing/marketing-ideas | 139-idea growth playbook for Bari's Israeli market context |
| **Core** | `T13` content-strategy | Content pillar planning, keyword-to-buyer-stage mapping, editorial calendar |
| **Core** | `T14` marketing/seo-audit | Technical SEO, hreflang for Hebrew locale, Core Web Vitals, on-page audit |
| **Supporting** | `T8` content-research-writer | Research-backed content: category articles, thought leadership |
| **Supporting** | `T1` frontend-design | Aesthetic reference when proposing landing page or campaign page design |
| **Optional** | `T6` find-skills | Discovering marketing-domain skills |
| **Optional** | `T10` skill-creator | Encoding marketing playbooks as skills |
| **Restricted** | `B1` bari-category-factory | No pipeline execution — marketing activates after BSIP2 readiness is confirmed |
| **Restricted** | `B2` bari-bsip2-scoring-governance | No scoring |
| **Restricted** | `B3` bari-qa-audit | No QA execution |
| **Restricted** | `B4` bari-frontend-ui | No frontend implementation |
| **Restricted** | `T3` react-best-practices | No frontend implementation |
| **Restricted** | `T4` composition-patterns | No frontend implementation |
| **Restricted** | `T7` webapp-testing | No test execution |
| **Restricted** | `T9` file-document-processing | No pipeline data processing |

---

## Skill Coverage Summary

| Skill | Product | Nutrition | Research | Data | Frontend | Design | QA | Content | Marketing |
|---|---|---|---|---|---|---|---|---|---|
| `B1` bari-category-factory | Core | — | — | Core | — | — | — | — | — |
| `B2` bari-bsip2-scoring-governance | Core | Core | — | — | — | — | — | — | — |
| `B3` bari-qa-audit | — | — | — | Supp | — | — | Core | — | — |
| `B4` bari-frontend-ui | — | — | — | — | Core | Supp | Supp | — | — |
| `T1` frontend-design | — | — | — | — | Supp | Core | — | — | Supp |
| `T2` web-design-guidelines | — | — | — | — | Supp | Core | Supp | — | — |
| `T3` react-best-practices | — | — | — | — | Core | — | — | — | — |
| `T4` composition-patterns | — | — | — | — | Core | Supp | — | — | — |
| `T5` ui-ux-pro-max | — | — | — | — | Opt | Core | — | — | — |
| `T6` find-skills | Opt | Opt | Opt | Opt | Opt | Opt | Opt | Opt | Opt |
| `T7` webapp-testing | — | — | — | — | Core | — | Core | — | — |
| `T8` content-research-writer | Supp | Supp | Core | Supp | — | — | — | Core | Supp |
| `T9` file-document-processing | — | Supp | Core | Core | — | — | Supp | Opt | — |
| `T10` skill-creator | Opt | Opt | Opt | Opt | Opt | Opt | Opt | Opt | Opt |
| `T11` marketing/copywriting | — | — | — | — | — | — | — | Supp | Core |
| `T12` marketing/marketing-ideas | Supp | — | — | — | — | — | — | — | Core |
| `T13` content-strategy | Supp | — | Supp | — | — | — | — | Supp | Core |
| `T14` marketing/seo-audit | — | — | Supp | — | — | — | — | — | Core |

**Key:** Core = primary owner, Supp = supporting use, Opt = optional/situational, — = not in stack

---

## Architecture Freeze Statement

This capability matrix is frozen as of 2026-05-31 (Skill Architecture v1). No skill may be added to any agent's Core or Supporting tier without:

1. A named capability gap that cannot be filled by existing skills
2. Written approval from the Head of Product
3. An update to this matrix and to `skill_registry.md`

`find-skills` and `skill-creator` are available to all agents at the Optional tier by design — they enable gap identification without bypassing the approval process.
