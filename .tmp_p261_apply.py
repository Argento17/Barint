#!/usr/bin/env python3
"""P261: label remediation + rank reindex (staging only)."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(r"C:/Bari/bari-web/src/data/comparisons")
MATERIAL = ("energyKcal", "protein", "fat", "sugar", "sodium")

COOKIES_FULL = {
    "confidence": "verified",
    "confidence_label_he": "מבוסס על נתונים מלאים",
    "confidence_tooltip_he": "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים.",
    "confidence_sub_reason": None,
    "expansion_confidenceLabel": "מבוסס על נתונים מלאים",
}

CAKES_FULL = {
    "confidence": "verified",
    "confidence_label_he": "נתונים מלאים",
    "confidence_tooltip_he": "כל הנתונים התזונתיים ורשימת הרכיבים נסרקו ישירות מהמוצר.",
    "confidence_sub_reason": None,
    "expansion_confidenceLabel": "נתונים מלאים",
}

PARTIAL_LABELS = {"ניתוח חלקי", "נתונים חלקיים"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def nutrition_of(p: dict) -> dict:
    return (p.get("expansion") or {}).get("nutrition") or {}


def missing_material(nut: dict) -> list:
    return [k for k in MATERIAL if nut.get(k) is None]


def is_fiber_only_null(nut: dict) -> bool:
    return len(missing_material(nut)) == 0 and nut.get("fiber") is None


def is_sugar_only_null(nut: dict) -> bool:
    return missing_material(nut) == ["sugar"]


def apply_full(p: dict, full: dict) -> None:
    p["confidence"] = full["confidence"]
    p["confidence_label_he"] = full["confidence_label_he"]
    p["confidence_tooltip_he"] = full["confidence_tooltip_he"]
    p["confidence_sub_reason"] = full["confidence_sub_reason"]
    exp = p.setdefault("expansion", {})
    exp["confidenceLabel"] = full["expansion_confidenceLabel"]


def is_stale_partial(p: dict) -> bool:
    return p.get("confidence_label_he") in PARTIAL_LABELS


def scores_before(data: dict) -> dict:
    return {p["barcode"]: p["score"] for p in data["products"]}


def monotonic_by_score(products: list) -> bool:
    scores = [p["score"] for p in products]
    return all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1))


def ranks_sequential(products: list) -> bool:
    ranks = [p.get("rank") for p in products]
    return ranks == list(range(1, len(products) + 1))


def reindex_ranks(products: list) -> None:
    n = len(products)
    for i, p in enumerate(products, start=1):
        p["rank"] = i
        if "categoryTotal" in p:
            p["categoryTotal"] = n


def process_cookies(data: dict) -> dict:
    before_n = len(data["products"])
    scores_orig = scores_before(data)
    discard_ids = {"7290017724171", "7296073659969"}
    kept = []
    discarded = []
    relabeled = []
    kept_partial = []

    for p in data["products"]:
        bc = p["barcode"]
        nut = nutrition_of(p)
        if bc in discard_ids:
            discarded.append({"barcode": bc, "missing": missing_material(nut)})
            continue
        miss = missing_material(nut)
        if miss and not is_sugar_only_null(nut) and not is_fiber_only_null(nut):
            discarded.append({"barcode": bc, "missing": miss, "unexpected": True})
            continue
        if is_stale_partial(p):
            relabel_fields = ("energyKcal", "protein", "fat", "sugar")
            if all(nut.get(k) is not None for k in relabel_fields):
                apply_full(p, COOKIES_FULL)
                relabeled.append(bc)
            else:
                kept_partial.append({"barcode": bc, "missing": miss})
        kept.append(p)

    kept.sort(key=lambda p: (-p["score"], p["barcode"]))
    reindex_ranks(kept)
    data["products"] = kept
    if "_meta" in data:
        data["_meta"]["product_count"] = len(kept)
        if "scored_count" in data["_meta"]:
            data["_meta"]["scored_count"] = len(kept)

    assert scores_orig == {p["barcode"]: p["score"] for p in kept}
    assert monotonic_by_score(kept)
    assert ranks_sequential(kept)

    return {
        "before_n": before_n,
        "after_n": len(kept),
        "discarded": discarded,
        "relabeled_count": len(relabeled),
        "kept_partial_count": len(kept_partial),
        "relabeled_barcodes": relabeled,
        "kept_partial": kept_partial,
    }


def process_cakes(data: dict) -> dict:
    before_n = len(data["products"])
    scores_orig = scores_before(data)
    tier_a = []
    tier_b = []
    tier_c = []
    kept = []

    for p in data["products"]:
        bc = p["barcode"]
        nut = nutrition_of(p)
        miss = missing_material(nut)
        if is_fiber_only_null(nut):
            tier_c.append(bc)
            kept.append(p)
            continue
        if miss:
            tier_a.append({"barcode": bc, "missing": miss})
            continue
        if is_stale_partial(p):
            apply_full(p, CAKES_FULL)
            tier_b.append(bc)
        kept.append(p)

    reindex_ranks(kept)
    data["products"] = kept
    if "_meta" in data:
        data["_meta"]["product_count"] = len(kept)
        if "scored_count" in data["_meta"]:
            data["_meta"]["scored_count"] = len(kept)
    if "page_copy" in data and "hero" in data["page_copy"]:
        data["page_copy"]["hero"]["productCount"] = len(kept)
        data["page_copy"]["hero"]["scoredCount"] = len(kept)

    assert scores_orig == {p["barcode"]: p["score"] for p in kept}
    assert monotonic_by_score(kept)
    assert ranks_sequential(kept)

    return {
        "before_n": before_n,
        "after_n": len(kept),
        "tier_a_discard": tier_a,
        "tier_a_count": len(tier_a),
        "tier_b_relabel": tier_b,
        "tier_b_count": len(tier_b),
        "tier_c_keep": tier_c,
        "tier_c_count": len(tier_c),
    }


def process_rank_only(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    before_n = len(data["products"])
    scores_orig = scores_before(data)
    ranks_before = [p.get("rank") for p in data["products"]]
    reindex_ranks(data["products"])
    assert scores_orig == scores_before(data)
    assert monotonic_by_score(data["products"])
    assert ranks_sequential(data["products"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return {
        "file": path.name,
        "before_n": before_n,
        "after_n": len(data["products"]),
        "rank_mismatches_before": sum(1 for a, b in zip(ranks_before, range(1, before_n + 1)) if a != b),
    }


def main() -> int:
    report = {}
    cookies_path = ROOT / "cookies_coffee_frontend_v2.json"
    with open(cookies_path, encoding="utf-8") as f:
        cookies = json.load(f)
    report["cookies"] = process_cookies(cookies)
    with open(cookies_path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
        f.write("\n")
    report["cookies"]["sha256"] = sha256(cookies_path)

    cakes_path = ROOT / "cakes_hard_cookies_frontend_v1.json"
    with open(cakes_path, encoding="utf-8") as f:
        cakes = json.load(f)
    report["cakes"] = process_cakes(cakes)
    with open(cakes_path, "w", encoding="utf-8") as f:
        json.dump(cakes, f, ensure_ascii=False, indent=2)
        f.write("\n")
    report["cakes"]["sha256"] = sha256(cakes_path)

    report["rank_only"] = []
    for name in ("cheese_frontend_v4.json", "chocolate_bars_frontend_v1.json", "milk_frontend_v1.json"):
        p = ROOT / name
        r = process_rank_only(p)
        r["sha256"] = sha256(p)
        report["rank_only"].append(r)

    out = Path(r"C:/Bari/.tmp_p261_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
