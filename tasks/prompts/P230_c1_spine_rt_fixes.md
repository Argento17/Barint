(route: C1-CURSOR)

# P230 — Spine red-team fixes (deterministic code). Worktree-isolated build.

You are a C1 builder working in an ISOLATED git worktree (cwd is the worktree root, NOT the
main C:\Bari tree). Make ONLY the edits below. Each is grounded in a verified red-team finding
with exact file:line. After editing, run the verification block and report results. Do NOT
touch scoring math, configs, or any file not listed. Do NOT git push.

Repo layout note: paths are relative to the worktree root (same structure as C:\Bari).

## FIX RT-2 (CRITICAL) — `03_operations/page_generator/gates/run_gates.py`
PROBLEM (verified): the PENDING_COPY fail check is inside `if schema_ver == "v3":` (~line 574),
so the 10 of 11 live pages that are NOT schema v3 get NO PENDING_COPY gate. `_collect_consumer_strings`
(~line 874-878) deliberately SKIPS `PENDING_COPY` strings, so G6 never catches them either.
FIX: add a schema-AGNOSTIC PENDING_COPY check, placed BEFORE the existing `if schema_ver == "v3":`
block. Logic:
  - pending = "PENDING_COPY"; n = len(products)
  - Detect copy-stage-ran = NOT every product's insightLine is PENDING (i.e. at least one product
    has a non-PENDING, present insightLine). This distinguishes a real authored/finalized page
    from a legitimate PRE-COPY generator dump (where ALL insightLines are PENDING).
  - If copy stage has NOT run: `g.info("PENDING_COPY base check: SKIP (pre-copy generator output)")`.
  - If copy stage HAS run: for each base consumer field in ["insightLine", "rowVerdict"], count
    products where the field is PRESENT and == pending; if count > 0 → `g.fail(f"{field}: {count}/{n} products still PENDING_COPY (page authored but incomplete)")`.
  - Keep the existing v3 block exactly as-is (it covers the v3 milk-depth fields).
This must FAIL the gate for a non-v3 page that has been through copy stage but still has PENDING
in insightLine/rowVerdict. It must NOT fail a pre-copy generator page (all insightLines PENDING).

## FIX RT-1 (CRITICAL) — `03_operations/page_generator/spine_flip.py`
PROBLEM (verified): a flip that moves milk's baseline produces overall_verdict=READY with no
mention. `run_summary.json` per-shelf entries DO include `c10_pass` (written by rescore_all.py:1052).
spine_flip already reads run_summary at ~lines 388-404 (captures score_moves/grade_moves/off_count).
FIX (surface only — do NOT re-add any hard block / exit-2):
  1. In the run_summary parse loop (~line 396-401), also capture `c10_pass`:
     `moves["c10_pass"] = bool(ent.get("c10_pass", True))` (default True if absent), and set
     `shelf_rec["c10_pass"] = moves["c10_pass"]` next to the other shelf_rec assignments (~404-406).
  2. After `gate_fails` is computed (~line 474), add:
     `baseline_moved = [s["shelf"] for s in per_shelf if s.get("c10_pass") is False]`
  3. Change overall_verdict (~line 506) so it is "REVIEW" when `baseline_moved` is non-empty too:
     `overall_verdict = "READY" if (not gate_fails and not baseline_moved and not any(s.get("error") for s in per_shelf)) else "REVIEW"`
  4. Add `baseline_moved` into the report JSON dict (near overall_verdict, ~line 521) and into the
     final DEPLOY-READY print line (~line 601): append `f" baseline_moved: {','.join(baseline_moved) or 'none'}."`
  Keep exit codes unchanged (1=movement, 0=none). This only makes baseline movement VISIBLE.

## FIX RT-10 (MEDIUM) — `03_operations/page_generator/affected_set.py`
PROBLEM: `build_corpus_to_shelves_map()` (~line 118-121) uses a bidirectional PREFIX path match
(`src.startswith(shelf_src) or shelf_src.startswith(src)`) which can spuriously map a corpus to
the wrong shelf under shared parent dirs.
FIX: change to EXACT normalized path equality (`if shelf_src and src == shelf_src:`). Remove the
`startswith` branch. (Verify conformance still 12/12 after — see verification.)

## FIX RT-4, RT-8, RT-9, RT-11 — `03_operations/page_generator/conformance.py` (all SOFT/warn, never hard-fail)
Add these as new SOFT checks inside `evaluate()` (alongside SOFT-4/5/6). Use the existing `add(check_id, hard=False, ok, detail)` helper. None may hard-fail.
- **RT-4 (SOFT-8-off_misplaced):** beyond the existing products-only HARD-7, scan the WHOLE served JSON text for OFF markers; subtract the count already found in products[]. If OFF markers appear OUTSIDE products[] AND outside any `"reason"`/`"note"`/`"_comment"`/`exclusions` context (i.e. a real misplaced OFF record), warn. Keep it conservative — if unsure, only warn when an OFF marker appears in a key that looks like product data outside products[]. Do not duplicate the HARD-7 hit.
- **RT-8 (SOFT-9-registry_source):** for each corpus mapping to this stem (use the already-computed `stem_corpora[stem]` / registry `corpora`), get its `source`; warn if that source dir is NOT among the config's `corpus_dirs` + `scoring.bsip1_dir` (normalized paths). Detail: "shadow source <X> not referenced by config corpus_dirs — shadow may validate a stale/partial corpus."
- **RT-9 (SOFT-10-shelf_rel):** if config `scoring.flags` has `BARI_SHELF_RELATIVE_V1=="on"` OR `BARI_SODIUM_SHELF_RELATIVE_V1=="on"` but `scoring.shelf_rel` is null/missing → warn "shelf-relative flag ON but no shelf_rel calibration (median/scale) — scores will be absolute, likely wrong."
- **RT-11 (SOFT-11-manifest_count):** count `len(data["products"])` in the served frontend JSON; compare to the live_manifest entry's `product_count` for this category; warn if they differ. Detail: "live_manifest product_count=<m> != served file products=<f> (manifest stale?)."

## VERIFICATION (run all, paste output into your return)
```
cd <worktree-root>
python -c "import ast;[ast.parse(open(f,encoding='utf-8').read()) for f in ['03_operations/page_generator/gates/run_gates.py','03_operations/page_generator/spine_flip.py','03_operations/page_generator/affected_set.py','03_operations/page_generator/conformance.py']];print('ALL 4 FILES: valid Python')"
$env:PYTHONIOENCODING="utf-8"; python 03_operations/page_generator/conformance.py --all
```
Report: (1) the 4-file syntax result, (2) the conformance SUMMARY line (MUST still be 12 conform / 0 non-conforming — if RT-10 or RT-8/9/11 changed it, STOP and report what changed), (3) any new SOFT warnings that now fire and on which categories, (4) a unified diff of every file you changed. End with the machine-readable return contract JSON.
