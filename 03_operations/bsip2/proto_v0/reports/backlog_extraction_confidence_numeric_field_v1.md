# BACKLOG — Numeric extraction-confidence field for State 6 (OCR/parse confidence)

**Status:** BACKLOG ONLY — not scheduled. No scoring change, no pipeline change, no threshold move.
**Owner (if scheduled):** Data Agent / BSIP0 emission layer.
**Raised by:** Nutrition Agent State-7 threshold report, §1(d) and §6 item 2
(`03_operations/bsip2/proto_v0/reports/state7_suppression_threshold_policy_v1.md`).
**Relates to:** confidence-indicator spec State 6 "low-confidence extraction"
(`01_framework/frontend/score_confidence_indicators_spec_v1.md`).
**Date logged:** 2026-06-10.

---

## Why this exists (the gap)

The confidence-indicator spec defines State 6 = "low-confidence extraction." The
Nutrition Agent's threshold report wired State 6 to fire on **categorical proxies that
already exist in the live pipeline**, because there is **no numeric OCR / extraction-
confidence float emitted anywhere in the in-house pipeline.** v1 State 6 fires on:

```
extract_low  =  ingredient_text_quality in {corrupted, malformed, marketing_bleed}
                OR nova_confidence_band == "low"
```

This is the honest v1 behavior and it stays. This note records what a *true numeric
band* would require, so the gap is documented and not silently re-invented later.

## 1. The required future field

| Property | Value |
|---|---|
| Proposed name | `extraction_confidence` (reuse the name already squatting as a string passthrough; promote it to a measured float) |
| Type | `float ∈ [0.0, 1.0]` (1.0 = clean structured parse; lower = degraded OCR/parse) |
| Location in trace | BSIP0 panel/ingredient extraction output, carried forward into the BSIP1 product and surfaced in the BSIP2 trace **L1** block alongside the existing `ingredient_text_quality` categorical (so the categorical proxy and the numeric measure sit side by side and the proxy remains the fallback) |
| Provenance | per EDPG, any externally-sourced (OFF/scrape) panel must carry the numeric value inside its `provenance`/`verification_status` envelope; the value stays a candidate until a BSIP0/QA pass promotes it |

It must be a **measured** value (from the parse/OCR step), not a hand-set default —
the current `extraction_confidence` is exactly the placeholder to avoid.

## 2. Likely source (grounded in the code, not guessed)

The signal would originate in the **BSIP0 ingredient/panel extraction (OCR/parse)
stage**, not in BSIP2. Verified against the live code:

- **`03_operations/bsip2/proto_v0/src/signal_extractor.py`** is purely downstream —
  it consumes `product.get("ingredient_text_quality")` (L1 build, ~line 588 region)
  and runs the categorical OCR/disclaimer-bleed sanitizer (`sanitize_ingredient_list`,
  TASK-144 Fix1/EV-026). It emits `ingredient_sanitization{raw_count, clean_count,
  dropped, truncated}` — a count delta, **not a parse-confidence score.** It never
  computes a numeric extraction confidence and is the wrong layer to add one.
- **`nova_confidence_band`** (`nova_proxy.py`) is a *categorical* band
  (`high | medium | low`) derived from evidence quality, e.g.
  `"medium" if not _ingredient_data_degraded else "low"` — it is a NOVA-inference
  confidence, not an OCR/parse score, and is already the proxy v1 leans on.
- **`extraction_confidence`** today exists only as a **string passthrough** in the
  bread loaders, e.g. `batch_run_bread_retail_003.py:163`
  `"extraction_confidence": raw.get("extraction_confidence") or "medium"` — it defaults
  to the literal `"medium"`; nothing measures it.
- **`03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`** is the actual panel
  parser (the `div.nutritionList` classifier, EV-026/EV-046 family). This shared parse
  layer is where a real per-product extraction-confidence float would naturally be
  produced — it already knows which rows classified cleanly vs. fell through, which is
  the raw material for a parse-quality score. Ingredient-side OCR confidence would
  originate at the same scrape/parse boundary that feeds `ingredient_text_quality`.

So the "likely source" is the **BSIP0 scrape/parse layer** (`_shared/bsip0_nutrition.py`
for the panel; the ingredient-text capture step that sets `ingredient_text_quality`),
which would emit the float to be carried through BSIP1 into the BSIP2 trace.

## 3. Downstream use

- Feeds confidence-spec **State 6** / the partial-vs-suppress line in the State-7
  threshold rule (`state7_suppression_threshold_policy_v1.md` §1, rule R6). A numeric
  band could refine R6 from "categorical proxy fired" to "extraction_confidence below a
  measured cutoff."
- **Governance gate:** any threshold that uses this float to **move the suppress
  (`טרם נוקד`) vs. caveat (`partial`) line** touches displayed-score visibility →
  requires an **evidence-registry entry (EV-###)** and **D7 co-sign** (Nutrition +
  Product) before it can ship. Until then State 6 stays on the categorical proxy. The
  numeric field on its own — emitted but not wired to any cutoff — is an observability
  addition and does not require D7; only a cutoff that changes the line does.

## 4. Constraints honored by this note

- Log only. Nothing wired. No numbers invented (no cutoff proposed).
- Current v1 behavior unchanged: State 6 fires on `ingredient_text_quality` /
  `nova_confidence_band`, which is the correct, honest behavior and never manufactures
  a differentiator that does not exist (cf. butter-clustering / "never manufacture
  differentiation").
- Promotion path if ever scheduled: emit field (BSIP0) → carry through trace →
  EV-### + D7 before any suppress/caveat threshold reads it.
