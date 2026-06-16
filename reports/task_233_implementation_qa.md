# TASK-233B/C/D Implementation QA — Final Validation

**Date:** 2026-06-10 · **Branch:** `salty-snacks-v4` · **Mode:** READ-ONLY (verifier; nothing fixed)
**QA Agent (Bari).** Validates the Phases 1–2 implementation of the TASK-233 sweep fixes.

## Verdict

| Subtask | Verdict |
|---|---|
| **TASK-233B** (shared packaging core + confidence) | **PASS** |
| **TASK-233C** (editorial copy routing + grade-literal strip) | **PASS** |
| **TASK-233D** (targeted data fixes) | **PASS** |
| **OVERALL** | **PASS WITH FIXES** — implementation is clean and ships safely on the leak/grade/dup/confidence/build axes. The one "FIX" is a **release-gate gap, not an implementation defect**: frozen_vegetables has **no red-team report**, so QA Hard Rule 9 blocks its go-live PASS (its own hold-gate condition #3 also depends on the 233A validation gate, which passes). Salty-snacks, by contrast, is fully gated and clean. |

No score-methodology change occurred in any validated artifact. No blocker is routed for the implementation itself; one go-live prerequisite (frozen-veg red-team) is routed to red-team-agent.

---

## Subtask 1 — Leak / `is_clean` sweep (Check 1)

Ran `hebrew_readability.analyze().is_clean` over **1,494 consumer strings** across all 7 touched JSONs
(insightLine, rowVerdict, confidence_label_he/tooltip_he/sub_reason, all expansion text + nutrition rows).

- **NN/X grade literals: 0.** Content's strip is complete across frozen_veg / snacks / cereals / bread.
- **Framework leaks: 0 real.** One raw hit (`yogurts` yog-005 insightLine, term "נובה") is a **false positive** —
  it is the substring `נובה` inside the brand name **תנובה (Tnuva)**. Verified no standalone `נובה`
  (`(?<![א-ת])נובה(?![א-ת])` → no match). The scanner lacks Hebrew word boundaries on multi-char terms.
- **Recommendation leaks: 0.**
- **48 strings fail `is_clean` solely on the `\d{2,3}\.\d+` rule** (Content reported 41; the extra 7 are the
  yogurts/butter strings outside Content's 4-category patch scope but inside the touched set). **Confirmed every
  one is a composition fact, not a score mechanic** — e.g. cereals `24.7 גרם סוכר`, yogurts `10.5 גרם חלבון`,
  snacks `37.3%` peanuts, butter rowVerdict `D/45.2` (the `45.2` is the displayed score-as-fact paired with its
  grade, not a `NN/X` mechanic — and the disk score is now the integer 45; see Check 3/float). **These are the
  gate's bare-decimal false-positive, NOT score mechanics.** 0 strings fail for any reason other than bare
  decimals / the Tnuva false positive.

**Result: PASS.** True leak count (framework + score-mechanic + recommendation) = **0**.

## Subtask 2 — Frozen-veg confidence integrity (Check 2) — `frozen_vegetables_frontend_v1.json`

- All **53/53 products now `confidence: partial`** (was 53× verified/"full data"). Label distribution:
  29× `מבוסס על נתונים חלקיים`, 24× `חסרים נתוני תזונה`.
- **verified-with-`unknowns` contradictions: 0.** No product claims full data while carrying gaps. (DA-005/DA-006 fixed.)
- **`ממקור המזון הרשמי` (the overclaiming "official food source") appears 0× anywhere in the file** (raw substring count 0).
- Tooltips are the canonical **partial-confidence** lines (`הציון מבוסס על נתונים חלקיים…` / `חלק מנתוני התזונה לא היו זמינים…`).
  Note: the canonical *verified* tooltip (`…רשימת הרכיבים ולוח התזונה המלאים`) correctly count = 0 here, because **no
  frozen-veg product is verified** — partial tooltips are the right canonical line for this confidence state.

**Result: PASS.**

## Subtask 3 — Grade consistency / DA-009 (Check 3)

Disk `grade` vs score-derived grade (A≥80/B≥65/C≥50/D≥35/E) for every product in all 7 files:

| file | products | mismatches |
|---|---|---|
| frozen_vegetables_v1 | 53 | 0 |
| salty_snacks_v4 | 38 | 0 |
| yogurts_v3 | 18 | 0 |
| snacks_v2 | 18 | 0 |
| butter_v2 | 31 | 0 |
| cereals_v2 | 34 | 0 |
| bread_v2 | 19 | 0 |

**0 mismatches total.** DA-009 drift eliminated; disk == `corpus.ts frontendGradeFromScore`. **Result: PASS.**
(Also verified: **all scores are integers** — butter `45.2` is now `45`, QA-007 fixed.)

## Subtask 4 — Duplicate barcodes (Check 4)

- yogurts `7290107936309`: **resolved** (no dup). snacks `7290011498894`: **resolved** (no dup).
- Full scan of all 7 files: **0 duplicate barcodes anywhere.** (QA-005/QA-006 fixed.) **Result: PASS.**

## Subtask 5 — Internal-field leak (Check 5)

Non-VM keys **still present as keys in the JSON** (unmigrated categories): yogurts/snacks/cereals/bread carry
`source_traceability_status`, `confidence_level`, and cluster fields (`_cluster`/`_internal_cluster`/`_website_cluster`,
`_subpool`/`_isChildrens`/`_wholeGrainClaim`); salty carries `subPool`. **This is expected** per the prompt's
"stripped at load vs absent from JSON" distinction.

**They are stripped at load and never reach the rendered VM.** Verified in `bari-web/src/lib/comparisons/corpus.ts`:
`loadComparisonCorpus → stripInternalProductFields` emits **only** `ALLOWED_PRODUCT_KEYS` (the `BariProductVM`
allowlist + 6 intentional lens keys `_subpool/_isChildrens/_wholeGrainClaim/subtype/subPool/_product_type`).
`source_traceability_status`, `confidence_level`, `novaGroup`, and the cluster fields are **not** in the allowlist
→ dropped. `assertProductConforms` adds a runtime conformance gate (id/name/confidence/expansion present, score
integer-or-null, grade A–E-or-null). All 6 consuming page-data files (frozen-veg, yogurts, snacks, cereals, bread,
butter) route through `loadComparisonCorpus` and their **local strips were removed** (confirmed by inline comments
+ no residual `delete`/omit in the load path). **Result: PASS.**

## Subtask 6 — Frozen-veg image URLs (Check 6)

- 53/53 imageUrls non-null; **53 distinct real scraped Shufersal/Cloudinary prefixes** (no longer one broadcast guess).
- The broadcast-`MNH68_` 404 bug is gone: only **1** product carries `MNH68_` and it is that product's **real** prefix
  (`MNH68_Z_P_7290018989456_1.png` → HTTP 200).
- HTTP HEAD sample (9 URLs incl. first 6 + index 20/46/52): **9/9 → HTTP 200.** (DA-006/233D image fix verified.) **Result: PASS.**

## Subtask 7 — salty_snacks_frontend_v4 deltas — CRITICAL analysis (Check 7)

**Characterization of the change:**
- The shipped `salty_snacks_frontend_v4.json` is **new on this branch** (absent on `master`; +1553 lines). The
  file's working-tree state **== committed HEAD** (`d7a082c7`) — no uncommitted score/grade deltas, no added/removed
  barcodes in the working tree. The deltas in question (41→38, 61→63, 42→43, 25→14, C→B) were committed as part of
  the v4-rebuild branch, and the file's own `_meta.task234_remediation` block documents every one of them.
- **The deltas are caused ONLY by corrected input data + exclusion logic — NO scoring methodology changed.**
  Confirmed independently:
  - **No engine/scoring source changed** in the working tree (`git status` shows only generators
    `03_build_frontend_v4.py`, `run_confidence_annotation_pass.py`, new `frontend_core.py`, `task233c_copy_patch.py` —
    no engine, no `grade_governance`, no scoring rule).
  - `_meta` states twice: **"Engine unchanged (engine-baseline-2026-06-04 + TASK-216)"** and rt7 **"Score-neutral."**
  - 61→63 / 42→43: OFF `trans-fat_serving=0.5g` ("<1g" declaration artifact) neutralized to 0.0 → re-scored on the
    **unchanged** engine. 25→14: impossible 38g/100g fiber set to None → re-scored on unchanged engine. C→B on
    `7290000066332`: same data-correction class. 41→38: 3 products (`7290018198254/…198148/…4943738`) dropped as
    `basis_error_excluded` (per-serving panel mislabeled per-100g, 128–145 kcal vs real ~450–540, unrecoverable).

**Scope-bleed recommendation:** The 3-product drop and the score deltas are **TASK-234** work
(`red_team_salty_snacks_v4.md` RT-2/RT-7/MEDIUM; TASK-234 is a registered HIGH task, `blocks: TASK-232`,
acceptance criteria cover exactly these corrections, explicitly "No scoring-engine change"). They are **not**
TASK-233 fixes.

> **Recommendation: do NOT revert; do re-attribute, not re-engineer.** This is a *bookkeeping* scope-bleed
> (TASK-234 data corrections landed in the same regen as TASK-233's packaging refactor on a shared branch), **not** a
> methodology scope-bleed. Reverting would re-introduce defensible-data defects the red-team already validated as
> corrected (phantom trans vetoes, impossible fiber, basis-error chips). All 38 published scores reproduce from
> current data through the frozen engine per the red-team report. **Action for the orchestrator:** keep the data as-is;
> ensure TASK-234's return block claims the 3-product drop + deltas so closing verification attributes them correctly,
> and do not close TASK-233B/C/D on the strength of TASK-234's deltas. No QA blocker.

**Result: PASS** (no methodology change; deltas are data-correction + exclusion, correctly belonging to TASK-234).

## Subtask 8 — Build (Check 8)

- `npx tsc --noEmit` → **exit 0**, no TypeScript errors.
- `npm run build` → **exit 0**, "✓ Compiled successfully", **48/48 static pages generated** (incl.
  `/hashvaot/frozen-vegetables`, `/hashvaot/salty-snacks`, and all 6 edited-JSON category routes). Confirms
  Frontend's 48/48 holds **after** Content's JSON edits. **Result: PASS.**

---

## FROZEN-VEG HOLD GATE — 4 release conditions

| # | Condition | Status | Evidence |
|---|---|---|---|
| 1 | Confidence contradiction fixed | **PASS** | 53/53 → `partial`; 0 verified-with-`unknowns`; `ממקור המזון הרשמי` 0× (Check 2) |
| 2 | Images return 200 | **PASS** | 9/9 sample HEAD → 200; broadcast-`MNH68_` 404 gone; 53 real per-product prefixes (Check 6) |
| 3 | Validation gate passes | **PASS** | tsc 0 / build 48/48; grade==score 0 mismatch; 0 dups; internal keys stripped at load; 0 true leaks (Checks 3/4/5/8) |
| 4 | Preview route reviewed | **OWNER'S CALL — not QA's.** | `/hashvaot/frozen-vegetables` builds clean; visual/preview sign-off is the owner's per the prompt. Not adjudicated here. |

**QA-owned conditions (1–3): all PASS.** Condition 4 is the owner's.

### Red-team gate (QA Hard Rule 9) — go-live readiness

- **salty-snacks: SATISFIED.** `02_products/salty_snacks/reports/red_team_salty_snacks_v4.md` exists, verdict
  CONDITIONAL PASS, **CRITICAL = "None"** (explicitly: all 41 published scores reproduce through the frozen engine).
  No open CRITICAL → Hard Rule 9 does not block.
- **frozen-vegetables: NOT SATISFIED.** No `02_products/frozen_vegetables/reports/red_team_*.md` exists.
  Per Hard Rule 9, a category go-live PASS cannot issue without it.

---

## Routed items

| Item | Severity | Route to | Note |
|---|---|---|---|
| frozen_vegetables has no red-team challenge report | **Go-live blocker (Hard Rule 9)** | **red-team-agent** | "Dispatch red-team-agent with the current frozen_vegetables corpus" before any frozen-veg QA PASS for go-live. Implementation itself is clean. |
| `hebrew_readability` scanner: `נובה` matches inside `תנובה`; `\d{2,3}\.\d+` flags composition decimals | LOW (tooling FP) | QA / tooling owner | Not a content defect. Word-boundary the Hebrew leak terms and exempt unit-suffixed decimals (`גרם`/`%`/`מ"ג`) to cut false positives. No action required for this release. |

## Notes
- No implementation defect found in TASK-233B/C/D. The only "WITH FIXES" item is the missing frozen-veg red-team
  report (a release prerequisite, not a code/data defect).
- This validation is **branch-local** (`salty-snacks-v4`, pre-merge) — the correct time to catch the frozen-veg gate gap.
- Verifier ran read-only; temp analysis scripts removed. No source edited.
