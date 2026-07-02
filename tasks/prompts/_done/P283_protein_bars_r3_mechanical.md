# P283 / Protein-bars round-3 mechanical JSON edits (route: C2)

TASK-365 (read `C:\Bari\tasks\TASK-365.md`). Zero-inference mechanical edits to ONE data file. Every operation below is fully determined by an explicit rule — do not infer, decide, or identify anything. Do NOT author or change any prose meaning; only the deletions/normalizations specified.

## Target file (edit ONLY this one)
`C:\Bari\bari-web\src\data\comparisons\protein_combined_frontend_v2.json`
(JSON: top keys `_meta`, `products`; `products` is an array of 33 product objects.)

## Operations (apply in order, exactly)
1. **Remove granola:** delete the single product object in `products` whose `"id" == "pb-001"`. (After this, 32 products remain.)
2. **Re-rank:** keep the remaining products in their current array order. Set each product's `"rank"` to its 1-based position in the array (first = 1 … last = 32) and set each product's `"categoryTotal"` to `32`.
3. **Meta count:** set `_meta["product_count"] = 32`.
4. **Strip trailing grade tag from rowVerdict ONLY:** for each remaining product, if `"rowVerdict"` is a string that matches the Python regex `r"\s*[—–\-]\s*[A-E]\.?\s*$"` at its end (e.g. it ends with " — D." or " — C" or " — B."), remove exactly that trailing match. Then `rstrip()` the string; if the result does not end with one of `. ! ?`, append a single `"."`. Do **NOT** modify `"insightLine"` or any other field.
5. Write the file back with `json.dump(..., ensure_ascii=False, indent=2)`, UTF-8.

## Hard guards
- **Run NO git commands** (no stash/checkout/add/commit). Edit only the one file above. Touch no other file.
- Do not reorder products (other than the pb-001 removal). Do not change scores, nutrition, names, displayTitle, comparisonContext, or insightLine.
- This is deterministic find/replace + delete; if any step seems to require a judgment call, STOP and report instead of guessing.

## Return (do NOT close — propose RETURNED)
Report: (a) products count after = should be 32; (b) confirm no product with id "pb-001" remains; (c) number of rowVerdicts changed by step 4; (d) the new first product's `id` + `score`; (e) the exact Python (or jq) you ran. End with the machine-readable return contract (`01_framework\operations\return_contract_v1.md`).
