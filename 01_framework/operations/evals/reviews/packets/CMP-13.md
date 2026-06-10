# Review packet — CMP-13
linked_prompt_id: bari-consumer-editorial-insights
surface_tier: consumer_facing
agent_owner: content-agent
reviewer (required): qa-agent
source_file: bari-web/src/lib/comparisons/milk-product-insights.ts
resolved_path: bari-web/src/lib/comparisons/milk-product-insights.ts

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Milk pid 7290000051352 (natural milk) + BSIP2 context
expected_output_or_baseline: AUTHORED gold: whatMatters = 'כאן הסיפור הוא מבנה חלב טבעי — חלבון, שומן — בלי שכבות פורמולציה.'
pass_criteria: Candidate ties/beats gold on D1-D4; no unsafe wording (D5).
fail_conditions: Factual drift vs trace; framework jargon; apology register; unsafe wording >0.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.