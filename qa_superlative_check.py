import json, io, sys

out = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('C:/Bari/bari-web/src/data/comparisons/protein_bars_frontend_v1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

# Build lookup
fields = {}
for p in products:
    pid = p['id']
    n = p.get('nutrition_per_100g', {})
    fields[pid] = {
        'name': p['name'],
        'score': p['score'],
        'protein': n.get('protein_g'),
        'sugar': n.get('sugars_g'),
        'fat': n.get('fat_g'),
        'sat_fat': n.get('fat_saturated_g'),
        'sodium': n.get('sodium_mg'),
        'fiber': n.get('dietary_fiber_g'),
        'kcal': n.get('energy_kcal'),
    }

protein_vals = {pid: v['protein'] for pid, v in fields.items() if v['protein'] is not None}
fiber_vals = {pid: v['fiber'] for pid, v in fields.items() if v['fiber'] is not None and v['fiber'] > 0}
sugar_vals = {pid: v['sugar'] for pid, v in fields.items() if v['sugar'] is not None}
sodium_vals = {pid: v['sodium'] for pid, v in fields.items() if v['sodium'] is not None}
sat_fat_vals = {pid: v['sat_fat'] for pid, v in fields.items() if v['sat_fat'] is not None}
kcal_vals = {pid: v['kcal'] for pid, v in fields.items() if v['kcal'] is not None}
fat_vals = {pid: v['fat'] for pid, v in fields.items() if v['fat'] is not None}

max_protein_pid = max(protein_vals, key=protein_vals.get)
max_fiber_pid = max(fiber_vals, key=fiber_vals.get)
max_sugar_pid = max(sugar_vals, key=sugar_vals.get)
max_sodium_pid = max(sodium_vals, key=sodium_vals.get)
max_sat_fat_pid = max(sat_fat_vals, key=sat_fat_vals.get)
max_kcal_pid = max(kcal_vals, key=kcal_vals.get)
max_fat_pid = max(fat_vals, key=fat_vals.get)
min_sodium_pid = min(sodium_vals, key=sodium_vals.get)
min_sugar_pid = min(sugar_vals, key=sugar_vals.get)

out.write("TRUE SUPERLATIVES:\n")
out.write("Max protein: " + max_protein_pid + " " + str(protein_vals[max_protein_pid]) + "g\n")
out.write("Max fiber: " + max_fiber_pid + " " + str(fiber_vals[max_fiber_pid]) + "g\n")
out.write("Max sugar: " + max_sugar_pid + " " + str(sugar_vals[max_sugar_pid]) + "g\n")
out.write("Max sodium: " + max_sodium_pid + " " + str(sodium_vals[max_sodium_pid]) + "mg\n")
out.write("Max sat_fat: " + max_sat_fat_pid + " " + str(sat_fat_vals[max_sat_fat_pid]) + "g\n")
out.write("Max kcal: " + max_kcal_pid + " " + str(kcal_vals[max_kcal_pid]) + " kcal\n")
out.write("Max fat: " + max_fat_pid + " " + str(fat_vals[max_fat_pid]) + "g\n")
out.write("Min sodium: " + min_sodium_pid + " " + str(sodium_vals[min_sodium_pid]) + "mg\n")
out.write("Min sugar: " + min_sugar_pid + " " + str(sugar_vals[min_sugar_pid]) + "g\n")
out.write("\n")

SUPERLATIVES = [
    "הגבוה בקבוצה",
    "הגבוהים בקבוצה",
    "הגבוה במדף",
    "הגבוהים במדף",
    "הצפוף ביותר",
    "הכי הרבה",
    "הכי גבוה",
    "הכי נמוך",
    "הנמוך בקבוצה",
    "המלוחים בקבוצה",
    "המלוחים במדף",
    "ביותר בקבוצה",
    "ביותר במדף",
    "אף חטיף אחר כאן",
    "הכי מתוק",
    "הכי מלוח",
]

out.write("=== SUPERLATIVE CLAIMS IN COPY ===\n")
findings = []
for p in products:
    pid = p['id']
    all_copy = []
    all_copy.append(("insightLine", p.get("insightLine", "")))
    all_copy.append(("rowVerdict", p.get("rowVerdict", "")))
    exp = p.get("expansion", {})
    all_copy.append(("comparisonContext", exp.get("comparisonContext", "")))
    for i, ps_item in enumerate(exp.get("positiveSignals", [])):
        all_copy.append(("positiveSignals[" + str(i) + "]", ps_item))
    for i, lf in enumerate(exp.get("limitingFactors", [])):
        all_copy.append(("limitingFactors[" + str(i) + "]", lf.get("text", "")))

    for field, text in all_copy:
        for sup in SUPERLATIVES:
            if sup in text:
                line = pid + " | " + field + " | " + text[:150]
                findings.append(line)

for f in findings:
    out.write(f + "\n")

out.write("\nTotal superlative claims: " + str(len(findings)) + "\n")
out.flush()
