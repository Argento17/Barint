# Yogurt caveat boxes — Nutrition co-sign record (TASK-515 / 515A)

Durable provenance record for the two "הערת קטגוריה" (category caveat) boxes, created to satisfy
the two-gate content sign-off's Nutrition-accuracy leg (resolves Adversarial-QA finding RT-7, which
correctly noted the co-sign was not independently verifiable in-repo). Both caveats were reviewed and
co-signed by the Nutrition Agent via live dispatch on 2026-07-05; no prior "D13 verbatim" artifact ever
existed in-repo (the earlier run_record/DISPATCH_BOARD references to "D13-approved caveat" were dangling
citations — confirmed by independent search).

## Drinkable caveat (TASK-515A)
- **Nutrition dispatch:** agent a79170f196c103ce0 (this session). Reviewed the Content placeholder,
  found a completeness gap (named 3 high-sugar outliers but omitted לאסי מנגו 12.0g — the one product
  actually crossing the 12.0g absolute floor), CORRECTED it (added the lassi + a consumer-actionable
  "check the number yourself" line; title ":" → "—" per corpus caveat convention), and returned the
  approved verbatim text.
- **Engine-behavior basis (Nutrition-verified vs artifacts):** drinkable sugar shelf-relative guard
  FAILED (IQR scale 1.85 < 3.0 variance floor; median 4.95g, n=22) → sugar scored absolute-floor-only;
  no DRINKABLE shelf-rel constant persisted (constants.py), per EV-105v2 + run_record.json.
- **Applied:** yogurt_drinkable_COPY_DRAFT_v2.json → page_copy.caveat, byte-identical to the Nutrition-
  approved text (orchestrator-verified equal to scratchpad d13_drinkable_caveat_APPROVED.json body);
  `_content_agent_flag` removed. Carried forward unchanged into v3.

## Spoonable caveat (TASK-515)
- **Nutrition dispatch:** agent a02dad1352c8075d5 (this session). Reviewed the Content placeholder,
  ruled it factually sound but incomplete (described surcharge direction only; the mechanism is
  bidirectional — the corpus-minimum-sugar product 7290110328221 gets a real +1 relief bonus), and
  returned corrected + co-signed text naming both directions + a consumer-actionable line.
- **Engine-behavior basis (Nutrition-verified vs artifacts):** spoonable sugar shelf-relative
  BARI_SHELF_RELATIVE_V1 is ACTIVE (IQR scale 4.6 ≥ 3.0; median 4.65g, n=80/94); constants
  SUGAR_SHELF_REL_YOGURT_SPOONABLE_* persisted + D6/D7 co-signed (EV-105v2-FINAL), non-activating on
  score_engine (persisting the constant moved no score).
- **Applied:** yogurt_spoonable_COPY_DRAFT_v2.json → page_copy.caveat (round-2 authoring).

Both caveats: no banned framework vocab; no score change; score_engine.py untouched (tripwire-1).
