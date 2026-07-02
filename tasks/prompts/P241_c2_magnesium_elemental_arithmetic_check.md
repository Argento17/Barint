# P241 / Magnesium elemental-dose arithmetic verification (route: C2)

<!-- META (read first): This is a ZERO-INFERENCE arithmetic check. Do ONLY the math
     stated below. Do not decide which value is "authoritative", do not infer missing
     data, do not rescore. Return the table + the flag list. Nothing else. -->

## Task
For each row below you are given: compound MASS (mg), magnesium FORM, the dossier
ELEMENTAL FRACTION for that form, and the page's CLAIMED elemental mg.

Compute `recomputed_elemental = round(mass × fraction, 1)`.
Then compare to `claimed_elemental`.

- If `|recomputed − claimed| ≤ 2.0` → mark `OK`.
- If the difference is `> 2.0` → mark `MISMATCH` and show both numbers.
- If FRACTION is given as `NONE` (form not in dossier) → mark `NO_FRACTION` (do not compute).
- If FORM is a `BLEND` (multiple forms, no per-form split) → mark `BLEND_UNVERIFIABLE` (do not compute).

Elemental fractions (dossier): oxide 0.603 · citrate 0.162 · bisglycinate 0.141 ·
malate 0.155 · taurate 0.089 · carbonate 0.288.

## Rows
| # | barcode | form | mass_mg | fraction | claimed_elemental_mg |
|---|---|---|---|---|---|
| 1 | 7290013142894 | oxide | 450 | 0.603 | 271 |
| 2 | 7290001065662 | oxide | 520 | 0.603 | 314 |
| 3 | 7290015318426 | oxide | 520 | 0.603 | 314 |
| 4 | 7290017218564 | oxide | 520 | 0.603 | 314 |
| 5 | 7290010207640 | hydroxide | 450 | NONE | 272 |
| 6 | 7290019444206 | oxide | 450 | 0.603 | 271 |
| 7 | 7290017847122 | oxide | 432 | 0.603 | 260 |
| 8 | 7290015429245 | carbonate | 160 | 0.288 | 46 |
| 9 | 7290001066973 | malate | 700 | 0.155 | 109 |
| 10 | 7290015318532 | malate | 136 | 0.155 | 21 |
| 11 | 7290011899967 | citrate | 200 | 0.162 | 32 |
| 12 | 7290013464248 | citrate | 250 | 0.162 | 41 |
| 13 | 7290019444480 | bisglycinate | 250 | 0.141 | 35 |
| 14 | 7290018439579 | taurate | 76 | 0.089 | 7 |
| 15 | 7290118818205 | BLEND | 550 | BLEND | 89 |
| 16 | 0033984005181 | citrate | 100 | 0.162 | 16 |
| 17 | 7290118816065 | BLEND | 200 | BLEND | NA |
| 18 | 7290001065594 | bisglycinate | 88 | 0.141 | 12 |
| 19 | 7290018439043 | bisglycinate | 168 | 0.141 | 24 |

## Return (to tasks/returns/P241_return.md)
1. The full table with two added columns: `recomputed_elemental`, `verdict`.
2. A list of every row whose verdict is MISMATCH, NO_FRACTION, or BLEND_UNVERIFIABLE.
3. Nothing else — no scoring opinions, no recommendations.
