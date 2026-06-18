# Graduated Sodium D7 Co-Sign — Product Agent
**Task:** TASK-267 / grad-sodium-d7-cosign
**Date:** 2026-06-13
**Author:** Product Agent
**Verdict: CO-SIGN APPROVED** (with conditions)
**Scope:** BARI_GRAD_SODIUM_V1 flag design — Product Agent D7 co-sign to Nutrition Agent ruling

---

## Verdict: CO-SIGN APPROVED

All four D7 decisions co-signed. Hard conditions recorded below. EV-055 may be registered; implementation may proceed.

---

## Decision 1 — Surgical Flag Endorsement: CONFIRMED

The surgical `BARI_GRAD_SODIUM_V1` gate is the correct and only governable path.

`BARI_REDLABEL_V1` is a bundled flag activating four simultaneous scoring effects. Effect #1 (the global regulatory-quality formula) moves published yogurt and cheese-spread scores and has not been through its own D7. Co-signing BARI_REDLABEL_V1 to reach the sodium path would constitute implicit approval of an unapproved scoring change. Nutrition correctly rejected it.

The surgical flag is a gate addition to existing written logic (lines 2005-2044), one line of code, default off, trivially reversible. The SODIUM_GENERAL_BANDS logic is already scoped to `REDLABEL_ENDEMIC_SATFAT_CATEGORIES = {dairy_protein, whole_food_fat}`. This is a minimum viable activation with a defined rollback. Product endorses.

---

## Decision 2 — Activation Scope `{dairy_protein, whole_food_fat}`: CONFIRMED

The "endemic-and-structural" criterion is concrete and falsifiable: can the manufacturer reduce sodium without changing the food's fundamental identity? Brined cheese — no (salt is the preservation medium). Crackers, cereals, processed spreads — yes (reformulation choice). The boundary holds.

The expansion gate is binding: any future category claiming endemic-sodium status requires a new EV + D7 co-sign from both Nutrition Agent and Product Agent + corpus evidence of false-equivalence failure. This is locked at the D7 level, not by convention.

Note: `whole_food_fat` (tahini, nut butters) has trace sodium well below the 450mg band floor and will be effectively inert at launch. That is acceptable — no inaccuracy, and it covers the scope correctly if high-sodium tahini variants appear in future corpus runs. Guard 6 must explicitly confirm whole_food_fat products show zero unexpected movement.

---

## Decision 3 — Cheese-Spreads ≤2pt: CONFIRMED AS NOISE, NO OWNER ESCALATION

Co-sign Nutrition's noise ruling. Explicit ruling on the "published movement" question:

Cheese-spreads have no live standalone category page. The ≤2pt movement only materializes when the Data Agent explicitly re-runs the cheese-spread corpus with the flag on. Until that run is committed to frontend JSON, no live score changes. The "irreversible AND consumer-facing" tripwire does not fire at the point of co-sign.

On re-score: ≤3 products, ≤2pt, no grade change, sodium ≥450mg (label-observable, correct signal). The ≤2pt = noise governance rule applies. This is within D7 lane authority. No owner escalation.

Cheese-spreads are NOT excluded from the activation scope. That exclusion would be an unprincipled carve-out against the endemic scope definition and would constitute score distortion in the wrong direction.

---

## Decision 4 — Brined Routing Fix: CONFIRMED AS CORRECTNESS FIX

Routing 19 brined-cheese products from `default`/`cracker` to `dairy_protein` is a data correction. The engine already has a `dairy_protein` context for dairy products. Brined cheese is dairy. The current routing is a category-detection bug. Fixing it applies existing, D7-approved dairy_protein rules to products that belong to that context — it does not create or alter any scoring formula.

The routing fix is a prerequisite to Guard 5 (pin-break verification). It must be implemented before run_003.

---

## Honesty Check — Graduated Bands Do Not Flatter High-Sodium Products

The specific concern: a 24% fat cheese at 800mg sodium must rank below a 5% fat cheese at 500mg sodium.

The graduated bands are strictly more penalizing than the hard cliff for any product that was already at or above the cliff. The cliff was the flattering model: it capped the sodium penalty and prevented NOVA+fat signal from expressing. A product above the cliff received the same penalty regardless of how far above it was. The graduated flag replaces that single-cap with a progressive series — more sodium = more penalty.

Products previously pinned at 72 will break the pin and score lower under graduated sodium. The ordering will be more differentiated, not less. No honesty concern.

---

## Hard Conditions for Implementation

All conditions are blocking. Implementation does not proceed without each.

1. **EV-055 registered first.** Write EV-055 into `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` before any engine code change.
2. **Flag default = off.** The BARI_GRAD_SODIUM_V1 env-var default must be "off". All published run records committed with flag=off.
3. **Guard 1 — Milk byte-identical.** Re-score run_005_headpin with BARI_GRAD_SODIUM_V1=on. Expected: 0/20 scores move. ANY milk movement = HALT, owner tripwire fires immediately.
4. **Guard 2 — Yogurt sodium path byte-identical.** Re-score run_yogurt_006 with BARI_GRAD_SODIUM_V1=on only (not bundled flag). Expected: 0 yogurt products move from sodium path.
5. **Guard 3 — Cheese-spreads ≤2pt, no grade change.** Re-score with flag on. Accept: ≤3 products, ≤2pt delta, same grade. Any grade change = STOP.
6. **Guard 4 — engine_invariants.py 342 cases pass** before merge.
7. **Routing fix is a prerequisite to Guard 5.** The 19 misrouted products must route to dairy_protein before run_003 is executed.
8. **Guard 5 — Pin broken in run_003.** NOVA-1 low-fat products score higher than NOVA-3 high-fat products. If the pin is not broken, the flag is not activating and merge is blocked.
9. **Guard 6 — Non-endemic zero movement.** Confirm whole_food_fat products show no unexpected movement. Confirm non-endemic categories (cereals, snacks, bread) are unaffected.

---

## Reversal Condition

If run_003 shows NOVA-1 low-fat products implausibly reaching A-grade with sodium ≥1000mg, the ≥900mg band penalty magnitude requires review. Set BARI_GRAD_SODIUM_V1=off and return to D7 with revised band thresholds.

---

## Decision Log

| Item | Options considered | Choice | Decisive reason | Reversal condition |
|---|---|---|---|---|
| Surgical flag vs BARI_REDLABEL_V1 | (a) Turn on BARI_REDLABEL_V1 full bundle; (b) Surgical BARI_GRAD_SODIUM_V1; (c) Do nothing | (b) Surgical flag | BARI_REDLABEL_V1 activates unapproved regulatory-quality formula change that moves published scores | Never — bundled flag remains ungoverned until its own D7 |
| Activation scope | (a) Brined-cheese only hardcode; (b) {dairy_protein, whole_food_fat} with expansion gate; (c) Global | (b) Principled scope | Owner systematic mandate; hardcode violates pipeline model; global removes deterrent cliff from formulation-sodium categories | Revisit scope if expansion gate produces false negatives at D7 (a legitimate endemic-sodium category refused) |
| Cheese-spreads noise ruling | (a) Exclude cheese-spreads from scope; (b) Accept ≤2pt as noise per governance | (b) Accept as noise | Exclusion is unprincipled carve-out; ≤2pt is accurate signal, within noise governance, no live page affected | Revisit if cheese-spreads get a standalone live page and any product is near a grade boundary |
| Owner escalation | (a) Escalate; (b) D7 lane sufficient | (b) D7 lane | No tripwire fires: frozen milk clear, flag default=off, reversible, no external commitment | Escalate immediately if any milk score moves or any grade change appears in Guards 1–3 |
