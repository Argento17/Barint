"""
TASK-264 / P45 — Factory trust layer: property-based invariant suite on score_engine.py.

Homed in Shadow per Shadow conventions.  Run with:
    cd C:\\Bari\\03_operations\\bsip2\\proto_v0\\src
    python ..\\..\\..\\shadow\\engine_invariants.py

The suite exercises 6 invariants derived strictly from the engine's own documented
contracts.  A false invariant (one the engine does not guarantee) is never asserted —
rather it is documented in the MONOTONICITY section below.

Invariants:
  I1  BOUNDS         — final_score in [0, 100] (or None for withheld); grade in valid set;
                       every dimension_score in [0, 100].
  I2  DETERMINISM    — same BSIP1 input scored twice → byte-identical score + dimension_scores.
  I3  NULL_SAFETY    — records missing any nutrition field do not crash; engine handles
                       each null per its documented rule.
  I4  OFF_FREE       — no "open_food_facts" / "off_" marker appears in any engine-produced
                       trace key or string value.
  I5  GRADE_CONSISTENCY — score→grade mapping: same score always yields same grade;
                          grade thresholds are monotonically ordered.
  I6  MONOTONICITY   — only asserted where provably guaranteed (see MONOTONICITY NOTE below).

MONOTONICITY NOTE (which relationships are / are not monotone):
  ASSERTED (provably guaranteed):
    - score_whole_food_integrity: fermentation_bonus is always non-negative; adding it
      can only increase (or hold) the wfi_score relative to the no-bonus case.
    - score_nutrient_density (single-signal protein-only path): within the protein-only
      path (fiber_not_applicable), increasing protein_g never decreases the score
      because lookup_protein_scale is a non-decreasing piecewise linear function.
    - score_satiety_support: (protein*3 + fiber*5) / max(50, kcal) * 400 is strictly
      non-decreasing in protein_g when kcal and fiber are fixed (numerator grows,
      denominator unchanged).

  NOT ASSERTED (engine does NOT guarantee):
    - score_calorie_density: uses CALORIE_DENSITY_TABLES (piecewise constant step table)
      — INCREASING kcal can DECREASE the score (higher kcal = worse calorie density).
      This is the correct behavior; asserting "more kcal = better score" would be wrong.
    - score_glycemic_quality / _score_glycemic_quality_sprint1: sugar_penalty grows with
      sugar_g (formula: 90 - sugar*2.5 + ...) — INCREASING sugar_g decreases the score.
      No monotone-positive relationship to assert in the direction of "more = better."
    - evaluate_guardrails / caps: the final_score is non-monotone in sugar_g, sodium_mg,
      and sat_fat because cap rules fire discontinuously at specific thresholds.  Any
      assertion about monotonicity of the composite score would be false.
    - Overall score_product: the composite weighted + capped + penalized score is NOT
      guaranteed monotone in any single nutrient because caps and penalties create
      deliberate non-linearities.  This is by design — we do not assert it.

Guards:
  - Read-only over the engine and real BSIP1 data — no engine file is touched.
  - stdlib only; no new dependencies.
  - No OFF data is introduced; the suite uses hand-rolled synthetic records.
"""
import copy
import hashlib
import json
import os
import pathlib
import random
import sys

# ---------------------------------------------------------------------------
# Path setup — must run regardless of cwd.
# ---------------------------------------------------------------------------
_SUITE_PATH = pathlib.Path(__file__).resolve()
_SHADOW_ROOT = _SUITE_PATH.parent          # .../03_operations/shadow
# parents[0] = .../03_operations,  parents[1] = <repo root>
_REPO_ROOT = _SHADOW_ROOT.parents[1]
_SRC = _REPO_ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"

# Ensure the engine src dir is on sys.path before any engine imports.
# Insert at position 0 so it wins over any stale partial imports.
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

# Also change cwd to the src dir so relative imports (if any engine module does them)
# resolve correctly — matches how shadow_backtest.py is invoked.
os.chdir(str(_SRC))

_BSIP1_BREAD_DIR = _REPO_ROOT / "02_products" / "bread_retail_001" / "bsip1"

# ---------------------------------------------------------------------------
# Engine flag setup — pin the default config that Shadow uses for most corpora
# (all OFF except BARI_GLASSBOX_W4 which ships as ON per its flag declaration).
# We reset env before importing engine modules so module-level flag reads are clean.
# ---------------------------------------------------------------------------
_DEFAULT_FLAGS = {
    "BARI_TASK144_FIXES":   "off",
    "BARI_RECAL_P0":        "off",
    "BARI_RECAL_P0_YOGURT_TRIM": "off",
    "BARI_GLASSBOX_D5D6":   "off",
    "BARI_GLASSBOX_W15":    "off",
    "BARI_GLASSBOX_W2":     "off",
    "BARI_GLASSBOX_W4":     "on",    # SHIPPED 2026-06-05 (TASK-181S), default ON in the flag
    "BARI_SODIUM_CEREAL":   "off",
    "BARI_REDLABEL_V1":     "off",
    "BARI_TASK250_CONF":    "off",
}
for _k, _v in _DEFAULT_FLAGS.items():
    os.environ[_k] = _v

# Purge any previously imported engine modules so the flag values above are respected.
for _mod in list(sys.modules.keys()):
    try:
        _f = getattr(sys.modules[_mod], "__file__", None)
        if _f and pathlib.Path(_f).resolve().parent == _SRC:
            del sys.modules[_mod]
    except Exception:
        pass

from input_loader import load_batch          # noqa: E402
from signal_extractor import extract_signals # noqa: E402
from router_v2 import classify_category      # noqa: E402
from nova_proxy import infer_nova            # noqa: E402
from evaluation_scope import assign_evaluation_scope  # noqa: E402
from score_engine import score_product       # noqa: E402
from constants import GRADE_THRESHOLDS, score_to_grade  # noqa: E402

# ---------------------------------------------------------------------------
# Valid grade set (from constants.py)
# ---------------------------------------------------------------------------
VALID_GRADES = {g for _, g in GRADE_THRESHOLDS} | {
    "insufficient_data",   # data_sufficiency gate
    "לא נוקד",  # GLASSBOX_WITHHELD_LABEL ("לא נוקד")
}


# ---------------------------------------------------------------------------
# Minimal synthetic BSIP1 record factory
# ---------------------------------------------------------------------------

def _minimal_product(
    pid="test-001",
    kcal=250.0, fat_g=5.0, fat_sat=2.0, fat_trans=None,
    sodium=300.0, carbs=40.0, sugar=5.0, fiber=3.0, protein=8.0,
    nova_level=2, ingredient_list=None, has_whole_grain=False,
):
    """Return a minimal BSIP1-shaped dict that all pipeline stages can process."""
    if ingredient_list is None:
        ingredient_list = ["קמח חיטה", "מים", "שמרים", "מלח"]
    return {
        "schema_version": "bsip1_v0_1",
        "canonical_product_id": pid,
        "canonical_name_he": f"מוצר בדיקה {pid}",
        "normalized_nutrition_per_100g": {
            "energy_kcal":      kcal,
            "fat_g":            fat_g,
            "fat_saturated_g":  fat_sat,
            "fat_trans_g":      fat_trans,
            "sodium_mg":        sodium,
            "carbohydrates_g":  carbs,
            "sugars_g":         sugar,
            "dietary_fiber_g":  fiber,
            "protein_g":        protein,
            "cholesterol_mg":   None,
        },
        "ingredients_list": ingredient_list,
        "ingredients_text_he": ", ".join(ingredient_list),
        "canonical_trust_level": "high",
        "nova_proxy_override": nova_level,   # let the nova_proxy respect this if it does,
                                              # otherwise router will derive it naturally
    }


def _score_product_full(product: dict) -> dict:
    """Run the full pipeline on a single product dict. Returns the score_product result."""
    sig = extract_signals(product)
    cat = classify_category(product)
    nova = infer_nova(product, sig["L3_inferred_classifications"])
    ev = assign_evaluation_scope(product, cat["category"])
    return score_product(product, sig, cat, nova, ev)


def _score_product_safe(product: dict):
    """Run full pipeline; return (result_dict, None) or (None, exception_string)."""
    try:
        return _score_product_full(product), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


# ---------------------------------------------------------------------------
# Random synthetic record generator
# ---------------------------------------------------------------------------

_RNG = random.Random(42)  # fixed seed for reproducibility


def _rand_product(idx: int) -> dict:
    """Generate a random but valid BSIP1 product within sane nutrition ranges."""
    kcal    = round(_RNG.uniform(50, 550), 1)
    fat_g   = round(_RNG.uniform(0, 40), 1)
    fat_sat = round(_RNG.uniform(0, min(fat_g, 25)), 1) if fat_g > 0 else 0.0
    fat_trans = round(_RNG.uniform(0, 0.4), 2) if _RNG.random() < 0.2 else None
    sodium  = round(_RNG.uniform(0, 900), 1)
    carbs   = round(_RNG.uniform(0, 80), 1)
    sugar   = round(_RNG.uniform(0, min(carbs, 60)), 1)
    fiber   = round(_RNG.uniform(0, 15), 1)
    protein = round(_RNG.uniform(0, 30), 1)
    nova    = _RNG.choice([1, 2, 3, 4])
    ing_count = _RNG.randint(1, 8)
    ing_list = [f"רכיב{i}" for i in range(1, ing_count + 1)]
    return _minimal_product(
        pid=f"rand-{idx:04d}",
        kcal=kcal, fat_g=fat_g, fat_sat=fat_sat, fat_trans=fat_trans,
        sodium=sodium, carbs=carbs, sugar=sugar, fiber=fiber, protein=protein,
        nova_level=nova, ingredient_list=ing_list,
    )


# ---------------------------------------------------------------------------
# Real BSIP1 loader
# ---------------------------------------------------------------------------

def _load_real_records() -> list:
    """Load real BSIP1 records from bread_retail_001/bsip1/.  Read-only."""
    if not _BSIP1_BREAD_DIR.exists():
        return []
    products = []
    for p in sorted(_BSIP1_BREAD_DIR.glob("bsip1_*.json")):
        try:
            products.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return products


# ---------------------------------------------------------------------------
# Result helpers
# ---------------------------------------------------------------------------

def _json_canonical(obj) -> str:
    """Canonical JSON string for byte-comparison (determinism test)."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)


def _dim_scores(result: dict) -> dict:
    return result.get("dimension_scores") or {}


def _final_score(result: dict):
    return result.get("final_score_estimate")


def _grade(result: dict) -> str:
    return result.get("grade_estimate", "")


def _trace_strings(result: dict) -> list:
    """Collect ALL string values that appear anywhere in the result dict tree."""
    strings = []
    stack = [result]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            for k, v in node.items():
                strings.append(str(k))
                stack.append(v)
        elif isinstance(node, list):
            stack.extend(node)
        elif isinstance(node, str):
            strings.append(node)
    return strings


# ---------------------------------------------------------------------------
# OFF-marker detection
# ---------------------------------------------------------------------------

_OFF_MARKERS = [
    "open_food_facts",
    "openfoodfacts",
    "off_source",
    "off_data",
    "from_off",
    "off_categories",   # key name in input records — must NOT appear in engine trace
    "open-food-facts",
]


def _contains_off_marker(result: dict) -> list:
    """Return list of (location, marker) for any OFF marker found in the trace."""
    hits = []
    trace_strs = _trace_strings(result)
    for s in trace_strs:
        sl = s.lower()
        for m in _OFF_MARKERS:
            if m in sl:
                hits.append((s[:80], m))
    return hits


# ---------------------------------------------------------------------------
# I5 — Grade consistency: pre-compute the expected grade boundaries from constants
# ---------------------------------------------------------------------------

def _check_grade_boundary_monotonicity() -> list:
    """Verify that GRADE_THRESHOLDS are sorted descending (highest threshold first)
    and that score_to_grade is consistent with them."""
    errors = []
    thresholds = [t for t, _ in GRADE_THRESHOLDS]
    if thresholds != sorted(thresholds, reverse=True):
        errors.append(
            f"GRADE_THRESHOLDS not sorted descending: {GRADE_THRESHOLDS}")
    # Verify score_to_grade on a sweep of integer scores 0..100
    prev_grade = None
    prev_score = 101
    for t, expected_grade in GRADE_THRESHOLDS:
        g = score_to_grade(float(t))
        if g != expected_grade:
            errors.append(
                f"score_to_grade({t}) = {g!r}, expected {expected_grade!r}")
        prev_score = t
    # Spot-check: score just below a threshold should yield the next lower grade
    for i in range(len(GRADE_THRESHOLDS) - 1):
        t_hi, g_hi = GRADE_THRESHOLDS[i]
        t_lo, g_lo = GRADE_THRESHOLDS[i + 1]
        if t_hi > 0:
            score_below = t_hi - 0.1
            g = score_to_grade(score_below)
            if g != g_lo:
                errors.append(
                    f"score_to_grade({score_below}) = {g!r}, "
                    f"expected {g_lo!r} (just below threshold {t_hi})")
    return errors


# ---------------------------------------------------------------------------
# I6 — Monotonicity assertions (only provably guaranteed ones)
# ---------------------------------------------------------------------------

def _test_monotonicity_satiety(n: int = 200) -> list:
    """I6-M1: score_satiety_support is non-decreasing in protein_g (fiber, kcal fixed)."""
    from score_engine import score_satiety_support
    failures = []
    rng = random.Random(99)
    for i in range(n):
        fiber = round(rng.uniform(0, 10), 1)
        kcal = round(rng.uniform(50, 500), 1)
        nn_low = {"protein_g": 0.0, "dietary_fiber_g": fiber, "energy_kcal": kcal}
        nn_hi  = {"protein_g": round(rng.uniform(1, 30), 1), "dietary_fiber_g": fiber, "energy_kcal": kcal}
        s_low, _ = score_satiety_support(nn_low)
        s_hi,  _ = score_satiety_support(nn_hi)
        if s_hi < s_low - 1e-9:
            failures.append(
                f"case {i}: protein 0→{nn_hi['protein_g']}g, "
                f"satiety_support {s_low}→{s_hi} DECREASED (fiber={fiber}, kcal={kcal})")
    return failures


def _test_monotonicity_wfi_fermentation() -> list:
    """I6-M2: score_whole_food_integrity: fermentation_bonus (FERMENTATION_DIRECT_BONUS)
    is non-negative, so the score with has_fermentation=True >= score with False."""
    from score_engine import score_whole_food_integrity
    from constants import FERMENTATION_DIRECT_BONUS
    failures = []
    for nova in [1, 2, 3, 4]:
        for ing_count in [1, 5, 10, 15, 20]:
            s_no_ferm, _ = score_whole_food_integrity(nova, ing_count, False)
            s_ferm,    _ = score_whole_food_integrity(nova, ing_count, True)
            if s_ferm < s_no_ferm - 1e-9:
                failures.append(
                    f"wfi: nova={nova} ing={ing_count}: ferm={s_ferm} < no_ferm={s_no_ferm}")
    if FERMENTATION_DIRECT_BONUS < 0:
        failures.append(
            f"FERMENTATION_DIRECT_BONUS={FERMENTATION_DIRECT_BONUS} is negative "
            f"(would be a penalty, not a bonus — engine contract violation)")
    return failures


def _test_monotonicity_satiety_protein_only(n: int = 100) -> list:
    """I6-M3: score_nutrient_density (protein-only path) is non-decreasing in protein_g.
    The protein-only path fires when fiber_not_applicable=True AND category is on the
    FIBER_NOT_APPLICABLE_CATEGORIES allowlist AND fiber is 0/None.  We test the underlying
    lookup_protein_scale directly (the non-decreasing guarantee is on the scale function)."""
    from constants import lookup_protein_scale
    failures = []
    rng = random.Random(123)
    # Test that lookup_protein_scale is non-decreasing over [0, 30]g
    prev_score = 0.0
    for g in [x * 0.5 for x in range(0, 61)]:   # 0 to 30 in 0.5g steps
        s = lookup_protein_scale(g, None, False)   # flag OFF path
        if s < prev_score - 1e-9:
            failures.append(
                f"lookup_protein_scale({g}g, None, False)={s} < previous={prev_score} — NOT monotone")
        prev_score = s
    # Also test recal_on=True path
    prev_score = 0.0
    for g in [x * 0.5 for x in range(0, 61)]:
        s = lookup_protein_scale(g, "bread", True)
        if s < prev_score - 1e-9:
            failures.append(
                f"lookup_protein_scale({g}g, 'bread', True)={s} < previous={prev_score} — NOT monotone")
        prev_score = s
    return failures


# ---------------------------------------------------------------------------
# Main invariant runner
# ---------------------------------------------------------------------------

def run_invariants(n_random: int = 300) -> dict:
    """Run all 6 invariants.  Returns a structured results dict."""

    results = {
        "I1_BOUNDS":             {"pass": True, "failures": [], "cases_checked": 0},
        "I2_DETERMINISM":        {"pass": True, "failures": [], "cases_checked": 0},
        "I3_NULL_SAFETY":        {"pass": True, "failures": [], "cases_checked": 0},
        "I4_OFF_FREE":           {"pass": True, "failures": [], "cases_checked": 0},
        "I5_GRADE_CONSISTENCY":  {"pass": True, "failures": [], "cases_checked": 0},
        "I6_MONOTONICITY":       {"pass": True, "failures": [], "cases_checked": 0},
    }

    # Load real records once
    real_records = _load_real_records()

    # ------------------------------------------------------------------
    # I5 — Grade consistency (constant-time, run first, no engine calls)
    # ------------------------------------------------------------------
    i5_errors = _check_grade_boundary_monotonicity()
    results["I5_GRADE_CONSISTENCY"]["cases_checked"] = len(GRADE_THRESHOLDS) * 2 + 101
    # Also spot-check score_to_grade on every integer 0..100 stays in valid grade set
    for s in range(0, 101):
        g = score_to_grade(float(s))
        if g not in {gr for _, gr in GRADE_THRESHOLDS}:
            i5_errors.append(
                f"score_to_grade({s}) returned {g!r} which is not in GRADE_THRESHOLDS")
    if i5_errors:
        results["I5_GRADE_CONSISTENCY"]["pass"] = False
        results["I5_GRADE_CONSISTENCY"]["failures"] = i5_errors

    # ------------------------------------------------------------------
    # I6 — Monotonicity (pure dimension-function tests, no full pipeline)
    # ------------------------------------------------------------------
    i6_fail = []
    i6_fail += _test_monotonicity_satiety(200)
    i6_fail += _test_monotonicity_wfi_fermentation()
    i6_fail += _test_monotonicity_satiety_protein_only(100)
    results["I6_MONOTONICITY"]["cases_checked"] = 200 + (4 * 5) + 61 * 2
    if i6_fail:
        results["I6_MONOTONICITY"]["pass"] = False
        results["I6_MONOTONICITY"]["failures"] = i6_fail

    # ------------------------------------------------------------------
    # I3 — Null-safety (targeted null-field cases)
    # ------------------------------------------------------------------
    NUTRITION_FIELDS = [
        "energy_kcal", "fat_g", "fat_saturated_g", "fat_trans_g",
        "sodium_mg", "carbohydrates_g", "sugars_g", "dietary_fiber_g",
        "protein_g",
    ]
    null_cases = 0
    for field in NUTRITION_FIELDS:
        prod = _minimal_product(pid=f"null-{field}")
        prod["normalized_nutrition_per_100g"][field] = None
        result, err = _score_product_safe(prod)
        null_cases += 1
        if err:
            results["I3_NULL_SAFETY"]["pass"] = False
            results["I3_NULL_SAFETY"]["failures"].append(
                f"CRASH with {field}=None: {err}")

    # Also test ALL fields null at once
    prod_all_null = _minimal_product(pid="null-all")
    for f in NUTRITION_FIELDS:
        prod_all_null["normalized_nutrition_per_100g"][f] = None
    result, err = _score_product_safe(prod_all_null)
    null_cases += 1
    if err:
        results["I3_NULL_SAFETY"]["pass"] = False
        results["I3_NULL_SAFETY"]["failures"].append(
            f"CRASH with ALL nutrition fields=None: {err}")

    # No ingredients_list
    prod_no_ing = _minimal_product(pid="null-ing")
    prod_no_ing["ingredients_list"] = None
    prod_no_ing["ingredients_text_he"] = None
    result, err = _score_product_safe(prod_no_ing)
    null_cases += 1
    if err:
        results["I3_NULL_SAFETY"]["pass"] = False
        results["I3_NULL_SAFETY"]["failures"].append(
            f"CRASH with ingredients_list=None: {err}")

    results["I3_NULL_SAFETY"]["cases_checked"] = null_cases

    # ------------------------------------------------------------------
    # Main loop: random + real records feed I1, I2, I4
    # ------------------------------------------------------------------
    all_products = (
        [_rand_product(i) for i in range(n_random)]
        + real_records
    )
    n_real = len(real_records)
    total_cases = len(all_products)

    for i, prod in enumerate(all_products):
        label = f"rand-{i}" if i < n_random else f"real:{prod.get('canonical_product_id','?')}"

        result1, err1 = _score_product_safe(prod)
        if err1:
            # A crash on a real record is a hard finding; on synthetic it is also a finding
            # but we capture it as a failure rather than a crash of the suite itself.
            msg = f"[{label}] CRASH on first call: {err1}"
            results["I1_BOUNDS"]["failures"].append(msg)
            results["I1_BOUNDS"]["pass"] = False
            results["I1_BOUNDS"]["cases_checked"] += 1
            results["I2_DETERMINISM"]["cases_checked"] += 1
            results["I4_OFF_FREE"]["cases_checked"] += 1
            continue

        # I1 — Bounds
        results["I1_BOUNDS"]["cases_checked"] += 1
        score = _final_score(result1)
        grade = _grade(result1)
        dim_sc = _dim_scores(result1)

        if score is not None:
            if not (0 <= score <= 100):
                results["I1_BOUNDS"]["pass"] = False
                results["I1_BOUNDS"]["failures"].append(
                    f"[{label}] final_score={score} OUT OF [0,100]")
        if grade not in VALID_GRADES:
            results["I1_BOUNDS"]["pass"] = False
            results["I1_BOUNDS"]["failures"].append(
                f"[{label}] grade={grade!r} NOT IN VALID_GRADES={VALID_GRADES}")
        for dim, ds in dim_sc.items():
            if not (0 <= ds <= 100):
                results["I1_BOUNDS"]["pass"] = False
                results["I1_BOUNDS"]["failures"].append(
                    f"[{label}] dimension_score[{dim}]={ds} OUT OF [0,100]")

        # I2 — Determinism (score the same product a second time)
        results["I2_DETERMINISM"]["cases_checked"] += 1
        prod2 = copy.deepcopy(prod)   # deep copy so no shared state
        result2, err2 = _score_product_safe(prod2)
        if err2:
            results["I2_DETERMINISM"]["pass"] = False
            results["I2_DETERMINISM"]["failures"].append(
                f"[{label}] second call crashed: {err2}")
        else:
            s1 = _final_score(result1)
            s2 = _final_score(result2)
            d1 = _dim_scores(result1)
            d2 = _dim_scores(result2)
            if s1 != s2:
                results["I2_DETERMINISM"]["pass"] = False
                results["I2_DETERMINISM"]["failures"].append(
                    f"[{label}] final_score: first={s1}, second={s2} — NOT deterministic")
            if d1 != d2:
                results["I2_DETERMINISM"]["pass"] = False
                results["I2_DETERMINISM"]["failures"].append(
                    f"[{label}] dimension_scores differ: {d1} vs {d2}")

        # I4 — OFF-free
        results["I4_OFF_FREE"]["cases_checked"] += 1
        off_hits = _contains_off_marker(result1)
        if off_hits:
            results["I4_OFF_FREE"]["pass"] = False
            for loc, marker in off_hits[:3]:   # cap at 3 per product to keep output manageable
                results["I4_OFF_FREE"]["failures"].append(
                    f"[{label}] OFF marker '{marker}' found in trace: ...{loc[:60]}...")

    return results, total_cases, n_real


# ---------------------------------------------------------------------------
# Pretty-print results
# ---------------------------------------------------------------------------

def _print_results(results: dict, total_cases: int, n_real: int):
    n_random = total_cases - n_real
    print()
    print("=" * 70)
    print("BARI Engine Invariant Suite — TASK-264 / P45")
    print("=" * 70)
    print(f"Synthetic cases: {n_random}   Real records: {n_real}   Total: {total_cases}")
    print()

    all_pass = True
    for inv, data in results.items():
        status = "PASS" if data["pass"] else "FAIL"
        if not data["pass"]:
            all_pass = False
        cases = data["cases_checked"]
        print(f"  {inv:30s}  [{status}]  ({cases} cases checked)")
        if not data["pass"]:
            for f in data["failures"][:5]:   # show first 5 failures max
                print(f"    FINDING: {f}")
            if len(data["failures"]) > 5:
                print(f"    ... and {len(data['failures']) - 5} more")

    print()
    print(f"OVERALL: {'ALL PASS' if all_pass else 'FAILURES DETECTED — see above'}")
    print()

    # Monotonicity documentation
    print("MONOTONICITY SCOPE (I6):")
    print("  ASSERTED:")
    print("    I6-M1  score_satiety_support non-decreasing in protein_g (fiber,kcal fixed)")
    print("    I6-M2  score_whole_food_integrity: fermentation_bonus >= 0 (ferm score >= no-ferm score)")
    print("    I6-M3  lookup_protein_scale non-decreasing in protein_g (both flag paths)")
    print("  NOT ASSERTED (engine does not guarantee these):")
    print("    -  score_calorie_density: DECREASES as kcal increases (by design)")
    print("    -  _score_glycemic_quality_sprint1: DECREASES as sugar_g increases (by design)")
    print("    -  evaluate_guardrails / caps: discontinuous — non-monotone in sugar/sodium/satfat")
    print("    -  score_product composite: NOT monotone in any single nutrient (caps + penalties)")
    print()

    # Factory gate wiring note
    print("FACTORY GATE WIRING:")
    print(
        "  This suite is the scoring-stage gate in the factory chain.  After the engine "
        "emits a score, the factory pipeline calls `python engine_invariants.py` (or "
        "imports run_invariants() directly).  If any invariant returns FAIL, the pipeline "
        "raises an error and halts before writing the score to the frontend JSON.  The "
        "Shadow backtest (shadow_backtest.py) verifies corpus-level regressions; this suite "
        "verifies per-record contracts that the backtest cannot: bounds, determinism, "
        "null-safety, and OFF-cleanliness on every individual score.  Together they form "
        "a two-layer gate — Shadow catches regressions, invariants catch corrupt individual "
        "scores — so the machine cannot silently ship a wrong or out-of-bounds score."
    )
    print()


# ---------------------------------------------------------------------------
# Machine-readable summary (JSON)
# ---------------------------------------------------------------------------

def _machine_summary(results: dict, total_cases: int, n_real: int) -> dict:
    n_random = total_cases - n_real
    inv_pass = sum(1 for d in results.values() if d["pass"])
    inv_fail = sum(1 for d in results.values() if not d["pass"])
    return {
        "suite": "engine_invariants",
        "task": "TASK-264",
        "overall": "PASS" if inv_fail == 0 else "FAIL",
        "invariants_implemented": len(results),
        "invariants_passing": inv_pass,
        "invariants_failing": inv_fail,
        "random_cases_run": n_random,
        "real_records_run": n_real,
        "off_introduced": 0,
        "engine_modified": False,
        "per_invariant": {
            inv: {"pass": data["pass"], "cases": data["cases_checked"],
                  "failures": len(data["failures"])}
            for inv, data in results.items()
        },
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    N_RANDOM = 300
    print(f"Running engine invariant suite (n_random={N_RANDOM}, loading real BSIP1 records)...")
    results, total_cases, n_real = run_invariants(N_RANDOM)
    _print_results(results, total_cases, n_real)
    summary = _machine_summary(results, total_cases, n_real)
    print("MACHINE-READABLE SUMMARY:")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if summary["overall"] == "PASS" else 1)
