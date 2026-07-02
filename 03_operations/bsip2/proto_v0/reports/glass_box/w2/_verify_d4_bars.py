import json, hashlib, pathlib

ROOT = pathlib.Path(r"C:\Bari")

files = {
    "snacks_frontend_v5.json": ROOT / "bari-web/src/data/comparisons/snacks_frontend_v5.json",
    "protein_bars_frontend_v1.json": ROOT / "bari-web/src/data/comparisons/protein_bars_frontend_v1.json",
}

for label, p in files.items():
    raw = p.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    fe = json.loads(raw)
    total = len(fe["products"])
    with_d4 = sum(1 for pr in fe["products"] if pr.get("d4_additives"))
    zero_d4 = sum(1 for pr in fe["products"] if "d4_additives" in pr and not pr["d4_additives"])
    missing_key = sum(1 for pr in fe["products"] if "d4_additives" not in pr)
    print(f"{label}")
    print(f"  SHA256: {sha}")
    print(f"  total={total}, with_additives={with_d4}, empty_array={zero_d4}, key_missing={missing_key}")
    for pr in fe["products"]:
        if pr.get("d4_additives"):
            enums = [e["e_number"] for e in pr["d4_additives"]]
            pid = pr["id"]
            print(f"  {pid}: {enums}")
    print()
