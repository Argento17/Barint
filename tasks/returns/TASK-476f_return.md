---
task: TASK-476f
status_proposed: RETURNED
agent: Data Agent
worktree: C:\bari_wt_t476
branch: golive/task476-rescore
commit: c35986a0
---

# TASK-476f — Surgical numbers-patch rebuild (bread + crackers rescore)

## What was wrong with the artifact this replaces

The worktree's `bread_frontend_v4.json` / `crackers_frontend_v1.json` were full
regenerations that wiped curated overhaul content — confirmed before starting:

- crackers non-mover `7290013740823`: `expansion.positiveSignals` and
  `expansion.limitingFactors` both wiped to `[]` (origin has 3 signals + 1
  limiting factor).
- bread flagship `7290016245325`: `confidenceLabel`/`confidence_tooltip_he`
  downgraded from "ניתוח חלקי" (partial analysis) to "נתונים בבדיקה" (data
  under review); additive tier text rewritten from neutral/functional framing
  to a "contested" cardiovascular-risk framing not present in the curated
  original.
- crackers mover `7290018790328`: `expansion.comparisonContext` replaced with
  a generic "הציון ממוקם ביחס ל-20 מוצרים בהשוואה" placeholder, and
  `limitingFactors` (5 authored bullets) wiped to `[]`.

None of this shipped. It stays in the worktree's prior commits, untouched.

## What was built instead

Base = `origin/master`'s two curated files (fetched via `git show`, byte-identical
to what's live). Per product, only these fields were overwritten:

- `score`, `grade` — from the rescore's authoritative source (see below)
- `rank` — recomputed 1..N by new score, descending, within each category
- `categoryTotal` (crackers only, where the field exists) — recomputed to N
- `bariInterpretation[].score` + `[].strength` (crackers only — bread's schema
  has no such field) — pulled from each product's `dimension_scores` in the
  per-product `_rescore_staging/{cat}/products/bsip1_*/bsip2_trace.json`.
  `interpretation` / `label` / `key` text left untouched (author-owned template
  strings, verified byte-identical to origin for every dimension/product).
- For the 5 grade-movers only — bread `2079033`/`2079927`/`2079996` (A→B),
  `4685027` (B→C); crackers `7290018790328` (C→D) — `insightLine` and
  `rowVerdict` were replaced with the content-authored strings already present
  in the prior (degraded) worktree JSONs. Not re-authored by this agent.

Everything else — every `expansion.*` sub-field, `_meta`, `d4_additives`,
`confidence*`, `_website_cluster`, `bestUseCases`, `consumerTakeaway`,
`consumerExplanation`, images, names, retailer, `_hash_no_rank` — copied
verbatim from origin via `copy.deepcopy`, never touched by the patch logic.

## Score source correction (found during verification, not in the original brief)

The brief named `rescore_all57_result.json` as the score source. Cross-checking
all 42 bread+crackers rows in that summary file against each product's own
`bsip2_trace.json` (the actual BSIP2 engine output — the file `run_gates.py`'s
G5 gate checks scores against) found **one disagreement**:

- crackers `8434165658523` ("קרקר קרם קרקר"): summary file says
  `recomputed_score=69.1/B`; its own trace says `final_score_estimate=68.1/B`,
  which also matches `_rescore_staging/crackers/crackers_rescored.json` (68.1)
  and the currently-live origin score (68.1) exactly — i.e. per the trace this
  product did not move at all.

I treated the trace as authoritative (it's the deeper engine artifact and what
the gate suite verifies against) and used 68.1 (delta 0.0) for this product,
not the summary file's 69.1. Grade is B either way so this has zero go-live
consequence, but it is a real data inconsistency between two files both
labeled as "the rescore result" — flagging it rather than silently picking one.

## Guardrail contradicted by the data — flagging, not overriding

The brief states "verify... all score moves downward" as a co-signed outcome.
The rescore data does not support this for the full bread+crackers set:

- bread `497044` ("לחם ברמן אקטיב"): 83.0/A → **83.7/A** (delta **+0.7**)
- bread `7290016967074` ("לחם אנג'ל חיטה מלאה"): 66.0/B → **69.0/B** (delta **+3.0**)

Both confirmed by **two independent artifacts** (the product's own
`bsip2_trace.json` and the staged `bread_rescored.json`) — not a summary-file
glitch like the case above. Both are non-movers (grade unaffected: A→A, B→B),
and both traces show plausible mechanics (`whole_food_integrity`,
`nutrient_density`, `additive_quality` dimension recomputation under the new
engine logic, no caps/floors distorting anything). This looks like a genuine
re-flow result, consistent with the standing re-flow policy ("nothing is
frozen... verify movement," not "verify only downward movement") — but since
the task brief explicitly asserted all-downward as a guardrail to re-check, I
did not suppress or "fix" these two numbers to make that guardrail pass. They
are included in the shipped patch as computed. If "all downward" was meant as
a hard invariant rather than an expectation to verify, this needs Nutrition
Agent / Product Agent sign-off before this branch is treated as go-live-ready
— it is currently only proposed RETURNED, not deployed.

## Field-level diff summary (full corpus, not spot-checks)

Ran an exhaustive per-field diff, product-by-product, both categories, origin
vs patched (`_task476_scratch/full_diff.py`). Diff logic: any field change is
"unexpected" unless it is `score`/`grade`/`rank`/`categoryTotal` (any product),
`bariInterpretation[].score`/`.strength` (any product, crackers only), or
`insightLine`/`rowVerdict` (5 movers only).

```
========== bread ==========
_meta identical: True
bread: total unexpected/disallowed diffs = 0

========== crackers ==========
_meta identical: True
crackers: total unexpected/disallowed diffs = 0

GRAND TOTAL unexpected diffs: 0
```

Spot-verified two representative cases by hand before the automated pass:
- crackers non-mover `7290013740823`: `positiveSignals`, `limitingFactors`,
  `comparisonContext`, `confidenceLabel` all byte-identical to origin
  (populated arrays, not `[]` — confirmed the degraded worktree version had
  wiped them and the patch does not).
- crackers mover `7290018790328`: `comparisonContext` and `limitingFactors`
  (5 bullets) restored to origin's authored text, not the generic placeholder.

## PENDING scan

```
grep -c "PENDING" bread_frontend_v4.json      -> 0
grep -c "PENDING" crackers_frontend_v1.json   -> 0
```

Also confirmed via `run_gates.py` G2 v3-coverage lines for crackers:
`v3 consumerTakeaway: 19/19 authored (0 PENDING)`,
`v3 consumerExplanation.whyRated: 19/19 authored (0 PENDING)`,
`v3 bariInterpretation.interpretation: 190/190 authored (0 PENDING)`,
`v3 bestUseCases: 19/19 authored (0 PENDING)`.

## Co-signed outcomes recheck

| Outcome | Expected | Result |
|---|---|---|
| Flagship bread `7290016245325` | 90.8/S | **90.8/S** — confirmed |
| bread `2079033` לחם דגנים לייט | A→B | **83.1/A → 78.6/B** — confirmed |
| bread `2079927` לחם דגנים מלא | A→B | **83.0/A → 78.6/B** — confirmed |
| bread `2079996` לחם אחיד פרוס קל | A→B | **82.0/A → 77.6/B** — confirmed |
| bread `4685027` לחם מחמצת וחיטה מלאה קל | B→C | **68.0/B → 64.0/C** — confirmed |
| crackers `7290018790328` קרקר מרובע מלוח | C→D | **52.9/C → 48.1/D** — confirmed |
| All score moves downward | expected | **NOT fully true** — see flag above (2 bread non-movers moved up: `497044` +0.7, `7290016967074` +3.0; both trace-confirmed, grade unaffected) |

6 of 7 co-signed outcomes hold exactly as stated; the 7th ("all downward") is
contradicted by trace-confirmed data on 2 of 42 products and is flagged above
rather than silently forced.

## Product counts

- bread: **23** products, barcode set identical to origin/master (verified via
  set equality, not just count).
- crackers: **19** products, barcode set identical to origin/master; the
  `7290112968807` discard (insufficient_data / nutrition-corruption, per
  TASK-433 FIX2b missing-data-discard rule) stays excluded, `_meta` exclusion
  note preserved verbatim from origin.

## Gate verification (run_gates.py, G1-G8)

**crackers_frontend_v1.json** (`--run _rescore_staging/crackers/products
--baseline` origin): **Overall PASS**. G1 schema pass, G2 coverage all fields
100% except sugar/fiber (pre-existing sparse-source fields, unchanged from
origin), G3 scope pass (19 displayed, 20 traced, 1 declared exclusion
matching), G4 OFF pass, G5 grade-integrity pass (every JSON score matches its
trace within tolerance — this is what caught the `8434165658523` summary-file
discrepancy), G6 copy-safety pass, G7 parity pass (1 grade change, matches the
expected mover), G8 data-sanity pass.

**bread_frontend_v4.json**: **Overall PASS** when given an isolated,
uncontaminated trace directory. First run against
`_rescore_staging/bread/products` directly showed G3/G5 warnings/fails, but
that directory contains 31 trace dirs — 8 of them are crackers barcodes (and 2
unrelated ones) sharing the same folder, a staging-directory artifact, not a
defect in the shipped JSON. Rebuilt an isolated copy containing only bread's
own 23 trace dirs (filtered by `rescore_all57_result.json`'s per-barcode
`category` field) and reran: G1 schema pass, G2 coverage pass, **G3 scope
pass** (23 displayed, 23 traced, 0 exclusions, "All scored barcodes are
displayed or explained"), G4 OFF pass, **G5 grade-integrity pass** (all 23
scores match trace exactly), G6 copy-safety pass, G7 parity pass (4 grade
changes, exactly the 4 expected movers), G8 data-sanity pass.

## sha256 (final committed files)

```
fe54b7440a0cda1956d7aed39ab16fccee456ee7d92eff87b9562f301920b300  bread_frontend_v4.json
660114ce6477126378e7ef3b2fb85ad63ced791dbe920a082e8dfd38004dcb6b  crackers_frontend_v1.json
```

## Not done / handoff

- No push, no PR, no merge — commit sits on `golive/task476-rescore` in
  `C:\bari_wt_t476` only, per instruction.
- The engine fix and run-records from earlier TASK-476 stages were left as-is,
  not touched.
- The two upward-delta bread non-movers (`497044`, `7290016967074`) need a
  decision from Nutrition Agent / Product Agent: ship as computed (re-flow
  policy — nothing frozen, verify movement in either direction) or treat "all
  downward" as a hard invariant that should gate this branch. I did not decide
  this unilaterally since it's a co-signed outcome, not an implementation
  detail.
- Gate-run scratch reports (`bread_frontend_v4_gates_report.md`,
  `crackers_frontend_v1_gates_report.md` in
  `bari-web/src/data/comparisons/`) were regenerated by my `run_gates.py`
  calls and are sitting as unstaged working-tree changes (pre-existing tracked
  files) — not staged or committed, left for the orchestrator/next agent to
  decide whether to keep or discard.

```json
{
  "task": "TASK-476f",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\bread_frontend_v4.json",
      "sha256": "fe54b7440a0cda1956d7aed39ab16fccee456ee7d92eff87b9562f301920b300"
    },
    {
      "path": "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\crackers_frontend_v1.json",
      "sha256": "660114ce6477126378e7ef3b2fb85ad63ced791dbe920a082e8dfd38004dcb6b"
    },
    {
      "path": "C:\\bari_wt_t476\\_task476_scratch\\build_patch.py",
      "sha256": null
    },
    {
      "path": "C:\\bari_wt_t476\\_task476_scratch\\full_diff.py",
      "sha256": null
    }
  ],
  "counts": {
    "bread_products_total": 23,
    "bread_products_matching_origin_barcode_set": 23,
    "crackers_products_total": 19,
    "crackers_products_matching_origin_barcode_set": 19,
    "crackers_declared_exclusions": 1,
    "pending_string_occurrences": 0,
    "unexpected_field_diffs_vs_origin_bread": 0,
    "unexpected_field_diffs_vs_origin_crackers": 0,
    "grade_movers_bread": 4,
    "grade_movers_crackers": 1,
    "grade_movers_confirmed_at_expected_grade": 5,
    "grade_movers_expected": 5,
    "upward_score_deltas_bread": 2,
    "upward_score_deltas_crackers": 0,
    "score_source_disagreements_summary_vs_trace": 1,
    "products_cross_checked_summary_vs_trace": 42
  },
  "commands_run": [
    {"cmd": "git show origin/master:bari-web/src/data/comparisons/bread_frontend_v4.json > _task476_scratch/origin_bread_frontend_v4.json", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/data/comparisons/crackers_frontend_v1.json > _task476_scratch/origin_crackers_frontend_v1.json", "exit_code": 0},
    {"cmd": "python3 _task476_scratch/build_patch.py", "exit_code": 0},
    {"cmd": "python3 _task476_scratch/crosscheck_traces.py", "exit_code": 0},
    {"cmd": "python3 _task476_scratch/full_diff.py", "exit_code": 0},
    {"cmd": "python3 03_operations/page_generator/gates/run_gates.py bari-web/src/data/comparisons/crackers_frontend_v1.json --schema 03_operations/page_generator/contract/page_output_schema_v1.json --run _rescore_staging/crackers/products --baseline _task476_scratch/origin_crackers_frontend_v1.json", "exit_code": 0},
    {"cmd": "python3 03_operations/page_generator/gates/run_gates.py bari-web/src/data/comparisons/bread_frontend_v4.json --schema 03_operations/page_generator/contract/page_output_schema_v1.json --run _task476_scratch/bread_traces_only --baseline _task476_scratch/origin_bread_frontend_v4.json", "exit_code": 0},
    {"cmd": "git add bari-web/src/data/comparisons/bread_frontend_v4.json bari-web/src/data/comparisons/crackers_frontend_v1.json && git commit", "exit_code": 0}
  ],
  "not_done": [
    "No push/PR/merge performed (instructed not to)",
    "Upward-delta guardrail conflict (2 bread non-movers) not resolved -- needs Nutrition/Product sign-off",
    "Gate-report scratch files left unstaged in working tree, not cleaned up (rm permission denied mid-session)"
  ],
  "self_check": {
    "acceptance_test": "Field-level diff proves the ONLY differences vs origin/master are score/grade/rank/categoryTotal (all products), bariInterpretation[].score+strength (crackers), and insightLine/rowVerdict (5 movers only); 0 unexpected diffs found across full bread+crackers corpus (42 products). PENDING=0. Product counts 23/19 match origin barcode sets exactly. 6/7 co-signed outcomes confirmed exactly; 7th ('all downward') contradicted by trace-verified data on 2 products and flagged, not overridden.",
    "result": "PASS with one flagged spec conflict (all-downward guardrail) requiring Nutrition/Product Agent decision before go-live"
  }
}
```
