---
id: TASK-171A
title: Phase 0 - SIE methodology & scope doc (D7 co-sign)
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
summary: >
  Author 01_framework/supplement_framework/methodology_v1.md: scoring object, 5 dimensions (compute + source per dim), supplement grade semantics, scope boundaries, Evidence Dossier schema, dimension-combination logic, EDPG firewall. Nutrition-led; Product D7 co-sign required before Phase 1.
---

# TASK-171A — Phase 0 - SIE methodology & scope doc (D7 co-sign)

**CLOSED 2026-06-03 — Phase 0 complete, D7 CO-SIGNED (Nutrition + Product).**

## Deliverable
`01_framework/supplement_framework/methodology_v1.md` — authoritative SIE scoring philosophy:
scoring object, 5 dimensions (compute logic + source feed + PASS/FAIL + edge cases each),
dimension combination + caps/floors/vetoes, redefined supplement grade semantics, Evidence
Dossier YAML schema, MVP 5-active stress matrix with pole-coverage proof, scope boundaries +
named out-of-scope machinery, `SUPP-EV-###` registry (5 seed entries), EDPG firewall, and a
new `## Invariants` block (SIE Invariant 1 — No-Necessity Rule). All numbers calibration-pending.

## Governance trail
- Authored by Nutrition Agent; sharpened the model (claim-specific evidence tiering, elemental-vs-compound
  mass split, clinical-megadose "labeled regimen decides" discriminator).
- Product D7 review → CO-SIGNED-WITH-CONDITIONS. Two blocking edits applied:
  **C1** "core active" defined (hidden-dose D-band vs C-band, label-observable);
  **C2** No-Necessity Rule promoted to numbered SIE Invariant 1.
  Two fold-ins applied: **C3** anti-pull-forward scope fence in §7; **C4** §11 D7 decision record.
- All 5 §10 open questions resolved (recorded in §11).
- **D7 = CO-SIGNED (Nutrition + Product).** Authorizes **Phase 1 (dossier build) only**; a supplement
  category go-live remains a separate D10/D1 decision (not made).

## Close-readiness gate (orchestrator-run)
Artifact verified on disk; both blocking edits (SIE Invariant 1, core-active definition) confirmed
present (grep lines 16, 56); §11 decision record + §7 scope fence confirmed. No code shipped; frozen
food invariants untouched (separate engine tree). `cc_reviewed: true`.

## Next
Phase 1 (TASK-171B, pending owner go) — build the 5 Evidence Dossiers (creatine, magnesium, vitamin D3,
caffeine, ashwagandha), Nutrition + Research, all `verification_status: candidate` / `should_affect_score_now: false`.
