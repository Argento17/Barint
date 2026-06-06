"""
SIE Prototype v0 — Dossier Loader
=================================
Loads + validates the in-house Evidence Dossiers (the firewall membrane, §9).
The engine reads THESE in-house artifacts — never a live external API on the
score path (EDPG). A dossier is `verification_status: candidate` until promoted.

Schema reference: methodology_v1.md §5. This loader is tolerant of the richer
Phase-1 dossier shape (proposed_evidence_tier + ratified evidence_tier, compound
form identity blocks, governing-UL decisions) while exposing a clean, normalized
view to score_engine.
"""
import pathlib
import yaml

DOSSIER_DIR = pathlib.Path(__file__).resolve().parent.parent / "evidence_dossiers"

# Map an active-slug (as referenced by a label) to its dossier filename.
ACTIVE_DOSSIER_FILES = {
    "creatine": "creatine_monohydrate.yaml",
    "creatine_monohydrate": "creatine_monohydrate.yaml",
    "magnesium": "magnesium.yaml",
    "vitamin_d3": "vitamin_d3.yaml",
    "vitamin_d": "vitamin_d3.yaml",
    "caffeine": "caffeine.yaml",
    "omega3": "omega3_epa_dha.yaml",
    "omega3_epa_dha": "omega3_epa_dha.yaml",
    "epa_dha": "omega3_epa_dha.yaml",
    # --- TASK-171H widen: 10 new coverage actives (candidate, no score movement) ---
    "vitamin_c": "vitamin_c.yaml",
    "vitamin_c_ascorbic_acid": "vitamin_c.yaml",
    "ascorbic_acid": "vitamin_c.yaml",
    "zinc": "zinc.yaml",
    "iron": "iron.yaml",
    "calcium": "calcium.yaml",
    "folic_acid": "folic_acid.yaml",
    "folate": "folic_acid.yaml",
    "vitamin_b9": "folic_acid.yaml",
    "vitamin_b12": "vitamin_b12.yaml",
    "b12": "vitamin_b12.yaml",
    "cobalamin": "vitamin_b12.yaml",
    "melatonin": "melatonin.yaml",
    "biotin": "biotin.yaml",
    "vitamin_b7": "biotin.yaml",
    "vitamin_e": "vitamin_e.yaml",
    "alpha_tocopherol": "vitamin_e.yaml",
    "coq10": "coq10.yaml",
    "coenzyme_q10": "coq10.yaml",
    "ubiquinone": "coq10.yaml",
    # constructed throwaway test dossier (§13.4 R2 snake-oil control) — not a real
    # active, not shipped. Every umbrella phrase resolves_to: null.
    "fixture_snakeoil": "_fixture_snakeoil.yaml",
}


class DossierError(ValueError):
    pass


def _require(d: dict, key: str, ctx: str):
    if key not in d:
        raise DossierError(f"dossier '{ctx}' missing required key '{key}'")
    return d[key]


def load_dossier(active_slug: str) -> dict:
    """Load + validate one dossier by active slug. Returns the raw dict plus a
    normalized view the engine consumes (claim->tier map, dose, forms, safety)."""
    fname = ACTIVE_DOSSIER_FILES.get(active_slug)
    if fname is None:
        raise DossierError(f"no dossier mapped for active '{active_slug}' "
                           f"(known: {sorted(set(ACTIVE_DOSSIER_FILES))})")
    path = DOSSIER_DIR / fname
    if not path.exists():
        raise DossierError(f"dossier file not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    ctx = active_slug
    active = _require(raw, "active", ctx)
    canonical = _require(active, "canonical_name", ctx)

    # ---- claims: build a claim-text -> ratified tier map (§2.1) -------------
    claims = _require(raw, "claims", ctx)
    claim_tiers = {}
    for c in claims:
        ctext = _require(c, "claim", ctx)
        # ratified field is `evidence_tier`; fall back to proposed if absent.
        tier = c.get("evidence_tier", c.get("proposed_evidence_tier"))
        if tier is None:
            raise DossierError(f"dossier '{ctx}' claim '{ctext}' has no tier")
        claim_tiers[ctext] = {
            "tier": tier,
            "contested": bool(c.get("contested_flag", False))
                         or str(tier).upper().startswith("CONTESTED"),
            "citations": c.get("citations", []),
            "claim_scope": c.get("claim_scope"),
        }

    # ---- effective dose (§2.2) --------------------------------------------
    ed = _require(raw, "effective_dose", ctx)
    dose = {
        "basis": ed.get("basis"),
        "min_effective": ed.get("min_effective"),
        "typical": ed.get("typical"),
        "upper_studied": ed.get("upper_studied"),
        "unit": ed.get("unit"),
        "elemental_fraction": ed.get("elemental_fraction"),
    }

    # ---- per-form elemental fractions for minerals (§2.2 elemental trap) ----
    elemental_by_form = {}
    for cf in active.get("compound_forms_identity", []) or []:
        frac = cf.get("elemental_mg_fraction", cf.get("elemental_fraction"))
        if frac is not None:
            elemental_by_form[_norm(cf.get("form", ""))] = frac

    # ---- forms ladder (§2.3) ----------------------------------------------
    forms = _require(raw, "forms", ctx)
    form_ladder = {
        "preferred": [_norm(f) for f in forms.get("preferred", [])],
        "acceptable": [_norm(f) for f in forms.get("acceptable", [])],
        "poor": [_norm(f) for f in forms.get("poor", [])],
    }

    # ---- structure/function claim-resolution umbrella (§2.1 / §5, v1.3) -----
    # The firewall membrane for vague-claim resolution. Pre-authored + cited,
    # NEVER inferred. Each mapping is an EXACT key the engine looks up; a key
    # maps iff resolves_to is non-null AND it carries a non-null resolved_tier.
    # A `resolves_to: null` entry is a DELIBERATE non-mapping (documented, not
    # silently absent). Engine reads `mappings[]`; `umbrella_resolution_summary`
    # is human-readable provenance only.
    umbrella = _load_umbrella(raw.get("structure_function_umbrella"), ctx)

    # ---- safety / UL (§2.5) — use governing UL if present ------------------
    safety = _require(raw, "safety", ctx)
    ul = safety.get("upper_limit_UL")
    dose_unit = ed.get("unit")

    normalized = {
        "canonical_name": canonical,
        "category": active.get("category"),
        "claim_tiers": claim_tiers,
        "dose": dose,
        "elemental_by_form": elemental_by_form,
        "form_ladder": form_ladder,
        "safety": {
            "upper_limit_UL": ul,
            "ul_basis": safety.get("ul_basis"),
            "ul_note_threshold": safety.get("ul_note_threshold"),
            "risky_flags": safety.get("risky_flags", []),
        },
        "structure_function_umbrella": umbrella,
        "supp_ev_refs": raw.get("provenance", {}).get("supp_ev_refs", []),
        "verification_status": raw.get("provenance", {}).get("verification_status"),
        "should_affect_score_now": raw.get("provenance", {}).get("should_affect_score_now"),
        "_raw": raw,
    }
    return normalized


# Generic structure/function suffix tokens — stripped to expose the distinctive
# claim term (e.g. "heart health" -> head token "heart"). This is a FROZEN token
# set, not NLP: it just lets an exact lookup of the umbrella phrase tolerate the
# legally-stock "...health/support/function" wording around the real term.
_UMBRELLA_GENERIC_TOKENS = {"health", "support", "supports", "function",
                            "and", "&", "the", "a", "of"}


def _umbrella_key_tokens(phrase: str) -> list:
    """Distinctive token(s) of an umbrella phrase key, used for the engine's
    EXACT membership lookup against the label claim. NO NLP — a frozen split +
    generic-suffix strip. 'heart health' -> ['heart']; 'bone health' -> ['bone']."""
    toks = [t for t in _norm(phrase).replace("&", " ").split()
            if t not in _UMBRELLA_GENERIC_TOKENS]
    return toks


def _load_umbrella(raw_umbrella, ctx: str) -> dict:
    """Validate + normalize the §5 structure_function_umbrella block.
    Returns {'mappings': [ {phrase, key_tokens, resolves_to, resolved_tier,
    citations, supp_ev, maps(bool)} ... ], 'has_umbrella': bool}.
    Tolerant: a dossier without an umbrella returns has_umbrella=False (the
    engine then falls back to the claim-specific path)."""
    if not raw_umbrella:
        return {"has_umbrella": False, "mappings": []}
    raw_maps = raw_umbrella.get("mappings")
    if raw_maps is None:
        raise DossierError(
            f"dossier '{ctx}' structure_function_umbrella missing 'mappings'")
    mappings = []
    for m in raw_maps:
        phrase = _require(m, "phrase", f"{ctx}.structure_function_umbrella")
        resolves_to = m.get("resolves_to")
        resolved_tier = m.get("resolved_tier")
        # a key MAPS iff it carries a non-null endpoint AND a non-null tier.
        maps = resolves_to is not None and resolved_tier is not None
        if maps and not m.get("citations") and not m.get("supp_ev"):
            # §2.1 boundary: a mapping must be CITED to count (authoring discipline).
            raise DossierError(
                f"dossier '{ctx}' umbrella phrase '{phrase}' maps but is "
                f"uncited (no citations and no supp_ev) — uncited correlates "
                f"do not map (§2.1 'plausibly maps' boundary)")
        mappings.append({
            "phrase": phrase,
            "key_tokens": _umbrella_key_tokens(phrase),
            "resolves_to": resolves_to,
            "resolved_tier": resolved_tier,
            "citations": m.get("citations", []),
            "supp_ev": m.get("supp_ev"),
            "maps": maps,
        })
    return {"has_umbrella": True, "mappings": mappings}


def _norm(s: str) -> str:
    """Lowercase + collapse whitespace for form-string matching."""
    return " ".join(str(s).lower().split())


def load_all() -> dict:
    """Load every distinct dossier once; keyed by canonical filename stem."""
    out = {}
    for fname in sorted(set(ACTIVE_DOSSIER_FILES.values())):
        slug = fname.replace(".yaml", "")
        out[slug] = load_dossier(slug if slug in ACTIVE_DOSSIER_FILES
                                 else _slug_for_file(fname))
    return out


def _slug_for_file(fname: str) -> str:
    for slug, f in ACTIVE_DOSSIER_FILES.items():
        if f == fname:
            return slug
    raise DossierError(f"no slug for {fname}")


if __name__ == "__main__":
    for slug in ["creatine", "magnesium", "vitamin_d3", "caffeine", "omega3"]:
        d = load_dossier(slug)
        print(f"{slug:16s} -> {d['canonical_name']:32s} "
              f"claims={len(d['claim_tiers'])} UL={d['safety']['upper_limit_UL']} "
              f"verif={d['verification_status']}")
