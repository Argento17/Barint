# Nutrition Opinion — Granola/Cereal Sodium Scoring Gap

**Author:** Nutrition Agent
**Date:** 2026-06-05
**Task:** TASK-189 (owner=nutrition-agent, `roadmap_impact: true`)
**Status:** OPINION ONLY — no scores or engine code changed. Any score movement requires
Product + owner D7 sign-off (published-scores tripwire).
**Evidence base:** `run_cereals_005` traces
(`02_products/breakfast_cereals/bsip2_outputs/run_cereals_005/products/<id>/bsip2_trace.json`),
the live page `bari-web/src/data/comparisons/granola_frontend_v1.json` (53 products),
engine `03_operations/bsip2/proto_v0/src/score_engine.py`, constants `…/constants.py`.

---

## Bottom line up front

The owner's instinct is **correct**. Sodium is a real, displayed property of this category
and the engine ignores it across the entire realistic range. A granola literally named
"מלוח" (salted), displaying **394 mg/100g** on a **504 kcal** product, scores **66/B** —
and sodium contributed **exactly nothing** to that grade
(`regulatory_quality=95`, no sodium cap, no sodium penalty; trace `bsip1_cereal_7290106773714`).
That is a defensible nutritional miss, and it is fixable with a narrow, evidence-grounded rule.

But two of the briefed findings need correcting against what the traces actually show:

- **The null-misfire is REFUTED.** In `run_cereals_005`, **zero** of 66 traces have
  `sodium_mg = null`. Every product the engine scored had a sodium value. The
  `HIGH_SODIUM_700MG_PLUS` cap never fired on a null product — it fired only on products
  whose sodium was a **unit-mangled garbage value** (4,000–10,000 mg/100g). So there is no
  null→cap misfire to fix in the engine. There IS a separate, real **frontend display gap**
  (engine saw sodium, the page shows `null` for 14 products) — the inverse problem.
- **The dominant data problem is not nulls, it is unit corruption** — and a sibling **fat
  collapse** (granola showing `fat = 0.5 g`, which is impossible for granola). Both must be
  understood before any sodium threshold is set, or a new rule will sit on dirty inputs.

---

## 1. Is the sodium gap a real nutritional problem for this category?

**Yes — Moderate-to-Strong evidence, with one important nuance about serving size.**

### What the evidence says

- **Israeli MoH red-label threshold for sodium (solids) = 600 mg/100g** (in the engine at
  `RED_LABEL_THRESHOLDS["sodium"] = 600.0`). The Israeli regulatory line itself treats
  sodium ≥ ~500–600 mg/100g as the "high" mandatory-warning band for solid foods. So the
  state has already drawn a line, and the real granola band brushes right up against it.
- **Typical breakfast-cereal/granola sodium is genuinely bimodal.** A clean own-the-oats
  granola (oats + nuts + dried fruit + a little oil/honey) carries **near-zero added
  sodium** — the 20–100 mg/100g band the owner cited as the benchmark is exactly right for
  that archetype. Mainstream flaked/extruded cereals and "savory-leaning" mueslis carry
  **300–500 mg/100g** because salt is a formulation/palatability ingredient, not an
  intrinsic one. International generics bear this out (USDA FDC: many ready-to-eat cereals
  sit 400–700 mg/100g; granolas typically far lower). This is a *processing/formulation*
  signal, which is precisely the kind of thing Bari exists to surface.

### What the run_cereals_005 distribution shows (verified)

The real, plausible sodium band on this shelf, excluding the unit-corrupted entries:

| Displayed sodium | Example | kcal | Score/Grade | Sodium's effect on score |
|---|---|---|---|---|
| 463 mg | Honey Roasted Cereal w/ Granola | 533 | 36/D | none (D is from calories) |
| 400 mg | מוזלי בוטנים/לוז/שקדים | 384 | 52/C | none |
| **394 mg** | **גרנולה מיקס קראנץ' מלוח** | **504** | **66/B** | **none** |
| 380 mg | מוזלי קראנצי תפוח קינמון | 394 | 58/C | none |
| 350 mg | מוזלי קראנצ'י / מוזלי 30% פירות | 385–424 | 55–58/C | none |
| 600 mg | (cereal) | — | 69.8/B | **none** — sits exactly ON the threshold |

Two things stand out:

1. The salty cluster (350–463 mg) sits **below both the 600 mg red-label and the 700 mg
   cap**, so it takes **zero** sodium action. Grades are driven entirely by calorie density
   and NOVA processing caps (the 394 mg "מלוח" product is bound by `SNACK_BAR_HIGH_CAL=70`
   and `NOVA_PROXY_3_PROCESSED`, never by sodium).
2. The product at **exactly 600 mg** gets `regulatory_quality=95` ("no red labels") because
   the red-label test is strictly `> 600`. So even the genuine red-label boundary lets
   600 mg through clean. (`signal_extractor.py:835` — `nn["sodium_mg"] > 600`.)

### The serving-size nuance (be honest about this)

Bari scores per-100g, which is correct for cross-product comparison. But 394 mg/100g at a
realistic **40–50 g granola serving = ~160–200 mg sodium per bowl** — meaningful but not
alarming on its own (a slice of bread is similar). The strongest framing is **not** "this
bowl is dangerous"; it is **"this is a formulation choice that a clean granola in the same
category simply doesn't make."** That is a *category-relative* statement, and it is exactly
how Bari already frames everything else. The owner's "394 screams; benchmark ~20–100" is
nutritionally sound **as a category-relative observation** — a granola at 394 mg is a clear
outlier against the 20–100 mg clean archetype on the same shelf, even if the absolute
per-serving number is moderate. The rule should bite on that relative gap, framed as
formulation, not as a health alarm (Hard Rule 5).

**Verdict:** the gap is real and worth scoring. The category's own distribution gives us a
clean, defensible calibration anchor (clean archetype ≈ 20–100 mg; salted outliers
≈ 300–500 mg; MoH high line = 600 mg).

---

## 2. Recommended sodium treatment (specific, implementable)

**Design goal:** bite in the real 300–600 mg band, scale with severity, never punish the
genuinely-clean 20–100 mg granola, and never manufacture a grade swing larger than the
nutritional reality. Implement behind a **default-OFF flag** (`BARI_SODIUM_CEREAL`,
mirroring the `RECAL_P0` / `GLASSBOX` pattern), category-scoped to `snack_bar_granola` and
`cereal` only.

### Form: a graduated SODIUM_LOAD penalty + a lowered category cap — not a single cliff

The current single 700 mg cliff is the wrong instrument: it is far above the real range and
it is a cap (a ceiling), so it does nothing until a product is already terrible. Replace the
*effect* (not delete the existing cap) with a **graduated penalty inside the existing
SODIUM_LOAD family** plus one **category-scoped cap** at the genuine high band:

**A. Graduated SODIUM_LOAD penalty (the part that bites the 300–600 band):**

| Sodium (mg/100g) | Penalty | Rationale |
|---|---|---|
| < 150 | 0 | clean granola archetype — fully protected |
| 150–299 | −2 | mild formulation salt; gentle nudge |
| 300–449 | −5 | clear added-salt formulation (the מלוח / salted-muesli band) |
| 450–599 | −8 | approaching the MoH high line |
| ≥ 600 | red-label path (below) | regulatory high band |

These penalties live in the existing `SODIUM_FAMILY_BUDGET = 8` coordination, so they are
budget-bounded and cannot stack into a runaway deduction. (At ≥600 the penalty saturates the
budget; the red-label cap then does the heavier lifting.)

**B. Fix the red-label boundary (within the existing regulatory subsystem):**

Change the sodium red-label test from `> 600` to `>= 600` so a product sitting exactly on the
MoH high line is flagged, not waved through. This is a one-line correctness fix, not a new
rule, but it MUST ride the same flag because it moves the 600 mg product's
`regulatory_quality` from 95 → 60 and trips `ISRAELI_RED_LABELS_2_PLUS` math.

**C. Category-scoped high-sodium cap (replaces the inert 700 cliff for these categories):**

Add `HIGH_SODIUM_CEREAL_500` cap at **500 mg/100g → cap 75** for `snack_bar_granola`/`cereal`
only. This is *above* the clean band, *below* the worst real values, and a cap (not a hard
floor), so it trims the top of high-sodium products without nuking them. Keep the existing
`HIGH_SODIUM_700MG_PLUS=60` as the universal backstop (it correctly catches the
unit-corrupted ≥700 garbage and any genuinely brined outlier).

### Why this shape

- The salted granola (394 mg, currently 66/B) would take a **−5 penalty** → ~61, and with
  the 500-cap untouched (it's under 500) it lands mid/low-C. That is the right answer: a
  504-kcal product literally named "salted" should not out-grade a clean 410-kcal granola.
- A clean 410-kcal/40 mg granola (currently ~66–71/B) is **completely untouched** (penalty
  band starts at 150 mg). No distortion of the genuinely-low-sodium products — the explicit
  design requirement.
- Everything stays inside the family budget, so this cannot interact pathologically with the
  sugar/calorie families.

### Rollback + verification (governance contract)

- Single flag `BARI_SODIUM_CEREAL=on`; OFF → engine byte-identical (assert via the existing
  `verify_*_off_identical.py` harness pattern).
- Required deliverable before D7: a **before/after score-delta table** for all 53 live
  granola products + the cereal page, classifying every move as expected/unexpected.
- EV-### evidence-registry entry citing the MoH 600 mg line + the category sodium
  distribution as the calibration anchor.

---

## 3. Scope: category-specific or cross-category?

**Keep the new penalty and the 500-cap CATEGORY-SCOPED to `snack_bar_granola` + `cereal`.
Do NOT generalize.** Reasons:

- The 150 mg "clean floor" is only correct for a category whose clean archetype is genuinely
  near-zero sodium. It would be **wrong** for bread (a clean sourdough is legitimately
  ~400–500 mg/100g — salt is structural to bread, not a palatability add), wrong for cheese,
  wrong for any brined/cultured food. A 300 mg bread penalty would be a nutritional error.
- **Frozen-invariant risk if generalized:** Bread scores are frozen on
  `real_bread_retail_003_v1`; milk on `run_005_headpin`; snacks at the snk-001=70/B ceiling.
  A cross-category sodium penalty would silently move bread (most affected — bread sodium is
  routinely 350–550 mg), which trips the frozen-invariant tripwire and contaminates a frozen
  baseline. **Hard stop.** Any sodium treatment that touches bread/milk/snacks must be its
  own governed task with its own freeze re-verification, not a side effect of TASK-189.
- The **red-label boundary fix (`>=600`)** is the one piece that is technically global
  (it lives in `signal_extractor`). Two options: (a) gate it behind the same cereal flag and
  apply category-scoped for now (cleanest, zero frozen-category risk), or (b) treat it as a
  global correctness fix and re-verify the frozen baselines. **I recommend (a)** for
  TASK-189 — fix it where the evidence is, leave the global correctness question to a
  dedicated cross-category sodium task. Flag for owner: the `>600` vs `>=600` boundary is a
  latent correctness issue everywhere, but fixing it globally is out of TASK-189 scope.

---

## 4. The null-capture / null-misfire issue

**My read: the briefed null-misfire does not exist in the engine, but there are TWO real
data problems that are MORE severe than the sodium gap and must be addressed first.**

- **Null-misfire: REFUTED.** 0/66 traces have `sodium_mg = null`; the
  `HIGH_SODIUM_700MG_PLUS` cap fired only on products with real (corrupted-high) sodium
  values. There is no null→700 coercion in the scored set. The suspected "capped to 60 on
  null sodium" products are capped to 60 by **other** caps (NOVA-4 `ADDITIVE_MARKERS` /
  calorie caps), not by sodium. Good news — nothing to fix there.

- **REAL problem #1 — unit corruption (must fix before any sodium rule).** Nine products
  carry sodium of **4,000–10,000 mg/100g** — physically impossible (that would be
  10–25% salt by weight). These currently get caught by the 700 cap *by accident*. If we add
  a graduated penalty on top, these garbage values will produce nonsense. **A sanity gate is
  mandatory:** sodium > ~2,000 mg/100g for a cereal/granola is a data-integrity failure →
  route to `confidence` reduction / insufficient-data, do NOT score it as if true. This is a
  cousin of EV-029 (the fat-overwrite bug) and likely the same class of BSIP0 parse error
  (per-serving vs per-100g, or a g↔mg slip).

- **REAL problem #2 — fat collapse (flag to Data/QA, blocks confident scoring).** The live
  page shows `fat = 0.5 g` for granolas that are obviously 10–20 g fat (גרנולה מיקס קראנץ'
  מלוח at 504 kcal shows fat=0.5). This is the same EV-029-family overwrite. It does not
  directly affect the sodium rule, BUT it means `fat_pct_of_kcal` is wrong, which is exactly
  why `HP_FAT_SODIUM` can never fire (it needs high fat%). **Two independent capture bugs are
  conspiring to make every fat/sodium hyper-palatability lever inert.** Fixing fat capture
  may even let the existing `HP_FAT_SODIUM` combo start working on its own.

- **Frontend display gap (separate, lower severity).** 14 frontend products show
  `sodium: null` even though the engine had a value (the 394 "מלוח" engine value is 394, but
  some sibling products' panel sodium did not propagate to the JSON). This is a
  packaging/propagation gap, not a scoring bug. It matters for the **copy** (the page can't
  cite a sodium fact it doesn't display), so it should be reconciled when the copy is
  re-authored, but it does not block the scoring change.

**Sequencing verdict:** fix the **fat + sodium unit-capture** (Data Agent, with a QA sanity
gate) BEFORE turning on any sodium penalty. Otherwise the new rule penalizes corrupted
inputs and we ship a different kind of wrong. This is the one hard dependency.

---

## 5. Are calories + processing weighted correctly for granola? (Brief)

**Calories: yes, working well and correctly dominant.** `calorie_density` is the live
differentiator and it is calibrated sensibly for the format
(`snack_bar_granola` table: 372 kcal→40, 504 kcal→15; caps `SNACK_BAR_HIGH_CAL=70`,
`HIGH_CAL_LOW_SATIETY_SEVERE`). For an energy-dense format that consumers under-portion,
calorie density *should* lead. No change needed.

**Processing: directionally correct, but two caveats.**
- Every granola is NOVA 3 or 4, so the NOVA caps (94.8 / 87 / 68) correctly prevent any
  granola from reaching A. That matches the category reality (granola is a manufactured
  mix). Fine.
- **Under-counted:** with fat capture broken, the `fat_quality` and HP-fat dimensions are
  effectively blind — a granola loaded with palm/seed oil and salt looks the same as a clean
  one on those axes. Once fat capture is fixed, processing/HP signals will sharpen
  considerably. This is the bigger latent inaccuracy, larger than sodium.
- `regulatory_quality` is only weighted **0.05** — so even when a red label DOES fire, its
  direct dimension contribution is tiny. This is *by design* (the real teeth are the caps),
  which is why the sodium fix belongs in the **cap/penalty** layer, not in re-weighting the
  regulatory dimension. Do not raise the regulatory weight to chase this — it would
  reverberate across every category. Confirmed correct to keep the fix in the guardrail
  layer.

**Net:** calories are right; processing is right in shape but **blinded by the fat-capture
bug** — fixing that data bug is higher-value for accuracy than the sodium rule itself.

---

## 6. Recommendation + open questions for the owner

### Recommendation (decisive)

1. **Yes, score sodium for granola/cereal.** The gap is real; the owner's instinct holds.
2. **Fix the data first.** Fat-capture + sodium unit-corruption (EV-029 family) are the
   blocking dependency. Add a sodium sanity gate (>2,000 mg/100g → data-integrity failure).
   This is a Data + QA task that must land before scoring changes.
3. **Then ship the §2 treatment behind `BARI_SODIUM_CEREAL` (default OFF):** graduated
   SODIUM_LOAD penalty (0 / −2 / −5 / −8 across <150 / 150–299 / 300–449 / 450–599), the
   `>=600` red-label boundary fix (category-scoped), and a category `HIGH_SODIUM_CEREAL_500`
   cap at 75. Keep the universal 700 cap as backstop.
4. **Category-scoped only.** Do NOT generalize to bread/milk/snacks — frozen-invariant
   tripwire. A cross-category sodium policy is a separate, later, governed task.
5. **Deliverables before D7:** before/after delta table for all 53 granola + cereal products,
   EV-### registry entry (MoH 600 mg + category distribution as anchor), OFF=byte-identical
   verification, and re-authored granola verdicts so the catch may now cite sodium causally
   (currently it is fact-only per Row Description Standard v2 §6).
6. **Expected directional impact:** the salted/savory cluster (350–463 mg) drops ~5–8 points
   and roughly one grade band; clean low-sodium granolas are untouched. No A appears or
   disappears (none reach A regardless). This is a true grade driver for ~6–9 products →
   published-score movement → owner D7 required.

### Open questions for the owner

1. **Per-serving framing.** Are you comfortable with sodium framed as a *category-relative
   formulation* signal (a salted granola vs the clean archetype), rather than an absolute
   per-bowl health claim? I recommend the former (it's honest and within Hard Rule 5); the
   per-serving number is moderate, so an absolute alarm would overclaim.
2. **Global red-label boundary.** The `>600` vs `>=600` issue is latent in EVERY category.
   Do you want it fixed only for cereal/granola now (my recommendation, zero frozen-category
   risk), or opened as a separate cross-category correctness task that re-verifies the bread/
   milk/snack freezes?
3. **Fat-capture priority.** Fixing the fat-collapse bug is higher-value for overall granola
   accuracy than the sodium rule. Do you want to fold it into TASK-189 as the prerequisite,
   or split it into its own EV-029-family data task that TASK-189 depends on? (I recommend
   the latter — clean dependency, and it likely helps other categories too.)

---

*Constraints honored: no scores or engine code changed. All claims above are verified
against `run_cereals_005` traces, the live granola JSON, and the engine/constants source.
Consumer-facing terms (NOVA/cap/floor/structural_class) are not used in any copy this
opinion would produce.*
