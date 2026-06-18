# Frozen Vegetables v2 — Phase 1 Lock Spec (score-free use-case guide)

**Task:** TASK-235
**Status:** PHASE 1 LOCKED (owner-approved 2026-06-10). Definitions only — **no implementation, no consumer copy.**
**Owners:** Nutrition (benefit logic) · Content (copy model) · Product/Orchestrator (framing). Marketing positioning is a separate, non-gating track.
**Scope:** frozen-vegetables category ONLY. Not a precedent for other categories (owner decision, 2026-06-10).

---

## 0. Owner decisions locked (2026-06-10)

- Frozen-vegetables-only for now; **not** a precedent for other categories.
- **Remove the score chip and A/B/C/D framing** for this category.
- **Segment bands** replace global ranking.
- **Highlights only — no replacement benefit score** (no hidden/computed benefit number).
- **Aromatics stay inside the page** under תיבול ובישול (not split to a separate page).
- USDA FDC is **generic reference enrichment only**, never presented as product-label fact.
- "Missing fiber = 0" is a **broader engine issue → logged separately (TASK-236), not solved here.**

## Hard rules (binding for every later phase)

1. **No "best overall"** — no category-wide winner, ever.
2. **No A/B/C/D** and no 0–100 score anywhere in this category.
3. **No hidden benefit score** — highlights are facts, not a disguised ranking number.
4. **No recommendation language** — `מומלץ`, `בריא יותר`, `כדאי`, `הכי טוב לבריאות` are banned (insight_line_spec).
5. **No USDA-derived exact product claims without Nutrition sign-off** — generic reference only, candidate-stamped.
6. **No consumer copy ships before Content + Nutrition approval.** Sample strings here are illustrative drafts, not locked copy.

---

## 1. Final segment definitions (4 — approved)

Each segment is a **use-case band with its own lens**; items are compared **within** a band, never across. Counts are from the live corpus' existing `_cluster` tags (53 products).

| # | Segment (consumer header) | Maps from `_cluster` | Lens — the question this band answers | Cross-rank? |
|---|---|---|---|---|
| 1 | **ירקות בודדים** (single vegetables) | `plain-veg` (21) | "A plain vegetable, one ingredient — what does a normal portion bring?" | Within-band only; expect honest clustering (many are both-excellent — say so, don't manufacture rank) |
| 2 | **קטניות** (legumes) | `legumes` (14) | "The protein-and-fiber band — which delivers most per portion?" | Within-band; real differentiation exists (fiber + protein) |
| 3 | **תערובות וארוחות** (blends & meals) | `mixes` (5) + `pasta-blends` (2) + blend-type `processed` | "Convenience over purity — what does the added pasta/sauce/seasoning cost?" | Within-band; **the only band where additives are a surfaced watch-out** |
| 4 | **תיבול ובישול** (seasoning & cooking) | `herbs-seasonings` (8) + single-veg `processed` (e.g. artichoke bottoms) | "Cooking ingredients (garlic, ginger, herbs) — judged as seasonings, not as a portion-eaten vegetable." | **No portion-nutrition ranking at all** |

**Segment-assignment note (for Phase 2 build, not now):** segment derives from `_cluster` per the table. The `processed` cluster (3 items) splits by item: blend-type → band 3; single prepped vegetable (artichoke bottoms, citric acid only) → band 4. This split is a per-item lookup to be reviewed in Phase 2, not auto-inferred.

---

## 2. Benefit facts allowed per segment (Nutrition-owned)

"Allowed" = the fact may be **surfaced** if true and sourced. It is never a score input. Everything is stated at a **realistic serving**, never per-100g where that misrepresents use.

| Segment | Serving basis | Benefit facts ALLOWED | Watch-out facts ALLOWED | Explicitly FORBIDDEN |
|---|---|---|---|---|
| **ירקות בודדים** | ~100g cooked portion (~1 cup) | fiber, Vit C, Vit A (carotenoids), Vit K; "single ingredient" identity | usually **none** (empty is the correct, honest output) | added-additive claims (there are none); per-100g sodium alarm |
| **קטניות** | ~100g portion | **fiber + protein (headline)**, folate; "single ingredient / legume" identity | usually none | implying it's a substitute for watery veg |
| **תערובות וארוחות** | per realistic portion **including** the added component | the % vegetable split; what the veg base brings | **added sodium / sugar / refined-carb / sauce-sachet** (consumed in a real portion — surface prominently) | crediting micros synthesized from a generic (no clean USDA join → mark "not characterized") |
| **תיבול ובישול** | per ~5g use (≈1 teaspoon) | **identity + ingredient simplicity + convenience only**; "what this is" | none as a deduction — energy/fat/sodium **suppressed**; if mentioned, stated as plain fact anchored to teaspoon use, never as a limit | any portion-nutrition ranking; any benefit-nutrient claim; treating oil/salt as a flaw (it's what makes it a seasoning) |

**Absence rule (locked):** a nutrient missing from the Israeli label is **absent, not zero**. It is filled from USDA generic reference (§4) for display, or marked "not characterized" — **never imputed as 0**. (The engine-side absence-as-zero scoring bug is out of scope → TASK-236.)

---

## 3. Copy model (structure only — NOT consumer copy)

Reuses the proven `comparison_row_verdict_model` (collapsed row = short interpretive verdict), **stripped of all grade/score-mechanism language** (no "ציון מלא", "יורד מ…", "B כי…"). The verdict is **type → benefit → honest catch**, and **changes shape by segment**.

**Collapsed row = standing marker + 2-line verdict:**
- **Standing marker** (replaces the chip): a *type* tag, not a quality tag — `רכיב אחד` / `קטנייה` / `ארוחה` / `תיבול`. Carries no better/worse charge.
- **Single vegetable / Legume →** what it is (one ingredient) + the one benefit fact that matters for its band. No catch when there isn't one.
- **Blend / meal →** the real composition split (X% veg / Y% pasta+sauce) + the honest reframe (this is a meal, not a pure vegetable).
- **Seasoning →** reframe **up front** ("a seasoning — judge it as one") + plain ingredient statement + scary per-100g number defused by use-context. The catch is "don't confuse it with a vegetable."

**Expansion (dropdown):** existing scaffold (ingredients · real nutrition values · what-works / what-to-know / bottom line) with two locked changes:
1. Seasoning expansions lead with the **reframe**, and use **"מה לדעת"** (what to know), **not** "מה מגביל" (what limits) — oil in garlic is not a limitation.
2. Surface **unknowns only where they'd change a buying decision** — no "ערך השומן הרווי לא היה זמין" boilerplate on a 20-calorie cauliflower.

**Per-segment methodology line (replaces "what does the score mean"):** a short consumer-vocabulary sentence, no framework terms — e.g. *(draft, pending approval)* "בעמודה הזו לא נותנים ציון — משווים מה כל מוצר מביא לשימוש שאתם מתכננים."

**Banned in all copy:** A/B/C/D, 0–100, "best overall", `מומלץ`/`בריא יותר`/`כדאי`, NOVA/cap/floor/structural_class, any health-outcome claim.

---

## 4. Confidence / source wording for USDA-backed generic reference (POLICY locked; exact strings pending approval)

**Policy (locked):**
- USDA FoodData Central is a **generic, authoritative reference** for benefit micronutrients (fiber, vitamins, potassium, folate) the Israeli label omits. It is **enrichment, never the product's own measured panel.**
- Every USDA-sourced value is **`verification_status = candidate`**, attributed to source + USDA release/version, and joined via an **explicit, reviewable generic→SKU lookup table** (built in Phase 2), never fuzzy auto-match.
- A USDA value **fills** a missing field for display; it **never overwrites** a present BSIP0 label value, and **never moves any number that orders or rates products** (there is no such number in this category by design).
- **Display attribution must make the genericness visible** — the value is presented as "typical for this vegetable," not as "this product measured X." Any phrasing that asserts an exact per-product figure from USDA is a **§Hard-rule 5 violation → requires Nutrition sign-off.**
- Blends have **no clean generic** → micros are **"not characterized,"** never synthesized.

**Draft consumer wording (illustrative, NOT locked — pending Content + Nutrition approval):**
- Generic-reference label: *"ערכים אופייניים לירק זה (מקור ייחוס: USDA), לא נמדדו על המוצר עצמו."*
- Per-fact framing: *"ברוקולי מספק בדרך כלל ~X גרם סיבים ל-100 גרם"* (typical-for-the-vegetable, not product-measured).

---

## 5. Boundaries / what Phase 1 does NOT do

- No JSON authored, no generator changed, no chip removed, no frontend built — that is Phases 2–4.
- No final consumer copy — the four sample verdicts produced in the Content concept remain **drafts** pending Content + Nutrition approval.
- No benefit-number computation — and if one is ever proposed later, it is a **new scoring dimension** requiring a Scoring Rule Proposal + **D7 co-sign + EV-### evidence** (flagged, not enacted).

## Phase gate

Phase 1 is **locked** on owner approval (this document). Phase 2 (external-data spine: the USDA generic→SKU lookup table + benefit dataset pull) does **not** begin until explicitly authorized.
