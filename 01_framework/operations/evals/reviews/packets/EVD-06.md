# Review packet — EVD-06
linked_prompt_id: bari-agent-research
surface_tier: operational_agent_os
agent_owner: research-agent
reviewer (required): nutrition-agent
source_file: external integration layer (TASK-170): OFF / DSLD / literature clients
resolved_path: UNRESOLVED (use TTL freshness)

rubric: 01_framework/editorial/hebrew_content_golden_eval_v1.md
dimensions: D1 factual_accuracy · D2 consumer-facing · D3 assertive/no-apology · D4 framework-invisible · D5 safe-wording

input_artifact_or_context: A claim extracted from an external read-only source (e.g. OFF additive entry)
expected_output_or_baseline: GOLD: claim matches the external record; Tzameret treated as DIRECTIONAL ONLY
pass_criteria: Claim matches source record; Tzameret never cited as authoritative; ties/beats gold.
fail_conditions: Tzameret used as authority; claim diverges from external record.

REVIEWER VERDICT (record in pairwise_verdicts_v1.yaml): PASS | FAIL
Confirm: no banned phrase, no framework term, no apology register, claims grounded.