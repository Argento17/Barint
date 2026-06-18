# P62 / C3 consult — brined golden page: make it cooler (tables, charts, visuals) (route: C3)

You are C3 — an independent, outside-the-family creative+product advisor for **Bari**, a Hebrew (RTL) consumer nutrition-intelligence site. This is an ADVICE-ONLY consult. You are not writing code or final copy — you are giving a sharp, concrete creative direction the Bari team will implement. Be bold but stay inside the hard constraints below.

## The page
"גבינות מלוחות" (brined/salted cheeses) — Bari's new GOLDEN comparison page (the quality bar for every future category page). It's a Hebrew RTL comparison page:
- A hero + an editorial **intro** (a story about why salt IS the cheese, then how Bari scored the shelf).
- A **comparison table**: one row per cheese — score badge (e.g. 75/B), product thumbnail, a 2-line human VERDICT, and nutrition columns (protein, sodium, kcal, fat). Each row expands to full analysis (what works / what limits / bottom line) + full nutrition + ingredients + an **additives dropdown** (per-E-number cards).
- A yellow **category caveat** box (every brined cheese is high-sodium by design — a built-in fact, not a flaw).

## The real data we can visualize (all true, already computed)
- ~48 cheeses (the count may drop slightly — some are being re-sourced/removed). Grade spread roughly A:9 / B:28 / C:9 / D:2.
- **Sodium** ranges 300–1,628 mg/100g; **shelf median = 1,000 mg**. 19/48 sit above the median. Bari scores sodium as DISTANCE from the shelf median (shelf-relative regression), not absolutely — so "A" here means best-in-a-salty-category, NOT low-sodium (7 of 9 A's are still above 900mg).
- Score differences come mostly from **ingredient count, presence of stabilizers/emulsifiers (agar, locust-bean gum), and fat %** — sodium contributes but isn't the lever. Protein is rewarded (these are real protein sources).
- Only **2 of 48** are "truly clean" (≤3 natural ingredients, zero additives).

## Owner brief (2026-06-13)
"Make it more interesting! Tables, visuals, charts — this can and should look cooler." The intro currently reads like a stats dump; the owner wants it to feel alive and visually engaging WITHOUT losing analytical credibility (Bari's whole brand is trustworthy intelligence, not marketing gloss).

## HARD constraints (do not violate — these are Bari law)
1. **No fabrication, ever.** Every visual must be backed by data we actually have (listed above). No invented numbers, no decorative fake charts.
2. **Grade is shown as number+letter only — NEVER color-coded** (no green=good/red=bad). Color may not encode quality. This is a firm rule.
3. Hebrew, RTL. Mobile-first (a mobile user must "get" the shelf in 15–20 seconds).
4. Restrained, credible, journalistic — "restrained but fearless." Cool ≠ flashy/gamified. Think The Economist / FT data-journalism, not a supermarket flyer.
5. Reuses a small set of canonical components; design-token system (no ad-hoc colors). Charts must be implementable in a Next.js/React/Tailwind page.

## What to return (concrete, ranked, implementable)
1. **2–4 specific visualizations/charts** that would make THIS page genuinely cooler AND sharpen the insight — e.g. a sodium-vs-shelf-median distribution strip, a "where each grade sits on sodium" plot, an ingredient-count vs score view, a "only 2 are truly clean" visual. For each: what it shows, why it earns its place (insight, not decoration), rough layout, and how it stays inside the no-color-for-grade rule. Mobile behavior for each.
2. **Table/row treatment**: how to make the comparison table itself more inviting and scannable (hierarchy, the score badge, the verdict line, the expand affordance, density) — concrete, not vague.
3. **Intro direction**: how to keep the 2-sentence story opening but make the rest feel alive (1–2 example Hebrew sentences welcome) and where a small inline visual could replace a sentence of stats.
4. **One thing to AVOID** — the most likely way a team makes this "cooler" and accidentally cheapens Bari's credibility.

Rank by impact. Keep it tight and usable — the Bari Content + Design agents will build directly from this.
