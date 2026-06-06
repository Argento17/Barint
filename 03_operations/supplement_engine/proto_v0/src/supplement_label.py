"""
SIE Prototype v0 — Supplement Label Model
=========================================
The in-house product label the engine reads (the BSIP0-S analogue, §1/§2). For
Phase 2 these are golden-corpus fixtures; in production they are scanned/curated
Israeli SKUs. The engine NEVER reads a live API on the score path — only this.

A label is the minimal observable surface: the active(s) present, the per-serving
quantity + unit, the chemical form, the on-label PRIMARY claim (selects the
dossier tier, §2.1), and proprietary-blend disclosure state.
"""
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class LabelActive:
    """One active row on the label."""
    active_slug: str                 # maps to a dossier (dossier_loader.ACTIVE_DOSSIER_FILES)
    display_name: str                # as printed on label
    quantity: Optional[float]        # per-serving (or per-day per `basis`); None if hidden in blend
    unit: Optional[str]              # "g" | "mg" | "IU" ...
    form: Optional[str]              # chemical form string, matched to the dossier form_ladder
    is_core: bool = True             # named in the product's PRIMARY claim? (§2.4 core vs secondary)
    in_proprietary_blend: bool = False   # dose hidden inside a blend total?
    quantity_basis: str = "per_serving"  # "per_serving" | "per_day"


@dataclass
class SupplementLabel:
    """The in-house product label record (BSIP0-S analogue)."""
    sku_id: str
    product_name: str
    primary_claim: str               # the on-label PRIMARY claim text — must match a dossier claim
    actives: List[LabelActive] = field(default_factory=list)
    servings_per_day: float = 1.0    # to normalize per_serving -> per_day for UL / dose-basis checks
    proprietary_blend_total: Optional[float] = None   # blend mass if a blend is declared
    proprietary_blend_unit: Optional[str] = None
    labeled_regimen: str = "daily"   # "daily" | "weekly" ... (§2.5 clinical-megadose discriminator)
    filler_dominant: bool = False    # actives are a minority of capsule mass (§2.4)
    pixie_roster: bool = False       # long list of trendy actives each at fairy-dust dose (§2.4)
    notes: str = ""

    def core_active(self) -> Optional[LabelActive]:
        """The active named in the primary claim (the scored lead, §2.1/§2.4)."""
        for a in self.actives:
            if a.is_core:
                return a
        return self.actives[0] if self.actives else None
