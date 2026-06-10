# Review packet — CMP-14
linked_prompt_id: bari-consumer-editorial-insights
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): nutrition-agent
source_file: bari-web/src/lib/comparisons/milk-product-insights.ts
resolved_path: bari-web/src/lib/comparisons/milk-product-insights.ts

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Milk pid 7290000051352 — positives[] array
expected_output_or_baseline: AUTHORED gold: positives ['רשימת רכיבים קצרה: חלב בלבד', 'חלבון טבעי סביר ל־100 מ"ל', 'מתאים כבסיס יומיומי ולבישול']
pass_criteria: Each positive verifiable against milk panel; ties/beats gold.
fail_conditions: Unsupported positive; invented nutrient.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.