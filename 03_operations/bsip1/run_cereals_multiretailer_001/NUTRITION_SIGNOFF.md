# Nutrition Sign-off — run_cereals_multiretailer_001 (TASK-184)

**Reviewer:** Nutrition Agent
**Date:** 2026-06-05
**Scope:** 42 genuinely-new breakfast-cereal + granola/muesli products (Carrefour + Yochananof),
scored by the byte-identical BSIP2 engine (`BARI_RECAL_P0=on`, engine tag `engine-baseline-2026-06-04`).
**Mandate:** review/sign-off only. No scores changed, no engine touched, frozen invariants respected.
This is a Hard-Rule-1 review (no invented data) and Hard-Rule-2 review (no score change) — flags only.

---

## VERDICT: CONDITIONAL GO

The set is **GO for promotion EXCEPT the items flagged below**, which are **NO-GO** until resolved.
The grade *distribution* is defensible and consistent with run_005 philosophy. The problems are
concentrated, not systemic: one over-grade I will not stand behind (the category-high A), a
contaminant brand-line that leaked into the scored set, and a fairness artifact at the B/A boundary.

- **NO-GO (hold from live):** the 81.2/A granola; all savory/non-cereal Fitness-brand SKUs; the
  two `insufficient_data` rows (already non-displayable).
- **GO (defensible):** the remaining standard-cereal and genuine-granola rows (B/C/D/E), whose
  grades track their macros sensibly.

---

## 1. Grade defensibility scan (all 42)

I read every per-product trace (macros + dimension scores + caps + penalties + confidence). The
spine is sound: high-sugar/low-fiber refined cereals land C–E with the correct caps firing
(`כריות וניל חדש` 38.5g sugar / 0g fiber → 28.6/**E**, cap 63 then dimension-driven below it;
`Cereal` 42.9g sugar → 44.4/**D**, cap 55; `Honey Roasted` 22g sugar / 463mg sodium → 36/**D**).
Plain oats and oat-flakes cluster at the top of B (76.7 / 76.5 / 75 / 74.8) on clean macros
(8g fat, ~1g sugar, 9–13g fiber, 11–14g protein) — exactly where a whole-grain oat *should* sit:
strong but not excellent, consistent with the frozen "best ≠ excellent" framing. **No systemic
mis-grade.** Three specific issues below.

## 2. RULING on the category-high — "גרנולה בתוספת חלבון" (Telma, Carrefour) 81.2/A

**Ruling: the A is NOT defensible as published. FLAG — recommend hold / regrade to B band.**
This is *not* a request to change the score (Hard Rule 2); it is a withheld sign-off with reasoning.

Two separate concerns, only the first of which is about the macros:

**(a) The macro panel is honest and plausible — this is not a data error.**
Per 100g: protein 24.8, fiber 15.4, sugar 7.2, fat 10.3 (sat 2.2), sodium 46. Mass balance is
internally consistent (P+F+C = 79g, leaving ~21g water/ash; Atwater ~368–399 kcal brackets the
declared 399 kcal). A 24.8g-protein / 15.4g-fiber / 7.2g-sugar protein-fortified granola is a real,
commercially-plausible product. The engine's dimension scores (nutrient_density 94.7,
protein_quality 94.6, glycemic 92, satiety 100, additive 100) correctly reflect a genuinely strong
macro profile. **If this were a fully-evidenced product, an A would be philosophically permissible** —
cereals/granola carry no frozen A-ceiling (unlike snack bars at 70/B), and a low-sugar high-protein
granola is materially better than anything Shufersal stocked (prior ceiling 79.9/B). An earned-A on a
granola is *not* inherently a philosophy violation.

**(b) BUT the A rests on a panel with ZERO ingredient visibility, and it cleared the A boundary on a
single-field accident — that is the problem.**
- `ingredient_count = 0`, `ingredient_text_quality = missing`. The score is **100% macro-derived**.
  We are awarding the only A on the shelf — the single strongest public claim Bari will make in this
  category — to a product whose ingredient list we have never seen. We cannot see added-sugar sources,
  protein source (isolate vs whole-food — the engine *assumed* whole_food on "no isolate markers
  detected", which with a missing list is an assumption, not an observation), sweeteners, or additive
  burden. `processing_quality` (64) and `whole_food_integrity` (85) are running on a NOVA proxy with
  `nova_confidence = 0.2` (the trace itself carries `unresolved_flag: LOW_NOVA_CONFIDENCE`). An A is a
  claim of *architecture*, and here the architecture is unobserved.
- **The grade is decided by a confidence-band knife-edge, not by food quality.** This product scored
  `confidence_score = 60` → band `medium` → **no 75-ceiling**, so the 81.15 weighted score passed
  through as 81.2/A. The two near-identical protein granolas next to it
  (`Granola Protein` weighted 79.98, `Protein granola` 75.03) scored `confidence = 55` → band `low` →
  the 75-confidence-ceiling bound them to **75/B**. The *only* reason this one is 60 and they are 55:
  OFF happened to carry a `sodium_mg` value for it (46) and not for them, sparing it one `-5`
  reduction (`missing: sodium_mg`). All three are equally missing the ingredient list (each takes the
  same `-25`). So an A vs a capped B turns on whether a crowd-sourced database had a sodium cell
  filled in — a data-completeness accident, not a nutritional difference.

**This exposes a real scoring-philosophy edge, and it is a confidence-architecture issue, not a
protein/sugar over-credit.** The dimension scoring did its job. The flaw is that the confidence
ceiling has a hard step exactly at band boundary 60, and a product with **no ingredient panel** can
sit one point above that step on an unrelated field and earn the category's top public grade. My
position: **an A should require ingredient observability** (or at minimum land in the confidence band
that the ceiling protects), precisely because A is the highest-stakes claim and — per the TASK-140
lesson — new unseen products are where over-confidence bites. **Recommend: do not promote this as an
A.** Until an ingredient panel is obtained, it belongs in the same `confidence=low → ≤75/B` treatment
as its two siblings. I am flagging this to Product Agent as a candidate confidence-architecture
review (potential evidence-registry item: "A-grade requires ingredient observability for non-anchor
products"); under Hard Rule 8 any such rule needs Product co-sign, so this is a proposal, not a
deployment.

## 3. Savory-cracker / Fitness exclusion (EV-045c) — nutritionally CORRECT, but verify it actually drops them

**The nutritional logic is correct:** Nestlé "Fitness" salt-pepper / Thins / Veggie-Mix items are
crispbreads/crackers, **not** breakfast cereal. Their macro signature confirms it — fat ≥ 13g/100g
(`פיטנס מלח פלפל` 22.4g fat / 380mg sodium; bare `Fitness` 17–22g fat) vs genuine Fitness *cereal*
(`קורנפלקס פיטנס` 2.3g fat, correctly 65.3/B). A savory crispbread does not belong on a breakfast-cereal
shelf and the fat-≥13g-OR-savory-descriptor guard cleanly separates them. **EV-045c is nutritionally
sound — endorsed as curation (contamination, not calibration).**

**However — important caveat the run record under-states:** EV-045c as run did **not remove** these
from the scored set. The router caught them as misroutes (→ `default`), but they are still present
with scores, including **bare "Fitness" at 70.3/B (17g fat — a cracker) and "Fitness almond honey"
70.0/B**. A 70/B savory cracker surfacing on the cereal page would be a TASK-140-class contaminant.
So: the *rule's intent* is correct; the *enforcement* must be flag-AND-drop for live, not flag-only.
**Of the 12 Fitness-brand SKUs, only 3 are genuine cereals** (`קורנפלקס פיטנס` 65.3/B,
`Fitness Thin` — borderline, still routed cereal, hold pending ingredient check, and
`Nestle Fitness Dark Chocolate` 68.2/B — a legit chocolate cereal). The remaining 9 savory/ambiguous
Fitness SKUs are **NO-GO** for the cereal shelf.

## 4. Per-set GO / NO-GO

| Bucket | Call | Notes |
|---|---|---|
| Standard cereal B/C/D/E (oats, corn flakes, Cheerios, sweet kids cereals) | **GO** | Grades track macros; caps fire correctly. |
| Genuine granola/muesli B/C (Mornflake, Sugarless GF, the two C granolas) | **GO** | Defensible B/C on real macros. |
| **גרנולה בתוספת חלבון 81.2/A** | **NO-GO as A** | Hold / regrade to B band. Macro-only panel, no ingredients, A decided by a confidence knife-edge (see §2). |
| **Savory/ambiguous Fitness SKUs (9 of 12)** | **NO-GO** | Crackers/crispbreads, not cereal. Must be dropped, not just flagged (see §3). Includes "Fitness" 70.3/B (17g fat). |
| `Fitness Thin` (56.3/C, routed cereal) | **HOLD** | 15.8g fat — cracker-adjacent; confirm with ingredient panel before promoting. |
| Two `insufficient_data` rows (`Fitness`, `Fitness Veggie Mix`, both 50) | **NO-GO** | Already non-displayable (score=null on the frontend path); fine to exclude. |

## Products I would NOT stand behind (explicit flags)

1. **גרנולה בתוספת חלבון — 81.2/A** (bc 7290116532769). The category's only A, built on a panel with
   zero ingredients, separated from a capped-75/B only by a missing-sodium-field accident in OFF. The
   single highest-stakes claim resting on the least-observed product. **Primary flag.**
2. **"Fitness" 70.3/B** (bc 7290115205176, 17g fat) and **"Fitness almond honey" 70.0/B** — savory/
   non-cereal items scoring in the B band on the cereal shelf. Contaminant-class; must be dropped.
3. **"Fitness Thin" 56.3/C** (bc 7290112968807) — 15.8g fat, still routed `cereal`. Cracker-adjacent;
   hold pending ingredient confirmation.

## Notes for the record
- Frozen invariants untouched (milk run_005_headpin, snack 70/B, bread provenance). No published score
  changed by this review.
- The whole-set median (60.2) sitting just above run_005's 58.7 is explained by a richer granola
  presence at Carrefour, not by drift — the engine is byte-identical (data-agent's documented hash;
  pipeline-identity verification is QA's lane, not mine).
- Evidence tier on the A ruling: **Strong** that the grade is decided by a confidence-band artifact
  (directly observable in the traces); **Moderate** on whether the underlying product would still
  merit A with full ingredient data (plausible, unverified). Recommend obtaining the ingredient panel.
