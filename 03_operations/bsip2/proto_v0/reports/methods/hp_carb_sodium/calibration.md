# HP carb+sodium cluster — calibration dataset (P173)

Generated: 2026-06-18T04:52:37.970913+00:00

## Summary

| Metric | Count |
|--------|------:|
| Products evaluated (denominator) | 979 |
| Fired (carb>40% kcal AND sodium>=200mg/100g) | 283 |
| Insufficient data | 89 |
| Did not fire | 607 |

## Fire rate per shelf

| Shelf | Evaluated | Fired | Insufficient | Fire rate |
|-------|----------:|------:|-------------:|----------:|
| brined_cheeses | 48 | 1 | 0 | 2.1% |
| cakes | 167 | 88 | 2 | 52.7% |
| cereals | 63 | 24 | 0 | 38.1% |
| cheese | 59 | 2 | 5 | 3.4% |
| cookies_coffee | 209 | 113 | 2 | 54.1% |
| granola | 103 | 40 | 12 | 38.8% |
| hard_cheeses | 67 | 0 | 40 | 0.0% |
| hummus_shelfrel_002 | 69 | 4 | 0 | 5.8% |
| juices | 32 | 1 | 19 | 3.1% |
| milk | 20 | 0 | 2 | 0.0% |
| snacks | 53 | 10 | 7 | 18.9% |
| yogurts | 89 | 0 | 0 | 0.0% |

## Manual false-positive review (fired products)

Per EV-013 `risk_of_misuse`: without calibrated thresholds, HP-style carb+salt
signals can falsely flag naturally salty+carbohydrate foods (bread, cheese, dates).
Review each fired product: refined-carb+salt snack vs defensible endemic food.

| Shelf | Barcode | Product | carb%kcal | sodium mg/100g | FP review |
|-------|---------|---------|----------:|---------------:|-----------|
| brined_cheeses | 2511236 | בולגרית מעודנת 5% | 45.55 | 880.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 2472087 | עוגת פס שוקולד | 49.82 | 283.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 2472117 | עוגת פס קפוצ'ינו | 42.41 | 308.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 2472148 | עוגת פס היער השחור | 46.29 | 307.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 2472186 | עוגת מאפין וניל | 55.26 | 440.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 2472193 | עוגת מאפין שוקולד | 55.27 | 493.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 2472223 | עוגת מאפין תפוז | 55.44 | 320.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 2472254 | עוגת מאפין אגוזים | 50.72 | 458.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 2472261 | עוגת מאפין תפוחי עץ | 57.97 | 405.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 2472841 | עוגת סבתא בטעם שוקולד | 54.29 | 357.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 313184 | עוגיות גן חיות טעם וניל | 68.01 | 285.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 4017100198151 | עוגיות היט בטעם וניל 220 גרם בלזן / 220 גרם ‏10.90 ‏₪ ‏4.95 | 50.39 | 260.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 4017100364112 | עוגיות היט בטעם שוקולד 220 גרם בלזן / 220 גרם ‏10.90 ‏₪ ‏4.9 | 49.61 | 510.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 46214731552 | עוגיות שוקולד צ'יפס | 47.63 | 249.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 46214930207 | עוגיות שוקולד צ'יפס | 49.92 | 283.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 4823077633317 | עוגיות LOVITA שוקולד | 49.98 | 288.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 5317194 | ביסקוויט בטעם וניל הדר | 69.59 | 256.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 5410126006049 | ביסקוויט לוטוס טעם קרמל | 60.0 | 370.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 5410126116168 | ביסקוויט בטעם קרמל | 60.0 | 370.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 5410126726244 | ביסקוויט קרמל | 60.0 | 370.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 5410126806250 | עוגיות לוטוס | 60.0 | 370.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 5718021 | עוגת שטרודל גבינה | 51.66 | 236.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 5718038 | עוגת שטרודל תפוחי עץ | 55.35 | 235.0 | review_needed — carb+salt threshold met; classify manually |
| cakes | 5901414200411 | עוגיות היט מיניס עם שוקולד 130 גרם בלזן / 130 גרם ‏8.90 ‏₪ ‏ | 50.89 | 300.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 6983770 | עוגת הבית שיש אסם | 52.43 | 310.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 6983787 | עוגת שוקולד צ'יפס | 53.21 | 300.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 6983794 | עוגת הבית תפוז | 52.2 | 310.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290000075143 | עוגיות שוקוצ'יפס קלאסי 200 גרם אסם / 200 גרם 2 יח' ב- ‏16 ₪ | 50.58 | 220.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290002026440 | פרצלס בראנץ' 70 גרם בראנץ אנד קראנץ / 280 גרם ‏13.00 ‏₪ ‏4.6 | 76.0 | 480.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| cakes | 7290006775023 | עוגה אנגלית 450 גרם אחוה / 450 גרם 2 יח' ב- ‏18 ₪ ‏10.90 ‏₪ | 54.68 | 214.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290006775085 | עוגת שמרים במילוי קרם בטעם שוקולד 400 גרם אחוה / 400 גרם ‏10 | 52.71 | 208.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290006775337 | עוגת שמרים פרג 400 גרם אחוה / 400 גרם ‏10.90 ‏₪ ‏2.73 ‏₪ / 1 | 57.14 | 204.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290011489625 | ביסקוויט בטעם שוקו | 69.59 | 256.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290011570798 | כרגיל תערובת עוגת שוקולד | 87.45 | 762.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290013453624 | עוגיות שוקולד צ'יפס כשלפ | 41.5 | 274.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7290013683595 | עוגת פס שביל החלב | 44.88 | 299.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7290015726528 | עוגת פס מוס טירמיסו | 44.26 | 216.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7290017962139 | עוגיות פירות יער כשל"פ | 45.81 | 264.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290018893036 | עוגיות סנדוויץ' שוקולד | 55.53 | 380.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290020030184 | עוגיות מזרחיות עם זעתר 400 גרם אחוה / 400 גרם 2 יח' ב- ‏18 ₪ | 47.84 | 730.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290106571921 | עוגיות פיטנס חמוציות 180 גרם פיטנס / 180 גרם ‏12.90 ‏₪ ‏7.17 | 58.07 | 255.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290106571945 | עוגיות קקאו דגנים מלאים עם נטיפי שוקולד מריר פיטנס 180 גרם פ | 50.79 | 290.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290109581156 | קציצות של סבתא פרז | 46.28 | 400.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7290112495228 | קורנפלקס דבש | 90.96 | 368.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290115206333 | עוגיות מיני שוקוצ'יפס | 51.1 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290118421924 | תערובת לעוגה ללא גלוטן אסם / 350 גרם ‏12.90 ‏₪ ‏3.69 ‏₪ / 10 | 47.3 | 396.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290118426615 | עוגיות מיני שוקולד | 54.94 | 260.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290119040513 | עוגת קראנץ שוקולד | 60.0 | 235.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290119040568 | עוגת קראנץ אגוזים | 60.0 | 235.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290119040612 | עוגת קראנץ קינמון | 60.0 | 235.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290119040667 | עוגת קראנץ פרג | 60.0 | 235.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290119040803 | עוגיות קינמון מסוכרות | 53.95 | 230.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290119040858 | עוגיות מקלות עלים | 53.95 | 230.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290119043095 | עוגיות שיבולת שועל | 52.16 | 373.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290119043743 | עוגיות מרוקאיות | 60.87 | 258.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290123330280 | עוגת שמרים בטעם שוקולד | 65.59 | 365.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290123330334 | עוגת שמרים בריוש שוקולד | 65.59 | 365.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290123330884 | עוגה בטעם שוקולד כשל"פ | 45.48 | 310.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7290123331034 | עוגה בטעם שוקולד כשל"פ | 49.54 | 283.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073132936 | עוגת מאפין שיש | 54.69 | 253.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073132943 | עוגת מאפין בטעם שוקולד | 54.03 | 252.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073132950 | עוגת מאפין שוקולד צ'יפס | 53.6 | 245.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073140184 | עוגת מאפין תפוז | 54.55 | 258.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073162001 | עוגיות במילוי קרם אגוזים | 41.48 | 258.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7296073431879 | עוגת מאפין שוקו צ'יפס | 52.83 | 307.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073431893 | עוגת מאפין אגוזים | 49.48 | 322.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073431909 | עוגת מאפין תפוח עץ | 53.51 | 280.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073431916 | עוגת מאפין בטעם תפוז | 51.93 | 330.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073453840 | קוקיס שבבי שוקולד חלבי | 53.11 | 384.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7296073453857 | קוקיס שוקולד לבן חלבי | 51.04 | 335.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| cakes | 7296073473664 | עוגת שוקולד ללא גלוטן | 41.07 | 288.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073473688 | עוגת שוקוציפס ללא גלוטן | 42.0 | 250.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7296073529019 | קוקיס שוקולד מריר חלבי | 51.51 | 368.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7296073529026 | קוקיס שוקו+שבבי שוקולד | 50.73 | 276.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7622201401900 | עוגיות מילקה סנסיישן אוראו 156 גרם מילקה / 156 גרם 2 יח' ב- | 46.69 | 230.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7622201809188 | ביסקוויט מילקה | 54.92 | 270.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7622210137234 | עוגיות אוראו דאבל קרם וניל אוראו / 170 גרם 2 יח' ב- ‏18 ₪ ‏1 | 54.4 | 280.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 7622210453327 | עוגיות מילקה סנסיישן 156 גרם מילקה / 156 גרם 2 יח' ב- ‏28 ₪ | 49.41 | 352.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7622300356767 | עוגיות שוקולד צ'יפס | 50.2 | 330.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 7622300489434 | עוגיות אוראו בציפוי שוקולד חלב 246 גרם אוראו / 246 גרם במבצע | 50.98 | 212.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 8000500366073 | ביסקוויט נוטלה | 49.71 | 220.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 8410376037784 | עוגיות סנדוויץ' שוקולד גולון / 250 גרם ‏13.00 ‏₪ ‏5.20 ‏₪ / | 63.51 | 240.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 8410376075915 | עוגיות+שבבי שוקולד לל"ג | 54.82 | 240.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 8710502139017 | מרבה עוגיות טריפל שוקולד ציפס מרבה / 180 גרם במבצע ‏7.90 ₪ ‏ | 49.8 | 245.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 8710502279010 | עוג. שוקולד צ'יפס מצופות | 45.26 | 240.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 8710502405204 | מרבה עוגיות ממולאות קרם שוקולד מרבה / 225 גרם במבצע ‏7.90 ₪ | 45.5 | 254.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 8710502470028 | עוגיות שוקוצ'יפס נוגטלי | 46.78 | 246.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cakes | 9397642 | 5עוגות מאפין בטעם שוקולד | 51.36 | 241.0 | likely_true_positive — refined-carb+salt snack profile |
| cakes | 9397697 | חמישיית מאפין שוקו צ'יפס | 53.04 | 251.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290011131371 | מוזלי קראנצ'י בוטנ+שקדים | 59.74 | 350.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290011131388 | מוזלי קראנצי תפוח קינמון | 71.57 | 380.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290011131395 | מוזלי 30% פירות | 66.04 | 350.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290014471412 | מוזלי בוטנים, לוז, שקדים | 59.9 | 400.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290014471429 | מוזלי פירות יבשים | 75.13 | 400.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290014471436 | מוזלי צימוק תפוח וקינמון | 71.76 | 400.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290017325910 | קורנפלקס אורגני הרדוף | 86.72 | 600.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290107647731 | דגני בוקר קוקומן חום לבן | 83.96 | 382.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290107647854 | דגני בוקר שוגי | 90.86 | 435.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290112494351 | קורנפלקס של אלופים בד"ץ | 88.85 | 375.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290112495228 | קורנפלקס דבש | 90.96 | 368.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290112495433 | דגני בוקר דליפקאן | 64.04 | 285.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290116530482 | מארז קורנפלקס של אלופים | 88.85 | 375.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7290118420811 | פריכ.דקות דגנים+קטניות | 80.82 | 400.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7296073642022 | דגני בוקר טבעות דבש לל"ג | 87.22 | 240.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7296073642046 | קורנפלקס ללא גלוטן | 87.37 | 390.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7296073705550 | כדורי דגנים טעם שוקו | 78.37 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7296073705567 | טבעות דגנים בטעם דבש | 80.0 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7296073705574 | ריבועי דגנים עם קינמון | 63.64 | 320.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 72968 | דגני בוקר סיני מיניס | 71.01 | 338.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 7297488199590 | פצפוצי אורז תפוח | 88.89 | 390.0 | review_needed — carb+salt threshold met; classify manually |
| cereals | 7613030979647 | טריקס דגנים בטעם פירות | 79.8 | 287.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 8445291638839 | צ'יריוס בטעם דבש ושקדים | 76.98 | 248.0 | likely_true_positive — refined-carb+salt snack profile |
| cereals | 884912126115 | דגני גרייט גריינס דייטס | 76.09 | 241.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cheese | 7290014217492 | תערובת תיבול פילדלפיה | 68.42 | 7905.0 | candidate_false_positive — structural dairy sodium + moderate carbs, not refined snack |
| cheese | 7290019635116 | גבינת שמנת זיתים 5% | 41.67 | 400.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 2472087 | עוגת פס שוקולד | 49.82 | 283.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 2472117 | עוגת פס קפוצ'ינו | 42.41 | 308.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 2472148 | עוגת פס היער השחור | 46.29 | 307.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 2472186 | עוגת מאפין וניל | 55.26 | 440.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 2472193 | עוגת מאפין שוקולד | 55.27 | 493.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 2472223 | עוגת מאפין תפוז | 55.44 | 320.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 2472254 | עוגת מאפין אגוזים | 50.72 | 458.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 2472261 | עוגת מאפין תפוחי עץ | 57.97 | 405.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 2472841 | עוגת סבתא בטעם שוקולד | 54.29 | 357.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 2986058 | פתי בר וניל | 66.18 | 208.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 2986065 | פתי בר בטעם שוקולד | 64.29 | 212.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 311128 | עוגיות בטעם חמאה | 57.82 | 220.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 311463 | עוגיות חמאה ללת"ס | 67.78 | 254.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 311708 | עוגיות מחיטה מלאה מן | 56.82 | 238.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 313160 | עוגיות שוקולד זהבה | 61.45 | 250.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 313184 | עוגיות גן חיות טעם וניל | 68.01 | 285.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 4017100198151 | עוגיות היט בטעם וניל 220 גרם בלזן / 220 גרם ‏10.90 ‏₪ ‏4.95 | 50.39 | 260.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 4017100364112 | עוגיות היט בטעם שוקולד 220 גרם בלזן / 220 גרם ‏10.90 ‏₪ ‏4.9 | 49.61 | 510.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 46214731552 | עוגיות שוקולד צ'יפס | 47.63 | 249.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 46214930207 | עוגיות שוקולד צ'יפס | 49.92 | 283.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 4823077614675 | ביסקוויט לקפה בטעם חלב | 58.32 | 309.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 4823077614699 | ביסקוויט לקפה בטעם חמאה | 58.19 | 282.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 4823077633317 | עוגיות LOVITA שוקולד | 49.98 | 288.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 5317194 | ביסקוויט בטעם וניל הדר | 69.59 | 256.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 5410126006049 | ביסקוויט לוטוס טעם קרמל | 60.0 | 370.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 5410126116168 | ביסקוויט בטעם קרמל | 60.0 | 370.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 5410126726244 | ביסקוויט קרמל | 60.0 | 370.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 5410126806250 | עוגיות לוטוס | 60.0 | 370.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 5718021 | עוגת שטרודל גבינה | 51.66 | 236.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 5718038 | עוגת שטרודל תפוחי עץ | 55.35 | 235.0 | review_needed — carb+salt threshold met; classify manually |
| cookies_coffee | 5901414200411 | עוגיות היט מיניס עם שוקולד 130 גרם בלזן / 130 גרם ‏8.90 ‏₪ ‏ | 50.89 | 300.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 6983770 | עוגת הבית שיש אסם | 52.43 | 310.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 6983787 | עוגת שוקולד צ'יפס | 53.21 | 300.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 6983794 | עוגת הבית תפוז | 52.2 | 310.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290000075143 | עוגיות שוקוצ'יפס קלאסי 200 גרם אסם / 200 גרם 2 יח' ב- ‏16 ₪ | 50.58 | 220.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290002026440 | פרצלס בראנץ' 70 גרם בראנץ אנד קראנץ / 280 גרם ‏13.00 ‏₪ ‏4.6 | 76.0 | 480.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| cookies_coffee | 7290006775023 | עוגה אנגלית 450 גרם אחוה / 450 גרם 2 יח' ב- ‏18 ₪ ‏10.90 ‏₪ | 54.68 | 214.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290006775085 | עוגת שמרים במילוי קרם בטעם שוקולד 400 גרם אחוה / 400 גרם ‏10 | 52.71 | 208.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290006775337 | עוגת שמרים פרג 400 גרם אחוה / 400 גרם ‏10.90 ‏₪ ‏2.73 ‏₪ / 1 | 57.14 | 204.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290011489625 | ביסקוויט בטעם שוקו | 69.59 | 256.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290011570798 | כרגיל תערובת עוגת שוקולד | 87.45 | 762.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290013453501 | ביסקוטי כוסמין שוקולד | 58.89 | 263.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290013453624 | עוגיות שוקולד צ'יפס כשלפ | 41.5 | 274.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7290013683595 | עוגת פס שביל החלב | 44.88 | 299.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7290013740137 | עוגיות אוזן פיל | 43.59 | 214.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290013740465 | עוגיות שושנים | 51.88 | 452.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290013740540 | עוגיות אוזן פיל ללת"ס | 45.32 | 213.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290015726528 | עוגת פס מוס טירמיסו | 44.26 | 216.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7290017962139 | עוגיות פירות יער כשל"פ | 45.81 | 264.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290018371923 | פתי בר קמח מלא אורגני | 58.88 | 235.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7290018371930 | פתי בר קמח כוסמין אורגני | 55.89 | 231.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7290018371947 | פתי בר כוסמין | 56.57 | 236.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7290018893036 | עוגיות סנדוויץ' שוקולד | 55.53 | 380.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290018893845 | פתי בר בטעם חמאה | 72.39 | 392.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7290020030184 | עוגיות מזרחיות עם זעתר 400 גרם אחוה / 400 גרם 2 יח' ב- ‏18 ₪ | 47.84 | 730.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290106571921 | עוגיות פיטנס חמוציות 180 גרם פיטנס / 180 גרם ‏12.90 ‏₪ ‏7.17 | 58.07 | 255.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290106571945 | עוגיות קקאו דגנים מלאים עם נטיפי שוקולד מריר פיטנס 180 גרם פ | 50.79 | 290.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290109354972 | פתי בר ללא גלוטן קלאסי | 75.07 | 220.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290109354996 | פתי בר ללא גלוטן שוקו | 74.49 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290109581156 | קציצות של סבתא פרז | 46.28 | 400.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7290112495228 | קורנפלקס דבש | 90.96 | 368.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290115206333 | עוגיות מיני שוקוצ'יפס | 51.1 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290118421924 | תערובת לעוגה ללא גלוטן אסם / 350 גרם ‏12.90 ‏₪ ‏3.69 ‏₪ / 10 | 47.3 | 396.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290118426615 | עוגיות מיני שוקולד | 54.94 | 260.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119040513 | עוגת קראנץ שוקולד | 60.0 | 235.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119040568 | עוגת קראנץ אגוזים | 60.0 | 235.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119040612 | עוגת קראנץ קינמון | 60.0 | 235.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119040667 | עוגת קראנץ פרג | 60.0 | 235.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119040803 | עוגיות קינמון מסוכרות | 53.95 | 230.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119040858 | עוגיות מקלות עלים | 53.95 | 230.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119041206 | עוגיות קוואקר | 52.16 | 373.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119041350 | עוגיות קוואקר ללת"ס | 52.16 | 373.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119043095 | עוגיות שיבולת שועל | 52.16 | 373.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119043743 | עוגיות מרוקאיות | 60.87 | 258.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290119043798 | עוגיות אוזניות | 53.33 | 238.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290123330280 | עוגת שמרים בטעם שוקולד | 65.59 | 365.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290123330334 | עוגת שמרים בריוש שוקולד | 65.59 | 365.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290123330884 | עוגה בטעם שוקולד כשל"פ | 45.48 | 310.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7290123331034 | עוגה בטעם שוקולד כשל"פ | 49.54 | 283.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073132936 | עוגת מאפין שיש | 54.69 | 253.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073132943 | עוגת מאפין בטעם שוקולד | 54.03 | 252.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073132950 | עוגת מאפין שוקולד צ'יפס | 53.6 | 245.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073140184 | עוגת מאפין תפוז | 54.55 | 258.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073162001 | עוגיות במילוי קרם אגוזים | 41.48 | 258.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7296073431879 | עוגת מאפין שוקו צ'יפס | 52.83 | 307.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073431893 | עוגת מאפין אגוזים | 49.48 | 322.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073431909 | עוגת מאפין תפוח עץ | 53.51 | 280.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073431916 | עוגת מאפין בטעם תפוז | 51.93 | 330.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073453840 | קוקיס שבבי שוקולד חלבי | 53.11 | 384.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7296073453857 | קוקיס שוקולד לבן חלבי | 51.04 | 335.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| cookies_coffee | 7296073473664 | עוגת שוקולד ללא גלוטן | 41.07 | 288.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073473688 | עוגת שוקוציפס ללא גלוטן | 42.0 | 250.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7296073529019 | קוקיס שוקולד מריר חלבי | 51.51 | 368.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7296073529026 | קוקיס שוקו+שבבי שוקולד | 50.73 | 276.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 74184 | פתי בר קלאסי | 66.52 | 290.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7622201401900 | עוגיות מילקה סנסיישן אוראו 156 גרם מילקה / 156 גרם 2 יח' ב- | 46.69 | 230.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7622201809188 | ביסקוויט מילקה | 54.92 | 270.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7622210137234 | עוגיות אוראו דאבל קרם וניל אוראו / 170 גרם 2 יח' ב- ‏18 ₪ ‏1 | 54.4 | 280.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 7622210453327 | עוגיות מילקה סנסיישן 156 גרם מילקה / 156 גרם 2 יח' ב- ‏28 ₪ | 49.41 | 352.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7622300356767 | עוגיות שוקולד צ'יפס | 50.2 | 330.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 7622300489434 | עוגיות אוראו בציפוי שוקולד חלב 246 גרם אוראו / 246 גרם במבצע | 50.98 | 212.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 8000500366073 | ביסקוויט נוטלה | 49.71 | 220.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 80083764 | עוגיות דגנים עם ש.שועל | 51.8 | 220.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 8008698037171 | עוגיות חמאה ללא גלוטן | 45.65 | 220.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 8410376037784 | עוגיות סנדוויץ' שוקולד גולון / 250 גרם ‏13.00 ‏₪ ‏5.20 ‏₪ / | 63.51 | 240.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 8410376075915 | עוגיות+שבבי שוקולד לל"ג | 54.82 | 240.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 8710502139017 | מרבה עוגיות טריפל שוקולד ציפס מרבה / 180 גרם במבצע ‏7.90 ₪ ‏ | 49.8 | 245.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 8710502279010 | עוג. שוקולד צ'יפס מצופות | 45.26 | 240.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 8710502405204 | מרבה עוגיות ממולאות קרם שוקולד מרבה / 225 גרם במבצע ‏7.90 ₪ | 45.5 | 254.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 8710502470028 | עוגיות שוקוצ'יפס נוגטלי | 46.78 | 246.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| cookies_coffee | 9397642 | 5עוגות מאפין בטעם שוקולד | 51.36 | 241.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 9397697 | חמישיית מאפין שוקו צ'יפס | 53.04 | 251.0 | likely_true_positive — refined-carb+salt snack profile |
| cookies_coffee | 99804 | עוגיות שוקולד לבן חלבי | 50.65 | 383.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 16000423534 | קראנצ'י שיבולת שועל עם שוקולד מריר | 51.86 | 259.04761904761904 | likely_true_positive — refined-carb+salt snack profile |
| granola | 3560071016074 | Corn flakes | 88.77 | 320.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 4005528115218 | דגני חיטה ואורז בטעם | 90.05 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 42400108153 | Cereal | 87.27 | 453.56 | likely_true_positive — refined-carb+salt snack profile |
| granola | 5900020046833 | Cheerios | 69.57 | 286.666666666667 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290011131371 | מוזלי קראנצ'י בוטנ+שקדים | 59.74 | 350.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290011131388 | מוזלי קראנצי תפוח קינמון | 71.57 | 380.0 | review_needed — carb+salt threshold met; classify manually |
| granola | 7290011131395 | מוזלי 30% פירות | 66.04 | 350.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290014471412 | מוזלי בוטנים, לוז, שקדים | 59.9 | 400.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290014471429 | מוזלי פירות יבשים | 75.13 | 400.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290014471436 | מוזלי צימוק תפוח וקינמון | 71.76 | 400.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290017325910 | קורנפלקס אורגני הרדוף | 86.72 | 600.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7290104506819 | דגני בוקר במילוי קרם בטעם נוגט | 62.38 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7290107647731 | דגני בוקר קוקומן חום לבן | 83.96 | 382.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290107647854 | דגני בוקר שוגי | 90.86 | 435.0 | review_needed — carb+salt threshold met; classify manually |
| granola | 7290112494351 | קורנפלקס של אלופים בד"ץ | 88.85 | 375.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7290112495228 | קורנפלקס דבש | 90.96 | 368.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7290112495433 | דגני בוקר דליפקאן | 64.04 | 285.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290112965660 | פיטנס מלח פלפל | 50.42 | 380.0 | review_needed — carb+salt threshold met; classify manually |
| granola | 7290112968807 | Fitness Thin | 56.06 | 400.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7290115205312 | Fitness | 53.74 | 400.0 | review_needed — carb+salt threshold met; classify manually |
| granola | 7290116530482 | מארז קורנפלקס של אלופים | 88.85 | 375.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7290116533599 | קורנפלקס | 90.91 | 350.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7290116537351 | כריות נוגט | 63.48 | 217.0 | review_needed — carb+salt threshold met; classify manually |
| granola | 7290116537962 | כריות וניל חדש | 69.27 | 258.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7290118420811 | פריכ.דקות דגנים+קטניות | 80.82 | 400.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7296073642022 | דגני בוקר טבעות דבש לל"ג | 87.22 | 240.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 7296073642046 | קורנפלקס ללא גלוטן | 87.37 | 390.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7296073705550 | כדורי דגנים טעם שוקו | 78.37 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7296073705567 | טבעות דגנים בטעם דבש | 80.0 | 200.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7296073705574 | ריבועי דגנים עם קינמון | 63.64 | 320.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 72968 | דגני בוקר סיני מיניס | 71.01 | 338.0 | review_needed — carb+salt threshold met; classify manually |
| granola | 7297488199590 | פצפוצי אורז תפוח | 88.89 | 390.0 | review_needed — carb+salt threshold met; classify manually |
| granola | 7613030979647 | טריקס דגנים בטעם פירות | 79.8 | 287.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 7613032045753 | Neslte Fitness Chocolate & Rice | 73.45 | 1272.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 8445291301948 | Multigrain Cheerios | 73.27 | 313.33333333333303 | likely_true_positive — refined-carb+salt snack profile |
| granola | 8445291638839 | צ'יריוס טעם דבש ושקדים | 76.98 | 248.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| granola | 884912102102 | Great Grains Cereal Blueberry Morning imp | 80.67 | 339.0 | likely_true_positive — refined-carb+salt snack profile |
| granola | 884912126115 | דגני גרייט גריינס דייטס | 76.09 | 241.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| granola | 884912359155 | Honey Roasted Cereal with Granola | 62.19 | 463.40999999999997 | likely_true_positive — refined-carb+salt snack profile |
| hummus_shelfrel_002 | 7290011800642 | סלט מטבוחה מרוקאית | 43.24 | 395.0 | review_needed — carb+salt threshold met; classify manually |
| hummus_shelfrel_002 | 7290104721533 | סלט פלפלים קלויים | 81.25 | 397.0 | review_needed — carb+salt threshold met; classify manually |
| hummus_shelfrel_002 | 7290106577572 | מטבוחה אמיתית | 53.16 | 395.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| hummus_shelfrel_002 | 7290111563492 | מטבוחה חריפה | 53.16 | 395.0 | likely_true_positive — long ingredient list suggests industrial formulation |
| juices | 7290013608680 | מיץ עגבניות 1ל | 85.71 | 300.0 | review_needed — carb+salt threshold met; classify manually |
| snacks | 4011800528416 | קורני חטיפי דגנים בוטנים מתוק מלוח | 42.68 | 377.0 | likely_true_positive — refined-carb+salt snack profile |
| snacks | 4011800628512 | קורני חטיפי דגנים+שוקולד חלב | 57.85 | 200.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
| snacks | 4011800629519 | חטיף דגנים עם אגוזים | 59.08 | 240.0 | likely_true_positive — refined-carb+salt snack profile |
| snacks | 5900020015174 | חטיפי דגנים פיטנס שוקולד מריר שישייה | 70.61 | 247.0 | likely_true_positive — refined-carb+salt snack profile |
| snacks | 5900020022325 | סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח' | 62.26 | 259.0 | likely_true_positive — refined-carb+salt snack profile |
| snacks | 5900020034021 | חטיפי דגנים פיטנס שוקולד בננה שישייה | 70.89 | 202.0 | likely_true_positive — refined-carb+salt snack profile |
| snacks | 7290014525306 | מרבה סלים דליס קריספי אוכמניות 125 גר | 76.62 | 320.0 | likely_true_positive — refined-carb+salt snack profile |
| snacks | 7290107646147 | חטיף דגנים שוגי שישייה 156 גרם | 51.19 | 333.0 | likely_true_positive — refined-carb+salt snack profile |
| snacks | 7290107646826 | חטיף דגנים שוגי שוקו שישייה 156 גרם | 55.79 | 310.0 | likely_true_positive — refined-carb+salt snack profile |
| snacks | 8423207206501 | סלים דליס חטיף רב דגנים מצופה שוקולד לבן בטעם יוגורט | 46.15 | 231.0 | candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class) |
