# D7 Co-Sign — Shelf-Relative Sodium + Dairy-Protein Reweight (v1)

**Product Agent, 2026-06-13.** Verdict: **GRANTED WITH CONDITIONS.** Both flags
(`BARI_SODIUM_SHELF_RELATIVE_V1`, `BARI_DAIRY_PROTEIN_REWEIGHT_V1`) may proceed, independently
rollback-able. Owner approved the direction; Nutrition ruled; this is the Product co-sign leg of D7.

## Why granted
- Absolute bands vs shelf-relative surcharge measure ORTHOGONAL signals (objective health vs
  shelf-outlier status) — not double-counting; the low-variance guard (stdev<150 → suppress) is what
  makes the surcharge honest (no punishing noise on tight shelves).
- Protein re-weight follows the established archetype-weight precedent (veg_spread EV-032/R6); +4pp
  protein / −4pp calorie-density, sum stays 1.00. HP-suppression for clean low-sodium dairy extends
  EV-054 with a TIGHTER gate (sodium≤400 AND additives=0).
- Honest: 1,550mg at 88/A is misleading; the differentiation vs a 300mg product is real (passes the
  butter-clustering rule — reflects, doesn't manufacture). Confidence ceiling on 4861070 (no
  ingredients → max B) is correct behavior.

## MANDATORY CONDITIONS (orchestrator must enforce before this is real)
1. **EV-056 (surcharge) + EV-057 (reweight) registered in the evidence registry BEFORE/with code.**
2. **Per-run opt-in ONLY** — flags MUST NOT become engine defaults; implementation must carry a
   comment forbidding default-on without a fresh D7 covering all dairy_protein/whole_food_fat corpora.
3. **No-regression gate = EV-053/054 standard:** invariants 342 → 0 regressions; **cross-corpus
   byte-diff vs 7 published categories** (milk, yogurt, bread, cereals, granola, snack-bars,
   cheese-spreads) → byte-identical. ANY published move = hard stop → owner. Committed artifact, not
   self-report.
4. **Verification artifact** on the first flag-on run: flat table
   `barcode,score,grade,binding_caps,nova,fat,sodium,shelf_median,surcharge_fired,context_flag` +
   full distribution (histogram/min/max/median/stdev/most-common-count).
5. **Codify as "standard" only AFTER QA hard-pass** on the first full brined run — not before.

## NOT approved (explicit)
- Auto-activating for yogurt/maadanim/butter/hard-cheeses without each one's own D7.
- Engine-default activation. Consumer-facing output before QA hard-pass.

## Reversal watch (Product)
Revisit if the protein re-weight lifts full-fat NOVA-3 cheeses above NOVA-1 lean cheeses (flattery),
or the surcharge reverses expected quality ordering. **Orchestrator: check this in verification.**

## Side-finding (deferred)
4861070 `context_flag=null` despite "צפתית" keyword — moot here (sodium 300<500 blocks brined_food),
needs investigation before the next hard-cheese run.
