# Review packet — CMP-17
linked_prompt_id: bari-consumer-comparison-copy
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): qa-agent
source_file: bari-web/src/data/comparisons/cereals_frontend_v2.json rowVerdict (build_cereals_008_frontend.py UPDATED_COPY)
resolved_path: bari-web/src/data/comparisons/cereals_frontend_v2.json

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Cereals product rowVerdict (008 run) + trace
expected_output_or_baseline: AUTHORED gold: existing literal rowVerdict string (captured 2026-06-10)
pass_criteria: Follows standing->why->catch->grade; grounded in trace; ties/beats gold.
fail_conditions: Verdict contradicts grade; ungrounded claim; terse-tag regression.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.