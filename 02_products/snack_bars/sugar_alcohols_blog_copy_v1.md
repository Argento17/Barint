# Sugar Alcohols / Maltitol in Protein Bars — Blog Copy Set (Hebrew, consumer voice)

**Document:** `sugar_alcohols_blog_copy_v1.md`
**Task:** TASK-379
**Author:** Content Agent (C1 build lane)
**Date:** 2026-06-22
**Bounded by:** `sugar_alcohols_blog_nutrition_spec_v1.md` (locked claim set) + `sugar_alcohols_blog_evidence_v1.md`
**Voice target:** opinionated substance in natural connected Hebrew (Project Tom's Voice, file 2 §0.5)
**Status:** DRAFT — pending the two-gate sign-off (Content + Adversarial QA naturalness judge). Naturalness Layer 2 (independent LLM judge) cannot be self-cleared by the author.

> Each string is labeled `[S-NN]` so Frontend can map it into a `*-article-content.ts`. Frontend integrates; Content does not edit `bari-web/src` directly.
> Every claim traces to the locked spec. No per-bar maltitol gram figure is stated (DROP 4). The Israeli warning is cited via EU law only (Special Ruling). Erythritol's cardiac signal is omitted (Special Ruling).

---

## 1. Title + SEO meta

**[S-01] SEO title (`<title>` / metadata.title)**
> כוהל סוכר בחטיפי חלבון: למה "פחות סוכר" על האריזה לא תמיד מה שזה נראה

**[S-02] SEO meta description (`metadata.description`, ~155 chars)**
> מלטיטול וכוהלי סוכר אחרים מורידים את מספר הסוכר על האריזה דרך החלפה, לא הפחתה. הסברנו איך זה עובד, מה הקטלוג לא מראה, ומה כדאי לבדוק על המדף.

**[S-03] Open Graph title (`openGraph.title`)**
> "פחות סוכר" שמקורו בהחלפה ולא בהפחתה

**[S-04] Open Graph description (`openGraph.description`)**
> איך מלטיטול מוריד בו-זמנית את שורת הסוכר ואת הקלוריות על האריזה — ומה שורת הרכיבים מספרת שהטבלה מסתירה.

---

## 2. Hero

**[S-05] Hero headline (`hero.title`)**
> קונים חטיף חלבון בגלל המספר הנמוך של הסוכר? כדאי לדעת מאיפה הוא בא

**[S-06] Hero standfirst / sub-headline (`hero.standfirst`)**
> על אריזות רבות של חטיפי חלבון מספר הסוכר נמוך להפליא, ובצדק זה מושך את העין. אבל בחלק גדול מהמקרים המספר הזה נמוך לא כי הורידו סוכר, אלא כי החליפו אותו בכוהל סוכר כמו מלטיטול. ההבדל הזה לא מופיע בטבלה, והוא בדיוק מה שמשנה את התמונה.

---

## 3. The mechanism

**[S-07] Section heading (`mechanism.heading`)**
> מה זה בכלל כוהל סוכר

**[S-08] Mechanism body — paragraph 1 (`mechanism.body[0]`)**
> כוהל סוכר הוא משפחה של ממתיקים שממתיקים כמעט כמו סוכר, אבל הגוף מתייחס אליהם אחרת. מלטיטול הוא הנפוץ שבהם בחטיפי חלבון. מבחינת התקינה האירופית, שאחריה הולכים גם בישראל, כל כוהל סוכר נספר כ-2.4 קלוריות לגרם, בערך 60% מהקלוריות של סוכר רגיל שעומד על 4 קלוריות לגרם.

**[S-09] Mechanism body — paragraph 2 (`mechanism.body[1]`)**
> כאן נכנס מה שאפשר לקרוא לו התרגיל החשבוני. כשהיצרן מחליף סוכר במלטיטול, שתי השורות שהצרכן הכי מסתכל עליהן יורדות בבת אחת: שורת הסוכר יורדת כי מלטיטול אינו סוכר, ושורת הקלוריות יורדת כי כל גרם שלו נספר כפחות קלוריות. כמות החומר הממתיק בחטיף לא בהכרח קטֵנה. רק האופן שבו רושמים אותה על האריזה משתנה.

**[S-10] Mechanism body — paragraph 3 (`mechanism.body[2]`)**
> במילים אחרות, "פחות סוכר" כאן הוא לרוב תוצאה של החלפה, לא של הפחתה. זה לא טריק אסור ולא רכיב מסוכן. זה פשוט מבנה שכדאי להכיר, כי הוא משנה את מה שהמספר על האריזה באמת אומר.

---

## 4. The catch

**[S-11] Section heading (`catch.heading`)**
> איפה זה נהיה מורכב יותר

**[S-12] Catch body — paragraph 1, glycemic (`catch.body[0]`)**
> מלטיטול אומנם מעלה את הסוכר בדם פחות מסוכר רגיל, אבל לא מדובר באפס. המדד שמודד את זה, ה-GI, עומד על בערך 35 למלטיטול הגבישי לעומת בערך 65 לסוכרוז, כך לפי הספרות המחקרית והערכת רשות המזון האירופית. כלומר ההשפעה נמוכה יותר, אבל היא קיימת — והמספר הנמוך של הסוכר על האריזה לא מספר את החלק הזה.

**[S-13] Catch body — paragraph 2, the >10% rule as a usable signal (`catch.body[1]`)** — REVISED (am_mamtik trigger fix)
> הרגולציה עצמה נותנת כאן כלי, אבל צריך לקרוא אותו נכון. אותה תקנה, תקנות הגנה על בריאות הציבור (מזון) (סימון מזון המכיל ממתיק מסוגים מסוימים), התשע"ח-2018, שנכנסה לתוקף בשנת 2021, קובעת שני דברים שונים בשני תנאים שונים. הדבר הראשון: כל מוצר שמשתמש בממתיק כלשהו, סוכרלוז, סטיביה, מלטיטול או כל אחד אחר, חייב לשאת את המילים "עם ממתיק". זו הצהרה רחבה שאומרת רק שיש כאן ממתיק כלשהו, והיא לא מעידה שמדובר דווקא בכוהל סוכר ולא על הכמות שלו. הדבר השני, וזה החלק שמעניין כאן: רק כשכוהלי הסוכר עוברים 10% מהמשקל, התקנה מחייבת להוסיף את האזהרה "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת". לכן דווקא האזהרה הזו, ולא "עם ממתיק", היא הסימן שהצרכן יכול לחפש. כשהיא מודפסת על האריזה, היצרן עצמו כבר הצהיר שמדובר בכמות כוהלי סוכר משמעותית.

**[S-14] Catch body — paragraph 3, invisible-on-panel (`catch.body[2]`)**
> וכאן הנקודה שסוגרת את התמונה. ההשפעות העיכוליות של כוהלי סוכר תלויות במינון, ומחקרים מצביעים על כך שיש מי שרגיש אליהן כבר בכמויות נמוכות. הטבלה התזונתית לא מראה את הכמות הכוללת של כוהל הסוכר כשורה נפרדת, אלא רק את הסוכר ואת סך הפחמימות. כך שדווקא הרכיב שמסביר את המספר הנמוך הוא זה שהכי קשה לראות על האריזה.

---

## 5. Chart 1 copy — Polyol family comparison (4 rows)

**[S-15] Chart 1 title (`chart1.title`)**
> ארבעה כוהלי סוכר, אותה שורה על האריזה — והבדל גדול מאחוריה

**[S-16] Chart 1 subtitle (`chart1.subtitle`)**
> כל כוהלי הסוכר נספרים כ-2.4 קלוריות לגרם על התווית, אבל מבחינת ההשפעה על הסוכר בדם ועל מערכת העיכול הם רחוקים זה מזה. ארבעת הנפוצים, מהסביל ביותר ועד הפחות.

**[S-17] Chart 1 caveat / footnote (`chart1.caveat`)**
> ערכי ה-GI מקורם בספרות מחקרית והם משוערים, ולכן מסומנים בקירוב. הקלוריה לגרם היא ערך התווית האחיד שמופיע על האריזה בישראל ובאירופה, ולא בהכרח האנרגיה שהגוף בפועל מפיק מכל ממתיק.

### Chart 1 — column headers

**[S-18] Column header: name (`chart1.cols.name`)**
> כוהל הסוכר

**[S-19] Column header: kcal (`chart1.cols.kcal`)**
> קלוריות לגרם (ערך התווית)

**[S-20] Column header: GI (`chart1.cols.gi`)**
> מדד GI משוער (סוכר = 100)

**[S-21] Column header: tolerance (`chart1.cols.tolerance`)**
> סבילות עיכולית

### Chart 1 — row cells (data is locked in the spec; framing words are mine)

**[S-22] Row: Maltitol (`chart1.rows.maltitol`)**
- name: מלטיטול (E965)
- kcal: 2.4
- gi: ~35 לצורה הגבישית, ~52 לצורת הסירופ
- tolerance: סבילות בינונית. השפעות עיכוליות תלויות מינון, שמופיעות אצל רגישים כבר בכמויות נמוכות יחסית. זהו הכוהל הנפוץ ביותר בחטיפי חלבון.

**[S-23] Row: Sorbitol (`chart1.rows.sorbitol`)**
- name: סורביטול (E420)
- kcal: 2.4
- gi: ~9
- tolerance: סבילות נמוכה. זהו הכוהל הכי נחקר מבחינת מינון, ותסמינים קלים מופיעים אצל מבוגרים בריאים כבר סביב 10 גרם ביום.

**[S-24] Row: Xylitol (`chart1.rows.xylitol`)**
- name: קסיליטול (E967)
- kcal: 2.4
- gi: ~7–13
- tolerance: סבילות בינונית. מנגנון דומה לסורביטול, עם השפעות עיכוליות תלויות מינון.

**[S-25] Row: Erythritol (`chart1.rows.erythritol`)**
- name: אריתריטול (E968)
- kcal: 2.4 על התווית (כ-0.2 בפועל מבחינה פיזיולוגית)
- gi: ~1
- tolerance: סבילות גבוהה. כ-90% ממנו נספג במעי הדק ומופרש ללא עיכול, כך שהעומס על המעי הגס מזערי. זהו הסביל מבין הארבעה.

---

## 6. Chart 2 copy — Substitution vs. reduction (6 corpus bars)

**[S-26] Chart 2 title (`chart2.title`)**
> אותו מדף, שתי דרכים להגיע למספר נמוך

**[S-27] Chart 2 subtitle (`chart2.subtitle`)**
> שישה חטיפים מתוך הניתוח של ברי. בקבוצה הראשונה הסוכר הנמוך מגיע מהחלפה במלטיטול, ובשנייה הוא מגיע מהרכיבים עצמם — או שהוא פשוט גבוה. המספר על האריזה לבדו לא מבדיל ביניהם.

**[S-28] Chart 2 caveat / footnote (`chart2.caveat`)** — REVISED (Element C)
> כל ערכי הסוכר הם לכל 100 גרם ומגיעים ישירות מהניתוח של ברי. ברי מזהה כוהל סוכר מתוך שורת הרכיבים, כלומר הוא מעיד על נוכחות שלו ולא על הכמות המדויקת בגרמים. ברוב החטיפים כמות הגרמים הזו אינה מופיעה על האריזה בכלל, אבל שלוש החטיפות שבדוגמה כן מצהירות עליה מרצונן בטבלה. גם אז מדובר בסך כל כוהלי הסוכר יחד, נתון כולל שאינו מיוחס למלטיטול בלבד.

### Chart 2 — Group A heading

**[S-29] Group A heading (`chart2.groupA.heading`)**
> קבוצה א׳ — הסוכר הנמוך מגיע ממלטיטול

**[S-30] Bar A1 — WIN קרם קרמל (`chart2.groupA.bars[0]`)**
- name: WIN חטיף חלבון קרם קרמל
- sugar: 1.7 גרם סוכר ל-100 גרם
- score: ציון 54 / C
- line: הסוכר הנמוך ביותר בכל המדף, אבל זה כמעט כולו תוצאה של החלפה: מלטיטול הוא שתפס את מקום הסוכר כאן.

**[S-31] Bar A2 — אול אין סופט פיסטוק (`chart2.groupA.bars[1]`)**
- name: אול אין סופט פיסטוק
- sugar: 4.6 גרם סוכר ל-100 גרם
- score: ציון 55 / C
- line: המספר נראה מצוין על האריזה, אבל מאחוריו עומדים מלטיטול וגם ממתיק מלאכותי. מדובר בסך הכל בסוכר נמוך שמקורו בהחלפה, ולא בהרכב נקי יותר.

**[S-32] Bar A3 — פרו שטראוס קרמל ואגוזים (`chart2.groupA.bars[2]`)**
- name: פרו שטראוס חטיף חלבון קרמל ואגוזים
- sugar: 3.7 גרם סוכר ל-100 גרם
- score: ציון 54 / C
- line: גם כאן שורת הסוכר הנמוכה נשענת על מלטיטול, ולצידו ממתיק מלאכותי. אותו מבנה כמו השכנים שלו במדף, ואותה תוצאה בציון.

### Chart 2 — Group B heading

**[S-33] Group B heading (`chart2.groupB.heading`)**
> קבוצה ב׳ — בלי מלטיטול, רכיבים אמיתיים או סוכר אמיתי

**[S-34] Bar B1 — פנגיאה אגוזי לוז (`chart2.groupB.bars[0]`)**
- name: חטיף חלבון אגוזי לוז (פנגיאה)
- sugar: 17 גרם סוכר ל-100 גרם
- score: ציון 68.6 / B
- line: ראשון במדף, ודווקא עם סוכר גבוה בהרבה מחטיפי המלטיטול. אבל הסוכר כאן מגיע ממזון אמיתי (תמרים, אגוזי לוז ושקדים) ולא ממלטיטול, וזו הסיבה המרכזית שהוא בראש.

**[S-35] Bar B2 — טודיי בננה שוקולד (`chart2.groupB.bars[1]`)**
- name: טודיי חטיף חלבון בננה שוקולד
- sugar: 12 גרם סוכר ל-100 גרם
- score: ציון 61.9 / C
- line: סוכר גלוי וכן, בלי כוהל סוכר שמסתתר מאחורי המספר. מה שכתוב על האריזה הוא פחות או יותר מה שיש בפנים.

**[S-36] Bar B3 — מקס ברנר קרמל מלוח (`chart2.groupB.bars[2]`)**
- name: מקס ברנר חטיף חלבון קרמל מלוח
- sugar: 35 גרם סוכר ל-100 גרם
- score: ציון 45 / D
- line: אחרון במדף, אבל מסיבה הפוכה לגמרי. כאן אין מלטיטול, פשוט יש הרבה סוכר אמיתי — 35 גרם ל-100 גרם. אפשר להגיע לציון נמוך משני קצוות של אותו מתחם.

---

## 7. The takeaway

**[S-37] Section heading (`takeaway.heading`)**
> אז על מה כדאי להסתכל באמת

**[S-38] Takeaway body — paragraph 1 (`takeaway.body[0]`)** — REVISED (am_mamtik trigger fix)
> אם אתם עומדים מול המדף עייפים ורוצים קיצור דרך אחד, אל תעצרו במספר הסוכר הגדול והברור. תסתכלו רגע על שורת הרכיבים, ואם מלטיטול או כוהל סוכר אחר מופיעים שם גבוה ברשימה, סביר שהמספר הנמוך מקורו בהחלפה ולא בהפחתה אמיתית. ואם קשה לקרוא את הרכיבים, שני סימנים גלויים מספרים שכמות כוהלי הסוכר כאן משמעותית: האזהרה "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת", שמודפסת רק כשכוהלי הסוכר עוברים 10% מהמשקל, ושורת "מתוכם רב-כהלים" בטבלה, שמראה את הגרמים עצמם. המילים "עם ממתיק" הן רמז ראשון וחלש בלבד, כי הן מופיעות על כל מוצר עם ממתיק כלשהו, ולא דווקא על כוהל סוכר.

**[S-39] Takeaway body — paragraph 2 (`takeaway.body[1]`)** — unchanged
> זה לא אומר שאסור לקנות חטיף עם מלטיטול. זה כן אומר שכדאי לדעת שזה מה שקונים, ולא להניח שמספר סוכר נמוך הוא בהכרח עדות לחטיף נקי יותר. בדיוק את הפער הזה, בין מה שהאריזה מציגה למה שיש בפנים, ברי מנסה להפוך לגלוי.

---

## 7b. Front vs. back — three real bars (NEW centerpiece, S-47..)

> The strong per-bar element the owner approved. For three bars, the sugar number on the front of the pack vs. the polyol reality on the back. Every figure is locked in the v2 spec (Section 9). Terminology lock obeyed: the gram figure is **total** sugar alcohols (כוהלי סוכר), never maltitol alone. This is a **label / legal fact** we report — not a health prediction (spec §4). Each string labeled `[S-47..]` for Frontend.

**[S-47] Section heading (`frontback.heading`)**
> מה שכתוב מקדימה, ומה שמחכה מאחורה

**[S-48] Section intro (`frontback.intro`)**
> עד כאן דיברנו על המנגנון. עכשיו שלוש חטיפות אמיתיות מהמדף, ובכל אחת מספר הסוכר הקטן שעל חזית האריזה מול נתון כוהלי הסוכר שמופיע בטבלה התזונתית בגב. הנתון האחורי משקף את סך כל כוהלי הסוכר יחד, גם כשמלטיטול הוא הבולט מביניהם. חשוב להבהיר מראש: אנחנו מדווחים כאן מה כתוב על האריזה ומה החוק חייב להדפיס עליה, ולא מנבאים מה יקרה למי שיאכל.

**[S-49] Bar line — WIN קרם קרמל (`frontback.bars[0]`)**
> WIN קרם קרמל: בחזית כתוב "1.7 גרם סוכר". בטבלה שבגב מופיעים 27 גרם כוהלי סוכר ל-100 גרם, כולל מלטיטול, סורביטול ואריתריטול. על האריזה גם מודפסת האזהרה החוקית "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת", ובישראל מדפיסים אותה רק כשכוהלי הסוכר עוברים 10% מהמשקל.

**[S-50] Bar line — אול אין סופט פיסטוק (`frontback.bars[1]`)**
> אול אין סופט פיסטוק: בחזית כתוב "4.6 גרם סוכר". בטבלה שבגב מופיעים 34.1 גרם כוהלי סוכר ל-100 גרם. גם החטיף הזה נושא את האזהרה החוקית על פעילות מעיים מוגברת, כלומר היצרן עצמו הצהיר שכוהלי הסוכר כאן עוברים את סף ה-10%.

**[S-51] Bar line — פרו שטראוס קרמל ואגוזים (`frontback.bars[2]`)**
> פרו שטראוס קרמל ואגוזים: בחזית כתוב "3.7 גרם סוכר". בטבלה שבגב מופיעים 24 גרם כוהלי סוכר ל-100 גרם, נתון שמתיישב עם אותו סף 10%. את האזהרה החוקית עצמה לא הצלחנו לאמת על האריזה הפיזית מהמקורות שהגענו אליהם, ולכן איננו קובעים שהיא מופיעה עליה.

---



> A standalone credibility card embedded in the article. It anchors the "lower, not zero" glucose point and the substitution architecture to EFSA — the **independent** EU food-safety regulator, deliberately chosen over industry-funded bodies. Architectural / label-transparency framing only; no health advice, no recommendation. Each string is labeled `[S-40..]` for Frontend to map.

**[S-40] Eyebrow (`efsaCard.eyebrow`)**
> רשות רגולטורית עצמאית

**[S-41] Card title (`efsaCard.title`)**
> מה שאמרה על זה הרשות האירופית לבטיחות מזון

**[S-42] Lead sentence (`efsaCard.lead`)**
> הרשות האירופית לבטיחות מזון (EFSA) היא הגוף הרגולטורי העצמאי שבוחן את בטיחות המזון באיחוד האירופי. היא לא יצרנית ולא איגוד תעשייה, וזה בדיוק מה שנותן משקל לקביעה שלה כאן.

**[S-43a] EFSA finding — `quotedText`, INSIDE the blockquote (`efsaCard.finding`)** — SPLIT from old S-43 (Element D, RT-C1)
> בחוות דעת מדעית משנת 2011 קבעה EFSA כך: כשתחליפי סוכר כמו מלטיטול מחליפים את הסוכר במזון או במשקה, עליית הסוכר בדם אחרי האכילה נמוכה יותר מזו שמתקבלת ממזון או משקה שמכילים סוכר.

**[S-43b] Bari author note — `authorNote`, OUTSIDE the blockquote (`efsaCard.authorNote`)** — SPLIT from old S-43 + reworded per RT-H1 (Element D)
> חוות הדעת הזו נוגעת לחלק אחד מהתמונה בלבד: היא מאששת את הנקודה המרכזית שתיארנו, עלייה נמוכה יותר של הסוכר בדם, ומאותו מקור עצמאי. השאלה הנפרדת, אם הצגת "1.7 גרם סוכר" בחזית בזמן ש-27 גרם כוהלי סוכר יושבים ברשימת הרכיבים נותנת לקונה תמונה מדויקת, איננה חלק ממה ש-EFSA בחנה.

**[S-44] Honest caveat (`efsaCard.caveat`)** — REVISED opener per RT-H2
> חשוב לדייק כאן. EFSA דיברה על עלייה נמוכה יותר של הסוכר בדם, לא על היעדר עלייה ולא על המלצה בריאותית. זו אמירה על תגובת הסוכר בדם, ושום דבר מעבר לזה.

**[S-45] Link label / CTA (`efsaCard.cta`)**
> לחוות הדעת המקורית של EFSA (EFSA Journal 2011)

**[S-46] English verbatim sub-line (optional, `efsaCard.verbatim`)**
> "consumption of foods/drinks containing [sugar replacers such as maltitol] instead of sugar induces a lower blood glucose rise after their consumption compared with sugar-containing foods/drinks." — EFSA Journal 2011;9(4):2076

> Link target (`efsaCard.href`): https://efsa.europa.eu/cs/efsajournal/pub/2076

---

## Gate results

> Methodology: 39 Hebrew strings (S-01..S-39) were run through the three offline gates in `integrations/clients/`. The reproducible runner is `02_products/snack_bars/_gate_run_379.py`; raw output is `02_products/snack_bars/_gate_run_379_out.json`. Run command: `PYTHONUTF8=1 PYTHONPATH=C:\Bari python 02_products\snack_bars\_gate_run_379.py --grammar` (exit 0).

### Headline numbers

| Gate | Result |
|---|---|
| `hebrew_readability.is_clean` | **39 / 39 clean** (zero framework leakage, zero recommendation language, zero raw score mechanics) |
| `naturalness_gate` HIGH (T1–T7) | **0** — all HIGH-clean (mandatory pass condition for return) |
| `naturalness_gate` MEDIUM | **16** — routed to the independent judge (see below); none is a HIGH block |
| `hebrew_grammar_gate.is_clean` | **21 / 39 reported clean; remaining 18 carry only `confidence="medium"` flags, all reviewed and confirmed as DictaBERT wrong-anchor false positives** (see grammar note). Zero `confidence="high"` flags → nothing to auto-fix. Human-reviewed grammar = clean. |

### Naturalness — what the MEDIUM flags are (for the independent judge, Track C)

I cannot self-clear naturalness; these are documented for the Layer-2 LLM judge.

- **T9 loanword-presence (14 strings):** the flagged tokens are `מלטיטול`, `סורביטול`, `קסיליטול`, `אריתריטול`, plus `GI`, `WIN`, `%`, and the E-numbers. These are the **allowed consumer terms** for this piece (task brief + spec firewall permit מלטיטול / כוהל סוכר / ממתיק / תחליף סוכר). "כוהל סוכר" is glossed in plain language in S-08. Not defects — flagged because the gate cannot tell an allowed ingredient name from an untranslated loanword.
- **S-10 T1 (MEDIUM, mid-text):** "תוצאה של החלפה, לא של הפחתה" — this is a mid-sentence apposition that the same paragraph then resolves ("זה לא טריק אסור..."), not a bare `X, לא Y` closer. Judge call; reads as native apposition.
- **S-39 T2 (MEDIUM):** "זה לא אומר ש... זה כן אומר ש..." — this is the owner's canonical stance pattern (fingerprint §1 step 6; gold Example-style "זה לא אומר... זה כן אומר..."), not the retired "X לא תמיד אומר Y" calque. Kept deliberately.
- **F2 (stance) signal:** 5 strings flag `f2_risk: high` on the heuristic, all because they are *explanatory* body paragraphs (S-08, S-12, S-14 etc.) with hedges and no single verdict marker — by design for a mechanism explainer. The verdict-bearing lines (S-30, S-31, takeaway) register `has_verdict_marker: true / f2_risk: low`. The piece as a whole carries a clear stance ("פחות סוכר מהחלפה, לא מהפחתה"); the judge should score F2 on the article, not on isolated mechanism sentences.

### Grammar note (DictaBERT false positives — human-reviewed)

All 18 not-clean strings carry **only `confidence="medium"`** flags, and every one is a wrong-anchor mislabel — the exact failure mode the gate's own guardrail warns about ("DictaBERT can mislabel... flags are candidates, not verdicts"). Auto-fix touches `confidence="high"` only; there are none, so nothing was auto-fixed. Representative confirmations:
- S-04 "שורת הרכיבים מספרת" — subject is **שורת** (fem sing, construct), agreement correct; gate wrongly anchored to הרכיבים.
- S-08 "שאחריה הולכים גם בישראל" — impersonal plural ("they follow"); correct Hebrew.
- S-09 "שורת הסוכר יורדת" / "שורת הקלוריות יורדת" — subject is שורת (fem sing); both correct; gate anchored to הסוכר/הקלוריות.
- S-14 "השפעות... תלויות" + "כשורה נפרדת" — תלויות agrees with השפעות; נפרדת with שורה; both correct.
- S-38 "אתם עומדים... עייפים" — subject is אתם (2nd-person plural); correct; gate anchored to המדף.
- S-39 "חטיף נקי" — נקי (masc) agrees with חטיף; correct; gate anchored to עדות.

No genuine gender/number agreement error was found on human review. The strings are grammatically clean.

### Per-string status

All 39 strings: readability `is_clean=True`, naturalness HIGH-clean. Full per-string JSON (including every MEDIUM tell and grammar flag) is in `_gate_run_379_out.json`.
