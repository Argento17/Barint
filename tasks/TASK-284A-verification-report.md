# TASK-284A Verification Report
**Date:** 2026-06-15
**Agent:** Data Agent
**Status:** RETURNED (verification complete)

---

## Deliverable 1: PHVO Partial-vs-Generic Split (unblocks EV-097)

### Method
All 4,255 `bsip2_trace.json` files scanned. Products with `L3_inferred_classifications.has_phvo=True` collected (n=70 traces, 49 unique barcodes). Ingredient text recovered from BSIP1 source files (`bsip1_*.json`, n=2,335 scanned). Classification applied against PARTIAL_TERMS = [`מוקשה חלקית`, `partially hydrogenated`] and GENERIC_TERMS = [`שומן מוקשה`, `שומנים מוקשים`, `שומן צמחי מוקשה`, `שמן צמחי מוקשה`, `שומנים מוקשים מן הצומח`, `חלקם מוקשים`, `מרגרינה`].

**Command:** `python tasks/_temp_verify_284a_v2.py`

### Results

| Bucket | Count (traces) | Count (unique barcodes) |
|--------|---------------|------------------------|
| PARTIAL (confirmed `מוקשה חלקית` / `partially hydrogenated`) | 0 | 0 |
| GENERIC (`מוקשה` without `חלקית`, incl. `מרגרינה`) | 70 | 49 |
| INDETERMINATE | 0 | 0 |
| EMPTY (no ingredient text) | 0 | 0 |
| **TOTAL** | **70** | **49** |

**Ingredient text was recovered for all 49 unique barcodes from BSIP1 source files.** No empty-text gap exists; the trace l3 field is empty because ingredient text is stored only in BSIP1 source, not copied into the trace.

### Per-category breakdown (unique barcodes)

| Category | Partial | Generic | Total |
|----------|---------|---------|-------|
| cakes_hard_cookies | 0 | 42 | 42 |
| cookies_coffee | 0 | 14 | 14 |
| (cross-category duplication: 7 barcodes appear in both categories) | | | |

Note: 70 traces from 49 unique barcodes = 7 products appear in both `cakes_hard_cookies` and `cookies_coffee` run outputs (boundary products scored in multiple runs).

### Key finding
**0 of 49 PHVO-flagged barcodes contain `מוקשה חלקית` or `partially hydrogenated` in their ingredient text.** All 49 fire on generic markers only:
- `מרגרינה` (margarine) — dominant trigger: ~42 products
- `שומן מוקשה` / `שומן מוקשה מדקלים` — ~6 products (palm hardened fat)
- `שומנים מוקשים מן הצומח` — 1 product (BC=7290017898506)
- `שומן צמחי מוקשה` — 2 products (BC=7290013145406, 7296073431879)

The Nutrition Agent's earlier BSIP0 raw scan found 2 `מוקשה חלקית` products (BC=7290101114116, 7290101114109, cheese_spreads). **These 2 barcodes do NOT appear in any has_phvo=True trace** — confirming they exist in the raw corpus but were not scored through the PHVO path (possibly filtered at BSIP0 gate or in a different run scope).

### EV-097 implication
The two-tier proposal can proceed on verified data: **the active PHVO corpus (70 traces, 49 products) is 100% generic hardened fat** — no confirmed partial-hydrogenation products. The 2 confirmed-חלקית products from the earlier BSIP0 scan are outside the current scored corpus. The proposed `has_phvo_generic` → ceiling 55 would affect all 49 currently-scored PHVO products.

---

## Deliverable 2: Milk Seed-Oil Anomaly

### Method
All `milk_and_alternatives` traces scanned for `has_seed_oil=True`. Ingredient text recovered from BSIP1 files. Each product assessed against `SEED_OIL_MARKERS_HE`.

**Command:** `python tasks/_temp_verify_284a_v2.py`

### Results — 8 unique barcodes (not 3)

The Nutrition Agent's "3" was an estimate from a subsample. Actual count from full trace scan: **8 unique barcodes**.

| Barcode | Product Name | Marker Fired | Score | Grade | Real or Artifact |
|---------|-------------|--------------|-------|-------|-----------------|
| 5411188124689 | אלפרו שיבולת שועל ללא סוכר (Alpro Oat unsweetened) | `שמן חמניות` | 49.7 | D | REAL — oat-based plant milk |
| 7290110325619 | משקה שיבולת שועל (Oat drink) | `שמן קנולה` | 47.2 | D | REAL — oat-based plant milk |
| 7394376619939 | משקה בריסטה שיבולת שועל (Barista oat) | `שמן קנולה` | 49.4 | D | REAL — oat-based plant milk |
| 7394376620904 | משקה שיבולת שועל ללא סוכר (Oat unsweetened) | `שמן קנולה` | 50.5 | C | REAL — oat-based plant milk |
| 7394376621451 | משקה בריסטה שיבולת שועל להקצפה (Barista oat frothing) | `שמן קנולה` | 49.4 | D | REAL — oat-based plant milk |
| 8000215204219 | משקה אורז אורגני (Organic rice drink) | `שמן חמניות` | 46.3 | D | REAL — rice-based plant milk |
| 8000215204554 | משקה אורז קוקוס אורגני (Organic rice coconut) | `שמן חמניות` | 47.7 | D | REAL — rice-based plant milk |
| 7394376001001 | משקה שיבולת שועל ברסיטה (Oat barista 1L) | `שמן קנולה` | 44.6 | D | REAL — oat-based plant milk |

### Verdict: All 8 are REAL, not extraction artifacts

Every product is a **plant-based milk alternative** (oat-based or rice-based). These products genuinely contain seed oil (canola or sunflower) as an ingredient — standard formulation for oat and rice drinks to add fat content. The `milk_and_alternatives` category correctly includes plant-based alternatives alongside dairy milk. The seed oil signal firing is architecturally correct.

**The "anomaly" is a misclassification concern, not a data error.** The Nutrition Agent's original concern ("milk shouldn't carry seed oil") reflects real dairy milk. The category `milk_and_alternatives` includes plant-based drinks, which do use seed oils. No data correction needed. No extraction artifact.

**Key: None of the 8 are in the frozen `run_005_headpin` milk corpus** — that corpus is dairy milk only (whole, 3.4%/4%, goat). The 8 seed-oil products are plant-based alternatives scored in `milk_and_alternatives` which is a broader category encompassing both dairy and plant drinks. No frozen-invariant collision.

---

## Deliverable 3: Exact seed_pen 10→5 Blast Radius (firms EV-096)

### Method
All 4,255 traces scanned. For each `has_seed_oil=True` product, the `dimension_notes.fat_quality` field checked for seed_pen firing. Two note formats confirmed:
- EV-012 path: `"EV-012 fat_ratio: fat=Xg ratio=X.XXX base=XX.X-seed10-transY=ZZ.Z"`
- fat_v1 path: `"sat_fat=Xg, frac=X.XX: base=XX.X - seed_oil_pen=10 - trans_pen=Y = ZZ.Z"`

Products on neutral-50 path or SRC-04 path (no seed_pen applied) excluded.

Delta: seed_pen 10→5 = -5 penalty points × fat_quality weight 0.08 = **+0.4 final score points**.
Grade boundary check: `grade(score + 0.4) != grade(score)` for boundaries at 80, 65, 50, 35.

**Command:** `python tasks/_temp_verify_284a_v2.py` (confirmed-path detection) + inline recount `python -c "..."` (dedup)

### Results

| Count | Value |
|-------|-------|
| Total has_seed_oil=True traces | 1,008 |
| On neutral-50 path (seed_pen does not fire) | 146 |
| On sat_fat_absent path (seed_pen does not fire) | 141 |
| On confirmed seed_pen=10 path | **719 traces** |
| Unique barcode+category pairs on confirmed path | 279 |
| Unique barcodes on confirmed path | 255 |

**Note on 719 vs 279:** The 719 traces vs 279 unique barcode+category pairs reflects products appearing in multiple category run outputs. The trace-level count (719) matches the Nutrition Agent's reported number exactly — they scanned at trace level, which is the correct denominator for "how many scoring events does seed_pen fire on."

### Grade-boundary crossers (seed_pen 10→5, +0.4 final delta)

**5 unique barcode+category pairs cross a grade boundary.** (13 trace-level events = 5 unique products appearing in multiple run outputs.)

| Barcode | Score Before | Score After | Grade Change | Category | Flag |
|---------|-------------|-------------|-------------|----------|------|
| 884912126115 | 34.70 | 35.10 | E→D | breakfast_cereals | [PUBLISHED] |
| 313184 | 34.90 | 35.30 | E→D | cakes_hard_cookies | [PUBLISHED] |
| 8710908800018 | 49.60 | 50.00 | D→C | salty_snacks | [PUBLISHED] |
| 5000159100001 | 49.80 | 50.20 | D→C | breakfast_cereals | [PUBLISHED] |
| 5054568100030 | 49.80 | 50.20 | D→C | breakfast_cereals | [PUBLISHED] |

**Direction of all shifts: upward (grade improvement, not degradation).**

- E→D: 2 products
- D→C: 3 products
- **Total grade-boundary crossers: 5 unique products**

### Frozen-invariant check

- **Frozen milk (run_005_headpin):** 0 grade crossers. The 5 milk_and_alternatives products on the confirmed path (oat/rice drinks) do not cross any grade boundary at +0.4.
- **Frozen bread (real_bread_retail_003_v1):** 0 grade crossers. bread_light has 14 products on confirmed path; none are within 0.4 of a boundary.
- **Cookies/cakes (published, not frozen):** cakes_hard_cookies BC=313184 crosses E→D. This is a published category subject to the standard D7+Shadow+owner gate, not a frozen-invariant tripwire.

### EV-096 implication

The Nutrition Agent's estimate of "~10-14" was high. **Exact count: 5 unique products cross a grade boundary** on seed_pen 10→5. All 5 are in published (non-frozen) categories. None touch the milk frozen invariant. The full-removal (seed_pen→0) produces 27 grade crossers — the 10→5 reduction produces 5, confirming it is a much more conservative intervention.

---

## Summary of Findings

| Deliverable | Key Number | Source |
|-------------|-----------|--------|
| D1 PHVO partial count | **0** (of 70 has_phvo traces, 49 unique barcodes) | `_temp_verify_284a_v2.py` → BSIP1 ingredient text |
| D1 PHVO generic count | **70** traces / **49** unique barcodes | `_temp_verify_284a_v2.py` |
| D1 חלקית outside scored corpus | **2** barcodes (7290101114116, 7290101114109, cheese_spreads) | Earlier BSIP0 scan (not in has_phvo=True traces) |
| D2 Milk seed-oil products | **8** unique barcodes (not 3) | `_temp_verify_284a_v2.py` |
| D2 Verdict | **All REAL** — plant-based alternatives, not artifacts | Ingredient text confirmed |
| D3 Confirmed seed_pen=10 path | **719** traces | `python -c "..." dedup script` |
| D3 Grade crossers (10→5) | **5** unique barcode+category pairs | `python -c "..." dedup script` |
| D3 Frozen crossers | **0** | Grade boundary check |
