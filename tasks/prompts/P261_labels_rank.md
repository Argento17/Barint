# P261 / Label remediation (cookies + cakes) + rank reindex (route: C1-CURSOR)

Repo C:\Bari, site under bari-web. TASK-420. STAGING ONLY — no commit/push/deploy. Do NOT run git stash/checkout/reset beyond your own lane. Touch ONLY these files: `cookies_coffee_frontend_v2.json`, `cakes_hard_cookies_frontend_v1.json`, `cheese_frontend_v4.json`, `chocolate_bars_frontend_v1.json`, `milk_frontend_v1.json` (all under bari-web/src/data/comparisons/). NO published-score changes (do not alter any `score` value). OFF-ban. NEVER invent data.

Materiality rule (owner policy [[missing_data_discard_rule]]): a product whose MATERIAL nutrition fields are missing (the scoring inputs: energy, protein, fat_g, sugar, sodium) should be DISCARDED from the page — NOT shown with a "partial/missing" label. A product that carries a "partial" label but actually HAS complete material data is a STALE LABEL → correct it to full-confidence (clear `confidence_label_he`="ניתוח חלקי" and the matching `confidence_tooltip_he` missing-data text; set the confidence to the full/complete state used by complete products in the same file). Fiber-only-null is NOT material (engine handles it) → keep, do not flag.

## 1. cookies_coffee_frontend_v2.json (owner already ruled)
- SORT the products array by `score` descending; reindex `rank` 1..N (this file was excluded from the earlier sort batch).
- DISCARD exactly these 2 products (genuinely missing material data — sodium / protein null): `ck-7290017724171` and `ck-7296073659969`.
- RELABEL to full-confidence every product that carries `confidence_label_he`="ניתוח חלקי" but has ALL of energy/protein/fat_g/sugar present (~30 stale-complete). Keep sugar-null (~5) and fiber-only-null (~26) as they are.
- Report: final N, the 2 discarded, count relabeled, count kept-as-partial.

## 2. cakes_hard_cookies_frontend_v1.json (apply the same rule; ALL 63 currently flagged partial)
- For each product, classify by material-field completeness: (A) genuinely missing a MATERIAL field (energy/protein/fat_g/sugar/sodium) → DISCARD; (B) complete data but stale "partial" label → RELABEL to full; (C) fiber-only-null → keep.
- Apply: discard tier A, relabel tier B. Report the exact tiering counts + the barcodes of every discarded product with which material field was null (evidence).
- (Products already sorted by score from the prior batch — preserve order; only reindex rank if you remove products.)

## 3. rank reindex (display bug — rank field ≠ position)
For `cheese_frontend_v4.json`, `chocolate_bars_frontend_v1.json`, `milk_frontend_v1.json`: these are already score-sorted but their `rank` field is not a clean 1..N by position. Reindex `rank` = 1-based array position. Do NOT reorder (already sorted); only fix rank. No other field changes.

## Verify + report
Per file: N before/after, monotonic-by-score confirmed, rank=1..N confirmed, and for cookies/cakes the discard+relabel counts with evidence. Confirm 0 `score` values changed. End with the return contract (01_framework/operations/return_contract_v1.md); status RETURNED, not CLOSED. Give trace-derived counts + the command that produced them.
