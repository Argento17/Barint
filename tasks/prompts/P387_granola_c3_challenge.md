# P387 / TASK-385 — Granola scoring + content independent CHALLENGE (route: C3)

You are an independent challenger (ChatGPT). Advice/critique ONLY — you do not build, edit, or close. Evidence-based reasoning; flag uncertainty. The owner reviewed the live page and said "there are some errors" — your job is to FIND them, in both the scoring and the Hebrew content. Be adversarial and specific.

## Context
Bari scores Israeli supermarket products 0–100 / A–E on nutritional architecture (processing, sugar, calorie density, additives, protein, fiber). This is the **granola** shelf, 22 products. It was just re-scored (the live page had drifted too lenient). The engine applies category caps: NOVA_PROXY_3/4 (processing), HIGH_SUGAR_25G_PLUS, ISRAELI_RED_LABEL_1_SUGAR + SNACK_BAR_RED_SUGAR_LABEL (≥ the Israeli red-label sugar threshold), SNACK_BAR_HIGH_CAL (calorie density), ADDITIVE_MARKERS_3/5_PLUS. Distribution: B4 / C8 / D8 / E2.

## Full score table (rank | grade score | name | per-100g | caps fired)
```
[1]  B 69.7 | גרנולה חמוציות ושקדים        | sugar 9.6  fat 14.8 prot 11.4 fib 14.5 kcal 386 na 10  | NOVA_3
[2]  B 69.3 | גרנולה פרוטאין+שוקולד         | sugar 8.0  fat 11.4 prot 20.7 fib 12.3 kcal 411 na 71  | NOVA_3
[3]  B 67.4 | גרנולה מייפל תמר פקאן         | sugar 11.9 fat 17.3 prot 12.1 fib 9.5  kcal 414 na 7   | NOVA_3
[4]  B 65.0 | גרנולה לוז וקינמון            | sugar 9.5  fat 20.0 prot 14.6 fib 14.7 kcal 451 na 6   | HIGH_CAL, NOVA_3
[5]  C 64.0 | גרנולה מיקס קראנץ' מלוח       | sugar 4.8  fat 34.2 prot 17.7 fib 11.7 kcal 504 na 394 | HIGH_CAL, NOVA_3
[6]  C 63.1 | גרנולה חלבון שקד+חמוציות      | sugar 8.8  fat 11.5 prot 23.6 fib 12.8 kcal 411 na 56  | NOVA_3
[7]  C 63.0 | גרנולה 18% חלבון             | sugar 13.2 fat 12.7 prot 18.0 fib 6.3  kcal 401 na 15  | NOVA_3
[8]  C 62.4 | גרנולה 48% סופרפוד           | sugar 13.5 fat 17.2 prot 12.0 fib 9.4  kcal 410 na 69  | NOVA_3
[9]  C 61.3 | גרנולה אגוזים חמוציות         | sugar 9.9  fat 19.3 prot 11.8 fib 14.4 kcal 440 na 9   | HIGH_CAL, NOVA_3
[10] C 61.0 | גרנולה פרוטאין+אגוזים         | sugar 9.0  fat 12.7 prot 23.7 fib 8.3  kcal 431 na 65  | HIGH_CAL, NOVA_3
[11] C 54.3 | גרנולה מייפל פקאן            | sugar 15.6 fat 19.7 prot 10.4 fib 6.7  kcal 451 na 8   | HIGH_CAL, NOVA_3
[12] C 51.9 | גרנולה 8% שוקולד מריר        | sugar 13.4 fat 14.0 prot 11.0 fib 6.5  kcal 416 na 99  | NOVA_3
[13] D 47.0 | גרנולה חלבה תמר קשיו         | sugar 9.3  fat 19.2 prot 13.0 fib 8.2  kcal 432 na 16  | HIGH_CAL, NOVA_4, ADDITIVE_3+
[14] D 40.2 | גרנולה פקאן                 | sugar 17.0 fat 12.0 prot 10.0 fib 7.0  kcal 414 na 40  | NOVA_4
[15] D 39.8 | גרנולה שוקולד פיטנס          | sugar 17.7 fat 14.8 prot 9.0  fib 7.6  kcal 435 na 77  | RED_SUGAR, ISR_SUGAR, HIGH_CAL, NOVA_3
[16] D 39.8 | גרנולה שוקולד קינואה         | sugar 17.9 fat 16.4 prot 9.1  fib 7.3  kcal 443 na 89  | RED_SUGAR, ISR_SUGAR, HIGH_CAL, NOVA_3
[17] D 39.2 | גרנולה דבש פיטנס            | sugar 17.9 fat 13.2 prot 8.7  fib 7.1  kcal 428 na 89  | RED_SUGAR, ISR_SUGAR, NOVA_4
[18] D 38.3 | גרנולה אגוזים               | sugar 18.0 fat 13.0 prot 10.0 fib 7.0  kcal 415 na 40  | RED_SUGAR, ISR_SUGAR, NOVA_4
[19] D 38.0 | גרנולה עשירה                | sugar 25.0 fat 17.2 prot 11.2 fib 5.7  kcal 423 na 195 | HIGH_SUGAR_25, RED_SUGAR, ISR_SUGAR, NOVA_3
[20] D 35.5 | גרנולה אגוזים               | sugar 20.0 fat 13.1 prot 9.0  fib 6.0  kcal 371 na 20  | RED_SUGAR, ISR_SUGAR, NOVA_4
[21] E 32.1 | גרנולה פירות                | sugar 21.0 fat 10.0 prot 9.0  fib 7.0  kcal 396 na 40  | RED_SUGAR, ISR_SUGAR, NOVA_4, ADDITIVE_3+
[22] E 31.4 | גרנולה עם פירות             | sugar 21.0 fat 11.5 prot 8.9  fib 6.0  kcal 364 na 20  | RED_SUGAR, ISR_SUGAR, NOVA_4, ADDITIVE_5+
```

## Challenge these — argue specifically, name the rank/product
1. **Sugar-ordering coherence (the owner is adding a SUGAR metric bar to the page).** Find every place where a LOWER-sugar product is graded BELOW a higher-sugar one, and say whether it's defensible. E.g. [13] חלבה 9.3g sugar = D, below [12] 13.4g = C and far below [5] 4.8g = C and [11] 15.6g = C. If a sugar bar is displayed next to the grade, will these read as contradictions to a consumer? Which specific rows look wrong?
2. **The red-label sugar threshold.** [15]–[18] fire ISRAELI_RED_LABEL_1_SUGAR at 17.7–18g, but [11] (15.6g) and [8] (13.5g) and [7] (13.2g) do NOT. Where exactly is the Israeli red-label sugar line for this product type, and is the engine applying it at a defensible cutoff? Is [19] עשירה at 25g really only D (38.0) — same band as 18g products — proportionate?
3. **Calorie vs sugar weighting.** [5] מלוח is a clean, no-added-sugar product (4.8g sugar) dragged to C by 504 kcal / 34g fat / 394mg sodium. Is grading a clean whole-food nut granola the same C as sugar-engineered [7][8] defensible, or is the calorie/fat penalty over-weighted vs the sugar penalty?
4. **NOVA inconsistency.** Why does [13] חלבה get NOVA_4 (9.3g sugar) while [19] עשירה gets only NOVA_3 (25g sugar, isoglucose)? Does the NOVA proxy look reliable here, or noisy?
5. **CONTENT errors — audit the 7 re-authored Hebrew verdicts below for factual/framing errors.** Specifically: [5]'s verdict says "חמישה סוגי אגוזים" (five kinds of NUTS) but the label is sunflower seeds + pumpkin seeds + almonds + cashew + hazelnut — two are SEEDS not nuts. Is that an error? Find any other claim that overstates, mislabels an ingredient, or asserts something the per-100g data doesn't support.

### The 7 re-authored verdicts (Hebrew)
[5] מלוח C64 — insight: "רשימת רכיבים נקייה לגמרי — שיבולת שועל, אגוזים, טחינה, סילאן. הסוכר נמוך (4.8 גרם), אבל 504 קק\"ל ו-34 גרם שומן ל-100 גרם מהאגוזים — זה מה שמוריד ל-C." | row: "רשימת רכיבים נקייה מהמדף: שיבולת שועל מלאה, חמישה סוגי אגוזים, טחינה, סילאן — ללא סוכר מוסף ובלי שמן צמחי. אבל 504 קק\"ל ו-34.2 גרם שומן ל-100 גרם (האגוזים הם מקורם) ו-394 מ\"ג נתרן מהמלח — זו צפיפות גבוהה שמורידה אותה ל-C, גם כשהמרכיבים עצמם ראויים לשבח."
[7] 18% חלבון C63 — insight: "18 גרם חלבון ל-100 גרם — חוזק אמיתי. חלבון אפונה מבודד ושומן צמחי מוסף מביאים אותו לשם — הנדסת מרכיבים ברשימה." | row: "18 גרם חלבון ל-100 גרם — זה ממש לא מעט. אבל הדרך לשם עוברת דרך חלבון אפונה מבודד ושומן צמחי מוסף; יחד עם 13.2 גרם סוכר ו-6.3 גרם סיבים בלבד — הפרופיל מורכב מספיק כדי להישאר על C."
[8] סופרפוד C62 — insight: "גוג'י ברי, צ'יה, שמן זית 1% — 'סופרפוד' בשם. בפועל 13.5 גרם סוכר ו-17.2 גרם שומן ל-100 גרם, ופרופיל תזונתי שמתיישב בחלק האמצעי של הקטגוריה." | row: "...13.5 גרם סוכר מסילאן ורכז תפוחים, 17.2 גרם שומן, ופצפוצי אורז ותמצית טעם... C היא הציון שמשקף נאמנה את הפער בין השם לבין מה שיש בפנים."
[19] עשירה D38 — insight: "25 גרם סוכר ל-100 גרם — גבול הסף האדום הישראלי. שני מקורות סוכר מוסף ברשימה: סוכר ואיזוגלוקוז." | row: "25 גרם סוכר ל-100 גרם — גבול האזהרה האדומה הישראלי — עם שני מקורות סוכר מוסף ברשימה (סוכר ואיזוגלוקוז), חומר משמר על הפירות היבשים, ו-195 מ\"ג נתרן... ומקבלת D בהתאם."
[20] אגוזים D35.5 — insight: "שמן דקלים הרכיב השלישי, שלושה מקורות סוכר מוסף, משפרי טעם — 20 גרם סוכר ל-100 גרם ו-4.5% אגוזים בלבד." | row: "שם: גרנולה אגוזים. בפועל: שמן דקלים כרכיב השלישי, שלושה מקורות סוכר מוסף (סוכר חום, סירופ גלוקוז, דבש), משפרי טעם וריח — ו-4.5% אגוזים בלבד. 20 גרם סוכר ל-100 גרם ומבנה תעשייתי שמסביר בדיוק למה הציון הוא D."
[21] פירות E32 — insight: "שמן דקלים בגרנולה וצבע מאכל קרמל מופיעים בשני חלקי הרשימה — 21 גרם סוכר ל-100 גרם, כל הפירות מסוכרים בנפרד." | row: "...וכל הפירות שבה (פפאיה, אננס, בננה, חמוציות) מסוכרים בנפרד עם חומרי שימור. התוצאה היא 21 גרם סוכר ל-100 גרם ומבנה מעובד מהקצה לקצה — ומכאן הציון E."
[22] עם פירות E31 — insight: "שמן דקלים וסירופ גלוקוז בגרנולה הבסיסית, כל הפירות (פפאיה, אננס, בננה, חמוציות) מסוכרים בנפרד — 21 גרם סוכר ל-100 גרם." | row: "שמן דקלים, סירופ גלוקוז וסוכר חום בגרנולה הבסיסית, ועוד 17% פירות שכולם מסוכרים בנפרד... שתי שכבות עיבוד שמסתכמות ב-21 גרם סוכר ל-100 גרם — מהנמוכים בקטגוריה, ובציון E בהתאם."

## Return
A specific, ranked list of ERRORS/WEAKNESSES you found — each tagged SCORING or CONTENT, with the rank/product, the problem, and your recommended fix. Then: is the sugar-led metric display coherent with these scores (yes/no + the rows that break it)? End with an explicit "ship-as-is / fix-these-first" call. No code.
