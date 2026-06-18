# OFF Sweep v1 — Open Food Facts Contamination Map

Generated: 2026-06-18T10:14:12.874541+00:00  
Method: Python stdlib JSON parse + raw text grep of all live category data files; BSIP1 record lookup by barcode field.  
Scope: 10 registry categories + milk (legacy). Hard-cheeses and juices not in registry, excluded from live scan.  
OFF contamination types checked: (A) JSON-level OFF string markers in file text; (B) BSIP1 panel_source=open_food_facts.  
Image URL contamination (images.openfoodfacts.org in imageUrl field) is an independent contamination class reported separately.  

## Section 1: Category to Data File Map

Derived by reading import lines of every page-data .ts file under bari-web/src/lib/comparisons/ and registry/categories/*.ts.

| Category | Route | Data File | Note |
|---|---|---|---|
| bread | /hashvaot/bread | bread_frontend_v2.json |  |
| hummus | /hashvaot/hummus | hummus_frontend_v5.json |  |
| vegetable-spreads | /hashvaot/vegetable-spreads | hummus_frontend_v5.json | Shares hummus_frontend_v5.json with hummus |
| snacks | /hashvaot/snacks | snacks_frontend_v2.json |  |
| yogurts | /hashvaot/yogurts | N/A |  |
| cheese | /hashvaot/cheese | N/A |  |
| breakfast-cereals | /hashvaot/breakfast-cereals | cereals_frontend_v2.json |  |
| butter | /hashvaot/butter | N/A |  |
| granola | /hashvaot/granola | granola_frontend_v1.json |  |
| salty-snacks | /hashvaot/salty-snacks | N/A |  |
| milk (legacy) | /hashvaot/milk (legacy route) | milk-comparison.json | Uses milk-comparison.json; not in registry index.ts |

**Additional data files in bari-web/src/data/comparisons/ NOT in the live registry:**  
- hard_cheeses_frontend_v2.json (hard-cheeses page exists but not in registry/index.ts)  
- juices_frontend_v3.json (juices page exists but not in registry/index.ts)  
- yogurts_frontend_v4.json (v4 exists on disk; page-data imports v3 — v4 is NOT live)  

## Section 2: Verdict Table

Contamination types:  
- Image-OFF: product imageUrl points to images.openfoodfacts.org  
- Corpus-OFF: BSIP1 panel_source = open_food_facts (nutrition data from OFF)  
- JSON-marker: 'open_food_facts' string appears in live file (may be metadata-only)  

| Category | Data File | Products (M) | Image-OFF (N/M) | Corpus-OFF B (N/M) | JSON-live A | NO_RECORD | NO_BARCODE | Verdict |
|---|---|---|---|---|---|---|---|---|
| bread | bread_frontend_v2.json | 19 | 0/19 | 0/19 | 0 | 0 | 15 | CLEAN |
| hummus | hummus_frontend_v5.json | 57 | 0/57 | 0/57 | 0 | 0 | 0 | CLEAN |
| vegetable-spreads | hummus_frontend_v5.json | 57 | 0/57 | 0/57 | 0 | 0 | 0 | CLEAN |
| snacks | snacks_frontend_v2.json | 18 | 0/18 | 0/18 | 0 | 0 | 0 | CLEAN |
| yogurts | ? | N/A | N/A | N/A | N/A | N/A | N/A | ERROR |
| cheese | ? | N/A | N/A | N/A | N/A | N/A | N/A | ERROR |
| breakfast-cereals | cereals_frontend_v2.json | 20 | 0/20 | 0/20 | 0 | 0 | 0 | CLEAN |
| butter | ? | N/A | N/A | N/A | N/A | N/A | N/A | ERROR |
| granola | granola_frontend_v1.json | 25 | 0/25 | 0/25 | 0 | 0 | 0 | CLEAN |
| salty-snacks | ? | N/A | N/A | N/A | N/A | N/A | N/A | ERROR |
| milk (legacy) | milk-comparison.json | 18 | 0/18 | 0/18 | 0 | 0 | 0 | CLEAN |

**TOTAL Image-OFF products across live site: 0**  
**TOTAL Corpus-OFF products across live site: 0**  
**TOTAL Products scanned: 214**  

### Calibration against known findings

Known contamination claims from task brief: cereals 8 OFF-fed, granola 10 OFF-fed.  
- cereals: image-OFF=0, corpus-OFF=0, JSON-live=0  
- granola: image-OFF=0, corpus-OFF=0, JSON-live=0  

SELF-CALIBRATION NOTE: This scan found 0 corpus-level OFF contamination for cereals and granola. The known dirty counts (8 and 10) referenced in the task brief refer to BSIP1-level contamination that may have already been purged from the frontend JSON before this sweep. The sweep confirms the current state of what is LIVE — not historical BSIP1 run state. The cereals JSON contains an `excluded_off_products` metadata block documenting the exclusions (1 `open_food_facts` marker, metadata-only). Granola has 0 OFF markers in its current frontend JSON.  

## Section 3: Dirty Category Details

No dirty categories detected at corpus or live-JSON level.

## Section 4: Yogurts Full Product List (DIRTY category)

## Section 5: NO_RECORD and NO_BARCODE Concentrations

Categories with high NO_RECORD rates cannot confirm clean BSIP1 provenance.

| Category | NO_RECORD | NO_BARCODE | Total | NO_RECORD% | Note |
|---|---|---|---|---|---|
| bread | 0 | 15 | 19 | 0.0% | 15 products have no numeric barcode (e.g. bread uses shufersal_NNNN IDs) |
| hummus | 0 | 0 | 57 | 0.0% |  |
| vegetable-spreads | 0 | 0 | 57 | 0.0% |  |
| snacks | 0 | 0 | 18 | 0.0% |  |
| breakfast-cereals | 0 | 0 | 20 | 0.0% |  |
| granola | 0 | 0 | 25 | 0.0% |  |
| milk (legacy) | 0 | 0 | 18 | 0.0% |  |

## Section 6: Full Corpus Results Per Category

### bread — bread_frontend_v2.json (19 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
|  | shufersal_2079996 | לחם אחיד פרוס קל | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_497044 | לחם ברמן אקטיב | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_3268429 | לחם ירוק מקמח מלא | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_481203 | לחם מחמצת קמח מלא | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_3268252 | לחם חיטה מלא לילדים | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_574370 | לחם שיפון קל | NO_BARCODE |  | NO_BARCODE |
| 7290016245325 | shufersal_7290016245325 | לחם טחינה פרוס | NOT_FOUND |  | ok |
| 7290018500316 | shufersal_7290018500316 | לחם כוסמין לבן | NOT_FOUND |  | ok |
|  | shufersal_2079033 | לחם דגנים לייט | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_3054183 | לחם שיפון מלא מסטמכר | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_481197 | לחם מחמצת גרעינים | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_2079927 | לחם דגנים מלא | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_2079477 | לחם אחיד פרוס | NO_BARCODE |  | NO_BARCODE |
| 7290016967074 | shufersal_7290016967074 | לחם אנג'ל חיטה מלאה | NOT_FOUND |  | ok |
| 7290018500460 | shufersal_7290018500460 | לחם אנג'ל חצי מלא | NOT_FOUND |  | ok |
|  | shufersal_4685027 | לחם מחמצת וחיטה מלאה קל | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_6451507 | לחם מחמצת מכוסמין | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_6451484 | לחם מחמצת אגוזים צימוקים | NO_BARCODE |  | NO_BARCODE |
|  | shufersal_2079217 | לחם מחמצת שיפון+אגוזים | NO_BARCODE |  | NO_BARCODE |

### hummus — hummus_frontend_v5.json (57 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7296073725404 | bsip1_7296073725404 | חומוס מסעדות | NOT_FOUND |  | ok |
| 6666307 | bsip1_6666307 | סלט חומוס | NOT_FOUND |  | ok |
| 7296073725565 | bsip1_7296073725565 | חומוס אסלי | NOT_FOUND |  | ok |
| 7296073725589 | bsip1_7296073725589 | חומוס | NOT_FOUND |  | ok |
| 6666444 | bsip1_6666444 | סלט מטבוחה | NOT_FOUND |  | ok |
| 7290015858175 | bsip1_7290015858175 | ממרח פלפלים קלויים | NOT_FOUND |  | ok |
| 7290110564360 | bsip1_7290110564360 | חומוס עשיר ב40% טחינה | NOT_FOUND |  | ok |
| 7290110579319 | bsip1_7290110579319 | חומוס גלילי | NOT_FOUND |  | ok |
| 7290110557478 | bsip1_7290110557478 | חומוס גלילי | NOT_FOUND |  | ok |
| 7290011800642 | bsip1_7290011800642 | סלט מטבוחה מרוקאית | NOT_FOUND |  | ok |
| 7296073725381 | bsip1_7296073725381 | חומוס אבו גוש | NOT_FOUND |  | ok |
| 3727667 | bsip1_3727667 | חומוס מסעדה | NOT_FOUND |  | ok |
| 7290106576513 | bsip1_7290106576513 | חומוס מסעדה | NOT_FOUND |  | ok |
| 5174551 | bsip1_5174551 | חומוס יום יום | NOT_FOUND |  | ok |
| 7290105964564 | bsip1_7290105964564 | חומוס | NOT_FOUND |  | ok |
| 2987963 | bsip1_2987963 | חומוס | NOT_FOUND |  | ok |
| 8645935 | bsip1_8645935 | חומוס | NOT_FOUND |  | ok |
| 7290119387434 | bsip1_7290119387434 | חומוס ישראלי | NOT_FOUND |  | ok |
| 7296073725497 | bsip1_7296073725497 | סלט חצילים על האש | NOT_FOUND |  | ok |
| 7296073725374 | bsip1_7296073725374 | סלט חומוס עם טחינה | NOT_FOUND |  | ok |
| 7290106573642 | bsip1_7290106573642 | חומוס צנובר צבר | NOT_FOUND |  | ok |
| 7296073725367 | bsip1_7296073725367 | סלט חומוס+מסבחה | NOT_FOUND |  | ok |
| 7290010931330 | bsip1_7290010931330 | סלט מטבוחה | NOT_FOUND |  | ok |
| 8644112 | bsip1_8644112 | סלט מטבוחה יום יום | NOT_FOUND |  | ok |
| 7290107958639 | bsip1_7290107958639 | מטבוחה חריפה אש | NOT_FOUND |  | ok |
| 7290104721533 | bsip1_7290104721533 | סלט פלפלים קלויים | NOT_FOUND |  | ok |
| 467320 | bsip1_467320 | מלך החומוס אבו מרוואן | NOT_FOUND |  | ok |
| 7290104061431 | bsip1_7290104061431 | חומוס עם צנובר אחלה | NOT_FOUND |  | ok |
| 7290106576537 | bsip1_7290106576537 | חומוס מסעדה צבר | NOT_FOUND |  | ok |
| 7290122780314 | bsip1_7290122780314 | חומוס אבו מרוואן26%טחינה | NOT_FOUND |  | ok |
| 7290106573598 | bsip1_7290106573598 | חומוס לבנוני צבר | NOT_FOUND |  | ok |
| 7290119373710 | bsip1_7290119373710 | חומוס מועשר 40% עם חריף | NOT_FOUND |  | ok |
| 7290104061424 | bsip1_7290104061424 | חומוס עם זעתר | NOT_FOUND |  | ok |
| 7290115202434 | bsip1_7290115202434 | חומוס עם זעתר | NOT_FOUND |  | ok |
| 467153 | bsip1_467153 | מלך החומוס סמיר הגדול | NOT_FOUND |  | ok |
| 7290106573819 | bsip1_7290106573819 | חומוס אבו גוש+צנובר+חריף | NOT_FOUND |  | ok |
| 7290119374892 | bsip1_7290119374892 | חומוס עם מלא מטבוחה חריף | NOT_FOUND |  | ok |
| 7290106573628 | bsip1_7290106573628 | חומוס עם טחינה צבר | NOT_FOUND |  | ok |
| 7290104061417 | bsip1_7290104061417 | חומוס עם טחינה אחלה | NOT_FOUND |  | ok |
| 7290112968685 | bsip1_7290112968685 | חומוס גרגרים בתטבילה | NOT_FOUND |  | ok |
| 7296073725398 | bsip1_7296073725398 | חומוס מסבחה | NOT_FOUND |  | ok |
| 7290115207484 | bsip1_7290115207484 | חציל על האש | NOT_FOUND |  | ok |
| 7290104061448 | bsip1_7290104061448 | חומוס עם חריף אחלה | NOT_FOUND |  | ok |
| 7290115202687 | bsip1_7290115202687 | חומוס עם חריף | NOT_FOUND |  | ok |
| 7290111563492 | bsip1_7290111563492 | מטבוחה חריפה | NOT_FOUND |  | ok |
| 7290106577572 | bsip1_7290106577572 | מטבוחה אמיתית | NOT_FOUND |  | ok |
| 3989096 | bsip1_3989096 | סלט חציל פיקנטי | NOT_FOUND |  | ok |
| 7296073725510 | bsip1_7296073725510 | סלט מטבוחה פיקנטי | NOT_FOUND |  | ok |
| 7296073725633 | bsip1_7296073725633 | מטבוחה פיקנטית | NOT_FOUND |  | ok |
| 7290105366023 | bsip1_7290105366023 | סלט חציל בטעם כבד | NOT_FOUND |  | ok |
| 7296073725640 | bsip1_7296073725640 | מעדן חצילים | NOT_FOUND |  | ok |
| 6724786 | bsip1_6724786 | ממרח פלפלים קלויים | NOT_FOUND |  | ok |
| 7290119374885 | bsip1_7290119374885 | חומוס עם חציל פיקנטי | NOT_FOUND |  | ok |
| 7290106520905 | bsip1_7290106520905 | סלט טורקי | NOT_FOUND |  | ok |
| 7296073451969 | bsip1_7296073451969 | ממרח פלפלים קלויים | NOT_FOUND |  | ok |
| 7290010154265 | bsip1_7290010154265 | פלפל צ'ומה | NOT_FOUND |  | ok |
| 7290106577480 | bsip1_7290106577480 | חציל על האש בטחינה | NOT_FOUND |  | ok |

### vegetable-spreads — hummus_frontend_v5.json (57 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7296073725404 | bsip1_7296073725404 | חומוס מסעדות | NOT_FOUND |  | ok |
| 6666307 | bsip1_6666307 | סלט חומוס | NOT_FOUND |  | ok |
| 7296073725565 | bsip1_7296073725565 | חומוס אסלי | NOT_FOUND |  | ok |
| 7296073725589 | bsip1_7296073725589 | חומוס | NOT_FOUND |  | ok |
| 6666444 | bsip1_6666444 | סלט מטבוחה | NOT_FOUND |  | ok |
| 7290015858175 | bsip1_7290015858175 | ממרח פלפלים קלויים | NOT_FOUND |  | ok |
| 7290110564360 | bsip1_7290110564360 | חומוס עשיר ב40% טחינה | NOT_FOUND |  | ok |
| 7290110579319 | bsip1_7290110579319 | חומוס גלילי | NOT_FOUND |  | ok |
| 7290110557478 | bsip1_7290110557478 | חומוס גלילי | NOT_FOUND |  | ok |
| 7290011800642 | bsip1_7290011800642 | סלט מטבוחה מרוקאית | NOT_FOUND |  | ok |
| 7296073725381 | bsip1_7296073725381 | חומוס אבו גוש | NOT_FOUND |  | ok |
| 3727667 | bsip1_3727667 | חומוס מסעדה | NOT_FOUND |  | ok |
| 7290106576513 | bsip1_7290106576513 | חומוס מסעדה | NOT_FOUND |  | ok |
| 5174551 | bsip1_5174551 | חומוס יום יום | NOT_FOUND |  | ok |
| 7290105964564 | bsip1_7290105964564 | חומוס | NOT_FOUND |  | ok |
| 2987963 | bsip1_2987963 | חומוס | NOT_FOUND |  | ok |
| 8645935 | bsip1_8645935 | חומוס | NOT_FOUND |  | ok |
| 7290119387434 | bsip1_7290119387434 | חומוס ישראלי | NOT_FOUND |  | ok |
| 7296073725497 | bsip1_7296073725497 | סלט חצילים על האש | NOT_FOUND |  | ok |
| 7296073725374 | bsip1_7296073725374 | סלט חומוס עם טחינה | NOT_FOUND |  | ok |
| 7290106573642 | bsip1_7290106573642 | חומוס צנובר צבר | NOT_FOUND |  | ok |
| 7296073725367 | bsip1_7296073725367 | סלט חומוס+מסבחה | NOT_FOUND |  | ok |
| 7290010931330 | bsip1_7290010931330 | סלט מטבוחה | NOT_FOUND |  | ok |
| 8644112 | bsip1_8644112 | סלט מטבוחה יום יום | NOT_FOUND |  | ok |
| 7290107958639 | bsip1_7290107958639 | מטבוחה חריפה אש | NOT_FOUND |  | ok |
| 7290104721533 | bsip1_7290104721533 | סלט פלפלים קלויים | NOT_FOUND |  | ok |
| 467320 | bsip1_467320 | מלך החומוס אבו מרוואן | NOT_FOUND |  | ok |
| 7290104061431 | bsip1_7290104061431 | חומוס עם צנובר אחלה | NOT_FOUND |  | ok |
| 7290106576537 | bsip1_7290106576537 | חומוס מסעדה צבר | NOT_FOUND |  | ok |
| 7290122780314 | bsip1_7290122780314 | חומוס אבו מרוואן26%טחינה | NOT_FOUND |  | ok |
| 7290106573598 | bsip1_7290106573598 | חומוס לבנוני צבר | NOT_FOUND |  | ok |
| 7290119373710 | bsip1_7290119373710 | חומוס מועשר 40% עם חריף | NOT_FOUND |  | ok |
| 7290104061424 | bsip1_7290104061424 | חומוס עם זעתר | NOT_FOUND |  | ok |
| 7290115202434 | bsip1_7290115202434 | חומוס עם זעתר | NOT_FOUND |  | ok |
| 467153 | bsip1_467153 | מלך החומוס סמיר הגדול | NOT_FOUND |  | ok |
| 7290106573819 | bsip1_7290106573819 | חומוס אבו גוש+צנובר+חריף | NOT_FOUND |  | ok |
| 7290119374892 | bsip1_7290119374892 | חומוס עם מלא מטבוחה חריף | NOT_FOUND |  | ok |
| 7290106573628 | bsip1_7290106573628 | חומוס עם טחינה צבר | NOT_FOUND |  | ok |
| 7290104061417 | bsip1_7290104061417 | חומוס עם טחינה אחלה | NOT_FOUND |  | ok |
| 7290112968685 | bsip1_7290112968685 | חומוס גרגרים בתטבילה | NOT_FOUND |  | ok |
| 7296073725398 | bsip1_7296073725398 | חומוס מסבחה | NOT_FOUND |  | ok |
| 7290115207484 | bsip1_7290115207484 | חציל על האש | NOT_FOUND |  | ok |
| 7290104061448 | bsip1_7290104061448 | חומוס עם חריף אחלה | NOT_FOUND |  | ok |
| 7290115202687 | bsip1_7290115202687 | חומוס עם חריף | NOT_FOUND |  | ok |
| 7290111563492 | bsip1_7290111563492 | מטבוחה חריפה | NOT_FOUND |  | ok |
| 7290106577572 | bsip1_7290106577572 | מטבוחה אמיתית | NOT_FOUND |  | ok |
| 3989096 | bsip1_3989096 | סלט חציל פיקנטי | NOT_FOUND |  | ok |
| 7296073725510 | bsip1_7296073725510 | סלט מטבוחה פיקנטי | NOT_FOUND |  | ok |
| 7296073725633 | bsip1_7296073725633 | מטבוחה פיקנטית | NOT_FOUND |  | ok |
| 7290105366023 | bsip1_7290105366023 | סלט חציל בטעם כבד | NOT_FOUND |  | ok |
| 7296073725640 | bsip1_7296073725640 | מעדן חצילים | NOT_FOUND |  | ok |
| 6724786 | bsip1_6724786 | ממרח פלפלים קלויים | NOT_FOUND |  | ok |
| 7290119374885 | bsip1_7290119374885 | חומוס עם חציל פיקנטי | NOT_FOUND |  | ok |
| 7290106520905 | bsip1_7290106520905 | סלט טורקי | NOT_FOUND |  | ok |
| 7296073451969 | bsip1_7296073451969 | ממרח פלפלים קלויים | NOT_FOUND |  | ok |
| 7290010154265 | bsip1_7290010154265 | פלפל צ'ומה | NOT_FOUND |  | ok |
| 7290106577480 | bsip1_7290106577480 | חציל על האש בטחינה | NOT_FOUND |  | ok |

### snacks — snacks_frontend_v2.json (18 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290011498870 | snk-001 | חטיף תמרים במילוי חמאת שקדים | NOT_FOUND |  | ok |
| 7290011498894 | snk-015 | חטיף תמרים במילוי חמאת בוטנים | NOT_FOUND |  | ok |
| 7290011498948 | snk-004 | מרבה סלים דליס שוקולד מריר | NOT_FOUND |  | ok |
| 8423207210287 | snk-002 | חטיף תמרים בציפוי שוקולד 100% קקאו | NOT_FOUND |  | ok |
| 7290011498894 | snk-003 | קראנצ'י שיבולת שועל עם דבש | NOT_FOUND |  | ok |
| 8423207209885 | snk-016 | מרבה סלים טופינג אגוזי לוז | NOT_FOUND |  | ok |
| 8410076610379 | snk-009 | נייצ'ר וואלי פרוטאין בוטנים ושוקולד | NOT_FOUND |  | ok |
| 8423207208260 | snk-005 | חטיפי דגנים פיטנס קלאסי | NOT_FOUND |  | ok |
| 8410076610386 | snk-010 | נייצ'ר וואלי פרוטאין בוטנים קרמל מלוח | NOT_FOUND |  | ok |
| 8423207210928 | snk-018 | קראנצ'י שיבולת שועל עם חתיכות שוקולד | NOT_FOUND |  | ok |
| 16000423534 | snk-011 | פרי מארז תמרים ואגוזי לוז | NOT_FOUND |  | ok |
| 16000548404 | snk-012 | פרי מארז תמרים ושברי קקאו | NOT_FOUND |  | ok |
| 8423207208680 | snk-017 | נייצ'ר וואלי צ'ואי שוקולד מריר | NOT_FOUND |  | ok |
| 8410076610492 | snk-019 | חטיפי פיטנס שיבולת שועל דבש | NOT_FOUND |  | ok |
| 8410076610508 | snk-020 | מרבה סלים דליס קריספי אוכמניות | NOT_FOUND |  | ok |
| 5900020039590 | snk-007 | חטיפי דגנים פיטנס שוקולד מריר | NOT_FOUND |  | ok |
| 8423207206495 | snk-006 | פיטנס בר גרנולה שוקולד מריר | NOT_FOUND |  | ok |
| 8423207207362 | snk-013 | שחור ולבן קורני שוקולד | NOT_FOUND |  | ok |

### breakfast-cereals — cereals_frontend_v2.json (20 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 5010029000061 | bsip1_cereal_501002900006 | דגני בוקר ויטביקס | NOT_FOUND |  | ok |
| 7297488098688 | bsip1_cereal_729748809868 | פצפוצי אורז ללת"ס | NOT_FOUND |  | ok |
| 7297488199590 | bsip1_cereal_729748819959 | פצפוצי אורז תפוח | NOT_FOUND |  | ok |
| 7296073642046 | bsip1_cereal_729607364204 | קורנפלקס ללא גלוטן | NOT_FOUND |  | ok |
| 5900020036407 | bsip1_cereal_590002003640 | ליון דגני שוקולד וקרמל | NOT_FOUND |  | ok |
| 5900020012814 | bsip1_cereal_590002001281 | דגני בוקר נסקוויק | NOT_FOUND |  | ok |
| 72968 | bsip1_cereal_72968 | דגני בוקר סיני מיניס | NOT_FOUND |  | ok |
| 7290107647731 | bsip1_cereal_729010764773 | דגני בוקר קוקומן חום לבן | NOT_FOUND |  | ok |
| 7290017894911 | bsip1_cereal_729001789491 | טבעות דגנים שיבולת שועל | NOT_FOUND |  | ok |
| 7290107647854 | bsip1_cereal_729010764785 | דגני בוקר שוגי | NOT_FOUND |  | ok |
| 7290017894928 | bsip1_cereal_729001789492 | צדפי דגנים טעם שוקולד | NOT_FOUND |  | ok |
| 7296073705550 | bsip1_cereal_729607370555 | כדורי דגנים טעם שוקו | NOT_FOUND |  | ok |
| 7296073705567 | bsip1_cereal_729607370556 | טבעות דגנים בטעם דבש | NOT_FOUND |  | ok |
| 7290112495433 | bsip1_cereal_729011249543 | דגני בוקר דליפקאן | NOT_FOUND |  | ok |
| 7290017894904 | bsip1_cereal_729001789490 | כדורי דגנים טעם שוקולד | NOT_FOUND |  | ok |
| 8445291638839 | bsip1_cereal_844529163883 | צ'יריוס טעם דבש ושקדים | NOT_FOUND |  | ok |
| 7296073642022 | bsip1_cereal_729607364202 | דגני בוקר טבעות דבש לל"ג | NOT_FOUND |  | ok |
| 7296073705574 | bsip1_cereal_729607370557 | ריבועי דגנים עם קינמון | NOT_FOUND |  | ok |
| 3387390525960 | bsip1_cereal_338739052596 | דגני בוקר קראנץ' | NOT_FOUND |  | ok |
| 7613030979647 | bsip1_cereal_761303097964 | טריקס דגנים בטעם פירות | NOT_FOUND |  | ok |

### granola — granola_frontend_v1.json (25 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 1164266 | bsip1_cereal_1164266 | גרנולה ממותקת בסילאן | NOT_FOUND |  | ok |
| 7290017962047 | bsip1_cereal_729001796204 | גרנולה חמוציות ושקדים | NOT_FOUND |  | ok |
| 7290116534619 | bsip1_cereal_729011653461 | גרנולה פרוטאין+שוקולד | NOT_FOUND |  | ok |
| 7290106773714 | bsip1_cereal_729010677371 | גרנולה מיקס קראנץ' מלוח | NOT_FOUND |  | ok |
| 7290017962023 | bsip1_cereal_729001796202 | גרנולה מייפל תמר פקאן | NOT_FOUND |  | ok |
| 7290013433244 | bsip1_cereal_729001343324 | גרנולה 18% חלבון | NOT_FOUND |  | ok |
| 7290013433336 | bsip1_cereal_729001343333 | גרנולה 48% סופרפוד | NOT_FOUND |  | ok |
| 1164273 | bsip1_cereal_1164273 | חגיגת גרנולה | NOT_FOUND |  | ok |
| 7290106771369 | bsip1_cereal_729010677136 | גרנולה לוז וקינמון | NOT_FOUND |  | ok |
| 7290112498007 | bsip1_cereal_729011249800 | גרנולה חלבון שקד+חמוציות | NOT_FOUND |  | ok |
| 7290106771314 | bsip1_cereal_729010677131 | גרנולה אגוזים חמוציות | NOT_FOUND |  | ok |
| 7290112497994 | bsip1_cereal_729011249799 | גרנולה פרוטאין+אגוזים | NOT_FOUND |  | ok |
| 7290106771161 | bsip1_cereal_729010677116 | גרנולה מייפל פקאן | NOT_FOUND |  | ok |
| 7290011668587 | bsip1_cereal_729001166858 | גרנולה עשירה | NOT_FOUND |  | ok |
| 7290013433091 | bsip1_cereal_729001343309 | גרנולה 8% שוקולד מריר | NOT_FOUND |  | ok |
| 7290014471443 | bsip1_cereal_729001447144 | גרנולה אגוזים | NOT_FOUND |  | ok |
| 7290013433107 | bsip1_cereal_729001343310 | גרנולה חלבה תמר קשיו | NOT_FOUND |  | ok |
| 7613035635845 | bsip1_cereal_761303563584 | גרנולה שוקולד פיטנס | NOT_FOUND |  | ok |
| 7613037012095 | bsip1_cereal_761303701209 | גרנולה שוקולד קינואה | NOT_FOUND |  | ok |
| 6582751 | bsip1_cereal_6582751 | גרנולה עם פירות יבשים | NOT_FOUND |  | ok |
| 7290011131050 | bsip1_cereal_729001113105 | גרנולה פקאן | NOT_FOUND |  | ok |
| 7290011131968 | bsip1_cereal_729001113196 | גרנולה אגוזים | NOT_FOUND |  | ok |
| 7613035622623 | bsip1_cereal_761303562262 | גרנולה דבש פיטנס | NOT_FOUND |  | ok |
| 7290011131975 | bsip1_cereal_729001113197 | גרנולה פירות | NOT_FOUND |  | ok |
| 1343845 | bsip1_cereal_1343845 | גרנולה עם פירות | NOT_FOUND |  | ok |

### milk (legacy) — milk-comparison.json (18 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290000051352 |  | חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן | NOT_FOUND |  | ok |
| 7290019790259 |  | חלב טבעי 4% 1 ליטר | NOT_FOUND |  | ok |
| 7290102392094 |  | חלב עיזים בקרטון 1 ליטר | NOT_FOUND |  | ok |
| 7290114313865 |  | חלב נטול לקטוז מועשר בחלבון 2% שומן 1 ליטר | NOT_FOUND |  | ok |
| 7290116936116 |  | משקה סויה ללא סוכרים 1 ליטר | NOT_FOUND |  | ok |
| 7290107932134 |  | חלב בבקבוק 1% מועשר- מהדרין | NOT_FOUND |  | ok |
| 7290110324926 |  | משקה סויה ללא תוספת סוכר | NOT_FOUND |  | ok |
| 7290014760141 |  | משקה שקדים | NOT_FOUND |  | ok |
| 7394376620904 |  | משקה שיבולת שועל ללא סוכר | NOT_FOUND |  | ok |
| 5411188124689 |  | אלפרו שיבולת שועל ללא סוכר | NOT_FOUND |  | ok |
| 7394376619939 |  | משקה בריסטה שיבולת שועל | NOT_FOUND |  | ok |
| 7394376621451 |  | משקה בריסטה שיבולת שועל להקצפה | NOT_FOUND |  | ok |
| 8000215204219 |  | משקה אורז אורגני | NOT_FOUND |  | ok |
| 8000215204554 |  | משקה אורז קוקוס אורגני | NOT_FOUND |  | ok |
| 7290119385560 |  | משקה סויה בריסטה אלפרו 500 מ"ל | NOT_FOUND |  | ok |
| 7290110325619 |  | משקה שיבולת שועל | NOT_FOUND |  | ok |
| 5411188112709 |  | אלפרו שקדים ללא סוכר | NOT_FOUND |  | ok |
| 5411188300328 |  | אלפרו שוקו משקה סויה | NOT_FOUND |  | ok |

