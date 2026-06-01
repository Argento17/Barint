# -*- coding: utf-8 -*-
"""
ingredient_taxonomy.py — TASK-133A (matrix_integrity_framework Req 1 enabling infra)
====================================================================================
Gives the engine ingredient *identity* + *form*, not just *class*.

Today the BSIP1 enricher emits `extracted_additives` / `extracted_matrix_markers`
as `{term, category, position}` dicts. `category` is a FUNCTION bucket
("emulsifier", "wheat_flour") — it does not say *which* emulsifier, nor whether a
starch is native or modified, nor whether a named additive is a flagged concern.

matrix_integrity_framework.md Requirement 1 ("ingredient-form sensitivity") needs
identity: "oats" vs "oat protein isolate", "carrageenan" vs "soy lecithin",
"native starch" vs "modified starch". This module resolves a Hebrew term (or an
existing marker category) to:

    e_number            : str | None   — e.g. "E407" (carrageenan), "E322" (lecithin)
    additive_class      : str | None   — refined functional class for tiering
    fragmentation_level : str | None   — intact | mechanical | fractional | reconstructed
    is_named_concern    : bool         — a specifically named additive of interest

This is ENABLING INFRA ONLY. It changes no score. F2/F1/F4 (TASK-133B/C/D) ride on
it and are gated by DEC-004; do NOT add calibration magnitudes here.

Design constraints (framework §"BSIP2 design implications"):
  • Req 2 — NOVA independence: `fragmentation_level` is derived from STRUCTURAL FORM
    (how far the ingredient is from its intact source food), never from a NOVA bin.
    A NOVA-2 pressed oil is `fractional`; a NOVA-3 stone-ground whole-grain flour is
    `mechanical`. The two axes are intentionally decoupled.
  • Req 3 — primary-ingredient weighting: `primary_fragmentation_profile()` weights by
    ingredient position (reuses the matrix_integrity `_pos_weight` curve when available).
  • Req 5 — gaming resistance: `primary_fragmentation_profile()` reports the
    fragmentation of the PRIMARY ingredients, so a 5% whole-food garnish on a 95%
    reconstructed base cannot claim a whole-food halo.

Evidence registry:
  • EV-003  mucus_thinning_emulsifier_load — CMC/P80/carrageenan vs lecithin vs gum arabic
            (grounds the named-emulsifier identity split that F1/TASK-133C consumes).
  • EV-010  extrusion_matrix_penalty       — grounds `reconstructed` fragmentation.
  • EV-018  reconstituted_matrix_flag      — grounds `reconstructed` for powders/isolates.
  (`bsip2_evidence_registry_v1`.)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

MODULE_VERSION = "ingredient_taxonomy_v1"

# Fragmentation spectrum (framework §"The matrix integrity spectrum").
INTACT = "intact"
MECHANICAL = "mechanical"
FRACTIONAL = "fractional"
RECONSTRUCTED = "reconstructed"
FRAGMENTATION_LEVELS = (INTACT, MECHANICAL, FRACTIONAL, RECONSTRUCTED)
# Ordinal severity for "worst-of" aggregation (intact = least fragmented).
_FRAG_RANK = {INTACT: 0, MECHANICAL: 1, FRACTIONAL: 2, RECONSTRUCTED: 3}


@dataclass(frozen=True)
class Identity:
    """Resolved identity for one ingredient term / marker category."""
    canonical: str                      # canonical machine key
    e_number: Optional[str] = None
    additive_class: Optional[str] = None
    fragmentation_level: Optional[str] = None
    is_named_concern: bool = False
    synonyms_he: tuple = field(default_factory=tuple)

    def as_marker_fields(self) -> dict:
        """The identity fields to graft onto an existing extracted marker dict."""
        return {
            "identity": self.canonical,
            "e_number": self.e_number,
            "additive_class": self.additive_class,
            "fragmentation_level": self.fragmentation_level,
            "is_named_concern": self.is_named_concern,
        }


# ---------------------------------------------------------------------------
# Additive identity table
# ---------------------------------------------------------------------------
# Keyed by canonical id. Each entry carries the Hebrew synonyms seen in BSIP1
# ingredient text AND the function-bucket `category` keys the enricher already
# emits, so we can resolve from either a raw term or an existing marker.
#
# `additive_class` is a REFINED bucket for downstream identity tiering (F1):
#   emulsifier_concern  — CMC, carrageenan, polysorbate-80 (EV-003 high-load)
#   emulsifier_benign   — soy/sunflower lecithin (EV-003 toward neutral)
#   antioxidant_named   — BHA (named concern, F4); BHT (explicitly NOT a concern)
#   thickener_concern   — carrageenan also acts as thickener/stabilizer
# `is_named_concern` marks additives F1/F4 single out by name.
# Additives carry no fragmentation_level (they are not a structural food matrix).
_ADDITIVES: list[Identity] = [
    # ── Emulsifiers / stabilizers — EV-003 identity split (F1 / TASK-133C) ──
    Identity(
        canonical="carrageenan", e_number="E407",
        additive_class="emulsifier_concern", is_named_concern=True,
        synonyms_he=("קרגינן", "קרגינאן", "קרגן", "כרכן ים", "E407", "E 407", "‏407"),
    ),
    Identity(
        canonical="cmc", e_number="E466",
        additive_class="emulsifier_concern", is_named_concern=True,
        synonyms_he=("קרבוקסי מתיל צלולוז", "קרבוקסימתיל צלולוז",
                     "צלולוז גליקולט", "CMC", "E466", "E 466"),
    ),
    Identity(
        canonical="polysorbate_80", e_number="E433",
        additive_class="emulsifier_concern", is_named_concern=True,
        synonyms_he=("פוליסורבט", "פוליסורבט 80", "טווין 80", "E433"),
    ),
    Identity(
        canonical="soy_lecithin", e_number="E322",
        additive_class="emulsifier_benign", is_named_concern=True,
        synonyms_he=("לציטין סויה", "לציטין מסויה", "לציטין", "E322", "E 322"),
    ),
    Identity(
        canonical="sunflower_lecithin", e_number="E322",
        additive_class="emulsifier_benign", is_named_concern=True,
        synonyms_he=("לציטין חמניות", "לציטין מחמניות", "לציטין חמנית"),
    ),
    # ── Named antioxidants — F4 / TASK-133D (BHA concern; BHT explicitly NOT) ──
    Identity(
        canonical="bha", e_number="E320",
        additive_class="antioxidant_named", is_named_concern=True,
        synonyms_he=("בוטילציאניזול", "בוטילטד הידרוקסיאניזול", "BHA", "E320", "E 320"),
    ),
    Identity(
        canonical="bht", e_number="E321",
        # NOT a named concern — F4 explicitly differentiates BHT from BHA.
        additive_class="antioxidant_named", is_named_concern=False,
        synonyms_he=("בוטילהידרוקסיטולואן", "בוטילטד הידרוקסיטולואן", "BHT", "E321", "E 321"),
    ),
]

# ---------------------------------------------------------------------------
# Matrix / structural ingredient identity table (fragmentation level)
# ---------------------------------------------------------------------------
# Maps the BSIP1 matrix-marker `category` keys (and key Hebrew synonyms) to a
# fragmentation level. Levels follow the framework spectrum and are STRUCTURAL,
# not NOVA-derived (Req 2):
#   intact        — cell walls intact (whole groats, whole nuts/seeds, whole legumes)
#   mechanical    — ground / milled / flaked; chemical relationships preserved
#                   (flour, rolled oats, nut butter, flakes)
#   fractional    — one component separated & concentrated (starch, isolate, pressed oil,
#                   refined sugar/syrup, protein concentrate)
#   reconstructed — industrially restructured / molecularly reassembled
#                   (puffed/extruded/expanded, maltodextrin, modified starch, powders)
_MATRIX_FRAGMENTATION: dict[str, str] = {
    # mechanical — milled / flaked grains (matrix disrupted, components co-present)
    "oat_flakes": MECHANICAL, "wheat_flakes": MECHANICAL, "corn_flakes": MECHANICAL,
    "flakes_generic": MECHANICAL,
    "whole_wheat_flour": MECHANICAL, "whole_rye_flour": MECHANICAL, "spelt_flour": MECHANICAL,
    "wheat_flour": MECHANICAL, "rye_flour": MECHANICAL, "oat_flour": MECHANICAL,
    "rice_flour": MECHANICAL, "corn_flour": MECHANICAL, "flour_generic": MECHANICAL,
    "rice_cakes": MECHANICAL,
    # fractional — single component separated & concentrated
    "potato_starch": FRACTIONAL, "corn_starch": FRACTIONAL, "wheat_starch": FRACTIONAL,
    "rice_starch": FRACTIONAL, "starch_generic": FRACTIONAL,
    "dextrose": FRACTIONAL, "dextrin": FRACTIONAL,
    # reconstructed — industrially restructured / molecularly reassembled
    "modified_starch": RECONSTRUCTED, "maltodextrin": RECONSTRUCTED,
    "puffed_cereal": RECONSTRUCTED, "puffed_rice": RECONSTRUCTED, "puffed_barley": RECONSTRUCTED,
    "puffed_corn": RECONSTRUCTED, "puffed": RECONSTRUCTED, "expanded": RECONSTRUCTED,
    "crisped_cereal": RECONSTRUCTED, "crunchy_pieces": RECONSTRUCTED,
}

# Structural ingredients identified directly from Hebrew text (not always emitted as
# a matrix marker today): native vs modified starch, intact whole foods, isolates.
_STRUCTURAL_TERMS: list[tuple[tuple, str, str]] = [
    # (Hebrew synonyms, canonical, fragmentation_level)
    # — native (unmodified) starch: F1 pulls native starch OUT of additive burden.
    (("עמילן עמילני", "עמילן טבעי", "עמילן לא מעובד", "עמילן אורז", "עמילן תירס", "עמילן"),
     "native_starch", FRACTIONAL),
    # — modified starch: stays penalized (reconstructed).
    (("עמילן מעובד", "עמילן שעבר עיבוד", "עמילן מותמר"),
     "modified_starch", RECONSTRUCTED),
    # — intact whole foods (Req 5 anchors: a real whole-food primary ingredient)
    (("גרגירי חומוס", "גרגרי חומוס", "חומוס מבושל", "גרגירים שלמים"),
     "whole_chickpeas", INTACT),
    (("שקדים שלמים", "שקד שלם", "אגוזים שלמים", "אגוז שלם"),
     "whole_nuts", INTACT),
    (("שיבולת שועל מלאה", "גרגירי שיבולת שועל", "גריסי שיבולת שועל"),
     "whole_oat_groats", INTACT),
    (("תמרים", "תמר שלם", "תמרים שלמים"),
     "whole_dates", INTACT),
    # — reconstructed protein isolates / concentrates (matrix absent; F2 anchors)
    (("חלבון מי גבינה מבודד", "חלבון מי גבינה איזולט", "אבקת חלבון מבודד",
      "חלבון סויה מבודד", "חלבון אפונה מבודד", "חלבון מבודד"),
     "protein_isolate", RECONSTRUCTED),
    (("חלבון מי גבינה מרוכז", "חלבון מרוכז", "תרכיז חלבון"),
     "protein_concentrate", FRACTIONAL),
    (("קולגן", "פפטידי קולגן", "חלבון קולגן"),
     "collagen", RECONSTRUCTED),
    # — pressed oils: NOVA-2 but structurally a fat fraction (framework §"What it is not")
    (("שמן דקלים", "שמן קוקוס", "שמן חמניות", "שמן קנולה", "שמן סויה", "שמן זרעי",
      "שמן צמחי", "שמן גרעיני דקלים"),
     "pressed_oil", FRACTIONAL),
    # — refined sugars / syrups: fractional extractions (sweetness without matrix)
    (("סירופ תמרים", "סילאן", "סירופ גלוקוז", "סירופ תירס", "סוכר חום", "סוכר לבן", "סוכר"),
     "refined_sugar", FRACTIONAL),
]


# Build fast lookup indices.
def _norm(s: str) -> str:
    return (s or "").strip().lower()


_BY_CANONICAL: dict[str, Identity] = {}
_SYNONYM_INDEX: dict[str, Identity] = {}   # normalized synonym -> Identity
_STRUCT_INDEX: list[tuple[str, Identity]] = []  # (normalized synonym, Identity)

for _id in _ADDITIVES:
    _BY_CANONICAL[_id.canonical] = _id
    for syn in _id.synonyms_he:
        _SYNONYM_INDEX[_norm(syn)] = _id

for _syns, _canon, _frag in _STRUCTURAL_TERMS:
    _ident = Identity(canonical=_canon, fragmentation_level=_frag, synonyms_he=_syns)
    _BY_CANONICAL.setdefault(_canon, _ident)
    for syn in _syns:
        _STRUCT_INDEX.append((_norm(syn), _ident))
# Longer synonyms first so "עמילן מעובד" wins over "עמילן".
_STRUCT_INDEX.sort(key=lambda kv: -len(kv[0]))


# ---------------------------------------------------------------------------
# Public resolution API
# ---------------------------------------------------------------------------

def resolve_additive(term: Optional[str], category: Optional[str] = None) -> Optional[Identity]:
    """Resolve a named additive from its Hebrew term (preferred) or marker category.

    Returns None when the term is not a *named* additive in the taxonomy — callers
    keep the existing functional `category` and simply gain no identity (graceful).
    """
    t = _norm(term)
    if t:
        # exact synonym hit
        if t in _SYNONYM_INDEX:
            return _SYNONYM_INDEX[t]
        # substring hit (ingredient terms may carry qualifiers, e.g. "לציטין סויה (E322)")
        for syn, ident in sorted(_SYNONYM_INDEX.items(), key=lambda kv: -len(kv[0])):
            if syn and syn in t:
                return ident
    # marker category fallback (e.g. category=="carrageenan" if BSIP1 ever emits it)
    if category and _norm(category) in _BY_CANONICAL:
        return _BY_CANONICAL[_norm(category)]
    return None


def resolve_structural(term: Optional[str], category: Optional[str] = None) -> Optional[Identity]:
    """Resolve a structural ingredient's fragmentation identity.

    Resolution order: marker `category` (most reliable — already disambiguated by the
    enricher) → longest-synonym Hebrew text match. Returns None when unknown.
    """
    c = _norm(category)
    if c and c in _MATRIX_FRAGMENTATION:
        return Identity(canonical=c, fragmentation_level=_MATRIX_FRAGMENTATION[c])
    if c and c in _BY_CANONICAL and _BY_CANONICAL[c].fragmentation_level:
        return _BY_CANONICAL[c]
    t = _norm(term)
    if t:
        for syn, ident in _STRUCT_INDEX:   # already longest-first
            if syn and syn in t:
                return ident
    return None


def fragmentation_for_category(category: Optional[str]) -> Optional[str]:
    """Direct category→fragmentation_level lookup (None when unmapped)."""
    return _MATRIX_FRAGMENTATION.get(_norm(category))


# ---------------------------------------------------------------------------
# Marker-list enrichment (non-destructive: adds identity fields, keeps the rest)
# ---------------------------------------------------------------------------

def enrich_additives(extracted_additives: list[dict]) -> list[dict]:
    """Return a copy of `extracted_additives` with identity fields grafted on.

    Each marker keeps {term, category, position} and gains
    {identity, e_number, additive_class, fragmentation_level, is_named_concern}
    when the term/category resolves to a named additive. Unknown additives are
    passed through unchanged (no identity keys) so existing consumers are unaffected.
    """
    out: list[dict] = []
    for m in extracted_additives or []:
        nm = dict(m)
        ident = resolve_additive(m.get("term"), m.get("category"))
        if ident is not None:
            nm.update(ident.as_marker_fields())
        out.append(nm)
    return out


def enrich_matrix_markers(extracted_matrix_markers: list[dict]) -> list[dict]:
    """Return a copy of `extracted_matrix_markers` with a fragmentation_level grafted on.

    Keeps {term, category, position}; adds {identity, fragmentation_level} when the
    category (or term) resolves. Non-destructive; unknown markers pass through.
    """
    out: list[dict] = []
    for m in extracted_matrix_markers or []:
        nm = dict(m)
        ident = resolve_structural(m.get("term"), m.get("category"))
        if ident is not None:
            nm.setdefault("identity", ident.canonical)
            nm["fragmentation_level"] = ident.fragmentation_level
        out.append(nm)
    return out


# ---------------------------------------------------------------------------
# Primary-ingredient fragmentation profile (Req 3 + Req 5)
# ---------------------------------------------------------------------------

try:  # reuse the calibrated position-weight curve when available
    from matrix_integrity import _pos_weight as _MI_POS_WEIGHT  # type: ignore
except Exception:  # pragma: no cover - standalone fallback
    def _MI_POS_WEIGHT(pos: Optional[int]) -> float:
        if pos is None:
            return 0.12
        table = {1: 1.0, 2: 0.82, 3: 0.68, 4: 0.55, 5: 0.44}
        return table.get(pos, 0.13 if pos <= 10 else 0.08)


def primary_fragmentation_profile(
    ingredient_order: list[dict],
    matrix_markers: list[dict],
    primary_n: int = 3,
) -> dict:
    """Position-weighted fragmentation of the PRIMARY ingredients.

    Req 3 — primary-ingredient focus: weights by ingredient position.
    Req 5 — gaming resistance: a whole-food ingredient that appears only in a late
    (minor) position contributes little weight, so a 5% garnish cannot move
    `dominant_fragmentation` away from a reconstructed primary base.

    Returns:
      dominant_fragmentation : worst (most-fragmented) level among the primary set,
                               or None when no primary ingredient resolves.
      weighted_levels        : {level: summed position weight} over resolved markers.
      primary_levels         : list of (position, identity, level) for positions ≤ primary_n.
      resolved_count / total : coverage of the primary set.
    """
    enriched = enrich_matrix_markers(matrix_markers)
    weighted: dict[str, float] = {lvl: 0.0 for lvl in FRAGMENTATION_LEVELS}
    primary_levels: list[tuple] = []
    resolved = 0

    # markers carry positions; also try to resolve raw text at primary positions
    by_pos: dict[int, str] = {}
    for m in enriched:
        lvl = m.get("fragmentation_level")
        pos = m.get("position")
        if lvl:
            weighted[lvl] += _MI_POS_WEIGHT(pos)
            if pos is not None and pos <= primary_n:
                primary_levels.append((pos, m.get("identity") or m.get("category"), lvl))
                by_pos[pos] = lvl
            resolved += 1

    # also scan raw primary ingredient text for structural identity (native starch,
    # isolates, whole foods) the matrix-marker list may not carry.
    for item in (ingredient_order or [])[:primary_n]:
        pos = item.get("position")
        if pos in by_pos:
            continue
        ident = resolve_structural(item.get("text"), None)
        if ident and ident.fragmentation_level:
            lvl = ident.fragmentation_level
            weighted[lvl] += _MI_POS_WEIGHT(pos)
            primary_levels.append((pos, ident.canonical, lvl))
            by_pos[pos] = lvl
            resolved += 1

    # dominant = the most-fragmented level present among the PRIMARY positions
    # (Req 5: judged on primaries, not on a minor whole-food garnish)
    dominant = None
    if by_pos:
        dominant = max(by_pos.values(), key=lambda lvl: _FRAG_RANK[lvl])

    total_primary = len([i for i in (ingredient_order or []) if (i.get("position") or 99) <= primary_n]) \
        or min(primary_n, len(ingredient_order or []))

    return {
        "dominant_fragmentation": dominant,
        "weighted_levels": {k: round(v, 3) for k, v in weighted.items() if v > 0},
        "primary_levels": sorted(primary_levels),
        "resolved_count": resolved,
        "primary_total": total_primary,
    }


# ---------------------------------------------------------------------------
# Self-test (run: python ingredient_taxonomy.py)
# ---------------------------------------------------------------------------
def _selftest() -> None:
    ok = True

    def check(cond: bool, label: str):
        nonlocal ok
        print(f"[{'PASS' if cond else 'FAIL'}] {label}")
        if not cond:
            ok = False

    # ── Named additives (133C/133D coverage) ──
    car = resolve_additive("קרגינן")
    check(car is not None and car.e_number == "E407"
          and car.additive_class == "emulsifier_concern" and car.is_named_concern,
          "carrageenan קרגינן -> E407, emulsifier_concern, named")
    cmc = resolve_additive("קרבוקסי מתיל צלולוז")
    check(cmc is not None and cmc.e_number == "E466" and cmc.additive_class == "emulsifier_concern",
          "CMC -> E466, emulsifier_concern")
    soy = resolve_additive("לציטין סויה")
    check(soy is not None and soy.e_number == "E322" and soy.additive_class == "emulsifier_benign",
          "soy lecithin לציטין סויה -> E322, emulsifier_benign (F1 down-weight)")
    # plain "לציטין" resolves to soy lecithin family (benign)
    lec = resolve_additive("לציטין")
    check(lec is not None and lec.additive_class == "emulsifier_benign",
          "bare לציטין -> emulsifier_benign")
    bha = resolve_additive("BHA")
    check(bha is not None and bha.e_number == "E320" and bha.is_named_concern,
          "BHA -> E320, is_named_concern=True")
    bht = resolve_additive("BHT")
    check(bht is not None and bht.e_number == "E321" and bht.is_named_concern is False,
          "BHT -> E321, is_named_concern=False (explicitly differentiated)")

    # ── Native vs modified starch (133C) ──
    native = resolve_structural("עמילן תירס", None)
    check(native is not None and native.canonical == "native_starch"
          and native.fragmentation_level == FRACTIONAL,
          "native corn starch עמילן תירס -> native_starch / fractional")
    modified = resolve_structural("עמילן מעובד", None)
    check(modified is not None and modified.canonical == "modified_starch"
          and modified.fragmentation_level == RECONSTRUCTED,
          "modified starch עמילן מעובד -> modified_starch / reconstructed (longest-match wins)")

    # ── Fragmentation levels from existing marker categories (Req 2: structural, not NOVA) ──
    check(fragmentation_for_category("wheat_flour") == MECHANICAL, "wheat_flour -> mechanical")
    check(fragmentation_for_category("corn_starch") == FRACTIONAL, "corn_starch -> fractional")
    check(fragmentation_for_category("puffed_cereal") == RECONSTRUCTED, "puffed_cereal -> reconstructed")
    check(fragmentation_for_category("modified_starch") == RECONSTRUCTED, "modified_starch -> reconstructed")

    # ── Enrichment is non-destructive ──
    add_in = [{"term": "לציטין חמניות", "category": "emulsifier", "position": 15},
              {"term": "מייצב", "category": "stabilizer", "position": 14}]
    add_out = enrich_additives(add_in)
    check(add_out[0]["category"] == "emulsifier" and add_out[0]["position"] == 15
          and add_out[0]["identity"] == "sunflower_lecithin" and add_out[0]["e_number"] == "E322",
          "enrich_additives grafts identity, keeps category/position")
    check("identity" not in add_out[1],
          "unknown additive (מייצב) passes through with no identity key")
    check(add_in[0] == {"term": "לציטין חמניות", "category": "emulsifier", "position": 15},
          "enrich_additives does not mutate input")

    mm_in = [{"term": "פתיתי שיבולת שועל", "category": "oat_flakes", "position": 1},
             {"term": "עמילן מעובד", "category": "modified_starch", "position": 5}]
    mm_out = enrich_matrix_markers(mm_in)
    check(mm_out[0]["fragmentation_level"] == MECHANICAL, "oat_flakes marker -> mechanical")
    check(mm_out[1]["fragmentation_level"] == RECONSTRUCTED, "modified_starch marker -> reconstructed")

    # ── Gaming resistance (Req 5): 95% reconstructed base + 5% whole-food garnish ──
    ingredient_order = [
        {"text": "חלבון מי גבינה מבודד", "position": 1},  # protein isolate (reconstructed)
        {"text": "עמילן מעובד", "position": 2},            # modified starch (reconstructed)
        {"text": "סירופ גלוקוז", "position": 3},            # refined syrup (fractional)
        {"text": "שיבולת שועל מלאה", "position": 9},        # whole-oat garnish, minor position
    ]
    profile = primary_fragmentation_profile(ingredient_order, [])
    check(profile["dominant_fragmentation"] == RECONSTRUCTED,
          "gaming: reconstructed primary base dominates; 5% whole-oat garnish cannot claim halo")

    # ── Intact whole-food product stays intact-dominant ──
    hummus_order = [
        {"text": "גרגירי חומוס מבושלים", "position": 1},
        {"text": "טחינה גולמית", "position": 2},
        {"text": "מיץ לימון", "position": 3},
    ]
    hp = primary_fragmentation_profile(hummus_order, [])
    check(hp["dominant_fragmentation"] == INTACT,
          "hummus: whole chickpeas at pos1 -> intact-dominant primary profile")

    print("\nSELFTEST: " + ("ALL PASS" if ok else "FAILURES PRESENT"))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    _selftest()
