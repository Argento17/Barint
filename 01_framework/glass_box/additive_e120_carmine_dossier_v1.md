---
document: additive_e120_carmine_dossier_v1
task: owner gap-fill (conversation work, 2026-06-26) — "we are missing information on E120"
program: TASK-181 (Glass Box D4 additive library) — addendum to additive_library_expanded_v1 (181A) + additive_tiered_library_v1 (181B)
phase: Evidence captured + detector wired. D4 TIER = likely-neutral (Nutrition CONFIRMED 2026-06-26). Product scope co-sign pending.
status: TIER CONFIRMED (Nutrition) — Product scope co-sign + promotion pending
created_at: 2026-06-26
owner: orchestrator (evidence transcription of owner-supplied research) → Nutrition (tier) → Product (scope co-sign)
provenance:
  - "research/Evidence Registry/Additives/E120/E120 Carmine and Cochineal Extract Evidence Registry Memo for Bari.pdf" (owner-supplied)
  - "research/Evidence Registry/Additives/E120/E120 Evidence Registry Research.pdf" (owner-supplied)
  - owner-pasted "Bari Evidence Registry Memo: E120" (conversation, 2026-06-26)
---

# Additive Evidence Dossier — E120 (Carmine / Cochineal Extract / Carminic Acid)

**Why this exists.** The D4 additive library (181A/181B, 36 additives) had **no entry for E120**,
and the canonical detector (`ingredient_taxonomy.py`) carried **no insect-derived colour and no
carmine synonyms** — Bari could not even recognise carmine on a label. Owner flagged the gap
2026-06-26 and supplied two research PDFs + a registry-ready memo. This dossier captures that
evidence in the 181A format and proposes the registry/tier values. It does **not** finalize the
D4 tier (Nutrition's call) and **does not** move any score.

**What was DONE in this pass (reversible, in-lane, no tripwire):**
1. **Detector wired** — `03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py` now resolves
   E120 → canonical `carmine_cochineal`, `additive_class="colorant_natural_insect"`,
   `is_named_concern=False`. The class is a **new string that no scoring branch in
   `signal_extractor.py` references** → **provably zero score delta** (verified by 3 added
   selftest checks incl. an explicit "outside every scoring branch" assertion; full selftest
   `ALL PASS`). Same posture as the TASK-328 benign additives.
2. **Evidence registered** — this dossier (below).
3. **Index pointer** — a PROPOSED row (#37) added to `additive_tiered_library_v1.md` §2.B,
   pointing here, marked pending co-sign.

**What was deliberately NOT done (flagged, not built):**
- **D4 tier not finalized** — proposed `likely-neutral`; Nutrition assigns, Product co-signs scope.
- **Dietary-preference (insect / non-vegan) flag NOT built** — this is a *new signal type* that
  does not exist in the engine today (the other plant colours E160a/E163/E162/E100 carry no such
  flag). Building a vegan/insect filter is a separate Product+Nutrition decision, out of scope here.
- **No consumer copy shipped** — the Hebrew explanation below is a *draft*; it cannot reach any
  page without the two-gate (Content Agent + Adversarial QA) per the content sign-off hard rule.
- **Citations not yet C0-verified** — DOIs/PMIDs are owner-supplied; `verify_citations.py` must
  pass before any consumer use (citation-fabrication gate).

---

## 1. Identity

| Field | Value |
|---|---|
| E-number | E120 (INS 120) |
| Names | carmine, cochineal extract, carminic acid, Natural Red 4, CI 75470 |
| Hebrew | כרמין · קרמין · קוצ'יניל · חומצה קרמינית · צבע אדום טבעי 4 |
| Function | red colorant (anthraquinone pigment; commercial carmine often an aluminium lake) |
| Origin | **insect-derived** — dried female cochineal (*Dactylopius coccus*) |
| Regulatory status | Authorised: EU (EFSA), US (FDA), JECFA/Codex, **Israel (MoH permitted-additives list, category max levels e.g. 100–200 mg/kg; quantum satis in some)** |
| ADI | **0–5 mg/kg bw/day** (EFSA expresses as 2.5 mg carminic acid/kg bw/day); typical dietary intake < ADI |

## 2. Evidence table (owner-supplied research)

| Source | Org / Journal | Year | ID | Key points | Strength |
|---|---|---|---|---|---|
| Re-evaluation of cochineal, carminic acid, carmines (E120) | EFSA ANS Panel | 2015 | doi:10.2903/j.efsa.2015.4288 | Maintains ADI; exposure < ADI in refined scenarios; carminic acid not genotoxic; no toxicological potential; advises purification to minimise proteinaceous allergens (no allergy threshold). | High (regulatory re-eval) |
| Evaluation of cochineal extract, carmine, carminic acid | JECFA 55th / WHO | 2000 | inchem.org jecmono v46je03 | ADI 0–5 mg/kg bw; may provoke allergic reactions in some individuals via residual proteins; recommends label disclosure to alert sensitised persons; sensitisation rare. | High (intl. expert cttee) |
| Cochineal/Carmine declaration Final Rule (21 CFR 73.100/73.1100) | FDA | 2009 (eff. 2011) | FR E8-31253 | Requires declaration by common name ("cochineal extract"/"carmine"); triggered by allergic-reaction reports incl. anaphylaxis; **not** added to major-allergen definition. | High (labeling mandate) |
| Cochineal dye-induced immediate allergy (Japanese cases, diagnostic chart) | Allergology International | 2018 | PMID:29705083 | IgE-mediated immediate reactions linked to ~38 kDa insect protein; often prior sensitisation via cosmetics/occupation; rare at population level. | Medium-High (case-series review) |
| רשימת תוספי מזון מותרים (permitted additives) | Israel MoH | 2017+ | gov.il PDFs | E120 explicitly listed with category max levels; authorised in Israel. | High (national list) |

## 3. Risk interpretation (non-alarmist, evidence-bounded)

- **Established:** anthraquinone pigment from cochineal insects; authorised with GMP/max levels across
  jurisdictions; ADI set; typical exposure well below ADI; residual insect proteins can elicit IgE
  responses in sensitised individuals (the pigment carminic acid itself is not the allergen).
- **Regulatory safety conclusion:** EFSA 2015 / JECFA 2000 / FDA — safe for the general population at
  approved use levels; no relevant adverse effects at pertinent doses; purification advised to lower
  protein content for sensitive individuals.
- **Rare allergy:** documented in case reports/occupational series (urticaria → anaphylaxis), IgE to
  insect protein, often post cosmetic/occupational sensitisation; **low population incidence**; not a
  major/declared allergen; avoidance handled by labeling. Do **not** equate to Big-9 allergens.
- **Dietary-preference relevance (HIGH for Bari):** insect origin ⇒ incompatible with vegan/strict
  vegetarian; relevant to kosher/halal transparency; often marketed as "natural colour" — true but
  incomplete without source disclosure.
- **Claims to AVOID:** "toxic"/"dangerous"/"harmful"; widespread population allergy; "banned/heavily
  restricted in major markets" (it is authorised with limits); "natural = inherently problematic";
  links to hyperactivity (no E120-specific data).

## 4. Proposed registry entry (PROPOSED — not finalized)

```yaml
signal_id: additive_E120_carmine_cochineal_insect_color
e_number: E120
canonical: carmine_cochineal            # MATCHES the wired detector
ingredient_names: [E120, carmine, cochineal extract, carminic acid, Natural Red 4, CI 75470]
hebrew_patterns: "E120|E-120|E 120|כרמין|קרמין|קוצ׳יניל|קוצ'יניל|חומצה קרמינית|צבע אדום טבעי 4|CI 75470"
english_patterns: "E120|E-120|E 120|INS 120|carmine|cochineal( extract)?|carminic acid|natural red 4|CI 75470"
additive_class: colorant_natural_insect_derived
proposed_d4_tier: likely-neutral        # PROPOSED — Nutrition to assign; rationale: documented but
                                        # RARE IgE signal nudges off `functional` (which the plant
                                        # colours E160a/E163/E162 hold); NOT contested/confirmed-negative.
evidence_level: high                    # regulatory consensus + consistent rarity evidence
scoring_effect:
  nutrition_score: no_change            # negligible kcal/nutrient; not a nutrient of concern
  additive_complexity: mild_flag_only   # colorant presence; long-established natural-origin, NOT a UPF marker
  dietary_preference: insect_non_vegan  # NEW SIGNAL — not yet built; strong transparency relevance
  allergy_caution: optional_contextual_rare  # non-alarmist; existing label declaration supports avoidance
confidence: high (~0.9)
citations: ["doi:10.2903/j.efsa.2015.4288", "JECFA 55th (2000)", "FDA 2009 Final Rule",
            "Israel MoH permitted-additives list", "PMID:29705083"]
```

### Draft Hebrew consumer explanation (DRAFT — two-gate required before any page)

> כרמין (E120) הוא צבע מאכל אדום המופק מחרקי קוצ'יניל. רשויות הבריאות (EFSA, JECFA, FDA) ומשרד
> הבריאות הישראלי קובעות שהוא בטוח לשימוש ברמות המאושרות, עם חשיפה תזונתית נמוכה מה-ADI. עלול לגרום
> לתגובות אלרגיות נדירות אצל אנשים רגישים לחלבוני החרק. אינו מתאים לתזונה טבעונית או צמחונית קפדנית.

## 5. Open items / routing

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Assign final D4 tier | **Nutrition Agent** | ✅ DONE 2026-06-26 — `likely-neutral` confirmed (proposal accepted, 0 amendments, 0 score moves); set `cosmetic_mup=true` per §7.2 colour rule |
| 2 | Scope co-sign (keep E120 though 0-on-shelf today?) | **Product Agent** | OPEN — Nutrition recommends RETAIN (parity with E282/E481/E575/E466) |
| 3 | Decide whether to build the insect/non-vegan dietary-preference signal | **Owner → Product + Nutrition** | PARKED (owner 2026-06-26 — "not sure, park it for now"; revisit, not pre-committed) |
| 4 | `verify_citations.py` C0 pass on the DOIs/PMID before any consumer use | C0 gate | PENDING |
| 5 | Two-gate (Content + Adversarial QA) on the Hebrew copy before any page | content gates | PENDING |
| 6 | Promote row #37 into the live library + display config | **Data Agent** | PENDING (needs item #2 first) |

**Shelf note:** E120 is **0 on every currently displayed Bari shelf** (grep 2026-06-26; the lone
"קוצ" hit in cakes was a false positive inside "שוקוצ'יפס"). It is wired now so it is recognised the
moment a product declares it (e.g. some yogurts / dairy desserts / candies / red beverages), exactly
as the 181A library retains 0-on-shelf additives (E282/E481/E575) for the same reason.
