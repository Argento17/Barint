# Review packet — CAV-04
linked_prompt_id: bari-consumer-category-caveat
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): nutrition-agent
source_file: bari-web/src/lib/comparisons/cereals-page-data.ts
resolved_path: bari-web/src/lib/comparisons/cereals-page-data.ts

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Cereal/granola engine behavior incl. known sodium-scoring gap (TASK-189)
expected_output_or_baseline: AUTHORED gold: existing cereals category caveat
pass_criteria: Grounded in real behavior; ties/beats gold.
fail_conditions: Claims sodium fully penalized when engine gap exists; overstated.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.