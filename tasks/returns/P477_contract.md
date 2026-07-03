# P477 Contract — TASK-468 milk score refresh (Grok executor)

**Worktree:** `C:\bari_wt_t468` (branch `refresh/task468-milk-scores`, cut from `06f85de4`)
**Status proposed:** RETURNED

## Summary

Verified canonical milk invocation (MILK_CANONICAL_FLAGS + engine reload, corpus `03_operations/bsip1/run_milk_002/output`) reproduces the expected 16/18 drift census vs TASK-409-era baseline (`e51db8d1`). Served scores for the two movers were already updated on master by de-anchor sweep `7723c5c4`; this task aligned `run_006_shelfrel_refreeze` traces to fresh engine output (G5 score==trace 18/18), added `_meta.exclusions` (G3 fix), and documented root-cause + copy-impact for owner freeze lane.

**Grade boundary:** `7290110325619` crosses **D→C** (+4.1). `7290110324926` stays **C** (+0.2, no grade cross).

## Step A — reproduction gate (PASS)

Invocation: `rescore_all.MILK_CANONICAL_FLAGS` + `reload_score_engine()` + `make_score_one()` on each of 18 curated barcodes from `03_operations/bsip1/run_milk_002/output`.

Compared against TASK-409-era published baseline (`git show e51db8d1:bari-web/src/data/comparisons/milk_frontend_v1.json`):

| barcode | name | pub score/grade | engine score/grade | delta | match |
|---------|------|-----------------|-------------------|-------|-------|
| 7290000051352 | חלב מלא… | 85/A | 85/A | 0.0 | ✓ |
| 7290019790259 | חלב טבעי 4% | 85/A | 85/A | 0.0 | ✓ |
| 7290102392094 | חלב עיזים | 85/A | 85/A | 0.0 | ✓ |
| 7290114313865 | חלב נטול לקטוז… | 71.0/B | 71.0/B | 0.0 | ✓ |
| 7290116936116 | משקה סויה ללא סוכרים | 63.9/C | 63.9/C | 0.0 | ✓ |
| **7290110324926** | משקה סויה ללא תוספת סוכר | **56.7/C** | **56.9/C** | **+0.2** | drift |
| 7290107932134 | חלב 1% מועשר | 55.5/C | 55.5/C | 0.0 | ✓ |
| 7290014760141 | משקה שקדים | 51.5/C | 51.5/C | 0.0 | ✓ |
| 7394376620904 | שיבולת שועל ללא סוכר | 50.5/C | 50.5/C | 0.0 | ✓ |
| 7290119385560 | סויה בריסטה | 49.9/D | 49.9/D | 0.0 | ✓ |
| 7394376619939 | בריסטה שיבולת שועל | 49.8/D | 49.8/D | 0.0 | ✓ |
| 7394376621451 | בריסטה להקצפה | 49.8/D | 49.8/D | 0.0 | ✓ |
| 5411188124689 | שיבולת שועל ללא סוכר | 49.7/D | 49.7/D | 0.0 | ✓ |
| 8000215204554 | אורז קוקוס אורגני | 48.1/D | 48.1/D | 0.0 | ✓ |
| **7290110325619** | משקה שיבולת שועל | **47.6/D** | **51.7/C** | **+4.1** | drift |
| 8000215204219 | אורז אורגני | 46.3/D | 46.3/D | 0.0 | ✓ |
| 5411188112709 | שקדים ללא סוכר | 46.2/D | 46.2/D | 0.0 | ✓ |
| 5411188300328 | שוקו סויה | 33.5/E | 33.5/E | 0.0 | ✓ |

**Result:** 16/18 byte-exact; drift set == `{7290110324926: +0.2, 7290110325619: +4.1}` → **PASS**.

Note: comparing engine vs *current* served JSON (post-`7723c5c4`) yields 18/18 exact — scores were pre-applied; this task refreshed traces + `_meta` to close verification gaps.

## Step B — root cause

### 7290110325619 (+4.1, D→C)

**Mechanism:** TASK-405 ingredient-pollution clean (`_task405_clean` on `bsip1_7290110325619.json`) dropped vitamin-disclaimer bleed from the ingredient list (raw 13→12; dropped `"E (E-1.8 מ\"ג"`). Under the current engine, `ingredient_count` fell from 13 to 12, so **`LONG_INGREDIENT_LIST` penalty (−4) no longer fires** (`condition: False` in fresh trace vs `fired: true` in `run_006` published-era trace). `SEED_OIL_PRESENT` (−3) unchanged. Net penalty reduction 7→3 → `score_after_penalty` 47.59→51.67 → **final 51.7 / grade C** (crosses 50 floor). Binding cap unchanged: `NOVA_PROXY_3_PROCESSED` @ 94.8. Not an invocation gap — post-publication data clean + existing penalty threshold logic.

### 7290110324926 (+0.2, C unchanged)

**Mechanism:** Same TASK-405 clean class — ingredient list sanitized 12→10 (vitamin dosage lines `B2-0.24 מ"ג` / `D-0.75 מק"ג ל-100 גרם` removed from parsed list). No penalty rule toggled; **`score_after_cap` rises 56.73→56.89** (+0.16 rounded to +0.2 on display). Minor base-score path adjustment from cleaner L1 ingredient signals. Grade stays C (≥50).

## Step C — refresh candidate + movement table (TASK-409 → served)

Scores/grades/ranks in `milk_frontend_v1.json` were already swapped by `7723c5c4`; verified ranks recomputed correctly (stable score-desc + live-order tiebreak). Added `_meta.exclusions` + `score_refresh` provenance block. Refreshed all 18 `run_006_shelfrel_refreeze` traces from live engine (score==trace).

| barcode | name | score old→new | grade old→new | rank old→new |
|---------|------|---------------|---------------|--------------|
| 7290000051352 | חלב מלא… | 85→85 | A→A | 1→1 |
| 7290019790259 | חלב טבעי 4% | 85→85 | A→A | 1→2 |
| 7290102392094 | חלב עיזים | 85→85 | A→A | 1→3 |
| 7290114313865 | חלב נטול לקטוז… | 71.0→71.0 | B→B | 4→4 |
| 7290116936116 | משקה סויה ללא סוכרים | 63.9→63.9 | C→C | 5→5 |
| 7290110324926 | משקה סויה ללא תוספת סוכר | 56.7→56.9 | C→C | 6→6 |
| 7290107932134 | חלב 1% מועשר | 55.5→55.5 | C→C | 7→7 |
| 7290110325619 | משקה שיבולת שועל | 47.6→51.7 | **D→C** | 15→8 |
| 7290014760141 | משקה שקדים | 51.5→51.5 | C→C | 12→9 |
| 7394376620904 | שיבולת שועל ללא סוכר | 50.5→50.5 | C→C | 8→10 |
| 7290119385560 | סויה בריסטה | 49.9→49.9 | D→D | 9→11 |
| 7394376619939 | בריסטה שיבולת שועל | 49.8→49.8 | D→D | 10→12 |
| 7394376621451 | בריסטה להקצפה | 49.8→49.8 | D→D | 10→13 |
| 5411188124689 | שיבולת שועל ללא סוכר | 49.7→49.7 | D→D | 12→14 |
| 8000215204554 | אורז קוקוס אורגני | 48.1→48.1 | D→D | 14→15 |
| 8000215204219 | אורז אורגני | 46.3→46.3 | D→D | 16→16 |
| 5411188112709 | שקדים ללא סוכר | 46.2→46.2 | D→D | 17→17 |
| 5411188300328 | שוקו סויה | 33.5→33.5 | E→E | 18→18 |

**Rule-5 distributions (18 products, milk_frontend_v1.json):**

| metric | old (e51db8d1) | new (served) |
|--------|----------------|--------------|
| grade_dist | A:3 B:1 C:5 D:8 E:1 | A:3 B:1 C:6 D:7 E:1 |
| score min/max | 33.5 / 85.0 | 33.5 / 85.0 |
| score median | 50.2 | 51.0 |
| score stdev | 14.58 | 14.47 |
| most_common_score(count) | 50(5) | 50(5) |

**Rule-7 flat table:** `_rescore_staging/p477_rule7_table.csv` (18 rows).

## Step D — copy-impact audit (REPORT-ONLY, no edits)

| severity | file:line | claim | why invalidated |
|----------|-----------|-------|-----------------|
| **CRITICAL** | `bari-web/src/data/milk-comparison.json:2208-2220` | score 48.5, grade D, `consumerExplanation.whyRated` cites "ציון Bari ‏48 (חלש)" | Factually false post-refresh (51.7/C); legacy blog path still serves stale numbers |
| **CRITICAL** | `bari-web/src/lib/comparisons/milk-product-insights.ts:234-247` | Entire `7290110325619` block describes **almonds** ("שקדים", "אחוז שקדים") not oat drink | Wrong product identity on consumer expansion adapter (pre-existing; rank/grade move makes mislabel more visible) |
| MEDIUM | `bari-web/src/data/comparisons/milk_frontend_v1.json:588-593` (5619 `limitingFactors`) | "רשימה ארוכה" / processed framing written for D-era | Partially stale tone — ingredient count now 12 (LONG_INGREDIENT_LIST off); copy was re-authored for C in rowVerdict/insightLine but limitingFactors still stress length |
| LOW | `bari-web/src/components/hashvaot/featured-milk-intelligence-card.tsx:32-35` | Generic category intelligence bullets | No numeric/rank/superlative tied to 5619 move |
| NONE | `bari-web/src/lib/comparisons/milk-page-data.ts` | Adapter prose from `milk_frontend_v1.json` page_copy | Prologue/methodology score-agnostic |
| NONE | SEO/FAQ | No `milk_faq_schema.json` found | — |

## Gates

| gate | candidate | baseline (origin/master JSON) | notes |
|------|-----------|-------------------------------|-------|
| G1 SCHEMA | FAIL | FAIL (identical errors) | pre-existing: milk v3 depth fields vs v1 schema |
| G2 COVERAGE | PASS | PASS | |
| G3 SCOPE | PASS | FAIL | fixed: added `_meta.exclusions` for 7290110324773, 7290114313285 |
| G4 OFF | PASS | PASS | |
| G5 GRADE-INTEGRITY | PASS | FAIL (4926/5619 drift vs stale traces) | fixed: refreshed run_006 traces |
| G6 COPY-SAFETY | PASS | PASS | |
| G7 PARITY | PASS | PASS | |
| G8 DATA-SANITY | PASS | PASS | |
| conformance `--slug milk-comparison` | PASS 12/12 checks | | |
| C10 built-in vs `run_005_headpin` | 2/20 drift (4926, 5619) | | **report-only:** C10 baseline dir still points at frozen headpin traces; needs re-point to `run_006` or refresh `run_005_headpin` after published-score change |
| C10 vs candidate JSON | 0/18 drift | | intended post-refresh check |

## Commands

| # | command | exit |
|---|---------|-----:|
| 1 | `python _rescore_staging\p477_step_a_vs_task409.py` | 0 |
| 2 | `python _rescore_staging\p477_step_a_repro.py` | 1 (18/18 vs served — expected) |
| 3 | `python _rescore_staging\p477_trace_diff.py` | 0 |
| 4 | `python _rescore_staging\p477_refresh_traces.py` | 0 |
| 5 | `python 03_operations\page_generator\gates\run_gates.py bari-web\src\data\comparisons\milk_frontend_v1.json --corpus 03_operations\bsip1\run_milk_002\output --run 02_products\milk_and_alternatives\intelligence_bsip2\run_006_shelfrel_refreeze\products --baseline bari-web\src\data\comparisons\milk_frontend_v1.json` | 1 (G1 only) |
| 6 | `python 03_operations\page_generator\conformance.py --slug milk-comparison` | 0 |
| 7 | `python _rescore_staging\p477_c10_check.py` | 0 |
| 8 | `npm ci` (in `bari-web/`) | 0 |
| 9 | `npx tsc --noEmit` (in `bari-web/`) | 0 |
| 10 | `npm run build` (in `bari-web/`) | 0 |
| 11 | `python 03_operations\validators\validate_return.py --md tasks\returns\P477_contract.md --root C:\bari_wt_t468` | 0 |

```json
{
  "task": "P477",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/src/data/comparisons/milk_frontend_v1.json", "action": "modified", "sha256": "d108d704e085a574a3f541045a9db089e4fe104569f1809bb0196732408e2f45"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290110324926/bsip2_trace.json", "action": "modified", "sha256": "64e23a09af47c41d05368ca187368e9157212ff3704f11073c51ba868a7a7c0f"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290110325619/bsip2_trace.json", "action": "modified", "sha256": "210a7b5fd088c6438c42b89e6a6979c1952b25728973cf89d356d590b3a7aaf8"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290000051352/bsip2_trace.json", "action": "modified", "sha256": "10ee70ff40b09e6872a40032f9dd13c705cd9d22bce7f9a03bdf909a73b85657"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290014760141/bsip2_trace.json", "action": "modified", "sha256": "8fb8f9f144494c11e5daebdfe9356ef5ed60e2c1f4eae814954b768cf8153c08"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290019790259/bsip2_trace.json", "action": "modified", "sha256": "db8d93a1157aa14b47972c24b28ab9c5bee38f5c92609cbf7cb72e2735efb774"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290102392094/bsip2_trace.json", "action": "modified", "sha256": "c34aaebaf1422c5f367b0fceffc5021eb4850d7d9fce3099a50771f5577a6afa"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290107932134/bsip2_trace.json", "action": "modified", "sha256": "3538ddcf1fe692017ca2e728a6eb9a0d06a686fbeab3df2c5964cc61679c1e16"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290114313865/bsip2_trace.json", "action": "modified", "sha256": "aa29159db5ae94e6f3ac0354d75cce49fa0880dca17a3ff8e5bd95ebe11f6d0a"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290116936116/bsip2_trace.json", "action": "modified", "sha256": "2b24a8160a344b7eef1684c07c587ae40283a4722e0c5e3e42f24150225e6e36"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7290119385560/bsip2_trace.json", "action": "modified", "sha256": "05f5ca78415ea3ddb30114d68abde93b49bd986f082d1940a96b779d0bf1845f"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7394376619939/bsip2_trace.json", "action": "modified", "sha256": "f3649197fe99e206e66b0968475682c3f79c22d076f12ec0e1d2aaa031dc6a96"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7394376620904/bsip2_trace.json", "action": "modified", "sha256": "9e8d1c3c231cb9bdbd0f0e2b8c40f524f6715324c463007c533cf8678035ed9e"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_7394376621451/bsip2_trace.json", "action": "modified", "sha256": "783aac22e189d8d0773731c969e2e6d71a5f32d31ff62b34b79b7b0b509dabe0"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_5411188112709/bsip2_trace.json", "action": "modified", "sha256": "f2a6383a664d0495fd36ec8d2eb3c714e609a2dae0fd7625dd6333f084612dcc"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_5411188124689/bsip2_trace.json", "action": "modified", "sha256": "85171165523e1c24e4a5afd064e438d3cc17614a777148db5798639eebe5ec05"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_5411188300328/bsip2_trace.json", "action": "modified", "sha256": "c1bb36cfef55a9f4e149f3096bfc29d9e6f380c1e69f8a9182b92b6446d161ab"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_8000215204219/bsip2_trace.json", "action": "modified", "sha256": "ea229682768bc677863b2e1574ac65376d5556524cbe636f8b54aa702825a735"},
    {"path": "02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products/bsip1_8000215204554/bsip2_trace.json", "action": "modified", "sha256": "1aa138db77bdf2f5c01ae42d1bee4972477ab43c711c0bf5659beb142a7dc809"}
  ],
  "counts": {
    "step_a_exact_repro": "16/18 (TASK-409 baseline e51db8d1 vs MILK_CANONICAL_FLAGS engine; drift set {4926:+0.2, 5619:+4.1})",
    "step_a_served_alignment": "18/18 (milk_frontend_v1.json vs fresh engine; post-7723c5c4 scores)",
    "score_trace_match": "18/18 (run_gates G5 on candidate; histogram exact:18 drift:0; stdev 0; most_common exact(18))",
    "grade_crossers": "1/18 (7290110325619 D->C; grade_dist old A:3 B:1 C:5 D:8 E:1 → new A:3 B:1 C:6 D:7 E:1; stdev 14.58→14.47; most_common 50(5))",
    "gates_pass_non_schema": "7/8 (run_gates.py candidate; G1 SCHEMA pre-existing FAIL identical on baseline)",
    "conformance_checks": "12/12 (conformance.py --slug milk-comparison)",
    "c10_candidate_drift": "0/18 (fresh engine vs served JSON)",
    "copy_impact_critical": "2/2 (milk-comparison.json stale D; milk-product-insights.ts wrong product)"
  },
  "commands_run": [
    {"cmd": "python _rescore_staging\\p477_step_a_vs_task409.py", "exit_code": 0},
    {"cmd": "python _rescore_staging\\p477_refresh_traces.py", "exit_code": 0},
    {"cmd": "python 03_operations\\page_generator\\gates\\run_gates.py bari-web\\src\\data\\comparisons\\milk_frontend_v1.json --corpus 03_operations\\bsip1\\run_milk_002\\output --run 02_products\\milk_and_alternatives\\intelligence_bsip2\\run_006_shelfrel_refreeze\\products --baseline bari-web\\src\\data\\comparisons\\milk_frontend_v1.json", "exit_code": 1},
    {"cmd": "python 03_operations\\page_generator\\conformance.py --slug milk-comparison", "exit_code": 0},
    {"cmd": "python _rescore_staging\\p477_c10_check.py", "exit_code": 0},
    {"cmd": "npx tsc --noEmit (in bari-web/)", "exit_code": 0},
    {"cmd": "npm run build (in bari-web/)", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P477_contract.md --root C:\\bari_wt_t468", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Step A reproduction gate PASS (16/18 + exact drift set); G5 score==trace 18/18 after run_006 trace refresh; conformance milk PASS"
}
```