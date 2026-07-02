import json, hashlib, copy, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent / "src/data/comparisons"

TARGETS = [
    "bread_frontend_v3.json",
    "brined_cheeses_frontend_v2.json",
    "cakes_hard_cookies_frontend_v1.json",
    "chocolate_tablets_frontend_v1.json",
    "granola_frontend_v2.json",
    "juices_frontend_v3.json",
    "snacks_frontend_v5.json",
]

sys.stdout.reconfigure(encoding="utf-8")

def product_key(p):
    return p.get("id") or p.get("barcode")

def stable_sort_key(p, idx):
    return (-p["score"], idx)

def hash_obj_except_rank(obj):
    obj_copy = copy.deepcopy(obj)
    obj_copy.pop("rank", None)
    return hashlib.sha256(
        json.dumps(obj_copy, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()

def sort_file(rel_path):
    path = BASE / rel_path
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data["products"]
    n = len(products)

    old_by_key = {}
    for p in products:
        k = product_key(p)
        old_by_key[k] = copy.deepcopy(p)
        old_by_key[k]["_hash_no_rank"] = hash_obj_except_rank(p)

    enriched = [(p, i) for i, p in enumerate(products)]
    enriched.sort(key=lambda x: stable_sort_key(x[0], x[1]))
    sorted_products = [p for p, _ in enriched]

    for i, p in enumerate(sorted_products):
        p["rank"] = i + 1

    barcodes_before = {product_key(p) for p in products}
    barcodes_after = {product_key(p) for p in sorted_products}
    assert barcodes_before == barcodes_after, f"BARCODE/ID SET CHANGED in {rel_path}"

    new_by_key = {}
    for p in sorted_products:
        k = product_key(p)
        new_by_key[k] = p
        new_by_key[k]["_hash_no_rank"] = hash_obj_except_rank(p)

    changed_fields = False
    for k in old_by_key:
        old_hash = old_by_key[k]["_hash_no_rank"]
        new_hash = new_by_key[k]["_hash_no_rank"]
        if old_hash != new_hash:
            old_without = {kk: vv for kk, vv in old_by_key[k].items() if kk not in ("rank", "_hash_no_rank")}
            new_without = {kk: vv for kk, vv in new_by_key[k].items() if kk not in ("rank", "_hash_no_rank")}
            for key in set(old_without) | set(new_without):
                if old_without.get(key) != new_without.get(key):
                    print(f"  DIFF in {k}: field '{key}' changed: {old_without.get(key)} -> {new_without.get(key)}")
            changed_fields = True

    if changed_fields:
        print(f"  ERROR: non-rank field changed in {rel_path}!")
        sys.exit(1)

    scores = [p["score"] for p in sorted_products]
    is_monotonic = all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1))
    if not is_monotonic:
        print(f"  ERROR: scores not monotonically non-increasing in {rel_path}!")
        print(f"  Scores: {scores}")
        sys.exit(1)

    data["products"] = sorted_products

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\n=== {rel_path} ===")
    print(f"  Products: {n}")
    print(f"  Scores monotonically non-increasing: YES")

    old_rank_map = {}
    for k, p in old_by_key.items():
        r = p.get("rank")
        old_rank_map[k] = r

    new_rank_map = {}
    for p in sorted_products:
        k = product_key(p)
        new_rank_map[k] = p["rank"]

    print(f"  Product set unchanged: YES ({len(barcodes_before)} barcodes/IDs)")
    print(f"  Only rank field changed: YES")

    moved = []
    for k in old_rank_map:
        old_r = old_rank_map[k]
        new_r = new_rank_map[k]
        name = old_by_key[k].get("name", k)
        if old_r is not None and old_r != new_r:
            moved.append((k, name, old_r, new_r))
        elif old_r is None:
            moved.append((k, name, "(missing)", new_r))

    if moved:
        print(f"  Products that moved:")
        for pid, name, old_r, new_r in moved:
            print(f"    {pid} {name}: rank {old_r} -> {new_r}")
    else:
        print(f"  No products moved (already in correct order)")

if __name__ == "__main__":
    for t in TARGETS:
        sort_file(t)
