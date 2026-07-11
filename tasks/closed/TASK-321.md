---
id: TASK-321
title: Zero-different-category conformance sweep — every live category on the uniform spine path, or deleted
owner: orchestrator
status: CLOSED
closed_at: 2026-07-11
close_reason: "DONE-IN-FACT - task body declares SWEEP COMPLETE 2026-06-18; conformance.py exists (asserted); 16/16 re-flow verified in later spine work (board 2026-06-18). Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: HIGH
created_at: 2026-06-17
depends_on: [TASK-314]
blocks: []
category_id: null
summary: >
  Owner hard goal 2026-06-17: after this sweep no live /hashvaot category may be structurally 'different' — each conforms to the uniform generate_page+render_fields+spine_flip path or is DELETED entirely (page+route). Project-wide (not just the 5 wiped shelves): also catches yogurts (still live), duplicate routes (bread-comparison, cakes-hard-cookies), vegetable-spreads lens, and milk (frozen flagship — owner-ruling pending, the one no-delete carve-out). Each go-live/delete owner-gated.
---

# TASK-321 — Zero-different-category conformance sweep — every live category on the uniform spine path, or deleted

## Binding goal (owner, 2026-06-17)
After the sweep, NO live `/hashvaot/*` category is structurally "different." Each conforms to the uniform path
(`generate_page` + `render_fields` → `copy_stage` → gates → `spine_flip`), **or is DELETED entirely (page+route).**
No third option; delete is the default fallback. Memory: `zero_different_category_mandate`. Every go-live AND every
deletion is owner-gated (consumer-facing). Supersedes the "milk = blessed exception" softness.

## Live-route disposition (20 routes audited on origin/master 2026-06-17)
- **CONFORMING (9):** breakfast-cereals, granola, juices, hummus, hard-cheeses, brined-cheeses, cakes, cookies-coffee, snacks.
- **DELETE — duplicate/legacy (2):** bread-comparison, cakes-hard-cookies.
- **CONFORM-OR-DELETE — stale/no-config:** bread (real frozen provenance → conform), cheese, maadanim, yogurts (still live, v4 rejected).
- **BORDERLINE:** vegetable-spreads (bespoke lens UI → conform to standard layout, recommended), snack-bars (A–E + frozen no-A ceiling → keep, audit).

## Owner decisions logged 2026-06-17 (updated)
- **DELETE batch (6):** butter, salty-snacks, **maadanim**, **vegetable-spreads**, bread-comparison, cakes-hard-cookies.
  (maadanim + vegetable-spreads added to deletion by owner; veg-spreads lens dropped — hummus page unaffected, it's its own route.)
- **REBUILD:** cheese, yogurts (real-barcoded direct-scrape run → conform; if a clean run can't be made one-shot → delete per the rule).
- **CONFORM (clean data exists):** bread (real frozen provenance `real_bread_retail_003_v1`).
- **Butter + salty-snacks takedown reason:** possible OFF/fabricated data live = standing hard-rule breach. Bundle into Wave-0 PR.
- **MILK → rescore AUTHORIZED by owner 2026-06-17** ("I don't mind the rescoring; expect ~same results from the new engine").
  Rebuild milk from its BSIP0 direct-scrape corpus through the uniform pipeline (BSIP0→BSIP1→BSIP2 blessed engine→generate_page→spine).
  This **lifts the CNO milk freeze** (`run_005_headpin` 85/A) — formally supersede that ruling once the rebuild ships. Orchestrator
  still runs a PREVIEW first (old 85/A vs new, all products + grade flips) and surfaces the diff before the page goes live; go-live merge stays owner-gated.

## Waves
- **Wave 0 (prereq):** clean `/hashvaot` index PR — drop stale cards, add the 3 new live ones (brined/cakes/cookies), + DELETE
  butter, salty-snacks, maadanim, vegetable-spreads (page+route) + the duplicate routes bread-comparison, cakes-hard-cookies. TASK-314 remainder.
- **Wave 1:** conform bread (proof-of-path; real frozen provenance).
- **Wave 2:** rebuild cheese + yogurts (real direct-scrape run → conform, else delete).
- **Wave 3:** milk BSIP0 rebuild — preview diff → conform → supersede the frozen ruling in the registry.
- Surviving catalog after sweep (target): cereals, granola, juices, hummus, hard-cheeses, brined-cheeses, cakes, cookies-coffee,
  snacks, snack-bars, bread, cheese, yogurts, milk — all on the uniform path; everything else deleted.

## Track progress 2026-06-17 (scoring track, parallel to TASK-321A frontend track)
- **Wave 0 (TASK-321A): orchestrator-verified** — clean FF branch, 6 routes deleted, index reconciled (9 kept + 3 added),
  0 dangling code refs, build green. One gap (orphan data JSONs) → follow-up sent to the parallel chat. Merge-ready after that.
- **Milk rescore PREVIEW done (unfreeze low-risk):** existing runs reproduce the frozen top exactly —
  `run_005_headpin` and `run_006_shelfrel_refreeze` both = 85/85/85 (whole 3.4% / natural 4% / goat) then 71/63.9/56.7;
  recal_p0 preview held the 85/A ceiling (0 products >85). A clean BSIP0 rescore is very unlikely to move milk's published scores.
- **Cheese rebuild = FEASIBLE:** scored run `cheese_spreads/bsip2_outputs/run_cheese_001` = 405 traces, **0 OFF references**.
  OFF is confined to LEGACY artifacts (old `yohananof_cheese_bsip0_raw…`, `cheese_frontend_v3.json`) — must NOT be the rebuild source.
- **Yogurt rebuild = FEASIBLE with discard:** `yogurt_system/bsip2_outputs` = 821 traces, **46 OFF-tainted** (in `run_yogurt_002`).
  Rebuild from a clean run + DISCARD the 46 OFF products (OFF-ban + missing-data-discard).
- **⚠️ Carry-forward risk:** confirm the LIVE cheese/yogurt pages aren't fed by OFF-tainted legacy data; if they are, take down pending clean rebuild (frontend-track check).

## Wave 3 milk — FULL CONFORM decision + parallel dispatch 2026-06-18 (orchestrator)
- **Owner ruling 2026-06-18: FULL CONFORM** of milk (not data-only, not exception). The flagship
  cinematic editorial page is replaced by the uniform `ComparisonPage`, per the zero-different mandate.
- **Blast-radius finding (corrects the earlier "deep dependency hub" worry):** only 4 files import the
  bespoke `milk-comparison-page-data.ts` (the JSON, milk-shelf-filters, milk-comparison-page, the route).
  The milk BLOG (`blog/milk-analysis/*`) is INDEPENDENT (imports `milk-analysis-content`, not the comparison
  data) — deletion does not touch it. Shared components do NOT import the milk module. Clean teardown.
- **Milk JSON is render-ready:** `milk_frontend_v1.json` (18 products, off_used=false, run_005_headpin scores,
  rowVerdict + insightLine present, page_copy with `caveat`/`prologue`(dict)/`shelf_lens_options`). On
  branch `sweep/milk-baseline-extract`, merged into worktree `C:\bari-milkconform` (branch `sweep/milk-conform`).
- **Three lanes dispatched in parallel (2026-06-18):**
  - **C1-GROK (P200)** — finalize `configs/milk.json` (render_fields, baseline_json=null, MILK_CANONICAL_FLAGS
    kept, RECAL_P0 stays off = reproduces published scores) + run `generate_page` → prove milk on the spine path,
    all gates green, G4 OFF=0. Main repo.
  - **C1-GEMINI (P201)** — rehab `sweep/cheese-conform` (stale: branched before PR#10/#11, would revert yogurt).
    Merge origin/master, keep yogurt-from-master + cheese-from-branch, rebuild, push. Worktree `C:\bari-cheese`.
  - **Frontend Agent (Sonnet)** — milk frontend conform mirroring yogurt PR#11, with milk's REAL lens filters
    preserved (cow/oat/soy/almond/rice). Worktree `C:\bari-milkconform` → push `sweep/milk-conform`.
- All three are RETURNED-UNVERIFIED until the orchestrator checks each claim against artifacts (build exit,
  gate table, grep-clean, yogurt-conform-intact-on-cheese-branch). No merge until verified + owner gate.

### P200 (milk spine config) — VERIFIED DONE 2026-06-18
Grok honestly BLOCKED on G2 COVERAGE=0 and correctly diagnosed root cause (corpus_dirs pointed at
`canonical_bsip1/run_001` = 8 dummies, not the 20 real barcodes). It did not fabricate a fix (stuck to my
4 bullets). Orchestrator fixed `corpus_dirs` → `03_operations/bsip1/run_milk_002/output` (the dir with the
20 real barcodes) and re-ran. RESULT: `generate_page` Overall **PASS** — 20 products, gates G1/G2/G3/G4(OFF=0)/
G5/G6/G8 all PASS, G7 SKIP (null baseline). Grade dist **A:3 B:1 C:5 D:10 E:1**, top **85/A** (7290000051352) —
reproduces published run_005_headpin scores exactly (conformance moves nothing). insightLines PENDING is expected
(authored copy is on the frontend track in milk_frontend_v1.json; null baseline = no copy carry). **Milk is on
the uniform spine path.** configs/milk.json `_status` = READY.

### Milk frontend conform — VERIFIED DONE 2026-06-18 (Frontend Agent + orchestrator)
Branch `sweep/milk-conform` (HEAD 64a45883, pushed). Route `/hashvaot/milk-comparison` now renders the thin
`MilkComparisonPage` → uniform `ComparisonPage` (reads milk_frontend_v1.json). Bespoke cinematic suite DELETED
(15 files: milk-editorial/* 10, milk-orbit-visual, milk-comparison-page-data, milk-shelf-filters, +2). Milk's
REAL lens filters PRESERVED (10 options, filter by filterTags) — richer than yogurt's empty set. milk-page-data.ts
kept dual-purpose (legacy block retained for the milk BLOG + bari-grade-badge + consumer-explanation-view, which
consume the old shape; the COMPARISON PAGE is fully conformed). Orchestrator-verified: npm run build exit 0,
39 pages, /hashvaot/milk-comparison present, full /hashvaot index intact, blog untouched. **The flagship
gold-standard page is no longer structurally "different."** Scores unchanged (run_005 published scores).

### P201 cheese-branch rehab — VERIFIED DONE 2026-06-18 (Gemini + orchestrator)
sweep/cheese-conform was stale (cut from PR#9). Gemini merged origin/master (zero conflicts, ort), preserving
yogurt-from-master + cheese-from-branch. Orchestrator-verified the yogurt conform survived + re-ran build
(exit 0, 39 pages, all routes) + pushed (Gemini auth-blocked). HEAD f3b38349. TASK-321I CLOSED.

### Wave 3 STATUS: both branches verified + pushed, awaiting owner merge gate
- `sweep/milk-conform` (HEAD 64a45883) — milk: spine config READY + frontend conformed.
- `sweep/cheese-conform` (HEAD f3b38349) — cheese conformed, rehabbed onto current master.
- Both build green; no scores moved; OFF=0. Merge to master = owner go-live gate (not done).

## SWEEP COMPLETE 2026-06-18 — every live category on the uniform spine
- Milk (PR #12) + cheese (PR #13) MERGED + LIVE. Yogurt (PR #11) live. Route deletions (6 delete-batch +
  duplicates) done. All 13 live comparison pages use the uniform ComparisonPage.
- **Bread (TASK-322) = the last structurally-different category — CONFORMED** via uniform pipeline re-run
  (freeze lifted by owner). Branch sweep/bread-conform (1a4b67c9): all gates PASS, OFF=0, copy authored,
  build green. Pending owner merge.
- Orphan cleanup: sweep/cleanup-orphans pushed (cheese_v3 + yogurts_v4 removed). Pending owner merge.
- snack-bars = redirect stub (not a category); its no-A ceiling is a frozen-invariant scoring matter (owner's call, separate).
- **Residual (optional, non-blocking):** milk-page-data.ts keeps a legacy block for the milk BLOG + bari-grade-badge +
  consumer-explanation-view (they read the old shape). The milk COMPARISON page is fully conformed; converting those
  other surfaces is a separate small follow-up if desired.
- After bread + cleanup merge: zero-different-category mandate SATISFIED. TASK-321 ready to close.

## Milk blocker #2 RETIRED 2026-06-17 (orchestrator)
rescore_all.py: the C10 milk-freeze gate (scored milk under MILK_CANONICAL_FLAGS, hard-failed on >0.001 drift vs
run_005_headpin) is DEMOTED from a hard gate to a diagnostic-only check (shelf_hard_failed no longer fails on c10;
delta still computed/printed/recorded for cross-shelf perturbation visibility). Owner lifted the CNO milk freeze
(scores don't matter, uniformity only). py_compile OK. Milk now scores as a normal shelf in the trigger path.
REMAINING milk: finish configs/milk.json render_fields (currently a TODO string) + bring the milk baseline JSON local
(on branch sweep/milk-baseline-extract) → generate_page/spine emits the conformed milk page → frontend wiring.
