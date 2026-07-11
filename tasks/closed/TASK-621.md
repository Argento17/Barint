---
id: TASK-621
title: Comma-corruption completeness: patch sibling BSIP0 nutrition paths + locale-safe disambiguation (challenge DO-NOT-SHIP)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: [TASK-614]
category_id: null
origin_task: TASK-619
lesson_trigger: recurrence
lesson_outcome: regression_test
lesson_artifact: 03_operations/bsip0/scrape/_shared/bsip0_nutrition.py
lesson_validator: python 03_operations/bsip0/scrape/_shared/bsip0_nutrition.py --selftest
lesson_evidence: "Comma-corruption recurred because each retailer/pipeline path re-implemented number parsing with its own blind replace(',','.'). Root fix = consolidate onto the shared normalize_decimal_comma; a cross-vendor challenge (Codex on TASK-619) exposed that TASK-619 patched only the shared parser. TASK-621 routed 7 sibling paths (extractor, hazi_hinam/acquire, salty_snacks_real, shufersal_butter/02b, yohananof/parser, yohananof_milk/04) through the shared normalizer and hardened the 0,DDD 3-decimal case (0,123->0.123 without breaking 1,000->1000). Guard = the shared --selftest (13->17 cases). Verified: worktree diff + selftest 17/17 + edge-case spot-check (0,123/1,000/1,200/16,5 all correct). Merged 71772f36."
close_reason: "VERIFIED + merged 71772f36. Built by Codex gpt-5.6-terra (BUILD-HEAVY primary, probed live), Opus-verified (cross-vendor: Claude verifying OpenAI). Checked: (1) 7 sibling paths now import+use normalize_decimal_comma (grep + read hazi_hinam _clean_quantity); (2) shared --selftest 17/17 exit 0 on main tree post-merge; (3) edge cases 0,123->0.123, 1,000->1000, 1,200->1200, 16,5->16.5 all correct; (4) merge touched only the 7 BSIP0 .py files. Comma-corruption class now closed corpus-wide. UNBLOCKS TASK-614 re-score."
summary: >
  GPT cross-vendor challenge (verified) found TASK-619 fixed only the shared parser; 4+ sibling paths still do blind replace(',','.') BEFORE it: acquire_hazi_hinam.py:122, yohananof/parser.py:26, pipeline/extractor.py:74, salty_snacks_real/01_scrape_yoh_panels.py:56, yohananof_milk/04_parse_and_build_bsip1.py. Route them through _normalize_decimal_comma; harden 0,123 3-decimal edge case. Blocks TASK-614 re-score.
---

# TASK-621 — Comma-corruption completeness: patch sibling BSIP0 nutrition paths + locale-safe disambiguation (challenge DO-NOT-SHIP)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
