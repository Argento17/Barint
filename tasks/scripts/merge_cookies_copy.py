"""
P91 merge script: merge corrected copy into cookies_coffee_frontend_v1.json
- Sets insightLine + rowVerdict per barcode
- Injects pageShell into page_copy (hero tagline, prologueSentences, methodologyLines, categoryCaveat)
- Prunes PENDING_COPY scaffolding (consumerTakeaway, consumerExplanation, bariInterpretation, bestUseCases, bottomLine)
- Keeps expansion.nutrition intact
- Does NOT touch score/grade/confidence/imageUrl/nutrition/d4_additives
"""

import json
import hashlib
import sys

COPY_PATH = r"C:\Bari\02_products\cookies_coffee\cookies_coffee_copy_v1.json"
FRONTEND_PATH = r"C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v1.json"
OUTPUT_PATH = r"C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v1.json"


def main():
    with open(COPY_PATH, encoding="utf-8") as f:
        copy_data = json.load(f)

    with open(FRONTEND_PATH, encoding="utf-8") as f:
        frontend = json.load(f)

    # ---- Build barcode → copy lookup ----
    copy_products = copy_data["products"]  # keyed by barcode string
    page_shell = copy_data["pageShell"]

    # ---- 1. Inject pageShell into page_copy ----
    # Structure page_copy to match what page-data.ts will read
    # hero.tagline = page_shell["hero"]
    # prologue.sentences = page_shell["prologueSentences"]  (3 sentences)
    # methodology.lines = page_shell["methodologyLines"]  (3 lines)
    # caveat = structured caveat
    frontend["page_copy"]["hero"]["tagline"] = page_shell["hero"]
    # prologue: 3 sentences (copy has 3, frontend only had 2 slots — expand)
    frontend["page_copy"]["prologue"]["sentences"] = list(page_shell["prologueSentences"])
    # methodology: store lines array
    frontend["page_copy"]["methodology"]["text"] = page_shell["methodologyLines"][0]
    frontend["page_copy"]["methodology"]["sourceNote"] = page_shell["methodologyLines"][1]
    # Add third methodology line
    frontend["page_copy"]["methodology"]["lines"] = list(page_shell["methodologyLines"])
    # caveat
    frontend["page_copy"]["caveat"] = {
        "title": page_shell["categoryCaveat"]["title"],
        "body": page_shell["categoryCaveat"]["body"]
    }

    # ---- 2. Merge per-product copy + prune PENDING scaffolding ----
    merged_count = 0
    missing_barcodes = []

    for product in frontend["products"]:
        barcode = product.get("barcode", "")
        if barcode in copy_products:
            cp = copy_products[barcode]
            product["insightLine"] = cp["insightLine"]
            product["rowVerdict"] = cp["rowVerdict"]
            merged_count += 1
        else:
            missing_barcodes.append(barcode)

        # Prune PENDING_COPY scaffolding (milk-depth copy fields)
        # Remove top-level copy fields
        product.pop("consumerTakeaway", None)
        product.pop("consumerExplanation", None)
        product.pop("bestUseCases", None)

        # Remove bariInterpretation if it only has PENDING explanations
        # (it does for all 58 — we prune the whole bariInterpretation array since
        #  scores are preserved in expansion.nutrition and the UI doesn't use bariInterpretation
        #  on the cookies page)
        product.pop("bariInterpretation", None)

        # In expansion: remove bottomLine PENDING, keep nutrition
        if "expansion" in product and isinstance(product["expansion"], dict):
            exp = product["expansion"]
            exp.pop("bottomLine", None)
            # Keep: nutrition, ingredients, confidenceLabel, servingNote, positiveSignals, limitingFactors

    # ---- 3. Update _meta copy_status ----
    frontend["_meta"]["copy_status"] = "MERGED — P91 copy integration complete; 0 PENDING_COPY"
    frontend["_meta"]["copy_merge"] = {
        "merged": merged_count,
        "total": len(frontend["products"]),
        "source": "cookies_coffee_copy_v1.json",
        "task": "P91"
    }

    # ---- Write output ----
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(frontend, f, ensure_ascii=False, indent=2)

    print(f"Merged: {merged_count}/58 products")
    if missing_barcodes:
        print(f"MISSING barcodes (not in copy): {missing_barcodes}")
    else:
        print("All barcodes matched")

    # ---- Verify 0 PENDING_COPY remaining ----
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        out_text = f.read()

    pending_count = out_text.count("PENDING_COPY")
    print(f"PENDING_COPY remaining: {pending_count}")

    # SHA256
    sha = hashlib.sha256(out_text.encode("utf-8")).hexdigest()
    print(f"SHA256: {sha}")

    if pending_count > 0:
        # Find context around each PENDING
        lines = out_text.split("\n")
        for i, line in enumerate(lines):
            if "PENDING_COPY" in line:
                print(f"  Line {i+1}: {line.strip()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
