---
id: TASK-585
title: Router v5 PIN-AT-AUTH: pin Codex tiers post-OAuth, revive Gemini lane via agy, fix codex --search invocation
owner: orchestrator
status: CLOSED
closed_at: 2026-07-10
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  All three halves verified live by the orchestrator. (1) Codex pinned post-owner-OAuth:
  gpt-5.6 sol/terra/luna onto BUILD-HEAVY/BUILD-LIGHT+ENG-RESEARCH/GRUNT, selftest-codex
  PASS (live subscription PONG). (2) Gemini lane REVIVED: root cause of every prior failure
  was agy 1.1's changed CLI surface (bare -p prints help; --print is headless) - auth was
  alive all along, no owner action needed; runner repointed npm-gemini -> agy.exe, primary
  pinned "Gemini 3.1 Pro (High)" (agy models lists 3.5 Flash L/M/H + 3.1 Pro L/H),
  selftest-gemini rewritten to stdout-token through the real runner - PASS 8.9s answering
  as the pinned model. (3) Web-search invocation fixed and live-verified: codex exec -c
  tools.web_search=true (returned a real current answer on luna); --search does not exist
  on the exec subcommand. Folded item done: dispatch_journal CLOUD_LANES annotated v4.2
  history. Law doc footnotes 1+2 rewritten to final truth; selftest-table byte-match green
  after every edit; route 14/14. Origin port: branch task585-lane-pins pushed, owner merges.
  Build note: two shell-heredoc Unicode corruptions self-caught and fixed (known Windows
  trap; used Edit/python io for the fixes).

summary: >
  Follow-up to TASK-583. After owner runs codex login (ChatGPT OAuth): read exact Codex tier IDs, replace PIN-AT-AUTH placeholders in capability_router_v5.md Layer 2 AND dispatch.py MODEL_BINDING together (selftest-table enforces byte-match), smoke-test build_heavy/build_light/grunt lanes. Gemini: repoint VISION-LONGREAD to agy.exe (v1.1.0, %LOCALAPPDATA%/agy/bin), fix headless flags, sentinel selftest green (failed 2026-07-10, flaky since 07-08), pin model ID. Fix ENGINEERING-RESEARCH: --search is top-level-only on codex-cli 0.144.1.
---

# TASK-585 — Router v5 PIN-AT-AUTH: pin Codex tiers post-OAuth, revive Gemini lane via agy, fix codex --search invocation

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
