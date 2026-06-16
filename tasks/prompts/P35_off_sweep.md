# P35 / OFF-audit sweep — every live category (route: C2)

**➡️ OWNER: after you send this prompt, open `tasks\DISPATCH_BOARD.md` and put an
`x` in the P35 line under 📬 Signals. Do that first, then paste the rest to the agent.**

---

ZERO-JUDGMENT MECHANICAL TASK. Scan, count, report. Fix nothing, delete nothing.

WHY (context): the OFF ban (TASK-238) is Bari's hardest rule — Open Food Facts may
never feed any page. Two live categories are now CONFIRMED contaminated (cereals:
8 products; granola: 10 products, both via incomplete purges). Yogurts is confirmed
clean. Every other live category is UNKNOWN. You produce the definitive map.

SCAN TARGETS — every category data file consumed by the live site:
1. List them by reading the import lines of every file in
   `bari-web/src/lib/comparisons/registry/categories/*.ts` AND
   `bari-web/src/lib/comparisons/milk-comparison-page-data.ts` (legacy milk) AND
   any other `bari-web/src/data/**/*.json` referenced by a page-data .ts under
   `bari-web/src/lib/comparisons/`. Cite every (category → data file) pair found.

FOR EACH category data file, two checks:
A. JSON-level: scan the file text for: `open_food_facts`, `openfoodfacts`,
   `images.openfoodfacts.org`, `world.openfoodfacts`. Count hits + list barcodes
   of affected products.
B. Corpus-level: for EVERY product barcode in the file, find its BSIP1 record
   under `03_operations/bsip1/*/output/*.json` (match by `"barcode"` field).
   Report per product: `panel_source` value (or the `source.panel_source` nested
   variant). Any record with panel_source = "open_food_facts" → the displayed
   product is OFF-FED. List barcode + product name + which corpus dir.
   A barcode with NO BSIP1 record anywhere = "NO_RECORD" (report, don't guess).

OUTPUT: `03_operations/off_sweep/off_sweep_v1.md` with:
- Verdict table: | category | data file | products | OFF-fed (B) | JSON markers (A) | NO_RECORD | verdict CLEAN/DIRTY/UNKNOWN |
- Per dirty category: the barcode list with names and corpus paths.
- Include the two known-dirty categories (cereals, granola) — your numbers must
  reproduce the known findings (cereals 8, granola 10); if they don't, say so
  loudly rather than adjusting.

RULES: read-only everywhere except `03_operations/off_sweep/`. No network. No
fixes. Python stdlib or text search — your choice, but report the method.

RETURN BLOCK: the verdict table verbatim; total OFF-fed products across the live
site; any NO_RECORD concentrations. End with the machine-readable JSON return
contract (`01_framework/operations/return_contract_v1.md`) — `counts` must
include per-category `off_fed: N/M` with M = products in that data file.
Propose RETURNED.
