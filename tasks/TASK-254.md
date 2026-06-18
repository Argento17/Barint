---
id: TASK-254
title: "Leap 6 — claim-entailment verification: copy cannot ship a claim its trace did not fire (build-time machine gate)"
owner: orchestrator
status: RETURNED
priority: HIGH
created_at: 2026-06-12
depends_on: []
blocks: []
category_id: null
summary: >
  Owner approval 2026-06-12 (tech leap 6, "Machine Gates"). Convert the
  read-every-consumer-string human gate into a build-time guarantee: every
  factual claim in a verdict / insight line / category caveat must be entailed
  by that product's glass-box trace JSON (+ methodology docs), or the build
  fails. Combines with the existing banned-phrase linter. Root incident: the
  fabricated "official food source" claim that shipped live. The human
  reviewer returns to judging tone/clarity only. Hebrew-aware; must
  distinguish "interpretive but grounded" (assertive-writing standard) from
  "invented" (fabrication). Sequenced BEFORE Leap 4+ (smaller, no infra
  dependency, de-risks the failure class that actually burned production).
---

# TASK-254 — Leap 6: claim-entailment machine gate

## Why (owner-approved rationale)
The deepest copy risk is fabrication, not style. The current defense is human
discipline (read-copy-before-ship hard gate) — it works but degrades with
volume. Trace JSON already records every fired rule/signal per product; copy
claims are checkable against it mechanically.

## Phase plan (proposed)
> AMENDED 2026-06-12: maadanim PURGED by owner (was an older version of yogurts) —
> original pilot choice invalid. New design: PILOT = yogurts v4 (pre-go-live,
> TASK-249) so the entailment run doubles as a pre-launch copy gate; CONTROL =
> cereals (live, human-approved) for false-block calibration.
1. Claim-extraction + entailment checker prototype over the yogurts v4 copy
   (pilot) + the live cereals copy (control) — false-block rate measured on the
   control (already human-approved), real findings expected on the pilot.
2. Calibration with Content + Nutrition: the "interpretive but grounded" vs
   "invented" boundary, Hebrew idiom handling, severity tiers (hard fail vs
   review flag).
3. Wire as build step next to the banned-phrase linter; failure blocks the
   category build. Read-copy-before-ship gate then narrows to tone/clarity.

## Phase 1a Return — ACCEPTED 2026-06-12 (orchestrator-verified)
Inventories delivered: yogurts (19 products, 19/19 traces) + cereals (34 products,
26/34 traces) at 03_operations/claim_entailment/inputs/. Verified corrections:
run_cereals_008 BSIP2 dir EXISTS but products/ is EMPTY (0 files) — agent said
"missing"; conclusion stands (live cereals page is trace-orphaned). Findings:
- **F1 (live integrity):** cereals live page traces: authoritative run dir empty;
  8/34 products traceless in every checked run → live claims currently
  unverifiable. Reconstruction dispatched (must also check
  run_cereals_multiretailer_001 — the 8 include Carrefour/US-brand products that
  likely arrived via merge_multiretailer_promote).
- **F2 (TASK-249 go-live gate):** verified missing: the authoritative
  reports/run_yogurt_006_run_record.json claimed in TASK-249's return block does
  not exist. Must be produced + verified before yogurts go-live. Also flag:
  barcode 7290107936309 appears twice on the page (Shufersal + Yohananof pools).
- **F3 (rubric impact):** fermentation_bonus_applied is null in per-product
  bsip2_trace.json (bonus applied at category layer, not persisted per-product) —
  rubric must cross-reference run-record A_list for fermentation claims until the
  trace schema carries it; trace-schema fix = separate small task, not the gate's.

## F1 resolution — cereals reconstruction ACCEPTED 2026-06-12 (orchestrator-verified)
run_cereals_008_reconstruction (63/63, 0 errors) + run_cereals_multiretailer_001_
reconstruction delivered; cereals_claims_input_v2.json gives 34/34 trace coverage
(verified: all paths resolve). The 8 ex-NO_TRACE products = multiretailer-promoted,
grades reconstruct to live values. **Drift finding:** 9/34 live scores are NOT
reproduced by the current engine (1–3 pts; 2 cross displayed grade boundaries:
7290107647854 53/C→50/D, 884912126115 D→E at 35). Ruling: numeric score/grade
claims verify vs LIVE frontend values; mechanism claims verify vs reconstructed
traces; the 9 drifted products carry a re-ship flag (copy + score regenerate
together at next cereals ship; joins TASK-189 sodium work). Governance note:
executing agent edited the Nutrition-owned rubric (OQ-06) — Nutrition ratifies at
calibration acceptance.

## Phase 1c Calibration — ACCEPTED 2026-06-12 (with methodology notes)
Outputs at 03_operations/claim_entailment/calibration/ (33+79 strings, 353 claims).
Methodology notes: agent verified numeric claims vs traces (not live frontend per
orchestrator ruling — flagged honestly as ambiguity #4) and did not open full
traces (UNVERIFIABLE inflated ~73 claims by inventory-field gaps). Conclusions
that survive verification:
- **YOGURTS:** copy authored against pre-TASK-249 state; SECOND S product found
  (bsip1_7290110565527 = 95.6/S vs 87/A on page) — strengthens P10 (run likely
  executed without ship flags). Full copy rewrite after P10 reconciliation.
- **CEREALS (orchestrator-verified live incidents):** 11+ products where card
  text contradicts own badge (e.g. ריבועי דגנים badge 36/D, text "drops to C";
  הרדוף badge 69/B, text "drops to C" + fabricated MoH red-label sodium driver).
  Root cause: rowVerdicts predate current scores AND the verdict standard
  (sodium = fact only, never driver). Remediation = regenerate all 34 cereal
  verdicts under the standard (P11) — cereals jumps the verdict-standard
  rollout queue. NOT deferred to next re-ship.
- **Rubric v2 queue (P12, Nutrition):** codify two-layer rule (numeric vs live
  frontend / mechanism vs trace); T4b internal-history class (REVIEW default);
  display_values added to inventory trace_summary; cross-product reference
  pass; fermentation bridge → UNVERIFIABLE (orchestrator override stands).

## P12 Return — Rubric v2 DELIVERED 2026-06-12 (proposed RETURNED)

Deliverable: `03_operations/claim_entailment/claim_entailment_rubric_v2.md`
v1 retained as history. Five calibration lessons codified:

1. **Two-Layer Verification (§4):** score/grade claims verify vs live display values (Layer 1); mechanism/causal claims verify vs trace (Layer 2). Drift between layers = PIPELINE finding (DISPLAY-DRIFT annotation), not copy HARD-FAIL.
2. **Fermentation Split (§7.2):** STATE A (run-record bridge available → REVIEW) / STATE B (no support → UNVERIFIABLE). Closes calibration Ambiguity 5, which misread OQ-03 as "all fermentation UNVERIFIABLE."
3. **T4b subtype (§2.4):** internal pipeline-history claims ("prior version had bad data") → REVIEW default. T4a zero tolerance unchanged.
4. **Cross-Product References (§8):** full §-procedure; verify claim about product Y against Y's trace; superlative = corpus-wide check; unresolvable → REVIEW.
5. **Display-Values Spec (§9):** 14-field inventory spec; Data Agent implements. Priority 1: display_score + display_grade. Priority 2: protein/sugar/sodium_mg (covers ~40/73 cereal UNVERIFIABLEs). Source: BSIP0 scrape only; OFF banned.

**Verdict changes from v1:**
- CHF-07: HARD-FAIL → REVIEW (T4b; internal pipeline history, not external authority)
- CEX-02 T4b claim: HARD-FAIL → REVIEW (string verdict unchanged — T2 fabricated causal still HARD-FAIL)
- CEX-08: UNVERIFIABLE → REVIEW (reconstructed trace now available)

**Nothing pushed back on.** Implementation note: `ingredient_list_raw` inline replaced by `ingredient_list_sha256` (hash + fetch-on-demand from BSIP0 scrape) to avoid bloating inventory files.

**Remaining open (not resolved in this rubric):**
- Ship-flag run regeneration (OQ-02): YHF-01/02/16 stay HARD-FAIL until display grades confirmed
- TASK-189: cereal sodium rule absent; all sodium T4a claims in cereals remain HARD-FAIL until task closes
- Trace schema fix: `fermentation_bonus_applied` non-null; fermentation claims remain REVIEW/UNVERIFIABLE until landed
- Phase 2 (build-time wiring): rubric is now spec-complete; Phase 2 = implement as build step next to banned-phrase linter

## Rubric v2 — ACCEPTED by orchestrator 2026-06-12 (verified)
All 5 codifications verified present in claim_entailment_rubric_v2.md (§4 two-layer,
§7.2 fermentation split, §2.4 T4b, §8 cross-product, §9 display-values 14-field spec
w/ ingredient_list_sha256). Verdict downgrades CHF-07 / CEX-02 / CEX-08 → REVIEW
follow correctly from the new law. §9 implementation dispatched as P15 (inventory
builder, cheap lane). Remaining launch blockers are non-rubric: ship-flag
regeneration (P13), TASK-189 cereal sodium, fermentation trace schema.

## P11 Return — Cereals copy remediation DRAFT DELIVERED 2026-06-12 (proposed RETURNED)

Output: `C:\Bari\02_products\breakfast_cereals\cereals_copy_remediation_draft_v1.json`
34 of 34 products regenerated. No live files touched — owner read-gate required before any ship.

**Confirmed-incident list (17 products; more than the 11+ calibration estimate):**

| Product | Incident type |
|---|---|
| קורנפלקס אורגני הרדוף | Grade contradiction (badge 69/B, text "יורד ל-C") + fabricated MoH red-label + sodium as causal |
| דגני בוקר סיני מיניס | Grade contradiction (badge 55/C, text "B") + sodium as causal |
| דגני בוקר קוקומן חום לבן | Grade contradiction (badge 55/C, text "B תחתון") + sodium as driver |
| דגני בוקר דליפקאן | Grade contradiction (badge 46/D, text "C") |
| כדורי דגנים טעם שוקו | Grade contradiction (badge 46/D, text "C") |
| טבעות דגנים טעם דבש | Grade contradiction (badge 46/D, text "C") |
| טבעות דגנים שיבולת שועל | Grade contradiction (badge 46/D, text "C") |
| צדפי דגנים טעם שוקולד | Grade contradiction (badge 43/D, text "C") |
| כדורי דגנים טעם שוקולד | Grade contradiction (badge 43/D, text "C") |
| דגני בוקר טבעות דבש לל"ג | Grade contradiction (badge 43/D, text "C") |
| קורנפלקס דבש | Grade contradiction (badge 40/D, text "C") |
| ריבועי דגנים עם קינמון | Grade contradiction (badge 36/D, text "יורד ל-C") + fabricated sodium causation |
| דגני גרייט גריינס דייטס | Fabricated cause: BHT attributed as grade driver |
| טריקס דגנים בטעם פירות | Grade contradiction (badge 32/E, text "D") |
| דגני בוקר ויטביקס | T4 violation + fabricated cause (vitamin enrichment as grade driver) |
| ליון דגני שוקולד וקרמל | T4 violation + fabricated cause (glucose/fat architecture) |
| דגני בוקר נסקוויק | T4 violation (prior-run reference) |

**Products where trace gives too little (flagged, not invented):** None blocked entirely.
Nine products have `sugar=null` in live frontend; for these, "סוכר גבוה" stated (backed by ISRAELI_RED_LABEL_1_SUGAR firing), no fabricated numerics.

**Live-vs-trace grade drift noted (text follows live badge per task rule):**
- שוגי: 53/C live vs 50/D reconstructed (noted in `trace_drivers_cited`)
- קורנפלקס דבש: 40/D live vs 37/D reconstructed (noted)

Awaiting owner read of draft before any ship to `cereals_frontend_v2.json`.

## P17 — First pre-ship gate run ACCEPTED 2026-06-12 (orchestrator-verified)
Gate output verified at 03_operations/claim_entailment/calibration/
cereals_draft_gate_v1.md: 68 strings → 51 PASS / 15 REVIEW / 2 UNVERIFIABLE /
**0 HARD-FAIL**. All 17 confirmed live incidents (CHF class) remediated in the
draft. The 2 UNVERIFIABLE = honest data-gap statements ("נתוני סיבים לא היו
זמינים") where fiber=null — correct per rubric §2.1, not fabrication. The 15
REVIEW = T3 editorial framing/superlatives (incl. 2 confidence-ceiling products
where copy names the nutritional profile rather than the ceiling — acceptable
T3, noted for Content's style ledger). **Draft is owner-read-ready; no Content
fix loop.** This was the gate's production rehearsal: rubric v2 executed
end-to-end on pre-ship copy with zero process gaps. Phase 2 (build-step wiring)
is now the only remaining phase.

## Constraints
- Trace + methodology docs are the ONLY entailment ground truth. Never
  external sources (OFF ban applies to verification too).
- No score or trace changes — this gate reads traces, it never edits them.
- Convergence: per-string checks should run as Spine stages (TASK-252);
  Shadow (TASK-253) stays the engine-side gate — this is the copy-side twin.
