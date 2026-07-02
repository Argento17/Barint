# Handoff → prevention / de-chain chat — Step 1: provenance bindings + harness fix

**From:** orchestrator (corpus traceability program) · **Date:** 2026-06-26
**Your lane:** the **"traceable"** plumbing (config bindings + the reproduce harness).
**My lane (separate, in flight):** Steps 2–5 — commit the TASK-405 clean, re-derive on the
corrected+clean corpus, two-gate copy on grade-movers, validate, stage for deploy.

---

## Why this exists — the real diagnosis (master-native, not the stale branch)

The earlier "175 untraceable / NO_CONFIG_BOUND" screenshot was **partly a harness false-negative**
(granola reproduces 22/22; cookies 118/119 — the harness keyed on `scoring.bsip1_dir`, which is
`null` by design on multi-source shelves, instead of `corpus_dirs`).

But re-running the round-trip **natively against `origin/master`** (master configs + master corpus +
master engine — i.e. what is actually live) confirms **real untraceability** in 7 categories. This is
NOT lost data and NOT my clean (the clean isn't in master). It is **wrong/stale config bindings +
engine drift since publish.**

### Master-native reproduce table (the true live baseline)
| category | reproduce ±0.1 | drift | nocorpus | grade-moves | max drift | read |
|---|---|---|---|---|---|---|
| brined_cheeses | **36/36** | 0 | 0 | 0 | 0.0 | clean-traceable |
| hummus | **57/57** | 0 | 0 | 0 | 0.0 | clean-traceable |
| cookies_coffee | **118/119** | 1 | 0 | 0 | 1.3 | clean-traceable |
| granola | **21/22** | 1 | 0 | 0 | 1.5 | clean-traceable |
| juices | **16/17** | 1 | 0 | 0 | 2.1 | clean-traceable |
| cheese | 43/53 | 10 | 0 | 7 | 4.0 | engine-drift |
| milk | 15/18 | 3 | 0 | 1 | 2.0 | engine-drift |
| cereals | 12/20 | 8 | 0 | 1 | 5.0 | engine-drift |
| bread | 12/29 | 17 | 0 | 5 | 3.3 | engine-drift / binding |
| hard_cheeses | 15/23 | 8 | 0 | 0 | 2.1 | **stale baseline file (v2≠v3)** |
| cakes | 11/63 | 52 | 0 | 1 | 8.0 | **binding / engine-drift** |
| **snacks** | **0/21** | 12 | 9 | 8 | 29.2 | **WRONG CORPUS bound** |

Evidence JSON (per-product drift + grade detail): `03_operations/page_generator/provenance/_reproduce_MASTER_baseline.json`
Harness (parametrized `REPO` arg for worktree runs): `03_operations/page_generator/provenance/_reproduce_diag.py`
Run it against any worktree: `python _reproduce_diag.py <WORKTREE_ROOT>`

---

## Your asks (Step 1)

### 1. Fix the two confirmed binding bugs (highest value)
- **snacks → 0/21 reproduce, 9 nocorpus.** `configs/snacks.json` binds `corpus_dirs` to a
  `score_bars_task362_...` dir — that did **not** produce the live snacks_frontend_v5 scores. Find the
  run that actually scored snacks_v5, re-point `corpus_dirs` + `run_products_dir`, persist `run_id`.
  Until this is right I **cannot** re-derive snacks.
- **hard_cheeses → audited against the wrong file.** `configs/hard_cheeses.json` has
  `baseline_json = hard_cheeses_frontend_v2.json`, but master serves **v3** (`hard_cheeses_frontend_v3.json`).
  Re-point `baseline_json` to the served file and re-check reproduce — the 15/23 is likely a v2/v3 artifact.

### 2. Per-category provenance root-cause (the rest of the non-reproducers)
For bread, cakes, cereals, cheese, milk: classify each non-reproducer as
**(a) engine-drift-since-publish** (small ≤~3pt deltas — expected; resolved by the re-derive in my lane),
**(b) wrong corpus/flag binding** (your fix), or **(c) stale baseline file** (your fix). Persist per
file: resolved `run_id`, corpus dir, flag vector, engine SHA. The `provenance_manifest.json` builder
(`03_operations/page_generator/provenance/_build_manifest.py`) is the place to record it.

### 3. Fix the reproduce harness (so its verdicts can be trusted)
The harness that produced the original screenshot must:
- **fall back to `corpus_dirs` / `run_products_dir`** when `scoring.bsip1_dir` is null (else it false-flags
  every multi-source shelf as "bsip1_dir missing" — that's the cookies/granola false UNTRACEABLE);
- **match served files by route, not by `_meta.run_id`** (null/ad-hoc run_ids caused the "NO_CONFIG_BOUND"
  false-negatives on granola + protein_bars, both of which DO have configs).

---

## Coordination / dependency
- I will **re-derive now** the categories whose bindings are already correct (cheese, milk, cereals,
  bread, cakes once corpus confirmed, choc-bars/tablets, + the 5 already-traceable need nothing).
- **snacks + hard_cheeses are BLOCKED on your binding fixes** — I won't re-derive them until you re-point
  the corpus/baseline. Flag me when each is fixed.
- **protein_bars** (ad-hoc lens, reproduces 3/16 via standard engine): I'm taking it in my lane —
  either rebind onto the standard BSIP pipeline or pin `batch_run_protein_bars_task365.py` + the recorded
  `_corpus_sha256` as the canonical reproducer. Will confirm which.

## UPDATE 2026-06-26 (post Steps 2-5 re-derive) — two items back to you

**Steps 2-5 are DONE + orchestrator-verified** for 12 categories (worktree `task409`, commits
`dcac4bf4f` clean → `120ff8f0c` re-derive; independent re-score of cheese/bread/milk vs staged = 0
mismatch; OFF=0; published==reproduce). 13 grade-movers (all upgrades) are in the content two-gate now.

**hard_cheeses — DE-ESCALATED from owner-tripwire, it's a binding-recovery (your lane):**
- The route on **master imports `hard_cheeses_frontend_v3.json`** (live); the **config is still bound to
  `v2`** (`baseline_json=hard_cheeses_frontend_v2.json`, `run_hc_redlabel_v2_001`, scores max 77.8 / min 37.0).
  v3 is a **separate rebuild** (the Tom's-Voice "own v3 rebuild") and isn't on the feature branch at all.
- So the "71→39 not a drift" = v2-config-flags re-scored against v3's published numbers. **Not a scoring
  failure — a stale binding.** The owner has already authorized every score move for this program, so this
  is NOT an owner decision; it needs **v3's provenance recovered** (which run/flags/corpus built v3 — it may
  be ad-hoc like protein_bars), then bind the config to v3. **Then I re-derive hard_cheeses on the clean
  corpus** like the other 12. Please recover + bind v3; flag me when done.

**snacks — your binding fix confirmed; one constraint for my re-derive:**
- Your working-tree fix (snacks 18/21) is committed (`c38bc6fad`) but lives on the feature branch, **not on
  master** — the `task409` worktree is off master so it doesn't have it yet. When I re-derive snacks I'll
  pull your fixed `snacks.json` in. Per your flag, the re-derive will read **`corpus_dirs`, NOT the
  `run_products_dir` bsip2 traces** (broken/stale layout). Confirm the corpus_dirs binding is the one that
  produced snacks_frontend_v5.

## The clean (FYI — my lane, but affects your re-shadow)
TASK-405 ingredient clean is **NOT score-neutral** (correcting my earlier handoff): removing
nutrition-panel bleed stops false additive/processing penalties → scores rise (proven: restore original
text → published score returns to the cent; cleaned text scores up to +5.3 on cheese). When you re-shadow,
expect cleaned-corpus scores to sit **above** the dirty-published ones in cleaned categories. Owner has
authorized every score movement; the target end-state is published == reproduce on the **clean** corpus.

## STAND-DOWN 2026-06-26 — handoff CLOSED, orchestrator owns all lanes
Owner: "you own all lanes now, no other chats." De-chain/prevention lane stood down.
- **snacks** binding fix (c38bc6fad) → re-derived + DEPLOYED (TASK-413, master `8761cf863`): 19/21 reproduce, 0 grade moves, 3 _task405_clean upgrades. 14th clean-traceable category. CLOSED.
- **hard_cheeses** → absorbed into the full rework (TASK-412). Key finding: the HC sat-fat machinery is NOT on master (only on hc380/feature) — a merge-to-master is required. Owner chose Candidate A (REDLABEL=on de-anchor). Engine merge + corpus augment in flight.
- **harness** (corpus_dirs fallback / route-match) → orchestrator's `_reproduce_diag.py` already implements it; provenance_manifest persisted (TASK-406). No further de-chain action.
The 7 "engine-drift" untraceable categories were resolved by the TASK-409 clean re-derive + deploy (646da02c9): live now == reproduce on the clean corpus. The separate TASK-395 de-chain-ENGINE program remains on its own track (not part of this handoff).
