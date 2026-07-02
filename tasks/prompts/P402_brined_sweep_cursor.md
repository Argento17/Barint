# P402 / Brined-cheeses honesty-sweep copy fixes (route: C1-CURSOR)

You are a C1 builder (Cursor). Fix verified honesty/accuracy defects in the LIVE brined-cheeses comparison copy. Consumer-facing copy under the two-gate rule — your output is a DRAFT (an Adversarial-QA gate follows). Edit ONLY the one JSON file. Do NOT change any score/grade/rank/nutrition value. OFF ban: never add data from any external source; everything must be grounded in the product's own existing fields.

## FILE (edit only this; it is the live origin/master version in this worktree)
C:\bari_sweep_brined\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json
(36 products, ids bc-001..bc-048 sparse. Each product: name, brand, grade, score, insightLine, rowVerdict, expansion{ingredients, positiveSignals, limitingFactors, comparisonContext, consumerExplanation}.)

## FIXES (all verified by the orchestrator against the file)

### F1 — Stale corpus count (bc-036)
rowVerdict contains "...מבין 48 המוצרים..." — the corpus is 36, not 48. Reword to "36 המוצרים" OR drop the raw count and say "הגבוה ביותר במדף" (the count adds nothing). Don't introduce a new number.

### F2 — UNGROUNDED manufacturer attribution (10 products) — the main fix
These rowVerdicts assert a manufacturer ("של טרה" / "של מחלבת המושבה" / "של מחלבת הנגב") that is NOT grounded in the product's own `brand` or `name` field. We have no manufacturer field beyond `brand`; asserting a different/specific producer is an ungrounded claim (fabrication-class — same rule as the granola "canola oil" incident). 
For EACH of these, read the product's `brand` + `name`, then rewrite the rowVerdict so it does NOT assert any manufacturer that isn't in those fields:
- bc-003 (brand שופרסל) — copy says "של טרה" → remove the producer claim (Shufersal is the retailer/private-label; do not name a producer).
- bc-010 (brand שופרסל) — "של טרה" → same.
- bc-025 (brand שופרסל) — "של טרה" → same.
- bc-027 (brand שופרסל) — "של טרה" → same.
- bc-041 (brand שופרסל) — "של טרה" → same.
- bc-014 (brand מחלבת רמת הגולן) — "של טרה" → wrong dairy; remove/replace with the actual brand if a manufacturer must be named, else drop it.
- bc-018 (brand מחלבות רמת הגולן) — "של טרה" → same.
- bc-024 (brand מחלבת רמת הגולן) — "של טרה" → same.
- bc-004 (brand מחלבות גד) — "של מחלבת המושבה" → wrong; remove or use the real brand (מחלבות גד).
- bc-005 (brand מחלבות גד) — "של מחלבת המושבה" → same.
The rewrite must keep the verdict's substance (the cheese's standing/quality) — only the false producer attribution goes. Natural Hebrew, insight-first. Do NOT invent a "real" manufacturer — if you can't ground it, don't name one.

### F3 — Ingredient-count contradiction (bc-038)
rowVerdict says "חמישה רכיבים" but the ingredient string is "חלב מפוסטר (פרה,כבשים,עיזים), מלח, מקריש" = 3 ingredients (milk/salt/rennet). Fix the count to match the displayed ingredients (3), or drop the count.

### F4 — Unverifiable interpretive claim (bc-035)
rowVerdict editorializes: "...לפי הבנת ברי, אחוז זה מתייחס לתמיסת המלח..." — Bari interpreting an ambiguous label as fact. Tighten: either state only what the label says (the value as fact) without asserting Bari's interpretation, or cut the interpretive sentence. Don't present an unverifiable reading as Bari's ruling.

### F5 — Undisclosed missing data (bc-031, bc-037, bc-048)
These have sugar=null (confidenceLabel "חסרים נתוני תזונה") but positiveSignals/verdict imply a complete picture. Add a short honest data-note (e.g. in limitingFactors or the verdict) that some nutrition data (sugar) is missing — don't make confident completeness claims on incomplete data.

### F6 — Fragile superlative (bc-007)
insightLine "החלבון הגבוה ביותר בקבוצת ה-A (21 גרם)" — but bc-002 has 20.5g, a 0.5g margin within label rounding. Soften "הגבוה ביותר" → "מהגבוהים" (among the highest).

## VERIFY BEFORE RETURNING (trace-derived, show commands)
- JSON parses.
- 0 score/grade/rank/nutrition fields changed (diff only copy fields: insightLine/rowVerdict/positiveSignals/limitingFactors/comparisonContext).
- 0 remaining "48", 0 ungrounded "של טרה"/"של מחלבת המושבה"/"של מחלבת הנגב" in the 10 products, count on bc-038 matches ingredients.
- Report before/after for F1, each F2 product, F3.

Do NOT close the task; this is a DRAFT pending the Adversarial-QA gate. End with the machine-readable return contract JSON (01_framework/operations/return_contract_v1.md).
