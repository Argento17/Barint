---
id: TASK-574
title: Strip raw internal fields from 6 served comparison JSONs (_scoring_trace, nutrition_per_100g, duplicate name_he/image_url)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-10
closed_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. Wave 1: 561 raw internal keys (_scoring_trace, nutrition_per_100g,
  duplicate name_he/image_url) stripped across 245 products in 6 served JSONs; orchestrator's
  independent structural diff = 0 value changes, 0 non-target removals. Wave 2 (evidence-classified):
  stripped unread internals (_d4_copy_flag, product-level category/consumerExplanation — sole reader
  consumer-explanation-view.ts imported nowhere; protein format/protein_per_100g/protein_per_bar/
  bar_weight_g/show_per_bar); whitelisted genuinely-read display fields as optional (juices top-level
  generatedAt/totalProducts, read at juices-page-data.ts:45-77). Two agent deviations adjudicated:
  (1) _score_correction removal (2 cookies products) ACCEPTED — provenance survives at
  02_products/cookies_coffee/staging/task393_rescore/cookies_coffee_DEPLOY.json + TASK-244/371;
  (2) displayTitle strip from protein: orchestrator ordered restore based on a SUBSTRING-GREP FALSE
  POSITIVE (comparison-row.tsx imports bari-product-thumbnail.tsx, not the milk-only
  product-thumbnail.tsx); agent refused with correct evidence, refusal UPHELD on orchestrator
  re-verification — desired behavior, schema whitelist for displayTitle correctly NOT added.
  G1 SCHEMA 6/6 PASS in BOTH trees (orchestrator re-ran, not agent-claimed): local C:\Bari and
  worktree C:/bari_wt_574. G1 overall now 16/16 across all shelves' schema gate. Origin port:
  branch task574-raw-fields commit e3512d1e pushed (local and origin file versions differ; strip
  re-applied to origin's versions, never copied). Return contract C0 PASS exit 0 (6 gates-report
  hashes mechanically refreshed after orchestrator gate re-runs regenerated them — known C2
  timestamp-drift class; data-file hashes untouched and matching). Owner merge of the PR pending;
  unblocks TASK-565 (run_gates in CI) pending the TASK-563 owner decision.
summary: >
  Found by TASK-564 shape census: chocolate_bars, chocolate_tablets, cookies_coffee, juices, protein_bars, snacks ship raw build-path fields in consumer-served JSON (internal _scoring_trace {category, protein_g}, raw nutrition_per_100g duplicating expansion.nutrition, duplicate name_he/image_url). Display-neutral cleanup of governed files: needs its own diff-verified pass (0 rendered-field changes) + both page gates before commit. Blocks the last 6 shelves of G1 and therefore TASK-565 (run_gates in CI). Do NOT whitelist these fields in the schema.
---

# TASK-574 — Strip raw internal fields from 6 served comparison JSONs (_scoring_trace, nutrition_per_100g, duplicate name_he/image_url)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
