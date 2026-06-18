# P171 / TASK-321B — Cheese conformance config REV2 (route: C1-GROK)

Repo: C:\Bari. NO engine/scoring-logic edits. NO push. NO deploy. OFF-ban absolute. Propose RETURNED (do not close).

## CORRECTED FRAMING (read first — supersedes any parity goal)
Cheese is a LEGACY category being CONFORMED, not re-baselined. **Do NOT match the old live page. Do NOT check score parity. Scores are whatever the engine produces — the owner does not care about the numbers, only that cheese flows through the uniform path like every other category.** The old `cheese_frontend_v3.json` is being REPLACED. The only hard gates: **OFF = 0** and a valid uniform config.

## Goal
Create/overwrite `03_operations/page_generator/configs/cheese.json` so cheese conforms to the uniform `generate_page` path. Model structure on `03_operations/page_generator/configs/hard_cheeses.json`; model the `render_fields` declaration on `configs/cereals.json` / `configs/juices.json`.

## Inputs (verified by orchestrator)
- **Use `run_products_dir` = `02_products/cheese_spreads/bsip2_outputs/run_cheese_004/products`** — 59 traces, **0 OFF** (verified). This is the run the live page actually descended from; run_cheese_001 was WRONG (ignore it).
- `bsip1_dir`: the matching cheese BSIP1 output dir (find it: `03_operations/bsip1/run_cheese_004/output` or under `02_products/cheese_spreads/`).
- `baseline_json`: **null** (legacy page is being replaced; copy will be authored fresh by Content/Sonnet later — not your job).

## Tasks
1. Emit **all valid cheese-spread products** in run_cheese_004 — NO editorial curation/exclusions. Only exclude a product if (a) it carries `open_food_facts` provenance (OFF-ban) or (b) it is genuinely not a cheese/spread (mis-routed); document any such exclusion with a per-barcode reason.
2. **OFF guard:** confirm 0 emitted products carry `open_food_facts` provenance (grep the chosen BSIP1 corpus + traces). Report the count.
3. `scoring.flags`: the standard dairy set (`BARI_SHELF_RELATIVE_V1=on, BARI_FAT_TECH_V1=on, BARI_RECAL_P0=on`, others off) — same as hard_cheeses. Set `shelf_rel` from the cheese-spread constants if present (`FATSAT_SHELF_REL_CHEESESPREAD_*`), else null.
4. Declare `render_fields` matching what the standard comparison component needs (model on hard_cheeses/brined_cheeses + the render_fields format in cereals.json).
5. Smoke: `generate_page.py --config configs/cheese.json` must emit the products with **G4 OFF PASS**. Report the emitted count + grade distribution (whatever it is — no target).

## Return (propose RETURNED, do not close)
`configs/cheese.json` + a verification note (emitted count, grade dist, OFF=0 confirmation, any non-cheese exclusions). Files changed (path+action+sha256). End with the TASK-321B return-contract JSON. Clean up any temp files you create.
