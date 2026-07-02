import json, io, sys

out = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('C:/Bari/bari-web/src/data/comparisons/protein_bars_frontend_v1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

meta = data['_meta']
out.write("_meta.copy_status: " + str(meta.get('copy_status')) + "\n")
out.write("_meta.version: " + str(meta.get('version')) + "\n")
out.write("_meta.product_count: " + str(meta.get('product_count')) + "\n")

products = data['products']
pid_map = {p['id']: p for p in products}

# prot-010 full copy
p010 = pid_map['prot-010']
out.write("\n--- prot-010 ---\n")
out.write("insightLine: " + p010.get('insightLine', '') + "\n")
out.write("rowVerdict: " + p010.get('rowVerdict', '') + "\n")
lf = p010.get('expansion', {}).get('limitingFactors', [])
for l in lf:
    out.write("LF: " + l.get('text', '') + " mag=" + str(l.get('magnitude')) + "\n")
out.write("CC: " + p010.get('expansion', {}).get('comparisonContext', '') + "\n")

# prot-001 positive signals
p001 = pid_map['prot-001']
out.write("\n--- prot-001 positiveSignals ---\n")
for s in p001.get('expansion', {}).get('positiveSignals', []):
    out.write(s + "\n")

# Sat fat reality check
out.write("\n--- SAT FAT RANKING ---\n")
sat_fats = [(pid, p.get('nutrition_per_100g', {}).get('fat_saturated_g')) for pid, p in pid_map.items()]
sat_fats_sorted = sorted(sat_fats, key=lambda x: -(x[1] or 0))
for pid, val in sat_fats_sorted:
    out.write(pid + ": " + str(val) + "g\n")

# prot-004 rowVerdict
p004 = pid_map['prot-004']
out.write("\n--- prot-004 rowVerdict ---\n")
out.write(p004.get('rowVerdict', '') + "\n")

# prot-003 insightLine
p003 = pid_map['prot-003']
out.write("\n--- prot-003 ---\n")
out.write("insightLine: " + p003.get('insightLine', '') + "\n")
out.write("rowVerdict: " + p003.get('rowVerdict', '') + "\n")

# prot-002 rowVerdict
p002 = pid_map['prot-002']
out.write("\n--- prot-002 rowVerdict ---\n")
out.write(p002.get('rowVerdict', '') + "\n")

# Check "copy_status" field - still says PARTIAL_PENDING_COPY
out.write("\nNOTE: _meta.copy_status is still 'PARTIAL_PENDING_COPY' - should be updated to reflect completed rewrite\n")

out.flush()
