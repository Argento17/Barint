---
id: TASK-508
title: Registry drift: snacks nameHe stale (חטיפים מלוחים → חטיפי דגנים)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-04
closed_at: 2026-07-05
close_reason: >
  Fixed + audited + orchestrator-verified (2026-07-05 unattended run). snacks.ts:11 nameHe
  'חטיפים מלוחים' → 'חטיפי דגנים' — commit 2c27c68c on fix/task508-registry-namehe (worktree
  C:\bari_wt_t508, off origin/master c6993b48); orchestrator eyeballed the diff: exactly 1 file,
  1 line. Audit denominator verified: 7/7 files in registry/categories/ checked, drift 1/7
  (snacks only); 0 remaining 'מלוחים' in registry. C0 validate_return.py VERDICT PASS exit 0.
  New value matches the live identity confirmed by TASK-507's Content gate. Branch NOT pushed —
  push+PR queued for supervised morning kick (unattended no-push decision).
depends_on: []
blocks: []
category_id: snacks
summary: >
  Typed registry src/lib/comparisons/registry/categories/snacks.ts nameHe is 'חטיפים מלוחים' (salty snacks — the retired/fabricated identity) but the live /hashvaot/snacks page and its FeaturedSnacksIntelligenceCard use 'חטיפי דגנים' (cereal/grain bars, post TASK-228 rebuild). Surfaced by TASK-507. Any code reading registry nameHe for snacks renders the wrong Hebrew identity. Fix registry to live identity; audit other categories for the same drift. Data/registry only — no scoring change.
---

# TASK-508 — Registry drift: snacks nameHe stale (חטיפים מלוחים → חטיפי דגנים)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
