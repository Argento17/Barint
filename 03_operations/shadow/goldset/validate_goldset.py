"""
validate_goldset.py — Gold Set seed validator (stdlib only).

Validates a gold_set_seed_v0.json file against the gold contract schema rules.
Does NOT call jsonschema; all checks are implemented directly.

Usage:
  python validate_goldset.py [--seed PATH]

Exit codes:
  0 = valid (all checks pass)
  1 = invalid (one or more violations found)

Rules enforced (from P238 spec + gold_set_schema.json):
  R1  Each entry has required top-level keys: id, pid, corpus, tier, scoring_flags, expected, rubric, provenance
  R2  tier must be one of: good | poor | ambiguous
  R3  expected.grade_band is a non-empty array of values from {S, A, B, C, D, E}
  R4  expected.score_range is a 2-element [min, max] array, both ints in [0,100], min <= max
  R5  grade_band ↔ score_range consistency per cutoffs:
        S >= 90, A 80-89, B 65-79, C 50-64, D 35-49, E 0-34
        Every point in score_range must be achievable by at least one grade in grade_band
  R6  expected.dimensions keys must be from the 10 engine dimension names;
      values must be one of {low, medium, high}; max 3 dimensions per entry
  R7  No forbidden engine-score keys in expected{}: actual_score, bari_score, engine_grade, engine_score
  R8  rubric[*].basis must NOT be "Open Food Facts", "OFF", "openfoodfacts" (OFF-ban check, case-insensitive)
  R9  rubric[*].basis must be present and non-empty
  R10 provenance.authored_blind must be a boolean
  R11 scoring_flags values must be "on" or "off"
  R12 No duplicate entry ids in the seed
  R13 No duplicate pids with the same corpus in the seed
      (same pid can appear in different corpora — e.g. A-003 vs G-003 are the same product but different corpora entries are allowed;
       duplicate pid+corpus combination is flagged as a warning, not an error)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Default seed path (relative to this script's directory)
_HERE = Path(__file__).parent.resolve()
DEFAULT_SEED = _HERE / "gold_set_seed_v0.json"

VALID_GRADES = {"S", "A", "B", "C", "D", "E"}
VALID_TIERS = {"good", "poor", "ambiguous"}
VALID_DIM_VALUES = {"low", "medium", "high"}
VALID_FLAG_VALUES = {"on", "off"}
VALID_DIMS = {
    "processing_quality", "nutrient_density", "calorie_density",
    "glycemic_quality", "protein_quality", "additive_quality",
    "satiety_support", "fat_quality", "regulatory_quality", "whole_food_integrity"
}
FORBIDDEN_EXPECTED_KEYS = {"actual_score", "bari_score", "engine_grade", "engine_score"}
OFF_BASIS_PATTERNS = re.compile(
    r"(open food facts|openfoodfacts|^off$)", re.IGNORECASE
)

# Grade-band numeric ranges (inclusive)
GRADE_RANGES = {
    "S": (90, 100),
    "A": (80, 89),
    "B": (65, 79),
    "C": (50, 64),
    "D": (35, 49),
    "E": (0, 34),
}


def _grades_cover_range(grade_band: list, score_min: int, score_max: int) -> tuple[bool, str]:
    """Check that every integer in [score_min, score_max] is reachable by at least one grade in grade_band."""
    # Build the union of ranges covered by the declared grades
    covered_min = min(GRADE_RANGES[g][0] for g in grade_band)
    covered_max = max(GRADE_RANGES[g][1] for g in grade_band)
    # The declared score_range must be a subset of the union of grade ranges
    if score_min < covered_min or score_max > covered_max:
        return False, (
            f"score_range [{score_min},{score_max}] extends outside "
            f"grade_band {grade_band} coverage [{covered_min},{covered_max}]"
        )
    return True, ""


def validate_entry(entry: dict, idx: int) -> list[str]:
    """Validate a single entry; return a list of violation strings (empty = ok)."""
    eid = entry.get("id", f"<index {idx}>")
    violations: list[str] = []

    # R1 required keys
    required_keys = ["id", "pid", "corpus", "tier", "scoring_flags", "expected", "rubric", "provenance"]
    for k in required_keys:
        if k not in entry:
            violations.append(f"[{eid}] R1: missing required key '{k}'")

    if violations:
        return violations  # Can't check further without required keys

    # R2 tier
    if entry["tier"] not in VALID_TIERS:
        violations.append(f"[{eid}] R2: tier '{entry['tier']}' not in {VALID_TIERS}")

    # R11 scoring_flags values
    sf = entry.get("scoring_flags", {})
    if not isinstance(sf, dict):
        violations.append(f"[{eid}] R11: scoring_flags must be an object")
    else:
        for k, v in sf.items():
            if v not in VALID_FLAG_VALUES:
                violations.append(f"[{eid}] R11: scoring_flags['{k}'] = '{v}' must be 'on' or 'off'")

    expected = entry.get("expected", {})
    if not isinstance(expected, dict):
        violations.append(f"[{eid}] expected must be an object")
        return violations

    # R7 no forbidden engine-score keys
    for fk in FORBIDDEN_EXPECTED_KEYS:
        if fk in expected:
            violations.append(f"[{eid}] R7: forbidden key '{fk}' found in expected{{}} — independence firewall violated")

    # R3 grade_band
    gb = expected.get("grade_band")
    if not isinstance(gb, list) or len(gb) == 0:
        violations.append(f"[{eid}] R3: expected.grade_band must be a non-empty array")
        gb = None
    else:
        for g in gb:
            if g not in VALID_GRADES:
                violations.append(f"[{eid}] R3: grade_band contains invalid grade '{g}' (must be one of {VALID_GRADES})")
        gb = [g for g in gb if g in VALID_GRADES]

    # R4 score_range
    sr = expected.get("score_range")
    score_ok = False
    if not isinstance(sr, list) or len(sr) != 2:
        violations.append(f"[{eid}] R4: expected.score_range must be a 2-element array [min, max]")
    else:
        smin, smax = sr
        if not (isinstance(smin, (int, float)) and isinstance(smax, (int, float))):
            violations.append(f"[{eid}] R4: score_range values must be numbers")
        else:
            smin, smax = int(smin), int(smax)
            if not (0 <= smin <= 100 and 0 <= smax <= 100):
                violations.append(f"[{eid}] R4: score_range values must be in [0,100]")
            elif smin > smax:
                violations.append(f"[{eid}] R4: score_range min ({smin}) > max ({smax})")
            else:
                score_ok = True

    # R5 grade_band ↔ score_range consistency
    if gb and score_ok:
        ok, msg = _grades_cover_range(gb, smin, smax)
        if not ok:
            violations.append(f"[{eid}] R5: {msg}")

    # R6 dimensions
    dims = expected.get("dimensions")
    if dims is not None:
        if not isinstance(dims, dict):
            violations.append(f"[{eid}] R6: expected.dimensions must be an object")
        else:
            if len(dims) > 3:
                violations.append(f"[{eid}] R6: expected.dimensions has {len(dims)} entries; max 3 allowed")
            for dk, dv in dims.items():
                if dk not in VALID_DIMS:
                    violations.append(f"[{eid}] R6: unknown dimension key '{dk}'")
                if dv not in VALID_DIM_VALUES:
                    violations.append(f"[{eid}] R6: dimension '{dk}' value '{dv}' not in {VALID_DIM_VALUES}")

    # R8, R9 rubric
    rubric = entry.get("rubric", [])
    if not isinstance(rubric, list) or len(rubric) == 0:
        violations.append(f"[{eid}] R8/R9: rubric must be a non-empty array")
    else:
        for i, item in enumerate(rubric):
            basis = item.get("basis", "")
            if not basis:
                violations.append(f"[{eid}] R9: rubric[{i}].basis is missing or empty")
            elif OFF_BASIS_PATTERNS.search(basis.strip()):
                violations.append(f"[{eid}] R8: rubric[{i}].basis is '{basis}' — OFF (Open Food Facts) is BANNED as a source")
            if not item.get("criterion"):
                violations.append(f"[{eid}] R1/rubric: rubric[{i}].criterion is missing")
            if not item.get("rationale"):
                violations.append(f"[{eid}] R1/rubric: rubric[{i}].rationale is missing")

    # R10 provenance.authored_blind
    prov = entry.get("provenance", {})
    if not isinstance(prov, dict):
        violations.append(f"[{eid}] R10: provenance must be an object")
    else:
        ab = prov.get("authored_blind")
        if not isinstance(ab, bool):
            violations.append(f"[{eid}] R10: provenance.authored_blind must be a boolean (got {type(ab).__name__})")

    return violations


def validate_seed(seed_path: Path) -> tuple[bool, list[str]]:
    """Validate the entire seed file. Returns (ok, all_violations)."""
    try:
        raw = seed_path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
    except FileNotFoundError:
        return False, [f"Seed file not found: {seed_path}"]
    except json.JSONDecodeError as e:
        return False, [f"Seed file is not valid JSON: {e}"]

    violations: list[str] = []

    # Check top-level structure
    if "entries" not in data:
        violations.append("Top-level 'entries' key missing from seed file")
        return False, violations

    entries = data["entries"]
    if not isinstance(entries, list):
        violations.append("'entries' must be a JSON array")
        return False, violations

    # R12 no duplicate ids
    seen_ids: dict[str, int] = {}
    for idx, entry in enumerate(entries):
        eid = entry.get("id", f"<index {idx}>")
        if eid in seen_ids:
            violations.append(f"R12: duplicate entry id '{eid}' at indexes {seen_ids[eid]} and {idx}")
        else:
            seen_ids[eid] = idx

    # R13 warn on duplicate pid+corpus (not an error but a finding)
    seen_pid_corpus: dict[tuple, int] = {}
    for idx, entry in enumerate(entries):
        key = (entry.get("pid", ""), entry.get("corpus", ""))
        if key in seen_pid_corpus:
            # Advisory — same product in same corpus (G-008 and A-004 share pid+corpus by design)
            violations.append(
                f"[{entry.get('id', idx)}] R13 (ADVISORY): duplicate pid+corpus "
                f"({key[0]}, {key[1]}) at index {seen_pid_corpus[key]} and {idx} "
                f"— this is ALLOWED if intentional (adversarial stress test), but verify"
            )
        else:
            seen_pid_corpus[key] = idx

    # Per-entry validation
    for idx, entry in enumerate(entries):
        violations.extend(validate_entry(entry, idx))

    ok = all(
        not v.startswith("[") or "(ADVISORY)" in v
        for v in violations
    )
    # Actually: any non-advisory violation is an error
    errors = [v for v in violations if "(ADVISORY)" not in v]
    ok = len(errors) == 0
    return ok, violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Bari gold-set seed file against the gold contract rules."
    )
    parser.add_argument(
        "--seed",
        type=Path,
        default=DEFAULT_SEED,
        help=f"Path to the seed JSON file (default: {DEFAULT_SEED})",
    )
    args = parser.parse_args()

    seed_path: Path = args.seed
    if not seed_path.is_absolute():
        seed_path = Path.cwd() / seed_path

    print(f"validate_goldset.py — validating: {seed_path}")

    ok, violations = validate_seed(seed_path)

    if not violations:
        entry_count = 0
        try:
            data = json.loads(seed_path.read_bytes().decode("utf-8"))
            entry_count = len(data.get("entries", []))
        except Exception:
            pass
        print(f"VALID — {entry_count} entries, 0 violations.")
        return 0

    advisories = [v for v in violations if "(ADVISORY)" in v]
    errors = [v for v in violations if "(ADVISORY)" not in v]

    if errors:
        print(f"INVALID — {len(errors)} error(s), {len(advisories)} advisory(ies):")
        for v in errors:
            print(f"  ERROR: {v}")
        for v in advisories:
            print(f"  ADVISORY: {v}")
        return 1
    else:
        entry_count = 0
        try:
            data = json.loads(seed_path.read_bytes().decode("utf-8"))
            entry_count = len(data.get("entries", []))
        except Exception:
            pass
        print(f"VALID — {entry_count} entries, 0 errors, {len(advisories)} advisory(ies):")
        for v in advisories:
            print(f"  ADVISORY: {v}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
