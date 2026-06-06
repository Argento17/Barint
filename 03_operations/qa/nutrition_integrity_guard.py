"""
COV-007 — Permanent, blocking nutrition data-integrity guard (COV-006 successor).

WHY THIS EXISTS (TASK-192, owner directive 2026-06-05 — 3rd occurrence)
-----------------------------------------------------------------------
The "פחות מ 0.5" total-fat mis-capture has now shipped three times. EV-029/EV-026
added a *shared parser* (`_shared/bsip0_nutrition.py`) and a *guard*
(`nutrition_implausible` / COV-006 in `run_qa.py`). The bug recurred in
run_cereals_005 anyway. This module closes BOTH gaps that let it through:

  GAP 1 — WIRING. COV-006's logic was sound but it was *not gated on every build*.
    Only the cheese + butter scrapers ever called `composition_nutrition_report`;
    the cereals / maadanim / hummus / yogurt scrapers import `nutrition_implausible`
    and never invoke it, and NO BSIP1 builder calls any plausibility check. The
    cereals corpus therefore passed through scrape → BSIP1 → frontend with ZERO
    plausibility gating. `run_qa.py` COV-006 exists but is opt-in (`--category`)
    and was not run as a hard gate before the cereals frontend was published.

  GAP 2 — COVERAGE. COV-006's *unambiguous* signature is `saturated_fat > total_fat`.
    In the cereals case there is NO saturated row at all (113/113 empty), and the
    TOTAL fat row label itself carried the value "פחות מ 0.5". So the
    sat>total signature could never fire. COV-006's *second* signature
    (energy-vs-macro balance) WOULD have caught it (57/113 flagged, 50.4%), but
    because of GAP 1 it was never executed. This module adds the explicit
    "פחות-מ / < token landed in a TOTAL field" signature so the defect is caught
    even when no energy panel is present, and a sodium absurd-value gate.

WHAT THIS GUARD IS
------------------
A single, stage-agnostic, importable + CLI gate. It runs against any corpus stage:
  • BSIP0 raw       (per-product `nutrition.*_raw` strings, incl. "פחות מ" tokens)
  • BSIP1 output    (per-product `normalized_nutrition_per_100g` floats)
  • frontend JSON   (per-product `expansion.nutrition` floats)
It auto-detects the stage from the record shape, so the SAME gate code runs at
every hop. A corpus with ANY blocking finding above the fail threshold returns a
non-zero exit code → a build/promotion step that shells out to it cannot proceed.

SIGNATURES (all per-100g)
-------------------------
  S1  less_than_token_in_total   — a "פחות מ" / "<" token in a TOTAL field
                                    (fat / carbs / sugars / protein / sodium /
                                    energy). BLOCKING — totals must be real numbers;
                                    a "<N" bound belongs only to trace/saturated
                                    sub-rows, never to a parent total. This is the
                                    direct cereals signature and needs no energy.
  S2  sat_gt_total_fat           — saturated_fat > total_fat (EV-029 signature).
                                    BLOCKING — a sub-row overwrote the total.
  S3  fat_understated_vs_energy  — fat ≤ FAT_NEAR_ZERO_G and declared energy exceeds
                                    4·protein + 4·carbs + 9·fat by ≥ ENERGY_GAP_KCAL.
                                    BLOCKING — fat is understated, not genuinely low
                                    (legit low-fat high-carb cereals pass: carbs carry
                                    the energy, gap ≈ 0-8 kcal in real data).
  S4  sodium_absurd              — sodium > SODIUM_MAX_MG mg/100g. BLOCKING — a
                                    data-integrity failure (unit error / parse error).
  S5  canonical_integrity_flag   — the BSIP1 record carries an `_integrity` flag set by
                                    the canonical extraction layer (Data, TASK-192 /
                                    EV-046: `fat_is_less_than_bound` / `sat_gt_total_fat`).
                                    BLOCKING — interlock so the guard and the canonical
                                    parser can never disagree, and so a "<" bound on a
                                    BSIP1 total (where the raw string is gone) is still
                                    caught without depending on the energy balance.

THRESHOLDS — co-signed with Nutrition Agent (TASK-192, 2026-06-05)
------------------------------------------------------------------
  FAT_NEAR_ZERO_G  = 0.5   "פחות מ 0.5" is the recurring captured value; the bound
                            is ≤0.5 so a genuine 0.4 g declaration is still tested by
                            the energy balance (and passes when carbs carry energy).
  ENERGY_GAP_KCAL  = 50    Validated on the real cereals corpus: genuine low-fat
                            cornflakes show gap ≈ 0-8 kcal (pass); mis-captured
                            granola shows gap 120-124 kcal (fail). 50 is a wide,
                            unambiguous separation — no real product in the swept
                            corpora sits between 8 and 120.
  SODIUM_MAX_MG    = 2000  > 2000 mg/100g is implausible for any retail food except
                            pure table salt (≈39000) / bouillon — neither is a Bari
                            category. (For reference, soy sauce ≈ 5500; the highest
                            legitimate Bari item, a hard cheese, is ≈ 1200.)

  Re-baselining any threshold is a Nutrition-co-signed change (it can move what the
  gate flags). The energy-balance method is intentionally physics-based, not a flat
  per-category fat floor, so it needs no per-category tuning.

USAGE
-----
  # gate a single stage file/dir (exit 1 if blocking findings ≥ fail threshold):
  python nutrition_integrity_guard.py --path <file_or_dir>
  python nutrition_integrity_guard.py --path 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_*.json

  # programmatic (wire into a scraper/builder main()):
  from nutrition_integrity_guard import gate_corpus
  result = gate_corpus(products)            # products: list[dict]
  if not result["passed"]:
      raise SystemExit(f"COV-007 BLOCK: {result['summary']}")

This module has NO third-party dependencies (stdlib only) so any stage can import it.
"""
from __future__ import annotations

import argparse
import glob as _glob
import json
import re
import sys
from pathlib import Path

# ── Co-signed thresholds (Nutrition Agent, TASK-192) ────────────────────────────
FAT_NEAR_ZERO_G = 0.5
ENERGY_GAP_KCAL = 50.0
SODIUM_MAX_MG = 2000.0

# A finding at/above this share of the corpus is a SYSTEMIC parse defect and is
# always blocking. A SINGLE blocking finding is also blocking on its own for the
# token / sat>total / sodium signatures (those are never legitimate). The percentage
# only governs the energy-balance signature, which can have rare genuine outliers.
SYSTEMIC_FAIL_PCT = 5.0

# Tokens that must NEVER appear in a TOTAL field's raw value.
_LESS_THAN_RE = re.compile(r"פחות\s*מ|פחות|\bless than\b|<")

# Raw-string fields that are TOTALS (a "<N" bound here is always a defect).
# saturated_fat / trans are sub-rows and MAY legitimately read "פחות מ 0.5".
_TOTAL_RAW_FIELDS = (
    "energy_kcal_raw", "fat_raw", "carbs_raw", "sugar_raw",
    "protein_raw", "sodium_raw", "fiber_raw",
)


def _to_float(v):
    """Parse a raw Hebrew/EN nutrition value to a float bound. '<0.5'/'פחות מ 0.5' → 0.5."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v)
    s = (s.replace("פחות מ", "").replace("פחות", "").replace("<", "")
           .replace("גרם", "").replace('מ"ג', "").replace("מ”ג", "")
           .replace("mg", "").replace("kcal", "").replace("ק\"ג", "")
           .replace(",", ".").strip())
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group()) if m else None


def _has_less_than_token(v) -> bool:
    return bool(v) and isinstance(v, str) and bool(_LESS_THAN_RE.search(v))


# ── Stage detection + field extraction ──────────────────────────────────────────

def _extract(product: dict) -> dict:
    """Return a normalised view of one product's nutrition across all stages.

    Output keys: stage, name, raw (dict of *_raw strings if present),
    energy, fat, sat, protein, carbs, sugar, sodium, fiber (floats or None).
    """
    name = (product.get("name_he") or product.get("name")
            or product.get("canonical_name_he") or product.get("id") or "?")

    # BSIP0 raw: nutrition.{*_raw}
    raw = product.get("nutrition") if isinstance(product.get("nutrition"), dict) else {}
    is_bsip0 = any(k.endswith("_raw") for k in raw)

    # BSIP1: normalized_nutrition_per_100g
    nn = product.get("normalized_nutrition_per_100g")
    # frontend: expansion.nutrition
    exp = (product.get("expansion") or {}).get("nutrition") if isinstance(product.get("expansion"), dict) else None

    if is_bsip0:
        stage = "bsip0"
        return {
            "stage": stage, "name": name, "raw": raw,
            "energy": _to_float(raw.get("energy_kcal_raw")),
            "fat": _to_float(raw.get("fat_raw")),
            "sat": _to_float(raw.get("saturated_fat_raw")),
            "protein": _to_float(raw.get("protein_raw")),
            "carbs": _to_float(raw.get("carbs_raw")),
            "sugar": _to_float(raw.get("sugar_raw")),
            "sodium": _to_float(raw.get("sodium_raw")),
            "fiber": _to_float(raw.get("fiber_raw")),
        }
    if isinstance(nn, dict):
        return {
            "stage": "bsip1", "name": name, "raw": {},
            "energy": _to_float(nn.get("energy_kcal")),
            "fat": _to_float(nn.get("fat_g")),
            "sat": _to_float(nn.get("fat_saturated_g", nn.get("saturated_fat_g"))),
            "protein": _to_float(nn.get("protein_g")),
            "carbs": _to_float(nn.get("carbohydrates_g")),
            "sugar": _to_float(nn.get("sugars_g")),
            "sodium": _to_float(nn.get("sodium_mg")),
            "fiber": _to_float(nn.get("dietary_fiber_g")),
        }
    if isinstance(exp, dict):
        return {
            "stage": "frontend", "name": name, "raw": {},
            "energy": _to_float(exp.get("energyKcal")),
            "fat": _to_float(exp.get("fat")),
            "sat": _to_float(exp.get("saturatedFat")),   # not usually present in frontend
            "protein": _to_float(exp.get("protein")),
            "carbs": _to_float(exp.get("carbs", exp.get("carbohydrates"))),
            "sugar": _to_float(exp.get("sugar")),
            "sodium": _to_float(exp.get("sodium")),
            "fiber": _to_float(exp.get("fiber")),
        }
    return {"stage": "unknown", "name": name, "raw": {},
            "energy": None, "fat": None, "sat": None, "protein": None,
            "carbs": None, "sugar": None, "sodium": None, "fiber": None}


# ── The four signatures ─────────────────────────────────────────────────────────

def check_product(product: dict) -> list[dict]:
    """Return a list of blocking findings for one product (empty = clean)."""
    v = _extract(product)
    findings: list[dict] = []

    # S1 — "פחות מ" / "<" token in any TOTAL raw field (BSIP0 only; floats can't carry it)
    for f in _TOTAL_RAW_FIELDS:
        rawval = v["raw"].get(f)
        if _has_less_than_token(rawval):
            findings.append({
                "sig": "S1_less_than_token_in_total",
                "field": f, "value": rawval,
                "detail": f'less-than token in TOTAL field {f}={rawval!r} '
                          f'(a "<N" bound belongs only to a saturated/trans sub-row)',
            })

    # S2 — saturated_fat > total_fat (EV-029 sub-row-overwrote-total signature)
    if v["fat"] is not None and v["sat"] is not None and v["sat"] > v["fat"] + 0.05:
        findings.append({
            "sig": "S2_sat_gt_total_fat",
            "detail": f'saturated_fat={v["sat"]}g > total_fat={v["fat"]}g (sub-row overwrote total)',
        })

    # S3 — fat understated vs declared energy
    if (v["fat"] is not None and v["fat"] <= FAT_NEAR_ZERO_G and v["energy"] is not None):
        macro = 4 * (v["protein"] or 0) + 4 * (v["carbs"] or 0) + 9 * v["fat"]
        gap = v["energy"] - macro
        if gap >= ENERGY_GAP_KCAL:
            findings.append({
                "sig": "S3_fat_understated_vs_energy",
                "detail": (f'total_fat={v["fat"]}g but {v["energy"]}kcal exceeds '
                           f'protein+carb+fat energy ({macro:.0f}kcal) by {gap:.0f}kcal '
                           f'(fat understated, not genuinely low)'),
            })

    # S4 — sodium absurd value
    if v["sodium"] is not None and v["sodium"] > SODIUM_MAX_MG:
        findings.append({
            "sig": "S4_sodium_absurd",
            "detail": f'sodium={v["sodium"]}mg/100g > {SODIUM_MAX_MG:g}mg (data-integrity failure)',
        })

    # S5 — interlock with the canonical extraction layer (Data, TASK-192 / EV-046).
    # parse_nutrition_numeric records an "_integrity" list on any BSIP1 record whose
    # raw panel carried a less-than bound in a total or a sat>total violation. Honour
    # it directly so the two halves cannot disagree: if the canonical parser flagged
    # the panel, the gate blocks even if the float-only signatures above did not fire.
    nn = product.get("normalized_nutrition_per_100g")
    integ = nn.get("_integrity") if isinstance(nn, dict) else None
    for tag in integ or []:
        if tag == "fat_is_less_than_bound":
            findings.append({
                "sig": "S5_canonical_integrity_fat_bound",
                "detail": "canonical extraction flagged total fat as a 'less-than' bound (EV-046 _integrity)",
            })
        elif tag.startswith("sat_gt_total_fat"):
            # already covered by S2 when both floats present; keep when only the flag exists
            if not any(f["sig"] == "S2_sat_gt_total_fat" for f in findings):
                findings.append({"sig": "S2_sat_gt_total_fat", "detail": f"EV-046 _integrity: {tag}"})

    for fd in findings:
        fd["name"] = v["name"]
        fd["stage"] = v["stage"]
    return findings


def gate_corpus(products: list[dict], fail_pct: float = SYSTEMIC_FAIL_PCT) -> dict:
    """Gate a list of product records. Returns a verdict dict; `passed` is the gate.

    Blocking rule:
      • ANY S1 / S2 / S4 finding  → BLOCK (these are never legitimate).
      • S3 findings               → BLOCK when their share of the corpus ≥ fail_pct
                                     (systemic parse defect) OR when any S1/S2/S4
                                     also fired. A lone, sub-threshold S3 is a WARN.
    """
    total = len(products)
    all_findings: list[dict] = []
    flagged_ids: set[int] = set()
    for i, p in enumerate(products):
        fs = check_product(p)
        if fs:
            flagged_ids.add(i)
        all_findings.extend(fs)

    by_sig: dict[str, int] = {}
    for fd in all_findings:
        by_sig[fd["sig"]] = by_sig.get(fd["sig"], 0) + 1

    n_always = sum(by_sig.get(s, 0) for s in
                   ("S1_less_than_token_in_total", "S2_sat_gt_total_fat",
                    "S4_sodium_absurd", "S5_canonical_integrity_fat_bound"))
    n_s3 = by_sig.get("S3_fat_understated_vs_energy", 0)
    s3_pct = round(n_s3 * 100 / total, 1) if total else 0.0

    blocking = n_always > 0 or (n_s3 > 0 and (s3_pct >= fail_pct or n_always > 0))
    passed = not blocking

    summary = (f"{len(flagged_ids)}/{total} products flagged; "
               f"by signature: " + (", ".join(f"{k}={v}" for k, v in sorted(by_sig.items())) or "none")
               + f"; S3 share={s3_pct}%")

    return {
        "passed": passed,
        "blocking": blocking,
        "total": total,
        "flagged_products": len(flagged_ids),
        "by_signature": by_sig,
        "s3_pct": s3_pct,
        "summary": summary,
        "findings": all_findings,
    }


# ── Corpus loading (stage-agnostic) ─────────────────────────────────────────────

def _load_products(path: Path) -> list[dict]:
    """Load product records from a file or directory, any stage."""
    products: list[dict] = []
    if path.is_dir():
        for f in sorted(path.glob("*.json")):
            products.extend(_load_products(f))
        return products
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [load error] {path}: {e}", file=sys.stderr)
        return products
    if isinstance(data, list):
        products.extend(data)
    elif isinstance(data, dict):
        if isinstance(data.get("products"), list):
            products.extend(data["products"])
        else:
            products.append(data)  # a single BSIP1 record
    return products


def main() -> int:
    ap = argparse.ArgumentParser(description="COV-007 nutrition data-integrity guard")
    ap.add_argument("--path", required=True,
                    help="file, directory, or glob of BSIP0/BSIP1/frontend JSON")
    ap.add_argument("--fail-pct", type=float, default=SYSTEMIC_FAIL_PCT)
    ap.add_argument("--max-examples", type=int, default=15)
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    paths = [Path(p) for p in _glob.glob(args.path)] or [Path(args.path)]
    products: list[dict] = []
    for p in paths:
        products.extend(_load_products(p))

    if not products:
        print(f"COV-007: no products loaded from {args.path!r}", file=sys.stderr)
        return 2

    result = gate_corpus(products, fail_pct=args.fail_pct)
    verdict = "PASS" if result["passed"] else "BLOCK"
    print(f"COV-007 {verdict} — {result['summary']}")
    for fd in result["findings"][:args.max_examples]:
        print(f"  [{fd['sig']}] {fd['name'][:42]} — {fd['detail']}")
    if len(result["findings"]) > args.max_examples:
        print(f"  ... and {len(result['findings']) - args.max_examples} more findings")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
