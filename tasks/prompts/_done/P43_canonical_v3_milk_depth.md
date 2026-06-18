# P43 / TASK-262 — Canonical schema v3 (milk-depth content) + generator + copy wiring (route: C1, Data Agent)

CONTEXT: Repo C:\Bari. Owner ruling: the **milk page is the content gold standard**, and the
factory's output is at granola/snacks depth, not milk depth (TASK-260 proved
`schema_carries_milk_depth=FALSE`). Widen the canonical schema to **v3 = yogurts structure +
milk content depth**, update the generator + copy wiring, and re-run the throwaway chain so
the factory CAN emit milk-depth pages. (Real milk-quality *authoring* is the next task — here
you build the schema + plumbing + a baseline fill.)

## READ FIRST — mirror the gold standard
`bari-web/src/data/milk-comparison.json`. The 4 per-product content fields to adopt:
- `consumerTakeaway` — one-line plain summary.
- `consumerExplanation` — object: `{whyRated, good[], watchOut[], context, takeaway}` (the richest editorial layer).
- `bariInterpretation[]` — array of `{key, label, score, strength, interpretation}` (per-dimension breakdown).
- `bestUseCases[]` — string array of consumer use-cases.
Page-level milk fields (`story_headline`, `story_teaser`, `philosophy_note`) already fit the
existing `_meta.page_copy` (additionalProperties) — no change needed there.

## DELIVERABLE
1. **`03_operations/page_generator/contract/page_output_schema_v3.json`** = a copy of v2 +
   the 4 fields above on each product (under `expansion` where it fits the existing shape;
   `bestUseCases` at product level). Keep ALL v2 fields (insightLine/rowVerdict/signals stay).
   v3 is additive — nothing removed. Document the deterministic-vs-authored split per field.
2. **`generate_page.py`** emits v3: populate the **deterministic** parts from the BSIP2 trace —
   `bariInterpretation[].{key,label,score,strength}` come straight from the trace's real
   dimension scores; set every **authored** text part to `PENDING_COPY`
   (`consumerTakeaway`, `consumerExplanation.*`, `bariInterpretation[].interpretation`,
   and pick `bestUseCases` deterministically only if a clean rule exists, else PENDING).
   **GUARD:** if a dimension score is missing/anomalous in the trace, emit it honestly
   (null + "data not available"), never a fabricated breakdown — milk surfaces real
   dimension scores, so the factory must too, truthfully.
3. **`build_copy_inputs.py`** fact-sheets carry the inputs the author needs for the rich
   fields (the dimension scores/labels/strengths, the drivers, null-safe nutrition).
4. **`author_copy.py` baseline + `authoring_contract.json`** updated to fill/declare the new
   fields (baseline placeholder, still law-abiding: standalone, grade=badge, sodium/fat never
   causal, no framework leakage). Bump the contract version.
5. **`merge_copy.py` + `gates/run_gates.py`** handle v3: G2 COVERAGE must check the new
   authored fields are non-PENDING; G6 COPY-SAFETY runs on them; readability on every new string.
6. **Re-run** `03_operations/spine/pipeline_e2e.py --execute` on the throwaway fixtures →
   final page validates against v3, **0 PENDING_COPY**, gates PASS, **`schema_carries_milk_depth=TRUE`**.

## ACCEPTANCE
- v3 schema file exists; v3 page validates against it; carries all 4 milk content fields populated (deterministic data real, authored text filled by baseline).
- `pipeline_e2e.py --execute` green end-to-end; final page 0 PENDING; G2/G6/readability PASS; resume + incremental still hold.
- `bariInterpretation` dimension scores trace back to the BSIP2 trace (show one product's dimension score = trace value).
- Zero OFF anywhere.

## GUARDS
- **THROWAWAY ONLY** — scratch dirs (`spine/_e2e_out`), synthetic fixtures, no live category, no consumer page, no yogurts/cereals. Do NOT touch `spine_yogurts.py`, live page JSONs, published scores, or the milk page itself (read-only reference). Do NOT change the scoring engine or any score.
- **OFF ban (TASK-238):** null stays "data could not be retrieved"; no OFF anywhere.
- v2 stays valid (additive only); import/reuse runner + existing scripts; stdlib only; no new deps.

## RETURN BLOCK
v3 schema path + the field/deterministic-vs-authored table; the generator/fact-sheet/merge
diffs (what changed); the `--execute` 8-stage dict; final page path + PENDING count (0);
the bariInterpretation→trace evidence (one dimension score = trace value); G2/G6/readability
verbatim; resume proof; zero-OFF grep. End with the machine-readable JSON return contract
(`01_framework/operations/return_contract_v1.md`); counts must include
`schema_carries_milk_depth: true`, `milk_fields_added: 4`, `pending_remaining: 0`,
`deterministic_fields`, `authored_fields`, `g2_g6_pass`, `off_introduced: 0`,
`v2_still_valid: true`. **Propose RETURNED — do NOT write CLOSED; the orchestrator verifies
and closes.**
