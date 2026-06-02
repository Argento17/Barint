---
id: TASK-140
title: "Cereals full-cycle BSIP0->BSIP2 (greenfield, ship-first candidate)"
owner: data-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-01
depends_on: []
blocks: []
category_id: breakfast-cereals
summary: >
  Clean greenfield full cycle for cereals via bari-category-factory: Shufersal shelf map -> corpus filter ->
  BSIP0 gate -> BSIP1 enrichment -> QA gate -> BSIP2 readiness -> frontend package. Governance is already DONE
  (cereals_gap_resolution_v1: verdict B, Launch-Ready-with-Conditions) so this is the unblocked workstream.
  Apply the four cereals governance constructs during enrichment/scoring. No dairy dependency — can ship first.
---

# TASK-140 — Cereals full-cycle BSIP0->BSIP2

Source for data: **Shufersal** (validated Israeli ingredient-bearing source, run_yogurt_003 precedent).
Governance reference: `01_framework/governance/cereals_gap_resolution_v1.md`.

## Pipeline (bari-category-factory, no stage skipped)
1. **Shelf map** — Shufersal cereal shelf slug(s) -> `shelf_map.json`. (Product approves, QA verifies.)
2. **Corpus filter** — cereal scope, no overlap with snacks/granola-as-snack; min corpus size met.
3. **BSIP0 gate** — Shufersal scrape; coverage target >=90% ingredient+nutrition; Hebrew names + gtin13.
4. **BSIP1 enrichment** — apply the four governance constructs:
   - **Granola sub-pool** (Constitution Sec 2.9): NOVA>=3 / added-sugar>=10g / added-fat>=10g 2-of-3 trigger.
   - **Children's product** (Sec 2.8): 2-of-4 indicator, serving <=25g; anti-immunity.
   - **Whole-grain thresholds** (Guardrails 5.2.1): composition >=30% / dominant >=51%, first-ingredient test.
   - **Endemic fortification notice** (Sec 6.4 DISTORTION-004): category-level shelf note if >=50% fortified.
5. **QA gate** — hard-fail-free; warnings reviewed.
6. **BSIP2 readiness** — scoring registered/approved (Nutrition); label observability; rollback.
7. **Frontend package** — comparison data + RTL labels + Hebrew coverage.

## Exit / DoD
Coverage >=90%, INSUFFICIENT 0% displayable, misroute <5%, four constructs applied + documented, QA green,
frontend_package.json ready. Then propose RETURNED.

## State — RETURNED (proposed) 2026-06-01, data-agent
Full 7-stage factory cycle executed via bari-category-factory, engine 0.4.0 UNMODIFIED, real Shufersal
scrape (run_yogurt_003 pattern). Run = **run_cereals_002**. Artifacts in
`02_products/breakfast_cereals/factory_run_002/` + findings at
`02_products/breakfast_cereals/reports/run_cereals_002_factory_findings.md`.

**Exit criteria:**
- ✅ Coverage ≥90% (100% on 92 displayable) · ✅ INSUFFICIENT 0% displayable · ✅ four constructs applied+documented
  · ✅ frontend_package.json ready (NON-AUTHORITATIVE)
- ❌ **misroute <5% — FAILS at 7.6%** (7 real cereals → bread/whole_food_fat/beverage; router has no
  cereal anchor — engine fix, OUT OF SCOPE, same class as run_yogurt_003) · ❌ **QA green** (QA-CER-001 hard fail)

**Results:** 113 scraped → 92 displayable (0 insufficient, 100% coverage, Hebrew 100%). Grades A7/B10/C48/D25/E2,
median 58.3. Constructs: granola pool 25; children's 4 (mascot brands); whole-grain 43 claims / 8 MDFs;
**fortification 27.2% — NOT endemic** (contradicts pre-data assumption; no Endemic Distortion note triggered).

**NO-GO to launch live; not promoted.** Frontend package preserved NON-AUTHORITATIVE (`NON_AUTHORITATIVE.md`
in run dir). Two scoped follow-ups gate live launch:
1. **Router** cereal-anchor fix (engine — Nutrition+Data); re-run as run_cereals_003.
2. **Nutrition** review of 4 NOVA-1 shaped-baked-flake A's + reconcile scoring.md A-threshold (TASK-139A).

Proposes **RETURNED**. Only the Central Controller records CLOSED.
