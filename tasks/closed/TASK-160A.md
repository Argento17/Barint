---
id: TASK-160A
title: snk-006 thumbnail (barcode 7290118427858) — re-scrape to source an image; no image_url/source_url persisted, Carrefour source
owner: data-agent
status: CLOSED
priority: LOW
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC close-gate PASS — verified against artifacts, not the return prose. (1) HIGHEST-RISK constructed-URL re-fetch: I independently fetched https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/1/2/12615222_7290118427858.jpg — HTTP 200, content-type image/jpeg, 842.7KB binary (no HTML/404/placeholder redirect); rendered the saved JPEG and visually confirmed the real product: Nestle Fitness, 'שוקולד מריר', GRANOLA BAR / CRUNCHY, משקל כולל 190 גרם (5 אריזות × 38 ג'), with the 2 red gov warning icons (סוכר/שומן רווי) — matches BSIP1 package_size_g=190/unit_count=5/unit_size_g=38. The constructed Yochananof path genuinely resolves to the correct image. (2) snacks_frontend_v2.json:599 — snk-006 imageUrl == that exact URL; id-matched diff vs HEAD = 0 score deltas / 0 grade deltas / 0 ids added-removed (the raw line-diff 44<->46 was a re-sort artifact, same false-flag class as TASK-160's bread note). (3) Score integrity: snk-006 still 17/E (json:600-601); display-only confirmed. In HEAD snk-006 was the ONLY null imageUrl; now 18/18 snacks have a non-null imageUrl (0 null). (4) Validation re-run by CC: node scripts/validate-corpus.mjs -> exit 0, 0 errors (snacks 0 errors, 3 pre-existing §2.8 token warnings on snk-001/snk-011, unrelated); npx tsc --noEmit -> exit 0. (5) BSIP1 provenance writes exist: bsip1_7290118427858.json:15-16 (image_url + image_url_source) and bsip1_audit_7290118427858.json:61-70 (image_recovery block). Snacks image coverage now complete (18/18). User holding on commit — NOT committed."
roadmap_impact: false
depends_on: [TASK-160]
blocks: []
category_id: snacks
summary: >
  snk-006 is the one cleanup item TASK-160 could not resolve: no persisted image source. Re-scrape the snacks source (Carrefour barcode 7290118427858) to recover an image_url, then populate snacks_frontend_v2.json. Display-only; no score touched.
---

# TASK-160A — snk-006 thumbnail (barcode 7290118427858) — re-scrape to source an image; no image_url/source_url persisted, Carrefour source

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
