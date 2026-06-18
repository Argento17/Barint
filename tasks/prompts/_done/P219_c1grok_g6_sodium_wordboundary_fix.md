# P219 — TASK-330 G6 sodium-causal word-boundary gate fix (route: C1-GROK)
# Data Agent build — conformance-gate regex precision fix, C3-reviewed

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-330.md`
**ONLY file you may edit:** `03_operations/page_generator/gates/run_gates.py`

## Change (C3-reviewed — P217)
At line ~106, replace:
```python
SODIUM_CAUSAL_PATTERN = re.compile(
    r"(?:כי|בגלל|בשל).{0,30}נתרן",
```
with the prefix-aware, word-boundary form:
```python
SODIUM_CAUSAL_PATTERN = re.compile(
    r"(?<![א-ת])(?:[וש])?(?:כי|בגלל|בשל)(?![א-ת]).{0,30}נתרן",
```
Keep any existing flags (re.UNICODE etc.). Add a one-line comment: "word-boundary guard (P217/C3) — stop
`כי` matching inside `נמוכים` / `בשל` inside `מבשל` (EV-051 substring-collision class); optional ו/ש prefix
preserves real causal forms `ובגלל`/`שבגלל`."

## Why this exact form (do not simplify to a bare `(?<![א-ת])`)
C3 (P217) proved a bare left-boundary would REGRESS real detection: `ובגלל הנתרן` / `שבגלל הנתרן` (vav/shin
prefix) would wrongly PASS. The optional `(?:[וש])?` preserves them while still blocking the in-word collision.

## Hard guards
- ONLY run_gates.py. Do NOT touch scoring, configs, copy, or any page JSON. No score movement. OFF-ban absolute.

## Acceptance test — REGRESSION (this is a gate; prove BOTH directions). Put results in self_check.
Write a tiny check (inline `python -c`) importing `SODIUM_CAUSAL_PATTERN` from run_gates and asserting:
- **MUST STILL MATCH (true causal — gate must keep catching these):**
  `יורד ל-D בגלל הנתרן הגבוה` · `עוצר ב-C כי הנתרן גבוה` · `ירד ל-D ובגלל הנתרן` · `מוגבל שבגלל הנתרן` ·
  `נחתך בשל הנתרן`
- **MUST NOT MATCH (false positives we are fixing):**
  `סיבים נמוכים הם הגורם המגביל. נתרן: 390 מ"ג` · `גריסי תירס מבושל עם 240 מ"ג נתרן` · `מבשל ... נתרן`
Show the pass/fail for each of the 8 strings (expect 5 match, 3 no-match).

Then re-run the spine and confirm the 2 cereals false-positives clear:
`python 03_operations/page_generator/spine_flip.py --set BARI_PALM_HYDRO_V1=on --note "TASK-330 gate fix verify"`
- cereals G6: `grep -E "FAIL: barcode" cereals report` → expect **0** (7296073642046 + 7296073642022 cleared).
- Confirm hummus G6 still 0 fails, G1 PASS both shelves, score_moves=0, frozen breach none.
- `git diff --stat` touches ONLY run_gates.py.

## Return
RETURNED proposal + return-contract JSON (`01_framework/operations/return_contract_v1.md`).
**Do not close. Do not commit or push.**
