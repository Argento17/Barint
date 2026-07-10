---
id: TASK-507
title: Explore-next module on leaf comparison/blog pages (stop paid-traffic dead-ends)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-04
closed_at: 2026-07-04
close_reason: >
  Built + four-gate verified. Content ✅ (heading "עוד השוואות" signed off; caught+fixed misleading CTA
  לכל ההשוואות→להשוואה). Product ✅ (shelf-scoping D1 + family-cap D2). Design ✅ CONFORMS (0 new WCAG, tokens
  trace real, golden-page not-drift). Adversarial QA: sole blocker HIGH-1 (category prop → silent bread/cheese
  expansion regression) RESOLVED — orchestrator independently confirmed 0 category-prop diff vs origin/master on
  all 4 formerly-wired files + dedicated exploreNextCategoryId prop wired (19 refs); Frontend runtime-proved
  DEFAULT_NUTRITION restored (cheese green, bread 40%). Suite green (20/20 task507 spec, 10/10 smoke, 0 new a11y,
  3 visual baselines refreshed+stable, lint/build clean). Branch frontend/task507-explore-next @ c67c5c7a pushed;
  PR open for OWNER merge (consumer-facing deploy = owner's call, tripwire #2). Spun off: TASK-508 (snacks registry
  drift), TASK-509 (dormant nutrition-config question), TASK-510 (live category-hero a11y defect).
depends_on: []
blocks: []
category_id: null
summary: >
  Add a canonical related-comparisons ('עוד השוואות') navigation module to the bottom of leaf /hashvaot comparison pages and /blog posts, so social/paid traffic landing directly stops dead-ending at 1.0 pages/session (vs 7-11 for hub entries). Data-driven from the category registry; conforms to the golden (brined-cheeses) template; any new copy routes through the two-gate; must NOT touch frozen rowVerdict/insightLine/expansion copy.
---

# TASK-507 — Explore-next module on leaf comparison/blog pages (stop paid-traffic dead-ends)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
