"""Food-additives reference — E-number identity, function class, EFSA evaluation links.

For: Nutrition + Red-Team Agents. Directly supports the Glass Box D4 "additive-evidence"
dimension (the MOAT): turns an `additives_tags` list (e.g. "en:e951") from OFF into
structured identity — canonical name, function class (sweetener / emulsifier / colour /
preservative…), and the link to EFSA's re-evaluation when one exists.

Source: the Open Food Facts additives taxonomy (free, no auth), which curates E-number ->
name -> class and carries EFSA-evaluation + over-exposure flags. Cached to disk on first
fetch (it's one file). Pair with `pubchem.get_compound()` for the chemical identity
(formula/CAS-by-synonym) of the same substance.

HONEST LIMIT: this gives identity + class + EFSA-eval *pointer*. It does NOT give a
numeric ADI value or Israeli-vs-EFSA approval divergence — there is no free REST API for
those; they require monitoring EFSA opinions and Israeli MoH circulars (a documented,
industry-wide gap). Anything that would move a score still needs an EV-### + D7 co-sign.

Taxonomy: https://world.openfoodfacts.org/data/taxonomies/additives.json
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from .http import get

CLIENT_VERSION = "1.0"
TAXONOMY_URL = "https://world.openfoodfacts.org/data/taxonomies/additives.json"
CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "off_additives_taxonomy.json"

_TAXONOMY: dict | None = None


def _normalize_code(s: str) -> str:
    """'E330' / 'e330' / 'en:e330' / '330' -> 'en:e330' (taxonomy key form)."""
    s = (s or "").strip().lower()
    if s.startswith("en:"):
        return s
    s = s.replace("e", "", 1) if s.startswith("e") else s
    digits = re.sub(r"[^0-9a-z]", "", s)
    return f"en:e{digits}" if digits and digits[0].isdigit() else f"en:{s}"


def _load_taxonomy(force: bool = False) -> dict:
    """Load the additives taxonomy, fetching+caching to disk on first use."""
    global _TAXONOMY
    if _TAXONOMY is not None and not force:
        return _TAXONOMY
    if CACHE_PATH.exists() and not force:
        try:
            _TAXONOMY = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            return _TAXONOMY
        except (ValueError, OSError):
            pass
    raw = get(TAXONOMY_URL, timeout=40).decode("utf-8", errors="replace")
    _TAXONOMY = json.loads(raw)
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(raw, encoding="utf-8")
    except OSError:
        pass
    return _TAXONOMY


@dataclass
class Additive:
    code: str                       # canonical 'en:e330'
    e_number: str | None = None     # 'E330'
    name: str | None = None         # 'Citric acid'
    classes: list[str] = field(default_factory=list)   # ['acidity regulator', 'antioxidant']
    efsa_evaluation_url: str | None = None
    overexposure_risk: str | None = None               # EFSA over-exposure flag if present
    from_palm_oil: str | None = None
    found: bool = True
    source_url: str = TAXONOMY_URL


def _lang(entry_field, default=None):
    """Taxonomy fields are {'en': 'x', 'fr': 'y'} — prefer English."""
    if isinstance(entry_field, dict):
        return entry_field.get("en") or next(iter(entry_field.values()), default)
    return entry_field or default


def lookup(code_or_name: str) -> Additive:
    """Resolve an E-number (any spelling) to its identity + class + EFSA-eval pointer."""
    tax = _load_taxonomy()
    key = _normalize_code(code_or_name)
    entry = tax.get(key)
    if entry is None:
        # fall back to a name scan (rare path; e.g. 'aspartame')
        needle = (code_or_name or "").strip().lower()
        for k, v in tax.items():
            nm = _lang(v.get("name"), "") or ""
            if needle and needle in nm.lower():
                key, entry = k, v
                break
    if entry is None:
        return Additive(code=key, found=False)
    name = _lang(entry.get("name"))
    if name and " - " in name:                 # 'E330 - Citric acid' -> 'Citric acid'
        name = name.split(" - ", 1)[1].strip()
    classes_raw = _lang(entry.get("additives_classes"), "") or ""
    classes = [c.replace("en:", "").replace("-", " ").strip()
               for c in classes_raw.split(",") if c.strip()]
    return Additive(
        code=key,
        e_number=(_lang(entry.get("e_number")) and f"E{_lang(entry.get('e_number'))}") or None,
        name=name,
        classes=classes,
        efsa_evaluation_url=_lang(entry.get("efsa_evaluation_url"))
        or _lang(entry.get("efsa_evaluation")),
        overexposure_risk=_lang(entry.get("efsa_evaluation_overexposure_risk")),
        from_palm_oil=_lang(entry.get("from_palm_oil")),
    )


def lookup_tags(additives_tags: list[str]) -> list[Additive]:
    """Resolve a whole OFF `additives_tags` list (['en:e330','en:e951',...])."""
    return [lookup(t) for t in (additives_tags or [])]


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for c in ("E330", "en:e951", "e621", "E102"):
        a = lookup(c)
        print(f"{c}: found={a.found} {a.e_number} {a.name!r} classes={a.classes} "
              f"efsa={'yes' if a.efsa_evaluation_url else 'no'} overexp={a.overexposure_risk}")
