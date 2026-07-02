"""TASK-404: Patch BSIP1 record for jc-021 with corrected sugar=9.4g."""
import sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

path = r'C:\Bari\02_products\juices\bsip1_outputs\bsip1_juice_7290001247891.json'

with open(path, 'r', encoding='utf-8') as f:
    doc = json.load(f)

old_sugar = doc.get('sugars_g')
old_norm = doc.get('normalized_nutrition_per_100g', {}).get('sugars_g')
print(f'BEFORE: sugars_g={old_sugar}, normalized sugars_g={old_norm}')

doc['sugars_g'] = 9.4
doc['normalized_nutrition_per_100g']['sugars_g'] = 9.4

doc['_task404_correction'] = {
    'field': 'sugars_g',
    'old_value': old_sugar,
    'new_value': 9.4,
    'corrected_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'authorized_by': 'TASK-404 owner tripwire-1 approval',
    'reason': (
        'Yochananof retailer data entry error: 2.25g sugar with 40kcal is physically '
        'impossible for a peach nectar with added white sugar and no fat/protein/fiber. '
        'Correction derived from sibling products jc-022=9.4g@41kcal, jc-024=9.0g@40kcal. '
        'Plausibility: 9.4*4=37.6kcal consistent with 40kcal and carbs=9.9g. '
        'All 4 retailers attempted per SOURCE_SELECTION_POLICY; '
        'Shufersal/Victory reached but barcode not found; Rami Levy/Yochananof blocked from sandbox.'
    ),
}

with open(path, 'w', encoding='utf-8') as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

sha256 = hashlib.sha256(open(path, 'rb').read()).hexdigest()
print(f'AFTER: sugars_g={doc["sugars_g"]}, normalized sugars_g={doc["normalized_nutrition_per_100g"]["sugars_g"]}')
print(f'SHA-256: {sha256}')
print('BSIP1 record patched.')
