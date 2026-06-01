# BSIP2 → Web Translation Contract — v1

**Task:** TASK-085
**Owner:** Product Agent
**Date:** 2026-05-31
**Status:** DRAFT — first version, hummus-anchored, intended to generalise
**Scope of this version:** Savory spreads (Hummus). Other categories adopt it as they reach Stage 6.
**Anchored in (does NOT supersede):**
- `01_framework/editorial/bari_explanation_framework_v1.md` — savory-spread explanation layer (TASK-073)
- `01_framework/editorial/score_presentation_v1.md` — score display mechanics (canonical)
- `01_framework/editorial/explainability_v1.md` — Universal Explainability System (canonical)
- `.claude/skills/bari-frontend-ui/SKILL.md` — comparison-page UI rules
**Companion deliverable:** `02_products/hummus/launch/hummus_web_readiness_rules.md`

---

## 0. Why This Document Exists

The Hummus page renders, but it does not reliably turn a BSIP2 score into something a shopper can use. Two failures motivated TASK-085:

1. **Generic grade fallback.** Every B-grade product currently shows the same per-band sentence ("פרופיל הרכב טוב ביחס לקטגוריה"). That restates the grade band; it never says *why this product* landed where it did. (`bari_explanation_framework_v1.md §0`.)
2. **No contract between the scorer and the page.** A BSIP2 trace is a rich internal object — `dimension_scores`, `caps_applied`, `penalties_applied`, `nova_proxy`, `confidence_band`, `missing_nutrition_fields`. Nothing defines *which* of those become web copy, in *what* words, and which must never surface. The page has been assembled by hand per product.

This contract closes that gap. It defines a deterministic, inspectable path:

```
BSIP2 trace  ──►  web data record  ──►  rendered comparison page
(internal)        (this contract)       (frontend-ui skill)
```

It does **not** invent scoring, change any published score, or define new visual mechanics. It defines the *translation* — the mapping from scored signals to consumer language — and the field contract the page consumes.

---

## 1. Category Boundary

> *Defines exactly what belongs in the ranked comparison, and where everything else goes.*

A product enters the **ranked comparison** only if it is a **member of the category as a consumer would shop it.** For savory spreads that means a *prepared, ready-to-eat spread you put on bread or serve as a dip.*

### 1.1 In the ranked comparison

- Hummus spreads (plain, flavoured, light, protein, high-tahini)
- Masabacha (whole chickpeas served in a tahini/sauce base — a prepared dip)
- Matbucha / Turkish salad / cooked pepper spreads
- Eggplant spreads
- Tahini-heavy prepared spreads that are *sold and eaten as a spread* (see `hummus_web_readiness_rules.md §4` for the tahini boundary with the Tahini category)

### 1.2 Excluded from the ranked comparison

The following are **not prepared spreads** — they are cooking ingredients or pantry items — and must not be ranked against spreads:

| Excluded | Reason |
|---|---|
| Raw / dried chickpeas | Single-ingredient legume; a cooking input, not a spread |
| Canned whole chickpeas | Cooking input; ingredient text often marketing copy, not a verified list |
| Frozen chickpeas | Cooking input |
| Cooking ingredients (tahini paste sold as an ingredient, raw oils, etc.) | Belong to their own category |
| Non-spread pantry items | Out of category entirely |

### 1.3 Where excluded products go — the decision

There are two destinations a product can land in. The rule:

1. **Non-ranked informational section** — for products that are **in the corpus, share the category name, and a shopper might reasonably expect to see** (raw / canned / frozen chickpeas under the name "חומוס"). Removing them silently would look like a gap. They are shown **without a rank, without a grade badge, and without score-vs-score ordering**, under an explicit heading that states they are raw material, not a prepared spread.
   - Heading (hummus): **"גרגירי חומוס — חומר גלם, לא ממרח מוכן"**
   - Section note: "מוצרים אלה הם גרגירי חומוס לבישול, ולא ממרחים מוכנים. הם מוצגים לעיון בלבד ואינם מדורגים מול הממרחים."

2. **Removed entirely** — for products that are **out of category** (non-spread pantry items, condiments, dairy spreads, schug/harissa). No shopper expects them on a hummus page; they carry no informational value here.

**Why a section and not deletion for chickpeas:** the boundary review (`hummus_boundary_review.md §3`) showed that 7 of 8 grade-A products were raw/canned chickpeas ranking *first* — and they ranked first *because Bari had the least information about them* (single-ingredient floor protected them from the data gap), not the most. Ranking them is apples-to-oranges and inflates the top of the list. But they share the name "חומוס", so silent deletion is also wrong. The non-ranked section is the honest middle: visible, contextualised, unranked.

**Rule of thumb:** *shares the category name → informational section; foreign to the category → removed.*

> **The ranked top result must be a genuine member of the category.** After excluding chickpeas, the #1 hummus result becomes a real prepared spread (סלט חומוס, 80.2/A), which is the honest, useful top result. A boundary is correct when the thing ranked #1 is the thing the shopper came to compare.

---

## 2. Web Data Contract

> *The required fields for each displayed product. The frontend consumes exactly this shape; the Data Agent generates to it from the BSIP2 trace.*

Every displayed product record carries the fields below. This extends the current `BariProductVM` (which already has `id`, `name`, `score`, `grade`, `insightLine`, `confidence`, `expansion`) with the structured explanation arrays this contract requires.

### 2.1 Required fields

| Field | Type | Source | Notes |
|---|---|---|---|
| `id` | string | trace `canonical_product_id` | Internal only; never rendered as text |
| `name` | string | label registry display name | Never a raw slug/barcode |
| `score` | number \| null | trace `final_score_estimate` | `null` only when `data_sufficiency = insufficient` |
| `grade` | "A"\|"B"\|"C"\|"D" \| null | trace `grade_estimate` | `null` with `score=null` |
| `insightLine` | string | Section-1 dominant signal (≤80 chars) | The card pill; one sentence; product-specific |
| `positiveSignals[]` | string[] | §3.A translation | "What helped the score." 0–2 items. May be empty. |
| `limitingFactors[]` | string[] | §3.B translation | "What limited the score." 0–2 items. May be empty. |
| `unknowns[]` | string[] | §3.C translation | "What could not be verified." Shown whenever data is missing. |
| `caveats[]` | string[] | `display_caveats` → `caveated_product_messages` | Product-level caveats (structural emptiness, routing, etc.) |
| `confidence` | "verified"\|"partial"\|"insufficient" | trace `confidence_band`/`data_sufficiency` | Always explicit, never blank (`score_presentation_v1 §5`) |
| `nutrition` | object | trace `L1_observed_signals` | Only the allowed fields below |

**Constraint — at least one of `positiveSignals` or `limitingFactors` must be non-empty for any scored product.** A scored product with both arrays empty is not web-ready (it would fall back to generic grade text — the exact failure this contract removes).

### 2.2 Nutrition fields allowed for display

Per category nutrition policy (`hummus_frontend_v1.json._meta.nutrition_policy`):

| Field | Allowed | Condition |
|---|---|---|
| `energyKcal` | ✅ | always when present |
| `protein` | ✅ | always when present |
| `sodium` | ✅ | always when present |
| `fiber` | ◐ | carried, but only rendered if it is in the active `NUTRIENT_LABELS` grid |
| `servingNote` | ✅ | basis label, e.g. "ל-100 גרם" |

### 2.3 Fields prohibited from display

| Field / value | Why prohibited |
|---|---|
| `fat`, `saturated_fat` | **Suppressed** — HUM-001 Shufersal fat-row defect (TASK-039); DEC-001 Option B. `fat = null`. The panel is shown; the fat row is hidden, with the mandatory disclosure line in the footer. |
| `sugar` | No coverage (HUM-002, 0%). `sugar = null`; not surfaced as "0", surfaced as unknown if material. |
| any internal slug / barcode / `id` | Never shown as text (`bari-frontend-ui` Data Display) |
| `nova_proxy`, `dimension_scores`, `caps_applied`, `penalties_applied`, `floors_applied`, `confidence_score` (numeric), `weighted_dimension_score`, `binding_cap`, weights | **Tier-4 internals** — never rendered or paraphrased into copy (`explainability_v1 §2.1`) |
| raw dimension point values (e.g. "protein_quality: 39.5") | Mechanics, not findings (`score_presentation_v1 §3`) |

**Empty-state rule:** a missing displayable value renders as an explicit empty state ("לא ידוע" or the relevant `unknowns[]` line), never as a blank cell or `—`/`N/A` (`score_presentation_v1 §5`, `bari-frontend-ui`).

---

## 3. BSIP2 Translation Rules

> *For each product, how scoring/data becomes the three answers. The same trace fields always map the same way — this is deterministic, not editorial taste.*

The three web arrays answer three questions. Each is sourced from specific trace fields and rendered in **consumer language only** — see the prohibitions in §3.D.

### 3.A — What helped the score → `positiveSignals[]`

Sourced from the **high dimension_scores, `floors_applied`, and clean structural observations** in the trace — re-expressed as observable facts about the *label*, never as dimension names or points.

| Trace evidence | Consumer-language pattern (savory spread) |
|---|---|
| high chickpea % declared + tahini early in list | "X% גרגירי חומוס ו-Y% טחינה גולמית — בסיס עשיר יחסית לקטגוריה" |
| low `ingredient_count`, `additive_count` 0–1 | "רשימת רכיבים קצרה — גרגירי חומוס וטחינה כרכיבים ראשונים" |
| high `protein_g` for category | "תכולת חלבון גבוהה יחסית לממרחים" |
| `floors_applied` whole-food / NOVA-1 floor | translate to the *observable* cause ("רכיב יחיד / רשימה נקייה"), **never** the floor's name |
| `regulatory_quality` high (no red labels) | usually not surfaced as a positive on its own — absence of a warning is not a selling point |

Rules:
- **Max two** positive signals. The dominant one is also the basis for `insightLine`.
- Each must be a fact a reader could verify on the pack ("I could have noticed that").
- A high *dimension* is never named. The *label evidence behind it* is named.

### 3.B — What limited the score → `limitingFactors[]`

Sourced from **`caps_applied`, `penalties_applied`, and low dimension_scores** — re-expressed as the observable additive / processing / sugar pattern that bounded the product, never as a cap/penalty/NOVA term.

| Trace evidence | Consumer-language pattern |
|---|---|
| `ADDITIVE_MARKERS_3_PLUS` cap | "הרשימה כוללת מספר תוספות מעבר לבסיס — חומר משמר ומווסת חומציות" (name *load and kind*) |
| single preservative only (`additive_count`=1) | "חומר משמר אחד מופיע ברשימה — תוספת בודדת על בסיס פשוט" |
| stabilizers + preservative | "מייצבים וחומר משמר ברשימה — מבנה רכיבים מורכב יותר מממרח פשוט" |
| `NOVA_PROXY_3_PROCESSED` cap | translate to list-shape language ("מבנה רכיבים מורכב"), **never** "NOVA" or "cap" |
| modified starch present | "עמילן מעובד מצוין ברשימה — לצד תוספות נוספות" |
| `SEED_OIL_PRESENT` penalty | surface only if material to the category; "שמן זרעים מצוין ברשימה" |
| added sugar (matbucha/pepper) | "סוכר מצוין ברשימת הרכיבים — תוספת סוכר על בסיס ירקות" |
| low chickpea share | "שיעור גרגירי חומוס נמוך יחסית, עם תוספות" |

Rules:
- **Max two** limiting factors; surface the **dominant** one(s) — the binding cap / largest penalty, not every penalty.
- **Anti-attribution:** additives are "מצוינים ברשימה", never "הוסיפו / הורידו את הציון". Ingredients are evidence of a pattern, not actors.
- **Never** "חומר משמר אחד" when the true additive load is more than one (TASK-064 R-3).

### 3.C — What could not be verified → `unknowns[]`

Sourced from **`missing_nutrition_fields`, `confidence_reductions`, `data_sufficiency`, and the category data gaps** — stated as matter-of-fact information, never as apology.

| Trace evidence | Consumer-language pattern |
|---|---|
| fat suppressed (category-wide, HUM-001) | "ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח." (mandatory, verbatim category line) |
| ingredient list absent / marketing copy | "פירוט הרכיבים המלא לא אומת ממקור הנתונים." |
| `sugars_g` missing where sugar is material | "נתוני הסוכר לא היו זמינים לקטגוריה זו." |
| `data_sufficiency = partial` | state what *is* known and what is *not* (`score_presentation_v1 §5`) |

Rules:
- `unknowns[]` is **shown whenever a displayable value is missing** — absence is itself a finding (`score_presentation_v1 §5`).
- Uncertainty is information, never apology: no לצערנו / לא הצלחנו / "בלבד" as a minimiser.
- Distinct from `caveats[]`: `unknowns[]` = data gaps; `caveats[]` = the four named product-level states in §3 of the content file (structural emptiness, low-NOVA confidence, routing imprecise, unavailable).

### 3.D — Hard constraints on all three arrays

| Constraint | Forbidden examples |
|---|---|
| **No framework vocabulary** | NOVA, cap, floor, penalty, dimension, weight, BSIP, structural_emptiness, confidence_score, field names |
| **No health claims** | בריא / לא בריא / נקי / מסוכן / טבעי-as-virtue |
| **No recommendations** | מומלץ / לא מומלץ / כדאי / עדיף / הימנע |
| **No generic grade fallback** | "פרופיל הרכב טוב ביחס לקטגוריה" or any per-band sentence applied to every product of a grade |
| **No taste / price / brand sentiment** | טעים / משתלם / מותג מוביל |
| **No score numbers in copy** | "קיבל 68 בגלל…" |
| **Category-relative framing** | every observation is relative to *spreads*, never to all food |

---

## 4. Per-Product Assembly (the algorithm)

For each product the Data Agent runs, deterministically:

```
1. Boundary gate (§1):
     out of category            → remove
     raw/canned/frozen chickpea → informational section (no rank, no grade badge)
     prepared spread            → ranked comparison, continue
2. score / grade  ← final_score_estimate / grade_estimate  (null if insufficient)
3. positiveSignals[] ← §3.A  (max 2, from high dims + floors + clean-list facts)
4. limitingFactors[] ← §3.B  (max 2, from binding cap + dominant penalties + low dims)
5. insightLine       ← the dominant positiveSignal, ≤80 chars
6. unknowns[]        ← §3.C  (always include the fat line; add ingredient/sugar gaps)
7. caveats[]         ← display_caveats → caveated_product_messages
8. nutrition         ← allowed fields only (§2.2); fat/sugar = null
9. Readiness gate    ← hummus_web_readiness_rules.md §5 acceptance criteria
```

The **expansion** ("why did this get the score?") renders, in order, the present sections only:
**מה שעזר** (`positiveSignals`) · **מה שהגביל** (`limitingFactors`) · **מה שלא ניתן לאמת** (`unknowns` + `caveats`). Empty sections render no header.

---

## 5. Determinism & Governance

- The translation is a **function of the trace**, not editorial choice: the same trace fields always produce the same web fields and the same language pattern. Two reviewers translating the same trace must produce the same arrays.
- Final Hebrew strings are authored by the **Content Agent**, fact-checked and co-signed by the **Nutrition Agent**, and rendered by the **Frontend Agent** (`ownership_matrix_v2.md`, "Consumer copy authoring").
- Any change to the *scoring* that changes which signals bind must re-run this translation — the contract reads the trace, so a rescore re-derives the copy. Numbers are versioned; the framing ("best ≠ excellent") is frozen (`CLAUDE.md`).
- This contract does not authorise any scoring change. Scoring changes go through `bari-bsip2-scoring-governance`.

---

## 6. Version History

| Version | Date | Change |
|---|---|---|
| v1 | 2026-05-31 | First BSIP2→Web translation contract. Category boundary, web data contract, three-array translation rules, per-product assembly. Hummus-anchored. TASK-085. |

---

*BSIP2 → Web Translation Contract v1 — TASK-085 — Product Agent — 2026-05-31*
*Companion: `hummus_web_readiness_rules.md`. Anchored in bari_explanation_framework_v1.md, score_presentation_v1.md, explainability_v1.md (canonical).*
