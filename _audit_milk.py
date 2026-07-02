import json, subprocess
raw = subprocess.check_output(["git","show","origin/master:bari-web/src/data/comparisons/milk_frontend_v1.json"])
d = json.loads(raw)
hidden = shown = no_brand = 0
for p in d["products"]:
    b = (p.get("brand") or "").strip()
    n = p.get("name","")
    if not b:
        no_brand += 1
        continue
    if b.lower() in n.lower():
        hidden += 1
        print("HIDDEN", p.get("barcode"), "|", n, "| brand:", b)
    else:
        shown += 1
print("---")
print("shown separate:", shown, "hidden (brand in name):", hidden, "no brand field:", no_brand)
