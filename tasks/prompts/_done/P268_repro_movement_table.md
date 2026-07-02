# P268 / TASK-418 clean-vs-baseline movement table (route: C1-CURSOR)

## 0. Repo / environment
- Repo: `C:\Bari` (monorepo). **Work in an ISOLATED git worktree ONLY** — create your own off `master`
  (HEAD `7733065a` or later): `git worktree add C:/bari_p268 -b p268/movement-table master`. Do ALL work
  there. Do NOT run any pipeline/git-stash/checkout in the main `C:\Bari` tree (a cloud lane that touches the
  main tree has wiped it before — hard rule). Single synchronous worker, no detached background pipelines.
- Python scoring lives at `03_operations/bsip2/proto_v0/src`. You have a PROVEN reproduction harness:
  `03_operations/page_generator/provenance/hard_cheeses_reproduce_harness.py` and its write-up
  `hard_cheeses_canonical_invocation_v1.md` (TASK-429). READ both first.

## 1. TASK to read
Read `tasks/TASK-418.md` (esp. the 2026-07-01 updates) and `tasks/TASK-429.md` (the pinned canonical
invocation). This job is the score-neutral VERIFICATION that TASK-418's owner-approved clean+refresh was
blocked on.

## 2. Objective
Produce ONE verified **clean-vs-baseline movement table** for the owner-approved refresh scope. For every
LIVE-PUBLISHED product in these 4 categories whose bsip1 record carries the ingredient-pollution signature,
report what its score/grade becomes when the pollution is removed, diffed against the pinned baseline
(= current published). This is ANALYSIS ONLY. You deploy NOTHING and change NO published score.

Scope categories + baselines (published = baseline):
- `hard_cheeses` → `bari-web/src/data/comparisons/hard_cheeses_frontend_v4.json` (corpus `02_products/hard_cheeses/bsip1_task412`, canonical invocation per TASK-429 doc)
- `juices`       → `.../juices_frontend_v3.json`
- `cheese`       → `.../cheese_frontend_v4.json`
- `cereals`      → `.../cereals_frontend_v2.json`

## 3. Method (deterministic; follow exactly)
1. **Per category, establish the baseline invocation and PROVE it reproduces published FIRST (gate).**
   Use the category config `03_operations/page_generator/configs/<cat>.json` (`scoring.flags`, `scoring.shelf_rel`,
   `corpus_dirs`). For hard_cheeses use the TASK-429 canonical exactly (corpus=`bsip1_task412`, the 7-flag
   vector, EV-090 shelf-stats, loader accepting `file_type∈{product,bsip1_enriched}`). If a category's config
   does NOT reproduce its published scores (repro < 100%), resolve its corpus the way TASK-429 did — find the
   `bsip1_*` dir that covers ALL published barcodes and byte-reproduces — and DOCUMENT which dir. **Do not
   proceed to cleaning a category until its baseline reproduces (drift 0 on the un-cleaned corpus). If it
   cannot be made to reproduce, report that category as BASELINE-NOT-REPRODUCIBLE and skip its cleaning.**
2. **Define the clean rule (deterministic, no invention).** A trailing `ingredients_list` element is
   NON-INGREDIENT and must be dropped if it matches the pollution signature:
   - retailer disclaimer lines (e.g. contains `אין להסתמך על הפירוט`, `יתכנו טעויות`, `יש לקרוא את המופיע על גבי`,
     `להמחשה בלבד`), and
   - nutrition-panel bleed (contains `ערכים תזונתיים`, or `קל`/`אנרגיה`+`חלבונים`+`פחמימות`+`שומנים` runs, or
     `כולסטרול`/`נתרן`/`שומן רווי`+numeric grams). When bleed is FUSED onto a real ingredient (e.g.
     `חומר משמר (E-202). מכיל חלב ערכים תזונתיים 100 גרם …`), keep only the real ingredient head
     (`חומר משמר (E-202)`) and strip from the nutrition/`מכיל`-panel onward.
   Recompute `ingredient_count` = len(cleaned list). Apply this to a COPY in your worktree only. Do NOT invent,
   substitute, or source any ingredient/nutrition value from anywhere (OFF is BANNED — TASK-238 — any OFF use
   or dependency is a launch blocker; if a field isn't in the direct scrape, it stays as-is/NULL).
3. **Re-score** each cleaned record through the SAME canonical invocation used for its baseline (same flags,
   same shelf-stats, same engine at HEAD). Reload order: `nova_proxy → signal_extractor → score_engine`.
4. **Diff** cleaned vs baseline per product: `delta = clean_score − published_score`, grade move (Y/N),
   before/after `ingredient_count`. Classify each moved product:
   - `corpus-clean-move` — moved only because pollution was removed (score change → tripwire, owner-gated),
   - `flag-only-neutral` — baseline mismatch was a config-flag gap already fixed (no real move),
   - `no-change` — |delta| ≤ 0.1.

## 4. Boundaries / guards
- **Isolated worktree only. Read-only on everything published**: do NOT write to any file under
  `bari-web/src/data/comparisons/`, any `configs/*.json`, or any live corpus record in the main tree. Your
  cleaned records + scripts live in your worktree and are NOT merged.
- **OFF-ban absolute** (TASK-238): no Open Food Facts anywhere, any field, any fallback.
- **No published-score change, no deploy, no gate-regeneration.** You output a TABLE, not a refresh.
- Do NOT close the task. Propose `RETURNED`.

## 5. Return format
Return markdown:
- **Per-category baseline gate:** repro N/N, drift 0? (Y/N), corpus dir used, invocation (flags+shelf).
- **Movement table** (one row per pollution-flagged live product): `category | barcode | name | pub_score/grade |
  clean_score/grade | delta | grade_move | ing_count before→after | classification`.
- **Totals:** # products moved, # grade moves, direction (all up?), per-category counts, and the exact clean
  rule you applied (with the token list).
- **Reproducibility:** the script(s) you used (paths in your worktree) so the orchestrator can re-run and verify.
- Any category that is BASELINE-NOT-REPRODUCIBLE, named, with why.
- End with the machine-readable return contract (`01_framework/operations/return_contract_v1.md`): artifacts
  with sha256, counts with named denominators, and a distribution marker on the full-set claim.

**Remember:** the entire point is a TRUSTWORTHY table. If your env cannot reproduce a baseline (drift 0),
say so and stop for that category — do not report cleaned numbers off an unverified baseline (that failure
mode already burned this task twice).
