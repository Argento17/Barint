"""Replay canonical BSIP0 captures and guard the committed flat baseline."""
from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "03_operations/bsip0/manifest/capture_manifest.json"
BASELINE = ROOT / "03_operations/bsip0/manifest/replay_baseline.jsonl"
PARSER = ROOT / "03_operations/bsip0/scrape/_shared/bsip0_nutrition.py"
RAW_KEYS = {"energy": "energy_kcal_raw", "fat": "fat_raw", "saturated_fat": "saturated_fat_raw", "trans_fat": "trans_fat_raw", "cholesterol": "cholesterol_raw", "sodium": "sodium_raw", "carbs": "carbs_raw", "sugar": "sugar_raw", "fiber": "fiber_raw", "protein": "protein_raw"}
NUMERIC_KEYS = {"energy": "energy_kcal", "fat": "fat_g", "saturated_fat": "fat_saturated_g", "trans_fat": "fat_trans_g", "cholesterol": "cholesterol_mg", "sodium": "sodium_mg", "carbs": "carbohydrates_g", "sugar": "sugars_g", "fiber": "dietary_fiber_g", "protein": "protein_g"}
BOUNDS = {"energy": (0, 1000), "fat": (0, 100), "saturated_fat": (0, 100), "trans_fat": (0, 100), "cholesterol": (0, 3000), "sodium": (0, 10000), "carbs": (0, 100), "sugar": (0, 100), "fiber": (0, 100), "protein": (0, 100)}

def assert_write_path(path: Path):
    if path.resolve() != BASELINE.resolve(): raise AssertionError(f"write outside TASK-601 boundary: {path}")

def load_parser():
    spec = importlib.util.spec_from_file_location("task601_bsip0_nutrition", PARSER)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def dereference(record):
    value = json.loads((ROOT / record["capture_file"]).read_text(encoding="utf-8"))
    for token in record["object_path"].lstrip("/").split("/"):
        if token: value = value[int(token)] if isinstance(value, list) else value[token.replace("~1", "/").replace("~0", "~")]
    return value["nutrition_raw_source"]

def flags(raw, parsed, field, numeric):
    text = str(raw or ""); result = []
    if re.search(r"\d,\d{3}(?:\D|$)", text): result.append("comma_ambiguous")
    units = set(re.findall(r"\b(?:mg|g|kcal|kj)\b", text.lower()))
    if len(units) > 1: result.append("unit_token_conflict")
    if raw not in (None, "") and parsed is None: result.append("unrecoverable")
    lo, hi = BOUNDS[field]
    if numeric is not None and not lo <= numeric <= hi: result.append("out_of_bound")
    return result

def replay():
    parser = load_parser(); manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = []
    for rec in manifest["records"]:
        if not rec["canonical"]: continue
        source = dereference(rec); classified = parser.parse_nutrition_rows(source.get("rows", []))
        raw_panel = {RAW_KEYS[k]: v for k, v in classified.items() if k in RAW_KEYS}
        numeric = parser.parse_nutrition_numeric(raw_panel)
        basis = source.get("selection", {}).get("selected_basis") or source.get("basis") or "unknown"
        for field, raw_key in RAW_KEYS.items():
            raw = raw_panel.get(raw_key); parsed = numeric.get(NUMERIC_KEYS[field])
            rows.append({"retailer": rec["retailer"], "gtin": rec["gtin"], "capture_file": rec["capture_file"], "basis": basis, "field": field, "raw_value": raw, "parsed_value": parsed, "flags": flags(raw, parsed, field, parsed)})
    return rows

def lines(rows): return [json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in rows]

def main():
    check = argparse.ArgumentParser(); check.add_argument("--check", action="store_true"); check.add_argument("--self-check", action="store_true"); args = check.parse_args()
    actual = lines(replay())
    if args.self_check:
        decoded = [json.loads(line) for line in actual]
        brined = next(row for row in decoded if row["gtin"] == "3075805" and row["field"] == "sodium")
        cereal = next(row for row in decoded if row["gtin"] == "5010029000061" and row["field"] == "fat")
        assert brined["raw_value"] == "1,628 מג" and "comma_ambiguous" in brined["flags"], brined
        assert cereal["raw_value"] == "2" and cereal["flags"] == [], cereal
        print("known-capture self-check passed: 3075805 sodium comma_ambiguous; 5010029000061 fat no flags")
        return 0
    if args.check:
        expected = BASELINE.read_text(encoding="utf-8").splitlines(keepends=True) if BASELINE.exists() else []
        if actual != expected:
            print("replay baseline drift:")
            print("".join(difflib.unified_diff(expected, actual, fromfile="committed-baseline", tofile="replay")), end="")
            return 2
        print(f"replay baseline check passed: {len(actual)} rows"); return 0
    assert_write_path(BASELINE); BASELINE.write_text("".join(actual), encoding="utf-8")
    print(f"replay baseline written: {len(actual)} rows"); return 0
if __name__ == "__main__": raise SystemExit(main())
