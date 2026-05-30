"""
BSIP2 Bakery Semantics Layer v1

Domain-specific interpretation framework for bread/cracker/crispbread systems.
Called after routing; adds structured bakery semantics to the trace.

This layer does NOT score products. It provides interpretation context:
- Flour hierarchy: dominant flour type and structural quality (1-5 scale)
- Fermentation quality: traditional / mixed_industrial / flavor_only / theater / none
- Fiber source quality: structural (grain) vs isolated (extracted) vs hybrid
- Seed semantics: structural role vs seed halo vs decorative surface coating

These signals then feed into:
- structural_classifier.py (rebalancing class weights for bakery products)
- score_engine.py (fiber source discount, calorie density, whole_food_integrity adjustment)
"""

from __future__ import annotations

BAKERY_SEMANTICS_VERSION = "bakery_semantics_v1"

BAKERY_CATEGORIES: frozenset[str] = frozenset({"bread", "cracker", "crispbread"})


# ─── Vocabulary ─────────────────────────────────────────────────────────────

# Whole-grain flour / grain terms (structural — bran intact)
WHOLE_GRAIN_TERMS: list[str] = [
    "קמח חיטה מלאה",     # whole wheat flour
    "קמח שיפון מלא",     # whole rye flour
    "קמח שיבולת שועל מלא",  # whole oat flour
    "קמח כוסמין מלא",    # whole spelt flour
    "קמח כוסמת",         # buckwheat flour (inherently whole grain)
    "קמח מלא",           # whole flour (generic)
    "חיטה מלאה",         # whole wheat grain (stone-ground dough)
    "שיפון מלא",         # whole rye grain
    "שיבולת שועל מלאה",  # whole oats (rolled)
    "כוסמת",             # buckwheat
    "כוסמין",            # spelt
    "גרגרי שיפון",       # rye berries
]

# Refined flour terms (structural bran removed)
REFINED_FLOUR_TERMS: list[str] = [
    "קמח חיטה",          # refined wheat flour (no "מלאה" qualifier)
    "קמח לבן",           # white flour
    "קמח עשיר",          # enriched white flour
    "גלוטן חיטה",        # vital wheat gluten (isolated protein)
    "עמילן חיטה",        # wheat starch (highly refined)
    "עמילן תירס",        # corn starch
    "עמילן",             # generic starch
    "קמח אורז",          # rice flour (typically white)
    "קמח תפוחי אדמה",    # potato flour
]

# Sourdough terms by authenticity tier
_SOURDOUGH_GENUINE: list[str] = ["מחמצת חיה", "מחמצת טבעית"]
_SOURDOUGH_DEHYDRATED: list[str] = ["מחמצת מגובשת", "אבקת מחמצת", "מחמצת יבשה", "מחמצת בסיס"]
_SOURDOUGH_GENERIC: str = "מחמצת"
_COMMERCIAL_YEAST: str = "שמרים"
_LACTIC_ACID_CHEMICAL: str = "חומצה לקטית"
_SOURDOUGH_STYLE_NAMES: list[str] = ["בסגנון מחמצת", "בטעם מחמצת"]

# Chemical leaveners (not fermentation — used when sourdough is just flavor)
_CHEMICAL_LEAVENERS: list[str] = ["E-450", "E450", "E-500", "E500", "E-501", "E501", "E-503", "E503"]

# Isolated fiber additives (NOT structural grain fiber)
ISOLATED_FIBER_TERMS: list[str] = [
    "אינולין",           # inulin (chicory extract)
    "ציליום",            # psyllium husk
    "סיבי ציליום",       # psyllium fiber
    "תאית",              # cellulose (extracted)
    "סיבי תאית",         # cellulose fiber
    "בטא-גלוקן",         # beta-glucan (can be isolated)
    "גואר",              # guar gum
    "קסנטן",             # xanthan gum
    "פקטין",             # pectin
    "פולידקסטרוז",       # polydextrose (synthetic fiber)
    "סיבים תזונתיים",    # dietary fiber (generic — often isolated)
]

# Seed terms (for structural vs halo analysis)
SEED_TERMS: list[str] = [
    "שומשום",    # sesame
    "פשתן",      # flax
    "צ'יה",      # chia
    "chia",
    "חמניה",     # sunflower seeds
    "חמניות",    # sunflower seeds (plural)
    "דלעת",      # pumpkin seeds
    "קנבוס",     # hemp seeds
    "מרווה",     # sage seeds
]


# ─── Helpers ────────────────────────────────────────────────────────────────

def _name(p: dict) -> str:
    return (p.get("canonical_name_he") or "").lower()

def _ing_text(p: dict) -> str:
    return (p.get("ingredients_text_he") or "").lower()

def _ing_order(p: dict) -> list[dict]:
    return p.get("ingredient_order") or []

def _nn(p: dict) -> dict:
    return p.get("normalized_nutrition_per_100g") or {}


def is_bakery_category(category: str) -> bool:
    return category in BAKERY_CATEGORIES


# ─── 1. Flour Hierarchy ─────────────────────────────────────────────────────

def interpret_flour_hierarchy(product: dict) -> dict:
    """
    Classify flour structure: dominant type, whole-grain dominance, quality class.

    flour_quality_class: 1=grain_compressed, 2=whole_dominant, 3=mixed, 4=refined_dominant, 5=refined_only
    whole_grain_dominance: high / partial / decorative / none
    dominant_flour_type: grain_compressed / whole / mixed / refined / unknown
    """
    order    = _ing_order(product)
    ing_text = _ing_text(product)
    notes: list[str] = []

    # Build flour hit lists from ingredient order (preferred — has position + pct)
    wg_hits: list[dict] = []
    rf_hits: list[dict] = []

    for item in order:
        pos  = item.get("position", 99)
        text = (item.get("text") or "").lower()
        pct  = item.get("percentage_declared")
        if any(kw in text for kw in WHOLE_GRAIN_TERMS):
            wg_hits.append({"pos": pos, "text": text, "pct": pct})
        elif any(kw in text for kw in REFINED_FLOUR_TERMS):
            rf_hits.append({"pos": pos, "text": text, "pct": pct})

    # Fallback: text detection without position
    if not wg_hits and not rf_hits:
        has_wg = any(kw in ing_text for kw in WHOLE_GRAIN_TERMS)
        has_rf = any(kw in ing_text for kw in REFINED_FLOUR_TERMS)
        if has_wg:
            wg_hits.append({"pos": 3, "text": "text_detected", "pct": None})
            notes.append("wg_detected_from_text_only:position_inferred")
        if has_rf:
            rf_hits.append({"pos": 2, "text": "text_detected", "pct": None})
            notes.append("refined_detected_from_text_only:position_inferred")

    has_wg = bool(wg_hits)
    has_rf = bool(rf_hits)

    if not has_wg and not has_rf:
        return _flour_result("unknown", "none", "unknown", 3, ["no_flour_detected"])

    wg_min = min(h["pos"] for h in wg_hits) if wg_hits else 99
    rf_min = min(h["pos"] for h in rf_hits) if rf_hits else 99
    wg_pct = sum(h["pct"] for h in wg_hits if h.get("pct")) or None
    rf_pct = sum(h["pct"] for h in rf_hits if h.get("pct")) or None

    if has_wg and not has_rf:
        if wg_pct and wg_pct >= 80:
            return _flour_result("grain_compressed", "high", "absent", 1,
                                 [f"whole_grain_dominant_pct={wg_pct}%"])
        return _flour_result("whole", "high", "absent", 2, [f"whole_grain_only:pos={wg_min}"])

    if has_rf and not has_wg:
        return _flour_result("refined", "none", "dominant", 5, [f"refined_only:pos={rf_min}"])

    # Mixed: both detected
    if wg_pct and rf_pct:
        notes.append(f"pct_data: wg={wg_pct}% rf={rf_pct}%")
        if wg_pct >= rf_pct * 1.5:
            dom, wgd, rfp, fqc = "whole", "high", "secondary", 2
        elif rf_pct >= wg_pct * 1.5:
            wgd = "decorative" if wg_min >= 4 else "partial"
            dom, rfp, fqc = "refined", "dominant", (4 if wgd == "decorative" else 3)
        else:
            dom, wgd, rfp, fqc = "mixed", "partial", "secondary", 3
    else:
        notes.append(f"position_proxy: wg_pos={wg_min} rf_pos={rf_min}")
        if wg_min < rf_min:
            wgd = "high" if wg_min <= 2 else "partial"
            dom, rfp, fqc = "whole", "secondary", (2 if wg_min <= 2 else 3)
        elif rf_min < wg_min:
            wgd = "decorative" if wg_min >= 4 else "partial"
            dom, rfp, fqc = "refined", "dominant", (4 if wgd == "decorative" else 3)
        else:
            dom, wgd, rfp, fqc = "mixed", "partial", "secondary", 3

    return _flour_result(dom, wgd, rfp, fqc, notes)


def _flour_result(dominant, wg_dom, rf_pres, fqc, notes):
    return {
        "dominant_flour_type":  dominant,
        "whole_grain_dominance": wg_dom,
        "refined_presence":     rf_pres,
        "flour_quality_class":  fqc,   # 1=best, 5=worst
        "flour_hierarchy_notes": notes,
    }


# ─── 2. Fermentation Quality ─────────────────────────────────────────────────

def classify_fermentation_quality(product: dict) -> dict:
    """
    Classify fermentation system depth.

    fermentation_quality: traditional | mixed_industrial | flavor_only | theater | none
    """
    ing_text  = _ing_text(product)
    name      = _name(product)
    order     = _ing_order(product)
    basis: list[str] = []

    # Theater: name claims sourdough but check ingredients first
    is_theater_name = any(kw in name for kw in _SOURDOUGH_STYLE_NAMES)

    # Find sourdough in ingredient order
    sourdough_pos = sourdough_pct = None
    for item in order:
        text = (item.get("text") or "").lower()
        if _SOURDOUGH_GENERIC in text:
            sourdough_pos = item.get("position")
            sourdough_pct = item.get("percentage_declared")
            break

    has_genuine    = any(kw in ing_text for kw in _SOURDOUGH_GENUINE)
    has_dehydrated = any(kw in ing_text for kw in _SOURDOUGH_DEHYDRATED)
    has_sourdough  = _SOURDOUGH_GENERIC in ing_text or has_genuine
    has_yeast      = _COMMERCIAL_YEAST in ing_text
    has_lactic_chem = _LACTIC_ACID_CHEMICAL in ing_text
    has_chem_leaven = any(kw in ing_text for kw in _CHEMICAL_LEAVENERS)

    if not has_sourdough:
        if is_theater_name:
            basis.append("sourdough_name_no_ingredient")
            return _ferm_result("theater", basis,
                                "Name uses sourdough claim but no sourdough in ingredient list.")
        return _ferm_result("none", [], "No fermentation markers detected.")

    if has_dehydrated:
        basis.extend([kw for kw in _SOURDOUGH_DEHYDRATED if kw in ing_text])
        if has_yeast or has_chem_leaven:
            basis.append("commercial_leavener_confirmed")
        return _ferm_result("flavor_only", basis,
                            "Dehydrated/powdered sourdough is a flavor agent, not a leavening system. "
                            + ("Commercial yeast/chemical leaveners do the actual leavening." if (has_yeast or has_chem_leaven) else ""))

    if sourdough_pct is not None and sourdough_pct < 10 and has_yeast:
        basis.extend(["מחמצת", f"pct={sourdough_pct}%", "שמרים"])
        return _ferm_result("flavor_only", basis,
                            f"Sourdough ({sourdough_pct}%) is a minor flavor contributor; "
                            "commercial yeast is the structural leavening agent.")

    if has_yeast and has_sourdough:
        basis.extend(["מחמצת", "שמרים"])
        pct_str = f" ({sourdough_pct}%)" if sourdough_pct else ""
        return _ferm_result("mixed_industrial", basis,
                            f"Mixed leavening system: sourdough starter{pct_str} + commercial yeast. "
                            "Sourdough contributes flavor and partial fermentation benefit.")

    # Check: sourdough without commercial yeast but WITH chemical leaveners
    # E-450, E-500 etc. do the actual leavening → sourdough is flavor contributor
    if sourdough_pct is not None and sourdough_pct < 10 and has_chem_leaven:
        basis.extend(["מחמצת", f"pct={sourdough_pct}%", "chemical_leavener"])
        return _ferm_result("flavor_only", basis,
                            f"Sourdough ({sourdough_pct}%) is a minor contributor; "
                            "chemical leaveners (E-450/E-500) do the actual leavening.")

    # Sourdough without commercial yeast or chemical leaveners → traditional
    basis.append("מחמצת")
    if has_genuine:
        basis.extend([kw for kw in _SOURDOUGH_GENUINE if kw in ing_text])
    pct_str = f" at {sourdough_pct}%" if sourdough_pct else ""
    return _ferm_result("traditional", basis,
                        f"Traditional sourdough fermentation{pct_str}. No commercial yeast detected.")


def _ferm_result(quality, basis, notes):
    return {
        "fermentation_quality": quality,
        "fermentation_basis":   basis,
        "fermentation_notes":   notes,
    }


# ─── 3. Fiber Source Quality ─────────────────────────────────────────────────

def classify_fiber_source_quality(product: dict, l3: dict) -> dict:
    """
    Distinguish structural grain fiber from isolated extracted fiber.

    fiber_source_quality: structural | isolated | hybrid | minimal | unknown
    """
    ing_text = _ing_text(product)
    nn       = _nn(product)
    fiber_g  = nn.get("dietary_fiber_g") or 0
    has_wg   = l3.get("has_whole_grain", False)

    isolated = [kw for kw in ISOLATED_FIBER_TERMS if kw in ing_text]
    has_iso  = bool(isolated)

    if fiber_g < 2 and not has_iso:
        return _fiber_result("minimal", [], "low_fiber",
                             f"Low fiber ({fiber_g}g). No isolated additives.")

    if not has_iso:
        return _fiber_result("structural", [], "whole_grain" if has_wg else "grain_milling",
                             f"{fiber_g}g fiber, no isolated markers. Grain-structural source.")

    if has_wg:
        return _fiber_result("hybrid", isolated, "whole_grain_partial",
                             f"{fiber_g}g fiber: whole grain detected AND isolated additives "
                             f"({', '.join(isolated)}). Cannot separate contributions.")

    return _fiber_result("isolated", isolated, "none",
                         f"{fiber_g}g fiber primarily from isolated sources ({', '.join(isolated)}). "
                         "No whole-grain basis — additive-origin fiber.")


def _fiber_result(quality, isolated, basis, notes):
    return {
        "fiber_source_quality":   quality,
        "isolated_fiber_markers": isolated,
        "structural_fiber_basis": basis,
        "fiber_source_notes":     notes,
    }


# ─── 4. Seed Semantics ───────────────────────────────────────────────────────

def interpret_seed_signals(product: dict) -> dict:
    """
    Classify seed role: structural identity vs halo vs decorative surface coating.

    seed_role: structural | halo | decorative | none | unpositioned
    """
    order    = _ing_order(product)
    ing_text = _ing_text(product)
    name     = _name(product)

    seeds_in_text = [kw for kw in SEED_TERMS if kw in ing_text]
    seeds_in_name = [kw for kw in SEED_TERMS if kw in name]

    if not seeds_in_text:
        return _seed_result("none", [], None, "No seed ingredients detected")

    # Find seed positions in ingredient order
    seed_hits: list[dict] = []
    for item in order:
        text = (item.get("text") or "").lower()
        pct  = item.get("percentage_declared")
        pos  = item.get("position", 99)
        if any(kw in text for kw in SEED_TERMS):
            seed_hits.append({"pos": pos, "text": text, "pct": pct})

    if not seed_hits:
        role = "halo" if seeds_in_name else "unpositioned"
        return _seed_result(role, seeds_in_text, None,
                            "Seeds detected in text but no position data available")

    min_pos = min(h["pos"] for h in seed_hits)
    dom     = next(h for h in seed_hits if h["pos"] == min_pos)
    dom_pct = dom.get("pct")

    notes_parts = []
    for h in seed_hits:
        pct_s = f"({h['pct']}%)" if h.get("pct") else ""
        notes_parts.append(f"'{h['text']}' pos{h['pos']} {pct_s}".strip())
    pos_notes = "; ".join(notes_parts)

    # Classification
    if min_pos <= 2 or (dom_pct and dom_pct >= 15):
        role = "structural"
    elif min_pos >= 5 or (dom_pct is not None and dom_pct < 5):
        role = "decorative"
    else:
        # Middle ground: halo if in name, otherwise borderline structural
        role = "halo" if seeds_in_name else "halo"

    return _seed_result(role, seeds_in_text, min_pos, pos_notes)


def _seed_result(role, found, dom_pos, notes):
    return {
        "seed_role":             role,
        "seed_terms_found":      found,
        "dominant_seed_position": dom_pos,
        "seed_position_notes":   notes,
    }


# ─── Main Entry Point ────────────────────────────────────────────────────────

def run_bakery_semantics(product: dict, category: str, l3: dict) -> dict | None:
    """
    Run full bakery semantics. Returns None for non-bakery categories.
    Result is attached to trace as 'bakery_semantics'.
    """
    if not is_bakery_category(category):
        return None

    flour = interpret_flour_hierarchy(product)
    ferm  = classify_fermentation_quality(product)
    fiber = classify_fiber_source_quality(product, l3)
    seed  = interpret_seed_signals(product)

    # Composite grain_structure_score (0-100, purely informational)
    fqc        = flour.get("flour_quality_class", 3)  # 1=best, 5=worst
    ferm_q     = ferm.get("fermentation_quality", "none")
    fiber_q    = fiber.get("fiber_source_quality", "unknown")

    fqc_score   = max(0, (5 - fqc) / 4 * 100)              # 1→100, 5→0
    ferm_scores = {"traditional": 100, "mixed_industrial": 55, "flavor_only": 20, "theater": 5, "none": 40}
    ferm_score  = ferm_scores.get(ferm_q, 40)
    fiber_scores = {"structural": 100, "hybrid": 60, "isolated": 20, "minimal": 50, "unknown": 50}
    fiber_score = fiber_scores.get(fiber_q, 50)

    grain_structure_score = round(0.50 * fqc_score + 0.30 * ferm_score + 0.20 * fiber_score, 1)

    return {
        "flour_hierarchy":         flour,
        "fermentation_quality":    ferm,
        "fiber_source_quality":    fiber,
        "seed_semantics":          seed,
        "grain_structure_score":   grain_structure_score,
        "bakery_semantics_version": BAKERY_SEMANTICS_VERSION,
    }
