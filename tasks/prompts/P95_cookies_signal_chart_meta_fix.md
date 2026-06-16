# P95 — Cookies: remove false "minimal-processing" signals + chart title + _meta (route: C1 / Frontend)

**Task:** TASK-275. **Lane:** C1 Frontend. Fix NEW-A (HIGH), NEW-B (MED), NEW-C (MED) from red-team v2.
Edits to the frontend JSON + the prologue-viz component. Do NOT touch rowVerdicts/insightLine (Content P94
owns those) or scores.

## NEW-A (HIGH) — remove the false "minimal processing" positive signal from 6 products
In `bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json`, these 6 products have NOVA=2 from a
**1-ingredient truncated parse** (low confidence) yet display the positive signal "עיבוד מינימלי יחסית
לקטגוריה" in `expansion.positiveSignals`, while their ingredient strings show flavoring/preservatives
(חומרי טעם וריח, E200/E202). Remove that specific positive signal entry from each:
`5317194`, `74184`, `311128`, `313160`, `7290119040179`, `99804`. (Verify each: the signal is present AND
the ingredient string contains a flavor/preservative marker — only remove where both hold.) Leave their
other signals/limitingFactors intact.
**Also (systematic, preferred):** in the generator `02_products/cookies_coffee/gen_frontend_json.py`,
suppress the "minimal processing" positive signal whenever `nova_confidence_band == "low"` AND the ingredient
string contains a flavor/preservative marker — so a future regen won't reintroduce it. (If the generator fix
is non-trivial, do the JSON removal for this page and note the generator follow-up in not_done.)

## NEW-B (MED) — chart B title is factually false
In `bari-web/src/components/comparisons/cookies-coffee-prologue-visualizations.tsx`, `SugarGradeChart` title
is hardcoded "גם ה-C מתוקים — אין ביסקוויט חסר סוכר." This is FALSE — the top product (540160) has sugar=0.0g
and appears in the chart. Change the title to an accurate line (e.g. "גם ה-C מתוקים — כמעט כל ביסקוויט מכיל
סוכר" or reframe so it doesn't claim zero sugarless biscuits exist). Keep it on-thesis.

## NEW-C (MED) — stale provenance
In the frontend JSON `_meta`, update `run_id` / `provenance` from `run_cookies_003` → `run_cookies_004`.
Non-consumer-facing but correct the traceability.

## Build gate (real exit, no tail pipe)
`cd bari-web && npm run build > build_cookies4.log 2>&1; echo "EXIT:$?"` — EXIT:0, route present.

## Guards
Do NOT change scores/grades/nutrition/imageUrl/verdicts/pageShell. Do NOT edit shared components or other
categories. Scope CSS to `.cc-page`. OFF ban. No new deps.

## Return
Return contract: task=P95, proposed_status=RETURNED, artifacts (JSON + prologue-viz.tsx [+ generator if
changed], +sha256), counts (signals_removed=6/6, chart_title_fixed=yes, _meta_run_id=run_cookies_004,
build_exit, route_present, 0 score/verdict changes), commands_run (build w/ real EXIT), not_done, self_check.
Propose RETURNED — do NOT close. Orchestrator re-runs build + re-screenshots.
