"""
BSIP0 — Milk Candidate Approval
Reads candidate_review.csv (edit approved_for_scrape column to YES/NO),
writes approved_candidates.json for the scraper.
"""
from pathlib import Path
import csv
import json
import re
import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
RETAILER_DIR = BASE_DIR / "outputs" / "yohananof_milk"


def clean(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def repair_barcode(row):
    barcode = clean(row.get("barcode"))
    if barcode and "E+" not in barcode.upper() and "." not in barcode:
        return barcode
    combined = f"{row.get('image_url_raw', '')} {row.get('card_text', '')} {row.get('image_alt', '')}"
    match = re.search(r"(729\d{10}|\d{13}|\d{12})", combined)
    return match.group(1) if match else ""


def main():
    csv_path = RETAILER_DIR / "candidate_review.csv"
    output_path = RETAILER_DIR / "approved_candidates.json"

    if not csv_path.exists():
        raise FileNotFoundError(f"candidate_review.csv not found: {csv_path}")

    approved = []
    skipped = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            flag = clean(row.get("approved_for_scrape")).upper()
            if flag != "YES":
                continue
            barcode = repair_barcode(row)
            name = clean(row.get("name"))
            if not barcode:
                skipped.append(name)
                print(f"Skipping (no barcode): {name}")
                continue
            approved.append({
                "barcode": barcode,
                "name": name,
                "brand": clean(row.get("brand")),
                "query": clean(row.get("query")),
                "decision_status": clean(row.get("suggested_decision")),
                "decision_reason": clean(row.get("decision_reason")),
                "card_text": clean(row.get("card_text")),
                "image_alt": clean(row.get("image_alt")),
                "image_url_raw": clean(row.get("image_url_raw")),
            })

    output_path.write_text(json.dumps(approved, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nApproved: {len(approved)}")
    print(f"Skipped (no barcode): {len(skipped)}")
    print(f"Saved: {output_path}")
    print("Next: python 03_scrape_milk.py")


if __name__ == "__main__":
    main()
