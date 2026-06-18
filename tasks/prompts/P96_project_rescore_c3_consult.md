# P96 / Project Rescore — strategic premise + math + plan consult (route: C3)

You are C3, the orchestrator's outside-the-family strong advisor. This is an **advice-only** consult for
a major Bari scoring program (TASK-278). Reason hard, take clear positions, and for each question give the
strongest counter-argument **against** your own position. You do not write code and you do not decide;
you pressure-test. Flag anything you think we have wrong.

**Return format:** Three sections (Q1, Q2, Q3). Each: your position → strongest counter-argument → (Q2
also: concrete formulas). End with a short "what we're not seeing" list.

---

## Background (what Bari is, and the problem)

Bari scores packaged supermarket products on a single A–E / 0–100 nutritional scale and presents them as
**per-category comparison pages** ("the shelf"): a biscuits page, a yogurts page, a brined-cheese page,
etc. Each page is built from a real retail shelf we scraped (typically 20–60 products).

**Current scoring** uses, among ~10 weighted dimensions, **hard caps tied to the Israeli Ministry of
Health binary "red-label" thresholds**: sugar ≥17.5 g/100g, saturated fat ≥5 g/100g, sodium ≥600 mg/100g.
Crossing a threshold (or ≥2) triggers a **hard score cap** (a ceiling), regardless of how far over the line
the product is or how it compares to its shelf.

**The failure mode** (observed repeatedly): the cliff collapses within-category differentiation.
- Brined cheese: 42 of 48 products pinned at exactly 72 by the sodium cap — a clean NOVA-1 low-fat cheese
  scored identically to a processed NOVA-3 high-fat one. The salt is *structural* (brine is the preservation
  medium), not a reformulation choice, so the cliff punished the whole shelf flat.
- Cookies/biscuits: most products pinned into D/E by the "≥2 red labels" cap (25/61 bound at cap 45) — a
  genuinely better spelt petit-beurre scored the same as industrial sandwich cookies.

**Owner directive (the program):** stop anchoring scores on the binary red-label caps. Move to a
**category-relative** model — for a biscuit, look at where it sits on the *sugar distribution of the actual
biscuit shelf we scraped* (e.g. distance from the shelf mean/median), not whether it crossed a fixed
government threshold. Rank relatively within the category.

**What already exists (important):** we already built and shipped exactly this for ONE nutrient in ONE
category family. `BARI_SODIUM_SHELF_RELATIVE_V1` (EV-056): at run start we compute the shelf's sodium
**median and stdev** over the scraped corpus; each product gets a penalty banded on its **distance above the
shelf median**; and there's a **low-variance guard** — if the shelf's stdev is below a threshold (everyone's
about the same), the relative surcharge is suppressed so we don't manufacture differences on a uniform shelf.
It uses median (robust to outliers). The shelf stats are frozen into the run record for reproducibility. This
program generalizes that prototype across nutrients (sugar, sat-fat) and categories.

**A philosophical line our own nutrition lead drew, that the owner's directive now pushes against:** we
currently say relative/graduated treatment is honest where a nutrient is *endemic/structural* to the food
class (brine salt in cheese — the maker can't remove it without destroying the product), but a *hard cliff*
is honest where the nutrient is a pure *formulation choice* (sugar a maker chose to add to a biscuit; they
could make it with less). The owner's biscuit-sugar example pushes relative ranking into formulation-choice
territory. This tension is the crux of Q1.

---

## QUESTION 1 — Is category-relative (distance-from-shelf-distribution) scoring the right logic?

We are NOT asking "relative or absolute." Pressure-test a specific synthesis and name its failure modes.

Our current thinking (challenge it): **Don't *replace* absolute nutrition with relative ranking — keep an
absolute backbone and add relative differentiation on top.** Concretely:
- The hard cliff is replaced by a *graduated* absolute penalty (more sugar = more penalty, continuously),
  which keeps the score honest in nutritional terms and prevents a junk shelf from looking healthy.
- A *category-relative* component then restores within-shelf resolution (where you sit vs the shelf), which
  is the information a shopper on a comparison page actually wants.

Stress-test specifically:
1. **Curve-grading / "best of a bad shelf" immunity.** Pure relative scoring gives the best product on a
   terrible shelf a high grade. Bari has a hard rule against this ("no snack bar reaches A" is a frozen
   invariant). Does absolute-backbone-plus-relative actually prevent curve-grading, or does it leak? How
   would you prevent it cleanly?
2. **Cross-category comparability.** Bari shows ONE A–E scale across all categories. If a biscuit is scored
   relative to biscuits and a yogurt relative to yogurts, does a 75/B biscuit "mean" the same as a 75/B
   yogurt? Is it acceptable for Bari's scale to be explicitly category-relative (with copy that says "best
   on this shelf, but this is an indulgence category"), or must an absolute backbone keep the number
   cross-category meaningful? **This is the single biggest design fork — give us your strongest view.**
3. **Endemic vs formulation.** Is the endemic/formulation distinction (relative for structural nutrients,
   cliff for formulation nutrients) a real principle to preserve, or a false distinction? If a shopper just
   wants the least-bad biscuit, does it matter *why* the sugar is there?
4. **Corpus dependence / gaming.** A relative score depends on what we scraped. Adding/removing one extreme
   product shifts everyone's score. What discipline keeps scores reproducible, non-drifting, and ungameable?

## QUESTION 2 — Best mathematical model for the relative component

We score 20–60 products per shelf; nutrient distributions are often **right-skewed** (a few very-high-sugar
outliers) and **small-n**. Candidate models — give a **ranked recommendation with concrete formulas**:

- **Standard z-score** (x − μ)/σ — simple, but σ unstable at small n and inflated by skew/outliers.
- **Robust z** (x − median)/MAD (or /IQR) — robust to outliers/skew. (Our sodium code uses median + a stdev
  guard; MAD would be a cleaner robust scale.)
- **Empirical percentile / rank** — maximally interpretable ("lower-sugar than 80% of the shelf"),
  distribution-free; but loses magnitude (a 2g spread looks as dramatic as a 30g spread).
- **Banded distance-above-median** (our current shipped sodium approach) — coarse, stable, auditable.

Address concretely:
1. **Which scale** for n≈20–60, right-skewed: σ, MAD, IQR, or percentile? Formula.
2. **One-sided vs two-sided:** for sugar in biscuits, penalize only above-median, or also *reward*
   below-median? Does the answer differ for a "bad" nutrient (sugar) vs a "good" one (protein)?
3. **Mapping function:** turning the relative statistic into score points — clamped linear, logistic/tanh
   (bounded, smooth), or discrete bands? We want bounded, monotone, auditable.
4. **Blending with the absolute backbone:** fixed-weight sum? Relative only breaks ties *within* an absolute
   band (lexicographic)? Relative scales the absolute penalty? Which best preserves cross-category meaning
   while restoring within-shelf resolution?
5. **Small-n / low-variance:** when do we *not* differentiate at all? Principled guard (min n, min coefficient
   of variation, min IQR)? How to handle skew so one outlier doesn't define the scale?

## QUESTION 3 — Implementation plan across all current shelves — sanity-check it

Live/in-flight categories: milk (frozen, must not move), yogurt, brined cheese (already shelf-relative on
sodium), hard cheese, cheese-spreads, bread, breakfast cereals, granola, snack bars, salty snacks,
cookies/biscuits, frozen vegetables. Each rescore that moves a *published* score requires: frozen categories
byte-identical, a 342-case invariant suite passing, flag-gated + reversible, evidence-registry entry, and
explicit owner sign-off before go-live.

Proposed phasing (critique sequencing, risk, gaps):
- **Phase 0** — Spec + this consult + internal nutrition/product sign-off on the Q1 philosophy fork.
- **Phase 1** — Generalize the EV-056 sodium-shelf-relative function into a category-agnostic, nutrient-
  agnostic "shelf-relative differentiator" (params: nutrient, scope categories, one/two-sided, scale,
  mapping, low-variance guard), behind a new default-off flag. Freeze shelf stats into run records.
- **Phase 2** — Pilot on ONE category that surfaced this: **biscuits/cookies, nutrient = sugar.** Rescore;
  compare distribution vs the cliff baseline; verify within-shelf resolution restored AND no curve-grading
  immunity (the shelf doesn't float up wholesale).
- **Phase 3** — No-regression gauntlet: frozen milk byte-identical, all published categories byte-identical
  under flag-off, invariant suite green, owner sees before/after published distribution.
- **Phase 4** — Roll out category-by-category and nutrient-by-nutrient (sugar → sat-fat → sodium done), each
  its own evidence entry + sign-off + owner go-live. De-anchor the page COPY in parallel (replace "crosses 2
  red labels" framing with "where this sits on the shelf").

Questions:
1. Is **biscuits/sugar** the right first pilot, or is a category where the cliff does the *least* damage a
   safer first move? What pilot most cleanly proves the model without conflating effects?
2. What migration discipline keeps the A–E scale coherent *while* categories are half-migrated (some
   relative, some still on cliffs)? Is a mixed-scale interim acceptable to ship?
3. What are we **not** seeing — the failure mode that bites us in 3 months?
