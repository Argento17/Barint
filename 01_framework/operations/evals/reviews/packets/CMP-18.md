# Review packet — CMP-18
linked_prompt_id: bari-consumer-comparison-copy
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): qa-agent
source_file: granola_frontend_v1.json rowVerdict (patch_granola_verdicts_v2.py)
resolved_path: UNRESOLVED (use TTL freshness)

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Granola product whose rowVerdict was PATCHED (authored)
expected_output_or_baseline: AUTHORED gold: patched rowVerdict string (captured 2026-06-10)
pass_criteria: Follows standing->why->catch->grade; grounded in trace; <=185 chars; ties/beats gold.
fail_conditions: Verdict contradicts grade; ungrounded claim; terse-tag regression; overlength.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.