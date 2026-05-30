import re


TARGET_FIELDS = {
    "energy_kcal_100g": None,
    "fat_g_100g": None,
    "saturated_fat_g_100g": None,
    "carbohydrates_g_100g": None,
    "fiber_g_100g": None,
    "protein_g_100g": None,
    "sodium_mg_100g": None,
    "cholesterol_mg_100g": None,
    "sugar_tbsp_100g": None
}


PER_100G_MARKERS = [
    "100",
    "100 גרם",
    "ל-100",
    "ל 100",
    "לכל 100",
    "ב-100",
    "ב 100"
]


LABEL_MAP = [
    # order matters
    (["כפיות סוכר"], "sugar_tbsp_100g"),

    (["חומצות שומן רוויות", "שומן רווי", "רוויות"], "saturated_fat_g_100g"),
    (["שומנים", "שומן"], "fat_g_100g"),

    (["סיבים תזונתיים", "סיבים"], "fiber_g_100g"),
    (["פחמימות", "סך הפחמימות"], "carbohydrates_g_100g"),

    (["חלבונים", "חלבון"], "protein_g_100g"),
    (["נתרן"], "sodium_mg_100g"),
    (["כולסטרול"], "cholesterol_mg_100g"),
    (["אנרגיה"], "energy_kcal_100g"),
]


IGNORE_LABELS = [
    "ויטמין",
    "ביוטין",
    "חומצה פולית",
    "ברזל",
    "סידן",
    "מינרלים",
    "B1",
    "B2",
    "B3",
    "B5",
    "B6",
    "B12",
    "ויטמין A",
    "ויטמין D",
    "ויטמין E",
    "סוכרים מתוך",
    "סוכרים"
]


def normalize_text(text: str) -> str:
    if not text:
        return ""

    return (
        str(text)
        .replace("״", '"')
        .replace("׳", "'")
        .replace(",", ".")
        .replace("־", "-")
        .strip()
    )


def clean_lines_from_ocr(ocr_obj: dict) -> list[str]:
    if not ocr_obj:
        return []

    if isinstance(ocr_obj, str):
        return [line.strip() for line in ocr_obj.splitlines() if line.strip()]

    lines = ocr_obj.get("lines", [])
    return [line.strip() for line in lines if line.strip()]


def parse_number(text: str):
    text = normalize_text(text)

    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def normalize_label(label: str) -> str:
    label = normalize_text(label)
    label = re.sub(r"\(.*?\)", "", label)
    label = re.sub(r"\s+", " ", label).strip()
    return label


def should_ignore_label(label: str) -> bool:
    label = normalize_label(label)

    return any(token in label for token in IGNORE_LABELS)


def map_label(label: str):
    label = normalize_label(label)

    if should_ignore_label(label):
        return None

    for variants, field in LABEL_MAP:
        for variant in variants:
            if variant in label:
                return field

    return None


def cell_has_100g_marker(cell: str) -> bool:
    cell = normalize_text(cell)

    return any(marker in cell for marker in PER_100G_MARKERS)


def find_100g_column(table: list[list[str]]):
    for row in table:
        for col_idx, cell in enumerate(row):
            if cell_has_100g_marker(cell):
                return col_idx

    # fallback: common table format = label | 100g | serving
    max_cols = max((len(row) for row in table), default=0)

    if max_cols >= 2:
        return 1

    return None


def find_label_cell(row: list[str]):
    for col_idx, cell in enumerate(row):
        field = map_label(cell)
        if field:
            return col_idx, field

    return None, None


def extract_nutrition_from_tables(tables: list[list[list[str]]]) -> dict:
    result = dict(TARGET_FIELDS)
    warnings = []

    if not tables:
        warnings.append("no_tables_found")
        return result, warnings

    candidate_tables = []

    for table in tables:
        label_hits = 0

        for row in table:
            _, field = find_label_cell(row)
            if field:
                label_hits += 1

        if label_hits >= 3:
            candidate_tables.append(table)

    if not candidate_tables:
        warnings.append("no_nutrition_table_detected")
        return result, warnings

    table = max(candidate_tables, key=lambda t: sum(1 for r in t if find_label_cell(r)[1]))

    col_100g = find_100g_column(table)

    if col_100g is None:
        warnings.append("no_100g_column_detected")
        return result, warnings

    seen_fields = set()

    for row in table:
        label_col, field = find_label_cell(row)

        if not field:
            continue

        if field in seen_fields:
            continue

        if col_100g >= len(row):
            warnings.append(f"{field}_100g_cell_missing")
            continue

        value = parse_number(row[col_100g])

        if value is None:
            warnings.append(f"{field}_value_missing")
            continue

        result[field] = value
        seen_fields.add(field)

    for field, value in result.items():
        if value is None:
            warnings.append(f"{field}_missing_or_uncertain")

    return result, warnings


def extract_metadata(ingredients_ocr: dict) -> dict:
    lines = clean_lines_from_ocr(ingredients_ocr)
    text = "\n".join(lines)

    def find(pattern: str):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None

    return {
        "brand": find(r"מותג/יצרן:\s*(.+)"),
        "country_of_origin": find(r"ארץ ייצור:\s*(.+)"),
        "package_size": find(r"מידה/סוג:\s*(.+)"),
        "sku": find(r'מק["]?ט:\s*([0-9]+)'),
        "kosher": find(r"כשרות:\s*(.+)"),
        "passover_status": find(r"פסח:\s*(.+)"),
        "dairy_meat_parve": find(r"חלבי/בשרי/פרווה:\s*(.+)")
    }


def extract_ingredients_raw(ingredients_ocr: dict):
    lines = clean_lines_from_ocr(ingredients_ocr)

    if not lines:
        return None

    start = None

    for i, line in enumerate(lines):
        if line == "רכיבים":
            start = i + 1
            break

    if start is None:
        for i, line in enumerate(lines):
            if "%" in line or "שוקולד" in line or "סירופ" in line:
                start = i
                break

    if start is None:
        return None

    stop_markers = [
        "מכיל",
        "עלול להכיל",
        "מאפיינים",
        "נוספים",
        "סוכר",
        "שומן רווי",
        "בכמות גבוהה"
    ]

    end = len(lines)

    for i in range(start, len(lines)):
        if any(lines[i].startswith(marker) or lines[i] == marker for marker in stop_markers):
            end = i
            break

    result = " ".join(lines[start:end]).strip()

    return result if len(result) > 20 else None


def extract_allergens(ingredients_ocr: dict) -> dict:
    lines = clean_lines_from_ocr(ingredients_ocr)

    contains = []
    may_contain = []

    for i, line in enumerate(lines):
        if line == "מכיל" and i + 1 < len(lines):
            contains.append(lines[i + 1])

        if line.startswith("עלול להכיל"):
            value = line.replace("עלול להכיל", "").strip()
            if value:
                may_contain.append(value)
            elif i + 1 < len(lines):
                may_contain.append(lines[i + 1])

    return {
        "contains_raw": contains,
        "may_contain_raw": may_contain
    }


def extract_product(raw_ocr: dict) -> dict:
    ingredients_ocr = raw_ocr.get("ingredients", {})

    nutrition_tables = []

    for key, value in raw_ocr.items():
        if key.startswith("nutrition"):
            if isinstance(value, dict):
                nutrition_tables.extend(value.get("tables", []))

    nutrition, nutrition_warnings = extract_nutrition_from_tables(nutrition_tables)

    return {
        "metadata": extract_metadata(ingredients_ocr),
        "ingredients_raw": extract_ingredients_raw(ingredients_ocr),
        "allergens": extract_allergens(ingredients_ocr),
        "nutrition_per_100g": nutrition,
        "nutrition_parser_status": "table_parser_v1",
        "nutrition_parser_warnings": nutrition_warnings
    }