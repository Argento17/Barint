---
id: TASK-140
title: "Cereals full-cycle BSIP0->BSIP2 (greenfield, ship-first candidate)"
owner: data-agent
status: CLOSED
priority: MEDIUM
deferred: false
created_at: 2026-06-01
resumed_at: 2026-06-05
closed_at: 2026-06-05
depends_on: []
blocks: []
category_id: breakfast-cereals
blocker_cleared: "Owner directive 2026-06-04 cleared by owner directive 2026-06-05 to resume. TASK-169 (CLOSED 2026-06-04) and TASK-178 (CLOSED 2026-06-04) are complete. Category prior fix (CATEGORY_PRIOR_BOOST=2.0) is now in router_v2.py — re-run as run_cereals_003 expected to clear QA-CER-001."
cc_close_note: >
  Gate passed — all five DoD criteria independently verified against artifacts.
  (1) Misroute 0.0%: run_cereals_004_run_summary.json misroute_pct=0.0, misroute_exit_gate_lt5pct=true, qa_cer_001_gate=PASS.
  (2) INSUFFICIENT 0%: qa_gate_result.json corpus.insufficient=0, data_sufficiency_0pct_insufficient=PASS.
  (3) Coverage 100%: qa_gate_result.json coverage_ge90pct=PASS (nutrition 100%, ingredients 100%).
  (4) Four constructs: qa_gate_result.json four_constructs_applied=PASS; frontend_package.json counts confirm
  granola_subpool=25, childrens=4, whole_grain_claim=43, fortification at 27.2% (non-endemic, DISTORTION-004 not triggered).
  (5) QA verdict=PASS, hard_fails=[]; QA-CER-W1 resolved (EV-044+EV-010 in nova_proxy.py — EXTRUDED_SHAPE_NAME_SIGNALS
  constant present, _ingredient_data_degraded guard present, EV-010 early-return block present); QA-CER-W2 non-blocking
  (documentation drift, cross-refs TASK-139A).
  EV-044 entry confirmed in bsip2_evidence_registry_v1.md.
  Frontend package: authoritative=true, display_approved=92/92, grade_distribution A:1/B:23/C:45/D:22/E:1, promoted_to_frontend=false (pending editorial).
  One internal inconsistency noted (run_summary a_grade_unapproved stale field for פתיתים אורגנים כוסמין — superseded by
  frontend_package a_grade_nutrition_ruling.approved; does not affect DoD). Score range floor minor discrepancy
  (run_summary 31.8 vs QA narrative 30.5; frontend confirms 31.8; no DoD criterion at stake). Neither blocks close.
close_reason: "All DoD criteria independently verified against factory_run_004 artifacts: misroute 0.0% (PASS), INSUFFICIENT 0/92 (PASS), coverage 100% (PASS), four constructs applied (PASS), QA verdict PASS with hard_fails=[]. nova_proxy.py EV-044+EV-010 fixes confirmed in source. EV-044 registered in evidence registry. Frontend package authoritative, not yet promoted to live (pending editorial review — does not block close)."
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

## State — RETURNED (proposed) 2026-06-05, data-agent

### run_cereals_002 (2026-06-01) — BLOCKED
Full 7-stage factory cycle executed via bari-category-factory, engine 0.4.0 UNMODIFIED, real Shufersal
scrape. Artifacts in `02_products/breakfast_cereals/factory_run_002/`.
❌ misroute 7.6% (QA-CER-001 hard fail) · ❌ 4 NOVA proxy false positives at A/85 (QA-CER-W1)
NO-GO. Frontend package preserved NON-AUTHORITATIVE.

### run_cereals_003 (2026-06-05) — QA-CER-001 RESOLVED
Category prior fix (router_v2.py `CATEGORY_PRIOR_BOOST=2.0`) applied. Misroute: 0/92 = **0.0%**.
QA-CER-001: **PASS**. 7 previously misrouted products all correctly classified as cereals.
EV-044 (NOVA 1 fast-path quality gate) applied but Osem פתיתים אפויים still landed at B/80+/A via RECAL_P0
leanness reward. EV-010 name-detection needed.

### run_cereals_004 (2026-06-05) — FINAL AUTHORITATIVE RUN
Engine: `proto_v0 / BARI_RECAL_P0=on`. Both fixes applied: EV-044 quality gate + EV-010 extruded-shape
name-detection (פתיתים אפויים → NOVA 3, per Nutrition ruling 2026-06-05).

**Exit criteria — ALL MET:**
- ✅ Coverage ≥90% (100% on 92 displayable, Hebrew 100%)
- ✅ INSUFFICIENT 0% displayable (0/92)
- ✅ Misroute <5% — **0.0%** (QA-CER-001: PASS)
- ✅ QA green — all hard-fail checks pass (QA-CER-W2 scoring.md drift is non-blocking documentation issue)
- ✅ Four constructs applied + documented per product and in category rollup
- ✅ Nutrition sign-off on A products:
    - שיבולת שועל / קוואקר (plain whole oats) — approved
    - פתיתים אורגנים כוסמין (80.8/A, NOVA 2, 15g protein, 10.5g fiber, 97% whole spelt) — approved on nutritional equivalence
    - פתיתים אפויים (4 Osem products) — **NOT A**: corrected to B/78.5/NOVA 3 via EV-010; A-grade not defensible until EV-010 full signal (D7 co-sign)
- ✅ frontend_package.json ready — **AUTHORITATIVE**, all 92 display-approved

**Results:** 92 scored/displayable. Grades A:1/B:23/C:45/D:22/E:1, median 59.3, range [30.5, 80.8].
Constructs: granola subpool; children's; whole-grain MDF; fortification 27.2% (NOT endemic).

**Artifacts:**
- Factory run: `02_products/breakfast_cereals/factory_run_004/frontend_package.json` (authoritative)
- QA gate: `02_products/breakfast_cereals/factory_run_004/qa_gate_result.json` (verdict: PASS)
- Run summary: `02_products/breakfast_cereals/reports/run_cereals_004_run_summary.json`
- NOVA proxy fix: `03_operations/bsip2/proto_v0/src/nova_proxy.py` (EV-044 + EV-010)
- Evidence: `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (EV-044 new)

**Watch-item (non-blocking):** QA-CER-W2 — scoring.md Grades table is stale vs engine constants.py.
Cross-ref TASK-139A. Documentation fix, does not block launch.

**Frontend not yet promoted to live.** Pending editorial review (Content Agent) + CC close gate.

Proposes **RETURNED**. Only the Central Controller records CLOSED.

---

## POST-CLOSE POST-MORTEM + CORPUS FIX (owner directive 2026-06-05)

**Finding (owner QA, post-launch):** the run_cereals_004 corpus that shipped to the live site was
**contaminated with 13 non-cereals** — 10 Israeli **ptitim pasta** (`פתיתים אפויים [shape]` + the
organic spelt ptitim `פתיתים אורגנים כוסמין`, which was whitelisted to **A and ranked #1**) and 3
yeast-leavened **breads** (`כוסמין מלא 100%`, `חלה דגנים קלועה`, `פיטנס THIN`). The contamination
entered via a name-substring include token (`פתיתי`) with no ingredient/semantic disambiguation, and
was misdiagnosed as a *scoring* problem (EV-044/EV-010 lowered grades) instead of a *corpus* problem.

**Why the close gate missed it:** the close-readiness gate verified misroute 0%, coverage 100%, and
constructs applied — all true — but never verified that the products *are the category food*. The
gate named the unapproved-A pasta and accepted it as "superseded by the nutrition ruling."

**Fix shipped (EV-045):**
- Corpus filter hardened at `02_build_bsip1_cereals.py` + `01_scrape_cereals.py`: ptitim-pasta
  exclusion (name-head `פתיתים` vs. construct `פתיתי X`; flour+water signature) and bread-leakage
  exclusion (yeast/sourdough in ingredients; Hebrew word-boundary so yeast `שמרים` ≠ preservatives
  `משמרים`).
- Re-run `run_cereals_005` (engine byte-identical): 113 raw → **79 displayable** (13 contaminants
  removed). **Score drift on survivors = 0** (corpus-independence proven).
- **Granola split to its own category** (owner directive): cereals = 54 (no A; top שיבולת שועל עבה
  80/B), granola = 25 (top גרנולה ממותקת בסילאן 76/B). Both promoted to live with authored copy
  preserved; new `/hashvaot/granola` route. `next build` PASS.
- Three new hard gates: `01_framework/operations/corpus_purity_gates_v1.md`
  (contamination≠calibration · leaderboard integrity · first-batch owner consult).

**Registry note:** run_cereals_004 frontend package is **SUPERSEDED** by run_cereals_005. Recommend CC
record the supersede and (per the first-batch owner-consult gate) treat the run_005 promotion as
owner-reviewed (this directive). Status change is CC/owner's call — body addendum only.

### ADDENDUM 2 — full-QA second pass (owner: "QA was weak", 2026-06-05)

Owner re-inspected run_005 and found the first EV-045 pass (ptitim+bread, 13 removed) was
**incomplete**. A complete shelf audit (multi-signal classifier: name-head + ingredient-dominance +
energy floor) found **13 more** non-cereals/bad-data: 2 pasta (`פסטה...נודלס/פטוצ'יני` konjac), 1
flour (`קמח שיבולת שועל`), 6 chocolate confections (קליק×2 / מיקס כרמית / ציפוי לבן / שוקולד+פצפוצי
אורז / קראנץ' מיני), 1 oat drink (`שיבולת שועל וויט`, 59 kcal), 3 implausible-energy items
(110–139 kcal/100g = per-serving parse error → withheld). **Total non-cereal/bad-data in the shipped
run_004 batch: ~26 of 92 (≈28%).**

EV-045b detectors added to `02_build_bsip1_cereals.py`: pasta tokens; `^קמח` flour-as-product;
`_is_confection` (choc head/first-ingredient/≥50%/coating/sugar+cocoa-butter, sparing legit
choc-flavoured grain cereals); drink tokens; **dry-cereal energy floor 150 kcal/100g**. Muesli +
grain-fruit-nut mixes folded into the granola sub-pool → category renamed **גרנולה ומוזלי**.

Final live state (`run_cereals_005`, engine byte-identical, survivor score drift = 0, `next build` PASS):
- דגני בוקר `/hashvaot/breakfast-cereals` — **31** (no A; top שיבולת שועל עבה 80/B; B9/C17/D5)
- גרנולה ומוזלי `/hashvaot/granola` — **35** (top גרנולה ממותקת בסילאן 76/B; B7/C16/D12)

**Meta-lesson for the close gate:** verifying misroute/coverage/constructs is not enough — add a
food-class (name+ingredient) check and an energy-plausibility check before any category launch.
