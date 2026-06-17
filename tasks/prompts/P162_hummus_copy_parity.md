# P162 / TASK-309 — Hummus copy parity: carry + schema-strip (route: C1-GROK)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Full repo access. Staging-only. No deploy, no commit.

## Context (read first)
The 6 clean shelves went through TWO post-generate steps before Content authored them:
1. `_rescore_staging/copy_carryover.py` (TASK-305) — carry live copy by barcode for grade-UNCHANGED products.
2. `_rescore_staging/schema_strip.py` (TASK-307) — reduce each staging page to its LIVE copy field set ("Minimal publish — match live schema").
Hummus was being re-curated in parallel (P160/P161) and was LEFT OUT of both scripts. As a result
`_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json` still has ~1041 PENDING_COPY: the generator
emitted the rich v3 schema and NO live copy was carried. Content (TASK-308) authored only the 2 grade-changed dips.
Fix it the SAME way the other 6 were fixed.

## Ground truth
- Staging: `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json` (57 products).
- Live (authoritative copy source): `C:\Bari\bari-web\src\data\comparisons\hummus_frontend_v5.json` (64 products; all 57 staging barcodes exist in it).
- Live v5 per-product COPY field set (this is the target schema — match it exactly):
  - `insightLine` (every live product has it) — CARRY.
  - `rowVerdict` (present on 35/64 live products; optional — carry where live has it, omit/empty where it doesn't, matching live).
  - All `expansion.*` STRUCTURAL fields the generator already produces (nutrition, ingredients, positiveSignals, limitingFactors, unknowns, caveats, servingNote, confidenceLabel) — KEEP as generated.
  - Live v5 has NO `bariInterpretation`, NO `bestUseCases`, NO `consumerTakeaway`, NO `expansion.comparisonContext`, NO `expansion.consumerExplanation`. STRIP these staging-only fields from EVERY hummus product.

## The 2 grade-CHANGED products (do NOT clobber — already authored by Content TASK-308)
- `7290106577480` — חציל על האש בטחינה — C→**E** (live v5 copy describes grade C and is WRONG for the new grade)
- `7290106577572` — מטבוחה אמיתית — C→**D**
For these 2: PRESERVE the `insightLine` and `rowVerdict` currently in the STAGING file (Content's fresh, grade-correct copy).
Do NOT carry the old v5 copy onto them. Do NOT reset them to PENDING_COPY.

## Do this (idempotent, reproducible script preferred — e.g. `_rescore_staging/hummus_copy_parity.py`)
1. For each of the 55 grade-UNCHANGED hummus products (grade in staging == grade in v5): copy `insightLine` (and `rowVerdict` where live has it) DIRECTLY from the live v5 product by barcode.
2. For the 2 grade-CHANGED products above: keep the existing staging `insightLine`/`rowVerdict` (authored).
3. For ALL 57 products: strip the staging-only rich fields (`bariInterpretation`, `bestUseCases`, `consumerTakeaway`, `expansion.comparisonContext`, `expansion.consumerExplanation`) so the schema matches live v5.
4. Touch ONLY copy/schema fields. Do NOT change any score, grade, nutrition value, barcode, or the product set (stays 57). Do NOT touch the engine, configs, any other shelf, bari-web, or deploy.

## Then verify / gate
- `python 03_operations/page_generator/rescore_all.py --shelf hummus_shelfrel_002` is NOT what you run here (it would regen and wipe copy again). Instead re-run the existing gate on the patched staging page (same gate the other shelves pass): `python 03_operations/page_generator/gates/run_gates.py` against `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json` (use the same invocation the existing `*_gates_report.md` was produced with — check the report header).
- Confirm ALL of: G8 DATA-SANITY PASS, C10 milk Δ0 (if the gate runs it), OFF=0, score==trace OK.
- Confirm `PENDING_COPY` count in the patched file == 0.
- Confirm the 2 grade-changed dips still carry their authored (grade-E / grade-D) copy, NOT v5's old grade-C copy.
- Confirm 55 products' `insightLine` now == their v5 `insightLine`.

## Return (do NOT close — propose RETURNED)
- Counts: products patched, carried-from-v5 (should be 55), authored-preserved (should be 2), rich-fields-stripped, final PENDING_COPY (must be 0).
- Confirm scores/grades/product-set unchanged vs the pre-patch staging file (diff: 0 score moves, 0 grade moves, 57==57).
- Gate results (G8/C10/OFF/score==trace).
- Files changed (path + action + sha256).
- End with the return contract JSON (`01_framework/operations/return_contract_v1.md`): `task` (TASK-309), `proposed_status`, `artifacts[]`, `counts{}` (with the command that produced them), `commands_run[]`, `not_done[]`, `self_check`.
- Boundaries: staging-only; ONLY the hummus staging JSON (+ your repair script); no engine/config/other-shelf/bari-web; OFF-ban absolute; no commit, no deploy.
