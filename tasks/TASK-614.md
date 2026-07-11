---
id: TASK-614
title: Corrected-nutrition re-score: bread fat placeholder (+ other MATERIAL shelves) — orchestrator authority |Δ|≤30
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
blocker: "Sequenced AFTER (a) TASK-602 re-scrape baseline complete (batch-5 pending) + consolidated manifest rebuild, and (b) BSIP0 parser fix lands (other session). NOT owner-gated: score movements are the orchestrator's authority (owner ruling 2026-07-11, |Δ|≤30; bread diagnosed max |Δ|=6, 1 grade flip B->C on keto bread 7290014321168). Re-score bread on the CURRENT engine with corrected nutrition via the uniform pipeline (re-enrich BSIP1 from batch-3 captures -> BSIP2 -> generate), full re-audit + Adversarial QA gate, verify every |Δ|<=30 (>30 = defect, stop). Fold in other MATERIAL shelves the re-scrape surfaced (cheese 3, +batch-5). EXCLUDE 7290016967074 (name/SKU identity anomaly, route to Data Agent separately). Consumer deploy still owner-merge."
depends_on: []
blocks: []
category_id: null
origin_task: TASK-612
lesson_trigger: none
summary: >
  Bread bsip2 traces scored on placeholder fat (0.25/0.5g) not real (1-9.1g) — VERIFIED (trace L1 fat_g=0.25 + fat_quality formula reproduced 18/18). Correcting lowers 14/18 by 0.1-6.0pts, flips 1 grade B->C. Systematic re-score on current engine (fixes TASK-563 non-derivability for bread as bonus). Evidence: bread_diff.json + scratchpad task612 sim.
---

# TASK-614 — Corrected-nutrition re-score: bread fat placeholder (+ other MATERIAL shelves) — orchestrator authority |Δ|≤30

## Proven data-integrity damage (from the TASK-602 re-scrape — live panels now exist to prove it)
The re-scrape PROVED published nutrition was computed on placeholder/wrong values on multiple shelves
(TASK-595 could not prove this — no panels then). Two magnitude classes:

**A. Fat placeholder (EV-026 signature) — corrections SMALL (fat weight 0.08, ≤~6pt like bread) → orchestrator authority (|Δ|≤30):**
- **bread**: 18/23 fat = 0.25/0.5g vs live 1.0-9.1g (diagnosed TASK-612: 14/18 move, 1 grade flip B→C, max |Δ|=6).
- **crackers**: **19/19 (100%)** fat = 0.25g(16)/3.5g(3) vs live 2.0-32.2g (batch-5).
- (cereals was display-only — traces scored correct fat, no re-score, TASK-596.)

**B. Whole-panel scale error — corrections potentially LARGE (>30) → DEFECT-CLASS, investigate + OWNER DIGEST, do NOT auto-ship:**
- **cookies_coffee**: 4 products with served nutrition ~5-6x LOWER than live across EVERY field
  (served 92-97 kcal vs live 465-554 kcal/100g, both per-100g basis confirmed). All-field error →
  multi-dimension score move likely >30 → per owner ruling (|Δ|>30 = defect) these are NOT
  auto-applied: root-cause the capture/basis bug (per-serving vs per-100g?), confirm, surface to owner.
- cookies_coffee: +1 product sodium 4x (opposite direction), recorded.
- cheese: 3 MATERIAL (small isolated, batch-4).

## Deliverable / approach (orchestrator authority per owner ruling 2026-07-11)
1. Consolidated manifest rebuild + registry recompile FIRST (after PD-2 join), so re-enrich reads clean captures.
2. Re-enrich BSIP1 from the corrected batch-3/4/5 captures → re-score on the CURRENT engine via the
   uniform pipeline (systematic, not artisanal) → generate. Fixes the TASK-563 non-derivability for
   these shelves as a bonus (certified, trace-derivable numbers).
3. Full re-audit of the new verdicts + Adversarial QA gate (rescore_full_reaudit_and_c3).
4. **Class A (bread/crackers/cheese): verify every |Δ|≤30 → APPLY (orchestrator authority).**
   **Class B (cookies 5-6x): if |Δ|>30 → DEFECT, do NOT ship, root-cause + OWNER DIGEST.**
5. EXCLUDE 7290016967074 (bread name/SKU identity anomaly — route to Data Agent separately).
6. Consumer DEPLOY of any changed scores = owner merge (two-speed).

## Root-cause note (for the BSIP0/BSIP1 fix — other session)
The fat placeholder (0.25/0.5) = null→placeholder fallback (EV-026). The cookies 5-6x = likely a
per-serving-vs-per-100g basis capture error. Comma-thousands sodium parser bug (bsip0_nutrition.py
_to_float) also re-flagged by batch-5. These are the upstream defects; TASK-614 corrects the OUTPUTS
using the verified re-scraped values.
