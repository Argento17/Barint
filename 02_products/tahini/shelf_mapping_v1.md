# Tahini — Shelf Mapping v1

**Task:** TASK-054  
**Owner:** Data Agent  
**Date:** 2026-05-31  
**Category:** Tahini  
**Status:** Draft — requires probe run to confirm shelf codes before full traversal

---

## Overview

Tahini is sold across two distinct shelf locations at Israeli retailers:

1. **Ambient grocery** (primary): Raw tahini and flavored tahini products in ambient-temperature jars, usually shelved alongside oils, sesame products, and condiments
2. **Refrigerated dips** (secondary): Ready-to-eat tahini dip ("טחינה מוכנה") shelved alongside hummus — the boundary case previously deferred from the Hummus category

Both locations must be traversed. The refrigerated dips location is the direct continuation of the Hummus corpus; the ambient location is new territory.

---

## Section 1 — Shufersal

### 1.1 Primary shelf — Ambient Tahini

**Location in Shufersal hierarchy:** מזון יבש (dry goods) → ממרחים ורוטבים (spreads and sauces) → טחינה / שמנים ורוטבים

Shufersal does not always have a single dedicated "tahini" sub-code. Tahini products may appear in:
- A dedicated "טחינה" sub-category (preferred — full traversal)
- The "ממרחים מלוחים" (savory spreads) code
- The "שמנים ורוטבים" (oils and sauces) code

| Shelf code (estimated) | Label | Strategy | Contamination estimate | Notes |
|---|---|---|---|---|
| טחינה sub-code (primary) | טחינה / Tahini | **Full traversal** | 10–15% | Core shelf. Contains raw tahini, organic tahini, flavored tahini. Minor contamination from sesame candy/halva |
| ממרחים מלוחים | Savory spreads | **Selective** | 40–50% | May contain tahini products not on primary shelf. Also contains pesto, tapenade, schug — OOS. Use search-within |
| מזון אורגני / בריאות | Organic / health foods | **Search-within** | 40–60% | Premium organic tahini often shelved here (e.g., from Adam/Achva/Rena brands). Worth checking; do not traverse blindly |
| ממרחים מתוקים | Sweet spreads | **Do not traverse** | 85%+ | Jam, honey, chocolate spreads. Skip entirely; use search query for "טחינה עם תמר" to capture sweetened tahini SKUs |

### 1.2 Secondary shelf — Refrigerated Ready-to-Eat Tahini

**Location:** מזון מקורר → חומוס וסלטים → סלטי חומוס וטחינה (A162406 — same code used for hummus)

Ready-to-eat tahini dip ("טחינה מוכנה", "ממרח טחינה", "טחינה ביתית") is shelved alongside hummus. The hummus corpus was acquired from shelf code A162406. Do not re-traverse A162406 entirely — the hummus corpus already processed it. Instead:

**Strategy for refrigerated tahini:** Run targeted search queries for "טחינה מוכנה", "ממרח טחינה", "סלט טחינה", "טחינה ביתית" and cross-check against the existing hummus exclusion log to confirm these products were not already captured (they should appear in the exclusion log from the hummus corpus_filter, TASK-026).

| Shelf code | Label | Strategy | Notes |
|---|---|---|---|
| A162406 | סלטי חומוס וטחינה | **Search-only** | Do not re-traverse. Use search queries. Cross-check hummus exclusion_log |

### 1.3 Shufersal Search Queries

Run these queries against Shufersal search. Do not trust the category tag from search results — products can appear across codes.

| Query | Target product type | Priority |
|---|---|---|
| `טחינה` | All tahini products (raw, ready-to-eat, organic) | **HIGH** |
| `טחינה גולמית` | Raw sesame paste | **HIGH** |
| `טחינה מוכנה` | Ready-to-eat tahini dip | **HIGH** |
| `ממרח טחינה` | Tahini spread (ready-to-eat) | **HIGH** |
| `טחינה ביתית` | Home-style tahini dip | **HIGH** |
| `טחינה אורגנית` | Organic tahini | **MEDIUM** |
| `טחינה שומשום מלא` | Whole sesame tahini | **MEDIUM** |
| `טחינה כל שומשום` | Whole sesame tahini (alt name) | **MEDIUM** |
| `טחינה קלויה` | Roasted tahini | **MEDIUM** |
| `טחינה עם תמר` | Tahini with date | **MEDIUM** |
| `טחינה עם דבש` | Tahini with honey | **MEDIUM** |
| `סלט טחינה` | Tahini salad (ready-to-eat) | **MEDIUM** |
| `שומשום מלא` | Whole sesame (keyword search) | **LOW** |

### 1.4 Known Shufersal Contamination Sources

| Contamination type | Hebrew | Estimated volume | Exclusion mechanism |
|---|---|---|---|
| Halva and halva spread | חלבה, ממרח חלבה | 5–10 products | Hard exclude: "חלבה" in name |
| Chocolate tahini spread | טחינה שוקולד, ממרח טחינה ושוקולד | 3–6 products | Hard exclude: "שוקולד" in name for tahini products |
| Sesame candy / sesame brittle | עוגיות שומשום, פלאפל שומשום | 3–5 products | Hard exclude: "עוגיות", "ממתק" in name |
| Sesame oil | שמן שומשום | 3–5 products | Hard exclude: "שמן" as first word AND "שומשום" — different format |
| Sesame seeds (whole) | גרעיני שומשום | 3–5 products | Hard exclude: "גרעיני" in name |
| Ready-to-eat pita bread rolls with tahini | פיתה + טחינה | 1–3 products | Hard exclude: "פיתה" in name |
| Hummus products with tahini as secondary ingredient | חומוס + טחינה | 10–20 products | Already in hummus corpus — cross-check bsip1 IDs; do not duplicate |

### 1.5 Shufersal Probe Protocol

Before full traversal, run shufersal_probe_v3.py (or equivalent) on the primary tahini shelf code:
1. List first 50 product names
2. Count: (OOS product names / 50) = contamination rate
3. If contamination rate > 25%: reduce to search-only for that code
4. If contamination rate ≤ 25%: proceed with full traversal

---

## Section 2 — Yohananof

### 2.1 Search-first approach

Yohananof does not have an exactly equivalent shelf hierarchy to Shufersal for tahini. Use search queries only. Do not attempt full shelf traversal at Yohananof.

**Value of Yohananof for tahini:** Local brands and organic brands that are underrepresented at Shufersal. Israeli tahini brands with strong Yohananof presence include smaller premium producers (e.g., Har Bracha, Adina, Achla, local-brand store products). Expect 10–20 additional SKUs not found at Shufersal.

| Query | Target | Priority |
|---|---|---|
| `טחינה` | All tahini products | **HIGH** |
| `טחינה גולמית` | Raw tahini | **HIGH** |
| `טחינה מוכנה` | Ready-to-eat dip | **HIGH** |
| `טחינה אורגנית` | Organic tahini | **MEDIUM** |
| `טחינה מלאה` | Whole sesame tahini | **MEDIUM** |

### 2.2 Yohananof-specific considerations

- Barcode quality at Yohananof: EAN-13 barcodes on tahini are generally clean (unlike hummus, where short-codes were common). Cross-matching with Shufersal should be possible for major brands.
- Nutrition data quality: Yohananof nutrition data was reliable in previous runs. No known anomalies for tahini category.
- De-duplication: After both retailers are scraped, de-duplicate by barcode. Keep one record per product; prefer Shufersal data where available (more detailed label text in some cases).

---

## Section 3 — Retailer Difference Notes

| Aspect | Shufersal | Yohananof |
|---|---|---|
| Shelf code approach | Category codes available (allow traversal) | Category browse less structured; search preferred |
| Organic brand coverage | Moderate | Stronger (local brands) |
| Ready-to-eat tahini coverage | Good (adjacent to hummus shelf) | Moderate |
| Barcode format | Mix of EAN-13 and short-codes | Primarily EAN-13 |
| Nutrition label format | HTML parse, prone to fat-row defect (TASK-039) | Generally cleaner |
| Ingredient text quality | Generally good; some marketing copy contamination | Generally good |

---

## Section 4 — Contamination Risk Ranking

| Risk level | Source | Signal terms to hard-exclude |
|---|---|---|
| **Critical** | Halva and halva spread (same primary ingredient, different structure) | "חלבה", "חלווה", "ממרח חלבה" |
| **High** | Chocolate-tahini spread (sugar-dominant dessert product) | "שוקולד" (combined with "טחינה") |
| **Medium** | Sesame candy and confections | "ממתק", "קרוקנט", "עוגיות", "ריבה" |
| **Medium** | Hummus products carrying tahini as secondary ingredient | Cross-check with existing hummus corpus IDs |
| **Low** | Sesame oil | "שמן שומשום" as full name |
| **Low** | Sesame seeds (unprocessed) | "גרעיני שומשום" |
| **Low** | Ready-to-eat flatbread with tahini filling | "פיתה", "לאפה" |

---

## Section 5 — Shelf Probe Checklist (Pre-Acquisition)

Before committing to full traversal, complete:

| Check | Action | Pass criterion |
|---|---|---|
| Identify primary Shufersal shelf code | Browse shufersal.co.il → dry goods → spreads → locate tahini section; record URL code | Code identified |
| Probe contamination rate | Run probe script on first 50 products; count OOS names | < 25% contamination → full traversal |
| Confirm A162406 exclusion | Verify ready-to-eat tahini products appear in hummus exclusion_log | Exclusion log has ≥ 1 "טחינה מוכנה" entry |
| Verify organic tahini in organic section | Manual spot-check: is "Har Bracha" or "Adina" brand listed separately in organic section? | Note if organic section requires separate search |
| Confirm Yohananof query volume | Run search for "טחינה" at Yohananof and count results | ≥ 10 products found |

---

## Section 6 — Discovery Script Configuration

Adapt `01_discover_hummus_shufersal.py` for tahini:

**Add to hard-exclude terms:**
```python
HARD_EXCLUDE_TERMS = [
    "חלבה", "חלווה",           # halva
    "ממתק", "קרוקנט",          # confection
    "שמן שומשום",              # sesame oil
    "גרעיני שומשום",           # whole sesame seeds
    "עוגיות שומשום",           # sesame cookies
    "שוקולד",                  # chocolate (applied to tahini context)
    "פיתה", "לאפה", "לחם",    # bread with tahini filling
    "חטיף", "בר",             # snack bars
    "אבקת",                   # powder format
    "מארז",                   # multi-pack
]
```

**Add to positive-type signals (suggested YES):**
```python
POSITIVE_TYPE_SIGNALS = [
    "טחינה", "טחינה גולמית", "טחינה מוכנה",
    "ממרח טחינה", "טחינה ביתית",
    "שומשום מלא", "שומשום קלוף",
]
```

---

*Shelf Mapping v1 — Tahini — TASK-054 — 2026-05-31*  
*Status: Draft. Requires probe run before full traversal commitment.*  
*Owner: Data Agent → Frontend Architect (execution)*
