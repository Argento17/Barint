# Bari Explanation Framework — Savory Spreads (Hummus) — v1

**Task:** TASK-073
**Owner:** Product Agent (architecture)
**Co-owners on execution:** Content Agent (authors final strings), Nutrition Agent (fact-check + co-sign), Frontend Agent (renders)
**Date:** 2026-05-31
**Status:** DRAFT — pre-Hummus-launch redesign spec
**Anchored in (does not supersede):**
- `01_framework/frontend/explainability_v1.md` — Universal Explainability System (canonical)
- `01_framework/editorial/score_presentation_v1.md` — Score Presentation Philosophy (canonical)
- `01_framework/bsip2_framework/ui_language.md` — tone reference

---

## 0. Why This Document Exists

TASK-073 identified that current Bari product explanations provide little consumer value. The cited examples —

> "פרופיל הרכב טוב ביחס לקטגוריה"
> "מבנה הרכב חזק ביחס לקטגוריה"

— are not product explanations at all. They are the **per-grade `grade_descriptions`** in `hummus_content_v2.json` (lines 42–65), applied verbatim to every product that shares a grade. Every B-grade product gets the identical sentence. They tell the reader the grade band's name, restated — they do not tell the reader *why this product* received *its* score.

**The architectural gap:** Bari's hummus content today has three layers —
1. Category introduction + methodology (good, factual, fact-checked under TASK-064)
2. Grade descriptions (generic, per-band — the cited problem)
3. Per-product `insightLine` (good, specific — already exists in `hummus_insights_v1.md`)

— but it has **no per-product *explanation* layer** that connects the composition to the score in the structured, inspectable way `explainability_v1.md` mandates for every other category. The one-line `insightLine` is a description of the ingredient list; it is not the "Why This Landed Here" block.

This document defines that missing layer for the savory-spread category, as the category-native translation system that `explainability_v1.md §5` is missing for hummus (it covers only bread, snack bars, and milk).

**This document does NOT invent new scoring, new vocabulary rules, or new display mechanics.** It applies the canonical frameworks to the savory-spread category and supplies the category-specific signal language.

---

## 1. What Should a Bari Explanation Answer?

A Bari savory-spread explanation answers exactly one question, at the right level of abstraction:

> **"What did a careful reader of *this* label notice that placed it where it landed among the spreads?"**

It does **not** answer:
- "How was the number 68.2 calculated?" (system disclosure — forbidden, `explainability_v1.md §1.1`)
- "Is this product healthy / should I buy it?" (recommendation — forbidden, `score_presentation_v1.md`)
- "What did the manufacturer intend?" (attribution — forbidden, `explainability_v1.md §3.2`)

Concretely, for a savory spread the explanation must let the reader reconstruct three things from the label itself:

| The reader should come away knowing… | Sourced from |
|---|---|
| **What the product *is* compositionally** — its base, and the chickpea-to-tahini balance (or tomato/pepper/eggplant/oil base) | declared ingredient order + on-pack percentages |
| **What separated it from its neighbours** — simple short list vs. multi-component; clean base vs. several added agents | `ingredient_count`, `additive_count`, ingredient list |
| **What Bari could not see** — the fat-data gap, or an unverified/absent ingredient list | `fat_quality_reliable`, `display_caveats`, `confidence_score` |

The test from `explainability_v1.md §1.1` applies unchanged:
> A good explanation makes the reader feel: *"I could have noticed that if I knew what to look for."*

---

## 2. What Information Must Appear

Of the dimensions TASK-073 listed as candidates, the following are **mandatory** in a savory-spread explanation, in priority order. The rest are conditional.

### Always present
1. **Base composition / ingredient quality** — what the product is built from. For hummus: the chickpea share and tahini share and their balance. For matbucha/pepper/eggplant: the vegetable base. This is the Section-1 dominant observation and is never omitted.
2. **Category context** — every observation is framed *relative to savory spreads*, never to all food. (`score_presentation_v1.md`; `hummus_content_v2.json.methodology.category_relative_note`.)

### Present when material (the score-differentiating signals in this corpus)
3. **Additive observations** — preservative / acidity regulator / stabilizers / modified starch. This is the single biggest differentiator inside the hummus sub-type (clean short list → A/B; several added agents → C). Name the *load and kind*, never attribute intent.
4. **Processing observations** — simple-base vs. reconstructed/multi-component structure. Expressed as list shape ("רשימת רכיבים קצרה" vs. "מבנה רכיבים מורכב"), **never** as `NOVA`, `cap`, or any framework term.
5. **Added sugar** — material for matbucha and pepper spreads specifically; surface only when sugar appears in the list.
6. **Tradeoffs / limitations** — the limiting observation that bounded the interpretation (Section 2). One only; the dominant limiter.

### Mandatory disclosure (data-gap, present per existing rule)
7. **Fat-data unavailability** — already mandated category-wide (`hummus_content_v2.json.mandatory_disclosure`, KL-1). In the per-product block this lives in Section 3, phrased as matter-of-fact information, never as apology.
8. **Product-level caveats** — when `display_state = "caveated"`, the relevant caveat from `caveated_product_messages` is surfaced in Section 3.

### Explicitly excluded (per canonical frameworks — do not appear)
- Score weights / dimension percentages / per-dimension point values (`explainability_v1.md §2.1 Tier 4`)
- `NOVA`, `cap`, `floor`, `structural_emptiness`, `BSIP`, field names, `confidence_score` numbers
- Health/judgment language (בריא/לא בריא, נקי, מסוכן) and recommendations (מומלץ, כדאי)
- Taste, texture, price, brand sentiment (`hummus_content_v2.json.faq-06`)

---

## 3. The Mandatory Explanation Template

The savory-spread explanation **is** the `WhyThisLandedHere` three-section block from `explainability_v1.md §4.1`, populated with savory-spread-native language. No new structure is introduced.

```
מה שבלט        (Section 1 — ALWAYS present, exactly one sentence)
  [base / ingredient-quality observation] — [what it represents among spreads]

מה שהגביל       (Section 2 — present ONLY when an additive/processing/sugar
                 observation materially bounded the interpretation; ≤1 sentence)
  [the dominant limiting observation] — [factual, not apologetic, not score-mechanics]

מה שלא ניתן לאמת  (Section 3 — present ONLY when a data gap or caveat applies; ≤1 sentence)
  [the fat-data note and/or the product-level caveat] — matter-of-fact
```

### Display-level mapping (inherited unchanged from `explainability_v1.md §4.2`)

| Surface | Sections shown | Field in dataset |
|---|---|---|
| Comparison row / product card | Section 1 only (the `dominant_signal_he` pill) | `dominant_signal_he` |
| Product detail drawer / page | All present sections | `short_summary_he` + `limiting_summary_he?` + `uncertainty_summary_he?` |
| Tooltip | Section 1, shortened to ≤12 words | derived from `dominant_signal_he` |

The existing one-line `insightLine` from `hummus_insights_v1.md` becomes the **Section 1 / `dominant_signal_he`** source after light editing — it already carries the base + additive observation. The redesign's net new work is **Sections 2 and 3 per product**, plus promoting the grade-description text out of the per-product position.

### Authoring rules (savory-spread translation system — fills the `explainability_v1.md §5` gap)

**Section 1 — base / ingredient-quality language**

| Data signal | Savory-spread consumer language |
|---|---|
| chickpea % + tahini % declared | "X% גרגירי חומוס ו-Y% טחינה גולמית — [balance observation]" |
| `ingredient_count` low, `additive_count` 0–1 | "גרגירי חומוס וטחינה כרכיבים ראשונים — רשימת רכיבים קצרה" |
| high chickpea share | "בסיס עשיר בגרגירי חומוס יחסית לקטגוריה" |
| low chickpea share / many additions | "שיעור גרגירי חומוס נמוך יחסית, עם תוספות" |
| matbucha | "X% עגבניות ו-Y% פלפל — בסיס ירקות **מבושל**" (never קלוי / roasted — matbucha is stewed; per TASK-064 B-6) |
| eggplant spread | "חציל קלוי כרכיב מרכזי, עם שמן ותבלינים" |
| pepper spread, oil-first | "ממרח על בסיס שמן עם X% פלפל" |
| single whole chickpeas | "גרגירי חומוס שלמים — חומר גלם, לא ממרח מוכן" (see §5 boundary rule) |

**Section 2 — limiting (additive / processing / sugar) language**

| Data signal | Consumer language |
|---|---|
| one preservative only | "חומר משמר אחד מופיע ברשימה — תוספת בודדת על בסיס פשוט" |
| preservative + acidity regulator | "הרשימה כוללת חומר משמר ומווסת חומציות — מספר תוספות מעבר לבסיס" |
| stabilizers + preservative | "הרשימה כוללת מייצבים וחומר משמר — מבנה רכיבים מורכב יותר מממרח פשוט" |
| modified starch present | "עמילן מעובד מצוין ברשימה — לצד תוספות נוספות" |
| added sugar (matbucha/pepper) | "סוכר מצוין ברשימת הרכיבים — תוספת סוכר על בסיס ירקות" |
| long multi-component list | "רשימת רכיבים ארוכה עם מספר רכיבים מוספים" |

**Section 3 — uncertainty language (reuse `explainability_v1.md §6` + existing strings)**

| Condition | Consumer language |
|---|---|
| fat-data gap (default, 84% of corpus) | "ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח." |
| ingredient list absent/marketing-copy | "פירוט הרכיבים המלא לא אומת ממקור הנתונים." |
| `low_nova_confidence` caveat | use `caveated_product_messages.low_nova_confidence.long` |
| `structural_emptiness` caveat | use `caveated_product_messages.structural_emptiness.long` |
| `category_routing_imprecise` caveat | use `caveated_product_messages.category_routing_imprecise.long` |

### Hard authoring constraints (carried from canonical frameworks)
- **Anti-attribution** (`explainability_v1.md §3.2`): never "מרכיב X הוריד את הציון". Ingredients are evidence; name the pattern. Additives are "מצוינים ברשימה", never "הוספו כדי ל…".
- **Max two dominant drivers**; **≥2 dimensions named for any comparison gap >10 points**.
- **No score numbers, no weights, no rule names** in any section.
- **Uncertainty is information, not apology** — never לצערנו / לא הצלחנו / בלבד-as-minimizer.
- Section 1 is mandatory on every scored product; Sections 2–3 render only when populated (no empty headers).

---

## 4. Five Example Explanations

All five are grounded in real corpus products (`hummus_frontend_v1.json`, `hummus_insights_v1.md`). Hebrew strings are authoring drafts for Content Agent; they require Nutrition Agent fact-check + Product+Nutrition co-sign before integration (per `ownership_matrix_v2.md`, "Consumer copy authoring").

---

### 4.1 — A-grade hummus (prepared spread)
**Product:** סלט חומוס · `bsip1_6666307` · score 80.2 · grade A · `additive_count` 1

> **מה שבלט:** גרגירי חומוס וטחינה גולמית כרכיבים ראשונים — רשימת רכיבים קצרה, בלי מייצבים או עמילן מוסף.
> **מה שהגביל:** חומר משמר אחד מופיע ברשימה — תוספת בודדת על בסיס פשוט.
> **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.

*Why this works:* names the base (ingredient quality) and the short-list/processing observation in one sentence; the single preservative is the honest, mild limiter; the fat gap is stated flatly. No grade restated, no number, no recommendation. This is the genuine top-of-category *prepared* spread (see boundary review for why it should be #1, not the raw chickpeas above it).

---

### 4.2 — B-grade hummus
**Product:** חומוס · `bsip1_2987963` · score 68.2 · grade B · 61% chickpea / 15.5% tahini / garlic · `additive_count` 3

> **מה שבלט:** בסיס של 61% גרגירי חומוס ו-15.5% טחינה גולמית עם שום — הרכב חומוס קלאסי.
> **מה שהגביל:** הרשימה כוללת חומר משמר ומווסת חומציות — מספר תוספות מעבר לבסיס.
> **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.

*Why this works:* the declared percentages give the reader the exact base; the limiter names additive *load and kind* (preservative + acidity regulator) without claiming "one preservative only" — which TASK-064 R-3 flagged as misleading when `additive_count` is 3.

---

### 4.3 — C-grade hummus
**Product:** חומוס עם טחינה אחלה · `bsip1_7290104061417` · score 63.5 · grade C · 56% chickpea / 17% tahini · stabilizers + preservative

> **מה שבלט:** 56% גרגירי חומוס ו-17% טחינה — בסיס חומוס עם שיעור גרגירים נמוך יחסית לקטגוריה.
> **מה שהגביל:** הרשימה כוללת מייצבים וחומר משמר — מבנה רכיבים מורכב יותר מממרח חומוס פשוט.
> **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.

*Why this works:* makes the C visible — the reader sees both the lower chickpea share *and* the multi-agent list, the two convergent observations that separate it from the B above. Framed entirely relative to the category ("יחסית לקטגוריה").

---

### 4.4 — Matbucha
**Product:** סלט מטבוחה · `bsip1_7290010931330` · score 61.8 · grade C · 63% tomato / 13% pepper · contains white sugar

> **מה שבלט:** 63% עגבניות מרוסקות ו-13% פלפל — בסיס ירקות מבושל.
> **מה שהגביל:** סוכר לבן מצוין ברשימת הרכיבים — תוספת סוכר על בסיס ירקות.
> **מה שלא ניתן לאמת:** ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.

*Why this works:* uses **מבושל** (cooked/stewed), not **קלוי** (roasted) — the exact error TASK-064 B-6 caught. Added sugar is "מצוין ברשימה" (anti-attribution), surfaced because it is the dominant limiter for matbucha. Note: for the two `structural_emptiness`-caveated matbucha products (`bsip1_7290111563492`, `bsip1_7290106577572`), Section 3 instead carries the `structural_emptiness` caveat string.

---

### 4.5 — Canned chickpeas (boundary product)
**Product:** הקיסר חומוס ענק · `bsip1_7290018359686` · score 80.4 · grade A · whole canned chickpeas · ingredient text was marketing copy (TASK-064 R-2)

> **מה שבלט:** גרגירי חומוס שלמים בשימור — מוצר חד-רכיבי, חומר גלם ולא ממרח מוכן.
> **מה שהגביל:** —
> **מה שלא ניתן לאמת:** פירוט הרכיבים המלא לא אומת ממקור הנתונים — לא ניתן לאשר נוכחות או היעדר חומר משמר.
>
> *Boundary treatment (display, not a Section):* "מוצר זה הוא גרגירי חומוס לבישול ומוצג לעיון בלבד — אינו מדורג מול ממרחים מוכנים."

*Why this works:* tells the truth that the A grade comes from a single, unprocessed ingredient (`ingredient_count` 1, `additive_count` 0) **and** that the list itself was not verifiable — so it does **not** repeat the unverified "ללא חומר משמר" claim (TASK-064 R-2). The boundary treatment line implements the recommendation in `hummus_boundary_review.md`: this is raw material, shown for context, not ranked against prepared spreads.

---

## 5. Interaction With the Boundary Problem

Examples 4.5 exposes the core architectural issue handled in the companion deliverable `hummus_boundary_review.md`: when the most honest possible explanation of a product is *"this is a raw cooking ingredient, not a prepared spread,"* that product should not be sitting at the **top of a prepared-spread ranking**. The explanation framework and the boundary decision must ship together — the explanation layer makes the mismatch legible; the boundary decision removes the mismatch from the ranking.

---

## 6. Governance Checklist (per-product, before integration)

Inherits `explainability_v1.md` checklist; savory-spread additions in **bold**:

- [ ] Section 1 present on every scored product; base/ingredient observation is the dominant driver
- [ ] **Every observation framed relative to savory spreads, never to all food**
- [ ] No grade-description text reused as a per-product explanation
- [ ] No Tier-4 exposure (NOVA, cap, floor, BSIP, weights, field names, confidence numbers)
- [ ] No single-ingredient causation; additives "מצוינים ברשימה", not "הוסיפו / הורידו ציון"
- [ ] **Matbucha described as מבושל, never קלוי** (TASK-064 B-6)
- [ ] **"חומר משמר אחד" used only when total additive load is genuinely one** (TASK-064 R-3)
- [ ] **No "ללא חומר משמר" for products whose ingredient list was not verified** (TASK-064 R-2)
- [ ] Fat-data note present in Section 3 wherever `fat_quality_reliable = false`
- [ ] Product-level caveat surfaced in Section 3 when `display_state = "caveated"`
- [ ] No health claim, no recommendation, no taste/price/brand sentiment
- [ ] Nutrition Agent fact-check + Product+Nutrition co-sign obtained

---

## 7. Required Dataset Fields (Frontend / Data Agent)

To feed the per-product block, `hummus_frontend_v1.json` product records need three CE-authored string fields (it already carries the structured inputs `ingredient_count`, `additive_count`, declared percentages, `display_state`, `display_caveats`, `fat_quality_reliable`):

```
dominant_signal_he   : string   // Section 1 — derived from the existing insightLine
limiting_summary_he  : string?  // Section 2 — new; null when no material limiter
uncertainty_summary_he: string? // Section 3 — new; fat note and/or caveat string
```

This matches the contract already defined in `explainability_v1.md §12.2`.

---

*Bari Explanation Framework — Savory Spreads v1 — TASK-073 — Product Agent — 2026-05-31*
*Companion: `hummus_boundary_review.md`. Anchored in explainability_v1.md and score_presentation_v1.md (canonical).*
