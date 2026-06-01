"""
BSIP2 MVP Recalibration — re-score frontend corpora (R-01 through R-05).

Reads BSIP1 / BSIP0 sources, runs patched score_engine pipeline,
writes updated scores to c:\\Users\\HP\\bari\\src\\data\\...
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from input_loader import load_batch, load_product
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from constants import score_to_grade

# Import bread normalizer
from batch_run_bread_retail_003 import normalize_to_bsip1

BREAD_RAW = pathlib.Path(r"C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json")

BARI = pathlib.Path(r"c:\bari\bari-web")
DOCS = BARI / "docs"
TODAY = datetime.date.today().isoformat()

SNACKS_FRONTEND = BARI / "src/data/comparisons/snacks_frontend_v2.json"
BREAD_FRONTEND = BARI / "src/data/comparisons/bread_frontend_v2.json"
YOGURTS_FRONTEND = BARI / "src/data/comparisons/yogurts_frontend_v1.json"
MILK_FRONTEND = BARI / "src/data/milk-comparison.json"

SNACKS_BSIP1 = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")
MILK_BSIP1 = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output")
YOGURTS_BSIP1 = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_001\output")

YOGURT_NAME_HINTS: dict[str, list[str]] = {
    "yog-001": ["יוגורט מלא", "3%", "תנובה"],
    "yog-002": ["ביו", "1.5%", "תנובה"],
    "yog-003": ["יוגורט 0%", "שומן", "תנובה"],
    "yog-004": ["יווני", "5%", "שטראוס"],
    "yog-005": ["יווני", "0%", "שטראוס"],
    "yog-006": ["אקטיביה", "טבע"],
    "yog-007": ["יופלה", "פירות"],
    "yog-008": ["אקטיביה", "טעמ"],
    "yog-009": ["קוקוס", "ללא גלוטן"],
    "yog-010": ["סויה", "טבע"],
    "yog-011": ["שתיה", "וניל"],
    "yog-012": ["GO", "פירות יער", "יופלה"],
    "yog-013": ["מילקי", "שוקולד"],
    "yog-014": ["0%", "ממתיק"],
}


def run_simple_pipeline(product: dict) -> dict:
    signals = extract_signals(product)
    cat_result = classify_category(product)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    return score_product(product, signals, cat_result, nova_result, eval_result)


def round_score(score: float | None) -> int | None:
    if score is None:
        return None
    return int(round(score))


def grade_from_score(score: float | None, grade_raw: str | None) -> str | None:
    if score is None:
        return grade_raw
    if grade_raw == "insufficient_data":
        return grade_raw
    return score_to_grade(score)


def barcode_from_image(url: str | None) -> str | None:
    if not url:
        return None
    m = re.search(r"/(\d{12,13})_", url)
    return m.group(1) if m else None


def load_bsip1_index(source: pathlib.Path) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    if not source.exists():
        return idx
    for p in source.glob("bsip1_*.json"):
        if "audit" in p.name:
            continue
        try:
            data = load_product(p)
            bc = str(data.get("barcode") or "")
            if bc:
                idx[bc] = data
        except Exception:
            pass
    return idx


def find_yogurt_bsip1(product_id: str, name: str, pool: list[dict]) -> dict | None:
    hints = YOGURT_NAME_HINTS.get(product_id, [])
    name_l = name.lower()
    best = None
    best_hits = 0
    for p in pool:
        pn = (p.get("canonical_name_he") or "").lower()
        hits = sum(1 for h in hints if h.lower() in pn or h.lower() in name_l)
        if hits > best_hits:
            best_hits = hits
            best = p
    return best if best_hits >= 2 else None


def update_bottom_line(text: str | None, old_score, new_score, old_grade, new_grade) -> str | None:
    if not text or new_score is None or new_grade is None:
        return text
    pattern = r"^\d+(?:\.\d+)?/[A-E]:"
    replacement = f"{new_score}/{new_grade}:"
    if re.match(pattern, text):
        return re.sub(pattern, replacement, text, count=1)
    return text


def rescore_snacks(old_snap: list) -> list:
    corpus = json.loads(SNACKS_FRONTEND.read_text(encoding="utf-8"))
    bsip1 = load_bsip1_index(SNACKS_BSIP1)
    changes = []

    for p in corpus["products"]:
        old_score, old_grade = p.get("score"), p.get("grade")
        bc = barcode_from_image(p.get("imageUrl"))
        src = bsip1.get(bc or "")
        if not src:
            changes.append({"id": p["id"], "name": p["name"], "old": (old_score, old_grade), "new": (old_score, old_grade), "note": "no BSIP1"})
            continue
        result = run_simple_pipeline(src)
        new_score = round_score(result.get("final_score_estimate"))
        new_grade = grade_from_score(new_score, result.get("grade_estimate"))
        p["score"] = new_score
        p["grade"] = new_grade
        if p.get("expansion", {}).get("bottomLine"):
            p["expansion"]["bottomLine"] = update_bottom_line(
                p["expansion"]["bottomLine"], old_score, new_score, old_grade, new_grade
            )
        changes.append({"id": p["id"], "name": p["name"], "old": (old_score, old_grade), "new": (new_score, new_grade)})

    corpus["products"].sort(key=lambda x: x.get("score") or 0, reverse=True)
    corpus["_meta"]["generated"] = f"{TODAY}T00:00:00Z"
    corpus["_meta"]["production_pass"] = (
        (corpus["_meta"].get("production_pass") or "")
        + f" R-01–R-05 recalibration rescore {TODAY}: BSIP2 engine patch + full snacks re-run."
    )
    SNACKS_FRONTEND.write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changes


def rescore_bread(old_snap: list) -> list:
    corpus = json.loads(BREAD_FRONTEND.read_text(encoding="utf-8"))
    raw_products = json.loads(BREAD_RAW.read_text(encoding="utf-8"))
    raw_by_bc = {str(r.get("barcode")): r for r in raw_products if r.get("barcode")}
    changes = []

    for p in corpus["products"]:
        old_score, old_grade = p.get("score"), p.get("grade")
        bc = p["id"].replace("shufersal_", "")
        raw = raw_by_bc.get(bc)
        if not raw:
            changes.append({"id": p["id"], "name": p["name"], "old": (old_score, old_grade), "new": (old_score, old_grade), "note": "no raw"})
            continue
        prod = normalize_to_bsip1(raw)
        result = run_simple_pipeline(prod)
        new_score = round_score(result.get("final_score_estimate"))
        new_grade = grade_from_score(new_score, result.get("grade_estimate"))
        p["score"] = new_score
        p["grade"] = new_grade
        if p.get("expansion", {}).get("bottomLine"):
            p["expansion"]["bottomLine"] = update_bottom_line(
                p["expansion"]["bottomLine"], old_score, new_score, old_grade, new_grade
            )
        changes.append({"id": p["id"], "name": p["name"], "old": (old_score, old_grade), "new": (new_score, new_grade)})

    corpus["products"].sort(key=lambda x: x.get("score") or 0, reverse=True)
    corpus["_meta"]["generated"] = f"{TODAY}T00:00:00Z"
    corpus["_meta"]["production_pass"] = (
        (corpus["_meta"].get("production_pass") or "")
        + f" R-01–R-05 recalibration rescore {TODAY}: BSIP2 engine patch + bread re-run."
    )
    BREAD_FRONTEND.write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changes


def rescore_milk() -> list:
    page = json.loads(MILK_FRONTEND.read_text(encoding="utf-8"))
    bsip1 = load_bsip1_index(MILK_BSIP1)
    changes = []

    for p in page["products"]:
        old_score, old_grade = p.get("score"), p.get("grade")
        bc = str(p.get("barcode") or "")
        src = bsip1.get(bc)
        if not src:
            changes.append({"id": bc, "name": p.get("shortName"), "old": (old_score, old_grade), "new": (old_score, old_grade), "note": "no BSIP1"})
            continue
        result = run_simple_pipeline(src)
        new_score = round_score(result.get("final_score_estimate"))
        new_grade = grade_from_score(new_score, result.get("grade_estimate"))
        p["score"] = new_score
        p["grade"] = new_grade
        changes.append({"id": bc, "name": p.get("shortName"), "old": (old_score, old_grade), "new": (new_score, new_grade)})

    page["products"].sort(key=lambda x: x.get("score") or 0, reverse=True)
    page["generated_at"] = TODAY
    page["recalibration_pass"] = f"R-01–R-05 BSIP2 rescore {TODAY}"
    MILK_FRONTEND.write_text(json.dumps(page, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changes


def rescore_yogurts() -> list:
    corpus = json.loads(YOGURTS_FRONTEND.read_text(encoding="utf-8"))
    pool = load_batch(YOGURTS_BSIP1) if YOGURTS_BSIP1.exists() else []
    changes = []

    for p in corpus["products"]:
        old_score, old_grade = p.get("score"), p.get("grade")
        src = find_yogurt_bsip1(p["id"], p["name"], pool)
        if not src:
            changes.append({"id": p["id"], "name": p["name"], "old": (old_score, old_grade), "new": (old_score, old_grade), "note": "no BSIP1 match"})
            continue
        result = run_simple_pipeline(src)
        new_score = round_score(result.get("final_score_estimate"))
        new_grade = grade_from_score(new_score, result.get("grade_estimate"))
        p["score"] = new_score
        p["grade"] = new_grade
        if p.get("expansion", {}).get("bottomLine"):
            p["expansion"]["bottomLine"] = update_bottom_line(
                p["expansion"]["bottomLine"], old_score, new_score, old_grade, new_grade
            )
        changes.append({"id": p["id"], "name": p["name"], "old": (old_score, old_grade), "new": (new_score, new_grade), "bsip1": src.get("canonical_name_he")})

    corpus["products"].sort(key=lambda x: x.get("score") or 0, reverse=True)
    corpus["_meta"]["generated"] = f"{TODAY}T00:00:00Z"
    corpus["_meta"]["version"] = "v1-bsip2-rescore"
    corpus["_meta"]["scope_note"] = "מדגם מדף ישראלי — ציונים מ-BSIP2 לאחר R-01–R-05"
    corpus["_meta"]["production_pass"] = f"R-01–R-05 recalibration {TODAY}: BSIP2 engine rescore (yogurt BSIP1 name match)"
    YOGURTS_FRONTEND.write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changes


def pick_examples(changes: list, corpus_key: str = "products") -> dict:
    scored = [c for c in changes if c["new"][0] is not None]
    if not scored:
        return {}
    scored.sort(key=lambda x: x["new"][0], reverse=True)
    mid = scored[len(scored) // 2]
    return {"strongest": scored[0], "middle": mid, "weaker": scored[-1]}


def write_docs(all_changes: dict) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)

    summary = [
        "# Implemented Recalibration Summary",
        "",
        f"**Date:** {TODAY}",
        "",
        "## Engine changes (BSIP2 proto_v0)",
        "",
        "| Rule | Implementation |",
        "|---|---|",
        "| R-01 | NOVA3 cap 82 → 87 in `constants.py` + dynamic lookup in `score_engine.py` |",
        "| R-02 | +8 direct fermentation bonus (NOVA ≤ 3) before guardrail caps |",
        "| R-03 | Fiber ND ceiling 85 → 95 at ≥12g/100g |",
        "| R-04 | `product_type_dairy` signal + SC-2-equivalent sugar cap relief |",
        "| R-05 | `yogurt` calorie density table + router subtype routing |",
        "",
        "## Frontend corpora updated",
        "",
        "- `src/data/comparisons/snacks_frontend_v2.json`",
        "- `src/data/comparisons/bread_frontend_v2.json`",
        "- `src/data/comparisons/yogurts_frontend_v1.json`",
        "- `src/data/milk-comparison.json`",
        "",
        "## Rescore runner",
        "",
        "`C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\rescore_mvp_frontend_v1.py`",
        "",
    ]
    (DOCS / "implemented_recalibration_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    ba_lines = ["# Before / After Scores", "", f"**Date:** {TODAY}", ""]
    for cat, changes in all_changes.items():
        ex = pick_examples(changes)
        ba_lines.append(f"## {cat.title()}")
        ba_lines.append("")
        ba_lines.append("| Role | Product | OLD SCORE | NEW SCORE | OLD GRADE | NEW GRADE |")
        ba_lines.append("|---|---|---:|---:|---|---|")
        for role in ("strongest", "middle", "weaker"):
            e = ex.get(role)
            if not e:
                continue
            os, og = e["old"]
            ns, ng = e["new"]
            ba_lines.append(f"| {role} | {e['name']} | {os} | {ns} | {og} | {ng} |")
        ba_lines.append("")
    (DOCS / "before_after_scores.md").write_text("\n".join(ba_lines) + "\n", encoding="utf-8")

    reg = [
        "# Regenerated Category Outputs",
        "",
        f"**Date:** {TODAY}",
        "",
        "## Pipeline",
        "",
        "BSIP2 engine (patched) → `rescore_mvp_frontend_v1.py` → frontend JSON → Next.js static import → comparison pages",
        "",
        "## Change counts",
        "",
    ]
    for cat, changes in all_changes.items():
        changed = sum(1 for c in changes if c["old"] != c["new"])
        reg.append(f"- **{cat}:** {changed}/{len(changes)} products with score or grade change")
    reg.append("")
    (DOCS / "regenerated_category_outputs.md").write_text("\n".join(reg) + "\n", encoding="utf-8")

    files = [
        "# Files Changed — Recalibration",
        "",
        "## BSIP2 engine",
        "- `C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\constants.py`",
        "- `C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\score_engine.py`",
        "- `C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\signal_extractor.py`",
        "- `C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\rescore_mvp_frontend_v1.py` (new)",
        "",
        "## Frontend corpora",
        "- `src/data/comparisons/snacks_frontend_v2.json`",
        "- `src/data/comparisons/bread_frontend_v2.json`",
        "- `src/data/comparisons/yogurts_frontend_v1.json`",
        "- `src/data/milk-comparison.json`",
        "",
        "## Docs",
        "- `docs/implemented_recalibration_summary.md`",
        "- `docs/before_after_scores.md`",
        "- `docs/regenerated_category_outputs.md`",
        "- `docs/files_changed.md`",
        "",
    ]
    (DOCS / "files_changed.md").write_text("\n".join(files) + "\n", encoding="utf-8")


def main():
    snapshot = {
        "snacks": json.loads(SNACKS_FRONTEND.read_text(encoding="utf-8")),
        "bread": json.loads(BREAD_FRONTEND.read_text(encoding="utf-8")),
        "yogurts": json.loads(YOGURTS_FRONTEND.read_text(encoding="utf-8")),
        "milk": json.loads(MILK_FRONTEND.read_text(encoding="utf-8")),
    }
    snap_path = DOCS / f"pre_recalibration_snapshot_{TODAY}.json"
    DOCS.mkdir(parents=True, exist_ok=True)
    snap_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Snapshot: {snap_path}")

    all_changes = {
        "snacks": rescore_snacks([]),
        "bread": rescore_bread([]),
        "milk": rescore_milk(),
        "yogurts": rescore_yogurts(),
    }

    for cat, changes in all_changes.items():
        changed = [c for c in changes if c["old"] != c["new"]]
        print(f"\n=== {cat}: {len(changed)}/{len(changes)} changed ===")
        for c in changed[:5]:
            print(f"  {c['name']}: {c['old']} -> {c['new']}")

    write_docs(all_changes)
    print("\nDocs written to docs/")


if __name__ == "__main__":
    main()
