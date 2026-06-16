#!/usr/bin/env python3
"""merge_copy.py — Part 3 of the Copy Engine (P29 / TASK-257 Phase 2).

Merges authored Hebrew strings into the generated page JSON (replacing
PENDING_COPY; structure untouched), then self-gates:

  (a) readability — runs integrations/clients/hebrew_readability.analyze on EVERY
      consumer string; 100% is_clean required (else non-zero exit).
  (b) full gate suite — invokes gates/run_gates.py with corpus/run/schema/
      baseline/config; all gates must PASS (G6 COPY-SAFETY included).
  (c) emits a seeded 10-card random sample into copy_sample_for_review.md.

Merge rules:
  - Only barcodes present in BOTH the page and the authored copy are written.
    Authored barcodes not on the page (e.g. a staged product) are skipped and
    listed (never injected).
  - Per product: insightLine, rowVerdict, expansion.comparisonContext,
    expansion.positiveSignals, expansion.limitingFactors.
    limitingFactors is OMITTED from expansion when the authored list is empty
    (schema: absent when no limits) — matches live granola/snacks.
  - S products additionally get s_grade_explanation (verbatim).
  - Page-level strings are written under _meta.page_copy (non-rendering carrier
    until the frontend wires them; keeps them gate-scanned and versioned).

stdlib only (+ the project's offline readability client). No OFF. No network.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "integrations", "clients"))

import hebrew_readability  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PENDING = "PENDING_COPY"


def load(path):
    return json.load(open(path, encoding="utf-8"))


def collect_product_strings(prod):
    """All consumer strings on a product (for readability scan)."""
    out = []
    for f in ("insightLine", "rowVerdict", "s_grade_explanation", "consumerTakeaway"):
        v = prod.get(f)
        if isinstance(v, str) and v and v != PENDING:
            out.append((f, v))
    exp = prod.get("expansion", {}) or {}
    for f in ("comparisonContext", "confidenceLabel", "servingNote", "bottomLine"):
        v = exp.get(f)
        if isinstance(v, str) and v and v != PENDING:
            out.append((f"expansion.{f}", v))
    for f in ("positiveSignals", "limitingFactors", "unknowns", "caveats"):
        for i, item in enumerate(exp.get(f) or []):
            if isinstance(item, str) and item:
                out.append((f"expansion.{f}[{i}]", item))
    # v3: consumerExplanation sub-fields
    ce = exp.get("consumerExplanation") or {}
    for f in ("whyRated", "context", "takeaway"):
        v = ce.get(f)
        if isinstance(v, str) and v and v != PENDING:
            out.append((f"expansion.consumerExplanation.{f}", v))
    for i, item in enumerate(ce.get("good") or []):
        if isinstance(item, str) and item and item != PENDING:
            out.append((f"expansion.consumerExplanation.good[{i}]", item))
    for i, item in enumerate(ce.get("watchOut") or []):
        if isinstance(item, str) and item and item != PENDING:
            out.append((f"expansion.consumerExplanation.watchOut[{i}]", item))
    # v3: bariInterpretation[].interpretation
    for i, entry in enumerate(prod.get("bariInterpretation") or []):
        interp = entry.get("interpretation") if isinstance(entry, dict) else None
        if isinstance(interp, str) and interp and interp != PENDING:
            out.append((f"bariInterpretation[{i}].interpretation", interp))
    # v3: bestUseCases[]
    for i, item in enumerate(prod.get("bestUseCases") or []):
        if isinstance(item, str) and item and item != PENDING:
            out.append((f"bestUseCases[{i}]", item))
    return out


def collect_page_strings(meta):
    out = []
    pc = meta.get("page_copy")
    if not pc:
        return out

    def walk(prefix, node):
        if isinstance(node, str):
            if node and node != PENDING:
                out.append((prefix, node))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(f"{prefix}[{i}]", v)
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(f"{prefix}.{k}", v)

    walk("page_copy", pc)
    return out


def merge(page, authored):
    products = page["products"]
    copy_by_bc = authored["products"]
    page_barcodes = {p["barcode"] for p in products}

    written = 0
    skipped_authored = [bc for bc in copy_by_bc if bc not in page_barcodes]
    missing_copy = []

    for prod in products:
        bc = prod["barcode"]
        c = copy_by_bc.get(bc)
        if not c:
            missing_copy.append(bc)
            continue
        prod["insightLine"] = c["insightLine"]
        prod["rowVerdict"] = c["rowVerdict"]
        if "s_grade_explanation" in c:
            prod["s_grade_explanation"] = c["s_grade_explanation"]
        exp = prod.setdefault("expansion", {})
        cexp = c.get("expansion", {})
        exp["comparisonContext"] = cexp.get("comparisonContext", "")
        exp["positiveSignals"] = list(cexp.get("positiveSignals", []))
        lim = list(cexp.get("limitingFactors", []))
        if lim:
            exp["limitingFactors"] = lim
        else:
            exp.pop("limitingFactors", None)  # absent when no limits (schema)

        # v3: merge milk-depth fields
        if "consumerTakeaway" in c:
            prod["consumerTakeaway"] = c["consumerTakeaway"]
        if "consumerExplanation" in cexp:
            exp["consumerExplanation"] = cexp["consumerExplanation"]
        if "bariInterpretation" in c:
            # Merge authored interpretations back onto the deterministic entries
            authored_interp = c["bariInterpretation"]
            existing_interp = prod.get("bariInterpretation") or []
            # Build lookup: key → authored entry
            authored_by_key = {e["key"]: e for e in authored_interp if isinstance(e, dict)}
            merged_interp = []
            for entry in existing_interp:
                if not isinstance(entry, dict):
                    merged_interp.append(entry)
                    continue
                key = entry.get("key", "")
                authored_entry = authored_by_key.get(key)
                if authored_entry:
                    # Take key/label/score/strength from deterministic (page); interpretation from authored
                    merged_entry = dict(entry)
                    merged_entry["interpretation"] = authored_entry.get("interpretation", entry.get("interpretation"))
                    merged_interp.append(merged_entry)
                else:
                    merged_interp.append(entry)
            prod["bariInterpretation"] = merged_interp
        if "bestUseCases" in c:
            prod["bestUseCases"] = list(c["bestUseCases"])

        written += 1

    # page-level strings → _meta.page_copy
    page["_meta"]["page_copy"] = authored.get("_page", {})

    return written, skipped_authored, missing_copy


def run_readability(page):
    results = []  # (location, field, text, is_clean, flags)
    for prod in page["products"]:
        bc = prod["barcode"]
        for field, text in collect_product_strings(prod):
            r = hebrew_readability.analyze(text)
            results.append((bc, field, text, r.is_clean, r.flags))
    for field, text in collect_page_strings(page["_meta"]):
        r = hebrew_readability.analyze(text)
        results.append(("_page", field, text, r.is_clean, r.flags))
    return results


def emit_sample(page, out_path, seed=2257):
    rng = random.Random(seed)
    prods = list(page["products"])
    sample = rng.sample(prods, min(10, len(prods)))
    lines = ["# Yogurts Copy — 10-Card Editorial Sample",
             f"_Seeded (seed={seed}); reproducible. {len(prods)} products on page._",
             ""]
    for p in sample:
        exp = p.get("expansion", {})
        lines.append(f"## {p['name']}  ·  {p['grade']} / {p['score']}")
        lines.append(f"- **insightLine:** {p.get('insightLine')}")
        lines.append(f"- **rowVerdict:** {p.get('rowVerdict')}")
        lines.append(f"- **comparisonContext:** {exp.get('comparisonContext')}")
        lines.append(f"- **positiveSignals:** {exp.get('positiveSignals')}")
        if "limitingFactors" in exp:
            lines.append(f"- **limitingFactors:** {exp.get('limitingFactors')}")
        if "s_grade_explanation" in p:
            lines.append(f"- **s_grade_explanation:** {p.get('s_grade_explanation')}")
        # v3 fields
        if "consumerTakeaway" in p:
            lines.append(f"- **consumerTakeaway:** {p.get('consumerTakeaway')}")
        ce = exp.get("consumerExplanation")
        if ce:
            lines.append(f"- **consumerExplanation.whyRated:** {ce.get('whyRated')}")
            lines.append(f"- **consumerExplanation.good:** {ce.get('good')}")
            lines.append(f"- **consumerExplanation.watchOut:** {ce.get('watchOut')}")
        bi = p.get("bariInterpretation")
        if bi:
            lines.append(f"- **bariInterpretation (first):** {bi[0] if bi else None}")
        buc = p.get("bestUseCases")
        if buc:
            lines.append(f"- **bestUseCases:** {buc}")
        lines.append("")
    open(out_path, "w", encoding="utf-8").write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", required=True)
    ap.add_argument("--copy", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", required=True, help="category config (corpus/run/baseline)")
    ap.add_argument("--schema", required=True)
    ap.add_argument("--sample-out", default=None)
    args = ap.parse_args()

    page = load(args.page)
    authored = load(args.copy)
    config = load(args.config)

    written, skipped_authored, missing_copy = merge(page, authored)
    print(f"Merged copy into {written}/{len(page['products'])} products.")
    if skipped_authored:
        print(f"Authored barcodes NOT on page (skipped, never injected): {skipped_authored}")
    if missing_copy:
        print(f"WARNING — page products with NO authored copy: {missing_copy}")

    # any PENDING_COPY left?
    blob = json.dumps(page, ensure_ascii=False)
    pending_remaining = blob.count(PENDING)
    print(f"PENDING_COPY remaining: {pending_remaining}")

    # write merged page
    json.dump(page, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote merged page → {args.out}")

    # (a) readability
    rr = run_readability(page)
    unclean = [r for r in rr if not r[3]]
    print(f"Readability: {len(rr) - len(unclean)}/{len(rr)} strings is_clean.")
    for bc, field, text, clean, flags in unclean:
        print(f"  NOT CLEAN — {bc} {field}: {flags} :: {text[:60]}")

    # (c) sample
    sample_out = args.sample_out or os.path.join(os.path.dirname(args.out), "copy_sample_for_review.md")
    emit_sample(page, sample_out)
    print(f"Wrote 10-card sample → {sample_out}")

    # (b) gate suite
    gates = os.path.join(REPO, "03_operations", "page_generator", "gates", "run_gates.py")
    cmd = [
        sys.executable, gates, args.out,
        "--corpus", config["corpus_dirs"][0],
        "--run", config["run_products_dir"],
        "--schema", args.schema,
        "--config", args.config,
    ]
    if config.get("baseline_json") and os.path.isfile(config["baseline_json"]):
        cmd += ["--baseline", config["baseline_json"]]
    print(f"\nRunning gate suite: {' '.join(cmd[1:])}\n")
    gate_proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(gate_proc.stdout)
    if gate_proc.stderr:
        print("GATE STDERR:", gate_proc.stderr)

    # final verdict
    ok = (pending_remaining == 0) and (len(unclean) == 0) and (gate_proc.returncode == 0) and (not missing_copy)
    print(f"\n=== SELF-GATE: {'PASS' if ok else 'FAIL'} ===")
    print(f"  pending_remaining={pending_remaining} (need 0)")
    print(f"  readability_clean={len(rr) - len(unclean)}/{len(rr)} (need all)")
    print(f"  gates_exit={gate_proc.returncode} (need 0)")
    print(f"  missing_copy={len(missing_copy)} (need 0)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
