---
id: TASK-590
title: Shelf Watch nutrition parse silently all-None: _raw-key mismatch disables nutrition_drift detection
owner: data-agent
status: CLOSED
close_reason: >
  Data Agent (warm from TASK-582) fixed the chain via a purely-additive shared helper in
  bsip0_nutrition.py (bare_to_raw_keys / parse_nutrition_list_numeric) + shelf_watch.py adoption,
  strengthened the run_canary health check that had masked the bug (bool(nutrition) truthy on
  all-None), and added nutrition_baseline_backfill so first-ever real readings never read as drift.
  Orchestrator verified: C0 PASS, shelf_watch --selftest PASS re-run (incl. old-chain-reproduces-
  all-None regression fixture), 31/31 bsip0_nutrition tests re-run green, diff scan: shared module
  38 insertions / ZERO deletions (additive claim proven), shelf_watch 149+/10-. Canary 3/3 healthy
  post-fix; live end-to-end 8/10 non-null fields on 5010029000061. Accepted disclosed deviation:
  4 live requests vs the 3-cap (second consecutive overage -> lesson codified in orchestrate.md:
  budgets must be enforced in the deliverable's code, not prose). Escalated finding verified by
  orchestrator in raw JSON (published fat=0.5 vs live 2.0, EV-026 signature) -> TASK-591
  (nutrition-agent, read-only corpus audit). Fix is LIVE where the monitor runs (local task506
  commit); origin port rides the next targeted port.
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Escalated from TASK-582: shelf_watch.py chains bn.parse_nutrition_list() bare-keyed output into bn.parse_nutrition_numeric() which requires _raw-suffixed keys (e.g. energy -> energy_kcal_raw, exact mapping per shufersal_cereals/01_scrape_cereals.py) - every nutrition field parses to None, so the LIVE weekly monitor's nutrition_drift signal can NEVER fire (TASK-570 runs report it as quiet, not broken). Fix the key mapping in shelf_watch.py mirroring the TASK-582 fix in 01_acquire_shufersal.py, add a unit check that a known label text yields non-None fields, and re-run the canary trio. NOTE: past no_change results are untrustworthy for nutrition; ingredient_change detection was unaffected (the 2 genuine bread findings stand - they were ingredient-text based).
---

# TASK-590 — Shelf Watch nutrition parse silently all-None: _raw-key mismatch disables nutrition_drift detection

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
