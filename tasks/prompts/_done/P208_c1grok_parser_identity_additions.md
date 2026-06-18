# P208 — TASK-328 named-additive identity additions, no-score (route: C1-GROK)
# Data Agent build — identity/resolution table ONLY, score-neutral

**Repo:** `C:\Bari`
**Task to read:** `C:\Bari\tasks\TASK-328.md`
**ONLY file you may edit:** `03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py`
(Do NOT edit `signal_extractor.py` — adding an ADDITIVE_MARKER_PATTERN there changes additive_marker_count =
a SCORE move = belongs to the spine, NOT this lane. Identity table only.)

## Objective
Add authoritative named-additive identities so these resolve correctly for explanation/display, **without moving
any score.** Evidence: `research/16.08/` (EFSA re-evaluations, JECFA, FDA 21 CFR).

## Exact additions (new `Identity(...)` entries, mirroring the existing table style)
- **E903** carnauba wax — glazing/surface-finishing; benign; aliases `חומרי הזגה`, `חומר הזגה`, `שעוות קרנובה`,
  `קרנובה`, `E903`, `E-903`.
- **E492** sorbitan tristearate — emulsifier (low/structural concern, `is_named_concern=False`); aliases
  `סורביטן טריסטארט`, `סורביטן טרי-סטארט`, `E492`, `E-492`.
- **E553b** talc (magnesium silicate) — anti-caking; benign; aliases `טלק`, `טלקום`, `E553b`, `E-553b`.
- **E525** potassium hydroxide — acidity/pH regulator; benign; aliases `אשלגן הידרוקסיד`, `אשלגן הידרוקסידי`,
  `E525`, `E-525`. (Do NOT infer any potassium-nutrient benefit.)
- **E327** calcium lactate — firming/acidity; benign; aliases `לקטט סידן`, `סידן לקטט`, `E327`, `E-327`.
- **E326** potassium lactate — humectant/acidity; benign; aliases `לקטט אשלגן`, `אשלגן לקטט`, `E326`, `E-326`.
  (Add E326 explicitly so E327≠E326 never collide — E327 is calcium, E326 is potassium.)

Choose `additive_class` values consistent with the existing enum; all `is_named_concern=False`.

## Hard guards — the critical one
- **These identities must carry ZERO scoring delta.** Verify they are NOT picked up by any
  `ADDITIVE_IDENTITY_DELTAS` / additive_quality scoring path (TASK-222A F1 deltas). If adding any of these would
  change `additive_quality` or `additive_marker_count` for a real product, **STOP and flag it** — that converts
  this into a score move (spine territory), which this lane must not do.
- OFF-ban absolute. Do not invent data — every identity is from the cited regulators only.

## Acceptance test (run it, put result in self_check)
Take a real product whose text contains these E-numbers (e.g. the cake at `research/16.08`, or any cake trace).
Run the engine signal extraction on it **before and after** your edit and show that:
- the new identities now RESOLVE via the taxonomy lookup, AND
- `additive_marker_count` and the product's score/grade are **byte-identical** before vs after.
Show the deriving command + the two score/grade values (must be equal).

## Return
RETURNED proposal + return-contract JSON (`01_framework/operations/return_contract_v1.md`).
**Do not close. Do not commit or push.**
