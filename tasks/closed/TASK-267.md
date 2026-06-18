---
id: TASK-267
title: Graduated-sodium capability for endemic-sodium dairy (systematic; unblocks brined cheese)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-13
depends_on: []
blocks: [TASK-266]
category_id: null
summary: >
  Owner-authorized 2026-06-13 (systematic, not artisanal). Brined-cheese real-shelf run proved the hard HIGH_SODIUM_700MG_PLUS cap collapses endemically-salty categories: 31/48 pinned at 72 across all NOVA+fat. Build/activate graduated sodium (BARI_REDLABEL_V1 / SODIUM_GENERAL_BANDS path) for endemic-sodium dairy so NOVA+fat express. HARD CONSTRAINT: must NOT move FROZEN milk (run_005_headpin) or any published dairy score (yogurt/cheese-spreads) — frozen-invariant tripwire. Sequence: blast-radius recon -> Nutrition+Product D7 -> implement w/ heavy no-regression -> re-score brined run_003. Then TASK-266 packaging resumes.
---

# TASK-267 — Graduated-sodium capability for endemic-sodium dairy (systematic; unblocks brined cheese)

## Stage 1 — Blast-radius recon ✅ VERIFIED (2026-06-13)
Report: `02_products/brined_cheeses/reports/graduated_sodium_blast_radius_v1.md`. Orchestrator-verified:
- Engine untouched by recon (score_engine.py sha `d711ec58…` before=after) ✓.
- **FROZEN-MILK TRIPWIRE CLEAR — structurally:** milk sodium 40–120mg, far below lowest SODIUM_GENERAL_BANDS threshold (~450mg) → graduated sodium = 0 penalty → byte-identical guaranteed (orchestrator confirmed sodium ranges, not just the recon's count).
- Graduated sodium BREAKS the brined 72-pin (NOVA+fat express).
- **Key finding:** `BARI_REDLABEL_V1` is BUNDLED — it also flips a global regulatory-quality formula that moves published yogurt(7)/cheese-spreads(32)/cereals(8). Wrong vehicle.
- **Clean path = new surgical `BARI_GRAD_SODIUM_V1`** isolating only the sodium bands: milk + yogurt byte-identical, ≤2pt on a few highest-sodium cheese-spreads. Plus a routing fix (19/48 brined products route to default/cracker → need dairy_protein).

## Stage 2 — Nutrition D7 design ruling ✅ DESIGN APPROVED (2026-06-13)
`02_products/brined_cheeses/methodology/graduated_sodium_d7_design_v1.md` (sha `1b311c98…`). 4 decisions: (1) surgical `BARI_GRAD_SODIUM_V1` flag (reject bundled REDLABEL_V1); (2) scope `{dairy_protein, whole_food_fat}` on the "endemic+structural sodium" principle + expansion gate; (3) cheese-spreads ≤2pt (≤3 products) = acceptable noise, within D7 lane; (4) brined routing fix = correctness, not a scoring change. EV-055 drafted. Owner escalation NOT required (frozen milk clear). Ruling rests on orchestrator-verified facts.

## Stage 3 — Product D7 co-sign ✅ APPROVED (2026-06-13)
`graduated_sodium_d7_cosign_v1.md` (sha `42ea9ab0…`). Both signatures complete. Precedent gate = falsifiable test ("can sodium be reduced without changing the food's identity?"); ≤2pt cheese-spreads = noise (no live page affected, flag default off); overbuild OK; honesty confirmed (graduated bands MORE penalizing than cliff). No owner tripwire.

## Stage 4 — Implementation ✅ VERIFIED & CLOSED (2026-06-13)
score_engine.py (sha `e926421d…`, matches), router_v2.py (3 anchors → 48/48 brined route to dairy_protein), EV-055 registered, run_brined_003. Orchestrator independently verified:
- **Flag default OFF** (`:148`) + new path fully gated → committed engine INERT in production until explicitly enabled. engine_invariants re-run at default = all pass, 0 failures → published categories byte-identical.
- **No-regression structurally guaranteed:** flag gated on `context_flag=="brined_food"` (only brined products carry it) → milk/yogurt/cheese-spreads/cereals CANNOT be affected. Agent's on/off diffs (milk 0/40, yogurt 0/88, cheese-spreads 0/59 + 0 grade, cereals 0/63) confirm. Frozen-milk tripwire safe 3 ways (flag-off default + below-bands + brined_food gating).
- **run_003 (verified from traces):** off=0; A:12 B:27 C:7 D:2; range 39–88.8, median 74.4, stdev 10.8; **72-pin BROKEN** (HIGH_SODIUM cap 43→1; 39 distinct scores/48). Honest NOVA+fat spread, not a new pin.

**close_reason:** D7-approved (Nutrition ruling + Product co-sign), implemented as a surgical flag, orchestrator-verified: zero published-score movement (flag-gated + default-off), frozen milk safe, the endemic-salt collapse resolved (pin broken, honest spread). **Implementation note (accepted deviation):** narrower than the literal co-signed `{dairy_protein,whole_food_fat}` category scope — additionally gated on `context_flag=="brined_food"`, keying graduated sodium on the structural-sodium signal rather than category name. Safer, achieves the goal, and the systematic-expansion path is preserved (relax the gate + new EV per the expansion gate). Accepted as a more-conservative implementation of the approved intent.
