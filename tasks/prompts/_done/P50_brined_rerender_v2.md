# P50 / Re-render brined-cheese page v2 (run_004 + authored copy) (route: C1-CURSOR)

Re-render the brined/salty-cheese (גבינות מלוחות) local comparison page after the data remediation + content authoring. This MERGES corrected scores + cleaned ingredients + milk-quality copy into the existing page. LOCAL only — no deploy/commit. Build the v1 page already exists; this produces v2.

## Repo
Root `C:\Bari`, app `C:\Bari\bari-web`. Reuse the existing brined-cheese trio (do NOT rebuild from scratch — update it).

## Inputs to merge (all real — never fabricate)
1. **Corrected scores:** BSIP2 `02_products/brined_cheeses/bsip2_outputs/run_brined_004/` (48 products; dist A:12 B:28 C:7 D:1). Use `final_score_estimate` (round) + `grade_estimate` + caps/context_flag from each `bsip2_trace.json`. Key change: barcode **3075805** is now 68.8/B (was 39/D).
2. **Cleaned ingredients/nutrition:** BSIP1 `03_operations/bsip1/run_brined_cheeses_002/output/` (hygiene-fixed; 2 marketing-bleed products have NULL ingredients + confidence=partial — barcodes 7290114310550, 2107071).
3. **Authored copy:** `02_products/brined_cheeses/brined_cheeses_copy_v1.json` — keyed by **barcode**: per-product `insightLine` + `rowVerdict`, and `pageShell` (heroTitle, prologueSentences, methodologyLines, categoryNote). USE THESE VERBATIM for the consumer-facing strings (replace the v1 first-pass factual placeholders).

## Update these files (the existing brined trio)
1. `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` (new v2; keep v1) — `_meta` (run_id run_brined_004, version v2) + 48 `BariProductVM` with: score/grade from run_004, insightLine + expansion.rowVerdict from copy_v1 (by barcode), expansion.nutrition + ingredients from run_002 BSIP1 (null where nulled), confidence reflecting the downgrades. imageUrl unchanged (scrape urls) — keep as-is.
2. `bari-web/src/lib/comparisons/brined-cheeses-page-data.ts` — point at v2 JSON; set hero/prologueSentences/methodologyLines/categoryNote from copy_v1 `pageShell`. Remove the `// DRAFT first-pass` markers (copy is now authored).
3. Component + route — unchanged unless the data import path needs updating to v2.

## Acceptance (hard gate)
- `cd bari-web && npm run build` MUST pass. Report output + that `/hashvaot/brined-cheeses` is in the route list.
- Verify: bc for barcode 3075805 now shows B (not D); the 2 marketing-bleed products show no ingredient list + partial confidence; hero/categoryNote come from the authored pageShell.

## Guards
- OFF ban (TASK-238): all fields from the pipeline; null stays null; never source elsewhere.
- Consumer strings come from copy_v1 — do NOT auto-generate or alter the authored Hebrew (no re-writing, no double-counting additives).
- No deploy/commit. Propose RETURNED.

## Return — Return Contract v1 JSON (+ rule 5 full distribution):
task "P50", artifacts (v2 JSON + page-data.ts, path+action+sha256), counts (products: 48/48, npm_build_pass: 1/1, bc3075805_grade (must be B), marketing_bleed_null: 2, off_used: 0, the full grade_dist of the v2 JSON derived from the file), commands_run (npm build w/ exit), not_done, self_check (build_passes, copy_verbatim_from_authored, bc048_is_B).
