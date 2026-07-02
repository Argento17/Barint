# P454 / Crackers go-live independent red-team (route: C3)

You are the outside-the-family independent challenger (C3). TASK-433: the crackers comparison category is about to be recommended to the owner for consumer go-live (a tripwire-2 consumer-facing launch). Your job is to REFUTE its readiness — find what cannot be publicly defended. You do not fix, approve, or close; you raise findings (CRITICAL / HIGH / MEDIUM) with the specific row + field + why.

## Context (facts, not for re-litigation)
- Crackers were split out of the bread corpus. 20 displayable products, scored under the engine's dedicated "cracker" calorie-density archetype (D7-precedented) — NOT the bread table. Legacy-6 delta = 0.000 (they were already on the cracker table).
- Bari principle: category-relative scoring; "best ≠ excellent"; every consumer claim must trace to a real field; unknown is acceptable, fabrication and Open Food Facts are NOT.
- Grade dist A1/B12/C5/D2, range 47–81.6.

## Data to review
- C:\Bari\bari-web\src\data\comparisons\crackers_frontend_v1.json  (copy fields: nameHe, rowVerdict, insightLine, consumerTakeaway, bariInterpretation, expansion.*, _meta.categoryCaveat)

## Challenge these axes (raise a finding wherever the answer is "no / can't defend")
1. **Defensibility** — can each rowVerdict / insightLine / consumerTakeaway be publicly defended from the row's OWN data fields? Any claim that overstates, editorializes beyond the trace, or implies a health verdict the numbers don't support.
2. **Superlatives** — any "highest/lowest/cleanest/weakest on shelf / במדף / בהשוואה" claim that is not actually true against the full 20-row corpus (name the row it's actually true/false for).
3. **Proportionality & confidence honesty** — does an A/B row's copy oversell? Does a C/D row's copy get unfairly punitive vs the category-relative frame? Is any confidence state overclaimed given missing fields?
4. **False independence / framing** — does any copy leak the framework (make Bari sound like it's applying a hidden rulebook rather than reading the label)? Does the category caveat honestly explain the calorie-archetype without hand-waving?
5. **The one-read test** — would a mobile Hebrew reader understand each row's standing in 15–20s, or is any verdict ambiguous / internally contradictory?
6. **Missing-data honesty** — the KRIT SKU has brand=null and one nameHe was expanded from a packaging abbreviation; is anything presented as known that isn't?

## Output
Ranked findings (most severe first): `severity | row(barcode)/field | the problem | why it can't be defended | suggested reframe direction (not final words)`. If a class is clean, say so explicitly. This is an additive advisory review (no veto); the orchestrator folds it. End with the machine-readable return-contract JSON block (finding counts by severity + go/no-go recommendation with reason).
