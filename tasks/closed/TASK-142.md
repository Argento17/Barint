---
id: TASK-142
title: "Cottage/White Cheese full-cycle BSIP0->BSIP2 (gated on stress-test B + dairy calibration)"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-02
close_reason: "Cleanup of formatter duplication in the future"
reopened_at: 2026-06-01
returned_at: 2026-06-02
returned_reason: "TASK-142A (EV-029 parser fix) CLOSED. Full cycle re-run on corrected fat: re-scrape (corrupt 2026-06-01 raw replaced) -> BSIP1 run_cheese_003 -> BSIP2 run_cheese_003 (engine 0.4.1 UNMODIFIED). All data/routing/plausibility gates GREEN (COV-006 0.0% implausible vs 31.9% corrupt; misroute 1.7%; fat sane all 4 sub-pools; INSUFFICIENT 0% displayable; A-ceiling withholds the lone macro-A on real fat). Only remaining gate = Nutrition/Product grade-publication sign-off (human; blocks_live). Frontend package factory_run_003 NON-AUTHORITATIVE. See run_003 return block."
reopen_reason: "REOPENED from a premature CLOSED (same day). The Nutrition grade-publication review (Nutrition Agent, 2026-06-01) surfaced a DATA-INTEGRITY DEFECT that invalidates the cheese SCORES: the BSIP0 scraper captured the trans-fat row ('שומן טראנס פחות מ-0.5') as total fat, so fat_g=0.5 for 62/116 raw products (incl. 18% cream cheese and 5% white cheese). Because fat feeds the score engine, run_cheese_001/002 grades are INVALID. TASK-145 (router fix) is UNAFFECTED (routing is name-based; 47.4%->1.8% stands; remains CLOSED). The pipeline ARCHITECTURE (4 sub-pools, constructs, A-ceiling, disclosures, routing) is validated; only the nutrition input is corrupted."
blocker: "BLOCKED on TASK-142A — investigate + fix the BSIP0 nutrition-parse data-integrity bug (trans-fat row captured as total fat; nutrition panel bleeding into ingredients_text_he; possible cross-category blast radius to cereals/yogurt sharing the same NUTR_LABEL_MAP). Parent resumes after 142A: re-scrape -> re-build BSIP1 -> re-score (run_cheese_003) -> re-validate (QA + Nutrition) -> re-propose RETURNED."
depends_on: [TASK-139, TASK-141, TASK-142A]
blocks: []
category_id: cheese_spreads
blocker: "CLEARED 2026-06-01. Gate satisfied: TASK-141 verdict B (CLOSED) + dairy calibration TASK-139 (parent + 139A/B/C CLOSED, 139D RETURNED) all landed. (When this cycle began, 139 was still IN_PROGRESS pending its yogurt re-score; it was CLOSED later the same day — gate satisfied either way.) Full cycle then executed."
summary: >
  Full real Shufersal BSIP0->BSIP2 cycle for cottage/white cheese (cheese spreads) on the calibrated dairy
  engine, applying the sub-pool/light-threshold/endemic structure from TASK-141. Pipeline per
  bari-category-factory: shelf map -> corpus filter -> BSIP0 gate -> BSIP1 enrichment -> QA gate ->
  BSIP2 readiness -> frontend package. Starts only when 141 verdict >= B and 139 calibration is applied.
---

# TASK-142 — Cottage/White Cheese full-cycle BSIP0->BSIP2

**BLOCKED until:** TASK-141 verdict >= B **and** TASK-139 calibration applied (enricher culture-vocab + A-ceiling ruling both feed cheese).

## Pipeline (bari-category-factory)
1. Shelf map — Shufersal cottage/white-cheese shelf slug(s).
2. Corpus filter — cheese-spreads scope; no overlap with maadanim or hard cheese.
3. BSIP0 gate — Shufersal scrape; coverage >=90% ingredient+nutrition; Hebrew names + gtin13.
4. BSIP1 enrichment — apply TASK-141 sub-pools (cottage/cream/labaneh/white-quark), 'light' threshold, endemic notice; culture credit via 139B.
5. QA gate — hard-fail-free.
6. BSIP2 readiness — scoring registered/approved (Nutrition); A-ceiling ruling (139A) applied; rollback.
7. Frontend package — comparison data + RTL labels + Hebrew coverage.

## Exit / DoD
Coverage >=90%, INSUFFICIENT 0% displayable, misroute <5%, sub-pool structure applied + documented, QA green,
frontend_package.json ready. Then propose RETURNED.

---

## Return block — proposed RETURNED (data-agent, 2026-06-01)

**Run:** `run_cheese_001` · **Engine:** proto_v0 / 0.4.1 (UNMODIFIED — no score tuning, no router changes).
**Deliverables:** `02_products/cheese_spreads/` (category_config + factory_run_001/{shelf_map, corpus_filter,
bsip0_gate_result, qa_gate_result, bsip2_readiness_checklist, frontend_package, pipeline_summary}.json),
`03_operations/bsip0/scrape/shufersal_cheese/{01_scrape,02_build_bsip1,03_package_frontend}_cheese.py`,
`03_operations/bsip1/run_cheese_001/output/` (57 BSIP1 + curation + cheese_constructs reports),
`03_operations/bsip2/proto_v0/src/batch_run_cheese_001.py`,
`02_products/cheese_spreads/bsip2_outputs/run_cheese_001/` (57 traces),
`02_products/cheese_spreads/reports/run_cheese_001_{run_summary.json, factory_findings.md}`.

**Full BSIP0→BSIP2 cycle executed end-to-end on the calibrated dairy engine.** 116 real Shufersal products →
57 displayable. **Four sub-pools applied + documented** (cottage 11 / white-cheese-quark 17 / cream-cheese-spread 26 /
labaneh 3; fat tiers = variants; Sec 2.9). All TASK-141 governance applied: Sec 2.8 developmental D3≤20g (0 detected),
Sec 5.2.1 light threshold relative ≥25% (1 claim, 0 MDF), A-ceiling C1–C6 with A≥80 (the lone macro-A
גבינה טבורוג 5%/81.0 correctly **WITHHELD** — fails C1/C2/C3), 139B FERMENTATION_TERMS + EV-015 flavor-vs-marker
guard (3/57 credited, 0 violations), and the **two PO-approved Sec 6.4 disclosure texts** wired in clean RTL Hebrew.

**DoD scorecard:** coverage ≥90% ✅ (100% nutrition / 91.2% ingredients) · sub-pools applied+documented ✅ ·
frontend_package.json ready ✅ (NON-AUTHORITATIVE) — **BUT** INSUFFICIENT 0% ❌ (5.3%) and misroute <5% ❌ (**47.4%**)
and QA green ❌.

**Single blocking cause — QA-CHS-001 (out of scope here):** `router_v2.py` has no cream-cheese/spread anchor, so
**all 26 cream-cheese products misroute** (גבינת שמנת/ממרח גבינה/פילדלפיה/נפוליאון → default/whole_food_fat); the 3
insufficient are the same root cause. Cottage / white-cheese / labaneh (31 products) route correctly and are
launch-quality. The router fix is a **governed engine change** (CLAUDE.md "do not redesign scoring"; cereals
QA-CER-001 / TASK-139C precedent) — NOT hand-tuned in this data-pipeline task.

**Guards honored:** engine unmodified; no published scores changed; CLAUDE.md frozen invariants untouched;
constructs are label-observable classification/disclosure layers (no new scoring rule); frontend package
NON-AUTHORITATIVE and NOT promoted.

**Two scoped follow-ups gate live launch:** (1) router cream-cheese anchor + regression-lock → **run_cheese_002**
(own governed engine task); (2) Nutrition sign-off (A-ceiling withhold + correctly-routed grades).

### Update — follow-up (1) LANDED via TASK-145 (2026-06-01)

The router cream-cheese anchor was registered and executed as **TASK-145** (RETURNED), governed under
bari-bsip2-scoring-governance (**EV-025**), regression-locked (router 15/15). Re-ran the same BSIP1 corpus as
**run_cheese_002** (`factory_run_002/`): **misroute 47.4% → 1.8% (PASS)**, **insufficient 5.3% → 0% (PASS)**,
QA gate **GREEN**, frontend package **50/57 display-approved** (NON-AUTHORITATIVE). The A-ceiling correctly
withholds 6 macro-A white cheeses (fail C3). **TASK-142 DoD now met on all data/routing/QA gates** — the only
remaining gate to LIVE promotion is follow-up (2): Nutrition/Product grade-publication sign-off (a human gate).
run_cheese_001 / factory_run_001 retained as the pre-fix diagnostic record.

**Gate note:** all cheese-relevant dairy calibration (139A/B/D + parent 139) is CLOSED/RETURNED, so the
TASK-142 gate is satisfied. (At cycle start 139 was still IN_PROGRESS pending its yogurt re-score; the
Controller closed it later the same day — corrected per CC audit 2026-06-01.)

**Proposing RETURNED.** Only the Central Controller records CLOSED.

---

## Return block — proposed RETURNED (data-agent, 2026-06-02) — run_cheese_003 on EV-029-corrected fat

**TASK-142A is CLOSED** (BSIP0 trans-fat→total-fat parser bug fixed in shared `_shared/bsip0_nutrition.py`,
wired into `shufersal_cheese/01_scrape_cheese.py`). Resumed TASK-142 and **completed the full cycle on
corrected data** — engine **0.4.1 UNMODIFIED** (no score tuning, no threshold/weight/penalty/cap change, no
router change; the fix is BSIP0 data-ingestion only).

**Run:** `run_cheese_003` · supersedes run_cheese_002 (INVALID — corrupt fat) and run_cheese_001 (pre-router-fix diagnostic).

**Deliverables:**
- Re-scrape: `02_products/cheese_spreads/bsip0_outputs/cheese_bsip0_raw_20260602T054843.json` (corrupt 2026-06-01 raw **replaced/deleted**).
- BSIP1: `03_operations/bsip1/run_cheese_003/output/` (59 records + curation + cheese_constructs report) via `02_build_bsip1_cheese_003.py`.
- BSIP2: `02_products/cheese_spreads/bsip2_outputs/run_cheese_003/` (59 traces) via `proto_v0/src/batch_run_cheese_003.py`.
- Factory: `02_products/cheese_spreads/factory_run_003/{qa_gate_result, bsip2_readiness_checklist, pipeline_summary, frontend_package, NUTRITION_SIGNOFF_REQUEST}`.
- Reports: `reports/run_cheese_003_{run_summary.json, factory_findings.md}`.
- Scrape import fix: `01_scrape_cheese.py` now imports `composition_nutrition_report` (BSIP0 plausibility gate).

**The parser fix is validated end-to-end.** BSIP0 plausibility gate **0.0% implausible** (the corrupt
run_cheese_001/002 corpus measured **31.9% FAIL**). **fat sane across all 4 sub-pools** — fat≤0.5: **0** in every
pool, saturated>fat: **0** in every pool; cream-cheese now reads **real 25–32% fat** where the bug read 0.5g
(cottage 1–12, white-cheese-quark 5–17, labaneh 14). COV-006 PASS on the BSIP1 corpus (0/59).

**DoD scorecard — all data/routing/plausibility gates MET:** coverage ≥90% ✅ (displayable 100%, full corpus 91.5%) ·
INSUFFICIENT 0% displayable ✅ (0/54) · misroute <5% ✅ (**1.7%**, 1 residual goat cheese → snack_bar_granola, same
as run_002, under gate) · sub-pools applied+documented ✅ (cottage 11 / white-cheese-quark 18 / cream-cheese-spread
24 / labaneh 1) · QA green ✅ (engine unchanged) · frontend_package ready ✅ (factory_run_003; **52/59
display-approved**; NON-AUTHORITATIVE).

**A-ceiling re-checked on REAL fat data and HOLDS.** Exactly **one** product reaches grade A — גבינה טבורוג 5%
(82.0) — and is **WITHHELD** (`a_eligible_pre_routing=false`; fails C1 added-sugar, C2 engineered-additives, C3 no
confirmed live culture, C4 non-intact matrix). **0** products A-eligible pre-routing. Conservative dairy ceiling
confirmed correct on corrected fat (run_002 had 6 macro-A's on the corrupt corpus; on real fat far fewer reach A
and the lone one is still withheld).

**Two truthful findings the fix exposed (NOT regressions):**
1. **Score shift.** Overall median 65.0→55.0; cream-cheese-spread 60.7→52.0 — high-fat spreads now scored on real
   25–32% fat. Engine unchanged; this is corrected-data truth. Grades: A 1 / B 20 / C 25 / D 7 / E 1.
2. **5 transparency-tier withholds.** גבינת שמנת 30% (+3 variants) + גבינה לאבנה 5% are withheld because the
   **Shufersal source panel itself omits total fat/protein/carbs** (verified on the live page P_554969). run_002's
   literal "0/57 insufficient" was an **artifact of the EV-029 bug** mislabeling the saturated row as total fat,
   making partial panels look complete. Exposing them is correct (parallels run_yogurt_003).

**Guards honored:** engine unmodified; no published/frozen scores changed; CLAUDE.md frozen invariants untouched;
constructs are label-observable classification/disclosure layers; frontend package NON-AUTHORITATIVE and NOT promoted.

**Handed to Nutrition** (grade-publication sign-off — the only remaining gate to live; `blocks_live`):
`factory_run_003/NUTRITION_SIGNOFF_REQUEST.md` (5 explicit decisions: A-ceiling withhold, corrected per-pool grades,
score-shift acceptance, sparse culture credit, 5 partial-panel withholds).

**Proposing RETURNED.** Only the Central Controller records CLOSED. (Downstream LIVE re-scrape/re-score of maadanim
+ hummus on the same EV-029 fix remain separate tasks per the 142A follow-ups — out of scope here.)

### Nutrition sign-off — APPROVED-FOR-PUBLICATION (Nutrition Agent, 2026-06-02)

Stage-6 grade-publication gate **PASSED**. All 5 decisions **APPROVED**, verified against traces
(`factory_run_003/NUTRITION_SIGNOFF_VERDICT.md`):
1. A-ceiling withhold of גבינה טבורוג 5% (82.0) — **correct** (trace fails C1 added-sugar, C2 stabilizers/sorbate,
   C3 not culture-credited, C4 structural-D); no clean live-culture SKU qualifies for A in this corpus.
2. Corrected per-pool grades — **approved** (cream-cheese 52.0/C confirmed via sat-fat red-label cap + HP penalty).
3. Score shift vs run_002 — **approved** as corrected-fat truth.
4. Sparse EV-015 culture credit (3/54) — **approved** as truthful coverage.
5. 5 transparency-tier withholds — **approved** (trace 554969: panel genuinely omits macros).

**One mandatory doc fix it caught + I applied:** engine is **0.4.1** (algorithm_version per `trace_writer.py:15`;
TASK-144 EV-026/027/028), NOT 0.4.0. Both run_002 and run_003 ran on 0.4.1, so "engine unchanged between runs"
holds — only the label was wrong. Corrected across all run_003 artifacts. **Display conditions:** labaneh n=1
standalone; ship the 2 PO-approved Sec 6.4 disclosure notes. D7 Product co-sign NOT triggered (no scoring rule
changed) — this is the D13 publication gate.

**State for the Controller:** all TASK-142 DoD gates MET and Nutrition has signed. **Ready for the Central
Controller to record CLOSED.** Promotion of factory_run_003 to the LIVE frontend (flip `authoritative` /
`promoted_to_frontend`) is a separate Product/Controller act — the package stays NON-AUTHORITATIVE until then.
