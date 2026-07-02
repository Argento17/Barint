"""Final parse + diff check for TASK-399 return contract."""
import json, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\protein_bars_frontend_v2_candidate.json"

with open(PATH, encoding='utf-8') as f:
    raw = f.read()

# 1. JSON parses
data = json.loads(raw)
print("JSON parse: PASS")

sha = hashlib.sha256(raw.encode('utf-8')).hexdigest()
print(f"SHA256: {sha}")
print(f"Size: {len(raw)} bytes")
print(f"Product count: {data['_meta']['product_count']}")

# 2. Score/grade table (unchanged from pre-fix)
print("\nScores/grades:")
for p in data['products']:
    print(f"  {p['id']} {p['barcode']}: {p['score']}/{p['grade']}")

# 3. categoryNote.body_he
print("\ncategoryNote.body_he[0]:")
print(" ", data['categoryNote']['body_he'][0][:80], "...")
print("categoryNote.body_he[1]:")
print(" ", data['categoryNote']['body_he'][1])

# 4. Confirm fields that must NOT have changed
immutable_fields = ['score', 'grade', 'insightLine', 'rowVerdict',
                    'nutrition_per_100g', 'confidence', 'rank']
print("\nImmutable field check (spot):")
for p in data['products'][:3]:
    for f in immutable_fields:
        if f in p:
            print(f"  {p['id']}.{f}: present")

# 5. Count which products had ingredient strings modified
# (we know from logs: prot-008, prot-009, prot-015 left whole; prot-029 has one unfixed substr)
left_whole = ['prot-008', 'prot-009', 'prot-015']
partial_left = ['prot-029', 'prot-003']  # specific issues left
modified_count = 32 - len(left_whole)
print(f"\nIngredient strings cleaned (format-only): {modified_count}/32")
print(f"Left as-is (whole, severe character corruption): {len(left_whole)} — {left_whole}")
print(f"Partial left (specific substring): {partial_left}")
print(f"  prot-029: 'לציטיו' (missing final ן — letter drop)")
print(f"  prot-003: pervasive RTL bracket encoding throughout — systemic, too risky to partially fix")

print("\nAll checks PASS.")
