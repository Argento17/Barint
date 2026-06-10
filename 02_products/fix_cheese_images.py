# -*- coding: utf-8 -*-
"""
Inject barcode + imageUrl into hard_cheeses_frontend_v2.json.
The cheese frontend JSON was built without barcodes; match by canonical name
from discovery.json files in the scrape directory.
"""
import sys
import json
import pathlib
import shutil

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT         = pathlib.Path(r"C:\Bari")
CHEESE_JSON  = ROOT / "02_products" / "hard_cheeses" / "hard_cheeses_frontend_v2.json"
SCRAPE_DIR   = ROOT / "02_products" / "hard_cheeses" / "yohananof_scrape"
WEB_OUT      = ROOT / "bari-web" / "src" / "data" / "comparisons" / "hard_cheeses_frontend_v2.json"

YOHANANOF_BARCODES = {
    "7290000057118", "7290004137311", "7290102394463", "7290110320867",
    "7290004122195", "7290014763395", "7290004122683", "7290014760912",
    "7290004125776", "7290102396672", "7290004122348", "7290110320850",
    "7290110324872", "7290000057088", "7290102394845", "7290004122270",
    "7290110323301", "7290102397204", "7290014455252", "3073781199918",
    "7290117265888", "7290117265918", "7290108502725", "7290108501346",
    "7290116931524", "7290108503999", "7290019635192", "7290017065434",
    "7290102302864", "8711528211138",
}


def build_name_to_image_map(scrape_dir: pathlib.Path) -> dict:
    """Return {name: (barcode, image_url)} only for yohananof barcodes."""
    name_map = {}
    for d in scrape_dir.iterdir():
        if not d.is_dir():
            continue
        dj = d / "discovery.json"
        if not dj.exists():
            continue
        try:
            data = json.loads(dj.read_text(encoding="utf-8"))
            barcode = data.get("barcode") or d.name
            if barcode not in YOHANANOF_BARCODES:
                continue
            name = (data.get("name") or "").strip()
            url = (data.get("image") or {}).get("source_image_url")
            if name:
                name_map[name] = (barcode, url)
        except Exception as e:
            print(f"  WARN: {dj}: {e}")
    return name_map


def normalize(s: str) -> str:
    """Strip trailing/leading whitespace and trailing period for fuzzy match."""
    return s.strip().rstrip(".")


def main():
    name_map = build_name_to_image_map(SCRAPE_DIR)
    print(f"Loaded {len(name_map)} name→(barcode, url) entries from scrape dir")

    doc = json.loads(CHEESE_JSON.read_text(encoding="utf-8"))
    products = doc.get("products", [])

    matched = 0
    unmatched = []
    images_set = 0

    for p in products:
        pid  = p.get("id", "?")
        name = (p.get("name") or "").strip()

        # Try exact match first
        entry = name_map.get(name)
        if entry is None:
            # Try normalized (strip trailing period)
            norm_name = normalize(name)
            for k, v in name_map.items():
                if normalize(k) == norm_name:
                    entry = v
                    break

        if entry:
            barcode, url = entry
            p["barcode"] = barcode
            p["imageUrl"] = url
            matched += 1
            if url:
                images_set += 1
            print(f"  [{pid}] MATCHED barcode={barcode}  imageUrl={'SET' if url else 'null'}")
        else:
            p["barcode"] = None
            p["imageUrl"] = None
            unmatched.append((pid, name))
            print(f"  [{pid}] NO MATCH: '{name}'")

    print(f"\nMatched: {matched}/{len(products)}")
    print(f"Images set: {images_set}")
    if unmatched:
        print(f"Unmatched ({len(unmatched)}):")
        for uid, uname in unmatched:
            print(f"  {uid}: '{uname}'")

    CHEESE_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWritten:  {CHEESE_JSON}")
    shutil.copy2(CHEESE_JSON, WEB_OUT)
    print(f"Deployed: {WEB_OUT}")


if __name__ == "__main__":
    main()
