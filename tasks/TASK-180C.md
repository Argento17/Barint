---
id: TASK-180C
title: Bread re-baseline — rescore on pinned baseline, fold in TASK-169F 4 recal moves, owner sign-off + QA freeze + reship
owner: data-agent
status: CLOSED
priority: HIGH
deferred: false
created_at: 2026-06-04
blocker: null
resumed_at: 2026-06-05
resume_reason: "TASK-180B CLOSED 2026-06-05. Blocker lifted. TASK-169F CLOSED (4 B→A bread moves frozen, ship obligation transferred here)."
closed_at: 2026-06-05
cc_reviewed: 2026-06-05
depends_on: [TASK-169F]
blocks: []
category_id: null
summary: >
  Step3 (final) of TASK-180. CLOSED. run_bread_008_headpin is the canonical bread baseline. 13 grade-affecting moves shipped (7 B→A via W4, 5 C→B upgrades, 1 A→B resolved by recal). 5 recal products use RECAL_P0=on scores (all 82/A). Calibration layer superseded (recal scores exceed any calibration target). bread_frontend_v2.json reshippped: A=13 / B=11 / C=0. TASK-180 umbrella (milk+snacks+bread) complete.
---

# TASK-180C — Bread re-baseline — rescore on pinned baseline, fold in TASK-169F 4 recal moves, owner sign-off + QA freeze + reship

## Context

Step 3 (final) of TASK-180. Engine baseline pinned as git tag `engine-baseline-2026-06-04` (f075d9e).
Milk (180A) CLOSED + LIVE. Snack bars (180B) CLOSED + LIVE (2026-06-05).

Bread is the worst-affected legacy category. When the bread sprint1 baseline was compared against
HEAD engine at the start of the TASK-180 program: **165/256 products with drift, including 83 upward
grade changes**. The live bread page is substantially stale.

**Frozen provenance** (must not be touched):
`real_bread_retail_003_v1` (Shufersal, 25–26 May 2026): 258 scanned → 81 coherent → 31 curated
(24 scored + 7 transparency). This is the display corpus.

**Two layers of changes to separate:**
1. **Engine drift** — scores that changed on HEAD engine vs the sprint1 baseline due to accumulated
   engine updates since the original run (unrelated to recal)
2. **TASK-169F recal B→A moves** — 4 specific bread products that the BSIP_RECAL_P0 flag promotes
   from B to A (owner-modeled in 169F, never shipped, ship obligation transferred here)

Run with `BARI_RECAL_P0=off` for the primary baseline (engine-baseline-2026-06-04 HEAD).
Also run with `BARI_RECAL_P0=on` separately to isolate the 4 TASK-169F B→A moves.

**lechem calibration layer** (`calibrate_lechem_scores.py`): this was a manual calibration patch
applied to correct for BSIP2 having no ingredient access at the time. Check whether the current
HEAD engine (which has ingredient access) produces scores that make the calibration layer obsolete
or contradictory. Surface in the sign-off memo; owner decides whether to retain or retire it.

## Key Artifacts
- Corpus (31 display products): `C:\Bari\02_products\bread\` (bread BSIP1 run)
- Bread BSIP2 output dir: `C:\Bari\02_products\bread\bsip2_outputs\`
- Lechem calibration script: `C:\Bari\02_products\bread\calibrate_lechem_scores.py` (reference)
- Milk baseline pattern: `02_products/milk/bsip2_outputs/run_005_headpin/` + `batch_run_milk_005_headpin.py`
- Snack bars pattern (just completed): `02_products/snack_bars/bsip2_outputs/run_snackbars_007_headpin/`
- TASK-169F output (4 frozen B→A moves): `03_operations/bsip2/proto_v0/` (recal runner)
- Live bread frontend JSON: `bari-web/src/data/comparisons/lechem_frontend_v2.json`
- Output dir: `02_products/bread/bsip2_outputs/run_bread_008_headpin/`

## Run Configuration
- Primary run: `BARI_RECAL_P0=off` | `BARI_GLASSBOX_W4=on` | `BARI_TASK144_FIXES=off`
- Recal isolation run: `BARI_RECAL_P0=on` (identify the 4 TASK-169F B→A moves only)
- Output: `run_bread_008_headpin/off.json` (primary) + `run_bread_008_headpin/recal_on.json`

## Deliverable
1. **Runner script** `run_bread_008_headpin.py` — scores the bread display corpus on HEAD engine
2. **Reproduction audit** — HEAD-OFF vs live lechem_frontend_v2.json: reproduce rate + per-product
   diff table, classified as grade-affecting / ≥2pt cosmetic / <2pt cosmetic
3. **Run record** `run_record.json` with corpus_n, config_hash, reproduction rate
4. **4 TASK-169F B→A moves table** — for each of the 4 products: product name + old grade (B) +
   HEAD-no-recal score + HEAD-with-recal score + grade. Owner decides per-move: ship or hold.
5. **Lechem calibration layer assessment** — does HEAD engine make the calibration layer obsolete?
   Specific products + score comparisons. Recommendation: retain / retire / partially retire.
6. **Sign-off memo** — grade-affecting moves table, 4 recal moves surfaced with recommendation,
   calibration layer recommendation; explicit per-move owner decision requested
7. **Corrected crosswalk** `bread_crosswalk_run008.md` — lech-XXX → bsip1_pid → run_008 score
   (use imageUrl-barcode extraction to verify labels, per the lesson from 180B)
8. **No frontend JSON changes** — freeze only; reship after owner sign-off

## Return Format
Propose RETURNED with:
- Reproduction rate vs live page
- Grade-affecting moves count + list
- 4 TASK-169F B→A moves: show per-product score (recal-off vs recal-on)
- Lechem calibration assessment: obsolete / still needed / partially
- Sign-off memo ready for owner

---

## Data Agent Return Block (2026-06-05)

**Status: RETURNED — awaiting owner sign-off**

- Reproduction rate (vs lechem_frontend_v2.json calibrated scores): 2/24 (8%) — explained by accumulated engine drift + GLASSBOX_W4 + calibration offset
- Rollback identity: 31/31 (engine deterministic)
- Grade-affecting moves vs live: 13 (7 B→A, 5 C→B, 1 A→B downgrade)
- Key driver of B→A upgrades: GLASSBOX_W4 raises fat_quality dimension from 50→83-92 for whole-grain breads
- Recal isolation (RECAL_P0=on): 5 products with grade change B→A
- The A→B downgrade (קרקר כוסמין מלא ושומשום, 82→78.4) is reversed by recal (→81.6/A)
- Calibration layer: HEAD scores 9-12pt above all calibrated targets; all 5 calibration-targeted products also appear in recal_isolation_grade_moves — recal supersedes calibration for them
- Artifacts: `02_products/bread_retail_003/bsip2_outputs/run_bread_008_headpin/` (7 files)
- Actual live file: `bari-web/src/data/comparisons/bread_frontend_v2.json` (not lechem_frontend_v2.json — that file lives only in 02_products/)

---

## Owner Sign-off (2026-06-05)

**"approve all - sign off"**

All decisions approved:
1. ✓ 7 B→A upgrades (GLASSBOX_W4 / whole-grain fat quality)
2. ✓ 5 C→B upgrades
3. ✓ 1 A→B downgrade resolved by recal (קרקר כוסמין מלא ושומשום → recal 82/A)
4. ✓ 5 recal isolation grade moves — all ship with on_score
5. ✓ Calibration layer superseded (recal scores cover all 5 calibration-targeted products)

---

## CC Close Record (2026-06-05)

**Close-readiness gate: PASSED**

Independent verification findings:

1. **Correct live file identified** — run_record and Data Agent referenced `lechem_frontend_v2.json` (lives in 02_products/, 81 products). Actual live website file is `bari-web/src/data/comparisons/bread_frontend_v2.json` (24 products). Reship was correctly targeted at bread_frontend_v2.json.

2. **All 7 run artifacts confirmed** at `02_products/bread_retail_003/bsip2_outputs/run_bread_008_headpin/`: runner, off.json, recal_on.json, run_record.json, sign_off_memo_180C.md, bread_crosswalk_run008.md, AUTHORITATIVE.md.

3. **Score map verified** — 24 product map (5 recal + 19 off) independently derived from crosswalk barcodes + run_record. SCORE_MAP in reship_bread_180C.py matches run_record exactly.

4. **Reship executed and verified** — bread_frontend_v2.json: 24 products, A=13/B=11/C=0, sorted descending, max=82/min=66. grade_divergences cleared (engine now agrees with 82/A).

5. **Frozen invariants** — no bread A-ceiling invariant exists (unlike snacks). Max=82/A is the HEAD engine score for a verified whole-grain product (לחם טחינה פרוס, exact match). Acceptable.

6. **TASK-169F obligation discharged** — all 4 originally modeled B→A moves reconciled: 2 no longer grade moves under HEAD+W4 (absorbed into larger drift), 2 remain as recal grade moves, approved and shipped.

7. **Calibration layer retired** — superseded by recal scores for all 5 calibration-targeted products. No manual calibration patch applied in the reship.

8. **TASK-180 umbrella complete** — all 3 waves CLOSED: milk (180A), snacks (180B), bread (180C).

**Status: CLOSED** (by CC Agent, delegated closing authority 2026-06-02)
