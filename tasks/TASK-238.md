---
id: TASK-238
title: "PROJECT-WIDE OFF BAN — Open Food Facts contamination halt + remediation (launch blocker)"
owner: orchestrator
status: IN_PROGRESS
priority: CRITICAL
created_at: 2026-06-10
depends_on: []
blocks: [TASK-233F, TASK-234]
roadmap_impact: true
work_type: data-governance
reopened_at: 2026-06-10
---

> **REINSTATED 2026-06-10 — PROJECT-WIDE, PERMANENT.** The earlier same-day "localize to
> salty-snacks only" reconciliation was WRONG and is itself retracted. The owner reconfirmed live
> and emphatic: *"rip it off from EVERY product page and the rule is to NEVER use it again."* The
> project-wide OFF ban stands. The de-OFF remediation already applied to butter/cereals/granola/
> hard_cheeses/juices/yogurts is CORRECT — do NOT revert it. Now encoded as a CLAUDE.md Hard rule +
> memory `off_ban_hard_rule`. Audit `reports/open_food_facts_contamination_audit_v1.md` is an active
> launch gate again.
>
> A prior revision of this file (committed during the retraction window) recorded `status: CLOSED`
> with a "RETRACTED / OFF remains permissible" close_reason. That revision is VOID and must never
> be restored — the project-wide ban is current owner policy. This task stays OPEN until the full
> DoD below is met (the TASK-242 release remediates images/client/dead-files, NOT nutrition).

# TASK-238 — Open Food Facts ban: halt + remediation

Owner hard rule (2026-06-10): **OFF is prohibited as a Bari data source** — nutrition, ingredients,
names, barcodes, images, serving sizes, category, fallback, enrichment, validation, "temporary"
fills, comparison JSON, frontend display, generated copy, scoring traces, confidence. No exceptions
without a future written owner policy. "Unknown is acceptable. OFF is not." Saved as memory
`off_ban_hard_rule`. Any OFF dependency = launch blocker.

## Status: HALT (partially remediated by TASK-242)
All comparison-page launches and regenerations of the OFF-contaminated categories remain HALTED
until the per-category OFF launch gate passes. This blocks TASK-233F and TASK-234 for those
categories. Audit (read-only): `reports/open_food_facts_contamination_audit_v1.md`.

## Audit verdict: PARTIALLY CONTAMINATED — BLOCK LAUNCH UNTIL REMEDIATED
- **Contaminated (8 shipped):** yogurts, hard_cheeses, cereals, granola (OFF images + OFF nutrition),
  butter, salty_snacks, cheese, juices (OFF nutrition / source chain). + dead files olive_oil,
  crackers_staged. yogurts = entire corpus scraped from OFF.
- **Proven clean (5):** bread (`bread_retail_003`), hummus, maadanim, snacks (`snack_bars`), milk.
- 38 OFF images render on 4 live pages; OFF nutrition reached published scores + "verified" confidence.
- Root capability: `integrations/clients/open_food_facts.py`, used by ≥9 BSIP0 scrapers.

## Remediation status (updated by TASK-242, 2026-06-11)
1. ~~Disable/remove the OFF client~~ — **DONE in TASK-242** (`open_food_facts.py` hard-fails on
   every entry point). EDPG admission revocation in `integrations/README.md` still **OPEN**
   (not in the 242 release scope).
2. Strip OFF from the ≥9 BSIP0 scrapers — **OPEN** (working-tree edits exist, unreviewed/uncommitted).
3. ~~OFF images → NULL in cereals/granola/hard_cheeses/yogurts~~ — **DONE in TASK-242**
   (39 OFF image URLs → null; honest placeholder, no guessed substitutes). Real retailer image
   backfill = TASK-243.
4. OFF nutrition → NULL + re-score the affected categories — **OPEN. THE BIG REMAINING ITEM.**
   Post-242, OFF-derived nutrition values and the scores built on them are STILL LIVE in
   cereals, granola, hard_cheeses, yogurts, butter, cheese, juices. salty_snacks is the only
   category fully re-sourced (TASK-237/241 pattern = the template). Per-category re-source or
   owner pull-decision required; report all score/grade deltas.
5. yogurts: owner decision — re-acquire from retailer scrape or pull the category — **OPEN**.
6. ~~Delete dead OFF files (olive_oil, crackers_staged, OFF-bearing archives)~~ — **DONE in
   TASK-242.** Archive of `bread_retail_001` still **OPEN**.
7. Re-run QA OFF launch gate per category (5 conditions) before any go-live — **OPEN**.

## DoD
- [ ] 0 OFF references in any shipped category's source chain
- [x] 0 OFF images in any shipped frontend JSON (TASK-242; grep over `bari-web/src/data` = 0)
- [ ] 0 OFF-derived nutrition/score fields in any shipped frontend JSON (items 4-5)
- [x] OFF client disabled (TASK-242) — EDPG admission revocation in `integrations/README.md` pending
- [ ] All re-score deltas reported; incomplete fields visibly NULL/unknown (never OFF-filled)
- [ ] QA OFF launch gate PASS per category; owner ruling on yogurts recorded
