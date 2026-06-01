# Bari System Guardrails
**Status:** Active  
**Last updated:** 2026-05-20  
**Audience:** Engineers, AI coding assistants (Claude Code, Cursor), future contributors

This document is the constitutional constraint layer for the Bari pipeline. When in doubt about a design decision, check here first.

---

## 1. Layer Boundaries

Each BSIP layer has a single, bounded responsibility. Do not bleed logic across layers.

| Layer | Responsibility | Input | Output |
|-------|---------------|-------|--------|
| **BSIP0** | Raw observation capture — scraping, OCR, parsing | Retailer pages, physical labels | Raw product JSON (unstructured) |
| **BSIP1** | Canonicalization + semantic observability — ingredient parsing, additive detection, nutritional normalization, enrichment | Raw BSIP0 JSON | Canonical enriched product record (structured, stable) |
| **BSIP2** | Structural interpretation — scoring, matrix integrity, NOVA proxy, signal extraction | BSIP1 canonical record | Scored trace JSON (scores, signals, provenance) |
| **UI** | Explanation and comparison only — grades, labels, comparison pages | BSIP2 trace JSON | Human-readable output (Hebrew-primary) |

**The pipeline is one-directional.** Data flows BSIP0 → BSIP1 → BSIP2 → UI. No layer reads from a later layer.

---

## 2. What Is Forbidden in Each Layer

### BSIP0 — must NOT
- Parse ingredients beyond raw text extraction
- Assign any structured meaning to what it scrapes
- Make any decisions about product quality or composition

### BSIP1 — must NOT
- Assign scores of any kind (no numeric quality judgement)
- Make health claims or recommendations
- Infer processing level (that is BSIP2's job)
- Discard information: if something is on the label and parseable, it belongs in the record
- Contain retailer-specific logic (it is the cross-retailer canonical layer)

### BSIP2 — must NOT
- Contain consumer-facing language (no "this product is bad for you")
- Make brand-dependent decisions (score must be identical for identical formulations regardless of brand)
- Use ML embeddings or learned weights until ontology is fully stabilized
- Hard-code category exceptions (all logic must generalize across categories)
- Access the raw BSIP0 data — only BSIP1 canonical records

### UI — must NOT
- Compute or transform scores (consume BSIP2 trace as-is)
- Add interpretation logic that belongs in the engine
- Make clinical or medical claims
- Present grades without the supporting signal context

---

## 3. Source-of-Truth Files

When multiple files appear to cover the same thing, these are the canonical versions. Archive everything else.

### Active Schemas
- BSIP1 canonical record: `01_framework/bsip2_framework/` (field definitions)
- BSIP2 trace schema: defined by `trace_writer.py` output structure

### Active BSIP1 Enrichment
- Engine: `03_operations/bsip1/core/ingredient_enricher.py`
- Runner: `03_operations/bsip1/core/enrich_runner.py`
- Test suite: `03_operations/bsip1/core/test_enricher.py` (64 checks, run with pytest)

### Active BSIP2 Scoring
- Main scorer: `03_operations/bsip2/proto_v0/src/score_engine.py`
- Signal extraction: `03_operations/bsip2/proto_v0/src/signal_extractor.py`
- NOVA proxy: `03_operations/bsip2/proto_v0/src/nova_proxy.py`
- Constants + thresholds: `03_operations/bsip2/proto_v0/src/constants.py`
- Evaluation scope: `03_operations/bsip2/proto_v0/src/evaluation_scope.py`

### Active Matrix Integrity Engine
- **v2 (current):** `03_operations/bsip2/proto_v0/src/matrix_integrity.py`
- v1 (archive, read-only): `99_archive/legacy_bsip2/matrix_integrity_v1.py`

### Active Batch Runners
- `batch_run_snack_bars_001.py`, `batch_run_cereals_001.py`, `batch_run_yogurt_001.py`, `batch_run_milk_004.py`
- All in `03_operations/bsip2/proto_v0/src/`

### Active Validation Runners
- Matrix integrity comparison: `run_matrix_validation_v2.py`
- Milk run reports: `generate_run_004_reports.py`
- Visuals: `generate_visuals.py`

### Latest Reports
- Matrix integrity validation: `03_operations/reports/matrix_integrity/matrix_integrity_validation_001.md`
- Matrix integrity calibration (v1 vs v2): `03_operations/reports/matrix_integrity/matrix_integrity_calibration_v2.md`
- Enrichment coverage: `03_operations/reports/enrichment/enrichment_validation_001.md`

### UI Language Rules
- `01_framework/bsip2_framework/ui_language.md` — Hebrew grade labels, tone rules, dimension names

---

## 4. Change Discipline

Every change to engine code (BSIP1 or BSIP2) must be accompanied by the following before merging:

| Requirement | What it means |
|-------------|--------------|
| **Reason for change** | Why this change is needed — problem being solved, not just what changed |
| **Affected logic** | Which functions, signals, or score dimensions are touched |
| **Regression run** | Re-run all active batch runners; compare output traces to prior run |
| **Report output** | A validation or calibration report must be generated and committed alongside the code change |
| **Known risks** | Any cases where the change may produce unexpected results; edge cases to watch |

Changes to `constants.py` (thresholds, grade bounds) require extra scrutiny — they affect every product across all categories simultaneously.

Changes to `matrix_integrity.py` require a v1 vs vN comparison report via `run_matrix_validation_v2.py`.

Do not ship a scoring change without a report.

---

## 5. Regression Baseline (Future)

Bari does not yet have a formal regression test corpus. This section defines what it must contain when built.

### What the golden corpus must include
- **Fixed representative products** — one clear exemplar per archetype (whole milk, oat drink, granola bar, plain yogurt, flavored yogurt, etc.)
- **Expected archetypes** — the category and transformation type each product should be classified as
- **Expected score bands** — not exact scores, but acceptable ranges (e.g., plain whole milk: 90–100, granola bar with isolates: 55–72)
- **Edge cases** — products that stress the ontology: fortified-but-clean cereals, fermented-but-processed yogurts, flavored-but-minimal milks
- **Regression alerts** — any run that shifts a baseline product's score by more than ±5 points must be flagged and explained before the run is accepted

### Where it lives (when built)
- Golden products: `01_framework/bsip2_framework/validation/golden_corpus/`
- Expected outputs: alongside golden products as `expected_bsip2_trace.json`
- Regression runner: `03_operations/reports/regression/` (reserved, currently empty)

Until the corpus exists, batch run comparisons (old vs new) are the de facto regression check.

---

## 6. Ontology Principles

These are the epistemic rules that govern how Bari interprets food. Violating them produces outputs that feel sophisticated but are wrong.

**Observable evidence first.**  
Scores derive from what is actually in the ingredient list and label. No inference beyond what the text supports. If it cannot be observed, it cannot be scored.

**No brand influence.**  
The score for a product is determined by its formulation. Two products with identical ingredient lists must receive identical scores regardless of brand, price, or retailer.

**Carbohydrates are not inherently bad.**  
Oats, whole grains, legumes, fruit — these carry carbohydrates as part of intact food structure. Penalizing carbs as such would misclassify most traditional foods. Context and source matter.

**Protein is not inherently good.**  
Isolated whey, hydrolyzed proteins, and protein powders added to reconstruct engineered products are engineering signals, not quality signals. Protein content ≠ product quality.

**Processing is not automatically bad.**  
Yogurt is fermented. Cheese is aged. Tahini is ground. Traditional transformation is not the same as industrial restructuring. The matrix integrity engine distinguishes transformation types for this reason.

**Structure and context matter more than ingredient lists alone.**  
A long ingredient list is not automatically worse than a short one. What matters is the structural relationship between ingredients: is the food assembled from intact components, or reconstructed from isolates?

**Ingredient order matters.**  
Position in the ingredient list is a structural signal. Sugar at position 2 means something different than sugar at position 12. The engine weights position explicitly.

**Do not confuse flavor with category.**  
"Vanilla yogurt" is still yogurt. "Chocolate oat drink" is still an oat drink. Flavor additions are HP signals; they do not change the base product archetype classification.

---

## Enforcement

These guardrails are not aspirational. They are the current working constraints.

When an AI assistant (Claude Code, Cursor) proposes a change that violates a guardrail, reject the proposal and reference this document. When a human engineer is tempted to take a shortcut that violates a guardrail, the question to ask is: *will this still be correct in six months, across a new category, without remembering why we did it?*

If the answer is no, the shortcut is not a shortcut.
