---
id: TASK-586
title: Align 9 governed docs to Capability Router v5 (orchestrate.md + 8 agent files reference retired P-number dispatch)
owner: orchestrator
status: CLOSED
closed_at: 2026-07-10
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. All 9 governed docs realigned from Router v4.2 to Capability
  Router v5 (13 edit hunks): orchestrate.md band table + P-number/route-tag flow replaced with
  Layer-1 capability questions and named dispatch.py lane functions, fallback discipline with
  registry logging, grunt re-verify + C0-supremacy lessons preserved; 8 agent files got
  capability-aligned frontmatter (QA agent correctly re-pinned opus per critic_lane ruling).
  C7 containment CRITICAL on all 10 .claude writes adjudicated per protocol: orchestrator read
  the orchestrate.md diff in full and spot-checked agent frontmatter diffs personally.
  Orchestrator independent grep: the only remaining retired-lane terms are the kill notices
  themselves ("killed forever" statements) - correct and desired. Note: the agent files carried
  pre-existing uncommitted TASK-505-era edits (flagged by the agent on marketing-agent.md,
  present since session start on all); committed together with a commit-message note rather
  than left dangling. Every session now learns v5 from CLAUDE.md (hard-loaded) + memory;
  /orchestrate and all agent personas now teach it too.

summary: >
  TASK-583 not_done item: .claude/commands/orchestrate.md and 8 .claude/agents/*.md files still document the retired v4.2 P-number/route-tag CLI dispatch flow (grok/cursor/deepseek era). Rewrite the routing sections to reference capability_router_v5.md Layer 1/2 and the new dispatch.py entry points. Also refresh lane memories.
---

# TASK-586 — Align 9 governed docs to Capability Router v5 (orchestrate.md + 8 agent files reference retired P-number dispatch)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
