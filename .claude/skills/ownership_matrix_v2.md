# Bari Ownership Matrix v2

**Status:** ACTIVE
**Version:** 2.0
**Published:** 2026-05-31
**Owner:** Product Agent
**Task:** TASK-049E
**Companion:** `capability_stack_matrix.md` (skill assignments), `decision_rights_matrix.md` (decision rights)

This matrix defines ownership of domains, processes, artifacts, and repositories across the 9 Bari agents. It is the authoritative reference for "who owns what" at a system level.

Ownership means: the designated agent is the single point of accountability for that item. Others may contribute or must be consulted, but the owner is responsible for quality, consistency, and compliance.

---

## Domain Ownership

| Domain | Owner | Notes |
|---|---|---|
| Product strategy & roadmap | Product Agent | Sole authority on what Bari builds and when |
| Scoring philosophy & methodology | Nutrition Agent | Sole authority on BSIP scoring rules |
| Scientific evidence & research | Research Agent | Sole authority on evidence tier classification |
| Data pipeline & corpus | Data Agent | Sole authority on pipeline execution |
| Website implementation | Frontend Agent | Sole authority on all code in `C:\bari-web\src\` |
| Visual design & UX | Design Agent | Sole authority on visual spec and drift prevention |
| QA & verification | QA Agent | Sole authority on rollout verdicts and QA baselines |
| Consumer-facing copy | Content Agent | Sole authority on category page language |
| Marketing & growth | Marketing Agent | Sole authority on campaigns and SEO strategy |
| Skill architecture | Frontend Agent + Product Agent | Joint authority (D15, D16) |
| Agent OS & governance | Product Agent + Frontend Agent | Joint authority (D16) |

---

## Repository Ownership

| Repository | Owner | Other agents |
|---|---|---|
| `C:\bari-web\src\` | Frontend Agent | QA Agent (reads/verifies), Design Agent (reviews renders) |
| `C:\bari-web\src\data\comparisons\` | Data Agent (generates) / Frontend Agent (integrates) | QA Agent (verifies) |
| `C:\Bari` (pipeline) | Data Agent | Nutrition Agent (scoring configs), Product Agent (strategy docs) |
| `C:\Bari\01_framework\frontend\` | Design Agent | Frontend Agent (implements from specs) |
| `C:\Bari\.claude\agents\` | All agents (their own file) | Product Agent + Frontend Agent (architecture changes) |
| `C:\Bari\.claude\skills\` | Frontend Agent | Product Agent (governance docs) |

---

## Process Ownership

| Process | Owner | Required Approvals | Verifier |
|---|---|---|---|
| Category pipeline initiation | Product Agent | Product Agent | QA Agent |
| Shelf mapping | Data Agent | Product Agent | QA Agent |
| Corpus filter | Data Agent | Product Agent | QA Agent |
| BSIP0 gate | Data Agent | Product Agent | QA Agent |
| BSIP1 enrichment | Data Agent | Nutrition Agent | QA Agent |
| QA gate execution | QA Agent | — (QA owns verdict) | — |
| BSIP2 readiness | Data Agent | Nutrition Agent + Product Agent | QA Agent |
| Frontend JSON generation | Data Agent | — (after BSIP2 approval) | QA Agent |
| Scoring rule design | Nutrition Agent | — | — |
| Scoring rule approval | Nutrition Agent + Product Agent | Both must sign | QA Agent |
| Scoring rule implementation | Data Agent | Nutrition Agent + Product Agent | QA Agent |
| Frontend component implementation | Frontend Agent | Design Agent (spec) + Product Agent (scope) | QA Agent |
| Design spec authoring | Design Agent | Product Agent (if scope change) | QA Agent (post-implementation) |
| Consumer copy authoring | Content Agent | Nutrition Agent + Product Agent | QA Agent |
| Marketing campaign | Marketing Agent | Product Agent | QA Agent (landing pages) |
| New skill installation | Frontend Agent | Product Agent | QA Agent |
| Agent OS changes | Product Agent + Frontend Agent | Both required | QA Agent |

---

## Artifact Ownership

### Pipeline Artifacts

| Artifact | Owner | Consumers |
|---|---|---|
| `shelf_map.json` | Data Agent | Product Agent (approval), QA Agent (verification) |
| `corpus_filter.json` | Data Agent | Product Agent (approval), QA Agent (verification) |
| `bsip0_gate_result.json` | Data Agent | Product Agent (approval), QA Agent (verification) |
| `bsip1_enrichment_report.json` | Data Agent | Nutrition Agent (approval), QA Agent (verification) |
| `bsip2_readiness_checklist.json` | Data Agent | Nutrition Agent + Product Agent (approval) |
| `frontend_package.json` | Data Agent | Frontend Agent (integration), QA Agent (verification) |
| Evidence registry | Data Agent | Nutrition Agent (references), QA Agent (audit) |

### Website Artifacts

| Artifact | Owner | Consumers |
|---|---|---|
| Canonical components (`src/components/shared/`) | Frontend Agent | QA Agent (verification), Design Agent (review) |
| View Model (`BariProductVM`) | Frontend Agent | Data Agent (generates to contract), QA Agent (verifies) |
| Design tokens (`bari-comparison-tokens.ts`) | Design Agent (values) + Frontend Agent (file) | All frontend work |
| Category registry | Frontend Agent | QA Agent (verification) |
| Frontend JSON (`src/data/comparisons/`) | Data Agent (source) + Frontend Agent (deployment) | QA Agent (verification) |

### Content Artifacts

| Artifact | Owner | Consumers |
|---|---|---|
| Hero sentences | Content Agent | Frontend Agent (integration), QA Agent (presence verification) |
| Prologue paragraphs | Content Agent | Frontend Agent (integration), QA Agent (presence verification) |
| Product insight lines | Content Agent | Frontend Agent (integration), QA Agent (presence verification) |
| Methodology text | Content Agent | Frontend Agent (integration), QA Agent (leakage verification) |
| Label registry (display names) | Content Agent | Data Agent (pipeline use), Frontend Agent (rendering) |
| Hebrew style guide | Content Agent | All agents producing Hebrew-language outputs |

### Governance Artifacts

| Artifact | Owner | Status |
|---|---|---|
| `agent_os_v2.md` | Product Agent + Frontend Agent | ACTIVE |
| `capability_stack_matrix.md` | Product Agent + Frontend Agent | FROZEN v1 |
| `decision_rights_matrix.md` | Product Agent | FROZEN v1 |
| `ownership_matrix_v2.md` (this document) | Product Agent | ACTIVE v2 |
| `skill_registry.md` | Frontend Agent | ACTIVE |
| `skill_activation_guide.md` | Frontend Agent | ACTIVE |
| 9 agent definition files | Each agent (their own) | ACTIVE |
| `deprecated_personas.md` | Product Agent + Frontend Agent | ACTIVE |
| `mcp_registry.md` | Frontend Agent | ACTIVE |
| `C:\Bari\.mcp.json` | Frontend Agent (config) | ACTIVE — not version controlled |
| `agent_os_v1.md` | — | ARCHIVED |
| `head-of-product.md` | — | DEPRECATED |
| `chief-nutrition-officer.md` | — | DEPRECATED |
| `research-analyst.md` | — | DEPRECATED |
| `frontend-architect.md` | — | DEPRECATED |
| `design-director.md` | — | DEPRECATED |
| `qa-audit-lead.md` | — | DEPRECATED |

---

## Cross-Agent Dependency Map

This shows who depends on whom, in sequence, for the primary category launch flow.

```
Product Agent ──────────────────────────────────────────┐
    │ (initiates)                                         │ (approves each gate)
    ▼                                                     │
Research Agent ──► Nutrition Agent ──► Data Agent ───────┤
    │ (evidence)     │ (scoring)        │ (pipeline)      │
    │                │                  ▼                 │
    │                └───────────► Data Agent ◄───────────┤
    │                              (implements)           │
    │                                   │                 │
    │                                   ▼                 │
    │                             Frontend Agent ◄────────┤
    │                             (builds page)           │ (scope approval)
    │                                   │                 │
    │                            Design Agent ◄───────────┘
    │                            (spec, review)
    │                                   │
    │                             Content Agent
    │                             (copy authoring)
    │                                   │
    └──────────────────────────────► QA Agent ◄──── (all artifacts)
                                          │
                                    Product Agent
                                    (go-live decision)
                                          │
                                   Marketing Agent
                                   (post-launch)
```

---

## Ownership Gaps (Known, Accepted)

The following items do not yet have a dedicated owner. They are tracked here for future Agent OS iterations.

| Item | Current State | Proposed Owner |
|---|---|---|
| Hebrew SEO keyword strategy | Shared between Marketing Agent and Research Agent | Marketing Agent (primary), Research Agent (data) |
| Exception registry (frozen constraint violations) | Referenced in Design Agent and Frontend Agent but no owner | Design Agent |
| Product-marketing context file (`.agents/product-marketing.md`) | Referenced by marketing skills | Marketing Agent |

---

## Version History

| Version | Date | Change |
|---|---|---|
| v1 | — | Not published (v1 was capability_stack_matrix.md + agent_os_v1.md) |
| v2.0 | 2026-05-31 | First dedicated ownership matrix. Covers domain, repository, process, artifact, and governance ownership. TASK-049E. |
| v2.1 | 2026-05-31 | Added `mcp_registry.md` and `C:\Bari\.mcp.json` to governance artifacts. TASK-057. |
