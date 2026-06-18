# P81 — C3 review #1: Hebrew fresh-eyes on cookies copy (route: C3)

Outside-the-family Hebrew fresh-eyes reviewer (gpt-5.5). ADVICE ONLY — flag issues; do not rewrite the
product data or invent facts. This is the pre-red-team copy gate (it once caught a fabricated methodology
line on the brined page). The COPY below is for a NEW page: "עוגיות לקפה" (coffee biscuits), an honest
C-ceiling indulgence shelf (0 A, 0 B, 9 C, 22 D, 30 E; top product 63/C). Framing = "least-bad", not "healthy".

## What to review
Read `02_products/cookies_coffee/cookies_coffee_copy_v1.json` — the page shell (hero, 3 prologue sentences,
3 methodology lines, category caveat) + 61 per-product `insightLine` + `rowVerdict` (Hebrew).
Cross-check claims against the scored data in `02_products/cookies_coffee/bsip2_outputs/run_cookies_003/`
(scores/grades) and the methodology `02_products/cookies_coffee/methodology/cookies_coffee_scoring_interpretation_v1.md`.

## Flag (ranked CRITICAL / HIGH / MED), with the exact offending string + why
1. **Fabrication / unsupported claims** — any statement not backed by the product's real nutrition/
   ingredients or the methodology (e.g. a health implication, an invented number, a "clean"/"natural" claim
   on a product that isn't). This is the #1 thing to catch.
2. **Framing integrity** — does any line imply a cookie is "healthy"/"recommended"? The honest frame is
   least-bad / harm-reduction within an indulgent shelf. Flag anything that breaks it OR is needlessly
   demoralizing.
3. **Hebrew quality** — awkward phrasing, grammar/agreement errors, unnatural register, robotic repetition
   across the 61 verdicts (they should feel individually written, not templated).
4. **Thesis coherence** — the page's spine is fat-type + sugar + additives/processing (NOT sodium, NOT
   "lowest sugar wins"). Flag lines that contradict or muddle it.
5. **Internal-token / mechanics leakage** — any run id, cap name, NOVA/EV/flag token, or raw score-mechanics
   exposed in consumer copy.

## Output
A ranked list (CRITICAL/HIGH/MED) — each item: the exact Hebrew string, the problem, and a suggested
direction (not a full rewrite). If the copy is clean on a dimension, say so. End with a one-line verdict:
SHIP / SHIP-WITH-FIXES / BLOCK. No product data invented. This is advice the orchestrator weighs.
