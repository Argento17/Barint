# TASK-461 Phase-2 #8 — protein_combined copy overhaul: author report

Author lane: Content Agent (C1 native, this session). DRAFT until Adversarial QA.
Date: 2026-07-02.

## 1. Isolation proof (zero git writes, origin/master baseline)

- Baseline obtained read-only: `git show origin/master:bari-web/src/data/comparisons/protein_combined_frontend_v2.json`
  → scratchpad `protein_origin.json`. **No file under C:\Bari was touched; no git write commands were run** (only `ls-tree` + `show`).
- origin blob sha (git ls-tree): `4127b58965bebb689016ba58388eda39b312f9d7`
- baseline sha256: `75967651a249a636f87b1adc2783475806661be1acd0f108fd8caf181378dd2b` (250,745 bytes)
- artifact sha256: `90ce9cd09a81ea8ca111d0b4dcc36eed24922e39b53733fb0537180e96114c80` (`protein_copy_overhaul.json`, 251,902 bytes)
- Field isolation (script `verify_overhaul.py`): `_meta` byte-identical; **32/32 products changed in exactly {insightLine, rowVerdict} and nothing else**; key-sets identical (no keys added — rowVerdict coverage was 32/32 in production, unlike hummus); scores/grades/ranks identical.
- Text-level unified diff: **-64/+64 lines, zero non-copy-field lines.** Line count unchanged (5,270).
- Serialization: `json.dumps(ensure_ascii=False, indent=2)`, no trailing newline — verified to round-trip the origin file byte-identically before use.

## 2. Metrics (script-derived, `verify_overhaul.py` / `rank_check.py`)

| metric | production (origin/master) | new copy |
|---|---|---|
| em/en dashes (both fields, 32 products) | **54** | **0** |
| products reciting panel numbers | **32/32** | **5/32** (all shelf extremes, list below) |
| engine-vocab hits (חיסרון/חציון/מדד/פרמטר/נקודות/רמת אמון/ציון/דירוג…) | 2 in copy fields (חיסרון ×2) + score-word ציון ×1 (pb-026) | **0** |
| antithesis-pattern hits (`, לא / ולא /אלא`) | **10** | **0** |
| opening-3-words duplicates (per field) | not measured | **0** (64/64 unique across both fields) |
| R4 purchase-verb hits (כדאי/שווה+לקנות/לבחור/לרכוש…) | — | **0** |
| 5-gram census (R3) | — | **max repetition = 2**, exactly one 5-gram at 2× (see §3) |
| empty fields | — | 0 |
| insightLine length | — | mean 74.2, stdev 9.3, min 55, max 98 |
| rowVerdict length | — | mean 186.0, stdev 28.2, min 148, max 261 |

Panel-number products (Rule 2 — number IS the story), 5/32 ≤ budget 5:
1. **pb-033** — 35 g sugar + 396 mg sodium: sole holder of BOTH shelf maxima (rank-checked #1/#1).
2. **pb-013** — 1.7 g sugar: shelf-minimum sugar achieved via three polyols; the number is the deception.
3. **pb-009** — 13 g saturated fat: shelf maximum (next is 11).
4. **pb-006** — 496 kcal: shelf-maximum energy density.
5. **pb-002** — 17 g sugar: the honest cost of the date-sweetened shelf leader (#5 of 32).

## 3. 5-gram self-census (house rule R3)

Zero 5-grams above 2×. Single 5-gram at exactly 2×: **"קזאין סויה חיטה ומי גבינה"** — the factual four-isolate-family composition shared by pb-024 and pb-026, the only two products on the shelf with a 4-family stack (trace-verified). Factual recitation at 2×, matching the precedent QA accepted on choc-tablets (shared ingredient-recitation 5-gram, factual, 2× only).

## 4. Rank-check table (every superlative/comparative claim, verified vs all 32 by `rank_check.py`)

| claim (product) | verification |
|---|---|
| pb-002 "השומן הרווי והנתרן שלו הם הנמוכים בקטגוריה כולה" | satFat 1.8 = #32/32 (min); sodium 29 = #32/32 (min; next 92) ✔ |
| pb-002 "17 גרם סוכר מהגבוהים במדף" | sugar #5/32 ✔ |
| pb-003 "יותר סיבים מכל מוצר אחר במדף" | fiber 19.0 = #1 (next 16.6) ✔ |
| pb-003 "כמות חלבון שרק אח אחד שלו משתווה אליה" | protein 36.0 tied #1 with pb-004, same brand (טודיי) ✔ |
| pb-003 "נתרן שרק שיאן המלח של הקטגוריה עוקף" | sodium 387 = #2, only pb-033 (396) above ✔ |
| pb-004 "נתרן צמוד לצמרת השלילית" | sodium 385 = #3/32 ✔ |
| pb-004 "סוכר… בחלק הגבוה של הקטגוריה" | sugar 16.0 = #7/32 ✔ |
| pb-005+pb-006 "יחד עם אחיו הוא עוקף בקלוריות ובשומן את כל שאר המדף" | kcal 489/496 = #2/#1 (next 465); fat 28.3/29.5 = #2/#1 (next 24) ✔ |
| pb-005 "גם המלח והסוכר שלו גבוהים" | sodium #4, sugar #4 ✔ |
| pb-006 "שיא האנרגיה… 496 קלוריות" / "אין מוצר צפוף יותר בקלוריות או בשומן" | kcal #1, fat #1 ✔ |
| pb-007 "הפיסטוק… כשני אחוזים וקצת" | parse: "פיסטוק 2.8%" ✔ |
| pb-007 "מלטיטול בשתי צורות" | parse: "מלטיטול, סירופ מלטיטול" ✔ |
| pb-007 "צבע מאכל על בסיס נחושת" | d4 E141 (תרכובות נחושת של כלורופיל) ✔ |
| pb-007 "השומן הרווי מהגבוהים בקטגוריה" | satFat 9.4 = #4/32 ✔ |
| pb-009 "13 גרם, יותר מכל מוצר אחר" incl. "ממתקי השוקולד של תחתית הטבלה" | satFat #1; Max-Brenner trio max = 11.0 ✔ |
| pb-009 "מלטיטול, אריתריטול וסוכרלוז" | parse tokens מלטיטול+אריתריטול visible; E955 in d4 ✔ |
| pb-010 "שלושה תחליפי סוכר… מלטיטול, סורביטול וסוכרלוז" | parse tokens מלטיטול+סורביטול visible; E955 in d4 ✔ |
| pb-010 "גליצרול כפול" | parse: גליצרול in caramel layer + standalone ✔ |
| pb-011 "מלטיטול גם בציפוי וגם בקרם" / "שישה תוספים מזוהים" | parse: maltitol in שוקולד 17% + ממרח קרמל 12%; d4 count = 6 ✔ |
| pb-011 "הנתרן מהנמוכים בקטגוריה" | sodium 92 = #30-31/32 ✔ |
| pb-012 "מסתכמים בקומץ קלוריות וגרם שומן" | deltas vs pb-011: kcal 5, fat 1.0, rest ≤1.0/0.7 ✔ |
| pb-013 "מספר הסוכר הנמוך בקטגוריה… 1.7" / "מלטיטול, סורביטול ואריתריטול" | sugar #32 (min); all three tokens visible in parse ✔ |
| pb-013 "שקדים קלויים בנתח מכובד" | parse: "שקדים קלויים (12%)" ✔ |
| pb-013 "תערובת החלבון… החוליה החלשה" | protein_quality dim 32.4 = shelf-lowest ✔ |
| pb-014 "הבדלים זעירים בלבד" | deltas vs pb-013: 3 kcal / 0.5 / 0.6 ✔ |
| pb-015 "רשימה מהקצרות במדף" / "תוסף מזוהה אחד" | d4 = 1 (E500), tied min (with pb-005/008/016) ✔ |
| pb-015 "שמן זית ושמן קוקוס" / fiber "מהדלים בקטגוריה" | parse tokens ✔; fiber 3.8 = #27/31 ✔ |
| pb-016 "הנתרן מטפס לחלק הגבוה" / "הסיבים… כמעט לתחתיתו" | sodium 300 = #7/32; fiber 3.0 = #28/31 (below only 2.3, 0, 0) ✔ |
| pb-008 "קלוריות ושומן רווי בחלק הגבוה" / "סיבים מהנמוכים שנרשמו" | kcal 435 #5, satFat 9.9 #3; fiber 2.3 = lowest nonzero ✔ |
| pb-017 family "משכפלת את עצמה שש פעמים" | pb-017..022 all טודיי, all 50.0, same 4-source blend + maltitol+sucralose+glycerol (traces identical) ✔ |
| pb-017 "הרשימה הקצרה יחסית בסדרה" / "הקלוריות… מהנמוכות בקטגוריה" | d4 6 vs siblings 7,7,8,8,8; family kcal 303–316 = shelf ranks #27–#32 ✔ |
| pb-018 "רק חמישה מוצרים במדף מלוחים ממנו" / "גבוה בבירור מכל אחיו" | sodium 352 = #6/32; family: 352 vs 272/160/160/100/100 ✔ |
| pb-020 "שיא החלבון של כל קבוצת התחליפים" | protein 34.8 = max of 24 maltitol carriers (#3 shelf) ✔ |
| pb-020 "שמונה תוספים מזוהים" + sulfite allergen | d4 = 8 incl. E224 ✔ |
| pb-021/022 "נתרן מהנמוכים במדף וקלוריות בתחתית שלו" | sodium 100 = #28-29/32; kcal 303 = tied last (#30-32) ✔ |
| pb-022 "ההבדל מהתאום מסתכם בגרם חלבון ובקצת סיבים" | deltas vs pb-021: protein 1.0, fiber 0.7, sugars 0.2 ✔ |
| pb-023 "מלטיטול רגיל, סירופ מלטיטול וסוכרלוז" / satFat "מהגבוהים" | parse tokens all visible; satFat 9.1 = #5-6/32 ✔ |
| pb-024 "ארבעה ממתיקים… מלטיטול, קסיליטול, סוכרלוז וסטיביה" | all four tokens visible in parse ✔ |
| pb-024 "סיבים מהגבוהים במדף כולו" / 4-family stack | fiber 16.4 = #3/32; trace families casein/soy/wheat/whey ✔ |
| pb-025 "שוקולד חלב ולבן, שניהם ממותקים במלטיטול" | parse: both coatings "עם ממתיק [מלטיטול]" ✔ |
| pb-025 "הנתרן מהגבוהים בקבוצת התחליפים" | sodium 291 = #3 of 24 maltitol carriers ✔ |
| pb-026 "ארבעה תחליפי מתיקות וארבע משפחות חלבון" | parse: מלטיטול+אריתריטול+קסיליטול+סוכרלוז visible; trace 4 families ✔ |
| pb-027 "הסיבים השניים בגובהם" / "רק חטיף אחד עוקף" | fiber 16.6 = #2 (below 19.0) ✔ |
| pb-028 "מוותר על הממתיק הסינתטי שמלווה את רוב אחיו במותג" | E955 in 7 of 9 all-in siblings; pb-028 has none (trace tierC=false, d4 E960 stevia) ✔ |
| pb-028 "הסיבים הגבוהים" | fiber 16.2 = #4/32 ✔ |
| pb-029 "תחליפי סוכר בשלוש רשומות" / satFat "בחלק הגבוה" | parse: מלטיטול, סירופ מלטיטול, סוכרלוז; satFat 8.9 = #9/32 ✔ |
| pb-030 "כמעט כל השומן הוא רווי, יחס שאין דומה לו" | satFat/fat = 0.827 = #1 by wide margin (next 0.645) ✔ |
| pb-031 "יותר מרבע חטיף של סוכר, עם אפס סיבים" | sugar 27 g/100 g = 27%; fiber 0.0 on panel ✔ |
| pb-032 "כמעט רבע מהמשקל שלו הוא שומן" / "הכבד בשומן הרווי" בשלישייה / "רק עוגייה אחת… עוקפת" / "הסוכר שלו שני בקטגוריה" | fat 23% ✔; trio satFat 9/11/9 ✔; shelf satFat #2 after pb-009 (cookie) ✔; sugar 31 = #2 ✔ |
| pb-033 "הכי הרבה סוכר והכי הרבה נתרן" / "שליש מהמוצר הוא סוכר" | sugar 35 #1, sodium 396 #1; 35% ≈ שליש ✔ |

Trace-grounded (non-numeric) claims: glycerol mentions only where trace `glycerol=true` (or parse token visible); maltitol claims only where trace `maltitol=true`; "בלי מלטיטול ובלי ממתיקים מלאכותיים" (pb-005/006/031) matches traces (all four sweetener signals false); collagen mentions only where trace `collagen_detected=true` + parse token.
Sweetener-count discipline (per dispatch spec): ingredient strings in the artifact are TRUNCATED (~330 chars, cut mid-word), so count claims ("ארבעה ממתיקים", "שלושה תחליפים") are used ONLY where all tokens are visible in the stored parse; elsewhere presence rests on trace signals + d4 and no counts are claimed. No sweetener numbers were reused from old copy.

## 5. Family map (rule once, differentiate by real deltas)

| family | members | ruling carrier | differentiators used |
|---|---|---|---|
| טודיי core line (six flavors, all 50.0) | pb-017, 018, 019, 020, 021, 022 | pb-017 (family definition: 4-source blend, maltitol+sucralose+glycerol, low kcal) | 018 sodium signature (#6 shelf, family max); 019 flavor-only + mild sodium; 020 protein max of all maltitol carriers + 8 additives + sulfite; 021 calmest panel (sodium/kcal lows) + ruled twin; 022 declared twin of 021 (deltas ≤1 g) |
| טודיי upper pair | pb-003, pb-004 | pb-003 (fiber #1 + sodium #2 + protein tie-max) | pb-004 adds 3-family isolate stacking; sodium #3 |
| all in "soft/cookie" 50-band | pb-023…pb-029 (7 incl. D-grade 029) | maltitol-swap system ruled at pb-007 (shelf-level) | 023 double-maltitol + satFat; 024 four sweeteners + 4-family stack + fiber #3; 025 dual maltitol chocolate coatings + sodium; 026 4+4 (sweeteners/families); 027 fiber #2; 028 no-sucralose outlier (7/9 siblings carry it); 029 accumulation verdict (opens the D band) |
| all in cookie twins | pb-015, pb-016 | pb-015 (short list, 1 additive, olive+coconut) | pb-016: sodium +21 mg (#7 shelf), fiber to near-bottom |
| WIN twins + sibling | pb-013, pb-014 (identical name, 2 barcodes), pb-008 | pb-013 (sugar-min illusion, 3 polyols, collagen+egg) | pb-014 declared duplicate listing ("שתי אריזות של כמעט אותו מוצר"); pb-008: no glycerol, kcal/satFat high, fiber min-positive |
| פרוטאין brand | pb-011, pb-012 (twins), pb-030 | pb-011 (collagen padding + double maltitol + 6 additives) | pb-012 format twin (kcal/fat deltas only); pb-030 saturated-fat-ratio shelf outlier (0.83) |
| נייטשר וואלי twins | pb-005, pb-006 | pb-005 (real peanuts, cleanest sweetening, heaviest load) | pb-006 kcal shelf max 496 (number carrier) |
| פרו שטראוס | pb-009, pb-010 | none needed (different stories) | 009 satFat #1; 010 three-sweetener pile-up |
| מקס ברנר trio (45/D) | pb-031, 032, 033 | pb-031 (real-sugar dessert identity, "בכנות של ממתק") | 031 Dubai trend + 0 fiber; 032 fat/satFat role (#2 shelf satFat); 033 double shelf-max (numbers carrier) |
| פנגיאה | pb-002 | sole B; real-food story + honest catches | — |

Tie discipline: 55-band (4 products), 54-band (7), 50-band (12), 49.8/49.7, and the 45-trio are treated as ties; no cross-product superiority claims inside any sub-2pt band; differentiation is panel-fact-only, never score-implying. Grades never referenced (also because of the pb-029/030 grade-field inconsistency, §7).

## 6. Before/after ×5

**pb-026 — the worst engine-vocab leak specimen on the shelf (חיסרון + ציון + em dashes + antithesis):**
- OLD RV: "8.8 גרם סיבים ל-100 גרם זה היתרון שלו — ארבע משפחות חלבון מבודד זה החיסרון שלו. ב-All In בוטנים קרמל, כל השכבות עשויות הנדסה: קזאין, סויה, חיטה, מי גבינה — ועליהן מלטיטול, ממתיק מלאכותי וגליצרול. הבוטנים לא מסבירים את הציון; ארבע המשפחות המבודדות כן."
- NEW IL: "בוטנים קרמל של אול אין משלים רביעייה כפולה: ארבעה תחליפי מתיקות וארבע משפחות חלבון."
- NEW RV: "הצפיפות כאן שיטתית: מלטיטול, אריתריטול, קסיליטול וסוכרלוז מצד המתיקות; קזאין, סויה, חיטה ומי גבינה מצד החלבון. הסיבים מכובדים ומרככים מעט את התמונה."
  (Also kills the old copy's implied peanut-content claim — peanuts are not visible in the stored parse.)

**pb-002 — shelf leader, number recitation → opinion:**
- OLD IL: "חלבון מאגוזי לוז אמיתיים — אבל גליצרול ברשימה מסגיר חטיף מהונדס במפעל."
- NEW IL: "המוביל של המדף בנוי מחומרים שאפשר לדמיין במטבח: אגוזי לוז טחונים, תמרים וחלבון אפונה."
- NEW RV: "הפסגה כאן שייכת לחטיף שהכי מתרחק מהמעבדה: אגוזים ותמרים עושים את העבודה, והשומן הרווי והנתרן שלו הם הנמוכים בקטגוריה כולה. ההסתייגות מגיעה ישר מהתמרים, 17 גרם סוכר מהגבוהים במדף, והגליצרול עם חומר משמר מזכירים שגם אותו הרכיבו במפעל."
  (Old IL also misattributed the protein to hazelnuts; the parse shows pea protein as the protein source, hazelnuts as bulk.)

**pb-013 — min-sugar illusion, template → finding:**
- OLD IL: "סוכר 1.7 גרם — הנמוך במדף, אבל זה כמעט כולו מלטיטול שהחליף סוכר."
- NEW IL: "מספר הסוכר הנמוך בקטגוריה נרשם כאן, 1.7 גרם, ושלושה תחליפים מייצרים את המתיקות בפועל."
- NEW RV: "ההישג שעל האריזה נבנה במעבדה: מלטיטול, סורביטול ואריתריטול ממלאים את מקום הסוכר שירד. יש גם צד חיובי של ממש, שקדים קלויים בנתח מכובד וסיבים יפים; תערובת החלבון, שנשענת על קולגן וביצה, היא החוליה החלשה."

**pb-017 — the six-flavor family stamp → family ruling:**
- OLD IL: "כל מאפייני ההנדסה במקום אחד: מלטיטול, ממתיק מלאכותי, וחלבון מכמה מקורות מבודדים."
- NEW IL: "כאן מתחילה שורת ששת הטעמים של טודיי: שלד אחד, מלטיטול, סוכרלוז וארבעה מקורות חלבון."
- NEW RV: "המשפחה הזאת משכפלת את עצמה שש פעמים במדף, עם אותה תערובת של חלבון חלב, חיטה מפורקת, סויה ומי גבינה, ואותם תחליפי מתיקות. גרסת קרם העוגיות מחזיקה את הרשימה הקצרה יחסית בסדרה, והקלוריות, כמו אצל כל האחים, מהנמוכות בקטגוריה. ההיגיון זהה בכולם; ההבדלים חיים בפרטים."

**pb-033 — double shelf-max, recitation → verdict:**
- OLD RV: "מחזיק לבדו את שני השיאים השליליים של המדף: 35 גרם סוכר ו-396 מ\"ג נתרן ל-100 גרם — צירוף מתוק-מלוח שמסביר את עצמו. קרמל מלוח עם טענת חלבון מעליו."
- NEW IL: "השיאן הכפול של הקטגוריה: הכי הרבה סוכר והכי הרבה נתרן, באותו חטיף."
- NEW RV: "35 גרם סוכר ו-396 מ\"ג נתרן בכל מאה גרם, שני שיאי המדף מתאחדים בקרמל המלוח הזה. שליש מהמוצר הוא סוכר פשוט, והחלבון שמודפס על החזית חי בתוך ממתק גמור."

## 7. Truth defects fixed + data flags (routed, not fixed here — out of 2-field scope)

Live-copy truth defects fixed by this pass:
1. **pb-002 protein misattribution** — production IL claims "חלבון מאגוזי לוז אמיתיים"; the stored parse shows the protein source is חלבון אפונה (pea), with hazelnuts as the bulk ingredient. New copy attributes correctly.
2. **pb-026 implied peanut content** — production RV argues "הבוטנים לא מסבירים את הציון" implying peanut content; no peanut token exists in the stored parse (name-flavor only). New copy makes no peanut-content claim.
3. **pb-026/pb-014 engine-vocab + score-word leaks** (חיסרון ×2, ציון ×1) — killed shelf-wide.

Data-agent flags (pre-existing, untouched by this lane):
- **pb-029 + pb-030 grade-field vs trace contradiction**: `_scoring_trace.grade_proportionality_applied` records old D → new C (TASK-365 <1.0pt rule), but the displayed `grade` field remains "D" on both. Either the trace note or the displayed grade is stale. Copy stays grade-silent.
- **pb-002 ingredient percentages sum >100** (pea 33% + hazelnuts 51% + cocoa 8.4% + dates + syrup) — parse suspect; copy avoids citing either percentage.
- **Ingredient strings truncated corpus-wide** (~330 chars, cut mid-word) — limits verifiability of list-tail claims; systemic artifact issue.
- **Parse corruption tokens**: pb-009 "nמייצב (-1412E)", pb-027 "מלטיט ול", pb-008 "חומר הלחה )ליצרול)", pb-013/14 "סיני תירם עלול לד מסיסים" — OCR-grade noise in stored ingredients.
- **Trace erythritol under-detection**: `key_signals.erythritol=false` on pb-009/013/014 although אריתריטול appears in their stored parses (no score impact asserted; signal-only observation).
- **pb-013/pb-014 duplicate listing**: identical name "WIN חטיף חלבון קרם קרמל", two barcodes (7290015130035/42), near-identical panels; copy rules them as one product in two packages.

## 8. QA hotspot suggestions (for the adversarial lane)

1. pb-018 "רק חמישה מוצרים במדף מלוחים ממנו" — exact-count claim; re-derive independently.
2. pb-020 "שיא החלבון של כל קבוצת התחליפים" — requires the 24-carrier maltitol set; re-derive from traces.
3. pb-030 saturated-ratio outlier claim ("יחס שאין דומה לו") — re-compute ratios.
4. pb-028 "רוב אחיו במותג" sucralose scoping — brand-set membership check (10 all-in products, 7 with E955).
5. pb-032 "רק עוגייה אחת במדף כולו עוקפת אותו" (satFat) — cross-format check (pb-009 is format=cookie).
6. The 5 number carriers vs Rule-2 justification.
7. Sweetener count claims (pb-010/013/024/026) vs truncated parses — confirm all counted tokens are visible in the stored strings.

## Return contract

```json
{
  "task_id": "TASK-461",
  "subtask": "phase2_protein_combined_copy_overhaul",
  "agent": "content-agent",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\af7acb6d-dc7c-4a64-90ca-b4509eea738a\\scratchpad\\protein_copy_overhaul.json",
      "sha256": "90ce9cd09a81ea8ca111d0b4dcc36eed24922e39b53733fb0537180e96114c80",
      "bytes": 251902
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\af7acb6d-dc7c-4a64-90ca-b4509eea738a\\scratchpad\\TASK-461_protein_author_report.md",
      "role": "author_report"
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\af7acb6d-dc7c-4a64-90ca-b4509eea738a\\scratchpad\\protein_origin.json",
      "sha256": "75967651a249a636f87b1adc2783475806661be1acd0f108fd8caf181378dd2b",
      "role": "baseline_origin_master",
      "git_blob": "4127b58965bebb689016ba58388eda39b312f9d7"
    }
  ],
  "isolation": {
    "baseline": "origin/master via git show (read-only)",
    "git_writes": 0,
    "repo_files_touched": 0,
    "fields_changed": ["insightLine", "rowVerdict"],
    "products_changed": "32/32",
    "keys_added": 0,
    "meta_identical": true,
    "scores_grades_ranks_identical": true,
    "text_diff_lines": "-64/+64, 0 non-copy-field"
  },
  "metrics": {
    "em_dashes": {"before": 54, "after": 0},
    "panel_number_products": {"before": "32/32", "after": "5/32"},
    "number_products_list": ["pb-002", "pb-006", "pb-009", "pb-013", "pb-033"],
    "engine_vocab_hits": {"before_copy_fields": 3, "after": 0},
    "antithesis_hits": {"before": 10, "after": 0},
    "opening_3word_unique": "64/64 (both fields)",
    "r4_purchase_verbs": 0,
    "five_gram_census": {"max_repetition": 2, "at_2x": 1, "at_2x_gram": "קזאין סויה חיטה ומי גבינה (factual 4-family stack, pb-024+pb-026)"},
    "length_distributions": {
      "insightLine": {"mean": 74.2, "stdev": 9.3, "min": 55, "max": 98},
      "rowVerdict": {"mean": 186.0, "stdev": 28.2, "min": 148, "max": 261}
    },
    "rank_checked_claims": 45,
    "rank_check_failures": 0
  },
  "truth_defects_fixed_live": [
    "pb-002 insightLine misattributes protein to hazelnuts; parse shows pea protein",
    "pb-026 rowVerdict implies peanut content absent from stored parse",
    "engine-vocab/score-word leaks (חיסרון x2, ציון x1) killed"
  ],
  "data_flags": [
    "pb-029/pb-030 displayed grade D contradicts trace grade_proportionality_applied D->C (TASK-365 rule)",
    "pb-002 ingredient percentages sum >100 (33% pea + 51% hazelnut + 8.4% cocoa + more)",
    "ingredient strings truncated corpus-wide (~330 chars)",
    "parse corruption tokens pb-008/009/013/014/027",
    "trace erythritol=false while parse lists erythritol (pb-009/013/014)",
    "pb-013/pb-014 duplicate product listing (same name, 2 barcodes)"
  ],
  "engine_caveat_respected": "TASK-457 de-anchor HOLD: no reference to pending re-scores or grade movement; artifact scores treated as live truth",
  "constraints": {
    "subagents_spawned": 0,
    "off_sources_used": 0
  },
  "next_gate": "Adversarial QA (independent lane) — DRAFT until sign-off"
}
```


---

## 9. QA fix RT-1 (post-gate, 2026-07-02) — SUPERSEDES §1 artifact hash and the §Return-contract above

Adversarial QA verdict: **GO_WITH_FIXES (0 CRITICAL / 0 HIGH / 3 MEDIUM)**. M2 (pb-009 "אינו מתקרב" warm-but-true) and M3 (pb-021 "מולחם" cosmetic) ruled monitor-only. **RT-1 required rework:**

- Finding: pb-005 rowVerdict claimed a sole cleanliness title ("משחק הכי נקי בקטגוריה במחלקת ההמתקה") — QA verified it is a TIE on the no-substitutes axis (pb-002 date-sweetened + Max Brenner trio equally substitute-free).
- Fix: sole superlative → membership framing: "**נמנה עם הנקיים בקטגוריה** במחלקת ההמתקה: סוכר רגיל, בלי מלטיטול ובלי ממתיקים מלאכותיים…" (rest of the verdict unchanged; the real insight — plain sugar, no substitutes — retained).
- Truth basis: substitute-free set (trace maltitol=false AND sweetener_tier_c=false) = 8/32: pb-002, pb-003, pb-004, pb-005, pb-006, pb-031, pb-032, pb-033 → membership claim literally true.
- pb-006 consistency check: "אותו ויתור מבורך על תחליפי סוכר" is a shared-trait reference, no sole superlative → **left untouched** (per fix scope rules; logged).

Artifact continuity:
- pre-fix preserved: `protein_overhaul_v1_preQA.json`, sha256 `90ce9cd09a81ea8ca111d0b4dcc36eed24922e39b53733fb0537180e96114c80` (byte-identical to the QA-gated version).
- fixed artifact: `protein_copy_overhaul.json`, sha256 `962624c7d9a34ea4a182602bcdd451328217df1f31bd32d3320310c19a5aaf1b` (251,906 bytes).
- diff pre-fix → fixed: exactly `{pb-005: rowVerdict}` (script-verified).
- Full verification suite re-run on the fixed artifact: isolation vs origin/master 32/32 clean (copy fields only, -64/+64 text lines, 0 non-copy), em 0, banned vocab 0, antithesis 0, openings 64/64 unique, digits 5/32 (unchanged set), R4 0, 5-gram max = 2 (same single factual gram), serialization round-trip stable.

### Return contract (superseding)

```json
{
  "task_id": "TASK-461",
  "subtask": "phase2_protein_combined_copy_overhaul_qa_fix_rt1",
  "agent": "content-agent",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "C:\Users\HP\AppData\Local\Temp\claude\c--Bari\af7acb6d-dc7c-4a64-90ca-b4509eea738a\scratchpad\protein_copy_overhaul.json", "sha256": "962624c7d9a34ea4a182602bcdd451328217df1f31bd32d3320310c19a5aaf1b", "bytes": 251906, "role": "final_fixed_artifact"},
    {"path": "C:\Users\HP\AppData\Local\Temp\claude\c--Bari\af7acb6d-dc7c-4a64-90ca-b4509eea738a\scratchpad\protein_overhaul_v1_preQA.json", "sha256": "90ce9cd09a81ea8ca111d0b4dcc36eed24922e39b53733fb0537180e96114c80", "role": "pre_fix_qa_gated_version"},
    {"path": "C:\Users\HP\AppData\Local\Temp\claude\c--Bari\af7acb6d-dc7c-4a64-90ca-b4509eea738a\scratchpad\TASK-461_protein_author_report.md", "role": "author_report_with_fix_section"}
  ],
  "fix_scope": {"products_touched": ["pb-005"], "fields_touched": ["rowVerdict"], "pb_006_touched": false, "pb_006_reason": "shared-trait wording, no sole superlative"},
  "verification": {
    "diff_vs_prefix": "exactly {pb-005: rowVerdict}",
    "isolation_vs_origin": "32/32 copy-fields-only, meta/scores/grades/ranks identical, -64/+64 text lines 0 non-copy",
    "em_dashes": 0, "banned_vocab": 0, "antithesis": 0,
    "openings_unique": "64/64", "digit_products": "5/32 (unchanged set)",
    "r4_hits": 0, "five_gram_max": 2
  },
  "constraints": {"git_writes": 0, "repo_files_touched": 0, "subagents_spawned": 0},
  "next_step": "handover package (sibling git lane) — RT-1 closed, M2/M3 monitor-only"
}
```
