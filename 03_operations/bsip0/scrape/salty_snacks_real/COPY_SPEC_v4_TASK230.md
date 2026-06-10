# Salty-snacks v4 — Copy generation spec (TASK-230 → implement in TASK-231)

Author: Content Agent. Status: RETURNED with deliverable (not closed).
Target build script: `03_build_frontend_v4.py`. Target data: `salty_snacks_frontend_v4.json` (47 products).
Gate: every consumer string MUST pass `hebrew_readability.is_clean` (offline, `C:\Bari\integrations\clients\`).

This spec replaces the copy functions `limiting_signals()`, `build_insight()`, `bottom_line()`,
and the confidence-label/positive-signal wording. The Data Agent applies these rules in the build
script; no string in this file leaks framework vocabulary or prescribes a purchase.

---

## 0. What was wrong (audit result, grounded in the shipped data)

| # | Defect | Instances | Evidence |
|---|--------|-----------|----------|
| 1 | **Framework leakage** — `limitingFactors` renders `"מוצר אולטרה-מעובד (NOVA 4)"` verbatim | **8 products** | The string is emitted whenever a cap *rule name* contains "NOVA", regardless of the product's real `novaGroup`. **5 of the 8 are novaGroup 3, not 4** — so the label is both banned vocabulary AND factually wrong (e.g. `9322969000022` פריכיות תירס, novaGroup=3, shows "(NOVA 4)"). |
| 2 | **Recommendation language** — `bottomLine` ends `"…עדיף לבחור חטיף עם פרופיל נקי יותר"` | **14 products** (D+E) | Bari describes, never prescribes. `עדיף לבחור` is banned alongside מומלץ/כדאי. (Task said 13; actual count is 14.) |
| 3 | **Confusing confidence label** — `"מבוסס על נתוני תזונה בלבד"` | **34/47 products** | Reads as jargon; a shopper can't tell it means "the ingredient list wasn't on the product, so the score used the nutrition table only." |
| 4 | **Weak/formulaic descriptions** | most C/D/E rows | e.g. every C row: `"חטיף ממוצע למדף — לא בולט לטובה ולא נופל בבירור"` + a boilerplate line 2 `"הציון X/Y משקף את האיזון הכולל בין הרכיב לעיבוד"`. Template repetition, no product specificity. |

Leakage count for the return block: **8 framework-term instances** (all the "NOVA" string), **14 recommendation instances**.

---

## 1. Hard rules the generator must enforce (apply to EVERY emitted string)

1. **No framework vocabulary, ever.** Never emit: NOVA, BSIP, cap, floor, dimension, penalty, weight, processing-class names, score mechanics. The `novaGroup` field and any cap/penalty rule name are **internal** — they may drive *which template fires*, but their literal text must never appear in a consumer string.
2. **Never read a rule name into copy.** The old `limiting_signals()` bug copied the cap rule string. Drive the "highly processed" line off the real **`novaGroup` integer**, not the rule name (see §2).
3. **No prescriptions.** Never emit עדיף / מומלץ / כדאי / "בחרו" / "הימנעו" / "אל תקנו". Close descriptively (state what the product *is*), not with advice.
4. **One em-dash per paragraph, max.** Never use "—" as a list separator or connector. Prefer period + new sentence, or a colon. Insight line 1 and line 2 are separate paragraphs (split on `\n`), so each may hold at most one "—".
5. **Degrade gracefully on missing data.** If a numeric field is `None`, drop the clause that needs it — never print "None", "0", or invent a value. If the only available facts are missing, fall back to the neutral template (§3 C/average) — do not fabricate a finding.
6. **Numbers stay as plain consumer facts** ("312 מ\"ג נתרן ל-100 גרם"). Never print a `score/grade` mechanic inside a sentence as the *point* of the line; the numeric score is shown by the chip, not narrated.
7. **Run the gate.** After generation, the build script should assert `hebrew_readability.analyze(s).is_clean` for every consumer string and fail loudly on any leak.

---

## 2. The "highly processed" line — replaces the NOVA leak (defect 1)

**Delete** the `limiting_signals()` block that appends `"מוצר אולטרה-מעובד (NOVA 4)"`.

Replace with a processing descriptor driven by the **`novaGroup` integer** (not the rule name). Only
add a processing line when `novaGroup == 4` AND no nutrient line already carries the message. For
`novaGroup == 3` do **not** add a generic processing line — let the real nutrient drivers (sodium,
fat, sugar, saturated fat) speak; they already do on these products.

```python
def processing_line(nova_group, sig):
    # consumer language only; never the integer, never "NOVA"
    if nova_group == 4:
        return "מעובד מאוד, עם רשימת רכיבים ארוכה ורחוקה מהחומר הגלם."
    return None   # nova 2/3: nutrient drivers carry the limitingFactors, no generic processing label
```

- Cap `limitingFactors` at 3 entries; nutrient facts take priority over the processing line.
- This removes all 8 leaks and the 5 false "(NOVA 4)" labels on novaGroup-3 products in one move.

If the category insists on a processing note for nova-3 puffed/extruded snacks, use a **specific,
true** phrasing tied to the food, not a class label, e.g. `"תירס מנופח בתבלינים ושמן."` — but only
when the ingredient/text supports it. When unsure, omit. Never guess a class.

---

## 3. Insight line (collapsed-row verdict) — replaces `build_insight()` (defects 1,4)

Two short paragraphs joined by `\n`: **line 1 = the finding / where it stands; line 2 = the catch
or the character.** Finding-first, product-specific, no boilerplate line 2. Pick the line-1 template
by the product's strongest real signal, in priority order. All `{…}` are rounded plain numbers; drop
any clause whose source field is `None`.

### Line 1 — by strongest signal (first match wins)

| Priority | Condition | Line 1 template |
|---|---|---|
| P1 high-fiber/protein baked | `fiber >= 6` or `protein >= 9` | `אחד החטיפים הבודדים במדף עם {fiber} גרם סיבים{+ " ו-{protein} גרם חלבון" if protein>=9} ל-100 גרם.` |
| P2 clean/low-sodium | `sodium <= 120` | `מהפרופילים הנקיים במדף: רק {sodium} מ\"ג נתרן ל-100 גרם.` |
| P3 sweet-leaning | `sugar >= 15` | `חטיף מתוק שמתחזה למלוח: {sugar} גרם סוכר ל-100 גרם.` |
| P4 very salty | `sodium >= 600` | `חטיף מלוח מאוד: {sodium} מ\"ג נתרן ל-100 גרם.` |
| P5 fatty/extruded | `fat >= 28` | `חטיף עתיר שומן: {fat} גרם שומן ל-100 גרם, רובו מהטיגון והשמן.` |
| P6 top-of-shelf, no standout | `grade in (A,B)` | `נשאר בין הטובים במדף, גם בלי תכונה אחת שבולטת.` |
| P7 mid | `grade == C` | `פרופיל ממוצע: לא בולט לטובה אבל גם לא נופל.` |
| P8 weak | else (D/E) | `מהחלק התחתון של המדף, עם פרופיל תזונתי חלש.` |

### Line 2 — the catch / the character (never the boilerplate "משקף את האיזון")

Choose by what is *true and notable* about this product, first match wins. Each is one short
sentence. Never repeat a fact already stated in line 1.

| Condition | Line 2 |
|---|---|
| `sodium >= 600` (and not already said) | `שקית שלמה לבדה מכסה חלק ניכר מהנתרן היומי.` |
| `fat >= 28` (and not already said) | `רוב הקלוריות כאן מגיעות מהשומן.` |
| `saturated_fat >= 7` | `כולל {saturated_fat} גרם שומן רווי ל-100 גרם.` |
| `sugar >= 15` and line1 wasn't sweet | `הסוכר הוא הסיפור כאן, לא המליחות.` |
| `grade in (A,B)` and a positive was stated | `נשאר חטיף מעובד, אבל מהפרופילים הסבירים שתמצאו על המדף הזה.` |
| `grade == B` clean rice/popcorn | `הטעם דל בהתאם — זה המחיר של פרופיל נקי.` |
| fallback (C, nothing notable) | `נתרן וקלוריות במרכז הטווח של המדף, בלי יתרון תזונתי שמושך תשומת לב.` |

**Note on the "best ≠ excellent" frame (frozen invariant):** keep the framing that a top-of-shelf
salty snack is still a snack — but express it as *character*, not advice. Allowed:
`"נשאר חטיף מעובד"`. Forbidden: `"עדיף"` / `"מומלץ"` / a class label.

---

## 4. Bottom line — replaces `bottom_line()` (defects 2,4)

Descriptive close, no prescription. By grade band:

```python
def bottom_line(score, grade, sig):
    sod = sig.get("sodium_mg"); fib = sig.get("dietary_fiber_g")
    if grade in ("A", "B"):
        # frozen "best != excellent" framing, stated as fact not advice
        return "מהטובים שתמצאו על המדף הזה, וזה עדיין חטיף מעובד. \"הכי טוב\" כאן לא אומר \"מצוין\"."
    if grade == "C":
        return "חטיף סביר בלי יתרון תזונתי בולט. נמצא בדיוק במרכז המדף."
    # D / E — describe the weakness, do NOT prescribe an alternative
    return "מהחלשים במדף: פרופיל עתיר שומן, נתרן או סוכר, בלי צד מאזן."
```

- For D/E, if you want product-specificity, swap the generic tail for the **one** dominant driver
  that fired (highest of sodium≥600 / sugar≥15 / sat_fat≥7 / fat≥28), phrased as a fact. Still no
  "עדיף/מומלץ/כדאי".
- One em-dash max per string. The A/B string uses none; keep it that way.

---

## 5. Confidence label — replaces the jargon (defect 3)

Applies to the 34 panel-only products (`confidence == "partial"`, `source_traceability_status ==
"panel_only"`).

| Field | OLD (jargon) | NEW (shopper-legible) |
|---|---|---|
| `confidence_label_he` (partial) | `מבוסס על נתוני תזונה בלבד` | `דירוג לפי הטבלה התזונתית בלבד` |
| `confidence_tooltip_he` (partial) | `הציון מבוסס על לוח התזונה; רשימת הרכיבים אינה זמינה במקור.` | `רשימת הרכיבים לא הופיעה על המוצר, אז הדירוג נשען על הטבלה התזונתית בלבד — בלי ניתוח רשימת הרכיבים.` |
| `confidenceLabel` (expansion, partial) | `נתונים חלקיים` | `טבלה תזונתית בלבד` |
| `confidence_label_he` (verified) | `מבוסס על נתונים מלאים` | `דירוג לפי רכיבים וטבלה תזונתית` |
| `confidence_tooltip_he` (verified) | `הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים.` | `הדירוג נשען גם על רשימת הרכיבים וגם על הטבלה התזונתית.` |
| `confidenceLabel` (expansion, verified) | `נתונים מלאים` | `רכיבים + טבלה תזונתית` |

Rationale: "נתוני תזונה / לוח תזונה" reads as a code phrase. "הטבלה התזונתית" is the panel a shopper
sees on the back of the pack. The tooltip now *says why* — the ingredient list wasn't available — in
one sentence (one em-dash, allowed).

---

## 6. Positive signals — keep, lightly de-formulaic

The existing positive-signal lines are facts and pass the gate; keep them but vary the lead so 30+
rows don't read identically. Suggested forms (pick by signal, still plain facts):

- fiber: `{fiber} גרם סיבים ל-100 גרם` (keep)
- protein: `{protein} גרם חלבון ל-100 גרם` (keep)
- low sodium: `נתרן נמוך: {sodium} מ\"ג ל-100 גרם` (drop the em-dash form `נמוך יחסית —`)
- low sugar: `כמעט בלי סוכר` (keep)

---

## 7. Replacement templates by archetype (exact Hebrew, gate-passed)

Each block: insight line 1 \n line 2, then bottomLine. All verified `is_clean == True`,
`readability_score == 100.0`.

### A. High-fiber / protein baked snack (e.g. חטיפי קרקר פיטנס חיטה מלאה 67/B; פריכיות משולשות 77/B)
```
INSIGHT: אחד החטיפים הבודדים במדף עם 6.2 גרם סיבים ו-10 גרם חלבון ל-100 גרם.
         נשאר בין הטובים במדף, אבל זה עדיין חטיף: 11 גרם שומן ו-312 מ"ג נתרן ל-100 גרם.
BOTTOM:  מהטובים שתמצאו על המדף הזה, וזה עדיין חטיף מעובד. "הכי טוב" כאן לא אומר "מצוין".
```

### B. Plain rice cake / popcorn, clean profile (e.g. פריכונים מאורז מלא ללא תוספת מלח 76/B, נתרן 15)
```
INSIGHT: מהפרופילים הנקיים במדף: רק 15 מ"ג נתרן ו-2.8 גרם שומן ל-100 גרם.
         הטעם דל בהתאם — זה המחיר של פרופיל נקי.
BOTTOM:  מהטובים שתמצאו על המדף הזה, וזה עדיין חטיף מעובד. "הכי טוב" כאן לא אומר "מצוין".
```

### C. Extruded puff, fatty, NOVA-3/4 (e.g. במבה יום הולדת 65/C, שומן 30; was the false-"NOVA 4" case)
```
INSIGHT: חטיף עתיר שומן: 30 גרם שומן ל-100 גרם, רובו מהטיגון והשמן.
         17 גרם חלבון ל-100 גרם לא משנים את התמונה — רוב הקלוריות מהשומן.
BOTTOM:  חטיף סביר בלי יתרון תזונתי בולט. נמצא בדיוק במרכז המדף.
```
(For the *real* nova-4 case e.g. דוריטוס/ביסלי, line 2 may be the processing descriptor from §2:
`מעובד מאוד, עם רשימת רכיבים ארוכה ורחוקה מהחומר הגלם.`)

### D. Sweet-leaning snack (e.g. במבה במילוי קרם נוגט 32/E, סוכר 26; קליק כריות נוגט סוכר 48)
```
INSIGHT: חטיף מתוק שמתחזה למלוח: 26 גרם סוכר ל-100 גרם, יותר מחלק מהממתקים.
         הסוכר הוא הסיפור כאן, לא המליחות.
BOTTOM:  מהחלשים במדף: פרופיל עתיר שומן, נתרן או סוכר, בלי צד מאזן.
```

### E. Very salty pretzel/chip (e.g. בייגלה רשתות מלח 60/C, נתרן 850; צ'יפס+ 33/E נתרן 836)
```
INSIGHT: חטיף מלוח מאוד: 850 מ"ג נתרן ל-100 גרם.
         שקית שלמה לבדה מכסה חלק ניכר מהנתרן היומי.
BOTTOM:  חטיף סביר בלי יתרון תזונתי בולט. נמצא בדיוק במרכז המדף.
```

### F. Panel-only / partial-data product (any of the 34; copy must not imply ingredient knowledge)
Copy is identical in shape to the matching nutrient archetype above — it is driven entirely by the
nutrition table, which is present. The **only** difference is the confidence label/tooltip (§5).
Do **not** add any ingredient-derived claim (e.g. "רשימת רכיבים ארוכה") on a panel-only product,
because the ingredient list is unknown. The §2 nova-4 processing line is allowed only when
`novaGroup` is known from the trace (it is) AND no ingredient text is asserted.

### G. Mid / average, nothing notable (default C)
```
INSIGHT: פרופיל ממוצע: לא בולט לטובה אבל גם לא נופל.
         נתרן וקלוריות במרכז הטווח של המדף, בלי יתרון תזונתי שמושך תשומת לב.
BOTTOM:  חטיף סביר בלי יתרון תזונתי בולט. נמצא בדיוק במרכז המדף.
```

---

## 8. Products blocked on TASK-231 data fixes

Copy that needs these fields cannot be finalized until Data fixes the source. The build can still
emit gate-clean copy using the **graceful-degradation** rules (§1.5) in the meantime, but flag:

**Garbled / English ingredient text** (blocks any ingredient-derived line; keep these panel-only,
do NOT assert ingredient claims until fixed):
- `7290000068770` במבה יום הולדת — ingredients are scanner garbage (`םרי וייו ןוימיוc…`).
- `9322969000022` פריכיות תירס — English ingredient text (`Maize (89%)…`).
- `7290000069364` פריכונים מאורז מלא ללא תוספת מלח — English (`whole rice (99.9%)…`).
- `4014400925319` פופקורן בציפוי קרמל — English (`sugar, corn, glucose syrup…`).
- `7290112968807` פיטנס קרקר דק סלק — English (`whole wheat flour (31%)…`).
- `7290112494313` קליק קורנפלקס — partially garbled Hebrew (`9תות תירס (25)…`).
- `7290100850916` דוריטוס חמוץ חריף — minor: decimal comma `70,5%` (cosmetic, not blocking).

**Missing sodium** (blocks the salty/clean line-1 templates P2/P4 and the §3 catch lines; these
products fall back to grade-band templates until sodium is restored):
- `7290000066332` אפרופו 50 ג' — sodium = None (also a false "(NOVA 4)" label today; novaGroup=3).
- `7290106573314` חטיף קריספי אפוי כפרי — sodium = None.
- `7290116537375` קליק כריות נוגט — sodium = None (sweet-leaning; sugar 48 still drives line 1, OK).

**Not blocking** (graceful-degradation handles it): 20 products have `fiber = None` — the fiber
clause simply drops; no fabrication.

---

## 9. Acceptance check for TASK-231 implementation

After the build script applies §2–§6, run:
```python
# every consumer string must pass
for p in products:
    for s in [p["insightLine"], p["expansion"]["bottomLine"],
              p["confidence_label_he"], p["confidence_tooltip_he"],
              *p["expansion"]["positiveSignals"], *p["expansion"]["limitingFactors"]]:
        assert hebrew_readability.analyze(s).is_clean, s
```
Expected: 0 framework leaks, 0 recommendation terms, 0 "(NOVA 4)" strings, 0 false processing labels
on novaGroup-3 products. Confidence label reads as plain shopper Hebrew.
