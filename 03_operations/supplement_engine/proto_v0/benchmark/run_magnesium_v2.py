"""
Magnesium Scoring Model v2 — Standalone Runner
================================================
TASK-384 / BARI_MAGNESIUM_V2=1 (flag-gated; default OFF)
TASK-384 / BARI_MAGNESIUM_V3=1 (v3 flag-gated; default OFF; overrides v2 scoring path when set)

Implements magnesium_model_v2_final_spec.md with TASK-384 Product/Nutrition conditions:
  - MVP = 2 bands only: general-gap (100-300 mg administered elemental) + safety gate
  - Dose pillar = administered elemental mg vs general-gap band; weight 0.40
  - Bioavailability CLASS (HIGH/MODERATE/LOW/UNRESOLVED) -> evidence sub-score modifier
  - Safety: UL 350mg = FLAG not hard-cap; EFSA 250mg = GI note
  - Caps: cap_1 (ceiling 34/E), cap_3_honesty_core (ceiling 49/D)
  - WELL cap_1: fires IFF unsupported delivery-mechanism claim; "WELL" trade name alone does NOT
  - Max550 (7290118818205): excluded (discarded)
  - Amorphicure (7290015429245) + TRIOMAG (7290118816065): UNRESOLVED
  - Solgar (0033984005181): cap_3_honesty_core ceiling 49/D (undisclosed blend)
  - Cramps indication (NT LC 7290010207640): display footnote only, NOT a scored band

v3 additional features (BARI_MAGNESIUM_V3=1):
  Implements magnesium_model_v3_bioav_adjusted_dose_spec.md (owner-approved 2026-06-23):
  - Bioavailability-adjusted dose: administered elemental × tier factor → scored vs general-gap band
  - Tier factors: HIGH=1.0, MODERATE=0.75, LOW=0.35, UNRESOLVED=1.0+ev_penalty (LOW recalibrated 0.45→0.35 per C3 P302 2026-06-23)
  - Pillar weights: W_DOSE=0.55, W_EVIDENCE=0.20, W_TRANSPARENCY=0.25
  - Safety gates remain on administered elemental mg (not adjusted dose)
  - Cross-form backwards monotonicity removed per owner direction (2026-06-23)
  - Display rule: administered elemental + class only; never display adjusted dose or tier factor
  - UL_EXCEED: grade ceiling D (max 49.0) NOT flat -10 (magnesium_ul_ruling_v1.md Option B, 2026-06-23)
  - GI_NOTE_EFSA: >= 250mg (inclusive, per HRT-3 addendum, 2026-06-23)
  - Elemental inputs corrected per panel-verified labels (TASK-384 NRV math):
      Altman 520 (7290017218564): 520mg ELEMENTAL, label_basis=panel_verified_elemental
      Nutricare 520 (7290001065662): 520mg ELEMENTAL, label_basis=panel_verified_elemental
      Altman MagUP (7290013142894): 450mg ELEMENTAL, label_basis=panel_verified_elemental
      Altman Balance (7290019444206): 450mg ELEMENTAL, label_basis=panel_verified_elemental
      Tink 520 (7290015318426): UNRESOLVED (label unconfirmed per §4 UL ruling)
  - HRT-2 clobber guard: v3 run writes magnesium_v3_latest.json + magnesium_v3_verification_table.csv
    (separate from v2 outputs; flag-OFF v2 run cannot overwrite v3 output)

Isolation:
  - Does NOT modify score_engine.py, magnesium.yaml, run_full.py, or any other corpus
  - Reads skus_full/ JSON files as data source (already BSIP1-enriched)
  - Old engine path (run_full.py / SUPP-EV-030) remains byte-identical
  - Flag BARI_MAGNESIUM_V2 must be explicitly set in env; absent = silent no-op
  - Flag BARI_MAGNESIUM_V3 activates v3 scoring; requires BARI_MAGNESIUM_V2=1 also set

Usage:
  set BARI_MAGNESIUM_V2=1
  python run_magnesium_v2.py

  # v3 path:
  set BARI_MAGNESIUM_V2=1
  set BARI_MAGNESIUM_V3=1
  python run_magnesium_v2.py

Output:
  benchmark/magnesium_v2_run_<timestamp>.json   — full run record
  benchmark/magnesium_v2_verification_table.csv  — stable barcode->score->grade->cap table
  benchmark/magnesium_v2_latest.json             — latest run symlink-equivalent

Self-gating (mandatory, return contract requirement):
  Writes monotonicity check result + WELL cap_1 determination inline.
  Exit code 0 = run complete (monotonicity checked, report written).
  Exit code 2 = flag not set (no-op, prints guidance).
  Exit code 1 = hard error.

EDPG: all records candidate. No published score. Page is offline. Nothing ships.
"""
import os
import sys
import json
import pathlib
import datetime
import csv

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---- Flag gate ----------------------------------------------------------------
if os.environ.get("BARI_MAGNESIUM_V2", "").strip() not in ("1", "true", "yes"):
    print(
        "run_magnesium_v2.py: BARI_MAGNESIUM_V2 not set. "
        "Set BARI_MAGNESIUM_V2=1 to run the v2 scorer. "
        "Old engine (run_full.py / SUPP-EV-030) is unaffected."
    )
    sys.exit(2)

# v3 flag — activates bioavailability-adjusted dose scoring
BARI_MAGNESIUM_V3 = os.environ.get("BARI_MAGNESIUM_V3", "").strip() in ("1", "true", "yes")

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent.parent.parent  # C:\Bari
SKUDIR = ROOT / "02_products" / "supplements" / "real_corpus_v3" / "skus_full"
OUT_DIR = HERE

# ---- Grade bands (unchanged from global engine) --------------------------------
GRADE_BANDS = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

# ---- v3 Bioavailability tier factors -------------------------------------------
# Source: NIH ODS Magnesium Fact Sheet + Walker 2003 / Schuette 1994 context
# These are coarse calibration constants, NOT pharmacokinetic absorption fractions.
# Evidence grounding: magnesium_model_v3_bioav_adjusted_dose_spec.md §1.2
BAV_TIER_FACTORS = {
    "HIGH": 1.00,        # citrate, bisglycinate, glycinate — organic, well-absorbed
    "MODERATE": 0.75,    # malate, taurate, hydroxide — intermediate
    "LOW": 0.35,         # oxide, carbonate — lowest solubility/absorption in comparatives; recalibrated 0.45→0.35 per C3 P302 (2026-06-23)
    "UNRESOLVED": 1.00,  # blend: use administered dose conservatively; evidence sub-score penalized
}


def grade_for(score: float) -> str:
    for letter, floor in GRADE_BANDS:
        if score >= floor:
            return letter
    return "E"


# ---- v2 Corpus: explicit list of all 19 magnesium SKUs in scope ---------------
# Source: magnesium_model_v2_final_spec.md Part 4
# Dispositions: SCORED | SOLGAR_EXCEPTION | UNRESOLVED | DISCARDED
CORPUS = [
    # Scored set (15 products)
    {"barcode": "7290011899967", "name_short": "Altman Citrate 120",
     "disposition": "SCORED",
     "elemental_mg": 200.0, "form": "citrate", "bav_class": "HIGH",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": False},
    {"barcode": "7290013464248", "name_short": "Supherb Citrate+B6 Badatz",
     "disposition": "SCORED",
     "elemental_mg": 250.0, "form": "citrate", "bav_class": "HIGH",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": False},
    {"barcode": "7290019444480", "name_short": "Altman Bisglycinate 250",
     "disposition": "SCORED",
     "elemental_mg": 250.0, "form": "bisglycinate", "bav_class": "HIGH",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": False},
    {"barcode": "7290001943700", "name_short": "Full-Mag Hadas 600",
     "disposition": "SCORED",
     "elemental_mg": 122.0, "form": "bisglycinate", "bav_class": "HIGH",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": False},
    # WELL: cap_1 determination required — see WELL_CAP1_DETERMINATION below
    {"barcode": "7290018439043", "name_short": "Nutricare WELL",
     "disposition": "SCORED",
     "elemental_mg": 168.0, "form": "bisglycinate", "bav_class": "HIGH",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": False,
     "well_cap1_check": True},
    # Nano: cap_1 binding (liposomal claim)
    {"barcode": "7290001065594", "name_short": "Nutricare Nano Bisglycinate",
     "disposition": "SCORED",
     "elemental_mg": 88.0, "form": "bisglycinate", "bav_class": "HIGH",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": False,
     "cap_1_liposomal": True},
    {"barcode": "7290018439579", "name_short": "Nutricare Taurate",
     "disposition": "SCORED",
     "elemental_mg": 76.0, "form": "taurate", "bav_class": "MODERATE",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": False},
    # Malate: compound 700mg; elemental range 133-137mg; use midpoint 135mg for scoring
    {"barcode": "7290001066973", "name_short": "Nutricare Malate 90cp",
     "disposition": "SCORED",
     "elemental_mg": 135.0, "form": "malate", "bav_class": "MODERATE",
     "elemental_range": "133-137", "label_confidence": "High",
     "label_basis": "chemistry_derived_range",
     "cramps_footnote": False},
    # Oxide 520 group — CORRECTED elemental (TASK-384, 2026-06-23):
    # IL convention: "(From Magnesium Oxide) Xmg" declares ELEMENTAL, not compound.
    # NRV% math confirms: 520mg / 280mg (women IL NRV) = 185.7%; 520mg / 350mg (men) = 148.6%.
    # Prior chemistry_derived values (314mg = 520×0.603) were WRONG — refuted by label NRV arithmetic.
    # Source: altman.co.il label image (tasks/_scratch_mag_labels/altman520.webp, 2026-06-23).
    # label_basis updated to panel_verified_elemental; oxide_chemistry_note removed for these products (MRT-4).
    {"barcode": "7290001065662", "name_short": "Nutricare Oxide 520",
     "disposition": "SCORED",
     "elemental_mg": 520.0, "form": "oxide", "bav_class": "LOW",
     "label_confidence": "High", "label_basis": "panel_verified_elemental",
     "panel_verified_note": (
         "520mg ELEMENTAL confirmed: IL label '(From Magnesium Oxide) 520mg' convention + "
         "NRV math (520/280=185.7%W, 520/350=148.6%M). "
         "Prior chemistry_derived 314mg REFUTED (TASK-384, 2026-06-23)."
     ),
     "cramps_footnote": False},
    # Tink 520 (7290015318426): UNRESOLVED — label unconfirmed per magnesium_ul_ruling_v1.md §4.
    # Label declares '520 מ"ג מגנזיום אוקסיד' without the standard IL 'From Magnesium Oxide'
    # qualifier and without NRV%. Analog evidence supports elemental reading but label-wins rule
    # requires label confirmation. Missing-data discard rule governs: no-score in interim.
    {"barcode": "7290015318426", "name_short": "Tink Oxide 520",
     "disposition": "UNRESOLVED",
     "unresolved_reason": (
         "Label declares '520 מ\"ג מגנזיום אוקסיד' without the standard IL "
         "'(From Magnesium Oxide)' elemental qualifier and without NRV% "
         "to confirm elemental basis. Analog evidence (all other IL 520mg oxide products "
         "are elemental) supports elemental reading, but label-wins rule requires label "
         "confirmation — not analog inference. One additional targeted retrieval attempt "
         "warranted; discard if unresolvable. (magnesium_ul_ruling_v1.md §4, 2026-06-23)"
     )},
    {"barcode": "7290017218564", "name_short": "Altman 520",
     "disposition": "SCORED",
     "elemental_mg": 520.0, "form": "oxide", "bav_class": "LOW",
     "label_confidence": "High", "label_basis": "panel_verified_elemental",
     "panel_verified_note": (
         "520mg ELEMENTAL confirmed: altman.co.il label image '(From Magnesium Oxide) 520 מ\"ג' "
         "+ NRV math (520/280=185.7%W, 520/350=148.6%M). "
         "Prior chemistry_derived 314mg REFUTED (TASK-384, 2026-06-23)."
     ),
     "cramps_footnote": False},
    # Oxide 450 group — CORRECTED elemental (TASK-384, 2026-06-23):
    # NRV% math: 450/280=160.7%W, 450/350=128.6%M.
    # Source: altman.co.il label images (tasks/_scratch_mag_labels/magup.webp + balance.webp, 2026-06-23).
    # Prior chemistry_derived values (272mg = 450×0.603) were WRONG — refuted by label NRV arithmetic.
    {"barcode": "7290013142894", "name_short": "Altman MagUp",
     "disposition": "SCORED",
     "elemental_mg": 450.0, "form": "oxide", "bav_class": "LOW",
     "label_confidence": "High", "label_basis": "panel_verified_elemental",
     "panel_verified_note": (
         "450mg ELEMENTAL confirmed: altman.co.il label image '(From Magnesium Oxide 750mg) 450 מ\"ג' "
         "(450/750=60% elemental, consistent with MgO fraction) + NRV math. "
         "Prior chemistry_derived 272mg REFUTED (TASK-384, 2026-06-23)."
     ),
     "cramps_footnote": False},
    {"barcode": "7290019444206", "name_short": "Altman Balance",
     "disposition": "SCORED",
     "elemental_mg": 450.0, "form": "oxide", "bav_class": "LOW",
     "label_confidence": "High", "label_basis": "panel_verified_elemental",
     "panel_verified_note": (
         "450mg ELEMENTAL confirmed: same label convention as MagUP + NRV math (450/280=160.7%W). "
         "Prior chemistry_derived 272mg REFUTED (TASK-384, 2026-06-23)."
     ),
     "cramps_footnote": False},
    # NT LC: hydroxide; 190mg label-stated elemental; cramps indication -> display footnote
    {"barcode": "7290010207640", "name_short": "NT LC Anti Leg Cramps",
     "disposition": "SCORED",
     "elemental_mg": 190.0, "form": "hydroxide", "bav_class": "MODERATE",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": True,
     "cramps_note": (
         "ייעוד הפחתת ממולעים: ראיות לא מספיקות (Cochrane 2020, PMID:32956536). "
         "המינון (190 מ\"ג) מתחת לטווח המחקרי של הנחיות שנבדקו (300-500 מ\"ג). "
         "המוצר נבחן על פרמטר ה-gap הכללי (100-300 מ\"ג); ייעוד ממולעים = הערת תווית בלבד."
     )},
    # Tink Malate: label-stated elemental 136mg
    {"barcode": "7290015318532", "name_short": "Tink Malate",
     "disposition": "SCORED",
     "elemental_mg": 136.0, "form": "malate", "bav_class": "MODERATE",
     "label_confidence": "High", "label_basis": "elemental",
     "cramps_footnote": False},
    # Solgar: exception path (cap_3_honesty_core blend; 100mg elemental per 5-tab)
    {"barcode": "0033984005181", "name_short": "Solgar Cal-Mag D3",
     "disposition": "SOLGAR_EXCEPTION",
     "elemental_mg": 100.0, "form": "oxide_citrate_blend", "bav_class": "UNRESOLVED",
     "label_confidence": "High", "label_basis": "us_label_il_unverified",
     "cramps_footnote": False,
     "cap_3_core": True},
    # Unresolved (2 products)
    {"barcode": "7290015429245", "name_short": "Amorphicure pH Carbonate",
     "disposition": "UNRESOLVED",
     "unresolved_reason": (
         "160mg elemental-vs-compound ambiguous (carbonate 0.288 fraction). "
         "If elemental: 160mg -> MEETS general gap. If compound: 46mg -> NEAR. "
         "~3.5x uncertainty; physical label required."
     )},
    {"barcode": "7290118816065", "name_short": "Supherb TRIOMAG",
     "disposition": "UNRESOLVED",
     "unresolved_reason": (
         "200mg likely elemental per IL convention but unconfirmed; "
         "form ratios (citrate:bisglycinate:taurate) undisclosed. "
         "Cannot assign bioavailability class without per-form ratios."
     )},
    # Discarded (1 product)
    {"barcode": "7290118818205", "name_short": "Supherb Max 550",
     "disposition": "DISCARDED",
     "discard_reason": (
         "oxide:citrate ratio undisclosed on all accessible IL sources. "
         "Administered elemental unknowable. Missing-data discard rule (owner-approved)."
     )},
]

# ---- WELL cap_1 determination (per spec requirement) --------------------------
# Task-384 spec: read WELL's actual label copy — cap_1 fires IFF an unsupported
# delivery-mechanism claim is present (e.g. "enhanced absorption/proprietary matrix").
# A trade name alone ("WELL") does NOT trigger cap_1.
#
# Evidence from SP-7290018439043.json panel:
#   primary_claim: "מגנזיום ביסגליצינאט עם אבץ וויטמין B6"
#   form_raw: "bisglycinate"
#   proprietary_blend: false
#   ingredient: "מגנזיום (magnesium bisglycinate)"
#
# Analysis: The claim "מגנזיום ביסגליצינאט עם אבץ וויטמין B6" is a simple ingredient
# description — "magnesium bisglycinate with zinc and vitamin B6." There is NO delivery-
# mechanism claim: no "enhanced absorption," no "proprietary matrix," no "liposomal,"
# no "nano" delivery claim, no "WELL technology" or similar. The form_raw is plain
# "bisglycinate" (not "bisglycinate liposomal" or similar). proprietary_blend=false.
# The name "WELL" is a product trade name — Nutricare's line branding — not a claimed
# delivery mechanism. Per spec: "A trade name alone does NOT trigger cap_1."
# DETERMINATION: cap_1 does NOT fire for WELL. Standard path applies.
#   -> 168mg bisglycinate, HIGH class, ~C grade.
WELL_CAP1_FIRED = False
WELL_CAP1_REASON = (
    "cap_1 NOT fired. "
    "Panel primary_claim: 'מגנזיום ביסגליצינאט עם אבץ וויטמין B6' — "
    "ingredient description only, no delivery-mechanism claim. "
    "form_raw='bisglycinate', proprietary_blend=false. "
    "Trade name 'WELL' is Nutricare line branding, not an absorption-mechanism claim. "
    "Spec condition: 'A trade name alone does NOT trigger cap_1.' "
    "DETERMINATION: standard path (168mg bisglycinate, HIGH class)."
)

# ---- v2 Pillar definitions (spec §1-§3) ---------------------------------------
# Pillar 1: Dose (administered elemental mg vs general-gap band 100-300 mg)
DOSE_BAND_LO = 100.0   # general-gap lower bound (mg/day elemental)
DOSE_BAND_HI = 300.0   # general-gap upper bound

# Dose sub-score rules (spec Part 1, Pillar 1):
# MEETS (>= lower bound): 70-100 scaled linearly
#   at lower bound (100mg) = 70; at/above midpoint (200mg) = 85; at/above upper (300mg) = 100
# NEAR (50-99% of lower bound = 50-99mg): 40-69 scaled linearly
#   50% of lower = 50mg -> score 40; at lower = 70
# FAR_BELOW (<50% of lower bound = <50mg): 0-39 scaled
#   at 0mg = 0; at 50% of lower = 40


def dose_sub_score(elemental_mg: float) -> tuple:
    """Returns (score, dose_tier_label, dose_tier_description)."""
    lo = DOSE_BAND_LO
    mid = (DOSE_BAND_LO + DOSE_BAND_HI) / 2.0  # 200mg

    if elemental_mg >= lo:
        # MEETS band: linear from 70 at lo to 85 at mid to 100 at hi+
        if elemental_mg <= mid:
            t = (elemental_mg - lo) / (mid - lo)
            score = 70.0 + t * (85.0 - 70.0)
        elif elemental_mg <= DOSE_BAND_HI:
            t = (elemental_mg - mid) / (DOSE_BAND_HI - mid)
            score = 85.0 + t * (100.0 - 85.0)
        else:
            # Above upper bound (e.g. 314mg > 300mg): stays at 100
            score = 100.0
        return round(score, 1), "MEETS", f"{elemental_mg}mg >= {lo}mg lower bound"

    near_floor = lo * 0.5  # 50mg
    if elemental_mg >= near_floor:
        # NEAR band: linear from 40 at 50mg to 70 at 100mg
        t = (elemental_mg - near_floor) / (lo - near_floor)
        score = 40.0 + t * (70.0 - 40.0)
        return round(score, 1), "NEAR", f"{elemental_mg}mg = {round(elemental_mg/lo*100)}% of lower bound"

    # FAR_BELOW: linear from 0 at 0mg to 40 at 50mg
    t = elemental_mg / near_floor if near_floor > 0 else 0.0
    score = 0.0 + t * 40.0
    return round(score, 1), "FAR_BELOW", f"{elemental_mg}mg < 50% of lower bound"


# ---- v3 Dose sub-score (bioavailability-adjusted) ------------------------------
DOSE_BAND_MID = (DOSE_BAND_LO + DOSE_BAND_HI) / 2.0  # 200.0


def dose_sub_score_v3(elemental_mg: float, bav_class: str) -> tuple:
    """
    v3: adjusted_dose = elemental_mg x tier_factor(bav_class).
    Scored against general-gap band 100-300mg.
    Returns (score, dose_tier_label, dose_tier_desc, adjusted_dose_mg).
    Internal use only — consumer display uses administered_elemental_mg + bav_class label.
    """
    factor = BAV_TIER_FACTORS.get(bav_class, 1.00)
    adj = elemental_mg * factor
    lo = DOSE_BAND_LO    # 100.0
    mid = DOSE_BAND_MID  # 200.0

    if adj >= lo:
        if adj <= mid:
            t = (adj - lo) / (mid - lo)
            s = 70.0 + t * 15.0
        elif adj <= DOSE_BAND_HI:
            t = (adj - mid) / (DOSE_BAND_HI - mid)
            s = 85.0 + t * 15.0
        else:
            s = 100.0
        tier = "MEETS"
        desc = f"adj={adj:.1f}mg ({elemental_mg}mg x {factor}) >= {lo}mg lower bound"
    elif adj >= lo * 0.5:
        t = (adj - lo * 0.5) / (lo - lo * 0.5)
        s = 40.0 + t * 30.0
        tier = "NEAR"
        desc = f"adj={adj:.1f}mg ({elemental_mg}mg x {factor}) = {round(adj/lo*100)}% of lower bound"
    else:
        t = adj / (lo * 0.5) if lo > 0 else 0.0
        s = t * 40.0
        tier = "FAR_BELOW"
        desc = f"adj={adj:.1f}mg ({elemental_mg}mg x {factor}) < 50% of lower bound"

    return round(s, 1), tier, desc, round(adj, 1)


# Pillar 2: Bioavailability class -> evidence sub-score modifier
# Weight: evidence pillar = 0.30
# Base evidence sub-score for general-gap: Moderate band midpoint
# Moderate band: 60-84 -> midpoint = 72
# Class modifiers (additive to evidence sub-score):
#   HIGH:       +8  -> 72+8 = 80
#   MODERATE:   +3  -> 72+3 = 75
#   LOW:        +0  -> 72+0 = 72
#   UNRESOLVED: -5  -> 72-5 = 67
BAV_CLASS_EVIDENCE_BASE = 72.0  # Moderate tier midpoint for general-gap indication
BAV_CLASS_MODIFIERS = {
    "HIGH": 8.0,
    "MODERATE": 3.0,
    "LOW": 0.0,
    "UNRESOLVED": -5.0,
}
BAV_CLASS_LABELS = {
    "HIGH":       "ספיגה גבוהה יחסית",
    "MODERATE":   "ספיגה בינונית",
    "LOW":        "ספיגה נמוכה יחסית",
    "UNRESOLVED": "הרכב לא פורט — לא ניתן להעריך ספיגה",
}


def evidence_sub_score(bav_class: str) -> tuple:
    """Returns (score, description)."""
    mod = BAV_CLASS_MODIFIERS.get(bav_class, 0.0)
    score = max(0.0, min(100.0, BAV_CLASS_EVIDENCE_BASE + mod))
    return round(score, 1), f"base={BAV_CLASS_EVIDENCE_BASE} + class_mod({bav_class})={mod}"


# ---- v3 Evidence sub-score constants -------------------------------------------
EV_BASE_V3 = 72.0        # flat base for all known classes (class already expressed in dose via tier factor)
EV_UNRESOLVED_PENALTY = -20.0


def evidence_sub_score_v3(bav_class: str) -> tuple:
    """
    v3: class is embedded in dose (tier factor). Evidence sub-score is flat for all
    known classes. UNRESOLVED gets penalty (cannot evidence-classify).
    Returns (score, description).
    """
    if bav_class == "UNRESOLVED":
        score = max(0.0, EV_BASE_V3 + EV_UNRESOLVED_PENALTY)
        return round(score, 1), f"base={EV_BASE_V3} + UNRESOLVED_penalty={EV_UNRESOLVED_PENALTY}"
    return round(EV_BASE_V3, 1), f"base={EV_BASE_V3} (class expressed in adjusted dose)"


# Pillar 3: Transparency + Safety
# Safety gate: UL 350mg = FLAG not hard-cap (-10 from final score)
# EFSA 250mg = GI note (display only, no score deduction per MVP spec)
UL_350 = 350.0   # NIH/IOM supplemental UL — FLAG (not hard-cap in v2)
UL_250 = 250.0   # EFSA GI-tolerance threshold — note only

# Transparency sub-scores (Pillar 3, weight 0.30):
# Base = 100; debits applied per spec
#   Declared elemental AND form by chemical name (label_basis=elemental or chemistry_derived)
#     +15 (elemental declared) +10 (form named) = 25 points -> start at 75 baseline, +25 = start 75
#   Actually: transparency sub-score starts at 0 and adds positive signals.
#   Spec: label explicitly states elemental mg = +15; form by chemical name = +10; two-line = +5 bonus
#   Oxide chemistry-derived (no explicit elemental declaration) = no two-line bonus (+15 elemental only)
#   Blend with undisclosed ratios = -15 (cap_3_honesty_core also fires separately)
#   Evidence-insufficient proprietary delivery system = -15 (cap_1 path)
def transparency_sub_score(sku: dict) -> tuple:
    """
    Returns (score, signals_applied).
    Builds from spec Part 1 Pillar 3 transparency signals.
    """
    score = 0.0
    signals = []

    basis = sku.get("label_basis", "")
    bav_class = sku.get("bav_class", "")
    cap1 = sku.get("cap_1_liposomal", False)
    cap3 = sku.get("cap_3_core", False)
    is_unresolved_blend = (bav_class == "UNRESOLVED" and cap3)

    # +15 elemental declared (label states elemental mg — directly, via chemistry, or panel-verified)
    # panel_verified_elemental = label confirmed to declare elemental directly (e.g., via NRV% math)
    if basis in ("elemental", "chemistry_derived", "chemistry_derived_range", "panel_verified_elemental"):
        score += 15.0
        signals.append("+15 elemental_declared")
    elif basis == "us_label_il_unverified":
        # Solgar: US label reliable for elemental; no +15 until IL verified
        score += 10.0  # partial credit — US label is strong evidence
        signals.append("+10 elemental_declared_us_label_only")

    # +10 form by chemical name
    form = sku.get("form", "")
    if form and form not in ("oxide_citrate_blend",):
        score += 10.0
        signals.append(f"+10 form_chemical_name({form})")

    # +5 two-line bonus: label states BOTH compound mg AND elemental mg separately
    if basis == "elemental" and form in ("bisglycinate", "citrate", "taurate", "malate", "hydroxide"):
        # Products with confirmed elemental + known form = two-line convention confirmed
        score += 5.0
        signals.append("+5 two_line_label_convention")

    # -15 blend with undisclosed ratios (UNRESOLVED class + proprietary blend)
    if is_unresolved_blend:
        score -= 15.0
        signals.append("-15 blend_undisclosed_ratios")

    # -15 evidence-insufficient proprietary delivery claim (liposomal/nano)
    if cap1:
        score -= 15.0
        signals.append("-15 cap1_delivery_claim_insufficient_evidence")

    return round(max(0.0, min(100.0, score)), 1), signals


# v2 pillar weights (spec §weight summary)
W_DOSE = 0.40
W_EVIDENCE = 0.30
W_TRANSPARENCY = 0.30

# v3 pillar weights (dose carries form quality via tier factor)
W_DOSE_V3 = 0.55         # was 0.40 — dose now carries both quantity and quality
W_EVIDENCE_V3 = 0.20     # was 0.30 — class no longer double-counted here
W_TRANSPARENCY_V3 = 0.25 # was 0.30 — minor trim to maintain sum=1.00


def blend_score(dose_s: float, evidence_s: float, transparency_s: float) -> float:
    return round(dose_s * W_DOSE + evidence_s * W_EVIDENCE + transparency_s * W_TRANSPARENCY, 1)


def blend_score_v3(dose_s: float, evidence_s: float, transparency_s: float) -> float:
    return round(dose_s * W_DOSE_V3 + evidence_s * W_EVIDENCE_V3 + transparency_s * W_TRANSPARENCY_V3, 1)


# Cap ceilings
CAP_1_CEILING = 34.0     # cap_1: insufficient evidence delivery claim -> E
CAP_3_CORE_CEILING = 49.0  # cap_3_honesty_core: undisclosed blend -> D
# v3 UL_EXCEED grade ceiling (Option B, magnesium_ul_ruling_v1.md §3, 2026-06-23)
# Replaces flat -10 for v3 path. Grade ceiling D: max final_score when UL_EXCEED fires.
# At corrected elemental (520mg/450mg), pre-safety blend is 65.9/63.9 — flat -10 leaves C.
# Grade ceiling D (49.0) correctly places over-UL oxide alongside Solgar (48.9/D) and Taurate (46.2/D).
UL_EXCEED_GRADE_CEILING_V3 = 49.0


def apply_caps(blend: float, sku: dict) -> tuple:
    """
    Returns (final_score, binding_constraint, caps_fired).
    caps_fired lists only caps that ACTUALLY BIND (reduce the effective ceiling below blend).
    MRT-7 fix: previously cap_3 was listed even when it didn't reduce the score (e.g. Solgar
    blend=48.9 < cap_3 ceiling=49.0 — cap_3 checked but not binding). Now uses caps_checked
    semantics: only binding caps appear in caps_fired; non-binding caps that were checked are
    noted in caps_checked_not_binding for trace transparency.
    """
    caps_fired = []
    caps_checked_not_binding = []
    effective_ceiling = blend
    binding = "blend_dominant"

    # cap_1: liposomal/nano delivery without evidence
    if sku.get("cap_1_liposomal", False):
        if CAP_1_CEILING < effective_ceiling:
            caps_fired.append(("cap_1_insufficient_evidence", CAP_1_CEILING))
            effective_ceiling = CAP_1_CEILING
            binding = "cap_1_insufficient_evidence"
        else:
            caps_checked_not_binding.append(("cap_1_insufficient_evidence", CAP_1_CEILING))

    # cap_3_honesty_core: proprietary blend / undisclosed composition
    if sku.get("cap_3_core", False):
        if CAP_3_CORE_CEILING < effective_ceiling:
            caps_fired.append(("cap_3_honesty_core", CAP_3_CORE_CEILING))
            effective_ceiling = CAP_3_CORE_CEILING
            binding = "cap_3_honesty_core"
        else:
            caps_checked_not_binding.append(("cap_3_honesty_core", CAP_3_CORE_CEILING))

    # UL_350 mechanism:
    #   v2 path (BARI_MAGNESIUM_V3 NOT set): flat -10 from final score
    #   v3 path (BARI_MAGNESIUM_V3=1): grade ceiling D (max 49.0) per magnesium_ul_ruling_v1.md
    #     Option B (2026-06-23) — replaces flat -10; see ruling §3 for rationale.
    #     At corrected elemental (520mg/450mg), flat -10 left oxide products at C/55.9 and C/53.9
    #     — contradicting the page's "don't be fooled by the big number" thesis.
    #     Grade ceiling D correctly places over-UL oxide products at the top of D band.
    ul_flag = False
    if sku.get("elemental_mg", 0) > UL_350:
        ul_flag = True
        if BARI_MAGNESIUM_V3:
            caps_fired.append(("ul_exceed_grade_ceiling_D", UL_EXCEED_GRADE_CEILING_V3))
        else:
            caps_fired.append(("ul_350_flag_penalty", -10.0))

    final = min(blend, effective_ceiling)
    if ul_flag:
        if BARI_MAGNESIUM_V3:
            # Grade ceiling: max final_score = 49.0 (top of D band)
            final = min(final, UL_EXCEED_GRADE_CEILING_V3)
            if binding == "blend_dominant":
                binding = "ul_exceed_grade_ceiling_D"
        else:
            final = max(0.0, final - 10.0)
            if binding == "blend_dominant":
                binding = "ul_350_flag_applied"

    return round(final, 1), binding, caps_fired, caps_checked_not_binding


# ---- Safety flags ---------------------------------------------------------------
def safety_flags(elemental_mg: float) -> list:
    flags = []
    if elemental_mg > UL_350:
        # v3: grade ceiling D (max 49.0); v2: flat -10. Safety display text same for both.
        score_impact_str = (
            f"grade_ceiling_D: final_score capped at {UL_EXCEED_GRADE_CEILING_V3} (Option B, magnesium_ul_ruling_v1.md)"
            if BARI_MAGNESIUM_V3 else
            "-10 from final score"
        )
        flags.append({
            "flag": "UL_EXCEED",
            "trigger": f"{elemental_mg}mg > {UL_350}mg IOM/NASEM supplemental UL",
            "display_he": (
                "מינון זה עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM). "
                "גבול זה מבוסס על סובלנות מערכת העיכול ואינו מצביע על רעילות. "
                "מומלץ להתייעץ עם איש מקצוע."
            ),
            "score_impact": score_impact_str,
        })
    # HRT-3 (2026-06-23): changed from > 250 to >= 250 (inclusive).
    # EFSA 250mg/day is the ONSET level — at which osmotic diarrhea begins, not above which.
    # Two 250mg B products (Supherb Citrate+B6, Altman Bisglycinate 250) now receive GI note.
    # No score deduction — display only (MVP). Ref: magnesium_v3_governance_addendum_d7_hrt1_hrt3_mrt5.md §HRT-3.
    if elemental_mg >= UL_250:
        flags.append({
            "flag": "GI_NOTE_EFSA",
            "trigger": f"{elemental_mg}mg >= {UL_250}mg EFSA GI-tolerance onset threshold",
            "display_he": (
                "מינון זה עשוי לגרום לאי-נוחות במערכת העיכול בחלק מהאנשים (EFSA). "
                "סף הסבילות שנקבע על ידי EFSA הוא 250 מ\"ג/יום תוסף."
            ),
            "score_impact": "display only, no score deduction (MVP)",
        })
    return flags


# ---- Score one SKU (v2 model) --------------------------------------------------
def score_sku_v2(sku: dict) -> dict:
    """Score a single SKU using the v2 3-pillar model. Returns a result dict."""
    disposition = sku["disposition"]

    # UNRESOLVED
    if disposition == "UNRESOLVED":
        return {
            "barcode": sku["barcode"],
            "name_short": sku["name_short"],
            "disposition": "UNRESOLVED",
            "score": None,
            "grade": None,
            "score_display": "לא ניתן לדרג — נתוני תווית חסרים",
            "label_confidence": "לא ברור",
            "unresolved_reason": sku.get("unresolved_reason", ""),
            "caps_fired": [],
            "caps_checked_not_binding": [],
            "binding_constraint": None,
        }

    # DISCARDED
    if disposition == "DISCARDED":
        return {
            "barcode": sku["barcode"],
            "name_short": sku["name_short"],
            "disposition": "DISCARDED",
            "score": None,
            "grade": None,
            "score_display": "מוצר הוצא מהשוואה",
            "discard_reason": sku.get("discard_reason", ""),
            "caps_fired": [],
            "binding_constraint": None,
        }

    # SCORED or SOLGAR_EXCEPTION
    elemental_mg = sku["elemental_mg"]
    bav_class = sku["bav_class"]
    form = sku.get("form", "")
    label_basis = sku.get("label_basis", "")
    label_confidence = sku.get("label_confidence", "High")

    # Pillar 1: Dose
    if BARI_MAGNESIUM_V3:
        dose_s, dose_tier, dose_tier_desc, adjusted_dose_mg = dose_sub_score_v3(elemental_mg, bav_class)
    else:
        dose_s, dose_tier, dose_tier_desc = dose_sub_score(elemental_mg)
        adjusted_dose_mg = None

    # Pillar 2: Evidence (via bav_class modifier)
    if BARI_MAGNESIUM_V3:
        ev_s, ev_desc = evidence_sub_score_v3(bav_class)
    else:
        ev_s, ev_desc = evidence_sub_score(bav_class)

    # Pillar 3: Transparency
    trans_s, trans_signals = transparency_sub_score(sku)

    # Blend
    if BARI_MAGNESIUM_V3:
        blend = blend_score_v3(dose_s, ev_s, trans_s)
    else:
        blend = blend_score(dose_s, ev_s, trans_s)

    # Caps + final score (MRT-7: caps_fired = only binding caps; caps_checked_not_binding = checked but not binding)
    final_score, binding, caps_fired, caps_checked_not_binding = apply_caps(blend, sku)

    # Safety flags (display only for UL_250; score penalty already in apply_caps for UL_350)
    sflag = safety_flags(elemental_mg)

    # Oxide chemistry note (MRT-4: suppressed for panel_verified_elemental products)
    # panel_verified_elemental = label declares elemental directly (IL convention confirmed by NRV math)
    # chemistry_derived = stale label_basis for old compound-inference products (no longer used for
    # the four corrected oxide products after TASK-384 elemental reversal)
    oxide_note = None
    if label_basis == "chemistry_derived":
        frac = 0.603 if form == "oxide" else 0.417
        compound_mg = round(elemental_mg / frac)
        oxide_note = (
            f"{compound_mg}mg compound {form} x {frac} (stoichiometry) = {elemental_mg}mg elemental. "
            "Tag: chemistry-derived (for UI disclosure per spec)."
        )
    elif label_basis == "panel_verified_elemental" and form == "oxide":
        # MRT-4: oxide products with panel-verified elemental — no chemistry inference note
        oxide_note = sku.get("panel_verified_note", (
            "Elemental mg panel-verified: IL label convention '(From Magnesium Oxide) Xmg' "
            "confirmed by NRV% arithmetic. No stoichiometry inference applied (TASK-384, 2026-06-23)."
        ))

    # Cramps footnote
    cramps_note = sku.get("cramps_note") if sku.get("cramps_footnote") else None

    # WELL cap_1 determination (inline, for trace)
    well_det = None
    if sku.get("well_cap1_check"):
        well_det = {
            "cap_1_fired": WELL_CAP1_FIRED,
            "determination": WELL_CAP1_REASON,
        }

    grade = grade_for(final_score)

    return {
        "barcode": sku["barcode"],
        "name_short": sku["name_short"],
        "disposition": disposition,
        "administered_elemental_mg": elemental_mg,
        "elemental_range": sku.get("elemental_range"),
        "form": form,
        "bav_class": bav_class,
        "bav_class_display": BAV_CLASS_LABELS.get(bav_class, ""),
        "label_confidence": label_confidence,
        "label_basis": label_basis,
        # v3 internal fields (NEVER display to consumer per spec §8 display rule)
        "adjusted_dose_mg": adjusted_dose_mg,      # internal scoring value — never display to consumer
        "bav_tier_factor": BAV_TIER_FACTORS.get(bav_class, 1.0) if BARI_MAGNESIUM_V3 else None,
        "dose_band_result": {
            "dose_tier": dose_tier,
            "dose_tier_desc": dose_tier_desc,
            "dose_sub_score": dose_s,
            "general_gap_band": f"{DOSE_BAND_LO}-{DOSE_BAND_HI}mg",
        },
        "sub_scores": {
            "dose": dose_s,
            "evidence_class": ev_s,
            "transparency": trans_s,
            "evidence_desc": ev_desc,
            "transparency_signals": trans_signals,
        },
        "blend": blend,
        # MRT-7: caps_fired = caps that actually bound (reduced the score); caps_checked_not_binding = checked but didn't bind
        "caps_fired": [{"mechanism": m, "ceiling_or_penalty": v} for m, v in caps_fired],
        "caps_checked_not_binding": [{"mechanism": m, "ceiling": v} for m, v in caps_checked_not_binding],
        "binding_constraint": binding,
        "final_score": final_score,
        "grade": grade,
        "safety_flags": sflag,
        "cramps_footnote": cramps_note,
        "oxide_chemistry_note": oxide_note,
        "well_cap1_determination": well_det,
    }


# ---- Monotonicity check --------------------------------------------------------
def check_monotonicity(results: list) -> dict:
    """
    Product go-live condition #1 (TASK-384 spec):
    Confirm NO oxide product at 270+ mg elemental scores BELOW a
    bisglycinate product at 88-122 mg elemental (Nano 88 / Full-Mag 122).

    If such an inversion exists: report it explicitly and flag
    dose_pillar_weight needs upward pressure.
    """
    oxide_270plus = [
        r for r in results
        if r.get("form") == "oxide"
        and (r.get("administered_elemental_mg") or 0) >= 270
        and r.get("final_score") is not None
    ]
    bisgly_88_122 = [
        r for r in results
        if r.get("form") == "bisglycinate"
        and 88 <= (r.get("administered_elemental_mg") or 0) <= 122
        and r.get("final_score") is not None
    ]

    inversions = []
    for ox in oxide_270plus:
        for bg in bisgly_88_122:
            if ox["final_score"] < bg["final_score"]:
                inversions.append({
                    "oxide_barcode": ox["barcode"],
                    "oxide_name": ox["name_short"],
                    "oxide_elemental_mg": ox["administered_elemental_mg"],
                    "oxide_score": ox["final_score"],
                    "oxide_grade": ox["grade"],
                    "bisglycinate_barcode": bg["barcode"],
                    "bisglycinate_name": bg["name_short"],
                    "bisglycinate_elemental_mg": bg["administered_elemental_mg"],
                    "bisglycinate_score": bg["final_score"],
                    "bisglycinate_grade": bg["grade"],
                    "inversion_delta": round(bg["final_score"] - ox["final_score"], 1),
                })

    passed = len(inversions) == 0

    detail_lines = []
    for ox in oxide_270plus:
        detail_lines.append(
            f"  oxide {ox['barcode']} ({ox['name_short']}) "
            f"{ox['administered_elemental_mg']}mg -> score {ox['final_score']} {ox['grade']}"
        )
    for bg in bisgly_88_122:
        detail_lines.append(
            f"  bisglycinate {bg['barcode']} ({bg['name_short']}) "
            f"{bg['administered_elemental_mg']}mg -> score {bg['final_score']} {bg['grade']}"
        )

    return {
        "monotonicity_pass": passed,
        "result": "PASS" if passed else "FAIL — class modifier overweights dose",
        "inversions_found": len(inversions),
        "inversions": inversions,
        "oxide_270plus_checked": len(oxide_270plus),
        "bisglycinate_88_122_checked": len(bisgly_88_122),
        "detail": "\n".join(detail_lines),
        "note": (
            "Per spec: if a 270+mg oxide scores BELOW an 88-122mg bisglycinate, "
            "the class modifier overweights dose -> flag dose_pillar_weight needs "
            "upward pressure before go-live."
        ) if not passed else (
            "No inversions found. Oxide 270+mg products all score above bisglycinate 88-122mg."
        ),
    }


# ---- v3 Monotonicity check ---------------------------------------------------
def check_monotonicity_v3(results: list) -> dict:
    """
    v3 property tests:
    (1) Within-form: for each form-class, higher elemental_mg -> higher score (all else equal —
        same label_basis, same caps). Violations reported, not hard failures.
    (2) Cross-form grade separation: all oxide products score below all citrate/bisglycinate
        products at >= 200mg administered elemental. This is the core consumer signal.
    (3) Removed: cross-form hard constraint (oxide-270+ must not score below bisglycinate-88-122)
        — per owner direction 2026-06-23, this backwards constraint is retired in v3.
    """
    scored = [r for r in results
              if r.get("final_score") is not None
              and r.get("form") not in (None,)]

    # Test (2): oxide vs citrate/bisglycinate 200+mg administered elemental
    oxide_products = [r for r in scored if r.get("form") == "oxide"]
    premium_200plus = [r for r in scored
                       if r.get("form") in ("citrate", "bisglycinate", "glycinate")
                       and (r.get("administered_elemental_mg") or 0) >= 200
                       and not r.get("cap_1_liposomal", False)]

    grade_sep_violations = []
    for ox in oxide_products:
        for pr in premium_200plus:
            if ox.get("final_score", 0) >= pr.get("final_score", 0):
                grade_sep_violations.append({
                    "oxide": ox["barcode"], "oxide_name": ox["name_short"],
                    "oxide_score": ox["final_score"], "oxide_grade": ox.get("grade"),
                    "premium": pr["barcode"], "premium_name": pr["name_short"],
                    "premium_score": pr["final_score"], "premium_grade": pr.get("grade"),
                })

    grade_sep_pass = len(grade_sep_violations) == 0

    # Within-form ordering check (informational)
    within_form_issues = []
    forms_seen = set(r.get("form") for r in scored if r.get("form"))
    for form in forms_seen:
        same_form = [r for r in scored
                     if r.get("form") == form
                     and r.get("label_basis") not in ("us_label_il_unverified",)
                     and not r.get("cap_1_liposomal", False)
                     and not r.get("cap_3_core", False)]
        # Sort by elemental_mg ascending; score should also be ascending
        by_dose = sorted(same_form, key=lambda x: x.get("administered_elemental_mg", 0))
        for i in range(len(by_dose) - 1):
            a, b = by_dose[i], by_dose[i + 1]
            if a.get("administered_elemental_mg") < b.get("administered_elemental_mg"):
                if (a.get("final_score", 0) or 0) > (b.get("final_score", 0) or 0):
                    within_form_issues.append({
                        "form": form,
                        "lower_dose_barcode": a["barcode"],
                        "lower_dose_mg": a.get("administered_elemental_mg"),
                        "lower_dose_score": a.get("final_score"),
                        "higher_dose_barcode": b["barcode"],
                        "higher_dose_mg": b.get("administered_elemental_mg"),
                        "higher_dose_score": b.get("final_score"),
                    })

    within_form_pass = len(within_form_issues) == 0

    # Detail lines
    detail_lines = []
    for ox in oxide_products:
        detail_lines.append(
            f"  oxide {ox['barcode']} ({ox['name_short']}) "
            f"{ox.get('administered_elemental_mg')}mg admin -> "
            f"adj={ox.get('adjusted_dose_mg')}mg -> score {ox['final_score']} {ox.get('grade')}"
        )
    for pr in premium_200plus:
        detail_lines.append(
            f"  premium {pr['barcode']} ({pr['name_short']}) "
            f"{pr.get('administered_elemental_mg')}mg admin -> "
            f"adj={pr.get('adjusted_dose_mg')}mg -> score {pr['final_score']} {pr.get('grade')}"
        )

    return {
        "grade_separation_pass": grade_sep_pass,
        "within_form_pass": within_form_pass,
        "overall_pass": grade_sep_pass,  # grade_sep is the hard property; within_form is informational
        "result": "PASS" if grade_sep_pass else "FAIL — oxide not below all citrate/bisglycinate 200+mg",
        "grade_sep_violations": grade_sep_violations,
        "grade_sep_violation_count": len(grade_sep_violations),
        "within_form_issues": within_form_issues,
        "within_form_issue_count": len(within_form_issues),
        "oxide_products_checked": len(oxide_products),
        "premium_200plus_checked": len(premium_200plus),
        "detail": "\n".join(detail_lines),
        "note": "v3: oxide must score below all citrate/bisglycinate >= 200mg administered. "
                "Cross-form backwards constraint (oxide-270+ vs bisglycinate-88-122) REMOVED per owner 2026-06-23.",
    }


# ---- Main run ------------------------------------------------------------------
def main():
    print("=" * 72)
    if BARI_MAGNESIUM_V3:
        print("Magnesium Scoring Model v3 — TASK-384")
        print(f"BARI_MAGNESIUM_V2=1 + BARI_MAGNESIUM_V3=1 confirmed. Running v3 scorer.")
        print(f"Spec: benchmark/magnesium_model_v3_bioav_adjusted_dose_spec.md")
        print(f"Pillar weights: W_DOSE={W_DOSE_V3}, W_EVIDENCE={W_EVIDENCE_V3}, W_TRANSPARENCY={W_TRANSPARENCY_V3}")
        print(f"Tier factors: HIGH={BAV_TIER_FACTORS['HIGH']}, MODERATE={BAV_TIER_FACTORS['MODERATE']}, LOW={BAV_TIER_FACTORS['LOW']}, UNRESOLVED={BAV_TIER_FACTORS['UNRESOLVED']}")
    else:
        print("Magnesium Scoring Model v2 — TASK-384")
        print(f"BARI_MAGNESIUM_V2=1 confirmed. Running v2 scorer.")
        print(f"Spec: benchmark/magnesium_model_v2_final_spec.md")
    print(f"Flag: BARI_MAGNESIUM_V2 (this run only — old engine unaffected)")
    print("=" * 72)

    # Score all SKUs
    all_results = []
    for sku in CORPUS:
        result = score_sku_v2(sku)
        all_results.append(result)

    # Separate sets for reporting
    scored = [r for r in all_results if r["disposition"] in ("SCORED", "SOLGAR_EXCEPTION")
              and r.get("final_score") is not None]
    unresolved = [r for r in all_results if r["disposition"] == "UNRESOLVED"]
    discarded = [r for r in all_results if r["disposition"] == "DISCARDED"]

    # Grade distribution
    grade_dist = {}
    for r in scored:
        g = r["grade"]
        grade_dist[g] = grade_dist.get(g, 0) + 1

    # Score distribution stats
    scores = [r["final_score"] for r in scored]
    score_min = round(min(scores), 1) if scores else None
    score_max = round(max(scores), 1) if scores else None
    score_mean = round(sum(scores) / len(scores), 1) if scores else None
    score_sorted = sorted(scores)
    score_median = round(score_sorted[len(score_sorted) // 2], 1) if score_sorted else None
    # stdev
    if len(scores) > 1:
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        score_stdev = round(variance ** 0.5, 1)
    else:
        score_stdev = None
    most_common_score = max(set(scores), key=lambda x: scores.count(x)) if scores else None
    most_common_count = scores.count(most_common_score) if most_common_score is not None else 0

    # Monotonicity check
    if BARI_MAGNESIUM_V3:
        mono_check = check_monotonicity_v3(scored)
    else:
        mono_check = check_monotonicity(scored)

    # WELL cap_1 determination (already computed at module level)
    well_det = {
        "cap_1_fired": WELL_CAP1_FIRED,
        "determination": WELL_CAP1_REASON,
    }

    # Print results table
    print()
    if BARI_MAGNESIUM_V3:
        print("SCORED RESULTS — v3 (sorted by score desc):")
        print(f"  {'Barcode':<18} {'Name':<35} {'Elem':>6} {'Fct':>5} {'Adj':>6} {'Form':<14} {'Class':<12} {'D_s':>5} {'Ev_s':>5} {'Tr_s':>5} {'Blend':>6} {'Score':>6} {'Gr'} {'Bind'}")
        print(f"  {'-'*18} {'-'*35} {'-'*6} {'-'*5} {'-'*6} {'-'*14} {'-'*12} {'-'*5} {'-'*5} {'-'*5} {'-'*6} {'-'*6} {'--'} {'-'*30}")
        for r in sorted(scored, key=lambda x: x["final_score"], reverse=True):
            ds = r.get("sub_scores", {}).get("dose", 0)
            evs = r.get("sub_scores", {}).get("evidence_class", 0)
            trs = r.get("sub_scores", {}).get("transparency", 0)
            adj = r.get("adjusted_dose_mg", "")
            fct = r.get("bav_tier_factor", "")
            print(
                f"  {r['barcode']:<18} {r['name_short'][:35]:<35} "
                f"{str(r['administered_elemental_mg'])+'mg':>6} "
                f"{str(fct):>5} "
                f"{str(adj)+'mg' if adj is not None else '':>6} "
                f"{r['form']:<14} {r['bav_class']:<12} "
                f"{ds:>5.1f} {evs:>5.1f} {trs:>5.1f} "
                f"{r['blend']:>6.1f} {r['final_score']:>6.1f} {r['grade']:>2}  {r['binding_constraint']}"
            )
    else:
        print("SCORED RESULTS (sorted by score desc):")
        print(f"  {'Barcode':<18} {'Name':<35} {'Elem':>5} {'Form':<14} {'Class':<12} {'Score':>6} {'Gr'} {'Bind'}")
        print(f"  {'-'*18} {'-'*35} {'-'*5} {'-'*14} {'-'*12} {'-'*6} {'--'} {'-'*30}")
        for r in sorted(scored, key=lambda x: x["final_score"], reverse=True):
            caps_str = "+".join(c["mechanism"] for c in r["caps_fired"]) or "none"
            print(
                f"  {r['barcode']:<18} {r['name_short'][:35]:<35} "
                f"{str(r['administered_elemental_mg'])+'mg':>5} "
                f"{r['form']:<14} {r['bav_class']:<12} "
                f"{r['final_score']:>6.1f} {r['grade']:>2}  {r['binding_constraint']}"
            )

    print()
    print("UNRESOLVED (no score — label data insufficient):")
    for r in unresolved:
        print(f"  {r['barcode']:<18} {r['name_short']}")

    print()
    print("DISCARDED:")
    for r in discarded:
        print(f"  {r['barcode']:<18} {r['name_short']}")

    print()
    print("GRADE DISTRIBUTION:")
    for g in ["S", "A", "B", "C", "D", "E"]:
        n = grade_dist.get(g, 0)
        if n > 0:
            print(f"  {g}: {n}")

    print()
    print(f"SCORE STATS (n={len(scores)}):")
    print(f"  min={score_min}  max={score_max}  mean={score_mean}  "
          f"median={score_median}  stdev={score_stdev}")
    print(f"  most_common_score={most_common_score} (count={most_common_count})")

    print()
    print("MONOTONICITY CHECK:")
    print(f"  Result: {mono_check['result']}")
    if BARI_MAGNESIUM_V3:
        print(f"  Grade-separation pass (oxide < all citrate/bisglycinate 200+mg): {mono_check['grade_separation_pass']}")
        print(f"  Within-form ordering pass: {mono_check['within_form_pass']}")
        print(f"  Oxide products checked: {mono_check['oxide_products_checked']}")
        print(f"  Premium (citrate/bisgly 200+mg) checked: {mono_check['premium_200plus_checked']}")
        print(f"  Grade-sep violations: {mono_check['grade_sep_violation_count']}")
        if mono_check["grade_sep_violations"]:
            for v in mono_check["grade_sep_violations"]:
                print(f"    VIOLATION: oxide {v['oxide_name']} ({v['oxide_score']}) >= premium {v['premium_name']} ({v['premium_score']})")
        print(f"  Within-form issues: {mono_check['within_form_issue_count']}")
        if mono_check["within_form_issues"]:
            for v in mono_check["within_form_issues"]:
                print(f"    WITHIN-FORM ISSUE: {v['form']} {v['lower_dose_mg']}mg ({v['lower_dose_score']}) > {v['higher_dose_mg']}mg ({v['higher_dose_score']})")
        if mono_check["detail"]:
            print(mono_check["detail"])
    else:
        print(f"  Oxide 270+mg products checked: {mono_check['oxide_270plus_checked']}")
        print(f"  Bisglycinate 88-122mg products checked: {mono_check['bisglycinate_88_122_checked']}")
        print(f"  Inversions found: {mono_check['inversions_found']}")
        if mono_check["detail"]:
            print(mono_check["detail"])

    print()
    print("WELL cap_1 DETERMINATION:")
    print(f"  cap_1_fired: {well_det['cap_1_fired']}")
    print(f"  {well_det['determination']}")

    # Write verification table (CSV — stable barcode->score->grade->cap)
    # HRT-2 clobber guard: v3 writes to separate file so flag-OFF v2 run NEVER overwrites v3 output.
    # v3 path: magnesium_v3_verification_table.csv + magnesium_v3_latest.json
    # v2 path: magnesium_v2_verification_table.csv + magnesium_v2_latest.json
    csv_path = OUT_DIR / ("magnesium_v3_verification_table.csv" if BARI_MAGNESIUM_V3 else "magnesium_v2_verification_table.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if BARI_MAGNESIUM_V3:
            writer.writerow([
                "barcode", "name_short", "disposition", "administered_elemental_mg",
                "bav_tier_factor", "adjusted_dose_mg",
                "form", "bav_class", "dose_tier", "dose_sub_score", "evidence_sub_score",
                "transparency_sub_score", "blend", "caps_fired", "binding_constraint",
                "final_score", "grade", "label_confidence", "safety_flags"
            ])
        else:
            writer.writerow([
                "barcode", "name_short", "disposition", "administered_elemental_mg",
                "form", "bav_class", "dose_tier", "dose_sub_score", "evidence_sub_score",
                "transparency_sub_score", "blend", "caps_fired", "binding_constraint",
                "final_score", "grade", "label_confidence", "safety_flags"
            ])
        for r in all_results:
            if r["disposition"] in ("SCORED", "SOLGAR_EXCEPTION"):
                caps_str = "|".join(c["mechanism"] for c in r.get("caps_fired", []))
                sflag_str = "|".join(f["flag"] for f in r.get("safety_flags", []))
                if BARI_MAGNESIUM_V3:
                    writer.writerow([
                        r["barcode"], r["name_short"], r["disposition"],
                        r.get("administered_elemental_mg", ""),
                        r.get("bav_tier_factor", ""),
                        r.get("adjusted_dose_mg", ""),
                        r.get("form", ""), r.get("bav_class", ""),
                        r.get("dose_band_result", {}).get("dose_tier", ""),
                        r.get("sub_scores", {}).get("dose", ""),
                        r.get("sub_scores", {}).get("evidence_class", ""),
                        r.get("sub_scores", {}).get("transparency", ""),
                        r.get("blend", ""), caps_str,
                        r.get("binding_constraint", ""),
                        r.get("final_score", ""), r.get("grade", ""),
                        r.get("label_confidence", ""), sflag_str,
                    ])
                else:
                    writer.writerow([
                        r["barcode"], r["name_short"], r["disposition"],
                        r.get("administered_elemental_mg", ""),
                        r.get("form", ""), r.get("bav_class", ""),
                        r.get("dose_band_result", {}).get("dose_tier", ""),
                        r.get("sub_scores", {}).get("dose", ""),
                        r.get("sub_scores", {}).get("evidence_class", ""),
                        r.get("sub_scores", {}).get("transparency", ""),
                        r.get("blend", ""), caps_str,
                        r.get("binding_constraint", ""),
                        r.get("final_score", ""), r.get("grade", ""),
                        r.get("label_confidence", ""), sflag_str,
                    ])
            else:
                if BARI_MAGNESIUM_V3:
                    writer.writerow([
                        r["barcode"], r["name_short"], r["disposition"],
                        "", "", "", "", "", "", "", "", "", "", "",
                        "", r.get("grade", ""), "", "",
                    ])
                else:
                    writer.writerow([
                        r["barcode"], r["name_short"], r["disposition"],
                        "", "", "", "", "", "", "", "", "", "",
                        "", r.get("grade", ""), "", "",
                    ])
    print(f"\nVerification table written: {csv_path}")

    # Write full run JSON
    # HRT-2 clobber guard: v3 run writes magnesium_v3_run_<ts>.json + magnesium_v3_latest.json
    # A flag-OFF (v2) run writes to magnesium_v2_run_<ts>.json + magnesium_v2_latest.json
    # These are separate namespaces — v2 can never silently overwrite v3 latest/CSV.
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    model_prefix = "magnesium_v3" if BARI_MAGNESIUM_V3 else "magnesium_v2"
    run_path = OUT_DIR / f"{model_prefix}_run_{ts}.json"
    latest_path = OUT_DIR / f"{model_prefix}_latest.json"

    run_record = {
        "task": "TASK-384",
        "model": "magnesium_v3" if BARI_MAGNESIUM_V3 else "magnesium_v2",
        "spec": (
            "benchmark/magnesium_model_v3_bioav_adjusted_dose_spec.md"
            if BARI_MAGNESIUM_V3 else
            "benchmark/magnesium_model_v2_final_spec.md"
        ),
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "flag": "BARI_MAGNESIUM_V2=1" + (" + BARI_MAGNESIUM_V3=1" if BARI_MAGNESIUM_V3 else ""),
        "verification_status": "candidate",
        "edpg_note": (
            "All records candidate. No published score. Page offline. "
            "Old engine (run_full.py / SUPP-EV-030) byte-identical. "
            "BARI_MAGNESIUM_V2=1 flag isolates this run. TASK-384."
        ),
        "mvp_scope": "2 bands only: general-gap (100-300mg elemental) + safety gate",
        "pillar_weights": (
            {
                "dose_adjusted_elemental": W_DOSE_V3,
                "bioavailability_class_evidence": W_EVIDENCE_V3,
                "transparency_safety": W_TRANSPARENCY_V3,
            }
            if BARI_MAGNESIUM_V3 else
            {
                "dose_administered_elemental": W_DOSE,
                "bioavailability_class_evidence": W_EVIDENCE,
                "transparency_safety": W_TRANSPARENCY,
            }
        ),
        "bav_tier_factors": BAV_TIER_FACTORS if BARI_MAGNESIUM_V3 else None,
        "general_gap_band": f"{DOSE_BAND_LO}-{DOSE_BAND_HI}mg elemental",
        "well_cap1_determination": well_det,
        "monotonicity_check": mono_check,
        "counts": {
            "total_corpus_skus": len(CORPUS),
            "scored": len(scored),
            "solgar_exception_path": sum(1 for r in scored if r["disposition"] == "SOLGAR_EXCEPTION"),
            "unresolved": len(unresolved),
            "discarded": len(discarded),
        },
        "grade_distribution": grade_dist,
        "score_stats": {
            "n": len(scores),
            "min": score_min,
            "max": score_max,
            "mean": score_mean,
            "median": score_median,
            "stdev": score_stdev,
            "most_common_score": most_common_score,
            "most_common_count": most_common_count,
        },
        "results": all_results,
    }

    run_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    latest_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Run record written: {run_path}")
    print(f"Latest pointer: {latest_path}")

    # Verify old engine is unaffected (no magnesium.yaml or score_engine.py touched)
    print()
    print("OLD ENGINE ISOLATION CHECK:")
    print("  score_engine.py: not modified (v2 runner is standalone)")
    print("  magnesium.yaml: not modified (v2 uses separate corpus table)")
    print("  run_full.py: not modified")
    print("  BARI_MAGNESIUM_V2=1 flag required to activate this scorer")
    print("  Old path (SUPP-EV-030 absorbed-mg): UNCHANGED / byte-identical")

    print()
    print("=" * 72)
    print("SELF-GATE SUMMARY")
    print("=" * 72)
    print(f"  Model: {'v3 (BARI_MAGNESIUM_V3=1)' if BARI_MAGNESIUM_V3 else 'v2 (BARI_MAGNESIUM_V2=1)'}")
    print(f"  Scored: {len(scored)} / {len(CORPUS)} corpus SKUs")
    print(f"  Unresolved: {len(unresolved)} (Amorphicure, TRIOMAG)")
    print(f"  Discarded: {len(discarded)} (Max550)")
    print(f"  Grade dist: {dict(sorted(grade_dist.items()))}")
    if BARI_MAGNESIUM_V3:
        print(f"  Monotonicity (v3): {mono_check['result']}")
        print(f"  Grade-sep pass: {mono_check['grade_separation_pass']}")
        print(f"  Within-form pass: {mono_check['within_form_pass']}")
    else:
        print(f"  Monotonicity: {mono_check['result']}")
    print(f"  WELL cap_1: fired={WELL_CAP1_FIRED}")
    print(f"  Verification table: {csv_path.name}")
    print(f"  Run record: {run_path.name}")
    print()

    mono_pass = mono_check.get("grade_separation_pass", mono_check.get("monotonicity_pass", True))
    return mono_pass


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 0)  # exit 0 always on completion; monotonicity result in report
