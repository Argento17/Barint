"""
Composition gate for bread_retail_003 acquisition.

Purpose: verify the scraped corpus is a representative supermarket shelf,
not a wellness/premium universe. Classifies each product into archetypes,
then checks structural thresholds.

Gate PASS criteria:
  - Total products    ≥ 150
  - Mainstream share  ≥ 20%   (commodity_white + generic_bread + pita + laffah + toast_loaf + challah + baguette)
  - Non-wellness share ≥ 20%  (same as above — same definition)
  - Spelt share       ≤ 20%
  - Sourdough-label   ≤ 20%
  - Commodity anchors ≥ 10    (commodity_white + generic_bread)
  - Simple white bread ≥ 5
  - Pita/toast        ≥ 5
"""

from __future__ import annotations
import re
from typing import NamedTuple


# ──────────────────────────────────────────────────────────────────────────────
# Archetype classifier
# ──────────────────────────────────────────────────────────────────────────────

ARCHETYPE_RULES: list[tuple[str, list[str]]] = [
    # order matters — first match wins
    ("cracker",         ["קרקר", "פריך", "מצה", "cracker", "crispbread", "לחמית"]),
    ("pita",            ["פיתה", "פיטה", "פיתות", "פיטות"]),
    ("laffah",          ["לאפה", "לאפות"]),
    ("toast_loaf",      ["טוסט", "toast"]),
    ("baguette",        ["בגט", "baguette", "צ'בטה", "ciabatta"]),
    ("challah",         ["חלה", "challah"]),
    ("sourdough_label", ["מחמצת", "sourdough"]),
    ("rye",             ["שיפון", "rye"]),
    ("spelt",           ["כוסמין", "spelt"]),
    ("wholegrain",      ["קמח מלא", "100% מלא", "מלא 100%", "חיטה מלאה", "שיבולת שועל", "whole grain", "wholegrain"]),
    ("rolls",           ["לחמנייה", "לחמניה", "לחמניות", "roll"]),
    ("flatbread",       ["פוקצ'ה", "focaccia", "נאן", "naan", "tortilla", "טורטייה"]),
    ("specialty_diet",  ["ללא גלוטן", "gluten free", "gluten-free", "vegan", "טבעוני", "דיאט"]),
    ("commodity_white", ["לחם לבן", "לחם חלב", "לחם אחיד", "white bread", "לחם רגיל"]),
]

# Commodity anchor keywords (in product name) — broad plain bread signals
COMMODITY_ANCHOR_KW = [
    "לחם לבן", "לחם אחיד", "לחם חלב", "לחם רגיל",
    "ברמן", "וונדר", "wonder", "berman",
    "לחם קל", "לחם פרוס",
    "לחם תוצרת בית",
]

# Simple white bread signals (subset of commodity anchors)
SIMPLE_WHITE_KW = [
    "לחם לבן", "לחם אחיד", "לחם חלב",
    "ברמן", "וונדר", "wonder",
]

# Mainstream archetypes
MAINSTREAM_ARCHETYPES = {
    "commodity_white", "generic_bread", "pita", "laffah",
    "toast_loaf", "challah", "baguette",
}


def classify_archetype(name_he: str) -> str:
    name = name_he.strip()
    for archetype, keywords in ARCHETYPE_RULES:
        if any(kw in name for kw in keywords):
            return archetype
    # Generic bread fallback
    if re.search(r"\bלחם\b", name):
        return "generic_bread"
    return "other"


def is_commodity_anchor(name_he: str) -> bool:
    return any(kw in name_he for kw in COMMODITY_ANCHOR_KW)


def is_simple_white(name_he: str) -> bool:
    return any(kw in name_he for kw in SIMPLE_WHITE_KW)


def is_pita_or_toast(name_he: str) -> bool:
    archetype = classify_archetype(name_he)
    return archetype in ("pita", "laffah", "toast_loaf")


# ──────────────────────────────────────────────────────────────────────────────
# Gate result
# ──────────────────────────────────────────────────────────────────────────────

class GateResult(NamedTuple):
    passed: bool
    total: int
    archetype_counts: dict[str, int]
    archetype_pcts: dict[str, float]
    mainstream_count: int
    mainstream_pct: float
    spelt_count: int
    spelt_pct: float
    sourdough_label_count: int
    sourdough_label_pct: float
    commodity_anchor_count: int
    simple_white_count: int
    pita_toast_count: int
    failures: list[str]
    warnings: list[str]


def check_composition(products: list[dict]) -> GateResult:
    """
    Classify products and run all gate checks.
    products: list of raw BSIP0 dicts with at least 'name_he' field.
    """
    total = len(products)
    archetype_counts: dict[str, int] = {}
    mainstream_count = 0
    commodity_count = 0
    simple_white_count = 0
    pita_toast_count = 0

    for p in products:
        name = p.get("name_he", "") or ""
        arch = classify_archetype(name)
        archetype_counts[arch] = archetype_counts.get(arch, 0) + 1
        if arch in MAINSTREAM_ARCHETYPES:
            mainstream_count += 1
        if is_commodity_anchor(name):
            commodity_count += 1
        if is_simple_white(name):
            simple_white_count += 1
        if is_pita_or_toast(name):
            pita_toast_count += 1

    def pct(n: int) -> float:
        return round(n * 100 / total, 1) if total > 0 else 0.0

    archetype_pcts = {k: pct(v) for k, v in archetype_counts.items()}

    spelt_count = archetype_counts.get("spelt", 0)
    sourdough_count = archetype_counts.get("sourdough_label", 0)
    mainstream_pct = pct(mainstream_count)
    spelt_pct = pct(spelt_count)
    sourdough_pct = pct(sourdough_count)

    failures: list[str] = []
    warnings: list[str] = []

    if total < 150:
        failures.append(f"FAIL: total products {total} < 150 required")
    if mainstream_pct < 20:
        failures.append(f"FAIL: mainstream {mainstream_pct}% < 20% required (n={mainstream_count})")
    if spelt_pct > 20:
        failures.append(f"FAIL: spelt {spelt_pct}% > 20% cap (n={spelt_count})")
    if sourdough_pct > 20:
        failures.append(f"FAIL: sourdough-label {sourdough_pct}% > 20% cap (n={sourdough_count})")
    if commodity_count < 10:
        failures.append(f"FAIL: commodity anchors {commodity_count} < 10 required")
    if simple_white_count < 5:
        failures.append(f"FAIL: simple white bread {simple_white_count} < 5 required")
    if pita_toast_count < 5:
        failures.append(f"FAIL: pita/toast {pita_toast_count} < 5 required")

    if mainstream_pct < 30 and not [f for f in failures if "mainstream" in f]:
        warnings.append(f"WARN: mainstream {mainstream_pct}% is above threshold but low — consider adding more commodity queries")
    if spelt_pct > 15 and spelt_pct <= 20:
        warnings.append(f"WARN: spelt {spelt_pct}% approaching cap")
    if sourdough_pct > 15 and sourdough_pct <= 20:
        warnings.append(f"WARN: sourdough-label {sourdough_pct}% approaching cap")

    passed = len(failures) == 0

    return GateResult(
        passed=passed,
        total=total,
        archetype_counts=archetype_counts,
        archetype_pcts=archetype_pcts,
        mainstream_count=mainstream_count,
        mainstream_pct=mainstream_pct,
        spelt_count=spelt_count,
        spelt_pct=spelt_pct,
        sourdough_label_count=sourdough_count,
        sourdough_label_pct=sourdough_pct,
        commodity_anchor_count=commodity_count,
        simple_white_count=simple_white_count,
        pita_toast_count=pita_toast_count,
        failures=failures,
        warnings=warnings,
    )


def print_gate_result(gate: GateResult) -> None:
    status = "PASS" if gate.passed else "FAIL"
    print(f"\n=== Composition Gate: {status} ===")
    print(f"Total products: {gate.total}")
    print(f"Mainstream:     {gate.mainstream_count} ({gate.mainstream_pct}%) [need ≥20%]")
    print(f"Spelt:          {gate.spelt_count} ({gate.spelt_pct}%) [cap ≤20%]")
    print(f"Sourdough-label:{gate.sourdough_label_count} ({gate.sourdough_label_pct}%) [cap ≤20%]")
    print(f"Commodity anchors: {gate.commodity_anchor_count} [need ≥10]")
    print(f"Simple white bread: {gate.simple_white_count} [need ≥5]")
    print(f"Pita/toast:     {gate.pita_toast_count} [need ≥5]")
    print("\nArchetype breakdown:")
    for arch, count in sorted(gate.archetype_counts.items(), key=lambda x: -x[1]):
        print(f"  {arch:20s}: {count:4d} ({gate.archetype_pcts[arch]:.1f}%)")
    if gate.failures:
        print("\nFailures:")
        for f in gate.failures:
            print(f"  {f}")
    if gate.warnings:
        print("\nWarnings:")
        for w in gate.warnings:
            print(f"  {w}")


if __name__ == "__main__":
    import sys, json
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) > 1:
        data = json.loads(open(sys.argv[1], encoding="utf-8").read())
        products = data if isinstance(data, list) else data.get("products", [])
        gate = check_composition(products)
        print_gate_result(gate)
    else:
        print("Usage: composition_gate.py <raw_json_file>")
