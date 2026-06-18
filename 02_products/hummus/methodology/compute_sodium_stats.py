import json, os, glob, statistics

bsip1_dir = r"C:\Bari\02_products\hummus\canonical_bsip1"
files = glob.glob(os.path.join(bsip1_dir, "bsip1_*.json"))

IN_SCOPE = {"hummus_spread", "hummus_and_savory_dips"}

products = []
excluded = []
missing_sodium = []

for f in sorted(files):
    with open(f, encoding="utf-8") as fh:
        d = json.load(fh)
    cat = d.get("bsip0_source", {}).get("product_category", "MISSING")
    barcode = d.get("barcode", "N/A")
    name = d.get("canonical_name_he", "")
    sodium = d.get("normalized_nutrition_per_100g", {}).get("sodium_mg")

    if cat not in IN_SCOPE:
        excluded.append({"barcode": barcode, "name": name, "cat": cat})
        continue

    if sodium is None:
        missing_sodium.append({"barcode": barcode, "name": name})
        continue

    products.append({"barcode": barcode, "name": name, "sodium_mg": sodium, "cat": cat})

print("n_total_corpus: 69")
print("n_excluded (eggplant+matbucha): %d" % len(excluded))
print("n_in_scope: %d" % (len(products) + len(missing_sodium)))
print("n_missing_sodium: %d" % len(missing_sodium))
print("n_with_valid_sodium: %d" % len(products))
print()

if missing_sodium:
    print("Missing sodium:")
    for p in missing_sodium:
        print("  %s | %s" % (p["barcode"], p["name"]))
    print()

sodiums = sorted([p["sodium_mg"] for p in products])
n = len(sodiums)

mean_val = statistics.mean(sodiums)
stdev_val = statistics.stdev(sodiums)


def percentile(data, pct):
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * pct / 100
    lo = int(k)
    hi = lo + 1
    if hi >= len(sorted_data):
        return float(sorted_data[-1])
    frac = k - lo
    return sorted_data[lo] + frac * (sorted_data[hi] - sorted_data[lo])


q1 = percentile(sodiums, 25)
med = percentile(sodiums, 50)
q3 = percentile(sodiums, 75)
p80 = percentile(sodiums, 80)
p85 = percentile(sodiums, 85)
iqr = q3 - q1
deviations = sorted([abs(s - med) for s in sodiums])
mad = percentile(deviations, 50)
robust_scale = max(iqr / 1.349, 1.4826 * mad, 3.0)

print("=== DISTRIBUTION STATS (n=%d) ===" % n)
print("mean:          %.2f" % mean_val)
print("stdev:         %.2f" % stdev_val)
print("min:           %.2f" % min(sodiums))
print("Q1 (25th):     %.2f" % q1)
print("median (50th): %.2f" % med)
print("Q3 (75th):     %.2f" % q3)
print("P80:           %.2f" % p80)
print("P85:           %.2f" % p85)
print("max:           %.2f" % max(sodiums))
print("IQR:           %.2f" % iqr)
print("MAD:           %.2f" % mad)
print("robust_scale:  %.2f" % robust_scale)
print("|Q3 - median|: %.2f" % abs(q3 - med))
if abs(q3 - med) <= 5:
    print("FLAG: Q3 within 5mg of median -- escalate to Nutrition Agent (use P85)")
    floor_rec = "P85=%.1fmg (Q3=%.1fmg within 5mg of median -- Nutrition escalation)" % (p85, q3)
else:
    floor_rec = "Q3=%.1fmg" % q3
print("floor_threshold_recommendation: %s" % floor_rec)
print()
print("=== TOP 5 HIGHEST SODIUM ===")
top5 = sorted(products, key=lambda x: x["sodium_mg"], reverse=True)[:5]
for p in top5:
    print("  %s | %s | %.1f mg" % (p["barcode"], p["name"], p["sodium_mg"]))
print()
print("=== TOP 5 LOWEST SODIUM ===")
bot5 = sorted(products, key=lambda x: x["sodium_mg"])[:5]
for p in bot5:
    print("  %s | %s | %.1f mg" % (p["barcode"], p["name"], p["sodium_mg"]))
print()

# Histogram by 25mg buckets
print("=== HISTOGRAM (25mg buckets) ===")
min_s = int(min(sodiums) // 25) * 25
max_s = (int(max(sodiums) // 25) + 1) * 25
bucket = min_s
while bucket < max_s:
    count = sum(1 for s in sodiums if bucket <= s < bucket + 25)
    bar = "#" * count
    print("  %4d-%4d: %s (%d)" % (bucket, bucket + 25, bar, count))
    bucket += 25

# Also print all sodium values sorted for verification
print()
print("=== ALL SODIUM VALUES (sorted) ===")
for i, s in enumerate(sodiums):
    print("  [%02d] %.1f" % (i + 1, s))
