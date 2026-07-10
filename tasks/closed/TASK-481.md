---
id: TASK-481
title: Chocolate-tablets curation gap: 3 grade-C tablets excluded w/ no documented reason + stale _meta (33 vs 35) + no B-grade filter chip (TASK-474 CRITICAL)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "SHIPPED LIVE PR #65 (merged f2908d2f). Product verdict DOCUMENTED-EXCLUSION (3 grade-C tablets had ingredients-scrape gap → correct discard per missing_data_discard_rule, was undisclosed); config exclusions documented + _meta 33→35 (products byte-identical, 0 score/grade/rank change) + grade-B chip reaches the 2 B leaders. Verified, tsc/build 0. Optional owner follow-up: one-shot re-scrape of the 3 before exclusion is durable."
depends_on: []
blocks: []
category_id: null
summary: >
  Chocolate-tablets curation gap: 3 grade-C tablets excluded w/ no documented reason + stale _meta (33 vs 35) + no B-grade filter chip (TASK-474 CRITICAL)
---

# TASK-481 — Chocolate-tablets curation gap (TASK-474 batch 5 CRITICAL)

Source: TASK-474 chocolate-tablets red-team, CRITICAL F-V3. Orchestrator-VERIFIED against origin/master e615244a.

## Verified facts
- Live `chocolate_tablets_frontend_v1.json` displays **35** products (grades B:2, C:6, D:10, E:17 — NOT "all E"; dark-choc B-grades lead #1 65.8 / #2 65.1).
- **3 genuine grade-C tablets EXCLUDED from display with NO documented reason:** barcodes `3046920023429` (שוקולד חלב חתיכות קרמל), `3046920023368` (שוקולד חלב מעולה), `3046920023443` (שוקולד מריר מעולה) — all classified `chocolate_tablet`, grade **C**, score **50** in run manifest `fresh_rescore_task391_20260624_113405_manifest.json`. Config `exclusions: []` (empty — no reason), `dedup: one_card_per_barcode` (per-barcode, would NOT merge these 3 distinct barcodes), `subpool_filter: category==chocolate_tablet` (says display ALL tablets). So they SHOULD display but don't → silent, undocumented omission of legitimate products that score = displayed C-grades. Undermines "we scored the whole shelf" completeness promise.
- **Stale `_meta`:** `corpus_records`=33 and `scored`=33 but `product_count`=35 and actual displayed=35 (carry-over from a TASK-409 rederive).
- **No B-grade filter chip:** shelf filters are C/D/E only, but #1/#2 are B-grade co-leaders → unreachable via any filter (F-C1 HIGH).

## Deliverable (Data + Product adjudication; NOT a blind fix)
1. Determine WHY the 3 grade-C tablets are excluded (data-quality? intended curation? bug in the display-selection step?). Either INCLUDE them (if legitimate) or record a documented, valid exclusion reason in config `exclusions` + _meta (G3 disclosure). Product co-signs the completeness call.
2. Fix stale `_meta.corpus_records`/`scored` 33→35 (or the true number post-adjudication).
3. Add a B-grade (or "top of shelf") filter chip so the B co-leaders are reachable — frontend, small.
4. Any score/display change → two-gate + owner PR (tripwire-2). Meta/reason-doc-only → non-consumer, lighter.

## RESOLVED (owner "go ahead" unblocked) — DIAGNOSIS + DOCUMENTED-EXCLUSION applied → PR #65
- **Root cause (Data-diagnosed, evidence):** the 3 grade-C tablets (3046920023429/368/443) were dropped in commit c294039e (2026-06-24) because `ingredients_raw` scraped only a 45-char allergen fragment (no ingredient list); nutrition complete. Correct discard per missing_data_discard_rule — the defect was NON-disclosure (never written to config/_meta). The 33-vs-35 was a TASK-409 rederive artifact (CHOC_TABS_BC locked to live set).
- **Product adjudication = DOCUMENTED-EXCLUSION** (not INCLUDE): showing products with no ingredient list breaks the verified-data completeness bar. Remedy = disclose, not reverse.
- **Applied (commit 1ac624ad, orchestrator-verified):** (1) config.exclusions = 3 barcodes w/ real reason + grade/score + provenance; (2) _meta corpus_records/scored 33→35 + disclosure block, products[] sha256-IDENTICAL to origin (0 score/grade/rank change); (3) grade-B filter chip added → reaches the 2 B co-leaders (7290112197467, 7296073382416). 3 files, tsc/build 0.
- **PR #65** https://github.com/Argento17/Barint/pull/65 — consumer-visible (B chip) = owner merge. CLOSE on merge; prune C:\Bari\bari_wt_t481.
- Follow-up option (owner): a one-shot ingredient re-scrape of the 3 before the exclusion becomes durable — NOT done (missing_data_discard_rule: no re-sourcing investment).
