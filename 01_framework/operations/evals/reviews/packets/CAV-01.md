# Review packet — CAV-01
linked_prompt_id: bari-consumer-category-caveat
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): nutrition-agent
source_file: bari-web/src/lib/comparisons/milk-comparison-page-data.ts
resolved_path: bari-web/src/lib/comparisons/milk-comparison-page-data.ts

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Milk category engine behavior (frozen run_005; whole/4%/goat at top)
expected_output_or_baseline: AUTHORED gold: existing milk category caveat (הערת קטגוריה), captured 2026-06-10
pass_criteria: Caveat grounded in REAL engine behavior; ties/beats gold; no jargon.
fail_conditions: Generic caveat not tied to engine behavior; contradicts frozen invariant; unsafe wording.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.