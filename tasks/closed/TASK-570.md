---
id: TASK-570
title: Shelf Watch pilot: weekly label-change monitor for cereals + bread (alert-only)
owner: data-agent
status: CLOSED
closed_at: 2026-07-10
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. Design doc (01_framework/operations/shelf_watch/shelf_watch_pilot_v1.md),
  canary 3/3 healthy, monitor script + selftest (03_operations/shelf_watch/shelf_watch.py), weekly
  Windows scheduled task "Bari - Shelf Watch (local)" orchestrator-confirmed via Get-ScheduledTask
  (State Ready, next run 2026-07-12 03:00). Real supervised run (twice, identical): 37/43 no_change,
  4 cosmetic, 2 GENUINE ingredient_change, 0 nutrition_drift/page_gone/scrape_failed. Agent caught
  and fixed a 30% false-positive wave before shipping (wrong DOM container, Shufersal newline
  serialization quirk, inconsistent allergen-tail scope) - re-ran to stability. Design: baseline =
  live served frontend JSON (sidesteps TASK-563 run-dir ambiguity); Shufersal-only disclosed as
  scope-fit (both corpora 100% Shufersal). OFF-clean (orchestrator grep). C0 PASS exit 0
  (orchestrator re-run). DIGEST: two real bread label changes - 2079927 (flour composition changed,
  E481 added; same barcode as the v3/v4 grade-flip product) and 7290016967074 (seeds 25.4%->8.2%,
  E471/E481 removed). ALERT-ONLY honored: no score, no served JSON touched. Bonus finding:
  01_acquire_shufersal.py 404s (stale URL template) -> TASK-582 registered.

summary: >
  Owner-approved 2026-07-10, pilot scope only. Weekly lightweight re-scrape (nutrition + ingredients) of live cereals + bread corpora via the existing retailer engines; diff vs last BSIP0 snapshot; classify cosmetic/nutrition_drift/ingredient_change/page_gone; surface in owner digest. ALERT-ONLY: never changes scores, never auto-publishes; failed scrape = discard per missing-data rule, never a drift signal. Must run as a LOCAL scheduled task (cloud lanes cannot push - Hebrew Health Scan precedent). Design doc + canary adapter-health check first.
---

# TASK-570 — Shelf Watch pilot: weekly label-change monitor for cereals + bread (alert-only)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
