---
id: TASK-505
title: Agent OS upgrade: implement all findings from 2026-07-04 skills/agents audit
owner: orchestrator
status: CLOSED
priority: HIGH
created_at: 2026-07-04
closed_at: 2026-07-04
depends_on: []
blocks: []
category_id: null
summary: >
  Full implementation of the skills+agents audit: revive third_party skills (nesting bug), purge stale contradictions (OFF refs, ScoreChip, milk, retired red-team-agent), rebuild Marketing/SEO agent, rewrite bari-frontend-ui + bari-qa-audit, OFF-ban + two-gate hooks, CI gate extension, Hebrew copy eval harness, Design vision-in loop, telemetry self-improvement step, dependency lane, model pin fixes, loop-first autonomy codification.
close_reason: >
  All 12 workstreams delivered and verified against artifacts by the orchestrator (working tree only —
  nothing committed; owner controls the commit). (1) 13 third_party skills git-mv'd to .claude/skills/
  and CONFIRMED loading in-session (were undiscoverable at nested depth); flat-name refs updated in all
  9 agent files. (2) OFF-ban violations removed: nutrition-agent (OFF row now BANNED/DISABLED),
  research-agent:150-153 (hierarchy + do-not-cite), frontend-agent (OFF images → self-hosted TASK-478).
  (3) frontend-agent ScoreChip law = gradePalette (matches design-agent + bari-comparison-tokens.ts:2-8).
  (4) conformance skill milk carve-out retired (owner 2026-06-22). (5) category-factory: red-team-agent →
  Adversarial QA Agent, stages 8/9 reordered. (6) adversarial-qa pin sonnet→opus (critic_lane_opus_and_c3).
  (7) telemetry §8 skill-edit proposals (self-improvement loop). (8) Loop-first autonomy codified:
  /orchestrate §Loop autonomy + CLAUDE.md + memory (owner directive 2026-07-04). (9) Hooks TESTED:
  guard-off-ban.ps1 (synthetic OFF import → exit 2; clean → 0), guard-two-gate-commit.ps1 (live-fired,
  caught 4 unsigned comparison JSONs; markers = tasks/signoffs/<json>.ok). (10) CI: bari_page_gates.yml
  (conformance.py --all verified exit 0 locally + OFF census) + security_review.yml (activates on
  ANTHROPIC_API_KEY secret). (11) Subagent builds, each verified: marketing-agent v2.0 + bari-seo skill
  (old seo-audit git-rm'd; client statuses honest: GA4 MCP LIVE, GSC NEEDS-ENV, pagespeed LIVE);
  bari-frontend-ui rewritten to real frozen architecture (values cross-checked vs tokens file);
  bari-qa-audit rewritten command-first from the actual gate scripts; copy eval harness
  (03_operations/evals/copy_evals — orchestrator re-ran run_evals.py: exit 0, 22 cases, regression path
  fires) ; vision-in loop LIVE (bari-web scripts/vision-in.mjs, verified on /hashvaot/brined-cheeses,
  design-agent instruments updated); deps lane (deps skill + deps_report.py, real report emitted:
  11 npm vulns / 8 majors / 82 minors, manifests untouched). (12) Memory corrected: GA4 measurement-vs-
  property id, analytics branch name.
follow_ups: >
  Routed, not blocking close: (a) Design Agent — vision-in measured collapsed rows 180-236px vs frozen
  72/80px cap (rowVerdict two-line model postdates the frozen value; spec ruling needed). (b) Frontend —
  pre-existing quarantine violation comparison-row.tsx imports BariGradeBadge; methodology color
  triple-divergence (#AAAAAA spec vs #666C67 token vs #6B7070 shipped); StickyFilterButton documented
  but absent from code. (c) Adversarial QA — chartered fixture library 03_operations/page_generator/
  fixtures/ does not exist (skill now says MISSING). (d) hebrew_readability leak-list misses מדד עיבוד
  (eval case fl-001 = deliberate baseline FN). (e) Deps: hono high (patch now), tmp high via @lhci/cli
  (major), 14-package minor batch. (f) Owner actions to unlock: ANTHROPIC_API_KEY repo secret (security
  review CI), GSC_ACCESS_TOKEN/GSC_SITE_URL (Search Console), pip install pip-audit.
---

# TASK-505 — Agent OS upgrade: implement all findings from 2026-07-04 skills/agents audit

Scope, evidence, and per-workstream verification recorded in `close_reason` above and on the
2026-07-04 board entry. Audit source: in-session skills/agents review + SOTA research
(anthropics/skills spec, superpowers, wshobson/agents, VoltAgent, claude-seo, Anthropic engineering
posts on agent skills / multi-agent / long-running harnesses).
