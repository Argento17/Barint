# TASK-144 — GO Score Diagnosis

**Product:** יופלה GO מועשר בחלבון (`bsip1_maadanim_7290110321031`)
**Live score:** 70/B (frontend rounds 69.6 → 70) · engine 0.4.0 · confidence verified (90/high)
**Trace:** `02_products/maadanim/bsip2_outputs/run_maadanim_001/products/bsip1_maadanim_7290110321031/bsip2_trace.json`
**Owner:** nutrition-agent · **Status:** diagnosis only, no score/engine change (frozen per TASK-136 / CNO invariants)

---

## A. Where the points are lost — exact breakdown

The 70 is **NOT a cap and NOT a dessert ceiling.** The binding cap (`NOVA_PROXY_3_PROCESSED` = 87) fires but is **non-binding** — the raw weighted dimension sum (69.58) sits below it. No penalty fired, no floor applied, no confidence ceiling. **The score is lost entirely inside the dimension scores.**

| Dimension | Score | Weight | Contribution | Diagnosis |
|---|---|---|---|---|
| processing_quality | 65 | 0.15 | 9.75 | **NOVA 3** → 65 (NOVA 1=95, 2=85). Costs ~3.0 pts vs NOVA 2. |
| nutrient_density | **32.5** | 0.15 | **4.88** | protein 10g→50, **fiber absent treated as 0→0**, weighted 0.65×50 + 0.35×0 = 32.5. The single biggest loss. |
| calorie_density | 85 | 0.15 | 12.75 | 72 kcal, dessert table. Fine. |
| glycemic_quality | 90 | 0.12 | 10.80 | sugar penalty 0. Fine. |
| protein_quality | 42.5 | 0.10 | 4.25 | 10g→base 50, **source="mixed"×0.85**→42.5. Dairy protein mis-typed. |
| additive_quality | 100 | 0.10 | 10.00 | 0 additives. Correct. |
| satiety_support | 100 | 0.06 | 6.00 | Correct. |
| fat_quality | 50 | 0.08 | 4.00 | sat-fat absent → neutral 50 (not penalized, not credited). |
| regulatory_quality | 95 | 0.05 | 4.75 | No red labels. Fine. |
| whole_food_integrity | 60 | 0.04 | 2.40 | NOVA 3 base 60 (NOVA 1=100, 2=85). |
| **Total** | | | **69.58** | |

### Root cause — a single upstream data error propagates into three dimensions

The trace shows `ingredient_count: 8` and an 8-item `ingredient_list`. **Only the first three are real ingredients** (`חלב`, `חלבוני חלב (7.4%)`, `אבקת חלב`). Items 4–8 are **OCR bleed** — the nutrition panel and the site disclaimer captured as phantom "ingredients":
> "...20 גרם חלבון בגביע", "...10.7 גרם חלבוני מי גבינה", "9.3 גרם קזאינים... ערכים תזונתיים 100 גרם 72 קל...", "אין להסתמך על הפירוט המופיע באתר", "יתכנו טעויות או אי התאמות", "יש לקרוא את המופיע על גבי אריזת המוצר..."

This 3-real-ingredient product is read as having **8 ingredients**, which triggers, in `nova_proxy.py:117`:
```python
elif additive_count >= 1 or added_sugar_ct >= 1 or ing_count > 5:
    level = 3   # "Some processing signals but not ultra-processed"
```
With **0 additives and 0 added sugars**, the *only* thing forcing NOVA 3 instead of NOVA 2 is `ing_count > 5` — a count inflated purely by OCR noise. NOVA 3 then cascades:
- `processing_quality` 85→**65**
- `whole_food_integrity` 85→**60**
- caps the score at 87 (harmless here, but real)

The other two losses are structural, not data:
- **fiber-absent-as-zero:** `score_nutrient_density` reads missing fiber as `0` and weights it 35%. A dairy product *has no fiber by nature* — penalizing its absence as if fiber were expected drags nutrient_density from a protein-justified 50 down to 32.5. **Largest single contributor to the gap (≈2.6 weighted pts).**
- **protein source "mixed" ×0.85:** the enricher typed the protein source as `mixed` (basis: `אבקת חלב`). For a 100%-dairy product (whey + casein) this 15% quality haircut is not justified; dairy is a complete, high-DIAAS protein.

---

## B. Verdict — is 70/B justified?

**No — 70/B understates this product, but the corrected, honest score is ~76–77/B, not 85/A.**

Two distinct findings:

1. **There is a genuine defect.** The NOVA 3 classification is wrong-on-the-data: it is driven by an OCR-inflated ingredient count, not by any real processing signal. The trace's own positiveSignals confirm zero additives/sugar/stabilizers. A clean 3-ingredient dairy product should read **NOVA 2**, and the absent-fiber penalty mis-models a naturally fiber-free food. These are **bugs/mis-modelling**, and fixing them is defensible without touching the dairy-A philosophy.

2. **But the PO's 85/A target is not reachable by bug-fixes, and should not be granted.** Modelled corrected scenarios:

| Scenario | Score | Grade |
|---|---|---|
| Current (live) | 69.6 | B |
| Fiber-not-applicable only | 72.2 | B |
| NOVA 3→2 only | 73.6 | B |
| NOVA→2 **+** fiber-not-applicable | 76.2 | B |
| **+ dairy protein source (drop ×0.85)** | **77.0** | B |

All three legitimate corrections together land at **~77/B**. To reach 80/A this product would additionally need credit it has **not earned**: it has **no confirmed live culture** (`has_fermentation: false`), so it does **not** satisfy the A-condition. Its fat is neutral-scored (no sat-fat data), and it is a **reconstituted/enriched** matrix (added milk-protein powder + milk-protein isolate), not an intact dairy matrix.

**70/B is too low by ~6–7 points; ~77/B is the truthful score; 85/A is not justified.**

---

## C. Reconciliation with TASK-139A / RULING-DAIRY-A-01 / DEC-005

RULING-DAIRY-A-01 (139A, Product co-signed 2026-06-01) is the governing precedent and it **directly constrains this case.** A is reachable by dairy **only** under the C1–C6 condition:
> no added sugar · no engineered additives · **live culture confirmed AND credited** · **intact dairy matrix (reconstituted base excluded)** · correct dairy routing · verified confidence. **Earned by score; no grant, no floor, no format credit.**

GO satisfies C1, C2, C5, C6 — but **fails C3 (no live culture: `has_fermentation: false`) and fails C4 (it is a protein-enriched/reconstituted matrix: `אבקת חלב` + `חלבוני חלב`, not intact).** Under the governing ruling, **GO is correctly excluded from A.** Granting it 85/A would contradict 139A and would re-introduce exactly the "A-by-format/A-by-grant" failure the ruling forbids.

**My recommendation does NOT contradict 139A — it is consistent with it.** I recommend correcting the *bugs* that wrongly suppress GO from its earned ~77/B, and explicitly **declining** the PO's 85/A. This is the same posture as the milk precedent (A is earned by clean intact matrix + credited fermentation, not by enrichment) and the snack-bar B-ceiling (B is a legitimate, honest ceiling for an enriched processed dessert).

If the PO still wants 85/A, that is a **philosophy change to 139A**, not a scoring patch, and must go back through joint Nutrition+Product re-ruling. I do not recommend it: a protein-fortified, culture-free, reconstituted dessert is, on Bari's architecture, a strong B — not the equal of intact whole milk.

---

## D. Proposed governed fix (per bari-bsip2-scoring-governance)

Three changes. **#1 and #2 are bug/mis-modelling fixes (high confidence, recommend). #3 is a calibration tweak (recommend). None grants A; all are evidence-grounded and reversible.**

### Fix 1 — Sanitize ingredient_count before NOVA inference (UPSTREAM, highest priority)
- **What:** Strip non-ingredient OCR bleed (nutrition-panel tokens like `ערכים תזונתיים`, `קל אנרגיה`, `מג נתרן`, gram-quantity fragments; site disclaimers like `אין להסתמך`, `יש לקרוא את המופיע על גבי`) from the ingredient list in BSIP1 enrichment / signal extraction, so `ingredient_count` reflects real ingredients. Then `ing_count > 5` in `nova_proxy.py:117` stops mis-firing.
- **Layer:** BSIP1 enricher / `signal_extractor.py` (data hygiene), not a scoring rule. This is the cleanest fix because it removes the *cause*, not the symptom.
- **Evidence basis:** EV (OCR-sanitization gap is a known open item in the robustness-sprint memory; ingredient-count integrity). No new scoring rule = no Tension-5 rule-budget cost.
- **Effect on GO:** NOVA 3→2; processing_quality 65→85, WFI 60→85. **+4.0 pts → ~73.6/B.**
- **Blast radius:** Affects *any* maadanim/dairy product whose ingredient list ate OCR noise. Re-run maadanim corpus to size it; likely small score lifts for a handful of clean products currently mis-flagged NOVA 3 on phantom counts. No product loses points. **Must re-run full maadanim batch + regression corpora.**
- **Rollback:** Revert the tokenizer filter; counts return to raw. Deterministic.

### Fix 2 — Fiber "absent vs. zero" for naturally fiber-free categories (nutrient_density)
- **What:** In `score_nutrient_density`, when fiber is **missing/not-applicable** for a dairy/dairy_protein category (where ~0 fiber is the expected, correct value — not a deficiency), score nutrient_density on **protein alone** rather than blending in a 0 fiber at 35% weight. Concretely: for these categories use protein-only `ps` (or re-normalize the 65/35 split to 100/0 when fiber is structurally not-applicable).
- **Layer:** Scoring (`score_engine.py`, dimension scorer). Activation scope: **gated to dairy / dairy_protein / dessert-dairy categories only** — do NOT apply where fiber absence IS a real deficiency (bread, cereal, bars).
- **Evidence basis:** EV registry — nutrient_density must not penalize the structural absence of a nutrient the food category is not expected to contain (parallels the whole-food-fat-floor logic: don't punish a food for not being something it isn't). Register as a new EV finding if not already covered.
- **Effect on GO:** nutrient_density 32.5→50.0. **+2.6 weighted pts.** Combined with Fix 1 → **~76.2/B.**
- **Blast radius:** All dairy/dessert-dairy products with absent fiber gain a few points; capped to the gated categories so bread/cereal/bars are untouched. Re-run those categories' regression to confirm no leakage. **Highest-care item** — must confirm activation gate is tight.
- **Rollback:** Remove the category gate; revert to flat 0.65/0.35 blend.

### Fix 3 — Dairy protein source typing (protein_quality) — calibration, optional
- **What:** When the protein source is **100% dairy** (whey + casein, milk-protein), type it `whole_food`/dairy-complete (factor 1.0) instead of `mixed` (0.85). The enricher currently types GO as `mixed` on basis `אבקת חלב`.
- **Layer:** Enricher protein-source classification + `source_factors` mapping.
- **Evidence basis:** dairy protein is complete/high-DIAAS; the 0.85 "mixed" haircut is for genuinely blended/uncertain sources, not pure dairy.
- **Effect on GO:** protein_quality 42.5→50.0. **+0.75 weighted pts.** Combined with Fix 1+2 → **~77.0/B.**
- **Blast radius:** Lifts pure-dairy products slightly; must NOT reclassify reconstructed *bar* isolates (F2/TASK-133B protects those — keep the matrix discount intact). Confirm no collision with PROTEIN_QUALITY_MATRIX_DISCOUNT. Smallest effect; can defer.
- **Rollback:** Revert source factor / classification.

**Net effect of all three on GO: 69.6 → ~77/B.** Grade stays B. A remains correctly out of reach (fails 139A C3/C4).

---

## E. Governance summary

- **Defect confirmed:** GO is suppressed ~6–7 pts below its earned score by an OCR-driven NOVA mis-classification + two mis-modelling choices (fiber-as-zero, dairy-as-mixed-protein).
- **70/B not justified; ~77/B is the truthful score; 85/A is NOT justified** and would contradict the governing RULING-DAIRY-A-01.
- **Recommend Fixes 1–3** (all evidence-grounded, all reversible, none grants A). **DEC-004 calibration-signoff** governs Fix 2/3 magnitudes; Fix 1 is data hygiene.
- **Do not execute under freeze.** TASK-136/CNO invariant lists "GO top-B" — the corrected score is still B, so the *grade* invariant survives, but the *number* changes (70→~77). Re-running is a numbers-versioning event requiring Central Controller + Product Owner sign-off and a fresh maadanim baseline freeze + QA.
- **Required validation before any execution:** `run_regression_check.py`, `run_router_regression.py`, full `batch_run_maadanim_001.py` re-run, plus dairy/bread/cereal regression to bound Fix 2's blast radius.
