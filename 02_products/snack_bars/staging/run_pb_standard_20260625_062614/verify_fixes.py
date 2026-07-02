import json, re, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\protein_bars_frontend_v2_candidate.json', encoding='utf-8') as f:
    raw = f.read()
data = json.loads(raw)

sha = hashlib.sha256(raw.encode('utf-8')).hexdigest()
print(f"SHA256: {sha}")
print(f"File size: {len(raw)} bytes")

# Check FIX A
print("\n=== FIX A: categoryNote.body_he[1] ===")
print(data['categoryNote']['body_he'][1])

# Check scores
print("\n=== SCORES/GRADES (must be unchanged) ===")
for p in data['products']:
    print(f"  {p['id']}: {p['score']} / {p['grade']}")

# Residual scan
print("\n=== RESIDUAL ARTIFACT SCAN ===")
residuals = []
for p in data['products']:
    pid = p['id']
    ingr = p['expansion'].get('ingredients', '')
    issues = []

    if re.search(r'\)%\d', ingr): issues.append('REVERSED %)N pattern')
    if re.search(r'\d%\(', ingr): issues.append('N%( reversed pattern')
    if re.search(r'[א-ת]n[א-ת]', ingr): issues.append('stray n between Hebrew chars')
    if re.search(r',n[א-ת]', ingr): issues.append(',n before Hebrew')
    if re.search(r'\bn[א-ת]', ingr): issues.append('leading stray n before Hebrew')
    if re.search(r'\b\d{3}E\b', ingr) or re.search(r'\b\d{4}E\b', ingr):
        issues.append('reversed E-code NNNe present')

    known_splits = [
        'גבינ ה', 'ציטרי ת', 'ח מניות', 'גליצרו ל', 'סיבי ם',
        'הלח ה', 'לציטי ן', 'קו קוס', 'ח לב', 'טב עיים',
        'מינימו ם', 'שוקול ד', 'מסיס ים', 'סי בים', 'מסמיך',
        'ממ תיק', 'חי טה', 'פולידקסטר וז', 'ש מן', 'מלטיטו ל',
        'מלטיט ול', 'אסט ר', 'מק ריש', 'מת חלב', 'ורי ח',
        'מ ים', 'מי ם', 'ממתי ק', 'ונילי ן', 'חומ ציות',
        'גלוק וזה', 'ר זה', 'צמ חיים', 'מר וכז', 'מרו כז',
        'מאכ ל', 'מס מיך', 'חו מצות', 'חומ ר',
    ]
    for label in known_splits:
        if label in ingr:
            issues.append(f'mid-word split still: {label}')

    if issues:
        residuals.append((pid, issues))
        print(f"  {pid}: {issues}")

if not residuals:
    print("  No residual artifacts found in fixable products.")

# Spot-check selected products
print("\n=== SPOT CHECK — key products (first 300 chars of ingredients) ===")
check_pids = ['prot-001', 'prot-003', 'prot-004', 'prot-005', 'prot-007',
              'prot-010', 'prot-020', 'prot-030', 'prot-031', 'prot-032']
for p in data['products']:
    if p['id'] in check_pids:
        ingr = p['expansion']['ingredients']
        print(f"\n{p['id']} ({p['barcode']}):")
        print(ingr[:300])

# Count cleaned vs left
print("\n=== COUNTS ===")
left_whole = ['prot-008', 'prot-009', 'prot-015']  # whole product left
print(f"Whole products left as-is: {len(left_whole)} => {left_whole}")
print(f"Specific substrings left: prot-029 'לציטיו' (missing ן — letter drop)")
cleaned = 32 - len(left_whole)
print(f"Products with ingredient strings touched: up to {cleaned}/32 (some may have been already clean)")
print("Done.")
