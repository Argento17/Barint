---
id: TASK-428
title: /hashvaot index card titles — derive from approved comparison-pages.json hero.title (no numbers)
owner: frontend-agent
status: CLOSED
priority: HIGH
closed_at: 2026-07-01
close_reason: >
  Deployed (commit b91c75b6, pushed origin/master -> Vercel). Owner review #2 (simpler titles,
  key insight, no numbers) was applied to the comparison-page heroes earlier but the /hashvaot INDEX
  cards hardcoded old numbered titles (e.g. "גרנולה ומוזלי: 53 מוצרים, פער של 47 נקודות") in the
  featured-*-intelligence-card*.tsx components — a source missed in the first pass, so the owner still
  saw old numbered titles on the index. C1-CURSOR (P266) repointed all 15 comparison cards at
  getComparisonPageChrome(slug).hero.title (single source of truth = QA-approved, digit-free titles),
  including milk and protein-bars. magnesium left as-is (title already digit-free). Verified by
  orchestrator against artifacts: 0 approved hero.titles contain digits; commit b91c75b6 = exactly 15
  card files, 0 others; npm run build exit 0, /hashvaot compiles. Note: cursor lane also produced an
  out-of-scope stripCardDigits() runtime hack on the magnesium card (reverted) and initially appeared to
  touch cheese_frontend_v4.json — that turned out to be the concurrent, legitimate TASK-426 cheese fix
  (cede5e54), left intact.
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
prompt: tasks/prompts/_done/P266_hashvaot_card_titles.md
---

# TASK-428 — /hashvaot index card titles (no numbers, approved key-insight titles)

Follow-up remediation to owner review item #2. The comparison-page hero titles were rewritten and
deployed, but the /hashvaot INDEX cards render titles hardcoded in the
`featured-*-intelligence-card*.tsx` components — never updated — so the live index still showed the
old numbered titles the owner flagged. Fix: point every comparison card at the approved
`getComparisonPageChrome(slug).hero.title`. Deployed b91c75b6.
