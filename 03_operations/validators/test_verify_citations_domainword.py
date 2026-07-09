"""
test_verify_citations_domainword.py — TASK-528 regression suite
================================================================

Verifies TWO invariants introduced by the TASK-528 vocabulary extension:

  (A) GLP-1 / incretin / body-composition papers that previously produced a
      false MISMATCH (no shared food-domain word) now PASS _topic_consistent.
      Representative case: PMID 41877354 — "Lean Mass Changes With Incretin
      Therapy Versus Lifestyle Intervention: A Systematic Review and
      Meta-Analysis of RCTs" (*Diabetes Obes Metab* 2026).

  (B) The fabrication-detection path is UNWEAKENED.  Two negative controls:
      (B1) A citation whose resolved title contains a _RED_FLAG_WORDS term
           not present in the context — still produces MISMATCH.
      (B2) A citation with no shared domain words AND no red-flag collision —
           still produces MISMATCH (Rule 3 conservative fallback).

All tests are OFFLINE (no PubMed / CrossRef calls).  The test patches
_topic_consistent with realistic fixtured data drawn directly from the
PMIDs that surfaced the TASK-528 false-positive.

Exit 0  = all assertions pass.
Exit 1  = one or more assertions failed (printed to stdout).
"""
from __future__ import annotations

import sys
import os

# ---------------------------------------------------------------------------
# Ensure the validators directory is importable
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

# We also need the repo root on sys.path so verify_citations can import its
# own integrations clients (it handles ImportError gracefully).
_REPO_ROOT = os.path.dirname(os.path.dirname(_THIS_DIR))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from verify_citations import _topic_consistent, _RED_FLAG_WORDS, _FOOD_NUTRITION_WORDS


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _run_case(name: str, context: str, title: str, abstract: str,
              expect_consistent: bool) -> bool:
    consistent, reason = _topic_consistent(context, title, abstract)
    ok = consistent == expect_consistent
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}")
    print(f"           consistent={consistent}, expected={expect_consistent}")
    print(f"           reason: {reason}")
    if not ok:
        print(f"           *** ASSERTION FAILED ***")
    return ok


# ---------------------------------------------------------------------------
# (A) GLP-1 / incretin / body-composition papers must NOT false-MISMATCH
# ---------------------------------------------------------------------------

def test_glp1_lean_mass_pmid_41877354():
    """
    PMID 41877354 — the exact false-positive that triggered TASK-528.
    Title: "Lean Mass Changes With Incretin Therapy Versus Lifestyle
            Intervention: A Systematic Review and Meta-Analysis of RCTs"
    Journal: Diabetes Obes Metab 2026
    Context as it appears in GLP1_GUIDE_SCIENCE_COSIGN_v1.md (excerpt).
    Before TASK-528: no shared word → MISMATCH.
    After  TASK-528: "lean mass" + "incretin" in both title & context → PASS.
    """
    context = (
        "PMID:41877354 Lean Mass Changes With Incretin Therapy Versus Lifestyle "
        "Intervention systematic review meta-analysis RCTs GLP-1 lean mass loss "
        "body composition semaglutide 25-39% primary source Claim 1"
    )
    title = (
        "Lean Mass Changes With Incretin Therapy Versus Lifestyle Intervention: "
        "A Systematic Review and Meta-Analysis of RCTs"
    )
    abstract = (
        "Background: GLP-1 receptor agonists cause significant weight loss but "
        "their effects on lean mass versus fat mass are unclear. Methods: We "
        "conducted a systematic review and meta-analysis of randomized controlled "
        "trials. Results: Lean mass loss accounted for 25-39% of total weight "
        "loss with incretin therapy. Conclusions: Lean body mass is preserved "
        "better with lifestyle intervention than pharmacotherapy alone."
    )
    return _run_case(
        "A1 – PMID 41877354 GLP-1/incretin lean-mass meta-analysis (primary false-positive case)",
        context, title, abstract,
        expect_consistent=True,
    )


def test_glp1_body_composition_pmid_39719170():
    """
    PMID 39719170 — "Effect of GLP-1RAs and co-agonists on body composition"
    Corroborating paper for Claim 1; also affected by the false-positive.
    """
    context = (
        "PMID 39719170 GLP-1RAs co-agonists body composition network meta-analysis "
        "Metabolism 2025 lean mass fat mass weight loss semaglutide tirzepatide "
        "corroborating Claim 1 GLP-1 body composition"
    )
    title = (
        "Effect of GLP-1 receptor agonists and co-agonists on body composition: "
        "A systematic review and network meta-analysis"
    )
    abstract = (
        "GLP-1 receptor agonists and dual GIP/GLP-1 agonists reduce fat mass and "
        "total body weight in adults with obesity. Lean mass changes vary by agent. "
        "Semaglutide and tirzepatide show the greatest adiposity reduction. "
        "Body composition outcomes differ between incretin classes."
    )
    return _run_case(
        "A2 – PMID 39719170 GLP-1RA body-composition network meta-analysis",
        context, title, abstract,
        expect_consistent=True,
    )


def test_glp1_lean_body_mass_sglt2_pmid_42319968():
    """
    PMID 42319968 — "Effects of GLP-1RAs and SGLT2i on Lean Body Mass"
    """
    context = (
        "PMID 42319968 GLP-1RAs SGLT2i lean body mass humans systematic review "
        "meta-analysis Diabetes Metab Res Rev 2026 body composition weight loss "
        "corroborating Claim 1"
    )
    title = (
        "Effects of GLP-1 Receptor Agonists and SGLT2 Inhibitors on Lean Body "
        "Mass in Humans: A Systematic Review and Meta-Analysis"
    )
    abstract = (
        "We assessed changes in lean body mass with GLP-1 receptor agonists and "
        "SGLT2 inhibitors in randomised controlled trials in adults with type 2 "
        "diabetes or obesity. Both drug classes reduce total body weight; lean "
        "body mass loss is proportionally smaller with pharmacotherapy."
    )
    return _run_case(
        "A3 – PMID 42319968 GLP-1RA + SGLT2i lean body mass",
        context, title, abstract,
        expect_consistent=True,
    )


def test_incretin_weight_loss_body_composition_pmid_41996180():
    """
    PMID 41996180 — "Effect of Incretin-Based and Nonpharmacologic Weight Loss
    on Body Composition" — Ann Intern Med 2026
    """
    context = (
        "PMID 41996180 incretin-based nonpharmacologic weight loss body composition "
        "Ann Intern Med 2026 systematic review lean mass fat mass incretin therapy "
        "lifestyle corroborating Claim 1"
    )
    title = (
        "Effect of Incretin-Based and Nonpharmacologic Weight Loss on Body "
        "Composition: A Systematic Review"
    )
    abstract = (
        "Incretin-based pharmacotherapy produces greater total weight loss than "
        "lifestyle intervention alone, but the proportion of lean mass lost differs. "
        "Body composition outcomes from 32 randomised trials were meta-analysed. "
        "Lean mass fraction of total weight loss was higher with pharmacotherapy."
    )
    return _run_case(
        "A4 – PMID 41996180 incretin weight loss body composition",
        context, title, abstract,
        expect_consistent=True,
    )


def test_sarcopenia_glp1_pmid_42303931():
    """
    PMID 42303931 — "GLP-1RAs for Obesity Management in Older Adults: sarcopenia risk"
    """
    context = (
        "PMID 42303931 GLP-1RAs obesity management older adults sarcopenia risk "
        "scoping review Curr Nutr Rep 2026 lean mass protein intake"
    )
    title = (
        "GLP-1 Receptor Agonists for Obesity Management in Older Adults: "
        "Sarcopenia Risk and Mitigation Strategies"
    )
    abstract = (
        "Older adults with obesity who use GLP-1 receptor agonists face a risk of "
        "sarcopenic obesity. Adequate dietary protein intake and resistance exercise "
        "may mitigate lean mass loss. We review evidence from clinical trials on "
        "skeletal muscle outcomes with semaglutide and liraglutide in this population."
    )
    return _run_case(
        "A5 – PMID 42303931 GLP-1RA sarcopenia older adults",
        context, title, abstract,
        expect_consistent=True,
    )


# ---------------------------------------------------------------------------
# (B) Fabrication detection must remain unweakened
# ---------------------------------------------------------------------------

def test_red_flag_leukemia_still_mismatch():
    """
    B1 — Negative control: resolved title contains a _RED_FLAG_WORDS term
    ("leukemia") that is NOT in the context.  Rule 1 must still fire → MISMATCH.
    Simulates the classic fabrication pattern: context claims a nutrition paper
    but the PMID resolves to an oncology paper.
    """
    context = (
        "cheese dairy LDL cardiovascular PMID 99999991 fat saturated "
        "meta-analysis protein calcium"
    )
    title = (
        "Acute Myeloid Leukemia treatment outcomes with targeted therapy: "
        "a randomized phase III trial"
    )
    abstract = (
        "We evaluated targeted chemotherapy regimens for acute myeloid leukemia. "
        "Outcomes measured included complete remission rate and overall survival. "
        "No dietary intervention was included."
    )
    return _run_case(
        "B1 – red-flag 'leukemia' in resolved title absent from context → MISMATCH",
        context, title, abstract,
        expect_consistent=False,
    )


def test_no_shared_words_no_red_flag_still_mismatch():
    """
    B2 — Negative control: resolved title has NO shared domain word with context
    AND no red-flag word, context is not too short (> 40 chars).
    Rule 3 conservative fallback must still fire → MISMATCH.

    Design note: the context must NOT share ANY word from _FOOD_NUTRITION_WORDS
    with the paper title+abstract — that is exactly the MISMATCH condition.
    Here the context mentions cheese/butter/LDL but the paper is an orthopaedic
    surgical technique paper with zero nutrition/food/pharmacology vocabulary.
    "orthopedic" IS in _RED_FLAG_WORDS but we avoid it in the title to test
    the Rule-3 conservative fallback path independently of Rule 1.
    """
    # Context: legitimate nutrition evidence context
    context = (
        "cheese butter LDL saturated fatty acids PMID 99999992 "
        "crossover RCT serum lipids whole milk full-fat dairy"
    )
    # Paper: hip implant fixation — no food/nutrition/pharmacology words.
    # Deliberately avoids _RED_FLAG_WORDS terms ("orthopedic") so Rule 1 does
    # not fire; Rule 3 conservative fallback must catch this.
    title = (
        "Cementless hip implant fixation: ten-year follow-up of aseptic loosening"
    )
    abstract = (
        "We reviewed 412 primary total hip arthroplasties performed between 2010 "
        "and 2020. Aseptic loosening was the primary failure mode. Implant "
        "survival and Harris Hip Score were assessed at 2, 5 and 10 years. "
        "No correlation with patient body-mass-index was found in this series."
    )
    return _run_case(
        "B2 – unrelated surgical paper (hip arthroplasty), no red-flag word → MISMATCH (Rule 3)",
        context, title, abstract,
        expect_consistent=False,
    )


def test_red_flag_stroke_still_mismatch():
    """
    B3 — Additional negative control: "stroke" is a _RED_FLAG_WORDS term.
    Even though "cardiovascular" appears in context (which would normally pass
    Rule 2), the red-flag check (Rule 1) should fire first and block passage.
    """
    context = (
        "omega-3 fatty acid cardiovascular disease PMID 99999993 heart health "
        "dietary supplement fish oil meta-analysis"
    )
    title = (
        "Hemorrhagic stroke outcomes following anticoagulant therapy: "
        "a registry-based cohort study"
    )
    abstract = (
        "We investigated 30-day mortality after hemorrhagic stroke in patients "
        "receiving anticoagulation. Stroke severity and anticoagulant class "
        "were the primary predictors. No dietary interventions were studied."
    )
    return _run_case(
        "B3 – red-flag 'stroke' in resolved title absent from context → MISMATCH",
        context, title, abstract,
        expect_consistent=False,
    )


def test_glp1_word_in_context_matches_new_vocabulary():
    """
    Vocabulary sanity check: verify that the new TASK-528 terms are actually
    present in _FOOD_NUTRITION_WORDS (tests the data structure, not just logic).
    """
    required = {
        "glp-1", "glp1", "incretin", "lean mass", "lean body mass",
        "body composition", "sarcopenia", "weight loss", "semaglutide",
        "tirzepatide", "sglt2", "pharmacotherapy", "adiposity",
    }
    missing = required - _FOOD_NUTRITION_WORDS
    ok = len(missing) == 0
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] Vocabulary sanity – TASK-528 terms present in _FOOD_NUTRITION_WORDS")
    if missing:
        print(f"           MISSING terms: {sorted(missing)}")
        print(f"           *** ASSERTION FAILED ***")
    else:
        print(f"           All {len(required)} required terms confirmed present")
    return ok


def test_red_flag_words_unchanged():
    """
    Guard: verify that TASK-528 did NOT accidentally remove any _RED_FLAG_WORDS
    terms.  Tests the invariant that the fabrication-detection vocabulary is
    at least as strong as before the patch.
    """
    expected_red_flags = {
        "stroke", "cerebral", "leukemia", "leukaemia", "nursing",
        "dermatology", "ophthalmology", "orthopedic", "trauma",
        "surgery", "schizophrenia", "alzheimer", "epilepsy", "sepsis",
        "dialysis", "transplant", "spinal",
    }
    missing = expected_red_flags - _RED_FLAG_WORDS
    ok = len(missing) == 0
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] Red-flag invariant – no _RED_FLAG_WORDS terms removed")
    if missing:
        print(f"           MISSING from _RED_FLAG_WORDS: {sorted(missing)}")
        print(f"           *** ASSERTION FAILED ***")
    else:
        print(f"           All {len(expected_red_flags)} sentinel red-flag terms confirmed present")
    return ok


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 72)
    print("TASK-528 domain-word false-positive regression suite")
    print("(A) GLP-1/incretin/body-composition papers must PASS _topic_consistent")
    print("(B) Fabrication / wrong-paper detection must remain UNWEAKENED")
    print("=" * 72)

    results = []

    print("\n--- (A) GLP-1 / incretin false-positive cases ---")
    results.append(test_glp1_lean_mass_pmid_41877354())
    results.append(test_glp1_body_composition_pmid_39719170())
    results.append(test_glp1_lean_body_mass_sglt2_pmid_42319968())
    results.append(test_incretin_weight_loss_body_composition_pmid_41996180())
    results.append(test_sarcopenia_glp1_pmid_42303931())

    print("\n--- (B) Fabrication / wrong-paper negative controls ---")
    results.append(test_red_flag_leukemia_still_mismatch())
    results.append(test_no_shared_words_no_red_flag_still_mismatch())
    results.append(test_red_flag_stroke_still_mismatch())

    print("\n--- Structural invariants ---")
    results.append(test_glp1_word_in_context_matches_new_vocabulary())
    results.append(test_red_flag_words_unchanged())

    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"\n{'=' * 72}")
    print(f"Result: {passed}/{total} assertions passed")
    if passed == total:
        print("ALL PASS — TASK-528 regression suite complete")
    else:
        print(f"FAIL — {total - passed} assertion(s) failed")
    print("=" * 72)

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
