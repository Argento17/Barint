"""TGA ARTG — Australian Register of Therapeutic Goods (Listed Medicines).

STATUS: BLOCKED — see module-level docstring.

For: supplement corpus worldwide benchmark (TASK-361). Intended to pull
magnesium-primary listed medicines with ingredient + dose + form from the
Australian TGA's open data resources.

--- BLOCKED: NETWORK ACCESS FAILURE ---

Every HTTP route to TGA's data infrastructure was attempted on 2026-06-20
from this environment. Summary:

  Host                    DNS    TCP   Result
  www.tga.gov.au          OK     FAIL  read timeout (firewall / geo-block)
  www.ebs.tga.gov.au      OK     200   reachable but no ARTG data endpoints
  search.tga.gov.au       FAIL   —     DNS not found
  api.tga.gov.au          FAIL   —     DNS not found
  opendata.tga.gov.au     FAIL   —     DNS not found
  health.gov.au           OK     FAIL  read timeout
  healthdirect.gov.au     OK     301   no ARTG medicine ingredient API
  data.gov.au (CKAN)      OK     OK    zero TGA datasets indexed

Paths tried on www.ebs.tga.gov.au (reachable, 200 HEAD /):
  /ebs/artg/artg.nsf/search               404
  /ebs/artg/artg.nsf/PublicSearch         404
  /ebs/artg/artg.nsf/ByIngredient         404
  /ebs/artg/artg.nsf/artg_public_extract.csv  404
  /ebs/artg/artg.nsf/artg_public_extract.json 404
  /ebs/artg/artg.nsf/artg_extract.xlsx    404

Paths tried on www.tga.gov.au (DNS OK, TCP timeout):
  /resources/artg/data/artg_public_extract.xlsx  (timeout)
  /resources/artg/data/artg_extract_listed.csv   (timeout)
  /sites/default/files/artg-extract-listed-medicines.xlsx (timeout)
  /api/v1/artg/search.json                       (timeout)

The TGA does publish a quarterly ARTG public extract (Excel/CSV) at
https://www.tga.gov.au/resources/artg but that URL is not reachable from
this environment.  The EBS portal (ebs.tga.gov.au) is the TGA's
eBusiness Services authentication portal — it has no public ARTG data
endpoints.

--- WHAT TO DO WHEN UNBLOCKED ---

Option A (API, preferred): TGA provides a public ingredient search at
  https://www.tga.gov.au/resources/artg
  No formal REST API is documented; as of 2025 TGA uses a Drupal/CMS
  frontend with no clean JSON endpoint. The approach would be:
    1. Download the quarterly ARTG public extract (Excel) from the URL above.
    2. Parse with openpyxl or pandas; filter Type='L' (Listed) + ingredient='Magnesium'.
    3. Map to the shelf JSON schema (see _SHELF_SCHEMA below).

Option B (bulk extract): The ARTG extract is also available at data.gov.au
  but was not indexed when searched on 2026-06-20.  Check:
    https://data.gov.au/search?q=artg+therapeutic+goods

Option C (Permissible Ingredients): The TGA Permissible Ingredients
  determination (PI) lists approved Mg forms + max doses per claim.
  Available as a PDF/table at:
    https://www.legislation.gov.au/current/F2017L00557
  Use as a form/dose cross-reference, not as a product corpus.

--- SHELF OUTPUT SCHEMA (when implemented) ---
  {
    "region": "AU",
    "source": "TGA ARTG",
    "captured": "YYYY-MM-DD",
    "n": <int>,
    "products": [
      {
        "artg_id": <str>,       # ARTG identifier
        "brand": <str>,
        "name": <str>,
        "form": <str>,          # Mg compound form
        "elemental_mg_per_serving": <float|null>,
        "serving": <str|null>,
        "servings_per_day": <float|null>,
        "dosage_form": <str>,
        "source_url": <str>,    # TGA ARTG product page URL
        "provenance": { ... }
      }
    ]
  }

--- ELEMENTAL CONVERSION FRACTIONS ---
If the TGA source gives compound mass (not elemental), use these fractions
from magnesium_benchmark_v1.md §4:
  oxide 60.3% · trimagnesium dicitrate anhydrous 16.2% / nonahydrate 11.9%
  bisglycinate 14.1% / dihydrate 11.7% · malate 15.5% · taurate 8.9%
  carbonate 28.8% · chloride anhydrous 25.5% / hexahydrate 12.0%
  lactate 12.0% / dihydrate 10.2% · hydroxide 41.7%

OFF is not used as a source for any field — ever.
"""
from __future__ import annotations

CLIENT_VERSION = "1.0"
SOURCE = "tga"

# Elemental fraction lookup (compound name keyword → fraction of elemental Mg)
ELEMENTAL_FRACTIONS: dict[str, float] = {
    "oxide": 0.603,
    "citrate anhydrous": 0.162,
    "citrate nonahydrate": 0.119,
    "citrate": 0.162,          # anhydrous assumed when hydration not stated
    "bisglycinate dihydrate": 0.117,
    "bisglycinate": 0.141,
    "glycinate": 0.141,
    "malate": 0.155,
    "taurate": 0.089,
    "carbonate": 0.288,
    "chloride hexahydrate": 0.120,
    "chloride": 0.255,
    "lactate dihydrate": 0.102,
    "lactate": 0.120,
    "hydroxide": 0.417,
    "gluconate": 0.054,         # 54 mg per 1000 mg compound
    "sulfate": 0.099,
    "threonate": 0.077,
    "orotate": 0.063,
}


def compound_to_elemental_mg(compound_mg: float, form: str) -> float | None:
    """
    Convert compound mass (mg) to elemental Mg (mg) using ELEMENTAL_FRACTIONS.

    form — the compound name as a string (e.g. "Magnesium citrate").
    Returns None if no matching fraction is found (flag as unknown).
    """
    form_lower = form.lower()
    # Longest match wins (e.g. "citrate nonahydrate" before "citrate")
    for keyword, fraction in sorted(ELEMENTAL_FRACTIONS.items(), key=lambda x: -len(x[0])):
        if keyword in form_lower:
            return round(compound_mg * fraction, 2)
    return None


def _raise_blocked() -> None:
    raise NotImplementedError(
        "TGA ARTG client is BLOCKED — www.tga.gov.au is not reachable from this "
        "environment (TCP timeout / geo-block on 2026-06-20). "
        "See tga.py module docstring for unblock instructions."
    )


def search_magnesium(cafile: str | None = None) -> list[dict]:
    """Entry point — raises NotImplementedError with diagnosis until unblocked."""
    _raise_blocked()


if __name__ == "__main__":
    print("TGA ARTG client STATUS: BLOCKED")
    print("www.tga.gov.au is not reachable from this environment (TCP timeout).")
    print("See tga.py module docstring for the full diagnosis and unblock path.")
    print(f"\nElemental fraction reference (for when unblocked):")
    for k, v in ELEMENTAL_FRACTIONS.items():
        print(f"  {k}: {v:.1%}")
