"""
BSIP2 Prototype v0 — Input Loader
Loads frozen BSIP1 v0.1 products. Read-only. Never modifies source.
"""
import json
import pathlib
import logging

log = logging.getLogger(__name__)

REQUIRED_FIELDS = [
    "schema_version", "file_type", "canonical_product_id", "barcode",
    "canonical_name_he", "brand", "source_retailers",
    "normalized_nutrition_per_100g", "ingredients_list",
    "allergens_contains", "allergens_may_contain",
    "confidence", "conflicts_summary", "missing_fields",
    "inferred_fields", "audit_ref",
]

NUTRITION_FIELDS = [
    "energy_kcal", "fat_g", "fat_saturated_g", "fat_trans_g",
    "sodium_mg", "carbohydrates_g", "sugars_g",
    "dietary_fiber_g", "protein_g",
]


def load_product(path: pathlib.Path) -> dict:
    """Load a single BSIP1 product JSON. Returns the parsed dict unchanged."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def validate_product(data: dict) -> list[str]:
    """
    Check required fields are present. Returns list of validation errors.
    Does NOT raise — errors are recorded in the trace.
    """
    errors = []
    if data.get("file_type") != "product":
        errors.append(f"file_type is '{data.get('file_type')}', expected 'product'")
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")
    if "normalized_nutrition_per_100g" in data:
        nn = data["normalized_nutrition_per_100g"]
        if not isinstance(nn, dict):
            errors.append("normalized_nutrition_per_100g is not an object")
    return errors


def load_batch(source_dir: pathlib.Path) -> list[dict]:
    """
    Load all non-audit BSIP1 product JSONs from source_dir.
    Returns list of dicts with an added '_source_path' key for traceability.
    """
    source_dir = pathlib.Path(source_dir)
    paths = sorted(
        p for p in source_dir.glob("bsip1_*.json")
        if "audit" not in p.name
    )
    products = []
    for path in paths:
        try:
            data = load_product(path)
            data["_source_path"] = str(path)
            errors = validate_product(data)
            data["_load_errors"] = errors
            if errors:
                log.warning("Validation errors in %s: %s", path.name, errors)
            products.append(data)
        except Exception as e:
            log.error("Failed to load %s: %s", path.name, e)
    log.info("Loaded %d products from %s", len(products), source_dir)
    return products


def get_nutrition(product: dict) -> dict:
    """Return normalized_nutrition_per_100g with all fields, defaulting to None."""
    nn = product.get("normalized_nutrition_per_100g", {}) or {}
    return {f: nn.get(f) for f in NUTRITION_FIELDS}


def get_ingredients(product: dict) -> list[str]:
    """Return the ingredient list for scoring, in fidelity-preference order.

    Precedence (TASK-476, Nutrition-approved fallback chain):
      1. ``ingredients_list`` if non-empty (highest fidelity — already
         structured/sanitized by BSIP1's signal extractor).
      2. ``ingredient_order`` — extract each entry's ``text`` field, in the
         order BSIP1 recorded them (structured but not yet flattened into
         ``ingredients_list``).
      3. A bracket-depth-aware comma split of ``ingredients_text_he`` /
         ``ingredients_raw`` — used only when no structured field is
         available. This does NOT fragment parenthesised/bracketed
         sub-groups (e.g. "קמחים 36% (פשתן, שומשום, אפונה)" stays one item).

    Callers must still run the result through ``sanitize_ingredient_list()``
    before using it for scoring or display — this function only resolves
    *which* raw source to read, it does not sanitize.
    """
    primary = product.get("ingredients_list")
    if primary:
        return primary

    order = product.get("ingredient_order")
    if order:
        texts = [entry.get("text") for entry in order
                 if isinstance(entry, dict) and entry.get("text")]
        if texts:
            return texts

    raw_text = product.get("ingredients_text_he") or product.get("ingredients_raw")
    if raw_text:
        items = _split_top_level_commas(raw_text)
        if items:
            return items

    return []


def _split_top_level_commas(text: str) -> list[str]:
    """Bracket-depth-aware comma split.

    Splits on commas only at bracket-depth 0, so parenthesised/bracketed
    sub-groups (declared ingredient sub-lists) are never fragmented into
    separate top-level items. Tracks (), [], and {} as one shared depth
    counter (curly braces included per TASK-476 Step-4 follow-up so a
    stray "{" does not truncate/merge unrelated real ingredients).
    """
    items: list[str] = []
    depth = 0
    current: list[str] = []
    openers = "([{"
    closers = ")]}"
    for ch in text:
        if ch in openers:
            depth += 1
            current.append(ch)
        elif ch in closers:
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch == "," and depth == 0:
            piece = "".join(current).strip()
            if piece:
                items.append(piece)
            current = []
        else:
            current.append(ch)
    tail = "".join(current).strip()
    if tail:
        items.append(tail)
    return items


def get_ingredients_text(product: dict) -> str:
    """Return full ingredients text in Hebrew, defaulting to empty string."""
    return product.get("ingredients_text_he") or ""


def get_trust(product: dict) -> tuple[str, float]:
    """Return (trust_level, trust_score). Level: high/medium/low/unknown."""
    level = product.get("canonical_trust_level") or "unknown"
    score = product.get("canonical_trust_score")
    return level, (score if score is not None else 0.5)
