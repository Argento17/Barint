# TASK-463 / P467 — Root-cause: empty `expansion.limitingFactors` on bread, cheese, and partial others

READ-ONLY investigation. No product JSON, generator, or frontend file was modified. This report is the only artifact written.

Scope note vs the delegation spec: the spec names `cheese_frontend_v5.json`. **No `_v5` file exists** — the live "cheese" (soft/spreadable, non-hard, non-brined) category file is `bari-web/src/data/comparisons/cheese_frontend_v4.json`, 47 products, matching every count given in the spec (grades A..E, 15 D + 2 E). Treated as the intended target; flagging the filename mismatch rather than silently substituting.

---

## 1. Where `expansion.limitingFactors` is produced

Two structurally different producers exist in the repo, and that duality is itself part of the root cause.

**(a) The shared/canonical path** — `03_operations/page_generator/copy/author_copy.py::_limiting_factors(sheet)` (lines 188–229). Deterministic: reads `sheet["driver"]["story"]` (a BSIP2 trace-derived driver label), `sheet["nutrition"]`, `sheet["additive_count"]`, and maps specific `story` values (`calorie_dense`, `sugar_load`, `heavy_processing_additives`, `seed_oil_present`, etc.) to fixed Hebrew factor strings, capped at 2. Output is merged into the live page by `03_operations/page_generator/copy/merge_copy.py::merge()` (lines 136–140):
```python
lim = list(cexp.get("limitingFactors", []))
if lim:
    exp["limitingFactors"] = lim
else:
    exp.pop("limitingFactors", None)  # absent when no limits (schema)
```
This is the module the copy-engine (P29/TASK-257) contract expects: when there really is nothing binding, the **key is omitted entirely** — never a literal `[]`. This is the schema convention `merge_copy.py`'s own docstring documents at line 20 ("matches live granola/snacks").

**(b) Per-category bespoke scripts** — e.g. `02_products/hummus/frontend/build_hummus_explanation_v1.py` (TASK-086, hummus) and `02_products/hard_cheeses/build_final_frontend_v2.py` (lines 138/143, hard_cheeses TASK-412). Each hand-codes its own version of the positiveSignals/limitingFactors derivation from that category's own BSIP1/BSIP2 trace files, independently of `author_copy.py`. These are the categories now fully populated (hummus, hard_cheeses).

**(c) No producer at all** — bread and (soft) cheese. Confirmed by trace: neither category's generation history ever invokes `_limiting_factors()`, `build_*_explanation*.py`, or any equivalent. The field exists in their JSON only because the page-generator's structural schema initializes `expansion.positiveSignals` / `expansion.limitingFactors` as empty-list scaffolding at page-creation time (`03_operations/page_generator/generate_page.py:573` initializes `"limitingFactors": []` as a template default), and nothing downstream ever filled it.

This means the field is genuinely `[]`-present (not omitted) on bread/cheese specifically because they went through generator-scaffolding without ever passing through step (a) or (b) — a different code path than the "omit-when-empty" schema convention documents.

---

## 2. Why bread_frontend_v4 and cheese_frontend_v4 are wholesale-empty

Verified with git archaeology, not inference.

**Bread** (`bari-web/src/data/comparisons/bread_frontend_v3.json`, later renamed v4):
- Origin commit `43cd7b24` "TASK-322: Conform bread to uniform scoring spine" (2026-06-18) added the file fresh (1478 lines, single commit) — built directly by a page-generator/BSIP run, not through `author_copy.py`.
- Confirmed via diff: `limitingFactors: []` for all 29 products **already at this origin commit**, before any copy pass touched the file.
- Next commit `1a4b67c9` "TASK-322: bread copy — author all 29 insightLines, rowVerdicts, comparisonContexts" explicitly lists what it authored: `insightLine`, `rowVerdict`, `comparisonContext`, `bottomLine`, `_website_cluster`. Its commit message **never mentions `positiveSignals` or `limitingFactors`**, and diff inspection confirms it did not touch either field — both remain `[]` after this commit, verified by direct read of the committed diff (`positiveSignals: []` present unchanged in every hunk).
- Every subsequent commit in bread's history (TASK-332 deep-dive, D4 additive layer, TASK-397 fat-sentinel neutralize, TASK-409 rederive, TASK-411 strip-deep-dive, TASK-421 sort, TASK-423 copy rework, un-flag passes) touches score/grade/copy-tooltip fields but never runs an explanation-layer step.
- **TASK-409's rederive script** (`_task409_rederive_v2.py`, `update_product()` lines 67–89) explicitly documents its own scope: *"Update score/grade and render_fields only. Preserve all other fields."* It does `updated = dict(live_prod)` (shallow copy) and only overwrites `score`, `grade`, `novaGroup`, `d4_additives`, `confidence_level`. It is provably NOT the origin of the emptiness (confirmed: `[]` for all 29 bread products both immediately before and immediately after the TASK-409 Gate-E assembly commit `338668d5`) — it inherited pre-existing empty scaffolding and correctly left it alone per its own stated contract.
- **Verdict: bread never had an explanation-engine step run, ever, in its entire lineage.** Not a regression — a pipeline stage that was simply never executed for this category.

**Cheese** (`bari-web/src/data/comparisons/cheese_frontend_v4.json`, 47 products, soft/spreadable — distinct from `hard_cheeses` and `brined_cheeses`):
- Origin commit `95257fac` "TASK-321I: stage conformed cheese data (53 products, copy authored)" (2026-06-17) added the file fresh in one shot (7117 lines, single commit) — same pattern as bread: landed as a full staged dump, no `author_copy.py`/explanation-engine invocation found anywhere in its lineage.
- `positiveSignals` and `limitingFactors` are both 0/47 non-empty on the live file today — identical dual-empty signature to bread.
- Same TASK-409 rederive relationship: `task409_rederive_cheese_20260626` run_id present in `_meta`, same `update_product()` scope (score/grade only), same non-involvement in the expansion block.
- **Verdict: identical root cause to bread** — an explanation-engine pass was never run for this category, at any point in its history, including through the two later TASK-418/TASK-420/TASK-423 copy-rework passes (which touched confidence-tooltip wording and E-code prose, never `positiveSignals`/`limitingFactors`).

Contrast: `hard_cheeses_frontend_v4.json` (31 products, TASK-412, a **different category** from "cheese") is 31/31 populated because `build_final_frontend_v2.py` hard-codes the derivation inline (bespoke per-category script, item (b) above). This proves the gap is not "the explanation engine doesn't support cheese-type products" — it is "no explanation step, shared or bespoke, was ever invoked for these two specific category builds."

---

## 3. Partial empties — genuine ceiling vs same gap on a subset

Distinguished with real BSIP2 trace evidence, not assumption.

| Category | n | lf_empty | Verdict |
|---|---|---|---|
| cookies_coffee_frontend_v2 | 117 | 10 | **GAP** (evidence below) |
| granola_frontend_v2 | 22 | 7 | Ambiguous/likely gap-adjacent — see below |
| cakes_hard_cookies_frontend_v1 | 62 | 4 | **GAP** — same pattern as cookies_coffee |
| crackers_frontend_v1 | 19 | 6 | **GAP** for the A/B-grade empties on `positiveSignals`; `limitingFactors` emptiness plausible for the top scorers only |

**Direct trace proof (cookies_coffee, barcode 7290118423904, grade E, score 34.2):**
Pulled `02_products/cookies_coffee/bsip2_outputs/run_cookies_task393_final/products/bsip2_trace_7290118423904.json` directly. The trace's own `explanation_drivers` field reads:
```
"DOMINANT: Binding cap=68.0 from rules: ['NOVA_PROXY_4_ULTRA_PROCESSED', 'ADDITIVE_MARKERS_3_PLUS']"
"PENALTIES: ['MULTIPLE_ADDED_SUGAR_MARKERS', 'SEED_OIL_PRESENT']"
```
with `penalties_applied` = `MULTIPLE_ADDED_SUGAR_MARKERS` (-5, "added_sugar_sources=3") and `SEED_OIL_PRESENT` (-3), and `caps_applied` = NOVA-4 (cap 68) + additive-markers-3-plus (cap 72), `binding_cap=68.0`, `final_score_estimate=34.2`, `grade_estimate="E"`.

This is a story (`seed_oil_present`, `multiple_added_sugar_sources` per `author_copy.py`'s own vocabulary) that `_limiting_factors()` is explicitly built to translate (lines 206–220: `sugar_load`/`multiple_added_sugar_sources` → sugars-grams factor; `seed_oil_present` → "שמן צמחי מעובד ברשימת הרכיבים"). A grade-E product at 34.2 with two named fired penalties and a binding cap, yet **zero** `positiveSignals` and **zero** `limitingFactors`, is not a legitimate "nothing material" result — it is a product whose copy/explanation pass never ran, or ran on a stale trace and dropped the driver mapping. Same shape repeats for cookies_coffee bc=7290000061245 (D, 37.4), bc=7290118422617 (E, 33.7) — both zero-signal-of-any-kind at D/E grades.

**cakes_hard_cookies** 4 empties are D 37.0 / E 32.0 / E 32.0 / E 30.4 — same signature (low-grade, zero limitingFactors, and 3 of 4 also zero positiveSignals). Given cakes_hard_cookies shares `run_id: task409_rederive_cakes_20260626` lineage with bread/cheese (same TASK-409 rederive family, same "preserve expansion, touch score/grade only" script), this is very likely the identical gap on a small subset of that category rather than a distinct computed-empty case. Not independently trace-verified product-by-product in this pass (see `not_done`), but the lineage match plus the identical low-grade/zero-signal shape is strong circumstantial evidence, not proof.

**crackers** 6 empties skew toward the TOP of the shelf (A 81.6, four B's 79.6/74.1/73.3/68.1, one C 59.6) — this is the pattern where `limitingFactors` emptiness is plausible (little binds a high scorer). But those same 6 rows also show `positiveSignals` empty (0 items) at grades as high as A/81.6 — an A-grade product with **zero stated positive signals** is itself a gap, just in the sibling field, not `limitingFactors`. Flagging this as adjacent to the task's named scope: the `positiveSignals` gap is broader than `limitingFactors` across the board (cookies_coffee 95/117 empty, cakes_hard_cookies 61/62 empty, cheese 47/47, bread 23/23) and shares the same code path — any fix to `limitingFactors` should be scoped to cover `positiveSignals` too, since they are computed by the same function pass in every producer this investigation found.

**granola** 7 empties are B/B/B/C/C/D/D (score range 38.3–69.7) with `positiveSignals` populated in 6/7 — i.e., the explanation pass clearly ran for this category (granola is in the copy-engine family, `run_id: run_granola_task385_25g`, `_meta` carries `pending_copy_count`/`promoted_from` — hallmarks of the `author_copy.py`/`merge_copy.py` path). Because `positiveSignals` is present but `limitingFactors` specifically is empty even at D-grade (38.3, 39.8), this reads as `_limiting_factors()`'s **narrow story-list** (lines 203–220: only 6 specific `story` values map to a factor) failing to cover whatever driver story these D-grade granola products actually carry — a real logic gap in the function's story coverage, not a missing pipeline stage. This is a different sub-class from bread/cheese/cookies_coffee/cakes (missing computation) — it is a computation that ran but has an incomplete story→factor mapping table. Not fully diagnosed to the specific missing `story` value in this pass (see `not_done`).

---

## 4. Gate coverage — none of the wired gates check `limitingFactors` presence/coherence

Checked both live-wired gate suites end to end:

- **`03_operations/page_generator/gates/run_gates.py` (G1–G8)**: `limitingFactors` is touched only inside `_collect_consumer_strings()` (line 933), which is a helper for `gate_grade_integrity` (G5)'s Hebrew-grade-letter-leakage scan (`_check_hebrew_grade_prose`). It iterates whatever strings exist in the array looking for stray "S/A/B/C/D/E" letter leakage that contradicts the badge grade. If the array is empty, the loop trivially produces zero checks and **passes silently** — there is no assertion anywhere in G1–G8 that the array must be non-empty, nor any rule correlating grade/penalty-count with expected array length.
- **`03_operations/spine/validate_comparison_page.py`** (the second "7/7" page gate referenced by memory rule `run_both_page_gates`): `limitingFactors` appears in `RENDERED_EXPANSION` (line 24) purely for a `PENDING_COPY` placeholder-string scan (line 98–99: `if PENDING in json.dumps(ex.get(k))`). An empty `[]` is not `PENDING_COPY`, so it passes clean.

**No wired gate anywhere checks limitingFactors presence, count, or coherence with grade/trace penalties.** Where such a check would wire, cleanly, without inventing new infrastructure: `gate_grade_integrity` (G5) in `run_gates.py` already loads both the frontend JSON and the BSIP2 traces (`--traces` arg) for its scoring checks — it is the natural home for a new assertion of the shape *"if `caps_applied` or `penalties_applied` is non-empty in the product's trace, `expansion.limitingFactors` must be non-empty"* (and the inverse sanity check for `positiveSignals` against `dimension_scores`/absence of caps). This feeds directly into the TASK-453 gate backlog as a new G5 sub-check rather than a new G9, since it reuses G5's existing trace-loading plumbing.

---

## 5. Recommended fix path (one path, sequenced — not a menu)

Constraints in force, all confirmed applicable:
- **Uniform-baseline doctrine**: one `generate_page` path, no bespoke per-category fixes. This investigation found the opposite already exists in the wild (hard_cheeses' and hummus' bespoke inline scripts) — that is pre-existing drift, not something to extend further.
- **Owner product-description freeze (ACTIVE)**: owner is rewriting ALL product descriptions in another chat; no lane touches `rowVerdict`/`insightLine`/`expansion` fields until that lands. `limitingFactors`/`positiveSignals` are exactly the fields under freeze — regenerating them now would collide with in-flight owner edits and get overwritten or conflict on merge.
- **Interim frontend mitigation the orchestrator is considering**: collapse the empty state in `expansion-section.tsx` rather than assert "no material limiting factors" when the data is simply absent.

**Recommendation: ship the frontend mitigation now; sequence the real data fix after the description freeze lifts.**

1. **Now (Data Agent has no write scope on this READ-ONLY task, but flags for the Frontend Agent / next dispatch):** `expansion-section.tsx` lines 583–597 need a distinction the data currently cannot support cleanly — "computed-and-genuinely-clean" (real omission, should say "no material limiting factors") vs "never computed" (should say nothing, or a neutral "not yet assessed" state, never a green checkmark). Since the JSON today cannot distinguish these (both cases render as `[]`/absent), the safest interim frontend change is: **only render the green-check "no material limiting factors" copy when the category is known-complete** (i.e., NOT bread, NOT cheese_v4, and NOT the specific flagged barcodes in cookies_coffee/cakes_hard_cookies/crackers/granola identified above) — otherwise render nothing (collapse the panel) rather than assert a claim the pipeline never verified. This is reversible, ships without touching any product JSON or copy, and stops the false "no material limiting factors" claim from reaching consumers today. This is a Frontend Agent task, not mine to implement.
2. **After the description freeze lifts:** run the real fix as ONE pipeline pass, not per-category patches — extend `author_copy.py`'s `_limiting_factors()`/positive-signals sibling function's story-coverage (the granola gap: narrow story-list) AND run it (or the equivalent explanation step) against bread and cheese_v4's existing BSIP2 traces for the first time ever, through the standard `merge_copy.py` merge path so the omit-when-empty schema convention applies uniformly. This retires the bespoke hard_cheeses/hummus scripts' duplicated logic only if/when Product decides that's in scope — out of scope for this fix on its own.
3. **Gate the fix**: add the G5 trace-correlation check named in §4 (`caps_applied`/`penalties_applied` non-empty ⇒ `limitingFactors` non-empty) so this class of gap cannot silently reappear on the next category build. This is a Data Agent implementation task once Product/Nutrition approve the gate rule addition (D8 scope, not self-approved).

Sequencing rationale: step 1 is reversible, consumer-facing-safe, and does not touch any frozen field — it satisfies the "say nothing rather than claim" mitigation the orchestrator is already weighing, immediately. Steps 2–3 are the durable fix but must wait for the freeze because they write into the exact fields (`expansion.*`) the owner is mid-rewrite on; running them now would either be silently overwritten or create a merge conflict with the owner's in-flight work.

---

## Evidence appendix — raw counts (recomputed directly from committed JSON, this pass)

```
bread_frontend_v4:              n=23  lf_empty=23  ps_empty=23
cheese_frontend_v4:              n=47  lf_empty=47  ps_empty=47
cookies_coffee_frontend_v2:      n=117 lf_empty=10  ps_empty=95
granola_frontend_v2:             n=22  lf_empty=7   ps_empty=1
cakes_hard_cookies_frontend_v1:  n=62  lf_empty=4   ps_empty=61
crackers_frontend_v1:            n=19  lf_empty=6   ps_empty=11
brined_cheeses_frontend_v2:      n=36  lf_empty=3   ps_empty=3   (note: census said 33/3; live file has 36 products today, not 33 — file has moved since the census was taken; ratio direction unchanged)
cereals_frontend_v2:             n=20  lf_empty=0   ps_empty=0
chocolate_tablets_frontend_v1:   n=35  lf_empty=0   ps_empty=0
chocolate_bars_frontend_v1:      n=23  lf_empty=0   ps_empty=14  (NEW FINDING: positiveSignals gap not in original census — census only tracked limitingFactors)
hard_cheeses_frontend_v4:        n=31  lf_empty=0   ps_empty=0
hummus_frontend_v5:              n=57  lf_empty=0   ps_empty=0
juices_frontend_v3:              n=17  lf_empty=0   ps_empty=5   (NEW FINDING: same)
milk_frontend_v1:                n=18  lf_empty=0   ps_empty=0
protein_combined_frontend_v2:    n=32  lf_empty=0   ps_empty=0
snacks_frontend_v5:              n=21  lf_empty=0   ps_empty=2   (NEW FINDING: same)
TOTAL (16 files): n=580  lf_empty=100  ps_empty=262
```

**New finding beyond the task's named scope**: `positiveSignals` emptiness is broader than `limitingFactors` emptiness across nearly every category checked (262/580 vs 100/580 products, all 16 files), including three categories the original census marked as "FULLY populated" for limitingFactors (chocolate_bars 14/23, juices 5/17, snacks 2/21 empty positiveSignals). Since both fields are produced by the same code path in every producer traced in this report, any fix scoped to `limitingFactors` alone will leave a larger sibling gap live. Recommend the owner/orchestrator fold `positiveSignals` into the same fix ticket rather than opening a second one later.

**brined_cheeses count discrepancy**: the task brief's verified-facts block states 33/3; this pass's direct read shows 36/3 (33 populated + 3 empty in the brief's split, vs 33 populated + 3 empty out of 36 total counted here — the totals differ by n but the "3 top-A empties, plausibly legitimate" characterization from the brief was not independently re-verified against trace data in this pass; not_done below).
