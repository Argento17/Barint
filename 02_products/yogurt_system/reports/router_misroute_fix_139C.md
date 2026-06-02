# TASK-139C — Router yogurt-anchor misroute fix

**Date:** 2026-06-01
**Owner:** data-agent
**Engine:** router_v2 (BSIP2 proto_v0), no scoring change
**Status:** RETURNED (proposed)

## Problem

`run_yogurt_003` (Shufersal real corpus) misrouted **18/88 (20%)** of products
(memory cited 17/88; live count was 18). Three failure shapes:

1. **Flavored / "GO" protein yogurts → dessert.** Brand-led names (`יופלה GO …`)
   hit the `"יופלה"` dessert anchor (0.91); names like `דנונה ביו/פרו` and
   `מולר פרופ` had no dairy head, so weak dessert signals (`מוס` from ingredient
   text, `ללא סוכר`) won.
2. **Crunch / topping yogurts → cereal / snack / WFF.** `יוגורט קראנצ קורנפלקס`
   lost to the `"קורנפלקס"` cereal anchor (0.93 > יוגורט 0.92); `מולר מיקס …`
   topped cups routed on the topping noun (`קורנפלקס` / `שקד` / `דגנים` / `בוטנים`).
3. **`זית ירוק יווני` (green olives) → whole_food_fat.** Olives leaked into the
   yogurt corpus through the `"יווני"`/greek include token in the shelf map, then
   routed to WFF on the `"זית"` signal.

## Changes (no scoring logic touched)

### Router — `03_operations/bsip2/proto_v0/src/router_v2.py`
- **8 yogurt sub-brand / product-line anchors → `dairy_protein`**, confidence set
  *above* the competing topping/dessert anchors so dairy identity wins:
  `יופלה go` (0.94), `מולר מיקס` (0.94), `מולר פרוטאין` / `מולר פרופ` /
  `דנונה פרו` / `דנונ.פרו` / `דנונה ביו` / `דנונה יווני` (0.93).
- **Dairy-head topping suppression** (`_check_anchors`): when the name *leads* with
  a dairy-head term (`יוגורט`/`קפיר`), cereal/snack/WFF topping anchors are skipped
  so the dairy anchor wins. Gated to name-start to avoid catching
  topping-flavoured products (`גרנולה בטעם יוגורט`).
- **Drinkable exclusion** on the new anchors (`משקה`/`שתייה`/`שתיה`): the yogurt
  category excludes drinkables, so drink variants stay on the beverage gate. This
  deliberately leaves the **frozen milk category untouched** (0 changes).

### Shelf map — `01_scrape_yogurt.py` + `02_build_bsip1_yogurt.py`
- Added `זית`/`זיתים`/`olive` to the non-yogurt exclusion (runs before the
  `יווני`/greek include), so olives are dropped at curation. `"יווני"` is *kept*
  as a yogurt qualifier so real Greek yogurts (`דנונה יווני מארז`,
  `יוגורט יווני 8%`) are still included.
- Corpus rebuilt from raw (`yogurt_bsip0_raw_20260601T142757.json`):
  **88 → 86** (2 olives excluded), ingredient coverage 86/86.

## Validation

| Check | Result |
|-------|--------|
| run_yogurt_003 misroute rate | **20% → 0% (0/86)** — all route to dairy_protein ✅ (<5% target) |
| Golden router regression (12 cases) | **12/12 PASS** ✅ |
| Structural/signal-bundle regression | 11P / 1W / 0F — the 1 warning is pre-existing (TASK-139B), not routing |
| Frozen milk corpus (run_milk_002) | **0 routing changes** ✅ |
| cereals_002 / bread_light / hummus_001 / snacks(run_001) | **0 routing changes** ✅ |

## ⚠️ Cross-category flag — Nutrition / Product co-sign needed

The router is category-global, so fixing the yogurt run also reclassifies **8
products in the live `maadanim` corpus**, all `dessert`/`snack_bar_granola` →
`dairy_protein` (6× `יופלה GO …`, `דנונ.פרו ללא סוכר פיסטוק`,
`מולר פרוטאין טופ בוטנים`). These are genuine protein/mix-in spoon yogurts and the
flip is a **correction** (maadanim already routed siblings like
`מולר פרוטאין יוגורט תות` and `דנונה פרו 20ג חלבון תות` to dairy_protein — the old
behaviour was internally inconsistent).

- The **shipped/frozen maadanim JSON is unchanged** — a router edit only affects
  future re-runs.
- This is the unresolved **dairy_protein-vs-dessert boundary** (Gap 3, ruled in
  TASK-139A pending Product co-sign). A maadanim re-score is *already* flagged
  pending (TASK-139B culture credit); these 8 reroutes should fold into that same
  review.

## Handoff

- Re-running `batch_run_yogurt_003.py` on the cleaned 86-corpus (to refresh scored
  traces with corrected routing) is left to the consuming task (TASK-135/142) — out
  of scope for this router fix; run_yogurt_003 remains NON-AUTHORITATIVE.
