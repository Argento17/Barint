import json, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
path = r"C:\bari\bari-web\src\data\comparisons\milk_frontend_v1.json"
content = open(path, "rb").read()
sha256 = hashlib.sha256(content).hexdigest()
print(f"sha256: {sha256}")
data = json.loads(content)
print(f"product_count: {len(data['products'])}")
print(f"grade_dist: {data['_meta']['grade_distribution']}")
