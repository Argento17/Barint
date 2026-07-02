---
id: TASK-446
title: Productionize Azure DI OCR prototype into a BSIP0 label-image fallback stage (rescue image-only-label products)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  A working Azure Document Intelligence OCR client exists at 03_operations/bsip0/pipeline/main.py but is a PROTOTYPE (~3 sample products, per README), not wired into the production BSIP0 flow. Productionize it as a fallback stage: when HTML scrape yields NULL ingredients/nutrition AND a direct-scrape label image exists, route the image through Azure DI (layout+tables), parse panel+ingredients, feed BSIP1 with provenance + per-field confidence. Confidence gate: low-confidence stays NULL, never fabricated. Enforce OFF image-ban (direct-scrape image only). Measure rescue rate across live categories. Extends missing_data_discard_rule (rescue before discard).
---

# TASK-446 — Productionize Azure DI OCR prototype into a BSIP0 label-image fallback stage (rescue image-only-label products)

## Why
Bari's premise is "parsed ingredients + nutrition, or the field is NULL and the product is discarded" ([[missing_data_discard_rule]]). Today, a product whose nutrition panel / ingredient list exists only as a **label image** yields NULL and is thrown away — even though a working OCR path already exists. A real Azure Document Intelligence client is built at `03_operations/bsip0/pipeline/main.py` (layout+tables mode, `.env` key `AZURE_DI_KEY`, endpoint `bsip0ocr.cognitiveservices.azure.com`, `ocr_cache.json`), but the README labels `pipeline/` a **prototype** and only ~3 sample products exist (`pipeline/outputs/product_00{1,9,10}.json`). Capability exists; it is not wired into the production BSIP0 flow. This rescues discarded products before discard — it does not change the discard rule, it front-runs it.

## Scope / deliverable
Turn the prototype into a standing BSIP0 fallback stage:
1. **Trigger:** invoked only when the HTML/direct scrape yields NULL ingredients and/or NULL nutrition for a product that HAS a label image **from the direct scrape**.
2. **Extract:** route that image through Azure DI (layout+tables), parse the nutrition panel (per-100g) and the ingredient list.
3. **Feed BSIP1** with the OCR'd values, carrying provenance (`ocr_engine`, source image URL) and **per-field confidence** (Azure DI returns confidences).
4. **Integrate** into the real category-build path (corpus/factory/BSIP0 runner), not a side script.

## Definition of Done (hard gates)
- [ ] **Confidence gate:** below a set threshold, the field stays **NULL** — never a fabricated value. "Unknown is acceptable; a wrong number is not." (No-fabrication + [[missing_data_discard_rule]].)
- [ ] **OFF image-ban enforced:** the image MUST come from the direct product scrape; never OFF, never any substitute source ([[off_ban_hard_rule]] — the ban covers images).
- [ ] **Hebrew RTL panel parse validated:** RTL nutrition tables + Hebrew ingredient lists parse correctly (watch [[hebrew_shell_corruption_and_verify_gotchas]]); spot-checked against the real label, not assumed.
- [ ] **Provenance on every OCR'd field** (engine + source image + confidence) so it survives into BSIP1/trace and is auditable ([[citations_discipline]]).
- [ ] **Cost/caching retained** (keep `ocr_cache.json`; batch; per-page Azure DI cost is real).
- [ ] **Rescue-rate measured:** report how many currently-NULL/discarded products across the live categories this actually recovers (trace-derived count, not estimated).

## Governance
- Score-neutral to build (adds/rescues data; does not touch scoring logic). Any downstream score change from newly-populated fields flows through the normal verify → two-gate → owner path like any data refresh.
- Not a scoring change; owning agent = Data Agent. No tripwire on the build itself; a large corpus expansion that changes many published scores would surface for owner review at deploy.

## Related
- Sibling image capability: rembg (product-photo background removal / card cutouts) — the two together are the product-image asset stream.
- Depends on the wired-in capability audit (TASK-447) confirming no other OCR path is already live.

<!-- Live orchestrator view: tasks/DISPATCH_BOARD.md. -->
<!-- opened with new_task.py -->

