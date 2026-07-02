"""
TASK-399 FIX B pass 2: Address residuals from first pass.
"""
import json, re, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')

SRC = r"C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\protein_bars_frontend_v2_candidate.json"

with open(SRC, encoding='utf-8') as f:
    raw = f.read()
data = json.loads(raw)

before_scores = {p['id']: (p['score'], p['grade']) for p in data['products']}

changes_made = []

# ─────────────────────────────────────────────────────────────────────────────
# Inspect prot-003 residual: 'N%( reversed pattern'
# ─────────────────────────────────────────────────────────────────────────────
for p in data['products']:
    if p['id'] == 'prot-003':
        ingr = p['expansion']['ingredients']
        print("prot-003 full ingredients:")
        print(ingr)
        print()
        # Find all % patterns
        for m in re.finditer(r'[%()]{1,3}\d+[%()]{1,3}', ingr):
            print(f"  % context: '{ingr[max(0,m.start()-5):m.end()+5]}'")

# ─────────────────────────────────────────────────────────────────────────────
# Inspect מסמיך hits — check if it's the split form or the correctly-spelled word
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- מסמיך occurrences (checking for split vs whole) ---")
for p in data['products']:
    ingr = p['expansion'].get('ingredients', '')
    for m in re.finditer(r'מס.?מיך', ingr):
        print(f"  {p['id']}: '{ingr[max(0,m.start()-10):m.end()+10]}'")

# ─────────────────────────────────────────────────────────────────────────────
# Inspect prot-030 E476( residual
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- prot-030 E476 context ---")
for p in data['products']:
    if p['id'] == 'prot-030':
        ingr = p['expansion']['ingredients']
        for m in re.finditer(r'E\d+.', ingr):
            print(f"  '{ingr[max(0,m.start()-10):m.end()+10]}'")
