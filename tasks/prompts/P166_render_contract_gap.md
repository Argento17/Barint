# P166 / TASK-316 — Spine step 1: close the generator render-contract gap (route: Data Agent / C1)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Staging-only. NO scoring/engine edits. NO bari-web edits. No commit, no deploy. You propose RETURNED.

## The gap (and why it matters)
`03_operations/page_generator/generate_page.py` is the single page generator. It emits **scoring + copy** fields but NOT the full frontend **render contract**. The live comparison pages carry display fields the generator omits — and those fields are produced today by the **bespoke per-category builders**:
- `03_operations/bsip2/proto_v0/src/build_juices_frontend_v3.py` (sugarPer100ml, kcalPer100ml, novaGroup, retailers, subPool)
- `03_operations/bsip2/proto_v0/src/build_hard_cheeses_frontend.py` (glassBox, novaGroup, _has_phvo, d3_processing_signal, d4_additives)
- `03_operations/bsip2/proto_v0/src/batch_run_hummus_001.py` (_product_type, glassBox)
- plus `build_salty_snacks_frontend_v2.py` etc. for patterns
Because the generator doesn't emit these, this week's publish needed a manual OVERLAY-MERGE (TASK-310) and a true "flip a flag → deploy-ready page" flow is impossible. **Close the gap: port the render-field derivation INTO generate_page so its output is drop-in.**

## What to build
Extend `generate_page.py`'s config-driven mechanism — `build_product()` + `get_extension_field_value()` + each category config's `extension_fields` — so the generator emits the render contract each category's LIVE page carries. Data comes from what the generator ALREADY reads: `corpus_rec` (normalized_nutrition_per_100g, source_retailers, ingredients, subtype) and `trace` (L3_inferred_classifications incl additive markers / NOVA / processing signals, dimension_scores, confidence).

Fields to emit (derive each from corpus/trace; the LIVE page JSON for each category is the source of truth for WHICH fields + their shape):
- **Nutrition-derived:** `sugarPer100ml`, `kcalPer100ml` (liquids — juices), `novaGroup`, `_has_phvo`, `confidence_level`.
- **Provenance:** `retailers` / `_source_retailers`, `subPool` / `_category_routed`.
- **Classifier:** `_product_type` (e.g. hummus subtypes hummus_spread/masabacha/matbucha/eggplant_spread/pepper_spread) — port the classifier from `batch_run_hummus_001.py`; config-driven keyword map over name/ingredients; null if unclassifiable (NEVER guess, NEVER OFF). This one powers the /vegetable-spreads lenses.
- **Structured:** `glassBox`, `d3_processing_signal`, and populate `d4_additives` — port from `build_hard_cheeses_frontend.py` logic, built from trace additive/processing signals.

Make it **config-driven**: each category's config declares the render fields it needs (extend `extension_fields` or an analogous block) so a category gets exactly its live schema — no category-special-cased code paths in the generator (uniform-baseline doctrine). Port the SHARED derivation once; drive per-category via config.

## Hard constraints
- **Additive OUTPUT only. ZERO score/grade change** — score stays `trace.final_score_estimate`, grade unchanged. Do NOT touch the scoring engine or any `score_engine`/`signal_extractor` module.
- **OFF-ban absolute** — derive only from the direct-scrape corpus + trace. If a value isn't present, emit null (the VM types are optional). NEVER fabricate, NEVER use Open Food Facts.
- Scope to the **7 re-baselined categories** for now: cereals, cakes (cakes_hard_cookies), cookies_coffee, granola, juices, brined_cheeses, hummus.
- Edit ONLY `generate_page.py` + the per-category configs (+ a small shared helper module if cleaner). Do NOT edit bari-web, the scoring engine, or the live JSONs.

## Acceptance test (this is the point — prove drop-in parity)
For each of the 7 categories: regenerate via `python 03_operations/page_generator/rescore_all.py --shelf <shelf>` (staging), then compare the generated product objects to the **live** page (`bari-web/src/data/comparisons/<live>.json`) for products present in both:
- The render fields the live page carries are now PRESENT in the generated output with matching shape/values (glassBox present where live has it; _product_type populated → matbucha/eggplant/pepper counts match live; sugarPer100ml/novaGroup present; etc.).
- score == trace and grade unchanged (regression check); OFF=0.
- Report per-category: which render fields are now emitted, drop-in parity result (field presence + spot value match vs live), and any field that CANNOT be derived from corpus/trace (list it honestly as a residual — do not fake it).

## Return (do NOT close — propose RETURNED)
Per-category render-field coverage + drop-in parity vs live; the regression check (score==trace, grade unchanged, OFF=0); files changed (path+action+sha256); any residual underivable fields. End with the TASK-316 return-contract JSON (`01_framework/operations/return_contract_v1.md`): task, proposed_status, artifacts[], counts{} (with commands), commands_run[], not_done[], self_check.
