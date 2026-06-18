# Granola Diff Report v1 — Generator vs Live

Generated: 2026-06-12
Generator output: `03_operations/page_generator/outputs/granola_generated_v1.json`
Live page: `bari-web/src/data/comparisons/granola_frontend_v1.json`

## Summary counts

| Category | Count |
|----------|-------|
| Products in generator | 25 |
| Products in live page | 42 |
| Common (both) | 24 |
| LIVE_DEBT (live has, generator correctly excludes) | 18 |
| GAP (generator has, live doesn't — net new) | 1 |
| COPY_PHASE diffs (PENDING strings vs authored copy) | 25 products |
| Grade diffs in common | 0 |

## Classification

### LIVE_DEBT — Live page has these, generator correctly excludes them

Generator excludes these because their corpus records carry `off_candidate_panel` in `canonical_risk_flags` (TASK-238 OFF ban). These products were on the live page before the OFF ban. They must NOT be re-added until a clean re-scrape replaces the OFF-contaminated corpus record.

| Barcode | Name (live) | Score/Grade (live) | Exclusion reason |
|---------|------------|-------------------|-----------------|
| 7297488099821 | Sugarless Gluten Free Granola | 71/B | off_banned |
| 7290120871069 | Granola Protein | 75/B | off_banned |
| 7290114603034 | גרנולה אגוזים ציפוקיים וחמוציות | 68/B | off_banned |
| 7290019603634 | גרנולה קוקוס ופירות | 60/C | off_banned |
| 7290011668570 | גרנולה | 52/C | off_banned |
| 3560070826186 | MUESLI & Co 2 CHOCOLATS & NOISETTES | 51/C | off_banned |
| 7613035758834 | פיטנס גרנולה חמוציות | 46/D | off_banned |

Additionally, these live products have `bsip_cereal_subtype` ≠ `granola` — they were in the live page but the subpool split was not enforced at build time. The generator correctly excludes them per the `subpool_filter`:

| Barcode | Name (live) | Score/Grade (live) | Live subtype | Exclusion reason |
|---------|------------|-------------------|-------------|-----------------|
| 5018357006731 | תע.דגנים 40% פירות ואגוז | 68/B | oat_cereal | subpool_filter |
| 5018357006755 | תע.דגנים 50% פירות ואגוז | 55/C | oat_cereal | subpool_filter |
| 5010026515919 | Mornflake Crispy Muesli Nutty | 70/B | (off_banned also) | off_banned |
| 5010026521149 | Crispy Muesli | 54/C | (off_banned also) | off_banned |
| 7290011131371 | מוזלי קראנצ'י בוטן +שקדים | 46/D | muesli | subpool_filter |
| 7290011131388 | מוזלי קראנצ'י תפוח קינמון | 44/D | muesli | subpool_filter |
| 7290011131395 | מוזלי 30% פירות | 26/E | muesli | subpool_filter |
| 7290014471412 | מוזלי בוטנים, לוז, שקדים | 40/D | muesli | subpool_filter |
| 7290014471429 | מוזלי פירות יבשים | 32/E | muesli | subpool_filter |
| 7290014471436 | מוזלי ציפוק תפוח וקינמון | 36/D | muesli | subpool_filter |
| 7290016883183 | מוזלי 47% דגנים מלאים | 38/D | muesli | subpool_filter |

Note on barcode 7290014471436: the TASK spec flagged this as "live shows D, trace says E". The live page indeed shows D (36/D). The generator output for this product is excluded via subpool_filter (bsip_cereal_subtype=muesli). If subpool were re-classified as granola, the trace score is 36.0 → grade E (floor policy). So the live D is incorrect — this would be a LIVE_DEBT grade inflation. Generator correctly flags via subpool exclusion.

### GAP — Generator has this, live page doesn't

| Barcode | Name | Score/Grade (generator) | Action |
|---------|------|------------------------|--------|
| 7290014471443 | גרנולה אבוזים (Granola Nuts — Telma) | 36.7/D | KEEP — new product in run_cereals_008, not in live page. Should be included. Not a gap in the generator — the generator is correct. |

### COPY_PHASE — Present in both, copy fields differ

All 25 generator products have `insightLine="PENDING_COPY"`, `rowVerdict="PENDING_COPY"`, and `expansion.comparisonContext="PENDING_COPY"`. The live page has authored Hebrew copy for all 24 common products. These diffs are expected — the copy engine is Phase 2.

- 24 products: all copy fields PENDING_COPY vs authored live copy → **COPY_PHASE** for all
- `expansion.positiveSignals` = `[]` in generator vs authored arrays in live → **COPY_PHASE**
- `expansion.limitingFactors` = `[]` in generator vs authored arrays in live → **COPY_PHASE**

### Data diffs in common (24 products)

- **confidence fields**: generator maps mechanically from trace `confidence_band` + missing fields; live has hand-authored labels. Some may differ in label text — these are **COPY_PHASE** differences.
- **imageUrl**: generator has 25/25 (100%); live had 78.6%. Generator correctly carries all images from BSIP1. Images are 25/25 non-null.
- **score/grade**: 0 grade diffs in the 24 common products. Scores match within tolerance.

## Gate summary

```
G1 SCHEMA:   PASS
G2 COVERAGE: PASS — 25/25 imageUrl, name, score, grade; images 100%
G3 SCOPE:    PASS — 25 displayed, 63 in run, 75 exclusions all documented
G4 OFF:      PASS — no OFF markers in products array
G5 GRADE-INTEGRITY: PASS
G6 COPY-SAFETY:     PASS
G7 PARITY:   PASS (informational)
Overall: PASS
```

## Source paths discovered

- Granola corpus: `03_operations/bsip1/run_cereals_005/output` (66 products) + `03_operations/bsip1/run_cereals_multiretailer_001/output` (37 products)
- Granola BSIP2 runs: `02_products/breakfast_cereals/bsip2_outputs/run_cereals_008/products` (63 traces) + `02_products/breakfast_cereals/bsip2_outputs/run_cereals_multiretailer_001/products` (37 traces)
- Source confirmed via: `granola.ts` → `granola-page-data.ts` → `granola_frontend_v1.json`; `_meta.provenance` in live JSON
- Subpool filter: `bsip_cereal_subtype=granola` in BSIP1 corpus records
