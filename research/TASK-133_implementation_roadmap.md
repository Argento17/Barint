# TASK-133 — Implementation Roadmap (plan-of-record)

**Objective:** Ship the owner-approved BSIP2 Evidence-Watch 2026-06-01 revisions — **F2** (protein-bar matrix discount), **F1** (emulsifier identity tiering), **F4** (BHA named penalty). **F3 deferred.**
**Origin:** [TASK-132 evaluation](BSIP2_Evidence_Watch_20260601_EVALUATION.md) · approved 2026-06-01.
**Surface:** code sprint in `03_operations/bsip2/proto_v0/`, validated by the existing regression harness. Not a greenfield build — `matrix_integrity.py` (v2) and `constants.py` already exist.
**Calibration sign-off:** see [DEC-004](../decisions/decisions.json).

---

## Critical path

```
133A (taxonomy)  ──►  133B (F2)  ──►  133C (F1) ∥ 133D (F4)  ──►  Phase E (closure)
```

133A is the hard gate. F2 is sequenced first (most value, exercises the taxonomy most). F1 and F4 are thin once 133A lands and run concurrently.

---

## Phase A — Named-additive + ingredient-fragmentation taxonomy (133A)

**Goal:** give the engine ingredient *identity* + *form*, not just class (matrix_integrity_framework Req 1).

- **Code:** new `ingredient_taxonomy.py` (name/synonyms → E-number, additive_class, fragmentation_level, is_named_concern); extend `extracted_additives` / `extracted_matrix_markers` extraction to emit identity, not just presence. `matrix_integrity.py` already has consumption hooks.
- **Must cover:** carrageenan (E407), CMC (E466), soy lecithin (E322), native vs. modified starch, BHA (E320), BHT; fragmentation levels intact / mechanical / fractional / reconstructed.
- **Constraints:** NOVA-independence (Req 2), primary-ingredient weighting (Req 3 — `_pos_weight` exists), gaming resistance (Req 5 — a 5% whole-food garnish cannot claim the halo).
- **DoD:** resolves every additive referenced by B/C/D; extraction unit-tested on golden-product ingredient lists; `run_matrix_validation_v2.py` green.
- **Size:** L (this is the real work).

## Phase B — F2 protein-bar matrix discount + collagen (133B) — highest value

- **Code:** add `collagen` marker; wire `matrix_integrity.py` output into the **Protein Quality dimension** as a discount; collagen sub-penalty; discount curve in `constants.py`.
- **Key design call:** discount the protein-**quality** contribution only (leave protein mass feeding satiety / nutrient density). **Coordinate via the PROCESSING_LOAD family** so it does not double-count with the degradation penalty `matrix_integrity.py` already applies to reconstructed products.
- **Validation:** `batch_run_snack_bars_001.py` + matrix case studies — isolate bar drops; hummus / Greek yogurt / whey-isolate-in-context unchanged (golden suite §"Protein pudding", §"Whey isolate").
- **DoD:** golden qualitative behavior preserved; isolate bar moves in the intended direction; no unintended swings on the dairy_protein corpus.
- **Size:** M.

## Phase C — F1 emulsifier identity tiering (133C)

- **Code:** replace the flat emulsifier penalty with identity-modulated weights in `constants.py` / additive-quality + processing dimensions: carrageenan & CMC up; **soy lecithin down toward neutral** (corrects today's over-penalty); native starch out of additive burden; modified starch unchanged.
- **Constraint:** single RCT (n=60) → modest deltas, **no new caps** (Tension-5 rule budget); note food-grade vs. degraded carrageenan in the rule rationale.
- **Validation:** lecithin products tick up slightly; carrageenan-heavy (dairy-alt, deli) tick down; additive-burden caps (3–4→65, 5+→55) stay stable.
- **Size:** S.

## Phase D — F4 BHA named penalty (133D) — do last, verify first

- **Gate:** WebSearch the current FDA BHA / GRAS-rule outcome before coding (Apr-2026 comment window closed; spring-2026 rule may have landed). Go/no-go on the result.
- **Code:** BHA (E320) small named penalty in additive/processing dimension via the taxonomy; **BHT explicitly excluded**. No regulatory-tracking subsystem.
- **Size:** S.

## Phase E — Closure (objective DoD)

1. **Integrated regression** — full `run_regression_check.py` + real-corpus batch runs (milk, snack bars, cereals, yogurt, bread); golden behavior intact; document deltas.
2. **Version bump** — `0.3.1 → 0.4.0` (new signals + protein-quality behavior change).
3. **Spec sync** — update frozen docs to shipped code: `signal_system.md` (collagen, additive identity, fragmentation level), `processing_analysis.md` (emulsifier tiering), `methodology.md` (Protein Quality now matrix-aware); mark `matrix_integrity_framework.md` Req 1 **implemented**; add a revision-contract note (cf. `score_resolution_contract.md`).
4. **UI language** — entries in `ui_language.md` for each new penalty (Tension-5 explainability).

**TASK-133 closes when A–D are closed and E passes.**

---

## Decision gates needing owner sign-off (DEC-004)

Not derivable from architecture — these need a calibration call:

1. **Calibration magnitudes** — F2 discount curve (47–81% is a band, not a per-product number), F1 penalty deltas, F4 penalty size. `constants.py` states *"calibration is a separate phase."* Recommend deferring numeric magnitudes to a dedicated calibration run against real corpora; build the structure now.
2. **F2 scope** — quality-dimension-only discount (recommended) vs. also discounting protein's satiety / nutrient-density contribution.
3. **Spec reconciliation** — prototype has drifted from frozen spec (code `constants.py`: protein_quality **0.10**, additive **0.10**, processing **0.15**; `methodology.md` says 9% / 7% / 18%). Decide whether proto_v0 is now source-of-truth or the spec is re-synced. Directly affects F2's effective impact (protein weight).

## Top risks

- **F2 double-count** — `matrix_integrity.py` already penalizes reconstructed bars; the new protein-quality discount must coordinate or bars get hit twice. Highest-attention item.
- **F1 lecithin reduction** broadly lifts scores — verify no golden grade jumps (commercial peanut butter must stay below pure nut butter).
- **F2 ↔ deferred F3** — keep F3 deferred; a naive fiber-diversity bonus would partially undo F2 on the same bar class.
