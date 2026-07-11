"""
layer2_evidence.py — Layer 2 (raw evidence + provenance) assembly for the
Product Dossier compiler (PD-2 / TASK-610).

Per STF memo `2026-07-11_product-dossier-architecture.md` §4:
  "Layer 2 -- Raw evidence. Truth = TASK-601 manifest + raw captures + replay
  baseline. No new store. Per-field cell {value, raw_source_text, source,
  extraction(parser_version), captured_at, content_hash, flags}, lifted from
  replay rows (already ~90% built; the PD pivots per-field-rows -> per-
  product). OFF-never structurally: manifest membership admits only direct-
  scrape containers; a cell whose source is off-enum is a build failure.
  Missing = {value:null, status:not_retrieved} + Layer-4 fail; the compiler
  has NO imputation code path."

This module does NOT fork 03_operations/bsip0/manifest/replay_harness.py --
it loads that module by file path (the same importlib.util technique
replay_harness.py itself uses to load the parser) and calls its
`dereference()`, `flags()`, `load_parser()`, `RAW_KEYS`, `NUMERIC_KEYS`,
`BOUNDS` directly. Any bugfix to the dereference/flag logic lands once, in
replay_harness.py, and both the replay CI gate and this compiler pick it up.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
REPLAY_HARNESS_PATH = REPO_ROOT / "03_operations" / "bsip0" / "manifest" / "replay_harness.py"
BSIP0_PARSER_PATH = REPO_ROOT / "03_operations" / "bsip0" / "scrape" / "_shared" / "bsip0_nutrition.py"


class DossierBuildError(Exception):
    """Raised for any structural build-integrity violation (banned OFF-source
    cell, cross-namespace metric, banned overall_score, etc). A raised
    DossierBuildError must ALWAYS abort the compile -- never be caught and
    downgraded to a warning anywhere in build_dossiers.py.
    """


# ---------------------------------------------------------------------------
# Reuse replay_harness.py (loaded by path, not forked)
# ---------------------------------------------------------------------------

def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_replay_harness = None


def replay_harness():
    """Lazily load and cache 03_operations/bsip0/manifest/replay_harness.py."""
    global _replay_harness
    if _replay_harness is None:
        _replay_harness = _load_module(REPLAY_HARNESS_PATH, "pd2_replay_harness_ref")
    return _replay_harness


_bsip0_parser = None


def bsip0_parser():
    global _bsip0_parser
    if _bsip0_parser is None:
        _bsip0_parser = replay_harness().load_parser()
    return _bsip0_parser


def parser_version() -> str:
    """Content-hash-derived version stamp. The BSIP0 nutrition parser module
    has no explicit __version__/PARSER_VERSION constant (checked directly --
    there isn't one), so we stamp with a content hash of the parser file
    itself. This is deterministic (no wall-clock) and satisfies R-D's
    requirement that any pre-fix projection is "stamped with its actual
    parser_version" so a post-fix re-run is trivially distinguishable.
    Follow-up (not this task): if the parser module gains an explicit
    version string, prefer that instead.
    """
    digest = hashlib.sha256(BSIP0_PARSER_PATH.read_bytes()).hexdigest()
    return f"sha256:{digest[:16]}"


# ---------------------------------------------------------------------------
# Banned-source structural guard (memo: "a cell whose source is off-enum is
# a build failure"). Reuses the same banned-source marker vocabulary
# run_gates.py's G4 gate enforces (TASK-238 hard rule: Open Food Facts is
# banned project-wide for every field, forever), so both the page gate and
# this compiler recognize the identical banned-source signature. These
# markers exist ONLY to detect and reject a forbidden source -- never to
# use one; see off_ban_hard_rule.
# ---------------------------------------------------------------------------

BANNED_SOURCE_MARKERS = [
    "open_food_facts",     # banned marker (TASK-238) -- OFF is never a real source
    "openfoodfacts.org",   # banned marker (TASK-238) -- OFF is never a real source
    "images.openfoodfacts",  # banned marker (TASK-238) -- OFF is never a real source
    "off_client",          # banned marker (TASK-238) -- the disabled OFF client, never used
]

# Known-good retailer-fleet tags observed in the TASK-601 capture manifest.
# "unknown" is a legacy untagged DIRECT-SCRAPE capture (pre-dates retailer
# tagging in early BSIP0 raw-scrape files) -- it is NOT a banned marker and
# NOT invented data; the manifest's own membership rule (TASK-601) already
# admits only direct-scrape containers, so "unknown" here means "untagged
# retailer", never "off-sourced". It is allowed but is visible in Layer-2
# data_quality coverage stats as a lower-confidence source.
KNOWN_RETAILER_TAGS = {
    "shufersal", "victory", "yochananof", "rami_levy", "tiv_taam",
    "hazi_hinam", "unknown",
}
ALLOWED_SOURCE_ENUM = KNOWN_RETAILER_TAGS | {"manufacturer_page"}


def assert_source_not_banned(source_value: str, context: str = "") -> None:
    """Raise DossierBuildError if `source_value` matches any banned-source
    marker. This is the hard structural guard the selftest exercises
    directly (never use one of these; only ever detect and reject one).
    """
    text = str(source_value or "").lower()
    for marker in BANNED_SOURCE_MARKERS:
        if marker in text:
            raise DossierBuildError(
                f"banned-source evidence cell detected (marker={marker!r}) in {context or source_value!r} "
                f"-- forbidden project-wide (off_ban_hard_rule); build aborted."
            )


# ---------------------------------------------------------------------------
# Manifest indexing
# ---------------------------------------------------------------------------

def load_manifest() -> dict:
    rh = replay_harness()
    return json.loads(rh.MANIFEST.read_text(encoding="utf-8"))


def build_capture_index(manifest: dict) -> Tuple[Dict[Tuple[str, str], dict], Dict[str, List[dict]]]:
    """Returns (by_retailer_gtin, by_gtin_only). Canonical records only."""
    by_pair: Dict[Tuple[str, str], dict] = {}
    by_gtin: Dict[str, List[dict]] = {}
    for rec in manifest.get("records", []):
        if not rec.get("canonical"):
            continue
        key = (rec["retailer"], rec["gtin"])
        by_pair[key] = rec
        by_gtin.setdefault(rec["gtin"], []).append(rec)
    return by_pair, by_gtin


def _is_in_category(rec: dict, category_folder) -> bool:
    """Whether a capture belongs to the product's configured corpus.

    A retailer/GTIN pair alone is not sufficient: GTINs can collide across
    shelves in the manifest.  With a configured category, every successful
    match must therefore pass this path guard.
    """
    if not category_folder:
        return True
    capture_file = str(rec.get("capture_file") or "").replace("\\", "/")
    folders = [category_folder] if isinstance(category_folder, str) else category_folder
    return any(f"/{folder}/" in capture_file for folder in folders)


def _deduplicate_equivalent_captures(candidates: List[dict], retailer: str) -> List[dict]:
    """Collapse only byte-identical canonical captures.

    The TASK-626 cookies cluster has a legacy ``unknown`` manifest row and a
    retailer-tagged row for the same raw capture.  Same GTIN alone is never
    enough to collapse candidates; a content hash is required.  Prefer the
    requested retailer, then a tagged retailer over ``unknown``, so the chosen
    record is deterministic and preserves the best manifest provenance.
    """
    groups: Dict[str, List[dict]] = {}
    unique: List[dict] = []
    for rec in candidates:
        content_hash = rec.get("content_hash")
        if not content_hash:
            unique.append(rec)
            continue
        groups.setdefault(content_hash, []).append(rec)

    def preference(rec: dict) -> tuple:
        return (
            rec.get("retailer") != retailer,
            rec.get("retailer") == "unknown",
            str(rec.get("retailer") or ""),
            str(rec.get("capture_file") or ""),
            str(rec.get("object_path") or ""),
        )

    unique.extend(min(group, key=preference) for group in groups.values())
    return unique


def find_capture(
    retailer: str,
    gtin: str,
    category_folder: Optional[str],
    by_pair: Dict[Tuple[str, str], dict],
    by_gtin: Dict[str, List[dict]],
) -> Tuple[Optional[dict], str]:
    """Resolve the canonical manifest record for a served product.

    Match strategy (never guesses across a genuine ambiguity -- returns
    (None, "ambiguous_capture_match") instead, which surfaces as a
    not_retrieved cell + Layer-4 traceability flag rather than a silent
    wrong-product join):
      1. Exact (retailer, gtin) match, only when its capture belongs to the
         product's category folder.
      2. gtin-only match, filtered to capture_file paths under the
         product's own category folder (derived from the shelf config's
         corpus_dirs/run_products_dir, e.g. "breakfast_cereals"). Applied
         because ~31% (249/807 canonical, worktree count) of gtins in the
         manifest are captured under more than one shelf/category, and the
         `retailer` tag on manifest records is not always populated for
         legacy captures ("unknown"), so retailer alone is not a reliable
         disambiguator.
         Byte-identical duplicate records (same content hash) are one capture,
         not an ambiguity; the tagged record is preferred deterministically.
      3. If step 2 still yields 0 or >1 distinct captures, return ambiguous /
         not-found rather than picking one arbitrarily.
    """
    rec = by_pair.get((retailer, gtin))
    if rec is not None and _is_in_category(rec, category_folder):
        return rec, "matched_retailer_gtin"

    candidates = by_gtin.get(gtin, [])
    if not candidates:
        return None, "no_canonical_capture"

    filtered = [c for c in candidates if _is_in_category(c, category_folder)]
    filtered = _deduplicate_equivalent_captures(filtered, retailer)

    if len(filtered) == 1:
        return filtered[0], "matched_gtin_category_filtered"
    if len(candidates) == 1 and not category_folder:
        return candidates[0], "matched_gtin_only"
    if rec is not None:
        return None, "category_mismatch_capture"
    return None, "ambiguous_capture_match"


# ---------------------------------------------------------------------------
# Per-product Layer-2 cell assembly
# ---------------------------------------------------------------------------

RAW_KEYS = None    # populated lazily from replay_harness to avoid import-order coupling
NUMERIC_KEYS = None


def _keys():
    global RAW_KEYS, NUMERIC_KEYS
    if RAW_KEYS is None:
        rh = replay_harness()
        RAW_KEYS = rh.RAW_KEYS
        NUMERIC_KEYS = rh.NUMERIC_KEYS
    return RAW_KEYS, NUMERIC_KEYS


def null_cell() -> dict:
    """The ONE shape a missing field is allowed to take. No imputation code
    path exists anywhere else in this module -- grep for `null_cell(` to
    audit every call site if this invariant is ever in doubt.
    """
    return {
        "value": None,
        "raw_source_text": None,
        "source": None,
        "extraction": None,
        "captured_at": None,
        "content_hash": None,
        "flags": [],
        "status": "not_retrieved",
    }


def assemble_layer2_for_product(
    retailer: str,
    gtin: str,
    category_folder: Optional[str],
    by_pair: Dict[Tuple[str, str], dict],
    by_gtin: Dict[str, List[dict]],
) -> Tuple[Dict[str, dict], str]:
    """Returns (field_cells, match_note). field_cells keys are the 10
    RAW_KEYS logical field names (energy, fat, saturated_fat, trans_fat,
    cholesterol, sodium, carbs, sugar, fiber, protein).
    """
    rh = replay_harness()
    raw_keys, numeric_keys = _keys()

    rec, match_note = find_capture(retailer, gtin, category_folder, by_pair, by_gtin)
    if rec is None:
        return {field: null_cell() for field in raw_keys}, match_note

    # Structural banned-source guard -- raise BEFORE touching any downstream value.
    assert_source_not_banned(rec.get("retailer"), context=f"manifest record retailer for gtin={gtin}")
    if rec.get("retailer") not in ALLOWED_SOURCE_ENUM:
        raise DossierBuildError(
            f"manifest record source '{rec.get('retailer')}' for gtin={gtin} is outside the "
            f"allowed source enum {sorted(ALLOWED_SOURCE_ENUM)} -- build aborted (off_ban_hard_rule)."
        )

    parser = bsip0_parser()
    source_obj = rh.dereference(rec)
    classified = parser.parse_nutrition_rows(source_obj.get("rows", []))
    raw_panel = {raw_keys[k]: v for k, v in classified.items() if k in raw_keys}
    numeric = parser.parse_nutrition_numeric(raw_panel)

    pv = parser_version()
    cells: Dict[str, dict] = {}
    for field, raw_key in raw_keys.items():
        raw = raw_panel.get(raw_key)
        parsed = numeric.get(numeric_keys[field])
        cell_flags = rh.flags(raw, parsed, field, parsed)
        cells[field] = {
            "value": parsed,
            "raw_source_text": raw,
            "source": rec["retailer"],
            "extraction": {"parser_version": pv},
            "captured_at": rec.get("scrape_timestamp"),
            "content_hash": rec.get("content_hash"),
            "flags": cell_flags,
            "status": "retrieved",
        }
    return cells, match_note


def coverage_stats(field_cells: Dict[str, dict]) -> dict:
    total = len(field_cells)
    retrieved = sum(1 for c in field_cells.values() if c.get("status") == "retrieved" and c.get("value") is not None)
    flagged = sum(1 for c in field_cells.values() if c.get("flags"))
    return {"fields_total": total, "fields_retrieved": retrieved, "fields_flagged": flagged}
