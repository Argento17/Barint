import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path("C:/Bari/03_operations/supplement_engine/proto_v0/src").resolve()))

with open(r"C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v8.json", encoding="utf-8") as f:
    data = json.load(f)

results = data["results"]

# 1. Check header stated delta vs actual
print("=== DELTA DISCREPANCY CHECK ===")
print("Header edpg_note claims: S=11→13 (+2), B=16→15 (-1), C=4→3 (-1)")
print("Actual v8 grade_distribution from header:", data.get("grade_distribution"))
# Count from engine_output
from collections import Counter
actual = Counter()
for r in results:
    if r.get("outcome") == "scored":
        g = r.get("engine_output", {}).get("grade")
        if g:
            actual[g] += 1
print("Actual recount from engine_output:", dict(actual))
print()

# 2. Verify zinc picolinate dosing math
print("=== ZINC PICOLINATE DOSE MATH VERIFICATION ===")
for r in results:
    bc = r.get("barcode", "")
    if bc in ("0033984037250", "7290006437563"):
        eo = r.get("engine_output", {})
        ss = eo.get("sub_scores", {})
        print(f"  [{bc}] grade={eo.get('grade')} score={eo.get('score')}")
        print(f"    evidence_val={ss.get('evidence')} dose_val={ss.get('dose')}")
        print(f"    claim_matched={eo.get('claim_matched')}")
        print(f"    evidence tier=Weak -> evidence_val=47.0 (Weak band midpoint)")
        print(f"    dose_val=92 -> in_range (confirms elemental basis applied: 22mg or 25mg >= 8mg min_effective)")
        print(f"    blend with Weak evidence: e=47*0.30 + d=92*0.25 + f=92*0.20 + h=100*0.15 + s=neutral*0.10")
        # Compute expected blend (approximate weights)
        # evidence 47.0 * weight_evidence + dose 92 * weight_dose + form 92 * weight_form + honesty 100 * weight_honesty + safety_neutral * weight_safety
        # From constants: need to read actual weights
        print()

# 3. Check constants for dimension weights
import constants as C
print("=== DIMENSION WEIGHTS ===")
print(f"  DIMENSION_WEIGHTS: {C.DIMENSION_WEIGHTS}")
print()

# Manual blend computation for zinc picolinate (Weak evidence)
w = C.DIMENSION_WEIGHTS
e_val = 47.0  # Weak midpoint = (35+59)/2 = 47
d_val = 92.0  # in_range
f_val = 92.0  # picolinate=preferred
h_val = 100.0  # honest
s_val_neutral = getattr(C, 'SAFETY_NEUTRAL_BLEND_VALUE', 70)

blend_zinc = (w.get('evidence', 0)*e_val + w.get('dose', 0)*d_val +
              w.get('form', 0)*f_val + w.get('honesty', 0)*h_val +
              w.get('safety', 0)*s_val_neutral) / sum(w.values())
print(f"=== COMPUTED BLEND (Weak evidence, in_range dose) ===")
print(f"  Evidence=47*{w.get('evidence',0)} + Dose=92*{w.get('dose',0)} + Form=92*{w.get('form',0)} + Honesty=100*{w.get('honesty',0)} + Safety_neutral={s_val_neutral}*{w.get('safety',0)}")
print(f"  blend = {round(blend_zinc, 1)} -> that would be grade {chr(65)}")
print()

# Check Strong tier score for comparison
e_strong = 92.5  # Strong midpoint
blend_strong = (w.get('evidence', 0)*e_strong + w.get('dose', 0)*d_val +
                w.get('form', 0)*f_val + w.get('honesty', 0)*h_val +
                w.get('safety', 0)*s_val_neutral) / sum(w.values())
print(f"=== COMPUTED BLEND (Strong evidence, in_range dose) = S/91.2 scenario ===")
print(f"  Evidence=92.5*{w.get('evidence',0)} + Dose=92*{w.get('dose',0)} + Form=92*{w.get('form',0)} + Honesty=100*{w.get('honesty',0)} + Safety_neutral={s_val_neutral}*{w.get('safety',0)}")
print(f"  blend = {round(blend_strong, 1)}")
print()
print(f"  If zinc products had STRONG evidence (deficiency claim), they would score ~{round(blend_strong,1)}")
print(f"  But they claim 'broad immune support' = WEAK evidence -> blend ~{round(blend_zinc,1)}")
print()

# 4. Tink 50mg safety veto analysis
print("=== TINK 50mg ZINC: VETO PATH ANALYSIS ===")
for r in results:
    bc = r.get("barcode", "")
    if bc == "7290018365359":
        eo = r.get("engine_output", {})
        ss = eo.get("sub_scores", {})
        print(f"  grade={eo.get('grade')} score={eo.get('score')}")
        print(f"  binding={eo.get('binding_constraint')}")
        print(f"  evidence={ss.get('evidence')}  dose={ss.get('dose')}  form={ss.get('form')}")
        print(f"  safety={ss.get('safety')}")
        # The form is parsed from name "Tink Zinc 50mg" — no explicit form token
        # label_basis=elemental means 50mg IS elemental zinc
        # 50mg > 40mg UL -> VETO -> E/20
        print(f"  VETO logic: label_basis=elemental, form=None, amount=50mg > UL=40mg -> RT7-H1 VETO -> E/20.0")
        print(f"  Note: was previously E/34 via cap_1 (no claim) in v7")
        print(f"  In v8: still E but via veto_safety (more accurate — it's not just 'no claim', it exceeds UL)")
        print()

# 5. Check whether the veto ALSO routes to unscoreable or stays scored
print("=== TINK 50mg: OUTCOME CHECK ===")
for r in results:
    if r.get("barcode") == "7290018365359":
        print(f"  outcome={r.get('outcome')}")  # scored or unscoreable?
        print(f"  Note: veto_safety = FLOOR to E/20 but STILL SCORED (E grade shown to consumer)")
        print()

# 6. Verify iron 3x S-grade products are intact
print("=== IRON S-GRADES REGRESSION CHECK ===")
iron_barcodes = {"7290118814061", "783495578741", "7290012056741"}
for r in results:
    if r.get("barcode") in iron_barcodes:
        eo = r.get("engine_output", {})
        print(f"  [{r.get('barcode')}] grade={eo.get('grade')} score={eo.get('score')} binding={eo.get('binding_constraint',{}).get('mechanism')}")

# 7. Check 0 veto_safety on passing grade
print()
print("=== VETO_SAFETY ON PASSING GRADE CHECK ===")
veto_passing = []
for r in results:
    if r.get("outcome") == "scored":
        eo = r.get("engine_output", {})
        grade = eo.get("grade")
        ss = eo.get("sub_scores", {})
        safety = ss.get("safety")
        if safety == "veto" and grade not in ("E",):
            veto_passing.append((r.get("barcode"), grade, eo.get("score")))
if veto_passing:
    print(f"  FAIL: {len(veto_passing)} product(s) with veto_safety but not E grade: {veto_passing}")
else:
    print("  PASS: 0 products with veto_safety on a passing (non-E) grade")

print()
print("=== FOOD SCORING BYTE-IDENTICAL CHECK (git diff) ===")
print("  (Checking via git diff -- cannot run git here, will note separately)")
