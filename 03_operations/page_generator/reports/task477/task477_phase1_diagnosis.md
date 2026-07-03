# TASK-477 Phase 1 — Protein-bars corpus lineage cleanup + ingredient-handoff re-measure

Status: DIAGNOSE + CLEAN + MEASURE only. No live score changed. No rescore shipped.
Worktree: `C:\bari_wt_t477`, branch `fix/task477-protein-corpus`, base `origin/master` @ `f2908d2f` (merge PR #65 fix/task481-tablets).

## 1. True live protein-bars corpus lineage

The live route (`bari-web/src/app/hashvaot/protein-bars/`) imports
`bari-web/src/lib/comparisons/protein-bars-comparison-page-data.ts`, which loads
`bari-web/src/data/comparisons/protein_combined_frontend_v2.json` directly (not
through the generic comparison-corpus loader's category registry — a hardcoded
static import).

`protein_combined_frontend_v2.json._meta` self-declares:
- `run_id: protein_bars_task365_rescore_20260621_134052`
- `corpus_source: C:\Bari\02_products\snack_bars\protein_combined_corpus_task365_33_20260621_fix.json`
- `corpus_sha256: 469c65015bb7e5e80cd844d5d69066c53048e2f34446c917b0eb2b1b77987dc3`

Verified independently (not just trusting the self-declared meta):
- `protein_combined_corpus_task365_33_20260621_fix.json` on disk hashes to
  **469c65015bb7e5e80cd844d5d69066c53048e2f34446c917b0eb2b1b77987dc3** — exact match.
- This corpus contains 33 products (`_discarded_barcodes`: 2 WIN barcodes,
  `7290015130271`/`7290015130288`, dropped for truncated ingredient lists per
  `missing_data_discard_rule`).
- `02_products/snack_bars/bsip2_outputs/protein_bars_task365/rerank_table_rescore.json`
  (the actual scoring output, run_id matches) contains exactly the same 33
  barcodes as the corpus — 0 extra, 0 missing.
- The live frontend displays 32/33 (the 33rd, granola barcode `7290112497994`,
  is scored but not surfaced on the page — legitimate editorial curation, not
  contamination: same barcode present in corpus + rerank, simply not rendered).

**Conclusion: the true live corpus is the 33-product
`protein_combined_corpus_task365_33_20260621_fix.json` file itself.** There is
no BSIP1 trace directory behind it — it was built and scored inline
(`batch_run_protein_bars_task365.py` / `rescore_task365_inplace.py`) directly
from a flat corpus JSON, confirming the config's own `_reproduce_note` and
`_comment` claims are accurate, not stale (except one stale detail: the
`_comment`'s "16/33 curated" line describes a pre-rescore build state; the
current live page shows 32/33, not 16/33).

## 2. Contamination diagnosis

**a) `02_products/snack_bars/bsip2_outputs/protein_bars_task365/` (the dir the
config's `corpus_dirs`/`run_products_dir` point at) has ZERO `bsip1_*.json`
files** — confirmed (`rerank_table.json`, `rerank_table_rescore.json`,
`run_record.json`, `run_record_rescore.json` only). This matches the task
description exactly.

**b) Candidate BSIP1 trace dirs exist elsewhere in the tree, none of which
fully covers the 33-product corpus:**

| Candidate dir | Files | Overlap w/ true 33-corpus |
|---|---|---|
| `02_products/snack_bars/canonical_bsip1/run_001` | 106 | 2/33 |
| `02_products/snack_bars/canonical_bsip1/run_task362` | 41 | 14/33 |
| `03_operations/bsip1/run_snacks_task360_phase2_.../output` | 28 | 0/33 |
| `03_operations/bsip1/run_snacks_task360_phase3_.../output` | 113 | 18/33 |
| `03_operations/bsip1/run_snacks_task360_shuf_.../output` | 54 | 1/33 |
| Union of all five | — | 20/33 (13 barcodes in NO known BSIP1 dir) |

`canonical_bsip1/run_001` is confirmed (via its own `README.md`) to be an
**older, unrelated "generic snack bars" run** — 53 products, Yohananof-sourced,
predating TASK-365 — not a protein-bars-specific trace at all. Its 2/33
overlap is coincidental barcode reuse across builds, not intended coverage.

**c) The `run_maadanim_001` stray-record risk is real and confirmed, but is a
duplicate-record collision, not a wrong-category swap of different physical
products.** `03_operations/bsip1/run_maadanim_001/output/` (a genuine deli/appetizer
category run, built 2026-06-02, 200 products, `bsip_maadanim_subtype:
protein_dessert`) contains 5 of the 33 protein-bars-corpus barcodes
(`7290019401018`, `7290019401049`, `7290019401544`, `8410076610379`,
`8410076610386`) — because both scrapes independently searched Shufersal for
"protein"-branded items and picked up the same physical SKUs. Checked all 5:
same name, same nutrition-per-100g, same source URL in every case. Ingredient
text core content matches too; the differences are trailing-scrape-noise
capture length (allergen boilerplate / package-size nutrition table glued onto
the end of the string in some copies), not substantive ingredient divergence.
**This is a real risk factor for any FUTURE tool that globs `bsip1_*.json` by
barcode across `03_operations/bsip1/run_*` without corpus-scoping** — a naive
lookup could silently pick the maadanim copy over the canonical one. It did
NOT taint the actual published scores, because the published scores were
never computed from any BSIP1 dir at all (see analysis above — scoring is
corpus-JSON-direct). Routing this stray-record risk to TASK-409 corpus-hygiene
as a shared root cause: **any category's BSIP1 lookup that resolves by
barcode-glob instead of an explicit corpus-scoped file list is exposed to this
same class of collision.**

**d) 13 of the 33 corpus barcodes exist in NO known BSIP1 trace directory
anywhere in the repo.** These products were apparently enriched directly
during the task365 corpus build without ever producing a standalone BSIP1
file. This is consistent with the config's own disclosure
("no standard BSIP1 pipeline run... scored inline from corpus JSON directly")
and is not, by itself, a defect — it is the documented shape of this
category's non-conforming pipeline.

**e) Conform-vs-exception recommendation: DOCUMENT AS EXCEPTION, do not force
conform.** `rescore_all.py --shelf protein_bars` was already confirmed
(TASK-476b run record, `03_operations/page_generator/reports/task476b/run_record_task476b.json`)
to hard-error because `corpus_dirs` has no `bsip1_*.json` files. Forcing this
category onto the standard BSIP1-trace-dir path would require re-deriving 13
missing BSIP1 records with no source scrape guaranteed to reproduce
byte-identically, which risks silent data drift for zero pipeline-conformance
benefit — the existing `protein_bars_reproduce_harness.py` already reproduces
the true corpus through the SAME scoring engine modules
(`score_engine`/`router_v2`/`signal_extractor`/`nova_proxy`) that every other
category uses; only the *loading* step differs (flat corpus JSON vs BSIP1
directory glob). Recommend registering this as an Exception Registry entry
(alongside EXCEPTION-001) rather than a forced conform.

## 3. LIVE score contamination check

**No LIVE score is computed from a stray/wrong-category record.** The
published `protein_combined_frontend_v2.json` scores trace 1:1 to
`rerank_table_rescore.json`, which traces 1:1 (by barcode, exact match, 0
extra/0 missing) to the corpus-JSON's own scraped `ingredients_full` /
`nutrition_per_100g` fields — never to any `bsip1_*.json` file, stray or
otherwise. Barcode-level content comparison between the corpus copy and the
`run_maadanim_001` stray copy (section 2c) shows identical nutrition and
materially identical ingredients for all 5 overlapping barcodes, so even if a
future tool had cross-wired them, no numeric divergence would have resulted
today.

**A separate, unrelated LIVE-DEFECT was found and is flagged here (out of
this task's scope to fix, reporting per the escalation duty):** two products
score below the grade_boundary_policy_v1 "floor" (C starts at 50) —
barcode `7290019766230` (49.8) and `7290019401544` (49.7) — yet
`rerank_table_rescore.json`'s own `tied_group_map` assigns them grade **C**
(grouped with 13 other 50.0-scored products in the same tied bucket) while the
live frontend correctly re-derives grade **D** per the floor policy. The
**live frontend is currently policy-correct** (shows D); the rerank table's
own grade field for these 2 rows is the actual bug (a tie-grouping routine
overrode the floor rule near a boundary). This does not require Nutrition/
Product action to fix (it's a boundary-derivation bug, not a scoring-rule
question) but is flagged for the record since it touches consumer-facing
grades. Recommend a follow-up ticket to correct `rerank_table_rescore.json`'s
grade-assignment routine to always apply the floor after tie-grouping.

## 4. Ingredient-handoff (input_loader fix) re-measurement — CLEAN, STABLE

Reproducer: `03_operations/page_generator/provenance/protein_bars_reproduce_harness.py`
(already built + committed under TASK-476b/TASK-457/P462 — not authored in
this phase, reused as-is). It scores the true 33-product corpus through the
current (post-fix) `input_loader.get_ingredients()` precedence chain via the
canonical engine path (`extract_signals` → `classify_category` → `infer_nova`
→ `assign_evaluation_scope` → `score_product`), using the same flags the
published page used (`BARI_PROTEIN_BAR_V1=on, BARI_FAT_TECH_V1=on,
BARI_GLASSBOX_W4=on`, rest off — confirmed these are the true published flags,
not the config's stale `off` values, per the harness's own inline
documentation and cross-checked against the config's stated flags for
consistency of what changed).

Ran twice, back-to-back, to confirm stability (this replaces the prior
unstable 8/7/8 count from the pre-clean-corpus runs):

- **Run 1: 19/32 exact match, 13/32 move. Grade distribution: B=1, C=23, D=8.**
- **Run 2: 19/32 exact match, 13/32 move. Mismatch set byte-identical to Run 1.**

### Movers (13 total)

**Grade movers: 3 (all DOWN, C→D — no upgrades):**

| Barcode | Name | Published | Re-measured | Direction |
|---|---|---|---|---|
| 7290015130028 | WIN חטיף חלבון קרם חלב | 51.5 / C | 49.7 / D | DOWN |
| 7290019401049 | חטיף פרוטאין שוקולד קרמל | 54 / C | 49.5 / D | DOWN |
| 7290019401018 | חטיף פרוטאין קרם עוגיות | 54 / C | 48.9 / D | DOWN |

**Score-only movers, same grade: 10** (deltas from −6.4 to +7.0; see
`protein_bars_gate_b_result.json` → `mismatches` for the full list; largest:
barcode 7290019766025 "אול אין סופט פיסטוק" 55→62 (+7, stays C); barcode
7290019401544 "חטיף פרוטאין עוגיות טופי" 49.7→43.3 (−6.4, stays D)).

**19/32 unchanged exactly (score AND grade identical).**

### Flagship/top-product check

Top published product (barcode `7290017516295`, "חטיף חלבון אגוזי לוז",
68.6/B — the flagship referenced in the page's own prologue copy) moves
+0.7 to 69.3, **stays B.** The flagship holds. No B-grade product drops to C
or below; no C-grade product rises to B. All 3 grade-movers move C→D, and all
3 already carry a `PROTEIN_BAR_MALTITOL_TIER1` binding cap (maltitol-based
sweetener replacement) per the flat table — consistent with the category's
own published finding that maltitol-based products cluster near the score
floor, not a new/surprising failure mode.

Full reproduction table (score, grade, binding caps, fat, sodium per product):
`03_operations/page_generator/reports/task477/protein_bars_gate_b_flat_table.csv`
(copied verbatim from `_rescore_staging/protein_bars_gate_b_flat_table.csv`,
sha256 `a9d7c1c4044479cf81d47831a31acf66f3880547c2a279e8e8fc3881a4547c52`).

## 5. What ships later, not now

This phase stages the clean corpus confirmation + the stable re-measured
mover set only. Per the task's guard, cleaning/re-measuring did NOT itself
require touching `protein_combined_frontend_v2.json` — the live file is
untouched in this worktree (`git status` clean on that path). The actual
13-product rescore (3 grade-movers) ships only after Nutrition + Product
co-sign the mover set, followed by orchestrator verification, matching the
same two-gate pattern already used for bread/crackers in TASK-476b.
