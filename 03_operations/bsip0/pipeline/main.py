from pathlib import Path
import json
import hashlib
import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from dotenv import load_dotenv

from extractor import extract_product

load_dotenv()  # reads AZURE_DI_KEY from C:\Bari\.env (gitignored)

BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "data" / "raw" / "snack_bars"
OUTPUT_DIR = BASE_DIR / "outputs"
CACHE_DIR = BASE_DIR / "cache"
CACHE_FILE = CACHE_DIR / "ocr_cache.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

EXCLUDED_PRODUCTS = {"product_010"}

AZURE_ENDPOINT = "https://bsip0ocr.cognitiveservices.azure.com/"
AZURE_KEY = os.environ["AZURE_DI_KEY"]

azure_client = DocumentIntelligenceClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_KEY)
)


def load_cache() -> dict:
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def azure_ocr_image(image_path: Path, cache: dict) -> dict:
    img_hash = file_hash(image_path)

    # New cache key avoids old plain-text cache entries
    cache_key = f"azure_layout_tables_v1:{img_hash}"

    if cache_key in cache:
        print(f"Using cached OCR: {image_path.name}")
        return cache[cache_key]

    print(f"Calling Azure OCR: {image_path.name}")

    with open(image_path, "rb") as f:
        poller = azure_client.begin_analyze_document(
            "prebuilt-layout",
            body=f
        )

    result = poller.result()

    lines = []
    for page in result.pages:
        for line in page.lines:
            lines.append(line.content)

    structured_tables = []

    if result.tables:
        for table in result.tables:
            row_count = table.row_count
            col_count = table.column_count

            grid = [["" for _ in range(col_count)] for _ in range(row_count)]

            for cell in table.cells:
                row = cell.row_index
                col = cell.column_index
                content = (cell.content or "").strip()

                grid[row][col] = content

            structured_tables.append(grid)

    ocr_result = {
        "lines": lines,
        "tables": structured_tables
    }

    cache[cache_key] = ocr_result
    save_cache(cache)

    return ocr_result


def scan_product(product_dir: Path, cache: dict) -> dict:
    front_image = product_dir / "front.png"
    ingredients_image = product_dir / "ingredients.png"
    nutrition_image = product_dir / "nutrition1.png"

    images = {
        "front": str(front_image) if front_image.exists() else None,
        "ingredients": str(ingredients_image) if ingredients_image.exists() else None,
        "nutrition": [str(nutrition_image)] if nutrition_image.exists() else []
    }

    raw_ocr = {}

    if front_image.exists():
        raw_ocr["front"] = azure_ocr_image(front_image, cache)

    if ingredients_image.exists():
        raw_ocr["ingredients"] = azure_ocr_image(ingredients_image, cache)

    if nutrition_image.exists():
        raw_ocr["nutrition_1"] = azure_ocr_image(nutrition_image, cache)

    extracted = extract_product(raw_ocr)

    return {
        "product_id": product_dir.name,
        "images": images,
        "raw_ocr": raw_ocr,
        "ocr_engine": "azure_document_intelligence_layout_tables",
        "extracted": extracted,
        "review_status": "extraction_completed_table_parser_v1"
    }


def main():
    print("Scanning products...")

    cache = load_cache()

    for product_dir in sorted(RAW_DIR.iterdir()):
        if not product_dir.is_dir():
            continue

        if product_dir.name in EXCLUDED_PRODUCTS:
            print(f"Skipping excluded product: {product_dir.name}")
            continue

        print(f"\nProcessing: {product_dir.name}")

        product_data = scan_product(product_dir, cache)

        output_file = OUTPUT_DIR / f"{product_dir.name}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(product_data, f, ensure_ascii=False, indent=2)

        print(f"Created JSON: {output_file}")

    print("\nDone.")


if __name__ == "__main__":
    main()