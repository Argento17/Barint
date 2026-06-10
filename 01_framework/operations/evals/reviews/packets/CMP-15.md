# Review packet — CMP-15
linked_prompt_id: bari-consumer-editorial-insights
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): qa-agent
source_file: bari-web/src/lib/comparisons/milk-product-insights.ts
resolved_path: bari-web/src/lib/comparisons/milk-product-insights.ts

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Milk plant-alternative product — cautions[] array
expected_output_or_baseline: AUTHORED gold: cautions (existing strings, captured 2026-06-10)
pass_criteria: Cautions fact-based, non-alarmist; ties/beats gold.
fail_conditions: Alarmist/blaming register; sodium presented as judgement not fact.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.