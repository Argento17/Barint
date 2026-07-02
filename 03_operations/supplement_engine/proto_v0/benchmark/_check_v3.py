"""Quick verification script for v3 run output. Run from the benchmark directory."""
import json, pathlib, sys

d = json.loads(pathlib.Path("magnesium_v3_latest.json").read_text(encoding="utf-8"))
print("model:", d["model"])
print("flag:", d["flag"])
print("counts:", d["counts"])
print("grade_dist:", d["grade_distribution"])
print("stats:", d["score_stats"])
print()

print(f"{'barcode':<20} {'name':<35} {'elem':>6} {'cls':<12} {'fct':>5} {'adj':>6} {'d_s':>5} {'ev_s':>4} {'tr_s':>4} {'blend':>6} {'final':>6} {'gr':<3} {'bind':<38} {'ul_flags'}")
print("-" * 165)

for r in d["results"]:
    if r["disposition"] in ("SCORED", "SOLGAR_EXCEPTION"):
        sf_flags = "|".join(f["flag"] for f in r.get("safety_flags", []))
        caps_bind = "|".join(c["mechanism"] for c in r.get("caps_fired", []))
        caps_check = "|".join(c["mechanism"] for c in r.get("caps_checked_not_binding", []))
        bind = r.get("binding_constraint", "")
        ss = r.get("sub_scores", {})
        elem = r["administered_elemental_mg"]
        adj = r.get("adjusted_dose_mg", "")
        fct = r.get("bav_tier_factor", "")
        note = ""
        if caps_check:
            note = f" [checked_not_binding:{caps_check}]"
        print(
            f"{r['barcode']:<20} {r['name_short'][:35]:<35} {str(elem)+'mg':>6} "
            f"{r['bav_class']:<12} {str(fct):>5} {str(adj)+'mg':>7} "
            f"{ss.get('dose', 0):>5.1f} {ss.get('evidence_class', 0):>4.1f} "
            f"{ss.get('transparency', 0):>4.1f} {r['blend']:>6.1f} "
            f"{r['final_score']:>6.1f} {r['grade']:<3} {bind:<38} {sf_flags}{note}"
        )
    elif r["disposition"] == "UNRESOLVED":
        print(f"{r['barcode']:<20} {r['name_short'][:35]:<35} {'UNRESOLVED':>6}")

print()
# Self-checks
scored = [r for r in d["results"] if r["disposition"] in ("SCORED", "SOLGAR_EXCEPTION")]
scores = [r["final_score"] for r in scored]

# 1. Four oxide products all D/49.0
oxide = [r for r in scored if r.get("form") == "oxide" and r.get("administered_elemental_mg", 0) >= 450]
assert len(oxide) == 4, f"Expected 4 UL-exceed oxide products, got {len(oxide)}"
for o in oxide:
    assert o["final_score"] == 49.0, f"Oxide {o['barcode']} expected 49.0, got {o['final_score']}"
    assert o["grade"] == "D", f"Oxide {o['barcode']} expected D, got {o['grade']}"
print("CHECK 1 PASS: 4 oxide products (520mg/450mg) all D/49.0 via UL grade ceiling")

# 2. Two 250mg B products carry GI note
b250 = [r for r in scored if r.get("administered_elemental_mg") == 250.0]
assert len(b250) == 2, f"Expected 2 products at 250mg, got {len(b250)}"
for p in b250:
    gi_flags = [f for f in p.get("safety_flags", []) if f["flag"] == "GI_NOTE_EFSA"]
    assert len(gi_flags) == 1, f"{p['barcode']} expected GI_NOTE_EFSA flag, got {p.get('safety_flags')}"
    assert p["grade"] == "B", f"{p['barcode']} expected B, got {p['grade']}"
print("CHECK 2 PASS: 2 x 250mg B products carry GI_NOTE_EFSA; grades unchanged (B)")

# 3. Tink 520 is UNRESOLVED
tink = [r for r in d["results"] if r["barcode"] == "7290015318426"]
assert len(tink) == 1 and tink[0]["disposition"] == "UNRESOLVED", f"Tink expected UNRESOLVED, got {tink}"
print("CHECK 3 PASS: Tink 520 = UNRESOLVED / no-score")

# 4. Grade distribution: B4 C4 D6 E1 (15 scored)
dist = d["grade_distribution"]
assert dist.get("B", 0) == 4, f"Expected B=4, got {dist}"
assert dist.get("C", 0) == 4, f"Expected C=4, got {dist}"
assert dist.get("D", 0) == 6, f"Expected D=6, got {dist}"
assert dist.get("E", 0) == 1, f"Expected E=1, got {dist}"
assert len(scored) == 15, f"Expected 15 scored, got {len(scored)}"
print(f"CHECK 4 PASS: Grade distribution B4/C4/D6/E1 (15 scored) — matches co-signed estimate")

# 5. Score==trace self check: blend formula
import math
for r in scored:
    ss = r.get("sub_scores", {})
    d_s = ss.get("dose", 0)
    ev_s = ss.get("evidence_class", 0)
    tr_s = ss.get("transparency", 0)
    expected_blend = round(d_s * 0.55 + ev_s * 0.20 + tr_s * 0.25, 1)
    actual_blend = r["blend"]
    assert abs(expected_blend - actual_blend) < 0.05, (
        f"{r['barcode']}: blend mismatch expected {expected_blend} got {actual_blend}"
    )
print("CHECK 5 PASS: score==trace self-check (blend formula verified for all 15 products)")

# 6. Solgar caps_checked_not_binding shows cap_3 was checked but didn't bind
solgar = [r for r in scored if r["barcode"] == "0033984005181"][0]
assert solgar["binding_constraint"] == "blend_dominant", f"Solgar binding expected blend_dominant, got {solgar['binding_constraint']}"
assert any(c["mechanism"] == "cap_3_honesty_core" for c in solgar.get("caps_checked_not_binding", [])), (
    f"Solgar: cap_3 should be in caps_checked_not_binding. Got {solgar.get('caps_checked_not_binding')}"
)
assert not any(c["mechanism"] == "cap_3_honesty_core" for c in solgar.get("caps_fired", [])), (
    f"Solgar: cap_3 should NOT be in caps_fired. Got {solgar.get('caps_fired')}"
)
print("CHECK 6 PASS: MRT-7 — Solgar cap_3 in caps_checked_not_binding (not caps_fired); blend_dominant")

# 7. OFF=0 check (no Open Food Facts source anywhere in results)
result_str = json.dumps(d["results"])
assert "open_food_facts" not in result_str.lower(), "OFF reference found!"
assert "off.co" not in result_str.lower(), "OFF reference found!"
print("CHECK 7 PASS: OFF=0 (no Open Food Facts reference in results)")

# 8. Before/after distribution comparison
print()
print("BEFORE/AFTER vs prior verified run (B4/C9/D2/E1 / 16 scored):")
print("  Before (pre-correction): B4, C9, D2, E1 (16 scored)")
print(f"  After  (this run):        B{dist.get('B',0)}, C{dist.get('C',0)}, D{dist.get('D',0)}, E{dist.get('E',0)} (15 scored)")
print("  Changes: 4xC->D (Altman520, Nutricare520, MagUP, Balance -- UL grade ceiling D)")
print("           1xC->no-score (Tink520 -> UNRESOLVED, label confirmation required)")

print()
print("ALL CHECKS PASSED — v3 run authoritative.")
