# Brined Cheeses — Golden Template Render Spec v1 (TASK-268 instance)

**Owner ruling 2026-06-13:** this page is the **golden template** — every future category run and every back-correction of an older page inherits it. **Zero tolerance for mistakes.** Build to 10/10. Charts/visuals/editorial rows are REQUIRED (owner: "tables, visuals charts — this can and should look cooler").

This spec consolidates the converged C3 (gpt-5.5) creative direction + Design Agent specs + locked data. Implement exactly. The data is LOCKED from the final 36-product corpus (`bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json`). Charts must be DATA-DRIVEN (compute from that JSON at render), but the expected values below are given for self-verification — if your computed values differ, STOP (the JSON changed under you).

> ⚠️ `bari-web/AGENTS.md`: this Next.js has breaking changes — read the relevant `node_modules/next/dist/docs/` guide before writing component/build code.

---

## PART A — Copy propagation (NO re-authoring; install these exact strings)

Target file: `bari-web/src/lib/comparisons/brined-cheeses-page-data.ts`. The corrected, verified, gate-clean copy (source: `02_products/brined_cheeses/brined_cheeses_copy_v2_draft.json`). The current consts still say "48 / תקרה ב-75 / 7 מתוך 9" — REPLACE.

**`brinedCheesesPrologueSentences` → exactly these 4:**
1. `כשאת קונה גבינה מלוחה, המלח הוא לא רכיב שנוסף לטעם — הוא מה שהופך את החלב לגבינה. הכבישה בתמיסת מלח שומרת על הגבינה, מעצבת את המרקם שלה, ומגדירה את אופייה.`
2. `זה אומר שלפטה, לבולגרית ולצפתית יש נתרן גבוה מלידה. זו לא בחירה ייצורית — זה מה שהן. ברי לא מענישה אותן על כך. השאלה שנשאלת כאן היא שאלה אחרת: כשהנתרן הוא נתון קבוע, מה בכל זאת מבדיל גבינה טובה מגבינה בינונית?`
3. `ברי בחנה 36 גבינות מלוחות — ומצאה שהתשובה לא נמצאת במלח. בפיזור הציונים: 9 בדירוג A, 20 ב-B, 5 ב-C ו-2 ב-D. ההבדלים הגדולים נובעים מהרשימה: כמה רכיבים, אילו מייצבים, כמה חלבון, עד כמה הגבינה נשארת פשוטה.`
4. `הנדיר כאן הוא המינימליזם: רק שתי גבינות במדף מגיעות בלי שום תוסף — חלב, מלח ותרבית בלבד. המרשימה שבהן היא הבולגרית 13% של יורו מחלבות אירופה: רשימה נקייה, תרבית לקטית חיה, נתרן נמוך יחסית של 720 מ"ג, וציון בדירוג A. וכאן מתחדדת הנקודה: הציונים הגבוהים ביותר, 85, שייכים לצפתיות ולפטה של מחלבות גד, גבינות מצוינות שנשענות על חומר משמר. הגבינה הנקייה השנייה, טמרה של רג'ב, יושבת דווקא ב-C כי הנתרן שלה הוא הגבוה במדף. נקי לא תמיד אומר ציון גבוה, וזה בדיוק מה שברי באה למדוד.`

**`brinedCheesesMethodologyLines` → exactly these 3:**
1. `כל גבינה מלוחה מקבלת הגנת קטגוריה, כי הנתרן שלה הוא חלק ממה שהיא ולא תוסף שנבחר. המנגנון אינו מתייחס לנתרן כאל כשל — הוא מדרג אותו יחסית למדף. רק גבינה שנמצאת מעל 200 מ"ג מחציון הקטגוריה מקבלת חיסרון נוסף. לא כל גבינה שעל החציון.`
2. `מה שמניע את ההבדלים האמיתיים: מספר הרכיבים, נוכחות מייצבים ומתחלבים, ואחוז השומן. חלב, מלח ותרבית לקטית הם הגרעין. גומי זרעי חרובים, אגר וגלוקונו-דלתא-לקטון הם שכבה אחרת לגמרי. החלבון שוקל לחיוב — גבינה מלוחה היא מקור חלבון ממשי, וזה מה שהמנגנון מתגמל עליו.`
3. `כל מוצר שמוצג כאן עבר אימות מלא: רשימת רכיבים ונתוני תזונה ממקור ישיר. גבינה שלא ניתן היה לאמת אותה לא מופיעה. הערה לגבי אחוזי שומן: '24%' בשם גבינה כמעט תמיד מתייחס לשומן בחומר היבש — מדד תעשייתי שאינו שווה ערך לשומן ב-100 גרם מוכנה. ברי עובדת עם הנתון שעל התווית.`

**`brinedCheesesComparisonMetadata.description`** → replace "48" with "36": `השוואת 36 גבינות מלוחות מהמדף הישראלי — ציון Bari, נתרן, חלבון ושומן ל-100 גרם. מידע, לא המלצה.`

Leave `brinedCheesesHero`, `brinedCheesesCategoryNote` as-is. After edit: grep the file for `48`, `תקרה ב-75`, `7 מתוך 9` → must be ZERO.

---

## PART B — Three charts (REQUIRED), in the Prologue section, BEFORE the product table

New component `BrinedCheesesPrologueVisualizations` (props: `products: BariProductVM[]`). Rendered inside the prologue, after the prose, before the table. Data-driven from the 36 products.

**HARD RULE (non-negotiable):** grade is NEVER color-encoded. No green-A/red-D, no traffic lights, no quality hue. Dots are a single neutral ink. Grade, where shown, is plain TEXT only. Violating this fails the golden bar. (Memory: `bari_score_presentation_v1`.)

### Chart 1 — "ספקטרום המלח" (sodium distribution strip)
- 36 ticks/dots on a horizontal axis 600→1,628 mg/100g. One vertical marker at the **shelf median 1,000 mg** labeled `חציון המדף · 1,000 מ"ג`. Min/median/max labels.
- LOCKED expected: min **600**, median **1000**, max **1628**, and a visible cluster of **19 dots in 900–1,099**.
- Single ink color for all dots (no grade color). Median marker in a neutral rule or token accent (not a grade color).
- Mobile: full-width; 3 labels only (`600`, `1,000 חציון`, `1,628`); tap a dot → tooltip with product name + sodium + score.
- Place directly under prologue sentence 3 (it carries the numbers that sentence references).

### Chart 2 — "A הוא לא דל-נתרן" (grade × sodium plot)
- Four text-labeled rows `A / B / C / D` (top→bottom), each product a dot at its sodium x-position. Median line at 1,000.
- LOCKED expected per grade: **A** n=9, 600–1550, **6 of 9 ≥900mg**; **B** n=20, 770–1500; **C** n=5, 950–1628; **D** n=2, 800–950.
- One annotation near the A row: `6 מתוך 9 גבינות ה-A יושבות מעל 900 מ"ג — A כאן הוא 'הטוב במדף', לא 'דל-נתרן'.`
- Grade row labels are TEXT only, identical neutral dots — separation by vertical position, not color.
- Mobile: 4 stacked rows, dots by sodium, tooltip on tap.

### Chart 3 — "נדירות התווית הנקייה" (clean-label rarity)
- Headline stat `2 מתוך 36` + a 36-mark unit grid; the 2 clean marks distinguished by **shape/outline/opacity — NOT color**. Caption: `שתי גבינות בלבד ללא שום תוסף: חלב, מלח ותרבית.`
- LOCKED: exactly **2 of 36** clean = `יורו מחלבות אירופה בולגרית 13%` (80/A, 720mg) and `מחלבת רג'ב טמרה 17%` (65/C, 1628mg). (Definition: ingredient list has no preservative/stabilizer and ≤4 parts. Do NOT use "limitingFactors null" — that gives 16 and is WRONG for this claim.)
- Mobile: big `2/36`, then the unit grid below.

(Optional 4th "three levers" explainer — only if it does NOT clutter; the methodology copy already covers levers. Default: skip; the 3 charts above are required. If you add it, it must be a text/icon explainer, NOT a fake quantitative chart — C3's explicit warning.)

**C3's AVOID (enforce):** no colorful health-dashboard, no "winner/loser" badges, no gamification. Register = data-journalism (Economist/FT), credible, calm.

---

## PART C — Editorial row + page polish (Design Agent spec; brined-first, NO regression to other categories)

Apply the additive, no-regression polish (all reversible; verify other categories unaffected). From the Design spec:
- Rows: even-row bg `#F5F5F2` (warmer than current `#fbfbf9`); bottom border `rgba(17,19,24,0.07)`; hover `rgba(31,143,106,0.055)` + new `:active rgba(31,143,106,0.09)`; row padding `16px 16px`.
- Column header: drop monospace/uppercase → `font-sans 0.65rem, weight 600, tracking 0.04em, color #8A908B` (human label, not a DB schema).
- Band dividers: sans-serif label, `transparent` background (remove `#fafaf7` stripe); keep the grade-accent TEXT color (that is the existing canonical grade text color, allowed — it is not a new color encoding).
- Thumbnail: border `black/[0.09]`, img padding `p-[7px]` (sharper product-card frame).
- Category-note box: `px-4 py-3 rounded-xl leading-[1.6]`.
- Add a 1px separator between the prologue/note block and the table (`border-t rgba(17,19,24,0.06)`, section-aligned mx).
- Hero mobile top padding `pt-5`.
- `rowVerdict` top margin `mt-[6px]`.

**Do NOT** change scores, grades, product data, the chip geometry, the gradePalette, the 4-section structure, single-expand behavior, or `dir="rtl"`. Do NOT touch legacy pages (milk/bread/snacks). If a change would ripple to another category's shared component, keep it brined-scoped or confirm it's strictly additive.

**Pre-existing conflict (flagged, do NOT resolve here):** comparison-template-standard §22 wants chip tier-word `72 · B · טוב`; FIX-2 in comparison-row.tsx suppresses it. Leave chip as-is; just note it in your return.

---

## PART D — Governance

- **Drift amendment (owner-sanctioned):** the comparison-template "no chart above the first product row" drift guideline is DELIBERATELY amended for the golden standard — these are grounded, in-prologue category-context visuals the owner explicitly requested. Document this in your return; it is not a violation.
- Stay inside design-token governance (`bari_design_token_governance_v1`); propose new tokens only inside the 7 allowed categories with justification (the column-header class + even-row value are the expected additions).
- Canonical components only; charts are a NEW brined sub-component, not a modification to the shared `ComparisonPage`/`ComparisonTable` core (additive).

---

## PART E — Build gate + self-verification (the page is NOT done until ALL pass)

1. `npm run build` exits 0 (run it; paste the tail).
2. Copy: grep page-data.ts → zero `48`, zero `תקרה ב-75`, zero `7 מתוך 9`; the 4 prologue + 3 methodology strings match this spec byte-for-byte.
3. Charts render REAL values (not stale): median line at 1000, max 1628, clean = 2/36, A-row annotation = 6/9. Recompute from the JSON in your verification and show the numbers.
4. **No grade color anywhere in the charts** — confirm dots are single-ink, grade shown as text only.
5. Images still render in-page for the 36 (the imageUrl→VM map already exists at page-data.ts:31 — don't break it).
6. Mobile (375px) and desktop both coherent; charts legible; 15–20s shelf comprehension preserved.
7. No legacy/other-category regression (spot-check one other comparison page builds + looks unchanged).

Return with the machine-readable return contract (`01_framework/operations/return_contract_v1.md`). **Propose RETURNED — do NOT close.** The orchestrator red-teams (Stage 9, zero CRITICAL required for golden) and closes.
