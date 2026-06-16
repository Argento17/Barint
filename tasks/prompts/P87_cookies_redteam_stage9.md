# P87 — Cookies page: closing Red-Team Stage-9 gate (route: C1 / Red-Team)

**Task:** TASK-275. **Lane:** C1 Red-Team Agent. The page is NEVER done until adversarially torn apart.
Produce a structured report; classify findings **CRITICAL / HIGH / MED**. **Owner-ready only at zero CRITICAL.**
You do not fix, do not close — you challenge.

## The page under test
- Route: `/hashvaot/cookies-coffee` (built; a dev/start server can be run on a port for inspection).
- Data (ships): `bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json` (61 products, scored+copy).
- Components: `cookies-coffee-comparison-page.tsx`, `cookies-coffee-page-data.ts`,
  `cookies-coffee-prologue-visualizations.tsx`, route + index card.
- Ground truth: `02_products/cookies_coffee/bsip2_outputs/run_cookies_003/` (traces) ;
  methodology `…/methodology/cookies_coffee_scoring_interpretation_v1.md` + `…_routing_ruling_v1.md`.
- Screenshots already taken in `bari-web/public/qa/cookies/` (you may regenerate via `scripts/shot-cookies-page.mjs`).

## A. Deterministic hard-fail checks (any FAIL = CRITICAL)
1. `npm run build` → EXIT:0, route present (capture real exit, no `| tail`).
2. **Every product `score`+`grade` == its run_cookies_003 trace** (61/61 exact). Any mismatch = CRITICAL.
3. **OFF = 0** everywhere (JSON + components). Any OFF reference = CRITICAL (launch blocker).
4. **Images RESOLVE** — HTTP-check all 61 `imageUrl`s (HEAD/GET); report how many actually load vs dead
   hosts (salty-snacks precedent: scrape image hosts can be dead). Dead images that render broken = HIGH.
5. **Additives dropdown** complete per product (`d4_additives` present, [] not undefined).
6. **0 PENDING_COPY**; grade dist == C9/D22/E30.

## B. Adversarial content / honesty / visual review (judgment)
1. **Fabrication / unsupported claims** — every verdict/insightLine/prologue/caveat/chart-caption claim must
   trace to real nutrition/ingredients or the methodology. Hunt for invented numbers, false "clean"/"no
   additives", health implications. (C3 review #1 already fixed a batch — confirm none remain + scan fresh.)
3. **Charts:** is each chart's DATA faithful to the JSON? Is the signature (sugar×sat-fat) on-thesis? Is
   grade EVER color-encoded (must be NO — uniform ink, grade as text lane only)? Threshold lines correct
   (17.5g sugar / 5g sat-fat)? Any chart caption number wrong vs the data?
4. **Framing integrity** — honest "least-bad" / C-ceiling; nothing implies a cookie is healthy/recommended;
   not demoralizing. Sodium correctly NOT presented as the differentiator.
5. **WATCH-ITEMS (carried — scrutinize each):**
   - The **2 peanut-butter cookies** (protein ~15g) ruled IN despite methodology §1.3 ">10g protein → OUT"
     (overridden as natural-not-fortified). Are they fairly on-shelf, or do they read as off-category?
   - **Choc-chip biscuits** IN under the structural test — fair?
   - The **1 grain product** (`עוגיות דגנים…`) that routed to snack_bar_granola, not biscuit — should it be
     on this page at all?
   - Are the **9 C-grade "least-bad"** products genuinely the best, scored fairly under the new biscuit
     category? (Extraction-trust note: P69 dual-extract did NOT complete — spot-check the featured C-products'
     nutrition vs their raw HTML/BSIP0.)
6. **RTL / mobile** coherence at 375px; images dominate or row hierarchy broken?

## Return
A ranked CRITICAL/HIGH/MED report → `02_products/cookies_coffee/reports/red_team_cookies_page_v1.md`. Each
finding: what + where (file/product/line) + why + severity. End: the deterministic-check table + a one-line
verdict (ZERO-CRITICAL = owner-ready candidate / BLOCKED). Return contract: task=P87, proposed_status=RETURNED,
artifact (+sha256), counts (criticals/highs/meds, build exit, score==trace N/61, images-resolve N/61, OFF),
not_done, self_check. Propose RETURNED — do NOT close. The orchestrator re-verifies every CRITICAL itself.
