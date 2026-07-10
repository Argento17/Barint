#!/usr/bin/env python3
"""
generate_faq_schema.py — Stage 9 of the Bari category factory.

Reads a *_frontend_vN.json produced by the category pipeline and emits
a JSON-LD FAQPage schema file for injection by the Next.js comparison page.

No LLM calls. Fully deterministic slot-fill from corpus data.

Usage:
    python generate_faq_schema.py \
        --input path/to/cheese_frontend_v3.json \
        --category-he "גבינות מרוחות" \
        --url https://bari.digital/hashvaot/cheese \
        --out path/to/cheese_faq_schema.json
"""

import io
import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def load_products_sorted(data: dict) -> list[dict]:
    products = data.get("products", [])
    return sorted(products, key=lambda p: p.get("score", 0), reverse=True)


def frontend_grade(product: dict) -> str:
    """The grade the PAGE shows: the engine's 6-grade scale folds S into A on the frozen
    ScoreChip (corpus.ts frontendGradeFromScore). Emitting the raw engine grade leaked
    "ציון S" into live structured data while the chip beside it read "A", and undercounted
    the A-list. Copy law: copy never writes "S"."""
    if product.get("_aCappedToB"):
        return "B"
    score = product.get("score")
    if not isinstance(score, (int, float)):
        return product.get("grade", "")
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    if score >= 35:
        return "D"
    return "E"


def grade_a_products(products: list[dict]) -> list[dict]:
    return [p for p in products if frontend_grade(p) == "A"]


def best_text(product: dict) -> str:
    return product.get("insightLine") or product.get("rowVerdict") or ""


def build_faq_entries(products: list[dict], category_he: str) -> list[dict]:
    entries = []
    if not products:
        return entries

    top = products[0]
    top_name = top.get("name", "")
    top_score = top.get("score", 0)
    top_grade = frontend_grade(top)
    top_insight = best_text(top)

    # Q1 — best product
    q1_answer = f"{top_name} קיבל את הציון הגבוה ביותר — {top_score}/100 (ציון {top_grade})."
    if top_insight:
        q1_answer += f" {top_insight}"
    entries.append({
        "@type": "Question",
        "name": f"מה המוצר הבריא ביותר ב{category_he}?",
        "acceptedAnswer": {"@type": "Answer", "text": q1_answer},
    })

    # Q2 — A-grade list (skip if none)
    a_products = grade_a_products(products)
    if a_products:
        # The count and the enumeration must agree. The old code named a_products[:8] while
        # stating len(a_products), so any category with >8 A-products emitted
        # self-contradicting structured data ("9 מוצרים…" followed by 8 names).
        A_LIST_CAP = 12
        shown = a_products[:A_LIST_CAP]
        names = [p["name"] for p in shown]
        if len(names) == 1:
            names_str = names[0]
        else:
            names_str = ", ".join(names[:-1]) + " ו-" + names[-1]
        truncated = len(a_products) > len(names)
        entries.append({
            "@type": "Question",
            "name": f"אילו מוצרי {category_he} מקבלים ציון A מבארי?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    f"{len(a_products)} מוצרים קיבלו ציון A, ביניהם: {names_str}."
                    if truncated
                    else f"{len(a_products)} מוצרים קיבלו ציון A: {names_str}."
                ),
            },
        })

    # Q3 — coverage / score range
    total = len(products)
    max_score = products[0].get("score", 0)
    min_score = products[-1].get("score", 0)
    entries.append({
        "@type": "Question",
        "name": f"כמה מוצרים בדקה בארי בקטגוריית {category_he}?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": (
                f"בארי בדקה {total} מוצרים בקטגוריית {category_he}. "
                f"הציון הגבוה ביותר הוא {max_score}/100 והציון הנמוך ביותר הוא {min_score}/100."
            ),
        },
    })

    # Q4 — top-2 comparison (only when 2+ products exist)
    if len(products) >= 2:
        second = products[1]
        second_name = second.get("name", "")
        second_score = second.get("score", 0)
        second_insight = best_text(second)

        q4_text = f"{top_name} קיבל {top_score}/100, {second_name} קיבל {second_score}/100."
        if top_insight:
            q4_text += f" {top_name}: {top_insight}"
        if second_insight:
            q4_text += f" {second_name}: {second_insight}"
        entries.append({
            "@type": "Question",
            "name": f"מה ההבדל בין {top_name} ל-{second_name} ב{category_he}?",
            "acceptedAnswer": {"@type": "Answer", "text": q4_text},
        })

    return entries


def generate_faq_schema(
    frontend_json_path: Path,
    category_he: str,
    page_url: str,
    output_path: Path,
) -> None:
    with open(frontend_json_path, encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("_meta", {})
    source_version = frontend_json_path.name
    category_slug = meta.get("category", frontend_json_path.stem)
    product_count = meta.get("product_count", len(data.get("products", [])))

    # Coverage gates
    if product_count < 5:
        print(f"FAIL [{category_slug}]: product_count={product_count} < 5 — coverage gate not met", file=sys.stderr)
        sys.exit(1)

    products = load_products_sorted(data)
    if not products:
        print(f"FAIL [{category_slug}]: no products array", file=sys.stderr)
        sys.exit(1)

    if not best_text(products[0]):
        print(f"WARN [{category_slug}]: top product has no insightLine — Q1 answer will be score-only")

    if not grade_a_products(products):
        print(f"WARN [{category_slug}]: no A-grade products — Q2 will be omitted")

    faq_entries = build_faq_entries(products, category_he)

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "_bari_meta": {
            "category": category_slug,
            "category_he": category_he,
            "source_version": source_version,
            "generated": datetime.now(timezone.utc).isoformat(),
            "product_count": product_count,
            "page_url": page_url,
        },
        "mainEntity": faq_entries,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)

    print(f"OK [{category_slug}]: {len(faq_entries)} FAQ entries -> {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate JSON-LD FAQPage schema from a Bari frontend JSON."
    )
    parser.add_argument("--input", required=True, help="Path to *_frontend_vN.json")
    parser.add_argument("--category-he", required=True, help='Hebrew category name, e.g. "גבינות מרוחות"')
    parser.add_argument("--url", required=True, help="Canonical page URL")
    parser.add_argument("--out", required=True, help="Output path for the faq_schema.json")
    args = parser.parse_args()

    generate_faq_schema(
        frontend_json_path=Path(args.input),
        category_he=args.category_he,
        page_url=args.url,
        output_path=Path(args.out),
    )


if __name__ == "__main__":
    main()
