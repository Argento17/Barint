"""
reship_bread_180C.py — TASK-180C bread re-baseline reship
Owner sign-off received 2026-06-05: "approve all - sign off"

Score sources:
  - 5 recal products: on_score (B→A grade change with RECAL_P0=on)
  - All others: off_score (HEAD engine, RECAL_P0=off, GLASSBOX_W4=on)

Rounds all scores to nearest integer.
Re-sorts by score descending.
Clears stale grade_divergences (resolved by new engine scores).
"""

import json
import os
from datetime import datetime, timezone

FRONTEND_PATH = r"C:\Bari\bari-web\src\data\comparisons\bread_frontend_v2.json"

# (new_score, new_grade, score_source)
# off_score values from run_bread_008_headpin/off.json (rounded)
# on_score values from run_bread_008_headpin/recal_on.json (rounded)
SCORE_MAP = {
    # --- Recal-on (RECAL_P0=on): B→A grade moves, approved 2026-06-05 ---
    "shufersal_2079996":         (82, "A", "recal_on"),   # לחם אחיד פרוס קל     off=78.3→on=82.0
    "shufersal_497044":          (82, "A", "recal_on"),   # לחם ברמן אקטיב       off=79.4→on=82.0
    "shufersal_7290018500316":   (82, "A", "recal_on"),   # לחם כוסמין לבן        off=74.8→on=81.6
    "shufersal_2079033":         (82, "A", "recal_on"),   # לחם דגנים לייט        off=78.8→on=82.0
    "shufersal_96086000966":     (82, "A", "recal_on"),   # קרקר כוסמין מלא ושומשום off=78.4→on=81.6

    # --- HEAD-off A-grade products ---
    "shufersal_7290016245325":   (82, "A", "off"),        # לחם טחינה פרוס        82.0 (exact match)
    "shufersal_3268429":         (82, "A", "off"),        # לחם ירוק מקמח מלא     82.0
    "shufersal_481203":          (82, "A", "off"),        # לחם מחמצת קמח מלא     82.0
    "shufersal_3054183":         (81, "A", "off"),        # לחם שיפון מלא מסטמכר  81.0
    "shufersal_2079927":         (80, "A", "off"),        # לחם דגנים מלא         80.2
    "shufersal_3268252":         (82, "A", "off"),        # לחם חיטה מלא לילדים   82.0
    "shufersal_574370":          (82, "A", "off"),        # לחם שיפון קל           82.0
    "shufersal_481197":          (81, "A", "off"),        # לחם מחמצת גרעינים     80.9

    # --- HEAD-off B-grade products ---
    "shufersal_96086000577":     (76, "B", "off"),        # קרקר כוסמין אורגני   76.3
    "shufersal_2079477":         (73, "B", "off"),        # לחם אחיד פרוס         72.7
    "shufersal_7290016967074":   (72, "B", "off"),        # לחם אנג'ל חיטה מלאה  72.0 (exact match)
    "shufersal_4685027":         (72, "B", "off"),        # לחם מחמצת וחיטה מלאה קל 72.0
    "shufersal_7290018500460":   (72, "B", "off"),        # לחם אנג'ל חצי מלא    72.0
    "shufersal_7296073134459":   (71, "B", "off"),        # קרקר פריך בסגנון שוודי 70.9
    "shufersal_7296073134442":   (70, "B", "off"),        # קרקר פריך עם קמח שיפון 70.0
    "shufersal_6451507":         (69, "B", "off"),        # לחם מחמצת מכוסמין     69.0
    "shufersal_6451484":         (67, "B", "off"),        # לחם מחמצת אגוזים צימוקים 67.4
    "shufersal_2079217":         (66, "B", "off"),        # לחם מחמצת שיפון+אגוזים 66.1
    "shufersal_8434165658523":   (66, "B", "off"),        # קרקר קרם קרקר         66.1
}


def reship():
    with open(FRONTEND_PATH, encoding="utf-8") as f:
        data = json.load(f)

    products = data["products"]
    changes = []
    missing = []

    for p in products:
        pid = p["id"]
        if pid not in SCORE_MAP:
            missing.append(pid)
            continue
        new_score, new_grade, source = SCORE_MAP[pid]
        old_score = p["score"]
        old_grade = p["grade"]
        if old_score != new_score or old_grade != new_grade:
            changes.append({
                "pid": pid,
                "name": p["name"],
                "old_score": old_score,
                "old_grade": old_grade,
                "new_score": new_score,
                "new_grade": new_grade,
                "score_source": source,
            })
        p["score"] = new_score
        p["grade"] = new_grade

    # Sort by score descending
    products.sort(key=lambda x: x["score"], reverse=True)

    # Update meta
    data["_meta"]["generated"] = datetime.now(timezone.utc).isoformat()
    data["_meta"]["source_run_id"] = "run_bread_008_headpin"
    data["_meta"]["production_pass"] = (
        "TASK-180C re-baseline 2026-06-05. Scores from run_bread_008_headpin "
        "(engine-baseline-2026-06-04, BARI_RECAL_P0=off primary + on for 5 products, "
        "BARI_GLASSBOX_W4=on). Owner sign-off 2026-06-05. "
        "Original: " + data["_meta"].get("production_pass", "")
    )
    # Clear stale grade divergences — engine now agrees (82/A for all affected products)
    data["_meta"]["grade_divergences"] = []
    data["_meta"]["grade_divergences_note"] = (
        "Cleared 2026-06-05 (TASK-180C): engine now independently scores "
        "לחם ירוק מקמח מלא at 82/A — no divergence."
    )

    with open(FRONTEND_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Reship complete. {len(changes)} products updated.")
    if missing:
        print(f"WARNING: {len(missing)} products not in SCORE_MAP: {missing}")

    print("\n=== Score changes ===")
    grade_moves = [c for c in changes if c["old_grade"] != c["new_grade"]]
    cosmetic = [c for c in changes if c["old_grade"] == c["new_grade"]]

    print(f"Grade moves ({len(grade_moves)}):")
    for c in grade_moves:
        src = f"[{c['score_source']}]"
        print(f"  {c['name']}: {c['old_score']}/{c['old_grade']} → {c['new_score']}/{c['new_grade']} {src}")

    print(f"\nCosmetic ({len(cosmetic)}):")
    for c in cosmetic:
        delta = c['new_score'] - c['old_score']
        sign = "+" if delta >= 0 else ""
        print(f"  {c['name']}: {c['old_score']}/{c['old_grade']} → {c['new_score']}/{c['new_grade']} ({sign}{delta})")

    print("\n=== Final score distribution ===")
    final_scores = sorted([SCORE_MAP[p["id"]][0] for p in products], reverse=True)
    a_products = [p for p in products if p["grade"] == "A"]
    b_products = [p for p in products if p["grade"] == "B"]
    c_products = [p for p in products if p["grade"] == "C"]
    print(f"A: {len(a_products)} products, B: {len(b_products)} products, C: {len(c_products)} products")
    print(f"Score range: {min(final_scores)}–{max(final_scores)}")
    print("Sorted scores:", final_scores)


if __name__ == "__main__":
    reship()
