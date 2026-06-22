---
id: TASK-378
title: Sugar re-parse program: fix scrape sugar-capture gap across high-carb categories (bread worst 28/29); re-verify top A-grade juices/milk; guard stays flag-OFF backstop
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-22
closed_at: 2026-06-22
close_reason: >
  Sugar re-parse program COMPLETE (owner ruling: backstop + targeted re-parse, guard
  stays flag-OFF). Ph1 BREAD: parser bug (bread scraper inline map checked carbs before
  sugar, "סוכרים מתוך פחמימות" → discarded sugar); re-parsed 28/31 + regression test;
  staging re-score 0 grade-movers (bread sugar 0–5.4g, max −1.6pt) → "bread collapses to 1"
  fear moot. Ph2 (estimate) + Ph3 (REAL Shufersal labels): sugar GENUINELY ABSENT from the
  Yohananof panels (not a parser bug there). The flagship A-grades are SAFE — pomegranate
  juice real sugar 12.6g still 85/A (NOVA-1 single-ingredient floor overrides EV-091 ceiling;
  the Phase-2 A→B estimate was an artifact of not modeling the floor — re-verify-before-move
  was correct), clementine + whole milk hold A. Only confirmed grade-mover = ALMOND MILK
  (7290014760141) 51.5/C → 49.7/D (real 6g sugar, "סוכר" 2nd ingredient, was scored zero-sugar).
  Ph4 APPLIED + LIVE: bari.digital/hashvaot/milk-comparison (master 0938ab04f, verified live:
  new verdict present, stale "55" gone). Re-ranked shelf, filterTags soy→almond fixed,
  rowVerdict rewritten (gate 0C/0H, M1 precision fix applied). 0 other scores changed.
  6/9 phase-3 products (4 cookies + oat milk) have no sugar row on Shufersal either →
  genuine missing-data, left as-is (flag-OFF guard is their eventual backstop).
  FOLLOW-UPS LOGGED (non-blocking, NOT yet done):
  (1) DURABILITY: almond-milk 6g sugar is in the frontend JSON + rescore artifact but NOT in
      its BSIP1 — a future milk re-score from BSIP1 would revert it to C. Patch BSIP1 sugars_g=6.0.
  (2) Juice field-name bug: BSIP1 stores `juice_subpool`, engine reads `juice_sub_pool` →
      EV-091 juice ceiling silently never fires (0 impact today; fix before any juice rescore).
  (3) Milk G1 schema gap: milk-specific fields (filterTags/milkProductType/satFat/carbs) not in
      the page-output schema (pre-existing, like granola's rank/categoryTotal — schema catch-up).
  (4) Milk score-in-copy backlog (I1/I2): 3 milk products bake a stale numeric score into the
      rowVerdict prose (e.g. "74" vs score 71.0) — older milk-page format; content backlog.
depends_on: [TASK-377]
blocks: []
category_id: null
summary: >
  Owner ruling 2026-06-22 (backstop+re-parse, off TASK-377 blast-radius): root cause of sugar-null-scored-as-zero is a SCRAPE sugar-parse gap, not missing data. Re-parse 'of which sugars' for the 44 affected products across 9 categories (bread 28/29 = systematic, on hold first; cookies-coffee 5; milk 4; hummus 2; juices 2; brined/cakes/cereals 1 ea). Re-verify the top A-grade juices (pomegranate/clementine 85/A) + #1 milk (whole 3.4% 85/A) with REAL sugar before any score move. BARI_SUGAR_NULL_GUARD stays flag-OFF backstop. Chocolate already clean (TASK-376). BLOCKED on usage-limit reset 5:50pm Amsterdam to start dispatches.
---

# TASK-378 — Sugar re-parse program

## PHASE 1 (BREAD) — DONE 2026-06-22 (staging only, 0 score changes)
Root cause: bread scraper `shufersal_probe_v3.py` inline NUTR_LABEL_MAP checked "פחמימות"(carbs) before "סוכרים"(sugar) → label "סוכרים מתוך פחמימות" matched carbs first, discarded sugar. Shared parser (bsip0_nutrition.py) was already correct — only the bread scraper had its own buggy inline map. Required re-scrape (raw HTML not stored in BSIP0). Re-parsed 28/31 (3 have no sugar panel). Regression test added (test_shufersal_sugar_row_label, 34/34 pass). Staging re-score: **0 grade-movers, 0 published scores changed** — bread sugar is 0–5.4g/100g, max −1.6 pt final, no grade crosses. The "bread collapses to 1" fear is moot; re-parse (not discard) confirmed correct. Guard stays OFF. Artifacts: 02_products/bread/staging/run_378_*.json + scripts.

## PHASE 2 (remaining categories) — DONE 2026-06-22 (staging only, 0 score changes)
DIFFERENT root cause than bread: sugar is GENUINELY ABSENT from the panels (11/11 diagnosable products, 0 parser-miss) — the Yohananof per-liter juice/milk panels + cookie panels simply don't declare an "of which sugars" sub-row. Re-parse can't recover it; need a 2nd-retailer label. Estimated impact (USDA reference values): only ONE grade-mover = **7290013153395 סחוט רימונים (pomegranate juice) 85/A rank1 → ~75.1/B (−9.9)** — real fruit sugar (~10.5g) triggers BOTH glycemic penalty AND the EV-091 juice shelf-relative surcharge, both currently nulled. Clementine holds A (−3.3), whole milk holds A (−1.8 lactose 4.7g), hummus/cereal/brined hold grade, cookies (C/E) + almond/oat milk + cake = SKIP (no reference / can't cross grade). **0 published scores changed; 1 estimated tripwire.** Artifacts: 02_products/_parsing_audit/task378_phase2_*.

## PHASE 3 (confirmatory re-scrape) — DONE 2026-06-22 (staging; 0 changed)
Shufersal real labels: pomegranate sugar=12.6g (>USDA est) BUT **stays 85/A** — NOVA-1 single-ingredient floor (SRC-01) overrides the EV-091 ceiling (no Class-B cap fires <25g/<500kcal). The Phase-2 A→B estimate was an artifact of not modeling the floor → re-verify-before-move was correct. Clementine + whole-milk also hold A. **Only confirmed grade-mover: almond milk 7290014760141 51.5/C → 49.7/D** (real Shufersal sugar 6.0g, "סוכר" = 2nd ingredient; was scored as zero-sugar). Forest-fruit cookie holds C. 6/9 (4 cookies + oat milk) have NO sugar row on Shufersal either → genuine missing-data, stay as-is (flag-OFF backstop). Latent bug flagged: BSIP1 stores `juice_subpool` but engine reads `juice_sub_pool` → EV-091 silently never fires (0 impact today; fix before any future juice rescore). Artifacts: 02_products/_parsing_audit/task378_phase3_*.

## PHASE 4 (apply almond-milk correction) — owner approved 2026-06-22 ("apply it now")
Only confirmed published-score move: almond milk (7290014760141) → 49.7/D with real 6.0g sugar. Update BSIP1 + milk_frontend_v1.json (score/grade/re-rank), revise any now-wrong copy, red-team the change, deploy to bari.digital/hashvaot/milk-comparison. Scoped to this one product (NOT a full milk-page audit). Juice field-name bug = separate queued fix.
