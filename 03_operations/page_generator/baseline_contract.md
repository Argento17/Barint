# P268 — Baseline per-product DATA contract

Owner-locked contract for every live comparison shelf JSON served by `bari-web/src/data/comparisons/*` and imported by `*-page-data.ts`. Golden reference shapes: `cereals_frontend_v2.json`, `juices_frontend_v3.json`. Enforced read-only by `03_operations/page_generator/conform_baseline.py`.

**Checker:** `python 03_operations/page_generator/conform_baseline.py --all` (or `--shelf <id>`). Exit 0 = conform; 1 = violations; 3 = usage error. Drift report: `tasks/returns/P268_drift_report.md`.

**Not in scope:** `brand` (deferred). **Never changed by conformance:** `score`, `grade`, nutrition values.

---

## 1. Required per product

| Field | Type / rule |
|-------|-------------|
| `id` | string |
| `barcode` | string |
| `name` | string |
| `imageUrl` | string, **non-empty** |
| `score` | number |
| `grade` | string |
| `rank` | integer, score-consistent (1 = highest score) |
| `categoryTotal` | integer, equals shelf product count |
| `confidence` | string or number |
| `confidence_label_he` | string |
| `confidence_sub_reason` | string or null |
| `confidence_tooltip_he` | string |
| `insightLine` | string |
| `rowVerdict` | string |
| `d4_additives` | array (may be empty) |
| `expansion` | object with keys below |

### Required `expansion` keys

| Key | Type |
|-----|------|
| `positiveSignals` | array |
| `limitingFactors` | array |
| `nutrition` | object |
| `ingredients` | string or null |
| `comparisonContext` | string |
| `servingNote` | string |
| `confidenceLabel` | string |

---

## 2. Forbidden per product (deep-dive layer OUT for all shelves)

| Location | Keys |
|----------|------|
| Product root | `bariInterpretation`, `consumerTakeaway`, `bestUseCases`, `caps_applied` |
| `expansion` | `consumerExplanation`, `bottomLine`, `unknowns` |

These fields existed on snacks-only deep-dive rendering; the baseline contract removes them from **all** shelves.

---

## 3. Keep-if-functional internal fields

Category-internal underscore fields are **allowed** when a shelf filter or page-data loader references them. Otherwise they are orphan candidates for a later sweep.

### Functional (grep evidence)

| Field | Shelf(s) | Consumer | Evidence |
|-------|----------|----------|----------|
| `_subpool` | cereals, granola (data) | `cereals-shelf-filters.ts` filter logic | `rg "_subpool" bari-web/src/lib/comparisons/cereals-shelf-filters.ts` → lines 20, 45–47 |
| `_isChildrens` | cereals, granola (data) | `cereals-shelf-filters.ts` | `rg "_isChildrens" bari-web/src/lib/comparisons/cereals-shelf-filters.ts` → lines 21, 57 |
| `_wholeGrainClaim` | cereals, granola | `cereals-shelf-filters.ts`, `granola-shelf-filters.ts` | `rg "_wholeGrainClaim" bari-web/src/lib/comparisons/` → cereals-shelf-filters.ts:22,49; granola-shelf-filters.ts:17,33 |
| `_internal_cluster` | snacks | stripped in page-data before UI | `rg "_internal_cluster" bari-web/src/lib/comparisons/snacks-comparison-page-data.ts` → lines 27, 32–33 |
| `_product_type` | hummus | filter + strip in page-data | `rg "_product_type" bari-web/src/lib/comparisons/hummus-comparison-page-data.ts` → lines 21, 94–97 |
| `_website_cluster` | bread | `bread-shelf-filters.ts` lens matching | `rg "_website_cluster" bari-web/src/lib/comparisons/bread-shelf-filters.ts` → lines 30, 34–35 |
| `_has_phvo` | cakes, cookies_coffee (data) | cakes PHVO filter id-set | `rg "_has_phvo" bari-web/src/lib/comparisons/cakes-hard-cookies-page-data.ts` → lines 45, 173–174 |
| `_calibration` | any (pipeline) | stripped by `loadComparisonCorpus` | `rg "_calibration" bari-web/src/lib/comparisons/corpus.ts` → lines 17, 34–35 |

### Orphan candidates (present in JSON, no runtime consumer in page-data / filters)

| Field | Shelf(s) | Evidence |
|-------|----------|----------|
| `_subpool`, `_isChildrens` on **granola** | granola | Only `_wholeGrainClaim` read in `granola-shelf-filters.ts`; `_subpool`/`_isChildrens` grep hits are JSON-only |
| `_category_routed` | cakes, cookies_coffee | `rg "_category_routed" bari-web/src --glob "*.{ts,tsx}"` → **no matches** (JSON only) |
| `_source_retailers` | cakes, cookies_coffee | `rg "_source_retailers" bari-web/src --glob "*.{ts,tsx}"` → type-only in `cakes-hard-cookies-page-data.ts:46`, never read |
| `_has_phvo` on **cookies_coffee** | cookies_coffee | Field present in JSON; `cookies-coffee-page-data.ts` does not reference `_has_phvo` (cakes shelf owns the filter) |

---

## 4. Curation rules (checker violations → fix in conform sweep)

1. **no-image:** missing or empty `imageUrl` → violation (product to discard in sweep).
2. **size-duplicate-sets:** two+ products with the same size-normalized name (size tokens stripped) → violation (dedupe, keep one).
3. **rank/total mismatch:** `rank` must match descending score order; `categoryTotal` must equal live product count.

---

## 5. Consumer-copy hygiene (flagged, copy fixes separate)

In `insightLine`, `rowVerdict`, `expansion.comparisonContext`, `expansion.positiveSignals[]`, `expansion.limitingFactors[]` text:

- No internal id prefixes: `jc-`, `snk-`, `hc-`
- No `bsip1_` / `bsip1-` tokens
- No raw barcode or product `id` embedded in copy
- No raw E-codes (`E\d{3}`)
- No `NN/grade:` score prefix pattern

---

## 6. Live shelf map (page-data imports)

| Shelf id | Served JSON | page-data import |
|----------|-------------|------------------|
| bread | `bread_frontend_v3.json` | `bread-comparison-page-data.ts` |
| brined_cheeses | `brined_cheeses_frontend_v2.json` | `brined-cheeses-page-data.ts` |
| cakes | `cakes_hard_cookies_frontend_v1.json` | `cakes-hard-cookies-page-data.ts` |
| cereals | `cereals_frontend_v2.json` | `cereals-page-data.ts` |
| cheese | `cheese_frontend_v4.json` | `cheese-page-data.ts` |
| cookies_coffee | `cookies_coffee_frontend_v2.json` | `cookies-coffee-page-data.ts` |
| granola | `granola_frontend_v1.json` | `granola-page-data.ts` |
| hard_cheeses | `hard_cheeses_frontend_v2.json` | `hard-cheeses-page-data.ts` |
| hummus | `hummus_frontend_v5.json` | `hummus-comparison-page-data.ts` |
| juices | `juices_frontend_v3.json` | `juices-page-data.ts` |
| milk | `milk_frontend_v1.json` | `milk-page-data.ts` |
| snacks | `snacks_frontend_v3.json` | `snacks-comparison-page-data.ts` |

Snacks uses **v3** (`snacks_frontend_v3.json`), not v2.

---

## 7. Violation classes (drift report)

| Class | Meaning |
|-------|---------|
| `missing-required` | Required key missing or wrong type |
| `forbidden-present` | Deep-dive / bespoke key present |
| `no-image` | Empty/missing `imageUrl` |
| `size-duplicate-sets` | Same product, different package size |
| `rank/total-mismatch` | Rank or `categoryTotal` inconsistent |
| `copy-hygiene` | Internal token / E-code / barcode leak in consumer copy |
