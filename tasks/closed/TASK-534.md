---
id: TASK-534
title: Codify white-background image treatment (blendWhite) as a rule, apply to yogurt pages
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-08
closed_at: 2026-07-08
close_reason: >
  Frontend Agent (Sonnet-pinned) codified blendWhite into a single declaration
  (bari-web/src/lib/comparisons/thumbnail-blend-white-categories.ts →
  shouldBlendWhiteForCategory(), backed by BLEND_WHITE_CATEGORIES set = magnesium +
  yogurt-spoonable + yogurt-drinks), replacing the scattered inline `category === "magnesium"`
  boolean; wired both comparison-row.tsx and the GLP-1 guide shortlist; documented in the
  component doc-comment + frontend_integration_checklist_v1.md. ORCHESTRATOR VERIFIED: read the
  config file + both callsites (grep confirmed shouldBlendWhiteForCategory wired at
  comparison-row.tsx:190 and yogurt-glp1-guide-page.tsx:127); confirmed yogurt pages pass the
  exact slugs "yogurt-spoonable"/"yogurt-drinks"; re-rendered localhost (157 white-tile classes
  now present on /hashvaot/yogurt, 0 before). DESIGN AGENT VISUAL GATE = PASS: measured geometry
  on 5 routes — yogurt 78/78 + yogurt-drinks 20/20 + magnesium 18/18 tiles white, hummus control
  35/35 cream (byte-identical to pre-fix), GLP-1 shortlist 4/4 white; border(1px)+shadow retained,
  tile size 56px/radius 18px unchanged, no drift. Two pre-existing WCAG contrast bugs surfaced
  during the pass (site-wide eyebrow label + yogurt insight pills) — independent of this diff
  (proven via control-page parity), split out to TASK-537, not a blocker for this task.
depends_on: []
blocks: []
category_id: null
summary: >
  Owner review 2026-07-08: white product photos render as white boxes inside cream tiles on yogurt pages. blendWhite prop exists (bari-product-thumbnail.tsx, built for supplements) but is manual opt-in and yogurt never enabled it. Codify: category-config-driven or auto-detected rule so this never recurs by omission; apply to /hashvaot/yogurt + yogurt-drinks; Design Agent conformance check after.
---

# TASK-534 — Codify white-background image treatment (blendWhite) as a rule, apply to yogurt pages

CLOSED 2026-07-08 — see close_reason. Codified via shouldBlendWhiteForCategory(); Design visual gate PASS; pre-existing contrast findings split to TASK-537.
