# OFF Sweep v1 — Open Food Facts Contamination Map

Generated: 2026-07-02T04:42:21.523252+00:00  
Method: DYNAMIC discovery from `bari-web/src/lib/seo/public-corpus-registry.ts` (the same file the live Next.js app imports its comparison JSON from) — cross-checked against `03_operations/page_generator/configs/*.json` `baseline_json` fields. NOT a hardcoded filename list (TASK-450 fix).  
Scope: 16 JSON-backed live categories + 1 TS-embedded live categories out of JSON-scan scope (['magnesium']).  
OFF contamination types checked: (A) JSON-level OFF string markers in file text; (B) BSIP1 panel_source=open_food_facts.  
Image URL contamination (images.openfoodfacts.org in imageUrl field) is an independent contamination class reported separately.  

## Section 1: Category to Data File Map (dynamically discovered)

Derived by parsing `bari-web/src/lib/seo/public-corpus-registry.ts` at scan time — the file the live app itself imports comparison JSON from.

| Category | Data File |
|---|---|
| bread | bread_frontend_v4.json |
| breakfast-cereals | cereals_frontend_v2.json |
| brined-cheeses | brined_cheeses_frontend_v2.json |
| cakes | cakes_hard_cookies_frontend_v1.json |
| cheese | cheese_frontend_v4.json |
| chocolate-bars | chocolate_bars_frontend_v1.json |
| chocolate-tablets | chocolate_tablets_frontend_v1.json |
| cookies-coffee | cookies_coffee_frontend_v2.json |
| crackers | crackers_frontend_v1.json |
| granola | granola_frontend_v2.json |
| hard-cheeses | hard_cheeses_frontend_v4.json |
| hummus | hummus_frontend_v5.json |
| juices | juices_frontend_v3.json |
| milk-comparison | milk_frontend_v1.json |
| protein-bars | protein_combined_frontend_v2.json |
| snacks | snacks_frontend_v5.json |

**TS-embedded live categories (no frontend JSON file — out of scope for this scanner by construction):**  
- magnesium: TS-embedded product array (magnesium-page-data.ts), not a frontend JSON file (underlying source: `C:\Bari\03_operations\supplement_engine\proto_v0\benchmark\magnesium_v3_latest.json`)

**Page-generator config baseline_json mismatches (informational, non-fatal):**  
- `bread.json` (category=bread) declares baseline_json `C:\Bari\bari-web\src\data\comparisons\bread_frontend_v3.json` which is not among the registry-live files — likely a config pending a rebuild sync, not a live-site risk.

## Section 2: Verdict Table

Contamination types:  
- Image-OFF: product imageUrl points to images.openfoodfacts.org  
- Corpus-OFF: BSIP1 panel_source = open_food_facts (nutrition data from OFF)  
- JSON-marker: 'open_food_facts' string appears in live file (may be metadata-only)  

| Category | Data File | Products (M) | Image-OFF (N/M) | Corpus-OFF B (N/M) | JSON-live A | NO_RECORD | NO_BARCODE | Verdict |
|---|---|---|---|---|---|---|---|---|
| bread | bread_frontend_v4.json | 23 | 0/23 | 0/23 | 0 | 0 | 0 | CLEAN |
| breakfast-cereals | cereals_frontend_v2.json | 20 | 0/20 | 0/20 | 0 | 0 | 0 | CLEAN |
| brined-cheeses | brined_cheeses_frontend_v2.json | 36 | 0/36 | 0/36 | 0 | 0 | 0 | CLEAN |
| cakes | cakes_hard_cookies_frontend_v1.json | 62 | 0/62 | 0/62 | 0 | 0 | 0 | CLEAN |
| cheese | cheese_frontend_v4.json | 47 | 0/47 | 0/47 | 0 | 0 | 0 | CLEAN |
| chocolate-bars | chocolate_bars_frontend_v1.json | 23 | 0/23 | 0/23 | 0 | 0 | 0 | CLEAN |
| chocolate-tablets | chocolate_tablets_frontend_v1.json | 35 | 0/35 | 0/35 | 0 | 0 | 0 | CLEAN |
| cookies-coffee | cookies_coffee_frontend_v2.json | 117 | 0/117 | 0/117 | 0 | 0 | 0 | CLEAN |
| crackers | crackers_frontend_v1.json | 19 | 0/19 | 0/19 | 0 | 0 | 0 | CLEAN |
| granola | granola_frontend_v2.json | 22 | 0/22 | 0/22 | 0 | 0 | 0 | CLEAN |
| hard-cheeses | hard_cheeses_frontend_v4.json | 31 | 0/31 | 0/31 | 0 | 31 | 0 | UNKNOWN |
| hummus | hummus_frontend_v5.json | 57 | 0/57 | 0/57 | 0 | 0 | 0 | CLEAN |
| juices | juices_frontend_v3.json | 17 | 0/17 | 0/17 | 0 | 17 | 0 | UNKNOWN |
| milk-comparison | milk_frontend_v1.json | 18 | 0/18 | 0/18 | 0 | 0 | 0 | CLEAN |
| protein-bars | protein_combined_frontend_v2.json | 32 | 0/32 | 0/32 | 0 | 8 | 0 | CLEAN |
| snacks | snacks_frontend_v5.json | 21 | 0/21 | 0/21 | 0 | 0 | 0 | CLEAN |

**TOTAL Image-OFF products across live site: 0**  
**TOTAL Corpus-OFF products across live site: 0**  
**TOTAL Products scanned: 580**  

## Section 3: Dirty Category Details

No dirty categories detected at corpus or live-JSON level.

## Section 4: NO_RECORD and NO_BARCODE Concentrations

Categories with high NO_RECORD rates cannot confirm clean BSIP1 provenance.

| Category | NO_RECORD | NO_BARCODE | Total | NO_RECORD% | Note |
|---|---|---|---|---|---|
| bread | 0 | 0 | 23 | 0.0% |  |
| breakfast-cereals | 0 | 0 | 20 | 0.0% |  |
| brined-cheeses | 0 | 0 | 36 | 0.0% |  |
| cakes | 0 | 0 | 62 | 0.0% |  |
| cheese | 0 | 0 | 47 | 0.0% |  |
| chocolate-bars | 0 | 0 | 23 | 0.0% |  |
| chocolate-tablets | 0 | 0 | 35 | 0.0% |  |
| cookies-coffee | 0 | 0 | 117 | 0.0% |  |
| crackers | 0 | 0 | 19 | 0.0% |  |
| granola | 0 | 0 | 22 | 0.0% |  |
| hard-cheeses | 31 | 0 | 31 | 100.0% | HIGH — cannot confirm BSIP1 provenance |
| hummus | 0 | 0 | 57 | 0.0% |  |
| juices | 17 | 0 | 17 | 100.0% | HIGH — cannot confirm BSIP1 provenance |
| milk-comparison | 0 | 0 | 18 | 0.0% |  |
| protein-bars | 8 | 0 | 32 | 25.0% |  |
| snacks | 0 | 0 | 21 | 0.0% |  |

## Section 5: Full Corpus Results Per Category

### bread — bread_frontend_v4.json (23 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290016245325 | bsip1_bread_7290016245325 | לחם טחינה פרוס | NOT_FOUND |  | ok |
| 3268429 | bsip1_bread_3268429 | לחם ירוק מקמח מלא | NOT_FOUND |  | ok |
| 3268252 | bsip1_bread_3268252 | לחם חיטה מלא לילדים | NOT_FOUND |  | ok |
| 481203 | bsip1_bread_481203 | לחם מחמצת קמח מלא | NOT_FOUND |  | ok |
| 481197 | bsip1_bread_481197 | לחם מחמצת גרעינים | NOT_FOUND |  | ok |
| 574370 | bsip1_bread_574370 | לחם שיפון קל | NOT_FOUND |  | ok |
| 3054183 | bsip1_bread_3054183 | לחם שיפון מלא מסטמכר | NOT_FOUND |  | ok |
| 2079033 | bsip1_bread_2079033 | לחם דגנים לייט | NOT_FOUND |  | ok |
| 2079927 | bsip1_bread_2079927 | לחם דגנים מלא | NOT_FOUND |  | ok |
| 497044 | bsip1_bread_497044 | לחם ברמן אקטיב | NOT_FOUND |  | ok |
| 2079996 | bsip1_bread_2079996 | לחם אחיד פרוס קל | NOT_FOUND |  | ok |
| 7290018500316 | bsip1_bread_7290018500316 | לחם כוסמין לבן | NOT_FOUND |  | ok |
| 7290018540329 | bsip1_bread_7290018540329 | פיתה פיתה | NOT_FOUND |  | ok |
| 2079477 | bsip1_bread_2079477 | לחם אחיד פרוס | NOT_FOUND |  | ok |
| 9398281 | bsip1_bread_9398281 | מארז פיתות אסליות | NOT_FOUND |  | ok |
| 2079217 | bsip1_bread_2079217 | לחם מחמצת שיפון+אגוזים | NOT_FOUND |  | ok |
| 7290014321168 | bsip1_bread_7290014321168 | לחם לס פרוס קיטו | NOT_FOUND |  | ok |
| 6451484 | bsip1_bread_6451484 | לחם מחמצת אגוזים צימוקים | NOT_FOUND |  | ok |
| 6451507 | bsip1_bread_6451507 | לחם מחמצת מכוסמין | NOT_FOUND |  | ok |
| 7290018500460 | bsip1_bread_7290018500460 | לחם אנג'ל חצי מלא | NOT_FOUND |  | ok |
| 4685027 | bsip1_bread_4685027 | לחם מחמצת וחיטה מלאה קל | NOT_FOUND |  | ok |
| 7290016967074 | bsip1_bread_7290016967074 | לחם חיטה מלאה | NOT_FOUND |  | ok |
| 1902325 | bsip1_bread_1902325 | חלה קלועה | NOT_FOUND |  | ok |

### breakfast-cereals — cereals_frontend_v2.json (20 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 5010029000061 | bsip1_cereal_501002900006 | דגני בוקר | NOT_FOUND |  | ok |
| 7297488098688 | bsip1_cereal_729748809868 | פצפוצי אורז ללת"ס | NOT_FOUND |  | ok |
| 7297488199590 | bsip1_cereal_729748819959 | פצפוצי אורז תפוח | NOT_FOUND |  | ok |
| 7296073642046 | bsip1_cereal_729607364204 | קורנפלקס ללא גלוטן | NOT_FOUND |  | ok |
| 5900020036407 | bsip1_cereal_590002003640 | ליון דגני שוקולד וקרמל | NOT_FOUND |  | ok |
| 5900020012814 | bsip1_cereal_590002001281 | דגני בוקר נסקוויק | NOT_FOUND |  | ok |
| 7290107647731 | bsip1_cereal_729010764773 | דגני בוקר קוקומן חום לבן | NOT_FOUND |  | ok |
| 72968 | bsip1_cereal_72968 | דגני בוקר סיני מיניס | NOT_FOUND |  | ok |
| 7290017894911 | bsip1_cereal_729001789491 | טבעות דגנים שיבולת שועל | NOT_FOUND |  | ok |
| 7290107647854 | bsip1_cereal_729010764785 | דגני בוקר שוגי | NOT_FOUND |  | ok |
| 7290017894928 | bsip1_cereal_729001789492 | צדפי דגנים טעם שוקולד | NOT_FOUND |  | ok |
| 7296073705550 | bsip1_cereal_729607370555 | כדורי דגנים טעם שוקו | NOT_FOUND |  | ok |
| 7296073705567 | bsip1_cereal_729607370556 | טבעות דגנים בטעם דבש | NOT_FOUND |  | ok |
| 7290017894904 | bsip1_cereal_729001789490 | כדורי דגנים טעם שוקולד | NOT_FOUND |  | ok |
| 7290112495433 | bsip1_cereal_729011249543 | דגני בוקר דליפקאן | NOT_FOUND |  | ok |
| 8445291638839 | bsip1_cereal_844529163883 | צ'יריוס טעם דבש ושקדים | NOT_FOUND |  | ok |
| 7296073642022 | bsip1_cereal_729607364202 | דגני בוקר טבעות דבש לל"ג | NOT_FOUND |  | ok |
| 7296073705574 | bsip1_cereal_729607370557 | ריבועי דגנים עם קינמון | NOT_FOUND |  | ok |
| 3387390525960 | bsip1_cereal_338739052596 | דגני בוקר קראנץ' | NOT_FOUND |  | ok |
| 7613030979647 | bsip1_cereal_761303097964 | טריקס דגנים בטעם פירות | NOT_FOUND |  | ok |

### brined-cheeses — brined_cheeses_frontend_v2.json (36 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290019635826 | bc-001 | קוביות פטה עיזים מעודנת 5% | NOT_FOUND |  | ok |
| 554457 | bc-004 | גבינה צפתית 5% שומן | NOT_FOUND |  | ok |
| 554532 | bc-005 | גבינה צפתית מעודנת 5% | NOT_FOUND |  | ok |
| 7296073641940 | bc-003 | בולגרית מסורתית 5% | NOT_FOUND |  | ok |
| 7290102397334 | bc-002 | גבינה בולגרית 5% | NOT_FOUND |  | ok |
| 7290011499303 | bc-008 | פטה מעודנת עיזים 5% | NOT_FOUND |  | ok |
| 2133162 | bc-007 | גבינה בולגרית 5% שומן | NOT_FOUND |  | ok |
| 2133889 | bc-009 | בולגרית מעודנת 5% שומן | NOT_FOUND |  | ok |
| 7296073641964 | bc-010 | בולגרית מעודנת 5% | NOT_FOUND |  | ok |
| 7290108509106 | bc-013 | קוביות בולגרית מעודנת 13% | NOT_FOUND |  | ok |
| 7290011499129 | bc-006 | קוביות בולגרית מעודנת 5% | NOT_FOUND |  | ok |
| 7290011499327 | bc-012 | גבינה בולגרית מעודנת 5% | NOT_FOUND |  | ok |
| 7290011499105 | bc-011 | גבינה בולגרית מסורתית 5% | NOT_FOUND |  | ok |
| 7290011499358 | bc-029 | פטה עיזים 20% שומן | NOT_FOUND |  | ok |
| 7290019790402 | bc-014 | בולגרית של פעם 16% | NOT_FOUND |  | ok |
| 4861360 | bc-031 | גבינה צפתית בטעמים | NOT_FOUND |  | ok |
| 7290017065663 | bc-015 | פטה עיזים מעודנת 16% | NOT_FOUND |  | ok |
| 2107798 | bc-016 | בולגרית מעודנת 5% | NOT_FOUND |  | ok |
| 7296073641957 | bc-025 | בולגרית מסורתית 16% | NOT_FOUND |  | ok |
| 7296073641902 | bc-027 | פטה כבשים 20% | NOT_FOUND |  | ok |
| 7290011499051 | bc-028 | גבינה פטה כבשים 20% | NOT_FOUND |  | ok |
| 7290019790808 | bc-018 | פטה עיזים 16% שומן | NOT_FOUND |  | ok |
| 7290019790112 | bc-024 | פטה כבשים 20% שומן | NOT_FOUND |  | ok |
| 7290114314015 | bc-017 | בולגרית 24% | NOT_FOUND |  | ok |
| 7290011499112 | bc-030 | גבינה בולגרית 16% שומן | NOT_FOUND |  | ok |
| 7290019635222 | bc-032 | קוביות בולגרית מעודנת 16% | NOT_FOUND |  | ok |
| 7290017065236 | bc-035 | בולגרית מעודנת 24% | NOT_FOUND |  | ok |
| 48413 | bc-037 | גבינה מלוחה חמד 16% | NOT_FOUND |  | ok |
| 7290108509755 | bc-038 | גבינת חלומי 23% | NOT_FOUND |  | ok |
| 3075805 | bc-036 | גבינת טמרה מלוחה בקר 17% | NOT_FOUND |  | ok |
| 7290102393718 | bc-039 | חלומי בקר | NOT_FOUND |  | ok |
| 7296073641919 | bc-041 | חלומי בקר 24% | NOT_FOUND |  | ok |
| 7290011499365 | bc-044 | גבינת חלומי 24% | NOT_FOUND |  | ok |
| 7290114312707 | bc-043 | בולגרית מעודנת 16% | NOT_FOUND |  | ok |
| 369617 | bc-048 | כדורי פטה בשמן מתובל | NOT_FOUND |  | ok |
| 7290114312486 | bc-047 | בולגרית שום+עשבי תיבול 16% | NOT_FOUND |  | ok |

### cakes — cakes_hard_cookies_frontend_v1.json (62 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290119030095 | cake_7290119030095 | עוגת גבינה אפויה ללת"ס | NOT_FOUND |  | ok |
| 7296073346340 | cake_7296073346340 | עוגות אישיות קרם שוקולד | NOT_FOUND |  | ok |
| 5718021 | cake_5718021 | עוגת שטרודל גבינה | NOT_FOUND |  | ok |
| 7290119045013 | cake_7290119045013 | עוגת גבינה אפויה | NOT_FOUND |  | ok |
| 7290016162264 | cake_7290016162264 | עוגת גבינה רנסנס | NOT_FOUND |  | ok |
| 7290006983787 | cake_7290006983787 | עוגת הבית שוקולד צ'יפס 400 גרם | NOT_FOUND |  | ok |
| 5431913 | cake_5431913 | עוגת גבינה פירורים | NOT_FOUND |  | ok |
| 2472261 | cake_2472261 | עוגת מאפין תפוחי עץ | NOT_FOUND |  | ok |
| 7290119039746 | cake_7290119039746 | עוגת פס דובוש דולצ'ה | NOT_FOUND |  | ok |
| 9399288 | cake_9399288 | עוגת פס גבינה אפויה | NOT_FOUND |  | ok |
| 2472254 | cake_2472254 | עוגת מאפין אגוזים | NOT_FOUND |  | ok |
| 1361207 | cake_1361207 | עוגת פס אוכמניות | NOT_FOUND |  | ok |
| 2472186 | cake_2472186 | עוגת מאפין וניל | NOT_FOUND |  | ok |
| 5718038 | cake_5718038 | עוגת שטרודל תפוחי עץ | NOT_FOUND |  | ok |
| 4504649 | cake_4504649 | מיני שטרודל קרם פטיסייר | NOT_FOUND |  | ok |
| 7290018893661 | cake_7290018893661 | עוגות ספוג אישיות מצופות שוקולד מריר במילוי קרם קק | NOT_FOUND |  | ok |
| 4504687 | cake_4504687 | מיני שטרודל חלבה שוקולד | NOT_FOUND |  | ok |
| 7290111534010 | cake_7290111534010 | עוגת גבינה שמנת ופירורים | NOT_FOUND |  | ok |
| 7290119042302 | cake_7290119042302 | עוגת דבש | NOT_FOUND |  | ok |
| 7290006775023 | cake_7290006775023 | עוגה אנגלית 450 גרם | NOT_FOUND |  | ok |
| 7290016416961 | cake_7290016416961 | עוגת מוס גבינה+תות שדה | NOT_FOUND |  | ok |
| 2472193 | cake_2472193 | עוגת מאפין שוקולד | NOT_FOUND |  | ok |
| 7296073346333 | cake_7296073346333 | עוגות אישיות קרם חלב | NOT_FOUND |  | ok |
| 1361177 | cake_1361177 | עוגת פס דובדבנים | NOT_FOUND |  | ok |
| 7290106578821 | cake_7290106578821 | עוגת שמרים שוקולד | NOT_FOUND |  | ok |
| 7296073431893 | cake_7296073431893 | עוגת מאפין אגוזים עם ציפוי | NOT_FOUND |  | ok |
| 7296073132936 | cake_7296073132936 | עוגת מאפין שיש | NOT_FOUND |  | ok |
| 4170103 | cake_4170103 | עוגת קרנץ אגוזים וקינמון | NOT_FOUND |  | ok |
| 7290018893487 | cake_7290018893487 | עוגות אישיות קוקוס | NOT_FOUND |  | ok |
| 7296073140184 | cake_7296073140184 | עוגת מאפין תפוז | NOT_FOUND |  | ok |
| 9397642 | cake_9397642 | 5עוגות מאפין בטעם שוקולד | NOT_FOUND |  | ok |
| 7296073431909 | cake_7296073431909 | עוגת מאפין תפוח עץ | NOT_FOUND |  | ok |
| 2472223 | cake_2472223 | עוגת מאפין תפוז | NOT_FOUND |  | ok |
| 6983794 | cake_6983794 | תפוז | NOT_FOUND |  | ok |
| 7296073431879 | cake_7296073431879 | עוגת מאפין שוקו צ'יפס | NOT_FOUND |  | ok |
| 7290123330884 | cake_7290123330884 | עוגה בטעם שוקולד כשל"פ — קקאו | NOT_FOUND |  | ok |
| 7290105692498 | cake_7290105692498 | עוגת בראוניס כשל"פ | NOT_FOUND |  | ok |
| 7296073132950 | cake_7296073132950 | עוגת מאפין שוקולד צ'יפס | NOT_FOUND |  | ok |
| 4170097 | cake_4170097 | עוגת קרנץ' בטעם שוקולד | NOT_FOUND |  | ok |
| 6983787 | cake_6983787 | עוגת שוקולד צ'יפס | NOT_FOUND |  | ok |
| 7296073431817 | cake_7296073431817 | עוגת קרנץ' שוקולד | NOT_FOUND |  | ok |
| 7296073132943 | cake_7296073132943 | עוגת מאפין בטעם שוקולד | NOT_FOUND |  | ok |
| 7296073431916 | cake_7296073431916 | עוגת מאפין בטעם תפוז | NOT_FOUND |  | ok |
| 2472841 | cake_2472841 | עוגת סבתא בטעם שוקולד | NOT_FOUND |  | ok |
| 6983770 | cake_6983770 | שיש אסם | NOT_FOUND |  | ok |
| 7290123330280 | cake_7290123330280 | עוגת שמרים בטעם שוקולד | NOT_FOUND |  | ok |
| 7290123330334 | cake_7290123330334 | עוגת שמרים בריוש שוקולד | NOT_FOUND |  | ok |
| 7296073473664 | cake_7296073473664 | עוגת שוקולד ללא גלוטן | NOT_FOUND |  | ok |
| 7290123331034 | cake_7290123331034 | עוגה בטעם שוקולד כשל"פ — נטיפים | NOT_FOUND |  | ok |
| 7296073473688 | cake_7296073473688 | עוגת שוקוציפס ללא גלוטן | NOT_FOUND |  | ok |
| 7290006775337 | cake_7290006775337 | עוגת שמרים פרג 400 גרם | NOT_FOUND |  | ok |
| 7290013927996 | cake_7290013927996 | עוגת שמרים קרנאץ' בטעם שוקולד 400 גרם | NOT_FOUND |  | ok |
| 7290006775085 | cake_7290006775085 | עוגת שמרים במילוי קרם בטעם שוקולד 400 גרם | NOT_FOUND |  | ok |
| 7290013683595 | cake_7290013683595 | עוגת פס שביל החלב | NOT_FOUND |  | ok |
| 2472117 | cake_2472117 | עוגת פס קפוצ'ינו | NOT_FOUND |  | ok |
| 9397697 | cake_9397697 | חמישיית מאפין שוקו צ'יפס | NOT_FOUND |  | ok |
| 2472087 | cake_2472087 | עוגת פס שוקולד | NOT_FOUND |  | ok |
| 7290012244032 | cake_7290012244032 | עוגת מוס היער השחור | NOT_FOUND |  | ok |
| 2472148 | cake_2472148 | עוגת פס היער השחור | NOT_FOUND |  | ok |
| 7290015726528 | cake_7290015726528 | עוגת פס מוס טירמיסו | NOT_FOUND |  | ok |
| 7290012244056 | cake_7290012244056 | עוגת מוס גבינה פרורים | NOT_FOUND |  | ok |
| 7290015726535 | cake_7290015726535 | עוגת פס מוס בלגי פרווה | NOT_FOUND |  | ok |

### cheese — cheese_frontend_v4.json (47 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290014758681 | bsip1_cheese_729001475868 | קוטג 1% שומן | NOT_FOUND |  | ok |
| 6040619 | bsip1_cheese_6040619 | גבינה טבורוג 5% | NOT_FOUND |  | ok |
| 4127077 | bsip1_cheese_4127077 | קוטג' 3% שומן | NOT_FOUND |  | ok |
| 4127329 | bsip1_cheese_4127329 | קוטג' 5% שומן | NOT_FOUND |  | ok |
| 41445 | bsip1_cheese_41445 | קוטג' 5% | NOT_FOUND |  | ok |
| 7290110321277 | bsip1_cheese_729011032127 | קוטג' בקטנה 5% | NOT_FOUND |  | ok |
| 474502 | bsip1_cheese_474502 | גבינה לבנה 5% שומן | NOT_FOUND |  | ok |
| 7290010945481 | bsip1_cheese_729001094548 | גבינה לבנה 5% שומן | NOT_FOUND |  | ok |
| 7290102393268 | bsip1_cheese_729010239326 | גבינה לבנה 5% שומן | NOT_FOUND |  | ok |
| 7290114311472 | bsip1_cheese_729011431147 | גבינה לבנה 5% מהדרין | NOT_FOUND |  | ok |
| 7290116934280 | bsip1_cheese_729011693428 | גבינה לבנה 5%+שמיר ושום | NOT_FOUND |  | ok |
| 7290114310918 | bsip1_cheese_729011431091 | קוטג' 5% | NOT_FOUND |  | ok |
| 2868996 | bsip1_cheese_2868996 | קוטג' 5% שומן | NOT_FOUND |  | ok |
| 4127336 | bsip1_cheese_4127336 | קוטג' 9% שומן | NOT_FOUND |  | ok |
| 41452 | bsip1_cheese_41452 | קוטג' מהדרין 9% שומן | NOT_FOUND |  | ok |
| 2824183 | bsip1_cheese_2824183 | גבינה לבנה 5% שומן | NOT_FOUND |  | ok |
| 2824640 | bsip1_cheese_2824640 | גבינה לבנה 5% | NOT_FOUND |  | ok |
| 56272 | bsip1_cheese_56272 | גבינה לבנה עם זיתים 5% | NOT_FOUND |  | ok |
| 3523230065467 | bsip1_cheese_352323006546 | גבינת עזים שום+עשב תיבול | NOT_FOUND |  | ok |
| 7290116931241 | bsip1_cheese_729011693124 | קוטג' 12% שומן | NOT_FOUND |  | ok |
| 7290011194246 | bsip1_cheese_729001119424 | קוטג' 5% שומן | NOT_FOUND |  | ok |
| 3075850 | bsip1_cheese_3075850 | לבנה עם זעתר | NOT_FOUND |  | ok |
| 7622201798154 | bsip1_cheese_762220179815 | גבינת לייט 13% | NOT_FOUND |  | ok |
| 7290116934365 | bsip1_cheese_729011693436 | 16% שום שמיר | NOT_FOUND |  | ok |
| 7290019635369 | bsip1_cheese_729001963536 | גבינת שמנת 16% שומן | NOT_FOUND |  | ok |
| 7290119375219 | bsip1_cheese_729011937521 | גבינה 5% עם תבלין בייגלס | NOT_FOUND |  | ok |
| 6492852 | bsip1_cheese_6492852 | גבינה לבנה עיזים 5% גד | NOT_FOUND |  | ok |
| 7290108504378 | bsip1_cheese_729010850437 | גבינת שמנת עם זיתים 20% | NOT_FOUND |  | ok |
| 7290019635376 | bsip1_cheese_729001963537 | גבינת שמנת גורגונזולה24% | NOT_FOUND |  | ok |
| 7290014759084 | bsip1_cheese_729001475908 | גבינת שמנת בטעם טבעי16% | NOT_FOUND |  | ok |
| 7290019635116 | bsip1_cheese_729001963511 | גבינת שמנת זיתים 5% | NOT_FOUND |  | ok |
| 7290108502541 | bsip1_cheese_729010850254 | גבינת שמנת טבעי 18% | NOT_FOUND |  | ok |
| 7622201521493 | bsip1_cheese_762220152149 | שום+ע.תיבול 12% | NOT_FOUND |  | ok |
| 7622201139278 | bsip1_cheese_762220113927 | גבינת שמנת 25% | NOT_FOUND |  | ok |
| 7290116935409 | bsip1_cheese_729011693540 | גבינת שמנת מוקצפת 25% | NOT_FOUND |  | ok |
| 7290014762831 | bsip1_cheese_729001476283 | גבינת שמנת+פלפל חלפיניו | NOT_FOUND |  | ok |
| 7290112342102 | bsip1_cheese_729011234210 | גבינה 5% בצל מקורמל | NOT_FOUND |  | ok |
| 7290116936604 | bsip1_cheese_729011693660 | גבינת שמנת עשבי תיבול25% | NOT_FOUND |  | ok |
| 4129118 | bsip1_cheese_4129118 | גבינת שמנת 24% עם זיתים | NOT_FOUND |  | ok |
| 4129101 | bsip1_cheese_4129101 | גבינת בטעם טבעי | NOT_FOUND |  | ok |
| 4129156 | bsip1_cheese_4129156 | גבינת שום שמיר | NOT_FOUND |  | ok |
| 7290116933078 | bsip1_cheese_729011693307 | גבינת שמנת+פלפל פיקנטי | NOT_FOUND |  | ok |
| 7290116931982 | bsip1_cheese_729011693198 | גבינת שמנת עם עירית 25% | NOT_FOUND |  | ok |
| 7290116932644 | bsip1_cheese_729011693264 | גבינת שמנת 25% עם זעתר | NOT_FOUND |  | ok |
| 7290019635581 | bsip1_cheese_729001963558 | גבינת שמנת סלסה 24% | NOT_FOUND |  | ok |
| 7290011499624 | bsip1_cheese_729001149962 | גבינת שמנת טעם טבעי 30% | NOT_FOUND |  | ok |
| 7290019635383 | bsip1_cheese_729001963538 | גבינת שמנת ריבת בצל 24% | NOT_FOUND |  | ok |

### chocolate-bars — chocolate_bars_frontend_v1.json (23 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 5000159560511 | cb-001 | חטיף בודד | NOT_FOUND |  | ok |
| 72991008 | cb-002 | שוקולד קלאסי | NOT_FOUND |  | ok |
| 7290106651265 | cb-003 | קלאסי מגדים | NOT_FOUND |  | ok |
| 7290116536781 | cb-004 | אין קרם חלבי | NOT_FOUND |  | ok |
| 7290116536774 | cb-005 | אין קרם נוגט | NOT_FOUND |  | ok |
| 5900951310379 | cb-006 | קרימי חטיף בודד | NOT_FOUND |  | ok |
| 7290110571405 | cb-007 | מיני פסק זמן | NOT_FOUND |  | ok |
| 5000159559485 | cb-008 | חטיף בודד | NOT_FOUND |  | ok |
| 3800020401552 | cb-009 | קיט קט צ'אנקי פאנקי | NOT_FOUND |  | ok |
| 7290105362377 | cb-010 | כיף כף מגדים | NOT_FOUND |  | ok |
| 7290100249086 | cb-011 | חטיף נוגט לבן כשל"פ | NOT_FOUND |  | ok |
| 7290116532011 | cb-012 | חטיף נוגט | NOT_FOUND |  | ok |
| 7290116531748 | cb-013 | שוקו מיקס כשל"פ | NOT_FOUND |  | ok |
| 7290116532042 | cb-014 | כריות נוגט כשל"פ | NOT_FOUND |  | ok |
| 7290116537375 | cb-015 | כריות | NOT_FOUND |  | ok |
| 7290112494283 | cb-016 | חום לבן | NOT_FOUND |  | ok |
| 72917329 | cb-017 | חטיף שוקולד אגוזי | NOT_FOUND |  | ok |
| 72917367 | cb-018 | חטיף שוקולד טעמי | NOT_FOUND |  | ok |
| 4823077617041 | cb-019 | חטיף שוקולד ממולא קרמל | NOT_FOUND |  | ok |
| 5000159561976 | cb-020 | חטיף בודד | NOT_FOUND |  | ok |
| 7290116534442 | cb-021 | חטיף שוקולד קרם חלבי | NOT_FOUND |  | ok |
| 72918388 | cb-022 | חטיף שוקולד טוויסט | NOT_FOUND |  | ok |
| 34000250103 | cb-023 | חטיף שוקולד ממולא בוטנים | NOT_FOUND |  | ok |

### chocolate-tablets — chocolate_tablets_frontend_v1.json (35 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7296073382416 | ct-001 | שוקולד מריר 90% | NOT_FOUND |  | ok |
| 7290112197467 | ct-002 | שוקולד מריר | NOT_FOUND |  | ok |
| 3046920029759 | ct-003 | שוקולד מריר 90% | NOT_FOUND |  | ok |
| 7296073726562 | ct-038 | שוקולד מריר ללת"ס 72% | NOT_FOUND |  | ok |
| 7290119500482 | ct-034 | שוקולד מריר 62% | NOT_FOUND |  | ok |
| 4000539280740 | ct-007 | שוקולד מריר 78% | NOT_FOUND |  | ok |
| 7290119500437 | ct-008 | שוקולד מריר | NOT_FOUND |  | ok |
| 5941021001674 | ct-014 | שוקולד מריר 85% | NOT_FOUND |  | ok |
| 7290018893609 | ct-009 | שוקולד מריר 85% | NOT_FOUND |  | ok |
| 7290112197443 | ct-010 | שוקולד חלב | NOT_FOUND |  | ok |
| 7290119500383 | ct-011 | שוקולד חלב | NOT_FOUND |  | ok |
| 3046920028363 | ct-012 | שוקולד מריר 85% | NOT_FOUND |  | ok |
| 7290105961525 | ct-013 | שוקולד מריר 85% | NOT_FOUND |  | ok |
| 7296073747819 | ct-015 | שוקולד מריר פרימיום 81% | NOT_FOUND |  | ok |
| 7290107955782 | ct-016 | טבלת שוקולד מריר ללת"ס | NOT_FOUND |  | ok |
| 4000539280726 | ct-017 | שוקולד מריר 70% מילד | NOT_FOUND |  | ok |
| 7610400075770 | ct-018 | שוקולד מריר אגוזי לוז | NOT_FOUND |  | ok |
| 7296073747802 | ct-039 | שוקולד מריר פרימיום 75% | NOT_FOUND |  | ok |
| 4000417025005 | ct-019 | שוקולד מריר עם מרציפן | NOT_FOUND |  | ok |
| 3046920023047 | ct-020 | אקסלנס פיסטוק | NOT_FOUND |  | ok |
| 3046920028004 | ct-035 | שוקולד מריר 70% | NOT_FOUND |  | ok |
| 7290018893401 | ct-036 | שוקולד מריר 70% | NOT_FOUND |  | ok |
| 7290019870043 | ct-021 | שוקולד מריר 60% | NOT_FOUND |  | ok |
| 7290019939412 | ct-022 | שוקולד חלב ללא סוכר | NOT_FOUND |  | ok |
| 7610008641001 | ct-026 | טבלת חלב | NOT_FOUND |  | ok |
| 3046920028752 | ct-023 | שוקולד מריר מנטה | NOT_FOUND |  | ok |
| 3046920029674 | ct-024 | שוקולד מריר מלח | NOT_FOUND |  | ok |
| 7290112331984 | ct-025 | קראנצ' בסקויט | NOT_FOUND |  | ok |
| 7614500010617 | ct-027 | מריר | NOT_FOUND |  | ok |
| 7290110579463 | ct-028 | חלב שברי אגוז | NOT_FOUND |  | ok |
| 7622202257506 | ct-029 | אקסטרה קקאו | NOT_FOUND |  | ok |
| 7614500010013 | ct-030 | חלב 100 גרם | NOT_FOUND |  | ok |
| 7290112914699 | ct-032 | שוקולד חלב וקרמל מלוח | NOT_FOUND |  | ok |
| 7622202265648 | ct-031 | שוקולד לבן | NOT_FOUND |  | ok |
| 7290112348548 | ct-033 | לבן | NOT_FOUND |  | ok |

### cookies-coffee — cookies_coffee_frontend_v2.json (117 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290013453693 | ck-7290013453693 | עוגיות גרידת לימון ללת"ס | NOT_FOUND |  | ok |
| 80083764 | bsip1_cookies_80083764 | עוגיות דגנים עם ש.שועל | NOT_FOUND |  | ok |
| 7290017962139 | ck-7290017962139 | עוגיות פירות יער כשל"פ | NOT_FOUND |  | ok |
| 7290020030184 | ck-7290020030184 | עוגיות מזרחיות עם זעתר 400 גרם | NOT_FOUND |  | ok |
| 7290122781359 | ck-7290122781359 | מיני עוגיות קלאסי 80 גרם | NOT_FOUND |  | ok |
| 7290013740113 | ck-7290013740113 | עוגיות מרוקאיות | NOT_FOUND |  | ok |
| 7290013453068 | ck-7290013453068 | עוגיות כוסמין פירות יער | NOT_FOUND |  | ok |
| 540160 | ck-540160 | עוגיות ללת"ס מקמח מלא | NOT_FOUND |  | ok |
| 7290013740137 | ck-7290013740137 | עוגיות אוזן פיל | NOT_FOUND |  | ok |
| 7290119043743 | ck-7290119043743 | עוגיות מרוקאיות | NOT_FOUND |  | ok |
| 7290013740557 | ck-7290013740557 | עוגיות רייפעת | NOT_FOUND |  | ok |
| 7290119043149 | ck-7290119043149 | עוגיות בטעם חמאה | NOT_FOUND |  | ok |
| 7290013740229 | ck-7290013740229 | עוגיות פרסות שקדים | NOT_FOUND |  | ok |
| 960860015432 | ck-960860015432 | עוגיות ללת"ס מקמח מלא | NOT_FOUND |  | ok |
| 7290013740472 | ck-7290013740472 | עוגיות מושלגות | NOT_FOUND |  | ok |
| 311463 | ck-311463 | עוגיות חמאה ללת"ס | NOT_FOUND |  | ok |
| 7290013453501 | ck-7290013453501 | ביסקוטי כוסמין שוקולד | NOT_FOUND |  | ok |
| 7290013740052 | ck-7290013740052 | עוגיות פרחי ריבה | NOT_FOUND |  | ok |
| 7290013740540 | ck-7290013740540 | עוגיות אוזן פיל ללת"ס | NOT_FOUND |  | ok |
| 7290013740465 | ck-7290013740465 | עוגיות שושנים | NOT_FOUND |  | ok |
| 7290013740342 | ck-7290013740342 | עוגיות פרחי ריבה ללת"ס | NOT_FOUND |  | ok |
| 7290013156921 | ck-7290013156921 | עוגיות אצבעות מתוקות ללא סוכר גאקובס 350 גרם | NOT_FOUND |  | ok |
| 7290017898506 | ck-7290017898506 | ביסקוטי | NOT_FOUND |  | ok |
| 5317194 | ck-5317194 | ביסקוויט בטעם וניל | NOT_FOUND |  | ok |
| 7290011489625 | ck-7290011489625 | ביסקוויט בטעם שוקו | NOT_FOUND |  | ok |
| 7290119041053 | ck-7290119041053 | עוגיות סגנון מרוקאי | NOT_FOUND |  | ok |
| 7290119041107 | ck-7290119041107 | עוגיות מרוקאיות עגול | NOT_FOUND |  | ok |
| 7290119041152 | ck-7290119041152 | עוגיות ריפ'את | NOT_FOUND |  | ok |
| 7290000061245 | ck-7290000061245 | עוגיות שוקוצ'יפס ממולאות 220 גרם | NOT_FOUND |  | ok |
| 7290013740014 | ck-7290013740014 | עוגיות שוקוצ'יפס | NOT_FOUND |  | ok |
| 7290018893845 | ck-7290018893845 | פתי בר בטעם חמאה | NOT_FOUND |  | ok |
| 7290013156006 | ck-7290013156006 | עוגיות מיני מרוקאיות 350 גרם | NOT_FOUND |  | ok |
| 7290017894317 | ck-7290017894317 | עוגיות כוסמין מלא שוקולד | NOT_FOUND |  | ok |
| 2986065 | ck-2986065 | פתי בר בטעם שוקולד | NOT_FOUND |  | ok |
| 2986058 | ck-2986058 | פתי בר וניל | NOT_FOUND |  | ok |
| 313184 | ck-313184 | עוגיות גן חיות טעם וניל | NOT_FOUND |  | ok |
| 7290118423904 | ck-7290118423904 | קראנץ שוקו וניל עוגיות 200 גרם | NOT_FOUND |  | ok |
| 7290118422617 | ck-7290118422617 | קראנץ קרם וניל עוגיות 200 גרם | NOT_FOUND |  | ok |
| 7290019293804 | ck-7290019293804 | קראנץ אגוזי לוז | NOT_FOUND |  | ok |
| 7296073453840 | ck-7296073453840 | קוקיס שבבי שוקולד חלבי | NOT_FOUND |  | ok |
| 7296073453857 | ck-7296073453857 | קוקיס שוקולד לבן חלבי | NOT_FOUND |  | ok |
| 7290106571945 | ck-7290106571945 | עוגיות קקאו דגנים מלאים עם נטיפי שוקולד מריר 180 ג | NOT_FOUND |  | ok |
| 8410376037784 | ck-8410376037784 | עוגיות סנדוויץ' שוקולד | NOT_FOUND |  | ok |
| 7290013740694 | ck-7290013740694 | עוגיות אלפחורס | NOT_FOUND |  | ok |
| 7290019816034 | ck-7290019816034 | מאגדת מיני קראנץ עוגיות | NOT_FOUND |  | ok |
| 7290018371923 | ck-7290018371923 | פתי בר קמח מלא אורגני | NOT_FOUND |  | ok |
| 7290018371930 | ck-7290018371930 | פתי בר קמח כוסמין אורגני | NOT_FOUND |  | ok |
| 7290118426615 | ck-7290118426615 | עוגיות מיני שוקולד | NOT_FOUND |  | ok |
| 7290106571921 | ck-7290106571921 | עוגיות חמוציות 180 גרם | NOT_FOUND |  | ok |
| 8410376075915 | ck-8410376075915 | עוגיות+שבבי שוקולד לל"ג | NOT_FOUND |  | ok |
| 7290018371947 | ck-7290018371947 | פתי בר כוסמין | NOT_FOUND |  | ok |
| 7290119043798 | ck-7290119043798 | עוגיות אוזניות | NOT_FOUND |  | ok |
| 80083665 | ck-80083665 | עוגיות אורגניות+שוקולד | NOT_FOUND |  | ok |
| 7290019870470 | ck-7290019870470 | עוגיות סנדוויץ עם קרם בטעם שוקו 176 גרם | NOT_FOUND |  | ok |
| 4823077614699 | ck-4823077614699 | ביסקוויט לקפה בטעם חמאה | NOT_FOUND |  | ok |
| 4823077633317 | ck-4823077633317 | עוגיות LOVITA שוקולד | NOT_FOUND |  | ok |
| 4820180816576 | ck-4820180816576 | עוגיות עם שבבי קוקוס | NOT_FOUND |  | ok |
| 4820180816590 | ck-4820180816590 | עוגיות עם גרעיני חמנייה | NOT_FOUND |  | ok |
| 7290123330488 | ck-7290123330488 | עוגיות בוטנים כשל"פ | NOT_FOUND |  | ok |
| 311708 | ck-311708 | עוגיות מחיטה מלאה | NOT_FOUND |  | ok |
| 8008698037171 | ck-8008698037171 | עוגיות חמאה ללא גלוטן | NOT_FOUND |  | ok |
| 313160 | ck-313160 | עוגיות שוקולד זהבה | NOT_FOUND |  | ok |
| 4006529002170 | ck-4006529002170 | עוגיות גולד רינג 400 גרם | NOT_FOUND |  | ok |
| 7290119041206 | ck-7290119041206 | עוגיות קוואקר | NOT_FOUND |  | ok |
| 7290119041350 | ck-7290119041350 | עוגיות קוואקר ללת"ס | NOT_FOUND |  | ok |
| 7290119043095 | ck-7290119043095 | עוגיות שיבולת שועל | NOT_FOUND |  | ok |
| 74184 | ck-74184 | פתי בר קלאסי | NOT_FOUND |  | ok |
| 7296073162001 | ck-7296073162001 | עוגיות במילוי קרם אגוזים | NOT_FOUND |  | ok |
| 7290119040803 | ck-7290119040803 | עוגיות קינמון מסוכרות | NOT_FOUND |  | ok |
| 7290119040858 | ck-7290119040858 | עוגיות מקלות עלים | NOT_FOUND |  | ok |
| 7290018893036 | ck-7290018893036 | עוגיות סנדוויץ' שוקולד | NOT_FOUND |  | ok |
| 5410126006049 | ck-5410126006049 | ביסקוויט טעם קרמל | NOT_FOUND |  | ok |
| 5410126116168 | ck-5410126116168 | ביסקוויט בטעם קרמל | NOT_FOUND |  | ok |
| 5410126726244 | ck-5410126726244 | ביסקוויט קרמל | NOT_FOUND |  | ok |
| 5410126806250 | ck-5410126806250 | עוגיות | NOT_FOUND |  | ok |
| 7290105364784 | ck-7290105364784 | קראנץ' שוקולד לבן | NOT_FOUND |  | ok |
| 8710502139017 | ck-8710502139017 | עוגיות טריפל שוקולד ציפס | NOT_FOUND |  | ok |
| 8710502405204 | ck-8710502405204 | עוגיות ממולאות קרם שוקולד | NOT_FOUND |  | ok |
| 311128 | ck-311128 | עוגיות בטעם חמאה | NOT_FOUND |  | ok |
| 8710502279010 | ck-8710502279010 | עוג. שוקולד צ'יפס מצופות | NOT_FOUND |  | ok |
| 4823077614675 | ck-4823077614675 | ביסקוויט לקפה בטעם חלב | NOT_FOUND |  | ok |
| 99804 | ck-99804 | עוגיות שוקולד לבן חלבי | NOT_FOUND |  | ok |
| 7290119043897 | ck-7290119043897 | עוגיות רולדה תמרים | NOT_FOUND |  | ok |
| 7290112961754 | ck-7290112961754 | עוגיות שוקוציפס קרם אגוז | NOT_FOUND |  | ok |
| 46214731552 | ck-46214731552 | עוגיות שוקולד צ'יפס | NOT_FOUND |  | ok |
| 7296073529019 | ck-7296073529019 | קוקיס שוקולד מריר חלבי | NOT_FOUND |  | ok |
| 7296073529026 | ck-7296073529026 | קוקיס שוקו+שבבי שוקולד | NOT_FOUND |  | ok |
| 4017100364112 | ck-4017100364112 | עוגיות היט בטעם שוקולד 220 גרם בלזן | NOT_FOUND |  | ok |
| 4820180816552 | ck-4820180816552 | עוגיות עם ש.שועל קוקוס | NOT_FOUND |  | ok |
| 7622300489427 | ck-7622300489427 | עוגיות בציפוי שוקולד לבן 246 גרם | NOT_FOUND |  | ok |
| 8000500366073 | ck-8000500366073 | ביסקוויט | NOT_FOUND |  | ok |
| 7622210137234 | ck-7622210137234 | עוגיות דאבל קרם וניל | NOT_FOUND |  | ok |
| 5901414200411 | ck-5901414200411 | עוגיות היט מיניס עם שוקולד 130 גרם | NOT_FOUND |  | ok |
| 61245 | ck-61245 | עוגיות שוקוציפס+שוקולד | NOT_FOUND |  | ok |
| 7296073161981 | ck-7296073161981 | עוגיות במילוי קרם שוקולד | NOT_FOUND |  | ok |
| 4017100198151 | ck-4017100198151 | עוגיות היט בטעם וניל 220 גרם בלזן | NOT_FOUND |  | ok |
| 8710502470028 | ck-8710502470028 | עוגיות שוקוצ'יפס נוגטלי | NOT_FOUND |  | ok |
| 7290106656727 | ck-7290106656727 | עוגיות חיוכים שוקולד | NOT_FOUND |  | ok |
| 46214930207 | ck-46214930207 | עוגיות שוקולד צ'יפס | NOT_FOUND |  | ok |
| 7622300489434 | ck-7622300489434 | עוגיות בציפוי שוקולד חלב 246 גרם | NOT_FOUND |  | ok |
| 7290019870463 | ck-7290019870463 | עוגיות סנדוויץ עם קרם בטעם וניל 176 גרם | NOT_FOUND |  | ok |
| 7290119040605 | ck-7290119040605 | עוגיות נסיכה בטעם תות | NOT_FOUND |  | ok |
| 7290119040650 | ck-7290119040650 | עוגיות נסיכה מיקס | NOT_FOUND |  | ok |
| 7622201401900 | ck-7622201401900 | עוגיות סנסיישן אוראו 156 גרם | NOT_FOUND |  | ok |
| 7290112340276 | ck-7290112340276 | עוגיות קרם קפה נמס 200 גרם עלית | NOT_FOUND |  | ok |
| 7622300356767 | ck-7622300356767 | עוגיות שוקולד צ'יפס | NOT_FOUND |  | ok |
| 7290019816232 | ck-7290019816232 | קראנץ סנדויץ שוקולד | NOT_FOUND |  | ok |
| 7290115206333 | ck-7290115206333 | עוגיות מיני שוקוצ'יפס | NOT_FOUND |  | ok |
| 7622201809188 | ck-7622201809188 | ביסקוויט | NOT_FOUND |  | ok |
| 7290000075143 | ck-7290000075143 | עוגיות שוקוצ'יפס קלאסי 200 גרם | NOT_FOUND |  | ok |
| 7290019816058 | ck-7290019816058 | קראנץ מיני אלפחורס | NOT_FOUND |  | ok |
| 7290119040179 | ck-7290119040179 | עוגיות פרח עם ריבת תות | NOT_FOUND |  | ok |
| 7290101111986 | ck-7290101111986 | עינוגים קוקיס עוגיות | NOT_FOUND |  | ok |
| 7622210453327 | ck-7622210453327 | עוגיות סנסיישן 156 גרם | NOT_FOUND |  | ok |
| 8710502064814 | ck-8710502064814 | עוגיות שוקוצ'יפס מרקם רך | NOT_FOUND |  | ok |
| 7290109354996 | ck-7290109354996 | פתי בר ללא גלוטן שוקו | NOT_FOUND |  | ok |
| 7290109354972 | ck-7290109354972 | פתי בר ללא גלוטן קלאסי | NOT_FOUND |  | ok |

### crackers — crackers_frontend_v1.json (19 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 96086000966 | bsip1_crackers_9608600096 | קרקר כוסמין מלא ושומשום | NOT_FOUND |  | ok |
| 96086000577 | bsip1_crackers_9608600057 | קרקר כוסמין אורגני | NOT_FOUND |  | ok |
| 7290013740823 | bsip1_crackers_7290013740 | קרקר כוסמין טבעי | NOT_FOUND |  | ok |
| 7290112963918 | bsip1_crackers_7290112963 | קרקר דק רוזמרין פיטנס | NOT_FOUND |  | ok |
| 7296073659952 | bsip1_crackers_7296073659 | קרקר דק כפרי | NOT_FOUND |  | ok |
| 7290013740809 | bsip1_crackers_7290013740 | קרקר כוסמין סלק | NOT_FOUND |  | ok |
| 7296073659945 | bsip1_crackers_7296073659 | קרקר דק רוזמרין | NOT_FOUND |  | ok |
| 7290112968821 | bsip1_crackers_7290112968 | קרקר דק פיטנס בטטה | NOT_FOUND |  | ok |
| 7296073134459 | bsip1_crackers_7296073134 | קרקר פריך בסגנון שוודי | NOT_FOUND |  | ok |
| 7290115205176 | bsip1_crackers_7290115205 | קרקר דק כפרי פיטנס | NOT_FOUND |  | ok |
| 7296073134442 | bsip1_crackers_7296073134 | קרקר פריך עם קמח שיפון | NOT_FOUND |  | ok |
| 8434165658523 | bsip1_crackers_8434165658 | קרקר קרם קרקר | NOT_FOUND |  | ok |
| 7296073398875 | bsip1_crackers_7296073398 | קרם קרקר | NOT_FOUND |  | ok |
| 7290013740083 | bsip1_crackers_7290013740 | קרקר דגנים ללת"ס | NOT_FOUND |  | ok |
| 74252 | bsip1_crackers_74252 | קרקר שומשום אסם | NOT_FOUND |  | ok |
| 7290011489595 | bsip1_crackers_7290011489 | קרקר טופז שומשום | NOT_FOUND |  | ok |
| 7290018790328 | bsip1_crackers_7290018790 | קרקר מרובע מלוח | NOT_FOUND |  | ok |
| 74375 | bsip1_crackers_74375 | קרקר זהב אסם | NOT_FOUND |  | ok |
| 5000396021202 | bsip1_crackers_5000396021 | קרקר | NOT_FOUND |  | ok |

### granola — granola_frontend_v2.json (22 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290017962047 | bsip1_cereal_729001796204 | גרנולה חמוציות ושקדים | NOT_FOUND |  | ok |
| 7290116534619 | bsip1_cereal_729011653461 | גרנולה פרוטאין+שוקולד | NOT_FOUND |  | ok |
| 7290017962023 | bsip1_cereal_729001796202 | גרנולה מייפל תמר פקאן | NOT_FOUND |  | ok |
| 7290106771369 | bsip1_cereal_729010677136 | גרנולה לוז וקינמון | NOT_FOUND |  | ok |
| 7290112498007 | bsip1_cereal_729011249800 | גרנולה חלבון שקד+חמוציות | NOT_FOUND |  | ok |
| 7290013433244 | bsip1_cereal_729001343324 | גרנולה 18% חלבון | NOT_FOUND |  | ok |
| 7290013433336 | bsip1_cereal_729001343333 | גרנולה 48% סופרפוד | NOT_FOUND |  | ok |
| 7290106771314 | bsip1_cereal_729010677131 | גרנולה אגוזים חמוציות | NOT_FOUND |  | ok |
| 7290112497994 | bsip1_cereal_729011249799 | גרנולה פרוטאין+אגוזים | NOT_FOUND |  | ok |
| 7290106773714 | bsip1_cereal_729010677371 | גרנולה מיקס קראנץ' מלוח | NOT_FOUND |  | ok |
| 7290106771161 | bsip1_cereal_729010677116 | גרנולה מייפל פקאן | NOT_FOUND |  | ok |
| 7290013433091 | bsip1_cereal_729001343309 | גרנולה 8% שוקולד מריר | NOT_FOUND |  | ok |
| 7290013433107 | bsip1_cereal_729001343310 | גרנולה חלבה תמר קשיו | NOT_FOUND |  | ok |
| 7290011131050 | bsip1_cereal_729001113105 | גרנולה פקאן | NOT_FOUND |  | ok |
| 7613035635845 | bsip1_cereal_761303563584 | גרנולה שוקולד | NOT_FOUND |  | ok |
| 7613037012095 | bsip1_cereal_761303701209 | גרנולה שוקולד קינואה | NOT_FOUND |  | ok |
| 7613035622623 | bsip1_cereal_761303562262 | גרנולה דבש | NOT_FOUND |  | ok |
| 7290011131968 | bsip1_cereal_729001113196 | גרנולה אגוזים | NOT_FOUND |  | ok |
| 7290011668587 | bsip1_cereal_729001166858 | גרנולה עשירה | NOT_FOUND |  | ok |
| 7290014471443 | bsip1_cereal_729001447144 | גרנולה אגוזים | NOT_FOUND |  | ok |
| 7290011131975 | bsip1_cereal_729001113197 | גרנולה פירות | NOT_FOUND |  | ok |
| 1343845 | bsip1_cereal_1343845 | גרנולה עם פירות | NOT_FOUND |  | ok |

### hard-cheeses — hard_cheeses_frontend_v4.json (31 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290110324872 | bsip1_hardcheese_72901103 | פרוסות גבינת גלבוע 5% 200 גרם | NO_RECORD |  | NO_RECORD |
| 7290004122348 | bsip1_hardcheese_72900041 | פרוסות גבינת עמק מופחתת שומן 9% בד"צ 200 גרם | NO_RECORD |  | NO_RECORD |
| 4137311 | HC-4137311 | גבינה צהובה 9% מופחתת | NO_RECORD |  | NO_RECORD |
| 52311 | HC-52311 | גבינה צהובה עמק15% פרוס | NO_RECORD |  | NO_RECORD |
| 7290014760448 | HC-7290014760448 | גבינה צהובה 22% | NO_RECORD |  | NO_RECORD |
| 7290117265888 | bsip1_hardcheese_72901172 | גבינת גאודה מגורדת יוחננוף 400 גרם | NO_RECORD |  | NO_RECORD |
| 7296073731856 | HC-7296073731856 | גבינת גאודה פרוסה 28% | NO_RECORD |  | NO_RECORD |
| 5384356 | HC-5384356 | גבינה חצי קשה אמנטל 28% | NO_RECORD |  | NO_RECORD |
| 9150162 | HC-9150162 | גאודה חצי קשה 28% שומן | NO_RECORD |  | NO_RECORD |
| 7290116931524 | HC-7290116931524 | פרוסות גאודה | NO_RECORD |  | NO_RECORD |
| 3073781199918 | bsip1_hardcheese_30737811 | גבינה חצי קשה 24% בייבי בל 5*20 גרם | NO_RECORD |  | NO_RECORD |
| 5079658 | HC-5079658 | נעם גבינה צהובה28% חריץ | NO_RECORD |  | NO_RECORD |
| 5079665 | HC-5079665 | נועם גבינה צהובה9% חריץ | NO_RECORD |  | NO_RECORD |
| 5079672 | HC-5079672 | נעם גבינה צהובה22% משקל | NO_RECORD |  | NO_RECORD |
| 7290004122195 | bsip1_hardcheese_72900041 | פרוסות גבינה חצי קשה גוש חלב 28% מהדרין 200 גרם | NO_RECORD |  | NO_RECORD |
| 7290014455245 | HC-7290014455245 | גרנה פדנו משולש | NO_RECORD |  | NO_RECORD |
| 7290017065434 | bsip1_hardcheese_72900170 | פרוסות גבינת גאודה הולנדית 30% 200 גרם | NO_RECORD |  | NO_RECORD |
| 7290019635192 | HC-7290019635192 | גאודה עיזים פרוס 30%שומן | NO_RECORD |  | NO_RECORD |
| 7290020467393 | HC-7290020467393 | גאודה מאסדם אמנטל הולנדי | NO_RECORD |  | NO_RECORD |
| 7290114311601 | HC-7290114311601 | גאודה נעם 30% | NO_RECORD |  | NO_RECORD |
| 7290114312813 | HC-7290114312813 | אמנטל נועם פתיחה חוזרת | NO_RECORD |  | NO_RECORD |
| 8606974 | HC-8606974 | גבינת גאודה גוסטו 30% | NO_RECORD |  | NO_RECORD |
| 8711528211138 | bsip1_hardcheese_87115282 | גבינת גאודה עיזים. | NO_RECORD |  | NO_RECORD |
| 7290014760912 | HC-7290014760912 | גבינה צהובה 28% מהדרין | NO_RECORD |  | NO_RECORD |
| 4122270 | HC-4122270 | גבינה צהובה פרוס 28% | NO_RECORD |  | NO_RECORD |
| 7290110320850 | HC-7290110320850 | פתיתי עמק 28% | NO_RECORD |  | NO_RECORD |
| 7296073735151 | HC-7296073735151 | גבינה גרנה פדנו מגורד | NO_RECORD |  | NO_RECORD |
| 8606608 | HC-8606608 | גבינת גאודה פסטו אדום32% | NO_RECORD |  | NO_RECORD |
| 53219 | HC-53219 | גבינה צהובה 32% | NO_RECORD |  | NO_RECORD |
| 7290110323301 | HC-7290110323301 | גבינה צהובה טל העמק 32% | NO_RECORD |  | NO_RECORD |
| 7296073453482 | HC-7296073453482 | גבינה צהובה 32% פרוס | NO_RECORD |  | NO_RECORD |

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

### juices — juices_frontend_v3.json (17 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290004030100 | jc-003 | 100% מיץ תפוזים ולנסיה סחוט 1 ליטר פריני | NO_RECORD |  | NO_RECORD |
| 7290013608260 | jc-006 | מיץ רימונים 100%מיץ סחוט טרי מצונן 1ליט | NO_RECORD |  | NO_RECORD |
| 7290000525969 | jc-001 | מיץ תפוזים סחוט 1 ליטר | NO_RECORD |  | NO_RECORD |
| 7290013153395 | jc-005 | סחוט 1 ליטר רימונים | NO_RECORD |  | NO_RECORD |
| 7290110114886 | jc-011 | סחוט קלמנטינה 2 ליטר | NO_RECORD |  | NO_RECORD |
| 7290003009640 | jc-002 | סחוט תפוז 1 ליטר | NO_RECORD |  | NO_RECORD |
| 7290008690713 | jc-017 | מיץ חמוציות 1 ליטר | NO_RECORD |  | NO_RECORD |
| 7290019056720 | jc-018 | מיץ ענבים 2 ליטר | NO_RECORD |  | NO_RECORD |
| 7290006822192 | jc-019 | מיץ חמוציות דיאט 1 ליטר | NO_RECORD |  | NO_RECORD |
| 7290000136523 | jc-020 | ג'אמפ ענבים 1.5 ליטר | NO_RECORD |  | NO_RECORD |
| 7290001247891 | jc-021 | נקטר אפרסקים פחית 330 מ"ל | NO_RECORD |  | NO_RECORD |
| 7290001247723 | jc-022 | נקטר תות בננה פחית 330 מ"ל | NO_RECORD |  | NO_RECORD |
| 7290019056737 | jc-023 | מיץ אשכולית 2 ליטר | NO_RECORD |  | NO_RECORD |
| 7290001247730 | jc-024 | נקטר מנגו פחית 330 מ"ל | NO_RECORD |  | NO_RECORD |
| 7290019056355 | jc-025 | לימונענע 1.5 ליטר | NO_RECORD |  | NO_RECORD |
| 7290019056591 | jc-026 | ענבים 1.5 ליטר | NO_RECORD |  | NO_RECORD |
| 7290013153418 | jc-027 | סחוט לימונענע 1 ליטר | NO_RECORD |  | NO_RECORD |

### milk-comparison — milk_frontend_v1.json (18 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290000051352 | milk_7290000051352 | חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן | NOT_FOUND |  | ok |
| 7290019790259 | milk_7290019790259 | חלב טבעי 4% 1 ליטר | NOT_FOUND |  | ok |
| 7290102392094 | milk_7290102392094 | חלב עיזים בקרטון 1 ליטר | NOT_FOUND |  | ok |
| 7290114313865 | milk_7290114313865 | חלב נטול לקטוז מועשר בחלבון 2% שומן 1 ליטר | NOT_FOUND |  | ok |
| 7290116936116 | milk_7290116936116 | משקה סויה ללא סוכרים 1 ליטר | NOT_FOUND |  | ok |
| 7290110324926 | milk_7290110324926 | משקה סויה ללא תוספת סוכר | NOT_FOUND |  | ok |
| 7290107932134 | milk_7290107932134 | חלב בבקבוק 1% מועשר- מהדרין | NOT_FOUND |  | ok |
| 7290014760141 | milk_7290014760141 | משקה שקדים | NOT_FOUND |  | ok |
| 7394376620904 | milk_7394376620904 | משקה שיבולת שועל ללא סוכר | NOT_FOUND |  | ok |
| 7290119385560 | milk_7290119385560 | משקה סויה בריסטה 500 מ"ל | NOT_FOUND |  | ok |
| 7394376619939 | milk_7394376619939 | משקה בריסטה שיבולת שועל | NOT_FOUND |  | ok |
| 7394376621451 | milk_7394376621451 | משקה בריסטה שיבולת שועל להקצפה | NOT_FOUND |  | ok |
| 5411188124689 | milk_5411188124689 | שיבולת שועל ללא סוכר | NOT_FOUND |  | ok |
| 8000215204554 | milk_8000215204554 | משקה אורז קוקוס אורגני | NOT_FOUND |  | ok |
| 7290110325619 | milk_7290110325619 | משקה שיבולת שועל | NOT_FOUND |  | ok |
| 8000215204219 | milk_8000215204219 | משקה אורז אורגני | NOT_FOUND |  | ok |
| 5411188112709 | milk_5411188112709 | שקדים ללא סוכר | NOT_FOUND |  | ok |
| 5411188300328 | milk_5411188300328 | שוקו משקה סויה | NOT_FOUND |  | ok |

### protein-bars — protein_combined_frontend_v2.json (32 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290017516295 | pb-002 | חטיף חלבון אגוזי לוז | NOT_FOUND |  | ok |
| 7290121161886 | pb-003 | חטיף חלבון בננה שוקולד | NOT_FOUND |  | ok |
| 7290121166850 | pb-004 | חטיף חלבון וניל קראנץ' | NOT_FOUND |  | ok |
| 8410076610379 | pb-005 | נייטשר פרוטאין שוקולד | NOT_FOUND |  | ok |
| 8410076610386 | pb-006 | נייטשר פרוטאין קרמל מלוח | NOT_FOUND |  | ok |
| 7290019766025 | pb-007 | אול אין סופט פיסטוק | NO_RECORD |  | NO_RECORD |
| 7290119371129 | pb-009 | חטיף חלבון שוקולד עוגיות | NO_RECORD |  | NO_RECORD |
| 7290119371112 | pb-010 | חטיף חלבון קרמל ואגוזים | NOT_FOUND |  | ok |
| 7290019401018 | pb-011 | חטיף קרם עוגיות | NOT_FOUND |  | ok |
| 7290019401049 | pb-012 | חטיף שוקולד קרמל | NOT_FOUND |  | ok |
| 7290015130035 | pb-013 | WIN חטיף חלבון קרם קרמל | NOT_FOUND |  | ok |
| 7290015130042 | pb-014 | WIN חטיף חלבון קרם קרמל | NOT_FOUND |  | ok |
| 7290018703991 | pb-015 | עוגיית חלבון דאבל שוקולד | NO_RECORD |  | NO_RECORD |
| 7290018703984 | pb-016 | עוגיית חלבון שוקולד צ'יפ | NO_RECORD |  | NO_RECORD |
| 7290015130028 | pb-008 | WIN חטיף חלבון קרם חלב | NO_RECORD |  | NO_RECORD |
| 7290117384572 | pb-017 | חטיף חלבון קרם עוגיות | NOT_FOUND |  | ok |
| 7290117384589 | pb-018 | חטיף חלבון קרמל מלוח | NOT_FOUND |  | ok |
| 7290117384596 | pb-019 | חטיף חלבון פאי קינמון | NOT_FOUND |  | ok |
| 7290121160582 | pb-020 | חטיף חלבון חמאת בוטנים | NOT_FOUND |  | ok |
| 7290121161916 | pb-021 | חטיף חלבון טריפל שוקולד | NOT_FOUND |  | ok |
| 7290121161930 | pb-022 | חטיף חלבון טעם בננה טופי | NOT_FOUND |  | ok |
| 7290019766018 | pb-023 | אול אין חלבון סופט עוגיות | NOT_FOUND |  | ok |
| 7290018703304 | pb-024 | אול אין קרם עוגיות | NO_RECORD |  | NO_RECORD |
| 7290018703076 | pb-025 | אול אין דאבל שוקולד | NOT_FOUND |  | ok |
| 7290018043899 | pb-026 | אול אין בוטנים קרמל | NOT_FOUND |  | ok |
| 7290018043134 | pb-027 | אול אין שוק.לבן עוגיות | NOT_FOUND |  | ok |
| 7290019310235 | pb-028 | אול אין ונילה קראנץ | NO_RECORD |  | NO_RECORD |
| 7290019766230 | pb-029 | חטיף חלבון אסטרה סופט | NO_RECORD |  | NO_RECORD |
| 7290019401544 | pb-030 | חטיף עוגיות טופי | NOT_FOUND |  | ok |
| 7290112915382 | pb-031 | חטיף חלבון שוקולד דובאי | NOT_FOUND |  | ok |
| 7290112913487 | pb-032 | חטיף חלבון קרם אגוזים | NOT_FOUND |  | ok |
| 7290112915351 | pb-033 | חטיף חלבון קרמל מלוח | NOT_FOUND |  | ok |

### snacks — snacks_frontend_v5.json (21 products)

| Barcode | Raw ID | Name | panel_source | img_off | Status |
|---|---|---|---|---|---|
| 7290100659090 | snk-001 | חטיף תמרים וקינמון | NOT_FOUND |  | ok |
| 7290011498894 | snk-002 | חטיפי תמר + חמאת בוטנים | NOT_FOUND |  | ok |
| 7290105436382 | snk-003 | חטיפי תמרים קשיו | NOT_FOUND |  | ok |
| 7290011498948 | snk-004 | חטיפי תמר בציפוי שוקולד | NOT_FOUND |  | ok |
| 7290105431516 | snk-005 | חטיפי תמרים ובוטנים | NOT_FOUND |  | ok |
| 16000548404 | snk-006 | חטיף שיבולת שועל עם דבש | NOT_FOUND |  | ok |
| 16000548503 | snk-007 | חטיף שיבולת שועל+מייפל | NOT_FOUND |  | ok |
| 7290011498986 | snk-008 | חטיף תמרים עם חמאת קשיו | NOT_FOUND |  | ok |
| 7290011498917 | snk-009 | חטיפי תמר+קוקוס מצופים | NOT_FOUND |  | ok |
| 7290011498900 | snk-010 | חטיף תמר עם חמאת שקד | NOT_FOUND |  | ok |
| 16000423534 | snk-011 | חטיף שיבולת שועל+שוקולד | NOT_FOUND |  | ok |
| 6009684861000 | snk-013 | חטיף גרנולה דבש ומייפל | NOT_FOUND |  | ok |
| 7290107971522 | snk-012 | חטיף בוטנים ושקדים קראנצ | NOT_FOUND |  | ok |
| 8423207208703 | snk-014 | חטיף דגנים שוקולד מריר · | NOT_FOUND |  | ok |
| 8410076610508 | snk-015 | חטיף בוטנים עם שוקולד | NOT_FOUND |  | ok |
| 8423207208680 | snk-016 | חטיף קידס שוקולד חלב | NOT_FOUND |  | ok |
| 8410076610492 | snk-017 | חטיף בוטנים ושיבולת שועל | NOT_FOUND |  | ok |
| 7290019297208 | snk-018 | חטיף גרנולה פירות יבשים | NOT_FOUND |  | ok |
| 4011800633516 | snk-019 | חטיף דגנים שוקולד מריר · | NOT_FOUND |  | ok |
| 4011800628512 | snk-020 | חטיפי דגנים+שוקולד | NOT_FOUND |  | ok |
| 4011800632519 | snk-021 | חטיפי קוקוס שוקולד | NOT_FOUND |  | ok |

