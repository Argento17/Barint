# P86 — Cookies render fix (metric→sugar) + prologue charts (route: C1 / Frontend)

**Task:** TASK-275. **Lane:** C1-Frontend (Sonnet; C1-CURSOR down). One macro = fix the off-thesis metric +
add the signature charts, so the orchestrator re-screenshots ONCE. Build must stay EXIT:0.

## Context (orchestrator-verified)
The render trio (P85) is built and builds clean (route prerendered, shared components untouched, RTL good,
grade NOT color-coded, images render). TWO changes needed:

### Fix 1 — Row metric is OFF-THESIS (sodium → sugar)
`bari-web/src/lib/comparisons/cookies-coffee-page-data.ts` + `...comparison-page.tsx` currently use
`SODIUM_METRIC` (cloned from brined). But the cookies thesis + the page's OWN copy say "נתרן אינו הנושא"
(sodium is NOT the differentiator). Replace it:
- Import **`SUGAR_METRIC`** (already exists in `@/components/shared/comparison-metric-column.tsx` line ~154)
  instead of `SODIUM_METRIC`. Do NOT edit the shared component.
- In page-data `metrics`: replace `sodium_mg`/`protein_g` with **`sugar_g: p.expansion?.nutrition?.sugar ?? null`**
  (protein is not a cookie differentiator — drop it; sugar is the headline). Update `COOKIES_COFFEE_METRIC_SPECS`
  to the sugar metric + the Hebrew header label (e.g. "סוכר ל-100 גרם").
- Sat-fat stays visible in the expansion nutrition panel (already there). The headline row metric = sugar.

### Fix 2 — Add the 3 prologue charts (the page's data-journalism spine)
Clone the pattern of `bari-web/src/components/comparisons/brined-cheeses-prologue-visualizations.tsx` into
`cookies-coffee-prologue-visualizations.tsx`, rendered in the comparison page before the table (give it a
`data-testid="cookies-viz"` wrapper). **recharts only** (already in the app — do NOT hand-roll SVG, no CDN).
Data-driven from the 61 products' `expansion.nutrition` (sugar, satFat, energyKcal) + score/grade.
Charts (cookies thesis — sugar+sat-fat, NOT sodium):
1. **SIGNATURE — "מבחן הביסקוויט הפשוט": sugar (x) × saturated-fat (y), one dot per product.** Shows the
   shelf clusters high on both. Median reference lines at 17.5g sugar + 5g sat-fat (the red-label thresholds).
2. **sugar × grade** (grade as a text lane label on the axis — shows even the top biscuits carry real sugar).
3. **calories × score** (or sat-fat distribution) — supporting.
**HARD chart rules (golden playbook):** grade is NEVER color-encoded — uniform ink dots; grade shown only as
a text lane label. Median/threshold lines may use the brand accent (reference, not quality). Hollow-point
aesthetic. Mobile-readable at 375px. Captions derive key numbers from the data, don't hardcode.

## Guards
- Scope all page-local CSS to `.cc-page`. Do NOT edit shared components or any other category. No new deps
  (recharts is present). Do NOT touch scores/copy in the JSON. OFF ban.

## Build gate (REAL exit code, no tail pipe)
`cd bari-web && npm run build > build_cookies2.log 2>&1; echo "EXIT:$?"` — must be EXIT:0, route present.

## Return
Return contract: task=P86, proposed_status=RETURNED, artifacts (changed page-data.ts + comparison-page.tsx +
new prologue-visualizations.tsx, +sha256), counts (metric=sugar yes/no, sodium removed yes/no, charts added=3,
grade-color-encoded=NO, build exit, route present), commands_run (build w/ real EXIT), not_done, self_check.
Propose RETURNED — do NOT close. The orchestrator re-runs the build AND re-screenshots (incl. charts) itself.
