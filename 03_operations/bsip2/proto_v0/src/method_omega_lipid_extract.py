#!/usr/bin/env python3
"""
P175 / TASK-324 — Standalone omega-3/omega-6 / specific-lipid extraction method.

Measurement only — NOT wired to score_engine. EV-011 contract:
  declared quantitative omega → extract; absent → declared:false (never zero, never worst-case).

Run: python method_omega_lipid_extract.py --coverage
OFF-ban: lipid values from in-house BSIP0/BSIP1 panel text only; no Open Food Facts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Inert — not referenced by score_engine.py
OMEGA_LIPID_METHOD_VERSION = "omega_lipid_extract_v1"

REPO = Path(__file__).resolve().parents[4]
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
REPORT_DIR = (
    REPO / "03_operations" / "bsip2" / "proto_v0" / "reports" / "methods" / "omega_lipid"
)

PANEL_MARKER = "ערכים תזונתיים"

# Hebrew + Latin label tokens (quantitative panel rows / normalized fields)
_OMEGA3_LABEL = re.compile(
    r"(?:אומגה[\s\-]*3|omega[\s\-]*3|ω[\s\-]*3|n-3|n3|"
    r"חומצות\s+שומן\s+אומגה[\s\-]*3|polyunsaturated\s+omega[\s\-]*3)",
    re.I,
)
_OMEGA6_LABEL = re.compile(
    r"(?:אומגה[\s\-]*6|omega[\s\-]*6|ω[\s\-]*6|n-6|n6|"
    r"חומצות\s+שומן\s+אומגה[\s\-]*6|polyunsaturated\s+omega[\s\-]*6|"
    r"חומצות\s+שומן\s+בלתי\s+רוויות\s+אומגה[\s\-]*6)",
    re.I,
)
_SPECIFIC_LIPID_LABELS = {
    "EPA": re.compile(r"\bEPA\b|אי\.?\s*פי\.?\s*אי|איקוסאפנטאנואית", re.I),
    "DHA": re.compile(r"\bDHA\b|די\.?\s*אי\.?\s*אי|דוקוסהקסאנואית", re.I),
    "ALA": re.compile(r"\bALA\b|אלפא[\s\-]*לינולנית|alpha[\s\-]*linolenic", re.I),
}

_QUALITATIVE_OIL_TERMS = (
    "שמן קנולה", "canola oil", "canola",
    "שמן פשתן", "flax", "פשתן",
    "שמן חמניות", "sunflower oil",
    "שמן דגים", "fish oil",
    "שמן אגוזי מלך", "walnut oil",
    "שמן סויה", "soybean oil",
    "שמן זית", "olive oil",
)

_UNIT_MG = frozenset({"מג", 'מ"ג', "מ״ג", "mg", "מיליגרם"})
_UNIT_G = frozenset({"גרם", 'גר', "g", "גר'"})
_BASIS_100G = re.compile(r"100\s*(?:גרם|גר|g|מ[\"״']?ל|ml)", re.I)


def _is_off_sourced(doc: dict[str, Any]) -> bool:
    """True when nutrition panel provenance is Open Food Facts (TASK-238 ban)."""
    prov = doc.get("provenance") or {}
    if prov.get("panel_source") == "open_food_facts":
        return True
    if doc.get("_off_data_used"):
        return True
    flags = doc.get("canonical_risk_flags") or []
    if "off_candidate_panel" in flags:
        return True
    url = str(doc.get("source_url") or "")
    return "openfoodfacts" in url.lower()


def _parse_float(val: Any) -> float | None:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(",", ".")
    m = re.search(r"[\d.]+", s)
    if not m:
        return None
    try:
        return float(m.group())
    except ValueError:
        return None


def _to_mg_100g(value: float, unit: str | None, basis_per_100g: bool = True) -> float:
    """Normalize a declared amount to mg per 100g (assumes per-100g unless caller overrides)."""
    u = (unit or "").strip().lower()
    mg = value
    if u in {x.lower() for x in _UNIT_G} or u in ("גרם", "גר"):
        mg = value * 1000.0
    if not basis_per_100g:
        # Caller must scale externally; we keep raw mg for the stated basis.
        pass
    return round(mg, 4)


def _classify_omega_label(label: str) -> str | None:
    text = label.strip()
    if _OMEGA3_LABEL.search(text) and not _OMEGA6_LABEL.search(text):
        return "omega3"
    if _OMEGA6_LABEL.search(text) and not _OMEGA3_LABEL.search(text):
        return "omega6"
    if _OMEGA3_LABEL.search(text):
        return "omega3"
    if _OMEGA6_LABEL.search(text):
        return "omega6"
    return None


def _classify_specific_lipid(label: str) -> str | None:
    for name, pat in _SPECIFIC_LIPID_LABELS.items():
        if pat.search(label):
            return name
    return None


def _extract_from_nutrition_rows(rows: list[dict[str, Any]]) -> tuple[dict[str, float], list[dict], str | None]:
    """Parse BSIP0 nutrition_raw_source.rows[] — direct scrape panel."""
    omega3: float | None = None
    omega6: float | None = None
    specifics: list[dict[str, Any]] = []
    source_field: str | None = None

    for row in rows:
        label = str(row.get("label") or "")
        val = _parse_float(row.get("value"))
        if val is None:
            continue
        unit = str(row.get("unit") or "")
        kind = _classify_omega_label(label)
        lipid = _classify_specific_lipid(label)

        if kind == "omega3":
            omega3 = _to_mg_100g(val, unit)
            source_field = "bsip0.nutrition_raw_source.rows"
        elif kind == "omega6":
            omega6 = _to_mg_100g(val, unit)
            source_field = "bsip0.nutrition_raw_source.rows"
        elif lipid:
            specifics.append({
                "lipid": lipid,
                "mg_100g": _to_mg_100g(val, unit),
                "kind": "quantitative",
                "source": "bsip0.nutrition_raw_source.rows",
                "label": label,
            })

    out: dict[str, float] = {}
    if omega3 is not None:
        out["omega3_mg_100g"] = omega3
    if omega6 is not None:
        out["omega6_mg_100g"] = omega6
    return out, specifics, source_field


def _extract_from_normalized(nn: dict[str, Any]) -> tuple[dict[str, float], list[dict], str | None]:
    """Read structured per-100g fields when present on BSIP1."""
    key_map = {
        "omega3_mg_100g": (
            "omega3_mg", "omega_3_mg", "omega3_mg_100g", "omega_3_mg_100g",
            "polyunsaturated_omega3_mg",
        ),
        "omega6_mg_100g": (
            "omega6_mg", "omega_6_mg", "omega6_mg_100g", "omega_6_mg_100g",
            "polyunsaturated_omega6_mg",
        ),
    }
    specifics: list[dict[str, Any]] = []
    out: dict[str, float] = {}
    source_field: str | None = None

    for target, keys in key_map.items():
        for k in keys:
            v = _parse_float(nn.get(k))
            if v is not None:
                out[target] = round(v, 4)
                source_field = "bsip1.normalized_nutrition_per_100g"
                break

    for lipid, keys in {
        "EPA": ("epa_mg", "epa_mg_100g"),
        "DHA": ("dha_mg", "dha_mg_100g"),
        "ALA": ("ala_mg", "ala_mg_100g"),
    }.items():
        for k in keys:
            v = _parse_float(nn.get(k))
            if v is not None:
                specifics.append({
                    "lipid": lipid,
                    "mg_100g": round(v, 4),
                    "kind": "quantitative",
                    "source": "bsip1.normalized_nutrition_per_100g",
                })
                break

    return out, specifics, source_field


def _panel_text_chunks(bsip1: dict[str, Any], bsip0: dict[str, Any] | None) -> list[tuple[str, str]]:
    """Collect in-house panel / bleed text segments (never OFF)."""
    chunks: list[tuple[str, str]] = []

    remediation = bsip1.get("_data_remediation") or {}
    before = remediation.get("before_ingredients_text_he_first200") or remediation.get(
        "before_ingredients_text_he"
    )
    if before and PANEL_MARKER in before:
        idx = before.find(PANEL_MARKER)
        chunks.append((before[idx:], "bsip1._data_remediation.before_ingredients"))

    for field in ("ingredients_text_he", "ingredients_raw"):
        text = bsip1.get(field) or ""
        if PANEL_MARKER in text:
            idx = text.find(PANEL_MARKER)
            chunks.append((text[idx:], f"bsip1.{field}"))

    if bsip0:
        ing = bsip0.get("ingredients_raw") or ""
        if PANEL_MARKER in ing:
            idx = ing.find(PANEL_MARKER)
            chunks.append((ing[idx:], "bsip0.ingredients_raw"))
        nrs = bsip0.get("nutrition_raw_source") or {}
        html = nrs.get("html") or ""
        if html and not re.search(r"openfoodfacts", html, re.I):
            chunks.append((re.sub(r"<[^>]+>", " ", html), "bsip0.nutrition_raw_source.html"))

    return chunks


def _extract_from_panel_text(text: str, source: str) -> tuple[dict[str, float], list[dict]]:
    """
    Parse interleaved Israeli panel bleed: 'ערכים תזונתיים 100 גרם 120 מג אומגה 3 ...'
    Also handles 'אומגה 3 120 מג' and row-style '120 מג אומגה 3'.
    """
    out: dict[str, float] = {}
    specifics: list[dict[str, Any]] = []
    basis_per_100g = bool(_BASIS_100G.search(text))

    # value unit label  (120 מג אומגה 3)
    triplet = re.compile(
        r"([\d.,]+)\s*(מג|מ\"ג|מ״ג|mg|גרם|גר|g)\s+"
        r"((?:אומגה[\s\-]*[36]|omega[\s\-]*[36]|"
        r"חומצות\s+שומן\s+אומגה[\s\-]*[36]|EPA|DHA|ALA))",
        re.I,
    )
    for m in triplet.finditer(text):
        val = _parse_float(m.group(1))
        if val is None:
            continue
        unit = m.group(2)
        label = m.group(3)
        mg = _to_mg_100g(val, unit, basis_per_100g=basis_per_100g)
        kind = _classify_omega_label(label)
        lipid = _classify_specific_lipid(label)
        if kind == "omega3":
            out["omega3_mg_100g"] = mg
        elif kind == "omega6":
            out["omega6_mg_100g"] = mg
        elif lipid:
            specifics.append({
                "lipid": lipid,
                "mg_100g": mg,
                "kind": "quantitative",
                "source": source,
                "label": label.strip(),
            })

    # label value unit  (אומגה 3 120 מג)
    reverse = re.compile(
        r"((?:אומגה[\s\-]*[36]|omega[\s\-]*[36]|חומצות\s+שומן\s+אומגה[\s\-]*[36]|EPA|DHA|ALA))"
        r"[^0-9]{0,8}([\d.,]+)\s*(מג|מ\"ג|מ״ג|mg|גרם|גר|g)",
        re.I,
    )
    for m in reverse.finditer(text):
        label = m.group(1)
        val = _parse_float(m.group(2))
        if val is None:
            continue
        mg = _to_mg_100g(val, m.group(3), basis_per_100g=basis_per_100g)
        kind = _classify_omega_label(label)
        lipid = _classify_specific_lipid(label)
        if kind == "omega3" and "omega3_mg_100g" not in out:
            out["omega3_mg_100g"] = mg
        elif kind == "omega6" and "omega6_mg_100g" not in out:
            out["omega6_mg_100g"] = mg
        elif lipid and not any(s["lipid"] == lipid for s in specifics):
            specifics.append({
                "lipid": lipid,
                "mg_100g": mg,
                "kind": "quantitative",
                "source": source,
                "label": label.strip(),
            })

    return out, specifics


def _qualitative_callouts(bsip1: dict[str, Any], bsip0: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Non-quantitative lipid call-outs (claims / marketing) — never converted to mg."""
    callouts: list[dict[str, Any]] = []
    seen: set[str] = set()

    for field in ("claims", "front_of_pack_claims", "claims_raw"):
        raw = bsip1.get(field)
        items: list[str]
        if isinstance(raw, list):
            items = [str(x) for x in raw]
        elif isinstance(raw, str) and raw.strip():
            items = [raw]
        else:
            items = []
        for item in items:
            text = item.strip()
            if not text:
                continue
            if _OMEGA3_LABEL.search(text) or _OMEGA6_LABEL.search(text):
                key = f"claim:{text}"
                if key not in seen:
                    seen.add(key)
                    callouts.append({
                        "lipid": text,
                        "kind": "qualitative_callout",
                        "source": f"bsip1.{field}",
                    })
            for lipid, pat in _SPECIFIC_LIPID_LABELS.items():
                if pat.search(text):
                    key = f"{lipid}:{field}"
                    if key not in seen:
                        seen.add(key)
                        callouts.append({
                            "lipid": lipid,
                            "kind": "qualitative_callout",
                            "source": f"bsip1.{field}",
                            "text": text,
                        })

    if bsip0:
        for field in ("claims_raw", "name_he"):
            text = str(bsip0.get(field) or "")
            if _OMEGA3_LABEL.search(text) or _OMEGA6_LABEL.search(text):
                key = f"bsip0:{field}:{text[:40]}"
                if key not in seen:
                    seen.add(key)
                    callouts.append({
                        "lipid": text[:80],
                        "kind": "qualitative_callout",
                        "source": f"bsip0.{field}",
                    })

    return callouts


def _qualitative_oil_signals(bsip1: dict[str, Any], bsip0: dict[str, Any] | None) -> list[dict[str, str]]:
    """Ingredient-level oil mentions — explicitly NON-quantitative."""
    signals: list[dict[str, str]] = []
    seen: set[str] = set()
    texts = [
        bsip1.get("ingredients_text_he") or "",
        bsip1.get("ingredients_raw") or "",
    ]
    if bsip0:
        texts.append(bsip0.get("ingredients_raw") or "")
    blob = " ".join(texts).lower()
    for term in _QUALITATIVE_OIL_TERMS:
        if term.lower() in blob:
            if term not in seen:
                seen.add(term)
                signals.append({
                    "signal": term,
                    "note": "non-quantitative ingredient mention; not converted to mg",
                })
    return signals


def evaluate_omega_lipid_extract(
    bsip1: dict[str, Any],
    bsip0: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Extract omega-3/omega-6 and specific-lipid declarations from in-house label data.

    EV-011 contract: absent declaration → declared:false (not zero, not insufficient_data).
    """
    omega3: float | None = None
    omega6: float | None = None
    specifics: list[dict[str, Any]] = []
    source_field: str | None = None

    # 1) BSIP0 structured rows (direct scrape — highest trust)
    if bsip0:
        rows = (bsip0.get("nutrition_raw_source") or {}).get("rows") or []
        if rows:
            o, s, src = _extract_from_nutrition_rows(rows)
            omega3 = omega3 or o.get("omega3_mg_100g")
            omega6 = omega6 or o.get("omega6_mg_100g")
            specifics.extend(s)
            source_field = source_field or src

    # 2) BSIP1 normalized fields — only when not OFF-sourced
    if not _is_off_sourced(bsip1):
        nn = bsip1.get("normalized_nutrition_per_100g") or {}
        o, s, src = _extract_from_normalized(nn)
        if omega3 is None:
            omega3 = o.get("omega3_mg_100g")
        if omega6 is None:
            omega6 = o.get("omega6_mg_100g")
        specifics.extend(s)
        source_field = source_field or src

    # 3) Panel text bleed (in-house scrape text)
    for chunk, src in _panel_text_chunks(bsip1, bsip0):
        o, s = _extract_from_panel_text(chunk, src)
        if omega3 is None:
            omega3 = o.get("omega3_mg_100g")
        if omega6 is None:
            omega6 = o.get("omega6_mg_100g")
        for item in s:
            if not any(x.get("lipid") == item["lipid"] and x.get("kind") == "quantitative" for x in specifics):
                specifics.append(item)
        if (o.get("omega3_mg_100g") or o.get("omega6_mg_100g")) and source_field is None:
            source_field = src

    qualitative = _qualitative_callouts(bsip1, bsip0)
    for q in qualitative:
        if not any(
            x.get("lipid") == q.get("lipid") and x.get("kind") == q.get("kind")
            for x in specifics
        ):
            specifics.append(q)

    declared = omega3 is not None or omega6 is not None
    ratio: float | None = None
    if omega3 is not None and omega6 is not None and omega3 > 0:
        ratio = round(omega6 / omega3, 4)

    return {
        "omega3_mg_100g": omega3,
        "omega6_mg_100g": omega6,
        "omega6_3_ratio": ratio,
        "specific_lipids": specifics,
        "qualitative_oil_signals": _qualitative_oil_signals(bsip1, bsip0),
        "declared": declared,
        "source_field": source_field,
    }


# ---------------------------------------------------------------------------
# Coverage runner (mirrors P173 calibrator)
# ---------------------------------------------------------------------------

_BSIP0_INDEX: dict[str, dict[str, Any]] | None = None


def _load_bsip0_index() -> dict[str, dict[str, Any]]:
    global _BSIP0_INDEX
    if _BSIP0_INDEX is not None:
        return _BSIP0_INDEX

    index: dict[str, dict[str, Any]] = {}
    skip_names = {"gate", "manifest", "curation", "report", "log"}
    for path in REPO.rglob("*.json"):
        pstr = str(path).lower()
        if "bsip0" not in pstr and "observations_bsip0" not in pstr:
            continue
        if any(x in path.name for x in skip_names):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        records: list[dict[str, Any]]
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict) and "products" in data:
            records = data["products"]
        elif isinstance(data, dict) and data.get("barcode"):
            records = [data]
        else:
            continue
        for rec in records:
            bc = str(rec.get("barcode") or "").strip()
            if bc and bc not in index:
                index[bc] = rec

    _BSIP0_INDEX = index
    return index


def discover_shelf_configs() -> list[Path]:
    return sorted(
        p for p in CONFIGS_DIR.glob("*.json") if not p.name.startswith("_generated_")
    )


def normalize_corpus_dirs(config: dict, scoring: dict) -> list[str]:
    bsip1_dir = scoring.get("bsip1_dir")
    if bsip1_dir:
        return [bsip1_dir]
    corpus_dirs = config.get("corpus_dirs", [])
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]
    return [d for d in corpus_dirs if d]


def collect_bsip1_products(corpus_dirs: list[str]) -> list[tuple[Path, dict]]:
    seen: set[str] = set()
    out: list[tuple[Path, dict]] = []
    for corpus_dir in corpus_dirs:
        cdir = Path(corpus_dir)
        if not cdir.is_dir():
            continue
        for path in sorted(cdir.glob("bsip1_*.json")):
            if "audit" in path.name:
                continue
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            barcode = str(doc.get("barcode") or "").strip()
            if not barcode or barcode in seen:
                continue
            seen.add(barcode)
            out.append((path, doc))
    return out


def _product_name(doc: dict) -> str:
    return (
        doc.get("canonical_name_he")
        or doc.get("product_name_he")
        or doc.get("canonical_product_id")
        or ""
    )


def run_coverage() -> dict[str, Any]:
    bsip0_index = _load_bsip0_index()
    products: list[dict[str, Any]] = []
    shelf_totals: dict[str, dict[str, int]] = {}

    for config_path in discover_shelf_configs():
        shelf = config_path.stem
        config = json.loads(config_path.read_text(encoding="utf-8"))
        scoring = config.get("scoring") or {}
        corpus_dirs = normalize_corpus_dirs(config, scoring)
        if not corpus_dirs:
            continue

        shelf_totals.setdefault(
            shelf,
            {
                "evaluated": 0,
                "declaring_omega3": 0,
                "declaring_omega6": 0,
                "declaring_either": 0,
                "ratio_computable": 0,
                "qualitative_only": 0,
            },
        )

        for path, doc in collect_bsip1_products(corpus_dirs):
            bsip0 = bsip0_index.get(str(doc.get("barcode") or "").strip())
            result = evaluate_omega_lipid_extract(doc, bsip0)

            st = shelf_totals[shelf]
            st["evaluated"] += 1
            if result["omega3_mg_100g"] is not None:
                st["declaring_omega3"] += 1
            if result["omega6_mg_100g"] is not None:
                st["declaring_omega6"] += 1
            if result["declared"]:
                st["declaring_either"] += 1
            if result["omega6_3_ratio"] is not None:
                st["ratio_computable"] += 1
            if not result["declared"] and result["specific_lipids"]:
                st["qualitative_only"] += 1

            products.append({
                "barcode": str(doc.get("barcode") or ""),
                "shelf": shelf,
                "product_name": _product_name(doc),
                "declared": result["declared"],
                "omega3_mg_100g": result["omega3_mg_100g"],
                "omega6_mg_100g": result["omega6_mg_100g"],
                "omega6_3_ratio": result["omega6_3_ratio"],
                "specific_lipids": result["specific_lipids"],
                "qualitative_oil_signals": result["qualitative_oil_signals"],
                "source_field": result["source_field"],
                "bsip1_source": str(path),
                "bsip0_matched": bsip0 is not None,
            })

    products.sort(key=lambda r: (r["shelf"], r["barcode"]))

    totals = {
        "evaluated": len(products),
        "declaring_omega3": sum(1 for p in products if p["omega3_mg_100g"] is not None),
        "declaring_omega6": sum(1 for p in products if p["omega6_mg_100g"] is not None),
        "declaring_either": sum(1 for p in products if p["declared"]),
        "ratio_computable": sum(1 for p in products if p["omega6_3_ratio"] is not None),
        "qualitative_only": sum(
            1 for p in products if not p["declared"] and p["specific_lipids"]
        ),
    }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "omega_lipid_extract",
        "method_version": OMEGA_LIPID_METHOD_VERSION,
        "off_ban": "nutrition from in-house BSIP0/BSIP1 only; OFF-sourced normalized panels skipped",
        "ev011_contract": "absent declaration → declared:false; never zero or worst-case default",
        **totals,
        "coverage_per_shelf": {
            s: {
                **t,
                "omega3_rate": round(t["declaring_omega3"] / t["evaluated"], 4) if t["evaluated"] else 0.0,
                "omega6_rate": round(t["declaring_omega6"] / t["evaluated"], 4) if t["evaluated"] else 0.0,
                "either_rate": round(t["declaring_either"] / t["evaluated"], 4) if t["evaluated"] else 0.0,
                "ratio_rate": round(t["ratio_computable"] / t["evaluated"], 4) if t["evaluated"] else 0.0,
            }
            for s, t in sorted(shelf_totals.items())
        },
        "products": products,
    }, shelf_totals


def write_reports(summary: dict[str, Any], shelf_totals: dict[str, dict[str, int]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    cov_json = REPORT_DIR / "coverage.json"
    cov_md = REPORT_DIR / "coverage.md"

    cov_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    n = summary["evaluated"]
    lines = [
        "# Omega-3/6 / specific-lipid extraction — label coverage (P175)",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Summary",
        "",
        "| Metric | Count | Rate |",
        "|--------|------:|-----:|",
        f"| Products evaluated (denominator) | {n} | — |",
        f"| Declaring omega-3 (quantitative) | {summary['declaring_omega3']} | {summary['declaring_omega3']/n:.1%} |" if n else "",
        f"| Declaring omega-6 (quantitative) | {summary['declaring_omega6']} | {summary['declaring_omega6']/n:.1%} |" if n else "",
        f"| Declaring either omega-3 or omega-6 | {summary['declaring_either']} | {summary['declaring_either']/n:.1%} |" if n else "",
        f"| Ratio computable (both declared, ω6/ω3) | {summary['ratio_computable']} | {summary['ratio_computable']/n:.1%} |" if n else "",
        f"| Qualitative call-out only (no quantitative) | {summary['qualitative_only']} | {summary['qualitative_only']/n:.1%} |" if n else "",
        "",
        "EV-011 contract: absent panel declaration → `declared:false` (not zero, not penalized).",
        "OFF-ban: normalized nutrition skipped when panel provenance is Open Food Facts.",
        "",
        "## Coverage per shelf",
        "",
        "| Shelf | Evaluated | Ω3 declared | Ω6 declared | Either | Ratio computable |",
        "|-------|----------:|------------:|------------:|-------:|-----------------:|",
    ]
    for shelf, t in sorted(shelf_totals.items()):
        ev = t["evaluated"]
        lines.append(
            f"| {shelf} | {ev} | {t['declaring_omega3']} | {t['declaring_omega6']} | "
            f"{t['declaring_either']} | {t['ratio_computable']} |"
        )

    declared_products = [p for p in summary["products"] if p["declared"]]
    if declared_products:
        lines.extend([
            "",
            "## Products with quantitative omega declarations",
            "",
            "| Shelf | Barcode | Product | Ω3 mg/100g | Ω6 mg/100g | Ratio | Source |",
            "|-------|---------|---------|----------:|----------:|------:|--------|",
        ])
        for p in declared_products:
            name = p["product_name"].replace("|", "/")
            lines.append(
                f"| {p['shelf']} | {p['barcode']} | {name} | "
                f"{p['omega3_mg_100g']} | {p['omega6_mg_100g']} | "
                f"{p['omega6_3_ratio']} | {p['source_field']} |"
            )
    else:
        lines.extend([
            "",
            "## Products with quantitative omega declarations",
            "",
            "_None in the evaluated corpora — all products returned `declared:false`._",
        ])

    qual_only = [p for p in summary["products"] if not p["declared"] and p["specific_lipids"]]
    if qual_only:
        lines.extend([
            "",
            "## Qualitative-only lipid call-outs (non-quantitative)",
            "",
            "| Shelf | Barcode | Product | Call-outs |",
            "|-------|---------|---------|-----------|",
        ])
        for p in qual_only[:50]:
            callouts = "; ".join(
                str(x.get("lipid")) for x in p["specific_lipids"][:3]
            )
            name = p["product_name"].replace("|", "/")
            lines.append(f"| {p['shelf']} | {p['barcode']} | {name} | {callouts} |")
        if len(qual_only) > 50:
            lines.append(f"| … | … | _{len(qual_only) - 50} more_ | … |")

    cov_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Omega lipid extraction method (P175)")
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run label-coverage measurement over live BSIP1 corpora",
    )
    parser.add_argument(
        "--single",
        help="Single-product test: path to BSIP1 JSON (optional sibling BSIP0 via --bsip0-json)",
    )
    parser.add_argument("--bsip0-json", help="Optional BSIP0 JSON for --single")
    args = parser.parse_args(argv)

    if args.single:
        bsip1 = json.loads(Path(args.single).read_text(encoding="utf-8"))
        bsip0 = None
        if args.bsip0_json:
            bsip0 = json.loads(Path(args.bsip0_json).read_text(encoding="utf-8"))
        result = evaluate_omega_lipid_extract(bsip1, bsip0)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.coverage:
        summary, shelf_totals = run_coverage()
        write_reports(summary, shelf_totals)
        print(json.dumps({
            "products_evaluated": summary["evaluated"],
            "declaring_omega3": summary["declaring_omega3"],
            "declaring_omega6": summary["declaring_omega6"],
            "declaring_either": summary["declaring_either"],
            "ratio_computable": summary["ratio_computable"],
            "report_dir": str(REPORT_DIR),
        }, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())