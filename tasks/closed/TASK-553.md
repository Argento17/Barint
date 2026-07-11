---
id: TASK-553
title: build_copy_inputs.py hygiene: code the superlative margin gate + de-hardcode S_VERBATIM
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-10
closed_at: 2026-07-11
close_reason: >
  Both fixes delivered and orchestrator-verified. (1) Margin gate coded in superlatives_for()
  (all 5 policy conditions; Rule-5 tier-2 cannot-compute explicitly flagged in docstring, not
  silently skipped): cereals tokens 3->1 - rice-apple lowest_sugar REVOKED (gap 0.4g < threshold
  2.61g, the TASK-550 RT-6 case) and Vitabix lowest_kcal revoked (gap 9.0 < 9.8); orchestrator
  independently walked both scratch fact-sheets: cereals grants only highest_protein, yogurt only
  lowest_sugar. (2) S_VERBATIM global GONE from shared code; per-category s_verbatim/<slug>.json;
  s_products derived from page-JSON grade=="S" - orchestrator cross-checked yogurt page: exactly
  2/52 (7290112336712, 7290110565527), matches; cereals _meta.s_products == []. Extracted Hebrew
  strings verified byte-identical to the old signed-off global (join-normalized). Tests 9/9
  re-run independently. C0 PASS exit 0. Scratch-only, freeze respected, no live JSON touched.
  NOTE (pre-existing, carried not fabricated): the _source doc pointer
  02_products/yogurt_system/s_grade_explanations_v1.md does not exist in the tree - it was a stale
  comment in the old code; real provenance = old S_VERBATIM global in git history. Commit on task506.
depends_on: []
blocks: []
category_id: null
summary: >
  Two follow-ups surfaced by TASK-550's red-team. (1) superlatives_allowed_policy_v1.md rule 3 (margin >=10% of corpus range over 2nd place) is written but NOT coded; retroactively it would revoke rice-apple's thin lowest_sugar token (0.4g gap on a 26.1g range). (2) S_VERBATIM is a module-level global in the SHARED build_copy_inputs.py hardcoded with the YOGURT category's S-grade barcodes — it leaked phantom s_products into every category's fact sheet _meta. A minimal filter fix was applied; the architecture (per-category data hardcoded in a shared script) violates the uniform-baseline doctrine and needs a real cleanup.
---

# TASK-553 — build_copy_inputs.py hygiene: code the superlative margin gate + de-hardcode S_VERBATIM

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Dispatch log
- 2026-07-11 03:xx (unattended orchestrate run) — dispatched Data Agent (claude-sonnet pin,
  background). Capability = BUILD-LIGHT; **fallback activation logged (Router v5 Layer-0 inv. 6):
  primary Codex terra SKIPPED — trigger = unattended-run operating constraint (native Sonnet only;
  cloud/CLI lanes queued for supervised morning).** Scratch outputs only — product-descriptions
  freeze respected; no live JSON regeneration. No commit; orchestrator commits post-verification.
