"""
BSIP1 Brand-from-Name Extraction — shared helper (TASK-433)

Deterministic, conservative brand-token detector used by BOTH the crackers
BSIP1 builder (run_crackers_conform_001) and the bread BSIP1 builder
(run_bread_conform_001, re-derive pass) so the two builders apply the exact
same rule.

RULE (conservative — never invent):
  A brand is populated ONLY when one of the confirmed brand tokens below
  appears literally (substring match) in the scraped `name_he` or the
  scraped `brand` field. No fuzzy matching, no manufacturer inference,
  no cross-referencing external brand databases (OFF-adjacent — banned).
  If no token matches, brand stays None — "unknown is acceptable."

Token list is intentionally short and will only be extended when a new
token is confirmed to appear literally in scraped data (see call sites'
run records for the evidence trail). Longer/more-specific tokens are
checked first so a substring token doesn't mis-fire inside another
(e.g. "אנג'ל" variants before any future shorter overlapping token).

Canonical display form is what ships in `brand` — chosen as the shortest
literal token that positively identifies the manufacturer (matches how
the 3 pre-existing bread brands were entered: "KRIT", "מאפיית אנג'ל" /
"אנג'ל", "אסם" pattern).
"""

from __future__ import annotations

# Ordered (token, display_brand) pairs. First literal substring match wins.
# Longer / more specific tokens are listed first to avoid ambiguity.
BRAND_TOKENS: list[tuple[str, str]] = [
    ("מסטמכר", "מסטמכר"),          # Mestemacher
    ("ברמן", "ברמן"),               # Berman
    ("אנג'ל", "אנג'ל"),             # Angel bakery (apostrophe form)
    ("אנגל", "אנג'ל"),              # Angel bakery (non-apostrophe form, same brand)
    ("אסם", "אסם"),                 # Osem
    ("KRIT", "KRIT"),               # KRIT (Latin-script brand, already seen in bread v3)
    ("קריט", "KRIT"),               # KRIT Hebrew transliteration, if it ever appears
]


def extract_brand(name_he: str | None, brand_field: str | None = None) -> str | None:
    """
    Conservative brand-from-name extraction.

    Args:
        name_he: scraped canonical_name_he (or raw name_he) string.
        brand_field: scraped `brand` field, if the retailer populated one
            directly (checked first — a direct retailer brand field is
            higher-confidence evidence than a name substring).

    Returns:
        The canonical display brand string if a token is found, else None.
        NEVER invents a brand not literally present in the inputs.
    """
    # 1. Trust a non-empty, non-generic direct retailer brand field first.
    if brand_field and brand_field.strip():
        bf = brand_field.strip()
        for token, display in BRAND_TOKENS:
            if token in bf:
                return display
        # Retailer supplied a brand string that isn't in our confirmed token
        # list — do NOT invent/normalize it away, but this helper only
        # returns confirmed tokens per the conservative rule; caller may
        # choose to pass through bf itself at a higher layer if desired.
        return None

    # 2. Fall back to scanning the product name for a literal brand token.
    name = (name_he or "")
    for token, display in BRAND_TOKENS:
        if token in name:
            return display

    return None
