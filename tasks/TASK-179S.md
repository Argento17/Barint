---
id: TASK-179S
title: "Glass Box W2 — D4 engine wire: additive tier detector behind BARI_GLASSBOX_W2 flag"
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-04
depends_on: [TASK-179Q, TASK-179R]
blocks: [TASK-179V]
category_id: null
roadmap_impact: true
work_type: execution
---

# TASK-179S — Glass Box W2: D4 engine wire

Part of TASK-179 (Glass Box), Wave 2. Runs in parallel with TASK-179T (frontend panel) and
TASK-179U (Hebrew content). Gates TASK-179V (QA).

**No score movement in this task.** The D4 signal is emitted per-product (additive tier
findings) but does NOT feed into the headline score formula. Score movement is demand-gated
on the W2 engagement gate (TASK-179R) passing — that is a W3 decision. For W2, D4 is
*presentation-only*: the data agent wires the detector so the frontend panel has structured
additive data to render.

## Prerequisites (both CLOSED before this opens)
- `TASK-179Q` (CLOSED 2026-06-04) — `additive_prototype_set_v1.md` with 20 additives,
  tiers, and draft Hebrew explanations. Nutrition + Product D7 co-signed.
- `TASK-179R` (CLOSED 2026-06-04) — `w2_engagement_gate_spec_v1.md` with design brief.
  go_nogo_locked = true.

## Source of truth
`01_framework/glass_box/additive_prototype_set_v1.md` — the 20-additive tier sheet.
This is the ONLY tier input; do not invent tier assignments or add additives not in the
sheet. If an additive is in an ingredient string but not in the sheet, emit it as
`tier: "unclassified"` with the matched name — do NOT assign a tier.

## Scope

### Phase 1 — Build the additive lookup table in `constants.py`
Add a new constant `GLASSBOX_W2_ADDITIVES` to
`03_operations/bsip2/proto_v0/src/constants.py`.

Shape:
```python
GLASSBOX_W2_ADDITIVES: dict[str, dict] = {
    "E330": {
        "name_he": "חומצת לימון",
        "name_en": "Citric acid",
        "tier": "functional",
        "function_he": "מווסת חומציות / מונע חמצון",
    },
    "E202": { ... },
    # ... all 20 entries
}
```
Fields per entry: `e_number`, `name_he`, `name_en`, `tier`, `function_he`.
Tier values (from additive_prototype_set_v1.md §Phase 3):
`"functional"` | `"likely-neutral"` | `"dose-dependent"` | `"contested"` | `"disclosure-gap"` | `"confirmed-negative"` | `"unclassified"`.

Include ALL 20 additives from the sheet. Add a comment referencing TASK-179S and
`additive_prototype_set_v1.md`.

### Phase 2 — Add the D4 flag and detector in `score_engine.py`

Add at the flag block (after `BARI_GLASSBOX_W15`, line ~87):
```python
# TASK-179S — Glass Box W2 D4 additive tier wire.
# DEFAULT OFF → engine byte-identical. Source: additive_prototype_set_v1.md.
# No score movement; D4 signal is presentation-only for the W2 prototype.
BARI_GLASSBOX_W2 = os.environ.get("BARI_GLASSBOX_W2", "off").lower() == "on"
```

Add a `detect_additives_d4(ingredient_text: str) -> list[dict]` function:
- Scans `ingredient_text` for each of the 20 additives using:
  - E-number pattern (e.g., `E330`, `E-330`, `ה-330`)
  - Hebrew name variants from `additive_prototype_set_v1.md` (include the main
    `name_he` from constants; exact regex patterns must be added per-entry where the
    E-number alone is insufficient — e.g., "חומצת לימון" for E330)
- Applies Hebrew final-letter normalization (reuse `_DIAAS_FINAL_MAP` pattern)
- Returns a list of matched findings, one per *distinct* detected additive:
  ```python
  [
    {
      "e_number": "E330",
      "name_he": "חומצת לימון",
      "tier": "functional",
      "function_he": "מווסת חומציות / מונע חמצון",
      "match_source": "e_number" | "name_he",
    },
    ...
  ]
  ```
- Order: by first occurrence in the ingredient string (not by E-number).
- Deduplication: if the same additive is matched twice (once by E-number, once by name),
  emit it once, `match_source = "both"`.
- No findings → returns `[]`.

### Phase 3 — Wire into the main scoring path

In `score_engine.py`, at the point where the per-product result dict is assembled
(after the D5/D6 gate, before return), add:

```python
if BARI_GLASSBOX_W2:
    result["d4_additives"] = detect_additives_d4(
        signals.get("ingredient_text", "")
    )
```

`d4_additives` is purely additive to the result dict. It does NOT affect `score`,
`grade`, `gate`, or any existing field. The OFF path must leave the result dict
byte-identical to the `BARI_GLASSBOX_D5D6`-only baseline.

### Phase 4 — Add a verify script
Add `03_operations/bsip2/proto_v0/verify_glassbox_w2_off_identical.py`:
- Mirrors `verify_glassbox_off_identical.py` / `verify_glassbox_w15_off_identical.py`
- Runs the engine on the pilot corpus (hummus + maadanim) with `BARI_GLASSBOX_W2=off`
  and the baseline (no W2 flag), diffs the outputs.
- Asserts zero differences. Prints a PASS/FAIL summary.

### Phase 5 — Pilot JSON wire
After QA PASS (TASK-179V), wire the D4 signal into the pilot frontend JSONs using the
`wire_glassbox_frontend.py` pattern:
- Read engine ON output per product.
- Append `d4_additives` array to each product dict in `hummus_frontend_v4.json` and
  `maadanim_frontend_v2.json`.
- Published score/grade/glassBox fields are NEVER modified.
- This phase runs after TASK-179V (QA) passes.

## Guardrails
- `BARI_GLASSBOX_W2` OFF must be byte-identical to baseline (verified in Phase 4 + TASK-179V).
- Do NOT move any score or grade field.
- Do NOT add additives not in `additive_prototype_set_v1.md`; unclassified = `"unclassified"` tier.
- Frozen invariants (milk run_005_headpin / snack 70/B / bread provenance) untouched (no rescore).
- Evidence registry entry for D4 (EV-041) to be filed before Phase 3 ships (Nutrition owns this;
  coordinate with TASK-179U if not yet filed).

## Deliverables
1. `constants.py` — `GLASSBOX_W2_ADDITIVES` lookup table (20 entries)
2. `score_engine.py` — `BARI_GLASSBOX_W2` flag + `detect_additives_d4()` + wire
3. `verify_glassbox_w2_off_identical.py` — OFF byte-identity verification script
4. Phase 5 pilot JSON update (post-QA — coordinate with TASK-179V)

## Return block
Data returns with: (a) constants updated, (b) engine updated, (c) verify script runs PASS,
(d) `d4_additives` sample output for 3 hummus + 3 maadanim products showing tier variety.
QA (TASK-179V) runs the verify script independently before closing.
