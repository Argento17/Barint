# P163 / TASK-310 — Assemble: overlay-merge 7 re-baselined pages into bari-web (route: Frontend Agent / C1)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Full repo access. Repo-side + REVERSIBLE (git). **NO push, NO deploy.**

## Why an overlay-merge (NOT a file swap)
The staging pages (`_rescore_staging/<shelf>/<shelf>_rescored.json`) are score- and copy-complete, but the generic
generator does NOT emit the frontend's display/render fields. Live pages have them; staging lacks them (verified):
- juices: `sugarPer100ml`, `kcalPer100ml`, `novaGroup`, `retailers`, `subPool`
- cakes/cookies: `novaGroup`, `_has_phvo`, `_source_retailers`, `_category_routed`
- hummus: `glassBox` (64/64 live), `d3_processing_signal`, and `_product_type` (null in staging; live has matbucha/eggplant_spread/pepper_spread/hummus_spread/masabacha)
- cereals/granola: `confidence_level`
These are OPTIONAL in the VM types (pages degrade, don't crash), BUT dropping them is a real consumer regression
(e.g. hummus loses ALL glass-box panels; the **/vegetable-spreads page** — which imports the SAME `hummus_frontend_v5.json`
and builds its filter map from `_product_type` — loses its matbucha/eggplant/pepper lenses). So: keep live's fields, overlay only what changed.

## The 7 shelves → live JSON targets
| staging | live target |
|---|---|
| _rescore_staging/cereals/cereals_rescored.json | bari-web/src/data/comparisons/cereals_frontend_v2.json |
| _rescore_staging/cakes/cakes_rescored.json | bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json |
| _rescore_staging/cookies_coffee/cookies_coffee_rescored.json | bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json |
| _rescore_staging/granola/granola_rescored.json | bari-web/src/data/comparisons/granola_frontend_v1.json |
| _rescore_staging/juices/juices_rescored.json | bari-web/src/data/comparisons/juices_frontend_v3.json |
| _rescore_staging/brined_cheeses/brined_cheeses_rescored.json | bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json |
| _rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json | bari-web/src/data/comparisons/hummus_frontend_v5.json |

## Owner ruling 2026-06-17 — CLEAN CATEGORY SCOPE (apply exactly)
- **hummus:** prepared-dips-only — DROP these 7 (in live, not staging): `1990261, 3643714, 3643820, 7296073005889, 7296073006015, 7296073733324, 7296073733331`. Net-new: 0.
- **granola:** muesli→granola swap — DROP these 7 muesli (in live, not staging): `5018357006731, 5018357006755, 7290011131371, 7290011131388, 7290011131395, 7290014471436, 7290016883183`. ADD these 7 granola net-new: `7290011131968, 7290011668587, 7290014471443, 7290112497994, 7290112498007, 7290116534619, 7613035635845`.
- **cookies_coffee:** ADD 1 net-new: `80083764` (עוגיות דגנים עם ש.שועל).
- **juices:** ADD 1 net-new: `7290013608680` (מיץ עגבניות — tomato juice). **DROP the 3 non-juice items** (plant-milk/iced-coffee — a juices page must not list these): `5411188115434` (Alpro Barista Soy), `7290110325893` (Tnuva iced coffee), `7290110558420` (Alpro oat cold). ALSO add these 3 to `03_operations/page_generator/configs/juices*.json` `exclusions` (reason `out_of_scope: plant-milk/coffee drink, not a juice`) so future re-scores stay clean.
- **cereals / cakes / brined_cheeses:** no add/drop — pure re-score+copy overlay.

## Algorithm (per shelf, write the assembled JSON back to the live target)
1. Load live target + staging. Index both by barcode.
2. Start from the LIVE products list. **Remove** the drop-barcodes above.
3. **Overlay-merge** every product present in BOTH: take the live product object as the base; overlay from staging ONLY: `score`, `grade`, and the copy fields that live's schema carries for that shelf (`insightLine`, `rowVerdict` where the field exists on that page, and any other LIVE copy field the staging product also has — e.g. cakes/cookies `consumerTakeaway`/`bestUseCases`/`bariInterpretation[].interpretation` etc.). KEEP every other live field untouched (all render/display fields). Do NOT introduce staging-only fields that live's schema doesn't have.
4. **Net-new products** (granola 7, cookies 1, juices tomato 1 = 9): construct each to EXACTLY the live product schema for that shelf. Bring score/grade/copy from staging; DERIVE the render/display fields from the product's BSIP2 trace / staging nutrition (`02_products/<cat>/.../bsip2_trace.json` or the staging product's own nutrition block):
   - `novaGroup` ← trace NOVA group; `confidence_level` ← trace confidence; `_has_phvo` ← trace PHVO/hardened-fat signal; juices `sugarPer100ml`/`kcalPer100ml` ← per-100ml nutrition; `retailers`/`subPool`/`_source_retailers`/`_category_routed` ← trace/corpus provenance. If a field genuinely cannot be derived, set it to the same null/empty shape the VM type allows (never fabricate, never OFF). `_product_type`: only hummus uses it for filtering and there are 0 hummus net-new, so net-new on other shelves may carry null if live peers do.
5. **_meta:** update `product_count`, `scored_count`, `grade_distribution` (recompute from final products IF the live _meta carries it), `generated` (now), and `run_id` to the shelf's re-baseline run (cereals/granola=run_cereals_008 per existing; hummus=run_hummus_shelfrel_002; use the staging _meta `source_paths`/run to pick the correct id). Fix stale _meta (prior RT-1/RT-2 findings) — counts MUST equal the final product array.
6. **Sort** `products` by `score` descending (golden-page lesson).
7. OFF-ban: 0 OFF anywhere in output. Direct-scrape data only; null if absent.

## Verify (report all)
- `cd bari-web && npx tsc --noEmit` → 0 errors; `npm run build` → exit 0 (capture the real exit code).
- All 7 routes build + render: /hashvaot/breakfast-cereals, /cakes, /cookies-coffee, /granola, /juices, /brined-cheeses, /hummus — AND **/hashvaot/vegetable-spreads** (shares hummus JSON; confirm its matbucha/eggplant/pepper lenses still populate from `_product_type`).
- score==trace on every assembled page (page score == BSIP2 trace `final_score_estimate`); 0 mismatches.
- OFF=0; product counts per page == _meta; no PENDING_COPY on displayed products beyond the pre-existing cookies_coffee live-parity set.
- Frozen invariants untouched: milk page NOT modified; no snack-bar reaches A.

## Boundaries
- Edit ONLY: the 7 bari-web live comparison JSONs + the juices config `exclusions`. No engine, no scoring, no other JSON, no milk, no route/component code unless a build error REQUIRES a minimal schema-compat fix (if so, report it explicitly). No push, no deploy.

## Return (do NOT close — propose RETURNED)
Per-shelf: final product count, drops applied, net-new added (with derived-field provenance), grade distribution, _meta diff.
Build: tsc result + `npm run build` exit code (paste the tail). Route render confirmation incl /vegetable-spreads. score==trace + OFF=0 results. Files changed (path+action+sha256). End with the return contract JSON (`01_framework/operations/return_contract_v1.md`): `task` (TASK-310), `proposed_status`, `artifacts[]`, `counts{}` (with commands), `commands_run[]`, `not_done[]`, `self_check`.
