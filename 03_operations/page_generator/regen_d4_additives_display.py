#!/usr/bin/env python3
"""
Regenerate the `d4_additives` DISPLAY field on every served comparison JSON so it
equals the engine's CURRENT detection — closing the display-vs-scoring divergence
that BARI_D4_SCORE_V1 activation exposed (the published boxes were built by an
older detect_additives_d4 and were missing contested additives like E224/E466/E171
that the live scorer penalises).

ADD-ONLY MERGE (never remove): the published boxes are RICHER than the scorer's
current detect_additives_d4 (the old display detector recognised generic E-classes,
glycerol E422, sorbic acid E200, modified starches, glazing agents, etc. that the
current scorer's detector does not). A full regen would STRIP those — a regression.
So we only APPEND engine-detected additives that are absent from the existing box
(this is where the missing contested score-drivers — E224/E466/E433/E171/E124 — get
added), each enriched with explanation_he from w2_additive_copy_v1.md. Existing
entries are preserved verbatim. Output shape (matches live schema):
    {e_number, name_he, tier, function_he, explanation_he}

Touches ONLY the `d4_additives` field. Products with no ingredient text in the BSIP1
index are LEFT UNTOUCHED. Idempotent. Never deploys; never touches git.

Usage:  python regen_d4_additives_display.py [--write]
"""
from __future__ import annotations
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "03_operations/bsip2/proto_v0/src"))

import render_fields as rf            # noqa: E402
import score_engine as se            # noqa: E402
import importlib.util                # noqa: E402

# Reuse the patch's ingredient index + config→served-file resolver (single source).
_spec = importlib.util.spec_from_file_location(
    "patch", str(HERE / "apply_d4_surgical_patch.py"))
_patch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_patch)

W2 = rf._load_w2_lookup()


# Score-eligible CONTESTED additives: these drive the D4 penalty, so their DISPLAY
# entry must agree with the engine (tier=contested) — else a product is penalised for
# an additive its own box labels neutral (the bread/cakes E471 incoherence).
import constants as _C  # noqa: E402
SCORE_ELIGIBLE_CONTESTED = {
    e for e, v in _C.GLASSBOX_W2_ADDITIVES.items()
    if v.get("tier") == "contested" and v.get("score_eligible") is True
}


# display_e_number remap: some entries display a GROUP label (e.g. E224 -> "E220–E228")
# instead of their detection key. KEY_OF maps the displayed label back to the dict key so
# the merge stays idempotent (a box already carrying the display label is not re-added).
DISPLAY_OF = {k: v["display_e_number"]
              for k, v in _C.GLASSBOX_W2_ADDITIVES.items() if v.get("display_e_number")}
KEY_OF = {disp: k for k, disp in DISPLAY_OF.items()}


def _norm_key(e_number: str) -> str:
    """Map a (possibly display-label) e_number back to its dict key."""
    return KEY_OF.get(str(e_number), str(e_number))


def _entry_explanation(key: str) -> str:
    """w2 copy keyed by dict key, falling back to the dict entry's own explanation_he."""
    return W2.get(key) or _C.GLASSBOX_W2_ADDITIVES.get(key, {}).get("explanation_he", "")


def merge_missing_entries(ing_text: str, existing: list[dict]) -> list[dict]:
    """ADD missing engine-detected additives (never remove), AND SYNC the
    name/tier/function/explanation/display-e_number of any EXISTING entry for a
    score-eligible CONTESTED additive to the engine + w2 (so a penalising additive is
    never shown as neutral or under a wrong compound name). Non-score-eligible existing
    entries are preserved verbatim (their display-tier staleness is a separate,
    non-score follow-up). Idempotent (display-label aware)."""
    existing = list(existing or [])
    if not ing_text or not ing_text.strip():
        return existing
    detected = {a.get("e_number", ""): a for a in (se.detect_additives_d4(ing_text) or [])}
    have = {_norm_key(e.get("e_number", "")) for e in existing}
    # sync existing score-eligible-contested entries to the engine value
    for e in existing:
        key = _norm_key(e.get("e_number", ""))
        if key in detected and key in SCORE_ELIGIBLE_CONTESTED:
            add = detected[key]
            ent = _C.GLASSBOX_W2_ADDITIVES.get(key, {})
            e["e_number"] = DISPLAY_OF.get(key, key)
            e["name_he"] = add.get("name_he", "")
            e["tier"] = add.get("tier", "")
            e["function_he"] = add.get("function_he", "")
            e["explanation_he"] = _entry_explanation(key)
    # append additives the box is missing
    for key, add in detected.items():
        if key in have:
            continue
        have.add(key)
        existing.append({
            "e_number": DISPLAY_OF.get(key, key),
            "name_he": add.get("name_he", ""),
            "tier": add.get("tier", ""),
            "function_he": add.get("function_he", ""),
            "explanation_he": _entry_explanation(key),
        })
    return existing


def main() -> int:
    do_write = "--write" in sys.argv
    ing = _patch._build_ingredient_index()

    served = []
    for cfg_path in sorted((HERE / "configs").glob("*.json")):
        if cfg_path.name.startswith("_generated"):
            continue
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        bj = cfg.get("baseline_json")
        if bj:
            served.append(Path(bj))

    tot_prod = tot_changed = tot_skipped = 0
    empty_expl = []        # (file, barcode, e_number) displayed with no explanation
    e224_check = []        # confirm E224 now appears where it drives a penalty
    per_file = []

    for bj in served:
        if not bj.exists():
            print(f"  SKIP (missing): {bj}")
            continue
        data = json.loads(bj.read_text(encoding="utf-8"))
        changed = skipped = 0
        for pr in data.get("products", []):
            tot_prod += 1
            bc = str(pr.get("barcode") or pr.get("id") or "")
            it = ing.get(bc, "")
            if not it:
                skipped += 1
                tot_skipped += 1
                continue
            cur = pr.get("d4_additives") or []
            cur_e = {_norm_key(e.get("e_number", "")) for e in cur}
            new_d4 = merge_missing_entries(it, cur)
            # validate every displayed additive has an explanation (incl. synced ones)
            for e in new_d4:
                if not e["explanation_he"]:
                    empty_expl.append((bj.name, bc, e["e_number"]))
                if _norm_key(e.get("e_number", "")) == "E224":   # sulphite group (now E220–E228)
                    e224_check.append((bj.name, bc))
            # safety: never remove — merged set (normalised) must be a superset of existing
            new_e = {_norm_key(e.get("e_number", "")) for e in new_d4}
            assert cur_e.issubset(new_e), f"REMOVAL detected {bj.name} {bc}"
            if cur != new_d4:
                changed += 1
                tot_changed += 1
                pr["d4_additives"] = new_d4
        per_file.append((bj.name, len(data.get("products", [])), changed, skipped))
        if do_write:
            bj.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                          encoding="utf-8")

    print(f"{'FILE':44s} {'prods':>6s} {'changed':>8s} {'no-ing':>7s}")
    for name, n, ch, sk in per_file:
        print(f"{name:44s} {n:>6d} {ch:>8d} {sk:>7d}")
    print(f"\nTOTAL products={tot_prod} changed={tot_changed} skipped(no-ingredients)={tot_skipped}")
    print(f"Displayed additives with EMPTY explanation_he: {len(empty_expl)}"
          + ("" if not empty_expl else f"  -> {empty_expl[:15]}"))
    print(f"E224 now present on {len(e224_check)} product boxes (was missing): "
          f"{sorted(set(b for _, b in e224_check))[:10]}")
    print(f"\n{'WROTE' if do_write else 'DRY-RUN (no --write)'}")
    return 1 if empty_expl else 0


if __name__ == "__main__":
    sys.exit(main())
