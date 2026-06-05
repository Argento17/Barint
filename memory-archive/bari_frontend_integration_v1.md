---
name: bari_frontend_integration_v1
description: Frontend integration checklist v1 — 10-section onboarding document for entering any Bari frontend repo; covers repo/arch/component/token/styling/responsive/drift discovery + 7 canonical components + risk map + מעדנים rollout plan
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

File: `C:\Bari\01_framework\frontend\frontend_integration_checklist_v1.md`

**Why:** Bari transitioned from Governance Phase → Live Interface Validation Phase (2026-05-28). Priority is now: real component implementation → mobile testing → scroll rhythm → visual density → user comprehension → drift monitoring. No new philosophy/governance documents unless a new production failure mode appears.

**The 10 sections:**
1. Repo Discovery — framework, routing, RTL, deployment
2. Architecture Discovery — page structure, data fetching, state management
3. Component Discovery — audit table for all 7 required components
4. Design-System Discovery — 18 canonical Bari tokens, check against existing system
5. Styling-System Discovery — Tailwind/modules/etc, override and isolation risks
6. Responsive-System Discovery — mobile-first check, viewport assumptions, sticky behavior
7. Drift Detection — greps for dashboard patterns, NOVA/BSIP leakage, card overuse, tooltip count
8. Required Canonical Components — exactly 7: ProductRow, ScoreChip, ExpansionSection, CategoryHero, CategoryPrologue, StickyFilterButton, MethodologyFooter — nothing more in v1
9. Risk Mapping — 10 named risks with severity, trigger, mitigation
10. מעדנים Rollout — 6-step plan: data wire-up → component build order → geometry validation → drift audit → 5 QA gates → mobile validation steps

**First live target:** מעדנים — data at `C:\Bari\02_products\maadanim\bsip2_outputs\`, insight lines at `maadanim_insight_lines_v1.md`

**Rule:** Run all 10 sections before writing implementation code. Do not build until sections 1–7 are complete and their statuses documented.

**Related:** [[bari_comparison_template_v1]] [[bari_insight_line_spec_v1]] [[bari_exception_registry_v1]]
