# Orchestrate digest — 2026-06-25 (UNATTENDED 3 AM run)

One full dispatch pass against `C:\Bari\tasks\`. Constraints honored: native-Sonnet C1 only (no cloud CLI lanes), no published-score moves, no consumer-facing deploys, autonomous close only on verified non-tripwire work. Branch: `task-374-toms-voice` (no commits this run — see *Notes on commits*).

## State at start (the frontier is owner-gated)
The entire category-rework sweep is **deployed and live, pending owner live-review** — granola (TASK-385), breakfast-cereals (TASK-387), chocolate-tablets (TASK-391, CLOSED), cookies-coffee (TASK-393), magnesium v3 (TASK-384), brand-names across 9 shelves (TASK-392, CLOSED). Those are owner-gated walls, not actionable unattended. The remaining big item, **TASK-395 (de-chain the engine)**, moves published scores across all 12 categories and starts a major program → tripwires #1 + #3 → owner-gated. So the only genuinely-ready, non-tripwire, non-deploy work was internal-artifact follow-ups.

## Dispatched (2 → native Sonnet C1, parallel, independent files)
- **TASK-383(b)** → Research Agent (native): harden `verify_citations.py` with an author-surname + year cross-check to close the F-10 same-domain-miss gap.
- **TASK-384** (post-publish queue #1) → general-purpose (native Sonnet): write the owner-requested magnesium post-mortem.

## Closed (with evidence)
No registry tasks reached `CLOSED` this run — both dispatches advance multi-part tasks that remain legitimately IN_PROGRESS (TASK-383 has open follow-ups a/c + 2 new findings; TASK-384 is live-pending-owner-review). Both **deliverables** are complete and orchestrator-verified:

- **TASK-383(b) — verify_citations.py hardening — VERIFIED DONE.**
  - Scope: `git diff --stat` = `verify_citations.py` only, +474/−9; no score/JSON/engine/consumer files touched. Post-mortem is the only other new (untracked) file.
  - `python 03_operations/validators/verify_citations.py --selftest` → **8/8 PASS, exit 0**, including the live round-trip on PMID 28615384 (Thorning claimed → Salas-Salvadó resolved → **MISMATCH**) — the exact F-10 case the old heuristic missed is now caught end-to-end.
  - `--all` sweep → 55 checked / 51 PASS / **2 MISMATCH** / 0 FABRICATED / 2 UNRESOLVED-DOI. The 2 MISMATCHes are **genuine, independently confirmed** (see Findings), not false positives — the hardened gate working as designed.

- **TASK-384 — magnesium post-mortem — VERIFIED DONE.**
  - `02_products/supplements/magnesium_v3_postmortem_v1.md` (24 KB) written; structure verified (timeline cycles 0/1/2 · grouped root causes · gates caught-vs-missed · concrete recommendations · net assessment). Exec-summary facts cross-checked against the board record and accurate. Old cycle-1 file `magnesium_postmortem_v1.md` left intact; new file states it supersedes it.

## New findings (the hardened citation gate's first catch — route to Research)
Both are **governance-doc attribution errors → no published-score / consumer impact, no tripwire.** Correction = QUEUED Research work (resolve the correct PMID for each claim, or fix the attribution text):
1. `01_framework/glass_box/diaas_source_table_v1.md:52` — PMID **37357639** attributed to "Nosworthy et al. (2023)" but resolves to Bailey/Fanelli/Stein 2023 (rapeseed heat-treatment). (Same PMID is used correctly for rapeseed claims elsewhere in the file; line 52 is the mis-attached one, paired with a whey-protein claim.)
2. `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md:2430` — PMID **9771853** cited "Willett 1997" resolves to Judd et al. 1998 (margarine/butter). Board had flagged borderline; now deterministically caught.

## Blocked
- **TASK-393 (cookies-coffee)** — deployed/live, IN_PROGRESS pending owner live-review (not blocked on work).
- BLOCKED-status tasks untouched (stale/long-standing): 182, 236, 270, 281, 282, 286, 331, 342, 390. None became ready.

## Parked-for-owner (tripwires / deploys — HALT points)
- **TASK-395 — de-chain the BSIP engine.** Tripwire #1 (published scores across all 12 categories) **and** #3 (start a major program). Owner-directed in principle (2026-06-24) but needs supervised design + go/no-go; not run unattended.
- **Owner live-review backlog** (all deployed, awaiting owner eyes): magnesium v3 (TASK-384/384A), granola (TASK-385), breakfast-cereals (TASK-387), cookies-coffee (TASK-393). No action available to the orchestrator until the owner reviews.
- **Any further category deploy** = tripwire #2 → owner's separate step.

## Queued-for-supervised-lanes (need cloud CLI — NOT run unattended)
- **TASK-383(d-new):** correct the 2 attribution errors above — small, but a Research/judgment call (find the right citation). Can be native-Sonnet in the supervised session; no cloud lane strictly required.
- **TASK-383(a)/(c):** wire `verify_citations.py` as a standing CI gate + D7 pre-condition; re-ground the EV-024 fermented-dairy claim.
- **TASK-386 (LOW):** coconut→palm-oil detector false-positive — an engine-detector change; "0 current impact" must be re-measured with a full re-score sweep before any change ships (tripwire-adjacent). Defer to supervised.
- **TASK-384 post-publish deferrals:** H-1 supplements discoverability (Product), H-2 magnesium theme image (Design), M-1 systemic grade-chip contrast (Design), Tink label re-attempt, skus_full JSON sync.

## Notes on commits
No commit this run. The two artifacts sit **uncommitted in the working tree** on `task-374-toms-voice` (already dirty with TASK-381 Hebrew-Health-Scan WIP — ~140 modified / ~450 untracked). Committing them to a dedicated branch would *hide* them from the working tree on branch switch-back, reducing owner visibility; leaving them in place is lower-risk for the supervised morning review. Files to review/commit:
- `03_operations/validators/verify_citations.py` (hardening, +474/−9)
- `02_products/supplements/magnesium_v3_postmortem_v1.md` (new report)

## WALL
Out of ready non-tripwire work. Everything else is owner-gated (live-review, deploys) or a tripwire (TASK-395, TASK-386 re-measure). Handing back to the owner for the supervised morning kick.
