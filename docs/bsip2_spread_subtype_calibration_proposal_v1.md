# BSIP2 Spread Subtype-Aware Calibration Proposal v1

**Task:** TASK-089A
**Owner:** Chief Nutrition Officer
**Assigned agent:** CE (Claude Code — Intelligence & Content)
**Date:** 2026-05-31
**Builds on:** `bsip2_spread_subtype_calibration_assessment_v1.md` (TASK-089)
**Constraint:** Design + quantified impact only. **The engine was not modified.** Impact was measured by re-running the real pipeline under a proposed weight vector (method below).

---

## Executive summary

| Question | Answer |
|----------|--------|
| Should Bari begin consuming `category_subtype` inside BSIP2? | **Yes — scoped to `sauce_spread` first.** |
| Recommendation | **B — Subtype-aware calibration** (one extra weight vector keyed on subtype). Not A, not C. |
| Effect on hummus corpus | **Zero.** 0 of 46 legume items move (avg 57.3 → 57.3). |
| Effect on vegetable corpus | Avg **45.9 → 55.4 (+9.5)**; 12 of 23 items change grade; **8 correctly held at D** by sodium/additive signals. |
| Case study `ממרח פלפלים קלויים` | **42.8/D → 53.7/C** — lands inside the 50–57 expectation band from TASK-089. |

**Headline:** A subtype-aware weight vector fixes the vegetable-spread mis-grade *exactly to the predicted band*, costs the hummus corpus **nothing**, and still lets genuinely worse vegetable spreads (high sodium, heavy additives) stay low. The `category_subtype` field the router already emits is sufficient to drive it.

---

## Method (how the numbers were produced)

Analysis harness: [`analyze_spread_subtype_calibration.py`](../Bari/03_operations/bsip2/proto_v0/src/analyze_spread_subtype_calibration.py) → output `spread_subtype_impact.json`.

- Drives the **real** pipeline unchanged: `extract_signals → classify_category → infer_nova → assign_evaluation_scope → score_product`.
- Corpus: 69 items from `hummus_frontend_v3.json`, carrying nutrition, ingredients, and the already-assigned `_product_type` subtype label.
- **Baseline** = BSIP2-native output under current `DIMENSION_WEIGHTS`.
- **Proposed** = same items re-scored after temporarily rebinding `score_engine.DIMENSION_WEIGHTS` to a subtype-specific vector (restored after each call). The engine's own cap/penalty/floor/ceiling/confidence logic runs identically under both weightings — only the dimension weights differ.

**Faithfulness checks:**
- The case-study SKU reproduces at **42.8/D**, matching the brief's stated 43/D — the reconstruction is true to BSIP2-native behaviour.
- Legume items, scored under the *unchanged* vector, move by exactly **0.0** — confirming the harness isolates the subtype effect.

**Stated limitations (identical under both runs, so deltas are robust):** the corpus lacks `fat_saturated_g` / `fat_trans_g` / `carbohydrates_g` (null → `fat_quality` neutralises to 50, no sat-fat red label possible); ingredient counts come from comma/paren tokenisation; 6 legume items are `insufficient_data` (a data-completeness gap, unrelated to this proposal). These bound the *absolute* baseline, not the *movement*.

---

## Deliverable 1 — Proposed subtype framework

Operate **inside** the existing `sauce_spread` category. Introduce a `spread_family` resolved from the router's `category_subtype` plus a base-ingredient-share rule:

| `spread_family` | Members (router subtype / `_product_type`) | Archetype | Calibration |
|-----------------|--------------------------------------------|-----------|-------------|
| **legume** | `hummus_spread`, `masabacha` | Chickpea/legume base; protein 6–9 g, real fiber | **Current weights (unchanged)** |
| **tahini_rich** | `tahini`, tahini-heavy hummus (tahini ≥ ~25% or `טחינה` anchor) | Sesame-fat base; protein-and-fat dense | **Current weights** (legume-family for calibration; see note) |
| **vegetable** | `matbucha`, `pepper_spread`, `eggplant_spread`, similar cooked-vegetable condiments | Tomato/pepper/eggplant base ≥ ~50%; intrinsically low protein & fiber | **Adjusted vector (Deliverable 3)** |

**Detection rule (the one real implementation risk):** classify `vegetable` by **base-ingredient share + absence of a legume/tahini anchor**, never by topping keywords. Items like `חומוס עם מטבוחה` / `חומוס עם חריף` are legume-primary and must stay `legume`. (In this corpus the `_product_type` labels already encode this; production must derive it from `category_subtype`.)

**Tahini note:** tahini-heavy spreads are *not* a protein problem — sesame carries both protein and fat, so the current protein-centric vector treats them fairly. They are folded into the legume family for calibration. If a future tahini corpus shows a `fat_quality` mismatch, that is a separate calibration question, not part of this proposal.

---

## Deliverable 2 — Dimensions that remain **universal** (identical across all spreads)

These encode hazards/qualities that mean the same thing regardless of base ingredient. They are **unchanged** (and several are *strengthened* for the vegetable vector so the subtype still discriminates internally):

| Dimension | Why universal |
|-----------|---------------|
| **calorie_density** | Energy per 100 g is base-agnostic; the `sauce_spread` table already fits both. |
| **glycemic_quality** | Added sugar in a matbucha is as relevant as in a hummus. Keeps sugary veg spreads honest. |
| **additive_quality** | Preservative/stabilizer/colour load is a real processing signal for any spread. |
| **regulatory_quality** | Israeli red labels (sodium/sugar/sat-fat) are statutory — never subtype-relative. |
| **fat_quality** | Sat-fat/trans/seed-oil chemistry is base-agnostic. |
| **processing_quality** | NOVA is a universal processing axis (slightly up-weighted for veg, not redefined). |

**Evidence they still bite:** of the 8 vegetable items that **stay D** under the proposal, every one is held down by `regulatory_quality=60` (one red label, i.e. sodium > 600 mg), a sodium cap (60), or `additive_quality=10` (5+ additive markers) — **none** by protein. The universal dimensions do exactly their job.

---

## Deliverable 3 — Dimensions that are **subtype-adjusted** (vegetable vector only)

The three protein/fiber-driven dimensions identified in TASK-089 are **down-weighted** for the `vegetable` family and the freed weight is redistributed to the universal dimensions above. Weights still sum to 1.00.

| Dimension | Current | Vegetable | Δ | Rationale |
|-----------|:------:|:---------:|:--:|-----------|
| nutrient_density | 0.15 | **0.10** | −0.05 | 65% protein / 35% fiber blend — penalises a vegetable for lacking legume protein. |
| protein_quality | 0.10 | **0.03** | −0.07 | Scoring a pepper spread on protein grams is a category error. |
| satiety_support | 0.06 | **0.03** | −0.03 | `(protein×3 + fiber×5)/kcal` — structurally low for a low-cal condiment. |
| calorie_density | 0.15 | **0.19** | +0.04 | Where veg spreads genuinely excel; reward it. |
| glycemic_quality | 0.12 | **0.16** | +0.04 | Keep the sugar signal strong (matbucha often lists `סוכר לבן`). |
| additive_quality | 0.10 | **0.13** | +0.03 | Keep processing-load discrimination strong. |
| processing_quality | 0.15 | **0.17** | +0.02 | NOVA remains a major axis. |
| regulatory_quality | 0.05 | **0.07** | +0.02 | Up-weight statutory sodium/sugar signal. |
| fat_quality | 0.08 | 0.08 | 0 | Unchanged. |
| whole_food_integrity | 0.04 | 0.04 | 0 | Unchanged. |
| **Sum** | 1.00 | 1.00 | | |

**Recommended guard (not yet quantified here):** pair the down-weight with a *neutralisation floor* — when the vegetable family has near-zero protein, read `protein_quality` as "not applicable" (~neutral) rather than near-zero, mirroring the engine's existing SRC-04 `fat_quality → 50` pattern. The re-weight alone already achieves the target band; the floor is belt-and-suspenders and can be evaluated in implementation.

---

## Deliverable 4 — Quantified impact

### 4.1 Hummus / legume corpus (n = 46) — **invariant**

| Metric | Baseline | Proposed |
|--------|:--------:|:--------:|
| Avg score | 57.3 | **57.3** |
| Items with any score change | — | **0 / 46** |
| Grade distribution | A 6 · B 1 · C 26 · D 7 · *insufficient 6* | **identical** |

The legume family keeps the current vector, so its scores, grades, and rankings are **bit-for-bit unchanged**. (The 6 `insufficient_data` items are a nutrition-completeness gap, independent of this proposal.)

### 4.2 Vegetable-spread corpus (n = 23)

| Metric | Baseline | Proposed | Δ |
|--------|:--------:|:--------:|:--:|
| Avg score | 45.9 | **55.4** | **+9.5** |
| Grade distribution | C 5 · D 18 | **B 2 · C 13 · D 8** | 12 items up a grade |

Per `_product_type`:

| Subtype | n | Avg base → prop | Δ | Grade base → prop |
|---------|:-:|:---------------:|:--:|-------------------|
| matbucha | 11 | 46.5 → 56.3 | +9.8 | C3 D8 → B1 C6 D4 |
| pepper_spread | 5 | 46.1 → 54.5 | +8.4 | C2 D3 → B1 C2 D2 |
| eggplant_spread | 7 | 44.7 → 54.5 | +9.8 | D7 → C5 D2 |

### 4.3 Score / grade / ranking movement (representative items)

| Item | Base | Proposed | Δ rank (of 69) | NOVA / cap |
|------|:----:|:--------:|:-------------:|-----------|
| **ממרח פלפלים קלויים** (case study) | **42.8 / D** | **53.7 / C** | **+23** | NOVA3 / 82 |
| סלט פלפלים קלויים | 55.1 / C | 67.0 / B | +6 | NOVA3 / 82 |
| סלט חצילים על האש | 49.0 / D | 60.6 / C | +41 | NOVA3 / 82 |
| סלט מטבוחה | 49.3 / D | 60.4 / C | +35 | NOVA3 / 82 |
| מטבוחה חריפה אש | 49.5 / D | 60.5 / C | +34 | NOVA3 / 82 |
| חומוס עם חציל פיקנטי | 48.3 / D | 55.8 / C | +34 | NOVA3 / 82 |

Maximum vegetable rank jump: **+41 places**. Because legumes don't move and vegetables rise, the two families **interleave** in the combined ranking instead of vegetables forming a floor — which is the editorially correct outcome (a clean low-cal pepper spread should sit among, not beneath, the hummus shelf).

### 4.4 The proposal discriminates — it does not blanket-lift

8 of 23 vegetable items **remain D**. Every one is held by a *legitimate* universal signal, not by protein:

| Item | Base → Prop | Held by |
|------|:-----------:|---------|
| מטבוחה פיקנטית | 39.8 → 48.0 | `regulatory=60` (sodium red label) + cap 60 |
| פלפל צ'ומה | 37.0 → 43.3 | `regulatory=60` + cap 60 |
| חציל על האש בטחינה | 37.5 → 45.0 | `additive_quality=10` (5+ markers) |
| מעדן חצילים | 38.6 → 47.9 | NOVA4 / cap 68 |

This is the key safety result: the reweight removes the *unfair* protein penalty while the *fair* penalties (sodium, additives, ultra-processing) still bind.

---

## Deliverable 5 — Recommendation

### **B — Subtype-aware calibration.** And **yes, begin consuming `category_subtype` inside BSIP2**, scoped to `sauce_spread` as the first consumer.

**Why B over A (keep current):** The data shows the D grade is an artifact of a legume prior, not a nutritional fact. Under subtype-aware weights the case study moves to exactly the 50–57 band TASK-089 predicted, with no guardrail hacks. Preserving the current model preserves a known mis-grade.

**Why B over C (separate scoring profile):** The quantified result shows only the three protein/fiber dimensions need to change; calorie, glycemic, additive, regulatory, fat, processing all transfer unchanged and still do real work (they hold 8 items at D). A full second profile would duplicate all of that to fix one axis and double the calibration surface forever. **B is the smallest change that reaches the target**, and its footprint is a single extra weight vector keyed on a field the router already emits.

**Why start consuming `category_subtype` now:**
1. The plumbing exists end-to-end (router emits it; every category infers it) — only the final consumption step in `score_engine` is missing.
2. The first use is **safe and bounded**: legume/tahini keep current behaviour (proven zero-movement), so the blast radius is the vegetable family only.
3. It establishes the pattern — subtype as a *calibration selector*, not a new category — that other shelves (yogurt, cereals, snacks) can reuse without a category explosion.

### Implementation guardrails (for the separately-approved build)
1. Resolve `vegetable` by **base share + legume/tahini-anchor absence**, never topping keywords. This is the only accuracy-critical decision.
2. Change **only** the vegetable weight vector; leave the global vector (and therefore legume/tahini) untouched. Add a **regression gate**: every `legume`/`tahini` item must score identically pre/post.
3. Keep `glycemic_quality`, `additive_quality`, `regulatory_quality`, `fat_quality` at full strength so the vegetable family still discriminates internally.
4. Consider the `protein_quality` neutralisation floor (Deliverable 3) as a follow-up refinement, not a launch blocker.
5. **Register the deviation in the Exception Registry** — two weight vectors in one category is a deliberate, bounded deviation that must be documented before shipping.

---

## Open items for the Chief Nutrition Officer

- **Confirm the editorial value call.** B is correct only if a clean roasted-pepper spread *should* be a C/B everyday condiment. If the framework's position is that all spreads are judged on protein contribution, A is internally consistent (but produces the D the brief flagged).
- **Confirm the canonical baseline.** The BSIP2-native case study is 42.8/D; `hummus_frontend_v3.json` *display* shows analogues higher. Decide whether a frontend/partial-data adjustment is already masking part of this, which changes how much of the +9.5 reaches the consumer.
- **Tahini corpus.** This proposal treats tahini-rich as legume-family on the (sound) basis that sesame carries protein+fat. A dedicated tahini run should confirm no separate `fat_quality` mismatch before that assumption is frozen.

---

*Prepared under the BSIP2 evaluation mandate. No constants, weights, tables, or engine logic were modified; impact was measured by an analysis-time re-run. Implementation requires a separate task and an Exception Registry entry. Reproduce with `analyze_spread_subtype_calibration.py` → `spread_subtype_impact.json`.*
