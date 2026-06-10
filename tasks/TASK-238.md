---
id: TASK-238
title: "PROJECT-WIDE OFF BAN — Open Food Facts contamination halt + remediation (launch blocker)"
owner: orchestrator
status: CLOSED
priority: CRITICAL
created_at: 2026-06-10
closed_at: 2026-06-10
depends_on: []
blocks: [TASK-233F, TASK-234]
roadmap_impact: true
work_type: data-governance
close_reason: "RETRACTED by owner reconciliation 2026-06-10 (later session). The owner directed that OFF removal is to be handled LOCALLY for salty-snacks only — NOT project-wide. The project-wide OFF ban and the global comparison-page launch HALT are lifted. OFF remains a permissible source in other categories unless/until the owner issues a future written per-category policy. Salty-snacks OFF removal proceeds under TASK-237/TASK-240. The 'off_ban_hard_rule' memory has been retracted/localized accordingly. Do NOT de-OFF other categories on the basis of this task."
---

> **RETRACTED 2026-06-10 — see close_reason.** Owner reconciled two conflicting same-day directives
> in favor of LOCAL (salty-snacks only). This task's project-wide ban + launch halt are void. The
> audit (`reports/open_food_facts_contamination_audit_v1.md`) is retained as read-only information,
> not an active launch blocker. Other categories are NOT blocked and are NOT to be de-OFF'd on this basis.

# TASK-238 — Open Food Facts ban: halt + remediation

Owner hard rule (2026-06-10): **OFF is prohibited as a Bari data source** — nutrition, ingredients,
names, barcodes, images, serving sizes, category, fallback, enrichment, validation, "temporary"
fills, comparison JSON, frontend display, generated copy, scoring traces, confidence. No exceptions
without a future written owner policy. "Unknown is acceptable. OFF is not." Saved as memory
`off_ban_hard_rule`. Any OFF dependency = launch blocker.

## Status: HALT
All comparison-page launches and regenerations are HALTED. This blocks TASK-233F and TASK-234
until OFF is removed. Audit complete (read-only): `reports/open_food_facts_contamination_audit_v1.md`.

## Audit verdict: PARTIALLY CONTAMINATED — BLOCK LAUNCH UNTIL REMEDIATED
- **Contaminated (8 shipped):** yogurts, hard_cheeses, cereals, granola (OFF images + OFF nutrition),
  butter, salty_snacks, cheese, juices (OFF nutrition / source chain). + dead files olive_oil,
  crackers_staged. yogurts = entire corpus scraped from OFF.
- **Proven clean (5):** bread (`bread_retail_003`), hummus, maadanim, snacks (`snack_bars`), milk.
- 38 OFF images render on 4 live pages; OFF nutrition reached published scores + "verified" confidence.
- Root capability: `integrations/clients/open_food_facts.py`, used by ≥9 BSIP0 scrapers.

## Remediation (NOT started — awaiting owner go; do not fix before instructed)
1. Disable/remove the OFF client + revoke EDPG admission.
2. Strip OFF from the ≥9 BSIP0 scrapers.
3. OFF images → NULL in cereals/granola/hard_cheeses/yogurts (no guessed substitutes).
4. OFF nutrition → NULL + re-score the 8 categories; report all score/grade deltas.
5. yogurts: owner decision — re-acquire from retailer scrape or pull the category (no non-OFF source).
6. Delete dead OFF files; archive `bread_retail_001`.
7. Re-run QA OFF launch gate per category (5 conditions) before any go-live.

## DoD
- [ ] 0 OFF references in any shipped category's source chain
- [ ] 0 OFF-derived fields / 0 OFF images in any shipped frontend JSON
- [ ] OFF client disabled + EDPG admission revoked
- [ ] All re-score deltas reported; incomplete fields visibly NULL/unknown (never OFF-filled)
- [ ] QA OFF launch gate PASS per category; owner ruling on yogurts recorded
