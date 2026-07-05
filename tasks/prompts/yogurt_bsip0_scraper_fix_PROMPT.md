# Yogurt BSIP0 — reach ≥3 usable retailer sources (TASK-515 / 515A resume)

**Repo:** `C:\Bari` (root Agent-OS tree). This is a resume of a PARKED task — owner ruled 2026-07-05
"leave it for now and continue; we'll fix the scraper in another session."

## Objective
Get the yogurt BSIP0 acquisition to **≥3 usable retailer sources with cross-check** (owner HARD requirement).
Today it is at **2/3** (Shufersal + Yohananof). Reaching ≥3 unblocks the two comparison pages —
**TASK-515 spoonable yogurt** + **TASK-515A yogurt drinks** — which then continue the normal build-page pipeline
(BSIP1 → BSIP2 → page → two-gate → red-team). Read `tasks/TASK-515.md` for the full blocker + resume condition.

## What is DONE — do NOT redo
- **Shufersal:** works (requests-based). 119 survivors in the last run. Keep.
- **Yohananof:** landed but THIN (see below). A real **sugar-field parser bug was already found + fixed** in
  `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py` (a "מתוכן כפיות סוכר" teaspoon row was bleeding into the
  grams field). Do not re-fix.
- **Plausibility gate already patched** (`03_operations/bsip0/scrape/_shared/plausibility_gate.py`): two new yogurt
  FoodClasses `DAIRY_SEMISOLID` (floor 8.0g, kcal 30–250) and `DAIRY_CULTURED_DRINK` (floor 4.0g, kcal 20–150);
  labneh routes to the existing `DAIRY_SOLID`. Ruling doc: `01_framework/governance/yogurt_plausibility_floor_ruling_v1.json`.
  Use this gate as-is; do NOT touch cheese's `DAIRY_SOLID` calibration.
- Preserved corpus + manifests under `02_products/yogurt_system/bsip0_task515/`.
- **NOTE:** the above are uncommitted in a dirty working tree (~289 ambient files from other threads). Everything is
  local-only, not committed. Preserve it.

## The problem (diagnosed 2026-07-05) — per retailer

**Victory — INTRACTABLE under 3 architecturally-distinct automated attempts (all documented, do NOT just re-run them):**
1. Generic `cloudfront.net` image scan grabbed the **home-page promo carousel** (`class="special-item"`,
   `ng-repeat="chunk in chunks"`, `SOURCES.HOME_PAGE_CAROUSEL`) — `/category?search=<q>` does not filter to search results.
2. The real search UI (`.search-input`, behind a collapse icon) was triggered correctly, but the Angular autocomplete
   panel stays `ng-hide` regardless of `fill()`/`type()` — client-side search never activates in the session.
3. Direct category navigation (real category URLs pulled from the site's own left-nav, e.g. `יוגורט לבן` →
   `/categories/79721/products`, `משקאות יוגורט` → `/categories/95039/products`) with `networkidle` + scroll → **zero
   real product cards**, only the SEO nav sidebar (`ng-repeat="link in seoLinks"`), no `gs1-products` images, no
   add-to-cart. **A milk-category control (`/categories/79723/products`) behaved identically → the failure is site-wide,
   not yogurt-specific.** No branch/store-selection modal was found.
   → Hypotheses to try NEXT (not yet attempted): Victory likely needs a **real branch/store selection (a location
   cookie) before product grids render**, and/or a **persistent authenticated browser context**, and/or reverse-
   engineering the **actual product API via a real-browser HAR capture** (watch XHR while a human browses a category).
   The Cloudflare bot-wall means a plain HTTP HEAD check falsely reports "DOWN"; a headed Playwright page DOES load —
   the problem is the product-data XHR, not reachability.

**Rami-Levy — BLOCKED (consistent across 06-05/06-07/06-20/07-05 probes):** price-transparency feed DNS-dead;
storefront is a Nuxt SSR shell with zero server-rendered product data; guessed client-API endpoints 404. Needs a
real-browser HAR capture to find the Nuxt client API. Diagnosis: `03_operations/bsip0/scrape/retailer_capabilities/
rami_levy_task515_reprobe.md`. Treat as low-probability; not required if another source reaches ≥3.

**Yohananof — THIN (scraper-pacing gap, not shelf coverage):** only 8 candidates captured; a diagnostic re-load showed
~22 discoverable. `browse_yohananof_candidates` under-captures a page that renders more — the stability-based scroll fix
attempted did not reproduce the 22 count automatically. Needs a genuine scroll/load-more timing fix to pull the real
shelf (a comparable retailer should carry dozens of yogurt SKUs like Shufersal's 100+).

## The task — pick the path(s) that reach ≥3, in priority order
1. **Crack Victory** (best: it's a canonical source and reachable as a site). Try the un-attempted hypotheses above —
   branch/store cookie first, then a real-browser HAR capture of the product XHR, then replay that API. This is the
   highest-value fix.
2. **AND/OR fix Yohananof pacing** to get its full shelf (improves the 2nd source's weight regardless of Victory).
3. **If Victory stays intractable → add a 4th non-canonical retailer** (Osher Ad or Tiv Taam — both have web
   storefronts) by building a new scraper per `03_operations/bsip0/scrape/BSIP0_PLAYBOOK.md`. Osher Ad / Tiv Taam are
   the owner-flagged fallbacks.
Goal state: **≥3 retailers with usable, cross-checked yogurt nutrition + ingredients.**

## Hard constraints (non-negotiable)
- **OFF is BANNED — every field, forever.** Ingredients + nutrition ONLY from the direct product scrape; unparsed = NULL.
  Any OFF dependency is a launch blocker. (A prior Yohananof scraper was OFF-paired and had to be replaced.)
- **Per-100(g/ml) plausibility gate is mandatory** (drinks are a per-bottle-vs-per-100ml trap; use the patched gate).
- **Missing-data discard rule:** data not found one-shot → discard that SKU; never punish/cap, never over-invest re-sourcing.
- **Cross-check nutrition across sources** per SKU where the same product appears; report disagreements, never silently average.
- **Tag every SKU by subpool** (`spoonable` vs `drinkable`) + edge flags (`kefir`/`labneh`). Note: kefir currently has 0 real
  products — a dedicated kefir query pass is needed before that edge case can be ruled.
- Document any blocked/unreachable retailer explicitly — never silently skip.
- **Tree safety:** the working tree is dirty with ambient files from other threads. Do NOT `git stash -u` / `reset` /
  `checkout .` / `clean` the whole tree (a cloud CLI lane will wipe it — run in an isolated `git worktree` or a
  shared-tree editor that touches ONLY scraper files + outputs). Do not commit without owner supervision.

## Deliverable / return
Run the final cross-check + `03_operations/bsip0/validators/bsip0_qa_validator.py` (all 6 checks; report exit code),
then emit the machine-readable return contract (`01_framework/operations/return_contract_v1.md`): artifact paths +
sha256 per raw retailer JSON, per-retailer AND per-subpool counts (spoonable/drinkable), a reachable-vs-blocked
retailer table, plausibility result, validator exit, cross-check coverage (SKUs in ≥2 sources + disagreements), and an
explicit **≥3 verdict (met? y/n)**. Propose RETURNED — do not close (orchestrator verifies + closes).
