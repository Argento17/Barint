---
id: TASK-179F
title: Glass Box W1 — finalize + append D5/D6 evidence entries (Nutrition co-sign)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
close_reason: >
  D5/D6 evidence entries finalized + relocated to the correct registry. Nutrition D6/D7 + Product D7
  co-signs carried; EV-038 wording fix in place; five entries adopted-behind-flag in the BSIP2 registry
  as EV-035…039 (governance BEV- file reverted to BEV-only after the v1 mis-append — an orchestrator
  briefing error, not a Nutrition fault). Cross-refs swept (spec + memo by Nutrition; task files by CC).
  CC gate verified both registries (governance max BEV-077 clean; BSIP2 new max EV-039). No code, no
  score moved; entries inert behind BARI_GLASSBOX_D5D6 (OFF). Unblocks Data build (TASK-179G).
depends_on: [TASK-179E]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
cc_comments:
  - flag: fyi
    text: "Orchestrator briefing error (NOT Nutrition's): the entries were appended to the GOVERNANCE registry (01_framework/governance/evidence_registry_v1.md, BEV- series) instead of the BSIP2 engine registry (03_operations/bsip2/evidence_registry/, EV- series) where the cited precedents (EV-029/030/031/034) live and where BSIP2 scoring rules belong. Cause: a grep matched the 'EV-078' substring inside 'BEV-078'. Correction dispatched: revert the governance Section 11, append to the BSIP2 registry as EV-035…039 (native format; current EV- max=034), sweep cross-refs. Content unchanged — relocate+renumber only."
summary: >
  Wave 1 dual-sign finalization (corrected): Nutrition logged its formal D6/D7 co-sign on the four D5/D6
  binding numbers (authored in 179D, Product-co-signed in 179E), applied the EV-038 wording fix, and the
  five entries are now adopted-behind-flag in the BSIP2 engine registry as EV-035…039
  (03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md, new max EV-039). NOTE: v1
  mistakenly appended them to the governance BEV- registry (orchestrator briefing error); that file was
  reverted to BEV-only and the entries relocated. Inert behind BARI_GLASSBOX_D5D6 (default OFF),
  revisitable after the pilot diff. Registry edit only — no engine code (Data builds next, 179G), no
  score movement, OFF = byte-identical. Unblocks the Data build.
---

# TASK-179F — Finalize + append D5/D6 evidence entries (Nutrition co-sign)

**Part of:** TASK-179 (Glass Box), Wave 1. **Unblocks:** Data build (179G). Closes the dual-sign loop on
the four numbers (Nutrition proposed in 179D, Product co-signed in 179E). Domain agent proposes RETURNED.

Actions:
1. Log Nutrition's formal D6/D7 co-sign on DEMOTE_CEILING_BOUND=60 · NULL_FLOOR=30 (AND-severe) · D5→D6 −10/−20 · structural-only=0.
2. Apply Product's EV-038 wording fix: state that DEMOTE=60 is a no-op restatement of the live band edge and that ALL ON-vs-OFF movement originates in EV-037's −10/−20 reduction + the panel-absent→null flip (demote/null only, never promotion).
3. Flip EV-035…039 DRAFT → **adopted-behind-flag** (`BARI_GLASSBOX_D5D6`, default OFF; not live-active; revisitable after the pilot diff).
4. Append EV-035…039 to the live registry `01_framework/governance/evidence_registry_v1.md`.

Constraints: registry edit only; no engine/frontend code; no score movement; entries do not activate any rule (flag OFF = byte-identical).
