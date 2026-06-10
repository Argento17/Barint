"""
TASK-234 (RT-7) — Reconcile the BSIP1 nova_proxy contradiction corpus-wide.

Finding: BSIP1 stored `nova_proxy` = the RAW OFF nova_group (often 4), but the scoring
engine independently INFERS its own NOVA level (infer_nova) which is the value that actually
scores and is published. For the beet cracker (7290112968807) BSIP1 said nova_proxy=4 with a
15-item ingredient list, while the trace + published record showed NOVA-3 — an internal
contradiction within the product's own provenance chain (RT-7). Five products carry this
raw-OFF-vs-engine mismatch.

Resolution (no scoring-engine change; the engine already infers its own NOVA and that value
is unchanged): make each BSIP1 record internally consistent by
  - preserving the raw OFF value under `nova_group_off_raw` (provenance, not used for scoring),
  - setting `nova_proxy` to the engine-inferred level (the authoritative scored/published value),
  - logging a data_corrections entry.
This removes the "BSIP1 says X, published says Y" contradiction the red-team flagged, without
touching any score (engine NOVA was already the published value).
"""
import json, sys, os, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ["BARI_RECAL_P0"] = "on"
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")

from input_loader import load_batch  # noqa: E402
from signal_extractor import extract_signals  # noqa: E402
from router_v2 import classify_category  # noqa: E402
from nova_proxy import infer_nova  # noqa: E402

BSIP1 = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")


def main():
    batch = {p.get("barcode"): p for p in load_batch(BSIP1)}
    fixed = []
    for bc, p in batch.items():
        f = BSIP1 / f"bsip1_snack_{bc}.json"
        rec = json.loads(f.read_text("utf-8"))
        raw_off = rec.get("nova_proxy")
        if raw_off is None:
            continue
        sig = extract_signals(p)
        cat = classify_category(p)
        l3 = sig["L3_inferred_classifications"]
        eng = infer_nova(p, l3)["nova_level"]
        if raw_off == eng:
            continue
        # already reconciled?
        if rec.get("nova_group_off_raw") is not None and rec.get("nova_proxy") == eng:
            continue
        rec["nova_group_off_raw"] = raw_off
        rec["nova_proxy"] = eng
        rec.setdefault("inferred_fields", [])
        if "nova_proxy" not in rec["inferred_fields"]:
            rec["inferred_fields"].append("nova_proxy")
        rec.setdefault("data_corrections", []).append({
            "field": "nova_proxy",
            "old_value": raw_off,
            "new_value": eng,
            "reason": (f"RT-7 reconciliation: stored nova_proxy was the RAW OFF nova_group "
                       f"({raw_off}); the scoring engine infers and publishes NOVA-{eng} for "
                       f"this product (the value that actually scores). Raw OFF value preserved "
                       f"as nova_group_off_raw (provenance only). No score change: engine NOVA "
                       f"was already the published value."),
            "task": "TASK-234",
            "corrected_at_source": "engine infer_nova (authoritative scored NOVA)",
        })
        f.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        fixed.append((bc, raw_off, eng, rec["canonical_name_he"][:25]))

    print("RT-7 nova reconciliation:")
    for bc, r, e, n in fixed:
        print(f"  {bc}: nova_proxy {r} -> {e} (raw OFF kept as nova_group_off_raw)  {n}")
    print(f"reconciled: {len(fixed)} products")


if __name__ == "__main__":
    main()
