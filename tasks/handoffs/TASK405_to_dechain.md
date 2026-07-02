# Handoff → de-chain (TASK-395) chat — Finding 1 (ingredient pollution) DONE

**From:** orchestrator (TASK-405) · **Date:** 2026-06-26 · **You can unblock now.**

## TL;DR
Finding 1 (the hard blocker you were holding on) is cleaned. **No published score moved.**
Re-run your reproducibility map / re-shadow on the cleaned BSIP1 whenever you're ready.

## What I found (important — changes the premise)
- The sanitizer CODE (`03_operations/bsip2/proto_v0/src/signal_extractor.py :: sanitize_ingredient_list`
  + `_truncate_glued_bleed`) is **already correct**: it truncates at the `ערכים תזונתיים` marker and
  yields true counts (קוטג' 7290014758681 → **3**: חלב, מלח, תוסף תזונה: סידן). The "parses as 6" you
  measured is `ingredient_count_raw`; the old `run_cheese_002` trace showing clean_count=2 was a STALE
  earlier sanitizer version.
- The real defect: the **stored BSIP1 source fields** (`ingredients_list` / `ingredients_text_he` /
  `ingredients_raw` / `ingredient_order`) still hold the raw run-on blob at rest. The BSIP2 engine
  sanitizes at runtime (so **scores are unaffected**), but **raw-text consumers** — the additive
  detector (`re.search` over `ingredients_text_he`) and the matrix probe — read the stored fields
  directly and get fooled. That's the exposure.

## What I did (score-neutral data hygiene)
- Ran the proven `sanitize_ingredient_list` over the stored BSIP1 fields corpus-wide; wrote back the
  cleaned list + rebuilt text/raw/order. Every changed file carries a **reversible `_task405_clean`
  audit block** (original fields + dropped/truncated delta).
- Scripts: `03_operations/bsip1/_task405_detect.py` (read-only) · `_task405_clean.py` (`--apply`).
- **Result: distinct-product pollution 28.6% → 14.7%; 473 files cleaned across 25 run dirs.**
- All 8 verification barcodes now parse true: 7290014758681 / 4127077 / 4127329 / 4127336 / 41445 /
  41452 → **3**; 2824183 / 2824640 → **5**.

## Manifest (what changed — for your reproducibility map)
- Full per-file list: **`03_operations/bsip1/task405_reports/clean_report.json`** (`per_dir` + every
  cleaned file + barcode + raw→clean counts).
- Changed files are identifiable by the `_task405_clean` key: `grep -rl _task405_clean 03_operations/bsip1`.
- **NOT committed** (the shared tree carries unrelated bread-sentinel work + ~880 dirty files; a clean
  commit would tangle them). The clean is live in the working tree on `task-374-toms-voice`. If you need
  it committed in isolation, the audit key isolates exactly my files — say the word.

## Excluded by design
- **maadanim (116) + yogurt (135)** — wiped/dead categories; cleaning them is pointless churn. They are
  the bulk of the 14.7% residual.

## ⚠️ 5 files FLAGGED, NOT auto-cleaned (need re-scrape — never imputed, no OFF)
Single-item lists whose ONLY item is entirely nutrition-panel bleed (`clean_count==0`) — i.e. the real
ingredient list was never scraped:
- `7297488098688` (cereals; in run_cereals_002/006/008)
- `7296073733324` and `7296073733331` (hummus; run_hummus_001)
These need a re-scrape or human read. I left them untouched.

---

# Finding 2 (provenance / TASK-406) — orchestrator side DONE; round-trip verification is yours

**Reframe:** provenance was not lost — every shelf config (`03_operations/page_generator/configs/*.json`)
already records the per-category `scoring/flags` (incl `BARI_D4_SCORE_V1`), `scoring/bsip1_dir`,
`run_products_dir`, and `baseline_json`. It just wasn't persisted per published file, and one flag was unmanaged.

**What I persisted / fixed:**
1. **Per-published-file provenance manifest:** `03_operations/page_generator/provenance/provenance_manifest.json`
   — 15 live served files, each with resolved run_id (recovered from `run_products_dir` even where
   `_meta.run_id` is NULL), full flag vector incl D4, backing source + existence, engine head `b905ec9b4`,
   D4 patch commit `361748722`, per-file status. Builder `provenance/_build_manifest.py` (read-only).
   **7/15 are config-bound + source-present + flagged = REPRODUCIBLE_PENDING_RESHADOW** (your re-shadow
   confirms the hash round-trip). The other 8 carry explicit gaps below.
2. **Flag-management gap FIXED:** added `BARI_D4_SCORE_V1` to `MANAGED_BARI_VARS` in `rescore_all.py`
   + `gates/baseline_verify.py` (it was already in `monotonicity_invariant.py` — the inconsistency WAS
   the gap). D4 is now snapshotted/restored on managed runs.

**Gaps for you to resolve during re-shadow (I did NOT mutate configs/_meta — to keep your comparison
baseline clean; the manifest gives you the exact source + flag vector per file):**
- NULL `_meta.run_id` but resolvable from config: bread_v3, cheese_v4, chocolate_bars_v1,
  chocolate_tablets_v1, snacks_v5 (manifest carries `run_id_resolved`).
- Config→served mismatch (config baseline = v1, route serves v2): granola_v2, protein_combined_v2 —
  served files carry their own `_meta.run_id` (run_granola_task385_25g, protein_bars_task365_rescore),
  built by ad-hoc task runs outside the config. Re-point config or rebuild through it.
- Stale `bsip1_dir`: cookies_coffee config path missing.

**Yours:** the round-trip "every score re-derives to its committed hash" verification (you have the
re-shadow harness + worktrees). The manifest hands you the exact source + flag vector per file.

# Finding 3 (TASK-407, חומר משמר lexicon spelling) — small nutrition-lane fix, queued, not started.
You flagged it "likely out of your scope"; it's registered to nutrition-agent.
