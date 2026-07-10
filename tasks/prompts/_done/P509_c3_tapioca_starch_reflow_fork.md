# P509 / RT-2H1 modified-starch classifier fix + cross-category re-flow — independent challenge (route: C3)

You are C3, the orchestrator's outside-the-family independent challenger. This is a TRIPWIRE-1 fork (a fix that changes PUBLISHED scores across live categories). Challenge the reasoning; propose findings; you do NOT decide or implement. Return a crisp recommendation the orchestrator will weigh against Nutrition's co-sign before surfacing to the owner.

## Context — a scoring-engine detection bug found mid-build (yogurt TASK-515/515A)
Bari scores packaged foods; an "emulsifier complexity" penalty (ECS-v1) subtracts points when a product carries stabilizer/emulsifier additives. A classifier bug was found:

- `ingredient_taxonomy.py` matches modified starch by CONTIGUOUS substring: "עמילן מעובד" (modified starch) → classified `modified_starch`. But the source-qualified Hebrew label "עמילן טפיוקה מעובד" (modified TAPIOCA starch) is not a contiguous match (the word "טפיוקה"/tapioca sits between), so it falls through to the bare token "עמילן" (starch) and is **mis-classified as `native_starch` (benign)** — worse than an undetected miss, it's an active flip to the wrong bucket.
- Effect: the ECS `modified_starch_stabilizer` −3 penalty never fires → affected products score ~3 points too HIGH.

## Measured impact (sandbox, engine reverted byte-identical; additive_quality delta 0, ECS penalty delta +3/+2/+0)
- **27 live-indexed products** carry the miss across 5 pages: yogurt_drinkable 3, yogurt_spoonable 13, hummus 3, cakes_hard_cookies 7, crackers 1.
- **6 cross a published grade boundary** (all DOWN — more accurate/penalized): drinkable 573737 B→C + 938396 C→D; spoonable 7290010471669 D→E + 7290110578572 C→D + 7290119377404 B→C; crackers 7290011489595 C→D.
- The 2 yogurt pages are pre-launch (not yet deployed); hummus/cakes/crackers are LIVE on the site.
- Proposed fix: source-word-tolerant matcher `r"עמילן(?:\s+\S+){1,2}\s+מעובד"` → modified_starch, preserving a `r"לא\s+מעובד"` negative lookaround so genuinely-native "עמילן טפיוקה לא מעובד" still resolves native.

## Bari governing rules you must weigh
- "NEVER CUT CORNERS" + honest-data-over-grade-continuity: a real on-label additive being uncounted = over-generous score; fixing it is honest.
- Re-flow policy: "nothing is frozen; every live category re-scores on every scoring switch" — but an owner-initiated spine_flip is the expected re-flow vehicle; this is an orchestrator-found bug fix, not an owner spine_flip.
- Tripwire 1 (owner decision): "an agent would change published scores / scoring philosophy." Engine changes never auto-deploy; frontend JSONs are regenerated + owner-gated per category.

## Challenge questions (answer each, take a position)
1. Is fixing the classifier the correct call, or is there a defensible case to ship yogurt with the understated grades + acknowledge (Hard Rule 10) and defer? Weigh honest-data vs mid-launch scope.
2. Is the orchestrator's proposed split sound: APPLY the engine fix + re-score the pre-launch yogurt pages now (no published score protected), while the LIVE 3-category re-flow (hummus/cakes/crackers regenerate + redeploy) is queued for explicit owner approval? Or does applying the engine fix at all (which changes how live pages WOULD score vs their committed JSON) itself require owner sign-off before touching the engine?
3. Risk review of the fix pattern: does the `{1,2}`-word window risk false positives spanning a comma/ingredient boundary? Are there OTHER source-qualified additive variants (gelatin/pectin/lecithin source forms) likely to have the same contiguous-match bug and be worth scanning in the same pass?
4. Is 6 grade crossings across 5 categories a proportionate, defensible correction, or a signal the ECS −3 penalty itself is too blunt for modified starch (a common, arguably mild thickener)?

## Return
A crisp position on Q1-Q4 + a single recommended path (fix-now-split / fix-all-with-owner-approval / defer-and-acknowledge) with the one-line rationale, and any guardrail the fix must carry. No implementation. End with the machine-readable return contract JSON.
