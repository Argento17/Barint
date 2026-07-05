---
id: TASK-517
title: Crackers page: author insight-first-voice copy for 53 products (19 existing + 34 new פריכיות), then QA gate + frontend regen
owner: content-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-05
closed_at: 2026-07-05
close_reason: >
  SHIPPED to local task506 branch, commits 15c9ce8c/2215abbb (TASK-516 pipeline) +
  ef68ca2f (this task's copy + regen), NOT YET pushed/PR'd to origin. Copy authored
  for all 53 products (19 rewritten, 34 new), two-gate signed off after one QA fix
  cycle (6 findings, all resolved and re-verified: garbled number, unsupported
  sugar superlative on a 1/3-null field, decimal rounding vs. nutrition panel,
  overstated relational claim, flour-blend math error -- see TASK-517 history).
  One genuine data defect found during gating (barcode 4267230 bidi bracket-mirror
  bug in raw Shufersal HTML) repaired via a narrow, unit-tested, signature-gated
  fix per Nutrition Agent's diagnosis (corpus-wide scan confirmed 1/54 affected,
  not systemic) -- logged as EXCEPTION-004, score/grade unaffected.
  Verified independently by orchestrator before commit: 53/53 displayed, 53 unique
  ranks, 0 OFF markers, 0 null brand, score==trace 53/53. run_gates.py 7/8 PASS
  (the 1 fail is TASK-486's pre-existing PENDING_COPY schema gap, unchanged, not a
  regression). Two known non-blocking follow-ups NOT done here: (1) 34 new products
  lack a _website_cluster value (existing wheat/spelt/rye taxonomy has no rice
  axis -- they render in the default view but not under shelf-filter chips until
  a rice-appropriate cluster is defined); (2) KRIT brand casing doc-consistency nit
  from TASK-516. Neither blocks what shipped. NOT pushed to origin -- still needs
  owner/orchestrator decision on PR timing.
category_id: crackers
summary: >
  Neither the 19 existing crackers products nor the 34 new ricecakes/פריכיות products (scored in TASK-516) have insight-first-voice copy authored yet -- the file assumed to be TASK-461's crackers overhaul draft was actually a data-rework snapshot with copy preserved verbatim. Author one unified pass (cereals golden template, Tom/Bari voice), then Adversarial QA two-gate sign-off, then regen crackers_frontend_v1.json (53 products) + run G1-G8 gates + validate_comparison_page.py before anything ships.
---

# TASK-517 — Crackers page: author insight-first-voice copy for 53 products (19 existing + 34 new פריכיות), then QA gate + frontend regen

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Data Agent return (mechanical regen + gate step)

**Scope executed:** targeted-merge of Content-Agent-authored copy (5 fields:
insightLine, rowVerdict, expansion.comparisonContext, expansion.positiveSignals,
expansion.limitingFactors) into the 19 existing crackers products (all other
fields preserved byte-for-byte except rank/categoryTotal) + full frontend-record
build for the 34 new ricecakes products from BSIP1/BSIP2 (generate_page.py's own
build_product()/render_fields helpers, reduced to the task486 parity schema) +
copy merge + image self-hosting + rank/categoryTotal recompute for all 53 + the
standard QA battery. No copy text was authored or edited by this pass.

**Result: NOT clean — 1 genuine new finding surfaced by validate_comparison_page.py.
Written to the live path (uncommitted); needs a decision before sign-off.**

### What's clean
- 53/53 displayed (19 existing + 34 new), barcode 7290112968807 confirmed still
  excluded (pre-existing, unrelated to this expansion).
- 19 existing products: diffed field-by-field against the pre-regen file — ONLY
  insightLine, rowVerdict, expansion.{comparisonContext,positiveSignals,
  limitingFactors}, rank, categoryTotal changed. Verified programmatically
  (0 unexpected diffs across all 19).
- 34 new products: full schema parity with the 19 (same field set, task486
  Deep-Dive fields absent on both sets), 0 exclusions (all 34 BSIP2 traces are
  data_sufficiency=sufficient).
- rank 1..53 unique, categoryTotal=53 on all 53, score==trace on all 53 (0
  mismatch), 0 OFF markers, 0 PENDING_COPY anywhere, 53/53 imageUrl (all
  self-hosted under bari-web/public/products/, 0 external URLs remain in the
  file — TASK-478 same-origin rule).
- run_gates.py: 6/8 gates PASS (G1 SCHEMA, G3 SCOPE, G4 OFF, G5
  GRADE-INTEGRITY, G6 COPY-SAFETY, G7 PARITY, G8 DATA-SANITY all PASS). The 2
  G2 COVERAGE FAILs (consumerExplanation.whyRated / bestUseCases still
  "PENDING_COPY") are **pre-existing** — reproduced identically by re-running
  the same gate against the untouched pre-regen 19-product baseline with its
  original run dir. TASK-486 (2026-07-03) deliberately removed those fields
  from the live page; the gate's v3-schema check was never updated to account
  for that removal. Not a regression from this task.
- The 3 decimal values Adversarial QA pre-adjudicated (10.5, 25.5, 13.6) did
  not recur as flags in this run at all (G6/G8 both clean).
- rank_check.py superlative check: PASS, 0 false claims, 5 manual-review WARNs
  (uniqueness/"היחיד" and one subpool-scoped claim — WARN only, matches the
  Content Agent's stated corpus-wide verification methodology in the copy
  file's own _meta).

### What's NOT clean — new finding, not pre-cleared
`validate_comparison_page.py` exit 1: **ingredient gate FAILs, 16/53 flagged**
(this same check PASSes 0/19 clean on the pre-regen baseline — this is 100%
new, introduced by the 34 ricecakes rows):
- **15/16 are gate-calibration false positives**, not data problems: genuinely
  short-but-complete ingredient lists (1-3 real ingredients, e.g.
  `"כוסמת (99.5%), מלח"` = buckwheat 99.5%, salt) that trip the check's
  `len(ingredients) < 40` heuristic. Nothing is missing or cut off; simple
  single-grain rice/buckwheat cakes legitimately have short lists.
- **1/16 is a genuine data defect**: barcode 4267230 (בsip1_ricecakes_4267230)
  — its `ingredients_text_he` in the BSIP1 record
  (`03_operations/bsip1/run_ricecakes_conform_001/output/bsip1_4267230.json`,
  a TASK-516 artifact predating this task) has systematically reversed/
  mismatched bracket pairs throughout (`"פריכיות אורז)אורז חום,מלח("` — close-
  paren before open-paren — consistent with a Hebrew RTL bidi bracket-flip
  scraping artifact), ending in an unclosed `{`. This was carried through
  verbatim (no BSIP1 text is ever rewritten by a frontend-packaging step).

**Flagged per Spec-Conflict Duty, not resolved unilaterally:** the task spec
requires "confirm final displayed count is exactly 53" while also requiring a
passing QA battery — for barcode 4267230 those two requirements are in
tension (discarding it would satisfy the gate but break the 53-count; leaving
it breaks the gate). Rewriting the bracket-flipped ingredient text myself
would be fabricating/cleaning structural data outside a "mechanical regen,
do not touch copy" mandate and outside a Data Agent's authority to do
unilaterally on a single product without a reproducible rule. Recommend:
Nutrition/Product Agent decide between (a) a reproducible bracket-repair rule
for this scrape-artifact class (if one can be confirmed against the raw
scrape) or (b) discard 4267230 per the same missing-data-discard rule already
used for 7290112968807, updating the expected count to 52. Until decided, the
regenerated file stays at 53 with this one row's ingredient text un-repaired.

**Known non-blocking gap (documented in `_meta.task517_expansion_and_copy`
in the JSON itself):** the 34 new ricecakes products do not carry
`_website_cluster` (whole_grain/mixed_grain/refined_white is a wheat/spelt/
rye-flour-percentage taxonomy with no rice axis; applying it as-is would
mislabel every whole-grain-rice product as "refined_white"). They render
correctly in the default "all products" view but won't appear under any of
the 3 shelf-filter chips until a rice-appropriate cluster axis is defined
(Product/Data judgment call, out of this task's mechanical scope).

### Process note
Running `bari-web/scripts/migrate-images-fetch.mjs` +
`migrate-images-rewrite.mjs` (required to self-host the 34 new products'
Shufersal/Cloudinary image URLs per the TASK-478 same-origin rule) had a
repo-wide side effect: it rewrote lingering external image URLs in 16
unrelated category JSON files that were apparently still un-migrated on this
branch's HEAD. Reverted all 16 via `git checkout --` immediately (verified by
mtime that they were untouched before my run and clean after revert) — out of
this task's scope and not something I should ship silently. 4 other
pre-existing dirty files (juices_frontend_v3.json, milk_frontend_v1.json,
milk-comparison.json, magnesium-page-data.ts) predate this session entirely
(mtime 2026-07-03) and were left untouched throughout.

**Not committed**, per instruction. New sign-off marker needed (the existing
`tasks/signoffs/crackers_frontend_v1.json.ok` is stale — covers the
brand-only version, not this content-and-expansion regen); per this task's
convention the orchestrator writes it, not the Data Agent.

```json
{
  "artifacts": [
    {"path": "C:\\Bari\\bari-web\\src\\data\\comparisons\\crackers_frontend_v1.json", "sha256": "576e9c799e9e49a41b3912167c54daca07b073bc5087f774d5b460594bfae069"},
    {"path": "C:\\Bari\\bari-web\\src\\data\\comparisons\\crackers_frontend_v1_gates_report.md", "sha256": "87538554ee5b9eba06631aed88daa1122a082351f019848e742166075af087c7"},
    {"path": "C:\\Bari\\tasks\\TASK-517.md", "sha256": "8d1364757d72e66647b196787d44550b99edd06c6024cae663deaf6db07219f8"}
  ],
  "counts": {
    "products_total": {"value": 53, "of": 53},
    "products_existing_preserved": {"value": 19, "of": 19},
    "products_new_built": {"value": 34, "of": 34},
    "new_products_excluded": {"value": 0, "of": 34},
    "copy_fields_merged_products": {"value": 53, "of": 53},
    "existing_products_nonzero_field_drift": {"value": 0, "of": 19},
    "rank_unique_1_to_53": {"value": 53, "of": 53},
    "categoryTotal_eq_53": {"value": 53, "of": 53},
    "score_eq_trace": {"value": 53, "of": 53},
    "imageUrl_present": {"value": 53, "of": 53},
    "imageUrl_self_hosted": {"value": 53, "of": 53},
    "imageUrl_external_remaining": {"value": 0, "of": 53},
    "off_markers_found": {"value": 0, "of": 53},
    "pending_copy_remaining": {"value": 0, "of": 53},
    "website_cluster_present": {"value": 19, "of": 53},
    "run_gates_G_pass": {"value": 6, "of": 8},
    "run_gates_G_fail": {"value": 2, "of": 8},
    "validate_page_hard_gates_pass": {"value": 6, "of": 7},
    "validate_page_ingredient_flags": {"value": 16, "of": 53},
    "validate_page_ingredient_flags_benign_short_list": {"value": 15, "of": 16},
    "validate_page_ingredient_flags_genuine_defect": {"value": 1, "of": 16},
    "rank_check_false_superlatives": {"value": 0, "of": 3},
    "rank_check_manual_review_warns": {"value": 5, "of": 5}
  },
  "commands_run": [
    {"cmd": "python build_ricecakes_products.py", "exit_code": 0},
    {"cmd": "python merge_final.py", "exit_code": 0},
    {"cmd": "node scripts/migrate-images-fetch.mjs", "exit_code": 0},
    {"cmd": "node scripts/migrate-images-rewrite.mjs", "exit_code": 0},
    {"cmd": "git checkout -- <16 unrelated files>", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py bari-web/src/data/comparisons/crackers_frontend_v1.json --corpus <combined> --run <combined> --schema page_output_schema_v1.json --baseline <pre-regen 19-file>", "exit_code": 1},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py <pre-regen 19-file> --corpus run_crackers_conform_001/output --run run_crackers_conform_001/products (control run to isolate pre-existing vs new FAILs)", "exit_code": 1},
    {"cmd": "python 03_operations/spine/validate_comparison_page.py --json crackers_frontend_v1.json --traces run_crackers_conform_001/products run_ricecakes_conform_001/products", "exit_code": 1},
    {"cmd": "python 03_operations/spine/validate_comparison_page.py --json <pre-regen 19-file> --traces run_crackers_conform_001/products (control run)", "exit_code": 0},
    {"cmd": "python 03_operations/validators/rank_check.py --json crackers_frontend_v1.json", "exit_code": 0}
  ],
  "not_done": [
    "validate_comparison_page.py ingredient gate is not green (16/53 flagged; 1 is a genuine BSIP1-source defect on barcode 4267230, needs Nutrition/Product decision between bracket-repair or discard-to-52)",
    "_website_cluster not assigned to the 34 new products (needs a rice-appropriate cluster axis decision, out of mechanical-regen scope)",
    "run_gates.py G2 v3-schema check still fails on consumerExplanation.whyRated/bestUseCases (pre-existing gap predating this task, not fixed — would require editing the shared gate script, a QA-owned instrument)",
    "New sign-off marker not written (orchestrator's job per stated convention)",
    "Nothing committed (per instruction)"
  ],
  "acceptance_test": {
    "spec_requirement": "regenerate crackers_frontend_v1.json (53 products), run run_gates.py + validate_comparison_page.py, confirm 0 OFF/0 PENDING_COPY/imageUrl 53/53, report exact counts/hashes/gate results",
    "result": "PARTIAL — regen mechanically complete and internally verified (53/53, 0 OFF, 0 PENDING_COPY, 53/53 imageUrl all self-hosted, 19-existing field integrity proven by diff), but the QA battery is NOT all-green: validate_comparison_page.py exits 1 on a genuine new finding (1 corrupted-bracket ingredient string inherited from TASK-516 BSIP1 output, plus 15 benign short-list false positives on the same check). run_gates.py's 2 FAILs are pre-existing/unrelated. This is reported per instruction ('DO fail on any other new leakage') rather than silently passed."
  }
}
```
