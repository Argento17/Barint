"""
dual_extract.py — Factory trust layer 4b: dual-extractor consensus (TASK-265 / P48 / P69)

GUARDS (hard):
  - Default mode: synthetic e2e fixtures. Raw-store mode via --raw-store CLI.
  - Does NOT modify replay_parse, the scoring engine, or any live artifact.
  - Read-only over inputs.
  - Zero Open Food Facts (OFF) — banned project-wide (TASK-238).
  - stdlib + subprocess to gemini CLI only; no new Python dependencies.

How it wires into the factory:
  This script runs at the extraction stage (post-scrape, pre-BSIP1).
  Fields that produce a DISAGREE or FLAG verdict block auto-publish and route
  to human review. Only fields with AGREE verdict are promoted to the scored
  pipeline. This prevents a single parser bug (or LLM hallucination) from
  silently corrupting downstream scores.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import hashlib
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Force UTF-8 stdout/stderr on Windows so Hebrew text doesn't crash print()
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path("C:/Bari")
FIXTURES_DIR = REPO_ROOT / "03_operations/spine/_fixtures_e2e/raw"
BSIP0_DIR = REPO_ROOT / "03_operations/spine/_e2e_out/bsip0"
OUT_DIR = REPO_ROOT / "03_operations/spine/_e2e_out"

GEMINI_BIN = shutil.which("gemini") or r"C:\Users\HP\AppData\Roaming\npm\gemini.cmd"

# Fields compared (numeric + ingredients)
NUMERIC_FIELDS = [
    "energy_kcal",
    "protein_g",
    "fat_g",
    "fat_saturated_g",
    "carbohydrates_g",
    "sugars_g",
    "dietary_fiber_g",
    "sodium_mg",
]
ALL_FIELDS = NUMERIC_FIELDS + ["ingredients"]

# Tolerance for numeric agreement
ABS_TOL = 0.1
REL_TOL = 0.01  # 1%

# Gemini call timeout (seconds)
GEMINI_TIMEOUT = 90


# ---------------------------------------------------------------------------
# Extractor A — rule-based (read existing BSIP0 outputs)
# ---------------------------------------------------------------------------

def _parse_numeric(raw):
    """Convert a raw string value to float, stripping units. Returns None on failure."""
    if raw is None:
        return None
    s = str(raw).strip()
    # Strip Hebrew unit suffixes and whitespace
    s = re.sub(r"[^\d.\-].*$", "", s)
    try:
        return float(s)
    except ValueError:
        return None


def extract_a(barcode: str, bsip0_source: Path | dict) -> dict:
    """Read BSIP0 JSON (file path or in-memory record) and normalise to canonical field names."""
    if isinstance(bsip0_source, Path):
        with open(bsip0_source, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = bsip0_source

    n = data.get("nutrition", {})
    return {
        "energy_kcal":    _parse_numeric(n.get("energy_kcal_raw")),
        "protein_g":      _parse_numeric(n.get("protein_raw")),
        "fat_g":          _parse_numeric(n.get("fat_raw")),
        "fat_saturated_g": _parse_numeric(n.get("saturated_fat_raw")),
        "carbohydrates_g": _parse_numeric(n.get("carbs_raw")),
        "sugars_g":       _parse_numeric(n.get("sugar_raw")),
        "dietary_fiber_g": _parse_numeric(n.get("fiber_raw")),
        "sodium_mg":      _parse_numeric(n.get("sodium_raw")),
        "ingredients":    (data.get("ingredients_raw") or "").strip() or None,
    }


# ---------------------------------------------------------------------------
# Extractor B — Gemini LLM (independent, different failure mode)
# ---------------------------------------------------------------------------

GEMINI_EXTRACTION_PROMPT_TEMPLATE = """\
You are a nutrition-label parser. Your ONLY job is to extract structured data from the HTML below.

STRICT RULES — you MUST follow all of them:
1. Extract ONLY values that are EXPLICITLY PRESENT in the provided HTML.
2. If a field is not in the HTML, return null for that field. DO NOT infer, estimate, \
round-from-memory, or use any outside world knowledge.
3. NEVER use Open Food Facts or any external data source (per project rule TASK-238). \
The HTML is the ONLY permitted source.
4. Return ONLY a single strict JSON object with EXACTLY these keys (no prose, no commentary, \
no markdown fences):
   energy_kcal, protein_g, fat_g, fat_saturated_g, carbohydrates_g, sugars_g, \
dietary_fiber_g, sodium_mg, ingredients
5. All numeric values as numbers (not strings). ingredients as a plain string or null.
6. No additional keys. No explanation. No units. Numbers only for numeric fields.

HTML TO PARSE:
{html}

Return the JSON object only. No prose before or after it."""


def _strip_json_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ``` or ``` ... ```)."""
    text = text.strip()
    # Remove opening fence
    text = re.sub(r"^```(?:json)?\s*\n?", "", text, flags=re.IGNORECASE)
    # Remove closing fence
    text = re.sub(r"\n?```\s*$", "", text)
    return text.strip()


def _permissive_json_parse(text: str) -> dict:
    """
    Try strict json.loads first; fall back to quoting unquoted keys
    (Gemini sometimes emits JS-object notation: {key: value}).
    Raises ValueError if all attempts fail.
    """
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: quote unquoted keys  e.g. {energy_kcal: 450, ...}
    # Only apply inside the outermost braces to avoid corrupting string values
    fixed = re.sub(
        r'(?<=[{,])\s*([A-Za-z_][A-Za-z0-9_]*)\s*:',
        lambda m: f' "{m.group(1)}":',
        text
    )
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass

    # Last resort: replace single-quote strings with double-quotes
    fixed2 = fixed.replace("'", '"')
    return json.loads(fixed2)  # raises if still bad


def extract_b(barcode: str, html_path: Path) -> dict | None:
    """
    Call Gemini CLI on the raw HTML and return parsed extraction dict.
    Returns None if the call fails or times out (caller marks B-side 'unavailable').
    """
    html_content = html_path.read_text(encoding="utf-8")
    
    # Split the template to pass most via stdin, and a small suffix via -p 
    # (to ensure -p is present for non-interactive mode).
    parts = GEMINI_EXTRACTION_PROMPT_TEMPLATE.split("{html}")
    prefix = parts[0]
    suffix = parts[1] if len(parts) > 1 else ""
    
    full_stdin = prefix + html_content + suffix

    cmd = [
        GEMINI_BIN,
        "--skip-trust",
        "-y",           # YOLO / auto-accept
        "-p", "Return the JSON object only.", # Trigger non-interactive mode
    ]

    try:
        result = subprocess.run(
            cmd,
            input=full_stdin,
            capture_output=True,
            text=True,
            timeout=GEMINI_TIMEOUT,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        print(f"  [B] TIMEOUT for barcode {barcode} after {GEMINI_TIMEOUT}s", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"  [B] gemini binary not found: {GEMINI_BIN}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [B] subprocess error for {barcode}: {e}", file=sys.stderr)
        return None

    stdout = result.stdout.strip()
    if result.returncode != 0:
        print(f"  [B] gemini exit {result.returncode} for {barcode}. stderr: {result.stderr[:400]}", file=sys.stderr)
        # Still try to parse stdout — gemini sometimes exits non-zero on warnings
        if not stdout:
            return None

    # Strip fences and parse JSON
    cleaned = _strip_json_fences(stdout)

    # If Gemini returned verbose text with a JSON block embedded, try to extract it
    if not cleaned.startswith("{"):
        # Search for first { ... } block
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if match:
            cleaned = match.group(0)
        else:
            print(f"  [B] no JSON found in Gemini output for {barcode}. Output: {stdout[:300]}", file=sys.stderr)
            return None

    try:
        parsed = _permissive_json_parse(cleaned)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"  [B] JSON parse error for {barcode}: {e}. Output: {cleaned[:300]}", file=sys.stderr)
        return None

    # Normalise to expected schema
    result_dict = {}
    for field in ALL_FIELDS:
        val = parsed.get(field)
        if field == "ingredients":
            result_dict[field] = str(val).strip() if val is not None else None
        else:
            if val is None:
                result_dict[field] = None
            else:
                try:
                    result_dict[field] = float(val)
                except (TypeError, ValueError):
                    result_dict[field] = None
    return result_dict


# ---------------------------------------------------------------------------
# Consensus compare
# ---------------------------------------------------------------------------

def compare_field(field: str, a_val, b_val) -> str:
    """
    Returns:
      AGREE        — both values match within tolerance
      DISAGREE     — both present but outside tolerance
      FLAG         — one present, other null
      BOTH_NULL    — both null (treated as AGREE for non-required fields)
    """
    a_none = a_val is None
    b_none = b_val is None

    if a_none and b_none:
        return "BOTH_NULL"

    if a_none != b_none:
        return "FLAG"

    # Both present
    if field == "ingredients":
        # String comparison: normalise whitespace
        a_norm = " ".join(str(a_val).split())
        b_norm = " ".join(str(b_val).split())
        return "AGREE" if a_norm == b_norm else "DISAGREE"
    else:
        # Numeric
        try:
            a_f = float(a_val)
            b_f = float(b_val)
        except (TypeError, ValueError):
            return "DISAGREE"
        diff = abs(a_f - b_f)
        rel = diff / max(abs(a_f), 1e-9)
        if diff <= ABS_TOL or rel <= REL_TOL:
            return "AGREE"
        return "DISAGREE"


def _field_verdict_tallies(products: list[dict]) -> dict:
    """Per-field AGREE / DISAGREE / FLAG / B_UNAVAILABLE counts from product field rows."""
    tallies = {
        field: {"AGREE": 0, "DISAGREE": 0, "FLAG": 0, "B_UNAVAILABLE": 0, "BOTH_NULL": 0}
        for field in ALL_FIELDS
    }
    for prod in products:
        for fr in prod["fields"]:
            verdict = fr["verdict"]
            if verdict in tallies[fr["field"]]:
                tallies[fr["field"]][verdict] += 1
    return tallies


def run_consensus(products: list[dict], *, meta: dict | None = None) -> dict:
    """Run full consensus comparison and return structured report."""
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fixtures_dir": str(FIXTURES_DIR),
        "bsip0_dir": str(BSIP0_DIR),
        "run_meta": meta or {"mode": "e2e_fixtures"},
        "fields_compared": ALL_FIELDS,
        "tolerance": {"absolute": ABS_TOL, "relative_pct": REL_TOL * 100},
        "fabrication_guard": (
            "Gemini prompt explicitly forbids: (1) inferring/estimating values, "
            "(2) using outside world knowledge, (3) using Open Food Facts or any "
            "external source (TASK-238). Disagreements with the rule-based parser "
            "are the consensus check — if Gemini invents a value it disagrees with "
            "Extractor A and is FLAGGED, never silently accepted."
        ),
        "factory_wiring": (
            "dual_extract.py runs at the extraction stage (post-scrape, pre-BSIP1). "
            "Fields with DISAGREE or FLAG verdict block auto-publish and route to "
            "human review. Only AGREE fields are promoted to the scored pipeline. "
            "B-side 'unavailable' (Gemini timeout/error) triggers manual review of "
            "the affected product — it does not crash the pipeline."
        ),
        "products": [],
        "summary": {},
    }

    total_fields = 0
    total_agree = 0
    total_disagree = 0
    total_flag = 0
    total_both_null = 0
    gemini_calls_ok = 0

    for p in products:
        barcode = p["barcode"]
        name = p["name"]
        a = p["extractor_a"]
        b = p["extractor_b"]
        b_available = b is not None

        if b_available:
            gemini_calls_ok += 1

        field_results = []
        for field in ALL_FIELDS:
            a_val = a.get(field) if a else None
            b_val = b.get(field) if b_available else None

            if not b_available:
                verdict = "B_UNAVAILABLE"
            else:
                verdict = compare_field(field, a_val, b_val)

            total_fields += 1
            if verdict == "AGREE":
                total_agree += 1
            elif verdict == "DISAGREE":
                total_disagree += 1
            elif verdict == "FLAG":
                total_flag += 1
            elif verdict == "BOTH_NULL":
                total_both_null += 1
                total_agree += 1  # BOTH_NULL counts as agreement for rate

            field_results.append({
                "field": field,
                "extractor_a": a_val,
                "extractor_b": b_val if b_available else "UNAVAILABLE",
                "verdict": verdict,
            })

        report["products"].append({
            "barcode": barcode,
            "name": name,
            "gemini_available": b_available,
            "fields": field_results,
        })

    # Agreement rate excludes B_UNAVAILABLE products from denominator
    compared_fields = total_fields - sum(
        1 for p in report["products"]
        for f in p["fields"] if f["verdict"] == "B_UNAVAILABLE"
    )
    agree_fields = total_agree
    agreement_rate = (agree_fields / compared_fields * 100) if compared_fields else 0.0

    b_unavailable_products = len(products) - gemini_calls_ok
    report["summary"] = {
        "products_cross_checked": len(products),
        "gemini_calls_ok": gemini_calls_ok,
        "gemini_calls_unavailable": b_unavailable_products,
        "fields_compared_total": total_fields,
        "fields_with_both_extractors": compared_fields,
        "fields_agree": total_agree,
        "fields_disagree": total_disagree,
        "fields_flag": total_flag,
        "fields_both_null": total_both_null,
        "agreement_rate_pct": round(agreement_rate, 1),
        "per_field_verdicts": _field_verdict_tallies(report["products"]),
        "nutrition_disagreements": [
            {
                "barcode": prod["barcode"],
                "name": prod["name"],
                "field": fr["field"],
                "extractor_a": fr["extractor_a"],
                "extractor_b": fr["extractor_b"],
                "verdict": fr["verdict"],
            }
            for prod in report["products"]
            for fr in prod["fields"]
            if fr["field"] in NUMERIC_FIELDS and fr["verdict"] == "DISAGREE"
        ],
    }

    return report


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def render_md(report: dict) -> str:
    lines = []
    lines.append("# Dual Extractor Consensus Report")
    lines.append("")
    lines.append(f"Generated: {report['generated_at']}")
    lines.append("")
    lines.append("## Summary")
    s = report["summary"]
    lines.append(f"- Products cross-checked: **{s['products_cross_checked']}**")
    lines.append(f"- Gemini calls succeeded: **{s['gemini_calls_ok']}**")
    lines.append(f"- Fields with both extractors: **{s['fields_with_both_extractors']}**")
    lines.append(f"- Fields AGREE: **{s['fields_agree']}** (includes BOTH_NULL)")
    lines.append(f"- Fields DISAGREE: **{s['fields_disagree']}**")
    lines.append(f"- Gemini calls unavailable: **{s.get('gemini_calls_unavailable', 0)}**")
    lines.append(f"- Fields FLAG (one-missing): **{s['fields_flag']}**")
    lines.append(f"- Agreement rate: **{s['agreement_rate_pct']}%**")
    lines.append("")
    if s.get("per_field_verdicts"):
        lines.append("### Per-field verdict tallies")
        lines.append("")
        lines.append("| Field | AGREE | DISAGREE | FLAG | B_UNAVAILABLE |")
        lines.append("|---|---:|---:|---:|---:|")
        for field in ALL_FIELDS:
            fv = s["per_field_verdicts"][field]
            lines.append(
                f"| {field} | {fv['AGREE']} | {fv['DISAGREE']} | {fv['FLAG']} | {fv['B_UNAVAILABLE']} |"
            )
        lines.append("")
    nutrition_disagreements = s.get("nutrition_disagreements") or []
    if nutrition_disagreements:
        lines.append("## Nutrition field DISAGREEMENTS")
        lines.append("")
        for row in nutrition_disagreements:
            lines.append(
                f"- **{row['barcode']}** ({row['name']}): `{row['field']}` "
                f"A={row['extractor_a']} vs B={row['extractor_b']}"
            )
        lines.append("")
    lines.append(f"Tolerance: abs={report['tolerance']['absolute']}, "
                 f"rel={report['tolerance']['relative_pct']}%")
    lines.append("")
    lines.append("## Fabrication Guard")
    lines.append("")
    lines.append(report["fabrication_guard"])
    lines.append("")
    lines.append("## Factory Wiring")
    lines.append("")
    lines.append(report["factory_wiring"])
    lines.append("")

    for p in report["products"]:
        lines.append(f"## Product: {p['name']} (barcode {p['barcode']})")
        lines.append("")
        if not p["gemini_available"]:
            lines.append("**Gemini (Extractor B): UNAVAILABLE** — manual review required.")
            lines.append("")

        lines.append("| Field | Extractor A (rule-based) | Extractor B (Gemini) | Verdict |")
        lines.append("|---|---|---|---|")
        for fr in p["fields"]:
            a_disp = str(fr["extractor_a"]) if fr["extractor_a"] is not None else "null"
            b_disp = str(fr["extractor_b"]) if fr["extractor_b"] not in (None, "UNAVAILABLE") else str(fr["extractor_b"])
            verdict = fr["verdict"]
            flag = ""
            if verdict in ("DISAGREE", "FLAG"):
                flag = " **"
            lines.append(f"| {fr['field']} | {a_disp} | {b_disp} | {verdict}{flag} |")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Discovery helpers
# ---------------------------------------------------------------------------

def _resolve_repo_path(path_str: str) -> Path:
    p = Path(path_str)
    if p.is_absolute():
        return p
    return REPO_ROOT / p


def load_in_scored_barcodes(corpus_path: Path) -> set[str]:
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    return {
        str(p["barcode"])
        for p in corpus.get("products", [])
        if p.get("decision") == "IN_SCORED"
    }


def load_bsip0_index(bsip0_path: Path) -> dict[str, dict]:
    raw = json.loads(bsip0_path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        records = raw
    elif isinstance(raw, dict) and "products" in raw:
        records = raw["products"]
    else:
        records = [raw]
    return {str(r.get("barcode", "")): r for r in records if r.get("barcode")}


def discover_raw_store_pairs(raw_store_dir: Path) -> dict[str, Path]:
    """Map barcode -> latest banked HTML under per-page_id subfolders."""
    pairs: dict[str, Path] = {}
    for page_dir in sorted(raw_store_dir.glob("P_*")):
        if not page_dir.is_dir():
            continue
        barcode = page_dir.name[2:] if page_dir.name.startswith("P_") else page_dir.name
        html_files = sorted(page_dir.glob("*.html"))
        if html_files:
            pairs[barcode] = html_files[-1]
    return pairs


def discover_e2e_products() -> list[dict]:
    html_files = sorted(FIXTURES_DIR.glob("raw_e2e_*.html"))
    if not html_files:
        raise FileNotFoundError("no HTML fixtures found")

    products_input = []
    for html_path in html_files:
        idx = re.search(r"raw_e2e_(\d+)\.html", html_path.name)
        if not idx:
            continue
        fixture_num = idx.group(1)

        bsip0_candidates = sorted(BSIP0_DIR.glob("bsip0_*.json"))
        matched_bsip0 = None
        for bc in bsip0_candidates:
            with open(bc, encoding="utf-8") as f:
                d = json.load(f)
            src = d.get("source_url", "")
            if f"raw_e2e_{fixture_num}" in src:
                matched_bsip0 = (bc, d)
                break

        if matched_bsip0 is None:
            print(f"  [A] WARNING: no BSIP0 match for {html_path.name}", file=sys.stderr)
            continue

        bsip0_path, bsip0_data = matched_bsip0
        barcode = bsip0_data.get("barcode", f"unknown_{fixture_num}")
        name = bsip0_data.get("name_he", f"product_{fixture_num}")

        products_input.append({
            "barcode": barcode,
            "name": name,
            "html_path": html_path,
            "bsip0_source": bsip0_path,
        })
    return products_input

def discover_raw_store_products(
    raw_store_dir: Path,
    bsip0_path: Path,
    corpus_path: Path | None,
    limit: int | None,
) -> tuple[list[dict], dict]:
    html_by_barcode = discover_raw_store_pairs(raw_store_dir)
    bsip0_index = load_bsip0_index(bsip0_path)

    allowed: set[str] | None = None
    if corpus_path is not None:
        allowed = load_in_scored_barcodes(corpus_path)

    products_input = []
    for barcode in sorted(html_by_barcode):
        if allowed is not None and barcode not in allowed:
            continue
        bsip0_record = bsip0_index.get(barcode)
        if bsip0_record is None:
            print(f"  [A] WARNING: no BSIP0 record for barcode {barcode}", file=sys.stderr)
            continue
        products_input.append({
            "barcode": barcode,
            "name": bsip0_record.get("name_he", barcode),
            "html_path": html_by_barcode[barcode],
            "bsip0_source": bsip0_record,
        })
        if limit is not None and len(products_input) >= limit:
            break

    meta = {
        "mode": "raw_store",
        "raw_store_dir": str(raw_store_dir),
        "bsip0_path": str(bsip0_path),
        "corpus_path": str(corpus_path) if corpus_path else None,
        "in_scored_filter": allowed is not None,
        "limit": limit,
        "html_discovered": len(html_by_barcode),
        "products_selected": len(products_input),
    }
    return products_input, meta


def process_products(
    products_input: list[dict],
    *,
    stop_unavailable_pct: float = 0.30,
) -> tuple[list[dict], bool]:
    products_data = []
    stopped_early = False

    for i, p in enumerate(products_input, start=1):
        print(f"Processing [{i}/{len(products_input)}]: {p['name']} ({p['barcode']})")

        print(f"  [A] Reading BSIP0 for {p['barcode']}")
        a_result = extract_a(p["barcode"], p["bsip0_source"])
        print(f"  [A] OK — energy={a_result.get('energy_kcal')}, protein={a_result.get('protein_g')}")

        print(f"  [B] Calling Gemini on {p['html_path'].name} ...")
        b_result = extract_b(p["barcode"], p["html_path"])
        if b_result is None:
            print("  [B] UNAVAILABLE — marking for manual review")
        else:
            print(f"  [B] OK — energy={b_result.get('energy_kcal')}, protein={b_result.get('protein_g')}")

        products_data.append({
            "barcode": p["barcode"],
            "name": p["name"],
            "extractor_a": a_result,
            "extractor_b": b_result,
        })
        print()

        processed = len(products_data)
        unavailable = sum(1 for row in products_data if row["extractor_b"] is None)
        if processed >= 3 and (unavailable / processed) > stop_unavailable_pct:
            print(
                f"STOPPING EARLY: {unavailable}/{processed} products B-unavailable "
                f"({unavailable / processed * 100:.1f}% > {stop_unavailable_pct * 100:.0f}% threshold).",
                file=sys.stderr,
            )
            stopped_early = True
            break

    return products_data, stopped_early


def emit_report(report: dict, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "dual_extract_report.json"
    md_path = out_dir / "dual_extract_report.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Written: {json_path}")

    md_content = render_md(report)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Written: {md_path}")
    return json_path, md_path

def print_summary(report: dict) -> None:
    s = report["summary"]
    print()
    print("=== CONSENSUS SUMMARY ===")
    print(f"  Products cross-checked : {s['products_cross_checked']}")
    print(f"  Gemini calls OK        : {s['gemini_calls_ok']}")
    print(f"  Gemini unavailable     : {s.get('gemini_calls_unavailable', 0)}")
    print(f"  Fields compared        : {s['fields_with_both_extractors']}")
    print(f"  AGREE                  : {s['fields_agree']}")
    print(f"  DISAGREE               : {s['fields_disagree']}")
    print(f"  FLAG                   : {s['fields_flag']}")
    print(f"  Agreement rate         : {s['agreement_rate_pct']}%")

    if s.get("per_field_verdicts"):
        print()
        print("=== PER-FIELD VERDICTS (key nutrition) ===")
        for field in ["energy_kcal", "protein_g", "fat_g", "sodium_mg", "sugars_g"]:
            fv = s["per_field_verdicts"].get(field, {})
            print(
                f"  {field:<18} AGREE={fv.get('AGREE', 0)} "
                f"DISAGREE={fv.get('DISAGREE', 0)} FLAG={fv.get('FLAG', 0)} "
                f"B_UNAVAIL={fv.get('B_UNAVAILABLE', 0)}"
            )

    nutrition_disagreements = s.get("nutrition_disagreements") or []
    if nutrition_disagreements:
        print()
        print("=== NUTRITION DISAGREEMENTS ===")
        for row in nutrition_disagreements:
            print(
                f"  {row['barcode']} {row['field']}: "
                f"A={row['extractor_a']} vs B={row['extractor_b']}"
            )

    print()
    print("=== PER-PRODUCT FIELD TABLE ===")
    for prod in report["products"]:
        print(f"\n{prod['name']} ({prod['barcode']})")
        print(f"  {'Field':<22} {'A':>10}  {'B':>10}  Verdict")
        print(f"  {'-'*22} {'-'*10}  {'-'*10}  -------")
        for fr in prod["fields"]:
            a_s = str(fr["extractor_a"]) if fr["extractor_a"] is not None else "null"
            b_s = str(fr["extractor_b"]) if fr["extractor_b"] not in (None, "UNAVAILABLE") else str(fr["extractor_b"])
            marker = " <-- REVIEW" if fr["verdict"] in ("DISAGREE", "FLAG") else ""
            print(f"  {fr['field']:<22} {a_s:>10}  {b_s:>10}  {fr['verdict']}{marker}")

    if s["fields_disagree"] > 0 or s["fields_flag"] > 0:
        print()
        print(f"NOTE: {s['fields_disagree']} DISAGREE + {s['fields_flag']} FLAG field(s) found.")
        print("These would block auto-publish in the factory. See report for details.")

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dual-extractor consensus (rule-based BSIP0 vs Gemini on banked HTML)."
    )
    parser.add_argument("--raw-store", help="raw_store category dir with per-code subfolders and manifest.jsonl")
    parser.add_argument("--bsip0", help="BSIP0 raw JSON (array of products) for extractor A")
    parser.add_argument("--corpus", help="Optional corpus_filter.json; restrict to IN_SCORED barcodes")
    parser.add_argument("--out", help="Output directory for consensus report (default: _e2e_out or alongside run)")
    parser.add_argument("--limit", type=int, default=None, help="Optional cap on products processed (rate-limit safety)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None):
    args = parse_args(argv)
    use_raw_store = bool(args.raw_store)

    if use_raw_store:
        if not args.bsip0:
            print("ERROR: --raw-store requires --bsip0", file=sys.stderr)
            sys.exit(2)
        raw_store_dir = _resolve_repo_path(args.raw_store)
        bsip0_path = _resolve_repo_path(args.bsip0)
        corpus_path = _resolve_repo_path(args.corpus) if args.corpus else None
        out_dir = _resolve_repo_path(args.out) if args.out else raw_store_dir.parent / "dual_extract"
        print("=== dual_extract.py — raw_store mode (P69) ===")
        print(f"Raw store: {raw_store_dir}")
        print(f"BSIP0    : {bsip0_path}")
        print(f"Corpus   : {corpus_path or '(all banked HTML with BSIP0 match)'}")
        print(f"Output   : {out_dir}")
        print(f"Gemini   : {GEMINI_BIN}")
        if args.limit:
            print(f"Limit    : {args.limit}")
        print()

        products_input, run_meta = discover_raw_store_products(
            raw_store_dir, bsip0_path, corpus_path, args.limit
        )
        if not products_input:
            print("ERROR: no products to process after discovery/filter.", file=sys.stderr)
            sys.exit(1)
        print(f"Found {len(products_input)} product(s) to process.\n")
    else:
        out_dir = _resolve_repo_path(args.out) if args.out else OUT_DIR
        run_meta = {"mode": "e2e_fixtures"}
        print("=== dual_extract.py — e2e fixture mode (TASK-265 / P48) ===")
        print(f"Fixtures : {FIXTURES_DIR}")
        print(f"BSIP0 dir: {BSIP0_DIR}")
        print(f"Output   : {out_dir}")
        print(f"Gemini   : {GEMINI_BIN}")
        print()
        try:
            products_input = discover_e2e_products()
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        if args.limit is not None:
            products_input = products_input[: args.limit]
        print(f"Found {len(products_input)} fixture(s) to process.\n")

    products_data, stopped_early = process_products(products_input)
    if stopped_early:
        run_meta["stopped_early_unavailable_threshold"] = True

    report = run_consensus(products_data, meta=run_meta)
    emit_report(report, out_dir)
    print_summary(report)

    print()
    print("dual_extract.py complete. Exit 0.")
    sys.exit(0)


if __name__ == "__main__":
    main()
