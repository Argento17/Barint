# Supplement Guides Re-Direction — Strategy Brief v1 (TASK-504)

**Author:** Orchestrator (C4), synthesizing the owner directive of 2026-07-04.
**Status:** DRAFT FOR CONSULTATION — Product Agent (scope co-sign), Nutrition Agent
(science co-sign), Adversarial QA (strategy red-team), C3 (independent challenge).
Nothing here is approved for build until consults return and the owner accepts the
concrete plan.
**Program authority:** owner-initiated (tripwire 3 cleared by origin — the owner is
starting this program himself). Buy-button/affiliate execution remains owner-gated
(tripwire 4) when real agreements appear.

---

## 1. The owner directive (2026-07-04, verbatim intent)

1. **Ranking supplements does not work.** The creatine comparison confirmed it, and the
   owner doubts the magnesium ranking too. Ordinal product rankings for supplements are
   retired as a product form.
2. **The supplement comparison guides come out of the comparisons category.** A new
   top-level category launches: **מדריכים (Guides)**. Supplements are the first
   occupants; other areas may follow later ("morph").
3. **The guide format:** keep the same card structure on the hub, but the page itself is
   a **detailed guide + information + real product comparison, but smarter** — no grades,
   organized around the attributes that make a supplement good or not (absorption,
   quantity, chemical compound).
4. **Worldwide benchmarks stay** — show where each product sits against the benchmark.
5. **Pricing differences shown clearly.**
6. **Clear linkage to buy** — just the button for now.
7. **Complementary data and information on the page** (which exists) — presented smartly.
8. Owner asked to be challenged before execution; the orchestrator's challenge (below)
   was delivered and the owner ordered this consultation round.

## 2. Diagnosis — what actually failed (orchestrator read, challenge it)

- The creatine page was already grade-free and attribute-based. What failed was the
  **frame**: a row-grid labeled "השוואה" promises a verdict and delivers columns. The
  product form (comparison table) and the content (equivalence + honesty bars) were
  mismatched.
- The engine itself had already ruled the underlying truth: creatine products are
  substantively equivalent (monohydrate is monohydrate); forcing differentiation is
  manufactured (butter-clustering precedent). Supplements as a class have thin
  legitimate ordinal differentiation.
- Magnesium is the partial exception: form-driven absorption differences (citrate/
  bisglycinate vs oxide) and UL crossings are real, science-backed differentiation —
  but tier-level, never rank-6-vs-rank-7-level.

## 3. Proposed product shape (for consult — this is the thing to attack)

**A guide (מדריך) =** one page per supplement with four layers:

1. **"What you should know before buying" spine** — the educational guide: what the
   supplement does (evidence-tiered, from the existing dossiers), what an effective dose
   is, which chemical forms exist and how they differ in absorption, what third-party
   verification means, safety notes (UL, contraindication flags).
2. **Honest bars, verdict-per-attribute** — every real product (Israeli shelf +
   worldwide benchmark) assessed pass / flag / fail per attribute:
   - **Quantity** (dose adequacy vs the literature-derived effective range; undisclosed
     = its own flag, per the missing-data discard rule)
   - **Compound/form** (absorbable form vs low-bioavailability form; tier by form class,
     not by product)
   - **Verification** (two-tier: directory-confirmed vs manufacturer-stated)
   - **Price fairness** (price per effective unit — ₪/absorbed-mg or ₪/effective-gram)
3. **The shortlist** — the page's headline output: products that clear every bar,
   UNORDERED. Clarity without fake precision. (This is the orchestrator's main addition
   to the owner's spec — a guide with no verdict layer fails the one-read test.)
4. **Benchmark placement + buy** — where each product sits vs the worldwide benchmark
   set (price, dose, verification), and a buy button per listed product (plain retailer
   link for v1, no affiliate params; buyUrl slot from TASK-427 already exists dormant).

**Hub:** `/madrichim` (consistent with the /hashvaot transliteration pattern), same card
structure as today's hub cards. Supplements leave the comparisons hub in the same PR
that the guides hub ships (no half-migrated state). 301s: `/hashvaot/magnesium` and
`/hashvaot/creatine` → their guide successors. `/hashvaot/supplements` → `/madrichim`.

**Magnesium call (recommendation):** keep form-tier bands + UL safety flags (they are
defensible science); drop the ordinal 1–18 list and the numeric score. Creatine: fully
flat, bars only. This preserves the strongest finding Bari owns in supplements (oxide is
cheap because the body discards most of it) inside the new format.

**Scope discipline:** v1 = supplements ONLY (magnesium + creatine, the two live data
sets). "Morph to other areas" is explicitly parked until the format proves itself. Food
comparisons are untouched — they have a working scored engine; nothing about this
program leaks into food scoring or the zero-different-category mandate for food.

## 4. What survives the pivot (asset inventory — nothing substantial is lost)

- Evidence dossiers + co-signs (creatine 20-claim tiered base; magnesium model v3
  absorbed-mg machinery → becomes the absorption-attribute display)
- Worldwide benchmarks (13 creatine products / 5 regions, NSF two-tier verification;
  magnesium worldwide set)
- Shelf scrapes (18 creatine IL; 18 magnesium IL; functional-dairy 44)
- Dose-honesty bands (functional_dose_ingredient_ruling_v1 §3.2)
- Price-per-effective-gram / price-per-absorbed-mg computations
- The live pages' data files (creatine-page-data.ts, magnesium-page-data.ts) — content
  re-shapes, data carries
- TASK-427 dormant buyUrl slot
- Paused-but-built: TASK-492B functional-dairy blog (unaffected in substance; re-gate
  after strategy settles), TASK-503 hub card (moot in current form; parked)

## 5. Known tensions the consults must resolve

- **T1 (trust):** Buy buttons vs אי-תלות (independence is the brand moat). Proposed
  rules: visible disclosure; buttons on every product that clears the bar, never
  selectively; verdict data and buy-link data in separate files so no affiliate deal can
  touch a verdict. Is that sufficient? What else?
- **T2 (clarity):** Does verdict-per-attribute + unordered shortlist deliver the
  one-read test, or does it still under-serve the "just tell me what to buy" user?
- **T3 (magnesium):** Are form-tier bands + UL flags defensible as retained verdicts, or
  does honesty require going fully flat there too? (Nutrition owns this.)
- **T4 (scope):** Is two guides (magnesium, creatine) the right v1, or one golden guide
  first? Which is the golden template?
- **T5 (SEO):** URL migration plan — anything wrong with /madrichim + 301s in one PR?
- **T6 (naming):** Is "מדריכים" the right consumer label for what these pages are?

## 6. Explicitly out of scope for v1

- Any change to food-category comparisons, scoring, or the BSIP2 engine.
- Affiliate agreements/params (owner-gated when real).
- New supplement categories beyond magnesium + creatine.
- "Morphing" guides to non-supplement areas.

## 7. Consultation questions

- **Product Agent:** MVP cut + sequencing; T2, T4, T6; anti-overbuild check on the
  4-layer page; go/no-go recommendation shape; does the shortlist concept hold as the
  page's headline output; buy-button v1 product rules.
- **Nutrition Agent:** T3 (magnesium tiers); is the attribute set (quantity/form/
  verification/price-fairness) scientifically complete and honest for supplements as a
  class; which claims are defensible in guide copy; UL/safety flag treatment; any
  attribute we're missing (e.g., form-specific side-effect profiles).
- **Adversarial QA (strategy red-team):** attack the whole shape — T1 hardest (buy
  button vs independence); can every element be publicly defended; failure modes where
  the guide misleads (shortlist read as endorsement, benchmark read as ranking-by-
  stealth, undisclosed-dose flag read as accusation); migration risks.
- **C3 (independent challenge):** challenge the premise itself — is retiring supplement
  rankings right, is "guides" the right product form, what would a smarter alternative
  look like, what is the strongest argument AGAINST this redirection.
