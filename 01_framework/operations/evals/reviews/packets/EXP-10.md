# Review packet — EXP-10
linked_prompt_id: bari-consumer-editorial-insights
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): nutrition-agent
source_file: bari-web/src/lib/comparisons/milk-product-insights.ts
resolved_path: bari-web/src/lib/comparisons/milk-product-insights.ts

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Milk authored cautions[] vs panel
expected_output_or_baseline: AUTHORED gold: existing cautions[]
pass_criteria: Cautions fact-based, non-blaming; ties/beats gold.
fail_conditions: Alarmist; sodium framed as judgement; unsafe wording.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.