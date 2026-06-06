"""
Task: TASK-179M
Glass Box D5/D6 -> pilot frontend JSON wiring (data-path step, go-live).

Reads the engine flag-ON pilot output (_pilot_<cat>_on.json) and writes a per-product
`glassBox` object into the LIVE pilot comparison JSON for hummus + maadanim.

CONTRACT / INVARIANTS (do not change):
  - Numbers are locked upstream (TASK-179J/179L): D5->D6 reduction -10/-20/0,
    NULL_FLOOR=30, DEMOTE_CEILING_BOUND=60. This script does NOT compute or change any
    score; it only carries the engine's already-decided ON result into the FE JSON.
  - PUBLISHED grade/score fields are NEVER modified. `glassBox` is purely additive: it is
    appended as a new key on each product dict. The frontend reads it ONLY when the
    NEXT_PUBLIC_GLASSBOX_D5D6 flag is ON; flag OFF -> existing grade renders, pages unchanged.
  - Hebrew prose is Content-owned (TASK-179K). We emit CODED gap-types only; the frontend
    maps codes -> Hebrew strings (w1_disclosure_copy_v1.md). No Hebrew strings written here.

EMITTED SHAPE (extends BariGlassBoxVM; coded-only):
  glassBox = {
    "gateState": "unconstrained" | "demote" | "withhold",
    # demote only: the gated (capped) grade/score the engine produced under the flag.
    #   With the locked numbers these equal the published value whenever the -10 cap does
    #   not cross a band boundary (the pilot case), so additivity holds.
    "gatedScore": <number|null>,        # demote only
    "gatedGrade": <"A".."E"|null>,      # demote only
    # withhold only: the null outcome.
    "withheld": true,                   # withhold only
    # demote + withhold: coded, de-duplicated disclosure-gap findings (order preserved).
    #   codes: proportions | compound | generic_additive | protein_source | missing_field
    "disclosureCodes": [ ... ]
  }
  unconstrained -> { "gateState": "unconstrained" } only (no surface).

Reproducibility: load -> add key -> dump with json.dumps(ensure_ascii=False, indent=2),
preserving each file's trailing-newline state, so all non-glassBox bytes are unchanged.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
COMPARISONS = os.path.join(ROOT, "bari-web", "src", "data", "comparisons")

# (engine ON output, live frontend JSON) per pilot category.
PILOTS = {
    "hummus": (
        os.path.join(HERE, "_pilot_hummus_on.json"),
        os.path.join(COMPARISONS, "hummus_frontend_v4.json"),
    ),
    "maadanim": (
        os.path.join(HERE, "_pilot_maadanim_on.json"),
        os.path.join(COMPARISONS, "maadanim_frontend_v2.json"),
    ),
}

VALID_CODES = {"proportions", "compound", "generic_additive", "protein_source", "missing_field"}


def dedup_preserve(codes):
    """De-duplicate while preserving first-seen order. The engine repeats e.g.
    'missing_field' once per missing field; the FE renders one calm line per gap type."""
    seen = set()
    out = []
    for c in codes:
        if c in VALID_CODES and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def build_glassbox(rec):
    gate = rec.get("gate")
    if gate == "unconstrained":
        return {"gateState": "unconstrained"}
    if gate == "demote":
        return {
            "gateState": "demote",
            "gatedScore": rec.get("score"),
            "gatedGrade": rec.get("grade"),
            "disclosureCodes": dedup_preserve(rec.get("findings", [])),
        }
    if gate == "withhold":
        return {
            "gateState": "withhold",
            "withheld": True,
            "disclosureCodes": dedup_preserve(rec.get("findings", [])),
        }
    raise ValueError(f"unexpected gate value: {gate!r}")


def process(category, engine_path, fe_path):
    with open(engine_path, encoding="utf-8") as f:
        engine = json.load(f)
    raw_before = open(fe_path, encoding="utf-8").read()
    ends_nl = raw_before.endswith("\n")
    fe = json.loads(raw_before)

    counts = {"unconstrained": 0, "demote": 0, "withhold": 0}
    missing = []
    for prod in fe["products"]:
        pid = prod["id"]
        rec = engine.get(pid)
        if rec is None:
            missing.append(pid)
            continue
        # additive: published score/grade fields are left untouched; we only append glassBox.
        prod["glassBox"] = build_glassbox(rec)
        counts[prod["glassBox"]["gateState"]] += 1

    out = json.dumps(fe, ensure_ascii=False, indent=2)
    if ends_nl:
        out += "\n"
    with open(fe_path, "w", encoding="utf-8") as f:
        f.write(out)

    return counts, missing


if __name__ == "__main__":
    for cat, (eng, fe) in PILOTS.items():
        counts, missing = process(cat, eng, fe)
        print(f"[{cat}] wrote glassBox -> {os.path.basename(fe)}")
        print(f"  gateState counts: {counts}")
        if missing:
            print(f"  WARNING: {len(missing)} FE ids not in engine output (no glassBox): {missing[:5]}")
        else:
            print("  all FE products matched an engine record")
