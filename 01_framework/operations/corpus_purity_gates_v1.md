# Corpus Purity Gates v1 — three hard gates born from the cereals contamination (TASK-140)

**Status:** ACTIVE · **Owner directive:** 2026-06-05 · **Origin:** breakfast-cereals run_cereals_002/004
shipped 13 non-cereals to the live site — 10 Israeli **ptitim pasta** (`פתיתים אפויים [shape]` +
organic spelt ptitim) and 3 yeast-leavened **breads** (`כוסמין מלא 100%` etc.). One pasta product
(`פתיתים אורגנים כוסמין`) was whitelisted to **A and ranked #1**. Root cause was misdiagnosis: the
contamination was treated as a *scoring* problem (lower the grade via NOVA fixes) instead of a
*corpus* problem (the product is not the food the category claims to compare).

These three gates are **category-agnostic** and apply to every factory run. They are enforced at the
stages named below and referenced from `03_operations/factory/category_factory_v1.md`.

---

## GATE 1 — Contamination ≠ calibration (the prime rule)

**A product that is the wrong *food* is removed at curation. It is never "fixed" by re-grading.**

- If a product does not belong to the category's food class (pasta on a cereal shelf, a bread loaf
  among RTE cereals, a drink among yogurts), the only correct action is **exclusion at Stage 6
  (Corpus Cleanup)** with a named reason. Lowering its score, adjusting NOVA, or capping its grade is
  **prohibited** — a low grade still leaves a non-cereal *on the cereal page*, distorting the set.
- Signal to catch the trap: a "shaped baked flake / NOVA under-call / grade-too-high" finding on a
  product whose **name or ingredients do not describe the category food** is a contamination finding
  in disguise. Route it to curation, not to the scoring engine.
- Engine changes (NOVA, recal, additive rules) **may not be used to suppress a contaminant.** If you
  find yourself tuning a score to make a product "look right" for the page, stop — exclude it.

**Enforced at:** Stage 6 (Corpus Cleanup), Stage 8 (QA Gate review of every grade-A and every
top-decile product against its name + ingredient panel).

## GATE 2 — Leaderboard integrity (no unapproved product at the top)

**A product that is not nutrition/display-approved may not occupy a top-of-leaderboard position.**

- A product flagged `nutrition_approved: false` / `display_approved: false` (pending Nutrition review,
  unresolved NOVA, contamination suspicion) is a **hard block on promotion** if it would render at or
  above any **approved** product — and unconditionally if it would be **rank #1**.
- The frontend promotion/build step must **abort** (not warn) when this is violated. A category does
  not go live with an unverified product as its face.
- Rationale: run_004 shipped an unapproved pasta product to #1/A. A warning was logged and ignored.
  Warnings do not gate; this gate does.

**Enforced at:** Stage 10 (Website Readiness) — promotion script assertion. See
`split_cereals_005_frontend.py` (regression + authored-copy assertions) for the enforcement pattern.

## GATE 3 — First-batch owner consult (after any BSIP0 / corpus calibration)

**The first category batch produced after a change to BSIP0 acquisition, the corpus include/exclude
filter, or scoring calibration is OWNER-GATED before live promotion.**

- "First batch after calibration" = the first full factory run that executes on a *new or changed*
  scraper, curation filter, or engine calibration flag. It **cannot auto-promote to live.**
- The owning agent produces the run summary + a one-screen diff (counts, grade distribution,
  leaderboard top 5, exclusion tally with reasons) and **routes it to the owner for sign-off.**
- This is a **consumer-facing-irreversible** tripwire under the Decision Authority Matrix: shipping a
  freshly-calibrated category is exactly the "irreversible AND consumer-facing" class. Subsequent
  re-runs on the *same, unchanged* pipeline are routine and do not re-trigger the gate.
- Rationale: the cereals corpus filter was effectively new (first real cereals run) and the first
  batch shipped without owner inspection. Had this gate existed, the pasta-at-#1 would have been
  caught at sign-off.

**Enforced at:** Stage 10 (Website Readiness) — promotion is blocked pending owner sign-off; logged in
the registry on the owning `TASK-XXX`.

## GATE 4 — One canonical nutrition-extraction path (no per-scraper re-implementation)

**Every Shufersal scraper and BSIP0→BSIP1 builder extracts nutrition through the ONE shared
function set in `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`. No category may
re-implement label classification or raw-string→float parsing.**

Origin: the `"פחות מ 0.5"` total-fat mis-capture (EV-029) recurred a **3rd time** in
`run_cereals_005` (TASK-192). EV-029 fixed the shared parser but two leaks let the bug come
back: (a) a per-category builder re-implemented the raw→float layer, and (b) the shared
parser's "of which" sub-row marker list missed the Hebrew final-mem form `מתוכם`. The
permanent fix is a single tested path with three invariants every consumer inherits:

1. **Total fat comes from the total row only.** An "of which" sub-row
   (`מתוכם/מתוכן/מתוכו … שומן`, saturated/trans) may NEVER populate the parent total-fat
   field. Same rule for sugars vs carbs. (`classify_nutr_label` + `_SUBROW_MARKERS`, which
   cover **every** Hebrew final-form of the "of which" stem.)
2. **`"פחות מ N"` / `"<N"` / `"עד N"` is a value < N, and is labelled as an upper bound** —
   never silently flattened to N and forgotten. (`parse_value_bound`.)
3. **`total_fat >= saturated_fat` is enforced.** A panel violating it is not silently
   repaired (that masks the upstream defect) — it is flagged (`_integrity` →
   `sat_gt_total_fat`) so the BLOCKING QA guard fails the run loudly.

The single entry points are `parse_nutrition_list` / `parse_nutrition_rows` (scrape layer,
label→field) and `parse_nutrition_numeric` / `parse_num` / `parse_sodium_mg` /
`parse_value_bound` (build layer, raw→float). Migrating a clean panel to these is
**byte-identical** by construction (proven in `_shared/test_bsip0_nutrition.py`, 12 tests).
A new category scraper/builder that hand-rolls its own nutrition parse is a gate violation.

**Enforced at:** Stage 4 (BSIP0 acquisition) + Stage 5 (BSIP1 enrichment) — every consumer
imports the shared functions; the permanent QA data-integrity guard (COV-006 successor)
hard-fails any build whose panels trip the three invariants (a `"פחות מ"` token in a total
field, `total_fat < saturated_fat`, fat implausibly low vs energy, or sodium >~2,000 mg/100g).
Reference: evidence registry **EV-046** (EV-029 family); tests
`03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py`.

---

## Detection helpers added to the cereals pipeline (reusable pattern)

- **Ptitim/pasta exclusion (EV-045):** a name *headed* by the plural noun `פתיתים` (vs. the construct
  `פתיתי X` = flakes-of-X, which is cereal), `פתיתים אפויים`, pasta-shape tokens, or a flour(+water)
  ingredient signature → excluded as `ptitim_pasta_excluded`.
- **Bread-leakage exclusion (EV-045):** yeast / sourdough / "מהלחם" in the ingredient panel → excluded
  as `bread_ingredient_leakage` (RTE cereals are not leavened). **Word-boundary required:** the yeast
  word `שמרים` is a substring of the preservatives word `משמרים` ("ללא חומרים משמרים" = *no*
  preservatives) — a naive match falsely excludes Nesquik / Cini Minis / Lion. (EV-029 substring-trap
  family.)

These live in `03_operations/bsip0/scrape/shufersal_cereals/02_build_bsip1_cereals.py` and the scraper
`01_scrape_cereals.py`. Generalize the *principle* (name-head disambiguation + ingredient-signature +
Hebrew word boundaries), not the specific tokens, when authoring a new category's filter.
