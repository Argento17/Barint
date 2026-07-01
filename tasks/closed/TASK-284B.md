---
id: TASK-284B
title: Shadow re-score: EV-096 (seed_pen=5) + EV-097 (two-tier PHVO ceiling) behind default-OFF flag; diff vs approved baseline
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-15
depends_on: []
blocks: []
category_id: null
summary: >
  Implement EV-096 (seed_pen 10->5) + EV-097 (PHVO ceiling two-tier: מוקשה חלקית/partially->40, generic מוקשה/מרגרינה->55) behind a NEW default-OFF env flag (BARI_FAT_TECH_V1 pattern, byte-identical baseline when OFF). Run shadow_backtest.py diff --approved --set flag=1. Report full grade-movement distribution + per-mechanism attribution: EV-097's actual grade blast radius across the 49 PHVO products (how many of 49 actually move when ceiling 40->55 vs inert under sat-fat), EV-096's confirmed 5 crossers, frozen-impact table (MUST be 0). No published-score writes, no flag flip, no promote.
---

# TASK-284B — Shadow re-score: EV-096 (seed_pen=5) + EV-097 (two-tier PHVO ceiling) behind default-OFF flag; diff vs approved baseline

## Results (2026-06-15) — flag `BARI_FAT_TECH_V1` (default OFF), shadow diff flag=ON
Implemented behind default-OFF flag; flag-OFF invariant test PASS (342 cases, 6/6 → byte-identical).
Shadow diff over 704 registered products (12 corpora). **Exit code 2 = FROZEN_TOUCHED** (expected).

- **EV-097 (PHVO ceiling 40→55): tiny.** Only **4 of 49** PHVO products move; **0 grade changes**;
  45/49 inert (sat-fat penalty already holds fat_quality ≤40). 2 movers in frozen snack_bars (E, no
  grade change), 2 in maadanim. The "softening margarine" concern is largely theoretical.
- **EV-096 (seed_pen 10→5): small on grades, broad on score.** 62 products move; **2 registered grade
  crossers** (E→D cereals, D→C maadanim), both upward. Touches frozen milk (4) + frozen snack_bars (23),
  **0 frozen grade changes**.
- **Frozen total: 29 products move score, 0 grade changes.** Exit 2 fired because milk + snack_bars are
  `class: frozen` in `shadow_registry_v1.json` and the milk invariant is a SCORE freeze
  (= run_005_headpin), so any score move is a flagged breach regardless of grade.

## Two reconciliation items for the owner/D7 (orchestrator-flagged)
1. **Milk freeze membership.** The 4 moved "milk" products are plant-based oat/rice drinks (per
   TASK-284A). shadow_registry `milk` = `run_milk_002`, flagged frozen (= run_005_headpin dairy). Need
   to confirm whether these plant drinks are INSIDE the frozen run_005_headpin published set (→ real
   breach) or sit in the broader corpus OUTSIDE the dairy freeze (→ harness conservative flag, not a
   true breach). Determines whether EV-096 actually touches the milk freeze.
2. **284A vs 284B crosser mismatch.** 284A (trace-delta estimate) found 5 crossers (cereals×3, cakes×1,
   salty×1); 284B (real re-score, registered corpora) found 2 (cereals×1, maadanim×1, the latter new).
   The real re-score supersedes the estimate for registered corpora; cookies/cakes/salty are
   NON-registered (not re-scored here) so up to 3 more may exist there. Total grade impact ≈ 2–5, all up.

## close_reason (orchestrator, 2026-06-15)
CLOSED — DoD met: gated implementation (flag default OFF), flag-OFF byte-identical PASS, shadow diff
produced with full per-mechanism attribution + frozen-impact table. Verified shadow_registry frozen
definitions. The exit-2 frozen-touch is the harness working correctly, not a task failure. Findings +
the two reconciliation items handed to parent TASK-284 for the owner ratification decision. NO scores
moved; flag stays OFF; no promote. Note: no APPROVED baseline existed → agent used a fresh flag-OFF
baseline (valid here since flag-OFF = committed behavior, byte-identical proven); promote a real
APPROVED baseline for future CI.
