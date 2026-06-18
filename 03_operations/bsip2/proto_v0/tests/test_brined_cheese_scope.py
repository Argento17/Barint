"""
EV-052 / TASK-266 — Regression test for brined-cheese `brined_food` keyword wiring.

Tests four guarantee groups:
  (a) Each of the 5 new keywords (בולגרית, פטה, צפתית, חלומי, גבינה מלוחה)
      with sodium > 500 receives context_flag == "brined_food".
  (b) The existing olives/pickles keywords still fire (no regression).
  (c) No cross-category leakage: cottage (קוטג'), hard cheese (גאודה), and a
      low-sodium item with a brined-cheese name do NOT get the brined_food flag.
  (d) Sodium > 500 guard gates correctly: a product with a matching name but
      sodium <= 500 mg must NOT receive the brined_food flag.

Run from repo root:
    python 03_operations/bsip2/proto_v0/tests/test_brined_cheese_scope.py

Or from any directory (the script fixes up sys.path automatically).

Guards:
  - Read-only over the engine source.
  - stdlib only; no new dependencies.
  - OFF ban: no Open Food Facts data introduced.
"""

import os
import pathlib
import sys

# ---------------------------------------------------------------------------
# Path setup: resolve engine src regardless of invocation directory.
# ---------------------------------------------------------------------------
_THIS_FILE = pathlib.Path(__file__).resolve()
_TESTS_DIR = _THIS_FILE.parent                          # .../proto_v0/tests
_SRC_DIR   = _TESTS_DIR.parent / "src"                  # .../proto_v0/src
_REPO_ROOT  = _TESTS_DIR.parents[3]                     # C:\Bari

if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# Change cwd to src so engine's own relative imports (if any) resolve cleanly.
os.chdir(str(_SRC_DIR))

# Pin engine flags to a clean baseline (matching engine_invariants.py conventions).
_DEFAULT_FLAGS = {
    "BARI_TASK144_FIXES":        "off",
    "BARI_RECAL_P0":             "off",
    "BARI_RECAL_P0_YOGURT_TRIM": "off",
    "BARI_GLASSBOX_D5D6":        "off",
    "BARI_GLASSBOX_W15":         "off",
    "BARI_GLASSBOX_W2":          "off",
    "BARI_GLASSBOX_W4":          "on",
    "BARI_SODIUM_CEREAL":        "off",
    "BARI_REDLABEL_V1":          "off",
    "BARI_TASK250_CONF":         "off",
}
for _k, _v in _DEFAULT_FLAGS.items():
    os.environ[_k] = _v

# Purge any cached engine modules so flag values above are respected.
for _mod in list(sys.modules.keys()):
    try:
        _f = getattr(sys.modules[_mod], "__file__", None)
        if _f and pathlib.Path(_f).resolve().parent == _SRC_DIR:
            del sys.modules[_mod]
    except Exception:
        pass

from evaluation_scope import assign_evaluation_scope  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_product(name_he: str, sodium_mg: float) -> dict:
    """Minimal product dict sufficient for assign_evaluation_scope."""
    return {
        "canonical_name_he": name_he,
        "ingredients_text_he": "",
        "normalized_nutrition_per_100g": {
            "energy_kcal":     200.0,
            "fat_g":           10.0,
            "fat_saturated_g": 5.0,
            "fat_trans_g":     None,
            "sodium_mg":       sodium_mg,
            "carbohydrates_g": 1.0,
            "sugars_g":        0.5,
            "dietary_fiber_g": 0.0,
            "protein_g":       12.0,
        },
        "ingredients_list": ["חלב", "מלח", "תרבית חיידקים"],
    }


def _scope(name_he: str, sodium_mg: float) -> dict:
    """Return the full assign_evaluation_scope result for a product."""
    return assign_evaluation_scope(_make_product(name_he, sodium_mg), category="brined_cheese")


# ---------------------------------------------------------------------------
# Group (a): New brined-cheese keywords fire with sodium > 500
# ---------------------------------------------------------------------------

GROUP_A_CASES = [
    # (product_name, sodium_mg, description)
    ("גבינה בולגרית מסורתית 16%",       700.0, "בולגרית — standard fat, high sodium"),
    ("גבינה בולגרית מעודנת 5%",          550.0, "בולגרית — refined low-fat variant"),
    ("גבינת פטה כבשים",                   800.0, "פטה — sheep milk"),
    ("פטה עיזים 180 גרם",                 650.0, "פטה — goat milk"),
    ("גבינה צפתית רכה",                  600.0, "צפתית"),
    ("גבינת חלומי לצלייה",               900.0, "חלומי — grilling variant"),
    ("גבינה מלוחה בבריין",               750.0, "גבינה מלוחה — generic salty brine"),
]


def test_group_a() -> list:
    """(a) Each new keyword fires context_flag == 'brined_food' when sodium > 500."""
    failures = []
    for name, sodium, desc in GROUP_A_CASES:
        result = _scope(name, sodium)
        flag = result.get("context_flag")
        status = result.get("evaluation_status")
        if flag != "brined_food":
            failures.append(
                f"  FAIL [{desc}]: name='{name}', sodium={sodium} "
                f"→ context_flag={flag!r} (expected 'brined_food')"
            )
        elif status != "context_limited":
            failures.append(
                f"  FAIL [{desc}]: name='{name}', sodium={sodium} "
                f"→ evaluation_status={status!r} (expected 'context_limited')"
            )
        else:
            print(f"  PASS (a) {desc}: '{name}' sodium={sodium} → brined_food / context_limited")
    return failures


# ---------------------------------------------------------------------------
# Group (b): Existing olives/pickles keywords still fire (no regression)
# ---------------------------------------------------------------------------

GROUP_B_CASES = [
    ("זיתים ירוקים ממולאים",             800.0, "זיתים"),
    ("זיתים כבושים שחורים",              700.0, "זיתים כבושים"),
    ("חמוצים מלפפונים",                  600.0, "חמוצים"),
    ("כרוב כבוש",                        650.0, "כרוב כבוש"),
    ("ירקות כבושים מיקס",               700.0, "ירקות כבושים"),
    ("קיפר במי מלח",                    900.0, "קיפר"),
]


def test_group_b() -> list:
    """(b) Existing keywords still fire — no regression introduced."""
    failures = []
    for name, sodium, desc in GROUP_B_CASES:
        result = _scope(name, sodium)
        flag = result.get("context_flag")
        if flag != "brined_food":
            failures.append(
                f"  FAIL REGRESSION [{desc}]: name='{name}', sodium={sodium} "
                f"→ context_flag={flag!r} (expected 'brined_food' — REGRESSION)"
            )
        else:
            print(f"  PASS (b) {desc}: '{name}' sodium={sodium} → brined_food (no regression)")
    return failures


# ---------------------------------------------------------------------------
# Group (c): No cross-category leakage
# ---------------------------------------------------------------------------

GROUP_C_CASES = [
    # (product_name, sodium_mg, description, expected_flag)
    ("קוטג' 5% שומן",                      300.0, "cottage — not brined, low sodium", None),
    ("קוטג' עם ירקות 9%",                  350.0, "cottage — not brined, moderate sodium", None),
    ("גבינה צהובה גאודה",                  550.0, "גאודה — hard aged cheese, not brined", None),
    ("גבינת עמק פרוסות",                   600.0, "עמק — hard sliced cheese, not brined", None),
    # A product with a matching word but sodium <= 500 — handled in group (d), but also
    # confirm non-brined high-sodium products (sauce, condiment) do not leakage-flag.
    ("רוטב עגבניות מרוכז",                 700.0, "tomato paste — high sodium, not cheese", None),
    ("חלב 3% שומן",                        120.0, "whole milk — low sodium", None),
]


def test_group_c() -> list:
    """(c) Non-brined products do NOT receive brined_food context_flag."""
    failures = []
    for name, sodium, desc, expected_flag in GROUP_C_CASES:
        result = _scope(name, sodium)
        flag = result.get("context_flag")
        if flag == "brined_food":
            failures.append(
                f"  FAIL LEAKAGE [{desc}]: name='{name}', sodium={sodium} "
                f"→ context_flag='brined_food' (should NOT be flagged — cross-category leakage)"
            )
        else:
            print(f"  PASS (c) {desc}: '{name}' sodium={sodium} → context_flag={flag!r} (not brined_food)")
    return failures


# ---------------------------------------------------------------------------
# Group (d): Sodium > 500 guard gates correctly
# ---------------------------------------------------------------------------

GROUP_D_CASES = [
    # Name matches a brined-cheese keyword but sodium is <= 500 — must NOT be flagged.
    ("גבינה בולגרית מעודנת",  499.0, "בולגרית name, sodium=499 (below guard) — must be standard"),
    ("גבינה בולגרית מעודנת",  500.0, "בולגרית name, sodium=500 (at guard boundary) — must be standard"),
    ("פטה עיזים",              300.0, "פטה name, sodium=300 (low-sodium product) — must be standard"),
    ("גבינת חלומי",            450.0, "חלומי name, sodium=450 (below guard) — must be standard"),
    ("גבינה מלוחה",            490.0, "גבינה מלוחה name, sodium=490 (below guard) — must be standard"),
]

GROUP_D_CASES_FIRE = [
    # Sodium = 501 — just above the guard — must fire.
    ("גבינה בולגרית מעודנת",  501.0, "בולגרית name, sodium=501 (just above guard) — must fire"),
    ("פטה כבשים",              501.0, "פטה name, sodium=501 — must fire"),
]


def test_group_d() -> list:
    """(d) Sodium > 500 guard gates correctly (border + boundary cases)."""
    failures = []

    # Cases that must NOT fire (sodium <= 500)
    for name, sodium, desc in GROUP_D_CASES:
        result = _scope(name, sodium)
        flag = result.get("context_flag")
        if flag == "brined_food":
            failures.append(
                f"  FAIL GUARD [{desc}]: name='{name}', sodium={sodium} "
                f"→ context_flag='brined_food' (sodium guard should have blocked this)"
            )
        else:
            print(f"  PASS (d) {desc}: '{name}' sodium={sodium} → context_flag={flag!r} (guard held)")

    # Cases that MUST fire (sodium > 500)
    for name, sodium, desc in GROUP_D_CASES_FIRE:
        result = _scope(name, sodium)
        flag = result.get("context_flag")
        if flag != "brined_food":
            failures.append(
                f"  FAIL GUARD-OVER [{desc}]: name='{name}', sodium={sodium} "
                f"→ context_flag={flag!r} (expected brined_food — guard over-triggered)"
            )
        else:
            print(f"  PASS (d) {desc}: '{name}' sodium={sodium} → brined_food (guard passed correctly)")

    return failures


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all() -> dict:
    print()
    print("=" * 70)
    print("EV-052 / TASK-266 — Brined Cheese Scope Regression Test")
    print("=" * 70)
    print()

    results = {}

    print("--- Group (a): New keywords fire with sodium > 500 ---")
    results["a_new_keywords_fire"] = test_group_a()
    print()

    print("--- Group (b): Existing olives/pickles keywords (no regression) ---")
    results["b_existing_no_regression"] = test_group_b()
    print()

    print("--- Group (c): No cross-category leakage ---")
    results["c_no_leakage"] = test_group_c()
    print()

    print("--- Group (d): Sodium guard gates correctly ---")
    results["d_sodium_guard"] = test_group_d()
    print()

    # Summary
    print("=" * 70)
    total_pass = 0
    total_fail = 0
    for group, failures in results.items():
        n_cases = {
            "a_new_keywords_fire":       len(GROUP_A_CASES),
            "b_existing_no_regression":  len(GROUP_B_CASES),
            "c_no_leakage":              len(GROUP_C_CASES),
            "d_sodium_guard":            len(GROUP_D_CASES) + len(GROUP_D_CASES_FIRE),
        }[group]
        n_fail = len(failures)
        n_pass = n_cases - n_fail
        total_pass += n_pass
        total_fail += n_fail
        status = "PASS" if n_fail == 0 else "FAIL"
        print(f"  {group:35s}  [{status}]  ({n_pass}/{n_cases} pass)")
        for f in failures:
            print(f)

    total = total_pass + total_fail
    overall = "ALL PASS" if total_fail == 0 else f"FAILURES: {total_fail}/{total}"
    print()
    print(f"OVERALL: {overall}  ({total_pass}/{total} cases pass)")
    print("=" * 70)
    print()

    return {
        "overall": "PASS" if total_fail == 0 else "FAIL",
        "total_pass": total_pass,
        "total_fail": total_fail,
        "total_cases": total,
        "group_results": {k: {"pass": len(v) == 0, "failures": len(v)} for k, v in results.items()},
    }


if __name__ == "__main__":
    summary = run_all()
    sys.exit(0 if summary["overall"] == "PASS" else 1)
