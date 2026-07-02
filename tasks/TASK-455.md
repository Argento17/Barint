---
id: TASK-455
title: Chocolate de-anchor: endemic sat-fat carve-out (EV-REDLABEL-013) + fix chocolate-tablets mis-shelving, then re-score + ship
owner: nutrition-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-02
blocker: ""
depends_on: []
blocks: []
category_id: chocolate
summary: >
  Nutrition ruled (EV-REDLABEL-013) the continuous red-label de-anchor must NOT apply to chocolate as-is: cocoa-butter sat-fat is endemic; 2 downward C->D tablet flips are double-count artifacts. Carve-out = add chocolate_bars/chocolate_tablets to REDLABEL_ENDEMIC_SATFAT_CATEGORIES (constants.py:247). SEPARATE blocker: chocolate tablets mis-classify as snack_bar_granola (scored vs wrong thresholds).
---

# TASK-455 — Chocolate de-anchor: endemic sat-fat carve-out (EV-REDLABEL-013) + fix chocolate mis-shelving, then re-score + ship

## Sign-offs (both present → unblocked, within-program, NO owner escalation)
- **Nutrition (EV-REDLABEL-013, 2026-07-02):** carve-out required. Continuous `regulatory_quality` double-taxes endemic cocoa-butter sat-fat; 2 downward C→D tablet flips (`3046920029759`, `7290119500482`) are artifacts. Fix = extend `REDLABEL_ENDEMIC_SATFAT_CATEGORIES`.
- **Product (D7 co-sign, 2026-07-02):** APPROVE carve-out (precedented by EV-048 butter + EV-REDLABEL-005 dairy; same compositionally-fixed test). Mis-shelving = **narrow classifier fix**, verified **58/58** chocolate products (23 bars + 35 tablets) classify as `snack_bar_granola` because `category_classifier.py` has NO chocolate bucket. Live-accuracy issue, the bigger of the two. Sequence: reclassify → carve-out → one re-score → Content+QA → ship. No tripwire.

## Key coupling (orchestrator-verified)
`REDLABEL_ENDEMIC_SATFAT_CATEGORIES` is matched against the **internal `category`** field (`score_engine.py:2227`), NOT `category_id`. So the classifier MUST assign chocolate a bucket name that is ALSO added to the endemic set, or the carve-out never fires. The two fixes are coupled.

## Scope / deliverable
1. Add a chocolate bucket to `category_classifier.py` (CATEGORIES + CATEGORY_SIGNALS) with high-confidence chocolate tokens that outrank the 0.3 granola/dessert overlap; pick the internal category name + its cap regime so chocolate is scored as chocolate (calorie-dense), not granola.
2. Add that bucket name to `REDLABEL_ENDEMIC_SATFAT_CATEGORIES` (`constants.py:247`).
3. **Cross-category regression gate:** reclassify ALL live corpora, prove no chocolate-*flavored* product (choc-chip cookies, choc granola, choc milk) is stolen into the chocolate bucket. (Future-safety; immediate re-score is chocolate-only.)
4. Re-score both chocolate shelves (corpus-pinned to published barcodes) with `BARI_REDLABEL_CONTINUOUS_V1=on` + both fixes; confirm the 2 downward flips resolve + report new moves/flips/distribution + which cap regime now applies.
5. Content authors any flips → Adversarial QA → Product go/no-go → ship in a go-live PR.

## Execution (DONE — awaiting owner merge)
- Data implemented router_v2 Rule 4 (shelf-identity gate) + chocolate CALORIE_DENSITY_TABLES + endemic carve-out. Regression: 0 flips / 803 products / 11 live cats.
- Re-score (flag on, pinned): bars 23/23 up / 0 flips (all E); tablets 34 up/1 down-0.2 / 7 upward flips (B2/C6/D10/E17).
- Nutrition regime CO_SIGN (calorie table + 2 B-grades defensible; all-E bars genuine clustering). Adversarial QA GO_WITH_FIXES both shelves (G5 PASS, parity/rank trace-exact).
- Content fixed RT-1 (#2 tablet sole-leader overclaim → hedged) + 4 pre-existing banned phrases on bars → G6 PASS. `_scoring_trace.category` refreshed → chocolate on all 58.
- **PR: golive/chocolate-task455 (commit f026f2dd) → https://github.com/Argento17/Barint/pull/new/golive/chocolate-task455.** Owner opens + merges (tripwire #2). On merge → CLOSED.
- Pre-existing follow-ups (NOT introduced): G1 SCHEMA → TASK-453; missing category-caveat on chocolate_bars page → frontend.
