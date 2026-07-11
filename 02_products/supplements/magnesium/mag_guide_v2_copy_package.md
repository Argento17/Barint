# Magnesium Guide v2 — Consumer Copy Package (Gate-1, Content Agent)

**Task:** TASK-575 subtask
**Governs:** `bari-web/src/lib/guides/magnesium-guide-data.ts` (630 lines, current live file — NOT edited by this task)
**Authored from:** `C:\Bari\02_products\supplements\magnesium\mag_guide_v2_nutrition_spec.md` (Nutrition D6, Product D7 CONDITIONAL GO, updated with §11 — sha256 `f17305132482d2e7b68fb988d6b682c5275dd62badafd7f6b6e80819353a29fc`) + the Product Agent's mid-flight correction message (median fix, bisglycinate bridging caveat, group-(c) severity split — §11 supersedes the group-(c) severity-split item below for #5/#7/#8/#10, see SLOT 11)
**Status:** GATE-1 DRAFT, amended. Every string below is a proposal pending Adversarial QA gate-2. Nothing here ships to `bari-web/src/` from this task — Frontend Agent integrates after gate-2 clears. **SLOT 11 (bottom of file) is the current group distribution (a:0, b:9, c:8, d:1) — it supersedes the 5/12 counts anywhere else in this document that weren't caught by the in-place fix; see SLOT 11 for the full amendment log.**
**Voice law applied:** `content_voice/tom_bari_voice/2_voice_fingerprint.md`, `4_approved_phrases.md`, `5_banned_phrases_and_claims.md`, `01_framework/editorial/assertive_writing_v1.md`, `01_framework/editorial/insight_line_spec_v1.md`.

Every Hebrew string that is a candidate for shipping is wrapped in a fenced ` ```text ` block so it can be mechanically extracted and run through `hebrew_readability.analyze()` / `hebrew_grammar_gate.analyze()`. Self-check results are in the return block.

---

## Corrections applied from the Product Agent's mid-flight message (binding, applied throughout below)

1. **Median corrected to 190 mg**, not 168 mg. Sorted 15 disclosed doses: 76, 88, 100, 122, 135, 136, 168, **190**, 200, 250, 250, 450, 450, 520, 520 → median = 8th value = 190 mg (product #5, NT L.C. Anti Leg Cramps, sits exactly at the median). Every dose-comparison sentence below uses 190, not 168. Product #4 (מגנזיום WELL, 168 mg) is now described as **below** the median, lower-middle of the range — never "at the median."
2. **Bisglycinate bridging caveat** kept explicit, uncompressed, in all four bisglycinate rows (#2, #4, #6, #15): each names that bisglycinate reads as a well-absorbed form in practice, but the direct evidence is too limited to rank it with confidence alongside citrate. This is stated in the row itself, not deferred to the education section only.
3. **Group (c) severity split** — every group-(c) row is written to keep "clean form, tolerance-note only" (#1, #2) visibly distinct from "weaker-absorption form + crosses the safety UL" (#11–#14). A short `classifierHe` badge-candidate phrase is supplied per group-(c) product in Slot 6 for Frontend's optional use. **Superseded in part by SLOT 11:** #5, #7, #8, #10 (originally listed here as "known weaker-absorption form") moved to Group (b) once Nutrition/Product's §11 ruling replaced the FLAG-tier "weaker-absorption" framing with the neutral `evidence_limited` state — see SLOT 11 for the corrected rationale and re-authored rows.

---

## SLOT 1 — Hero / intro block

**Maps to:** `h1` (line 430), `subtitle` (line 431), `buyingRuleIntro` (line 444).

**h1** — unchanged, does not carry any of the killed framing:
```text
איך לבחור מגנזיום
```

**subtitle** — stays `null`. No change proposed.

**buyingRuleIntro** — full rewrite. Kills "מהמדף הישראלי" as a market-completeness claim, kills the six-bars/"אף אחד לא עומד בכל שישה" framing, presents the four ASSESSED criteria only, and states the price/third-party gap once as a guide-level scope note (not a reason for any product's placement):
```text
בדקנו 18 תוספי מגנזיום הנמכרים בישראל, לפי ארבעה דברים שאפשר לקרוא ולבדוק ישירות מהתווית: כמה מגנזיום יסודי המוצר נותן במנה היומית המצוינת עליה, מה הצורה הכימית שלו, האם המינון מתקרב לסף שעלול לגרום לאי-נוחות עיכולית, והאם התווית בכלל מגלה את המידע הדרוש כדי לדעת מה קונים. אין צורך להבין כימיה כדי להשתמש בזה, רק לדעת מה לחפש לפני שמשלמים. שני דברים נוספים לא נבדקו בסבב הזה: מחיר למנה יומית, ובדיקת צד שלישי. שניהם מפורטים בהמשך כפער מידע ברמת המדריך כולו בלבד. הם אינם סיבה לשיוך של מוצר ספציפי לקבוצה כזו או אחרת.
```

---

## SLOT 2 — How-to-read block (assessed criteria cards)

**Maps to:** `buyingRule` array (lines 445–471). **Price and third-party cards are REMOVED from this array** — they no longer belong to the "assessed" set (owner directive). Only 4 cards remain, in `GUIDE_BAR_ORDER` order for the 4 bars that still render as assessed.

```text
המינון היומי: כמה מגנזיום יסודי המוצר נותן במנה היומית המצוינת על התווית. משקל התרכובת (ציטראט, אוקסיד וכו') שלפעמים מודפס גדול יותר על האריזה הוא מספר אחר לגמרי.
```
```text
הצורה הכימית: צורות מגנזיום שונות נספגות בגוף במידה שונה, וההבדל מתועד במקורות מקצועיים.
```
```text
בטיחות: האם המינון היומי המוצהר מתקרב לסף שעלול לגרום לאי-נוחות עיכולית, או חוצה אותו.
```
```text
שקיפות התיוג: האם התווית בכלל מאפשרת לדעת כמה מגנזיום יסודי מקבלים במנה, או שרק משקל התרכובת מצוין בלי חישוב.
```

**Open item for Frontend:** the `bar` key for each stays `doseAdequacy` / `formAbsorption` / `safety` / `labelTransparency` respectively — no change to `GuideBarKey`. `thirdPartyVerification` and `priceFairness` simply get no `GuideBuyingRuleBar` entry for magnesium (they already have no threshold geometry — this is consistent with existing `suppressedBars` handling, just now also absent from the intro card row, not merely visually suppressed downstream).

---

## SLOT 3 — Market-information-gaps guide-level statement

**Maps to:** `suppressedBarsDisclosureHe` (lines 511–512). This field already exists in `GuidePageVM` and is architecturally the right slot — it is already decoupled from the old tier framing in the type comment. Only the copy changes.

```text
שני דברים לא נבדקו במדריך הזה, אצל כל 18 המוצרים: מחיר למנה יומית, ובדיקת צד שלישי. מחיר הוא פער איסוף נתונים של בארי: עדיין לא נאספו נתוני מחיר לתוספי מגנזיום, ונוסיף אותם כשהנתונים ייאספו. בדיקת צד שלישי היא עובדה אחרת: לא מצאנו אישור או בדיקת צד שלישי הניתנים לאימות פומבי בקרב 18 המוצרים שנבדקו, נכון ליולי 2026. שני הפערים האלה לא משפיעים על השיוך של אף מוצר לאחת הקבוצות שלמטה. השיוך מבוסס רק על ארבעת הדברים שכן נבדקו.
```

Note: this carries the owner's exact required certification register ("לא מצאנו אישור או בדיקת צד שלישי הניתנים לאימות פומבי בקרב 18 המוצרים שנבדקו, נכון ליולי 2026") and scopes every market claim to "18 המוצרים שנבדקו" per spec §8, never "המדף הישראלי."

---

## SLOT 4 — Headline finding (replaces the empty-top-tier framing)

**Maps to:** `headlineFinding.title` + `headlineFinding.body[]` (lines 485–498). The old body embedded all 5 `passes_with_flag` product paragraphs inline (lines 491–495) — **removed**: product detail now lives only in each product's own `oneLinerHe` (Slot 6), never duplicated here. This also avoids any one sentence repeating across products.

**title** (amended per SLOT 11 / §11 MEDIUM-1 — see below; "צורה כימית מומלצת" rescoped to citrate alone):
```text
בין 18 תוספי המגנזיום שבדקנו, אף אחד לא משלב מינון בחצי העליון של הטווח, צורת ציטראט ובטיחות ותיוג נקיים בו-זמנית.
```

**body[0]** (the real, product-level reason — spec §2's "why (a) is empty"; amended per SLOT 11 — citrate and bisglycinate no longer share an evaluative adjective):
```text
כל מוצר שמגיע למינון הגבוה בטווח שנבדק (450 עד 520 מ"ג) עושה זאת בצורת אוקסיד, צורה שה-NIH ODS מונה במפורש כבעלת ספיגה נמוכה יותר מציטראט, אספרטט, לקטט וכלוריד. שני המוצרים היחידים בצורה עם עדות מבוססת לספיגה טובה יותר, ציטראט, נשארים מתחת ל-250 מ"ג. ביסגליצינט, הצורה הנפוצה השנייה בקטגוריה, מופיע במוצרים שנעים בין 88 ל-250 מ"ג, אך הראיות לדירוג הספיגה שלו בביטחון מוגבלות מדי כדי לצרף אותו לאותה קבוצה. אף אחד מ-18 המוצרים שנבדקו לא משלב בו-זמנית מינון בחצי העליון של הטווח, צורת ציטראט ובטיחות ותיוג נקיים. זה ממצא על השוק הנוכחי עצמו, מעבר לפערי הנתונים במחיר או בבדיקת צד שלישי.
```

**body[1]** (how the groups below read):
```text
בגלל זה אין כאן קבוצה אחת שכל מוצר "טוב" צריך להימצא בה. המוצרים מחולקים לפי הממצא האמיתי שיש לגביהם: מוצרים שההסתייגות היחידה עליהם היא מינון יסודי נמוך יותר מתוך הטווח שנבדק, מוצרים עם הסתייגות קבועה על הצורה הכימית או על סבילות עיכולית, ומוצר אחד שאי אפשר לדעת עליו מספיק מהתווית כדי לשייך אותו לאחת משלוש הקבוצות האלה.
```

**body[2]** (pointer to Slot 3, not a repeat of it):
```text
מחיר למנה ובדיקת צד שלישי לא נכללים בשיוך הזה כלל. הם לא נבדקו לאף אחד מ-18 המוצרים, וזה מפורט בנפרד למטה.
```

---

## SLOT 5 — Four group headers + one-line captions

**Maps to:** conceptually replaces `recommendationTierCaptions` (523–529), `veryRecommendedEmptyStateHe` (536–537), `cannotAssessSectionIntroHe` (545–546) — see **Open Questions for Frontend** below for why this is a field-shape question, not a drop-in copy swap.

**Group (a) — meets all assessed criteria (0/18):**
```text
עומדים בכל הקריטריונים שנבדקו
```
```text
אף מוצר מתוך 18 שנבדקו לא נמצא כאן. זה עצמו הממצא המרכזי של המדריך — מפורט למעלה.
```

**Group (b) — lower elemental amount (9/18: #3, #4, #5, #6, #7, #8, #9, #10, #15 — amended per SLOT 11 / §11: #5, #7, #8, #10 moved in from Group (c) once `formAbsorption` retired FLAG in favor of the neutral `evidence_limited` state):**
```text
מינון יסודי נמוך יותר
```
```text
מינון יסודי נמוך יותר מתוך הטווח שנבדק הוא המשותף לתשעת המוצרים האלה, ללא הסתייגות בטיחות אצל אף אחד מהם. שקיפות התיוג נקייה אצל שמונה מתוכם; מוצר אחד נושא פער תיוג, מפורט בשורה שלו. הצורה הכימית ידועה אצל כולם: ציטראט (מוצר אחד) נתמך בעדות מבוססת לספיגה טובה, אצל שאר הצורות הראיות לדירוג הספיגה בביטחון עדיין מוגבלות, ואצל מוצר אחד (תערובת שני רכיבים) היחס בתערובת אינו מפורסם כך שהספיגה שלו אינה ניתנת לדירוג כלל.
```

**Group (c) — form or tolerance concern (8/18: #1, #2, #11, #12, #13, #14, #16, #17 — amended count per SLOT 11; caption text unchanged, still accurate for the remaining 8):**
```text
הסתייגות על הצורה הכימית או על סבילות עיכולית
```
```text
אצל המוצרים האלה יש ממצא קבוע על הצורה הכימית עצמה, או מינון שנמצא בגובה הסף לתשומת לב עיכולית. ממצא כזה לא משתנה כמה שלוקחים מהמנה המצוינת על התווית.
```

**Group (d) — insufficient label information (1/18: #18):**
```text
מידע לא מספיק על התווית
```
```text
התווית של המוצר הזה לא מגלה מספיק כדי לדעת אילו מגנזיום, כמה, או שניהם.
```

---

## SLOT 6 — All 18 per-product lines (`oneLinerHe`)

**Maps to:** `products[]` array, lines 210–416. Real numbers, forms and barcodes are unchanged (mechanical `doseMg`/`formHe`/`identity()` fields untouched — only `oneLinerHe` and `bucket` assignment change). Group letter shown for each; `classifierHe` is a new, optional short phrase Frontend may render as a sub-badge — originally scoped to Group (c) only, extended per SLOT 11 to the 4 rows that moved into Group (b) with an evidence-limited form (#5, #7, #8, #10), so a reader isn't left to infer the form nuance from prose alone. The other 5 original Group (b) rows (#3, #4, #6, #9, #15) intentionally carry no classifier — out of this amendment's narrow scope; flagged in SLOT 11 as a candidate for a future consistency pass, not silently done here.

**#1 — מגנזיום ציטראט+B6, סופהרב (250 מ"ג, ציטראט) — Group (c), tolerance-note only**
`classifierHe`: `צורה נקייה, הערת סבילות בלבד`
```text
מגנזיום ציטראט+B6, סופהרב נותן 250 מ"ג מגנזיום יסודי במנה היומית המצוינת על התווית, בצורת ציטראט: אחת הצורות שה-NIH ODS מונה במפורש כבעלות ספיגה טובה יותר מאוקסיד. הצורה והתיוג נקיים. המינון נמצא בדיוק בגובה סף 250 מ"ג ליום שמעליו EFSA ממליצה על תשומת לב לאי-נוחות עיכולית אפשרית.
```

**#2 — מגנזיום ביסגליצינט, אלטמן (250 מ"ג, ביסגליצינט) — Group (c), tolerance-note only**
`classifierHe`: `צורה נקייה, הערת סבילות בלבד`
```text
מגנזיום ביסגליצינט, אלטמן נותן אותו מינון: 250 מ"ג מגנזיום יסודי במנה היומית, בצורת ביסגליצינט. הצורה והתיוג נקיים כאן גם, והמינון נמצא באותו סף 250 מ"ג לתשומת לב עיכולית. ביסגליצינט נחשב בפועל צורה בעלת ספיגה טובה, אבל ה-NIH ODS לא מזכיר אותה בשמה בכלל, וההוכחה הישירה חלשה מכדי לדרג את הספיגה שלה בביטחון לצד ציטראט.
```

**#3 — מגנזיום ציטראט 120, אלטמן (200 מ"ג, ציטראט) — Group (b)**
```text
מגנזיום ציטראט 120, אלטמן נותן 200 מ"ג מגנזיום יסודי במנה היומית, בצורת ציטראט. הצורה, הבטיחות והתיוג נקיים לגמרי. 200 מ"ג נמצא מעל החציון של 15 המוצרים עם מינון יסודי ברור (190 מ"ג), אך עדיין בחצי הנמוך של הטווח המלא (76 עד 520 מ"ג).
```

**#4 — מגנזיום WELL, נוטריקר (168 מ"ג, ביסגליצינט) — Group (b)**
```text
מגנזיום WELL, נוטריקר נותן 168 מ"ג מגנזיום יסודי במנה היומית, בצורת ביסגליצינט: צורה שנחשבת בפועל בעלת ספיגה טובה, אבל ההוכחה הישירה לכך מוגבלת מכדי לדרג אותה בביטחון לצד ציטראט. הבטיחות והתיוג נקיים. 168 מ"ג נמצא מתחת לחציון של 15 המוצרים עם מינון יסודי ברור (190 מ"ג), באמצע-התחתון של הטווח המלא.
```

**#5 — אנטי לג קרמפס, NT L.C. (190 מ"ג, הידרוקסיד) — Group (b) (moved from Group (c) per SLOT 11 / §11), evidence-limited form**
`classifierHe`: `צורה ידועה, ראיות מוגבלות לדירוג`
```text
אנטי לג קרמפס, NT L.C. נותן 190 מ"ג מגנזיום יסודי במנה היומית, בדיוק בחציון של 15 המוצרים עם מינון יסודי ברור, בצורת הידרוקסיד. הבטיחות והתיוג נקיים. הצורה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות. שם המוצר מתמקד בעוויתות שרירים: סקירת קוקריין משנת 2020 (Garrison et al., PMID 32956536) בדקה בדיוק את זה אצל מבוגרים עם עוויתות שרירים רגילות (שאינן קשורות להריון או לפעילות גופנית). הסקירה לא מצאה תמיכה קלינית משמעותית למגנזיום כתוסף מונע באוכלוסייה הזו.
```

**#6 — ביסגליצינט 600 כמוסות, פול-מג הדס (122 מ"ג, ביסגליצינט) — Group (b), the "600" correction**
```text
ביסגליצינט 600 כמוסות, פול-מג הדס נותן 122 מ"ג מגנזיום יסודי במנה היומית, בצורת ביסגליצינט: אותה צורה שנחשבת בפועל טובה לספיגה, אך ההוכחה הישירה לכך מוגבלת מכדי לדרג אותה בביטחון. ה-600 בשם המוצר הוא מספר הכמוסות באריזה בלבד. זה אינו מיליגרם מגנזיום, וזה מצוין בבירור על התווית. הצורה, הבטיחות והתיוג נקיים. 122 מ"ג נמצא ברבע התחתון של הטווח שנבדק (76 עד 520 מ"ג).
```

**#7 — מגנזיום מלאט, טינק (136 מ"ג, מלאט) — Group (b) (moved from Group (c) per SLOT 11 / §11), evidence-limited form**
`classifierHe`: `צורה ידועה, ראיות מוגבלות לדירוג`
```text
מגנזיום מלאט, טינק נותן 136 מ"ג מגנזיום יסודי במנה היומית, בצורת מלאט. הבטיחות והתיוג נקיים; 136 מ"ג נמצא בחלק התחתון של הטווח שנבדק (76 עד 520 מ"ג). הצורה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות.
```

**#8 — מגנזיום מלאט, נוטריקר (כ-135 מ"ג, מלאט) — Group (b) (moved from Group (c) per SLOT 11 / §11), evidence-limited form + label gap**
`classifierHe`: `צורה ידועה, ראיות מוגבלות לדירוג; פער תיוג נוסף`
```text
מגנזיום מלאט, נוטריקר נותן כ-135 מ"ג מגנזיום יסודי במנה היומית, גם הוא בצורת מלאט. הבטיחות תקינה. יש כאן גם פער תיוג: האריזה מציינת רק את משקל התרכובת (700 מ"ג מלאט), בלי לחשב את הכמות היסודית בעצמה. הצורה עצמה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות, כמו אצל מוצר המלאט הקודם.
```

**#9 — סידן ומגנזיום +D3, סולגר (100 מ"ג, תערובת אוקסיד+ציטראט) — Group (b), dominant reason (unaffected by SLOT 11 — form stays `cannot_verify`, a different state than `evidence_limited`)**
```text
סידן ומגנזיום +D3, סולגר נותן 100 מ"ג מגנזיום יסודי במנה היומית, מספר שכן מצוין בבירור על התווית. 100 מ"ג נמצא בחלק התחתון של הטווח שנבדק. הצורה היא תערובת אוקסיד וציטראט ביחס שלא מפורסם, כך שאי אפשר לדרג את הספיגה של התערובת הספציפית הזו בנפרד.
```

**#10 — מגנזיום טאוראט, נוטריקר (76 מ"ג, טאוראט) — Group (b) (moved from Group (c) per SLOT 11 / §11), evidence-limited form**
`classifierHe`: `צורה ידועה, ראיות מוגבלות לדירוג`
```text
מגנזיום טאוראט, נוטריקר נותן 76 מ"ג מגנזיום יסודי במנה היומית, המינון הנמוך ביותר בין 15 המוצרים עם מינון יסודי ברור, בצורת טאוראט. הבטיחות והתיוג נקיים. הצורה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות, כמו אצל צורת המלאט.
```

**#11 — מגנזיום אוקסיד 520, נוטריקר (520 מ"ג, אוקסיד) — Group (c), weaker form + crosses UL**
`classifierHe`: `צורה בספיגה נמוכה, חוצה סף בטיחות`
```text
מגנזיום אוקסיד 520, נוטריקר נותן 520 מ"ג מגנזיום יסודי במנה היומית, המינון הגבוה ביותר בין 18 המוצרים שנבדקו, בצורת אוקסיד. ה-NIH ODS מונה במפורש את אוקסיד כצורה עם ספיגה נמוכה יותר מציטראט, אספרטט, לקטט וכלוריד. 520 מ"ג חוצה גם את סף ה-350 מ"ג ליום שקבע המכון האמריקאי לרפואה (IOM/NASEM) למגנזיום מתוסף. זו אזהרת מינון גלויה על התווית, מעבר לממצא הספיגה.
```

**#12 — מגנזיום 520, אלטמן (520 מ"ג, אוקסיד) — Group (c), same as #11**
`classifierHe`: `צורה בספיגה נמוכה, חוצה סף בטיחות`
```text
מגנזיום 520, אלטמן נותן אותו מינון בדיוק כמו המוצר הקודם: 520 מ"ג מגנזיום יסודי במנה היומית, בצורת אוקסיד. אותם שני ממצאים חוזרים כאן: אוקסיד נספג פחות טוב לפי NIH ODS, והמינון חוצה את סף ה-350 מ"ג ליום.
```

**#13 — מגנזיום UP, אלטמן (450 מ"ג, אוקסיד) — Group (c)**
`classifierHe`: `צורה בספיגה נמוכה, חוצה סף בטיחות`
```text
מגנזיום UP, אלטמן נותן 450 מ"ג מגנזיום יסודי במנה היומית, גם הוא בצורת אוקסיד. המינון נמוך במקצת מהשניים הקודמים, אבל עדיין חוצה את סף ה-350 מ"ג ליום, ואותה מגבלת ספיגה של אוקסיד חלה כאן.
```

**#14 — מגנזיום באלאנס, אלטמן (450 מ"ג, אוקסיד) — Group (c)**
`classifierHe`: `צורה בספיגה נמוכה, חוצה סף בטיחות`
```text
מגנזיום באלאנס, אלטמן נותן 450 מ"ג מגנזיום יסודי במנה היומית, בצורת אוקסיד, עם אותו ממצא ספיגה ואותה חציית סף בטיחות כמו שני המוצרים הקודמים. אשווגנדה וולריאן מופיעים גם הם על התווית, אבל הם לא חלק מהבדיקה של המגנזיום עצמו.
```

**#15 — נאנו מגנזיום ליפוזומלי, נוטריקר (88 מ"ג, ביסגליצינט בסיס) — Group (b)**
```text
נאנו מגנזיום ליפוזומלי, נוטריקר נותן 88 מ"ג מגנזיום יסודי במנה היומית, בצורת בסיס ביסגליצינט: צורה שנחשבת בפועל טובה לספיגה, אך ההוכחה הישירה לכך מוגבלת מכדי לדרג אותה בביטחון. הבטיחות והתיוג נקיים. 88 מ"ג הוא המינון השני הנמוך ביותר בין 15 המוצרים עם מינון יסודי ברור. הכיתוב "נאנו ליפוזומלי" על האריזה הוא טענת שיווק נפרדת: לא מצאנו במקורות שבדקנו עדות לשיפור ספיגה מעבר לצורת הבסיס עצמה.
```

**#16 — מגנזיום אוקסיד 520, טינק, 90 כמוסות (מינון לא ניתן לאימות, אוקסיד) — Group (c)**
`classifierHe`: `צורה בספיגה נמוכה, מינון לא ניתן לאימות`
```text
מגנזיום אוקסיד 520, טינק (90 כמוסות) מציין 520 על האריזה, אבל התווית לא מבהירה אם זה מגנזיום יסודי או משקל התרכובת, כך שהמינון בפועל לא ניתן לאימות מהתווית. הצורה כן ידועה: אוקסיד, אותה צורה שה-NIH ODS מונה כבעלת ספיגה נמוכה יותר, ללא קשר לאיזו קריאה של "520" נכונה.
```

**#17 — pH מגנזיום, אמורפיקיור (מינון לא ניתן לאימות, קרבונט) — Group (c)**
`classifierHe`: `צורה בספיגה נמוכה, מינון לא ניתן לאימות`
```text
pH מגנזיום, אמורפיקיור לא מפרט על התווית מהו המינון היומי בפועל, כך שהמינון לא ניתן לאימות. הצורה כן ידועה: קרבונט. קרבונט לא מוזכר בשמו במקור ה-NIH ODS, אבל מסווג יחד עם אוקסיד כצורה בעלת ספיגה נמוכה על סמך דמיון כימי בין המלחים בלבד. זה סיווג חלש יותר מציטוט ישיר, וההוכחה לכך חלשה יותר מזו של אוקסיד עצמו.
```

**#18 — TRIOMAG, סופהרב (מינון לא ניתן לאימות, תערובת ציטראט/ביסגליצינט/טאוראט) — Group (d)**
```text
TRIOMAG, סופהרב מציין על התווית תערובת של ציטראט, ביסגליצינט וטאוראט, בלי לפרט את היחס בין השלושה. בלי היחס הזה, אי אפשר לדעת כמה מגנזיום יסודי מגיע בפועל למנה, ואי אפשר לדרג את הספיגה של התערובת הספציפית הזו. זה המוצר היחיד מתוך 18 שנבדקו שבו גם הצורה הכימית עצמה אינה ניתנת לקביעה מהתווית, בנוסף למינון.
```

---

## SLOT 7 — Education-spine sections

**Maps to:** `educationSpine[]`, lines 566–641 (10 sections in the live file). **Consolidated to 5 sections** — this removes the live duplication between "בטיחות" (592–596) and "מינון ובטיחות" (619–623), which say almost the same thing, and folds "הצורות הכימיות, מוסבר שוב בקצרה" (610–617) into the absorption section instead of repeating it. Flagged as an open simplification, not silently dropped — see Open Questions.

**§1 — heading: elemental vs. compound weight**
```text
מגנזיום יסודי מול משקל התרכובת: המספר שבאמת חשוב
```
```text
הספרה הרלוונטית היא כמות המגנזיום היסודי במנה היומית המצוינת על התווית. משקל התרכובת (ציטראט, אוקסיד, ביסגליצינט וכו') שלפעמים מודפס גדול יותר על האריזה הוא מספר אחר לגמרי. הוא לא מלמד ישירות על הכמות היסודית. כשאי אפשר לחשב את המינון היומי בכלל מהתווית, כמו אצל שלושה מהמוצרים שנבדקו, זהו פער מידע על אותו מוצר ספציפי בלבד. זה אינו ממצא על שאר הקטגוריה.
```

**§2 — heading: dose in context (no universal floor)**
```text
המינון בהקשר: איך להעריך מספר בלי סף יחיד
```
```text
אין מחקר שקובע סף בודד שמפריד בין מינון משמעותי למינון שולי עבור תוסף מגנזיום באופן כללי. שני הקשרים כנים אפשר להשתמש בהם במקום זה. ראשית, ביחס לטווח שנמצא בפועל בין 18 המוצרים שנבדקו: מתוך 15 מוצרים עם מינון יסודי ברור על התווית, המינונים נעים בין 76 ל-520 מ"ג ליום, החציון 190 מ"ג. שנית, ביחס לצריכה היומית המומלצת הכללית (RDA) שקבע המכון הלאומי לבריאות האמריקאי (NIH ODS): 310 עד 420 מ"ג ליום, בהתאם לגיל ולמין, מכל המקורות יחד: מזון, משקאות ותוספים כאחד. תוסף בדרך כלל משלים רק חלק מהכמות הזו, וכמה בדיוק תלוי בתזונה של כל אחד. בארי אינה יכולה לדעת את זה מהתווית בלבד.
```

**§3 — heading: absorption, 3 buckets (causal cost claim killed, carbonate weak-basis disclosed)**
```text
צורה כימית וספיגה: שלוש קבוצות ראיות במקום סולם אחד
```
```text
לפי גיליון המידע המקצועי של המכון הלאומי לבריאות האמריקאי (NIH Office of Dietary Supplements) על מגנזיום, ציטראט, אספרטט, לקטט וכלוריד נספגים בגוף בצורה מלאה יותר מאוקסיד וגופרתי (סולפט). מתוך 18 המוצרים שנבדקו, ציטראט הוא הצורה היחידה מהקבוצה הזו שמופיעה בפועל, בשלושה מוצרים. אוקסיד, הצורה הפחות נספגת לפי אותו מקור, מופיע בשישה מוצרים; הוא גם זול לייצור כתרכובת תעשייתית נפוצה, אבל אלה שתי עובדות נפרדות בלבד, בלי יחס של סיבה ותוצאה ביניהן. קרבונט, שמופיע במוצר אחד, אינו מוזכר במקור הזה בשמו: הוא מסווג יחד עם אוקסיד לפי דמיון כימי בין המלחים בלבד, סיווג חלש יותר מציטוט ישיר. שאר הצורות שנמצאו בקטגוריה, ביסגליצינט, מלאט, טאוראט והידרוקסיד, אינן מוזכרות בשמן בגיליון של NIH ODS כלל. ביסגליצינט נחשב לרוב שווה-ערך לציטראט מבחינת ספיגה, אבל מחקרים קטנים שבדקו את זה ישירות נתנו תוצאות מעורבות וחלשות, וזה לא מספיק כדי לדרג אותו באותה רמת ביטחון. ההערכה הכנה לגבי ארבע הצורות האלה: הראיות מוגבלות מכדי לקבוע בביטחון אם הספיגה שלהן טובה או חלשה.
```

**§4 — heading: safety and the upper limit (merged, meta-narration about the "previous page" removed, no capsule-stacking suggestion)**
```text
בטיחות: מתי מינון גבוה עלול להפריע
```
```text
הסף העליון למגנזיום מתוסף (בשונה ממגנזיום שמקורו במזון) הוא 350 מ"ג יסודי ליום, לפי המכון האמריקאי לרפואה (IOM/NASEM). הרשות האירופית לבטיחות מזון (EFSA) קבעה סף רך יותר, 250 מ"ג ליום, במקור בחוות דעת של הוועדה המדעית למזון של האיחוד האירופי (SCF) משנת 2001, ואושרר מחדש בחוות דעת של פאנל התזונה של EFSA משנת 2015. שני הסכומים מתארים את אותה תופעה: מינון גבוה מדי של מגנזיום מתוסף עלול לגרום לשלשול קל וזמני. זו לא רעילות. אנשים עם מחלת כליות, או שנוטלים תרופות מסוימות, צריכים לדבר עם רופא לפני נטילת מינונים גבוהים, ללא קשר לצורה הכימית של המוצר. המדריך הזה מתאר את המנה היומית המצוינת על התווית של כל מוצר בלבד. הוא לא מציע לקחת יותר כמוסות ממה שהיצרן ממליץ.
```

**§5 — heading: what magnesium does, and the narrowed cramps finding**
```text
מה מגנזיום עושה, ולמה זה לא כולל עוויתות שרירים אצל כולם
```
```text
מגנזיום הוא מינרל חיוני שמעורב בתפקוד של שרירים, עצבים ובעצם. תוסף מגנזיום נותן ערך אמיתי כשהתזונה היומית לא מספקת מספיק, בהתאם למינון ולצורה הכימית שנספגת בפועל. הטענה השכיחה ביותר על תוספי מגנזיום, הקלה בעוויתות שרירים, נבדקה בסקירה שיטתית של קוקריין משנת 2020 (Garrison et al., PMID 32956536). אצל מבוגרים עם עוויתות שרירים רגילות (שאינן קשורות להריון או לפעילות גופנית), הסקירה לא מצאה תמיכה קלינית משמעותית למגנזיום כתוסף מונע. אצל נשים בהריון התמונה שונה: הראיות מעורבות, בלי מסקנה שלילית אחידה. משלושה מחקרים שנבדקו: אחד ללא יתרון מובהק, אחד עם יתרון בתדירות ובעוצמת ההתכווצויות, ואחד לא עקבי בתוצאותיו. לגבי עוויתות הקשורות לפעילות גופנית או למחלות שריר ועצב, כלל לא בוצעו מחקרים מבוקרים: זהו פער מחקר בלבד, מעבר לכל ממצא שלילי.
```

---

## SLOT 8 — Sources list (display text + URL, for Frontend to render as clickable links)

**Maps to:** the "מקורות" education-spine section (lines 630–639), now rendered as a **structured list** with URLs rather than prose paragraphs. The banned phrase "אומת באמצעות ציטוטים משניים" (line 633) is removed and NOT replaced with any "verified/מאומת" framing — the source simply states what it supports.

```text
המכון הלאומי לבריאות האמריקאי, המשרד לתוספי תזונה (NIH Office of Dietary Supplements) — גיליון מידע מקצועי על מגנזיום. מקור להיררכיית הספיגה בין הצורות הכימיות, ולטווח הצריכה היומית המומלצת (310–420 מ"ג ליום, מכל המקורות יחד) ולסף העליון של 350 מ"ג ליום למגנזיום מתוסף.
כתובת: https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
```
```text
Garrison, S.R. et al., "Magnesium for skeletal muscle cramps," Cochrane Database of Systematic Reviews, 2020 (PMID 32956536). מקור לממצא שלא נמצאה תמיכה קלינית משמעותית להקלת עוויתות שרירים רגילות אצל מבוגרים, ולראיות הסותרות לגבי הריון.
כתובת: https://pubmed.ncbi.nlm.nih.gov/32956536/
```
```text
הוועדה המדעית למזון של האיחוד האירופי (SCF, חוות דעת 2001) ו-EFSA, פאנל NDA (חוות דעת 2015, אישרור מחדש); מרוכז בדוח הסיכום העדכני של EFSA על רמות עליון נסבלות (אוגוסט 2025). מקור לסף הרך של 250 מ"ג ליום למגנזיום מתוסף.
כתובת: https://www.efsa.europa.eu/sites/default/files/2024-05/ul-summary-report.pdf
```

**Closing methodology line** (kept from the live file, no factual change, matches the assertive-writing doctrine of one footer disclaimer rather than body-copy hedging):
```text
בארי קוראת תוויות. בארי אינה בודקת במעבדה. כל המינונים המוצגים הם מה שכתוב על האריזה הישראלית. המידע כאן הוא לצורך היכרות בלבד. הוא אינו תחליף לייעוץ רפואי.
```

---

## SLOT 9 — Other FAQ/methodology lines that change

**`buyLinkDisclosureLine`** (line 642) — minor edit, "דגלים" replaced with "השיוך לקבוצה" to match the new group model instead of the retired flag-ladder vocabulary:
```text
קישור קנייה אינו משפיע על הכללה, על השיוך לקבוצה או על סדר ההצגה.
```

**`updatedLabel`** (line 643) — date bump to match the "as of July 2026" certification-scope language used in Slot 3 (Frontend/Product to confirm against actual ship date):
```text
18 מוצרים · יולי 2026
```

**`expanderLabels`** (lines 550–553) — unchanged, no science content:
```text
הצג את הסולמות
```
```text
הסתר את הסולמות
```

**Dose gauge tick labels** (spec §3 "gauge geometry" — geometry itself is a Design/Frontend build item, not Content's, but the tick-label TEXT is copy and is supplied here per spec §3's explicit requirement that Nutrition/Content own the label wording):
```text
חציון בין 15 מוצרים עם מינון ברור
```
```text
מכל המקורות יחד — לא רק תוסף
```
(Second label is the mandatory qualifier attached to the RDA-all-sources band, 310–420 mg, per spec §3 "gauge geometry" — must render wherever that band appears, never presented as a bare number.)

**Retired fields** — no new copy authored for these; they belong to the ranked-tier model being retired for this guide (see Open Questions #1):
- `recommendationTierCaptions` (very_recommended / recommended / good / not_recommended captions)
- `veryRecommendedEmptyStateHe`
- `cannotAssessSectionIntroHe` (superseded by the Group (d) caption in Slot 5)

---

## SLOT 10 — Adjacent-surface stale strings (hub card + page metadata)

**Added post-integration:** Frontend wired Slots 1–9 into the page cleanly with zero missing-copy escalations, but flagged two stale strings on surfaces adjacent to the guide page itself — outside `magnesium-guide-data.ts`, so outside this package's original scope. Both still said "שישה דברים" / named `בדיקת צד שלישי והוגנות מחיר` as assessed, which contradicts the signed 4-criteria model. Replacements below are consistent with Slots 1–9: 4 assessed criteria, price/third-party never named as assessed, no "X, לא Y" phrasing, em dashes minimized (none used), scoped to the 18 reviewed products.

**#10a — Hub card description.**
**Maps to:** `bari-web/src/lib/guides/madrichim-categories.ts`, `MADRICHIM_CATEGORIES` array, the `magnesium-guide` entry's `description` field (line 38). Old string named "שישה דברים" and framed the guide as answering whether a product is "worth the money" — a claim price data (never collected) cannot support. New string names the 4 assessed criteria only and drops the worth-the-money framing entirely; no geographic completeness claim is made (no "מהמדף הישראלי").
```text
בדקנו 18 תוספי מגנזיום לפי ארבעה דברים שאפשר לבדוק ישירות מהתווית: מינון יסודי, צורה כימית, בטיחות ושקיפות התיוג.
```

**#10b — Page metadata description.**
**Maps to:** `bari-web/src/app/madrichim/magnesium/page.tsx`, `export const metadata: Metadata`, the `description` field (line 32). Old string named `בדיקת צד שלישי והוגנות מחיר` as part of what Bari checked — these are the two market-information gaps (Slot 3), never assessed criteria. New string names the same 4 criteria as Slots 1–2, SEO register, 141 characters (≤160 limit).
```text
בארי בדקה 18 תוספי מגנזיום הנמכרים בישראל לפי מינון מגנזיום יסודי, צורה כימית, בטיחות ושקיפות תיוג, כדי להראות מה לחפש על התווית לפני שקונים.
```

**Self-check on both:** `hebrew_readability.analyze().is_clean` — True for both (hub_card 113 chars, meta_desc 141 chars, zero HARD leaks, zero antithesis hits). `hebrew_grammar_gate.analyze().is_clean` — hub_card True; meta_desc carries 3 `confidence="medium"` flags, all the same documented closest-noun mis-anchoring already characterized above (`הנמכרים` correctly agrees with the plural `תוספי`, not the singular `מגנזיום` it got anchored to; `שקונים` correctly refers to an implicit "people who buy," not `התווית` the parser anchored to) — reviewed, no genuine agreement error, no change made.

---

## SLOT 11 — §11 QA Gate-2 ruling amendment (evidence_limited form state, regroup to 0/9/8/1)

**Trigger:** Adversarial QA gate-2 NO-GO (HIGH-1: bisglycinate rows showed `formAbsorption` = PASS badge next to prose saying its absorption evidence is too limited to rank against citrate — a same-row contradiction). Nutrition D6 ruling (spec §11, sha256 `f17305132482d2e7b68fb988d6b682c5275dd62badafd7f6b6e80819353a29fc`), Product D7 co-signed: introduce a new, off-ladder `evidence_limited` state for ALL 8 Bucket-3-form rows (#2, #4, #5, #6, #7, #8, #10, #15), not bisglycinate alone. Confirmed knock-on: #5, #7, #8, #10 move from Group (c) to Group (b) (their form concern was the only thing keeping them in (c); once `evidence_limited` is neutral for §2 grouping purposes, each falls through to its own independently-determinate dose finding). #2, #4, #6, #15 do NOT change group (their group membership was never form-driven). Updated distribution: **a:0, b:9, c:8, d:1** (of 18).

**Narrow scope applied:** only the 4 items below, plus the item-5 grep sweep. Slots 4, 5, and 6 were edited in place above (not left stale with a contradicting appendix) since they are internal to this same package — maps-to references below point at the corrected locations.

### 11.1 — New consumer string: `evidence_limited` form-bar label

**Maps to:** a NEW string, no prior slot — this is the off-ladder label the `formAbsorption` bar must render for the 8 rows in the table above, once Frontend implements the `evidence_limited` `GuideBarState`/rendering path (Frontend/Product implementation decision per spec §11, not authored here). Must NOT be "לא ניתן לאימות" (asserts missing data; the form here is known, only ranking confidence is limited) and must not read as a middle rung of the נמוכה/בינונית/גבוהה ladder — it renders off that ladder entirely, same non-ordinal treatment `cannot_verify` already gets for `thirdPartyVerification`/`priceFairness` in this file.

**Short label** (bar-label register, matching the length class of "גבוהה"/"בינונית"/"נמוכה"):
```text
ראיות מוגבלות לדירוג
```

**Longer tooltip/expansion variant** (for the per-row expander, alongside the other bar detail text):
```text
הצורה הכימית ידועה ומצוינת על התווית. הראיות לדירוג הספיגה שלה בביטחון, מול ציטראט, מוגבלות מדי כרגע.
```

### 11.2 — Group (b) caption qualified for its 9-member, mixed-form composition

**Maps to:** Slot 5, Group (b) header + caption (corrected in place above). Old caption made a blanket "form is clean" claim that was true for the original 5 members but is not true for 7 of the new 9 (only #3 is confirmed-good citrate; #9 is an undisclosed-ratio blend, `cannot_verify` — a different, unaffected state; the remaining 7 are `evidence_limited`). New caption names all three sub-cases inside the one caption slot, per Product's binding condition, without splitting into multiple captions.

**11.2-rev (post-QA-GO, one MEDIUM fixed before deploy):** the 11.2 caption's opening sentence still over-claimed — "ללא הסתייגות בטיחות **או תיוג**" asserted zero label reservation across all 9, but #8 (מגנזיום מלאט, נוטריקר) carries a disclosed label-transparency gap (the 700 mg compound-mass-only label, named on #8's own row and in its `classifierHe`). Safety IS clean for all 9 — that half of the claim stood. Label is clean for 8 of 9, not 9 of 9. Revised the caption (in place, Slot 5, above) to split the safety and label claims apart: safety stated as clean for all nine; label stated as clean for eight, with one product's disclosed gap acknowledged (not denied) without naming it in the caption — the row itself already names it. The three form sub-cases (citrate / evidence-limited / undisclosed blend) are unchanged. No "X, לא Y" construction, no em dash.

### 11.3 — Four moved rows re-authored for Group (b) membership

**Maps to:** Slot 6, products #5, #7, #8, #10 (corrected in place above). Each now leads with dose as the determinate Group-(b) driver, states the form as known-but-evidence-limited (using the standardized 11.1 phrasing "הצורה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות" for consistency across all 4), and drops any form-as-concern framing. `classifierHe` decision: extended to these 4 moved rows only (not retroactively to the original 5 Group-(b) rows, out of today's narrow scope — flagged as a follow-up candidate, not silently expanded).

### 11.4 — Headline rescoped to citrate alone (MEDIUM-1)

**Maps to:** Slot 4, `headlineFinding.title` + `body[0]` (corrected in place above). Verified against all 18 rows before writing: citrate appears in exactly 2 products (#1 at 250 mg, #3 at 200 mg — both ≤250 mg, both Bucket-1 per §5); bisglycinate appears in exactly 4 products (#2, #4, #6, #15, ranging 88–250 mg). The rewritten title and body[0] state the market-structure claim on citrate alone, mention bisglycinate only descriptively with its own range, and never share "מומלצת" or any evaluative adjective between the two forms in the same clause.

### 11.5 — Grep sweep for other stale co-attribution or blanket form-cleanliness claims

Ran `grep -n "ציטראט או ביסגליצינט\|ביסגליצינט או ציטראט"` and `grep -n "מומלצת\|מומלץ"` across the full package. Findings:
- The literal "ציטראט או ביסגליצינט" co-attribution occurred in exactly one place — the headline body[0] (now fixed, §11.4).
- "מומלצת" occurred in 4 places total: the headline title + body[0] (both fixed, §11.4); two mentions of "הצריכה היומית **המומלצת**" (the RDA reference intake — Slot 7 §2 and Slot 8 sources) — unrelated to form endorsement, describes NIH's recommended daily intake value, not a product/form claim, no change needed; one meta-reference inside this package's own Open-Questions section documenting the `EXCEPTION-003` tier-word rule — documentation, not consumer copy, no change needed.
- Slot 7 §3 (the absorption 3-buckets education section) already stated the bisglycinate-vs-citrate evidence gap correctly in the original package (written before this ruling existed, but already spec-compliant by construction — it never applied "מומלצת" to bisglycinate and explicitly says its evidence is insufficient to rank it at citrate's confidence level). No change needed there.
- No other blanket "form is clean across the board" claim was found outside the Group (b) caption already fixed in §11.2.

### Self-check

`hebrew_readability.analyze().is_clean` — True for all new/amended strings in this slot (11.1's 2 strings, 11.2's 1 caption, 11.3's 4 one-liners + 4 classifierHe strings, 11.4's 2 strings) — zero HARD leaks, zero antithesis hits, confirmed via full-file re-run below. `hebrew_grammar_gate.analyze().is_clean` — reviewed per the same protocol as the rest of the package; any `confidence="medium"` flags follow the same documented closest-noun false-positive pattern already characterized above, no `confidence="high"` flags, no genuine agreement errors found on manual review.

---

## Open questions for Frontend (flagged per Spec-Conflict Duty — not silently resolved)

1. **The group model needs a data-shape decision I cannot make from Content alone.** `GuideBucket` in `bari-web/src/lib/view-models/guide.ts` already has exactly 4 values (`clears_all` / `passes_with_flag` / `fails` / `cannot_assess`), and two of them line up 1:1 with the new model (`clears_all` = Group a, `cannot_assess` = Group d, both empty/single-product respectively in both models). But the OLD `passes_with_flag`/`fails` split was severity-based (any FAIL present → `fails`); the NEW Group (b)/(c) split is concern-type-based per the spec §2 precedence rule, regardless of FLAG vs FAIL. Two products in the current `fails` bucket (e.g. #6, #9, #15) need to move into what would become Group (b), and three current `passes_with_flag` products (#1, #2, #5) need to move into Group (c). **Recommendation:** reuse the existing `GuideBucket` enum values with reassigned per-product membership (per spec §2's table, already co-signed) and relabel `GUIDE_BUCKET_LABELS_HE` with the Slot 5 headers above — this is the smallest diff. **Risk:** `GUIDE_BUCKET_LABELS_HE` is a shared, cross-guide constant; if creatine's guide still uses the old severity-based bucket semantics, a global relabel would break creatine's copy. Frontend/Product must decide: relabel globally (only safe if creatine is re-audited too), or add a magnesium-specific override. I have not touched any `.ts` file — this is a structural call outside Content's lane.
2. **No existing field carries a caption per `GuideBucket`.** `recommendationTierCaptions` captions the retired `GuideRecommendationTier` (a *derived* ranked layer on top of bucket), not the bucket itself. The Slot 5 group captions in this package need either a new `bucketCaptionsHe: Partial<Record<GuideBucket, string>>` field, or reuse of `recommendationTierCaptions` if Frontend retires the tier-derivation logic (`dose_adequacy_sole_caveat` predicate) for magnesium entirely, since Group (b)/(c) is now a flat, non-ranked 4-way split that the tier layer's ranking logic no longer applies to.
3. **`EXCEPTION-003`** in `guide.ts` sanctions "מומלץ"/"מומלץ מאוד"/"טוב"/"לא מומלץ" as tier-heading field values only. None of the Slot 5 group headers use these words — confirmed clean against that constraint by design, not by exemption.
4. **Gauge geometry itself** (`MAGNESIUM_DOSE_GAUGE`, lines 96–106) needs a Design/Frontend rebuild per spec §3 ("corpus range shading, not pass/fail zones" + the RDA band) — out of Content's lane. The two tick-label strings needed for that rebuild are supplied in Slot 9 above so Design isn't blocked waiting on copy.
5. **Median correction (168 → 190 mg)** was Nutrition/Product's mid-flight fix to the spec itself; I'm told Nutrition is patching `mag_guide_v2_nutrition_spec.md` separately. This copy package already reflects the corrected 190 mg figure throughout — if the patched spec lands with a different number, Slot 6 (#3, #4, #5) and Slot 7 §2 need a second pass.
6. **Bisglycinate PMIDs (3 small studies referenced in the live copy's old "מקורות" section, lines 636–637)** — the nutrition spec describes these narratively (a 2024 human study with an undisclosed conflict of interest, a 2019 mouse study, a 1994 12-patient study) but does not supply verifiable PMIDs for them. Per the project's citation-fabrication gate, I did NOT carry these specific claims (COI, mouse study, 4-of-12 subgroup) into this copy package's Sources slot, since I cannot independently verify them. The general, unverifiable-detail-free statement ("מחקרים קטנים שבדקו את זה ישירות נתנו תוצאות מעורבות וחלשות") is used instead in Slot 7 §3. If Nutrition can supply verifiable PMIDs for these three studies, they can be added to Slot 8 in a follow-up pass.
7. **Zhang et al. (PMID 27402922, the blood-pressure/300mg study)** is in the nutrition spec's verified source table but is NOT cited anywhere in this consumer copy package, because the killed 300 mg framing was the only claim it supported in the old copy. I deliberately left it out of the public Sources list (Slot 8) rather than include an unused citation. Flagging in case Nutrition/QA wants it listed anyway for transparency about what was checked and ruled out.

---

## Self-check performed

Ran `integrations/clients/hebrew_readability.py` (`analyze().is_clean`) and `integrations/clients/hebrew_grammar_gate.py` (`analyze().is_clean`) against all fenced ` ```text ` blocks in this file (57 in the original package, 59 after Slot 10, 61 after Slot 11, 61 after the SLOT 11.2-rev caption fix — a revision in place, not a new block), via a scratch extraction script (`hebrew_readability`/`hebrew_grammar_gate` imported directly, no network).

**Readability/leakage/antithesis gate (HARD): 61/61 clean (57/57 original + 2/2 Slot 10 + Slot 11's blocks, including the 11.2-rev caption fix).** Iterated through 3 passes on the original package — the first pass found 12 blocks tripping the antithesis rule (`",\s*לא\b" / "\bולא\b" / "\bאלא\b"`, the mechanical form of the CLAUDE.md "no X-not-Y phrasing" ban), all rewritten to avoid comma-לא / ולא / אלא constructions while preserving meaning (e.g. splitting into two sentences, or "מעבר ל…" / "בלי קשר ל…" / "(שאינן קשורות ל…)" instead of a negation clause). Slot 10's two strings and Slot 11's amended/new strings were clean on first draft. No framework-leakage, score-mechanic, recommendation-language, sodium-term, or brand-spelling hits at any point.

**Grammar/agreement gate (DictaBERT-morph): 24/61 fully clean; the remaining 37 carry only `confidence="medium"` flags — zero `confidence="high"` flags anywhere.** Per the standing protocol, medium-confidence flags are candidates for human review, not an auto-fail. I reviewed every flag individually. The overwhelming majority (~95%) are the tool's documented limitation ("closest preceding NOUN/PRON" anchoring — see the module's own "HONEST LIMITS" docstring) misidentifying the true grammatical head in construct chains and coordinated NPs, e.g.:
- `בדיקת צד שלישי` flagged as a gender mismatch — this is pre-existing, already-shipped Bari terminology (`GUIDE_BAR_LABELS_HE.thirdPartyVerification` in `guide.ts` line 52, and lines 457/512/582 of the current live file) where `שלישי` (masc) correctly modifies `צד` (masc), not the construct-fem `בדיקת` the tool anchored to.
- `המכון הלאומי לבריאות האמריקאי` flagged similarly — also pre-existing shipped terminology (lines 594/621/634 of the current live file); `האמריקאי` correctly modifies `המכון` (masc), several words back, not the intervening `לבריאות` (fem).
- Mixed-gender coordination defaulting to masculine plural (`הצורה, הבטיחות והתיוג נקיים` — standard Hebrew: masculine-plural is the default agreement for a mixed-gender compound subject) was flagged repeatedly as if the adjective had to agree with the nearest single noun.
One **genuine clarity issue** did surface on manual review (not from a specific flag, but while reading the flagged sentence closely): the cramps-population sentence originally risked a garden-path reading ("cramps that are not pregnant"). Fixed by rephrasing to `עוויתות שרירים רגילות (שאינן קשורות להריון או לפעילות גופנית)` in both the product #5 row and the Slot 7 §5 education text. No other genuine agreement errors were found. Full flag list preserved in this task's scratch directory for QA's independent re-check if wanted.

```json
{
  "task": "TASK-575",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "02_products/supplements/magnesium/mag_guide_v2_copy_package.md", "action": "modified", "sha256": "RECOMPUTE_AT_ACCEPT (self-referential file; last command_run sha256sum is the authoritative pre-this-edit value, see agent's final chat message for the exact post-edit hash)"}
  ],
  "counts": {
    "products_covered": "18/18 (magnesium-guide-data.ts products array, lines 210-416)",
    "fenced_hebrew_blocks_authored": "61/61 (57 original + 2 Slot 10 + Slot 11 amendments, all blocks in this file)",
    "readability_leakage_antithesis_clean": "61/61 (hebrew_readability.analyze().is_clean, HARD gate)",
    "grammar_fully_clean": "24/61 (hebrew_grammar_gate.analyze().is_clean)",
    "grammar_high_confidence_flags": "0/61 (all remaining flags are confidence=\"medium\", human-reviewed per standing protocol, classified false-positive except 1 genuine clarity fix applied pre-Slot-11)",
    "groups_distribution": "a:0, b:9, c:8, d:1 (of 18) — amended per SLOT 11 / spec §11 (Nutrition D6, Product D7 co-signed); supersedes the earlier a:0,b:5,c:12,d:1 distribution",
    "rows_moved_c_to_b": "4/4 (#5, #7, #8, #10 — per §11 evidence_limited ruling)",
    "median_correction_applied": "190mg used in every dose-comparison slot that references it (product #3, #4, #5, Slot 7 §2 x2)",
    "slot10_char_lengths": "hub_card:113 chars, meta_desc:141/160 chars (SEO limit)",
    "slot11_grep_sweep": "2/2 stale co-attribution instances found and fixed (headline title + body[0]); 0 other instances found across the full file",
    "slot11_2_rev_scope_fixed": "1/1 (safety-vs-label cleanliness split into two sentences; safety clean 9/9, label clean 8/9 with 1 disclosed gap acknowledged not denied, #8 not named in the caption)"
  },
  "commands_run": [
    {"cmd": "python check_readability.py (hebrew_readability.analyze over all fenced blocks, re-run after Slot 11)", "exit_code": 0},
    {"cmd": "python check_grammar.py (hebrew_grammar_gate.analyze over all fenced blocks, re-run after Slot 11)", "exit_code": 0},
    {"cmd": "python slot10_check.py (hebrew_readability + length check on the 2 Slot 10 strings)", "exit_code": 0},
    {"cmd": "python slot10_grammar.py (hebrew_grammar_gate on the 2 Slot 10 strings)", "exit_code": 0},
    {"cmd": "grep -n \"ציטראט או ביסגליצינט|ביסגליצינט או ציטראט\" mag_guide_v2_copy_package.md (Slot 11 item 5 sweep, pre-fix)", "exit_code": 0},
    {"cmd": "grep -n \"מומלצת|מומלץ\" mag_guide_v2_copy_package.md (Slot 11 item 5 sweep, pre-fix)", "exit_code": 0},
    {"cmd": "sha256sum mag_guide_v2_nutrition_spec.md (verify coordinator-supplied hash before reading §11)", "exit_code": 0},
    {"cmd": "python check_readability.py (re-run after SLOT 11.2-rev caption fix)", "exit_code": 0},
    {"cmd": "python check_grammar.py (re-run after SLOT 11.2-rev caption fix)", "exit_code": 0},
    {"cmd": "sha256sum mag_guide_v2_copy_package.md", "exit_code": 0}
  ],
  "not_done": [
    "Sources slot does not include verifiable PMIDs for the 3 small bisglycinate-absorption studies described narratively in the nutrition spec (no PMIDs supplied by spec) — flagged as Open Question 6, not silently included",
    "Zhang et al. PMID 27402922 (the killed 300mg/BP citation) intentionally omitted from the public Sources list since no surviving consumer claim rests on it — flagged as Open Question 7",
    "GuideBucket/recommendationTierCaptions field-shape change needed for Frontend to actually render the 4 descriptive groups is NOT implemented (out of Content's lane) — flagged as Open Question 1-2 with a recommended minimal-diff path",
    "Gauge geometry (MAGNESIUM_DOSE_GAUGE rebuild) not implemented — Design/Frontend build item; only the 2 required tick-label copy strings are supplied (Slot 9)",
    "evidence_limited GuideBarState/rendering path not implemented — Frontend/Product implementation decision per spec §11; only the 2 required label strings are supplied (SLOT 11.1)",
    "classifierHe NOT retroactively added to the original 5 Group-(b) rows (#3, #4, #6, #9, #15) — out of this amendment's narrow scope per the coordinator's instruction; flagged in SLOT 11.3 as a candidate for a future consistency pass"
  ],
  "self_check": "Acceptance test: every shippable Hebrew string clears hebrew_readability.is_clean (framework-leakage, score-mechanic, recommendation-language, sodium-term, brand-spelling, and antithesis HARD gates) before handoff. Observed: 61/61 clean on final run (post-SLOT-11.2-rev, the last string before deploy). Grammar gate run as an additional honesty check per content-agent.md's mandatory pre-return instruments; 0 high-confidence flags across all 61 blocks, all medium-confidence flags manually reviewed with reasoning recorded above and in SLOT 11's self-check; the 11.2-rev caption fix introduced zero new flags. Group distribution a:0/b:9/c:8/d:1 verified to sum to 18 and matches spec §11's table exactly. The QA-flagged over-claim (caption denying #8's disclosed label gap) is corrected: safety stated clean for 9/9, label stated clean for 8/9 with the ninth acknowledged (not named, not denied)."
}
```
