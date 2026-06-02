# TASK-143 — Yogurt Shelf Re-author (Content) → run_yogurt_004 (B-capped)

**Date:** 2026-06-02 · **Owner:** Content Agent · **For:** Data (fold into `yogurts_frontend_v1.json` → v2; **do NOT** let Content touch live JSON)
**Source of every value below:** `reports/run_yogurt_004_run_summary.json` + per-product `bsip2_outputs/run_yogurt_004/products/**/bsip2_trace.json`
**Replaces:** the live DEC-005 manual shelf (A-heavy, 88/A top). New shelf is **B-capped, zero A** (machine max 78.7/B).

---

## 0. Hard-rule compliance (the maadanim/hummus swap trap — TASK-149/150)
- No line references an old grade, old score, a point-gap to the old shelf, or an "A"/"top-of-an-A" framing.
- The only mention of "A" anywhere is the prologue stating **none reach it** — that is the honest reframing, not a stale claim.
- Every numeric claim traces to a run_yogurt_004 value (barcode cited per row).
- Score display stays numeric/grade only (`78.7 / B`); no חזק/בינוני/חלש; no color encoding.

## 1. Product Owner ruling on soy/coconut rows → **DROP + DEFER** (forced by data)
run_yogurt_004 (dairy_protein scrape) contains **zero plant-based yogurt products**. Every "סויה" token is an
*additive* (soy-protein crisps / lecithin / flour) inside a dairy yogurt; every "קוקוס" / "שקדים" / "שיבולת"
token is a *flavor or mix-in* in a dairy yogurt. The live rows **yog-010 יוגורט סויה טבעי (72/B)** and
**yog-009 יוגורט קוקוס טבעי (68/B)** therefore have **no run_004-traceable equivalent**.
- A "separate plant pool" is **not buildable** on this run (no products to populate it).
- Keeping the rows on stale manual B scores would re-introduce exactly the drift the hard rule forbids.
- **Action:** remove both plant rows from the v2 shelf; **defer** plant-based yogurt to a dedicated plant-base run.
- Net: live 13 rows − 2 plant rows = **11 dairy rows** below.

## 2. Confidence state (presentation)
run_004 carries real ingredient panels + core macros (kcal/protein/sugar/fat/sodium) for all 11 → recommend
`confidence: "verified"` (was `"partial"` on the null-nutrition manual shelf). Sat-fat/fiber are missing on a
few; **Data/QA set the final `confidence` field.** No insight line depends on the confidence value.

---

## 3. PROLOGUE (Hebrew, RTL)

> בדקנו מחדש את מדף היוגורט על נתוני אריזה אמיתיים — רכיבים, חלבון, סוכר ושומן כפי שהם מופיעים על המוצר עצמו.
> התמונה ברורה: אף יוגורט בקטגוריה לא מגיע ל-A. הציון הגבוה הוא 78.7/B — יוגורט חלבון 0% עם חמישה מרכיבים.
> היוגורטים הפשוטים — ביו, נטול לקטוז, חלב עיזים — נעים סביב 71 עד 75, כולם B: בסיס חלבי, תרביות, מעט מרכיבים.
> מכאן זה רק יורד. ככל שמתווספים סוכר, חומרי טעם, מייצבים או פצפוצים — הציון נופל. גרסאות הטעם וה'קראנצ'' מגיעות
> עד C, D ו-E, גם כשכמות החלבון על האריזה זהה. ושומן גבוה לא מעלה ציון: יווני 8% עם 4.8 גרם שומן רווי יורד ל-62/C.
> במדף הזה "הכי טוב" הוא B — ולא יותר.

---

## 4. INSIGHT LINES (Hebrew, RTL) — 11 rows, score-descending

| # | barcode | name | score / grade | insightLine |
|---|---|---|---|---|
| 1 | 7290112336712 | דנונה פרו 21 חלבון 0% | 78.7 / B | 10.5 גרם חלבון ל-100 גרם ב-0% שומן, חמישה מרכיבים, בלי חומרי טעם או צבע. הציון הגבוה בקטגוריה — ונשאר B. |
| 2 | 7290110328221 | יוגורט נטול לקטוז 3% שומן | 75.5 / B | אותו בסיס חלבי של יוגורט ביו, עם חיידקי ביפידוס — ולקטוז עד 0.05%. |
| 3 | 7290014758100 | יוגורט ביו תנובה 3% | 74.9 / B | חלב, רכיבי חלב וחיידקי ביפידוס — 5.3 גרם חלבון, בלי טעמים מוספים. בסיס יוגורט פשוט. |
| 4 | 7290114311069 | מולר אקטיב לבן 0% 25 חלבון | 74.2 / B | 12.5 גרם חלבון ל-100 גרם עם 2.5 גרם סיבים, 0% שומן — ועדיין B. חלבון גבוה לבדו לא חוצה את התקרה. |
| 5 | 7290014758117 | יוגורט ביו תנובה 1.5% | 73.3 / B | אותו ביו של תנובה בגרסת 1.5% שומן — אותם חיידקי ביפידוס, פחות שומן, אותו אשכול ציון. |
| 6 | 7290012645297 | יוגורט עיזים ביו | 71.9 / B | חלב עיזים, סיבים תזונתיים ותרבית יוגורט — שישה מרכיבים, בלי טעמים. הבסיס הפשוט של מדף העיזים. |
| 7 | 7290107936309 | יוגורט בסגנון יווני 6.5% | 71.5 / B | מסוי בסגנון יווני, 5.5 גרם חלבון ו-0 סוכר מוסף — אבל 6.5% שומן (3.9 גרם רווי) מחזיק אותו ב-B. |
| 8 | 7290110321031 | יופלה GO מועשר בחלבון | 70.3 / B | 10 גרם חלבון, בלי סוכר מוסף ובלי תוספים — אבל החלבון מאבקת חלב, לא מתסיסה. נקודת המעבר התחתונה של ה-B. |
| 9 | 7290014890589 | יוגורט יווני 8% | 62.0 / C | שלושה מרכיבים בלבד — חלב, שמנת וחלבון חלב — אבל 8% שומן ו-4.8 גרם רווי ל-100 גרם מורידים אותו ל-C. נקי לא תמיד אומר רזה. |
| 10 | 7290110321680 | יופלה GO תות | 49.2 / D | אותם 10 גרם חלבון של ה-GO הלבן — אבל 9.6 גרם סוכר, 16 מרכיבים, צבע מאכל ועמילן מעובד מורידים אותו ל-D. הטעם הוא ההבדל. |
| 11 | 7290010471669 | יוגורט קראנצ תות קורנפלק | 34.3 / E | יוגורט עם תוסף קורנפלקס ושוקולד: 19 מרכיבים, 9.9 גרם סוכר ו-13.1 גרם פחמימות. הציון הנמוך במדף. |

**Editorial pair (template allows one):** rows **8 ↔ 10** — same brand, identical 10g protein on the label,
B vs D. The only difference is the flavoring/sugar/additive load. This is the shelf's central lesson.

### Per-row traceability (audit)
1. protein 10.5 / fat 0 / 5 ingredients / additive_categories=[] / max score in run (78.7).
2. lactose ≤0.05% / bifidus / NOVA 3 / 75.5.
3. protein 5.3 / bifidus / has_flavor_enhancer=false / 74.9.
4. protein 12.5 / fiber 2.5 / fat 0 / cap NOVA_3=87 / 74.2.
5. protein-base same family as row 3; 1.5% fat; 73.3 (1.6 pt vs row 3 = within noise).
6. goat milk / dietary fiber / cultures / 6 ingredients / 71.9.
7. protein 5.5 / "0 מתוכם סוכר מוסף" / fat 6.5, sat 3.9 / 71.5.
8. protein 10 / added_sugar=0 / sprint1_additives=0 / protein_source=mixed(אבקת חלב) / has_fermentation=false / 70.3 (B floor).
9. 3 real ingredients (חלב/שמנת/חלבון חלב) / fat 8, sat 4.8 / 109 kcal / NOVA 3 / 62.0.
10. protein 10 / sugar 9.6 / 16 ingredients / color + modified starch E1422 / NOVA 4 / cap 68 / 49.2.
11. 19 ingredients / sugar 9.9 / carbs 13.1 / NOVA 4 / 34.3 (run minimum).

---

## 5. 15–20s first-time-mobile comprehension self-test
**Q1 "What is this?"** Top line = `78.7 / B` + prologue line "אף יוגורט מגיע ל-A… הכי טוב הוא B" → reader
learns in one glance it's a ranked yogurt shelf that tops out at B. **PASS (~4s).**
**Q2 "Which is better, and why?"** Descending scores; row 1 line names the reason (חלבון גבוה, 0% שומן, מעט
מרכיבים, בלי תוספים). **PASS (~8s).**
**Q3 "What's the catch?"** The 8↔10 pair (same 10g protein → B vs D) + the יווני-8% contradiction (נקי ≠ רזה)
deliver the rule "added sugar/flavor/additives drop the grade; high fat doesn't lift it" without jargon.
**PASS (~15s).**
**Verdict: PASS** within the 15–20s window. Risk noted: 8 of 11 rows are B — the B-cluster could read flat.
Mitigation already in copy: rows differentiate on *named composition* (protein g, fat %, cultures, lactose),
not on a grade label, so the cluster stays legible without inventing separation.

---

## 6. Hand-off note to Data
Fold §3 (prologue) + §4 (11 insightLines) into v2. Drop yog-009/yog-010. Set `score`/`grade` per the table,
`confidence` per §2 (QA confirms). Keep the frozen comparison-template architecture (hero + prologue + table +
methodology). Expansion `bottomLine`/`positiveSignals`/`limitingFactors` for these 11 can be regenerated from
the same traces on request — this hand-off covers the two leakage-critical surfaces (prologue + insightLine).
