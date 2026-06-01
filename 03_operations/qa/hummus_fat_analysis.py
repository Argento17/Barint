"""
TASK-039 — Hummus fat_raw anomaly investigation.
Run from C:\Bari:
    python 03_operations/qa/hummus_fat_analysis.py
"""
from __future__ import annotations
import csv
import json
import re
import sys
import datetime
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OBS_DIR    = pathlib.Path(r"C:\Bari\02_products\hummus\observations_bsip0\shufersal")
CANON_DIR  = pathlib.Path(r"C:\Bari\02_products\hummus\canonical_bsip1")
AUDIT_DIR  = pathlib.Path(r"C:\Bari\02_products\hummus\audit")
REPORT_DIR = pathlib.Path(r"C:\Bari\03_operations\qa\reports")
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

_NUM_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def _num(s: str | None) -> float | None:
    if not s:
        return None
    m = _NUM_RE.search(str(s).replace(",", "."))
    return float(m.group(1)) if m else None


def implied_fat_g(kcal: float, prot_g: float, carbs_g: float) -> float:
    """Fat estimated from caloric gap: fat_g = (kcal - prot*4 - carbs*4) / 9"""
    fat_kcal = kcal - (prot_g * 4.0) - (carbs_g * 4.0)
    return fat_kcal / 9.0


def severity(scraped_fat: float | None, calc_fat: float | None, has_tahini: bool) -> str:
    if scraped_fat is None:
        return "LOW"
    if calc_fat is None:
        return "LOW"
    gap = calc_fat - scraped_fat
    if gap > 15 and has_tahini:
        return "CRITICAL"
    if gap > 10 and has_tahini:
        return "HIGH"
    if gap > 5:
        return "MEDIUM"
    if gap > 2:
        return "LOW"
    return "NONE"


def root_cause(scraped_fat_raw: str, calc_fat: float | None, scraped_fat: float | None) -> str:
    raw_lower = (scraped_fat_raw or "").lower()
    if "פחות מ" in scraped_fat_raw or "פחות" in raw_lower:
        # "less than 0.5" is a standard Israeli label encoding for trace amounts of saturated fat
        # When total fat is much higher (from caloric gap), this indicates the scraper captured
        # the saturated fat sub-row instead of the total fat row
        if calc_fat and calc_fat > 3:
            return "scraper_captured_sat_fat_subrow"
        else:
            return "legitimate_trace_fat"  # genuinely <0.5g fat (e.g., matbucha, pepper spread)
    if scraped_fat is not None and scraped_fat <= 0.5 and calc_fat and calc_fat > 2:
        return "scraper_html_misalignment"
    return "plausible_match"


records = []

for obs_file in sorted(OBS_DIR.glob("P_*.json")):
    raw = json.loads(obs_file.read_text(encoding="utf-8"))
    n = raw.get("nutrition", {})

    fat_raw_str  = n.get("fat_raw", "") or ""
    kcal_raw_str = n.get("energy_kcal_raw", "") or ""
    prot_raw_str = n.get("protein_raw", "") or ""
    carbs_raw_str= n.get("carbs_raw", "") or ""
    sodium_str   = n.get("sodium_raw", "") or ""

    fat_scraped  = _num(fat_raw_str)
    kcal         = _num(kcal_raw_str)
    prot         = _num(prot_raw_str)
    carbs        = _num(carbs_raw_str)
    sodium       = _num(sodium_str)

    ingr         = raw.get("ingredients_raw", "") or ""
    has_tahini   = "טחינה" in ingr
    ingr_lo      = ingr.lower()

    # Extract tahini percentage if declared
    tahini_pct = None
    m = re.search(r"טחינה[^(]*?(\d+(?:[.,]\d+)?)\s*%", ingr)
    if m:
        tahini_pct = float(m.group(1).replace(",", "."))

    # Calculate implied fat from caloric balance
    fat_implied = None
    fat_gap     = None
    if kcal is not None and prot is not None and carbs is not None:
        fat_implied = round(implied_fat_g(kcal, prot, carbs), 1)
        if fat_scraped is not None:
            fat_gap = round(fat_implied - fat_scraped, 1)

    rc = root_cause(fat_raw_str, fat_implied, fat_scraped)

    sev = severity(fat_scraped, fat_implied, has_tahini)

    # Determine BSIP2 decision per product
    if rc == "scraper_captured_sat_fat_subrow" and fat_gap and fat_gap > 5:
        bsip2_allowed   = "allowed_with_warning"
        recommended_act = (
            f"fat_g in BSIP1 record is WRONG (scraped={fat_scraped}g; implied={fat_implied}g from caloric gap). "
            f"fat_quality and calorie_density dimensions will score incorrectly. "
            f"Correct fat_g to {fat_implied}g before BSIP2 OR suppress fat_quality dimension for this run."
        )
    elif rc == "legitimate_trace_fat":
        bsip2_allowed   = "allowed"
        recommended_act = "Fat value is plausible for this product type. No action required."
    elif rc == "scraper_html_misalignment":
        bsip2_allowed   = "allowed_with_warning"
        recommended_act = (
            f"Suspected HTML mis-alignment (fat_scraped={fat_scraped}g vs implied={fat_implied}g). "
            f"Verify manually before BSIP2."
        )
    else:
        bsip2_allowed   = "allowed"
        recommended_act = "Fat value is consistent with caloric balance."

    barcode = raw.get("barcode", obs_file.stem.replace("P_", ""))

    # Get BSIP1 fat_g for cross-reference
    bsip1_file = CANON_DIR / f"bsip1_{barcode}.json"
    bsip1_fat  = None
    if bsip1_file.exists():
        b1 = json.loads(bsip1_file.read_text(encoding="utf-8"))
        bsip1_fat = (b1.get("normalized_nutrition_per_100g") or {}).get("fat_g")

    records.append({
        "product_id":              f"bsip1_{barcode}",
        "product_name":            raw.get("name_he", ""),
        "barcode":                 barcode,
        "fat_raw_shufersal":       fat_raw_str,
        "fat_g_bsip1":             bsip1_fat,
        "fat_g_scraped_parsed":    fat_scraped,
        "fat_g_implied_kcal_gap":  fat_implied,
        "fat_g_gap":               fat_gap,
        "energy_kcal":             kcal,
        "protein_g":               prot,
        "carbs_g":                 carbs,
        "sodium_mg":               sodium,
        "tahini_pct_declared":     tahini_pct,
        "ingredients_include_tahini": has_tahini,
        "suspected_root_cause":    rc,
        "severity":                sev,
        "bsip2_allowed":           bsip2_allowed,
        "recommended_action":      recommended_act,
        "source_url":              raw.get("source_url", ""),
    })

# ── Summary stats ──────────────────────────────────────────────────────────────
total = len(records)
rc_counts = {}
sev_counts = {}
for r in records:
    rc_counts[r["suspected_root_cause"]] = rc_counts.get(r["suspected_root_cause"], 0) + 1
    sev_counts[r["severity"]] = sev_counts.get(r["severity"], 0) + 1

blocked    = sum(1 for r in records if r["bsip2_allowed"] == "blocked")
with_warn  = sum(1 for r in records if r["bsip2_allowed"] == "allowed_with_warning")
allowed    = sum(1 for r in records if r["bsip2_allowed"] == "allowed")

print(f"Total BSIP0 products analysed: {total}")
print(f"Root cause breakdown:")
for rc, cnt in sorted(rc_counts.items(), key=lambda x: -x[1]):
    print(f"  {cnt:3}  {rc}")
print(f"Severity breakdown:")
for s, cnt in sorted(sev_counts.items(), key=lambda x: -x[1]):
    print(f"  {cnt:3}  {s}")
print(f"BSIP2 decisions: allowed={allowed}  with_warning={with_warn}  blocked={blocked}")

# ── Issue register (JSON) ──────────────────────────────────────────────────────
issue_register = {
    "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    "task": "TASK-039",
    "category": "hummus",
    "summary": {
        "total_products": total,
        "root_cause_scraper_sat_fat": rc_counts.get("scraper_captured_sat_fat_subrow", 0),
        "root_cause_legitimate": rc_counts.get("legitimate_trace_fat", 0),
        "root_cause_plausible": rc_counts.get("plausible_match", 0),
        "severity_critical": sev_counts.get("CRITICAL", 0),
        "severity_high": sev_counts.get("HIGH", 0),
        "severity_medium": sev_counts.get("MEDIUM", 0),
        "bsip2_blocked": blocked,
        "bsip2_with_warning": with_warn,
        "bsip2_allowed": allowed,
    },
    "products": records,
}
register_path = AUDIT_DIR / "fat_anomaly_TASK039.json"
register_path.write_text(
    json.dumps(issue_register, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"\nIssue register: {register_path}")

# ── Print critical/high severity products ─────────────────────────────────────
print("\n=== CRITICAL / HIGH severity products ===")
for r in [x for x in records if x["severity"] in ("CRITICAL", "HIGH")]:
    tahini_note = f"tahini {r['tahini_pct_declared']}%" if r["tahini_pct_declared"] else "tahini (undeclared %)"
    print(f"  [{r['severity']}] {r['product_name']}")
    print(f"    fat_scraped={r['fat_g_scraped_parsed']}g  fat_implied={r['fat_g_implied_kcal_gap']}g  gap={r['fat_g_gap']}g  kcal={r['energy_kcal']}")
    if r["ingredients_include_tahini"]:
        print(f"    Has {tahini_note}")
    print(f"    Root cause: {r['suspected_root_cause']}")
    print()

print(f"\nIssue register saved to {register_path}")
