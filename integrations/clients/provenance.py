"""Provenance envelope for externally-sourced data (TASK-170 follow-up).

Every record an ingestion client returns carries a `Provenance` stamp so QA can trace it
(source + fetch date) and so external data cannot silently become a scoring input. The
contract the four-agent review converged on:

  - source              which client/feed produced it (e.g. "open_food_facts",
                        "il_prices:laibcatalog:7290696200003", "il_gov_data:imported_foods")
  - source_id           the natural key at that source (barcode, dsld_id, resource_id, ...)
  - source_url          where it came from (for replay / audit)
  - fetched_at          ISO-8601 UTC, stamped at fetch time
  - client_version      the client's version constant (schema-drift guard)
  - verification_status ALWAYS born "candidate". A freshly-fetched external value is never
                        "verified" — that word means *cleared by BSIP0/QA for a scored
                        corpus*, not *the client reached the source*. Only the (future)
                        admission gate promotes candidate → verified. This split is the
                        firewall: the engine reads in-house labels; external data informs
                        calibration but is quarantined from scoring until promoted.

This module is data-only — it does not fetch, gate, or promote. Read-only by nature.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

CANDIDATE = "candidate"
VERIFIED = "verified"  # set only by the admission gate (not built here), never at fetch


def now_iso() -> str:
    """Current time as ISO-8601 UTC (second precision)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Provenance:
    source: str
    source_id: str | None = None
    source_url: str | None = None
    fetched_at: str = field(default_factory=now_iso)
    client_version: str = "unknown"
    verification_status: str = CANDIDATE

    def as_dict(self) -> dict:
        return {
            "source": self.source,
            "source_id": self.source_id,
            "source_url": self.source_url,
            "fetched_at": self.fetched_at,
            "client_version": self.client_version,
            "verification_status": self.verification_status,
        }


def stamp(source: str, source_id: str | None = None, source_url: str | None = None,
          client_version: str = "unknown") -> Provenance:
    """Build a candidate-status provenance stamp at fetch time."""
    return Provenance(source=source, source_id=source_id, source_url=source_url,
                      client_version=client_version)
