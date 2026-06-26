#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TASK-410 — Copy-preserving D4 activation regen for juices.

Pattern from TASK-393 build_deploy_merge.py:
  1. Start from LIVE juices_frontend_v3.json (17 products, real copy)
  2. Compute pure D4 delta for each product (s_on - s_off = -penalty)
  3. Apply delta to committed score: new_score = committed + delta
  4. Re-derive grade from new score
  5. Re-sort and re-rank
  6. Carry all other fields verbatim (insightLine, rowVerdict, expansion, etc.)
  7. FLAG the 3 movers for two-gate copy review (do NOT author copy)

Output: juices_task410_staged.json in this directory.

Produces run record with: run_id, date, config hash, artifact paths.
"""
from __future__ import annotations
import hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
WORKTREE = Path(__file__).resolve().parents[4]   # C:\Bari\.claude\worktrees\task410
REPO_MAIN = Path("C:/Bari")  # for BSIP1 data (stays in main tree, read-only)

SCORE_SRC = WORKTREE / "03_operations/bsip2/proto_v0/src"
# Use the WORKTREE copy of juices JSON (pre-D4 scores at d62331554 / origin/master).
# The main tree at C:\Bari has newer commits with D4 already applied — do NOT use it.
LIVE_JSON  = WORKTREE / "bari-web/src/data/comparisons/juices_frontend_v3.json"
BSIP1_DIR  = REPO_MAIN / "02_products/juices/bsip1_outputs"
STAGING    = Path(__file__).resolve().parent
OUT_JSON   = STAGING / "juices_task410_staged.json"
# Deploy target is the worktree's bari-web (not the main tree!)
DEPLOY_JSON = WORKTREE / "bari-web/src/data/comparisons/juices_frontend_v3.json"
RUN_RECORD  = STAGING / "run_record_task410.json"

sys.path.insert(0, str(SCORE_SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Engine import (D4 off at import time) ─────────────────────────────────────
os.environ.pop("BARI_D4_SCORE_V1", None)
from score_engine import compute_d4_score_penalty, detect_additives_d4  # noqa: E402
from constants import GLASSBOX_W2_ADDITIVES, D4_SCORE_CAP  # noqa: E402

# ── Grade boundary ────────────────────────────────────────────────────────────
GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

def score_to_grade(score: float) -> str:
    for grade, threshold in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "E"

# ── Load BSIP1 ingredients ───────────────────────────────────────────────────
def _load_bsip1_ingredients() -> dict[str, str]:
    index: dict[str, str] = {}
    if not BSIP1_DIR.exists():
        print(f"WARN: BSIP1 dir not found: {BSIP1_DIR}")
        return index
    for f in BSIP1_DIR.glob("*.json"):
        try:
            prod = json.loads(f.read_bytes().decode("utf-8"))
            bc = str(prod.get("barcode", "") or "").strip()
            ing = (prod.get("ingredients_text_he") or prod.get("ingredients_raw") or "")
            if bc and ing and len(ing) > 3 and bc not in index:
                index[bc] = ing
        except Exception:
            pass
    return index

# ── Pure D4 penalty ──────────────────────────────────────────────────────────
def _compute_pure_d4_penalty(ing: str) -> tuple[int, str, list]:
    """Returns (penalty_pts, trace_note, findings_list). ECS stub = 0."""
    if not ing:
        return 0, "D4_SCORE: no ingredient text", []
    l3_stub = {"emulsifier_complexity_penalty": 0}
    penalty, note = compute_d4_score_penalty(ing, l3_stub)
    findings = detect_additives_d4(ing)
    return penalty, note, findings

# ── Re-rank (score-desc, competition ranking) ─────────────────────────────────
def _rerank(products: list[dict]) -> None:
    if not products or not all("rank" in p for p in products):
        return
    products.sort(key=lambda p: -(float(p.get("score", 0) or 0)))
    for p in products:
        higher = sum(1 for q in products
                     if float(q.get("score", 0) or 0) > float(p.get("score", 0) or 0))
        p["rank"] = higher + 1

# ── SHA-256 ───────────────────────────────────────────────────────────────────
def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

# ── PREFLIGHT: E224 entry unchanged assertion ──────────────────────────────────
def _preflight_e224():
    e224 = GLASSBOX_W2_ADDITIVES["E224"]
    expected_patterns = [
        "פוטסיום מטביסולפיט", "אשלגן מטביסולפיט", "מטביסולפיט אשלגן",
        "סולפיט", "סולפיטים", "תרכובות גופרית", "E224", "e224",
    ]
    assert e224["tier"] == "contested", "E224 tier changed — STOP"
    assert e224["score_eligible"] is True, "E224 score_eligible changed — STOP"
    assert e224["cosmetic_mup"] is False, "E224 cosmetic_mup changed — STOP"
    assert e224["match_patterns_he"] == expected_patterns, (
        f"E224 match_patterns_he changed — STOP. Got: {e224['match_patterns_he']}"
    )
    print("PREFLIGHT PASS: E224 entry unchanged (tier, score_eligible, cosmetic_mup, patterns)")

# ── Main ─────────────────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 70)
    print("TASK-410: Juices D4 copy-preserving regen")
    print(f"Run timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # Preflight
    _preflight_e224()

    # Load live JSON
    print(f"\nLoading live JSON: {LIVE_JSON}")
    live_data = json.loads(LIVE_JSON.read_bytes().decode("utf-8"))
    live_products = live_data["products"]
    print(f"  Live products: {len(live_products)}")

    # Load BSIP1 ingredients
    print(f"\nLoading BSIP1 ingredients from: {BSIP1_DIR}")
    ing_index = _load_bsip1_ingredients()
    print(f"  BSIP1 indexed: {len(ing_index)} barcodes")

    # Process each product
    print("\nComputing D4 deltas...")
    import copy
    output = copy.deepcopy(live_data)
    output_products = output["products"]

    movers = []        # products with penalty > 0
    grade_changes = [] # products where grade changed
    flagged_movers = []  # movers that are in displayed set (need two-gate copy)
    no_ing = []

    for i, prod in enumerate(live_products):
        bc = str(prod.get("barcode", "") or "").strip()
        name = prod.get("name", bc)
        committed_score = prod.get("score")
        committed_grade = prod.get("grade")

        if committed_score is None:
            continue

        committed_score_f = float(committed_score)
        ing = ing_index.get(bc, "")

        if not ing:
            no_ing.append(bc)
            continue

        # Compute pure D4 penalty
        penalty, note, findings = _compute_pure_d4_penalty(ing)
        delta = -penalty  # always <= 0

        if penalty > 0:
            new_score = round(committed_score_f + delta, 1)
            new_grade = score_to_grade(new_score)
            grade_changed = (new_grade != committed_grade)

            movers.append({
                "barcode": bc,
                "name": name,
                "committed_score": committed_score_f,
                "committed_grade": committed_grade,
                "new_score": new_score,
                "new_grade": new_grade,
                "delta": delta,
                "grade_changed": grade_changed,
                "d4_note": note,
                "contested_fired": [f["e_number"] for f in findings
                                    if f["tier"] == "contested"
                                    and GLASSBOX_W2_ADDITIVES.get(f["e_number"], {}).get("score_eligible")],
            })

            if grade_changed:
                grade_changes.append(bc)
                print(f"  GRADE CHANGE: {bc} {name[:30]} {committed_grade}→{new_grade}")

            # Update the output product (score + grade only; carry all copy verbatim)
            out_p = output_products[i]
            out_p["score"] = new_score
            out_p["grade"] = new_grade
            # FLAG for two-gate copy — do NOT author copy
            out_p["_d4_copy_flag"] = {
                "status": "FLAGGED_FOR_TWO_GATE",
                "reason": f"Score moved by D4 sulphite activation: {committed_score_f}→{new_score} ({committed_grade}, delta={delta}). Copy may need update.",
                "contested_fired": movers[-1]["contested_fired"],
                "task": "TASK-410",
            }
            flagged_movers.append({
                "barcode": bc,
                "name": name,
                "old_score": committed_score_f,
                "new_score": new_score,
                "grade": new_grade,
                "delta": delta,
            })
        else:
            # No change — verify no unexpected D4 effect
            pass

    # Re-rank
    print("\nRe-ranking...")
    _rerank(output_products)

    # Update _meta
    output["_meta"]["run_id"] = "run_juices_task410_d4on"
    output["_meta"]["task410_d4_activation"] = {
        "flag_change": "BARI_D4_SCORE_V1=on (juices D4 sulphite activation)",
        "products_moved": len(movers),
        "grade_changes": grade_changes,
        "flagged_movers": flagged_movers,
        "no_ingredient_text": no_ing,
        "d4_note": "E220 sulphite-family + dedup via sulphite_family_key; 0 grade changes expected",
    }

    # Write staged output
    STAGING.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_bytes(json.dumps(output, ensure_ascii=False, indent=2).encode("utf-8"))
    print(f"\nStaged output: {OUT_JSON}")

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Live products: {len(live_products)}")
    print(f"Products with D4 penalty: {len(movers)}")
    print(f"Grade changes: {len(grade_changes)}")
    print(f"No ingredient text: {len(no_ing)}")
    print()
    print("MOVERS (flagged for two-gate copy):")
    for m in movers:
        flag = " *** GRADE CHANGE ***" if m["grade_changed"] else ""
        print(f"  {m['barcode']} | {m['name'][:35]} | "
              f"{m['committed_score']}→{m['new_score']} ({m['committed_grade']}→{m['new_grade']}) "
              f"delta={m['delta']} | fired={m['contested_fired']}{flag}")

    print()
    print("DISPLAY SET INTEGRITY:")
    print(f"  Input products: {len(live_products)}")
    print(f"  Output products: {len(output_products)}")
    assert len(output_products) == len(live_products), "DISPLAY SET CHANGED — FAIL"
    print(f"  PASS: display set = {len(live_products)} (unchanged)")

    # Check no PENDING_COPY
    pending_count = 0
    for p in output_products:
        for field in ["insightLine", "rowVerdict", "expansion"]:
            val = p.get(field)
            if isinstance(val, str) and "PENDING" in val:
                pending_count += 1
            elif isinstance(val, dict):
                for v in val.values():
                    if isinstance(v, str) and "PENDING" in v:
                        pending_count += 1
    print(f"  PENDING_COPY count: {pending_count}")
    if pending_count > 0:
        print(f"  WARN: {pending_count} PENDING_COPY fields detected")
    else:
        print("  PASS: no PENDING_COPY")

    # Run record
    run_record = {
        "run_id": "run_juices_task410_d4on",
        "task": "TASK-410",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config_sha256": _sha256(WORKTREE / "03_operations/page_generator/configs/juices.json"),
        "live_json_sha256": _sha256(LIVE_JSON),
        "output_sha256": _sha256(OUT_JSON),
        "output_path": str(OUT_JSON),
        "products_in": len(live_products),
        "products_out": len(output_products),
        "movers": movers,
        "grade_changes": grade_changes,
        "flagged_for_two_gate": flagged_movers,
        "no_ingredient_text": no_ing,
    }
    RUN_RECORD.write_bytes(json.dumps(run_record, ensure_ascii=False, indent=2).encode("utf-8"))
    print(f"\nRun record: {RUN_RECORD}")

    return 0 if len(grade_changes) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
