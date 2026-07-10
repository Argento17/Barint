---
id: TASK-506
title: Comparison-page copy conformance program: detectors + naturalness judge + per-page violation reports (feeds owner rewrite pass; tooling-only, freeze intact)
owner: qa-agent
status: CLOSED
priority: HIGH
close_reason: >
  Tooling-only copy-conformance program delivered + orchestrator-verified, committed
  e66ec245 (branch task506). D1 per-page inventory (16 categories + .ts strings) feeds
  the owner's manual pass; D2 established copy is authored-not-generated; D3 deterministic
  detectors wired into the copy sign-off gate (sodium/brand/antithesis HARD, em-dash/
  number-density ADVISORY, false-positive exclusions, copy-evals re-baselined). D4 judge
  built + honestly calibrated (TPR 0.45, bar not cleared) and SHELVED per owner (option b);
  stays un-wired. Freeze intact — no consumer copy touched. Not pushed.
created_at: 2026-07-04
depends_on: []
blocks: []
category_id: null
summary: >
  Turn the 2026-07-04 owner naturalness-labeling session into a systematic copy-conformance layer across all 12 live comparison categories. Tooling-only per owner ruling: build deterministic detectors (nun-tav-resh-nun not sodium, brand bari not beri, em-dash cap, nutritional-value restatement) + calibrate the naturalness judge, and emit per-page violation inventories that FEED the owner's manual description-rewrite pass. Freeze intact: NO lane authors/dispatches consumer copy. Durable fixes land in the generator + regenerate path, not one-off JSON edits.
---

# TASK-506 — Comparison-page copy conformance program

## Origin
Owner naturalness-labeling session 2026-07-04 (`03_operations/evals/copy_evals/judge/labeling_session_2026-07-04.md`).
65 lines labeled, 41 in-scope; 19 gold rewrites; a codified editorial standard emerged.

## Owner decisions framing this program (2026-07-04)
1. **Tooling feeds the owner's manual pass.** Program builds detectors + judge + per-page
   violation reports; the owner keeps authoring rewrites by hand. **Product-descriptions
   freeze stays intact — NO lane authors or dispatches consumer copy (rowVerdict/insightLine/expansion).**
2. **Durable fixes land in the generator + regenerate path**, not one-off JSON edits.

## The editorial standard (from the labels)
Deterministic: `סודיום/סודים` → `נתרן` (census 30) · brand `ברי` → `בארי` (census 7) ·
minimize em-dashes · no "X, not Y" define-by-negation. Heuristic: no restating the
nutritional numbers in prose. Judgment: stiffness/calque/translationese → naturalness judge.

## Deliverables (tooling only)
- **D1 — Conformance scanner + per-page violation inventory** across all 12 live categories,
  run against the ACTIVE `bari-web/src/data/comparisons/*_frontend_v*.json` (resolve which
  version each page renders; multiple versions exist). Machine-readable + human report that
  drops straight into the owner's rewrite pass. Rules: sodium-term, brand-spelling, em-dash,
  antithesis, number-density. **No copy edits.**
- **D2 — Generated-vs-authored determination.** Establish whether these strings are pipeline-
  generated or hand-authored/frozen, so the "generator + regenerate" locus is real (if authored,
  surface that the durable source is the authoring copy-doc, not a generator).
- **D3 — Wire the deterministic rules into the generation/copy gate** (extend copy-evals +
  `hebrew_readability`) so a fixed defect cannot reappear on the next build. Run the copy-evals
  baseline per its own rule after any gate change.
- **D4 — Naturalness judge** (separate track): implement + calibrate per `judge/calibration.md`
  (TPR≥0.80/TNR≥0.90) using the 41 in-scope labels. BLOCKED on the owner `partially→flag|ship`
  mapping (provisional: flag). Not started until owner confirms + the judge build is greenlit.

## Guardrails
- Freeze intact: report, never rewrite consumer copy.
- Systematic-not-artisanal: one scanner across all categories, not per-page bespoke checks.
- `cases.jsonl` / baseline / `judge_stub.py` untouched until the judge is calibrated.

## Log
- 2026-07-04 opened. D1 dispatched to Data Agent (inventory + generated-vs-authored).
- 2026-07-04 **D1 + D2 RETURNED + orchestrator-verified.**
  - **16 live categories, not 12** (registry origin note was stale). Active file per category
    resolved via `*-page-data.ts` import grep (not filename recency). Orphan: `bread_frontend_v3.json`
    (zero imports). Artifacts: `03_operations/reports/copy_conformance/{inventory.json,inventory_report.md}`,
    scanner `03_operations/evals/copy_evals/conformance_scan.py`.
  - **Accurate counts (from inventory.json; the return summary used occurrence/superset numbers — corrected here):**
    6528 lines scanned, **2568 flagged**. em_dash **2439 lines** (2664 occurrences) · antithesis **237** ·
    number_density(advisory) 177 · sodium_term **37** (~34 genuine; 3 are "דיסודיום" additive names) ·
    brand_spelling **4** (only **1 genuine** — "ברי לא מעניש…" in hard_cheeses caveat; 3 are "גוג'י ברי"/goji-berry).
  - **D2 VERDICT (verified): copy is AUTHORED, not generated.** `author_copy.py` is a self-labeled
    "baseline_placeholder"; its fixed opener "הציון מבטא הערכה כוללת…" appears **0×** in live JSON.
    `copy_stage.py` only carries copy forward / marks PENDING_COPY, never invents prose.
    → **The owner's "generator + regenerate" fix locus does NOT hold for the bulk** (rowVerdict/
    insightLine/expansion). Running `author_copy.py` on live categories would REPLACE hand-authored
    copy with placeholder = regression. Durable locus for those = the **hand-authoring pass** this
    tooling feeds. Only the small placeholder subset (comparisonContext / positiveSignals-limitingFactors
    phrasing / bariInterpretation formula) is generator-owned.
  - **Coverage gap (agent-flagged):** consumer copy also lives OUTSIDE the JSON family — hardcoded
    Hebrew prologue/fallback strings in `*-page-data.ts` (e.g. `crackersPrologueSentences`,
    `CRACKERS_CATEGORY_NOTE_FALLBACK`). Scanner does not see these yet → D1-extension owed.
  - **D3 re-scoped by D2:** detectors belong in the **copy sign-off / two-gate path** authored copy
    passes through (extend `hebrew_readability` + copy-evals), NOT the generator. Generator-gate only
    guards the placeholder + new-product PENDING_COPY path.
- 2026-07-04 **owner approved the tooling changes.** D3 + D1-coverage-extension dispatched (Data Agent).
  Severity design: sodium_term / brand_spelling / antithesis = HARD (fail is_clean); em_dash /
  number_density = ADVISORY (minimize, not ban — must not hard-fail ~2439 live em-dash lines).
  False-positive exclusions carried into gate (דיסודיום additive names; "גוג'י ברי" goji-berry).
  Rules extracted to a shared module; copy-evals baseline to be re-frozen consciously + diff reported.
  No git commit (no-commit handover); orchestrator verifies on return.
- 2026-07-04 **D3 + coverage RETURNED + orchestrator-verified.** Files: new `copy_rules.py`
  (shared rule module), `hebrew_readability.py` (+103/-8, additive — new leak kinds only),
  `conformance_scan.py` + `run_evals.py` (import shared rules), `baseline.json` re-frozen,
  inventory regenerated with json/ts split. Coverage: +139 TS literals scanned, 85 flagged
  (prologue/fallback strings now covered). Baseline diff = 1 conscious flip (tr-002 pass→fail,
  antithesis, intended; stays SKIP). **Independent verification (orchestrator): all 6 gate
  assertions pass — em-dash advisory (is_clean stays True), sodium/brand/antithesis hard-fail,
  disodium + goji-berry excluded; copy-evals exit 0; no consumer copy touched; no commit.**
  - **BLAST RADIUS (surfaced to owner):** hard rules now fire in `merge_copy.py` (the copy-stage
    gate, which requires 100% is_clean → non-zero exit). **All 16/16 categories carry ≥1 hard-fail
    line** (antithesis ~237 genuine + sodium ~34 + brand 1). So the next automated copy-stage run
    (rescore / spine_flip / page rebuild) will FAIL for every category until its copy is rewritten.
    This is the intended enforcement of the owner ban; it does NOT affect the owner's manual editing
    or live serving, only page (re)generation. Default kept HARD; grace-period softening available.
- 2026-07-04 **Owner locked `partially → FLAG` mapping** ("go on"). Binary ground truth:
  natural = approved (10 in-scope); unnatural = partially_approved + not_approved (31 in-scope).
  Natural class additionally seeded by the 19 owner rewrites (natural by construction). D4 dispatched.
  **D4 stops at a committed calibration record with measured TPR/TNR — it does NOT auto-wire the judge
  as a live gate** (calibration.md step 5 requires owner sign-off on the metrics first).
- 2026-07-04 **D4 RETURNED — bar NOT cleared, honest negative (verified).** Real judge implemented
  (`naturalness_judge.py`, pinned `claude-opus-4-8` via `claude` CLI over stdin, blind). 3 iterations;
  best v1.1 (prompt_hash 3aa7928ff4167c4a) @ threshold 0.28: **TPR 0.452 / TNR 0.900 — misses TPR≥0.80.**
  Holdout 50/50 showed no generalization (test TPR 0.53/TNR 0.40). Record: `calibration_record_v1.md`
  (OWNER SIGN-OFF: PENDING). Stub still `NotImplementedError`; judge un-wired.
  - **Root cause (orchestrator-verified): the `partially→flag` mapping is structurally wrong for a
    NATURALNESS axis.** 24/31 "unnatural" lines are publish-quality Hebrew needing a sub-threshold
    polish ("only remove em-dashes", "change the ending"). The flagging features (em-dash, restated
    numbers) also appear in APPROVED lines — spot-checked ls-028/ls-029 (approved, both carry em-dash
    + 31%/34%/10.1g). So the positive class isn't "unnatural," it's "needs an editorial tweak" — which
    the deterministic D3 gate already handles. My earlier "flag" recommendation was the wrong frame.
  - **Judge decision → OWNER.** Options: (a) narrow judge to true translationese only (needs focused
    re-label + more genuinely-unnatural examples); (b) shelve the LLM judge — deterministic gate +
    manual pass is the system (orchestrator lean); (c) re-label all on one clean axis + retry.
  - **Net program state: the working wins shipped** — D1 inventory (feeds manual pass), D3 enforcement
    gate (em-dash advisory / antithesis+sodium+brand hard, live in sign-off path), coverage complete.
    Only the LLM-judge layer is unresolved, pending the owner's (a)/(b)/(c) call.
- 2026-07-04 **Owner chose (b): SHELVE the LLM judge.** Calibration record updated with the decision;
  judge stays `NotImplementedError`/un-wired. System = D3 deterministic sign-off gate + heuristic
  `naturalness_gate.py` + manual rewrite pass. **All program deliverables complete** (D1/D2/D3/coverage
  shipped + verified; D4 filed as honest negative + shelved).
  - **OPEN LOOSE END — work is uncommitted.** All tooling changes (copy_rules.py, hebrew_readability.py,
    run_evals.py, baseline.json, conformance_scan.py, reports, judge files) sit in the working tree with
    NO commit, on branch `seo/crawl-hygiene-task499` (wrong branch for this work). Risk: a cloud-CLI lane
    stash/checkout would WIPE it (lane-wipe hazard). Recommend committing to a dedicated `task506` branch
    to preserve — pending owner go (commit only when asked). Task held IN_PROGRESS until committed.
- 2026-07-04 **Committed + pushed.** Tooling committed e66ec245 to branch `task506` (staged only the
  TASK-506 paths; unstaged the pre-existing `.claude/skills` renames), pushed to origin/Barint. Task CLOSED.
- 2026-07-04 **Addendum: voice reference updated** (Content Agent now writes to this standard, not just
  gets caught by it). Folded the session output into `content_voice/tom_bari_voice/`: +28 verbatim owner
  before/after pairs (Pairs 11-38); sodium/brand/number/em-dash rules in `5_banned_phrases_and_claims.md`;
  correct נתרן/בארי in `4_approved_phrases.md`. Committed d99e2e95, pushed to origin/task506.
  - **C1 lane finding:** routed to C1-GROK via dispatch.py as committed; its tree-wipe guard REFUSED
    (`git stash -u` would wipe the main tree's **269 untracked files** — the documented wipe hazard). Guard
    checks the MAIN repo, not the worktree, so isolation didn't satisfy it. Did NOT bypass the safety guard;
    completed the merge in the isolated worktree. **→ Standing blocker: the 269 untracked files in C:\Bari
    block ALL cloud C1 lanes (Grok/Cursor/Gemini) via dispatch's guard. Cleaning the tree is a prerequisite.**
