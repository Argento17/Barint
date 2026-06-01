## HUMMUS
traces=69 scored=69 | conf mean/min/max=87.5/5/100 | score mean/min/max=65.2/42.8/85.5
bands={'low': 2, 'high': 64, 'medium': 1, 'insufficient': 2} grades={'B': 28, 'A': 8, 'C': 27, 'D': 4, 'insufficient_data': 2}
counts: flagged=64 mktIng=15 lowCatConf=2 evalNonStd=2 dataInsuff=2 scGuess=16 singleCap=19

TOP6 (name | score | grade | conf):
  + חומוס ענק | 85.5 | A | 90
  + חומוס | 85.5 | A | 90
  + חומוס גדול שופרסל | 85.4 | A | 100
  + חומוס לבן ענק שופרסל | 85.4 | A | 100
  + חומוס מוקפא | 85 | A | 100
  + חומוס ענק | 85 | A | 95
BOTTOM6:
  - ממרח פלפלים קלויים | 42.8 | D | 90
  - ממרח פלפלים קלויים | 48.0 | D | 95
  - מטבוחה אמיתית | 48.7 | D | 90
  - מטבוחה חריפה | 49.6 | D | 90
  - חציל על האש בטחינה | 50.0 | C | 90
  - חומוס | 50 | insufficient_data | 5

MOST SEVERE EXCEPTIONS (sev>=2), up to 18:
  [sev 6] חומוס | sc=50 gr=insufficient_data conf=5 catconf=0.94 cat=sauce_spread | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 6] חומוס ענק | sc=50 gr=insufficient_data conf=5 catconf=0.94 cat=sauce_spread | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 5] חומוס שלם יכין | sc=79.9 gr=B conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,structural_class_guess<0.35,single_cap_driver
  [sev 5] הקיסר חומוס ענק | sc=80.4 gr=A conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,structural_class_guess<0.35,single_cap_driver
  [sev 5] חומוס אבו גוש | sc=69.9 gr=B conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,structural_class_guess<0.35
  [sev 5] חומוס מסעדות | sc=75.7 gr=B conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,structural_class_guess<0.35,single_cap_driver
  [sev 5] חומוס אסלי | sc=70.6 gr=B conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,structural_class_guess<0.35
  [sev 5] חומוס | sc=70.6 gr=B conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,structural_class_guess<0.35
  [sev 4] חומוס עם טחינה אחלה | sc=63.5 gr=C conf=90 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,ingredient_count<=1,missing>=3_nutr_fields
  [sev 4] סלט פלפלים קלויים | sc=63.5 gr=C conf=65 catconf=0.3 cat=default | low_category_confidence,category_instability,structural_class_guess<0.35,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 4] סלט חציל בטעם כבד | sc=56.1 gr=C conf=90 catconf=0.91 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,missing>=3_nutr_fields
  [sev 4] חומוס עם מלא מטבוחה חריף | sc=65.2 gr=B conf=90 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,ingredient_count<=1,missing>=3_nutr_fields
  [sev 4] חומוס לבן ענק שופרסל | sc=85.4 gr=A conf=100 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,ingredient_count<=1
  [sev 4] חומוס גדול שופרסל | sc=85.4 gr=A conf=100 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,ingredient_count<=1
  [sev 4] סלט חומוס+מסבחה | sc=68.2 gr=B conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients
  [sev 4] סלט חומוס עם טחינה | sc=68.5 gr=B conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients
  [sev 4] חומוס מסבחה | sc=64.2 gr=C conf=95 catconf=0.94 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients
  [sev 4] סלט חצילים על האש | sc=61.6 gr=C conf=95 catconf=0.91 cat=sauce_spread | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients

==========================================================================================

## MAADANIM
traces=200 scored=200 | conf mean/min/max=76.3/0/100 | score mean/min/max=45.1/21.5/77.0
bands={'insufficient': 29, 'medium': 10, 'high': 150, 'low': 11} grades={'insufficient_data': 31, 'D': 98, 'E': 28, 'C': 39, 'B': 4}
counts: flagged=179 mktIng=63 lowCatConf=71 evalNonStd=31 dataInsuff=31 scGuess=48 singleCap=59

TOP6 (name | score | grade | conf):
  + יוגורט גו נטול לקטוז | 77.0 | B | 90
  + ביו 25 פרוביוטיקה | 75 | insufficient_data | 40
  + גבינה צפתית מעודנת 5% | 71.2 | B | 90
  + יופלה GO מועשר בחלבון | 69.6 | B | 90
  + ברנפלקס ללא תוספת סוכר | 65.7 | B | 80
  + מולר פרוטאין טופ בוטנים | 64.3 | C | 95
BOTTOM6:
  - טארטלטים לקינוח | 21.5 | insufficient_data | 40
  - מילקי קייק מארז | 26.6 | E | 90
  - מילקי קייק | 26.6 | E | 90
  - מילקי קייק מיניס קרם חלב | 26.9 | E | 90
  - סירופ דיאט לימונענע | 27.3 | E | 70
  - קונפיטורה תות שדה לייט | 29.3 | E | 85

MOST SEVERE EXCEPTIONS (sev>=2), up to 18:
  [sev 9] שריר הזרוע (8) בעדני | sc=50 gr=insufficient_data conf=0 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,low_category_confidence,category_instability,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 9] ביו LR 25 בד"ץ | sc=50 gr=insufficient_data conf=0 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,low_category_confidence,category_instability,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 9] ביו 25 | sc=50 gr=insufficient_data conf=0 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,low_category_confidence,category_instability,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 9] מיקס לילד | sc=50 gr=insufficient_data conf=0 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,low_category_confidence,category_instability,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 9] גבינת בולגרית 5% גד ארוז | sc=50 gr=insufficient_data conf=0 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,low_category_confidence,category_instability,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 9] המבורגר ילדים | sc=50 gr=insufficient_data conf=0 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,low_category_confidence,category_instability,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 9] בולגרית מעודנת 24% | sc=50 gr=insufficient_data conf=0 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,low_category_confidence,category_instability,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 7] סופר גמדים תות בננה מארז | sc=52.8 gr=C conf=85 catconf=0.3 cat=default | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,low_category_confidence,category_instability,unresolved_flags
  [sev 7] גמדים לשתיה תות בננה | sc=46.5 gr=D conf=85 catconf=0.3 cat=default | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,low_category_confidence,category_instability,unresolved_flags
  [sev 7] ביו קיד אבקה | sc=49.2 gr=insufficient_data conf=20 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,low_category_confidence,category_instability,structural_class_guess<0.35,missing>=3_nutr_fields,unresolved_flags
  [sev 7] דנונה מולטי קולגן | sc=45.4 gr=D conf=87 catconf=0.55 cat=dessert | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,low_category_confidence,category_instability,unresolved_flags
  [sev 7] חסה מעודנת הידרופונית | sc=50 gr=insufficient_data conf=20 catconf=0.3 cat=default | eval_status=context_limited,data_suff=insufficient,ingredient_list=marketing_prose,low_category_confidence,category_instability,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 6] פנקייק מיקס | sc=48.7 gr=D conf=87 catconf=0.55 cat=snack_bar_granola | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,low_category_confidence,structural_class_guess<0.35,single_cap_driver
  [sev 6] ביו בליס פרוביוטיקה | sc=50 gr=insufficient_data conf=5 catconf=0.92 cat=dessert | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 6] מגה פרוביוטיק 500 מ"ג | sc=50 gr=insufficient_data conf=5 catconf=0.92 cat=dessert | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 6] פרוביוטיק SHAPE | sc=50 gr=insufficient_data conf=5 catconf=0.92 cat=dessert | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 6] ביוגאיה טיפות פרוביוטיקה | sc=50 gr=insufficient_data conf=5 catconf=0.92 cat=dessert | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 6] יומי פרוביוטיק בטעם תות | sc=50 gr=insufficient_data conf=5 catconf=0.92 cat=dessert | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags

==========================================================================================

## SNACKS
traces=53 scored=53 | conf mean/min/max=75.5/5/100 | score mean/min/max=37.5/13.4/70
bands={'high': 35, 'insufficient': 5, 'medium': 13} grades={'C': 12, 'insufficient_data': 5, 'E': 23, 'D': 12, 'B': 1}
counts: flagged=38 mktIng=14 lowCatConf=11 evalNonStd=5 dataInsuff=5 scGuess=11 singleCap=7

TOP6 (name | score | grade | conf):
  + חטיף תמרים במילוי חמאת שקדים | 70 | B | 72
  + מרבה סלים דליס שוקולד לבן בטעם יוגורט | 59.5 | C | 82
  + מרבה סלים דליס שוקולד חלב ללא גלוטן חדש | 59.2 | C | 67
  + מרבה סלים דליס שוקולד מריר חדש | 58.6 | C | 82
  + חטיף תמרים בציפוי שוקולד 100% קקאו | 56.7 | C | 60
  + חטיף תמרים במילוי חמאת בוטנים | 55.0 | C | 82
BOTTOM6:
  - שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קרם חלב | 13.4 | E | 100
  - קורני חטיפי דגנים קוקוס שוקולד | 15.2 | E | 95
  - חטיף דגנים שוגי שישייה 156 גרם | 15.6 | E | 90
  - חטיף דגנים שוגי שוקו שישייה 156 גרם | 15.8 | E | 90
  - קורני חטיפי דגנים+שוקולד חלב | 16.3 | E | 72
  - קורני חטיפי דגנים שוקולד בננה | 16.4 | E | 80

MOST SEVERE EXCEPTIONS (sev>=2), up to 18:
  [sev 6] חטיף אגוזים וחמוציות רפאלס 5*30 גרם | sc=50 gr=insufficient_data conf=5 catconf=0.81 cat=whole_food_fat | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,unresolved_flags
  [sev 6] חטיף פאי פקאן רפאלס 5*30 גרם | sc=50 gr=insufficient_data conf=5 catconf=0.92 cat=snack_bar_granola | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 6] חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם | sc=50 gr=insufficient_data conf=5 catconf=0.92 cat=cereal | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 6] חטיף דגנים מצופה שוקולד מריר סלים דליס | sc=50 gr=insufficient_data conf=5 catconf=0.92 cat=snack_bar_granola | eval_status=context_limited,data_suff=insufficient,ingredient_count<=1,missing>=3_nutr_fields,single_cap_driver,unresolved_flags
  [sev 5] נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים חמישייה | sc=38.7 gr=D conf=87 catconf=0.51 cat=snack_bar_granola | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,low_category_confidence
  [sev 4] קראנצ'י חטיף שיבולת שועל מיקס חמישייה | sc=34.2 gr=insufficient_data conf=27 catconf=0.65 cat=cereal | eval_status=context_limited,data_suff=insufficient,structural_class_guess<0.35,missing>=3_nutr_fields,unresolved_flags
  [sev 4] חטיפי דגנים פיטנס קרם ועוגיות שישייה | sc=25.7 gr=E conf=80 catconf=0.47 cat=snack_bar_granola | ingredient_list=marketing_prose,low_category_confidence,category_instability,unresolved_flags
  [sev 4] חטיף דגנים שוקו וניל נסטלה שישייה | sc=28.5 gr=E conf=95 catconf=0.92 cat=snack_bar_granola | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients
  [sev 4] סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6 יח' | sc=27.0 gr=E conf=92 catconf=0.62 cat=snack_bar_granola | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients
  [sev 4] חטיף דגנים עם פירות יער | sc=25.0 gr=E conf=95 catconf=0.92 cat=snack_bar_granola | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients
  [sev 4] פרי מארז חטיפי תמרים ושברי קקאו 5+1 | sc=42.3 gr=D conf=75 catconf=0.4 cat=whole_food_fat | low_category_confidence,category_instability,structural_class_guess<0.35,unresolved_flags
  [sev 4] פיטנס בר גרנולה שוקולד מריר | sc=17.9 gr=E conf=95 catconf=0.9 cat=snack_bar_granola | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients
  [sev 4] חטיפי פיטנס שיבולת שועל דבש 5*38 גרם | sc=39.8 gr=D conf=85 catconf=0.87 cat=cereal | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,unresolved_flags
  [sev 4] נייצר וואלי פרוטאין בוטנים ושבבי שוקולד רביעייה | sc=47.4 gr=D conf=95 catconf=0.8 cat=snack_bar_granola | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients
  [sev 4] נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה | sc=38.2 gr=D conf=72 catconf=0.53 cat=snack_bar_granola | ingredient_list=marketing_prose,low_category_confidence,category_instability,unresolved_flags
  [sev 3] חטיפי דגנים פיטנס שקדים ודבש שישייה | sc=45.0 gr=D conf=87 catconf=0.56 cat=whole_food_fat | low_category_confidence,category_instability,unresolved_flags
  [sev 3] מרבה סלים דליס קריספי תות 125 גר | sc=28.9 gr=E conf=67 catconf=0.54 cat=snack_bar_granola | low_category_confidence,category_instability,unresolved_flags
  [sev 2] קורני חטיפי דגנים+שוקולד חלב | sc=16.3 gr=E conf=72 catconf=0.77 cat=snack_bar_granola | ingredient_list=marketing_prose,structural_class_guess<0.35

==========================================================================================

## YOGURTS
traces=45 scored=45 | conf mean/min/max=93.6/75/100 | score mean/min/max=64.9/31.3/85
bands={'high': 44, 'medium': 1} grades={'A': 11, 'B': 9, 'C': 19, 'D': 5, 'E': 1}
counts: flagged=42 mktIng=0 lowCatConf=8 evalNonStd=0 dataInsuff=0 scGuess=0 singleCap=26

TOP6 (name | score | grade | conf):
  + לבן 1.5% חלב טנובה | 85 | A | 100
  + קפיר שתייה 3% | 85 | A | 92
  + לבן שתייה 3% טנובה | 85 | A | 92
  + יוגורט יווני חלבון 18 טהור | 85 | A | 100
  + קפיר 2% שומן | 85 | A | 100
  + לבן שתייה 3% שומן | 85 | A | 92
BOTTOM6:
  - מוס שוקולד יוגורט | 31.3 | E | 85
  - יוגורט מולר קורנר דבש אגוזים | 36.3 | D | 92
  - קרם יוגורט קרמל | 40.6 | D | 92
  - יוגורט ילדים תות ואניל | 46.3 | D | 100
  - יוגורט עם ריבת תות | 48.7 | D | 95
  - אקטימל משקה חלב פרוביוטי | 49.8 | D | 87

MOST SEVERE EXCEPTIONS (sev>=2), up to 18:
  [sev 3] יוגורט שיבולת שועל | sc=71.7 gr=B conf=87 catconf=0.53 cat=dairy_protein | low_category_confidence,category_instability,unresolved_flags
  [sev 3] יוגורט שקדים ואניל | sc=59.3 gr=C conf=87 catconf=0.55 cat=dairy_protein | low_category_confidence,category_instability,single_cap_driver,unresolved_flags
  [sev 2] אקטימל משקה חלב פרוביוטי | sc=49.8 gr=D conf=87 catconf=0.71 cat=beverage | category_instability,single_cap_driver,unresolved_flags
  [sev 2] שתייה חלב לילדים פרוביוטיקה | sc=50.4 gr=C conf=87 catconf=0.71 cat=beverage | category_instability,single_cap_driver,unresolved_flags
  [sev 2] יוגורט סויה טבעי | sc=74.8 gr=B conf=87 catconf=0.71 cat=dairy_protein | category_instability,unresolved_flags
  [sev 2] יוגורט שתייה תות | sc=56.8 gr=C conf=87 catconf=0.66 cat=dairy_protein | category_instability,single_cap_driver,unresolved_flags
  [sev 2] קפיר שתייה 3% | sc=85 gr=A conf=92 catconf=0.66 cat=dairy_protein | category_instability,ingredient_count<=1,unresolved_flags

==========================================================================================

## BREAD
traces=32 scored=32 | conf mean/min/max=90.1/82/95 | score mean/min/max=62.8/28.4/85
bands={'high': 32} grades={'D': 4, 'B': 15, 'A': 1, 'C': 11, 'E': 1}
counts: flagged=13 mktIng=0 lowCatConf=0 evalNonStd=0 dataInsuff=0 scGuess=6 singleCap=8

TOP6 (name | score | grade | conf):
  + עוגיות אורז ללא מלח | 85 | A | 95
  + קרקר חיטה מלאה פשוט | 79.7 | B | 90
  + לחמי קריספ מחמצת שיפון מסורתי | 79.4 | B | 90
  + לחמי קריספ שיפון וגרעינים נורדי | 79.4 | B | 90
  + לחמי קריספ שיפון פשוט | 79.3 | B | 90
  + לחם מחמצת אמיתי ממחיטה מלאה | 79.0 | B | 90
BOTTOM6:
  - קרקרים מתוקים לילדים "גולדה קידס" | 28.4 | E | 95
  - פצפוצי דגנים "פצ'פץ'" בטעם דבש | 35.3 | D | 90
  - קרקר מלוח פריך | 36.0 | D | 90
  - לחמי קריספ "שום ועשבים" תעשייתי | 40.6 | D | 95
  - לחם "קטו" דל פחמימות | 49.0 | D | 95
  - עוגיות אורז שוקולד "בלה שוקו" | 51.0 | C | 82

MOST SEVERE EXCEPTIONS (sev>=2), up to 18:

==========================================================================================

## MILK
traces=20 scored=20 | conf mean/min/max=87/77/95 | score mean/min/max=57.1/38.1/85
bands={'medium': 2, 'high': 18} grades={'D': 8, 'C': 7, 'A': 3, 'B': 2}
counts: flagged=16 mktIng=2 lowCatConf=5 evalNonStd=0 dataInsuff=0 scGuess=0 singleCap=6

TOP6 (name | score | grade | conf):
  + חלב עיזים בקרטון 1 ליטר | 85 | A | 95
  + חלב טבעי 4% 1 ליטר | 85 | A | 90
  + חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן | 85 | A | 95
  + חלב נטול לקטוז מועשר בחלבון 2% שומן 1 ליטר | 74.1 | B | 90
  + משקה סויה ללא סוכרים 1 ליטר | 67.0 | B | 90
  + חלב בבקבוק 1% מועשר- מהדרין | 60.2 | C | 85
BOTTOM6:
  - אלפרו שוקו משקה סויה | 38.1 | D | 90
  - משקה חלב גו 27 גרם חלבון 2% בטעם וניל 340 מ"ל | 41.4 | D | 87
  - אלפרו שקדים ללא סוכר | 45.3 | D | 77
  - משקה שיבולת שועל | 48.5 | D | 87
  - משקה סויה בריסטה אלפרו 500 מ"ל | 48.7 | D | 90
  - משקה אורז קוקוס אורגני | 49.1 | D | 87

MOST SEVERE EXCEPTIONS (sev>=2), up to 18:
  [sev 7] משקה שיבולת שועל | sc=48.5 gr=D conf=87 catconf=0.56 cat=beverage | ingredient_list=marketing_prose,HIGHCONF_on_bad_ingredients,low_category_confidence,category_instability,unresolved_flags
  [sev 3] אלפרו שיבולת שועל ללא סוכר | sc=51.0 gr=C conf=82 catconf=0.55 cat=beverage | low_category_confidence,category_instability,missing>=3_nutr_fields,unresolved_flags
  [sev 3] משקה שקדים | sc=52.7 gr=C conf=82 catconf=0.71 cat=beverage | ingredient_list=marketing_prose,category_instability,single_cap_driver,unresolved_flags
  [sev 3] משקה בריסטה שיבולת שועל | sc=50.7 gr=C conf=87 catconf=0.5 cat=beverage | low_category_confidence,category_instability,unresolved_flags
  [sev 3] משקה שיבולת שועל ללא סוכר | sc=51.9 gr=C conf=87 catconf=0.56 cat=beverage | low_category_confidence,category_instability,unresolved_flags
  [sev 3] משקה בריסטה שיבולת שועל להקצפה | sc=50.7 gr=C conf=87 catconf=0.5 cat=beverage | low_category_confidence,category_instability,unresolved_flags
  [sev 2] משקה חלב גו 27 גרם חלבון 2% בטעם וניל 340 מ"ל | sc=41.4 gr=D conf=87 catconf=0.71 cat=beverage | category_instability,unresolved_flags

==========================================================================================
