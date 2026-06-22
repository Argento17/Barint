---
id: TASK-375
title: Chocolate-tablets fix: fill cocoa ladder (missing 70%/80%) + repair failed ingredient parses
owner: orchestrator
status: CLOSED
priority: HIGH
created_at: 2026-06-22
closed_at: 2026-06-22
depends_on: []
blocks: []
category_id: chocolate-tablets
close_reason: >
  Shipped + LIVE on bari.digital/hashvaot/chocolate-tablets (master 0c2f0a1a4,
  propagated on first poll). Orchestrated to lanes per owner ("route to C1/C2/C3"):
  Data Agent pass-1 (Shufersal) + pass-2 (Victory) scrape+score via the EXISTING
  chocolate lens (score_chocolate_task362.py, unchanged); content lane; Adversarial
  QA gate x2. Shelf 33->38. Added 5 verified dark tablets: 62% Toso (50.5/C,
  sugar-free maltitol), 70% Lindt Excellence (28.7/E), 70% Tzokta (27.9/E), 72%
  Dubro (51/C, sugar-free maltitol+stevia), 75% premium (32/E). 70% now represented;
  E grades HONEST (mainstream 70% dark ~30g sugar/100g); sugar-free C's flag the
  maltitol mechanism. Fixed 3 Lindt "מעולה" products that had captured the allergen
  "may contain" line as ingredients -> honest null (real list not on Shufersal OR
  Victory). Removed standing-rejected "סוכר אמיתי" from ct-002. Gate#1 BLOCK (H-1
  ct-036 false fiber superlative "מהגבוהים במדף" — actually tied 5th; M-1 LF schema)
  -> fixed -> gate#2 PASS (0C/0H/0M). Build exit 0; 10/10 render checks. Deploy
  MERGED onto master base (preserved the concurrent D4 additive updates for
  ct-016/021/022/028/033 — caught the clobber risk in pre-deploy diff).
  DISCARDS (missing-data rule): 70% Max Brenner + 75% Heidi (garbled scraped
  ingredient text); Millennium 80%/74% (no nutrition panel).
  FOLLOW-UPS (logged, non-blocking, owner-accepted):
  (1) 80% cocoa = genuine availability gap (no 80% with nutrition in Shufersal/Victory).
  (2) 3 Lindt "מעולה" ingredient lists unavailable on any retailer -> null until a new source.
  (3) PIPELINE BUG: Victory/pass-2 BSIP1 canonical mapper silently dropped sugars_g
      (-> null), inflating scores (Lindt 70% bogus 61/C vs correct 28.7/E); cross-retailer
      raw nutrition agreed. Affects any Victory-sourced scoring -> Data/pipeline fix.
  (NOTE: lanes loosely called this "TASK-366" but that id was taken by the E476 task;
  this is the correct registry id.)
summary: >
  Chocolate-tablets fix: fill cocoa ladder (missing 70%/80%) + repair failed ingredient parses
---

# TASK-375 — Chocolate-tablets fix: fill cocoa ladder (missing 70%/80%) + repair failed ingredient parses

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
