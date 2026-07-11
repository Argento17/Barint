"""
layer1_identity.py — Layer 1 (identity) assembly for the Product Dossier
compiler (PD-2 / TASK-610).

Per STF memo `2026-07-11_product-dossier-architecture.md` §4:
  "Layer 1 -- Identity. Truth = registry for {pid, aliases, barcode_status,
  recovered_gtin}; ALL other identity facts (name/brand/pkg/manufacturer/
  urls/last_scrape) = provenance-pointed projections (R-B). Tripwire-1
  firewall: the registry never flows into published pages; served
  id/barcode stay untouched; any served-side backfill is a separate
  owner-gated write the registry merely informs."

PD-2 is registry-independent (see lib/registry_interface.py): the {pid,
barcode_status, recovered_gtin} half of Layer 1 is a documented stub here.
The identity-FACT half (name/brand/urls/last_scrape) is real and built now
-- per R-B these are projections sourced from the served JSON / manifest,
never authoritative copies, and this module never invents a value for one.
"""
from __future__ import annotations

from typing import Dict, Optional

from . import registry_interface as reg


def _fact(value, source: str, derivation: str) -> dict:
    return {"value": value, "source": source, "derivation": derivation}


def assemble_layer1(served_product: dict, layer2_cells: Dict[str, dict]) -> dict:
    key = reg.provisional_key(served_product)
    pid = reg.resolve_bari_pid(key, alias_type="served_id")

    # last_scrape = latest captured_at across retrieved Layer-2 cells (honest
    # "we don't know" if nothing was retrieved -- no imputation).
    captured_dates = [c["captured_at"] for c in layer2_cells.values() if c.get("captured_at")]
    last_scrape = max(captured_dates) if captured_dates else None

    identity_facts = {
        "name": _fact(served_product.get("name"), "served_json_verbatim", "served_json_projection"),
        "brand": _fact(served_product.get("brand"), "served_json_verbatim", "served_json_projection"),
        "package_size": _fact(None, None, "not_retrieved"),   # not present on served product schema today
        "manufacturer": _fact(None, None, "not_retrieved"),   # not present on served product schema today
        "retailer": _fact(served_product.get("retailer"), "served_json_verbatim", "served_json_projection"),
        "source_urls": _fact(
            [u for u in [served_product.get("imageUrl")] if u],
            "served_json_verbatim",
            "served_json_projection",
        ),
        "last_scrape": _fact(last_scrape, "layer2_evidence", "max_captured_at_across_retrieved_cells"),
    }

    return {
        "pid": pid,
        "pid_status": reg.PID_STATUS_RESOLVED if pid else reg.PID_STATUS_UNRESOLVED,
        "provisional_key": key,
        "aliases": sorted({key, f"barcode:{served_product.get('barcode')}"} - {None, "barcode:None"}),
        "barcode_state": {
            "status": "unknown",
            "reason": "stub pending registry join (TASK-609 PD-1)",
            "served_barcode_unadjudicated": served_product.get("barcode"),
        },
        "recovered_gtin": None,
        "identity_facts": identity_facts,
    }
