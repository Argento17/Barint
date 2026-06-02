# TASK-129B — Yogurt reconciliation findings (BLOCKED)

**Owner:** nutrition-agent · **Date:** 2026-06-01
**Origin:** `03_operations/bsip2/confidence_reaudit_launch_v1.md` §3 P0 #2, §7, Controller decision (line 128: "reconcile to machine run").
**Verdict:** **BLOCKED (hard).** Path (a) — reconcile-to-machine-run — is **not executable** against the only existing run (`run_yogurt_001`). No score change shipped; deployed corpus untouched.

---

## What was attempted

Diffed the 13 displayed hand-tuned yogurts (`bari-web/src/data/comparisons/yogurts_frontend_v1.json`,
`version: v1-mvp-manual`) against the frozen machine run `run_yogurt_001` (45 traces,
`02_products/yogurt_system/bsip2_outputs/run_yogurt_001`).

## Blocker 1 — the machine run is a SYNTHETIC architectural-stress corpus, not real branded SKUs

- Barcodes are sequential placeholders `7290200000001 … 7290200000045` (real Israeli barcodes are not sequential).
- BSIP1 records (`03_operations/bsip1/run_yogurt_001/output/`) have `bsip1_source_path: null`, no scrape provenance; the run analysis states "Framework: proto_v0 **unmodified**" and uses generic archetype names ("יוגורט טבעי 3% שומן") rather than the real brands the frontend ships (תנובה / שטראוס / דנונה / יופלה / אקטיביה).
- The displayed 13 are **real branded products**. There is no 1:1 machine trace for them.

## Blocker 2 — no 1:1 coverage; best-effort archetype map has collisions and grade-flipping deltas

Best-effort manual→machine archetype mapping (machine `final_score_estimate`):

| display id | manual | machine archetype | machine | delta | note |
|---|---:|---|---:|---:|---|
| yog-001 יוגורט מלא 3% תנובה | 88/A | יוגורט טבעי 3% שומן | 85/A | −3 | |
| yog-002 יוגורט ביו 1.5% תנובה | 87/A | יוגורט טבעי 1.5% שומן | 85/A | −2 | |
| yog-004 יוגורט יווני 5% שטראוס | 85/A | יוגורט יווני 5% שומן | 85/A | 0 | |
| yog-003 יוגורט 0% שומן | 82/A | יוגורט יווני 0% שומן | 85/A | +3 | **collides with yog-005** |
| yog-005 יוגורט יווני 0% שטראוס | 80/A | יוגורט יווני 0% שומן | 85/A | +5 | **collides with yog-003** |
| yog-006 אקטיביה טבעית דנונה | 78/B | יוגורט אקטיביה פרוביוטי | 60.6/C | **−17.4** | **grade flip B→C; collides with yog-008** |
| yog-010 יוגורט סויה טבעי | 72/B | יוגורט סויה טבעי | 74.8/B | +2.8 | |
| yog-012 יופלה GO פירות יער | 69/B | יוגורט חלבון 20 פרי יער | 75.5/B | +6.5 | |
| yog-009 יוגורט קוקוס | 68/B | יוגורט קוקוס | 55.0/C | **−13.0** | **grade flip B→C** |
| yog-008 אקטיביה טעמים דנונה | 65/B | יוגורט אקטיביה פרוביוטי | 60.6/C | −4.4 | grade flip B→C; collides with yog-006 |
| yog-007 יופלה בטעמי פירות | 62/C | יוגורט פירות יוטבתה 1.5% | 61.4/C | −0.6 | |
| yog-011 יוגורט שתיה וניל | 55/C | יוגורט שתייה תות | 56.8/C | +1.8 | |
| yog-014 יוגורט 0% ממותק ממתיק | 51/C | יוגורט 0% ללא סוכר תות | 54.8/C | +3.8 | |

- Two manual products map to one machine trace in **two** places (0% plain/greek; actibia plain/flavored) — the synthetic corpus has no distinct anchor for them.
- Audit-reported rank correlation manual↔machine = **0.45**; machine mean 75 vs manual 93.6. The two are not reconcilable by rule-based calibration.

## Blocker 3 — the machine run carries documented, governance-gated scoring bugs

Per `run_yogurt_001_analysis.md`, accepting machine scores would publish known defects:
- `ואניל` (natural vanilla) → NOVA4 false positive on 5 products (Evolution #5 bug).
- `NOVA1_SINGLE_FLOOR=85` over-applies — 11 products pinned at exactly 85; also overrides beverage-routing penalty for drink products.
- Plant-based yogurts (soy/coconut/oat/almond) misrouted to `dairy_protein`; coconut sat-fat treated as added.
- Ingredient-text contamination misroutes dessert yogurts to `sauce_spread` / `whole_food_fat`.

Fixing these is each a scoring-rule change requiring evidence-registry + Product co-sign + the DEC-004 calibration gate — out of scope for a reconciliation task, and not "free-hand tuning" we are permitted to do here.

---

## Why not just accept the machine scores

Doing so would (1) replace 13 real branded products with generic synthetic archetypes the consumer never sees on shelf, (2) flip ≥3 grades on defects the analysis already flags as bugs, and (3) collapse 2 product pairs to identical scores. That is less defensible than the current hand-tuned display, not more.

## Recommendation to Controller (either unblocks; nutrition-agent does not own the choice)

- **(i) Real-corpus path:** authorize a genuine `run_yogurt_002` = BSIP0 scrape of the 13 (or representative) **real** Shufersal yogurt SKUs → BSIP1 enrich → BSIP2 score → then reconcile. This is a **bari-category-factory** pipeline task (Data/QA + category factory), not nutrition reconciliation. Yogurts stays NO-GO until it closes.
- **(ii) Exception path** (audit §7 option b): register a **manual-MVP exception** in `exception_registry_v1.md` with explicit Controller approval, documenting that yogurt scores are editorial MVP estimates pending a machine run. Yogurts could then ship with an honest "MVP — not machine-frozen" disclosure, but this is a governance exception, not a score-freeze.

**No score, label, or freeze marker was changed. The deployed `yogurts_frontend_v1.json` is untouched. Yogurts remains 🔴 NO-GO.**
