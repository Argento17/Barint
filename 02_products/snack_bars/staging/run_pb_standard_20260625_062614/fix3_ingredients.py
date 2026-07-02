"""
TASK-399 FIX B pass 3: Fix remaining residuals.

Remaining issues:
1. prot-030: E476( → E476) — reversed closing bracket after E476
2. prot-022: (1442) → (E1442) — missing E prefix in E-code
   Note: prot-003 has pervasive RTL bracket system )...( throughout —
   this is a systemic encoding and too risky to partially fix; leave as-is.
"""
import json, re, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')

SRC = r"C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\protein_bars_frontend_v2_candidate.json"

with open(SRC, encoding='utf-8') as f:
    raw = f.read()
data = json.loads(raw)

before_scores = {p['id']: (p['score'], p['grade']) for p in data['products']}

changes_made = []

for p in data['products']:
    pid = p['id']
    ingr = p['expansion'].get('ingredients', '')
    original = ingr

    if pid == 'prot-030':
        # Fix: E476( → E476) — the closing bracket is reversed
        # Context: 'לציטין לפתית, E476(,' → 'לציטין לפתית, E476),'
        new = ingr.replace('E476(', 'E476)')
        if new != ingr:
            p['expansion']['ingredients'] = new
            changes_made.append(f"prot-030: E476( → E476)")
            ingr = new

    if pid == 'prot-022':
        # Fix: (1442) → (E1442) — missing E prefix for E-code
        # Context: 'מסמיך (1442)' — confirmed from audit
        new = re.sub(r'\(1442\)', '(E1442)', ingr)
        if new != ingr:
            p['expansion']['ingredients'] = new
            changes_made.append(f"prot-022: (1442) → (E1442)")
            ingr = new

# ─────────────────────────────────────────────────────────────────────────────
# Verify scores unchanged
# ─────────────────────────────────────────────────────────────────────────────
after_scores = {p['id']: (p['score'], p['grade']) for p in data['products']}
assert before_scores == after_scores, "SCORE CHANGED — ABORT"

# Write
out_str = json.dumps(data, ensure_ascii=False, indent=2)
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(out_str)

sha = hashlib.sha256(out_str.encode('utf-8')).hexdigest()
print(f"SHA256: {sha}")
print(f"Size: {len(out_str)} bytes")
print(f"Changes made: {changes_made}")
print("Scores/grades unchanged: PASS")

# Final residual scan
print("\n=== FINAL RESIDUAL SCAN ===")
for p in data['products']:
    pid = p['id']
    ingr = p['expansion'].get('ingredients', '')
    issues = []

    if re.search(r'[א-ת]n[א-ת]', ingr): issues.append('stray n between Hebrew chars')
    if re.search(r',n[א-ת]', ingr): issues.append(',n before Hebrew')
    if re.search(r'\bn[א-ת]', ingr): issues.append('leading stray n before Hebrew')
    if re.search(r'\b\d{3}E\b', ingr) or re.search(r'\b\d{4}E\b', ingr):
        issues.append('reversed E-code NNNe')
    # Check specifically for E476( (not E476))
    if 'E476(' in ingr: issues.append('E476( still present')

    if issues:
        print(f"  {pid}: {issues}")

# Also report products left as-is
print("\n=== PRODUCTS LEFT AS-IS (whole) ===")
for pid in ['prot-008', 'prot-009', 'prot-015']:
    for p in data['products']:
        if p['id'] == pid:
            print(f"  {pid} (barcode {p['barcode']}): left as-is — severe character-level corruption")

print("\n=== SPECIFIC SUBSTRINGS LEFT ===")
print("  prot-029 (7290019401544): 'לציטיו' — missing final ן from לציטין — letter drop, not format artifact")
print("  prot-003 (7290121166850): pervasive RTL bracket system )...( throughout — systemic encoding, too risky to partially fix")

print("\nDone.")
