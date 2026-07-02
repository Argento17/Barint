import hashlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
path = r"C:\Bari\02_products\milk_and_alternatives\task378_almond_milk_rescore.json"
content = open(path, "rb").read()
sha256 = hashlib.sha256(content).hexdigest()
print(f"sha256: {sha256}")
