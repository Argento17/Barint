**Task:** TASK-179B

# Bari Glass Box — Six-Dimension Contract (v1)

**Status:** FOUNDATIONAL CONTRACT / DOC ONLY. No engine code, no scoring change, no published score movement, no rewrite of existing governance docs. Reconciliation deltas against those docs are *listed* here, not applied. Adoption of any dimension or rule is a separate Nutrition (D6/D7) + Product co-sign gate, each requiring an evidence-registry entry.

**Author:** Nutrition Agent · **Date:** 2026-06-03 · **Wave:** TASK-179, Wave 0
**Inherits from (must read first):** `C:\Bari\research\glass_box\engine_enrichment_frameworks_scoping_v1.md` (TASK-179A scoping dossier)
**Reconciles against (no rewrite — deltas only):** `.claude/scoring.md`; `01_framework/governance/governance_v1.md` (Constitutional); `01_framework/bsip2_framework/confidence_framework.md`; `01_framework/governance/evidence_registry_v1.md`.

---

## 0. What this contract is for

Bari is evolving BSIP2 from a single collapsed A–E grade into **six explicit, separable dimensions** while **preserving one decisive consumer grade**. The strategic frame, from the clinician's stress-test, is that Bari is a **glass box**: decisive on the outside (one grade a shopper can act on in seconds), fully inspectable underneath (six dimensions a professional can audit). Same engine, two faces.

This is the **spine every later wave inherits**. It is precise enough that Data and Frontend can build D5 (transparency) and D6 (confidence) against it without re-deriving the philosophy — but it commits no numbers that belong to a governed TASK/BSIP rule. Where a threshold is conceptual, it is marked **(conceptual — needs EV-### + D7 to bind a number).**

The clinician's four structural truths govern throughout (179A §Framing):
1. **Partial visibility is a structural market limit.** Labels disclose only first-level ingredients — no proportions, "protein blend" hides composition, compound ingredients collapse sub-ingredients. Every quality computation is therefore **confidence-gated by disclosure**, never a precise per-product number.
2. **Engineered ≠ bad.** Engineering is a neutral fact. The engine scores what the engineering does to the nutritional/evidence picture, not the presence of a process.
3. **Additives need an EVIDENCE model, not a name-fear model.** "Unfamiliar name = harm" is forbidden. Absent an authoritative verdict, the tier is *disclosure-gap/uncertain* — never a guess.
4. **The engine must not pretend certainty.** Every signal carries a confidence note; undisclosed quality feeds D5 (transparency) and D6 (confidence).

---

## 1. Scoring-Philosophy Reframe

### 1.1 The grade is a within-shelf ranking over observable data — not a health verdict

The headline grade answers exactly one question: **on the data this label discloses, where does this product stand relative to others on its own shelf?** It is a *category-relative ranking over observable composition*, not a statement about health outcomes, dietary suitability, manufacturer intent, or absolute quality. This is continuous with governance_v1 §1 ("ברי מתאר. לא ממליצה") and BEV-001/BEV-003 — the six-dimension move makes the existing boundary *more* legible, not different.

Three things the grade is **not**, restated for the glass-box era:
- **Not a truth claim about the food.** It is a claim about the *disclosed* food. Where disclosure is partial (the normal case), the grade is explicitly confidence-gated (D6), and the gap is surfaced (D5), never silently absorbed.
- **Not a moral verdict on processing or on any molecule.** See §1.2.
- **Not six numbers.** The shopper sees one decisive grade + a confidence flag. The six dimensions live underneath, available on opt-in drilldown and in full on the professional surface (§3). We never surface six numbers to a shopper.

### 1.2 De-moralizing processing (D3)

Today's engine carries `processing_quality` (NOVA classification + additive burden, 15% in proto v0) and a `nova_proxy`. In the glass box, **D3 is reframed as a population-level *probabilistic correlate* of nutritional risk, carrying its own stated uncertainty — not a moral penalty on a process or a molecule.**

Concretely:
- D3 reports *"this formulation pattern is, at the population level, associated with [outcome direction], with [confidence]"* — never *"this is ultra-processed therefore bad."*
- The presence of an emulsifier, a stabilizer, or an industrial process is a **neutral fact**. D3 scores *what the engineering does to the nutritional and evidence picture* (does it co-occur with hyper-palatability patterns, displaced whole-food matrix, contested additives?), not the mere fact of engineering.
- D3's contribution is **bounded** and its uncertainty is **explicit**, so a clean engineered product (e.g. a well-formulated high-protein dairy) is not penalized for being engineered. This is the same instinct already shipped in TASK-169's category-relative whole-food rubric and the saturated-fat-in-dairy-matrix tension (179A §3) — D3 generalizes it.
- **No consumer-facing term "NOVA," "ultra-processed," "structural_class," "cap," or "floor."** (Nutrition Hard Rule 4; governance_v1 §7 framework-invisibility.) D3 surfaces, if at all, as a calm population-level note, not a verdict.

### 1.3 Reconciliation deltas (LISTED — not applied here)

The following will later need updating by their owners, via the governed TASK/BSIP path, each with an evidence-registry entry. **This contract does not edit them.**

**Against `.claude/scoring.md`:**
- D-SCO-1 — The "10 dimensions" table (`processing_quality`, `additive_quality`, etc.) is the *internal* dimension set. It must be reconciled to the **six public-facing dimensions** D1–D6 as a *grouping/relabeling layer* over the existing internals. The ten internal dimensions need not disappear; they roll up into D1–D5, and D6 (confidence) already exists as the confidence ceiling. Document the rollup map when D5/D6 ship.
- D-SCO-2 — Stage 6 step 4 ("Apply confidence ceiling: `CONFIDENCE_INSUFFICIENT_CEILING`, `CONFIDENCE_LOW_CEILING`") is the seed of D6's gate. D6 extends this from *ceiling-only* to *ceiling + demote + withhold (→ null)*. The constants and the "Confidence ceiling" gap row must be updated when D6 binds thresholds.
- D-SCO-3 — `additive_quality` (10%) is today a burden/type penalty. D4 replaces the *philosophy* (burden-count) with an *evidence-tiered, bounded-contribution* model (§2.4). The dimension stays; its internal logic is re-specified under D4 — a future scoring-rule proposal (D6/D7 + EV-###).
- D-SCO-4 — "Frontend Dataset Builder" output schema (`confidence_level: "full"`) must gain the D5 disclosure taxonomy fields and the D6 demote/withhold state (incl. `score: null`) when those ship. No change yet.

**Against `governance_v1.md` (Constitutional — supersedes on conflict):**
- D-GOV-1 — §1 Internal Version lists *four* observable dimensions (grain structure, fiber source, fermentation, label alignment) — bread-era. These are a *category-native instance*, not the universal set. The universal spine is now D1–D6. governance_v1 §5 (Category Independence) already anticipates this; when the four-dimension internal text is revised, frame D1–D6 as the universal layer and the four as bread's native application. **No rewrite here.**
- D-GOV-2 — §4 Uncertainty Ladder (5 levels) and D6 must be explicitly mapped (§2.6 below). They are compatible; the ladder is the *consumer-framing* of D6's gate. The mapping table belongs in a future revision of §4, with D6 as its engine-side counterpart.
- D-GOV-3 — DISTORTION-001 (category-blind fiber penalty) is a D1 concern already logged for BSIP3. D1's category-relative rubric (TASK-169) is the agreed direction; note that D1 must not re-import the fiber distortion when it rolls up.
- D-GOV-4 — The CAN/CANNOT table (§2) gains two new domains when D4/D5 ship: **Additives** (evidence-tier language: "מרכיב טכנולוגי מוכר," "קיים דיון מדעי," never "מסוכן") and **Disclosure** (D5 language: "לא צוין," "לא ניתן לאמת," never "היצרן מסתיר"). These are *additions*, not edits to the existing 58 pairs.

**Against `confidence_framework.md`:**
- D-CONF-1 — This doc IS the D6 substrate. D6 extends it: (a) the Insufficient band (<40) currently *caps at 50*; D6 adds **withhold → null** as a distinct outcome above a (conceptual) hard-floor disclosure threshold — i.e. "not enough to rank at all" routes to `לא נוקד`, not a capped-50 number. (b) D5 disclosure-completeness becomes a *named input* to confidence alongside the existing missing-field and suspicious-pattern reductions. Both are future rule proposals (EV-### + D7).
- D-CONF-2 — Confidence bands (High/Medium/Low/Insufficient) map cleanly to D6 states; the **null/withhold** state is new and must be added to the bands table and to the "product experience" section when D6 ships.

**Against `evidence_registry_v1.md`:**
- D-EV-1 — Every dimension rule that binds a number or a verdict gets an evidence-registry entry before it ships (append-only; BEV/EV discipline). D4 specifically: **no additive carries a score-moving verdict without an EV-### citing an authoritative source** (EFSA/JECFA/Cochrane/IARC/WHO per 179A §2). The six-tier taxonomy itself should be registered as the controlling framework entry when D4 is proposed.

---

## 2. The Six-Dimension Contract

Decisive-grade rule, stated once and binding on all six: **D1–D5 compose into ONE headline grade; D6 gates that grade.** The shopper never sees six numbers. The six dimensions are an *inspection layer*, surfaced only on the professional face and on opt-in consumer drilldown (§3).

### D1 — Nutritional quality
- **Status:** EXISTS (TASK-169 category-relative whole-food rubric).
- **Definition:** Category-relative nutritional standing of the disclosed nutrition panel — protein adequacy, sugar/sodium/sat-fat load against Israeli MoH red-label anchors (sugar 17.5, sat-fat 5.0, sodium 600 g·g·mg/100g), fiber where the category supports it, energy-density *in context* (never "fewer calories = better" — 179A §3). Saturated fat carries the dairy-matrix uncertainty (179A §3; TASK-169) rather than a flat penalty.
- **Inputs:** Disclosed nutrition panel (AVAILABLE — L1/L2 signals). Category from router_v2 (AVAILABLE). DIAAS source-tier signal for protein (NEW wiring — 179A §1 BULK table, confidence-gated, never a per-product DIAAS).
- **Output:** 0–100 sub-score (internal).
- **Contribution to grade:** Largest single contributor; the spine of the ranking.
- **Confidence interaction:** Quantities are HIGH-confidence (disclosed); *quality/form* (protein source, free-vs-total sugar, intrinsic-vs-added fiber) is usually a disclosure-gap → routes to D5/D6 and lowers confidence, never fabricates a value.

### D2 — Ingredient evidence
- **Status:** PARTIAL (Evidence Registry exists).
- **Definition:** Whether the *named, first-level* ingredients carry favorable / neutral / contested evidence as whole-food or formulation choices (distinct from D4, which is additives specifically). E.g. whole-grain vs refined base, named whole-food protein source vs generic "protein blend," genuine fermentation evidence vs theater.
- **Inputs:** BSIP1 ingredient enrichment (AVAILABLE — Hebrew detection, protein-source typing, matrix/fermentation signals). 179A §1 protein-source quality table (NEW BULK reference). Evidence registry (AVAILABLE).
- **Output:** 0–100 sub-score (internal).
- **Contribution to grade:** Moderate; modulates D1 (e.g. a refined base or designed-complement protein blend lowers standing within category).
- **Confidence interaction:** Heavily disclosure-bound — "protein blend (whey, soy, pea)" is the canonical gap (179A §1 row 11/25): report the tier of the best *disclosed* source and lower confidence; never resolve hidden proportions.

### D3 — Processing / formulation signal (DE-MORALIZED)
- **Status:** PARTIAL (`processing_quality` + `nova_proxy` exist; re-framed here).
- **Definition:** A **population-level probabilistic correlate** of nutritional risk arising from formulation pattern, **with explicit stated uncertainty** — NOT a moral penalty on a process or molecule (§1.2). Scores what the engineering *does to the nutritional/evidence picture* (co-occurrence with hyper-palatability patterns, displaced whole-food matrix, reliance on contested additives), not the presence of engineering.
- **Inputs:** NOVA proxy (AVAILABLE, internal-only), hyper-palatability detection (AVAILABLE, Stage 4), matrix-integrity signals (AVAILABLE).
- **Output:** 0–100 sub-score (internal), **bounded contribution** + an attached uncertainty note.
- **Contribution to grade:** Bounded and modest; can nudge but not dominate. A clean engineered product is not penalized for being engineered.
- **Confidence interaction:** D3's own uncertainty is first-class — a low-confidence processing inference contributes less and says so. No consumer-facing "NOVA/ultra-processed/structural_class" term ever (Hard Rule 4).

### D4 — Additive evidence (NEW)
- **Status:** NEW.
- **Definition:** Per-additive **evidence-tiered** assessment on the fixed six-tier taxonomy from 179A §2: `confirmed-negative · likely-neutral · functional · dose-dependent · scientifically-contested · disclosure-gap`. Evidence-first: absent an authoritative verdict, tier = disclosure-gap/uncertain, never a guess.
- **Inputs:** Additive detection in the panel (AVAILABLE — OFF additives taxonomy + Hebrew/E-number regex on the *raw* BSIP0 panel; note real panels live in `02_products\*\...bsip0_raw*.json`, not the curated web JSONs). Curated additive evidence library (NEW BULK — EFSA OpenFoodTox / JECFA / FDA / Cochrane per 179A §2/§4; **bulk-curate, not live per-product calls**). PubChem for identity disambiguation (AVAILABLE/WIRED).
- **Output:** Per-additive tier + a **bounded** aggregate contribution.
- **Contribution to grade — mapped to the 179A data:** The real shelf load is overwhelmingly **functional / likely-neutral** technological aids (E481, E471, E300, E282, E202, lecithin, citric acid, pectin, guar, xanthan). Per 179A's empirical finding, those carry **≈ no penalty** — they are neutral facts. Only the genuinely **scientifically-contested** (carrageenan E407, CMC E466, aspartame E951) and any **confirmed-negative** (industrial trans fat — already an engine veto) carry a **bounded, evidence-cited** signal. Dose-dependent additives (sulphites, NNS sweeteners, phosphates) carry a bounded, dose-aware note. **The taxonomy is asymmetric by design: most additives move nothing.** This keeps D4 consistent with the actual shelf and immune to name-fear.
- **Confidence interaction:** A generic panel term ("מייצב," "צבעי מאכל" with no E-code/name) auto-fires the **disclosure-gap** tier, which feeds D5 and lowers D6 — a transparency signal, not a penalty on a phantom additive.
- **Discipline:** Every tier assignment that moves a score needs an EV-### citing the authoritative source (D-EV-1). Quarterly EFSA-re-eval watch + immediate-trigger on IARC/WHO/JECFA change (179A §5) — an out-of-date verdict is a credibility event.

### D5 — Transparency / disclosure (NEW)
- **Status:** NEW.
- **Definition:** *"We score what you disclose, and we flag what you hide."* A dedicated axis scoring **disclosure completeness** of the label, penalized on its own axis (a true disclosure gap is a finding about the *product*, not just a data problem) **and** feeding D6.
- **Disclosed-vs-hidden taxonomy — what counts as a disclosure gap:**
  - **No proportions / %** for ingredients where it matters (e.g. "protein blend," "<2% almond" undisclosed).
  - **Generic ingredient names** that hide composition: "תערובת חלבונים," "מייצב," "צבעי מאכל," "טעמים" with no specific name/E-code.
  - **Compound ingredients** that collapse sub-ingredients (a named compound with no breakdown).
  - **Undisclosed quality/form** the panel structurally cannot show: protein source quality, free-vs-total sugar, intrinsic-vs-added fiber, fortification bioavailability (179A §3 — all structural market limits).
  - **Missing panel fields** (already counted by confidence_framework) — D5 names *which* are missing, not just that confidence dropped.
- **Inputs:** Logic over the *existing scraped panel* (AVAILABLE — no new library needed; this is why 179A R1 ranks it cheapest/highest-value). BSIP1 enrichment flags (AVAILABLE).
- **Output:** 0–100 disclosure sub-score + a structured gap list (which gaps fired).
- **Contribution to grade:** **OPEN QUESTION (§5, Q2)** — whether non-disclosure may *move* the grade on its own axis or only *annotate* it and act through D6. This is a Product/owner governance call. Default-conservative posture pending the call: D5 feeds D6 (which can demote/withhold) and annotates; a direct grade move is held until co-signed.
- **Confidence interaction:** D5 is a **named input to D6** (D-CONF-1). High disclosure → confidence unconstrained by this axis; severe disclosure gaps → confidence lowered, can trigger demote/withhold.
- **Consumer language:** "לא צוין," "לא ניתן לאמת מהנתונים הזמינים" — never "היצרן מסתיר" (intent attribution; governance_v1 §8 Intent Rule, Anti-Drift Q3).

### D6 — Confidence (PARTIAL → extended)
- **Status:** PARTIAL (confidence_framework.md exists; INSUFFICIENT→null is the extension).
- **Definition:** How much the engine trusts its own inputs — **not** a food-quality measure (confidence_framework, unchanged). D6 is the **gate**: it can demote or withhold the headline grade.
- **Inputs:** Existing confidence reductions (missing fields, suspicious patterns, classification uncertainty — AVAILABLE) **plus** D5 disclosure-completeness as a named input (NEW wiring).
- **Output:** 0–100 confidence + a **gate state**: `unconstrained · demote · withhold(→null)`.
- **How D6 gates the grade (conceptual thresholds — need EV-### + D7 to bind numbers):**
  - **Unconstrained** (High/Medium, ≈≥60): grade reflects the full D1–D5 composite.
  - **Demote / ceiling** (Low, ≈40–59): grade is capped (today: cap 75 = `CONFIDENCE_LOW_CEILING`, raised by the milk recal — the earlier "70" here was stale, corrected 2026-06-04 per TASK-179D; build against live constants) — extend to an explicit *demote* so a low-confidence A cannot stand; the existing cap is the seed.
  - **Withhold → null** (Insufficient, <≈40, *or* a disclosure gap so severe the product cannot be ranked at all): output `לא נוקד` / `score: null` rather than a capped-50 number. This is the **new** behavior vs today's "cap at 50" — the philosophical point is *"below a floor of observability, we decline to rank, we don't guess a middle."* The exact null-vs-cap boundary is **(conceptual — needs EV-### + D7)** and is also surfaced as an open question (§5, Q1: how aggressively D6 demotes).
- **Confidence interaction:** D6 IS the confidence axis; it is the only dimension that can *remove* the grade.

### 2.6 How D1–D5 compose into ONE decisive grade

- D1 is the spine; D2 and D3 modulate it within category; D4 contributes only where contested/confirmed-negative additives fire (asymmetric, bounded); D5 contributes/annotates per the open question (§5, Q2).
- The composite is a single 0–100 → A–E via the existing `GRADE_THRESHOLDS` (S 90+, A 80–89, B 65–79, C 50–64, D 35–49, E 0–34). **No new grade scale.** Frozen invariants depend on this (§4).
- **D6 then gates:** unconstrained passes the composite through; demote caps it; withhold replaces it with null.
- **The shopper sees:** one grade + one confidence flag (+ optional drilldown). **Never six numbers.** (governance_v1 §7 Sophistication Gradient — sophistication increases only as the reader opts in.)

### 2.7 Mapping to the Uncertainty Ladder (governance_v1 §4)

D6's gate states are the *engine-side* of the existing five-level consumer ladder (this mapping belongs in a future §4 revision — D-GOV-2):

| Ladder level (consumer framing) | D6 gate state | Disclosure (D5) |
|---|---|---|
| L1 Full data, clear signal | unconstrained | complete |
| L2 Full data, mixed signals | unconstrained (+ mixed-signal note) | complete, signals conflict |
| L3 Partial data (`ניתוח חלקי`) | demote / ceiling | partial gap |
| L4 Insufficient (`לא נוקד`) | **withhold → null** | severe gap |
| L5 Conflicting sources (`לא נוקד`, hold) | **withhold → null** | conflict |

---

## 3. Two Surfaces — the internal/external seam

**Same engine, two faces.** This is the glass-box principle and it is continuous with governance_v1 §7 (Internal/External Separation, Sophistication Gradient).

- **Consumer surface (external face):** one **decisive grade** (e.g. 72/B) + a **confidence flag** (`ניתוח חלקי` / `לא נוקד` per the ladder) + an **opt-in drilldown**. The drilldown may expose dimension *findings in plain language* ("בסיס קמח לבן," "מרכיב טכנולוגי מוכר," "מקור החלבון לא צוין") — never the six raw numbers, never internal terms (NOVA, structural_class, cap, floor, BSIP). Sophistication increases only as the reader opts in.
- **Professional surface (internal face):** the **full six-dimension graph** — D1–D6 sub-scores, the D4 per-additive tier list with EV citations, the D5 gap list, the D6 gate state and reasons, and the trace. This is the auditable "glass" — fully inspectable, for analysts/clinicians/Bari itself.
- **The seam principle:** the engine computes once; the *face* is a presentation contract over the same trace. The professional graph is the consumer drilldown's source of truth; the consumer face is a lossy, plain-language, decisive projection of it. Nothing the consumer sees is computed differently from what the professional sees — only *shown* differently. Frontend builds two renderers over one view-model, not two engines.

---

## 4. Invariant-Preservation Statement

This contract is doc-only and moves no score. The frozen invariants (CLAUDE.md; CNO ruling 2026-05-30) are preserved by construction, and remain preserved when D4/D5/D6 later ship **behind flags with OFF = byte-identical output**:

- **Milk = `run_004_recalibrated`** (top = 85/A whole/4%/goat). D1–D6 roll up *over the existing internals* and reuse the same `GRADE_THRESHOLDS` (A ≥ 80); the grouping/relabeling (D-SCO-1) is presentational. No milk score moves. When any glass-box rule activates, the milk golden run must be re-verified at 0-diff under the flag (same discipline as `BARI_RECAL_P0`, `BARI_TASK144_FIXES`).
- **Snack-bar ceiling snk-001 = 70/B** (no bar reaches A). D4's additive model is asymmetric/bounded and D6 can only *demote or withhold*, never *promote* — so no bar can be lifted to A by the new dimensions. The ceiling is structurally safe.
- **Bread provenance = `real_bread_retail_003_v1`.** D1–D6 read the same BSIP0 labels (EDPG firewall: engine reads in-house BSIP0 only; external sources calibrate/justify with an EV citation, never substitute a SKU's panel). Provenance and the "best ≠ excellent" framing are untouched.
- **Flag + byte-identical discipline:** every new dimension ships behind an env flag defaulting OFF, with the golden corpus + frozen runs verified 0-diff with the flag OFF, exactly as TASK-169 P0 and TASK-144 did. No silent activation; rollback = unset the flag.

---

## 5. Open Questions for Product Co-Sign

### 5.0 RESOLUTIONS (2026-06-04 — DEC-006; supersedes the conceptual defaults in §D5/§D6 inline notes)
All four calls are now resolved. Product (TASK-179C) co-signed Q1/Q3/Q4 + D-SCO-1; the owner ratified Q2.
- **Q1 — RESOLVED:** conservative-to-demote, **reluctant-to-withhold**. Demote + a visible `ניתוח חלקי` flag carries the normal partial-disclosure case; `לא נוקד` (withhold→null) is reserved for a genuine floor-of-observability failure. *Buy coverage over silence.* Numeric null-vs-cap boundary deferred to Nutrition D7 + EV-###.
- **Q2 — RESOLVED (owner-ratified):** **annotate-only — D5 never moves the headline grade on its own axis.** The grade ranks *disclosed* data; opacity acts solely through D6 (demote + visible flag + named gap) and never as a standalone quality deduction or intent attribution. *Opacity costs standing via confidence, not via a quality penalty.*
- **Q3 — RESOLVED:** contested-additive ceiling is **small, bounded, demote-only** — sub-one-grade-band; the **aggregate** of all contested additives on a product ≤ ~one band; never decisive between two far-apart grades. Trans-fat (confirmed-negative) is a separate tier, unaffected. Per-additive numeric weights deferred to Nutrition D7 + EV-###.
- **Q4 — RESOLVED:** consumer drilldown **exposes plain-language findings on opt-in** (the glass box is the differentiator) but **never the raw six numbers or internal terms**; the full six-dimension graph + EV trace stays on the professional surface.
- **D-SCO-1 — CO-SIGNED:** the 10 internal dimensions **roll up** into the 6 public ones (relabel layer, not a rewrite). Condition: the rollup map is explicitly documented and **0-diff-verified under flag** when D5/D6 ship.

*(The original open-question text is retained below for provenance.)*

These are genuine tradeoff/governance judgment calls, surfaced rather than decided unilaterally. Each needs Product (D7 co-sign) and, where it moves consumer-facing grades, owner sign-off — plus an evidence-registry entry before any rule binds.

**Q1 — How aggressively should D6 demote / withhold a low-confidence grade?**
Where is the null-vs-cap boundary? Today Insufficient caps at 50. The glass-box proposal is to *withhold → null* below a floor of observability rather than show a capped middle number. How much disclosure is "enough to rank at all"? A conservative D6 protects credibility but yields more `לא נוקד` (a real chunk of the shelf — bread saw ~40% unscored); an aggressive-to-rank D6 shows more grades but on thinner data. **Tradeoff: coverage vs. earned certainty.** (Conceptual threshold — must be bound by EV-### + D7.)

**Q2 — May D5 non-disclosure MOVE a grade, or only annotate it (and act via D6)?**
Is a disclosure gap a *product finding* that can lower the headline grade on its own axis, or only a *confidence* signal that demotes via D6 and annotates? This is the difference between "Bari penalizes opacity directly" and "Bari only declines to over-credit the undisclosed." It is a governance posture call about what the grade *means*. Default-conservative pending the call: D5 feeds D6 + annotates; no standalone grade move until co-signed.

**Q3 — How much weight may a single scientifically-contested additive carry?**
E.g. carrageenan (E407) or CMC (E466): EFSA/JECFA judge them safe-at-permitted-levels but live microbiome research is contested (179A §2). How large a bounded signal may "scientifically-contested" carry before it overstates an unsettled science — risking the fear-based register governance_v1 §9 forbids? The asymmetric taxonomy already says *most additives move nothing*; this question bounds the *ceiling* of the contested tier. (Must cite the controlling EV-### per D-EV-1.)

**Q4 (surfaced, lower-order) — Does the consumer drilldown expose dimension findings at all, or only the headline + confidence flag?**
This is partly a Design/Frontend call (D11) but has a content/governance edge (D12/D13): more drilldown = more glass, but more surface for framework leakage. Flagged for the Design/Product seam.

---

## 6. Build-Readiness Note (for Data + Frontend)

- **D5 and D6 are buildable today against this contract** — they reuse the existing scraped panel and the existing confidence machinery; no new BULK library is required (179A R1). D5 = logic over panel completeness + the gap taxonomy in §D5; D6 = extend `confidence_framework` with D5 as an input and add the `demote · withhold(→null)` gate state per §D6 and §2.6, behind a flag, OFF = byte-identical.
- **D4 requires the BULK additive library first** (179A R3 — prototype, one pilot category, instrumented; maadanim or snack-bars are the natural pilots given additive density). Do not build D4 as live per-product API calls; detect in panel → look up in curated library.
- **D1/D2 protein-source signal** needs the §1 DIAAS BULK table (179A R2) — confidence-gated signal, never a per-product DIAAS.
- **No rule ships without an evidence-registry entry** (D-EV-1; bsip2-scoring-governance discipline). No rule deploys that Product has blocked (Hard Rule 8). Every activation is flagged, 0-diff-verified OFF, and reversible.

---

*End of Six-Dimension Contract v1. Doc-only — no engine, scoring, frontend, or governance file was modified. Deltas against existing docs are listed (§1.3), not applied.*
