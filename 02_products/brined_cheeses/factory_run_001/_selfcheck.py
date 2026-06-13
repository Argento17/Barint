import json, sys, io, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('C:/Bari/02_products/brined_cheeses/factory_run_001/corpus_filter.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

prods = d['products']
in_s = sum(1 for p in prods if p['decision'] == 'IN_SCORED')
trans = sum(1 for p in prods if p['decision'] == 'TRANSPARENCY_NULL')
oos = sum(1 for p in prods if p['decision'] == 'OUT_OF_SCOPE')

print(f'Products array length: {len(prods)}')
print(f'IN_SCORED={in_s} TRANSPARENCY_NULL={trans} OUT_OF_SCOPE={oos} SUM={in_s+trans+oos}')
print(f'summary block matches: {d["summary"]["in_scored"]==in_s and d["summary"]["transparency_null"]==trans and d["summary"]["out_of_scope"]==oos}')
print(f'corpus_size_check: {d["corpus_size_check"]}')
print(f'off_used: {d["off_used"]}')

barcodes = [p['barcode'] for p in prods]
unique = set(barcodes)
print(f'Barcodes: total={len(barcodes)} unique={len(unique)} duplicates={len(barcodes)-len(unique)}')

# Verify every product has decision + reason
missing = [p['barcode'] for p in prods if not p.get('decision') or not p.get('reason')]
print(f'Products missing decision/reason: {len(missing)}')

# SHA256
with open('C:/Bari/02_products/brined_cheeses/factory_run_001/corpus_filter.json', 'rb') as f:
    sha = hashlib.sha256(f.read()).hexdigest()
print(f'SHA256: {sha}')
print('SELF-CHECK: PASS' if len(prods)==94 and in_s+trans+oos==94 and len(unique)==len(barcodes) and len(missing)==0 else 'SELF-CHECK: FAIL')
