# TASK-484 — Change Ledger

Page-narrative phrasing sweep: antithesis ("X, not Y") reword + em-dash minimization
across the 5 in-scope `*-comparison-page-data.ts` files and the milk JSON `page_copy`
block. All edits preserve meaning, numbers, and every non-narrative field. Scores,
rowVerdict/insightLine, and all product-level fields untouched.

Scope note: bread's and snacks' SEO `description` strings are NOT inline in their
page-data.ts files — they resolve from `bread-analysis-content.ts` /
`data/blog/snack-analysis.json`, which are outside the 6-file list given for this task.
Left untouched; flagging in case the sweep should extend there in a follow-up.

---

## 1. `bari-web/src/lib/comparisons/bread-comparison-page-data.ts`

| # | Field | Before | After | Decision |
|---|---|---|---|---|
| 1 | hero.title | "לחם: מה שכתוב על האריזה לא תמיד מה שבפנים" | "לחם: הציון קורא את מה שבאמת בפנים" | REWORD — antithesis about package-vs-contents; restated positively (what the score does) |
| 2 | prologue[2] | "...ותסיסה מאומתת ברשימת הרכיבים — לא על המיתוג." | "ההשוואה מתבססת על מה שאפשר לבדוק ברשימת הרכיבים עצמה: ערכי חלבון, סיבים, נתרן ותסיסה מאומתת." | REWORD — dropped "not on branding" antithesis; also removes 1 em-dash |
| 3 | categoryNote note 1 title+lead | "תסיסה ודגן מלא נקראים מהרשימה, לא מהמיתוג" / "...לפי מה שמופיע ברשימת הרכיבים — לא לפי הכותרת שעל החזית." | "תסיסה ודגן מלא נקראים מהרשימה" / "...לפי מה שמופיע ברשימת הרכיבים בפועל." | REWORD — both instances of the same antithesis flattened; em-dash dropped |
| 4 | methodologyLines[0] | "...מגלויות שופרסל — מדגם מדף, לא סקר שוק מלא." | "...מגלויות שופרסל: מדגם מדף ממוקד, בהיקף חנות בודדת." | REWORD — restates scope positively instead of "not a full market survey"; em-dash to colon |
| 5 | methodologyLines[2] | "ציון הלחם אינו מבוסס על קלוריות בלבד — הוא משקלל..." | "ציון הלחם משקלל מבנה, מקור הדגן ורמת ההנדסה במוצר, מעבר לקלוריות בלבד." | REWORD — flattened "isn't X — it's Y"; em-dash dropped |

**Kept as-is (with reason):**
- categoryNote note 2: "...אינה מבדילה בין מחמצת אמיתית ואיטית לבין אבקת מחמצת תעשייתית" — genuine parallel comparison of two real things (not a single-subject antithesis); factual limitation statement. KEEP.
- methodologyLines[3]: "...ולא מהווה המלצה תזונתית אישית" — standard site-wide disclaimer boilerplate (identical pattern used in every category page: "not personal nutritional/medical advice"). KEEP — legal/informational disclaimer, not product antithesis.
- Code comments with em-dashes (lines 23, 29, 60) — not consumer-facing narrative, out of scope.

Em-dash count: before 5 (narrative) → after 0 (narrative); 2 remain in code comments (untouched, non-narrative).

---

## 2. `bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts`

| # | Field | Before | After | Decision |
|---|---|---|---|---|
| 1 | hero.title | "חטיפי השוקולד האלה הם חטיפי ממתק, לא חטיפי ביניים — וכולם יודעים את זה" | "חטיפי השוקולד האלה הם חטיפי ממתק לכל דבר, וכולם יודעים את זה" | REWORD — the flagged example: dropped "not intermediate snacks" antithesis, positive declarative "candy bars, full stop"; em-dash dropped |
| 2 | prologueSentences[0] | "...עם 27 עד 60 גרם סוכר ל-100 גרם — וברוב המדף מעל 45." | "...עם 27 עד 60 גרם סוכר ל-100 גרם, וברוב המדף מעל 45." | Em-dash → comma only, no antithesis present |
| 3 | prologueSentences[1] | "ההבדלים ביניהם שוליים — קצת יותר אגוזים כאן, קצת פחות סוכר שם — אבל..." | "ההבדלים ביניהם שוליים, קצת יותר אגוזים כאן, קצת פחות סוכר שם, אבל..." | Em-dash → comma only |
| 4 | categoryNote[0] | "כל מוצר במדף הזה מקבל ציון E. זה לא מחמיר, זה מדויק: זו קטגוריה אחת..." | "כל מוצר במדף הזה מקבל ציון E. זהו ציון מדויק לקטגוריה אחת של ממתקים, וההשוואה היא בתוכה." | REWORD — dropped "isn't harsh, is accurate" antithesis; states positively that it's an accurate score |
| 5 | categoryNote[1] | "כשמוצר מדורג גבוה כאן, זה לא אומר שהוא טוב — זה אומר שהוא הכי פחות מהונדס:..." | "כשמוצר מדורג גבוה כאן, המשמעות היא שהוא הכי פחות מהונדס:..." | REWORD — dropped "doesn't mean X — means Y"; states meaning directly; em-dash dropped |
| 6 | methodologyLines[0] | "ניתחנו את חטיפי השוקולד במדף שופרסל — שמות, רכיבים..." | "ניתחנו את חטיפי השוקולד במדף שופרסל: שמות, רכיבים..." | Em-dash → colon |
| 7 | methodologyLines[2] | "...ואורך רשימת הרכיבים — לא על גודל החטיף." | "...ואורך רשימת הרכיבים, מעבר לגודל החטיף." | REWORD — "not bar size" antithesis flattened to positive "beyond X" |
| 8 | comparisonMetadata.description | "...מהמדף הישראלי — ציון Bari, כמות סוכר..." | "...מהמדף הישראלי: ציון Bari, כמות סוכר..." | Em-dash → colon |

**Kept as-is (with reason):**
- categoryNote[2]: **"אנחנו לא אומרים ולעולם לא נאמר לכם מה לאכול. אנחנו כן אומרים ש..."** — this is the explicit owner-voice signature rhythm named in the task brief verbatim. KEEP UNCHANGED — rewordemoving it would flatten the brand's authentic first-person rhetorical identity.
- prologueSentences[2]: "המילה 'חטיף' היא שיווק; ההבדל האמיתי היחיד הוא בין X...לבין Y" — genuine two-sided comparison between two named groups of products, not a single-subject antithesis. KEEP.
- comparisonMetadata.description closing "מידע, לא המלצה" — standard site-wide disclaimer boilerplate identical to chocolate-tablets. KEEP.

Em-dash count: before 6 (narrative) → after 0 (narrative); 1 remains in a code comment (line 25, untouched).

---

## 3. `bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts`

| # | Field | Before | After | Decision |
|---|---|---|---|---|
| 1 | hero.title | "שוקולד מריר לא הופך לבריא בגלל השם — הציון מפריד בין..." | "השם על טבלת השוקולד המריר מספר פחות מההרכב שבפנים; הציון קורא את הקקאו האמיתי מול הסוכר שלובש את השם" | REWORD (QA-revised) — original is an EPISTEMIC claim (don't trust the name/label); restored that framing positively ("the name tells you less than the composition inside; the score reads the real composition") WITHOUT reducing healthiness to a single cocoa:sugar ratio. Earlier "בריאות...נקבעת ביחס שבין קקאו לסוכר" overclaimed (methodology weighs cocoa%, sugar, fat type AND processing); reverted. Em-dash dropped; no antithesis |
| 2 | prologueSentences[0] | "שוקולד מריר לא הופך לבריא בגלל השם: גם טבלת 70%..." | "השם על טבלת השוקולד המריר מספר פחות מההרכב שבפנים: גם טבלת 70%..." | REWORD (QA-revised) — same epistemic-claim fix applied consistently to the repeated phrase; no single-ratio overclaim |
| 3 | categoryNote[0] | "...וגם שתי הטבלאות שמובילות את המדף לא מתחמקות מזה. ה-B הוא הצד הנכון של מדף הממתקים; לא מוצר בריאות." | "...וגם שתי הטבלאות שמובילות את המדף נושאות את זה במלואו. ה-B מסמן את הצד הטוב של מדף הממתקים, ולא שהמוצר הוא מוצר בריאות." | REWORD (QA-revised) — earlier reword weakened the health-halo guard to "עדיין בתוך משפחת הממתקים"; restored a STRONG explicit guard "...ולא שהמוצר הוא מוצר בריאות" in the approved "ולא ש…" misreading-guard form (same class as snacks item-10 and milk 'דל שומן' title). No "X, not Y" antithesis; no em-dash |
| 4 | categoryNote[1] | "...הציון מביא בחשבון את מורכבות הנוסחה הכוללת — היעדר הסוכר הוא רק חלק אחד ממנה." | "...הציון מביא בחשבון את מורכבות הנוסחה הכוללת, כשהיעדר הסוכר הוא רק חלק אחד ממנה." | Em-dash → comma, no antithesis present |
| 5 | categoryNote[2] | "שוקולד לבן הוא פרק בפני עצמו: אין בו מוצקי קקאו כלל — רק חמאת קקאו, חלב וסוכר." | "...אין בו מוצקי קקאו כלל, רק חמאת קקאו, חלב וסוכר." | Em-dash → comma |
| 6 | methodologyLines[0] | "ניתחנו את טבלאות השוקולד במדף שופרסל — שמות, רכיבים..." | "...במדף שופרסל: שמות, רכיבים..." | Em-dash → colon |
| 7 | methodologyLines[2] | "...וסוג השומן ורמת העיבוד — לא על כמות השוקולד בלבד." | "...וסוג השומן ורמת העיבוד, מעבר לכמות השוקולד בלבד." | REWORD — "not chocolate quantity alone" antithesis flattened |
| 8 | prologueSentences[2] | "הסתכלו על שניים ביחד — אחוז הקקאו וכמות הסוכר — ותדעו..." | "הסתכלו על שניים ביחד, אחוז הקקאו וכמות הסוכר, ותדעו..." | Em-dash → comma (×2) |
| 9 | comparisonMetadata.description | "...מהמדף הישראלי — ציון Bari, אחוז קקאו..." | "...מהמדף הישראלי: ציון Bari, אחוז קקאו..." | Em-dash → colon |

**Kept as-is (with reason):**
- categoryNote[2] closing sentence, "שוקולד לבן...רק חמאת קקאו" retains an implicit "no cocoa solids, only X" — this is a factual composition statement (what white chocolate actually contains), not antithesis of two competing claims. KEEP the "אין...כלל" phrasing (fact, not rhetorical negation).
- comparisonMetadata.description closing "מידע, לא המלצה" — standard disclaimer boilerplate. KEEP.

Em-dash count: before 8 (narrative) → after 0 (narrative); 1 remains in a code comment (line 25, untouched).

---

## 4. `bari-web/src/lib/comparisons/hummus-comparison-page-data.ts`

| # | Field | Before | After | Decision |
|---|---|---|---|---|
| 1 | prologueSentences[0] | "...לפי מה שבאמת נמצא בקופסה — רשימת הרכיבים..." | "...לפי מה שבאמת נמצא בקופסה: רשימת הרכיבים..." | Em-dash → colon |
| 2 | prologueSentences[1] | "...חומוס נמדד מול חומוס, לא מול מזון אחר." | "...חומוס נמדד מול חומוס בלבד." | REWORD — "measured against hummus, not other food" antithesis flattened to a scope statement |
| 3 | prologueSentences[2] | "בחזית כל מוצר בחרנו להציג את החלבון — ולא במקרה. חומוס הוא..." | "בחזית כל מוצר בחרנו להציג את החלבון, במכוון. חומוס הוא..." | REWORD — "and not by accident" idiom restated as "deliberately"; em-dash dropped |
| 4 | prologueSentences[3] | "חלבון גבוה הוא לרוב הסימן לממרח מלא יותר — אבל זו הכותרת, לא כל הסיפור: הציון משקלל..." | "חלבון גבוה הוא לרוב הסימן לממרח מלא יותר, וזו רק הכותרת: הציון משקלל..." | REWORD — "that's the headline, not the whole story" idiom restated positively ("that's only the headline"); em-dash dropped |
| 5 | categoryNote | "...המספר האמין ביותר שאפשר להעמיד להשוואה — והוא גם מסגיר..." | "...המספר האמין ביותר שאפשר להעמיד להשוואה, והוא גם מסגיר..." | Em-dash → comma, no antithesis |
| 6 | methodologyLines[1] | "...ההשוואה היא קטגורית בלבד — כל מוצר מוערך..." | "...ההשוואה היא קטגורית בלבד: כל מוצר מוערך..." | Em-dash → colon |

**Kept as-is (with reason):**
- categoryNote title: "הערת קטגוריה — ערכי שומן אינם מוצגים" — the em-dash here is the established site-wide "הערת קטגוריה — [title]" header convention used identically across bread/milk/chocolate-tablets/snacks. KEEP — structural formatting convention, not narrative prose.
- Code comments with em-dashes (lines 31–65, 143, 153) — internal exclusion-set annotations, not consumer-facing. Out of scope.

Em-dash count: before 6 (narrative) → after 0 (narrative, excluding the caveat-header convention dash which is unchanged); remainder in code comments and the header convention.

---

## 5. `bari-web/src/lib/comparisons/snacks-comparison-page-data.ts`

| # | Field | Before | After | Decision |
|---|---|---|---|---|
| 1 | hero.title | "חטיף דגנים נשמע כמו הבחירה הבריאה במדף — הרשימה לא תמיד מסכימה" | "חטיף דגנים נשמע כמו הבחירה הבריאה במדף; רשימת הרכיבים מספרת סיפור מדויק יותר" | REWORD — flattened "the list doesn't always agree" to a positive claim about what the list tells you; em-dash dropped |
| 2 | prologueSentences[0] | "...'מקור לסיבים' — וקל להניח..." | "...'מקור לסיבים', וקל להניח..." | Em-dash → comma |
| 3 | prologueSentences[1] | "הם לא. מצד אחד משפחה של חטיפי תמרים..." | "המדף מחזיק שני קצוות רחוקים: מצד אחד משפחה של חטיפי תמרים..." | REWORD — dropped the blunt "הם לא" ("they aren't [alike]") opener; kept the genuine two-sided מצד אחד/מצד שני comparison (legitimate parallel structure, not single-subject antithesis) |
| 4 | prologueSentences[1] cont'd | "...אותה הבטחה — וציונים שנעים..." | "...אותה הבטחה, וציונים שנעים..." | Em-dash → comma |
| 5 | prologueSentences[2] | "...כי במדף הזה 'טוב' אומר פחות מהונדס — לא בריא במובן הרחב." | "...כי במדף הזה 'טוב' אומר פחות מהונדס, במובן מצומצם." | REWORD — "not healthy in the broad sense" antithesis flattened to "in a narrow sense"; em-dash dropped |
| 6 | categoryNote[0] title | "'הכי טוב' כאן הוא B, לא A" | "'הכי טוב' כאן הוא B" | REWORD — dropped "not A"; the body already explains no product reaches A, so the fact survives without the antithesis framing |
| 7 | categoryNote[0] body | "...זו אינה החמרה אלא תיאור הקטגוריה: חטיפי דגנים..." | "...זו תיאור מדויק של הקטגוריה: חטיפי דגנים..." | REWORD — dropped "isn't harshness but description" (אלא); states positively |
| 8 | categoryNote[0] body cont'd | "...שמעלה את החיך — והציון משקף זאת." | "...שמעלה את החיך, והציון משקף זאת." | Em-dash → comma |
| 9 | categoryNote[1] body | "חטיפי חלבון (פרוטאין) — מוצרים מהונדסים...ותחליפי סוכר — נמדדים..." | "חטיפי חלבון (פרוטאין), מוצרים מהונדסים...ותחליפי סוכר, נמדדים..." | Em-dash ×2 → comma |
| 10 | categoryNote[2] body | "חטיף נמדד מול חטיפים אחרים, לא מול מזון אחר. ציון B כאן אומר '...' — לא שהמוצר שקול לארוחה..." | "חטיף נמדד מול חטיפים אחרים בלבד. ציון B כאן אומר '...', ולא שהמוצר שקול לארוחה..." | REWORD (partial) — "measured against other bars, not other food" antithesis flattened to "against other bars only"; second clause ("...not that it's equivalent to a meal") kept as a soft hedge — this negates a possible misreading of the grade rather than contrasting two named things, and a fully positive rephrase read as overreach/less honest, so it was softened (subordinate "ולא ש") rather than fully reworded. Em-dash dropped |

**Kept as-is (with reason):**
- categoryNote titles retain the "הערת קטגוריה — [title]" em-dash header convention (×3), matching every other category page. KEEP — structural convention, not narrative.
- Code comments with em-dashes (lines 41, 61, 75) — not consumer-facing. Out of scope.

Em-dash count: before 9 (narrative) → after 0 (narrative, excluding the 3 caveat-header convention dashes, unchanged); remainder in code comments.

---

## 6. `bari-web/src/data/comparisons/milk_frontend_v1.json` (`page_copy` only)

| # | Field | Before | After | Decision |
|---|---|---|---|---|
| 1 | prologue.sentences[3] | "לכן ההשוואה כאן לא מסתכלת רק על מספר אחד, אלא על התמונה הרחבה..." | "לכן ההשוואה כאן מסתכלת על התמונה הרחבה של המוצר כפי שהוא מופיע על המדף, מעבר למספר אחד." | REWORD — dropped "doesn't look only at X, but at Y" (אלא); positive declarative |
| 2 | methodology.lines[2] | "ההשוואה אינה נשענת רק על קלוריות, חלבון או סוכר, אלא מנסה להבין..." | "ההשוואה מנסה להבין את איכות המוצר כמכלול, מעבר לקלוריות, חלבון או סוכר בלבד." | REWORD — dropped "isn't based only on X, but tries to..." (אלא); positive declarative |
| 3 | caveat.notes[0].body | "הציון משקלל את הרכב המוצר כולו — חלבון, סוכר, תוספים ורמת עיבוד — ולא את אחוז השומן לבדו." | "הציון משקלל את הרכב המוצר כולו: חלבון, סוכר, תוספים ורמת עיבוד, מעבר לאחוז השומן בלבד." | REWORD — "not fat percentage alone" antithesis flattened; both em-dashes dropped |
| 4 | caveat.notes[1].body | "משקה שקדים, סויה או שיבולת שועל אינו מקבל ציון נמוך רק משום שאינו חלב. כל מוצר נמדד מול דומיו לפי ההרכב שעל האריזה — אך שימו לב..." | "משקה שקדים, סויה או שיבולת שועל נמדד מול משקאות מאותה משפחה, לפי ההרכב שעל האריזה. שימו לב..." | REWORD (QA-revised) — earlier reword ("...בדיוק כמו חלב פרה") introduced a NEW cross-category equivalence claim (plant drink ≡ cow's milk) not in the original and undercut by the fortification caveat in the same note. Restored the original peer-relative meaning "measured against drinks from its own family, by the composition on the label" (plant vs plant), positively, WITHOUT the "אינו מקבל ציון נמוך רק משום שאינו חלב" antithesis and WITHOUT any cow's-milk equivalence; em-dash dropped |

**Kept as-is (with reason):**
- methodology.lines[3]: "...ולא לשמש כהמלצה רפואית או תזונתית אישית" — standard site-wide disclaimer boilerplate. KEEP.
- caveat.notes[0].title: "'דל שומן' אינו אוטומטית ציון גבוה יותר" — factual negation of a false consumer assumption (myth-correction), not an "X, not Y" antithesis of two named things. KEEP.
- caveat.notes[1].title em-dash ("הערת קטגוריה — ...") — header convention. KEEP.
- shelf_lens_options[5].label: "ללא תוספים" — UI filter/checkbox label ("no additives"), standard terminology, not editorial antithesis prose. KEEP.

Em-dash count: before 5 (in page_copy narrative) → after 0 (narrative); 2 remain in caveat-note header convention (unchanged, matches site-wide pattern).

---

## Summary counts

| File | Antithesis found | Reworded | Kept-as-voice/factual/boilerplate | Em-dashes before → after (narrative only) |
|---|---|---|---|---|
| bread-comparison-page-data.ts | 4 instances (5 strings incl. duplicate) | 4 | 2 | 5 → 0 |
| chocolate-bars-comparison-page-data.ts | 3 | 3 | 3 (incl. 1 owner-voice signature) | 6 → 0 |
| chocolate-tablets-comparison-page-data.ts | 4 (incl. 1 repeated phrase) | 4 | 2 | 8 → 0 |
| hummus-comparison-page-data.ts | 4 | 4 | 1 (+ header convention) | 6 → 0 |
| snacks-comparison-page-data.ts | 6 (1 partial/softened) | 5.5 | 1 hedge partially kept + header convention | 9 → 0 |
| milk_frontend_v1.json (page_copy) | 4 | 4 | 3 | 5 → 0 |
| **Total** | **~25** | **~24.5** | **~12** | **39 → 0** (narrative) |

No scores, rowVerdict, insightLine, or any non-narrative field was touched in any file.
