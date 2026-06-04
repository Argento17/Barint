**Task:** TASK-179D

# Bari Glass Box — D5 (Transparency) + D6 (Confidence) Rule Specification (v1)

**Status:** SPEC + DRAFT EVIDENCE-REGISTRY ENTRIES. No engine code, no frontend code, no
score movement. Everything specified here ships behind a flag (`BARI_GLASSBOX_D5D6`, default
OFF); with the flag OFF the engine output and the golden/frozen runs MUST be 0-diff vs today.
All numeric thresholds in §2 are **PROPOSALS pending Product D7 co-sign** before Data builds.
This doc is precise enough for the Data Agent to implement D5 + D6 without re-deriving anything.

**Author:** Nutrition Agent · **Date:** 2026-06-04 · **Wave:** TASK-179, Wave 1, step 1
**Reads-first (binding):**
- `01_framework/glass_box/six_dimension_contract_v1.md` — the contract. Governing here: §D5,
  §D6, §2.6 (compose-then-gate), §2.7 (uncertainty-ladder map), and **§5.0 RESOLUTIONS
  (DEC-006, owner-ratified 2026-06-04)**.
- `research/glass_box/engine_enrichment_frameworks_scoping_v1.md` (179A) — disclosure-gap
  observations; "real panels live in `02_products\*\...bsip0_raw*.json`, not the curated web JSONs."
- `01_framework/bsip2_framework/confidence_framework.md` — the substrate D6 extends.
- `03_operations/bsip2/proto_v0/src/score_engine.py` (`compute_confidence`, Stage 9 ceiling,
  data-sufficiency gate) + `constants.py` (`CONFIDENCE_LOW_CEILING=75`,
  `CONFIDENCE_INSUFFICIENT_CEILING=50`).

**Binding governance rulings honored exactly (DEC-006, contract §5.0):**
- **Q2 — D5 NEVER moves the headline grade on its own axis.** Disclosure gaps act ONLY through
  D6 (confidence → demote + a visible `ניתוח חלקי` flag) and annotation. D5 is scored on its own
  axis *as a disclosure profile*, but that profile **feeds D6**; it does **not** deduct grade
  points. No intent attribution ever ("לא צוין"/"לא ניתן לאמת"; never "היצרן מסתיר").
- **Q1 — D6 is conservative-to-demote, reluctant-to-withhold.** Demote + flag carries the
  normal partial-disclosure case; `לא נוקד` (withhold→null) is reserved for a genuine
  floor-of-observability failure. *Buy coverage over silence.*

---

## 0. What this spec changes (and what it does not)

D5 and D6 are buildable today against the existing scraped BSIP0 panel and the existing
`compute_confidence` machinery — no new BULK library (179A R1). This spec does three things:

1. **D5 (new):** a deterministic detector over the raw BSIP0 ingredient panel that emits a
   structured **disclosure profile** (which gap types fired, with spans) and a **disclosure-
   completeness band** (D5-band). The band is an *input to D6 and an annotation source only*.
2. **D6 (extend, not reinvent):** add the D5-band as a named confidence input alongside the
   existing missing-field / suspicious-pattern / classification reductions, and extend today's
   ceiling-only outcome to a three-state gate: **`unconstrained · demote · withhold(→null)`**.
   The existing `CONFIDENCE_LOW_CEILING`/`CONFIDENCE_INSUFFICIENT_CEILING` ceilings are the
   *seed* of `demote`; the new behavior is `withhold(→null)` below a floor of observability.
3. **Flag + EV discipline:** all of the above is gated by `BARI_GLASSBOX_D5D6` (OFF =
   byte-identical), and every threshold is bound by a DRAFT EV-### (§3) pending Product co-sign.

**It does NOT:** deduct grade points for opacity (Q2), attribute intent, add a new grade scale,
touch frozen invariants, or call any external API at score time.

---

## 1. D5 — Disclosure-Gap Taxonomy + Detector Spec

### 1.1 Input surface (what the detector reads)

The detector runs over the **raw BSIP0 panel** — specifically the `ingredients_raw` string and
the disclosed `nutrition` / `nutrition_raw_source` fields of the per-product object in
`02_products\*\...bsip0_raw*.json` (NOT the curated web JSONs). Confirmed field names from the
maadanim run (`maadanim_bsip0_raw_20260602*.json`) and hummus (`observations_bsip0/shufersal/P_*.json`):
`ingredients_raw` (Hebrew ingredient string, may contain trailing nutrition-table bleed),
`ingredients_language`, `nutrition{...}`, `nutrition_raw_source.rows[]`.

**Pre-processing (deterministic, Data implements):**
- **P1 — Strip the nutrition-table bleed.** Real `ingredients_raw` strings append the
  `ערכים תזונתיים …` panel text (observed in every maadanim/hummus sample). Truncate the
  ingredient string at the first occurrence of `ערכים תזונתיים` (and the disclaimer
  `הנתונים המדויקים…`) before any gap detection. Everything after that anchor is not ingredients.
- **P2 — Normalize Hebrew final-letter + whitespace.** Collapse internal `\n`, normalize
  final/medial forms (mem ם/מ, nun ן/נ, etc. — same Hebrew final-letter trap as EV-029) and
  spurious spaces inside tokens (observed: `אצסולפאם k`, `קסנטאן גא ם`, `סיבים תזותיים`).
  Detection patterns MUST match on the normalized form.
- **P3 — Empty / absent panel (TOKEN-AWARE rule).** A panel is **absent** only when, after P1,
  it is blank/whitespace OR it contains **no coherent ingredient token** — where a coherent token
  is a run of **≥2 Hebrew letters** (i.e. an actual ingredient word, not stray digits, punctuation,
  or single orphan letters). A character-length cutoff alone is **wrong** and is explicitly NOT
  used: a clean single-ingredient whole-food panel can be very short (`אגוזי מלך` = 8 chars,
  `שקדים` = 5 chars, `גרגרי חומוס מבושלים`), and such panels are *maximally* transparent, not
  absent. So:
  - **Present** (run D5; e.g. resolves to `single_ingredient=true` → **full** band): any panel with
    ≥1 coherent ≥2-letter ingredient token after P1 — including very short single-ingredient ones.
  - **Absent** (do NOT run D5 gap detection): blank/whitespace, or only digits/punctuation/orphan
    single letters / nutrition-bleed remnants — i.e. no real ingredient word survives P1.
  When absent, this is the *already-counted* missing-ingredient case (`compute_confidence` −25);
  D5 emits `disclosure_profile.panel_present = false` and yields no gap findings; D6 handles it via
  the existing path (panel-absent ⇒ floor failure ⇒ `withhold→null`, §2.2). (16/200 maadanim and a
  non-trivial share of hummus had no usable panel — this branch is load-bearing.)
  - **Rationale (binding) — faithful to single-ingredient protection (§1.2 G1, sanity-check §5
    #1).** A length-only cutoff (`<15 chars`) would set `panel_present=false` on a clean walnut or
    almond panel and wrongly **withhold** a maximally-transparent whole food — the exact perverse
    inversion §1.2 G1 and §5 #1 exist to prevent. The token-aware rule withholds only genuinely
    unreadable panels and keeps short clean ones, which is the more conservative choice (Q1 "buy
    coverage over silence"). Verified on the pilot: it reduced hummus withholds **7→4**, the 3
    recovered panels all correctly keeping their grade (single-ingredient `חומוס`-type panels);
    truly panel-less SKUs still read absent. **Co-signed correct — Nutrition D6/D7 (TASK-179L,
    2026-06-04).**

### 1.2 The five disclosure-gap types (detect on the panel)

For each type: the deterministic detection rule, and its contribution to the **disclosure
profile** (a structured list of findings) and the **D5-band** (§1.3). All Hebrew patterns below
are matched against the P2-normalized string. **No gap type deducts grade points (Q2).**

> **Severity tiers** used below: **structural** (a gap the label format can never close — the
> market limit; e.g. proportions, protein-source quality) vs **closable** (a gap the manufacturer
> *could* have closed by naming the additive/E-code but did not). This structural-vs-closable
> split governs how the band maps to D6 in §2 and respects the contract's "partial visibility is
> a structural market limit" framing (§contract truth #1).

---

**G1 — Undisclosed proportions (`%` missing).**
- **Detection:** count ingredient tokens (split the P1-truncated string on `,` outside
  parentheses) vs. count of `%` occurrences (`\d+(?:[.,]\d+)?\s*%`). Fire G1 when the panel has
  **≥2 ingredient tokens and zero `%`**, OR when it has some `%` but the **first/lead ingredient
  carries no `%`** (the dominant ingredient's share is the one that matters most).
- **Severity:** **structural.** Israeli/EU labels disclose `%` only for emphasized/named
  ingredients (QUID); near-total absence of proportions is the market norm, not a manufacturer
  choice. 122/184 maadanim panels showed *at least one* `%`, so partial-QUID is common but full
  proportion disclosure is essentially never present.
- **Profile contribution:** `{type:"proportions", severity:"structural", tokens_n, pct_n}`.
- **NOTE — single-ingredient protection (mandatory):** if the panel resolves to **exactly one
  ingredient token** (e.g. hummus `גרגרי חומוס מבושלים`, a plain walnut), G1 does **NOT** fire —
  a single-ingredient whole food has nothing to apportion and is maximally transparent. Treat
  1-token panels as `disclosure_profile.single_ingredient = true` → **full-disclosure band**
  regardless of `%`. This prevents the perverse "clean whole food looks incomplete" inversion.

**G2 — Compound ingredient without internal breakdown.**
- **Detection:** a named ingredient followed by an empty or non-itemized parenthetical, OR a
  recognized compound food named with no `(`…`)` sub-list where one is expected. Concretely fire
  G2 when a token matches a compound-food lexicon entry (e.g. `שוקולד`, `עוגיות`, `קרם`,
  `ציפוי`, `סירופ גלוקוזה`, `נבט אורז`) **and** is not immediately followed by `(`…`)` listing
  sub-ingredients. (Counter-example that must NOT fire: `קרם ((66%), שמנת (46%), פירורי עוגיות
  (21%), קמח חיטה לבן …)` — the טירמיסו panel *does* break the compound down, so G2 is satisfied,
  not fired.)
- **Severity:** **closable** (the manufacturer could itemize) shading to structural for deep
  nesting. Implement as closable in v1.
- **Profile contribution:** `{type:"compound", severity:"closable", token:"<name>"}` per hit.

**G3 — "Protein blend" / unspecified protein source.**
- **Detection:** fire when the panel names protein generically without a single specific source:
  pattern set `תערובת חלבונים | תערובת חלבון | חלבון צמחי | חלבונים (… ,… ,…)` where the
  parenthetical lists ≥2 sources without proportions (the canonical pea+rice / whey+soy+pea gap,
  179A §1 row 11/25). Also fire the **incomplete-source flag** (distinct sub-type, not a penalty)
  when the *named* source is `קולגן`/`ג'לטין` (collagen/gelatin) — disclosed but an incomplete
  protein (179A §1 rows 22/23; observed `חלבון קולגן 13%` in a protein snack). G3 does NOT fire
  when a single complete source is named (`חלבוני מי גבינה`, `רכיבי חלב`, `גבינה לבנה`).
- **Severity:** **structural** for the blend (proportions hidden); the collagen/gelatin case is a
  **disclosed-but-low-quality SIGNAL routed to D2** (ingredient evidence), NOT a D5 gap — record
  it in the profile as `{type:"protein_source", subtype:"incomplete_named", note:"feeds D2, not a gap"}`
  so D2 can read it, but it does **not** raise the D5 gap band.
- **Profile contribution:** blend → `{type:"protein_source", subtype:"blend_unspecified", severity:"structural"}`.

**G4 — Generic additive class stated without an E-code or name.**
- **Detection:** for each generic-class term in the lexicon below, fire G4 once per occurrence
  where the term is **NOT** immediately followed (after optional whitespace) by `(` or `:`
  introducing a specific name/E-code. The `(`/`:` test is the discriminator and is empirically
  reliable on real panels (verified counts below).
  - Lexicon (P2-normalized): `מייצב`, `מייצבים`, `מתחלב`, `חומר משמר`, `חומרי שימור`,
    `צבע מאכל`, `צבעי מאכל`, `חומרי תפיחה`, `מגביר חוזק`, `מווסת חומציות`/`מווסתי חומציות`,
    `מסמיך`, `נוגד חמצון`, `ממתיקים`.
  - **`חומרי טעם וריח` / `חומר טעם וריח` (flavorings) — SPECIAL-CASE, see §1.4.** Detect and
    record, but treat as **endemic** (it is bare in 129/184 maadanim panels — essentially never
    disclosed by composition). It enters the profile as `endemic_flavoring` and is **excluded
    from the D5-band band-raising logic** so it does not demote nearly the entire shelf via D6.
- **Severity:** **closable** (an E-code/name was available and omitted). This is the cleanest
  "the manufacturer could have told us" gap.
- **Profile contribution:** `{type:"generic_additive", term:"<term>", severity:"closable"}` per bare hit.
- **Empirical calibration (maadanim, 184 panels, post-P2):** `מייצב` bare 66 / named 52;
  `מייצבים` bare 5 / named 54; `מתחלב` bare 15 / named 19; `חומר משמר` bare 3 / named 34;
  `צבע מאכל` bare 6 / named 41; `ממתיקים` bare 1 / named 37. So named-disclosure is the majority
  for most classes EXCEPT bare `מייצב` (common) and flavorings (endemic). The detector is
  therefore discriminating, not a blanket fire.

**G5 — Declared-quantity-missing where a panel would normally carry it.**
- **Detection:** over the disclosed `nutrition` block, fire G5 for each *expected-for-category*
  field that is absent or blank. This **reuses, does not duplicate**, the existing
  `compute_confidence` missing-field map (energy/protein/carbs/fat/fiber/sodium). D5's job is to
  **name which fields are missing** in the profile (the contract's "D5 names *which*, not just
  that confidence dropped", §D5). Additionally flag **saturated-fat / sugar absence** where the
  category red-label regime expects it (observed: `saturated_fat_raw:""` and blank fiber in
  several maadanim) — these are disclosure gaps even though they are not in the legacy −10/−5 map.
- **Severity:** **structural** (panel-format / scrape limit) for the legacy six; **closable** for
  sat-fat/sugar where the manufacturer omitted a red-label-relevant value.
- **Profile contribution:** `{type:"missing_field", field:"<name>", severity:"…"}` per field.
- **No double-counting (critical):** G5 does **not** add a new confidence deduction for the
  legacy six fields — those are *already* deducted in `compute_confidence`. G5 only (a) names
  them in the profile, and (b) for the *new* sat-fat/sugar omissions, contributes to the D5-band
  (which then feeds D6 once, in §2.2) — never a second raw deduction on top of the legacy map.

### 1.3 The disclosure profile and the D5-band

**D5 output object** (per product, internal/professional surface only):

```
disclosure_profile = {
  panel_present: bool,
  single_ingredient: bool,
  findings: [ {type, severity, term/field/token, span?}, ... ],
  counts: { structural_n, closable_n, endemic_flavoring: bool,
            protein_source_to_d2: [...] },
  d5_band: "full" | "minor" | "partial" | "severe",   # the band that feeds D6
  d5_completeness: int 0-100                            # see banded rationale below
}
```

**Why a BAND (4 levels), not a precise 0–100 as the load-bearing measure.** A precise
disclosure percentage would imply a precision the panel cannot support (you cannot know *how
much* is hidden when proportions are hidden — that is the whole point of truth #1). So the
**band is authoritative** for the D6 gate; `d5_completeness` (0–100) is emitted as a *monotone,
explainability-only* convenience number (professional surface), derived deterministically from
the band + counts, and is **never** itself a gate input. This keeps D5 honest: it reports a
*profile*, not a false metric.

**Band assignment (deterministic; the closable/structural split drives it):**

| D5-band | Condition (after single-ingredient + endemic-flavoring exclusions) | `d5_completeness` (explainability only) |
|---|---|---|
| **full** | `single_ingredient = true`, OR zero `findings` after exclusions | 90–100 |
| **minor** | only **structural** gaps fire (proportions/missing-field that the format can't close), no closable gaps | 70–89 |
| **partial** | **≥1 closable** gap fires (bare generic additive, un-itemized compound, omitted red-label value) | 45–69 |
| **severe** | panel absent (`panel_present=false`), OR **closable gaps across ≥3 distinct classes**, OR a generic protein blend (G3 structural) **co-occurring** with ≥2 closable gaps | < 45 |

**Q2 restatement — binding on this whole section:** the D5-band and `d5_completeness` are a
**disclosure profile only**. They **do not** deduct grade points and are **not** a quality axis
in the composite. They feed D6 (§2) and annotate the professional/consumer surfaces. A `severe`
band does not "lower the grade"; it lowers *confidence*, which is what may demote/withhold.

### 1.4 Endemic-flavoring rule (explicit)

`חומרי טעם וריח` bare is present in ~70% of maadanim panels. If it raised the band it would
push almost the entire shelf to `partial`/`severe` and demote the whole category via D6 — a
category-blind distortion (cf. DISTORTION-001 fiber). Ruling: **bare flavorings are recorded in
the profile as `endemic_flavoring:true` and annotated ("הרכב הטעמים לא פורט" — a calm, non-intent
note) but are EXCLUDED from band-raising and from D6.** This is a category-endemic-distortion
handling consistent with cereals_gap_resolution §6.4. If a future category shows flavorings are
*not* endemic, re-evaluate per that protocol. Bound by **EV-036** (BSIP2 registry; draft EV-080).

---

## 2. D6 — Gate Spec (extend the existing confidence machinery)

D6 is `compute_confidence` extended. **Do not reinvent it.** Today (`score_engine.py`
L70–161 + L1281–1301) it: deducts from 100 → bands High/Medium/Low/Insufficient → sets a
ceiling (`CONFIDENCE_LOW_CEILING=75` for 40–59, `CONFIDENCE_INSUFFICIENT_CEILING=50` for <40) →
applies the ceiling at Stage 9 → routes `confidence<40 or no_nutrition_data` to
`grade="insufficient_data"`. D6 adds **one named input** (the D5-band) and **one new outcome**
(`withhold(→null)`), and formalizes the existing ceiling as the **`demote`** state.

### 2.1 D6 confidence score (0–100)

`d6_confidence = compute_confidence(...)` **unchanged in its existing deductions**, PLUS a single
new D5-derived reduction term applied inside the same `deduct()` accumulator, gated by the flag:

| D5-band (from §1.3) | Additional D6 confidence reduction | Reason string |
|---|---|---|
| full | 0 | — |
| minor | 0 | structural-only gaps do not erode confidence (truth #1: market limit, not a data fault) |
| partial | **−10** *(PROPOSED — D7)* | `d5_disclosure=partial (closable gaps)` |
| severe | **−20** *(PROPOSED — D7)* | `d5_disclosure=severe` |

Rationale for the asymmetry: **structural** gaps (minor band) are the normal market floor and
must not bleed confidence (else every product demotes — Q1's "buy coverage"). Only **closable**
opacity (partial/severe) — where the manufacturer *could* have disclosed and did not — erodes the
engine's trust that it is seeing the real formulation. The reduction is modest by design so D5
acts *through* confidence, never as a back-door quality penalty (Q2). These two numbers are
**PROPOSALS — require Product D7 co-sign** (EV-037, BSIP2 registry; draft EV-081).

**No double-count guard:** the D5-band reduction is the *only* new term. The legacy missing-field
deductions (G5's legacy six) stay exactly as today; D5 names them but does not re-deduct (§1.2 G5).

### 2.2 The D6 gate state machine (`unconstrained · demote · withhold→null`)

After `d6_confidence` is computed, derive the **gate state**. This is the formalization +
extension of today's ceiling logic. `B_severe` = the D5-band is `severe`.

```
# floor-of-observability inputs (the two genuine "cannot rank at all" cases):
panel_absent      = (not disclosure_profile.panel_present) OR context_flag == "no_nutrition_data"
floor_failure     = panel_absent
                    OR (d6_confidence < NULL_FLOOR  AND  B_severe)     # both thin AND opaque

if floor_failure:
    gate_state = "withhold"        # → score: null, grade label "לא נוקד"
elif d6_confidence < DEMOTE_CEILING_BOUND:        # the existing Low/Insufficient region
    gate_state = "demote"          # → ceiling applies (existing behavior), + visible "ניתוח חלקי"
else:
    gate_state = "unconstrained"   # → composite passes through
```

**State → effect:**
- **`unconstrained`** (d6 ≈ ≥60, High/Medium): composite D1–D5 passes through. No ceiling, no flag.
- **`demote`** (d6 in the Low/Insufficient band but *above* the null floor): apply the **existing
  ceiling** (the seed: `CONFIDENCE_LOW_CEILING=75` at 40–59; `CONFIDENCE_INSUFFICIENT_CEILING=50`
  at <40) AND surface the visible **`ניתוח חלקי`** flag. This is "conservative-to-demote" (Q1):
  the *normal* partial-disclosure / thin-data case lands here and keeps a (capped) grade —
  coverage over silence.
- **`withhold(→null)`** (floor failure only): output `score: null`, grade label **`לא נוקד`**,
  lead the card with the data gap (existing `insufficient_data` presentation, confidence_framework
  §"product experience"). This replaces today's "cap at 50 and show a middle number" for the
  *genuine floor* case — "below a floor of observability, we decline to rank, we do not guess a
  middle" (contract §D6). Reserved and rare (Q1: reluctant-to-withhold).

### 2.3 PROPOSED binding numbers (require Product D7 co-sign before Data builds)

The contract said `CONFIDENCE_LOW_CEILING=70`; the **live constant is 75** (raised by the milk
recal, `constants.py` L435). The proposals below preserve the live constants for `demote` and add
*only* the new null floor — so OFF→ON cannot move a currently-graded product *unless* it crosses
the new null floor, which by construction only catches panel-absent / both-thin-and-opaque cases
that today already route to `insufficient_data` (cap-50 + `insufficient_data` grade). See §2.4.

| Symbol | Proposed value | Meaning | Maps to / supersedes |
|---|---|---|---|
| `DEMOTE_CEILING_BOUND` | **60** | d6_confidence below this → `demote` region (ceiling applies) | the existing band edge (High/Medium ≥60); **no change** to live behavior |
| (demote ceilings) | **75 / 50** (unchanged) | the ceilings applied *within* demote | reuse live `CONFIDENCE_LOW_CEILING=75`, `CONFIDENCE_INSUFFICIENT_CEILING=50` |
| `NULL_FLOOR` | **30** | d6_confidence below 30 **AND** `severe` D5-band → `withhold(→null)` | the **new** null-vs-cap boundary |
| (panel-absent) | always `withhold` | no usable ingredient panel ⇒ floor failure regardless of d6 number | tightens today's `insufficient_data` to `לא נוקד` for the genuinely panel-less |

**Why `NULL_FLOOR = 30` and gated on `severe` (the conservative, reluctant-to-withhold choice,
Q1):** today everything `<40` caps at 50 and is labelled `insufficient_data`. A pure "<40 → null"
rule would withhold a large chunk of the shelf (bread saw ~40% unscored) — too aggressive,
violates "buy coverage over silence." By requiring **both** `d6_confidence < 30` **and** a
`severe` disclosure band (or an outright absent panel), withhold fires only when the data is
*both* numerically thin *and* structurally opaque — a true floor-of-observability failure. The
40–59 (Low) and 30–39 (deep Insufficient but not severe-band) products keep a *capped* grade in
`demote` rather than going null. **`30` and `60` are PROPOSALS — Product D7 must co-sign**
(EV-038, BSIP2 registry; draft EV-082). If Product prefers even-more-reluctant withholding, raise the band requirement
(e.g. require panel-absent only) rather than lowering the number.

### 2.4 Why OFF = byte-identical and ON is near-identical-by-construction

- **Flag OFF:** none of §2.1/§2.2 executes; `compute_confidence` and Stage 9 are the current code
  path → 0-diff (verified in §4).
- **Flag ON, the only score-moving deltas:** (a) the −10/−20 D5 confidence reduction can push a
  borderline product across a band edge → possibly a different ceiling; (b) a panel-absent or
  both-thin-and-opaque product flips from `insufficient_data`(cap-50) to `לא נוקד`(null). Both are
  **demotions or null only** — D6 can never *raise* a score (contract §4 invariant: snack-bar A
  ceiling and milk top are structurally safe; D6 only removes/caps). Frozen golden runs must be
  re-verified under the flag and any delta inspected against this expectation before any go-live
  (separate D7/owner gate; this task ships nothing live).

---

## 3. DRAFT Evidence-Registry Entries (EV-035 … EV-039)

**These five entries were relocated (TASK-179F) to the BSIP2 engine registry**
`03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` as **EV-035…EV-039** —
they are BSIP2 packaged-food engine scoring rules and belong with the EV- series they cite
(EV-029/030/031/032/034), NOT the governance BEV- registry. They are drafted in the contract's
D-EV-1 discipline (every rule that binds a number/verdict gets an EV before it ships; append-only
on Product co-sign). The drafts below are retained for provenance; the controlling entries now
live in the BSIP2 registry (BSIP2 max = EV-039). ID mapping: EV-079→EV-035, EV-080→EV-036,
EV-081→EV-037, EV-082→EV-038, EV-083→EV-039.

---

### EV-035 (draft EV-079) — DRAFT
**Topic:** D5 disclosure-gap taxonomy (five types) over the raw BSIP0 panel
**Summary:** Defines the five deterministic disclosure-gap detectors — G1 undisclosed
proportions (with single-ingredient protection), G2 compound-without-breakdown, G3 protein
blend / unspecified source (collagen/gelatin routed to D2, not a gap), G4 generic additive class
without E-code/name, G5 declared-quantity-missing (names the field; no re-deduction of the legacy
six) — and the structural-vs-closable severity split. Detectors run on `ingredients_raw` +
`nutrition` from `02_products\*\...bsip0_raw*.json` after P1 nutrition-bleed truncation and P2
Hebrew normalization. Per Q2/DEC-006, the taxonomy produces a **disclosure profile only** and
**never deducts grade points**.
**Source:** `01_framework/glass_box/d5_d6_rule_spec_v1.md §1`; contract §D5;
179A §1–§3 disclosure observations; EV-029 (Hebrew final-letter parser trap).
**Status:** DRAFT — pending Product D7 co-sign
**Impact:** Scoring (via D6), Interpretation

---

### EV-036 (draft EV-080) — DRAFT
**Topic:** Endemic-flavoring exclusion from the D5 band
**Summary:** Bare `חומרי טעם וריח` is present in ~70% of maadanim panels (129/184). To avoid a
category-blind distortion (cf. DISTORTION-001), bare flavorings are recorded in the disclosure
profile as `endemic_flavoring` and annotated with a calm non-intent note, but are EXCLUDED from
D5 band-raising and from the D6 confidence reduction. Re-evaluate per cereals_gap_resolution
§6.4 if a future category shows flavorings are not endemic.
**Source:** `…d5_d6_rule_spec_v1.md §1.4`; maadanim BSIP0 frequency analysis 2026-06-04;
cereals_gap_resolution_v1 §6.4 (endemic-distortion protocol).
**Status:** DRAFT — pending Product D7 co-sign
**Impact:** Scoring (via D6), Interpretation

---

### EV-037 (draft EV-081) — DRAFT
**Topic:** D5-band → D6 confidence reduction (the only new D6 input)
**Summary:** The D5-band feeds D6 as a single named reduction inside the existing
`compute_confidence` accumulator: full 0, minor 0 (structural-only gaps are the market floor and
do not erode confidence), **partial −10**, **severe −20** (PROPOSED). Structural gaps never
reduce confidence; only closable opacity does. No double-count with the legacy missing-field map.
This operationalizes Q2 (D5 acts through confidence, not as a quality penalty) and the contract's
D-CONF-1 (D5 as a named confidence input).
**Source:** `…d5_d6_rule_spec_v1.md §2.1`; contract §D6, D-CONF-1; confidence_framework.md.
**Status:** DRAFT — pending Product D7 co-sign (the −10/−20 are proposals)
**Impact:** Scoring

---

### EV-038 (draft EV-082) — DRAFT
**Topic:** D6 gate state machine + null-vs-cap floor (`NULL_FLOOR=30`, `DEMOTE_CEILING_BOUND=60`)
**Summary:** Extends the existing confidence ceiling from ceiling-only to a three-state gate
`unconstrained · demote · withhold(→null)`. `demote` reuses the live ceilings
(`CONFIDENCE_LOW_CEILING=75`, `CONFIDENCE_INSUFFICIENT_CEILING=50`) plus a visible `ניתוח חלקי`
flag and carries the normal partial-disclosure case (Q1 conservative-to-demote).
`withhold(→null)` (`score:null`, label `לא נוקד`) fires ONLY on a floor-of-observability failure:
panel absent, OR `d6_confidence < 30` AND a `severe` D5-band (Q1 reluctant-to-withhold — buy
coverage over silence). The numbers 30 and 60 are PROPOSALS. D6 can only demote or withhold,
never promote (preserves frozen invariants).
**Source:** `…d5_d6_rule_spec_v1.md §2.2–§2.3`; contract §D6, §2.6, §2.7, §5.0 Q1; DEC-006;
confidence_framework.md; constants.py (CONFIDENCE_LOW_CEILING=75, CONFIDENCE_INSUFFICIENT_CEILING=50).
**Status:** DRAFT — pending Product D7 co-sign (binds the null-vs-cap boundary)
**Impact:** Scoring

---

### EV-039 (draft EV-083) — DRAFT
**Topic:** `BARI_GLASSBOX_D5D6` flag + OFF = byte-identical guarantee
**Summary:** All D5/D6 logic is gated by env flag `BARI_GLASSBOX_D5D6` (default OFF). With OFF the
engine output and the golden/frozen runs are 0-diff vs the pre-D5/D6 baseline (same discipline as
`BARI_RECAL_P0` / `BARI_TASK144_FIXES`). With ON, the only possible score-moving deltas are
demotions (band-edge ceiling shifts) and `insufficient_data`→`לא נוקד` flips — never promotions.
Rollback = unset the flag.
**Source:** `…d5_d6_rule_spec_v1.md §2.4, §4`; contract §4 invariant-preservation; score_engine.py
flag pattern (RECAL_P0_ON L53, TASK144_FIXES_ON L48).
**Status:** DRAFT — pending Product D7 co-sign
**Impact:** Scoring, Future Work

---

## 4. Flag Design

**Env flag:** `BARI_GLASSBOX_D5D6` — read once at module load, mirroring the existing pattern:

```python
GLASSBOX_D5D6_ON = os.environ.get("BARI_GLASSBOX_D5D6", "off").lower() == "on"
```

**Default:** OFF.

**OFF = byte-identical guarantee (precise).** With `GLASSBOX_D5D6_ON = False`:
- D5's detector is **not invoked** (no `disclosure_profile` is computed or attached).
- In `compute_confidence`, the new D5-band reduction term (§2.1) is guarded by
  `if GLASSBOX_D5D6_ON:` and is skipped → the `score` accumulator, bands, and ceilings are
  computed exactly as today.
- The gate-state machine (§2.2) is not entered; Stage 9 runs the **current** ceiling logic and the
  current `is_insufficient → grade="insufficient_data"` path verbatim.
- No new keys are emitted in the result dict when OFF (or, if emitted, they are `None`/absent and
  excluded from any golden-run comparison the same way `recal_p0_*` keys are gated).
- **Acceptance test (Data must run before commit):** the golden corpus + frozen category runs
  (milk `run_004_recalibrated`, snack-bars `snk-001=70/B` ceiling, bread
  `real_bread_retail_003_v1`) produce a **0-diff** result with `BARI_GLASSBOX_D5D6=off` vs the
  pre-change baseline — identical to the `BARI_RECAL_P0` OFF discipline. Any diff is a build bug,
  not an expected change.

**Wiring behind the flag (so OFF changes nothing):** all D5/D6 additions are *additive and
guarded* — a single `GLASSBOX_D5D6_ON` branch around (a) the detector call site, (b) the §2.1
reduction, and (c) the §2.2 gate-state derivation. The existing ceiling/`insufficient_data` code
remains the fall-through. Rollback = unset the flag (no code revert needed).

---

## 5. Pilot Sanity-Check (real hummus + maadanim panels)

Spot-checked against real `bsip0_raw*.json` panels. The rules are coherent; three panel realities
materially shaped the spec and are now encoded:

1. **Single-ingredient whole foods (hummus `P_104805` = `גרגרי חומוס מבושלים`).** A naive
   completeness measure would flag a pure cooked-chickpea panel as "incomplete" (no `%`, no
   additive names) — exactly backwards. A naive *length* measure (the original `<15 chars` P3
   cutoff) would do worse: it would mark a short clean panel (`אגוזי מלך`, `שקדים`) as panel-absent
   and **withhold** it. **Encoded:** the token-aware P3 rule (§1.1 P3) keeps any panel with a
   coherent ≥2-letter ingredient token *present*, and G1 single-ingredient protection (§1.2 G1)
   resolves it to `single_ingredient=true` → **full** band. Verified on the pilot (hummus withholds
   7→4, 3 recovered single-ingredient panels keeping their grade): the maximally-clean case is read
   as clean, not as a gap and not as absent.

2. **Nutrition-table bleed inside `ingredients_raw`.** Every maadanim/hummus `ingredients_raw`
   string appends the `ערכים תזונתיים …` panel text. Without P1 truncation the detector would
   mis-tokenize and mis-count `%`. **Encoded:** P1 pre-processing (§1.1).

3. **Endemic bare flavorings + Hebrew noise.** `חומרי טעם וריח` is bare in ~70% of panels; tokens
   carry final-letter and stray-space noise (`אצסולפאם k`, `קסנטאן גא ם`, `סיבים תזותיים`).
   **Encoded:** P2 normalization (§1.1) + the endemic-flavoring exclusion (§1.4 / EV-036, BSIP2 registry; draft EV-080), which
   prevents D5 from demoting nearly the whole category via D6.

Additional confirmations from the panels:
- The `(`/`:`-follows test for G4 (bare-vs-named additive) is empirically reliable: `מייצב (פקטין)`
  / `ממתיקים (אצסולפאם k, סוכרלוז)` are correctly *named*; bare `מייצב`, `חומרי תפיחה` correctly
  fire. Named-disclosure is the majority for most classes, so G4 is discriminating, not blanket.
- G3 collagen routing is real and needed: `חלבון קולגן 13%` (a protein snack) is a *disclosed*
  low-quality source — correctly routed to D2 as a SIGNAL, **not** a D5 transparency gap.
- ~16/200 maadanim and several hummus panels have no usable ingredient list → the P3 panel-absent
  branch and the `withhold(→null)` floor are load-bearing, not theoretical.

**No spec change required** beyond what is already encoded above; the panels confirm the design.

---

## 6. Open Items Carried to Product D7 Co-Sign

1. The two D5→D6 confidence reductions: **partial −10, severe −20** (§2.1, EV-037, BSIP2 registry; draft EV-081).
2. The gate thresholds: **`NULL_FLOOR=30`** (the null-vs-cap boundary) and
   **`DEMOTE_CEILING_BOUND=60`** (§2.3, EV-038, BSIP2 registry; draft EV-082).
3. Confirmation that withhold should be gated on **`severe`-band-AND-confidence<30** (the
   reluctant-to-withhold posture, Q1) rather than a plain confidence threshold.
4. EV-035…EV-039 appended to the BSIP2 engine registry on co-sign (done — TASK-179F relocation; draft ids EV-079…EV-083).

Nothing in this spec is adopted. Adoption is the Nutrition (D6/D7) + Product co-sign gate, behind
`BARI_GLASSBOX_D5D6`, 0-diff-verified OFF, and reversible.

---

## 7. Final Nutrition D6/D7 Co-Sign — the four numbers (TASK-179L, 2026-06-04)

Confirmed scientifically sound against the real pilot diff
(`reports/glass_box/proof_B_flag_on_pilot_diff.md` + `_pilot_summary.json`) and the independent
QA verification (`03_operations/qa/reports/qa_glassbox_d5d6_w1.md`). The four numbers **HOLD as
final** — no adjustment:

| Number | Value | Co-sign rationale (against observed behavior) |
|---|---|---|
| D5→D6 reduction: partial / severe / structural-only | **−10 / −20 / 0** | The asymmetry is the whole point: structural gaps are the market floor (QUID, panel-format limits) and correctly erode **0** confidence, so they never bleed the shelf; only *closable* opacity (a name/E-code the manufacturer could have disclosed) costs −10/−20. The pilot bears this out — the reduction drives only **5 maadanim demotes** (band-edge crossings into the legacy <40 gate), it does not cascade. Modest by design so D5 acts *through* confidence, never as a back-door quality penalty (Q2). |
| `NULL_FLOOR` | **30** | Reserves `withhold→null` for genuine floor-of-observability failure. Gated on **confidence<30 AND severe-band** (or panel-absent), **zero** products were withheld for being merely thin — exactly the reluctant-to-withhold posture (Q1, "buy coverage over silence"). A plain `<40→null` would have nulled a large slice (bread ~40%); 30+severe is correctly stingy. |
| `DEMOTE_CEILING_BOUND` | **60** | A no-op restatement of the existing High/Medium band edge (≥60); reuses the live ceilings (75/50) within `demote`. Moves nothing on its own — confirmed by QA's byte-identical OFF and by the bound itself producing no deltas. |

**Supporting evidence that the numbers are sound:**
- **Zero promotions** across 269 pilot products (independently re-derived by QA) — D6 only demotes
  or nulls, frozen invariants (milk 85/A, snack ceiling 70/B) structurally safe.
- **EV-036 load-bearing:** bare flavorings detected in 130/200 (~65%) maadanim; the exclusion keeps
  **163/200 unchanged**. Without it ~65% of the shelf demotes — the numbers only behave because the
  endemic-flavoring exclusion holds the structural floor steady. Confirmed working.
- **Withholds = floor-of-observability only:** maadanim 31 already-non-graded relabels
  (`insufficient_data`→`לא נוקד`) + 1 genuine severe+absent; hummus 4 panel-absent. No thin-only
  null. Reluctant-to-withhold posture confirmed in the data.

**Verdict: CO-SIGNED FINAL (Nutrition D6/D7).** The four numbers are scientifically sound and
require no adjustment. This does **not** re-open the Product co-sign (no number changed).
Flag-ON go-live remains a separate Product/owner decision (QA WARN-2 grade-removal blast radius).

*End of D5/D6 Rule Spec v1 (+ §7 final co-sign, TASK-179L). Spec/doc + EV consistency edits only — no engine, frontend, or score movement.*
