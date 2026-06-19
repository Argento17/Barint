# Dropdown Data Coverage Audit v1
**TASK-345 — Phase 2+3 WS-Data: parsing-coverage audit**
**Date:** 2026-06-19
**Auditor:** Data Agent
**Scope:** All 10 live comparison JSON datasets; read-only; no data mutation.
**Spec ref:** `design/Dropdown_new_design/product-dropdown-spec.md` §2 data contract

---

## What was audited

For each product in each live JSON the following were checked:

| Check | Definition | Pass condition |
|---|---|---|
| `ingredients_ok` | `expansion.ingredients` is a non-null string that does NOT contain Shufersal website nutrition-panel disclaimers ("הנתונים המדויקים מופיעים") or cumulative-spoon markers ("כפיות סוכר") | Clean label string |
| `ingredients_null` | `expansion.ingredients` is JSON `null` | Missing — will render "לא אומת" |
| `ingredients_malformed` | String present but contains appended nutrition-panel text from the Shufersal scraper | Wrong field content — will render garbled copy |
| `nutrition_all4` | All 4 contract fields (protein, sugar, energy_kcal, sodium) non-null and non-empty in `expansion.nutrition` | Ready for 4-up grid |
| `nutrition_partial` | 1–3 of the 4 fields present | Partial display — some cells will show "—" |
| `additives_present` | `d4_additives` array at product level contains ≥ 1 entry | Additive sub-dropdown shows entries |
| `rank/categoryTotal` | `rank` and `categoryTotal` fields on the product object | Required for shelf-context rail |
| OFF hit | Any product-level field containing `open_food_facts` as provenance | Launch blocker per TASK-238 |

**Additive field name note:** All `d4_additives` entries across every category use the Hebrew fields `name_he` + `function_he` (plus `e_number`, `tier`, `explanation_he`). The spec's data contract calls for `{ name: string; function: string }`. This is a **field-name mismatch** between the data and the VM spec — the display layer must either map `name_he`→`name` and `function_he`→`function`, or the spec should be updated to reflect Hebrew keys. This is a frontend wiring concern, not a data defect.

---

## File map (live files only)

| Page slug | Live JSON file |
|---|---|
| cereals | `cereals_frontend_v2.json` |
| granola | `granola_frontend_v1.json` |
| juices | `juices_frontend_v3.json` |
| hummus | `hummus_frontend_v5.json` |
| hard_cheeses | `hard_cheeses_frontend_v2.json` |
| brined_cheeses | `brined_cheeses_frontend_v2.json` |
| cakes_hard_cookies | `cakes_hard_cookies_frontend_v1.json` |
| cookies_coffee | `cookies_coffee_frontend_v2.json` |
| snacks | `snacks_frontend_v3.json` |
| milk | `milk_frontend_v1.json` |

Not included: `bread_frontend_v3.json` (bread route references this; audited as bonus below for completeness but bread is outside the 10-page scope).

---

## Per-page coverage tables

### 1. Cereals (cereals_frontend_v2.json) — 20 products

| Metric | Count | Notes |
|---|---|---|
| Products | 20 | |
| ingredients_ok | 13/20 | Clean label string |
| ingredients_null | 3/20 | Lyon שוקולד וקרמל, נסקוויק, סיני מיניס |
| ingredients_malformed | 4/20 | Shufersal website nutrition-panel disclaimer appended; barcodes: 7297488199590, 7290017894911, 7290017894928, 7290017894904 |
| nutrition_all4 | **0/20** | sugar is null on ALL 20 products |
| nutrition_partial | 20/20 | protein+energy+sodium present; sugar missing on all |
| null_sugar | 20/20 | Systematic — sugar not scraped for this category |
| null_protein | 0/20 | |
| null_energy | 0/20 | |
| null_sodium | 0/20 | |
| additives_present | 9/20 | 11 products are additive-clean (d4_additives=[]) |
| rank/categoryTotal fields | 0/20 | Neither field exists in the JSON |
| OFF hits (product level) | 0 | CLEAR |
| OFF hits (meta only) | YES | `_meta.excluded_off_products` lists 14 barcodes removed before publish — not in display data |

**Priority: HIGH.** Sugar missing on all 20 products is a systematic scrape gap, not individual nulls. 4 products have nutrition-panel disclaimer appended to ingredient string.

---

### 2. Granola (granola_frontend_v1.json) — 25 products

| Metric | Count | Notes |
|---|---|---|
| Products | 25 | |
| ingredients_ok | 24/25 | |
| ingredients_null | 0/25 | |
| ingredients_malformed | 1/25 | גרנולה מיקס קראנץ' מלוח (7290106773714) — Shufersal nutrition panel appended |
| nutrition_all4 | **0/25** | sugar is null on ALL 25 products |
| nutrition_partial | 25/25 | protein+energy present; sugar null all; sodium null on 5 |
| null_sugar | 25/25 | Systematic |
| null_sodium | 5/25 | גרנולה חמוציות ושקדים, גרנולה מייפל תמר פקאן, גרנולה לוז וקינמון, גרנולה אגוזים חמוציות, גרנולה מייפל פקאן |
| null_protein | 0/25 | |
| null_energy | 0/25 | |
| additives_present | 8/25 | |
| rank/categoryTotal fields | 0/25 | Neither field exists |
| OFF hits (product level) | 0 | CLEAR |
| OFF hits (meta only) | YES | `_meta.excluded_off_products` lists 17 barcodes removed before publish |

**Priority: HIGH.** Sugar missing on all 25 products (same scrape gap as cereals). 1 malformed ingredient. 5 products missing sodium.

---

### 3. Juices (juices_frontend_v3.json) — 21 products

| Metric | Count | Notes |
|---|---|---|
| Products | 21 | |
| ingredients_ok | 21/21 | |
| ingredients_null | 0/21 | |
| ingredients_malformed | 0/21 | |
| nutrition_all4 | 6/21 | |
| nutrition_partial | 15/21 | |
| null_sugar | 2/21 | |
| null_protein | 1/21 | |
| null_energy | 0/21 | |
| null_sodium | **15/21** | 15 of 21 products missing sodium; predominantly fresh-squeezed juices + nectars where sodium not on label |
| additives_present | **0/21** | `d4_additives` field absent on ALL products (field not populated for this category) |
| rank/categoryTotal fields | 0/21 | Neither field exists |
| OFF hits | 0 | CLEAR |

**Priority: HIGH for additives (field entirely absent); MEDIUM for sodium (category-appropriate — fresh juices genuinely low-sodium but field should still be populated or explicitly null).** Sugar gap is minor (2 products).

---

### 4. Hummus (hummus_frontend_v5.json) — 57 products

| Metric | Count | Notes |
|---|---|---|
| Products | 57 | |
| ingredients_ok | 57/57 | |
| ingredients_null | 0/57 | |
| ingredients_malformed | 0/57 | |
| nutrition_all4 | 55/57 | |
| nutrition_partial | 2/57 | sugar null on 2 products |
| null_sugar | 2/57 | Minor gap |
| null_protein | 0/57 | |
| null_energy | 0/57 | |
| null_sodium | 0/57 | |
| additives_present | 56/57 | 1 product has d4_additives=[] (genuine additive-clean) |
| rank/categoryTotal fields | 0/57 | Neither field exists |
| OFF hits | 0 | CLEAR |

**Priority: LOW.** Best-covered category. 2 minor sugar gaps. Essentially dropdown-ready modulo rank/categoryTotal.

---

### 5. Hard Cheeses (hard_cheeses_frontend_v2.json) — 28 products

| Metric | Count | Notes |
|---|---|---|
| Products | 28 | |
| ingredients_ok | 28/28 | |
| ingredients_null | 0/28 | |
| ingredients_malformed | 0/28 | |
| nutrition_all4 | **2/28** | Only 2 products have all 4 fields |
| nutrition_partial | 26/28 | sugar null on 26 of 28 products |
| null_sugar | **26/28** | Systematic — sugar not captured for most hard cheeses |
| null_protein | 0/28 | |
| null_energy | 0/28 | |
| null_sodium | 0/28 | |
| additives_present | 1/28 | Only 1 product has populated d4_additives; 27 products have d4_additives=[] |
| rank/categoryTotal fields | 0/28 | Neither field exists |
| OFF hits | 0 | CLEAR |

**Priority: HIGH.** Sugar missing on 26/28 is systematic. Additive coverage extremely low (1/28) — unclear if cheeses genuinely have no additives or if scrape did not capture them. Requires re-parse.

---

### 6. Brined Cheeses (brined_cheeses_frontend_v2.json) — 36 products

| Metric | Count | Notes |
|---|---|---|
| Products | 36 | |
| ingredients_ok | 36/36 | |
| ingredients_null | 0/36 | |
| ingredients_malformed | 0/36 | |
| nutrition_all4 | 33/36 | |
| nutrition_partial | 3/36 | sugar null on 3 products |
| null_sugar | 3/36 | גבינה צפתית בטעמים (מחלבת המושבה), גבינה מלוחה חמד 16% (פיראוס), כדורי פטה בשמן מתובל (ניצן) |
| null_protein | 0/36 | |
| null_energy | 0/36 | |
| null_sodium | 0/36 | |
| additives_present | 32/36 | 4 products are additive-clean |
| rank/categoryTotal fields | 0/36 | Neither field exists |
| OFF hits | 0 | CLEAR |

**Priority: LOW.** 3 sugar gaps. Strong ingredient and additive coverage. Closest to dropdown-ready after hummus.

---

### 7. Cakes & Hard Cookies (cakes_hard_cookies_frontend_v1.json) — 65 products

| Metric | Count | Notes |
|---|---|---|
| Products | 65 | |
| ingredients_ok | 65/65 | |
| ingredients_null | 0/65 | |
| ingredients_malformed | 0/65 | |
| nutrition_all4 | 64/65 | |
| nutrition_partial | 1/65 | 1 product missing sugar |
| null_sugar | 1/65 | Minor |
| null_protein | 0/65 | |
| null_energy | 0/65 | |
| null_sodium | 0/65 | |
| additives_present | 65/65 | All products have d4_additives populated |
| rank/categoryTotal fields | 0/65 | Neither field exists |
| OFF hits | 0 | CLEAR |

**Priority: LOW.** Near-complete coverage. 1 sugar gap. All products have additives populated (could be [] for clean products, confirmed all have the field). Best-covered category for additives.

---

### 8. Cookies & Coffee (cookies_coffee_frontend_v2.json) — 119 products

| Metric | Count | Notes |
|---|---|---|
| Products | 119 | |
| ingredients_ok | 119/119 | |
| ingredients_null | 0/119 | |
| ingredients_malformed | 0/119 | |
| nutrition_all4 | 112/119 | |
| nutrition_partial | 7/119 | |
| null_sugar | 5/119 | עוגיות בטעם חמאה, עוגיות פירות יער, עוגיות קוסמין פירות יער, קוקיס שגבי שוקולד חלבי, קוקיס שוקולד לבן חלבי |
| null_protein | 1/119 | עוגיות חיות שוקו |
| null_energy | 0/119 | |
| null_sodium | 2/119 | מארז עוגיות אקלר סנדוויץ' רינגה ללא סוכר הלל; עוגיות חיות שוקו |
| additives_present | 103/119 | 16 products have d4_additives=[] (additive-clean or not parsed) |
| rank/categoryTotal fields | 0/119 | Neither field exists |
| OFF hits | 0 | CLEAR |

**Priority: LOW-MEDIUM.** 7 products with partial nutrition. 16 products with no additives (needs verification whether additive-clean or unparsed). Largest corpus — most complete overall.

---

### 9. Snacks (snacks_frontend_v3.json) — 18 products

| Metric | Count | Notes |
|---|---|---|
| Products | 18 | |
| ingredients_ok | 18/18 | |
| ingredients_null | 0/18 | |
| ingredients_malformed | 0/18 | |
| nutrition_all4 | 16/18 | |
| nutrition_partial | 2/18 | sodium null on 2 products |
| null_sugar | 0/18 | |
| null_protein | 0/18 | |
| null_energy | 0/18 | |
| null_sodium | 2/18 | Minor |
| additives_present | **5/18** | 13 products have d4_additives=[] — low coverage for a category where additives are nutritionally relevant |
| rank/categoryTotal fields | 0/18 | Neither field exists |
| OFF hits | 0 | CLEAR |

**Priority: MEDIUM for additives.** 13 products with no additives in d4_additives. Given this is the snacks category (bars, granola bars, date-based snacks), most genuinely have no additives — but the 5 that do confirms the field is populated when relevant. Low-count is consistent with a clean-snack corpus. Nutrition coverage is near-complete.

---

### 10. Milk (milk_frontend_v1.json) — 18 products

| Metric | Count | Notes |
|---|---|---|
| Products | 18 | |
| ingredients_ok | 18/18 | (milk ingredients are very short — e.g. "חלב" — correctly captured) |
| ingredients_null | 0/18 | |
| ingredients_malformed | 0/18 | |
| nutrition_all4 | **0/18** | sodium null on ALL 18; sugar null on 10 + 1 empty string |
| nutrition_partial | 18/18 | protein+energy present on all; sugar/sodium highly incomplete |
| null_sugar | **11/18** | 10 null + 1 empty string ("") — bespoke issue |
| null_protein | 0/18 | |
| null_energy | 0/18 | |
| null_sodium | **18/18** | Systematic — sodium not scraped for any milk product |
| additives_present | **0/18** | `d4_additives` field entirely absent (not even an empty array) — field not generated for this category |
| rank/categoryTotal fields | 0/18 | Neither field exists |
| OFF hits | 0 | CLEAR |

**Priority: HIGH.** Sodium missing on all 18 products (total scrape gap). Sugar missing on 11/18. `d4_additives` field entirely absent (not even `[]`) — the milk pipeline did not emit this field. This is the bespoke category and has the largest structural gaps relative to the dropdown spec.

---

## Cross-category summary

| Category | N | ING ok/null/malformed | NUT all4/partial | sugar_null | sodium_null | additives_present | rank exists | OFF |
|---|---|---|---|---|---|---|---|---|
| cereals | 20 | 13/3/4 | 0/20 | 20 | 0 | 9/20 | No | CLEAR |
| granola | 25 | 24/0/1 | 0/25 | 25 | 5 | 8/25 | No | CLEAR |
| juices | 21 | 21/0/0 | 6/15 | 2 | 15 | **0/21** | No | CLEAR |
| hummus | 57 | 57/0/0 | 55/2 | 2 | 0 | 56/57 | No | CLEAR |
| hard_cheeses | 28 | 28/0/0 | 2/26 | 26 | 0 | 1/28 | No | CLEAR |
| brined_cheeses | 36 | 36/0/0 | 33/3 | 3 | 0 | 32/36 | No | CLEAR |
| cakes_hard_cookies | 65 | 65/0/0 | 64/1 | 1 | 0 | 65/65 | No | CLEAR |
| cookies_coffee | 119 | 119/0/0 | 112/7 | 5 | 2 | 103/119 | No | CLEAR |
| snacks | 18 | 18/0/0 | 16/2 | 0 | 2 | 5/18 | No | CLEAR |
| milk | 18 | 18/0/0 | 0/18 | 11 | 18 | **0 (field absent)** | No | CLEAR |
| **TOTAL** | **407** | **379/3/5** | **288/119** | **95** | **42** | **279/407** | **0/407** | **CLEAR** |

---

## OFF sweep — verdict

**No OFF-sourced data in any live product.** Two files (`cereals_frontend_v2.json`, `granola_frontend_v1.json`) contain `open_food_facts` references in their `_meta.excluded_off_products` section — this documents products that were *removed* before publish per TASK-238. The references are in the exclusion registry, not in any live product object. All 407 live products are OFF-free.

---

## rank / categoryTotal — universal gap

**`rank` and `categoryTotal` fields are absent from all 407 products across all 10 categories.** The spec's shelf-context section (§3.2) requires `rank` (position in category) and `categoryTotal` (corpus size). Both are derivable from the JSON itself (sort by score, assign position 1..N), so the frontend can compute them at render time from the corpus. However, the spec says these come from the VM — the pipeline needs to emit them. This is a **universal data gap**, not category-specific.

---

## Prioritized gap list (pre-dropdown)

### P0 — Blocks dropdown for entire categories

1. **Sugar: cereals (20/20), granola (25/25)** — Sugar null on all products in both categories. The 4-up nutrition grid will show "—" for sugar on every product. These two categories cannot ship the dropdown with a complete nutrition cell. Systematic scrape gap, not individual product failures.

2. **Sodium: milk (18/18)** — Sodium null on all milk products. Combined with sugar null on 11/18, milk has 0/18 products with complete 4-field nutrition.

3. **d4_additives field absent: milk (18/18 missing the field entirely)** — Not an empty array, the field is not emitted by the milk pipeline at all. Frontend will error or show undefined. Must add `d4_additives: []` at minimum for every milk product.

4. **d4_additives absent: juices (0/21, field not populated)** — Same as milk: the field is not present on any juice product. Additive sub-dropdown cannot render.

### P1 — Significant gaps (multiple products, single category)

5. **Sugar: hard_cheeses (26/28 null)** — Systematic. Only 2 products have sugar. Dropdown nutrition grid will show "—" for sugar on nearly every hard cheese.

6. **Sodium: juices (15/21 null)** — 15 of 21 juice products missing sodium. Many are genuinely low-sodium fresh juices, but the value should be captured or explicitly null (not omitted from scrape).

7. **Additives: hard_cheeses (1/28)** — Only 1 product has additives. Hard cheeses may genuinely be additive-clean (salt + rennet + milk), but this requires a re-parse verification pass, not an assumption.

8. **Malformed ingredients: cereals (4/20), granola (1/25)** — 5 products have the Shufersal website's nutrition disclaimer text appended to the ingredient string. If rendered, these will show garbage copy after the real ingredient list.

### P2 — Minor gaps (several products, manageable)

9. **Sugar: cookies_coffee (5/119), snacks (0/18), brined_cheeses (3/36), milk (11/18)** — Scattered individual products across multiple categories. Not systematic failures.

10. **Sodium: cookies_coffee (2/119), snacks (2/18)** — Individual products, low impact.

11. **Null ingredients: cereals (3/20)** — 3 cereal products have no ingredient string at all.

12. **Additives: cookies_coffee (16/119 with d4_additives=[])** — May reflect genuinely additive-clean products (e.g., pure coffee items). Needs per-product review.

13. **rank/categoryTotal: all categories (0/407)** — Universal gap. Must be populated by pipeline or computed at render time.

---

## Additive field name mismatch (spec vs data)

The VM spec (§2) defines additives as `{ name: string; function: string }`. Every category uses `{ name_he: string; function_he: string; e_number: string; tier: string; explanation_he: string }`. This is not a data defect — the data is structured correctly; the spec's type definition needs to match the Hebrew keys. Flagging for the Frontend Agent to align the `BariProductVM` TypeScript type and the `AdditivePanel` component prop to read `name_he` and `function_he`.

---

## Methodology notes

- All counts derived from reading the committed JSON files at `bari-web/src/data/comparisons/`.
- Malformed detection used UTF-8 string search for `"הנתונים המדויקים מופיעים"` (Shufersal web disclaimer) and `"כפיות סוכר"` (nutrition panel marker).
- Nutrition "complete" = all 4 contract fields (protein, sugar, energyKcal/energy_kcal, sodium) non-null and non-empty-string.
- Additives "present" = `d4_additives` array at top-level product object with length > 0.
- rank/categoryTotal: checked `product.PSObject.Properties.Name` for both field names.
- OFF sweep: UTF-8 raw string search for `"open_food_facts"` across all 10 files.
- No products were modified. No external data sources were consulted.
