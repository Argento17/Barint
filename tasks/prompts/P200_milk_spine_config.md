# P200 / Finalize milk spine config + prove generate_page on the uniform path (route: C1-GROK)

➡️ OWNER: TASK-321 Wave 3 (milk). Grok finalizes `configs/milk.json` and proves milk runs
through the uniform `generate_page` path with all gates green and OFF=0. Scoring-side only;
no frontend, no engine edits, no score philosophy. Orchestrator verifies before close.

---

You are completing the milk category's SPINE config so milk runs through the same
`generate_page` path as every other category (the "uniform spine"). This is scoring-side
work in the main repo `C:\Bari`. Do NOT touch the frontend (bari-web), the engine, or any
other category's config.

## Context
- The milk freeze was lifted by the owner; milk now scores as a normal shelf.
- The config draft is `C:\Bari\03_operations\page_generator\configs\milk.json` (status DRAFT).
- The generator: `python generate_page.py --config <cfg> --out <out>` (run from
  `C:\Bari\03_operations\page_generator\`). It self-gates by default (G1 SCHEMA, G2 COVERAGE,
  G3 SCOPE, G4 OFF, G5 GRADE-INTEGRITY, G6 COPY-SAFETY, G8 DATA-SANITY) and prints the gate report.
- Reference configs that ALREADY pass on this path: `configs/yogurts.json` and `configs/cheese.json`.
  Mirror their shape. Both use `"baseline_json": null` and a small `render_fields` list.

## Tasks (do exactly these)
1. Edit `configs/milk.json`:
   - Set `"baseline_json": null` (the gold-standard milk copy lives on the frontend track, not here;
     a null baseline matches yogurts.json / cheese.json).
   - Replace the `render_fields` TODO **string** with the list `["novaGroup", "confidence_level", "d4_additives"]`
     (mirror `cheese.json`).
   - Keep the `scoring.flags` exactly as drafted (MILK_CANONICAL_FLAGS, `BARI_RECAL_P0` stays `off` —
     this reproduces milk's published scores; flag harmonization is a separate owner decision, do NOT change it).
   - Set `"_status"` to `"READY — spine-runnable"` and trim the `_comment` to one line noting the config is finalized.
2. Run the generator:
   `python generate_page.py --config configs/milk.json --out _generated_milk.json`
3. Read the gate report it prints.

## Hard rules
- NEVER use Open Food Facts (OFF) — any field, any fallback. Unknown is acceptable; OFF is not.
  G4 OFF MUST be 0. If it isn't, STOP and report the offending barcodes — do not "fix" by substituting data.
- Do not invent product/nutrition data. Do not edit the engine or `rescore_all.py`. Do not touch other configs.
- If a gate fails (e.g. G8 data-sanity = nutrition text bled into ingredients), do NOT fabricate a fix.
  List the offending barcodes so the orchestrator can discard them via `exclusions` (missing-data-discard doctrine).

## Return block (end with this — fill in REAL numbers from the run)
- Command(s) run (verbatim).
- Product count in output / scored (run universe) / exclusions.
- Grade distribution (S/A/B/C/D/E counts).
- Gate table: each of G1,G2,G3,G4,G5,G6,G8 → PASS/FAIL (G4 OFF must show the literal OFF count).
- Top 3 products: barcode, score, grade.
- Any FAIL: which gate + offending barcodes (no fabricated fixes).
- Files changed (path + 1-line what).
