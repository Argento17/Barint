#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scoring_introspect.py  —  pipeline #4 ("scoring/nutrition enrichment, surface-only").

When a routine logs a SCORING-relevant signal (e.g. "CR + Yuka flagged E171 titanium
dioxide"), this does NOT touch any score. It answers the owner's two questions
DETERMINISTICALLY against Bari's own engine + corpus, then emits a review card for the
Notion queue:

  1. MODELED?    Does Bari's additive library / evidence registry already model this?
                 -> tier + cosmetic_mup + the exact registry line.
  2. IN PRODUCTS? Do any *scored* products actually carry it (d4_additives[].e_number),
                 or is the Hebrew alias merely mentioned in the data?
  3. VERDICT + the owner-facing card, including the explicit "authorize research?" ask
     when we own the rule but lack prevalence data.

It writes NO scores, NO code, NO repo files — surface only. The ONLY action it proposes
is "authorize research" (which, on approval, is the trigger for pipeline #1).

Usage:
  python scoring_introspect.py E171              # one concept by E-number or key
  python scoring_introspect.py --all             # every concept in CONCEPTS
  python scoring_introspect.py --selftest        # offline wiring proof (synthetic data)
  python scoring_introspect.py E171 --json       # machine-readable (for the Notion driver)
"""

import argparse
import json
import re
import sys
from pathlib import Path


def _rel(p):
    """Repo-relative label, with a safe fallback for paths outside the repo (tests)."""
    try:
        return str(Path(p).relative_to(REPO)).replace("\\", "/")
    except ValueError:
        return Path(p).name


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]                                   # .../01_framework/operations/insight_actions -> repo root
ADDITIVE_LIB = REPO / "01_framework" / "glass_box" / "additive_tiered_library_v1.md"
EVIDENCE_REG = REPO / "03_operations" / "bsip2" / "evidence_registry" / "bsip2_evidence_registry_v1.md"
COMPARISONS = REPO / "bari-web" / "src" / "data" / "comparisons"

# A signal -> concept spec. Seeded with the owner's worked example; the Notion driver
# (pipeline wiring) will add a concept on the fly from a Scoring/methodology row.
CONCEPTS = {
    "E171": {
        "code": "E171",
        "en": "titanium dioxide",
        "he_aliases": ["טיטניום", "דו תחמוצת הטיטניום", "דו-תחמוצת הטיטניום",
                       "תחמוצת טיטניום", "דו תחמוצת טיטניום"],
    },
}


# ----------------------------------------------------------------- modeled? (the rule)
def check_modeled(code, he_aliases, lib_path=ADDITIVE_LIB, reg_path=EVIDENCE_REG):
    """Is this additive/concept already modeled? Parse the additive library table row
    + the cosmetic_mup membership block. Falls back to an evidence-registry name hit."""
    out = {"modeled": False, "tier": None, "cosmetic_mup": None,
           "registry_line": None, "source": None}
    if lib_path.exists():
        text = lib_path.read_text(encoding="utf-8")
        # table row:  | 39 | E171 | Titanium dioxide | colorant | **contested** | True | ... |
        row = None
        for line in text.splitlines():
            cells = [c.strip() for c in line.split("|")]
            if len(cells) > 3 and re.fullmatch(rf"{re.escape(code)}", cells[2] if len(cells) > 2 else ""):
                row = line
                # tier = the **bolded** cell, if any
                m = re.search(r"\*\*([^*]+)\*\*", line)
                if m:
                    out["tier"] = m.group(1).strip()
                break
        if row:
            out["modeled"] = True
            out["registry_line"] = row.strip()
            out["source"] = _rel(lib_path)
            # cosmetic_mup membership: the True/False values are a 2-column table.
            # Find the header row carrying both, then read each following row's
            # LEFT cell (= cosmetic_mup True) vs RIGHT cell (= False).
            lines = text.splitlines()
            hdr = next((i for i, ln in enumerate(lines)
                        if "cosmetic_mup = True" in ln and "cosmetic_mup = False" in ln), None)
            if hdr is not None:
                started = False
                for ln in lines[hdr + 1:]:
                    if "|" not in ln:
                        if started:
                            break
                        continue
                    if re.fullmatch(r"\s*\|[-\s|]+\|\s*", ln):   # the |---|---| separator
                        continue
                    cells = [c.strip() for c in ln.split("|") if c.strip()]
                    started = True
                    if cells and re.search(rf"\b{re.escape(code)}\b", cells[0]):
                        out["cosmetic_mup"] = True
                        break
                    if len(cells) > 1 and re.search(rf"\b{re.escape(code)}\b", cells[1]):
                        out["cosmetic_mup"] = False
                        break
    # evidence-registry corroboration (by code or English/Hebrew name)
    if reg_path.exists():
        reg = reg_path.read_text(encoding="utf-8")
        if re.search(rf"\b{re.escape(code)}\b", reg):
            out["modeled"] = True
            out.setdefault("source", _rel(reg_path))
    return out


# ----------------------------------------------------------------- in our products?
def _walk_products(node, found, code, he_aliases, category):
    """Recursively find product objects (those carrying d4_additives) whose additive
    list contains `code`. Capture a human label for each hit."""
    if isinstance(node, dict):
        if isinstance(node.get("d4_additives"), list):
            for add in node["d4_additives"]:
                if isinstance(add, dict) and str(add.get("e_number", "")).upper() == code.upper():
                    found.append({
                        "category": category,
                        "barcode": node.get("barcode"),
                        "name": node.get("brand") or node.get("productName")
                                or node.get("name_he") or node.get("name") or "?",
                        "additive_name_he": add.get("name_he"),
                    })
        for v in node.values():
            _walk_products(v, found, code, he_aliases, category)
    elif isinstance(node, list):
        for v in node:
            _walk_products(v, found, code, he_aliases, category)


def check_products(code, he_aliases, comparisons_dir=COMPARISONS):
    """Returns (additive_hits, alias_text_mentions). additive_hits = structured presence
    in d4_additives (high confidence). alias_text_mentions = files where a Hebrew alias
    appears anywhere (low confidence, flagged for human confirm)."""
    additive_hits, alias_files = [], []
    if not comparisons_dir.exists():
        return additive_hits, alias_files
    for jf in sorted(comparisons_dir.glob("*.json")):    # top-level only -> skips archive/
        category = jf.stem
        raw = jf.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        _walk_products(data, additive_hits, code, he_aliases, category)
        if any(a and a in raw for a in he_aliases):
            alias_files.append(category)
    return additive_hits, alias_files


# ----------------------------------------------------------------- verdict + card
def assess(concept):
    code = concept["code"]
    he_aliases = concept.get("he_aliases", [])
    modeled = check_modeled(code, he_aliases)
    hits, alias_files = check_products(code, he_aliases)
    if not modeled["modeled"]:
        verdict = "NOT_MODELED"
    elif hits:
        verdict = "COVERED"
    else:
        verdict = "RULE_NO_DATA"
    return {
        "code": code, "en": concept.get("en"),
        "modeled": modeled, "product_hits": hits,
        "alias_text_mentions": alias_files, "verdict": verdict,
    }


def render_card(a):
    code, en = a["code"], a["en"] or ""
    m, hits, aliases = a["modeled"], a["product_hits"], a["alias_text_mentions"]
    L = []
    L.append(f"🔬 SCORING SIGNAL — needs your call: {code} ({en})")
    if m["modeled"]:
        bits = []
        if m["tier"]:
            bits.append(f"tier *{m['tier']}*")
        if m["cosmetic_mup"] is True:
            bits.append("cosmetic-markup additive")
        L.append(f"• Modeled? ✅ Yes — {', '.join(bits) or 'in the additive library'} "
                  f"({m['source']}).")
    else:
        L.append("• Modeled? ❌ No — not found in the additive library or evidence registry.")
    if hits:
        cats = sorted({h['category'] for h in hits})
        L.append(f"• In our products? ✅ {len(hits)} product(s) across {len(cats)} "
                 f"categor(ies): {', '.join(cats)}.")
    else:
        extra = (f" (Hebrew name appears as text in: {', '.join(aliases)} — needs human confirm)"
                 if aliases else "")
        L.append(f"• In our products? ⚠️ 0 ingredient-level hits across "
                 f"{len(list(COMPARISONS.glob('*.json')))} live shelves{extra}.")
    if a["verdict"] == "RULE_NO_DATA":
        L.append("• Gap: we own the *rule* but not the *prevalence data*.")
        L.append(f"• Your call: authorize research into {code} prevalence in Israeli "
                 f"products? [Approve → triggers pipeline #1] · [Not now]")
    elif a["verdict"] == "NOT_MODELED":
        L.append("• Gap: not modeled at all.")
        L.append(f"• Your call: authorize research + an EV-### proposal for {code}? "
                 f"[Approve] · [Not now]")
    else:
        L.append("• Status: modeled AND present in scored products — no gap. FYI only.")
    L.append("• Will NOT do automatically: move any score (tripwire).")
    return "\n".join(L)


# ----------------------------------------------------------------- selftest
def selftest():
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    lib = tmp / "lib.md"
    lib.write_text(
        "header\n"
        "| 39 | E171 | Titanium dioxide | colorant | **contested** | True | EFSA 2021 ... |\n"
        "| cosmetic_mup = True (30) | cosmetic_mup = False (16) |\n"
        "| Colors: E150, E171, E102 | Preservatives: E202 |\n"
        "cosmetic_mup = False\n", encoding="utf-8")
    comp = tmp / "comparisons"
    comp.mkdir()
    (comp / "withhit.json").write_text(json.dumps(
        {"products": [{"barcode": "111", "brand": "Test",
                       "d4_additives": [{"e_number": "E171", "name_he": "טיטניום"}]}]}),
        encoding="utf-8")
    (comp / "nohit.json").write_text(json.dumps(
        {"products": [{"barcode": "222", "brand": "Other",
                       "d4_additives": [{"e_number": "E322", "name_he": "לציטין"}]}]}),
        encoding="utf-8")
    mod = check_modeled("E171", [], lib_path=lib, reg_path=tmp / "missing.md")
    assert mod["modeled"] and mod["tier"] == "contested" and mod["cosmetic_mup"] is True, mod
    hits, _ = check_products("E171", ["טיטניום"], comparisons_dir=comp)
    assert len(hits) == 1 and hits[0]["barcode"] == "111", hits
    none, alias = check_products("E171", ["טיטניום"], comparisons_dir=tmp / "none")
    assert none == [], none
    print("SELFTEST PASS")
    return 0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("concept", nargs="?", help="E-number or CONCEPTS key, e.g. E171")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    targets = []
    if args.all:
        targets = list(CONCEPTS.values())
    elif args.concept:
        key = args.concept.upper()
        targets = [CONCEPTS.get(key, {"code": key, "en": None, "he_aliases": []})]
    else:
        ap.error("give a concept (e.g. E171), --all, or --selftest")

    results = [assess(c) for c in targets]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(render_card(r) for r in results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
