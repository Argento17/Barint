import json
import os
from collections import Counter

BASE = r"C:\bari\bari-web\src\data\comparisons"
OUT_DIR = r"C:\Bari\03_operations\qa"
OUT_FILE = os.path.join(OUT_DIR, "beaver_content_audit_v1.json")

FILES = {
    "hummus":   "hummus_frontend_v5.json",
    "yogurts":  "yogurts_frontend_v2.json",
    "cereals":  "cereals_frontend_v1.json",
    "granola":  "granola_frontend_v1.json",
    "snacks":   "snacks_frontend_v2.json",
    "maadanim": "maadanim_frontend_v3.json",
    "cheese":   "cheese_frontend_v2.json",
    "butter":   "butter_frontend_v2.json",
    "bread":    "bread_frontend_v2.json",
}

VALID_GRADES = {"A", "B", "C", "D", "E"}
VALID_CONFIDENCE = {"verified", "partial", "inferred"}


def score_to_expected_grade(score):
    if score is None:
        return None
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    if score >= 35:
        return "D"
    return "E"


os.makedirs(OUT_DIR, exist_ok=True)

report = {
    "run_date": "2026-06-07",
    "categories": {},
    "totals": {"high": 0, "medium": 0, "low": 0, "total_defects": 0},
}

for cat, fname in FILES.items():
    fpath = os.path.join(BASE, fname)
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    n = len(products)
    defects = []

    # Template-bleed: collect all rowVerdict values
    row_verdict_counts = Counter()
    for p in products:
        rv = p.get("rowVerdict", "")
        if rv:
            row_verdict_counts[rv] += 1

    # Score clusters
    score_counts = Counter()
    for p in products:
        sc = p.get("score")
        if sc is not None:
            score_counts[sc] += 1

    score_clusters = [
        {"score": sc, "count": cnt}
        for sc, cnt in score_counts.items()
        if cnt >= 5
    ]

    bleed_verdicts = {rv: cnt for rv, cnt in row_verdict_counts.items() if cnt >= 3}
    template_bleed_suspects = len(bleed_verdicts)

    missing_image = 0
    missing_retailer = 0
    missing_insight = 0
    missing_row_verdict = 0
    grade_mismatches = 0

    # Track which products already got a rowVerdict template_bleed defect
    bleed_flagged_products = set()

    for p in products:
        pid = p.get("id", "UNKNOWN")
        pname = p.get("name", "")

        # 1. imageUrl
        img = p.get("imageUrl")
        if img is None:
            missing_image += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "imageUrl",
                "issue": "null",
                "severity": "high",
            })
        elif img == "":
            missing_image += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "imageUrl",
                "issue": "empty",
                "severity": "high",
            })

        # 2. retailer
        retailer = p.get("retailer")
        if retailer is None or retailer == "":
            missing_retailer += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "retailer",
                "issue": "null" if retailer is None else "empty",
                "severity": "medium",
            })

        # 3. name
        name = p.get("name")
        if name is None or name == "":
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "name",
                "issue": "null or empty",
                "severity": "high",
            })
        elif len(name) < 5:
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "name",
                "issue": f"too_short ({len(name)} chars)",
                "severity": "high",
            })

        # 4. brand
        brand = p.get("brand")
        if brand is None or brand == "":
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "brand",
                "issue": "null or empty",
                "severity": "high",
            })

        # 5. score
        score = p.get("score")
        if score is None:
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "score",
                "issue": "null",
                "severity": "high",
            })
        elif score == 0:
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "score",
                "issue": "zero",
                "severity": "high",
            })
        elif not (0 <= score <= 100):
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "score",
                "issue": f"out_of_range ({score})",
                "severity": "high",
            })

        # 6. grade + score/grade consistency
        grade = p.get("grade")
        if grade is None:
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "grade",
                "issue": "null",
                "severity": "high",
            })
        elif grade not in VALID_GRADES:
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "grade",
                "issue": f"invalid_value ({grade})",
                "severity": "high",
            })
        else:
            expected = score_to_expected_grade(score)
            if expected is not None and grade != expected:
                grade_mismatches += 1
                defects.append({
                    "product_id": pid,
                    "product_name": pname,
                    "field": "grade",
                    "issue": f"mismatch: score={score} expects_grade={expected} actual_grade={grade}",
                    "severity": "high",
                })

        # 7. insightLine
        il = p.get("insightLine")
        if il is None:
            missing_insight += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "insightLine",
                "issue": "null",
                "severity": "high",
            })
        elif il == "":
            missing_insight += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "insightLine",
                "issue": "empty",
                "severity": "high",
            })
        elif len(il) < 20:
            missing_insight += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "insightLine",
                "issue": f"too_short ({len(il)} chars): '{il}'",
                "severity": "medium",
            })

        # 8. rowVerdict
        rv = p.get("rowVerdict")
        if rv is None:
            missing_row_verdict += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "rowVerdict",
                "issue": "null",
                "severity": "high",
            })
        elif rv == "":
            missing_row_verdict += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "rowVerdict",
                "issue": "empty",
                "severity": "high",
            })
        elif len(rv) < 30:
            missing_row_verdict += 1
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "rowVerdict",
                "issue": f"too_short ({len(rv)} chars): '{rv}'",
                "severity": "medium",
            })
        elif rv in bleed_verdicts and pid not in bleed_flagged_products:
            bleed_flagged_products.add(pid)
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "rowVerdict",
                "issue": f"template_bleed: appears {bleed_verdicts[rv]}x in category",
                "severity": "medium",
            })

        # 9. confidence
        conf = p.get("confidence")
        if conf is None:
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "confidence",
                "issue": "null",
                "severity": "high",
            })
        elif conf not in VALID_CONFIDENCE:
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "confidence",
                "issue": f"invalid_value ({conf})",
                "severity": "high",
            })

        # 10. barcode
        bc = p.get("barcode")
        if bc is None:
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "barcode",
                "issue": "null",
                "severity": "high",
            })
        elif bc == "":
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "barcode",
                "issue": "empty",
                "severity": "high",
            })
        elif not str(bc).replace(".", "").isdigit():
            defects.append({
                "product_id": pid,
                "product_name": pname,
                "field": "barcode",
                "issue": f"non_numeric: '{bc}'",
                "severity": "high",
            })

    # Category-level: score clusters (low severity)
    for cluster in score_clusters:
        defects.append({
            "product_id": "_category",
            "product_name": "_all",
            "field": "score",
            "issue": f"score_cluster: {cluster['count']} products share score={cluster['score']}",
            "severity": "low",
        })

    # Category-level: template bleed summaries (medium)
    for rv_text, cnt in bleed_verdicts.items():
        defects.append({
            "product_id": "_category",
            "product_name": "_all",
            "field": "rowVerdict",
            "issue": f"template_bleed_summary: '{rv_text[:80]}' appears {cnt}x",
            "severity": "medium",
        })

    report["categories"][cat] = {
        "file": fname,
        "n_products": n,
        "defects": defects,
        "summary": {
            "missing_image": missing_image,
            "missing_retailer": missing_retailer,
            "missing_insight_line": missing_insight,
            "missing_row_verdict": missing_row_verdict,
            "score_grade_mismatches": grade_mismatches,
            "template_bleed_suspects": template_bleed_suspects,
            "score_clusters": score_clusters,
        },
    }

# Compute totals
h = m = l = 0
for cat_data in report["categories"].values():
    for d in cat_data["defects"]:
        if d["severity"] == "high":
            h += 1
        elif d["severity"] == "medium":
            m += 1
        else:
            l += 1

report["totals"] = {
    "high": h,
    "medium": m,
    "low": l,
    "total_defects": h + m + l,
}

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"Report written: {OUT_FILE}")
print(f"Totals: high={h}, medium={m}, low={l}, total={h+m+l}")
print()
for cat, cd in report["categories"].items():
    s = cd["summary"]
    print(f"  {cat} ({cd['n_products']} products):")
    print(f"    missing_image={s['missing_image']}  missing_retailer={s['missing_retailer']}")
    print(f"    missing_insight={s['missing_insight_line']}  missing_row_verdict={s['missing_row_verdict']}")
    print(f"    grade_mismatches={s['score_grade_mismatches']}  template_bleed={s['template_bleed_suspects']}")
    print(f"    score_clusters={s['score_clusters']}")
    print(f"    total_defect_entries={len(cd['defects'])}")
    print()
