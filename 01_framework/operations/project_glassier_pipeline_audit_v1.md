# Project Glassier — End-to-End Pipeline Audit (BSIP0 → Comparison Page)

**Task:** TASK-233 · **Owner:** Orchestrator · **Date:** 2026-06-10 · **Status:** v1
**Grounded in:** `run_frozen_vegetables_001` + the live code paths (no invented behavior).

This audit walks the full path a category travels from raw shelf data to a live, polished
comparison page. Each STEP states **what runs**, **who owns it**, **weaknesses**, and a
**fix**. The canonical `bari-category-factory` skill documents 8 idealized stages; the *real*
pipeline has the steps below, several of which are **undocumented in the skill** — that gap is
itself finding G-0.

> **G-0 (HIGH) — the documented pipeline ≠ the real pipeline.** The factory skill stops at
> "Frontend Packaging / D4 wiring" and describes generic JSON artifacts (`shelf_map.json`,
> `corpus_filter.json`) that the real runs do not produce. Content authoring, frontend
> integration, design polish, and go-live — the back half of every launch — are not in any
> skill. Fix: replace the idealized stage list with the 14 real steps below; make the skill
> describe what actually happens.

---

## STEP 1 — BSIP0 Extraction (scrape + OCR)

**What runs.** `03_operations/bsip0/scrape/` pulls product pages per retailer (Shufersal for
frozen veg); the Azure OCR pipeline (`bsip0/pipeline/`) reads physical-label images.
`_shared/bsip0_nutrition.py::parse_nutrition_list()` parses the nutrition panel; output lands
in `02_products/{category}/bsip0_outputs/`.

**Agent responsible.** Data Agent (execution). Retailer/shelf selection: Product + Data.

**Weaknesses.**
- **W1.1 (CRITICAL→fixed-once) — dual-table parse.** The ginger record absorbed a per-cube
  *and* a per-100g table into one product; the parser took the wrong column. Fixed by hand in
  scope-clean output, not structurally. EV-029 fixed the fat-overwrite case but the
  multi-table case still has no guard.
- **W1.2 (HIGH) — no scraper-output validation gate.** No duplicate-barcode check, no
  conflicting-nutrition check, no value-range sanity. The salty-snacks corpus shipped fake
  barcodes + dead image hosts precisely because nothing validated BSIP0 output.
- **W1.3 (MEDIUM) — image URL is synthesized from barcode**, not from a scraped/verified asset
  (`MNH68_Z_P_{barcode}_1.png` Cloudinary pattern in the generator). Wrong/missing barcode →
  broken image with no detection.

**Fix.** Add a BSIP0 validation sub-stage that runs before BSIP1 and hard-fails on: duplicate
barcodes, one barcode with conflicting nutrition tables, out-of-range nutrients, and
unreachable image URLs. Make `parse_nutrition_list()` detect multiple tables and record which
basis (per-100g vs per-serving) it selected, into the trace.

---

## STEP 2 — Scope Assignment ("scope-clean")

**What runs.** `evaluation_scope.py` assigns each product a `bsip0_scope_class`
(e.g. `frozen_legume_sold_as_vegetable`, `frozen_herb_or_seasoning`). Frozen veg ran
"scope-clean v2_1." This class later drives routing **and** the frontend cluster.

**Agent responsible.** Data Agent (execution) · Nutrition Agent (class definitions).

**Weaknesses.**
- **W2.1 (HIGH) — scope class silently double-duties as a UI cluster.** `build_cluster()` in
  the generator keys shelf lenses off `bsip0_scope_class` + NOVA. A scope class invented for
  scoring is reused as a consumer-facing grouping with no review that the grouping makes sense
  to a shopper.
- **W2.2 (MEDIUM) — no record of scope-class coverage.** No report says how many products fell
  to a default/"other" scope, the early-warning sign of a missing class.

**Fix.** Emit a scope-coverage report (count per class + default rate). Decouple the UI cluster
from the scoring scope class, or require Content/Design sign-off when a scope class is promoted
to a consumer lens.

---

## STEP 3 — BSIP1 Enrichment

**What runs.** `bsip1/core/ingredient_enricher.py` — Hebrew ingredient detection (whole grain,
additives, fermentation markers), additive burden counting, protein-source typing, matrix
signals, and a BSIP1 trust level (`high|medium|low`). Output: canonical JSON per product +
`ingredients_text_he` (the source D4 wiring later reads). Test suite: `test_enricher.py`
(64 checks).

**Agent responsible.** Data Agent (execution) · Nutrition Agent (enrichment rules).

**Weaknesses.**
- **W3.1 (HIGH) — enrichment coverage isn't gated per run.** The skill says "validate coverage
  meets threshold," but no run artifact records it. D4 wiring has a 15%-ingredient-text floor;
  nothing upstream enforces a floor on the enrichment itself.
- **W3.2 (MEDIUM) — trust level doesn't propagate to the displayed confidence.** BSIP1
  `trust_level` and the engine `confidence_band` are computed separately; the frontend reads
  only the latter (see W11.3 / Step 9 confidence inflation).

**Fix.** Make the BSIP1 run emit `bsip1_enrichment_report.json` (coverage %, label
distribution, low-trust list) and hard-fail below threshold. Carry `trust_level` through to the
trace so confidence display can reflect it.

---

## STEP 4 — Routing (category assignment)

**What runs.** `router_v2.py` — 3-stage routing: (1) hard product-class **anchors**,
(2) context-gated signals (WFF-contamination prevention, beverage gate, dairy-protein
suppression), (3) resolution. Validated by `run_router_regression.py` (12 cases) +
`generate_router_validation.py`.

**Agent responsible.** Data Agent (run) · Nutrition Agent (anchors/methodology).

**Weaknesses.**
- **W4.1 (CRITICAL→recurring) — no anchor-coverage pre-check.** The first frozen-veg run threw
  **35 `CATEGORY_INSTABILITY` flags** because the router had no `frozen_vegetable` anchors. The
  batch runner does not verify the router knows the category before scoring.
- **W4.2 (HIGH) — default routing is not a hard fail.** A product routed by fallback rather
  than an anchor still gets scored and shipped. (hummus→sauce_spread class of error.)

**Fix.** Add a "router anchors registered for {category}?" pre-flight gate (now documented in
`scoring.md` + the QA skill); make default/`conf < 0.50` routing a QA hard fail. Surface a
per-run routing-distribution diff against the prior baseline.

---

## STEP 5 — BSIP2 Scoring

**What runs.** `score_engine.py` (algo v0.4.1) — 6 stages: feature extraction → 10-dimension
scoring → guardrails (vetoes/caps/floors) → hyper-palatability → concern coordination → final
resolution (caps, penalties, floors, confidence ceiling, clamp, `score_to_grade()`). Writes a
`bsip2_trace.json` per product. Batch runner: `batch_run_{category}_NNN.py`.

**Agent responsible.** Data Agent (run) · Nutrition Agent (methodology, rule changes;
co-approval with Product per D7) · QA Agent (value/propagation correctness).

**Weaknesses.**
- **W5.1 (HIGH) — known category-blind spots ship anyway.** The granola/cereal sodium gap
  (engine doesn't penalize granola sodium, TASK-189 open) and the bread/cracker routing gap are
  documented but there is no pre-run "known-gaps for this category" checklist that forces a
  decision before scoring.
- **W5.2 (MEDIUM) — no automated post-run plausibility check.** Salty-snacks shipped a
  6.5g-fiber/12g-protein health cracker at 0/E (TASK-232). Nothing flags rank-order inversions
  or implausible extremes before a human happens to look.
- **W5.3 (MEDIUM) — prototype weights ≠ methodology weights.** `constants.py` weights are
  acknowledged as uncalibrated; the gap is documented but unscheduled.

**Fix.** A per-category "known-gaps acknowledgement" gate (Nutrition signs that the gaps don't
distort this category, or scoring waits). Add an automated post-run sanity pass: rank-order
inversion detector + extreme-score plausibility against known-good pairs.

---

## STEP 6 — QA Gate

**What runs.** `bari-qa-audit` skill protocol: QA runner against enrichment/scoring output,
traceability (product→corpus, label→step, score→rule), hard-fail/warning classification,
baseline freeze. Output: `qa_gate_result.json`.

**Agent responsible.** QA Agent.

**Weaknesses.**
- **W6.1 (HIGH) — leak scan was not a QA hard rule until now.** Internal terms ("NOVA 4")
  reached consumer `limitingFactors` in salty-snacks; `source_traceability_status` (non-VM
  field) shipped on every frozen-veg product. The leak check existed only as tribal knowledge.
  *(Partially closed 2026-06-10: leak + default-routing + nutrition-consistency hard fails were
  just added to the QA skill.)*
- **W6.2 (MEDIUM) — QA runs after scoring, not interleaved.** BSIP0 data-integrity problems
  (Step 1) surface only at the QA gate, after a full scoring run has been spent on bad data.

**Fix.** Keep the new hard fails; add an offline `hebrew_readability.is_clean` gate on all
consumer strings as a standing QA step; move data-integrity checks earlier (Step 1) so QA at
Step 6 is confirmation, not first detection.

---

## STEP 7 — Red-Team Challenge

**What runs.** `red-team-agent` receives the scored corpus + methodology rationale, produces
`02_products/{category}/reports/red_team_{version}.md` with CRITICAL/HIGH/MEDIUM findings. Gate:
no open CRITICAL before advancing.

**Agent responsible.** Red-Team Agent (challenge) · Nutrition (resolves) · Orchestrator (gate).

**Weaknesses.**
- **W7.1 (HIGH) — the gate is skippable in practice.** It's a "required" stage in the skill,
  but the frozen-veg run shows no `reports/red_team_*.md` artifact. Nothing structurally blocks
  frontend packaging when the red-team report is absent.
- **W7.2 (MEDIUM) — severity grading runs hot.** (Meta-finding from this week's external
  review: two of three "critical" bugs were overstated/dormant.) Without a verification step,
  red-team severities can mis-prioritize remediation.

**Fix.** Make the presence of a red-team report with zero open CRITICAL a *machine-checked*
precondition of Step 9 (packaging refuses to run without it). Require each CRITICAL/HIGH to
cite the file:line or product ID it stems from, so severity is verifiable.

---

## STEP 8 — Content Authoring

**What *should* run (per skill / memory).** Content Agent authors the consumer copy: insight
lines (`rowVerdict`), prologue, the yellow "הערת קטגוריה" category note, methodology lines,
`bottomLine`, positive signals, limiting factors — under the Editorial Intelligence v3 +
Assertive Writing standards.

**What *actually* runs.** For frozen veg, **the copy is generated procedurally inside the
Python frontend script** (`build_insight_line`, `build_bottom_line`, `build_positive_signals`,
`build_limiting_factors`) from `grade_estimate` + `scope` + `nova` via hardcoded Hebrew
templates. The page-level prologue/category-note/methodology *are* hand-authored (in the
`*-comparison-page-data.ts`), but the per-product copy is template output.

**Agent responsible.** Content Agent (intended) · Data Agent (de facto, via the generator).

**Weaknesses.**
- **W8.1 (CRITICAL) — editorial copy bypasses the Content Agent.** Per-product consumer
  sentences are emitted by a data script with no editorial review. This is the *root cause* of
  the salty-snacks copy failures (banned "NOVA 4" term, prescriptive "עדיף לבחור…" lines): a
  template author isn't bound by the editorial banned-phrase library.
- **W8.2 (HIGH) — copy logic is reinvented per category.** Each generator hand-rolls its own
  `build_insight_line`. No shared phrase library, no shared banned-term filter, no consistency
  across categories.
- **W8.3 (MEDIUM) — the split between Python copy and TS copy is undocumented.** `insightLine`/
  `bottomLine` are authored in Python; `rowVerdict`/`rowReason`/`metrics` are computed at
  runtime in TS. No doc says which lives where, so every new category re-decides.

**Fix.** Two options, recommend (a): **(a)** extract a shared `bari_copy/` module the generator
calls, with the banned-phrase filter from the editorial standards applied at write time and a
Content Agent review gate on the *templates* (not per product). **(b)** Move all per-product
copy authoring to the Content Agent as a discrete reviewed step that writes a `copy_{category}.json`
the generator merges. Either way: a single banned-term linter must run on 100% of consumer
strings before packaging, and the Python/TS authoring boundary must be written down.

---

## STEP 9 — Frontend JSON Packaging

**What runs.** A bespoke per-category script, e.g.
`generate_frozen_vegetables_frontend.py`: loads traces, sorts by score, derives nutrition,
cluster, copy, confidence, and writes `{category}_frontend_vN.json` directly into
`bari-web/src/data/comparisons/`.

**Agent responsible.** Data Agent.

**Weaknesses.**
- **W9.1 (CRITICAL) — no output schema / contract.** `schemas/` and `docs/` are empty. The
  script reads `final_score_estimate`, `grade_estimate`, `nutrition_components` by key name. If
  the engine renames a field, the generator silently emits `null` — no error. There is no
  validation that the output conforms to `BariProductVM`.
- **W9.2 (HIGH) — confidence inflation.** `build_confidence()` maps **both** `high` *and*
  `medium` engine confidence to `verified` → the product is labeled "מבוסס על נתונים מלאים"
  (based on complete data) even when it isn't. This directly contradicts the
  `score_confidence_indicators_spec_v1` (7-state) model and overstates data backing.
- **W9.3 (HIGH) — internal fields leak by default.** `source_traceability_status` is written
  onto every product though it isn't in `BariProductVM`; `_cluster` must be stripped downstream.
  Stripping is left to each category's TS page-data, which is exactly where the frozen-veg
  shelf-filter bug came from.
- **W9.4 (HIGH) — bespoke per-category scripts.** No shared packaging library → grade logic,
  cluster logic, confidence logic, and copy are re-implemented (and re-bugged) every category.
- **W9.5 (MEDIUM) — provenance string is free text.** `_meta.provenance` is a hand-typed
  sentence; easy to leak internal terms (it was *claimed* to leak "BSIP"/"CATEGORY_INSTABILITY"
  — verified clean for frozen veg, but the format invites it).

**Fix.** Build one shared `generate_frontend_dataset.py` that: (1) validates output against a
committed `schemas/bsip2_frontend_v1.schema.json` and the TS `BariProductVM` shape (fail on
unknown/missing fields); (2) strips all non-VM fields at the source; (3) maps confidence per the
7-state spec (medium ≠ verified); (4) takes copy from Step 8's shared module. Make the per-category
script a thin config (selectors + cluster rules) over this shared core.

---

## STEP 10 — D4 Additive Wiring

**What runs.** `wire_d4_{category}.py` (per the factory skill) runs
`detect_additives_d4(ingredient_text)` over BSIP1 `ingredients_text_he`, enriches each hit with
Hebrew `explanation_he` from `w2_additive_copy_v1.md` (34 E-numbers), writes `d4_additives` into
the JSON, and asserts score/grade/glassBox are byte-identical after. 15%-ingredient-text floor.

**Agent responsible.** Data Agent (script) · Content Agent (copy doc).

**Weaknesses.**
- **W10.1 (MEDIUM) — frozen veg ships `ingredients: None`.** The expansion has no ingredient
  list (generator writes `'ingredients': None`), so D4 wiring has little to bite on for this
  category, and the consumer expansion shows no ingredients at all — a thin glass box.
- **W10.2 (MEDIUM) — D4 is flag-gated and easy to forget.** It's "required" but gated behind
  `NEXT_PUBLIC_GLASSBOX_D5D6`; a category can go live with the key absent and no one notices.

**Fix.** Carry `ingredients_text_he` through to the expansion (not just to D4) so the glass box
shows real ingredients. Add the D4 invariant assertion + coverage line to the QA gate so a
missing-D4 launch is caught.

---

## STEP 11 — Frontend Integration

**What runs.** Frontend wiring in `bari-web`: copy JSON to `src/data/comparisons/`; add the
`*-comparison-page-data.ts` (loads corpus via `loadComparisonCorpus`, strips internal fields,
enriches row surface); add `*-shelf-filters.ts`; register the category; add the route
`src/app/hashvaot/{category}/page.tsx`; the View Model (`src/lib/view-models/index.ts`) is the
BSIP→UI contract.

**Agent responsible.** Frontend Agent · (Cursor historically implements components).

**Weaknesses.**
- **W11.1 (HIGH) — internal-field handling is per-category and fragile.** Frozen veg read
  `_cluster` off the *post-strip* product → every shelf lens returned zero products (latent;
  the lens UI is currently globally disabled by "FIX-5", so it was dormant, not user-visible).
  The correct cheese pattern (read from raw JSON at init) is not enforced. *(Fixed for frozen
  veg 2026-06-10.)*
- **W11.2 (MEDIUM) — grade is computed twice.** Python writes `grade`; `corpus.ts`
  `normalizeGrade()` re-derives it from score and overrides. This is *intentional* (runtime is
  the single source of truth, per the comment) but the two can disagree silently.
- **W11.3 (MEDIUM) — VM conformance isn't checked at import.** `loadComparisonCorpus` spreads
  whatever JSON contains; undeclared fields ride along (W9.3). TypeScript doesn't catch it
  because the JSON is typed loosely.

**Fix.** Provide one shared shelf-filter factory that reads the internal grouping from raw JSON
by id (cheese pattern) so no category re-implements it. Add an import-time assertion that corpus
products match `BariProductVM` (no extra keys). Keep `normalizeGrade` as the sole grade source
but log a warning when it disagrees with the JSON grade (drift detector).

---

## STEP 12 — Design / Frontend Polish

**What runs.** Design Agent owns hierarchy, spacing, RTL, the 72px collapsed-row budget, the
score chip (gradePalette, Hard Rule 1), confidence indicators (`score_confidence_indicators_spec_v1`),
the category caveat box. Frontend Agent implements. Evaluated mobile-first at 375px.

**Agent responsible.** Design Agent (decisions) · Frontend Agent (implementation).

**Weaknesses.**
- **W12.1 (HIGH) — the confidence spec isn't wired to real data.** The 7-state confidence
  layer is an approved spec, but the data feed (Step 9) collapses medium→verified and only
  partially populates `confidence_sub_reason`. The design exists; the data to drive it honestly
  does not yet (ties back to W9.2).
- **W12.2 (MEDIUM) — disabled features ship silently.** Shelf lenses are globally off (FIX-5)
  yet every category still builds, registers, and tests lens code. Dead UI paths accumulate
  (this is what hid the `_cluster` bug).
- **W12.3 (MEDIUM) — metric rendering bugs reach the row.** Unrounded `7.6666…` overlapping
  metric values shipped in salty-snacks before `formatMetricValue` was added — a polish defect
  that QA, not design, caught.

**Fix.** Gate the confidence layer rollout on the data feed implementing the 7-state mapping
(don't ship the visual on inflated data). Track disabled features (FIX-5) in one place with a
re-enable checklist. Add a render-level numeric-format check (rounding, overflow) to the polish
QA pass.

---

## STEP 13 — Pre-Launch QA (propagation + leak + build)

**What runs.** QA Agent's pre-launch checklist: score propagation (trace→JSON→rendered),
leakage scan, routing drift, rank-order sanity, build/lint/route checks (the TASK-232 pattern).

**Agent responsible.** QA Agent.

**Weaknesses.**
- **W13.1 (HIGH) — this is the *first* full integrity check, and it's manual.** Many defects
  (leakage, 0/E inversions, garbled ingredients, duplicate SKUs) are only caught here, late,
  product-by-product. The checks aren't a runnable script.
- **W13.2 (MEDIUM) — no standing regression between categories.** Each launch QA is bespoke;
  there's no shared automated pre-launch suite a new category inherits.

**Fix.** Convert the pre-launch checklist into a runnable validator (`validate_frontend_json.py`
+ a pre-commit hook): leak terms, VM-conformance, null essential fields, duplicate barcodes,
rank-order inversions, image reachability. Make it a required gate, not a manual audit.

---

## STEP 14 — Upload / Go-Live

**What runs.** Merge the preview branch (e.g. `frozen-vegetables-preview`), the route goes
public at `/hashvaot/{category}`, registry task closed by the orchestrator after verifying
return-block claims against artifacts.

**Agent responsible.** Orchestrator (close + dispatch) · Product Agent (go-live decision —
tripwire #2: irreversible + consumer-facing) · Owner (only if a tripwire fires).

**Weaknesses.**
- **W14.1 (MEDIUM) — go-live readiness isn't a single checklist.** Readiness is spread across
  QA, design, content; there's no one "launch gate" artifact that must be green (red-team report
  present? leak scan clean? D4 wired? confidence honest? build green?).
- **W14.2 (LOW) — preview vs. live state isn't tracked in the registry.** "frozen-vegetables
  (preview)" lives in git branch state, not as a registry status, so what's live vs. staged is
  inferred from commits.

**Fix.** A single `launch_gate_{category}.md` that aggregates the green/red of Steps 6–13 and is
the orchestrator's close checklist. Record preview/live state in the category's registry entry.

---

## Weakness Register (prioritized)

| ID | Sev | Step | One-line | Owner |
|----|-----|------|----------|-------|
| W8.1 | CRITICAL | 8 | Per-product consumer copy is generated by a data script, no editorial review → banned-term + prescriptive leaks | Content + Data |
| W9.1 | CRITICAL | 9 | No output schema/contract; engine field rename → silent nulls | Data |
| W4.1 | CRITICAL | 4 | No router-anchor pre-check → mass CATEGORY_INSTABILITY | Data + Nutrition |
| W1.1 | CRITICAL | 1 | Dual-table nutrition parse, fixed by hand not structurally | Data |
| W9.2 | HIGH | 9 | Confidence inflation: medium→"verified/complete data" | Data + Design |
| W9.3/W9.4 | HIGH | 9 | Internal fields leak; bespoke per-category generators | Data |
| W8.2 | HIGH | 8 | Copy logic reinvented per category, no shared phrase/banned library | Content |
| W1.2 | HIGH | 1 | No BSIP0 validation gate (dupes, conflicts, ranges) | Data |
| W7.1 | HIGH | 7 | Red-team gate is skippable (no machine block) | Orchestrator |
| W5.1 | HIGH | 5 | Known category blind-spots ship without an acknowledgement gate | Nutrition |
| W11.1 | HIGH | 11 | Per-category internal-field handling fragile (the `_cluster` bug) | Frontend |
| W6.1 | HIGH | 6 | Leak scan was tribal knowledge (now partly a hard rule) | QA |
| W13.1 | HIGH | 13 | First full integrity check is late + manual | QA |
| W12.1 | HIGH | 12 | Confidence visual not backed by honest data | Design + Data |
| G-0 | HIGH | all | Documented pipeline ≠ real pipeline | Orchestrator |
| (remaining MEDIUM/LOW) | — | — | W2.x, W3.x, W5.2/3, W6.2, W7.2, W10.x, W11.2/3, W12.2/3, W14.x | per table above |

## The three structural root causes (most weaknesses collapse into these)

1. **No shared frontend-packaging core.** Every category hand-rolls copy, cluster, confidence,
   grade, and field-stripping in a bespoke Python script + bespoke TS — so every bug is
   re-introducible. (W8.2, W9.1, W9.3, W9.4, W11.1.)
2. **Validation happens late and by hand.** Data integrity, leak, plausibility, and conformance
   are caught at the QA gate (Step 13), product-by-product, instead of at the boundary they
   originate. (W1.2, W5.2, W6.1, W6.2, W13.1.)
3. **Editorial copy escapes the editorial system.** Consumer sentences are emitted by data code,
   not authored/filtered by Content. (W8.1, W8.2, W9.5.)

Fixing those three — a shared packaging core with a schema, an early+automated validation suite,
and routing per-product copy through Content's banned-term filter — closes the majority of the
register and prevents the next category from repeating frozen-veg and salty-snacks.
