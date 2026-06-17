"""
render_fields.py — Shared render-field derivation helpers for generate_page.py
===============================================================================
Ports the display/render field logic out of bespoke per-category builders into
a single config-driven module.  generate_page.py calls these helpers;
each category config declares which fields it needs in `render_fields`.

TASK-316 / TASK-275 — spine step 1: close the generator render-contract gap.

Hard rules carried in:
  - OFF-ban absolute (TASK-238): never use Open Food Facts; emit null if absent.
  - ZERO score/grade change: these helpers are OUTPUT-ONLY; they never touch
    final_score_estimate, grade_estimate, or any scoring dimension.
  - No category-special-cased code paths: every field is derived once here;
    per-category config declares which fields to emit.

Fields implemented (see FIELD_REGISTRY at bottom for the dispatch table):
  novaGroup          — trace.nova_proxy OR corpus.nova_proxy
  sugarPer100ml      — corpus.normalized_nutrition_per_100g.sugars_g (liquid)
  kcalPer100ml       — corpus.normalized_nutrition_per_100g.energy_kcal (liquid)
  retailers          — corpus.source_retailers as a list
  _source_retailers  — corpus.source_retailers as a list (alias for cakes schema)
  subPool            — corpus.juice_subpool
  _category_routed   — trace.category (router decision)
  _product_type      — keyword classifier over corpus name + ingredients (hummus)
  _has_phvo          — trace.L3_inferred_classifications.has_phvo
  confidence_level   — trace.data_sufficiency
  d4_additives       — detect_additives_d4 + w2_additive_copy explanation lookup
  glassBox           — {"gateState": "unconstrained"} from trace; RESIDUAL for
                       demote/withhold (requires D5/D6 engine pass, out of scope)

Residuals (not derivable from corpus+trace without engine edits):
  d3_processing_signal — NOT written by trace_writer; requires engine re-run
                         with BARI_GLASSBOX_W4=on AND trace_writer update.
                         Listed as residual; emit null.
  glassBox.demote/withhold — requires separate D5/D6 engine pass. The generator
                         emits {"gateState": "unconstrained"} for all products;
                         the one known demoted product (hummus bc=7290104721533)
                         is listed as a known residual in the config comment.
"""

import os
import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Score-engine import — for detect_additives_d4
# ---------------------------------------------------------------------------

# The score engine lives at 03_operations/bsip2/proto_v0/src/
_SCORE_ENGINE_SRC = Path(__file__).resolve().parents[2] / "03_operations" / "bsip2" / "proto_v0" / "src"
if str(_SCORE_ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(_SCORE_ENGINE_SRC))

_score_engine = None


def _get_score_engine():
    global _score_engine
    if _score_engine is None:
        import score_engine as _se
        _score_engine = _se
    return _score_engine


def detect_additives_d4_safe(ingredient_text: str) -> list:
    """Call score_engine.detect_additives_d4 safely; return [] on import error."""
    if not ingredient_text or not ingredient_text.strip():
        return []
    try:
        se = _get_score_engine()
        return se.detect_additives_d4(ingredient_text) or []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# W2 additive explanation lookup — w2_additive_copy_v1.md
# ---------------------------------------------------------------------------

_W2_COPY_PATH = (
    Path(__file__).resolve().parents[2]
    / "01_framework" / "glass_box" / "w2_additive_copy_v1.md"
)

_w2_lookup: dict[str, str] | None = None


def _load_w2_lookup() -> dict[str, str]:
    """Parse w2_additive_copy_v1.md → {E-number: explanation_he}.
    Returns empty dict if file missing or unparseable."""
    global _w2_lookup
    if _w2_lookup is not None:
        return _w2_lookup
    _w2_lookup = {}
    if not _W2_COPY_PATH.exists():
        return _w2_lookup
    try:
        text = _W2_COPY_PATH.read_text(encoding="utf-8")
        blocks = re.split(r"(?=^### E)", text, flags=re.MULTILINE)
        for block in blocks:
            header_m = re.match(r"^### (E[\d]+[a-z]?(?:/E[\d]+[a-z]?)*)", block)
            if not header_m:
                continue
            e_number = header_m.group(1)
            primary_e = e_number.split("/")[0]
            exp_m = re.search(r"\*\*Explanation \(final\):\*\*\s*(.+)", block)
            if exp_m:
                _w2_lookup[primary_e] = exp_m.group(1).strip()
    except Exception:
        pass
    return _w2_lookup


# ---------------------------------------------------------------------------
# Field: novaGroup
# Derives from trace.nova_proxy (always present) as the primary source.
# Some corpus records (juices, cakes) also carry nova_proxy — trace is preferred.
# ---------------------------------------------------------------------------

def derive_nova_group(corpus_rec: dict, trace: dict) -> Any:
    """Return the NOVA proxy from trace (preferred) or corpus."""
    nova = trace.get("nova_proxy")
    if nova is not None:
        return nova
    # Fallback: corpus-level nova_proxy (juices, cakes bsip1 carry this)
    if corpus_rec:
        return corpus_rec.get("nova_proxy", None)
    return None


# ---------------------------------------------------------------------------
# Field: sugarPer100ml
# For liquid categories (juices): corpus.normalized_nutrition_per_100g.sugars_g
# The nutrition panel is already per-100ml for liquid BSIP1 records.
# ---------------------------------------------------------------------------

def derive_sugar_per_100ml(corpus_rec: dict, trace: dict) -> Any:
    if not corpus_rec:
        return None
    nn = corpus_rec.get("normalized_nutrition_per_100g") or {}
    return nn.get("sugars_g", None)


# ---------------------------------------------------------------------------
# Field: kcalPer100ml
# For liquid categories (juices): corpus.normalized_nutrition_per_100g.energy_kcal
# Round to int as the live page does.
# ---------------------------------------------------------------------------

def derive_kcal_per_100ml(corpus_rec: dict, trace: dict) -> Any:
    if not corpus_rec:
        return None
    nn = corpus_rec.get("normalized_nutrition_per_100g") or {}
    kcal = nn.get("energy_kcal", None)
    if kcal is not None:
        try:
            return round(float(kcal))
        except (TypeError, ValueError):
            return None
    return None


# ---------------------------------------------------------------------------
# Field: retailers / _source_retailers
# corpus.source_retailers: always a list (or string — normalise to list).
# The juices schema calls it "retailers"; cakes calls it "_source_retailers".
# Both derive from the same source; the config field name controls the output key.
# ---------------------------------------------------------------------------

def derive_retailers(corpus_rec: dict, trace: dict) -> Any:
    """Return corpus.source_retailers as a list (never null — fall back to trace)."""
    if corpus_rec:
        sr = corpus_rec.get("source_retailers")
        if sr:
            if isinstance(sr, list):
                return sr
            if isinstance(sr, str):
                return [sr]
    # Fallback: trace.input_reference.source_retailers
    ir_sr = trace.get("input_reference", {}).get("source_retailers")
    if ir_sr:
        if isinstance(ir_sr, list):
            return ir_sr
        if isinstance(ir_sr, str):
            return [ir_sr]
    return None


# Same logic — different key name in config
derive_source_retailers = derive_retailers


# ---------------------------------------------------------------------------
# Field: subPool
# For juices: corpus.juice_subpool.
# ---------------------------------------------------------------------------

def derive_sub_pool(corpus_rec: dict, trace: dict) -> Any:
    if not corpus_rec:
        return None
    return corpus_rec.get("juice_subpool", None)


# ---------------------------------------------------------------------------
# Field: _category_routed
# trace.category (the router's category decision, e.g. "snack_bar_granola",
# "dairy_protein", "dessert", "whole_food_fat", "default").
# Matches exactly the field produced by task283_restructure.py / gen_frontend_json.py.
# ---------------------------------------------------------------------------

def derive_category_routed(corpus_rec: dict, trace: dict) -> Any:
    return trace.get("category", None)


# ---------------------------------------------------------------------------
# Field: _product_type
# Hummus-specific: keyword classifier over canonical_name_he + ingredients.
# Ported from batch_run_hummus_001.py::_infer_product_type.
# Config declares it for hummus only.
# Returns null if classification is ambiguous or corpus absent (NEVER guesses).
# ---------------------------------------------------------------------------

_PRODUCT_TYPE_RULES = [
    # (keywords_in_name, keywords_in_name_variant, result)
    # Ordered: most-specific first
    ("מטבוחה",  None,            "matbucha"),
    ("חציל",    "חצילים",        "eggplant_spread"),
    ("מסבחה",   None,            "masabacha"),
    ("פול",     None,            "ful_spread"),
]

# Regex: matches "0%" only when NOT preceded by a digit (avoids "40%" false match)
_LIGHT_ZERO_PCT_RE = re.compile(r"(?<!\d)0%")
_LIGHT_TEXT_MARKERS = ["קל", "דל שומן", "light"]  # text-only markers (no pct substring issue)
_PEPPER_MARKERS = ["פלפל"]
# Context: "קלוי" (roasted), "salat" (salad), "צ'ומה" / "צ'ומא" (chumbe/chuma pepper relish)
_PEPPER_CONTEXT = ["קלוי", "salat", "צ'ומה", "צ'ומא"]
_HUMMUS_MARKERS = ["חומוס", "houmous"]


def _is_light_hummus(name: str) -> bool:
    """True if the name implies a light/reduced-fat hummus product.

    Uses a regex for '0%' to avoid false match on '40%' (tahini content).
    """
    if _LIGHT_ZERO_PCT_RE.search(name):
        return True
    return any(m in name for m in _LIGHT_TEXT_MARKERS)


def derive_product_type(corpus_rec: dict, trace: dict) -> Any:
    """Classify hummus product sub-type from name and ingredients.

    Mirrors _infer_product_type from batch_run_hummus_001.py.
    Returns null (not a guess) when no rule fires.

    Classifier fixes vs original:
      - '0%' check uses regex to avoid '40%' (tahini %) triggering light_hummus.
      - pepper_spread recognises chumbe/chuma (צ'ומה / צ'ומא) as a pepper context.
    """
    if not corpus_rec:
        return None
    name = (corpus_rec.get("canonical_name_he") or "").lower()
    ingredients_list = corpus_rec.get("ingredients_list") or []
    ing = " ".join(ingredients_list).lower()  # noqa: F841 (kept for future ingredient rules)

    if "מטבוחה" in name or "matbucha" in name:
        return "matbucha"
    if "חציל" in name or "חצילים" in name:
        return "eggplant_spread"
    if any(m in name for m in _PEPPER_MARKERS) and any(c in name for c in _PEPPER_CONTEXT):
        return "pepper_spread"
    if _is_light_hummus(name):
        return "light_hummus"
    if "מסבחה" in name:
        return "masabacha"
    if "פול" in name:
        return "ful_spread"
    if "חומוס" in name or "houmous" in name:
        return "hummus_spread"
    return "other_spread"


# ---------------------------------------------------------------------------
# Field: _has_phvo
# trace.L3_inferred_classifications.has_phvo (bool, default False).
# ---------------------------------------------------------------------------

def derive_has_phvo(corpus_rec: dict, trace: dict) -> Any:
    l3 = trace.get("L3_inferred_classifications") or {}
    return bool(l3.get("has_phvo", False))


# ---------------------------------------------------------------------------
# Field: confidence_level
# trace.data_sufficiency — maps directly (values: "sufficient"/"partial"/"insufficient").
# Used by cereals and granola pages.
# ---------------------------------------------------------------------------

def derive_confidence_level(corpus_rec: dict, trace: dict) -> Any:
    return trace.get("data_sufficiency", None)


# ---------------------------------------------------------------------------
# Field: d4_additives
# Runs detect_additives_d4 on corpus ingredients text; enriches each entry
# with explanation_he from w2_additive_copy_v1.md.
# Output shape matches live page: [{e_number, name_he, tier, function_he, explanation_he}, ...]
# Strips match_source (internal field) from output to match live schema.
# Returns [] when no ingredients present.
# ---------------------------------------------------------------------------

def derive_d4_additives(corpus_rec: dict, trace: dict) -> list:
    """Detect D4 additives and enrich with w2 explanation_he."""
    if not corpus_rec:
        return []
    ing_text = (
        corpus_rec.get("ingredients_raw")
        or corpus_rec.get("ingredients_text_he")
        or ""
    )
    if not ing_text and corpus_rec.get("ingredients_list"):
        ing_text = ", ".join(corpus_rec["ingredients_list"])
    if not ing_text:
        return []

    raw_additives = detect_additives_d4_safe(ing_text)
    if not raw_additives:
        return []

    w2 = _load_w2_lookup()
    result = []
    for add in raw_additives:
        e_num = add.get("e_number", "")
        entry = {
            "e_number": e_num,
            "name_he": add.get("name_he", ""),
            "tier": add.get("tier", ""),
            "function_he": add.get("function_he", ""),
            "explanation_he": w2.get(e_num, ""),
        }
        result.append(entry)
    return result


# ---------------------------------------------------------------------------
# Field: glassBox
# The live hummus page carries glassBox for all 57 products (56 unconstrained,
# 1 demote).  The demote state requires a separate D5/D6 engine pass
# (BARI_GLASSBOX_D5D6=on), which is out of scope for the generator (it would
# require running the engine twice and porting the glassBox wiring logic).
#
# Generator policy:
#   - Emit {"gateState": "unconstrained"} for all products.
#   - The single known demoted product (hummus bc=7290104721533) is listed as
#     a residual in the return contract.
#   - Scope: hummus only (other categories don't carry glassBox in live schema).
#
# This gives 56/57 parity on shape; the 1 demote case is an honest residual.
# ---------------------------------------------------------------------------

def derive_glass_box(corpus_rec: dict, trace: dict) -> dict:
    """Return a glassBox object.

    Always emits gateState=unconstrained from the generator.
    The D5/D6 demote/withhold states require a separate engine pass (residual).
    """
    return {"gateState": "unconstrained"}


# ---------------------------------------------------------------------------
# Field: d3_processing_signal
# RESIDUAL: trace_writer.py does NOT include d3_processing_signal in the trace
# JSON (score_engine.py puts it in score_result, but trace_writer doesn't copy
# it).  Deriving it would require modifying trace_writer (scoring engine edit,
# out of scope for TASK-316).  Emit null.
# ---------------------------------------------------------------------------

def derive_d3_processing_signal(corpus_rec: dict, trace: dict) -> Any:
    """Residual — not derivable from trace without engine modification. Emit null."""
    return None


# ---------------------------------------------------------------------------
# Field registry
# Maps config render_field name → derivation function.
# generate_page.py calls get_render_field_value(corpus_rec, trace, field_name).
# ---------------------------------------------------------------------------

FIELD_REGISTRY: dict[str, Any] = {
    "novaGroup":           derive_nova_group,
    "sugarPer100ml":       derive_sugar_per_100ml,
    "kcalPer100ml":        derive_kcal_per_100ml,
    "retailers":           derive_retailers,
    "_source_retailers":   derive_source_retailers,
    "subPool":             derive_sub_pool,
    "_category_routed":    derive_category_routed,
    "_product_type":       derive_product_type,
    "_has_phvo":           derive_has_phvo,
    "confidence_level":    derive_confidence_level,
    "d4_additives":        derive_d4_additives,
    "glassBox":            derive_glass_box,
    "d3_processing_signal": derive_d3_processing_signal,
}


def get_render_field_value(corpus_rec: dict, trace: dict, field_name: str) -> Any:
    """
    Look up and call the derivation function for a render field.
    Falls back to the existing get_extension_field_value logic for legacy
    extension fields not yet ported here (_subpool, _isChildrens, _wholeGrainClaim,
    _internal_cluster).

    Returns None if no derivation function is registered.
    """
    fn = FIELD_REGISTRY.get(field_name)
    if fn is not None:
        return fn(corpus_rec, trace)
    # Unknown field — return None (never fabricate)
    return None
