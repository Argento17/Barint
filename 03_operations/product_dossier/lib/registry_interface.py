"""
registry_interface.py — the PD-1 <-> PD-2 join (TASK-610 follow-up, WIRED).

PD-1 (TASK-609, committed and live) built the immutable identity registry at
03_operations/product_dossier/registry/product_registry.json
(registry_ops.py): a minted, opaque `bari_pid` per served product, an alias
table (`{"type": "served_id", "value": ...}` / `{"type": "retailer_gtin",
"retailer": ..., "gtin": ...}` -> bari_pid, keyed via the SAME canonical-JSON
encoding registry_ops.canonical_json uses -- sort_keys, no spaces), a 5-state
`barcode_status` (verified / found_but_conflicting / malformed / not_found /
pending_manual_review) and a `recovered_gtin` candidate, per product.

This module is the ONLY place PD-2 reads that registry. It is read-only --
registry/ is PD-1's tree, never written here (Tripwire-1). It never guesses a
pid from a barcode or name match itself: it looks the alias up in the
registry's OWN alias table, which already excludes ambiguous aliases (a
PID_SPLIT/PID_COLLISION case is intentionally absent from that table --
registry_ops.py routed those products to pending_manual_review already), so
an absent lookup here is an honest "this registry does not resolve this
alias", never a fresh, un-adjudicated guess.

registry_available() reports whether the registry file exists (observability
+ used to distinguish "registry missing entirely" from "registry present but
this alias genuinely doesn't resolve" in downstream reason strings).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = REPO_ROOT / "03_operations" / "product_dossier" / "registry" / "product_registry.json"

PID_STATUS_UNRESOLVED = "unresolved"
PID_STATUS_RESOLVED = "resolved"

_registry_cache: Optional[dict] = None
_alias_table_cache: Optional[dict] = None
_records_by_pid_cache: Optional[dict] = None


def _canonical_json(value) -> str:
    """Must byte-for-byte match registry_ops.canonical_json's encoding
    (json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(",",
    ":"))) -- the alias table's keys were built with that exact function, so
    any drift here (spacing, key order, ensure_ascii) would silently break
    every lookup.
    """
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def registry_available() -> bool:
    """Observability only. Does not itself resolve anything."""
    return REGISTRY_PATH.is_file()


def load_registry() -> Optional[dict]:
    """Loads + caches product_registry.json once per process. Returns None
    (never raises) if the file is absent -- every caller treats that the
    same as "nothing resolves yet", never a hard failure (PD-2 must still
    build dossiers, with honest pid_status=unresolved, if the registry is
    somehow missing from a given worktree).
    """
    global _registry_cache
    if _registry_cache is None:
        if not REGISTRY_PATH.is_file():
            return None
        _registry_cache = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return _registry_cache


def _alias_table() -> dict:
    global _alias_table_cache
    if _alias_table_cache is None:
        reg = load_registry()
        _alias_table_cache = (reg.get("aliases") or {}) if reg else {}
    return _alias_table_cache


def _records_by_pid() -> dict:
    global _records_by_pid_cache
    if _records_by_pid_cache is None:
        reg = load_registry()
        products = (reg.get("products") or []) if reg else []
        _records_by_pid_cache = {p["bari_pid"]: p for p in products if p.get("bari_pid")}
    return _records_by_pid_cache


def resolve_bari_pid(alias: str, alias_type: str = "served_id") -> Optional[str]:
    """Resolves a served-id (the compiler's `provisional_key`, PD-2's only
    call site today) to a `bari_pid` via the registry's own alias table.
    Returns None -- never a fabricated pid -- when the registry is absent,
    or the alias is genuinely not present in the table (registry miss, or
    an ambiguous alias registry_ops.py deliberately excluded).
    """
    if not alias:
        return None
    table = _alias_table()
    if not table:
        return None
    key = _canonical_json({"type": alias_type, "value": alias})
    return table.get(key)


def resolve_bari_pid_by_gtin(retailer: str, gtin: str) -> Optional[str]:
    """Alternate lookup via the retailer_gtin alias shape registry_ops.py
    also writes (capture-pair keyed). Not on PD-2's primary path (served id
    resolves every product the registry knows about) but kept symmetric
    with the alias shapes actually present in the table, for a future
    caller that only has a capture pair.
    """
    if not retailer or not gtin:
        return None
    table = _alias_table()
    if not table:
        return None
    key = _canonical_json({"type": "retailer_gtin", "retailer": retailer, "gtin": gtin})
    return table.get(key)


def get_registry_record(bari_pid: str) -> Optional[dict]:
    """Full registry record for a resolved pid: {bari_pid, aliases,
    barcode_status, recovered_gtin, name_provenance, ...}. None if the pid
    is somehow absent from products[] (should not happen for a pid this
    module itself just resolved via the alias table -- defensive only).
    """
    if not bari_pid:
        return None
    return _records_by_pid().get(bari_pid)


def provisional_key(served_product: dict) -> str:
    """Deterministic, non-authoritative identity key. This is what gets
    resolved against the registry (as a served_id alias) AND is the
    dossier-filename fallback key for any product that does not resolve
    (registry miss / genuinely unresolvable) -- never a barcode-derived key
    reused as identity (the exact defect R-A of the memo diagnosed in the
    old barcode-derived ids). Uses the served product's own `id` field
    verbatim; falls back to a barcode-prefixed key only if `id` is somehow
    absent (defensive; every served product observed in this corpus carries
    `id`).
    """
    pid = served_product.get("id")
    if pid:
        return str(pid)
    bc = served_product.get("barcode")
    return f"no_id_barcode_{bc}" if bc else "no_id_no_barcode_unknown"
