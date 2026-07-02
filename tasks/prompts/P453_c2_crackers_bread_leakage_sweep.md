# P453 / Crackers + Bread copy leakage & consistency sweep (route: C2)

Zero-judgment mechanical audit. TASK-433. READ-ONLY — do not edit any file, only report. This is a rule-determined pattern scan; do NOT infer, interpret, or rewrite. Report exact hits with barcode + field + the offending substring.

## Inputs (read all fields, recursively, in both files)
- C:\Bari\bari-web\src\data\comparisons\crackers_frontend_v1.json  (20 products)
- C:\Bari\bari-web\src\data\comparisons\bread_frontend_v4.json     (23 products)

## Scan every string value (walk nested objects/arrays) for these EXACT rule violations
1. **OFF markers** — any occurrence of: "openfoodfacts", "open food facts", "off-", "world.openfoodfacts", or an OFF-style source attribution. (OFF is banned project-wide.)
2. **English framework-term leakage in CONSUMER copy fields** (rowVerdict, insightLine, consumerTakeaway, bariInterpretation, expansion.*): any of BSIP, NOVA, pillar, structural_class, matrix_integrity, "cap", "archetype", "calorie_density", d4_additives, "route:", "anchor". NOTE: these terms are EXPECTED inside internal id/key strings like `bsip1_crackers_...` and field NAMES — only flag them when they appear in a HUMAN-READABLE consumer copy VALUE, not in ids/keys.
3. **Banned Hebrew phrases** in any copy field: "חלבון נמוך", plus scan for other bald health-negative absolutes of the same shape ("... נמוך"/"גרוע"/"לא בריא") and list them so a human can rule.
4. **Grade-tail in verdicts** — any rowVerdict/insightLine ending in or containing a bare "ציון NN" / "ציון NN." grade-number tail.
5. **System/token leakage** — any stray "<", "system", "assistant", tool-call fragments, or JSON/markdown artifacts inside a copy value.

## Output (one table per rule)
For each violation: `file | barcode | field-path | exact substring`. If a rule has ZERO hits, say `RULE N: 0 hits`. Do not propose fixes. Do not summarize quality. Just the hit list.

End with the machine-readable return-contract JSON block: counts per rule, total hits, files scanned, product counts (must be 20 and 23).
