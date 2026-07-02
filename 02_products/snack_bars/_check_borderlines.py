"""Check remaining borderline products in the final corpus."""
import json, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = pathlib.Path(r"C:\Bari")
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / "run_snacks_task360_phase3_20260620_083413" / "output"
FRONTEND = ROOT / "bari-web" / "src" / "data" / "comparisons" / "snacks_frontend_v5.json"

with open(FRONTEND, encoding='utf-8') as f:
    fe = json.load(f)
prods = fe['products']

# Look at products that might be borderline: check their BSIP1 for ingredients
BORDERLINE_CHECK = [
    "110844",       # כיפלי חטיף בטעם גריל
    "40052403",     # חטיף קיט קאט אצבעות
    "3444009",      # חטיף שוקולד חלב עם חמאת בוטנים (Hershey's)
    "8000500023624",# קינדר הפי היפו
    "72917329",     # חטיף שוקולד אגוזי עלית
    "72918388",     # חטיף שוקולד טוויסט עלית
    "7290116532011",# חטיף קליק נוגט
    "7290112495112",# חטיף נשנושים זעתר בייגל בייגל
    "7290116536224",# חטיף נשנושים פלוס בייגל בייגל
    "8802241132821",# חטיף אצות
    "8802241136249",# חטיף אצות ים נורי
    "6342515",      # חטיף מאנצ'יס ששון הקולה
]

for barcode in BORDERLINE_CHECK:
    bsip1_path = BSIP1_DIR / f"bsip1_{barcode}.json"
    if not bsip1_path.exists():
        print(f"{barcode}: BSIP1 NOT FOUND")
        continue
    with open(bsip1_path, encoding='utf-8') as f:
        b = json.load(f)
    name = b.get('canonical_name_he', '')
    brand = b.get('brand', '')
    ingr = b.get('ingredients_text_he', '') or ''
    nutr = b.get('normalized_nutrition_per_100g', {}) or {}
    cats = b.get('allCategoryCodes', []) or b.get('shelf_categories', []) or []
    unit = b.get('unitDescription', '') or b.get('unit_description', '') or ''

    # Find product in frontend
    fe_prod = next((p for p in prods if str(p.get('barcode','')) == barcode), None)
    score = fe_prod.get('score') if fe_prod else '?'
    grade = fe_prod.get('grade') if fe_prod else '?'

    print(f"\n{barcode} | {brand} | {name}")
    print(f"  score={score}/{grade} | unit={unit}")
    print(f"  ingredients: {ingr[:100] if ingr else 'NONE'}")
    print(f"  kcal/100g={nutr.get('energy_kcal')} fat={nutr.get('fat_g')} sat={nutr.get('fat_saturated_g')} sugar={nutr.get('sugars_g')} protein={nutr.get('protein_g')}")
    print(f"  cats: {cats[:3]}")
