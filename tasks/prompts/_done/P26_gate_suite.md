# P26 / TASK-257 Phase 0b — Gate suite as code (route: C1)

CONTEXT: Repo C:\Bari. We are building a page GENERATOR (TASK-257): scored shelf →
complete category page. Before the generator exists, its correctness checks must
exist as CODE, because every failure of the last launch attempt (17/87 products
shown, images silently dropped, copy defects) was machine-detectable and nobody ran
a machine. These gates run on ANY category frontend JSON, today and forever.

BUILD: 03_operations/page_generator/gates/run_gates.py  (Python 3, stdlib only)
Usage: python run_gates.py <frontend_json> --corpus <bsip1_output_dir>
       --run <bsip2_run_products_dir> [--baseline <current_live_json>]
       [--schema <schema.json>] [--config <category_gate_config.json>]
Output: gates_report.md next to the input + exit code 0 (all pass) / 1 (any FAIL).
Each gate prints PASS/FAIL/WARN + evidence lines. One module per gate is fine, but
one entrypoint.

THE 7 GATES:
1. SCHEMA — input validates against the contract schema (path via --schema; if the
   P25 schema at 03_operations/page_generator/contract/page_output_schema_v1.json
   exists, default to it; if absent, SKIP with a warning, don't fail).
2. COVERAGE — for every display field (imageUrl, name, score, grade, insightLine,
   expansion.nutrition.*, expansion.ingredients, confidence labels): report non-null
   N/M. HARD RULES: imageUrl coverage must be >= the source corpus's image coverage
   (look up each barcode in --corpus BSIP1 files; if BSIP1 has an image and the JSON
   doesn't → FAIL, list barcodes). `name` must contain Hebrew characters (range
   ֐-׿) → else FAIL per product.
3. SCOPE — displayed product count vs scored count in --run (count trace dirs).
   Every missing barcode must be enumerated in _meta exclusions (any _meta key
   containing 'exclu'/'dedup') with a reason. Unexplained missing barcode → FAIL.
4. OFF — scan the JSON AND the corpus records of displayed barcodes for
   open_food_facts / openfoodfacts.org / images.openfoodfacts markers and
   panel_source=open_food_facts → any hit = FAIL (TASK-238 hard rule).
5. GRADE-INTEGRITY — recompute grade from score with the central scale
   (S>=90, A>=80, B>=65, C>=50, D>=35, else E) and compare to the JSON grade
   (respect a per-product cap-exception flag like _aCappedToB if present);
   compare JSON score to the trace's final_score_estimate (tolerance 0.05 after
   rounding; boundary policy configurable: --config {"boundary":"floor"|"round"},
   default floor — an engine E must never display as D). Mismatch → FAIL.
   Also: scan insightLine/rowVerdict prose for standalone Hebrew grade letters
   (א/ב/ג/ד/ה bounded by non-Hebrew) ≠ badge grade → FAIL. (Beware false
   positives: מ"ג, לל"ג, ה- prefixes — bound the regex by Hebrew-letter context.)
6. COPY-SAFETY — FAIL on: sodium causally framed (נתרן within 30 chars after
   כי/בגלל/בשל); prior-run refs (הציון הקודם, גרסה הקודמת, שלא הועברו, run_);
   framework leakage in consumer strings (NOVA, BSIP, cap=, proxy, dimension);
   the 9 banned phrases from 03_operations (search the claim_entailment rubric v2
   for the banned list and embed it).
7. PARITY (only when --baseline given) — vs the current live JSON: product count,
   image coverage %, avg consumer-text chars per product, per-barcode grade diffs,
   products removed/added. NEVER auto-fails; always emits the side-by-side table —
   this is the owner's swap-decision artifact.

VALIDATE BEFORE RETURNING (this is the acceptance test):
A. Run on bari-web/src/data/comparisons/yogurts_frontend_v4.json with
   --corpus 03_operations/bsip1/run_yogurt_006/output
   --run 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2/products/products
   --baseline bari-web/src/data/comparisons/yogurts_frontend_v3.json
   → MUST FAIL: gate 2 (6 images missing that BSIP1 has) and gate 3 (≈70 scored
   products unexplained). If it passes, your gates are broken — fix them.
B. Run on the granola frontend JSON with its sources (find them via
   bari-web/src/lib/comparisons/registry/categories/granola.ts and
   02_products/granola*/ + 03_operations/bsip1/) → expected mostly PASS; report
   what fails and why (that's signal about the working pages, don't "fix" data).

RULES: read-only outside 03_operations/page_generator/gates/. No OFF. No network.
Do not modify any frontend JSON, corpus, or trace. No score changes.

RETURN BLOCK: file paths; the two validation run outputs (verbatim summary tables);
exit codes; any gate you could not implement and why. Propose RETURNED.

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and tick the P26 line.
