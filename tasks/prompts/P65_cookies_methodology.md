# P65 — Cookies-near-coffee: scoring interpretation + subcategory definition (route: C1 / Nutrition)

**Task:** TASK-275 (factory run #7, `cookies-coffee`). Read `C:\Bari\tasks\TASK-275.md` first.
**Lane:** C1 native Nutrition Agent — Bari-judgment (category methodology + scoring philosophy).

## Objective
Author the scoring/methodology foundation for a NEW comparison page: **"cookies you eat with coffee"**
(עוגיות לקפה) — the small sweet accompaniment biscuit (archetype: Lotus Biscoff / speculoos; also petit
beurre, tea/marie, butter cookies, shortbread, digestive, biscotti). This is the analogue of the brined
cheese `scoring_interpretation_v1.md` — it governs corpus filtering, scoring, and the category caveat.

Deliverable: `02_products/cookies_coffee/methodology/cookies_coffee_scoring_interpretation_v1.md`

## What it must decide (ground every call in how the engine actually behaves — read `score_engine.py`, `nova_proxy.py`, `evaluation_scope.py`; cite line numbers)
1. **Subcategory boundary (the narrowing applied AFTER the broad BSIP0 scrape).** The scrape captures a
   broad cookie radius; you define which subset is the honest "coffee cookie" shelf. State clear IN /
   OUT / AMBIGUOUS rules by product type. Specifically rule on: chocolate-coated & cream-filled cookies,
   wafers, cake-like/soft cookies, children's character cookies, protein/"functional" cookies, gluten-free,
   vegan, organic. Mirror the brined methodology's §1.3-style scope rules.
2. **Scoring philosophy for an indulgence category.** These are NOVA-3/4 sweet biscuits. Decide the
   honest framing (cf. snack bars: "no snack bar reaches A; B is the ceiling" — `owner_systematic_not_artisanal`,
   the snk-001 ceiling). Is there a realistic grade ceiling here? What is it, and why — grounded in the
   engine, not invented. Do NOT manufacture differentiation that isn't there (`butter_clustering_honest_finding`):
   if cookies genuinely cluster, that's an honest finding, not a problem to "fix."
3. **The real differentiators (the page's thesis).** Rank what separates a better coffee biscuit from a
   worse one and which the engine already captures: sugar level, fat TYPE (butter vs margarine / palm /
   hydrogenated / trans), saturated fat, additive/emulsifier load (NOVA + E-numbers), whole-grain vs
   refined flour, ingredient-list simplicity, portion/energy density. Name the **signature thesis chart**
   (the equivalent of brined cheese's sodium×grade "A is not low-sodium" chart). Sodium is likely NOT the
   story here — say what is.
4. **Category caveat text** (Hebrew, grounded in real engine behavior) for the standard yellow
   "הערת קטגוריה" box — honest about what an A means on a cookie shelf.
5. **Whether any scoring-rule change is needed at all.** Strong preference: NONE — score these with the
   committed engine as-is. If you believe a scoped rule is genuinely required (e.g. a sugar shelf-relative
   surcharge), do NOT implement it — specify it as a flag-gated, default-off D7 proposal (Nutrition ruling
   + Product co-sign + no-regression proof + EV entry) and FLAG that a C3 "is-this-collapse-real" consult
   is mandatory before it ships. Default path = no engine change.

## Hard guards
- **Frozen invariants / published scores are untouchable** (milk run_005_headpin etc.). No engine edits
  in this task — this is a ruling document. Do not move any published score.
- **OFF ban absolute** — no Open Food Facts reasoning or data anywhere.
- No fabricated products or numbers; reason about the category, not invented SKUs.

## Return format
Domain agent: propose RETURNED, never CLOSED. End with the return contract
(`01_framework/operations/return_contract_v1.md`) JSON: task=P65, artifacts (the .md + sha256),
counts (sections delivered), the engine line-cites you grounded on, not_done, self_check.
