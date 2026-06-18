(route: C1-GEMINI)

# P204 — Verify + salvage the 19 EAN-confirmed image URLs (TASK-243)

## Context
Local branch `image-backfill-task-243` (commit `cbe05bf2d`, "TASK-243: backfill 19/32 null OFF
images with Yochananof EAN-confirmed URLs") added product image URLs for live categories. The
branch itself is an ancient pre-consolidation tree (unmergeable as a branch), so we only want
the 19 image URLs IF they still fill null/missing images on master's CURRENT live JSONs.

The URLs are **Yochananof EAN-confirmed** (direct retailer), NOT Open Food Facts. Do NOT add any
OFF URL or OFF-hosted image — OFF is banned project-wide (hard rule). If any of the 19 URLs
resolve to an openfoodfacts.org / world.openfoodfacts host, DISCARD that one and report it.

## Task
1. Extract the image-URL additions from `git show cbe05bf2d` for these three files:
   - `bari-web/src/data/comparisons/cereals_frontend_v2.json`
   - `bari-web/src/data/comparisons/granola_frontend_v1.json`
   - `bari-web/src/data/comparisons/hard_cheeses_frontend_v2.json`
   For each, list `{barcode/productId, image URL}` it sets.
2. For EACH of those products, check master's CURRENT version of the same JSON:
   - If the product's image field is null/empty/missing on master AND the branch URL is a
     non-OFF Yochananof URL → it's a salvageable fill.
   - If master already has a (non-OFF) image, or the product no longer exists on master → skip.
3. Apply ONLY the salvageable fills to master's current JSONs (do not touch any other field;
   do not reorder; do not change scores/copy). Preserve exact JSON formatting.
4. `cd bari-web && npm run build` — must exit 0.

## Hard constraints
- OFF = 0. Reject any OFF-hosted URL.
- Image field only. No score/copy/structure changes. No product add/remove.
- Branch from `origin/master`, name `sweep/image-backfill-salvage`, commit, push.

## Return (self-verifying)
- Table: each of the 19 → {fills master null | master already has image | product gone | OFF-rejected}.
- Count actually applied (e.g. "7 of 19 filled real nulls; 9 already had images; 2 products gone; 1 OFF-rejected").
- `npm run build` exit code + the "Compiled successfully" line.
- Push confirmation. If ZERO are salvageable, push nothing and say so — we'll just delete the branch.
