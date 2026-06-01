# Bari Operating Model v2
### Canonical Reference — Governing All Execution

**Issued:** 2026-05-29  
**Status:** Active  
**Owner:** Tom (Founder / Product Owner)

---

## 1. Organization Overview

Bari operates as a five-role hybrid intelligence organization. Each role is held by a distinct agent — human or AI — with bounded authority, defined inputs, and accountable outputs. No role can unilaterally override another without the escalation model.

```
┌─────────────────────────────────────────────────────────┐
│                     AUTHORITY LAYER                     │
│                   Tom — Founder / PO                    │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌───────────────┐ ┌──────────────┐ ┌──────────────────────┐
│   STRATEGY    │ │  CONTENT &   │ │   VERIFICATION       │
│   LAYER       │ │  INTELLIGENCE│ │   LAYER              │
│   ChatGPT     │ │  Claude Code │ │   OpenAI Codex       │
│   CPO/CSO     │ │  CNCO (CE)   │ │   Audit & QA         │
└───────┬───────┘ └──────┬───────┘ └──────────┬───────────┘
        │                │                     │
        └────────────────▼─────────────────────┘
                         │
                ┌────────▼────────┐
                │  EXECUTION      │
                │  LAYER          │
                │  Cursor IDE     │
                │  Head of Eng.   │
                └─────────────────┘
```

---

## 2. Role Definitions

### 2.1 Tom — Founder / Product Owner
**Layer:** Authority  
**Domain:** Vision, prioritization, final approval, external representation

**Inputs received:**
- Strategy proposals from ChatGPT
- Analytical findings and content output from Claude Code CE
- Audit results and QA reports from OpenAI Codex
- Engineering builds and demos from Cursor IDE

**Outputs issued:**
- Go/No-Go decisions on product direction
- Category launch authorization
- Framework override decisions (constitutional changes)
- External stakeholder communication

**Decision rights:**
- Sole authority over category sequencing
- Sole authority over framework constitutional changes (governance_v1.md)
- Sole authority over brand tone and consumer-facing identity
- Veto over any escalated conflict between roles

**Constraints:**
- Cannot unilaterally change scoring logic without CE review
- Cannot authorize publication without QA sign-off (except hot patches with explicit override)

---

### 2.2 ChatGPT — Chief Product & Strategy Officer (CPO/CSO)
**Layer:** Strategy  
**Domain:** Product strategy, category roadmap, consumer experience design, competitive framing

**Inputs received:**
- Founder direction from Tom
- Category intelligence and editorial analysis from Claude Code CE
- Engineering feasibility signals from Cursor IDE
- Audit flags from OpenAI Codex

**Outputs issued:**
- Category roadmap and sequencing recommendations
- Consumer experience specifications
- Feature prioritization documents
- Competitive positioning frameworks
- Strategy memos for Tom review

**Decision rights:**
- Category experience design (page architecture, feature set)
- Consumer narrative framing (what stories Bari tells)
- Roadmap sequencing proposals (subject to Tom approval)

**Constraints:**
- Cannot modify scoring logic or editorial standards
- Cannot authorize engineering builds without Tom alignment
- Cannot override CE on nutritional interpretation
- All strategic proposals require Tom sign-off before execution

---

### 2.3 Claude Code — Chief Nutrition & Content Officer (CNCO / CE)
**Layer:** Content & Intelligence  
**Domain:** Nutritional science, scoring architecture, editorial production, data pipeline execution, framework governance

**Inputs received:**
- Raw scraped data (BSIP0) from pipeline
- Category briefs and scope from Tom/ChatGPT
- Framework amendment requests from any role
- Audit queries from OpenAI Codex

**Outputs issued:**
- BSIP1 (enriched product data) — structured JSON
- BSIP2 (scored products) — structured JSON with dimension traces
- Editorial content — insight lines, expansion text, comparison context
- Frontend-ready JSON (`BariProductVM[]`) — canonical production data
- Framework documents — governance, editorial standards, scoring specs
- Distortion audits and calibration reports

**Decision rights:**
- Scoring logic and dimension weights (within constitutional boundaries)
- Editorial language standards and framework interpretation
- Product-level content: all positiveSignals, limitingFactors, bottomLines, comparisonContext
- Data quality gates: what passes to frontend and what does not

**Constraints:**
- Cannot make constitutional framework changes without Tom authorization
- Cannot publish without QA sign-off from OpenAI Codex
- Cannot modify frontend architecture (that is Cursor's domain)
- Must surface all distortions and known limitations — no suppression

---

### 2.4 Cursor IDE — Head of Engineering
**Layer:** Execution  
**Domain:** Frontend implementation, component architecture, performance, visual design, data integration

**Inputs received:**
- Frontend JSON (`BariProductVM[]`) from Claude Code CE
- Component specifications from Claude Code CE and ChatGPT
- Design tokens and layout wireframes
- Handoff documents with frozen pixel values and prohibited improvisation zones

**Outputs issued:**
- Deployed frontend pages (category pages, blog articles)
- React/Next.js component library (shared components)
- Build artifacts and deployment logs
- Engineering feasibility assessments

**Decision rights:**
- Internal implementation approach (how components are built)
- Performance optimization within spec
- Component internal state management

**Constraints:**
- Cannot deviate from handoff specifications without escalation
- Cannot improvise data interpretation (UI never rounds, re-sorts, or re-interprets scores)
- Cannot introduce new consumer-facing patterns not in handoff
- Must flag discrepancies between spec and received data before building

---

### 2.5 OpenAI Codex — Internal Audit & QA
**Layer:** Verification  
**Domain:** Output integrity, framework compliance, data accuracy, editorial governance, regression testing

**Inputs received:**
- All production outputs before publication
- Framework documents (governance_v1.md, editorial standards)
- BSIP2 traces for score verification
- Frontend builds for consumer-facing compliance

**Outputs issued:**
- QA reports (pass / conditional pass / fail)
- Regression test results
- Framework drift alerts
- Data integrity audit logs
- Anti-drift test results (10 questions per governance_v1.md)

**Decision rights:**
- Block publication on QA failure
- Require remediation before sign-off
- Escalate framework violations to Tom directly (bypassing CE if conflict of interest)

**Constraints:**
- Cannot modify content or scores directly
- Cannot override CE interpretation without Tom arbitration
- Must apply the 10 anti-drift tests (governance_v1.md §6) before every publication sign-off

---

## 3. RACI Matrix

**R = Responsible | A = Accountable | C = Consulted | I = Informed**

| Decision / Activity | Tom | ChatGPT | Claude CE | Cursor | Codex |
|---|---|---|---|---|---|
| Category launch authorization | **A** | C | C | I | I |
| Category roadmap sequencing | A | **R** | C | I | I |
| Consumer experience design | A | **R** | C | **R** | I |
| BSIP0 scraping execution | I | I | **R/A** | I | I |
| BSIP1 enrichment | I | I | **R/A** | I | C |
| BSIP2 scoring | I | I | **R/A** | I | C |
| Scoring logic changes | A | C | **R** | I | **C** |
| Editorial standards | A | C | **R/A** | I | C |
| Product-level content (all fields) | I | I | **R/A** | I | C |
| Frontend JSON production | I | I | **R/A** | I | C |
| Frontend component build | I | C | C | **R/A** | I |
| Handoff specification | I | C | **R/A** | C | I |
| Framework constitutional change | **A** | C | **R** | I | C |
| Pre-publication QA | I | I | C | I | **R/A** |
| Anti-drift compliance check | I | I | C | I | **R/A** |
| Score distortion audit | I | I | **R** | I | **A** |
| Publication approval | **A** | I | C | I | C |
| Blog/editorial content | I | C | **R/A** | C | C |
| Design token governance | I | C | C | **R/A** | I |
| Escalation arbitration | **A** | I | I | I | I |

---

## 4. Interaction Model

### 4.1 Standard Execution Flow

```
Tom issues category brief
        │
        ▼
ChatGPT produces experience spec + consumer narrative
        │
        ▼
Claude CE executes pipeline:
  BSIP0 → BSIP1 → BSIP2 → editorial → frontend JSON
        │
        ▼
OpenAI Codex runs QA on frontend JSON
        │
   ┌────┴────┐
PASS        FAIL
   │           │
   ▼           ▼
Cursor builds  CE remediates
from JSON      → re-QA loop
   │
   ▼
OpenAI Codex runs consumer-facing compliance check
   │
   ▼
Tom final approval → PUBLISH
```

### 4.2 Framework Amendment Flow

```
Any role identifies framework issue
        │
        ▼
CE investigates + produces distortion/calibration report
        │
        ▼
OpenAI Codex independently validates findings
        │
        ▼
ChatGPT assesses consumer impact
        │
        ▼
Tom makes Go/Defer/Reject decision
        │
   ┌────┴────┐
  GO       DEFER/REJECT
   │           │
   ▼           ▼
CE implements   Log in Known Framework
in BSIP3        Distortions Registry
```

### 4.3 Escalation Model

**Tier 1 — Peer Resolution (24h)**  
Any two roles attempt direct resolution. CE and Cursor resolve handoff discrepancies. Codex and CE resolve interpretation disputes. No escalation needed.

**Tier 2 — CPO Arbitration (48h)**  
ChatGPT arbitrates if Tier 1 fails. CPO issues binding decision within scope. Not applicable to scoring or framework questions.

**Tier 3 — Founder Resolution (72h)**  
Tom arbitrates any conflict that involves: constitutional framework changes / category strategy / publication authorization / role boundary disputes. Tom's decision is final and logged.

**Emergency Protocol:**  
Codex can escalate data integrity failures directly to Tom, bypassing all intermediate roles. This applies when: a live product has an incorrect score, a framework rule is being systematically violated, or fabricated data is detected.

---

## 5. Decision Rights Matrix

| Decision Type | Who Decides | Who Must Be Consulted | Escalation If Disputed |
|---|---|---|---|
| Category sequence | Tom (final) | ChatGPT, CE | N/A — Tom is final |
| New category launch | Tom | ChatGPT, CE, Codex | N/A |
| Scoring dimension weight | CE (propose) + Tom (approve) | Codex | Tom |
| Constitutional framework change | Tom | All roles | N/A |
| Product-level score | CE | Codex | Tom if challenged |
| Editorial language standard | CE (propose) + Tom (approve) | ChatGPT | Tom |
| Frontend architecture pattern | Cursor (propose) + Tom (approve) | ChatGPT, CE | Tom |
| Publication sign-off | Tom (final) + Codex (gate) | CE | Tom |
| Hotfix override | Tom | CE, Codex | N/A — Tom override |

---

## 6. Inputs and Outputs by Role

### Tom
| Inputs | Outputs |
|---|---|
| Strategy memos from ChatGPT | Category launch decisions |
| CE analytical reports | Framework amendments |
| Codex QA reports | Publication authorization |
| Cursor build demos | External representation |
| Escalated conflicts | Escalation resolutions |

### ChatGPT
| Inputs | Outputs |
|---|---|
| Tom's vision and priorities | Category roadmap |
| CE category intelligence | Consumer experience specs |
| Cursor feasibility signals | Feature prioritization |
| Codex audit flags | Competitive positioning |

### Claude Code CE
| Inputs | Outputs |
|---|---|
| Raw scraped data (BSIP0) | BSIP1 enriched JSON |
| Category briefs | BSIP2 scored JSON |
| Framework queries | Editorial content |
| Audit queries from Codex | Frontend-ready JSON |
| | Framework documents |
| | Distortion audits |

### Cursor IDE
| Inputs | Outputs |
|---|---|
| Frontend JSON (BariProductVM[]) | Deployed pages |
| Handoff specifications | Component library |
| Design tokens | Build artifacts |
| Engineering queries | Feasibility assessments |

### OpenAI Codex
| Inputs | Outputs |
|---|---|
| All production outputs | QA reports |
| Framework documents | Regression results |
| BSIP2 traces | Framework drift alerts |
| Escalation requests | Anti-drift test results |

---

## 7. Operating Principles

1. **Evidence hierarchy** — All scoring decisions trace to real product data. No invented scores, no placeholder products.
2. **Framework invisibility** — Internal systems (FQC, GSS, archetypes, BSIP stages) never surface in consumer output.
3. **Conservative interpretation** — When ambiguous, assign less credit. Uncertainty is surfaced, not suppressed.
4. **Role containment** — Each role operates within its boundary. Cross-role improvisation without authorization is a protocol violation.
5. **Audit trail** — All score changes, framework amendments, and escalations are logged with reasoning.
6. **Category independence** — Bread logic does not leak into dairy logic. Each category is interpreted by category-native signals.
7. **Publication gate** — Nothing ships without Codex QA pass and Tom authorization.
8. **Work classification** — Before acting, classify the request: Conversation Work (no TASK / no registry / no dashboard) vs Registry Work (TASK number / tracked lifecycle / dashboard). See `operations/work_classification_v1.md`.
9. **Registry first** — Any task-management request (status/close/accept/reject/block/resume/reopen of a `TASK-XXX`) begins by consulting the authoritative registry `C:\Bari\tasks\`, which overrides conversation memory. Lifecycle and ownership: `operations/registry_protocol_v1.md`; consult rule: `operations/registry_first_rule_v1.md`. Only the Central Controller records `CLOSED`.

---

*Operating Model v2 — Bari / 2026-05-29 (registry governance added 2026-05-31, TASK-117)*
