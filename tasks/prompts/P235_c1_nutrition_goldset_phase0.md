(route: C1)  # Sonnet via Nutrition Agent native subagent — nutrition-judgment piece, not a Sonnet-default

# P235 — Gold Set Phase 0: nutrition grounding + anchor seed proposal (TASK-349)

You are the Nutrition Agent (C1-Sonnet). This is the nutrition-JUDGMENT piece of Phase 0 for the
Bari Gold Set (read `tasks/TASK-349.md` first). The Gold Set is an expert-rubric ACCURACY gate
(sibling to Shadow1, which only catches stability/regression). It changes NO published score and NO
engine code — disagreements between a gold label and the engine are FINDINGS routed back to you, never
auto-fixes. Stay strictly read-only over the engine and published scores.

## Repo / paths
- Repo root: `C:\Bari`
- Engine: `03_operations/bsip2/proto_v0/src/score_engine.py` (dim_scores defined ~L3376; grade banding),
  `constants.py` (thresholds). 10 dimensions: processing_quality, nutrient_density, calorie_density,
  glycemic_quality, protein_quality, additive_quality, satiety_support, fat_quality,
  regulatory_quality, whole_food_integrity.
- Shadow harness + registry: `03_operations/shadow/shadow_backtest.py`,
  `03_operations/shadow/shadow_registry_v1.json` (12 registered corpora, ~704 products).
- Existing shadow tools to check for prior art: `03_operations/shadow/golden_diff_*.py`,
  `engine_invariants.py`.

## Objective — deliver a Phase-0 analysis note
Write ONE markdown file: `03_operations/shadow/goldset/phase0_nutrition_grounding.md`
(create the `goldset/` dir). It must contain:
1. **Grade cutoffs map** — the exact score→grade boundaries (S/A/B/C/D/E) and the data_sufficiency /
   confidence-ceiling model, cited at file:line in score_engine.py/constants.py. This tells us how an
   "expected grade band" maps to an expected score range.
2. **Prior-art check** — confirm (with file:line evidence) whether any existing artifact already
   encodes expert/expected ground-truth grades (not engine self-output). State plainly: does a gold
   set already exist in any form, or not? (golden_diff_*.py and engine_invariants.py are EV-diff /
   invariant tools — say whether they qualify.)
3. **Anchor seed proposal — ~30 products** drawn from the registered corpora. For each: pid, corpus,
   product name, the EXPECTED grade band + expected score range + 2–4 per-dimension expectations
   (direction: high/medium/low), and a one-line rubric RATIONALE grounded in first-principles
   nutrition + the physical label — NOT in any Bari score. Each rationale names its basis
   (USDA FDC / BSIP0 panel / direct product scrape). Compose the 30 as: ~10 clearly-good (whole-food,
   low additive, favorable macro), ~10 clearly-poor (high sugar/sat-fat/ultra-processed), ~10
   genuinely AMBIGUOUS / adversarial mid-tier that stress the engine. Mark which corpus each comes from.
   You may use the P233 candidate extract (top/bottom by score per corpus) as a STARTING shortlist, but
   derive each expected band from nutrition first principles, never by copying the engine's score.

## Boundaries / guards
- READ-ONLY over engine + published scores + all corpora. You only WRITE the one analysis .md file.
- Do NOT change scores, engine code, configs, or any page JSON. Do NOT run a rescore that mutates state.
- OFF ban (absolute): never source nutrition/ingredients/names from Open Food Facts, anywhere.
- Expected bands are RANGES (grade band + score range + dimension direction), never exact target scores.
- This is a finding/measurement artifact — frame disagreements as questions for review, not fixes.

## Return format
Path + sha of the .md, the grade-cutoff citations, the prior-art verdict (yes/no + evidence), and the
30-row seed table summarized (count per good/poor/ambiguous + per-corpus spread). End with the contract.

## Do not close — propose RETURNED.

```json
{
  "task": "P235",
  "proposed_status": "RETURNED",
  "artifacts": [{"path": "03_operations/shadow/goldset/phase0_nutrition_grounding.md", "action": "created", "sha256": "<hash>"}],
  "counts": {"seed_products": "30/30 (good:10 poor:10 ambiguous:10)", "corpora_covered": "<k>/12"},
  "commands_run": [{"cmd": "<grep/read commands for grade cutoffs + prior-art>", "exit_code": 0}],
  "not_done": [],
  "self_check": "grade cutoffs cited at file:line and prior-art verdict stated with evidence: <observed>"
}
```
