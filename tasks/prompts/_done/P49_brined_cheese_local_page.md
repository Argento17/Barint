# P49 / Build local brined-cheese comparison page from run_brined_003 (route: C1-CURSOR)

You are building a **locally-viewable** brined/salty-cheese (גבינות מלוחות) comparison page in the Bari Next.js app (`bari-web/`) so the owner can critically review the scoring-engine output. This is for LOCAL viewing only (`npm run dev`) — NOT a deploy. Follow the existing **hard-cheeses** page pattern EXACTLY (it is the closest, most recent analog).

## Repo
Root `C:\Bari`. App `C:\Bari\bari-web`. Reuse the canonical shared component + view-model — do NOT invent new components.

## Data source (real scores — do not invent)
- BSIP2 scores: `02_products/brined_cheeses/bsip2_outputs/run_brined_003/` — 48 scored products. Per-product trace dirs hold `bsip2_trace.json` (keys incl. `final_score_estimate`, `grade_estimate`, `caps_applied`, `context_flag`). The run summary `02_products/brined_cheeses/reports/run_brined_003_run_summary.json` has the product list with score/grade.
- BSIP1 (names, barcodes, nutrition, ingredients, nova, images): `03_operations/bsip1/run_brined_cheeses_001/output/bsip1_brinedcheese_<barcode>.json` (keys: canonical_name_he, barcode, brand, normalized_nutrition_per_100g, energy_kcal, fat_g, fat_saturated_g, protein_g, sodium_mg, carbohydrates_g, sugars_g, ingredients_text_he, nova_proxy, image_url).
- Only the **48 IN_SCORED** products (see `02_products/brined_cheeses/factory_run_001/corpus_filter.json`, decision==IN_SCORED).

## The pattern to copy (read these — they ARE the spec)
- Route: `bari-web/src/app/hashvaot/hard-cheeses/page.tsx`
- Data module: `bari-web/src/lib/comparisons/hard-cheeses-page-data.ts`
- Thin component: `bari-web/src/components/comparisons/hard-cheeses-comparison-page.tsx` (wraps shared `@/components/comparisons/comparison-page` + a headline metric column)
- View-model type: `bari-web/src/lib/view-models/index.ts` (`BariProductVM`)
- Reference data JSON (schema = `_meta` + `products: BariProductVM[]`): `bari-web/src/data/comparisons/hard_cheeses_frontend_v2.json`

## Create these 4 files (mirror the hard-cheeses trio)
1. `bari-web/src/data/comparisons/brined_cheeses_frontend_v1.json` — `_meta` (category "brined_cheeses", run_id "run_brined_003", provenance line, grade_distribution) + `products: BariProductVM[]` for the 48. Map: score = round(final_score_estimate), grade, barcode, name (canonical_name_he), retailer "שופרסל", novaGroup (nova_proxy), `expansion.nutrition` from BSIP1, `expansion.ingredients` = ingredients_text_he. `imageUrl` = BSIP1 image_url IF present else `null` (NEVER fabricate or source elsewhere). `confidence` per existing convention (partial when fields missing).
2. `bari-web/src/lib/comparisons/brined-cheeses-page-data.ts` — exports mirroring hard-cheeses-page-data (brinedCheesesProducts loaded from the JSON, hero, prologueSentences, methodologyLines, categoryNote, metadataLine).
3. `bari-web/src/components/comparisons/brined-cheeses-comparison-page.tsx` — thin wrapper copied from hard-cheeses-comparison-page.tsx. Headline metric: use **sodium** (the defining axis for this category) via the shared metric-column pattern (`@/components/shared/comparison-metric-column`) — if no sodium metric spec exists, use the protein one as hard-cheeses does; pick the closest existing spec, do not build new infra.
4. `bari-web/src/app/hashvaot/brined-cheeses/page.tsx` — route copied from hard-cheeses/page.tsx (Hebrew title "השוואת גבינות מלוחות | Bari").

## COPY — first-pass FACTUAL only (hard guard)
- `insightLine` per product: build STRICTLY from real BSIP1 facts like the reference does (fat %, protein g, sodium mg, NOVA group, named additives from the ingredient list). NO claims beyond those numbers. NO invented provenance, authority, health claims, or marketing language.
- `categoryNote`, `hero`, `prologueSentences`, `methodologyLines`: first-pass, factual, DRAFT. categoryNote may state the true, grounded fact that brined cheeses are endemically high-sodium (sodium is structural/preservation brine). Mark these in a code comment as `// DRAFT first-pass — Content Agent + Hebrew fresh-eyes pass pending`. Do NOT fabricate.

## Acceptance (hard gate)
- `cd bari-web && npm run build` MUST pass (report the output). If it fails, fix and re-run; if it cannot pass after one genuine fix attempt, STOP and report the exact error (do not leave a broken build).
- Report the local route (`/hashvaot/brined-cheeses`) and the exact command to view it (`cd bari-web && npm run dev`).

## Guards
- OFF ban (absolute, TASK-238): every field from the scrape/BSIP pipeline only; images = scrape image_url or null; never source data elsewhere.
- No fabricated copy or claims (Bari hard rule — generated copy has shipped false authority before).
- Reuse `ComparisonPage` + `BariProductVM`; do not invent components or view-model fields.
- Do NOT deploy, commit, or push. Local files only. Propose RETURNED, do not close.

## Return — end with Return Contract v1 JSON (per `01_framework/operations/return_contract_v1.md`):
task "P49", proposed_status, artifacts (the 4 files, path+action+sha256), counts (products_in_json: 48/48, npm_build_pass: 1/1, off_used: 0, images_real_or_null, fabricated_claims: 0), commands_run (incl. `npm run build` with exit code), not_done, self_check (build_passes, route_renders, copy_factual_only). **Per return-contract rule 5: include the full score/grade distribution of the 48 products you wrote into the JSON (histogram + grade_dist), derived from the JSON you produced.**
