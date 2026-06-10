---
id: TASK-159
title: Cheese /hashvaot index-card photo — wire missing photo prop + add cheese.jpg theme asset (visual parity with 6 peers)
owner: design-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC close-gate PASS — both claims verified against artifacts. (1) Asset exists: public/hashvaot/themes/cheese.jpg = 85,791 bytes (matches the reported GET 200 length exactly). (2) Prop wired: featured-cheese-intelligence-card.tsx:61 passes theme={{ accent: '#D8CBB0', photo: '/hashvaot/themes/cheese.jpg' }}, bringing the cheese index card to parity with the 6 peers that carry a /hashvaot/themes photo. Display-only; no data/score touched."
roadmap_impact: false
depends_on: [TASK-156]
blocks: []
category_id: cheese_spreads
summary: >
  Root cause: the /hashvaot index cheese card passed no photo prop while 6 peers do. Fix: featured-cheese-intelligence-card.tsx passes photo /hashvaot/themes/cheese.jpg; new asset public/hashvaot/themes/cheese.jpg (85,791 bytes). Screenshot-verified live (GET 200, full-grid + closeup + mobile375; layout pixel-identical to peers).
---

# TASK-159 — Cheese /hashvaot index-card photo — wire missing photo prop + add cheese.jpg theme asset (visual parity with 6 peers)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
