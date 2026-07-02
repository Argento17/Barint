# FORENSIC TRACEABILITY CENSUS — live published scores

Sources: provenance_manifest.json (15 served files) + manifest_roundtrip_v4.json (Phase B round-trip, tol=0.1).

## Per-category counts

CATEGORY            TOT FULL PART UNTR  FILECLASS     STATUS / ROUNDTRIP
bread               29    0   29    0  PARTIAL      GAP:NULL_meta_run_id / DRIFTS(off=1,max|Δ|=0.8)
brined_cheeses      36   36    0    0  FULLY_TRACEABLE REPRODUCIBLE_PENDING_RESHADOW / REPRODUCES
cakes               65   62    3    0  PARTIAL      REPRODUCIBLE_PENDING_RESHADOW / DRIFTS(off=3,max|Δ|=2.0)
cereals             20   14    6    0  PARTIAL      REPRODUCIBLE_PENDING_RESHADOW / DRIFTS(off=6,max|Δ|=2.8)
cheese              53    0   53    0  PARTIAL      GAP:NULL_meta_run_id / DRIFTS(off=22,max|Δ|=5.3)
chocolate_bars      23    0   23    0  PARTIAL      GAP:NULL_meta_run_id / DRIFTS(off=7,max|Δ|=0.4)
chocolate_tablets   35    0   33    2  PARTIAL      GAP:NULL_meta_run_id / DRIFTS(off=8,max|Δ|=4.5)
cookies_coffee     119    0    0  119  UNTRACEABLE  GAP:bsip1_dir_missing / CANNOT
granola             22    0    0   22  UNTRACEABLE  NO_CONFIG_BOUND / CANNOT
hard_cheeses        23   23    0    0  FULLY_TRACEABLE REPRODUCIBLE_PENDING_RESHADOW / REPRODUCES
hummus              57   57    0    0  FULLY_TRACEABLE REPRODUCIBLE_PENDING_RESHADOW / REPRODUCES
juices              17   17    0    0  FULLY_TRACEABLE REPRODUCIBLE_PENDING_RESHADOW / REPRODUCES
milk                18   16    2    0  PARTIAL      REPRODUCIBLE_PENDING_RESHADOW / DRIFTS(off=2,max|Δ|=4.1)
protein_bars        32    0    0   32  UNTRACEABLE  NO_CONFIG_BOUND / CANNOT
snacks              21    0   21    0  PARTIAL      GAP:NULL_meta_run_id / DRIFTS(off=3,max|Δ|=4.0)
--------------------------------------------------------------------------------------------
GRAND TOTAL        570  225  170  175

PARTIAL=170  UNTRACEABLE=175  FULLY=225  TOTAL=570

## PRODUCING RUN_IDS
- `(NULL via bsip1=output)` -> ['bread_frontend_v3.json', 'cheese_frontend_v4.json', 'chocolate_bars_frontend_v1.json', 'chocolate_tablets_frontend_v1.json', 'snacks_frontend_v5.json']
- `run_brined_005` -> ['brined_cheeses_frontend_v2.json']
- `run_cakes_shelfrel_001` -> ['cakes_hard_cookies_frontend_v1.json']
- `run_cereals_task387_25g` -> ['cereals_frontend_v2.json']
- `run_cookies_005+run_cakes_001_cookies` -> ['cookies_coffee_frontend_v2.json']
- `run_granola_task385_25g` -> ['granola_frontend_v2.json']
- `run_hc_redlabel_v2_001` -> ['hard_cheeses_frontend_v2.json']
- `run_hummus_shelfrel_002` -> ['hummus_frontend_v5.json']
- `run_juices_shelfrel_001` -> ['juices_frontend_v3.json']
- `run_005_headpin` -> ['milk_frontend_v1.json']
- `protein_bars_task365_rescore_20260621_134052` -> ['protein_combined_frontend_v2.json']

## FULL PARTIAL + UNTRACEABLE PRODUCT LIST
category | barcode | name | bucket | what is lost/missing | served_file
bread | 7290016245325 | לחם טחינה פרוס | PARTIAL | flag_drift d=-0.8 (pub 94.8 -> 94.0) | bread_frontend_v3.json
bread | 3268429 | לחם ירוק מקמח מלא | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 3268252 | לחם חיטה מלא לילדים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 481203 | לחם מחמצת קמח מלא | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 481197 | לחם מחמצת גרעינים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 574370 | לחם שיפון קל | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 3054183 | לחם שיפון מלא מסטמכר | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 2079033 | לחם דגנים לייט | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 2079927 | לחם דגנים מלא | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 497044 | לחם ברמן אקטיב | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 2079996 | לחם אחיד פרוס קל | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 7290018500316 | לחם כוסמין לבן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 96086000966 | קרקר כוסמין מלא ושומשום | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 96086000577 | קרקר כוסמין אורגני | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 7290018540329 | פיתה פיתה | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 2079477 | לחם אחיד פרוס | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 9398281 | מארז פיתות אסליות | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 7296073134459 | קרקר פריך בסגנון שוודי | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 7296073134442 | קרקר פריך עם קמח שיפון | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 2079217 | לחם מחמצת שיפון+אגוזים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 7290014321168 | לחם לס פרוס קיטו | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 8434165658523 | קרקר קרם קרקר | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 6451484 | לחם מחמצת אגוזים צימוקים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 6451507 | לחם מחמצת מכוסמין | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 7290018500460 | לחם אנג'ל חצי מלא | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 4685027 | לחם מחמצת וחיטה מלאה קל | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 7290016967074 | לחם אנג'ל חיטה מלאה | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 74252 | קרקר שומשום אסם | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
bread | 1902325 | חלה קלועה | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | bread_frontend_v3.json
cakes | 5718038 | עוגת שטרודל תפוחי עץ | PARTIAL | flag_drift d=+1.4 (pub 17.5 -> 18.9) | cakes_hard_cookies_frontend_v1.json
cakes | 7290123330884 | עוגה בטעם שוקולד כשל"פ — קקאו | PARTIAL | flag_drift d=+0.2 (pub 9.6 -> 9.8) | cakes_hard_cookies_frontend_v1.json
cakes | 1361177 | עוגת פס דובדבנים | PARTIAL | flag_drift d=+2.0 (pub 7.9 -> 9.9) | cakes_hard_cookies_frontend_v1.json
cereals | 7297488199590 | פצפוצי אורז תפוח | PARTIAL | flag_drift d=+2.8 (pub 59.0 -> 61.8) | cereals_frontend_v2.json
cereals | 7296073642046 | קורנפלקס ללא גלוטן | PARTIAL | flag_drift d=+0.8 (pub 55.4 -> 56.2) | cereals_frontend_v2.json
cereals | 7290107647731 | דגני בוקר קוקומן חום לבן | PARTIAL | flag_drift d=+0.7 (pub 54.3 -> 55.0) | cereals_frontend_v2.json
cereals | 7290107647854 | דגני בוקר שוגי | PARTIAL | flag_drift d=+0.9 (pub 46.8 -> 47.7) | cereals_frontend_v2.json
cereals | 7290112495433 | דגני בוקר דליפקאן | PARTIAL | flag_drift d=-2.0 (pub 43.0 -> 41.0) | cereals_frontend_v2.json
cereals | 7613030979647 | טריקס דגנים בטעם פירות | PARTIAL | flag_drift d=-2.0 (pub 32.2 -> 30.2) | cereals_frontend_v2.json
cheese | 7290014758681 | קוטג 1% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 6040619 | גבינה טבורוג 5% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 4127077 | קוטג' 3% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 4127329 | קוטג' 5% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 41445 | קוטג' תנובה 5% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290110321277 | קוטג' בקטנה 5% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 474502 | גבינה לבנה 5% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290010945481 | גבינה לבנה 5% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290102393268 | גבינה לבנה 5% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290116934280 | גבינה לבנה 5%+שמיר ושום | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 2868996 | קוטג' 5% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290114311472 | גבינה לבנה 5% מהדרין | PARTIAL | flag_drift d=+2.2 (pub 73.5 -> 75.7) | cheese_frontend_v4.json
cheese | 7290114310918 | קוטג' 5% | PARTIAL | flag_drift d=+2.2 (pub 72.5 -> 74.7) | cheese_frontend_v4.json
cheese | 4127336 | קוטג' 9% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 41452 | קוטג' מהדרין 9% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 2824183 | גבינה לבנה סקי 5% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 2824640 | גבינה לבנה 5% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290108506624 | גבינת עזים 32% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 56272 | גבינה לבנה עם זיתים 5% | PARTIAL | flag_drift d=+0.2 (pub 66.0 -> 66.2) | cheese_frontend_v4.json
cheese | 7290116931241 | קוטג' 12% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290011194246 | קוטג' 5% שומן | PARTIAL | flag_drift d=+0.2 (pub 64.9 -> 65.1) | cheese_frontend_v4.json
cheese | 3523230065467 | גבינת עזים שום+עשב תיבול | PARTIAL | flag_drift d=+4.2 (pub 63.8 -> 68.0) | cheese_frontend_v4.json
cheese | 3075850 | לבנה עם זעתר | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290116934365 | נפוליאון 16% שום שמיר | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7622201798154 | גבינת פילדלפיה לייט 13% | PARTIAL | flag_drift d=+2.2 (pub 60.6 -> 62.8) | cheese_frontend_v4.json
cheese | 6492852 | גבינה לבנה עיזים 5% גד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290108504378 | גבינת שמנת עם זיתים 20% | PARTIAL | flag_drift d=+0.2 (pub 53.4 -> 53.6) | cheese_frontend_v4.json
cheese | 7290019635369 | גבינת שמנת 16% שומן | PARTIAL | flag_drift d=+2.3 (pub 54.7 -> 57.0) | cheese_frontend_v4.json
cheese | 7290014759084 | גבינת שמנת בטעם טבעי16% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290019635376 | גבינת שמנת גורגונזולה24% | PARTIAL | flag_drift d=+4.3 (pub 51.2 -> 55.5) | cheese_frontend_v4.json
cheese | 7290119375219 | גבינה 5% עם תבלין בייגלס | PARTIAL | flag_drift d=+5.3 (pub 48.9 -> 54.2) | cheese_frontend_v4.json
cheese | 554983 | גבינה לאבנה5%  א.ח.נוכרי | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290108502541 | גבינת שמנת טבעי 18% | PARTIAL | flag_drift d=+0.1 (pub 43.6 -> 43.7) | cheese_frontend_v4.json
cheese | 7622201521493 | פילדלפיה שום+ע.תיבול 12% | PARTIAL | flag_drift d=+0.2 (pub 45.3 -> 45.5) | cheese_frontend_v4.json
cheese | 554969 | גבינת שמנת 30% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 554976 | גבינת שמנת 30% עם זיתים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 5992889 | גבינת שמנת שום שמיר 30% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7296073453123 | גבינת שמנת 30% שומן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7622201139278 | גבינת שמנת 25% פילדלפיה | PARTIAL | flag_drift d=+0.1 (pub 43.5 -> 43.6) | cheese_frontend_v4.json
cheese | 7290116935409 | גבינת שמנת מוקצפת 25% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290014762831 | גבינת שמנת+פלפל חלפיניו | PARTIAL | flag_drift d=+0.2 (pub 44.8 -> 45.0) | cheese_frontend_v4.json
cheese | 7290112342102 | גבינה 5% בצל מקורמל | PARTIAL | flag_drift d=+0.3 (pub 42.6 -> 42.9) | cheese_frontend_v4.json
cheese | 7290116936604 | גבינת שמנת עשבי תיבול25% | PARTIAL | flag_drift d=+0.2 (pub 44.5 -> 44.7) | cheese_frontend_v4.json
cheese | 7290019635116 | גבינת שמנת זיתים 5% | PARTIAL | flag_drift d=+4.2 (pub 44.3 -> 48.5) | cheese_frontend_v4.json
cheese | 4129118 | גבינת שמנת 24% עם זיתים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 4129101 | גבינת נפוליאון בטעם טבעי | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 4129156 | גבינת נפוליאון שום שמיר | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290116931982 | גבינת שמנת עם עירית 25% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290116933078 | גבינת שמנת+פלפל פיקנטי | PARTIAL | flag_drift d=+0.2 (pub 42.7 -> 42.9) | cheese_frontend_v4.json
cheese | 7290116932644 | גבינת שמנת 25% עם זעתר | PARTIAL | flag_drift d=+0.3 (pub 41.7 -> 42.0) | cheese_frontend_v4.json
cheese | 7290011499624 | גבינת שמנת טעם טבעי 30% | PARTIAL | flag_drift d=+0.2 (pub 31.6 -> 31.8) | cheese_frontend_v4.json
cheese | 7290019635581 | גבינת שמנת סלסה 24% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
cheese | 7290019635383 | גבינת שמנת ריבת בצל 24% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | cheese_frontend_v4.json
chocolate_bars | 5000159560511 | סניקרס חטיף בודד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 72991008 | שוקולד פסק זמן קלאסי | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290106651265 | פסק זמן קלאסי מגדים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290116536781 | קליק אין קרם חלבי | PARTIAL | flag_drift d=+0.2 (pub 17.6 -> 17.8) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290116536774 | קליק אין קרם נוגט | PARTIAL | flag_drift d=+0.2 (pub 17.4 -> 17.6) | chocolate_bars_frontend_v1.json
chocolate_bars | 5900951310379 | סניקרס קרימי חטיף בודד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290110571405 | מיני פינוקיות פסק זמן | PARTIAL | flag_drift d=+0.1 (pub 16.0 -> 16.1) | chocolate_bars_frontend_v1.json
chocolate_bars | 5000159559485 | טוויקס חטיף בודד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 3800020401552 | קיט קט צ'אנקי פאנקי | PARTIAL | flag_drift d=+0.1 (pub 15.7 -> 15.8) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290105362377 | כיף כף מגדים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290100249086 | חטיף קליק נוגט לבן כשל"פ | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290116532011 | חטיף קליק נוגט | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290116531748 | קליק שוקו מיקס כשל"פ | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290116532042 | קליק כריות נוגט כשל"פ | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290116537375 | קליק כריות | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290112494283 | קליק חום לבן | PARTIAL | flag_drift d=+0.1 (pub 14.7 -> 14.8) | chocolate_bars_frontend_v1.json
chocolate_bars | 72917329 | חטיף שוקולד אגוזי | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 72917367 | חטיף שוקולד טעמי | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 4823077617041 | חטיף שוקולד ממולא קרמל | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 5000159561976 | באונטי חטיף בודד | PARTIAL | flag_drift d=+0.4 (pub 13.1 -> 13.5) | chocolate_bars_frontend_v1.json
chocolate_bars | 7290116534442 | חטיף שוקולד קרם חלבי | PARTIAL | flag_drift d=+0.4 (pub 12.9 -> 13.3) | chocolate_bars_frontend_v1.json
chocolate_bars | 72918388 | חטיף שוקולד טוויסט | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_bars | 34000250103 | חטיף שוקולד ממולא בוטנים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_bars_frontend_v1.json
chocolate_tablets | 7296073382416 | שוקולד מריר 90% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290112197467 | שוקולד מריר | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 3046920029759 | שוקולד מריר לינדט 90% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 4000539280740 | שוקולד מריר לינדט 78% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290119500437 | טוסו שוקולד מריר | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290018893609 | צ'וקטה שוקולד מריר 85% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290112197443 | שוקולד חלב | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290119500383 | טוסו שוקולד חלב | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 3046920028363 | שוקולד מריר לינדט 85% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290105961525 | שוקולד ספלנדיד מריר 85% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 5941021001674 | שוקולד מריר 85% | PARTIAL | flag_drift d=+4.4 (pub 42.5 -> 46.9) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7296073747819 | שוקולד מריר פרימיום 81% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290107955782 | טבלת שוקולד מריר ללת"ס | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 4000539280726 | שוקולד מריר לינדט70%מילד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7610400075770 | שוק.לינדט מריר אגוזי לוז | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7296073747802 | שוקולד מריר פרימיום 75% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 4000417025005 | שוקולד מריר עם מרציפן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 3046920023047 | לינדט אקסלנס פיסטוק | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 3046920028004 | שוקולד מריר לינדט 70% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290018893401 | צ'וקטה שוקולד מריר 70% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290019870043 | צ'וקטה שוקולד מריר 60% | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290019939412 | שוקולד חלב ללא סוכר | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 3046920028752 | שוקולד מריר לינדט מנטה | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 3046920029674 | שוקולד מריר לינדט מלח | PARTIAL | flag_drift d=+0.1 (pub 22.4 -> 22.5) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290112331984 | שוקולד פרה קראנצ' בסקויט | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7610008641001 | טבלת טורינו חלב | PARTIAL | flag_drift d=+4.5 (pub 19.4 -> 23.9) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7614500010617 | טובלרון מריר | PARTIAL | flag_drift d=+0.1 (pub 17.4 -> 17.5) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290110579463 | שוקולד פרה חלב שברי אגוז | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7622202257506 | מילקה אקסטרה קקאו | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7614500010013 | טובלרון חלב 100 גרם | PARTIAL | flag_drift d=+0.9 (pub 14.8 -> 15.7) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7622202265648 | שוקולד לבן מילקה | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290112914699 | שוקולד חלב וקרמל מלוח | PARTIAL | flag_drift d=+0.2 (pub 14.0 -> 14.2) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290112348548 | שוקולד פרה לבן | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | chocolate_tablets_frontend_v1.json
milk | 7290110324926 | משקה סויה ללא תוספת סוכר | PARTIAL | flag_drift d=+0.2 (pub 56.7 -> 56.9) | milk_frontend_v1.json
milk | 7290110325619 | משקה שיבולת שועל | PARTIAL | flag_drift d=+4.1 (pub 47.6 -> 51.7) | milk_frontend_v1.json
snacks | 7290100659090 | חטיף FREE תמרים וקינמון | PARTIAL | flag_drift d=+0.1 (pub 66.8 -> 66.9) | snacks_frontend_v5.json
snacks | 7290011498894 | חטיפי תמר + חמאת בוטנים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 7290105436382 | חטיפי FREE תמרים קשיו | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 7290011498948 | חטיפי תמר בציפוי שוקולד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 7290105431516 | חטיפי FREE תמרים ובוטנים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 16000548404 | חטיף שיבולת שועל עם דבש | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 16000548503 | חטיף שיבולת שועל+מייפל | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 7290011498986 | חטיף תמרים עם חמאת קשיו | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 7290011498917 | חטיפי תמר+קוקוס מצופים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 7290011498900 | חטיף תמר עם חמאת שקד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 16000423534 | חטיף שיבולת שועל+שוקולד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 7290107971522 | חטיף בוטנים ושקדים קראנצ | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 6009684861000 | חטיף גרנולה דבש ומייפל | PARTIAL | flag_drift d=+4.0 (pub 26.0 -> 30.0) | snacks_frontend_v5.json
snacks | 8423207208703 | חטיף דגנים שוקולד מריר · סלים דליס | PARTIAL | flag_drift d=+0.2 (pub 24.4 -> 24.6) | snacks_frontend_v5.json
snacks | 8410076610508 | חטיף בוטנים עם שוקולד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 8423207208680 | חטיף קידס שוקולד חלב | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 8410076610492 | חטיף בוטנים ושיבולת שועל | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 7290019297208 | חטיף גרנולה פירות יבשים | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 4011800633516 | חטיף דגנים שוקולד מריר · קורני | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 4011800628512 | קורני חטיפי דגנים+שוקולד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
snacks | 4011800632519 | קורני חטיפי קוקוס שוקולד | PARTIAL | NULL_meta_run_id(resolvable via config+bsip1) | snacks_frontend_v5.json
chocolate_tablets | 7296073726562 | שוקולד מריר ללת"ס 72% | UNTRACEABLE | unscored_in_reproduction(score lost) | chocolate_tablets_frontend_v1.json
chocolate_tablets | 7290119500482 | טוסו שוקולד מריר 62% | UNTRACEABLE | unscored_in_reproduction(score lost) | chocolate_tablets_frontend_v1.json
cookies_coffee | 7290013453693 | עוגיות גרידת לימון ללת"ס — דני וגלית | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119043149 | עוגיות בטעם חמאה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 80083764 | עוגיות דגנים עם ש.שועל | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290017962139 | עוגיות פירות יער כשל"פ — דני וגלית | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290020030184 | עוגיות מזרחיות עם זעתר 400 גרם אחוה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290122781359 | מיני עוגיות קלאסי פיטנס 80 גרם פיטנס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740113 | עוגיות מרוקאיות — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013453068 | עוגיות כוסמין פירות יער | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 540160 | עוגיות ללת"ס מקמח מלא — האחים | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740137 | עוגיות אוזן פיל — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119043743 | עוגיות מרוקאיות — לה פזואלוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740557 | עוגיות רייפעת — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740229 | עוגיות פרסות שקדים — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 960860015432 | עוגיות ללת"ס מקמח מלא — אביבה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 311463 | עוגיות חמאה ללת"ס — מן | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013453501 | ביסקוטי כוסמין שוקולד — דני וגלית | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740052 | עוגיות פרחי ריבה — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740540 | עוגיות אוזן פיל ללת"ס — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740472 | עוגיות מושלגות — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740465 | עוגיות שושנים — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740342 | עוגיות פרחי ריבה ללת"ס — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013156921 | עוגיות אצבעות מתוקות ללא סוכר גאקובס 350 גרם ג'ייקוב אנד אס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290017898506 | ביסקוטי — החוש השישי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290000061245 | עוגיות שוקוצ'יפס ממולאות 220 גרם אסם | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740014 | עוגיות שוקוצ'יפס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013156006 | עוגיות מיני מרוקאיות 350 גרם בבקה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290017894317 | עוגיות כוסמין מלא שוקולד — גנדולה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 5317194 | ביסקוויט בטעם וניל הדר — הדר | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 2986065 | פתי בר בטעם שוקולד — גטניו | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290011489625 | ביסקוויט בטעם שוקו — הדר | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119041152 | עוגיות ריפ'את — VOILA | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119041107 | עוגיות מרוקאיות עגול — VOILA | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119041053 | עוגיות סגנון מרוקאי — VOILA | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 2986058 | פתי בר וניל — גטניו | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290018893845 | פתי בר בטעם חמאה — צ'וקטה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 313184 | עוגיות גן חיות טעם וניל | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7296073453840 | קוקיס שבבי שוקולד חלבי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7296073453857 | קוקיס שוקולד לבן חלבי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290118423904 | קרמוגית קראנץ שוקו וניל עוגיות 200 גרם קרמוגית | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290106571945 | עוגיות קקאו דגנים מלאים עם נטיפי שוקולד מריר פיטנס 180 גרם פ | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290118422617 | קרמוגית קראנץ קרם וניל עוגיות 200 גרם קרמוגית | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290019293804 | קראנץ אגוזי לוז | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8410376037784 | עוגיות סנדוויץ' שוקולד גולון | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290013740694 | עוגיות אלפחורס — קופסת העוגיות של רחלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290018371930 | פתי בר קמח כוסמין אורגני — השדה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290018371923 | פתי בר קמח מלא אורגני — השדה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290118426615 | עוגיות מיני שוקולד | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290106571921 | עוגיות פיטנס חמוציות 180 גרם פיטנס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8410376075915 | עוגיות+שבבי שוקולד לל"ג | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290019816034 | מאגדת מיני קראנץ עוגיות | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290018371947 | פתי בר כוסמין — השדה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 80083665 | עוגיות אורגניות+שוקולד — גנדולה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119043798 | עוגיות אוזניות — לה פזואלוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290019870470 | עוגיות סנדוויץ עם קרם בטעם שוקו צ'וקטה 176 גרם צ'וקטה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4823077614699 | ביסקוויט לקפה בטעם חמאה — ROSHEN | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4823077633317 | עוגיות LOVITA שוקולד | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4820180816590 | עוגיות עם גרעיני חמנייה — PASTICERE | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4820180816576 | עוגיות עם שבבי קוקוס — PASTICERE | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 311708 | עוגיות מחיטה מלאה מן — מן | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8008698037171 | עוגיות חמאה ללא גלוטן — שר | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290017724171 | מארז עוגיות אקלר סנדוויץ ריבה ללא סוכר הללס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 313160 | עוגיות שוקולד זהבה — אסם | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4006529002170 | עוגיות גולד רינג 400 גרם ללא מיתוג | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119041350 | עוגיות קוואקר ללת"ס — VOILA | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119043095 | עוגיות שיבולת שועל — לה פזואלוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119041206 | עוגיות קוואקר — VOILA | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 74184 | פתי בר קלאסי — אסם | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290123330488 | עוגיות בוטנים כשל"פ — לה פזואלוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7296073162001 | עוגיות במילוי קרם אגוזים | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119040803 | עוגיות קינמון מסוכרות — לה פזואלוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119040858 | עוגיות מקלות עלים | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290018893036 | עוגיות סנדוויץ' שוקולד | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290105364784 | פרה קראנץ' שוקולד לבן פרה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 5410126116168 | ביסקוויט בטעם קרמל — לוטוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 5410126006049 | ביסקוויט לוטוס טעם קרמל — לוטוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 5410126806250 | עוגיות לוטוס — לוטוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 5410126726244 | ביסקוויט קרמל — לוטוס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8710502405204 | מרבה עוגיות ממולאות קרם שוקולד מרבה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8710502139017 | מרבה עוגיות טריפל שוקולד ציפס מרבה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 311128 | עוגיות בטעם חמאה — מן | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8710502279010 | עוג. שוקולד צ'יפס מצופות | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4823077614675 | ביסקוויט לקפה בטעם חלב — ROSHEN | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 99804 | עוגיות שוקולד לבן חלבי — שופרסל | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290112961754 | עוגיות שוקוציפס קרם אגוז | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 46214731552 | עוגיות שוקולד צ'יפס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7296073529019 | קוקיס שוקולד מריר חלבי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7296073529026 | קוקיס שוקו+שבבי שוקולד | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4017100364112 | עוגיות היט בטעם שוקולד 220 גרם בלזן | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4820180816552 | עוגיות עם ש.שועל קוקוס — PASTICERE | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7622300489427 | עוגיות אוראו בציפוי שוקולד לבן 246 גרם אוראו | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8000500366073 | ביסקוויט נוטלה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7622210137234 | עוגיות אוראו דאבל קרם וניל אוראו | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 5901414200411 | עוגיות היט מיניס עם שוקולד 130 גרם בלזן | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7296073161981 | עוגיות במילוי קרם שוקולד | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 61245 | עוגיות שוקוציפס+שוקולד — אסם | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 4017100198151 | עוגיות היט בטעם וניל 220 גרם בלזן | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8710502470028 | עוגיות שוקוצ'יפס נוגטלי | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290106656727 | עוגיות חיוכים שוקולד | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 46214930207 | עוגיות שוקולד צ'יפס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7622300489434 | עוגיות אוראו בציפוי שוקולד חלב 246 גרם אוראו | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290019870463 | עוגיות סנדוויץ עם קרם בטעם וניל צ'וקטה 176 גרם צ'וקטה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7296073659969 | עוגיות חיות שוקו | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7622201401900 | עוגיות מילקה סנסיישן אוראו 156 גרם מילקה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290112340276 | עוגיות קרם קפה נמס 200 גרם עלית | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7622300356767 | עוגיות שוקולד צ'יפס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7622201809188 | ביסקוויט מילקה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290115206333 | עוגיות מיני שוקוצ'יפס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290000075143 | עוגיות שוקוצ'יפס קלאסי 200 גרם אסם | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119043897 | עוגיות רולדה תמרים | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290019816232 | קראנץ סנדויץ שוקולד | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7622210453327 | עוגיות מילקה סנסיישן 156 גרם מילקה | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119040650 | עוגיות נסיכה מיקס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119040605 | עוגיות נסיכה בטעם תות | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 8710502064814 | עוגיות שוקוצ'יפס מרקם רך | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290019816058 | קראנץ מיני אלפחורס | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290101111986 | עינוגים קוקיס עוגיות | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290109354996 | פתי בר ללא גלוטן שוקו — אסם | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290119040179 | עוגיות פרח עם ריבת תות — VOILA | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
cookies_coffee | 7290109354972 | פתי בר ללא גלוטן קלאסי — אסם | UNTRACEABLE | bsip1_dir_missing | cookies_coffee_frontend_v2.json
granola | 7290017962047 | גרנולה חמוציות ושקדים | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290116534619 | גרנולה פרוטאין+שוקולד | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290017962023 | גרנולה מייפל תמר פקאן | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290106771369 | גרנולה לוז וקינמון | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290106773714 | גרנולה מיקס קראנץ' מלוח | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290112498007 | גרנולה חלבון שקד+חמוציות | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290013433244 | גרנולה 18% חלבון | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290013433336 | גרנולה 48% סופרפוד | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290106771314 | גרנולה אגוזים חמוציות | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290112497994 | גרנולה פרוטאין+אגוזים | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290106771161 | גרנולה מייפל פקאן | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290013433091 | גרנולה 8% שוקולד מריר | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290013433107 | גרנולה חלבה תמר קשיו | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290011131050 | גרנולה פקאן | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7613035635845 | גרנולה שוקולד פיטנס | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7613037012095 | גרנולה שוקולד קינואה | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7613035622623 | גרנולה דבש פיטנס | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290011131968 | גרנולה אגוזים | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290014471443 | גרנולה אגוזים | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290011668587 | גרנולה עשירה | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 7290011131975 | גרנולה פירות | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
granola | 1343845 | גרנולה עם פירות | UNTRACEABLE | NO_CONFIG_BOUND | granola_frontend_v2.json
protein_bars | 7290017516295 | חטיף חלבון אגוזי לוז | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290121161886 | חטיף חלבון בננה שוקולד | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290121166850 | חטיף חלבון וניל קראנץ' | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 8410076610379 | נייטשר פרוטאין שוקולד | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 8410076610386 | נייטשר פרוטאין קרמל מלוח | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290019766025 | אול אין סופט פיסטוק | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290119371129 | חטיף חלבון שוקולד עוגיות | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290119371112 | חטיף חלבון קרמל ואגוזים | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290019401018 | חטיף פרוטאין קרם עוגיות | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290019401049 | חטיף פרוטאין שוקולד קרמל | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290015130035 | WIN חטיף חלבון קרם קרמל | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290015130042 | WIN חטיף חלבון קרם קרמל | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290018703991 | עוגיית חלבון דאבל שוקולד | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290018703984 | עוגיית חלבון שוקולד צ'יפ | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290015130028 | WIN חטיף חלבון קרם חלב | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290117384572 | חטיף חלבון קרם עוגיות | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290117384589 | חטיף חלבון קרמל מלוח | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290117384596 | חטיף חלבון פאי קינמון | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290121160582 | חטיף חלבון חמאת בוטנים | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290121161916 | חטיף חלבון טריפל שוקולד | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290121161930 | חטיף חלבון טעם בננה טופי | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290019766018 | אול אין חלבון סופט עוגיות | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290018703304 | אול אין קרם עוגיות | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290018703076 | אול אין דאבל שוקולד | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290018043899 | אול אין בוטנים קרמל | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290018043134 | אול אין שוק.לבן עוגיות | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290019310235 | אול אין ונילה קראנץ | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290019766230 | חטיף חלבון אסטרה סופט | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290019401544 | חטיף פרוטאין עוגיות טופי | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290112915382 | חטיף חלבון שוקולד דובאי | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290112913487 | חטיף חלבון קרם אגוזים | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json
protein_bars | 7290112915351 | חטיף חלבון קרמל מלוח | UNTRACEABLE | NO_CONFIG_BOUND | protein_combined_frontend_v2.json