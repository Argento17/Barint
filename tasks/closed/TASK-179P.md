---
id: TASK-179P
title: Glass Box W1.5 — DIAAS protein quality signal (Research table + Nutrition rule + Data wire)
owner: research-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
depends_on: [TASK-179]
blocks: [TASK-179Q]
category_id: null
roadmap_impact: true
work_type: execution
cc_reviewed: 2026-06-04
completed_at: 2026-06-04
cc_comments:
  - flag: fyi
    date: 2026-06-04
    note: >
      All 3 phases complete. QA PASS (independent run). Deliverables verified:
      diaas_source_table_v1.md (300 lines, 8 sources, Research + Nutrition Phase 2 rules + Product D7
      co-sign), EV-040 filed in evidence registry (Rule A +3 D2 credit for DIAAS ≥75 declared source /
      Rule B D5 annotation for undisclosed blends), score_engine.py updated with detect_diaas_signal()
      behind BARI_GLASSBOX_W15 (default OFF), verify_glassbox_w15_off_identical.py present.
      QA: 342 products (hummus 69 / maadanim 200 / snack 53 / golden_milk 20), 0 diffs flag-OFF.
      Rule A ON pilot: 25 genuine fires (23 maadanim, 2 milk), all whitelist-confirmed, grade
      letters unchanged. Frozen invariants: milk 85/A and snack 70/B both safe.
      Non-blocking notes: Rule B 0 fires (coverage gap — no pea+rice/תערובת חלבונים products in
      test corpus; D5 annotation-only so no score risk); ביצה pattern broad but match was genuine.
      Product D7 co-sign on +3: confirmed in diaas_source_table_v1.md Phase 2 Co-sign section.
      BARI_GLASSBOX_W15 may now be activated — awaits W1 flag flip (W1+W1.5 go live together,
      owner decision 2026-06-04).
summary: >
  W1.5 of Glass Box. Research builds an amino-acid completeness table for ~8 protein sources
  present on Israeli shelves (whey, casein, egg white, soy isolate, pea isolate, rice protein,
  oat protein). Nutrition defines a 2-rule disclosure-gated credit rule and co-signs as a new
  EV-### evidence entry. Data wires the detector into score_engine.py behind BARI_GLASSBOX_W15
  (flag OFF = byte-identical; flag ON = mild D2 credit for declared complete sources, D5/D6 flag
  for undisclosed "protein blend"). No grade movement until Nutrition + Product sign off.
  W1 flag flip (NEXT_PUBLIC_GLASSBOX_D5D6) deferred until W1.5 ships — both go live together.
---

# TASK-179P — Glass Box W1.5: DIAAS protein quality signal

Part of TASK-179 (Glass Box). Runs in parallel with TASK-179Q (W2 additive research) and
TASK-179R (W2 engagement gate spec). W1.5 ships together with the W1 flag flip.

## Scope

### Phase 1 — Research (research-agent)
Build `01_framework/glass_box/diaas_source_table_v1.md`:
- Sources to cover: whey protein, casein, egg white, whole egg, soy isolate, pea isolate,
  rice protein, oat protein (these are the ~8 sources that appear on Israeli shelves across
  hummus, maadanim, yogurt, snack bars).
- Per source: DIAAS score (USDA FoodData Central + literature client from TASK-170),
  limiting amino acid, completeness tier (complete = DIAAS ≥ 75 / incomplete = below).
- Sources: USDA FoodData Central API (wire via TASK-170 literature client or direct HTTP),
  FAO/WHO 2013 DIAAS reference, PubChem for cross-verification.
- Flag any source with contested or sparse evidence.

### Phase 2 — Nutrition rule (nutrition-agent)
Define the disclosure-gated D2 credit rule and co-sign:
- **Rule A (credit):** If product declares a specific protein source AND that source is
  complete (DIAAS ≥ 75 per table), award a mild D2 ingredient-evidence credit (magnitude
  to be determined by Nutrition, bounded to ≤ 0.5 grade band).
- **Rule B (flag, no penalty):** If product declares only "protein blend" / "מי גבינה" /
  undisclosed compound protein without source → D5 disclosure gap flag + D6 confidence
  downgrade; NO standalone quality deduction (consistent with DEC-006 Option B posture).
- Rule must be registered as EV-### in the BSIP2 evidence registry before any engine code
  ships. Nutrition files the evidence entry.
- Nutrition co-sign required; Product co-sign required for any rule that moves a grade.

### Phase 3 — Data wire (data-agent)
Wire the DIAAS detector into `03_operations/bsip2/proto_v0/src/score_engine.py` behind
environment flag `BARI_GLASSBOX_W15`:
- Flag OFF: byte-identical to engine-baseline-2026-06-04 (verify with verify script).
- Flag ON: apply Rule A credit and Rule B D5/D6 flag per Nutrition spec.
- Add a `verify_glassbox_w15_off_identical.py` script (mirrors `verify_glassbox_off_identical.py`).
- QA gate: QA agent runs OFF verification before Phase 3 is marked complete.

## Guardrails
- BARI_GLASSBOX_W15 flag OFF is non-negotiable until Nutrition + Product co-sign.
- Do not touch frozen invariants (milk run_005_headpin / snack ceiling 70/B / bread provenance).
- EV-### evidence registry entry must precede engine code (bari-bsip2-scoring-governance enforces).
- W1.5 ships together with W1 flag flip (NEXT_PUBLIC_GLASSBOX_D5D6=on) — not before.

## Deliverables
1. `01_framework/glass_box/diaas_source_table_v1.md` — Research
2. EV-### evidence registry entry — Nutrition
3. Updated `score_engine.py` with BARI_GLASSBOX_W15 detector — Data
4. `verify_glassbox_w15_off_identical.py` verification script — Data
5. QA OFF byte-identity confirmation — QA

## Return block (when complete)
- Research returns dossier to Nutrition for rule definition.
- Nutrition returns rule + EV-### to Data for wiring.
- Data returns with OFF byte-identity proof; QA verifies independently.
- Final return to orchestrator with all 5 deliverables confirmed.
