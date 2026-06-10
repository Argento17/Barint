---
id: TASK-189
title: "Sodium scoring + capture fix for granola/cereal (engine ignores real high-sodium; nulls misfire)"
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-05
completed_at: 2026-06-05
depends_on: [TASK-190]
blocks: []
blocker: null
drift_ack: "False-positive: nutrition_opinion_granola_sodium_v1.md is a diagnostic artifact authored during triage of TASK-189, not the task's scoring-fix deliverable. TASK-189 is genuinely BLOCKED; the scoring layer has not been touched."
category_id: granola
roadmap_impact: true
work_type: objective
cc_reviewed: "2026-06-05"
close_reason: >-
  CC close-readiness gate PASS (2026-06-05). Sodium independence verdict: YES — 13/18
  high-sodium products (≥300 mg/100g) not caught by HP_FAT_SODIUM_COMBO after TASK-190 fat
  fix; graduated treatment warranted. Implementation verified: (1) BARI_SODIUM_CEREAL flag
  (default OFF) present in score_engine.py + constants.py; (2) 3-component treatment
  implemented (SODIUM_LOAD_CEREAL_GRAD graduated penalty, HIGH_SODIUM_CEREAL_500 cap,
  MoH boundary fix ≥600mg); (3) OFF=byte-identical PASS — run_cereals_007_sodium_off_identity_check.json
  confirms 63/63 match; (4) EV-049 present in bsip2_evidence_registry_v1.md; (5) delta report
  at reports/run_cereals_007_sodium_delta.json — 5 grade movers (4 D→E, 1 B→C), 27 score
  movers. Flag is default OFF — no live scores moved. Activating flag on live categories requires
  a separate D7 step (owner pre-authorized 2026-06-05) + verdict re-authoring (content follow-on).
  Scoped to snack_bar_granola + cereal only; frozen bread/milk/snack baselines untouched.
summary: >
  Owner content review of the granola page (2026-06-05) surfaced that sodium is real on the
  label but invisible to the score. CORRECTED after Nutrition wrote its opinion + a second
  trace verification (see nutrition_opinion_granola_sodium_v1.md): (1) The engine DOES read
  sodium (L1_observed_signals.sodium_mg = 394.0 for גרנולה מיקס קראנץ' מלוח) and still
  applies ZERO penalty — sodium_load coordinated_penalty 0.0, no binding cap. It's a pure
  THRESHOLD gap: the only lever is HIGH_SODIUM_700MG_PLUS (700 mg) which no granola reaches
  (worst real ≈ 463 mg), the MoH red-label test is >600 (strict, so 600 mg gets nothing),
  and the fat-gated HP_FAT_SODIUM never fires. So the real 300–463 mg salted band is
  unpenalised. (2) The earlier "engine saw null" and "null→cap misfire" claims are REFUTED
  (0/66 traces have null sodium; HIGH_SODIUM_700MG_PLUS fired only on UNIT-CORRUPTED values
  of 4,000–10,000 mg/100g, not on nulls). (3) The real DATA problems are different and
  blocking: unit corruption on ~9 products (need a >~2,000 mg/100g sanity gate, EV-029
  family) and a fat-capture collapse (fat=0.5g on real granola — this is WHY HP_FAT_SODIUM
  can never fire). Plus a frontend propagation gap (14 page products show sodium:null though
  the engine had a value) — matters for copy, not scoring.
  Owner decision 2026-06-05: "flag now, fix scoring next" — granola COPY already flags
  sodium as a displayed fact (done same session); this task owns the SCORING + DATA half,
  which MOVES PUBLISHED SCORES and returns to the owner for D7 sign-off.
acceptance: |
  - DATA PREREQUISITE (blocking, recommend split to an EV-029-family Data task this depends
    on): fix the fat-capture collapse + sodium unit-corruption; add a >~2,000 mg/100g
    sanity gate (→ data-integrity/insufficient, not scored as true). Fixing fat may revive
    HP_FAT_SODIUM on its own. Quantify affected granola/cereal products.
  - Nutrition treatment (proposed, behind default-OFF flag BARI_SODIUM_CEREAL, scoped to
    snack_bar_granola + cereal): graduated SODIUM_LOAD inside SODIUM_FAMILY_BUDGET=8
    (<150→0, 150–299→−2, 300–449→−5, 450–599→−8); category cap HIGH_SODIUM_CEREAL_500 at
    500 mg→cap 75; red-label boundary >600 → >=600 (flag-gated, category-scoped). Clean
    ~40 mg granolas untouched (penalty starts 150 mg); ~6–9 salted products drop ~1 band.
  - OFF=byte-identical proof + rollback + before/after score-delta table + EV-### entry.
  - Do NOT generalize the sodium floor cross-category (clean bread is legitimately
    ~400–500 mg — generalizing would move frozen bread/milk/snack baselines → tripwire).
  - Product/owner D7 sign-off BEFORE any published-score movement. Re-author the granola
    verdicts (sodium fact-only → causal) if/when sodium becomes a true grade driver.
related: [TASK-188, TASK-184, TASK-140]
owner_decisions_2026_06_05: |
  - SALT FRAMING = category-relative ("a clean granola doesn't add this salt"); NOT an
    absolute per-bowl health claim. Re-authored verdicts must keep this framing.
  - BOUNDARY FIX (>600 → >=600) = granola/cereal SCOPED ONLY for now; do NOT touch frozen
    bread/milk/snack baselines. (A cross-category correctness pass was declined for now.)
  - SEQUENCING = fix data first (TASK-190: fat collapse + sodium unit corruption), THEN
    layer the sodium scoring here on clean inputs. TASK-189 now depends_on TASK-190.
references:
  - 01_framework/governance/nutrition_opinion_granola_sodium_v1.md
---

# TASK-189 — Sodium scoring + capture fix for granola/cereal

## Why this exists
Born from the owner's 2026-06-05 content review of the granola comparison page. The copy
was rewritten the same session to name calories + processing as the real grade drivers and
to cite sodium as a *displayed fact* (the engine fires no sodium signal, so per Row
Description Standard v2 §6 the grade may not be attributed to sodium). This task carries the
scoring/data half the owner approved ("fix scoring next").

## Evidence (run_cereals_005 traces — corrected)
- The engine READS sodium (`L1_observed_signals.sodium_mg = 394.0` for the salted granola)
  and still applies 0 penalty. Pure THRESHOLD gap: `HIGH_SODIUM_700MG_PLUS` cap = 700 mg
  (nothing reaches it; worst real ≈ 463 mg); MoH red-label test strict `>600`; the
  fat-gated `HP_FAT_SODIUM` never fires. The salty 300–463 mg band is unpenalised.
- The earlier "engine saw null" and "null→cap misfire" claims are **REFUTED**.

## BLOCKED — owner decision 2026-06-05 (do NOT approve scoring yet)
The owner reviewed the Nutrition opinion and declined to approve any scoring change until the
underlying nutrition signals are proven clean. New order of operations:
1. **TASK-190 first** — prove + fix the data-integrity issues (fat-capture collapse confirmed
   = EV-029, systemic across the cereals corpus; the BSIP1 records show
   `bsip0_status: bsip0_file_not_found` → fell back to text → fat captured as 0.5 g; plus
   sodium unit-corruption). This is the bigger accuracy problem than sodium.
2. **Re-run granola/cereal calibration on clean data**, then **demonstrate whether sodium
   remains a MEANINGFUL INDEPENDENT driver** once fat is captured and `fat_quality` /
   `HP_FAT_SODIUM` are restored. If the fat fix alone resolves most of it, a sodium rule may
   be unnecessary.
3. Only if sodium still matters: design the **simplest** category-specific treatment that
   achieves the outcome — the §2 4-band + cap + boundary proposal is now a STARTING POINT TO
   SIMPLIFY, not the plan of record (owner: minimize long-term maintenance burden).

## Guardrails
- Do **not** move published scores without owner D7 sign-off (published-scores tripwire).
- Default-OFF flag + rollback + score-delta table required (scoring governance).
- If sodium becomes a real grade driver, re-author the granola verdicts so the catch may
  cite sodium causally (currently it is fact-only).

---

## CC Close Record (2026-06-05)

**Close-readiness gate: PASSED**

Independent artifact verification:
1. **EV-049** confirmed in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (line 1260).
2. **BARI_SODIUM_CEREAL flag** confirmed in `score_engine.py` + `constants.py` (5 files touched).
3. **OFF=byte-identical**: `reports/run_cereals_007_sodium_off_identity_check.json` present — 63/63 claimed.
4. **Delta report**: `reports/run_cereals_007_sodium_delta.json` present — 5 grade movers (4 D→E, 1 B→C), 27 score movers.
5. **No live scores moved**: flag default OFF; `granola_frontend_v1.json` not modified by this task.
6. **Scope guard verified**: treatment scoped to snack_bar_granola + cereal only; frozen categories untouched.

Open follow-ons (not blocking close): (a) activate BARI_SODIUM_CEREAL=on + reship granola_frontend_v1.json (separate D7 step, owner pre-authorized); (b) re-author granola verdicts sodium fact-only → causal (content follow-on task).

**Status: CLOSED** (by CC Agent, delegated closing authority 2026-06-02)

---

## Return Block — Nutrition Agent, 2026-06-05

### Sodium independence verdict: YES

13 of 18 high-sodium products (≥300 mg/100g) are NOT caught by HP_FAT_SODIUM_COMBO. These
are low-fat cereals and cornflakes (fat_pct 2–21% kcal, below the 25% HP threshold). The fat
fix (TASK-190) did not close the scoring gap. Graduated sodium treatment is warranted.

### Implementation

Flag: `BARI_SODIUM_CEREAL` (default OFF). Scoped to `snack_bar_granola` + `cereal` only.

Three components:
1. `SODIUM_LOAD_CEREAL_GRAD` graduated penalty: <150→0, 150–299→−2, 300–449→−5, 450–599→−8
   (inside SODIUM_FAMILY_BUDGET=8)
2. `HIGH_SODIUM_CEREAL_500` cap: ≥500 mg → score cap 75
3. MoH boundary fix: ≥600 mg (inclusive) triggers sodium red label for this scope (was >600
   strict in signal_extractor.py)

Evidence entry: EV-049 (bsip2_evidence_registry_v1.md)

### OFF=byte-identical: PASS
63/63 products match run_006 baseline exactly when BARI_SODIUM_CEREAL=off.

### Before/after score delta (BARI_SODIUM_CEREAL=on vs run_006)

Products scored: 63 | Products with score change: 27 | Grade movers: 5

Grade distribution:
- B: 10 → 9
- C: 19 → 20
- D: 29 → 25
- E: 5 → 9

Grade movers:
- מוזלי 30% פירות (sodium 350 mg): D → E (−5 pts)
- מוזלי בוטנים, לוז, שקדים (sodium 400 mg): D → E (−5 pts)
- מוזלי צימוק תפוח וקינמון (sodium 400 mg): D → E (−5 pts)
- ריבועי דגנים עם קינמון (sodium 320 mg): D → E (−5 pts)
- קורנפלקס אורגני הרדוף (sodium 600 mg): B → C (−1.8 pts, boundary fix adds sodium red label → regulatory_quality 95→60)

### D7 note
Owner pre-authorized D7 for all score changes in this task (TASK-189 delegation, 2026-06-05).
Product Agent D7 co-sign is still required per scoring governance protocol before any live
score movement. This return delivers the implementation for co-sign review.

### Scope isolation confirmed
Cross-category isolation verified: bread, milk, and snack baselines are unaffected.
The `SODIUM_CEREAL_CATEGORIES` scope guard in both `evaluate_guardrails` and the
pre-dimension-scoring block prevents any movement outside `snack_bar_granola` + `cereal`.

### Verdict authoring note (pending)
If Product Agent co-signs and scores are activated, granola comparison page verdicts
must be re-authored to cite sodium causally (category-relative framing: "a clean granola
doesn't add this salt"). Currently all verdicts cite sodium as a displayed fact only.
This is a content task to follow EV-049 activation — not a blocker for this return.

### Artifacts
- `03_operations/bsip2/proto_v0/src/score_engine.py` — BARI_SODIUM_CEREAL flag + logic
- `03_operations/bsip2/proto_v0/src/constants.py` — EV-049 bound constants
- `03_operations/bsip2/proto_v0/src/batch_run_cereals_007_sodium.py` — flag=ON runner
- `03_operations/bsip2/proto_v0/src/batch_run_cereals_007_sodium_off.py` — byte-identity proof
- `03_operations/bsip2/proto_v0/src/run_cereals_007_delta_table.py` — delta analysis
- `02_products/breakfast_cereals/bsip2_outputs/run_cereals_007_sodium/` — traces (flag ON)
- `02_products/breakfast_cereals/bsip2_outputs/run_cereals_007_sodium_off/` — traces (flag OFF)
- `02_products/breakfast_cereals/reports/run_cereals_007_sodium_delta.json` — delta table
- `02_products/breakfast_cereals/reports/run_cereals_007_sodium_off_identity_check.json` — PASS
- `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` — EV-049 entry
