"""
registry_interface.py — documented STUB for the PD-1 identity-registry join.

PD-2 (this compiler, TASK-610) is explicitly scoped as REGISTRY-INDEPENDENT.
TASK-609 (PD-1) is building the real identity registry
(03_operations/product_dossier/registry/product_registry.json — a minted,
opaque, immutable `bari_pid` + alias table + 5-state barcode adjudication +
`recovered_gtin` candidates, per STF memo `2026-07-11_product-dossier-
architecture.md` §3 R-A/R-B). Per the PD-2 delegation spec: "build against
the MEMO's documented registry shape, NOT PD-1's live output, which doesn't
exist yet [in this worktree]" and "leave a clean documented interface stub;
PD-1 returns first, then a follow-up wires it."

Everything in this module is intentionally inert:
  - resolve_bari_pid() always returns None.
  - registry_available() reports whether registry/product_registry.json
    exists on disk (for observability only — its presence does NOT change
    any behavior in this module; the join is wired in a follow-up task).
  - provisional_key() is the ONLY identity key this compiler uses today. It
    is the served frontend JSON's own `id` field verbatim (e.g.
    "bsip1_cereal_5010029000061") — never barcode-derived-and-reused as a
    dedup key, so a future re-key to `bari_pid` is a pure rename of the
    dossier file, not a re-adjudication of identity (the exact defect R-A
    of the memo diagnosed in the old barcode-derived ids).

Follow-up (NOT this task): once PD-1's registry.json is verified live,
replace resolve_bari_pid()'s body with a real alias lookup (never a barcode
guess -- that would bypass PD-1's collision/split adjudication), re-key
dossiers/{key}.json -> dossiers/{bari_pid}.json, and flip
generation.pid_status from "unresolved_pending_registry_join" to "resolved".
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = REPO_ROOT / "03_operations" / "product_dossier" / "registry" / "product_registry.json"

PID_STATUS_UNRESOLVED = "unresolved_pending_registry_join"
PID_STATUS_RESOLVED = "resolved"  # not reachable yet -- reserved for the follow-up


def registry_available() -> bool:
    """Observability only. Does not change resolve_bari_pid's behavior."""
    return REGISTRY_PATH.is_file()


def resolve_bari_pid(alias: str, alias_type: str = "served_id") -> Optional[str]:
    """Always returns None in PD-2. Never guesses a pid from a barcode or name
    match -- that is precisely the un-adjudicated collision risk the registry
    (PD-1) exists to prevent. Real implementation lands in a follow-up task
    once TASK-609 is verified complete.
    """
    return None


def provisional_key(served_product: dict) -> str:
    """Deterministic, non-authoritative identity key used ONLY until a real
    bari_pid exists. Uses the served product's own `id` field verbatim.
    Falls back to a barcode-prefixed key only if `id` is somehow absent
    (defensive; every served product observed in this corpus carries `id`).
    """
    pid = served_product.get("id")
    if pid:
        return str(pid)
    bc = served_product.get("barcode")
    return f"no_id_barcode_{bc}" if bc else "no_id_no_barcode_unknown"
