# BSIP2 Confidence Re-Audit — Launch Categories (v1)

**Task:** TASK-129-A (slice of TASK-129 — BSIP Calibration & Confidence, launch slice)
**Owner:** nutrition-data-agent
**Date:** 2026-06-01
**Scope:** hummus, maadanim, snacks, yogurts, bread (+ milk, LEGACY/non-gating per DEC-003 Amendment A)
**Method:** Parsed every authoritative BSIP2 trace per category and reconciled against the shipping v2 frontend corpora (`src/data/comparisons/*.json`). Scratch parser + raw extracts: `C:\Bari\tmp_audit_129a\`.

> **Headline:** Only **hummus** is score-frozen and launch-defensible today. **yogurts is the hard blocker** (displayed scores are hand-tuned, not reproducible from any frozen run). **bread** has a dual-run authority ambiguity. A single **systemic confidence-gate defect** (presence-based "verified" label accepts marketing-prose ingredient lists) inflates confidence across hummus, maadanim, snacks and milk.

---

## 0. Two confidence systems (terminology)

The audit distinguishes two things both called "confidence":

1. **Internal scoring confidence** — trace `confidence_score` (0–100) + `confidence_band` (`low/medium/high/insufficient`). Driven by NOVA-proxy and category-classification uncertainty.
2. **Display data-sufficiency** — frontend `confidence` ∈ {`verified`, `partial`, `insufficient`}, per Launch-Definition §5: *verified = ≥3/6 nutrition fields AND ingredients present; else partial; null → insufficient.*

The §5 gate is **presence-based** and does **not** validate that the ingredient field contains real ingredients. This is the root cause of the cross-category confidence inflation below.

---

## 1. Category Confidence Table

| Category | Frozen? | Authoritative run audited | Corpus n | Displayed n | Internal conf (mean/min) | Display conf mix | Cat-conf mean/min | Headline confidence risk |
|---|---|---|---:|---:|---|---|---|---|
| **hummus** | ✅ run_hummus_002 (`AUTHORITATIVE.md`) | `intelligence_bsip2/run_hummus_002` | 69 | 66 (64 scored + 2 null) | 87.5 / 5 | verified 58 · partial 6 · insuff 2 | 0.915 / 0.30 | 15 marketing-prose ingredient lists pass as **verified**; `fat_quality` unreliable on 58/69 |
| **maadanim** | ❌ | `bsip2_outputs/run_maadanim_001` | 200 | 90 curated | 76.3 / **0** | mostly verified | 0.709 / 0.30 | corpus ~35% contaminated; **71/200 low cat-conf**, 31 insufficient (excluded); ≥3 instability items **survive into display** |
| **snacks** | ❌ | `bsip2_outputs/run_snack_bars_synthesis_001` | 53 (48 scored) | 18 curated | 75.5 / 5 | verified/partial | 0.742 / 0.40 | snk-001 shown **verified with all-null nutrition**; 14 marketing-prose; granola/cereal/whole_food routing instability |
| **yogurts** | ❌ **manual** | display = `v1-mvp-manual` (machine `run_yogurt_001` **not** displayed) | 45 machine / 13 shown | 13 | 93.6 / 75 (machine) | all partial | 0.827 / 0.45 | **Displayed scores are hand-tuned**, not reproducible from any frozen run — un-freezable as-is |
| **bread** | ❌ | display = `bread_retail_003` (256→24); separate `bread_light` run also exists | 256 | 24 curated | n/a (slim export schema) | **all partial (0 verified)** | n/a | dual-run authority ambiguity; whole shelf partial-confidence; `limitingFactors` field gap (Launch §6) |
| **milk** *(LEGACY)* | ❌ (not gating) | `intelligence_bsip2/run_004_recalibrated` | 20 | blog-legacy | 87 / 77 | high | 0.782 / 0.50 | plant "beverages" misrouted with instability; out of launch gate (DEC-003 Amend. A) |

Band/grade distributions and full rankings: `C:\Bari\tmp_audit_129a\audit_detail.md`.

---

## 2. Product-Level Exceptions (flag → action)

### 2.1 EXCLUDE / already-excluded (corpus contamination)
**maadanim run_001** scored 7 products at `confidence=0`, `cat=default`, `cat_conf=0.30` that are **not maadanim at all** — they are correctly **absent from the displayed 90**, but should be in a written exclusion list so they cannot re-enter on a re-run:
- `שריר הזרוע (8) בעדני` (arm-muscle **meat**), `המבורגר ילדים` (**hamburger**), `חסה מעודנת הידרופונית` (**lettuce**), `גבינת בולגרית 5% גד ארוז` / `בולגרית מעודנת 24%` (**brined cheese**), `ביו LR 25 בד"ץ`, `ביו 25`, `מיקס לילד`.
- Plus the probiotic-**supplement** cluster scored at `conf=5`, `cat=dessert` (placeholder 50): `ביו בליס פרוביוטיקה`, `מגה פרוביוטיק 500`, `פרוביוטיק SHAPE`, `ביוגאיה טיפות`, `יומי פרוביוטיק`, `ביו 25 פרוביוטיקה`.
- **Action:** formalize a maadanim `excluded_products` list (mirror the hummus pattern) and re-confirm none appear in the displayed 90.

### 2.2 CORRECT before publication (category-instability survivors that ARE displayed)
These reached the **displayed maadanim shelf** despite `cat=default/dessert` + `cat_conf ≤ 0.55` + `category_instability=true`:
- `סופר גמדים תות בננה מארז` (53/C, conf 85, cat_conf 0.30) — squeezable kids' drink, routed `default`.
- `גמדים לשתיה תות בננה` (46/D, conf 85, cat_conf 0.30) — drinkable, routed `default`.
- `דנונה מולטי קולגן` (45/D, conf 87, cat_conf 0.55) — collagen drink, routed `dessert`.
- **Action:** re-route or exclude; do not publish a category-instability product on the maadanim shelf with a `verified` label.

### 2.3 FREEZE WITH PLACEHOLDER (handled correctly — keep as reference pattern)
- **hummus** `bsip1_7296073733317`, `bsip1_7296073733348` — `insufficient_data`, displayed with **null score** + `insufficient` label. Correct. Documented in `run_hummus_002/AUTHORITATIVE.md`.

### 2.4 RELABEL (false "verified")
- **snacks snk-001** `חטיף תמרים במילוי חמאת שקדים` — score 70/B, `confidence: verified`, but **all six nutrition fields null** in the displayed VM. A "verified" label on a row with no nutrition values is a confidence failure. **Action:** relabel `partial` (or backfill nutrition).
- **All marketing-prose ingredient products** (see §3.1) currently labelled `verified` — relabel to `partial` until the ingredient field is validated.

### 2.5 ABSURD-SCORE check (none are true inversions, but note)
- Lowest scores carry **max confidence** (e.g., snacks `שחור ולבן … 30% מילוי קרם חלב` 13.4/E/conf100) — this is **correct** (clear ultra-processed junk, well-evidenced), not an absurd score.
- No whole-food-ranked-low or junk-ranked-high inversions found in any displayed shelf. The integrity problem is **confidence labelling**, not score ordering.

---

## 3. Required BSIP Fixes (prioritized)

### P0 — launch-blocking
1. **Confidence-gate hardening (systemic).** The §5 `verified` gate must validate ingredient-list *quality*, not mere presence. Add a marketing-prose / non-ingredient detector (heuristic available in the scratch parser: long prose, promo tokens such as `מסייע`, `האריזה`, `מיחזור`, `עשיר בחלבון`). When triggered: downgrade to `partial` **and** suppress ingredient-derived positive signals (additive-free / NOVA / sweetener claims). **Impact:** hummus 15, maadanim 63, snacks 14, milk 2 products currently over-labelled.
2. **yogurts reconciliation.** Displayed 13 are **hand-tuned** (`v1-mvp-manual`, "ציונים מכווננים ידנית"). Either (a) regenerate from a reproducible frozen run and reconcile deltas, or (b) register a **manual-MVP exception** in `exception_registry_v1.md` with explicit Controller approval. Score-freeze is impossible until one of these closes.
3. **maadanim corpus finalization.** Ship the §2.1 exclusion list + §2.2 corrections, then freeze the displayed 90.
4. **bread run-authority resolution.** Declare `bread_retail_003` authoritative for the launch shelf (it is what the frontend ships), archive/relabel `bread_light` synthesis as experimental, then freeze the 24. Close the `limitingFactors` field gap called out in Launch-Definition §6.

### P1 — should fix at/near launch
5. **hummus `fat_quality` defect.** 58/69 products carry a neutral-50 placeholder (Shufersal fat-row scrape defect, TASK-039). Currently *neutralized* so it does not distort scores, but it caps confidence. Re-scrape + re-run as `run_hummus_003` (post-launch acceptable; document as a known limitation at launch).
6. **structural-class guessing.** 16 hummus / 48 maadanim products have `structural_class.primary_confidence < 0.35` (model effectively guessing). Suppress any structural-class-derived consumer claim when `primary_confidence < 0.35`.
7. **weak/templated explanations.** Single-cap-driver explanations (hummus 19, yogurts 26, maadanim 59) where the only driver is one binding cap with no product-specific positive. Require the explanation engine to surface ≥1 product-specific signal per row.

### P2 — post-launch
8. **plant-beverage routing.** Milk plant "beverages" and yogurt drinks (`אקטימל`, `שתייה חלב לילדים`) route to `beverage` with instability — out of launch gate for milk; revisit in milk gen0→gen1→v2 onboarding (P1 §128E).

---

## 4. Score-Freeze Readiness (per category)

| Category | Freeze status | Gate to freeze |
|---|---|---|
| **hummus** | **READY — already frozen** (`run_hummus_002`) | Hold for launch with documented limitations (fat_quality, marketing-prose ingredients downgraded to `partial`). No re-run required to launch. |
| **maadanim** | **BLOCKED** | Apply §2.1 exclusions + §2.2 corrections, then freeze displayed 90. |
| **snacks** | **NEAR-READY** | Relabel snk-001 + null-nutrition `verified` rows → `partial`; confirm the 18 curated; then freeze. Low risk. |
| **yogurts** | **BLOCKED (hard)** | Cannot freeze hand-tuned scores. Reconcile to a reproducible run **or** register a manual-MVP exception. |
| **bread** | **BLOCKED** | Resolve `retail_003` vs `bread_light` authority; close `limitingFactors` gap; then freeze the 24. |
| **milk** | **DEFERRED** | LEGACY; not gating (DEC-003 Amend. A). Freeze in post-launch onboarding. |

---

## 5. Frontend v2 Migration Go / No-Go

| Category | Verdict | Condition |
|---|---|---|
| **hummus** | 🟢 **GO** | Already LIVE + frozen. Carry forward P1 fixes (fat re-run, `verified`→`partial` for marketing-prose rows) without blocking. |
| **maadanim** | 🟡 **CONDITIONAL GO** | NO-GO on the §2.2 instability survivors until re-routed/excluded. GO for the rest once corpus is finalized + frozen. |
| **snacks** | 🟡 **CONDITIONAL GO** | GO after relabeling false-`verified` rows (snk-001 + any null-nutrition). Scores/ordering are sound. |
| **yogurts** | 🔴 **NO-GO** | Hand-tuned scores are not launch-defensible as machine confidence. Reconcile to a frozen run or register an explicit exception first. **Biggest single blocker.** |
| **bread** | 🟡 **CONDITIONAL GO** | GO after resolving dual-run authority + closing `limitingFactors`. Disclose that the whole shelf is partial-confidence (0 verified). |
| **milk** | ⚪ **LEGACY (out of gate)** | Stays `/blog`, LEGACY-labelled; migrates post-launch. |

**Net:** 1 GO (hummus), 3 conditional (maadanim, snacks, bread), 1 NO-GO (yogurts), 1 legacy (milk). The §3 P0 confidence-gate fix unblocks the most products across categories with a single change.

---

## 6. Cross-cutting confidence failures (summary)

1. **Presence-based `verified` accepts marketing-prose ingredients** → false high data-confidence (hummus 15, maadanim 63, snacks 14, milk 2). *P0 #1.*
2. **Hand-tuned yogurts** break the reproducibility premise of score-freeze. *P0 #2.*
3. **Category-instability products published** on maadanim despite `cat=default/dessert` + `cat_conf ≤ 0.55`. *P0 #3 / §2.2.*
4. **Two parallel bread runs**; frontend ships the one without an authority marker. *P0 #4.*
5. **Structural-class guessing** (`primary_confidence < 0.35`) on 64 products surfaces class-derived claims the model can't support. *P1 #6.*
6. **Templated single-cap explanations** on 100+ products weaken the "why this score" story. *P1 #7.*

*Artifacts:* `C:\Bari\tmp_audit_129a\audit_summary.json`, `audit_detail.md`, `frontend_dump.md`, `bread_audit.md` (+ parsers `audit.py`, `detail.py`, `frontend.py`, `bread.py`).

---

## 7. Controller decisions (2026-06-01) → follow-up actions

- **Yogurts (P0 #2) — DECIDED: reconcile to machine run.** Regenerate yogurts from `run_yogurt_001`, diff the machine output against the 13 hand-tuned displayed scores, resolve each delta, and freeze the reconciled corpus. The `v1-mvp-manual` hand-tuned scores are retired as the source of truth. → recommend opening a follow-up task (nutrition-data + frontend reconciliation). Yogurts stays **NO-GO** until this closes.
- **Bread (P0 #4) — DECIDED: `bread_retail_003` is authoritative.** It is the corpus the frontend ships; `bread_light` is relabelled experimental and archived. Freeze the 24 displayed once the `limitingFactors` field gap (Launch §6) is closed. Bread moves from BLOCKED toward **CONDITIONAL GO** on that single remaining gate.

Both decisions are reflected in §4 (freeze readiness) and §5 (go/no-go); the run-authority decision removes the bread ambiguity in §1.
