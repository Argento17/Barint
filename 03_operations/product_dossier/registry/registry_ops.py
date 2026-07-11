#!/usr/bin/env python3
"""Build the Product Dossier identity registry from immutable input projections.

``bari_pid`` is ``bari_`` plus the first 24 hexadecimal characters of SHA-256
over a canonical JSON tuple ``["bari-pid-v1", shelf, served_id, verbatim_name]``.
It is deliberately opaque and never incorporates a barcode.  The tuple contains
the stable served/native key and its shelf, so adding another product cannot alter
an existing PID.  A 96-bit digest prefix makes accidental collisions negligibly
unlikely; should one nevertheless occur, this writer allocates distinct
domain-separated digest PIDs and marks every affected record for manual review.

This module is the only registry writer.  It reads only served comparison JSONs,
the capture manifest, and explicit TASK-602 reconciliation tables.  It never
reads Open Food Facts or observations directories, and writes only below this
module's registry directory.  Names are used transiently to mint the PID but are
not copied to the registry: the stored name reference is a provenance pointer.

Every ``malformed``-status record also carries an additive ``barcode_reason``
sub-classification (TASK-613): ``non_gtin_retailer_sku`` for a served barcode
that fails GTIN checksum/length but is a genuine, retailer-native SKU/PLU that
resolves to itself; ``truncated_or_invalid`` for a served barcode that is a true
truncation of a different, longer GTIN or is recorded as genuinely unresolvable;
``unclassified`` where no committed TASK-602 reconciliation evidence covers that
barcode value at all. The 5-state ``barcode_status`` enum is unchanged by this --
``barcode_reason`` is additive, never a replacement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
REGISTRY_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = REGISTRY_DIR / "product_registry.json"
COMPARISONS_DIR = REPO_ROOT / "bari-web" / "src" / "data" / "comparisons"
MANIFEST_PATH = REPO_ROOT / "03_operations" / "bsip0" / "manifest" / "capture_manifest.json"
TASK602_ROOT = REPO_ROOT / "02_products"
VALID_GTIN_LENGTHS = {8, 12, 13}
STATUSES = ("verified", "found_but_conflicting", "malformed", "not_found", "pending_manual_review")
BARCODE_REASONS = ("non_gtin_retailer_sku", "truncated_or_invalid", "unclassified")


def assert_write_boundary(path: Path) -> None:
    """Reject every write target outside the registry directory (Tripwire-1)."""
    resolved = path.resolve()
    root = REGISTRY_DIR.resolve()
    if root != resolved and root not in resolved.parents:
        raise ValueError(f"registry writer may write only below {root}: {resolved}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def gtin_is_valid(value: Any) -> bool:
    """Return whether a string is a valid EAN-8, UPC-A, or EAN-13 GTIN."""
    if not isinstance(value, str) or len(value) not in VALID_GTIN_LENGTHS or not value.isascii() or not value.isdigit():
        return False
    total = sum(int(char) * (3 if index % 2 == 0 else 1) for index, char in enumerate(value[-2::-1]))
    return (10 - total % 10) % 10 == int(value[-1])


def barcode_like(value: Any) -> bool:
    return isinstance(value, str) and value.isascii() and value.isdigit() and bool(value)


def shelf_for(source_file: Path, document: dict[str, Any]) -> str:
    # Metadata category is the durable shelf label; filename is a safe fallback.
    category = document.get("_meta", {}).get("category") or document.get("category")
    return str(category) if category is not None else source_file.stem.split("_frontend_")[0]


def pid_for(shelf: str, served_id: str, name: str, domain: str = "bari-pid-v1") -> str:
    payload = canonical_json([domain, shelf, served_id, name]).encode("utf-8")
    return "bari_" + hashlib.sha256(payload).hexdigest()[:24]


def served_products() -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    for source_file in sorted(COMPARISONS_DIR.glob("*.json")):
        document = json.loads(source_file.read_text(encoding="utf-8"))
        if not isinstance(document.get("products"), list):
            continue  # red-team ledgers are not served product shelves.
        shelf = shelf_for(source_file, document)
        for index, product in enumerate(document["products"]):
            if not isinstance(product, dict) or not isinstance(product.get("id"), str) or not isinstance(product.get("name"), str):
                raise ValueError(f"invalid served product identity at {source_file}:{index}")
            products.append({
                "shelf": shelf,
                "source_file": source_file.relative_to(REPO_ROOT).as_posix(),
                "locator": f"/products/{index}/name",
                "served_id": product["id"],
                "name": product["name"],
                "barcode": product.get("barcode"),
            })
    return products


def manifest_by_gtin() -> dict[str, list[dict[str, str]]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    records = manifest.get("records")
    if not isinstance(records, list):
        raise ValueError("capture manifest has no records list")
    result: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in records:
        gtin, retailer = record.get("gtin"), record.get("retailer")
        if isinstance(gtin, str) and isinstance(retailer, str):
            result[gtin].append({"retailer": retailer, "gtin": gtin})
    return {gtin: sorted(entries, key=lambda entry: (entry["retailer"], entry["gtin"])) for gtin, entries in result.items()}


def recovered_gtins() -> dict[str, set[str]]:
    """Read only explicit old-to-new GTIN mappings from committed TASK-602 tables.

    Capture outputs that merely contain a current barcode are intentionally ignored:
    without an explicit old/served barcode mapping they are not reconciliation evidence.
    """
    mappings: dict[str, set[str]] = defaultdict(set)
    # "barcode" is the served short/truncated code as recorded in the TASK-602
    # rescrape row itself (batch2 yogurt-drinkable schema); "true_gtin_discovered"
    # is that same row's recovered true GTIN (see _classify_reconciliation_row
    # docstring). Both are read literally -- never guessed or invented.
    old_keys = {"served_barcode", "old_barcode", "truncated_barcode", "source_barcode", "barcode"}
    new_keys = {"recovered_gtin", "resolved_gtin", "true_gtin", "resolved_barcode", "true_gtin_discovered"}
    for path in sorted(TASK602_ROOT.rglob("*")):
        if "task602" not in path.as_posix().lower() or path.suffix.lower() != ".json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows = data if isinstance(data, list) else data.get("records", []) if isinstance(data, dict) else []
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            old = next((row[key] for key in old_keys if isinstance(row.get(key), str)), None)
            new = next((row[key] for key in new_keys if isinstance(row.get(key), str)), None)
            if isinstance(old, str) and isinstance(new, str) and gtin_is_valid(new):
                mappings[old].add(new)
    return mappings


def _classify_reconciliation_row(row: dict[str, Any], served: str) -> str | None:
    """Read one TASK-602 batch record's own literal verdict for a non-GTIN served
    barcode. Returns None when the row carries no usable signal (caller falls
    back to ``unclassified``). Never infers beyond what the row states.

    Schemas observed across batches (each read literally, not guessed):
      - batch5 canonical shelves: flat ``barcode_class`` in
        {"benign_retailer_sku", "true_truncation"}.
      - batch2 yogurt-drinkable: ``true_gtin_discovered`` populated with a GTIN
        that differs from the served value -> true truncation.
      - batch3 bread/chocolate: nested ``barcode_reconciliation.resolution_method``
        -- any non-empty method here resolved the served value to *itself*
        (never to a different discovered GTIN in these batches), so it is benign.
      - batch4 cheese/hard_cheeses: flat ``is_valid_gtin_served`` + top-level
        ``resolution_method`` on a scraped row -- same "resolves to itself" case.
      - any row explicitly recorded as unresolved after a full retailer sweep
        (status other than "scraped") is a genuine unresolvable code.
    """
    barcode_class = row.get("barcode_class")
    if barcode_class == "benign_retailer_sku":
        return "non_gtin_retailer_sku"
    if barcode_class == "true_truncation":
        return "truncated_or_invalid"

    true_gtin = row.get("true_gtin_discovered")
    if isinstance(true_gtin, str) and true_gtin != served:
        return "truncated_or_invalid"

    reconciliation = row.get("barcode_reconciliation")
    if isinstance(reconciliation, dict) and isinstance(reconciliation.get("resolution_method"), str) and reconciliation["resolution_method"]:
        return "non_gtin_retailer_sku"

    if (
        row.get("is_valid_gtin_served") is False
        and isinstance(row.get("resolution_method"), str)
        and row.get("resolution_method")
        and row.get("status") == "scraped"
    ):
        return "non_gtin_retailer_sku"

    if row.get("status") not in (None, "scraped"):
        return "truncated_or_invalid"  # explicitly recorded as unresolved, not silently dropped

    return None


def barcode_reconciliation_reasons() -> dict[str, str]:
    """Classify every non-GTIN served barcode found in committed TASK-602 batch
    files as ``non_gtin_retailer_sku`` (genuine retailer-native SKU/PLU that
    resolves to itself) or ``truncated_or_invalid`` (resolves to a different,
    longer GTIN, or is recorded as genuinely unresolvable). A barcode value with
    conflicting evidence across files is intentionally left out of this table --
    it falls back to the ``unclassified`` default rather than being guessed.
    """
    votes: dict[str, set[str]] = defaultdict(set)
    for path in sorted(TASK602_ROOT.rglob("*")):
        if "task602" not in path.as_posix().lower() or path.suffix.lower() != ".json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows = data.get("records") if isinstance(data, dict) else data if isinstance(data, list) else None
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            served = row.get("barcode") if isinstance(row.get("barcode"), str) else row.get("served_barcode")
            if not isinstance(served, str) or gtin_is_valid(served):
                continue  # only non-GTIN served values are in scope for this split
            reason = _classify_reconciliation_row(row, served)
            if reason is not None:
                assert reason in BARCODE_REASONS
                votes[served].add(reason)
    return {barcode: next(iter(reasons)) for barcode, reasons in votes.items() if len(reasons) == 1}


def build_registry() -> dict[str, Any]:
    manifest = manifest_by_gtin()
    recovered = recovered_gtins()
    barcode_reasons = barcode_reconciliation_reasons()
    source_products = served_products()
    pid_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for product in source_products:
        product["bari_pid"] = pid_for(product["shelf"], product["served_id"], product["name"])
        product["identity_tuple"] = (product["shelf"], product["served_id"], product["name"])
        pid_groups[product["bari_pid"]].append(product)
    # A product present verbatim in two served JSON versions is one real product,
    # not a collision.  Preserve its primary provenance pointer and mint one PID.
    entities: list[dict[str, Any]] = []
    collision_products: set[int] = set()
    for group in pid_groups.values():
        identity_tuples = {product["identity_tuple"] for product in group}
        if len(identity_tuples) == 1:
            entities.append(sorted(group, key=lambda row: row["source_file"])[0])
        else:
            collision_products.update(id(product) for product in group)
            for position, product in enumerate(sorted(group, key=lambda row: (row["source_file"], row["served_id"]))):
                product["bari_pid"] = pid_for(product["shelf"], product["served_id"], product["name"], f"bari-pid-v1-collision-{position}")
                entities.append(product)

    alias_claims: dict[str, list[dict[str, Any]]] = defaultdict(list)
    records: list[dict[str, Any]] = []
    for product in entities:
        served = product["barcode"] if isinstance(product["barcode"], str) else None
        recovered_candidates = sorted(recovered.get(served, set())) if served is not None else []
        valid_values = set()
        if gtin_is_valid(served):
            valid_values.add(served)
        valid_values.update(recovered_candidates)
        capture_aliases = []
        for gtin in sorted(valid_values):
            capture_aliases.extend(manifest.get(gtin, []))
        aliases = [{"type": "served_id", "value": product["served_id"]}]
        # Today's served id is the legacy BSIP1 id; retain type once, not a duplicate alias.
        for capture in capture_aliases:
            aliases.append({"type": "retailer_gtin", "retailer": capture["retailer"], "gtin": capture["gtin"]})
        for alias in aliases:
            key = canonical_json(alias)
            alias_claims[key].append(product)
        status = "not_found"
        if served is not None:
            if barcode_like(served) and not gtin_is_valid(served):
                status = "malformed"
            elif gtin_is_valid(served):
                status = "verified" if manifest.get(served) else "pending_manual_review"
            else:
                status = "malformed"
        if len(valid_values) >= 2 or (recovered_candidates and served != recovered_candidates[0]):
            status = "found_but_conflicting"
        barcode_reason = barcode_reasons.get(served, "unclassified") if status == "malformed" and served is not None else None
        records.append({
            "bari_pid": product["bari_pid"],
            "aliases": aliases,
            "barcode_status": status,
            "barcode_reason": barcode_reason,
            "recovered_gtin": recovered_candidates[0] if len(recovered_candidates) == 1 else None,
            "name_provenance": {"source_file": product["source_file"], "locator": product["locator"]},
            "_collision": id(product) in collision_products,
        })

    ambiguous_product_ids = {id(product) for claims in alias_claims.values() if len({p["bari_pid"] for p in claims}) > 1 for product in claims}
    source_to_record = {record["bari_pid"]: record for record in records}
    for product in entities:
        record = source_to_record[product["bari_pid"]]
        if record.pop("_collision"):
            record["barcode_status"] = "pending_manual_review"
            record["barcode_reason"] = None
            record["review_reason"] = "PID_COLLISION"
        if id(product) in ambiguous_product_ids:
            record["barcode_status"] = "pending_manual_review"
            record["barcode_reason"] = None
            record["review_reason"] = "PID_SPLIT"

    alias_table: dict[str, str] = {}
    for key, claims in sorted(alias_claims.items()):
        pids = sorted({product["bari_pid"] for product in claims})
        if len(pids) == 1:
            alias_table[key] = pids[0]
    return {
        "schema": "bari_product_registry_v1",
        "pid_scheme": "sha256-96:bari-pid-v1:[shelf,served_id,verbatim_name]",
        "inputs": {
            "served_comparisons": "bari-web/src/data/comparisons/*.json",
            "capture_manifest": "03_operations/bsip0/manifest/capture_manifest.json",
            "task602_reconciliation_scope": "02_products/**/bsip0_outputs/task602*",
            "task602_barcode_reason_scope": "02_products/**/bsip0_outputs/task602* (barcode_class / barcode_reconciliation / is_valid_gtin_served+resolution_method / true_gtin_discovered fields)",
        },
        "products": sorted(records, key=lambda record: record["bari_pid"]),
        "aliases": alias_table,
    }


def write_registry(path: Path = OUTPUT_PATH) -> bytes:
    assert_write_boundary(path)
    payload = (json.dumps(build_registry(), ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return payload


def selftest() -> None:
    assert gtin_is_valid("7290016245325")
    assert not gtin_is_valid("7290016245326")
    assert not gtin_is_valid("123456")

    # barcode_reason classification logic, exercised on synthetic rows so the
    # assertions hold regardless of future corpus/reconciliation-file churn.
    assert _classify_reconciliation_row({"barcode_class": "benign_retailer_sku"}, "12345") == "non_gtin_retailer_sku"
    assert _classify_reconciliation_row({"barcode_class": "true_truncation"}, "12345") == "truncated_or_invalid"
    assert _classify_reconciliation_row({"true_gtin_discovered": "7290000012345"}, "12345") == "truncated_or_invalid"
    assert _classify_reconciliation_row({"true_gtin_discovered": "12345"}, "12345") is None  # discovered == served: no truncation signal
    assert _classify_reconciliation_row(
        {"barcode_reconciliation": {"resolution_method": "direct_by_served_short_code_on_shufersal_p_url_NAME_VERIFIED"}}, "12345"
    ) == "non_gtin_retailer_sku"
    assert _classify_reconciliation_row(
        {"is_valid_gtin_served": False, "resolution_method": "name_match_overlap_1.00", "status": "scraped"}, "12345"
    ) == "non_gtin_retailer_sku"
    assert _classify_reconciliation_row({"status": "NOT_FOUND"}, "12345") == "truncated_or_invalid"
    assert _classify_reconciliation_row({}, "12345") is None

    reasons = barcode_reconciliation_reasons()
    assert reasons, "expected non-empty TASK-602 barcode reconciliation evidence"
    assert set(reasons.values()) <= set(BARCODE_REASONS)

    # TASK-618: recovered_gtins() must read the actual committed batch-2
    # yogurt-drinkable field names -- served "barcode" (short/truncated code)
    # paired with "true_gtin_discovered" on the SAME row -- and nothing else.
    recovered = recovered_gtins()
    expected_recoveries = {
        "4068035": "7290004068035",
        "55336": "7290000055336",
        "58030": "7290000058030",
    }
    for served, true_gtin in expected_recoveries.items():
        assert recovered.get(served) == {true_gtin}, f"expected {served} -> {{{true_gtin}}}, got {recovered.get(served)}"

    registry = build_registry()
    for record in registry["products"]:
        assert record["barcode_reason"] in BARCODE_REASONS or record["barcode_reason"] is None
        if record["barcode_status"] == "malformed":
            assert record["barcode_reason"] in BARCODE_REASONS, "every malformed record must carry a barcode_reason"
        else:
            assert record["barcode_reason"] is None, "barcode_reason is additive to malformed only"

    # TASK-618: exactly the 3 genuine yogurt-drinkable truncations recover their
    # true GTIN and flip malformed -> found_but_conflicting; nothing else moves.
    expected_transitions = {
        "bsip1_yogurt_4068035": "7290004068035",
        "bsip1_yogurt_55336": "7290000055336",
        "bsip1_yogurt_58030": "7290000058030",
    }
    seen_served_ids: set[str] = set()
    for record in registry["products"]:
        for alias in record["aliases"]:
            if alias.get("type") == "served_id" and alias.get("value") in expected_transitions:
                seen_served_ids.add(alias["value"])
                expected_gtin = expected_transitions[alias["value"]]
                assert record["barcode_status"] == "found_but_conflicting", (
                    f"{alias['value']} expected found_but_conflicting, got {record['barcode_status']}"
                )
                assert record["recovered_gtin"] == expected_gtin, (
                    f"{alias['value']} expected recovered_gtin {expected_gtin}, got {record['recovered_gtin']}"
                )
                assert record["barcode_reason"] is None, "found_but_conflicting is not malformed; barcode_reason must be None"
    assert seen_served_ids == set(expected_transitions), f"expected all 3 target served_ids present, saw {seen_served_ids}"

    first, second = canonical_json(build_registry()), canonical_json(build_registry())
    assert first == second, "registry build is not deterministic"
    assert_write_boundary(OUTPUT_PATH)
    try:
        assert_write_boundary(COMPARISONS_DIR / "forbidden.json")
    except ValueError:
        pass
    else:
        raise AssertionError("write-boundary assertion did not reject served JSON")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--check", action="store_true", help="fail if the committed registry differs from the rebuild")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        print("selftest: PASS")
        return
    payload = (json.dumps(build_registry(), ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if args.check:
        if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_bytes() != payload:
            raise SystemExit("registry check failed: rebuild differs from product_registry.json")
        print("registry check: PASS")
        return
    write_registry()
    print(f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
