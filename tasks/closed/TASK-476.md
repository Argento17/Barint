---
id: TASK-476
title: Fix input_loader ingredient fallback + re-flow bread/crackers/protein-bars (owner-approved rescore)
owner: data-agent
status: CLOSED
priority: CRITICAL
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: >
  SHIPPED LIVE. PR #58 merged to origin/master as de8c7801 (verified: git merge-base --is-ancestor 17161929 origin/master = TRUE). Engine fix (input_loader get_ingredients fallback + router_v2 count-consumer) + bread(23)/crackers(19) surgical rescore live; 5 grade-movers all downward, flagship 90.8/S. Two-gate content sign-off complete (476d author + 476_final_qa Adversarial QA GO). Both co-signs on record (Nutrition+Product × loader fix + router delta). Merge-conflict re-resolution (vs TASK-478 imageUrl self-host) verified 0/0 union both files. Worktree C:\bari_wt_t476 pruned. Protein-bars split to TASK-477; generator hardening TASK-479; cheese traceability queued (TASK-474 b2). Post-merge: shadow APPROVED baseline re-promote dispatched.
depends_on: [TASK-475]
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-03 (tripwire-1 cleared). Fix 03_operations/bsip2/proto_v0/src/input_loader.py get_ingredients() to fall back to ingredient_order/ingredients_text_he when ingredients_list is empty; re-flow bread(23)+crackers(19)+protein-bars(32) through the spine (rescore->copy_stage->gates). Measured impact (TASK-475): 8 grades move, all downward; flagship bread stays S. GATES: Nutrition+Product co-sign FIRST (scoring-rule hard rule), then fix+reflow, copy re-audit (scores changed), both page gates + red-team, owner deploy PR. NO live deploy without owner click.
---

# TASK-476 — Fix input_loader ingredient fallback + re-flow bread/crackers/protein-bars (owner-approved rescore)

## Gate 1 — CO-SIGNS (both GREEN, 2026-07-03)
- **Product = CO-SIGN** (`tasks/returns/TASK-476_product_cosign.md`): GO; re-flow all 3 together, one pass, no staging, no delist; honest de-anchor doctrine; affirmed copy re-audit + both gates + two-gate required pre-deploy.
- **Nutrition = CO-SIGN-WITH-CONDITIONS** (`tasks/returns/TASK-476_nutrition_cosign.md`): fix is pure plumbing (feeds bleed-sanitizer, no philosophy change, no D6/D7); verified raw BSIP1; 5 movers spot-checked = justified drops. **3 binding conditions:** (1) precedence `ingredients_list→ingredient_order→ingredients_text_he/raw`; (2) sanitizer `dropped` audit across all 57; (3) re-derive "ingredient data missing" caveat copy alongside scores.

## Gate 2 — FIX + RE-FLOW (dispatched, t476-fix-reflow, bg)
Data Agent: fix `get_ingredients()` fallback + spine re-flow bread/crackers/protein-bars into a STAGING bundle (no deploy, no git). Must reproduce TASK-475 impact (8 grades down, flagship stays S) + Step-5 surgical proof (unaffected categories byte-identical) + Step-6 stale-caveat list for the copy pass.

## SEQUENCING NOTE (merge order — surfaced to owner)
The 3 rescore categories are exactly the copy the pending overhaul PRs touch: **#51 includes bread + protein-bars**, **#53 includes crackers**, **#56 = crackers provenance**. To avoid copy↔score collision, the overhauled copy (#51/#53) is the foundation the new scores sit on. Options for owner: (A) merge #51+#53 first, then rescore on top (2 deploys); (B) orchestrator assembles ONE combined bundle per category (overhauled copy + new scores + re-audited mover copy) → single deploy. Recommend B for a clean single consumer deploy per category. Held #56/#51/#53 crackers/bread/protein merges pending this decision.

## Gate 2 — FIX + RE-FLOW: RETURNED + orchestrator-verified (staging bundle)
- **Fix (2 files, uncommitted):** `input_loader.py::get_ingredients()` fallback `ingredients_list→ingredient_order→text` (Nutrition precedence). **+ scope expansion `router_v2.py`:** had a DUPLICATE naive ingredient-count fallback (never called get_ingredients) that mis-fragmented the flagship's bracketed sub-group 13→18 items → crossed REQ-362-R2 → misrouted tahini bread to snack_bar/protein-bar table → 89.6/A. Fix routes it through get_ingredients → 90.8/S. Blast radius 1/57 flips (the flagship, favorably). No rule/weight/threshold changed.
- **Verified from staging (`scratchpad/task476/rescore_all57_result.json`):** 57 rescored, **7 grade-movers ALL DOWN** (bread 2079033/2079927/2079996 A→B, 4685027 B→C; crackers 7290018790328 C→D; protein 7290015130028/7290018703076 C→D), 0 up. **Flagship 94.8/S→90.8/S stays S**, routed whole_food_fat/tahini. 34 score-down, 4 up (no grade cross). Matches co-sign.
- **8→7 correction:** TASK-475's 8th mover (7290019401018) measured vs a STRAY non-live BSIP1 `run_maadanim_001` artifact; real live corpus = no cross. Corpus-hygiene note → TASK-409 (why run_maadanim_001 exists + is picked up).
- **Surgical proof:** identity re-run hummus(57)+cheese(47) = 0 score diffs. **Sanitizer audit:** 9/57 had drops (24 items), 0 real ingredients lost, 0 bleed kept.
- **Disclosed:** agent ran one prohibited `git stash` mid-run, reverted clean (tree intact, verified). 3 PRE-EXISTING stray stashes on repo (wt-wip hummus copy-overhaul WIP + 2 feat-branch) — debris, NOT this task, left untouched.

## Gate 2b — router_v2 delta re-cosign: BOTH GREEN. Nutrition CO-SIGN (verified independently: read router code, pulled flagship raw BSIP1, confirmed 13→18 sub-group explosion + single count-consumer + tahini-bread-is-a-bread; no new condition). Product CO-SIGN (corrective+protective, blast radius 1 product, not rubric-shopping). **FIX FULLY CO-SIGNED (both agents × both the loader fix and the router delta) + orchestrator-verified.**

## Gate 3 — ASSEMBLY (worktree `C:\bari_wt_t476`, branch `golive/task476-rescore` off origin/master) + SPLIT
- **SPLIT (orchestrator call, data-justified, overrides Product "all 3 together"):** ship **bread+crackers ONLY**. **Protein-bars → TASK-477** (non-conforming corpus: config says generate_page incompatible; corpus pointer → dir w/ 0 bsip1 files; 7/15 REAL_LOSS rows scored vs STRAY WRONG-CATEGORY BSIP1 → mover set unstable 8/7/8; live scores may also be contaminated). Protein JSON reverted to origin (byte-identical) — its live scores untouched until cleaned.
- **TASK-476b (spine rebuild off origin/master):** applied engine fix FRESH in worktree; bread 4 movers + flagship 90.8/S + crackers 1 mover reproduce co-signed exactly; 16 other categories byte-identical.
- **TASK-476c (scope cleanup):** generator had re-added a deliberate crackers DISCARD (7290112968807, corrupted nutrition) AND silently dropped crackers mandatory `categoryCaveat` + provenance _meta → agent restored (crackers now 19, caveat back, ranks recomputed, G7 PARITY 19==19/1 grade change). Orchestrator caught + reverted a stray `_catalog-client.tsx appearance=dashboard` leak. **Diff now scope-clean:** bread_frontend_v4 + crackers_frontend_v1 + engine (input_loader/router_v2/run_gates) + run-records/gate-reports ONLY.
- **5 movers = PENDING_COPY** (bread 2079033/2079927/2079996 A→B, 4685027 B→C; crackers 7290018790328 C→D) → **Content two-gate IN FLIGHT** (author running; Adversarial QA next).

## Gate 4 — CONTENT + ASSEMBLY (DONE, orchestrator-verified)
- **476d Content author:** 5 movers' insightLine+rowVerdict authored (overhaul voice, driver-named, phrasing-clean: 0 em-dash/antithesis/grade-naming). Fixed leaked _website_cluster.
- **476e field close-out:** resolved all remaining PENDING → 0.
- **CRITICAL CATCH (476f):** the full spine regeneration DEGRADED curated content (emptied crackers positiveSignals/limitingFactors on ~12 non-movers, downgraded bread confidenceLabel 19, overwrote mover comparisonContext w/ generic placeholder) — same milk/cheese generator gap → **TASK-479 hardening**. **PIVOT: rebuilt as SURGICAL numbers-patch** (milk-style): origin curated pages + ONLY score/grade/rank/bariInterpretation-numbers + 5 movers' verdicts. Orchestrator-verified: 0 unexpected diffs vs origin, curated prose restored (positiveSignals/limitingFactors/confidenceLabel/comparisonContext == origin), PENDING=0, gates G1-G8 PASS, counts 23/19, flagship 90.8/S + 5 movers correct. Non-movers 497044(+0.7)/7290016967074(+3.0) score-up = KNOWN co-signed (TASK-475 "5 higher, none cross grade").

## Gate 5 — FINAL QA + red-team: GO (0 CRITICAL). Track V green (score-vs-trace 0 mismatch, surgical-patch integrity 0 curated-prose drift, gates PASS). 1 HIGH = RT-1 false "double sodium" claim on crackers mover (actual 1.59x not 2x — content author corrected to "highest by wide margin", orchestrator-verified accurate + phrasing-clean). RT-2/RT-3 non-blocking (trace authoritative + used; engine fix co-signed).

## SHIPPED — PR #58 (owner deploy click) — https://github.com/Argento17/Barint/pull/58
- Branch `golive/task476-rescore` **rebased onto current origin/master** (origin had advanced 5 commits w/ TASK-478 image work — NO overlap w/ my files; rebase clean, net diff = 9 files: bread+crackers JSON+reports, input_loader/router_v2/run_gates, run-records).
- **CI:** frontend ✅ · python-tests ✅ · off-sweep ✅ (OFF-clean) · Vercel ✅ · **shadow-backtest ❌ = EXPECTED** (exit 1 "engine movement, Nutrition must sign off" — the co-signed intentional score fix; NOT exit-2 frozen/invariant; Nutrition sign-off recorded TASK-476). mergeable:true.
- **Content two-gate COMPLETE:** author (476d) + Adversarial QA (476_final_qa GO) both signed off.

## CONFLICT RESOLVED — PR #58 re-pushed mergeable (2026-07-03)
- Owner hit merge conflicts. Cause: origin merged **TASK-478 Phase B (`eae897ce`)** which rewrote `imageUrl` → same-origin `/products/*.webp` in the SAME two JSONs my patch scores. Field-disjoint (origin=imageUrl only; mine=score/grade/rank/verdict only) — git conflicted on adjacent lines, no real data tension.
- Data Agent merged origin/master into branch, resolved both files by **JSON-level union** (origin imageUrl + my scores), re-ran gates, pushed a merge commit (`17161929` + gate-report `3b31a787`) — normal push, no force, PR #58 updated in place.
- **Orchestrator-verified:** union proof 0/0 both files (imageUrl==origin, all else==mine); counts 23/19; flagship 90.8/S rank 1; **`git merge-base --is-ancestor origin/master HEAD` = TRUE → PR #58 merges with ZERO conflicts**; local tip==remote tip `3b31a787`; imageUrl = `/products/<barcode>.webp` (TASK-478 self-host pattern) confirmed on product sample. Gates Overall PASS both.
- Ready for owner merge click again. Same tripwire-2 deploy.

## FOLLOW-UPS (post-merge)
- Re-promote the shadow APPROVED baseline to the new bread/crackers scores so future PRs don't re-flag this movement (Shadow1 baseline policy).
- **TASK-477** protein-bars corpus conformance (split out) · **TASK-479** generator carries curated expansion content · cheese traceability (TASK-474 batch 2) · red-team backfill remaining (cakes/choc-bars/choc-tablets/milk).
- Worktree `C:\bari_wt_t476` prune after merge.
**MERGE SEQUENCING (recommend to owner):** merge #51 (bread+protein copy overhaul) + #53 (crackers) FIRST → overhaul copy becomes the base → then a single rescore PR per the 3 categories (new scores + 7 movers' re-audited copy). Hold #56 (crackers provenance) — rescore regenerates crackers traces; fold provenance in at bundle assembly. #57 (product pages) independent, merge anytime.
