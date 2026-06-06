"""PubChem — compound / ingredient identity (NIH PUG REST).

For: Research + Nutrition Agents. Resolves an ingredient or additive name to a canonical
chemical identity (CID, formula, weight, synonyms) — useful for disambiguating additive
names, supplement actives, and E-number substances when reasoning about a label. Free,
no auth.

Docs: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
"""
from __future__ import annotations

import urllib.parse
from dataclasses import dataclass, field

from .http import HttpError, get_json

API = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"


@dataclass
class Compound:
    cid: int | None
    name: str
    formula: str | None = None
    weight: float | None = None
    iupac: str | None = None
    synonyms: list[str] = field(default_factory=list)
    found: bool = True


def get_compound(name: str) -> Compound:
    """Resolve a substance name to its PubChem identity. Returns found=False on miss."""
    enc = urllib.parse.quote(name)
    try:
        data = get_json(
            f"{API}/compound/name/{enc}/property/"
            f"MolecularFormula,MolecularWeight,IUPACName/JSON"
        )
    except HttpError as e:
        if e.status == 404:
            return Compound(cid=None, name=name, found=False)
        raise
    props = data.get("PropertyTable", {}).get("Properties", [{}])[0]
    cid = props.get("CID")
    synonyms: list[str] = []
    if cid:
        try:
            syn = get_json(f"{API}/compound/cid/{cid}/synonyms/JSON")
            synonyms = (syn.get("InformationList", {}).get("Information", [{}])[0]
                        .get("Synonym", []))[:8]
        except HttpError:
            pass
    weight = props.get("MolecularWeight")
    return Compound(
        cid=cid,
        name=name,
        formula=props.get("MolecularFormula"),
        weight=float(weight) if weight is not None else None,
        iupac=props.get("IUPACName"),
        synonyms=synonyms,
    )


if __name__ == "__main__":
    for n in ("creatine", "aspartame", "ascorbic acid"):
        c = get_compound(n)
        print(f"{n}: found={c.found} CID={c.cid} formula={c.formula} "
              f"weight={c.weight} synonyms={c.synonyms[:3]}")
