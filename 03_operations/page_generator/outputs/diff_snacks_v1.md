# Snacks Diff Report v1 — Generator vs Live

Generated: 2026-06-12
Generator output: `03_operations/page_generator/outputs/snacks_generated_v1.json`
Live page: `bari-web/src/data/comparisons/snacks_frontend_v2.json`

## Summary counts

| Category | Count |
|----------|-------|
| Products in generator | 53 |
| Products in live page | 18 |
| Common (both) | 17 |
| LIVE_DEBT (live has, generator doesn't) | 0 |
| NEW (generator has, live doesn't — run universe) | 36 |
| COPY_PHASE diffs | 18 live products |
| Grade diffs in common | 10 — all LIVE_DEBT (live carries stale pre-headpin scores) |
| snk-003/snk-004 barcode duplicate | 1 — see note |

## Classification

### LIVE_DEBT — Grade differences in common products

The live snacks page was hand-assembled using the older production baseline (2026-05-17) with lower scores. The generator uses `run_snack_bars_001` which has updated scores from the headpin rebaseline (`run_snackbars_007_headpin`, TASK-180B). All 10 grade diffs are cases where the generator's score is HIGHER and CORRECT — the live page has grade deflation that should be corrected.

| Barcode | Live score/grade | Generator score/grade | Classification |
|---------|-----------------|----------------------|---------------|
| 16000423534 | 44/D | 51.5/C | LIVE_DEBT (live D is stale; generator C is correct per headpin) |
| 16000548404 | 42/D | 53.5/C | LIVE_DEBT |
| 5900020039590 | 27/E | 46.0/D | LIVE_DEBT |
| 8410076610508 | 32/E | 38.9/D | LIVE_DEBT |
| 8423207206495 | 18/E | 58.8/C | LIVE_DEBT (large delta — live score appears to be from proto_v0 2026-05-17) |
| 8423207207362 | 16/E | 52.0/C | LIVE_DEBT |
| 8423207208260 | 48/D | 58.0/C | LIVE_DEBT |
| 8423207208680 | 41/D | 50.8/C | LIVE_DEBT |
| 8423207210287 | 57/C | 67.9/B | LIVE_DEBT (live page noted this as a ceiling-crowding concern in headpin run record; generator B is correct) |
| 8423207210928 | 46/D | 50.9/C | LIVE_DEBT |

Note: barcode 8423207210287 (snk-002) — live shows 57/C but both the headpin run record and the generator correctly compute 67.9/B. The live page provenance says "69.5/B note voided (product not displayed)" — but 8423207210287 IS in the live page at snk-002 with 57/C. This is a pre-headpin score. Generator's B is correct.

### NEW — 36 products in generator not in live page

The generator shows all 53 scored products. The live page displays only 18 (editorial curation). The 36 additional products are correctly shown in the generator output and would need editorial curation for the live page. These are NOT a generator gap — showing all scored products is the machine's correct behavior. Curation is a Phase 3 concern.

All 36 additional products represent the full scored corpus beyond the 18 editorially selected for display.

### snk-003/snk-004 duplicate barcode note

The live page has snk-003 (barcode=7290011498894) and snk-004 (barcode=7290011498948). snk-015 also has barcode=7290011498894 (same as snk-003). In the live page these are distinct entries with different `id` fields. The generator deduplicates by barcode — only one entry per barcode. This is a LIVE_DEBT in the live page (two entries with the same barcode, different ids). Generator correctly produces one entry per barcode.

### COPY_PHASE — Copy fields differ

All 53 generator products have `insightLine="PENDING_COPY"`, `expansion.comparisonContext="PENDING_COPY"`, `expansion.positiveSignals=[]`, `expansion.limitingFactors=[]`. The live 18 products have full authored copy. Not enumerated per product — all are COPY_PHASE.

The live page's `expansion.bottomLine`, `expansion.unknowns` (category-level invariant), and per-product copy are all absent from the generator output (PENDING). This is expected Phase 2 work.

### _internal_cluster

The live page carries `_internal_cluster` values (e.g. "date-simple") on all 18 products. The generator sets `_internal_cluster=null` for all 53 (this field requires Phase 2 copy engine classification). Classification: **COPY_PHASE**.

### Image coverage note

Generator: 48/53 (90.6%). Live: 18/18 (100%). The 5 generator products with null imageUrl have no image in the BSIP1 corpus (G2 confirms no regression vs BSIP1). The live page's 18 curated products may have manually added image URLs not in BSIP1 — these would be KEEP items for Phase 3 config.

## Gate summary

```
G1 SCHEMA:   PASS
G2 COVERAGE: PASS — 53/53 name/score/grade; 48/53 imageUrl (5 null = no BSIP1 image, correct)
G3 SCOPE:    PASS — 53 displayed = 53 in run; 0 exclusions; all accounted for
G4 OFF:      PASS — no OFF markers detected
G5 GRADE-INTEGRITY: PASS
G6 COPY-SAFETY:     PASS
G7 PARITY:   PASS (informational — 10 grade changes all LIVE_DEBT)
Overall: PASS
```

## Source paths discovered

- Snacks corpus: `03_operations/bsip1/run_001/output` (53/106 files used — the canonical snacks corpus)
  - Confirmed via: run_snackbars_007_headpin run_record.json `corpus=C:\Bari\03_operations\bsip1\run_001\output`, `corpus_n=53`
- Snacks BSIP2 traces: `02_products/snack_bars/bsip2_outputs/run_snack_bars_001/products` (53 dirs)
  - Source confirmed via: `snacks.ts` → `snacks-comparison-page-data.ts` → `snacks_frontend_v2.json`; `_meta.source_run_id="yochananof_snack_retail_v1"`
- BSIP1 canonical: `02_products/snack_bars/canonical_bsip1/run_001/` (53 flat BSIP1 files)
  - The run_001 at `03_operations/bsip1/run_001/output` contains all 106 bsip1 records; 53 have matching BSIP2 traces
