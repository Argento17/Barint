---
id: TASK-458
title: Catalog go-live package: port /catalog to origin/master + nav link + og:image fixes + barcode search (P0-2 of launch report)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-02
closed_at: 2026-07-02
close_reason: >
  Merged via PR #37 (merge 346e74fa) after two-gate (Content 4cf7dc3e + Adversarial QA GO_WITH_FIXES
  9f1aaebf, 0 CRITICAL) + QA fixups 8b63576a + master-merge conflict resolution 99576c32 (P463, C0 PASS).
  Production-verified by orchestrator 2026-07-02 post-deploy (both Vercel deploys success): /catalog = 200,
  title "קטלוג המוצרים | Bari", grade badges render, OG tags present in served HTML; homepage nav carries
  href="/catalog" + "קטלוג". red_team_cleared: yes (9f1aaebf, 0 CRITICAL open).
depends_on: []
blocks: []
category_id: null
summary: >
  Ship-or-delist resolution: port catalog feature from feature/homepage-mascots to a worktree off origin/master, add header nav entry, fix blog og:image + per-page og fallbacks, add sku to catalog search haystack, reconcile sitemap (no 404 advertised). Build+lint pass, branch pushed, owner merges (tripwire 2). Consumer-facing copy goes through two-gate before owner PR.
---

# TASK-458 — Catalog go-live package: port /catalog to origin/master + nav link + og:image fixes + barcode search (P0-2 of launch report)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
