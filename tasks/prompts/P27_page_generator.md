# P27 / TASK-257 Phase 1 — generate_page.py: the machine (route: C1)

CONTEXT: Repo C:\Bari. TASK-257 builds a GENERATOR: scored shelf → complete
category page JSON, mechanically. The gate suite already exists and is verified:
`03_operations/page_generator/gates/run_gates.py` (7 gates; it correctly FAILS the
hand-built `bari-web/src/data/comparisons/yogurts_frontend_v4.json` — that file is
the permanent known-bad). The contract inventory exists:
`03_operations/page_generator/contract/` (P25). You build the generator that makes
hand-assembled pages obsolete. Read `tasks/TASK-257.md` first.

NON-NEGOTIABLE LAWS: no Open Food Facts anywhere (TASK-238 — if a corpus record
has panel_source=open_food_facts, the product is EXCLUDED with evidence, never
used); never modify live page JSONs, corpora, or traces; no engine/score changes;
no network; Python 3 stdlib only.

## DELIVERABLE 0 — Schema v2 (fixes known P25 drift)
Create `03_operations/page_generator/contract/page_output_schema_v2.json`,
reconciled against the ACTUAL live canonical JSONs (granola + snacks are
authoritative). Known drift to fix: `score` is float in reality (schema said
integer); `comparisonContext` exists in live format but is missing from schema;
extension fields (`_subpool`, `_isChildrens`, `_wholeGrainClaim`,
`_internal_cluster`) are real and must be documented as CATEGORY-CONFIG-DRIVEN
optional fields. Every field in the live granola/snacks product objects must be
either in the schema or listed in a `x-deviations` note. v1 stays untouched.

## DELIVERABLE 1 — Category config format + 3 configs
Directory: `03_operations/page_generator/configs/`. Format (JSON):
```json
{
  "category": "<slug>",
  "corpus_dirs": ["<BSIP1 output dirs, ordered by priority>"],
  "run_products_dir": "<BSIP2 run products dir>",
  "baseline_json": "<current live frontend JSON path or null>",
  "retailer_scope": ["shufersal"],
  "subpool_filter": {"field": "<corpus field>", "value": "<v>"} ,
  "dedup": {"rule": "one_card_per_barcode", "keep": "highest_priority_corpus"},
  "exclusions": [{"barcode": "<bc>", "reason": "<evidence-backed reason>"}],
  "extension_fields": ["_subpool", "_isChildrens"],
  "boundary_policy": "01_framework/governance/grade_boundary_policy_v1.json"
}
```
(`subpool_filter`/`extension_fields` may be null/empty. If boundary policy file is
absent at run time, default = floor.)
Create configs for: **yogurts** (corpus `03_operations/bsip1/run_yogurt_006/output`,
run `02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2/products/products`,
baseline `bari-web/src/data/comparisons/yogurts_frontend_v3.json`, exclusion:
7290000408316 OFF-contaminated per TASK-238), **granola** and **snacks** (discover
their data files via the import lines in
`bari-web/src/lib/comparisons/registry/categories/{granola,snacks}.ts`, and their
corpora/runs under `03_operations/bsip1/` + `02_products/`; cite what you used).
KNOWN ISSUE to handle in the granola config: granola is a SUB-POOL of a shared
cereals corpus — the split must be expressed as `subpool_filter` and the generator
must document it in `_meta` (gate 3 currently fails the live granola page for
exactly this omission).

## DELIVERABLE 2 — the generator
`03_operations/page_generator/generate_page.py`
Usage: `python generate_page.py --config <category_config.json> --out <output.json>`
Behavior, per product in the run (every trace dir is a candidate — the run is the
universe; missing from output = documented exclusion, NOTHING silent):
1. Look up barcode in corpus_dirs (priority order). No corpus record → exclusion
   entry `"no_corpus_record"`. panel_source=open_food_facts → exclusion `"off_banned"`.
2. Score = trace `final_score_estimate`. Grade = boundary policy over the RAW
   score (floor: 34.7 → E, never D). Score displayed per live convention.
3. Carry mechanically from BSIP1: Hebrew `name` (must contain Hebrew; else
   exclusion `"no_hebrew_name"` — never an English OFF name), `imageUrl`,
   `expansion.nutrition` (normalized per-100g mapping), `expansion.ingredients`
   (null if absent — page shows its honest missing-data state), barcode, retailer.
4. Confidence fields: mechanical mapping from trace (confidence_band + missing
   fields → the existing label/tooltip/sub_reason conventions; copy the mapping
   used in live granola/snacks, cite where you took it from).
5. ALL copy fields (`insightLine`, `rowVerdict` if category uses it,
   `comparisonContext`, positiveSignals/limitingFactors) = `"PENDING_COPY"` /
   empty arrays. The copy engine is Phase 2 — you author NOTHING.
6. Extension fields per config. Dedup per config.
7. `_meta`: product_count, scored_count (run universe), full exclusions list with
   reasons (incl. subpool split documentation), retailer breakdown, source paths,
   schema_version "v2", generator_version, generated_at, config sha256.
Deterministic + idempotent: same inputs → byte-identical output (sort keys, sort
products by score desc, fixed timestamp source documented).

## DELIVERABLE 3 — self-gating (mandatory)
generate_page.py ENDS every run by invoking run_gates.py on its own output
(`--corpus`, `--run`, `--schema` v2, `--baseline` from config when present) and
prints the gate summary; exits non-zero if any gate FAILs (G6 copy gates will have
nothing to scan — strings are PENDING; G7 parity never fails by design).

## ACCEPTANCE (run all three, report verbatim summaries)
A. **Yogurts**: expect ≈80 products (87 minus documented exclusions), images
   100/100 vs BSIP1, gates G1–G5 PASS, G3 exclusions fully enumerated.
B. **Granola regen vs live**: generate from sources, then produce
   `diff_granola_v1.md` — EVERY difference vs the live JSON classified as one of:
   `KEEP` (live hand-edit worth preserving → note for config/copy phase),
   `GAP` (generator missing something → fix it before returning),
   `LIVE_DEBT` (live page is wrong — e.g. 7290014471436 shows D, trace says E;
   the generator's E is CORRECT, do not "fix" to match live). Copy-field diffs
   are expected (PENDING) — classify as `COPY_PHASE`, don't enumerate per-product.
C. **Snacks regen vs live**: same, `diff_snacks_v1.md`.
Do NOT modify the live JSONs to make diffs smaller. The diff reports are the
deliverable — surfacing undocumented hand-edits is a goal, not a failure.

RETURN BLOCK: file paths; the 3 acceptance summaries verbatim (gate results +
diff classification counts); the granola/snacks source paths you discovered;
any KEEP/GAP calls you were unsure about. End with the machine-readable JSON
return contract (artifacts+sha256, counts with denominators — including
images N/M per category — commands_run with exit codes, not_done, self_check).
Propose RETURNED.

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and tick the P27 line.
