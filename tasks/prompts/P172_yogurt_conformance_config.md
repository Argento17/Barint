# P172 / TASK-321C — Yogurt conformance config REV2 (route: C1-GEMINI)

Repo: C:\Bari. NO engine/scoring-logic edits. NO push. NO deploy. OFF-ban absolute. Propose RETURNED (do not close).

## CORRECTED FRAMING (read first)
Yogurt is a LEGACY/WIPED category being CONFORMED, not re-baselined. **Do NOT match any old/archived page. Do NOT check score parity. Scores are whatever the engine produces — the owner cares only that yogurt flows through the uniform path like every other category.** The only hard gates: **OFF = 0** and a valid uniform config. (Your REV-1 config was on the right run — keep it; just apply the corrections below.)

## Goal
Create/overwrite `03_operations/page_generator/configs/yogurts.json` for uniform `generate_page` conformance. Model on `configs/hard_cheeses.json` (structure) + `configs/cereals.json` (render_fields format).

## Inputs (verified by orchestrator)
- **`run_products_dir` = `02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_v2/products`** — 108 traces, **0 OFF** (verified). Keep this run. NEVER use run_yogurt_002 (OFF-tainted).
- **SCOPE: emit only the ~88 YOGURT products; EXCLUDE the ~20 milk-context products** (they belong to the milk shelf, not yogurt). Identify them by product type/category in the trace and exclude with reason `milk_context_not_yogurt`.
- `bsip1_dir`: the matching yogurt BSIP1 output dir.
- `baseline_json`: **null** (legacy/wiped page replaced; copy authored fresh by Content/Sonnet later).

## Tasks
1. Scope to yogurt-only (~88); exclude the milk-context ~20 (per-product reason). Also exclude any OFF-provenance product (should be 0) or non-yogurt.
2. **OFF guard:** confirm 0 emitted products carry `open_food_facts` (grep corpus + traces). Report count.
3. `scoring.flags`: standard dairy set (`BARI_SHELF_RELATIVE_V1=on, BARI_FAT_TECH_V1=on, BARI_RECAL_P0=on`, others off). Set `shelf_rel` from yogurt constants if present, else null.
4. Declare `render_fields` for the standard comparison component (model on cereals.json format).
5. Smoke: `generate_page.py --config configs/yogurts.json` emits the ~88 with **G4 OFF PASS**. Report emitted count + grade dist (no target).

## Return (propose RETURNED, do not close)
`configs/yogurts.json` + verification note (emitted count, grade dist, OFF=0, milk-context exclusions count). Files changed (path+action+sha256). End with the TASK-321C return-contract JSON. Clean up temp files.
