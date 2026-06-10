# Review packet — CMP-02
linked_prompt_id: bari-consumer-comparison-copy
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): qa-agent
source_file: bari-web/src/data/comparisons/hummus_frontend_v5.json (build_glassbox_w4_frontend.py carries v4 verbatim)
resolved_path: bari-web/src/data/comparisons/hummus_frontend_v5.json

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Hummus product insightLine + BSIP2 trace for grounding check
expected_output_or_baseline: AUTHORED gold: existing carried-verbatim insightLine (captured 2026-06-10)
pass_criteria: Verifiable vs trace; ties/beats gold on D1-D4; safe wording (D5).
fail_conditions: Factual drift vs trace; framework jargon; apology register; unsafe wording >0.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.