# BSIP2 Spread Subtype Calibration Assessment v1

**Task:** TASK-089
**Owner:** Chief Nutrition Officer
**Assigned agent:** CE (Claude Code — Intelligence & Content)
**Date:** 2026-05-31
**Constraint:** Evaluation only. **No BSIP2 changes were made.** This document recommends; it does not implement.

---

## Executive summary

| Question | Finding |
|----------|---------|
| Is the pepper-spread result a genuine modeling limitation? | **Yes — partially.** It exposes a real *category prior*, not a data bug or a one-off. |
| Should vegetable spreads be a distinct BSIP2 subtype? | **Yes, for calibration purposes.** They are physiologically distinct from legume spreads on the exact axes BSIP2 weights most heavily. |
| Which dimensions break? | `nutrient_density`, `protein_quality`, `satiety_support` — the three protein/fiber-driven dimensions (combined weight **0.31**). `whole_food_integrity` and `processing_quality` add NOVA drag. |
| Recommendation | **B — Introduce subtype-aware expectations** within the existing `sauce_spread` category. Not a separate scoring profile (C); not status-quo (A). |

**One-line diagnosis:** `sauce_spread` is calibrated around a *legume* archetype (hummus/tahini), where protein density is the headline virtue. Vegetable spreads share the category but not the archetype: they are intrinsically low-protein, low-fiber, low-calorie condiments. BSIP2 reads that absence as nutritional weakness rather than as a different — and legitimate — food role.

---

## 1. How the two subtypes are currently handled

Both legume and vegetable spreads enter the **same** `sauce_spread` category:

- **Router** (`router_v2.py`): `חומוס` (0.85), `טחינה` (anchor → `whole_food_fat`/`tahini`), `ממרח` (0.65), `רוטב` (0.90) and friends all resolve to `sauce_spread`. Roasted-pepper, matbucha, and eggplant items have no anchor of their own; they land in `sauce_spread` via `ממרח`/ingredient signals.
- **Scoring** (`score_engine.py`): scoring keys off `cat_result["category"]` **only**. There is exactly one `sauce_spread` calorie-density table and one global `DIMENSION_WEIGHTS` vector applied to everything in the category.

Critically: **the router already emits `category_subtype`** (e.g. `tahini`, `peanut_butter`, `cottage`), and every other shelf — snacks, yogurt, cereals, maadanim — infers subtypes during batch runs. But `score_engine.py` never reads `category_subtype`. **The plumbing to carry a subtype into scoring exists end-to-end except for the final consumption step.** This materially lowers the cost of Recommendation B.

---

## 2. Why the pepper spread lands at D — traced

Case study: **ממרח פלפלים קלויים**, BSIP2-native **43 / D**. Category-normalized expectation: **50–57 (C)**.

Using the closest corpus analogue (`סלט פלפלים קלויים`, `bsip1_7290104721533`): kcal 32, protein 0.8 g, fiber n/a→0, fat n/a→neutral, sugar n/a→0, sodium 397 mg; ingredients = roasted pepper 92%, vinegar, water, salt, spice blend, garlic, potassium sorbate (preservative), xanthan (stabilizer).

Dimension trace (illustrative; NOVA-4 / 2-additive reading — exact NOVA & source assumptions move the total ±4):

| Dimension | Weight | Score | Weighted | Driver |
|-----------|:-----:|:-----:|:--------:|--------|
| processing_quality | 0.15 | 35 | 5.25 | NOVA proxy (preservative + stabilizer) |
| **nutrient_density** | 0.15 | **2.6** | **0.39** | protein 0.8 g + fiber 0 g |
| calorie_density | 0.15 | 90 | 13.50 | 32 kcal — excellent |
| glycemic_quality | 0.12 | 90 | 10.80 | ~no sugar — excellent |
| **protein_quality** | 0.10 | **3.2** | **0.32** | protein 0.8 g |
| additive_quality | 0.10 | 64 | 6.40 | 2 additive markers |
| **satiety_support** | 0.06 | **19.2** | **1.15** | (protein×3 + fiber×5)/kcal |
| fat_quality | 0.08 | 50 | 4.00 | fat absent → neutral |
| regulatory_quality | 0.05 | 95 | 4.75 | no Israeli red labels |
| whole_food_integrity | 0.04 | 30 | 1.20 | NOVA proxy |
| **Weighted total** | 1.00 | | **≈47.8** | (→ D; the task's 43 sits within the NOVA/source band) |

**No cap or penalty binds** (NOVA-4 cap = 68; far above the score). No floor applies (not NOVA-1/whole-food-fat). The score is **purely the weighted dimension sum** — i.e. this is the model's honest opinion, not a guardrail artifact. That is what makes it diagnostic.

### The structural gap vs. a legume spread

Same trace for a representative hummus (`חומוס עם טחינה צבר`, kcal 196, protein 8.0 g):

| Dimension | Pepper spread | Hummus | Ratio |
|-----------|:-------------:|:------:|:-----:|
| nutrient_density | **2.6** | 26.0 | 10× |
| protein_quality | **3.2** | 34.0 | 10× |
| satiety_support | **19.2** | 49.0 | 2.5× |
| calorie_density | 90 | 75 | pepper *higher* |
| glycemic_quality | 90 | 90 | tie |
| regulatory_quality | 95 | 95 | tie |

The **entire** score separation between the two subtypes comes from the three protein/fiber-driven dimensions. On every axis a consumer would actually care about for a vegetable condiment — calorie density, glycemic load, additive burden, regulatory cleanliness — the pepper spread *matches or beats* hummus. It loses ~9–10 weighted points it can never recover because it is a vegetable, not a legume.

**This also explains the task's observation that ingredient-count and fiber corrections have minimal impact.** Fiber feeds `nutrient_density` (35% sub-weight) and `satiety_support`, but the dominant drag is the *protein* term in `nutrient_density` (65% sub-weight) and the whole of `protein_quality`. No realistic fiber value rescues a 0.8 g-protein food. The lever is protein-centric, and protein is the one thing a roasted pepper structurally cannot have.

---

## 3. Dimensions that become problematic for vegetable spreads

| Dimension | Problematic? | Why |
|-----------|:-----------:|-----|
| **nutrient_density** | **Yes — primary** | 65/35 protein/fiber blend. A vegetable spread is penalized for lacking protein it is not expected to provide. Highest single weight (0.15). |
| **protein_quality** | **Yes — primary** | Scores a food on protein grams it is categorically not a source of. Asking a pepper spread for protein quality is a category error. Weight 0.10. |
| **satiety_support** | **Yes — secondary** | `(protein×3 + fiber×5)/kcal`. Low-protein/low-fiber/low-kcal foods score low even though, per *serving*, no one expects a condiment to be satiating. Weight 0.06. |
| **whole_food_integrity** | Partial | NOVA-driven. Vegetable spreads carry a preservative + stabilizer (shelf-stable jarred format), so they read NOVA-3/4 despite a whole-vegetable base ≥73–92%. Penalizes *format*, not *substance*. Weight 0.04. |
| **processing_quality** | Partial | Same NOVA root cause as above. Weight 0.15 — so the NOVA reading matters a lot. |
| calorie_density | No (over-rewards) | Vegetable spreads excel here; this is the dimension *propping the score up*. |
| glycemic_quality | No | Generally excellent for veg spreads. |
| additive_quality | Mostly fair | Genuine signal; 2 markers is a defensible, modest deduction. |
| regulatory_quality | No | Correctly clean for most veg spreads. |
| fat_quality | Neutralized | Usually returns neutral 50 (fat data absent) — neither helps nor hurts. |

**Net:** ~0.31 of total weight is structurally adverse to vegetable spreads, and a further ~0.19 (processing + WFI) is format-adverse. Roughly half the score is computed on axes where a vegetable condiment is constitutionally disadvantaged, and the dimensions where it genuinely excels are capped at 90–95.

---

## 4. Three candidate calibration models

All three keep the `sauce_spread` category intact and operate **inside** it. None requires a new top-level category.

### Model 1 — Subtype-aware dimension re-weighting *(within `sauce_spread`)*
Detect a `vegetable_spread` subtype (router signal: tomato/pepper/eggplant base ≥ ~50%, no legume/tahini anchor) and apply a subtype-specific weight vector that **reallocates weight away from protein-centric dimensions** toward density/glycemic/regulatory. Illustrative shift: `nutrient_density` 0.15→0.10, `protein_quality` 0.10→0.04, redistribute the freed 0.11 to `calorie_density`, `glycemic_quality`, `additive_quality`, `regulatory_quality`.
- **Pros:** Targets the root cause exactly; legume spreads keep the current vector unchanged; leans on `category_subtype` plumbing that already exists.
- **Cons:** Two weight vectors in one category increases calibration surface; weight vectors must still sum to 1.0 and be re-validated.

### Model 2 — Subtype expectation floor / "category-appropriate" neutralization
Keep one weight vector, but for the `vegetable_spread` subtype **clamp the protein-driven dimensions to a neutral baseline** (e.g. `protein_quality` and the protein term of `nutrient_density` floored at ~45–50) so absence-of-protein reads as "not applicable," not "bad." Mirrors the existing pattern where `fat_quality` returns a neutral 50 when fat is absent/structurally empty (SRC-04) — a precedent already in the engine.
- **Pros:** Minimal, conceptually consistent with existing neutralization logic; one weight vector; easy to bound and explain.
- **Cons:** Floors can over-correct (a genuinely empty product also gets the neutral); needs a guard so it doesn't lift truly poor items.

### Model 3 — Subtype-specific calorie-density / expectation table only
Leave dimensions and weights alone; add a `vegetable_spread` row to the calorie-density and grade-normalization expectations so the *output band* is mapped to the subtype's realistic distribution (the 50–57 expectation in the brief). Effectively a post-hoc normalization layer rather than a dimension fix.
- **Pros:** Smallest code change; lowest regression risk; reversible.
- **Cons:** Treats the symptom (output band) not the cause (protein prior); a normalization that lifts scores without changing the underlying signal is harder to defend editorially and risks masking real differences *within* the vegetable-spread subtype.

---

## 5. Impact evaluation

| Corpus / property | Model 1 (re-weight) | Model 2 (neutral floor) | Model 3 (output band) |
|-------------------|--------------------|------------------------|----------------------|
| **Hummus corpus** | **No change** (legume vector untouched) | **No change** (floor only fires on veg subtype) | No change |
| **Vegetable-spread corpus** | Lifts ~+7–14 pts; pepper/matbucha/eggplant move D→C as expected | Lifts ~+6–10 pts; tighter, more uniform | Lifts to target band by construction |
| **Category comparability** | Preserved *if* both vectors are co-validated; risk = two scales drift apart over time | Best preserved (one scale, subtype reads N/A not 0) | Weakest — two output mappings can desync from the dimension signals |
| **Within-subtype discrimination** (good vs. bad veg spread) | Preserved | Slightly compressed (floors flatten the low end) | At risk (band remap can flatten) |
| **Regression surface** | Medium | Low | Lowest |
| **Editorial defensibility** | High (transparent: "judged on appropriate axes") | High (consistent with SRC-04 neutralization) | Lower ("we lifted the band") |
| **Governance footprint** | New calibration entry; subtype detection rule | New floor rule + subtype detection | Normalization table; no dimension change |

**Cross-cutting risks for any option:**
1. **Subtype detection accuracy.** A `vegetable_spread` detector must not catch hummus-with-pepper-topping (e.g. `חומוס עם מטבוחה`, `חומוס עם חריף`) — these are legume-primary and should keep the legume vector. Use **base-ingredient share + legume/tahini anchor absence**, not mere presence of "pepper."
2. **Missing-data interaction.** Much of the veg-spread corpus has null fat/fiber/sugar (display gap noted in `maadanim_corpus_report_v1` / shelf nulls). Any model that leans on fiber will under-deliver until BSIP1 panels are complete; this favors Model 1 or 2 over fiber-dependent fixes.
3. **Don't over-lift.** A vegetable spread with heavy added sugar (matbucha lists `סוכר לבן`) or high sodium should *not* be rescued into B. Keep `glycemic_quality`, `additive_quality`, and `regulatory_quality` at full strength so the subtype still discriminates internally.

---

## 6. Recommendation

**B — Introduce subtype-aware expectations**, implemented as **Model 1 (subtype-aware re-weighting) with a Model 2 neutralization guard**, scoped to a new `vegetable_spread` subtype inside `sauce_spread`.

Rationale:
- The pepper-spread result is a **genuine modeling limitation**, not an outcome to preserve. BSIP2 is penalizing a vegetable for not being a legume — a category prior, not a nutritional fact. So **A (keep current) is rejected**: the D grade is an artifact of archetype mismatch, and the model's own trace shows no cap/penalty/floor justifying it.
- **C (separate scoring profile) is over-engineered.** Legume and vegetable spreads share calorie-density behavior, glycemic behavior, additive logic, and regulatory thresholds. Only the protein/fiber expectation differs. A full second profile duplicates everything to fix one axis and doubles long-term calibration burden. The category is the right unit; the *expectation* is what must become subtype-aware.
- **B is the smallest change that fixes the cause**, reuses the `category_subtype` field the router already emits, and keeps the hummus corpus bit-for-bit unchanged.

Suggested guardrails for the eventual (separately-approved) implementation:
1. Detect `vegetable_spread` by **base share + anchor absence**, never by topping keywords.
2. Re-weight away from `protein_quality` / protein-term of `nutrient_density`; **do not touch** `glycemic_quality`, `additive_quality`, `regulatory_quality` (these keep the subtype honest).
3. Validate that no hummus/tahini item changes score (regression gate on the existing `sauce_spread` corpus).
4. Register the deviation in the **Exception Registry** before shipping — two weight vectors in one category is a deliberate, bounded deviation that must be documented.

---

## 7. Open items for the Chief Nutrition Officer

- **Confirm the editorial intent.** Should a clean, low-calorie roasted-pepper spread be a C (a fine everyday vegetable condiment) or should the framework hold that *all* spreads are judged on protein contribution? B only makes sense under the former. This is a values call, not a code call — it belongs to the CNO.
- **Reconcile the 43 vs. 64 display gap.** The BSIP2-native score in the brief is 43/D, but `hummus_frontend_v3.json` shows the analogue pepper item at 64/C. Before any recalibration, confirm which number is canonical and whether a frontend/partial-data adjustment is already silently doing some of this work (which would change the size of the fix).
- **Decide subtype boundary.** Where do tomato-based (matbucha), pepper-based, and eggplant-based spreads sit — one `vegetable_spread` subtype, or finer? The corpus supports one; finer splits await evidence.

---

*Prepared under the BSIP2 evaluation mandate. No constants, weights, tables, or engine logic were modified. Implementation, if approved, is a separate task and requires an Exception Registry entry.*
