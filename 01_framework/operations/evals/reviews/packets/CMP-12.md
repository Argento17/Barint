# Review packet — CMP-12
linked_prompt_id: bari-consumer-comparison-copy
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): qa-agent
source_file: bari-web/src/data/comparisons/granola_frontend_v1.json (patch_granola_verdicts_v2.py)
resolved_path: bari-web/src/data/comparisons/granola_frontend_v1.json

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Granola product insightLine + trace
expected_output_or_baseline: AUTHORED gold: existing patched insightLine
pass_criteria: Verifiable vs trace; ties/beats gold.
fail_conditions: Factual drift; jargon; unsafe wording.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.