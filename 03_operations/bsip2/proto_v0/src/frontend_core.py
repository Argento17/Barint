"""
Shared frontend-packaging core (TASK-233B).

Single source of truth for the parts of frontend-JSON packaging that kept drifting
across 10+ bespoke category generators (TASK-233 confirmation sweep, root cause #1):
grade derivation, confidence derivation, the canonical confidence tooltip set, the
VM field allowlist/strip, image-URL selection, numeric rounding, dedup, and the
A-cap field name.

OWNERSHIP BOUNDARY (TASK-233 sequenced rollout, Phase 1 = Data):
  * This module owns the NON-COPY data fields only:
      score, grade, confidence, confidence_label_he, confidence_tooltip_he,
      confidence_sub_reason, imageUrl, barcode, and internal `_`/trace stripping.
  * Consumer-copy STRINGS (insightLine, bottomLine, positiveSignals, limitingFactors,
    rowVerdict, comparisonContext wording) are CONTENT's (Phase 2 / TASK-233C). This
    module never authors or rewrites them — generators keep passing their existing copy
    through untouched.

Hard rules honored:
  * No scoring methodology. Grade is a pure function of the already-computed score.
  * `grade_from_score` BYTE-MATCHES bari-web corpus.ts `frontendGradeFromScore`
    (A>=80 / B>=65 / C>=50 / D>=35 / E) so disk grade == runtime grade (kills DA-009
    drift + DA-002: the 6-grade engine S folds into A here, never ships as "S"/"?").
  * Confidence derivation reuses `confidence_annotation.derive_from_trace` — medium
    does NOT map to verified (fixes DA-005); verified requires a full panel + ingredients.
  * The verified tooltip is the canonical Content-approved line; the retired overclaim
    `ממקור המזון הרשמי` is never emitted (grade_literal_in_copy_ruling_v1, Decision 3).
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import confidence_annotation as CA  # noqa: E402

# ── Re-exported canonical confidence strings (single source of truth) ───────────
# The verified tooltip is the canonical line approved in
# grade_literal_in_copy_ruling_v1 (Decision 3). The retired overclaim
# "כל נתוני התזונה והרכיבים היו זמינים ממקור המזון הרשמי" must NEVER be emitted.
RETIRED_OVERCLAIM_TOOLTIP = "כל נתוני התזונה והרכיבים היו זמינים ממקור המזון הרשמי"
CANONICAL_VERIFIED_TOOLTIP = CA.TOOLTIP_VERIFIED  # "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים."

# ── The A-ceiling cap field name corpus.ts honors (DA-011) ──────────────────────
# corpus.ts `normalizeGrade` reads `_aCappedToB` (NOT `_a_gate_capped`) to hold a
# high-scoring product at B. This is the ONE internal field allowed to survive into
# the raw products array because the runtime grade-normalizer reads it BEFORE the
# field-strip. Generators must write THIS name.
A_CAP_FIELD = "_aCappedToB"

# ── BariProductVM allowlist (emission side) ─────────────────────────────────────
# Top-level keys that may ship on a product. Mirrors view-models/index.ts BariProductVM
# plus the three intentionally-snake_case confidence copy fields the corpus loader
# allowlists (confidence_label_he / confidence_tooltip_he / confidence_sub_reason), plus
# the A-cap field corpus.ts reads at runtime. Everything else (source_traceability_status,
# _cluster, _subpool, novaGroup, _calibration, brand-internal, retailer_he, provenance, ...)
# is stripped at emission. A runtime backstop is also being added at corpus.ts by Frontend.
VM_TOPLEVEL_ALLOWLIST = frozenset({
    "id", "name", "imageUrl", "score", "grade", "insightLine", "confidence",
    "confidence_label_he", "confidence_tooltip_he", "confidence_sub_reason",
    "expansion", "metrics", "rowReason", "rowVerdict", "glassBox",
    "d4_additives", "d3_processing",
    # Established live-JSON identity fields (not in the TS interface but shipped corpus-wide
    # and relied on by the dup-barcode gate, the confidence-annotation trace join, and the
    # schema validator's RECOMMENDED check). These are NOT the DA-012 internal vocabulary
    # (source_traceability_status / _cluster / _subpool / novaGroup / _calibration) that the
    # strip targets — they are kept.
    "barcode", "retailer",
    A_CAP_FIELD,
})

# Expansion sub-keys allowed by BariExpansionVM (the nested object the UI reads).
VM_EXPANSION_ALLOWLIST = frozenset({
    "nutrition", "ingredients", "confidenceLabel", "servingNote",
    "positiveSignals", "limitingFactors", "unknowns", "caveats",
    "bottomLine", "comparisonContext",
})


# ── Grade ───────────────────────────────────────────────────────────────────────
def grade_from_score(score):
    """5-grade consumer scale, byte-matching corpus.ts frontendGradeFromScore.

    The engine's 6-grade S (>=90) folds into A here — the UI palette has no S, and a
    bespoke 'S'/'?' on disk is exactly the DA-002/DA-009 drift this kills. A null/None
    score returns None (INSUFFICIENT products carry no grade); the caller decides
    chip suppression.
    """
    if score is None:
        return None
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    if score >= 35:
        return "D"
    return "E"


def round_score(score):
    """Score is an integer on disk (QA-007: butter shipped 45.2). None stays None."""
    if score is None:
        return None
    return int(round(score))


# ── Confidence ────────────────────────────────────────────────────────────────
def confidence_from_trace(trace):
    """Derive the four confidence fields from a BSIP2 trace.

    Delegates to confidence_annotation.derive_from_trace (medium != verified; verified
    requires full panel + ingredients). Returns a dict with confidence /
    confidence_label_he / confidence_tooltip_he / confidence_sub_reason. The verified
    tooltip is guaranteed to be the canonical line, never the retired overclaim.
    """
    fields = CA.annotate_from_trace(trace)
    _assert_no_overclaim(fields)
    return fields


def confidence_fallback(existing_confidence):
    """For products that cannot join a trace (legacy id schemes). Never fabricates
    verified without trace evidence beyond what the source already carried (DA-013):
    a non-(verified|partial) existing value collapses to partial."""
    fields = CA.annotate_fallback(existing_confidence)
    _assert_no_overclaim(fields)
    return fields


def _assert_no_overclaim(fields):
    if fields.get("confidence_tooltip_he") == RETIRED_OVERCLAIM_TOOLTIP:
        raise ValueError(
            "Refused to emit the retired 'official food source' overclaim tooltip "
            "(grade_literal_in_copy_ruling_v1 Decision 3)."
        )


# ── Image URL ────────────────────────────────────────────────────────────────
def select_image_url(*sources):
    """Pick the real scraped/preserved source image URL, never a synthesized prefix.

    Accepts any number of candidate sources (bsip1 dicts, trace dicts, raw strings)
    in priority order and returns the first real http(s) URL found, trying the
    common scraped-image keys (image_url, image_url_jsonld, image_urls[0]). Returns
    None when no real URL is present — the caller must NOT synthesize a Cloudinary
    prefix guess (that is the frozen_vegetables MNH68_ 404 bug, DA-006/233D).
    """
    keys = ("image_url", "image_url_jsonld", "imageUrl")
    for src in sources:
        if src is None:
            continue
        if isinstance(src, str):
            if _is_real_url(src):
                return src.strip()
            continue
        if isinstance(src, dict):
            for k in keys:
                v = src.get(k)
                if _is_real_url(v):
                    return v.strip()
            arr = src.get("image_urls")
            if isinstance(arr, (list, tuple)):
                for v in arr:
                    if _is_real_url(v):
                        return v.strip()
    return None


def _is_real_url(v):
    return isinstance(v, str) and v.strip().lower().startswith(("http://", "https://"))


# ── Dedup ────────────────────────────────────────────────────────────────────
def dedup_by_barcode(products, key=lambda p: p.get("barcode"), prefer=None):
    """Collapse products sharing a barcode to one record.

    `prefer(a, b)` returns the record to KEEP when two share a barcode (default:
    keep the first seen, i.e. the earlier/frozen-baseline record). Products with a
    falsy barcode are never collapsed (each is distinct). Order is preserved.
    """
    seen = {}
    order = []
    for p in products:
        bc = key(p)
        if not bc:
            order.append(p)
            continue
        bc = str(bc)
        if bc not in seen:
            seen[bc] = p
            order.append(p)
        else:
            kept = seen[bc]
            winner = prefer(kept, p) if prefer else kept
            if winner is not kept:
                # replace in place, preserving position
                idx = order.index(kept)
                order[idx] = winner
                seen[bc] = winner
    return order


# ── Field strip (emission side) ────────────────────────────────────────────────
def strip_non_vm_fields(product, keep=()):
    """Return a copy of `product` carrying only BariProductVM-allowlisted keys.

    Drops every internal/trace/non-VM key at emission so they never ship:
    source_traceability_status, _subpool, _internal_cluster, novaGroup,
    _calibration, brand, retailer, retailer_he, provenance, confidence_level,
    _score_capped, etc. The A-cap field (_aCappedToB) is intentionally preserved
    because corpus.ts reads it at runtime before its own strip. The nested expansion
    object is allowlisted to BariExpansionVM keys too.

    `keep` is an explicit per-category allowlist of LOAD-BEARING internal fields that
    a page's own raw-JSON reader requires (e.g. frozen-vegetables / cheese shelf
    filters read `_cluster` off the raw JSON at module init — stripping it would make
    every shelf lens return zero products). Use it sparingly and only for fields a
    live page provably reads from the raw corpus; everything else stays stripped.
    """
    allow = VM_TOPLEVEL_ALLOWLIST | frozenset(keep)
    out = {k: v for k, v in product.items() if k in allow}
    exp = out.get("expansion")
    if isinstance(exp, dict):
        out["expansion"] = {k: v for k, v in exp.items() if k in VM_EXPANSION_ALLOWLIST}
    return out
