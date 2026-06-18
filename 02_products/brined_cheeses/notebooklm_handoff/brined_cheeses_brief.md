# Brined Cheeses (גבינות מלוחות) — Data & Chart Brief for NotebookLM

This is a self-contained brief for generating charts/visuals for Bari's brined-cheeses
comparison page. All numbers here are **final and verified** (Bari run_005, 36 products).
The companion data file is **`brined_cheeses_36_products.csv`** in this same folder — feed
both into NotebookLM.

Language: **Hebrew, right-to-left.** Register: credible data-journalism (Economist / FT),
not marketing. **Hard rule: grade (A/B/C/D) must NEVER be encoded by color** (no green-A /
red-D). Grade is shown as a letter only; color may not signal quality.

---

## The category in one paragraph
Brined/salted cheeses (feta, bulgarit, tzfatit, halloumi-style) are **structurally high in
sodium** — the salt brine is part of how the cheese is *made*, not a topping. So a high Bari
score here does NOT mean "low sodium." It means clean ingredients, moderate fat, and minimal
processing *relative to this salty shelf*. Sodium is scored relative to the shelf median, not
absolutely. The real score differences come from **ingredient count, presence of
stabilizers/emulsifiers, and fat %**; protein is rewarded.

---

## The dataset (final, verified)
- **36 products** scored.
- **Grade distribution:** A = 9 · B = 20 · C = 5 · D = 2.
- **Sodium (mg / 100g):** min **600**, median **1,000**, max **1,628**, mean ≈ 1,052.
- **Sodium distribution by band:**
  | band (mg/100g) | # cheeses |
  |---|---|
  | 600–699 | 2 |
  | 700–899 | 4 |
  | **900–1,099** | **19** ← the shelf clusters here, around the median |
  | 1,100–1,299 | 4 |
  | 1,300–1,499 | 4 |
  | 1,500+ | 3 |
- **"A is not low-sodium":** **6 of the 9 A-grade cheeses sit at ≥ 900 mg** sodium.
- **Clean label:** **only 2 of 36** cheeses have *no additive at all* (just milk, salt,
  culture): "קוביות בולגרית מעודנת 13% — יורו מחלבות אירופה" (score 80, grade A, 720 mg) and
  "גבינת טמרה מלוחה בקר 17% — מחלבת רג'ב" (score 65, grade C, 1,628 mg — clean but the saltiest
  on the shelf, which is why it's only a C).

---

## The 3 charts to create (each must read in ~5 seconds, mobile-first)

### Chart 1 — Sodium distribution ("ספקטרום המלח")
A **histogram** of the sodium bands above. The bar at **900–1,099 (19 cheeses)** should
dominate — it tells the whole story: the shelf is densely clustered around the **1,000 mg
median**. Mark the median (1,000). One neutral bar color (no grade color). Title in Hebrew.
*Insight it must convey:* "this is a salty shelf, tightly clustered — and Bari judges within it."

### Chart 2 — Score vs. sodium ("A הוא לא דל-נתרן")
A **scatter / strip plot**: each cheese a dot, X = sodium (600→1,628), Y = grade lane
(A / B / C / D, A on top). Mark the median line at 1,000. The point: **A-grade dots are spread
across the whole sodium range — 6 of 9 are above 900 mg.** Grade lanes labeled by letter only;
all dots one neutral color. *Insight:* "grade is set by ingredient quality, not by sodium —
an A can still be salty."

### Chart 3 — Clean-label rarity ("נדירות התווית הנקייה")
A **bold stat / unit chart**: a big **"2 / 36"**, with a 36-mark grid where the 2 clean
cheeses stand out (by shape/fill, **not** by quality color), and the 2 named.
*Insight:* "truly clean minimalism (milk, salt, culture only) is rare on this shelf."

(Optional 4th: a small "what moves the score" explainer — ingredient count · stabilizers · fat %.
Not a quantitative chart; an editorial note.)

---

## Page copy already written (for tone/context — Hebrew)

**Hero:** בולגרית, פטה, צפתית, חלומי — גבינות שהנתרן בהן הוא חלק מהייצור, לא תוספת.

**Intro (prologue):**
1. כשאת קונה גבינה מלוחה, המלח הוא לא רכיב שנוסף לטעם — הוא מה שהופך את החלב לגבינה. הכבישה בתמיסת מלח שומרת על הגבינה, מעצבת את המרקם שלה, ומגדירה את אופייה.
2. זה אומר שלפטה, לבולגרית ולצפתית יש נתרן גבוה מלידה. זו לא בחירה ייצורית — זה מה שהן. ברי לא מענישה אותן על כך. השאלה שנשאלת כאן היא שאלה אחרת: כשהנתרן הוא נתון קבוע, מה בכל זאת מבדיל גבינה טובה מגבינה בינונית?
3. ברי בחנה 36 גבינות מלוחות — ומצאה שהתשובה לא נמצאת במלח. בפיזור הציונים: 9 בדירוג A, 20 ב-B, 5 ב-C ו-2 ב-D. ההבדלים הגדולים נובעים מהרשימה: כמה רכיבים, אילו מייצבים, כמה חלבון, עד כמה הגבינה נשארת פשוטה.
4. הנדיר כאן הוא המינימליזם: רק שתי גבינות במדף מגיעות בלי שום תוסף — חלב, מלח ותרבית בלבד. המרשימה שבהן היא הבולגרית 13% של יורו מחלבות אירופה: רשימה נקייה, תרבית לקטית חיה, נתרן נמוך יחסית של 720 מ"ג, וציון בדירוג A. וכאן מתחדדת הנקודה: הציונים הגבוהים ביותר, 85, שייכים לצפתיות ולפטה של מחלבות גד, גבינות מצוינות שנשענות על חומר משמר. הגבינה הנקייה השנייה, טמרה של רג'ב, יושבת דווקא ב-C כי הנתרן שלה הוא הגבוה במדף. נקי לא תמיד אומר ציון גבוה, וזה בדיוק מה שברי באה למדוד.

**Methodology:**
1. כל גבינה מלוחה מקבלת הגנת קטגוריה, כי הנתרן שלה הוא חלק ממה שהיא ולא תוסף שנבחר. המנגנון אינו מתייחס לנתרן כאל כשל — הוא מדרג אותו יחסית למדף. רק גבינה שנמצאת מעל 200 מ"ג מחציון הקטגוריה מקבלת חיסרון נוסף.
2. מה שמניע את ההבדלים האמיתיים: מספר הרכיבים, נוכחות מייצבים ומתחלבים, ואחוז השומן. חלב, מלח ותרבית לקטית הם הגרעין. גומי זרעי חרובים, אגר וגלוקונו-דלתא-לקטון הם שכבה אחרת לגמרי. החלבון שוקל לחיוב.
3. כל מוצר שמוצג כאן עבר אימות מלא: רשימת רכיבים ונתוני תזונה ממקור ישיר. גבינה שלא ניתן היה לאמת אותה לא מופיעה.

**Category caveat:** כל הגבינות במדף הזה עשירות בנתרן — תכונה מובנית של ייצור, לא חריגה. ציון גבוה אינו מעיד שהגבינה נמוכה בנתרן; הוא מעיד על הרכב רכיבים נקי, שומן מתון ועיבוד מינימלי ביחס לשאר המדף.

---

## Files in this handoff folder
- `brined_cheeses_36_products.csv` — the 36 products: name, brand, score, grade, sodium, protein, fat, kcal, sat-fat, clean-label flag, ingredients, barcode. **This is the chart data source.**
- `brined_cheeses_brief.md` — this file.

## Where the rest lives (if you need more)
- Full frontend data (all fields incl. images, additives): `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json`
- Copy source: `02_products/brined_cheeses/brined_cheeses_copy_v2_draft.json`
- Scoring methodology: `02_products/brined_cheeses/methodology/`
- Per-product scoring traces: `02_products/brined_cheeses/bsip2_outputs/run_brined_005/`
