import json
import re
import sys
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

# -----------------------------------------------------------------------
# Load both files
# -----------------------------------------------------------------------
with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', encoding='utf-8') as f:
    v2 = json.load(f)

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json', encoding='utf-8') as f:
    v1 = json.load(f)

products_v2 = v2['products']
products_v1 = v1['products']

# -----------------------------------------------------------------------
# Build lookup maps
# -----------------------------------------------------------------------
v1_by_barcode = {str(p.get('barcode','')): p for p in products_v1}
v2_by_barcode = {str(p.get('barcode','')): p for p in products_v2}

# -----------------------------------------------------------------------
# Test 1: Total count = 122
# -----------------------------------------------------------------------
print('=== TEST 1: Product count ===')
count = len(products_v2)
print(f'Count: {count}  {"PASS" if count == 122 else "FAIL - expected 122"}')

# -----------------------------------------------------------------------
# Test 2: Protected 56 byte-identical to v1
# -----------------------------------------------------------------------
print('\n=== TEST 2: Protected 56 byte-identical to v1 ===')

# The 66 new products are those NOT in v1 by barcode
v1_barcodes = set(v1_by_barcode.keys())
# Protected = those in both v1 and v2 (the 56 from v1 that didn't change)
# Actually the task says "protected 56 from cookies_coffee_frontend_v1.json"
# Let's identify: products in v2 that exist in v1

protected_fail = []
protected_count = 0
new_count = 0

for p2 in products_v2:
    bc = str(p2.get('barcode',''))
    if bc in v1_by_barcode:
        protected_count += 1
        p1 = v1_by_barcode[bc]
        # Check rowVerdict and insightLine are identical
        for field in ['rowVerdict', 'insightLine']:
            if p2.get(field) != p1.get(field):
                protected_fail.append(f'  [{bc}] {field} CHANGED')
    else:
        new_count += 1

print(f'Protected products (in v1): {protected_count}')
print(f'New products (not in v1): {new_count}')
if protected_fail:
    print('FAIL - protected products changed:')
    for f in protected_fail:
        print(f)
else:
    print('PASS - all protected products byte-identical in rowVerdict + insightLine')

# -----------------------------------------------------------------------
# Test 3: Sweep all 66 new products for Hebrew number-word + gram patterns
# -----------------------------------------------------------------------
print('\n=== TEST 3: No Hebrew number-word + gram pattern in 66 new verdicts ===')

# Hebrew number words (ordinal/cardinal that could precede gram amounts)
SPELLED_GRAM_PATTERN = re.compile(
    r'(אחד|שניים|שלושה|שלוש|ארבעה|ארבע|חמישה|חמש|שישה|שש|שבעה|שבע|'
    r'שמונה|תשעה|תשע|עשרה|עשר|אחד עשר|שניים עשר|שלושה עשר|ארבעה עשר|'
    r'חמישה עשר|שישה עשר|שבעה עשר|שמונה עשר|תשעה עשר|'
    r'עשרים|שלושים|ארבעים|חמישים|ששים|שבעים|שמונים|תשעים|מאה|מאתיים)'
    r'[^.]*?גרם'
)

new_products = [p for p in products_v2 if str(p.get('barcode','')) not in v1_barcodes]
print(f'New products count: {len(new_products)}')

spelled_gram_fails = []
for p in new_products:
    bc = str(p.get('barcode',''))
    for field in ['rowVerdict', 'insightLine']:
        text = p.get(field, '')
        m = SPELLED_GRAM_PATTERN.search(text)
        if m:
            spelled_gram_fails.append(f'  [{bc}] {field}: ...{m.group()}...')

if spelled_gram_fails:
    print('FAIL - spelled gram patterns found:')
    for f in spelled_gram_fails:
        print(f)
else:
    print('PASS - zero spelled number-word + gram patterns')

# -----------------------------------------------------------------------
# Test 4: Per field <= 1 unit-quantity (digit + unit) across all 66 new
# -----------------------------------------------------------------------
print('\n=== TEST 4: Per field <= 1 unit-quantity (digit + unit) in new products ===')

# A "unit quantity" = digit(s) + optional space + unit (גרם, מ"ג, %, קלוריות)
UNIT_QTY_PATTERN = re.compile(r'\d+\s*(גרם|מ"ג|%|קלוריות|kcal|קק"ל)')

multi_qty_fails = []
for p in new_products:
    bc = str(p.get('barcode',''))
    for field in ['rowVerdict', 'insightLine']:
        text = p.get(field, '')
        matches = UNIT_QTY_PATTERN.findall(text)
        # Count distinct occurrences
        all_matches = UNIT_QTY_PATTERN.finditer(text)
        count_matches = sum(1 for _ in UNIT_QTY_PATTERN.finditer(text))
        if count_matches > 1:
            multi_qty_fails.append(f'  [{bc}] {field}: {count_matches} quantities found in: {text[:100]}')

if multi_qty_fails:
    print(f'FAIL - {len(multi_qty_fails)} fields with >1 unit-quantity:')
    for f in multi_qty_fails:
        print(f)
else:
    print('PASS - all fields have <= 1 unit-quantity')

# -----------------------------------------------------------------------
# Test 5: Zero E-number codes across all 66 new verdicts
# -----------------------------------------------------------------------
print('\n=== TEST 5: Zero E-number codes (E\\d{3}) in 66 new verdicts ===')

E_CODE_PATTERN = re.compile(r'E\d{3}')

e_code_fails = []
for p in new_products:
    bc = str(p.get('barcode',''))
    for field in ['rowVerdict', 'insightLine']:
        text = p.get(field, '')
        m = E_CODE_PATTERN.search(text)
        if m:
            e_code_fails.append(f'  [{bc}] {field}: found {m.group()} in: {text[:100]}')

if e_code_fails:
    print('FAIL - E-number codes found:')
    for f in e_code_fails:
        print(f)
else:
    print('PASS - zero E-number codes')

# -----------------------------------------------------------------------
# Test 6: JSON is valid and parseable (already loaded above)
# -----------------------------------------------------------------------
print('\n=== TEST 6: JSON valid ===')
print('PASS - JSON loaded without error')

# -----------------------------------------------------------------------
# Print all touched verdicts
# -----------------------------------------------------------------------
print('\n=== TOUCHED VERDICTS (all 25 changed products) ===')

touched_barcodes = {
    '7290122781359',  # C3 item 2
    '7290019870470',  # C3 item 5
    '8710502139017',  # C3 item 8
    '8710502279010',  # C3 item 9
    '7290112961754',  # C3 item 10
    '7290119040568', '7290119040612', '7290119040513', '7290119040667',
    '8710502405204', '7622300489427', '46214731552', '7296073529026',
    '8000500366073', '7622210137234', '7290106656727', '7290019870463',
    '7622300356767', '7622300489434', '7622201401900', '8710502064814',
    '7622210453327',
}

for p in products_v2:
    bc = str(p.get('barcode',''))
    if bc in touched_barcodes:
        name = p.get('name','')[:50]
        print(f'\n[{bc}] {name}')
        print(f'  rowVerdict: {p.get("rowVerdict","")}')
        print(f'  insightLine: {p.get("insightLine","")}')

# -----------------------------------------------------------------------
# SHA256 of the output file
# -----------------------------------------------------------------------
print('\n=== FILE HASH ===')
with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'rb') as f:
    sha = hashlib.sha256(f.read()).hexdigest()
print(f'SHA256: {sha}')
