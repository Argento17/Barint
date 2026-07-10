---
id: TASK-585
title: Router v5 PIN-AT-AUTH: pin Codex tiers post-OAuth, revive Gemini lane via agy, fix codex --search invocation
owner: orchestrator
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Follow-up to TASK-583. After owner runs codex login (ChatGPT OAuth): read exact Codex tier IDs, replace PIN-AT-AUTH placeholders in capability_router_v5.md Layer 2 AND dispatch.py MODEL_BINDING together (selftest-table enforces byte-match), smoke-test build_heavy/build_light/grunt lanes. Gemini: repoint VISION-LONGREAD to agy.exe (v1.1.0, %LOCALAPPDATA%/agy/bin), fix headless flags, sentinel selftest green (failed 2026-07-10, flaky since 07-08), pin model ID. Fix ENGINEERING-RESEARCH: --search is top-level-only on codex-cli 0.144.1.
---

# TASK-585 — Router v5 PIN-AT-AUTH: pin Codex tiers post-OAuth, revive Gemini lane via agy, fix codex --search invocation

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
