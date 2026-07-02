---
id: TASK-414
title: EV-candidate: heated vs non-heated sucralose (EFSA 2026 re-eval)
owner: nutrition-agent
status: IN_PROGRESS
priority: LOW
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  Watchlist EV candidate. EFSA Feb 2026 re-eval (doi:10.2903/j.efsa.2026.9854) held sucralose ADI at 15 mg/kg but found chlorinated-compound formation on HEATING; safety for fine bakery wares not confirmed. BSIP2 scores sucralose (E955) as a flat Tier-C penalty with ZERO application context (verified: signal_extractor.py:110-124, score_engine_v2.py:235-246). Label-derivable via proxy (sucralose x baked category = heated). Register + HOLD: no score change (D7 + owner gate on any live differentiation). Next: corpus count of sucralose x baked SKUs to scope worth.
---

# TASK-414 — EV-candidate: heated vs non-heated sucralose (EFSA 2026 re-eval)

**Type:** Evidence Horizon-Scan → EV candidate (watchlist, HELD). Owner: nutrition-agent.
**Status intent:** registered and parked — no active dispatch. Not on DISPATCH_BOARD (nothing running).

## The finding (from owner horizon-scan dump, 2026-07-01)
EFSA re-evaluation, 17 Feb 2026 (EFSA Journal, **doi:10.2903/j.efsa.2026.9854**):
- Current **ADI held at 15 mg/kg bw/day** — confirmed safe for **non-heated** use.
- **New:** chlorinated-compound formation when sucralose is **heated**; safety for the
  **extension of use in fine bakery wares NOT confirmed.**
- Character: **application-specific hazard**, *not* an ADI change. Confidence **high**
  (EFSA institutional peer-reviewed opinion); diffusion **low** (regulatory/industry
  channels only, not yet in IL discourse). Credible, evidence-backed — not misinformation.

## Why this is not auto radar-only
Standing doctrine [[efsa_no_scoring_exposure]] files *ADI/EFSA changes* as radar/editorial-only
(engine reads no EFSA runtime value). This is **not an ADI revision** — it's a mechanistic,
application-conditional hazard. Different class → does not get reflexively dismissed.

## Verified engine state (read 2026-07-01)
BSIP2 handles sucralose by **identity only, zero application context**:
- Sucralose (סוכרלוז / סוכרלוזה / E955) → **Tier C** (synthetic high-intensity, full penalty):
  `03_operations/bsip2/proto_v0/src/signal_extractor.py:110-124`
- Tier → penalty/cap is a flat map keyed on the tier letter and nothing else:
  `03_operations/bsip2/sprint1/score_engine_v2.py:235-246`
- No `heated` / `bakery` / `baking` / `application` conditioning anywhere (grep clean).
- **Consequence:** sucralose gets the identical Tier-C treatment in a no-heat diet drink and
  in a baked cookie. The heated/non-heated distinction EFSA now draws **does not exist** in our model.

## Label-derivability verdict
Heating is not printed on a label, but a clean **proxy** is:
> sucralose (E955) present × **baked category** (cookies / cakes / fine bakery / biscuits — already live) = heated application.
This clears the label-derivability bar via inference → lifts the finding out of KB-only into
**EV-candidate** territory. Beverage / no-bake sucralose = non-heated, untouched.

## Routing decision (HELD)
1. **No score change now.** Any live differentiation re-ranks published sweetener / baked-goods
   scores → trips tripwire #1 (published scores) → **D7 co-sign (Nutrition + Product) + owner gate.**
2. **EV-candidate, not radar-only and not KB-only** — proxy-sourceable from labels already parsed.
   If built: modelled as a *signal* (sucralose × baked-category → severity bump) justified by the
   EFSA citation, **never** by reading EFSA at runtime. Firewall intact. `food_additives` client
   limit still applies (no numeric ADI, no IL-vs-EFSA divergence).
3. **Stage on C:high / D:low** — log and hold, don't ship. Gate activation on either
   (a) diffusion rising into IL/mainstream discourse, or (b) a corpus count showing enough affected
   SKUs to justify a bespoke conditional over an editorial category-note.

## Corpus count result (2026-07-01) — scoping fact
Counted across all live comparison JSON in `bari-web/src/data/comparisons/` (per-product, VM schema).
**30 live SKUs contain sucralose (E955/סוכרלוז). Of those, only 3 are baked (fine-bakery):**
- `cookies_coffee` — עוגיות ללת"ס מקמח מלא **(D)**; עוגיות חמאה ללת"ס **(D)**  [both biscuit, d4 E955]
- `cakes_hard_cookies` — עוגת גבינה פירורים לייט **(E)**  [d4 E955]

The other 27 are **non-baked**, where EFSA's heated hazard does not apply: protein_combined (15),
protein_bars (8), juices (3), chocolate_tablets (1).

**Decisive observation:** all 3 baked sucralose SKUs already score **D/E** — bottom of their
categories, and the sweetener is *already* penalised (Tier-C fires today; the D cookies' own
rowVerdict names מלטיטול/סוכרלוז as the D driver). A heated-specific severity bump would nudge three
already-low scores marginally lower and **change no standing, no ranking, no grade that matters.**

## Scoping decision (nutrition-agent call, autonomy default)
**Do NOT build an engine branch. Route as an editorial / category-caveat candidate, and HOLD the EV.**
An application-conditional sucralose penalty is not worth engine complexity for 3 bottom-dwelling SKUs
where sucralose is already penalised. Revisit ONLY if a future sugar-free *baked* category launches with
more affected SKUs **and** higher grades (where a heated bump could actually move standing). The EFSA
finding stays on the watchlist as a potential **category-caveat / radar note**, not an EV activation.

## Definition of Done (this task)
- [x] **Corpus count** — done 2026-07-01: 3 baked SKUs (all D/E), 27 non-baked. Scopes out the engine branch.
- [~] **Research Agent retrieval** of the opinion (doi:10.2903/j.efsa.2026.9854) — DEFERRED. Only needed
      if a revisit trigger fires; not worth the pull for a note on 3 bottom-dwellers today.
- [~] **EV-### stub** — DEFERRED. Decision is editorial/radar note, not EV activation (see above).
- [ ] **On trigger only** (future sugar-free baked category with more SKUs + higher grades): reopen,
      retrieve opinion, and re-run the corpus count before any D6/D7 consideration.

## Card posture
IN_PROGRESS as a **living watchlist card**, not active build. Active deliverable (register + scope) is
complete; the card persists to hold the revisit trigger. No score touched, firewall intact.

## Do NOT
- Do not move any published score.
- Do not add a heated-sucralose branch to the engine without EV-### + D7 + owner gate.
- Do not let the EFSA opinion enter any runtime read path (firewall).
