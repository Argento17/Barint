# P217 — TASK-330 G6 sodium-causal word-boundary fix red-team (route: C3)
# ChatGPT challenge — advice only, never closes, never builds

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-330.md`
**Gate file:** `03_operations/page_generator/gates/run_gates.py:106`

## The bug
G6 copy-safety flags "sodium causal framing" with:
`SODIUM_CAUSAL_PATTERN = re.compile(r"(?:כי|בגלל|בשל).{0,30}נתרן")`
It is FALSE-POSITIVE firing on correct copy: `סיבים נמוכים הם הגורם המגביל. נתרן: 390 מ"ג` — the `כי`
substring inside `נמוכים` ("low") matches the conjunction alternative, then `נתרן` falls within 30 chars.
Sodium here is a standalone FACT across a sentence boundary, not causally framed. Same Hebrew
substring-collision class as EV-051 (`שמר` matching inside `משמרים`).

## Proposed fix (evaluate this)
Add a Hebrew word-boundary so the causal conjunctions only match as standalone words:
`re.compile(r"(?<![א-ת])(?:כי|בגלל|בשל)(?![א-ת]).{0,30}נתרן")`

## What we need from you (challenge, do NOT build)
1. **Does the word-boundary fix still catch GENUINE sodium-causal framing?** e.g. `יורד ל-D בגלל הנתרן הגבוה`,
   `עוצר ב-C כי הנתרן`, `נמוך בזכות הנתרן`. Confirm each still trips (or identify any real causal form it would
   now MISS).
2. **Does it over-relax?** Any string it would now wrongly PASS that is truly causal?
3. **Is `(?<![א-ת])...(?![א-ת])` the right boundary**, or is a trailing boundary on `כי` too strict / unnecessary
   (e.g. `כי` is always space-separated when used as "because")?
4. **Any other substring-collision risk** in the same pattern (e.g. `בשל` inside `בישול`/`מבושל` = "cooked"!,
   `בגלל`) we should guard while here? Note: `מבושל` (cooked) contains `בשל` — does the proposed boundary fix
   that too?

## Boundaries
- Advice only; do not edit files, do not propose closures. OFF-ban absolute.

## Return
Prose verdict per question 1–4 with concrete example strings, then the return-contract JSON
(`01_framework/operations/return_contract_v1.md`). Do not close — consult only.
