# Review packet — EVD-01
linked_prompt_id: bari-agent-research
surface_tier: operational_agent_os
agent_owner: research-agent
reviewer (required): nutrition-agent
source_file: evidence registry EV-029 (BSIP0 fat-overwrite)
resolved_path: UNRESOLVED (use TTL freshness)

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: Source: BSIP0 nutrition parser behavior + scrape replay data
expected_output_or_baseline: GOLD: extracted finding = fat parser bug; claim must trace to cited scrape/source
pass_criteria: Every extracted claim maps to a cited source; no overclaim; ties/beats gold.
fail_conditions: Claim not supported by cited source; miscitation; scope inflation.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.