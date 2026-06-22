"""
TASK-373 / P284 — Snacks whole-food scoring relief + calorie backstop OFF-vs-ON table.

Scores the 21-product snacks shelf from BSIP1 inputs at BARI_SNACK_WHOLEFOOD_V1 off/on,
asserts OFF matches published snacks_frontend_v5.json scores, and runs a cross-category guard.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
SRC_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

BSIP1_SNACKS_DIR = REPO_ROOT / "03_operations/bsip1/score_bars_task362_20260620_150421/output"
FRONTEND_JSON = REPO_ROOT / "bari-web/src/data/comparisons/snacks_frontend_v5.json"
VERIFY_OUT = REPO_ROOT / "02_products/snack_bars/task373_snacks_relief_verification.json"

CROSS_CATEGORY_SAMPLES = {
    "hummus": (REPO_ROOT / "03_operations/bsip1/run_hummus_001/output", 4),
    "cheese_spreads": (REPO_ROOT / "03_operations/bsip1/run_cheese_001/output", 3),
    "cereals": (REPO_ROOT / "03_operations/bsip1/run_cereals_001/output", 3),
}

ENGINE_MODULES = [
    "signal_extractor", "score_engine", "nova_proxy", "trace_writer",
    "router_v2", "evaluation_scope", "input_loader", "constants",
    "structural_classifier",
]


def _reload_engine(flag_on: bool):
    os.environ["BARI_SNACK_WHOLEFOOD_V1"] = "on" if flag_on else "off"
    for name in ENGINE_MODULES:
        sys.modules.pop(name, None)
    from score_engine import score_product
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    return score_product, extract_signals, classify_category, infer_nova, assign_evaluation_scope


def _score_product(product: dict, flag_on: bool) -> dict:
    score_product, extract_signals, classify_category, infer_nova, assign_evaluation_scope = _reload_engine(flag_on)
    signals = extract_signals(product)
    cat_result = classify_category(product)
    nova_result = infer_nova(product, signals["L3_inferred_classifications"])
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    return score_product(product, signals, cat_result, nova_result, eval_result)


def _load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_bsip1(barcode: str) -> dict:
    path = BSIP1_SNACKS_DIR / f"bsip1_{barcode}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    return _load_json(path)


def _fixes_fired(off: dict, on: dict) -> str:
    fixes = []
    if off.get("sugar_context_class") != on.get("sugar_context_class"):
        fixes.append(f"fix1_sc:{off.get('sugar_context_class')}->{on.get('sugar_context_class')}")
    off_caps = {c.get("rule") for c in off.get("caps_applied", [])}
    on_caps = {c.get("rule") for c in on.get("caps_applied", [])}
    if "ISRAELI_RED_LABELS_2_PLUS" in off_caps and "ISRAELI_RED_LABELS_2_PLUS" not in on_caps:
        fixes.append("fix2_2plus_cap")
    off_hp = {p.get("rule") for p in off.get("penalties_applied", [])}
    on_hp = {p.get("rule") for p in on.get("penalties_applied", [])}
    if "HP_FAT_SUGAR_COMBO" in off_hp and "HP_FAT_SUGAR_COMBO" not in on_hp:
        fixes.append("fix2_hp_fat_sugar")
    if on.get("sugar_context_class") == "SC-2" and off.get("sugar_context_class") != "SC-2":
        fixes.append("fix1_sc2_caps")
    if not fixes:
        wf = on.get("wholefood_bar_relief") or {}
        if wf.get("passed"):
            fixes.append("fix2_predicate")
        elif on.get("final_score_estimate") != off.get("final_score_estimate"):
            fixes.append("other")
        else:
            fixes.append("none")
    return ",".join(fixes)


def _scores_match(engine_score, published_score, tol: float = 0.05) -> bool:
    if engine_score is None or published_score is None:
        return engine_score == published_score
    return abs(float(engine_score) - float(published_score)) <= tol



def _backstop_fields(on: dict) -> dict:
    wf = on.get("wholefood_bar_relief") or {}
    if not wf.get("passed") or wf.get("score_before_backstop") is None:
        return {"before_bs": "", "after_bs": "", "backstop": "", "low_c": ""}
    from score_engine import score_to_grade
    before = wf.get("score_before_backstop")
    after = wf.get("score_after_backstop")
    return {
        "before_bs": f"{before}/{score_to_grade(before)}",
        "after_bs": f"{after}/{on.get('grade_estimate')}",
        "backstop": wf.get("calorie_backstop_ceiling", ""),
        "low_c": wf.get("low_c_exception_met", ""),
    }


def _grade_distribution(rows: list[dict], key: str) -> dict:
    grades = [str(r.get(key, "")).split("/")[-1] for r in rows if r.get(key)]
    grades = [g for g in grades if g and g != "None"]
    if not grades:
        return {}
    counts = Counter(grades)
    return {
        "histogram": dict(sorted(counts.items())),
        "n": len(grades),
        "most_common": counts.most_common(1)[0],
    }

def _print_table(rows: list[dict]):
    headers = [
        "id", "name_he", "barcode", "OFF", "ON", "before_bs", "after_bs",
        "backstop", "low_c", "delta", "predicate", "fixes",
    ]
    widths = [max(len(h), *(len(str(r.get(h, ""))) for r in rows)) for h in headers]
    sep = " | "
    print(sep.join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(sep.join(str(r.get(h, "")).ljust(widths[i]) for i, h in enumerate(headers)))


def main() -> int:
    frontend = _load_json(FRONTEND_JSON)
    products = frontend.get("products") or []
    if len(products) != 21:
        print(f"WARN: expected 21 snacks products, got {len(products)}")

    rows = []
    published_mismatches = []

    for p in products:
        barcode = p["barcode"]
        product = _load_bsip1(barcode)
        off = _score_product(product, False)
        on = _score_product(product, True)
        off_score = off.get("final_score_estimate")
        on_score = on.get("final_score_estimate")
        pub_score = p.get("score")
        pub_grade = p.get("grade")
        off_grade = off.get("grade_estimate")
        on_grade = on.get("grade_estimate")
        delta = None if off_score is None or on_score is None else round(on_score - off_score, 2)
        predicate = (on.get("wholefood_bar_relief") or {}).get("passed", False)
        if not _scores_match(off_score, pub_score) or off_grade != pub_grade:
            published_mismatches.append({
                "id": p.get("id"),
                "barcode": barcode,
                "published": f"{pub_score}/{pub_grade}",
                "off": f"{off_score}/{off_grade}",
            })
        bs = _backstop_fields(on)
        rows.append({
            "id": p.get("id", ""),
            "name_he": p.get("name_he") or p.get("name", ""),
            "barcode": barcode,
            "OFF": f"{off_score}/{off_grade}",
            "ON": f"{on_score}/{on_grade}",
            **bs,
            "delta": delta if delta is not None else "",
            "predicate": predicate,
            "fixes": _fixes_fired(off, on),
        })

    on_dist = _grade_distribution(rows, "ON")

    print("=== TASK-373 snacks shelf OFF vs ON (P284 backstop) ===")
    _print_table(rows)
    if on_dist:
        hist = on_dist["histogram"]
        n = on_dist["n"]
        mc = on_dist["most_common"]
        print()
        print(f"ON grade distribution: {hist} (n={n}, most_common={mc})")

    if published_mismatches:
        print("\nOFF=published: FAIL")
        for m in published_mismatches:
            print(f"  {m['id']} {m['barcode']}: published={m['published']} off={m['off']}")
        pub_ok = False
    else:
        print("\nOFF=published: PASS (21/21)")
        pub_ok = True

    cross_changes = []
    cross_total = 0
    print("\n=== Cross-category guard (OFF vs ON) ===")
    for cat_name, (src_dir, limit) in CROSS_CATEGORY_SAMPLES.items():
        if not src_dir.exists():
            print(f"{cat_name}: SKIPPED (no BSIP1 dir {src_dir})")
            continue
        files = sorted(src_dir.glob("bsip1_*.json"))[:limit]
        for fpath in files:
            cross_total += 1
            product = _load_json(fpath)
            off = _score_product(product, False)
            on = _score_product(product, True)
            if (off.get("final_score_estimate") != on.get("final_score_estimate")
                    or off.get("grade_estimate") != on.get("grade_estimate")):
                cross_changes.append({
                    "category": cat_name,
                    "barcode": product.get("barcode"),
                    "name": product.get("canonical_name_he", ""),
                    "off": f"{off.get('final_score_estimate')}/{off.get('grade_estimate')}",
                    "on": f"{on.get('final_score_estimate')}/{on.get('grade_estimate')}",
                })
        print(f"{cat_name}: sampled {len(files)} products")

    if cross_changes:
        print("Cross-category guard: FAIL — score/grade changed under flag ON:")
        for c in cross_changes:
            print(f"  [{c['category']}] {c['barcode']} {c['name']}: {c['off']} -> {c['on']}")
        cross_ok = False
    else:
        print(f"Cross-category guard: PASS — 0/{cross_total} non-snack products changed")
        cross_ok = True

    VERIFY_OUT.parent.mkdir(parents=True, exist_ok=True)
    VERIFY_OUT.write_text(json.dumps({
        "rows": rows,
        "on_grade_distribution": on_dist.get("histogram", {}),
        "published_assertion": "PASS" if pub_ok else "FAIL",
        "published_mismatches": published_mismatches,
        "cross_category_guard": "PASS" if cross_ok else "FAIL",
        "cross_category_changes": cross_changes,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nVerification artifact: {VERIFY_OUT}")

    return 0 if pub_ok and cross_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
