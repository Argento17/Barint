#!/usr/bin/env python3
"""P264: un-flag partial badges when only immaterial nutrition gaps remain."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("bari-web/src/data/comparisons")
FILES = [
    "bread_frontend_v3",
    "cakes_hard_cookies_frontend_v1",
    "cereals_frontend_v2",
    "cheese_frontend_v4",
    "cookies_coffee_frontend_v2",
    "granola_frontend_v2",
    "hard_cheeses_frontend_v4",
    "hummus_frontend_v5",
    "juices_frontend_v3",
]

MATERIAL = [
    ("energy", ["energyKcal", "energy", "energy_kcal"]),
    ("protein", ["protein", "protein_g"]),
    ("fat_g", ["fat", "fat_g"]),
    ("sugar", ["sugar", "sugars_g", "sugars"]),
    ("sodium", ["sodium", "sodium_mg"]),
]

PARTIAL_LABELS = {"ניתוח חלקי"}
PARTIAL_CONF = {"partial"}

FALLBACK_TEMPLATES = {
    "bread_frontend_v3": "cereals_frontend_v2",
    "hummus_frontend_v5": "brined_cheeses_frontend_v2",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def nutrition_of(product):
    exp = product.get("expansion") or {}
    nut = exp.get("nutrition") or {}
    if nut:
        return nut
    trace = product.get("_scoring_trace") or {}
    for key in ("nutrition", "normalized_nutrition", "nutrition_per_100g"):
        candidate = trace.get(key)
        if isinstance(candidate, dict) and candidate:
            return candidate
    return nut


def get_val(nut, aliases):
    for alias in aliases:
        if alias in nut:
            return nut.get(alias)
    return None


def material_status(nut):
    present = {}
    missing = []
    for canonical, aliases in MATERIAL:
        value = get_val(nut, aliases)
        present[canonical] = value
        if value is None:
            missing.append(canonical)
    return present, missing


def is_partial(product):
    return product.get("confidence") in PARTIAL_CONF or product.get("confidence_label_he") in PARTIAL_LABELS


def full_template_from_products(products):
    for product in products:
        if not is_partial(product):
            return {
                "confidence": product.get("confidence"),
                "confidence_label_he": product.get("confidence_label_he"),
                "confidence_tooltip_he": product.get("confidence_tooltip_he"),
                "confidence_sub_reason": product.get("confidence_sub_reason"),
                "expansion_confidenceLabel": (product.get("expansion") or {}).get("confidenceLabel"),
            }
    return None


def resolve_template(fn, products):
    template = full_template_from_products(products)
    if template is not None:
        return template, "in_file"
    fallback_fn = FALLBACK_TEMPLATES[fn]
    fallback_path = ROOT / (fallback_fn + ".json")
    with open(fallback_path, encoding="utf-8") as f:
        fallback_data = json.load(f)
    template = full_template_from_products(fallback_data["products"])
    return template, "fallback:" + fallback_fn


def apply_full(product, template):
    product["confidence"] = template["confidence"]
    product["confidence_label_he"] = template["confidence_label_he"]
    product["confidence_tooltip_he"] = template["confidence_tooltip_he"]
    if "confidence_sub_reason" in template:
        product["confidence_sub_reason"] = template["confidence_sub_reason"]
    expansion = product.setdefault("expansion", {})
    if template.get("expansion_confidenceLabel") is not None:
        expansion["confidenceLabel"] = template["expansion_confidenceLabel"]


def git_product_scores(path):
    try:
        raw = subprocess.check_output(["git", "show", "HEAD:" + path], stderr=subprocess.DEVNULL)
        data = json.loads(raw)
        return {p["barcode"]: (p.get("score"), p.get("grade")) for p in data["products"]}
    except Exception:
        return None


def process_file(fn):
    path = ROOT / (fn + ".json")
    rel = path.as_posix()
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    products = data["products"]
    git_scores = git_product_scores(rel)
    partial_before = 0
    unflagged = []
    kept = []
    to_unflag = []
    for product in products:
        if not is_partial(product):
            continue
        partial_before += 1
        nut = nutrition_of(product)
        present, missing = material_status(nut)
        if missing:
            kept.append({"barcode": product["barcode"], "missing_material": missing})
            continue
        to_unflag.append((product, present, nut))
    template = None
    template_source = None
    if to_unflag:
        template, template_source = resolve_template(fn, products)
        for product, present, nut in to_unflag:
            apply_full(product, template)
            unflagged.append({
                "barcode": product["barcode"],
                "material_present": present,
                "fiber": get_val(nut, ["fiber", "dietary_fiber_g", "fiber_g"]),
            })
    partial_after = sum(1 for p in products if is_partial(p))
    score_grade_changes = []
    if git_scores:
        for product in products:
            barcode = product["barcode"]
            if barcode not in git_scores:
                continue
            old_score, old_grade = git_scores[barcode]
            if product.get("score") != old_score or product.get("grade") != old_grade:
                score_grade_changes.append(barcode)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return {
        "file": fn,
        "template_source": template_source,
        "template": template,
        "partial_before": partial_before,
        "partial_after": partial_after,
        "unflagged_count": len(unflagged),
        "kept_count": len(kept),
        "unflagged_samples": unflagged[:5],
        "kept_samples": kept[:5],
        "score_grade_changes_vs_head": score_grade_changes,
        "sha256": sha256(path),
    }


def main():
    report = {"files": [process_file(fn) for fn in FILES]}
    out = Path(".tmp_p264_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("report written to .tmp_p264_report.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
