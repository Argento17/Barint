# Review packet — EXP-05
linked_prompt_id: bari-consumer-editorial-insights
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): nutrition-agent
source_file: bari-web/src/data/comparisons/hummus_frontend_v5.json (carried via build_glassbox_w4_frontend.py)
resolved_path: bari-web/src/data/comparisons/hummus_frontend_v5.json

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Hummus product positiveSignals[] content vs trace
expected_output_or_baseline: AUTHORED gold: existing carried-verbatim positiveSignals[]
pass_criteria: Each signal verifiable vs trace; ties/beats gold.
fail_conditions: Unsupported claim; stale claim referencing old score/position; unsafe wording.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.