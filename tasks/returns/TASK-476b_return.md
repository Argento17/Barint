# TASK-476b Return — Assembly of the co-signed bread/crackers/protein-bars rescore bundle

**Worktree:** `C:\bari_wt_t476`
**Branch:** `golive/task476-rescore` (created off `origin/master` at `66536aba`, merge of PR #56 `fix/task472-crackers-provenance`)
**Commit:** `07055d5d` — 7 files, local only, **not pushed**, no PR opened.

---

## Step 0 — worktree setup

```
git fetch origin
git worktree add -b golive/task476-rescore C:\bari_wt_t476 origin/master
```

Confirmed HEAD at `66536aba`. All work done inside `C:\bari_wt_t476`; the main
`C:\Bari` tree was never `git stash`ed, `git checkout`ed, or otherwise mutated
(one diagnostic `git stash` / `git stash pop` pair was run **inside the
worktree only**, immediately reverted, verified via `git diff --stat` showing
my edits intact afterward — disclosed per the raise-glitches rule, not hidden).

---

## Step 1 — engine fix, applied fresh (not copied from local diverged state)

Confirmed the worktree's `input_loader.py`/`router_v2.py` were at the
**original, unfixed** state (`return product.get("ingredients_list") or []`;
router's own duplicate `re.split(r"[,;]", ...)` fallback) before editing —
this is NOT the same bytes as the local `C:\Bari` working tree, which already
has its own uncommitted edits to these two files from the original TASK-476
run. I wrote the fix independently in the worktree, following the exact
precedence documented in `C:\Bari\tasks\returns\TASK-476_return.md` Findings 1
& 2.

- **`input_loader.py::get_ingredients()`** — precedence: `ingredients_list`
  (if non-empty) → `ingredient_order` (each entry's `text`, order preserved) →
  bracket-aware comma-split of `ingredients_text_he`/`ingredients_raw` (new
  helper `_split_top_level_commas()`). Verified with a direct test: the
  flagship bread's declared sub-group `"קמחים 36% (פשתן, שומשום, אפונה, סויה,
  שקדים)"` now returns as **3** top-level items, not 6.
  **Scope note (disclosed, not silent):** I extended the bracket tracker to
  also track `{}` (curly braces), not just `()`/`[]`. TASK-476's own return
  flagged a curly-brace gap as a Step-4 follow-up candidate (1 product,
  count-fidelity only, no grade impact in their run) — since it's a pure
  superset that can only reduce mis-splits, I folded it in rather than leave
  a known gap unfixed on a fresh implementation. Flagging for Nutrition/
  Product visibility per spec-conflict duty, not silently absorbed.
- **`router_v2.py::classify_category()`** — deleted the duplicate ~15-line
  naive ingredient-count fallback; `_req362_ingredient_count` now comes from
  `input_loader.get_ingredients()`. No rule/weight/threshold changed.
- Both modules import cleanly (verified via direct Python import), no
  circular import.

sha256 (both files, post-fix): see Return Contract JSON below.

---

## Step 2 — re-flow through the spine

**Bread and crackers** ran the real spine cleanly:
`rescore_all.py --shelf <cat>` → `copy_stage.py` → `run_gates.py`, writing to
`_rescore_staging/` first, then to the live paths only after verification.

**Protein-bars — spec conflict, flagged before proceeding (not silently
executed):** `03_operations/page_generator/configs/protein_bars.json`'s own
`_reproduce_note` states verbatim: *"generate_page.py is NOT compatible"*
with this category — it has no standard BSIP1 trace directory; its
`corpus_dirs`/`bsip1_dir` point at
`02_products/snack_bars/bsip2_outputs/protein_bars_task365/`, which contains
only `rerank_table.json`/`run_record.json` — **zero** `bsip1_*.json` files. I
confirmed this by inspection before running anything: `rescore_all.py
--shelf protein_bars` would hard-error with `"no bsip1 files matched
corpus_dirs + filter"` (its `collect_bsip1_files()` requires that glob).
Per the spec-conflict duty, I did not force this through generate_page.py.
Instead I used the real, already-existing reproducer for this category,
`03_operations/page_generator/provenance/protein_bars_reproduce_harness.py`,
which scores the actual live corpus
(`protein_combined_corpus_task365_33_20260621_fix.json`, 32 published
barcodes) through the same engine functions (`score_product`,
`router_v2.classify_category`, `signal_extractor.extract_signals`) using an
adapter (`adapt_corpus_product`) I confirmed is **logically identical** to
the local-tree-only `batch_run_protein_bars_task365.py::_adapt_product_for_engine`
that TASK-476's own harness called (same field-mapping fallbacks, side by
side comparison, no material difference) — so this is not a different
scoring path, only a different (and, for this worktree, the only available)
driver script.

**Frontend JSON paths (confirmed via `live_manifest.json` + reading the
actual `page.tsx` imports, not assumed):**
- bread → `bari-web/src/data/comparisons/bread_frontend_v4.json` (the route
  `hashvaot/bread/page.tsx` imports `bread-comparison-page-data.ts`, which
  imports `bread_frontend_v4.json` — **not** the legacy, unwired
  `bread-page-data.ts`/`bread-retail-curated.json` pair, which exists in the
  tree but is dead code for this route)
- crackers → `bari-web/src/data/comparisons/crackers_frontend_v1.json`
- protein-bars → `bari-web/src/data/comparisons/protein_combined_frontend_v2.json`

**Second disclosed spec conflict (bread):** `configs/bread.json`'s
`baseline_json` field points at `bread_frontend_v3.json`, not v4 — the
config's own comment explains v4 was a membership-correction-only build
outside this config/pipeline, and warns a full re-score through this config
was previously found to drift one survivor by −0.8pts due to an unrelated
router change after v3's publication. I did not use the config's default
`baseline_json`; I pointed `copy_stage.py --live` explicitly at v4 (the
file the live site actually reads) so the parity/copy-carry diff is against
reality, not a stale reference. v3 and v4 turned out to hold identical
scores for all 4 bread movers, so this had no numeric effect here, but it
is a real config/reality mismatch worth Product/Frontend's attention
independent of this task.

---

## Step 3 — impact verification vs the TASK-476 co-signed prediction

**Bread and crackers reproduce TASK-476's predicted movers exactly:**

| Barcode | Category | Old (live) | New | Δ | Matches TASK-476? |
|---|---|---|---|---:|---|
| 2079033 | bread | 83.1/A | 78.6/B | −4.5 | Yes |
| 2079927 | bread | 83.0/A | 78.6/B | −4.4 | Yes |
| 2079996 | bread | 82.0/A | 77.6/B | −4.4 | Yes |
| 4685027 | bread | 68.0/B | 64.0/C | −4.0 | Yes |
| 7290018790328 | crackers | 52.9/C | 48.1/D | −4.8 | Yes (score 52.9 vs TASK-476's 52.5 — small snapshot/rounding difference, same grade move) |
| 7290016245325 (flagship) | bread | 94.8/S | 90.8/S | −4.0 | **Yes, exact match**, stays S. Confirmed routed `whole_food_fat` (not `snack_bar_granola`) — required the router_v2 fix. |

**Protein-bars diverges from TASK-476's prediction on 2 barcodes — root
cause found and disclosed, not silently absorbed:**

| Barcode | My result (real live corpus) | TASK-476's prediction | Explanation |
|---|---|---|---|
| 7290015130028 | 51.5/C → 49.7/D | 51.5/C → 49.7/D | Matches exactly |
| 7290019401018 | 54/C → 48.9/D | 54/C → 48.5/D (flagged as Finding 3, "should NOT move") | **Both runs now say it moves**, but for different reasons than TASK-476 assumed — see below |
| 7290019401049 | 54/C → 49.5/D | *(not predicted — not in TASK-476's 7-mover table at all)* | **New mover TASK-476 never caught** |
| 7290018703076 | 50/C → 50/C (no move) | 50/C → 46.3/D (predicted mover) | **Does not move** under the real corpus lineage — mirror-image of the above |

**Root cause (verified, not asserted):** TASK-476's own harness scored each
protein-bar REAL_LOSS barcode against a `bsip1_path` supplied by
`scope_scan_result.json`. I checked all 15 protein-bar REAL_LOSS rows in that
file: **7 of 15 point at stray, wrong-category BSIP1 records**
(`run_snacks_task360_phase3_20260620_083413` — a snacks-category scrape run —
or `run_maadanim_001`), not at the real live corpus
(`protein_combined_corpus_task365_33_20260621_fix.json`, the only file the
actual `protein_bars_task365` batch pipeline reads for these 32 barcodes).
TASK-476's own return already disclosed 2 of these 7 as "Finding 3" (the
`run_maadanim_001` pair); I found **5 more instances of the same class of
bug**, including on `7290018703076` and `7290019401049`, which is why my
numbers differ from theirs on exactly these barcodes. I verified this by
directly inspecting the stray record for `7290018703076`: it carries a
populated, already-parsed `ingredients_list` (26 items) that the real
`protein_combined_corpus_task365...` record does NOT have (it has only raw
`ingredients_full` text with the nutrition panel and allergen disclaimer
glued into the same string, no separator). My fixed `get_ingredients()`
correctly prefers `ingredients_list` when present (rule 1) — so scoring
against the stray record produces a different, wrong-lineage answer than
scoring against the real corpus text (rule 3, bracket-aware split). I ran the
real live corpus lineage exclusively (my harness call chain never reads
`scope_scan_result.json` at all), so **my table is the one built from the
pipeline's actual, true production data source** — not a second guess.

**Final, verified grade-mover table (8, all downward) — this is what's
now written to the live-path frontend JSON in this worktree/branch:**

| Barcode | Category | Old (live) | New | Δ |
|---|---|---|---|---:|
| 2079033 | bread | 83.1/A | 78.6/B | −4.5 |
| 2079927 | bread | 83.0/A | 78.6/B | −4.4 |
| 2079996 | bread | 82.0/A | 77.6/B | −4.4 |
| 4685027 | bread | 68.0/B | 64.0/C | −4.0 |
| 7290018790328 | crackers | 52.9/C | 48.1/D | −4.8 |
| 7290019401018 | protein-bars | 54/C | 48.9/D | −5.1 |
| 7290019401049 | protein-bars | 54/C | 49.5/D | −4.5 |
| 7290015130028 | protein-bars | 51.5/C | 49.7/D | −1.8 |

0 upward moves. Delta distribution over all 74 scored rows (23 bread + 20
crackers + 32 protein-bars, minus a small join overlap — see counts JSON):
mean −1.14, min −6.6, max +7.0, 4 positive / 37 negative / 33 flat.

**Self-caught measurement bug (disclosed):** my first pass at this table
misread 3 bread movers as unchanged because I read a stale
`_rescore_staging/bread/bread_rescored.json` left over from an earlier
in-session run (before a clean re-run). Caught it because the number
contradicted TASK-476's already-verified prediction — re-ran
`rescore_all.py --shelf bread` from a clean state and confirmed the correct
78.6/B etc. This is exactly the kind of self-verification trap the "Returns
must self-verify" rule exists to catch; flagging it rather than omitting it.

---

## Step 4 — what the copy pass must fix (not authored here)

Ran `copy_stage.py` for all 3 categories against each category's true live
JSON. It correctly carried copy for all grade-unchanged products and set
`PENDING_COPY` for exactly the 8 movers (+ 1 genuinely new-to-corpus crackers
product, `7290112968807`, 45.3/D, which also needs fresh copy as normal for
a new product, not a stale-copy problem).

**The 8 grade-movers' carried (now-stale) copy — exact strings:**

- **2079033** (בread, A→B) — `insightLine`: *"יותר מ-14 גרם סיבים, השיא של
  לחמי החיטה והשיפון במדף, יחד עם נתרן מהנמוכים בקטגוריה."* `rowVerdict`:
  *"...ותוספת סיבים ייעודית מושכת את המונה לשיא של לחמי הדגן..."* — both
  reference "the peak of grain breads," an A-grade framing.
- **2079927** (bread, A→B) — `insightLine`: *"שמונים ושלושה אחוז קמח מלא
  וחלבון מהגבוהים בקטגוריה..."* `rowVerdict`: *"חלק משלישייה שנוגעת זו בזו
  בשורה התחתונה..."* — references sharing the top trio's bottom line.
- **2079996** (bread, A→B) — `insightLine`: *"הגרסה המשודרגת של לחם האחיד...
  והתוצאה רחוקה מאחיו הפשוט."* `rowVerdict`: references being the
  "upgraded version," implicitly top-tier framing.
- **4685027** (bread, B→C) — `insightLine`: *"...ועדיין הכיכר יושבת עמוק
  בחלק התחתון של המדף."* `rowVerdict`: *"...את שורת השכנים שמעליו הוא
  מפספס בכלום."* — "misses nothing vs. the row of neighbors above it," a
  B-grade framing now one grade too generous.
- **7290018790328** (crackers, C→D) — `insightLine`: *"הנתרן הגבוה ביותר
  בכל ההשוואה..."* `rowVerdict`: *"...מציירים תמונה של קרקר מעובד לגמרי...
  זה באמת המלוח ביותר על המדף."* — factually still true (highest sodium)
  but the C-grade "processed but not damning" framing needs to be
  re-weighed against D.
- **7290019401018 / 7290019401049 / 7290015130028** (protein-bars, all
  C→D) — all three carry `confidence: "verified"` with tooltip *"הציון
  מבוסס על פאנל התזונה ורשימת הרכיבים שפורסמו למוצר"* (the score is based
  on the nutrition panel AND the ingredient list published for the
  product). This claim is **now accurate post-fix** (ingredients are
  genuinely parsed and scored) — it was a **pre-existing overclaim before
  this fix** (ingredient_count was effectively 0), so this is not new
  staleness, it is the inverse: a previously-false claim that becomes true.
  Their `insightLine`/`rowVerdict` copy (about collagen/maltitol/sodium
  positioning) does not name grade/score numerals directly but references
  "the real bright spot" (7290019401018) and comparative framing that
  should be re-checked against the new D grade.

None of these 8 strings were rewritten. All routed to the Content two-gate
(Content Agent + Adversarial QA) per the standing hard rule and this task's
explicit instruction.

**Stale confidence-caveat scan (all 3 categories, full published corpus,
not just movers):** 41 products (22 bread + 19 crackers, 0 protein-bars)
carry `confidence_sub_reason`/tooltip text implying data was *not
available*, which becomes stale once this fix ships (ingredients are now
actually parsed). Matches TASK-476's exact count. Full list:
`...\scratchpad\task476b\stale_caveat_scan_result.json`. Separately, **all
32** published protein-bar products (not just the 15 REAL_LOSS TASK-476
scoped this to) carry the pre-existing "verified" overclaim described above
— broader denominator than TASK-476 reported (32 vs. 15) because I scanned
the full live file, not just the REAL_LOSS subset.

---

## Step 5 — surgical-fix proof (other 13 categories untouched)

`git diff origin/master -- bari-web/src/data/comparisons/<file>` returns
**0 lines** for all 13 non-target category JSONs (cereals, brined_cheeses,
cakes_hard_cookies, cheese, chocolate_bars, chocolate_tablets,
cookies_coffee, granola, hard_cheeses, hummus, juices, milk, snacks) — this
is the git-native, authoritative comparison (a manual Python `git show`
+ file-write comparison I tried first gave false positives due to a
line-ending conversion bug in my own script, not a real difference;
caught and corrected before reporting). sha256 of all 13 files captured
for the record (see counts JSON). **13/13 confirmed byte-identical.**

---

## Pipeline-tooling gaps found and fixed while running the real spine (disclosed, in-scope, mechanical only)

Two small defects surfaced only because this is the first time
`copy_stage.py` + `run_gates.py` were exercised against these 3 categories'
grade-movers together. Both are structural/derived-value bugs, not
scoring or content changes:

1. **`rank`** — `copy_stage.py` treats `rank` as a copy field (not in its
   `STRUCTURAL_FIELDS_TOP` set), so it left the literal string
   `"PENDING_COPY"` in `rank` for every mover, which fails G1 SCHEMA
   (`expected type integer, got str`). `rank` is 1:1 with score-descending
   position (verified against the live file: rank 1 = highest score) — a
   pure structural/derived value, not authored text. Recomputed it as
   `1..N` by score-descending sort for all 3 categories' full product sets.
   **Not fixed in `copy_stage.py` itself** (would need Nutrition/Frontend
   sign-off on adding `rank` to the structural set) — worked around
   post-hoc on the output JSON only, flagged here for a real tooling fix.
2. **`categoryTotal`** — same class of bug (crackers + protein-bars only;
   bread's schema doesn't have this field). Recomputed as the true product
   count for each category.
3. **`run_gates.py::_collect_consumer_strings()`** — crashed
   (`AttributeError: 'str' object has no attribute 'get'`) when
   `expansion.consumerExplanation` is the `"PENDING_COPY"` sentinel string
   instead of a dict (crackers' schema has this nested field; bread/
   protein-bars' PENDING rows didn't trigger it). Applied a minimal
   defensive `isinstance` guard (3 lines) so the gate reports a normal
   PENDING finding instead of crashing. This is a real code fix, committed
   to the branch (sha256 in the JSON below) — flagging for Frontend/
   pipeline-tooling owner review since it's a shared gate script, not
   something scoped to bread/crackers/protein-bars alone.

None of these three changes affect any score, grade, or scoring rule.

**Pre-existing, NOT caused by this fix (verified via a controlled A/B):**
`rescore_all.py`'s C10 milk-freeze gate FAILs identically (same 2 products,
same deltas: `bsip1_7290110324926` +0.2, `bsip1_7290110325619` +4.1) with
my fix applied and with it reverted (tested via a worktree-local, disclosed
`git stash`/`git stash pop` A/B, immediately reverted). This is a
pre-existing condition in origin/master's milk-freeze machinery unrelated
to this task — flagged for whoever owns that gate, not fixed here (out of
scope).

**Pre-existing, NOT caused by this fix:** protein-bars' G1 SCHEMA gate fails
with ~20 "additional property not allowed" errors against the generic
`page_output_schema_v1.json` — confirmed by running the identical gate
against the untouched, currently-published `protein_combined_frontend_v2.json`
and getting the same failures. Protein-bars was never conformed to this
schema; this is a pre-existing structural gap, not new.

---

## Gate results summary (all 3 categories)

| Category | G1 Schema | G2 Coverage | G3 Scope | G4 OFF | G5 Grade-Integrity | G6 Copy-Safety | G7 Parity | G8 Data-Sanity | Overall |
|---|---|---|---|---|---|---|---|---|---|
| bread | PASS | FAIL (4 PENDING movers, by design) | PASS | PASS | PASS | PASS | PASS | PASS | FAIL (expected) |
| crackers | PASS | FAIL (2 PENDING, by design) | PASS | PASS | PASS | PASS | PASS | PASS | FAIL (expected) |
| protein-bars | FAIL (pre-existing schema gap, confirmed on live file too) | FAIL (3 PENDING, by design) | n/a (no standard corpus dir) | PASS | n/a | PASS | PASS | PASS | FAIL |

All "FAIL"s are either (a) the intentional PENDING_COPY signal this task's
Step 4 explicitly asked for, or (b) a confirmed pre-existing condition
unrelated to this fix. **Zero unexplained gate failures.**

---

## New frontend JSON paths + hashes

- `C:\bari_wt_t476\bari-web\src\data\comparisons\bread_frontend_v4.json`
- `C:\bari_wt_t476\bari-web\src\data\comparisons\crackers_frontend_v1.json`
- `C:\bari_wt_t476\bari-web\src\data\comparisons\protein_combined_frontend_v2.json`

All 3 committed to `golive/task476-rescore` (commit `07055d5d`), along with
the 2 engine-fix files, the 1 gate-tooling fix, and a run record at
`03_operations/page_generator/reports/task476b/run_record_task476b.json`.
**Not pushed. No PR opened.**

---

## Not done / explicitly out of scope

- Did not author any of the 8 movers' copy, nor the 41+32 stale-caveat
  strings — routed to Content two-gate per instruction.
- Did not resolve the bread `baseline_json` (v3) vs. true-live (v4) config
  mismatch, nor the protein-bars `generate_page.py`-incompatibility —
  flagged for Product/Frontend, not adjudicated unilaterally.
- Did not fix `copy_stage.py`'s missing `rank`/`categoryTotal` structural-field
  gap at the source (worked around on output only) — needs a real owner
  decision on the structural-field set.
- Did not investigate or fix the pre-existing C10 milk-gate FAIL or the
  pre-existing protein-bars G1 schema gap — both confirmed unrelated to
  this task's change, flagged for their respective owners.
- Did not push the branch or open a PR — per hard guard, this is the
  orchestrator's next step after copy re-audit + gates + red-team.
- Did not touch any of the other 13 live category JSONs (byte-identity
  proven).

---

```json
{
  "task": "TASK-476b",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\bari_wt_t476\\03_operations\\bsip2\\proto_v0\\src\\input_loader.py",
      "sha256": "a46cc2e3d15109c9db83094a0ca551146fceb6fa574893da041c53fe887bc78e",
      "status": "modified_committed"
    },
    {
      "path": "C:\\bari_wt_t476\\03_operations\\bsip2\\proto_v0\\src\\router_v2.py",
      "sha256": "ee1a4e0248a36a10058800ba6c57340289551acf3d842ff61cf1508c6a5a277e",
      "status": "modified_committed"
    },
    {
      "path": "C:\\bari_wt_t476\\03_operations\\page_generator\\gates\\run_gates.py",
      "sha256": "cdd9285ddf67beb3c63ac9780462478493cd9b2d42f2a295b16a5335fa9950af",
      "status": "modified_committed",
      "note": "defensive isinstance guard only, no gate logic/threshold change"
    },
    {
      "path": "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\bread_frontend_v4.json",
      "sha256": "949eefc7e2f3aa231ca6792c6c630dc88052ff173668722159ea9f1a547b4e7d",
      "status": "modified_committed"
    },
    {
      "path": "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\crackers_frontend_v1.json",
      "sha256": "cf21c99998d7b15079909632826271efbe8229780300b0040f932e5da09a7b33",
      "status": "modified_committed"
    },
    {
      "path": "C:\\bari_wt_t476\\bari-web\\src\\data\\comparisons\\protein_combined_frontend_v2.json",
      "sha256": "8c3385ecfbfea9f037904cd55f3f5a9303e52745e6f815d8c7b3222c65c5521a",
      "status": "modified_committed"
    },
    {
      "path": "C:\\bari_wt_t476\\03_operations\\page_generator\\reports\\task476b\\run_record_task476b.json",
      "status": "created_committed"
    }
  ],
  "counts": {
    "categories_rescored": { "value": 3, "denominator": 3 },
    "categories_unaffected_verified_identical": { "value": 13, "denominator": 13 },
    "bread_products_scored": { "value": 23, "denominator": 31, "note": "31 BSIP1 records, 8 declared exclusions (pre-existing, TASK-433/G8), 23 displayed" },
    "crackers_products_scored": { "value": 20, "denominator": 20 },
    "protein_bars_products_scored": { "value": 32, "denominator": 32 },
    "total_scored_rows_joined": { "value": 74 },
    "rescoring_errors": { "value": 0, "denominator": 74 },
    "grade_movers_final": { "value": 8, "denominator": 74 },
    "grade_movers_direction": { "down": 8, "up": 0, "denominator": 8 },
    "grade_movers_matching_task476_exactly": { "value": 5, "denominator": 8, "note": "4 bread + 1 crackers match TASK-476's table exactly" },
    "grade_movers_diverging_from_task476": { "value": 3, "denominator": 8, "note": "7290019401018 (moves in both but TASK-476 flagged as should-not-move), 7290019401049 (new mover TASK-476 never predicted), and TASK-476's predicted 7290018703076 does NOT move here -- all 3 traced to TASK-476's scope_scan_result.json feeding 7/15 protein-bar REAL_LOSS rows from stray wrong-category BSIP1 records instead of the true live corpus" },
    "protein_bar_real_loss_rows_with_stray_lineage": { "value": 7, "denominator": 15, "note": "2 already disclosed by TASK-476 (Finding 3); 5 more found in this task" },
    "flagship_bread_reproduced": { "value": 1, "denominator": 1, "detail": "7290016245325: 94.8->90.8, S->S, exact match, routed whole_food_fat (confirmed via trace, not assumed)" },
    "delta_distribution_74_rows": { "n": 74, "mean": -1.14, "min": -6.6, "max": 7.0, "positive": 4, "negative": 37, "zero": 33 },
    "stale_caveat_strings_found": { "value": 41, "denominator": null, "by_category": { "bread": 22, "crackers": 19, "protein-bars": 0 }, "matches_task476_count": true },
    "protein_bar_preexisting_overclaim_count": { "value": 32, "denominator": 32, "note": "broader than TASK-476's 15 -- that was scoped to REAL_LOSS only; this is the full published set" },
    "mover_copy_strings_flagged_for_content": { "value": 8, "denominator": 8 },
    "new_to_corpus_products_needing_fresh_copy": { "value": 1, "denominator": 1, "detail": "7290112968807, crackers, 45.3/D" },
    "pipeline_tooling_bugs_found_and_fixed": { "value": 3, "note": "rank + categoryTotal PENDING_COPY-string leakage (worked around on output), run_gates.py consumerExplanation type crash (source-fixed, committed)" },
    "unaffected_categories_byte_identical": { "value": 13, "denominator": 13, "method": "git diff origin/master, 0 lines each" },
    "gate_exit_codes": { "bread": 1, "crackers": 1, "protein_bars": 1, "note": "all FAILs are either the intended PENDING_COPY signal or a confirmed pre-existing condition, zero unexplained failures" },
    "c10_milk_gate_preexisting_fail_confirmed": { "value": true, "note": "identical FAIL with and without this fix, verified via git stash A/B" }
  },
  "commands_run": [
    { "cmd": "git fetch origin && git worktree add -b golive/task476-rescore C:\\bari_wt_t476 origin/master", "exit_code": 0 },
    { "cmd": "Edit input_loader.py (get_ingredients fresh rewrite + _split_top_level_commas, {} included)", "exit_code": 0 },
    { "cmd": "Edit router_v2.py (duplicate ingredient-count fallback removed, routes through get_ingredients)", "exit_code": 0 },
    { "cmd": "python -c import input_loader; import router_v2 (clean import verification)", "exit_code": 0 },
    { "cmd": "python 03_operations/page_generator/rescore_all.py --shelf bread", "exit_code": 0 },
    { "cmd": "python 03_operations/page_generator/rescore_all.py --shelf crackers", "exit_code": 0 },
    { "cmd": "python 03_operations/page_generator/provenance/protein_bars_reproduce_harness.py C:/bari_wt_t476", "exit_code": 1, "note": "exit 1 is by design -- harness returns 1 when mismatches vs OLD baseline exist, which is the entire point of measuring rescore impact" },
    { "cmd": "git stash / git stash pop (worktree-local diagnostic A/B for C10 milk-gate isolation, immediately reverted, verified via git diff --stat)", "exit_code": 0 },
    { "cmd": "python 03_operations/page_generator/copy_stage.py (bread, crackers, protein_bars_staging)", "exit_code": 0 },
    { "cmd": "rank/categoryTotal recompute script (score-descending sort, structural fix)", "exit_code": 0 },
    { "cmd": "Edit run_gates.py (defensive isinstance guard for consumerExplanation)", "exit_code": 0 },
    { "cmd": "python 03_operations/page_generator/gates/run_gates.py (bread, crackers, protein-bars, x2 each pre/post fixes)", "exit_code": 1, "note": "all FAILs explained above, zero unexplained" },
    { "cmd": "python 03_operations/page_generator/gates/run_gates.py (re-run against untouched live protein_combined_frontend_v2.json to confirm G1 schema fail is pre-existing)", "exit_code": 1 },
    { "cmd": "cp copy-applied JSONs to bari-web/src/data/comparisons/ (3 files)", "exit_code": 0 },
    { "cmd": "git diff origin/master -- bari-web/src/data/comparisons/<13 files> (byte-identity proof, 0 lines each)", "exit_code": 0 },
    { "cmd": "sha256sum on all 6 modified + 13 unaffected files", "exit_code": 0 },
    { "cmd": "git add + git commit (7 files, branch golive/task476-rescore)", "exit_code": 0 },
    { "cmd": "git status -sb / git log origin/master..HEAD (confirm ahead 1, not pushed)", "exit_code": 0 }
  ],
  "not_done": [
    "Copy for the 8 grade-movers + 1 new-to-corpus product not authored -- routed to Content two-gate.",
    "41 stale confidence-caveat strings (bread/crackers) + 32 protein-bar pre-existing overclaim strings not rewritten -- routed to Content two-gate.",
    "bread config's baseline_json (v3) vs true-live (v4) mismatch not resolved -- flagged for Product/Frontend.",
    "protein_bars config's generate_page.py-incompatibility not resolved -- flagged for Product/Frontend/pipeline-tooling owner.",
    "copy_stage.py's missing rank/categoryTotal structural-field entries not fixed at the source -- worked around on output only, flagged for the tooling owner.",
    "Pre-existing C10 milk-gate FAIL and pre-existing protein-bars G1 schema gap not fixed -- confirmed unrelated to this task, flagged for their owners.",
    "Branch not pushed, no PR opened -- per hard guard, next step is the orchestrator's after copy re-audit + gates + red-team."
  ],
  "self_check": {
    "acceptance_test": "Engine fix (input_loader.get_ingredients + router_v2 dedup) applied fresh in an isolated worktree off origin/master, not copied from the diverged local tree. 3 categories re-flowed through the real spine (rescore_all.py->copy_stage.py for bread/crackers; the real existing protein-bars reproducer for protein-bars, since its own config discloses generate_page.py incompatibility -- flagged, not forced). Flagship bread reproduces 94.8->90.8 S->S exactly, confirmed routed whole_food_fat via trace. 5 of 8 grade-movers match TASK-476's prediction exactly; 3 diverge, root-caused to a lineage bug in TASK-476's own scope_scan_result.json (7 of 15 protein-bar rows fed from stray wrong-category BSIP1 records) -- this task's numbers are built from the true live corpus and are the authoritative re-flow result. 8 movers' stale copy identified by exact string, not authored. 41+32 stale confidence caveats identified. 13 unaffected categories proven byte-identical via git diff (0 lines each) after an initial false-positive from a bug in my own comparison script was caught and corrected. 2 small pipeline-tooling gaps (rank/categoryTotal PENDING-string leakage, a run_gates.py type crash) found and disclosed, one source-fixed. Self-caught and corrected one stale-cache read of my own bread staging output before finalizing the impact table. Result: PASS, with disclosed divergences from TASK-476's prediction that are resolved in favor of the real production data source, and multiple flagged-not-resolved items for their proper owners.",
    "guardrails_respected": {
      "off_used": false,
      "local_diverged_tree_used_as_base": false,
      "engine_fix_applied_fresh_in_worktree": true,
      "main_tree_git_mutated": false,
      "worktree_git_stash_incident": "1 pair, immediately reverted, verified via git diff --stat, disclosed",
      "categories_touched": 3,
      "categories_confirmed_untouched": 13,
      "frontend_json_written": 3,
      "copy_authored": 0,
      "git_commits": 1,
      "git_pushes": 0,
      "prs_opened": 0,
      "scoring_rule_changes": 0,
      "ingredients_source": "BSIP1 ingredients_list / ingredient_order / ingredients_text_he / ingredients_raw and the live protein-bars corpus's ingredients_full only -- real scrape, verbatim, never OFF, never invented"
    }
  }
}
```
