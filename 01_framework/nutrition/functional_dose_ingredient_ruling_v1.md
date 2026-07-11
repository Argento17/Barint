# Functional-Dose Ingredient Ruling v1

**Type:** Methodology ruling (D6-track, Nutrition-authored)
**Trigger:** TASK-492B gating step — creatine observed appearing in Israeli dairy drinks (Tnuva GO); Bari's engine has no bucket for it
**Status:** Ruling issued. Not yet a scoring rule — no EV-### exists, nothing is D7'd, nothing ships. This document is the prerequisite gate for the high-protein-dairy shelf scrape and blog, not the scrape itself.
**Scores affected today:** None. **Copy affected today:** None.
**Author:** Nutrition Agent
**Date:** 2026-07-03

---

## 0. Constraints observed

- No product data invented. Tnuva GO's actual creatine dose is unknown pending scrape; every number below is a worked *example*, not an asserted fact about any SKU.
- Open Food Facts not used or referenced.
- No consumer copy drafted here. No score changed. No engine code touched.

---

## 1. Which bucket does a functional-dose ingredient belong in?

**Ruling: (c) — a new bucket. Neither nutrient nor additive.**

Bari's two existing lanes are both wrong fits, and forcing creatine into either produces a false reading:

- **As a nutrient (spine)** — the scored spine (protein/fat/sugar/sodium/fiber/energy) measures *what the food is made of*, and BSIP2's governing question (BEV-008) is structural: does the composition match what the product presents itself as. Creatine is not a macronutrient and contributes no meaningful energy, protein, or structural mass. Folding it into "protein quality" or a density dimension would misrepresent what's being measured — it's not food matrix, it's an added physiological agent riding on a food matrix. This is the same category error the SIE methodology names explicitly for supplements ("scoring energy density... of a creatine tub is a category error") — except here it's inverted: the category error would be scoring a physiological agent *as if it were* food matrix.
- **As an additive (E4/D4 ladder)** — the additive ladder (EV-003/EV-019, emulsifier tiers; D4 Glass Box) exists to grade *processing-function* ingredients: things added to bind, emulsify, preserve, or texturize, evaluated on a harm-risk gradient (synthetic/high-risk → neutral → prebiotic-beneficial). Creatine is added for neither processing function nor structural integrity — it's added to *do something to the body*, which is precisely the additive ladder's exclusion criterion. It's also not a safety-harm case (creatine monohydrate has one of the cleanest safety profiles of any studied ergogenic compound — no ADI, no EFSA caution flag, decades of RCT data), so slotting it onto a penalty ladder built for E-number risk-tiering would be scientifically dishonest in the other direction: it would imply harm that isn't there.

**What it actually is:** a third category BSIP2 has never needed before — a **functional dose**: an ingredient added at a specific, evidence-anchored amount to produce a physiological effect unrelated to nutrition or food processing. This is structurally the *same object* the Supplement Intelligence Engine (SIE) was built to evaluate — `(active, dose, form, evidence)` — just showing up inside a food matrix instead of a capsule. The right mental model is not "a new food signal" but "a supplement claim embedded in a grocery product," and Bari already owns a framework for exactly that (`01_framework/supplement_framework/methodology_v1.md`).

---

## 2. Verdict on the annotation-only lane (challenging the prior)

**Confirmed — with one refinement on mechanism, not on conclusion.**

The instinct is right for the reason given (EFSA/radar precedent: engine findings that don't move a label-derivable score stay editorial; an engine finding never becomes a program) but the deeper reason is structural, not just precedential:

1. **BSIP2's spine is a food-structure instrument.** Its ten dimensions decompose "is this still food, and is it well-built." A functional dose is not a food-structure question — it's an efficacy/honesty question, which is what the *five SIE dimensions* (Evidence, Dose, Form, Honesty, Safety) were purpose-built to answer. Bolting a sixth food-structure dimension onto BSIP2 to handle one ingredient would violate the "don't accrete rules" instruction (skill `bari-bsip2-scoring-governance`) for a case that already has a home elsewhere.
2. **Refinement — it's not just "annotation," it's a borrowed-lens annotation.** Don't invent new annotation logic from scratch. The check should explicitly **run the SIE's Dose Adequacy sub-logic (§2.2)** against the on-label creatine content, using creatine's already-partially-specified dossier facts (effective dose ~3–5 g/day, no established UL, clean safety profile — SIE §2.5 already names creatine as the Safety **PASS control** anchor). The output is a dossier-grounded verdict — "meaningful dose" / "decorative dose" / "unknown, no per-serving disclosure" — that appears as a **radar-style annotation on the food page**, never as a BSIP2 sub-score, cap, or floor. This reuses machinery instead of inventing a fourth framework, and it means the annotation is evidence-anchored rather than an ad hoc editorial judgment call.
3. **Precedent chain this sits on:**
   - `efsa_no_scoring_exposure` — evidence-tier facts about a substance can inform editorial/radar content with zero engine exposure.
   - BEV-028 (fortification) — Bari already has a ruling for "an added beneficial substance that does not change food-structure quality": no structural credit, UI transparency instead of architecture change. Creatine is fortification's harder cousin (dose-dependent efficacy claim, not a flat public-health micronutrient), but the *disposition* — annotate, don't structurally credit — is the same shape.
   - `owner_systematic_not_artisanal` — an engine finding never becomes a program on its own; this ruling stops at "annotation lane exists," it does not launch a "functional dairy" initiative.

**So: confirmed as annotation-only, refined to specify the annotation is SIE-Dose-Adequacy-derived, not freehand.**

---

## 3. Dose-honesty check — threshold logic and scrape data contract

This directly reuses the SIE §2.2 Dose Adequacy machinery and the magnesium elemental-fraction precedent (`magnesium_model_offline_revision`), adapted for a food-matrix context rather than a capsule.

### 3.1 What the scrape must capture (hard requirement before any annotation can run)

| Field | Why it's required |
|---|---|
| `creatine_mg_per_serving` | The label-stated amount per stated serving. If absent, the check cannot run — **missing-data discard rule applies** (`missing_data_discard_rule`): no creatine annotation is shown, not "assumed low," not "assumed adequate." |
| `serving_size_g_or_ml` | Needed to normalize to per-100g/per-100ml for cross-product comparability, and to compute realistic daily intake. |
| `servings_per_container` / recommended servings per day if stated | Needed to compute a **daily dose**, not just a per-serving dose — SIE §2.2 explicitly normalizes to daily basis before comparing to `effective_dose_range`. |
| `creatine form` (monohydrate vs HCl vs buffered, if disclosed) | Monohydrate is the studied `preferred` form (SIE §2.3 form ladder); an unusual form on a dairy product is itself worth capturing even though it doesn't move a score. |
| Whether creatine appears in a named/quantified line vs. buried in a "functional blend" | If it's a blend with no per-active split, this is the SIE §2.4 fairy-dust/hidden-dose signal — the annotation must say "undisclosed," not attempt a dose verdict. |

If any of the first three fields is missing, the check **does not run** and the product shows no creatine dose-honesty annotation at all — silence, not a downgraded or hedged claim. This is the same discipline as "unknown is acceptable; OFF is not," extended to dose math.

### 3.2 Threshold logic (dossier comparison, not a new number Bari invents)

Reuse SIE §2.2's existing band structure directly, with creatine's known effective-dose literature (creatine monohydrate, ergogenic/strength claim: `min_effective` ≈ 3 g/day, `typical` ≈ 5 g/day, `upper_studied` ≈ 5 g/day per the SIE's own worked dossier example in §5 of `methodology_v1.md`):

| Computed daily dose | Annotation verdict (editorial only) |
|---|---|
| ≥ 3 g/day | "Meaningful dose" — in or above the range studied for the effect creatine is known for |
| 1.5–3 g/day | "Partial dose" — present but below the studied effective range (graded, per SIE's sub-therapeutic band) |
| < 1.5 g/day (SIE's `0.5 × min_effective` fairy-dust line) | "Decorative amount" — present on the label, not present at a physiologically meaningful level |
| Undisclosed / blended | "Amount not disclosed" — no verdict rendered, flagged as a transparency gap |

This is arithmetic against an already-accepted external literature-derived number (the SIE dossier's `min_effective`), not a new Bari-invented threshold — it inherits the SIE's own D6/D7-track dossier rather than creating a parallel one. **Important scope note:** this dossier value is *pending Phase-2 calibration* in the SIE itself (methodology_v1.md marks all SIE numbers "calibration-pending"). Using it for a food-page annotation is lower-stakes than using it for a supplement grade (no grade is at risk here), but the annotation copy must still hedge it as literature-derived, not Bari-certified-precise, consistent with Hard Rule 6.

### 3.3 What this check explicitly does NOT do

- It does not compute or display an "absorbed" or "effective" adjusted number — mirrors the magnesium v1-bug lesson (`magnesium_model_offline_revision`): display the observed label dose and the class verdict, never a derived/adjusted figure presented as fact.
- It does not touch BSIP2's confidence ceiling, additive_quality dimension, or any existing cap/floor.
- It does not imply a recommendation to consume creatine or that the product is "better" for containing it (SIE Invariant 1, No-Necessity Rule, applies here by inheritance even though this isn't a supplement page).

---

## 4. Scope and guardrails — how far does this generalize

**Ruling: the bucket generalizes; the specific dossier work does not (yet). Draw the line at "does the ingredient carry a dose-dependent efficacy claim independent of nutrition."**

### 4.1 The generalizable test (three questions, all must be true to enter the functional-dose lane)

1. **Is it added for a physiological effect, not nutrition or processing?** (Excludes ordinary fortification/enrichment — iron in flour, vitamin D in milk — which BEV-028 already handles as "no structural credit, no annotation needed" because those are public-health-dose, not performance-dose, additions with no serving-dependent efficacy claim being made to the consumer.)
2. **Does published literature define an effective dose range distinct from an RDI/nutritional-adequacy number?** (Creatine: yes, ergogenic dose ≠ any RDI, because there isn't one — creatine isn't an essential nutrient with a dietary reference intake. Added whey protein isolate: mostly no — protein has an RDI-anchored adequacy logic already inside BSIP2's nutrient spine; an added protein isolate is graded as protein content today, which is the correct existing lane, not a new one.)
3. **Is the ingredient's presence itself the marketing claim** (front-of-pack "with creatine," "with collagen") **rather than an incidental formulation choice?** (If yes, honesty-gap logic — same shape as SIE §2.4 claim-vs-substance gap — becomes relevant to whether the annotation should also flag under-dosing as a labeling-honesty note, still non-scoring.)

### 4.2 Applying the test to the named candidates

| Ingredient | Physiological (not nutritive) dose claim? | Distinct effective-dose literature? | Verdict |
|---|---|---|---|
| **Creatine** | Yes | Yes (3–5 g/day, ergogenic) | **Functional-dose lane.** This ruling applies directly. |
| **Collagen (added, e.g. "with collagen" dairy/beverage)** | Yes (skin/joint claims) | Contested/heterogeneous (evidence tier is Weak-to-Moderate depending on peptide type and claim — a Research Agent literature pull would be needed before any dossier exists) | **Functional-dose lane, but no dossier yet.** Same bucket, blocked on evidence review — do not annotate collagen doses until Research produces an evidence-tier verdict; this is a new KB/dossier task, not an extension of the creatine ruling. |
| **Added protein isolates (whey/pea isolate added to boost a label number)** | No — protein's role is nutritive; BSIP2 already scores protein quantity and BEV-032 already handles the *source/matrix* distinction (isolate vs. intact-food protein) as a structural signal | N/A — no separate "effective dose" independent of ordinary protein adequacy | **Stays in the nutrient spine.** Not a functional dose. No new lane needed. |
| **Vitamins/minerals at supplement-level potency in a food (e.g. a drink dosed to 100%+ RDI of B12, or megadose vitamin C)** | Borderline — nutritive in kind, but the *dose* has crossed from "nutrition" into "supplement-equivalent potency" | Yes, RDI/UL literature exists | **Enters the functional-dose lane only past a potency threshold**, not by ingredient identity. This is the closest case to the "functional food vs. supplement" boundary question (4.3) — flag for a future dedicated ruling rather than deciding here, since it requires a potency-threshold definition Bari hasn't set (e.g. "≥50% NRV in one serving") and touches EFSA fortification-ceiling rules Research should review first. |

### 4.3 Where's the functional-food/supplement boundary, and does it change scoring?

The boundary is **regulatory-form, not effect**: a supplement is sold as a discrete dose (capsule/powder/serving with a stated daily-intake instruction and no food-matrix pretense); a functional food is sold and eaten as food, with the physiological agent riding along. Bari's answer does **not** change based on which side of that line a product sits:

- A capsule of creatine → **SIE scores it** (it *is* the SIE's object of analysis — dose is the product).
- A dairy drink with creatine added → **BSIP2 scores the food structure; the SIE's Dose Adequacy logic is borrowed read-only to produce a non-scoring annotation.** The food is still scored as a food. The functional dose rides alongside, annotated, never blended into the food grade.

This is a clean, defensible line because it matches how a consumer actually encounters the product (drinking a beverage vs. taking a supplement) and it requires no new architecture — it's "which existing engine reads the label," not "invent a new scoring model." It generalizes to collagen, functional-potency vitamins, and any future functional-dairy/functional-snack trend without further architectural work — each new ingredient needs its own SIE-style dossier (Research + Nutrition evidence-tier work) before its annotation can run, but the *lane* itself doesn't need to be re-ruled each time.

---

## 5. Scoring-spine safety confirmation

- **No published score moves.** This ruling creates no EV-### entry, touches no `constants.py` value, and defines no cap/floor/veto. It is annotation-lane-only by design (§2), and annotation lanes have zero engine-score exposure by the same logic as `efsa_no_scoring_exposure`.
- **No new hard chain added to BSIP2.** The de-chaining directive (`engine_freedom_dechain_directive`, TASK-395) is about removing rigid caps/binary rules from the *scoring* engine. This ruling explicitly keeps the functional-dose check **outside** the scoring engine — it borrows the SIE's dose-comparison logic read-only, and the SIE is architecturally already a **sibling engine**, not a BSIP2 extension (methodology_v1.md §0: "shared acquisition plumbing, forked scoring brain... food invariants structurally untouchable"). Nothing here adds a rule, cap, or dimension to BSIP2's ten dimensions or seventeen hard caps (BEV-052).
- **Risk flag, honestly stated:** the one way this *could* accrete risk is if a future implementer takes the shortcut of adding a "functional dose penalty/bonus" directly into BSIP2's additive_quality or nutrient_density dimension instead of building the annotation as a separate read-only surface. That would be both a scoring-spine violation (new hard chain) and a category error (§1). This ruling explicitly forecloses that path — any implementation proposal that touches `score_engine.py`, `constants.py`, or any BSIP2 dimension weight for a functional-dose ingredient must come back through D6/D7 as a new scoring rule, not ride in under this ruling's authority. This ruling authorizes **annotation infrastructure only.**
- **Owner-strategic-tripwire check (per `decision_authority_matrix_v1.md`):** none of the five tripwires fire. This does not touch a frozen invariant or published score (tripwire 1), it is reversible (annotation copy, not irreversible consumer-facing commitment — tripwire 2), it does not start a major program by itself (tripwire 3 — a "functional dairy" *category program* would need a separate go/no-go from Product, this ruling only unblocks the gating step), it creates no spend/legal exposure (tripwire 4), and it does not redefine what Bari is (tripwire 5) — it extends Bari's existing "describe, don't recommend" posture to a new ingredient class using an engine Bari already owns. Decided and documented per the autonomy mandate; no owner escalation needed for this ruling itself. (A future go-live of a "functional dairy" shelf/category would separately need Product's D10 sign-off, per the standing process — not gated by this document.)

---

## 6. What this unblocks and what it does not

**Unblocked by this ruling:**
- The high-protein-dairy shelf scrape may proceed, provided BSIP0 captures the fields in §3.1 for any product declaring creatine (or a similar functional-dose ingredient) on-label.
- A future D5 enrichment-config review (Nutrition-approved) may add `creatine_mg_per_serving` / `functional_dose_ingredient` as BSIP1 extraction fields for the dairy-protein category, since this ruling defines what they'd be used for.

**NOT unblocked by this ruling:**
- No blog or consumer copy about creatine-in-dairy may ship from this document alone — that requires Content Agent authorship + the mandatory two-gate sign-off (Content + Adversarial QA/Red-Team), per the standing hard rule. This ruling supplies the *methodology* the copy must stay inside of, not the copy itself.
- No dossier exists yet for collagen or any other functional-dose ingredient beyond creatine — those need their own Research Agent evidence pull before §4.2's "functional-dose lane" verdict can produce a runnable annotation.
- No EV-### / D7 process has been run because nothing here is a scoring rule. If a future proposal wants this to influence a score (not just an annotation), it must return through D6/D7 as a net-new rule, co-signed by Product, exactly like any other scoring change.

---

## Return Contract

```json
{
  "task": "TASK-492B",
  "deliverable": "functional_dose_ingredient_ruling_v1",
  "status_proposed": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\01_framework\\nutrition\\functional_dose_ingredient_ruling_v1.md",
      "sha256": "19a2d63953eecee62b73f27c977a7edd1f4cca5d4eaedc15000d1fb937498459"
    }
  ],
  "counts": {
    "rulings_issued": {"value": 5, "denominator": "5 questions posed in the task spec (bucket / prior-challenge / dose-check / scope / spine-safety)"},
    "scores_changed": {"value": 0, "denominator": "0 published scores"},
    "engine_files_touched": {"value": 0, "denominator": "0 files in 03_operations/bsip2 or 03_operations/supplement_engine"},
    "ev_registry_entries_created": {"value": 0, "denominator": "0 — this is a methodology ruling, not a scoring rule; no EV-### opened"},
    "new_hard_caps_or_chains_added": {"value": 0, "denominator": "0 — explicitly foreclosed in Section 5"}
  },
  "commands_run": [],
  "not_done": [
    "No BSIP1 enrichment config change made — that is a separate D5 action for whoever owns the dairy-protein shelf scrape, referencing Section 3.1's field list",
    "No dossier built for creatine (or any ingredient) in the SIE evidence_dossiers/ tree — this ruling reuses the SIE's ALREADY-EXISTING worked example (min_effective 3g/typical 5g from methodology_v1.md §5) rather than authoring a new formal dossier; a formal creatine dossier entry is recommended but not required to unblock the scrape",
    "No Research Agent evidence pull performed for collagen or other candidate functional-dose ingredients (Section 4.2 explicitly defers these)",
    "No consumer copy drafted (out of scope per task constraints)",
    "No Product Agent co-sign sought — not required because this is not a D6/D7 scoring-rule proposal; flagged in Section 5 that any FUTURE proposal to move a score would require it"
  ],
  "acceptance_test": {
    "spec_requirement": "Ruling on bucket/prior/dose-check/scope/spine-safety, written to 01_framework/nutrition/functional_dose_ingredient_ruling_v1.md, no score changed, no consumer copy written, no OFF used, no invented product data, no subagents spawned",
    "result": "PASS",
    "evidence": "File written at specified path covering all 5 questions; Section 5 explicitly confirms zero score/engine changes; no Tnuva GO numbers asserted (Section 0 and throughout, all creatine dose figures are cited from the pre-existing SIE dossier example, not asserted as this product's actual content); OFF not referenced anywhere; work performed inline by Nutrition Agent, no Agent/Task tool calls made"
  }
}
```
