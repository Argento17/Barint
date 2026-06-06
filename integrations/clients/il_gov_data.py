"""Israeli government open-data (data.gov.il CKAN) — regulatory + identity layer.

For: Data Agent (corpus identity / legitimacy) and Nutrition Agent (a real food-quality
signal). data.gov.il exposes a CKAN datastore API; these are the Bari-relevant resources,
resolved live 2026-06-03. Resource ids can change — `resolve_resource(pkg)` re-resolves by
package slug if a hardcoded id ever 404s.

Resources:
  imported_foods   — list of imported food products & raw materials (identity, importer)
  pesticide_residues — MoH max pesticide-residue registry (food-quality reference signal)
  max_prices       — official sale points & maximum prices of price-controlled food
                     (a second, government-published price source — complements il_prices)
  food_manufacturers — licensed food manufacturers & businesses (legitimacy check)

NOTE: gov.il occasionally serves a finicky TLS chain; this client tolerates it (CKAN is
public, read-only data). Pair any product identity with `open_food_facts` / `tzameret`
for the nutrition panel — these datasets carry regulatory metadata, not full nutrition.
"""
from __future__ import annotations

import json
import ssl
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

from .provenance import Provenance, stamp

CLIENT_VERSION = "1.0"
API = "https://data.gov.il/api/3/action"

# Resolved live 2026-06-03 (package slug -> datastore-active resource id).
RESOURCES = {
    "imported_foods":     {"pkg": "mazon",           "resource_id": "4cc6c561-5975-4bac-904f-c06489ceeb6d"},
    "pesticide_residues": {"pkg": "673",             "resource_id": "cffe0c50-6856-4187-9315-51bc113cb718"},
    "max_prices":         {"pkg": "import_quotas",   "resource_id": "ef2bc38d-321a-4162-a4d2-ce806cf3f298"},
    "food_manufacturers": {"pkg": "fcs-manufacturer","resource_id": "9c55a7dd-3b92-4141-811c-5e30cc74a8a4"},
}

_CTX = ssl._create_unverified_context()  # gov.il TLS chain is inconsistent; public data


@dataclass
class GovRecords:
    resource_id: str
    total: int
    fields: list[str]
    records: list[dict]
    provenance: Provenance | None = None  # regulatory metadata — not a nutrition panel


def _getj(url: str) -> dict:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Bari/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40, context=_CTX) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def resolve_resource(pkg: str) -> str | None:
    """Re-resolve the first datastore-active resource id for a package slug."""
    d = _getj(f"{API}/package_show?id={urllib.parse.quote(pkg)}")
    if not d.get("success"):
        return None
    res = d["result"].get("resources", [])
    active = [x for x in res if x.get("datastore_active")]
    return (active or res)[0]["id"] if (active or res) else None


def datastore_search(resource_id: str, q: str | None = None, limit: int = 50,
                     filters: dict | None = None) -> GovRecords:
    """Query a CKAN datastore resource. `q` = free-text; `filters` = exact field matches."""
    params = {"resource_id": resource_id, "limit": limit}
    if q:
        params["q"] = q
    if filters:
        params["filters"] = json.dumps(filters)
    url = f"{API}/datastore_search?{urllib.parse.urlencode(params)}"
    d = _getj(url)
    res = d.get("result", {})
    fields = [f["id"] for f in res.get("fields", [])]
    return GovRecords(
        resource_id=resource_id, total=res.get("total", 0),
        fields=fields, records=res.get("records", []),
        provenance=stamp(f"il_gov_data:{resource_id}", resource_id, url, CLIENT_VERSION),
    )


def query(name: str, q: str | None = None, limit: int = 50,
          filters: dict | None = None) -> GovRecords:
    """Query a named Bari resource (see RESOURCES). Falls back to live re-resolve on 404."""
    if name not in RESOURCES:
        raise KeyError(f"unknown resource {name!r}; known: {list(RESOURCES)}")
    rid = RESOURCES[name]["resource_id"]
    try:
        return datastore_search(rid, q=q, limit=limit, filters=filters)
    except urllib.error.HTTPError as e:
        if e.code == 404:  # resource id rotated — re-resolve by package slug
            rid = resolve_resource(RESOURCES[name]["pkg"])
            if rid:
                return datastore_search(rid, q=q, limit=limit, filters=filters)
        raise


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for name in RESOURCES:
        try:
            r = query(name, limit=2)
            print(f"== {name}: total={r.total} ==")
            print(f"   fields: {r.fields[:8]}")
            if r.records:
                first = r.records[0]
                preview = {k: first[k] for k in list(first)[:5]}
                print(f"   sample: {preview}")
        except Exception as e:  # noqa: BLE001
            print(f"== {name}: ERR {type(e).__name__}: {str(e)[:60]}")
