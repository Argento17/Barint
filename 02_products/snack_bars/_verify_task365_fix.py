"""Self-verification of Task-365 fix artifacts."""
import json, pathlib, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FE_PATH = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\protein_combined_frontend_v2.json")
RR_PATH = pathlib.Path(r"C:\Bari\02_products\snack_bars\bsip2_outputs\protein_bars_task365\run_record.json")
RT_PATH = pathlib.Path(r"C:\Bari\02_products\snack_bars\bsip2_outputs\protein_bars_task365\rerank_table.json")
FC_PATH = pathlib.Path(r"C:\Bari\02_products\snack_bars\protein_combined_corpus_task365_33_20260621_fix.json")
V1_PATH = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\protein_bars_frontend_v1.json")

DISCARDED = {"7290015130271", "7290015130288"}

fe = json.loads(FE_PATH.read_text(encoding="utf-8"))
rr = json.loads(RR_PATH.read_text(encoding="utf-8"))
rt = json.loads(RT_PATH.read_text(encoding="utf-8"))
v1 = json.loads(V1_PATH.read_text(encoding="utf-8"))

fe_count = len(fe["products"])
meta_count = fe["_meta"]["product_count"]
rr_scored = rr["scored_count"]
rr_corpus = rr["corpus_product_count"]
rt_count = len(rt)

print("=== ARTIFACT VERIFICATION ===")
print(f"frontend products actual:  {fe_count}")
print(f"frontend meta.product_count: {meta_count}")
print(f"run_record scored_count:   {rr_scored}")
print(f"run_record corpus_count:   {rr_corpus}")
print(f"rerank_table count:        {rt_count}")

# All must be 33
assert fe_count == 33, f"FAIL: frontend has {fe_count} products, expected 33"
assert meta_count == 33, f"FAIL: meta.product_count={meta_count}, expected 33"
assert rr_scored == 33, f"FAIL: run_record scored_count={rr_scored}, expected 33"
assert rt_count == 33, f"FAIL: rerank_table has {rt_count} rows, expected 33"
print("COUNT CHECK: PASS — all artifacts show 33")

# Corpus sha256
computed_sha = hashlib.sha256(FC_PATH.read_bytes()).hexdigest()
recorded_sha = rr["corpus_sha256"]
sha_match = computed_sha == recorded_sha
print(f"corpus sha256 match: {sha_match} ({computed_sha[:16]}...)")
assert sha_match, "FAIL: corpus sha256 mismatch"

# Discarded barcodes absent from frontend
in_fe = {p["barcode"] for p in fe["products"]} & DISCARDED
print(f"discarded in frontend: {in_fe} (must be empty)")
assert not in_fe, f"FAIL: discarded barcodes still in frontend: {in_fe}"
print("OFF-ROLL CHECK: PASS — 7290015130271 and 7290015130288 absent")

# Score stability
stability = rr["score_stability_check"]["status"]
print(f"score stability: {stability}")
assert stability == "PASS", f"FAIL: score_stability={stability}"

# Completeness gate
comp_gate = rr["ingredient_completeness_gate"]["status"]
comp_found = rr["ingredient_completeness_gate"]["truncations_found"]
print(f"completeness gate: {comp_gate} ({comp_found} truncations)")
assert comp_gate == "PASS" and comp_found == 0

# Invariants
inv_overall = rr["acceptance_invariants"]["_overall"]["status"]
print(f"acceptance invariants: {inv_overall}")
assert inv_overall == "PASS", f"FAIL: invariants={inv_overall}"

# COND-2
cond2 = rr["cond2_collagen_check"]["status"]
cond2_issues = rr["cond2_collagen_check"]["double_fire_issues"]
print(f"COND-2 no-double-fire: {cond2} ({cond2_issues} issues)")
assert cond2 == "PASS" and cond2_issues == 0

# Grade histogram
hist = rr["score_distribution"]["grade_histogram"]
score_min = rr["score_distribution"]["min"]
score_max = rr["score_distribution"]["max"]
score_mean = rr["score_distribution"]["mean"]
print(f"grade histogram: {hist}")
print(f"score range: {score_min}–{score_max} mean={score_mean}")
assert hist.get("A", 0) == 0, f"FAIL: A grades present after fix: {hist}"
print("NO-A-GRADE CHECK: PASS — 0 A grades (false tops removed)")

# Ceiling: rank 1 = Talmah 70/B, rank 2 = Pangaea 68.6/B
rt_by_bc = {r["barcode"]: r for r in rt}
talmah = rt_by_bc.get("7290112497994", {})
pangaea = rt_by_bc.get("7290017516295", {})
print(f"Rank 1: {talmah.get('name')} score={talmah.get('score')} grade={talmah.get('grade')} rank={talmah.get('rank')}")
print(f"Rank 2: {pangaea.get('name')} score={pangaea.get('score')} grade={pangaea.get('grade')} rank={pangaea.get('rank')}")
assert talmah.get("rank") == 1 and talmah.get("score") == 70 and talmah.get("grade") == "B"
assert pangaea.get("rank") == 2 and pangaea.get("score") == 68.6 and pangaea.get("grade") == "B"
print("CEILING CHECK: PASS — תלמה 70/B at rank 1, פנגיאה 68.6/B at rank 2")

# v1 untouched
v1_count = v1["_meta"]["product_count"]
print(f"v1 product_count: {v1_count} (live, untouched)")

# OFF check
off_check = fe["_meta"].get("off_check", "")
print(f"OFF check: {off_check}")
assert "no Open Food Facts" in off_check, "FAIL: OFF check missing"

print("\n=== ALL CHECKS PASSED ===")
print(f"run_id: {rr['run_id']}")
