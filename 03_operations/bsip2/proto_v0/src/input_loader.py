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

    TASK-476 (root cause diagnosed in TASK-475): some BSIP1 builders leave
    `ingredients_list` empty even when the real scraped ingredient text is
    present elsewhere on the record. Previously this function returned `[]`
    with no fallback, so the engine's own bleed-sanitizer and NOVA/additive
    signals never saw real, already-scraped ingredient text for those
    products (57 live products across bread/crackers/protein-bars).

    Precedence (co-signed by Nutrition Agent, binding — never reorder):
      1. `ingredients_list` if non-empty — BSIP1's primary structured field.
      2. `ingredient_order` — BSIP1's structured, position-tagged parse
         output; each entry's `text` field is extracted, order preserved.
      3. `ingredients_text_he` / `ingredients_raw` — flat scraped string,
         last resort, split on top-level commas.

    The returned raw list still passes through
    `signal_extractor.sanitize_ingredient_list()` (TASK-144/EV-026) before
    any count or NOVA inference — this function does not bypass that gate.
    Never touches Open Food Facts or any external source (OFF is banned
    project-wide) — only fields already present on the BSIP1 record.
    """
    primary = product.get("ingredients_list")
    if primary:
        return primary

    order = product.get("ingredient_order")
    if order:
        texts = [
            entry.get("text") for entry in order
            if isinstance(entry, dict) and entry.get("text")
        ]
        if texts:
            return texts

    raw_text = product.get("ingredients_text_he") or product.get("ingredients_raw")
    if raw_text:
        items = _split_top_level_commas(raw_text)
        if items:
            return items

    return []


def _split_top_level_commas(text: str) -> list[str]:
    """Split ingredient text on top-level commas only — commas nested inside
    parentheses/brackets stay with their parent item (e.g. a declared
    sub-group like "קמחים 36% (פשתן, שומשום, אפונה)" is one ingredient, not
    four). A naive `text.split(",")` fragments every bracketed sub-list into
    separate pseudo-ingredients, inflating the count enough to feed wrong
    signal into anything that reads ingredient count (NOVA proxy, router
    thresholds). Matches the bracket-aware splitter TASK-475 measured
    against and Nutrition Agent co-signed — this is the exact method, not a
    re-derivation."""
    items: list[str] = []
    depth = 0
    buf: list[str] = []
    for ch in text:
        if ch in "([":
            depth += 1
            buf.append(ch)
        elif ch in ")]":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == "," and depth == 0:
            items.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        items.append("".join(buf).strip())
    return [i for i in items if i]


def get_ingredients_text(product: dict) -> str:
    """Return full ingredients text in Hebrew, defaulting to empty string."""
    return product.get("ingredients_text_he") or ""


def get_trust(product: dict) -> tuple[str, float]:
    """Return (trust_level, trust_score). Level: high/medium/low/unknown."""
    level = product.get("canonical_trust_level") or "unknown"
    score = product.get("canonical_trust_score")
    return level, (score if score is not None else 0.5)
