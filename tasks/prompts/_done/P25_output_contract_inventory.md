# P25 / TASK-257 Phase 0a — Output contract inventory (route: C2)

ZERO-JUDGMENT MECHANICAL TASK. Read the listed files, extract facts, write two
output files. Do not interpret, do not improve, do not skip a field.

GOAL: The Bari "page generator" must produce frontend JSON that working category
pages can render. Your job: document EXACTLY what the 3 working pages consume,
so the generator's output contract is the union of what already works.

READ THESE FILES (repo root C:\Bari):
1. bari-web/src/data/comparisons/granola_frontend_*.json   (highest version number)
2. bari-web/src/data/comparisons/snacks JSON — find it via
   bari-web/src/lib/comparisons/registry/categories/snacks.ts (read the import line)
3. The milk data file — find it via bari-web/src/lib/comparisons/milk-comparison-page-data.ts
   (read the import line)
4. bari-web/src/lib/comparisons/registry/categories/granola.ts
5. bari-web/src/lib/comparisons/registry/categories/snacks.ts
6. bari-web/src/lib/view-models/index.ts  (the BariProductVM type — lines 1-300)
7. bari-web/src/lib/comparisons/corpus.ts (the loader + grade function)

PRODUCE FILE 1: 03_operations/page_generator/contract/page_field_inventory_v1.md
A table with one row per field found in the product objects of EACH of the 3 JSONs:
| field path | type | present in granola? | in snacks? | in milk? | example value (truncated 60 chars) | null allowed? (does any product have it null) |
Then a second table for page-level/_meta fields, same columns.
Then a third table for page-level STRINGS consumed by the page-data .ts files
(hero title, prologue sentences, category note, methodology lines, metadata
description) — list the exported constant name, the file, and 1 example line.

PRODUCE FILE 2: 03_operations/page_generator/contract/page_output_schema_v1.json
A JSON Schema (draft-07) describing the product object and the top-level document,
derived ONLY from what you saw. Mark a field `required` ONLY if it is non-null in
ALL products of ALL 3 categories. Everything else optional-nullable.

RULES: read-only outside 03_operations/page_generator/contract/. No OFF anywhere.
Do not modify any source file. If a listed file does not exist, write the exact
path you tried in the report and continue — never guess content.

RETURN BLOCK: the 2 output paths; field count per table; which fields are required
vs nullable; any file you could not find. Propose RETURNED.

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and tick the P25 line.
