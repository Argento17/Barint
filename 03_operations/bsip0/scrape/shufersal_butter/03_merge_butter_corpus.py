"""
BSIP0 Merge — Butter Corpus (TASK-191).

Loads all three retailer JSONs (Shufersal + Yohananof + Carrefour), deduplicates
by barcode, applies EXCLUDE_SIGNALS filter to any new products, and writes the
merged corpus.

Deduplication rules:
  1. Exact barcode match → keep highest-confidence record.
  2. Confidence tie → prefer Shufersal > Yohananof > Carrefour.
  3. Items 6+7 from Shufersal (FERMA 82.5% / Alouette soft) → kept, flagged
     extraction_confidence="medium" (owner decision: IN corpus, INSUFFICIENT score).
  4. Item 10 (גבינות ניצן מתובלת) → kept with subtype="flavored_herbed".

Outputs:
  C:\\Bari\\02_products\\butter\\bsip0_outputs\\butter_merged_corpus.json
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

OUT_DIR = Path(r"C:\Bari\02_products\butter\bsip0_outputs")
BSIP1_OUTPUT = Path(r"C:\Bari\02_products\butter\bsip1_outputs")

# Retailer priority for dedup (lower index = higher priority)
RETAILER_PRIORITY = ["shufersal", "yohananof", "carrefour"]

EXCLUDE_SIGNALS = [
    "ממרח", "מרגרינה", "שמן לפתית", "שמן צמחי", "שמנים צמחיים",
    "נטורינה", "בטעם חמאה", "butter flavor", "butter flavour",
    "חמאת בוטנים", "חמאת שקדים", "חמאת קשיו", "חמאת פיסטוקים",
    "שמן קוקוס", "קרם צמחי", "פלמנטין", "שומן אפייה",
]

# Owner decisions (TASK-191):
# Items 6+7: FERMA 82.5% (barcode 4820217240114) and Alouette riche soft
#   (barcode 3161911229199) — no nutrition panel → keep, set extraction_confidence="medium"
MEDIUM_CONFIDENCE_BARCODES = {"4820217240114", "3161911229199"}

# Item 10: גבינות ניצן מתובלת (barcode 369709) → subtype="flavored_herbed"
FLAVORED_HERBED_BARCODES = {"369709"}

CONFIDENCE_RANK = {
    "high": 3,
    "medium": 2,
    "low": 1,
    "off_miss": 0,
}


def _should_exclude(name: str) -> bool:
    if not name:
        return False
    name_lower = name.lower()
    for sig in EXCLUDE_SIGNALS:
        if sig.lower() in name_lower:
            return True
    return False


def _conf_score(record: dict) -> int:
    conf = (record.get("extraction_confidence") or "low").lower()
    return CONFIDENCE_RANK.get(conf, 0)


def _retailer_priority(record: dict) -> int:
    rid = (record.get("retailer_id") or "").lower()
    try:
        return len(RETAILER_PRIORITY) - RETAILER_PRIORITY.index(rid)
    except ValueError:
        return 0


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        log.warning("File not found: %s", path)
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        log.warning("Expected list in %s, got %s", path, type(data).__name__)
        return []
    except Exception as e:
        log.error("Failed to load %s: %s", path, e)
        return []


def _find_latest(pattern: str, directory: Path) -> Path | None:
    candidates = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def main():
    # ── Find retailer files ─────────────────────────────────────────────────────
    shufersal_path = _find_latest("butter_bsip0_raw_*.json", OUT_DIR)
    yohananof_path = _find_latest("butter_yohananof_raw_*.json", OUT_DIR)
    carrefour_path = _find_latest("butter_carrefour_raw_*.json", OUT_DIR)

    log.info("=== Butter Corpus Merge (TASK-191) ===")
    log.info("  Shufersal: %s", shufersal_path or "NOT FOUND")
    log.info("  Yohananof: %s", yohananof_path or "NOT FOUND")
    log.info("  Carrefour: %s", carrefour_path or "NOT FOUND")

    shufersal_records = _load_json(shufersal_path) if shufersal_path else []
    yohananof_records = _load_json(yohananof_path) if yohananof_path else []
    carrefour_records = _load_json(carrefour_path) if carrefour_path else []

    n_shufersal_raw = len(shufersal_records)
    n_yohananof_raw = len(yohananof_records)
    n_carrefour_raw = len(carrefour_records)

    log.info("  Raw counts: Shufersal=%d, Yohananof=%d, Carrefour=%d",
             n_shufersal_raw, n_yohananof_raw, n_carrefour_raw)

    # ── Deduplication pass ─────────────────────────────────────────────────────
    # key = barcode (str); value = best record so far
    best: dict[str, dict] = {}
    dedup_replaced = 0

    all_records = shufersal_records + yohananof_records + carrefour_records

    for record in all_records:
        barcode = str(record.get("barcode", "")).strip()
        if not barcode:
            continue

        name = (record.get("name_he") or "").strip()
        if _should_exclude(name):
            continue

        # Apply owner decisions for known barcodes
        if barcode in MEDIUM_CONFIDENCE_BARCODES:
            record = dict(record)
            record["extraction_confidence"] = "medium"

        if barcode in FLAVORED_HERBED_BARCODES:
            record = dict(record)
            record["subtype_override"] = "flavored_herbed"

        if barcode not in best:
            best[barcode] = record
        else:
            existing = best[barcode]
            existing_score = (_conf_score(existing) * 10 + _retailer_priority(existing))
            new_score = (_conf_score(record) * 10 + _retailer_priority(record))
            if new_score > existing_score:
                best[barcode] = record
                dedup_replaced += 1

    merged = list(best.values())

    # ── Count by retailer ─────────────────────────────────────────────────────
    from_shufersal = [r for r in merged if r.get("retailer_id") == "shufersal"]
    from_yohananof = [r for r in merged if r.get("retailer_id") == "yohananof"]
    from_carrefour = [r for r in merged if r.get("retailer_id") == "carrefour"]

    # OFF-miss records in merged corpus (no nutrition, kept for tracking)
    off_miss = [r for r in merged if r.get("extraction_confidence") == "off_miss"]
    medium_conf = [r for r in merged if r.get("extraction_confidence") == "medium"]

    n_final = len(merged)
    n_dupes_removed = len(all_records) - len(best) - sum(1 for r in all_records
                                                          if _should_exclude(r.get("name_he", "")))

    # ── Write output ───────────────────────────────────────────────────────────
    out_path = OUT_DIR / "butter_merged_corpus.json"
    out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── Dedup summary ──────────────────────────────────────────────────────────
    log.info("=== Dedup Summary ===")
    log.info("  From Shufersal: %d / %d raw", len(from_shufersal), n_shufersal_raw)
    log.info("  From Yohananof: %d / %d raw", len(from_yohananof), n_yohananof_raw)
    log.info("  From Carrefour: %d / %d raw", len(from_carrefour), n_carrefour_raw)
    log.info("  Duplicates removed (replaced by higher-confidence): %d", dedup_replaced)
    log.info("  Final corpus size: %d", n_final)
    log.info("  Medium-confidence (no panel, owner keep): %d", len(medium_conf))
    log.info("  OFF-miss (barcode known, no OFF panel): %d", len(off_miss))
    log.info("  Saved: %s", out_path)

    if n_final < 30:
        log.warning("  TARGET MISS: Only %d products (target 30–50).", n_final)
        # Identify missing priority brands
        brand_names = {r.get("brand", "").upper() for r in merged}
        missing_targets = []
        for brand in ["KERRYGOLD", "ANCHOR", "LURPAK", "PRESIDENT"]:
            if not any(brand in b for b in brand_names):
                missing_targets.append(brand)
        if missing_targets:
            log.warning("  Missing target brands (OFF miss): %s", ", ".join(missing_targets))
            log.warning("  Reason: These barcodes returned OFF miss — not in OFF DB for Israel.")
            log.warning("  Recommendation: Supplement with Yohananof Playwright scrape for full panels.")
    else:
        log.info("  Target met: %d products (target 30–50).", n_final)

    # Print per-product summary
    log.info("\n=== Corpus Products ===")
    for r in sorted(merged, key=lambda x: x.get("retailer_id", "") + x.get("name_he", "")):
        log.info("  [%s] %s | %s | conf=%s",
                 r.get("retailer_id", "?"),
                 r.get("barcode", "?"),
                 r.get("name_he", "?"),
                 r.get("extraction_confidence", "?"))

    return merged, out_path


if __name__ == "__main__":
    main()
