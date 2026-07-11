---
id: TASK-616
title: Yogurt shelf configs have baseline_json:null -> 67 products never built into dossiers
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-11
close_reason: >
  Both yogurt configs fixed (data-agent, commit 431c30b3) + orchestrator-verified. baseline_json
  null→the live served JSONs (yogurt_{drinkable,spoonable}_frontend_v1.json, the confirmed live import
  per yogurt-*-page-data.ts:3), convention matching the 16 working configs. Agent self-verified via
  stash before/after rebuild: build_dossiers.py 620→**687 dossiers, 18/18 shelves** (+67 = 17 drinkable
  +50 spoonable), --selftest PASS both states. Orchestrator-verified: commit touched ONLY the 2 configs
  (git show), baseline_json now set in both, no score/served/other-config change. Minor cosmetic
  residual (not blocking): the two configs' `_comment` still says "baseline null" (stale 2026-07-05
  text) — non-functional; flag for a future config-comment tidy, not re-opened.
depends_on: []
blocks: []
category_id: null
origin_task: TASK-610
lesson_trigger: none
summary: >
  PD-2 join found yogurt_drinkable.json + yogurt_spoonable.json shelf configs carry baseline_json:null, so build_dossiers.py cannot reach their 67 registry products (17+50). Pre-existing config defect, unrelated to PD. Fix the two configs to point at the served baseline so all 687 registry products build into dossiers. build_dossiers.py already guards the resulting crash (skips null-baseline configs) so the other 16 shelves build.
---

# TASK-616 — Yogurt shelf configs have baseline_json:null -> 67 products never built into dossiers

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
