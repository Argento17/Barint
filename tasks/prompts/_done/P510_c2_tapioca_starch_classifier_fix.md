# P510 / RT-2H1 modified-starch classifier fix — mechanical implementation (route: C2)

Both co-signs are GRANTED (`02_products/yogurt_system/bsip2_task515_v3/TAPIOCA_STARCH_FIX_COSIGN.md`
has the full record — read it first). This is a fully-specified mechanical patch: apply exactly the
rule below, run exactly the tests below, report exact numbers. Do not use judgment beyond what's
specified — if you hit an ambiguous case not covered by the rule, STOP and report it rather than
deciding.

## File to edit
`03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py`, function `resolve_structural()`
(currently lines ~283-338 for the `_STRUCT_INDEX` synonym table, ~366-382 for the match loop).

## The rule (exact)
Currently these 3 synonym tuples exist (approximate current text, confirm exact current lines
before editing):
```python
(("עמילן עמילני", "עמילן טבעי", "עמילן לא מעובד", "עמילן אורז", "עמילן תירס", "עמילן"),
 "native_starch", FRACTIONAL),
(("עמילן מעובד", "עמילן שעבר עיבוד", "עמילן מותמר"),
 "modified_starch", RECONSTRUCTED),
```

**Replace the plain-substring match for the 3 modified-starch synonyms** (`עמילן מעובד`,
`עמילן שעבר עיבוד`, `עמילן מותמר`) with a source-word-tolerant regex check that:
1. Matches `עמילן` followed by 1-2 intervening words (a source qualifier like טפיוקה/תירס/תפוחי
   אדמה/אורז) followed by `מעובד` / `שעבר עיבוד` / `מותמר` — e.g.
   `r"עמילן(?:\s+\S+){1,2}\s+(מעובד|שעבר\s+עיבוד|מותמר)"`.
2. **MUST NOT cross a comma or other clause-boundary punctuation** between עמילן and the
   מעובד/שעבר-עיבוד/מותמר token. If a comma sits anywhere between עמילן and the modifier word, the
   match must NOT fire. (Implementation options: replace `\S+` with a character class that excludes
   `,` and other clause punctuation, e.g. `[^\s,()]+`, OR pre-split the ingredient string into
   comma-delimited clauses and only match within a single clause — pick whichever is simpler given
   the existing code structure, but the comma-boundary behavior is a hard requirement, not optional.)
3. **MUST NOT fire when `לא` (not) appears anywhere between עמילן and the מעובד/שעבר-עיבוד/מותמר
   token** — i.e. the negative form ("עמילן טפיוקה לא מעובד", "עמילן תירס (לא מעובד)") must continue
   to resolve `native_starch`, never `modified_starch`. This applies regardless of where לא sits
   relative to the source word (it can be immediately before מעובד, or wrapped in parens).
4. Keep the existing plain "עמילן מעובד" / "עמילן שעבר עיבוד" / "עמילן מותמר" contiguous matches
   working exactly as before (this is a superset extension, not a replacement of existing behavior).
5. `native_starch` synonyms (line ~286-287) are UNCHANGED — do not touch that tuple.

## Required regression tests (write + run, all must pass)
```python
test_cases = [
    # (ingredient_string, expected_identifier)
    ("עמילן מעובד", "modified_starch"),                          # existing, must still work
    ("עמילן טפיוקה מעובד (E-1442)", "modified_starch"),           # THE FIX — currently broken
    ("עמילן תירס (לא מעובד)", "native_starch"),                   # negative case — real corpus string, must NOT flip
    ("עמילן טבעי", "native_starch"),                              # existing native, unaffected
    ("עמילן תירס, חומר אחר מעובד", "native_starch"),               # comma-boundary guard — must NOT cross the comma
    ("עמילן שעבר עיבוד", "modified_starch"),                      # existing synonym #2, must still work
    ("עמילן תפוחי אדמה מותמר", "modified_starch"),                # synonym #3 w/ source qualifier — the fix's 2nd target
]
```
Report pass/fail on every one of these 7 cases individually. If any fails, do not proceed — report
the failure and stop.

## Cross-corpus baseline diff (after the code change, before declaring done)
Run the change against the FULL live corpus (every category under `02_products/` that backs a live
`bari-web/src/data/comparisons/*.json` page) and produce a before/after `tax_modified_starch` /
`resolve_structural` diff. Expected: **exactly 27 products flip** from `native_starch`/undetected to
`modified_starch`, matching this known list:
- yogurt_drinkable (3): 7290110573737, 7290110552244, 7290107938396
- yogurt_spoonable (13): [full list not repeated here — cross-check against the blast-radius scan
  artifact from dispatch a2e82720 if available in your context; otherwise report your own count and
  flag if it differs from 13]
- hummus (3), cakes_hard_cookies (7), crackers (1)

**If your diff produces a different total than 27, or flips any product NOT in scope, STOP and report
the discrepancy — do not silently accept a different number.** Report the full before/after list.

## Guards (hard)
- Only edit `ingredient_taxonomy.py`. Do NOT touch `score_engine.py`, `signal_extractor.py`,
  `constants.py`, any frontend JSON, or any copy field.
- OFF ban: not applicable to this file, but do not introduce any OFF reference anywhere.
- Do NOT re-score or regenerate any frontend page. This ticket is the classifier fix + verification
  only. Re-scoring the yogurt pages and re-authoring copy is a SEPARATE follow-up dispatch.
- Do NOT commit.

## Return
Exact diff of `ingredient_taxonomy.py` (the new regex/logic). Pass/fail on all 7 required test cases
(all must PASS). The cross-corpus before/after flip list + total count (expect 27; flag any
deviation). Confirm no other file touched. Then the machine-readable return contract per
`01_framework/operations/return_contract_v1.md`.
