#!/usr/bin/env python3
"""
run_all_faq_schemas.py - generates FAQ JSON-LD for every live comparison category.

Reads from: bari-web/src/data/comparisons/
Writes to:  bari-web/src/data/seo/

Run from C:/Bari:
    python 03_operations/seo/run_all_faq_schemas.py
"""

import io
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
COMPARISONS = REPO / "bari-web" / "src" / "data" / "comparisons"
SEO_OUT = REPO / "bari-web" / "src" / "data" / "seo"
GENERATOR = Path(__file__).parent / "generate_faq_schema.py"
BASE_URL = "https://bari.digital"

CATEGORIES = [
    {
        "slug": "cheese",
        "he": "גבינות מרוחות",
        "json": COMPARISONS / "cheese_frontend_v3.json",
        "out": SEO_OUT / "cheese_faq_schema.json",
    },
    {
        "slug": "yogurts",
        "he": "יוגורטים",
        "json": COMPARISONS / "yogurts_frontend_v3.json",
        "out": SEO_OUT / "yogurts_faq_schema.json",
    },
    {
        "slug": "bread",
        "he": "לחמים",
        "json": COMPARISONS / "bread_frontend_v2.json",
        "out": SEO_OUT / "bread_faq_schema.json",
    },
    {
        "slug": "butter",
        "he": "חמאה ומרגרינה",
        "json": COMPARISONS / "butter_frontend_v2.json",
        "out": SEO_OUT / "butter_faq_schema.json",
    },
    {
        "slug": "hummus",
        "he": "חומוס",
        "json": COMPARISONS / "hummus_frontend_v5.json",
        "out": SEO_OUT / "hummus_faq_schema.json",
    },
    {
        "slug": "breakfast-cereals",
        "he": "דגני בוקר",
        "json": COMPARISONS / "cereals_frontend_v2.json",
        "out": SEO_OUT / "breakfast_cereals_faq_schema.json",
    },
    {
        "slug": "granola",
        "he": "גרנולה ומוזלי",
        "json": COMPARISONS / "granola_frontend_v1.json",
        "out": SEO_OUT / "granola_faq_schema.json",
    },
    {
        "slug": "salty-snacks",
        "he": "חטיפים מלוחים",
        "json": COMPARISONS / "salty_snacks_frontend_v4.json",
        "out": SEO_OUT / "salty_snacks_faq_schema.json",
    },
    {
        "slug": "juices",
        "he": "מיצים ומשקאות פירות",
        "json": COMPARISONS / "juices_frontend_v3.json",
        "out": SEO_OUT / "juices_faq_schema.json",
    },
    {
        "slug": "hard-cheeses",
        "he": "גבינות קשות",
        "json": COMPARISONS / "hard_cheeses_frontend_v2.json",
        "out": SEO_OUT / "hard_cheeses_faq_schema.json",
    },
    {
        "slug": "brined-cheeses",
        "he": "גבינות מלוחות",
        "json": COMPARISONS / "brined_cheeses_frontend_v2.json",
        "out": SEO_OUT / "brined_cheeses_faq_schema.json",
    },
    {
        "slug": "cookies-coffee",
        "he": "עוגיות לקפה",
        "json": COMPARISONS / "cookies_coffee_frontend_v1.json",
        "out": SEO_OUT / "cookies_coffee_faq_schema.json",
    },
    {
        "slug": "vegetable-spreads",
        "he": "ממרחי ירקות",
        "json": COMPARISONS / "hummus_frontend_v5.json",
        "out": SEO_OUT / "vegetable_spreads_faq_schema.json",
    },
]


def main() -> None:
    ok = 0
    fail = 0

    for cat in CATEGORIES:
        if not cat["json"].exists():
            print(f"SKIP [{cat['slug']}]: {cat['json']} not found")
            fail += 1
            continue

        result = subprocess.run(
            [
                sys.executable,
                str(GENERATOR),
                "--input", str(cat["json"]),
                "--category-he", cat["he"],
                "--url", f"{BASE_URL}/hashvaot/{cat['slug']}",
                "--out", str(cat["out"]),
            ],
            capture_output=False,
        )
        if result.returncode == 0:
            ok += 1
        else:
            fail += 1

    print(f"\n{'='*40}")
    print(f"FAQ schema generation: {ok} OK, {fail} FAIL/SKIP")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
