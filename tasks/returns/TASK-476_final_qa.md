# TASK-476 Final QA — Adversarial QA Gate (Track V + Track C)

Reviewer: Adversarial QA Agent (independent — did not consult the builder's summary; read JSON/traces/commits directly)
Scope reviewed: worktree `C:\bari_wt_t476`, branch `golive/task476-rescore` (5 commits ahead of/behind `origin/master`), HEAD `c35986a0`
Files under review per brief: `bari-web/src/data/comparisons/bread_frontend_v4.json` (23 products), `bari-web/src/data/comparisons/crackers_frontend_v1.json` (19 products)

## VERDICT: GO

All three named PASS/FAIL gates are PASS. One HIGH finding (a falsifiable numeric overstatement in the crackers mover's copy) and two MEDIUM findings (tooling hygiene, not output defects) are raised below; none are CRITICAL and none touch score/grade/rank correctness or curated-content integrity. Recommend fixing the HIGH before publish since it's a two-line text edit, but it does not block the underlying rescore from going live on data-integrity grounds.

---

## Summary answers to the three mandatory questions

**(a) Surgical-patch integrity: PASS.**
Full field-level diff of every product in both files (before = `git show origin/master:<path>`, after = worktree file) shows the patch touched *only*: `score`, `grade`, `rank`, `bariInterpretation[].score`, `bariInterpretation[].strength`, and — on exactly the 5 named movers — `insightLine`/`rowVerdict`. Zero non-mover products had any curated-prose field (`expansion.positiveSignals`, `expansion.limitingFactors`, `expansion.comparisonContext`, `expansion.confidenceLabel`, `expansion.consumerExplanation`, `expansion.servingNote`, `insightLine`, `rowVerdict`) change. Zero products had `confidence`/`confidence_level`/`confidence_label_he`/`confidence_sub_reason` change anywhere. Zero `d4_additives` or `_website_cluster` changes anywhere. `bariInterpretation[]` sub-fields other than `score`/`strength` (i.e. `label`, `key`, `interpretation`) were checked across all 10 dimensions × 42 products = 420 entries: 0 unexpected diffs.

**(b) The 5 movers' copy: PASS on phrasing, CONDITIONAL on honesty (1 HIGH).**
No em-dash and no "X, not Y"/antithesis pattern in any of the 5 re-authored `insightLine`/`rowVerdict` strings (checked the actual re-authored fields, not the surrounding unchanged expansion fields, which do contain pre-existing em-dashes out of this patch's scope — see MEDIUM-2). No grade-letter used as a crutch (the two stray Latin "C" characters found are both "ויטמין C" / Vitamin C ingredient references, not grade mentions). Voice matches the surrounding non-mover copy (colon-led opening clause, specific gram/percent figures, comparative shelf-anchoring, no apology). All four bread movers' claims were checked word-for-word against their raw ingredient strings and nutrition blocks and are accurate. The crackers mover's claim of sodium "more than double" every other product in the comparison is factually false against the actual #2 product — see RT-1 (HIGH).

**(c) Score-propagation: PASS.**
All 23 bread products (100%) cross-checked against their individual `bsip2_trace.json` files (left in the worktree's scratch directory by the builder, read independently, not taken on faith): `final_score_estimate`/`grade_estimate` match the shipped JSON `score`/`grade` exactly on every product, zero mismatches. The crackers mover (7290018790328) independently verified against the rescore engine's `recomputed_score`/`recomputed_grade` output: matches (48.1/D). Flagship bread product 7290016245325 confirmed at 90.8/S/rank-1, trace-matched. `run_gates.py` G1–G8 executed directly by this reviewer (not taken from the builder's report) on both files with `--baseline` set to the actual `origin/master` copies: **Overall: PASS, exit 0** for both bread and crackers. G7 parity confirms exactly 4 bread grade-movers (A→B ×3, B→C ×1) and exactly 1 crackers grade-mover (C→D), matching the brief. Rank integrity: ranks are a contiguous 1..23 (bread) / 1..19 (crackers) permutation, monotonically non-increasing with score — no ties, no gaps, no inversions.

---

## Track V — deterministic verification detail

| Check | Result | Evidence |
|---|---|---|
| Barcode-set identity vs origin | PASS | bread: 23/23 identical barcode set; crackers: 19/19 identical; crackers discard 7290112968807 confirmed absent from products and present in `_meta.exclusions` with reason `insufficient_data: unrecoverable per-serving/per-100g nutrition corruption, discard-rule` |
| `_meta.categoryCaveat` on crackers | PASS | present, non-empty (`_meta.categoryCaveat`, ~200+ chars, category-specific calorie-density framing) |
| PENDING scan (any case) | PASS, 0 hits | Only match in either file is `_meta.gate_e_note` = "...staged->served; render-verify pending" — pre-existing in origin/master unchanged, a build-pipeline note field, not a consumer-facing placeholder. `run_gates.py`'s own G2 also independently confirms 0 PENDING across `consumerTakeaway`/`consumerExplanation.whyRated`/`bariInterpretation.interpretation`/`bestUseCases` on crackers (19/19, 190/190, 19/19 all authored) |
| OFF-ban | PASS, 0 hits | `off_used: false` in crackers `_meta` (pre-existing, unchanged). All literal `"off"` string matches in both files are `flag_vector` toggle states (e.g. `"BARI_REDLABEL_V1": "off"`) — disabled-flag markers, not Open Food Facts data. `run_gates.py` G4 OFF: PASS on both files ("No OFF markers detected") |
| Rank monotonicity | PASS | bread ranks == [1..23], crackers ranks == [1..19], score non-increasing with rank, 0 inversions, 0 ties, 0 gaps |
| Leakage/jargon in consumer strings | PASS | Scanned all `insightLine`/`rowVerdict`/`expansion.*`/`_meta.categoryCaveat` for BSIP/NOVA/pillar/structural_class/matrix_integrity/routing/cap/dimension: 0 hits. The only "BSIP" string hits anywhere in either file are in the internal `products[].id` field (e.g. `"bsip1_bread_2079033"`) and `_meta` build-pipeline paths — confirmed by grep of `bari-web/src/app` that `.id` is never rendered as visible text (only used as a React `key` prop elsewhere in the codebase, on an unrelated category-box list) |
| Score propagation (trace → JSON) | PASS | 23/23 bread products verified against individual `bsip2_trace.json` (`final_score_estimate`/`grade_estimate`), 0 mismatches. Crackers mover independently verified against `recomputed_score`/`recomputed_grade`. Flagship (7290016245325) verified at both nutrition-signal level (energy/fiber/protein/sodium match trace `L1_observed_signals` exactly) and score level |
| Confidence field integrity | PASS | 0 products had `confidence`/`confidence_level`/`confidence_label_he`/`confidence_sub_reason`/`confidence_tooltip_he` changed anywhere in either file |
| Null nutrition disclosure unchanged | PASS | bread: 1/23 null fiber, 22/23 null sugar — identical count before and after the patch (pre-existing, not a new gap; correctly shown as null rather than fabricated) |
| Gate suite (`run_gates.py`) | PASS | Bread: exit 0, "Overall: PASS" (G1 schema PASS, G4 OFF PASS, G6 copy-safety PASS, G7 parity PASS against origin baseline, G8 data-sanity PASS; G3/G5 show WARN only because no `--run`/corpus directory was supplied to this invocation — see MEDIUM-1). Crackers: identical, exit 0, "Overall: PASS" |
| Build/route | NOT RUN this session | Out of the JSON-only surgical-patch scope named in the brief; no frontend/component files changed on this branch (`_catalog-client.tsx` diff is net-zero — touched then reverted per commit `d3019f4e`) |

## Track C — adversarial challenge detail

### Findings by severity

**CRITICAL — none.**

**HIGH**

**RT-1: Crackers mover's "more than double" sodium claim is mathematically false against the actual runner-up product, in both re-authored strings.**
- Barcode: `7290018790328` (קרקר מרובע מלוח), crackers, rank 18, grade D, score 48.1
- `insightLine`: "הנתרן כאן הוא 1200 מיליגרם ל-100 גרם, **יותר מכפול** מכל קרקר אחר בהשוואה..." ("more than double every other cracker in the comparison")
- `rowVerdict`: "1200 מיליגרם נתרן ל-100 גרם, **יותר מפי שניים** מהקרקר המלוח הבא בתור." ("more than double the next saltiest cracker")
- Evidence: full sodium ranking pulled from `expansion.nutrition.sodium` across all 19 crackers products. #1 = this product at 1200mg. #2 = barcode `7290011489595` (קרקר טופז שומשום) at **754mg**. `1200 / 754 = 1.59×` — not "more than double." The claim is only true against the #3 product and below (all ≤ 578mg). 754×2 = 1508, which exceeds 1200, so the literal "double the next-saltiest" claim fails against its own stated referent ("the next saltiest cracker").
- Implication: this is a specific, falsifiable number a skeptical reader (competitor, journalist, or the product's own manufacturer) can check with a calculator in ten seconds and call out publicly. The directional claim ("highest sodium in the comparison, by a wide margin") is true and well-supported; the specific "2x" multiplier is not. This appears in **two** of the five re-authored strings for this product (insightLine and rowVerdict both make the same false-precision claim independently), so it is not a one-off typo — the same wrong comparison was authored twice.
- Routes to: `content-agent` (copy fix — e.g. "quadruple the median" or simply "the highest by a wide margin" would both be true and equally strong).

**MEDIUM**

**RT-2 / process note — the builder's rescore-summary tool (`rescore_all57_result.json`) has a demonstrated non-zero error rate against ground truth; only trace-file cross-checking caught it.**
- Evidence: independently confirmed 3 discrepancies between `rescore_all57_result.json`'s `live_score` (its own snapshot of the "before" state) and the actual origin/master JSON: barcode `7290011489595` (55.0 actual vs 54.8 tool-recorded), barcode `7290018790328` (52.9 actual vs 52.5 tool-recorded), and barcode `8434165658523` where the tool's `recomputed_score`/`recomputed_grade` (69.1/B, a claimed +1.0 move) disagreed with that product's own `bsip2_trace.json` (68.1/B, no move) — the trace was correct (matches the live, unchanged JSON) and the summary tool's row was wrong. The builder's patch script (`_task476_scratch/build_patch.py`) documents choosing the trace over the summary for this reason, and I independently re-derived the same conclusion from the raw files, so the *shipped output* is correct. But this means the summary artifact (`rescore_all57_result.json`) cannot be trusted standalone in future runs without a per-product trace cross-check — it silently drifted on at least 3 of 42 checked bread+crackers rows.
- Implication: no defect in this deploy, but a process risk for the next scoring-engine change if someone reads only the summary file.
- Routes to: `data-agent` (harden `rescore_all.py`/its summary emitter, or mandate the trace-first precedence build_patch.py used as a standing rule, not a one-off judgment call).

**RT-3 / scope note — the reviewed branch carries more than the two named JSON files, including a live scoring-engine source change.**
- Evidence: `git diff --name-only origin/master...HEAD` on this branch shows 10 files touched across 5 commits, not 2: `03_operations/bsip2/proto_v0/src/input_loader.py`, `03_operations/bsip2/proto_v0/src/router_v2.py`, and `03_operations/page_generator/gates/run_gates.py` are also modified, in addition to the two data files and their gate reports. `input_loader.py`/`router_v2.py` are the actual co-signed ingredient-handoff bug fix (the root cause this whole rescore exists to address) — `get_ingredients()` gained a 3-tier fidelity-preference fallback chain (`ingredients_list` → `ingredient_order` → a new bracket-depth-aware comma splitter `_split_top_level_commas()`), and `router_v2.py`'s `classify_category()` now routes its ingredient count through that same function instead of a duplicate, lower-fidelity inline fallback. I independently unit-tested `_split_top_level_commas()` against the flagship product's real ingredient string and confirmed it correctly keeps a parenthesised sub-list (e.g. "קמחים 36% (פשתן, שומשום, אפונה, סויה, שקדים)") as one top-level ingredient rather than fragmenting it — this matches the trace's `ingredient_count=13`. `run_gates.py`'s change is a narrow defensive type-guard (handles `consumerExplanation` arriving as a literal `PENDING_COPY` string instead of a dict without crashing) and does not weaken any check. `_catalog-client.tsx` was touched then reverted (commit `d3019f4e`, "out of rescore scope") — net zero diff, confirmed.
- Implication: this is very likely the correct, intended state (the brief's own framing — "an ingredient-handoff bug meant these products were scored WITHOUT their ingredients" — describes exactly this fix), and nothing here looks unsafe on inspection. But my delegation brief scoped me to compare "ONLY" the two JSON files, and undersold that the branch also ships an engine change affecting every future category rescore, not just bread/crackers. I did not evaluate `input_loader.py`/`router_v2.py` against the full BSIP2 scoring-governance checklist (evidence registry, activation scope, rollback plan) — that is Nutrition/Data's D8 lane, not mine, and the brief did not ask for it.
- Routes to: `product-agent` / orchestrator (confirm the engine-fix commits are the co-signed, intended scope for this PR and not accidentally bundled; if intended, no action needed beyond noting it was reviewed only at the "does the output look right" level, not a full scoring-governance audit).

### Product-by-product assessment of the 5 movers

| Barcode | Product | Score | Grade (before→after) | RT Assessment | Confidence | Critical Notes |
|---|---|---|---|---|---|---|
| 2079033 | לחם דגנים לייט | 83.1→78.6 | A→B | Justified — every number in the re-authored copy (80% whole wheat+rye, 14.2g fiber, 304mg sodium, 2 preservatives + emulsifier + acidity regulator) verified against raw ingredients/nutrition | sufficient (partial-analysis label, pre-existing) | none |
| 2079927 | לחם דגנים מלא | 83.0→78.6 | A→B | Justified — 83% whole wheat, 13.8g protein, 400mg sodium, 2 preservatives + 2 emulsifiers all verified | sufficient | none |
| 2079996 | לחם אחיד פרוס קל | 82.0→77.6 | A→B | Justified — 10.4g fiber, dark/refined wheat flour as first ingredient, 2 preservatives + emulsifier + acidity regulator all verified | sufficient | none |
| 4685027 | לחם מחמצת וחיטה מלאה קל | 68.0→64.0 | B→C | Justified — 100% whole flour + real rye sourdough claims verified true; correctly identifies the 4-item processing-aid tail (emulsifier, preservative, xanthan stabilizer, antioxidant/vitamin C) as the actual driver, doesn't hand-wave the drop | sufficient | none |
| 7290018790328 | קרקר מרובע מלוח | 52.9→48.1 | C→D | Plausible-but-overstated — sodium-highest claim directionally true and well-supported; the specific "more than double" multiplier is false (see RT-1) | data-sufficiency labeled "נתונים בבדיקה" (data under review) in this product's own `confidenceLabel`, consistent with its lower-confidence D-grade | RT-1 (HIGH) |

## Findings by severity (routing table)

| ID | Severity | Finding | Routes to |
|---|---|---|---|
| RT-1 | HIGH | "More than double" sodium claim false against actual #2 product (1.59x, not 2x+), appears in both insightLine and rowVerdict for crackers barcode 7290018790328 | content-agent |
| RT-2 | MEDIUM | Rescore-summary tool (`rescore_all57_result.json`) diverged from ground truth on 3/42 checked rows; only trace-first cross-check caught it | data-agent |
| RT-3 | MEDIUM | Branch scope is wider than the brief described (engine-fix source files + gate-suite defensive patch also included); reviewed at output-correctness level only, not full BSIP2 scoring-governance level | product-agent / orchestrator |

## Not checked (named, not invented)

- Mobile-geometry / rendered-DOM / build-route checklist: not run this session — brief scoped this to a JSON-only surgical-patch review; no frontend component files changed on this branch (confirmed by `git diff --name-only`)
- Full BSIP2 scoring-governance checklist (evidence registry entries, rollback plan, activation-scope sign-off) on `input_loader.py`/`router_v2.py`: out of this agent's lane (Nutrition/Data D8), flagged as RT-3 for the orchestrator to confirm is covered elsewhere, not evaluated here
- Bread `_meta.categoryCaveat` absence: pre-existing in origin/master (confirmed identical before/after), not a regression from this patch, so not raised as a blocking finding here — noted only because the standing rule says every comparison page needs one

---

```json
{
  "task": "TASK-476",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\bread_frontend_v4.json", "sha256": "fe54b7440a0cda1956d7aed39ab16fccee456ee7d92eff87b9562f301920b300"},
    {"path": "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\crackers_frontend_v1.json", "sha256": "660114ce6477126378e7ef3b2fb85ad63ced791dbe920a082e8dfd38004dcb6b"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-476_final_qa.md", "sha256": "computed post-write; this JSON block's own hash is necessarily excluded from itself — re-hash the file after this edit to get the final value"}
  ],
  "counts": {
    "bread_products_total": 23,
    "bread_products_byte_identical_to_origin": 2,
    "bread_products_with_any_diff": 21,
    "bread_grade_movers": 4,
    "bread_products_trace_verified": 23,
    "bread_trace_mismatches": 0,
    "crackers_products_total": 19,
    "crackers_products_byte_identical_to_origin": 4,
    "crackers_products_with_any_diff": 15,
    "crackers_grade_movers": 1,
    "crackers_exclusions": 1,
    "bariInterpretation_entries_checked_for_non_score_field_drift": 420,
    "bariInterpretation_unexpected_diffs": 0,
    "pending_placeholder_hits_consumer_facing": 0,
    "off_marker_hits": 0,
    "leakage_term_hits_in_consumer_strings": 0,
    "rank_inversions": 0,
    "confidence_field_changes_anywhere": 0,
    "critical_findings": 0,
    "high_findings": 1,
    "medium_findings": 2,
    "gate_suite_exit_code_bread": 0,
    "gate_suite_exit_code_crackers": 0
  },
  "commands_run": [
    {"cmd": "git diff --stat origin/master -- bread_frontend_v4.json crackers_frontend_v1.json", "exit_code": 0},
    {"cmd": "python full_compare.py (custom field-level deep-diff, both files)", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py bread_frontend_v4.json --baseline origin_master_bread_check.json", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py crackers_frontend_v1.json --baseline origin_master_crackers_check.json", "exit_code": 0},
    {"cmd": "python (independent trace cross-check, 23/23 bread bsip2_trace.json files)", "exit_code": 0},
    {"cmd": "python (unit test of _split_top_level_commas against flagship real ingredient string)", "exit_code": 0},
    {"cmd": "git diff --name-only origin/master...HEAD", "exit_code": 0},
    {"cmd": "git diff origin/master -- input_loader.py router_v2.py run_gates.py _catalog-client.tsx", "exit_code": 0},
    {"cmd": "grep -io pending / off-markers / leakage terms across both JSON files", "exit_code": 0}
  ],
  "not_done": [
    "Mobile-geometry/rendered-DOM/build-route checklist (no frontend files changed on this branch; out of the JSON-only scope named in the brief)",
    "Full BSIP2 scoring-governance audit of input_loader.py/router_v2.py (Nutrition/Data D8 lane, not this agent's; flagged as RT-3 for orchestrator confirmation)",
    "This report's own sha256 is necessarily post-hoc (a file's hash cannot include itself) — orchestrator should re-hash TASK-476_final_qa.md at close time to record the final value"
  ],
  "self_check": {
    "read_builder_summary_first": false,
    "verified_against_raw_artifacts_directly": true,
    "traces_read_independently_not_taken_on_faith": true,
    "git_mutations_performed": false,
    "scope_conflict_flagged": true
  }
}
```
