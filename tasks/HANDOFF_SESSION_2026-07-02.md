# SESSION HANDOFF — 2026-07-02 (gate-liveness / OFF / OCR / git-hygiene sweep)

**For the next chat:** read this file, then run `/roadmap`. Everything below is verified state as of end-of-session. The registry (`C:\Bari\tasks\`) is authoritative; `tasks/DISPATCH_BOARD.md` is the live view.

---

## TL;DR — how this started and where it went
Owner asked to review the Project Comp daily → surfaced a stale-MoH-threshold finding (TASK-442) → then "what am I missing from my tool stack?" → a capability audit (TASK-447) that uncovered a **systemic pattern: most of Bari's safety/quality gates are DESIGNED but NOT WIRED to fire** (see memory [[gates_designed_not_enforced]]). Chasing that produced: an OFF-ban breach (contained), a lost citation gate (restored — immediately caught 4 real defects), an OCR-enrichment inventory, and a full git cleanup. **The main working tree is now CLEAN.** Several owner decisions are open (below).

---

## THE ONE BLOCKER (owner decision needed first)
**Which branch is the live Agent-OS line?** Gate/governance fixes this session are SCATTERED across branches and none are consolidated to master. This matters because **verify_citations.py was lost precisely because it lived only on an unmerged branch** — and we're at risk of repeating it. Need: "consolidate all gate fixes onto `master` (or the confirmed live line) and merge." Ties to [[deploy_topology_main_vs_monorepo]] + [[local_origin_brain_divergence]]. Until decided, do NOT scatter more fixes.

### Branch/commit map (session artifacts — CRITICAL, do not lose)
- `master` @ **65e6a33d** — TASK-442 Track B (removed false MoH-threshold attributions; score-neutral). This is the honesty copy fix; already on master.
- `feature/homepage-mascots` (CURRENT checkout, clean) — **e4cd6d30** verify_citations restore (LIVE C0 gate) · **6871d374** WIP snapshot (889 files, swept whole tree incl. scratch) · **9b640dd** crackers frontend. Mascots also at **8a31565b**.
- `task448/off-ban-neutralize-callers` — **beab5572** (neutralize 5 OFF-importing scripts) · **1ec15bbf** (off_sweep detector fix). NOT on master → off_sweep fix is NOT live on the running branch.
- `task442/moh-redlabel-2021` — **d79c01c8** dormant flag `BARI_MOH_REDLABEL_2021_V1` (corrected MoH thresholds, default-OFF, EV-108).

---

## TASK-BY-TASK STATE

### CLOSED this session
- **TASK-448 (CRITICAL) — OFF-ban breach: NO LEAK.** 16/16 live categories verified clean at corpus level (0 OFF-origin nutrition displayed). OFF client hard-disabled at source (`OFF_DISABLED=True`). 5 caller scripts neutralized (raise-guard) → committed beab5572. Did NOT delete the OFF client file (needs owner written policy per hard rule). Memory: [[off_ban_enforcement_verify_by_census]].
- **TASK-450 (HIGH) — off_sweep detector fixed.** Was stale hardcoded filenames → reported "clean" while blind. Now discovers live targets dynamically from `public-corpus-registry.ts`, fails loud. 16 cats scanned, 0 OFF. Committed 1ec15bbf. Residual: v1 `run_off_sweep.py` same defect; corpus-scan blind for hard_cheeses/juices (bsip1-index gap).
- **TASK-452 (HIGH) — verify_citations C0 gate RESTORED + LIVE.** Source was lost (only committed at c90d49ef on an unmerged branch; master never had it → C6 was format-check+WARN only for weeks). Recovered, reconciled w/ newer .pyc, added the `--json` stdin contract, fixed acronym stop-word bug. Committed **e4cd6d30 on feature/homepage-mascots (kept LIVE)**. Follow-up: 'IJE' journal-abbrev stopword gap (2 false MISMATCH in --all mode only; C6 path safe) — better fix = don't treat ALL-CAPS tokens as surnames.

### RETURNED / verified (not yet actioned)
- **TASK-447 (MEDIUM) — capability audit DONE.** 17 capabilities classified. Dormant holes: (1) OFF breach→448; (2) ~10 authoritative research clients (pubchem/dsld/usda_fdc/literature/openfda/crossref/biorxiv/semantic_scholar/tzameret) built + self-test-green but wired to ZERO prod stages; (3) image/OCR dark (Azure OCR prototype=446, rembg + google_cloud_vision unused, no image-fetch/dead-image/perceptual-hash). GAPS: rapidfuzz (cross-retailer match), imagehash.
- **TASK-451 (MEDIUM) — evidence-client wiring PLAN delivered.** Ranked: #1 restore verify_citations (DONE via 452); #2 crossref retraction signal → Red-Team ledger; #3 pubchem as D4 identity-corroboration (identity-only, never writes a tier/delta). **BLOCKED:** food_additives (OFF-sourced + score-affecting + only in Bari-task243 clone). Score-affecting (need Nutrition/Product co-sign): dsld, usda_fdc. tzameret directional-only needs a CODE guard.
- **TASK-453 (HIGH) — GATE-LIVENESS SWEEP DONE. The key strategic finding.** Only **G1–G8 (run_gates) genuinely auto-fires + fails-closed**. Everything else thinner: **C0 return-contract (validate_return.py) is ADVISORY** (nothing auto-runs it; "auto CHANGES_REQUESTED" is a doc promise, no enforcer); **Stage-9 red-team + inversion/monotonicity/baseline/provenance invariants are DECORATIVE** (not imported by run_gates; onboard just PRINTS a reminder); **CI runs only lint+build+regression** (a11y/perf/visual/lhci exist, no workflow runs them); **two-gate content sign-off is thin** (only hebrew_readability wired; sign-off = self-attested `red_team_cleared` date); **conformance not re-checked on spine_flip**. Fix order: 1) off_sweep→CI + port fix, 2) wire Stage-9+invariants into run_gates, 3) enforce C0 in /orchestrate, 4) wire naturalness/grammar + real red-team artifact, 5) CI a11y/perf/visual, 6) conformance in spine_flip.
- **TASK-454 (HIGH) — citation triage DONE.** 2 clerical fixes APPLIED (uncommitted-then-swept-into-6871d374): PMID 37357639 Nosworthy→Bailey; PMID 9771853 Willett1997→Judd1998. **3 routed to Nutrition (evidence-tier/scoring fields — do NOT auto-edit):**
  - PMID 31122155 (NOVA / underpins D6 `BARI_HC_NOVA1_V1`) = a nursing case study; correct paper = Monteiro 2019 **PMID 30744710**. Verdict: weakened-by-wrong-citation, NOT scientifically invalidated; and EV-099 already governance-BLOCKS the reclassification independently. Fix PMID when EV-100 is drafted.
  - DOI 10.1016/j.cell… → unrelated; correct = Chassaing 2022 Gastroenterology **PMID 34774538 / DOI 10.1053/j.gastro.2021.11.006**. Feeds LIVE signal `mucus_thinning_emulsifier_load` (tier-A). Clean typo-fix, Nutrition co-sign to apply.
  - DOI 10.3390/nu11081781 → unrelated (Ramadan/skin study); **UNRESOLVED** — feeds the fermentation bonus (EV-024, tier-A). Nutrition must re-source or **downgrade tier (potential score move → tripwire)**.

### SCOPED, ready to dispatch (not started)
- **TASK-446 (HIGH) — productionize the Azure OCR prototype into a BSIP0 label-image fallback.** UPDATED INVENTORY (verified end-of-session): the prototype at `03_operations/bsip0/pipeline/` is a fuller 4-stage mini-pipeline, NOT just a client — `main.py` (Azure DocIntelligence layout+tables + cache), `extractor.py` (Hebrew nutrition parser: 9 per-100g fields w/ per-100g-column detection, ingredients, allergens מכיל/עלול-להכיל, metadata brand/country/SKU/kosher/passover/parve, per-field warnings), `evaluate_parser.py` + `ground_truth.xlsx` (accuracy harness), 10 real snack-bar products w/ multi-image label sets. **Measured accuracy = 40.7% (33/81 fields)** but clean-table cases hit 8/9 and 9/9 → parser capable, not yet robust; cholesterol missed even on clean case. `google_cloud_vision` installed but unused (2nd engine). Build = wire into BSIP0 + harden parser past 41% + confidence gate (fail-to-NULL, never guess) + enforce OFF image-ban + measure rescue-rate.

### BLOCKED / parked
- **TASK-442 (HIGH) — BLOCKED on owner go/no-go.** Nutrition strategic ruling (owner "drift away from red-label"): the de-anchor the owner wants ALREADY EXISTS (`BARI_REDLABEL_V1` + TASK-395 de-chain, at owner tripwire, SPLIT GO-10/NO-GO-2). **Ruling: do NOT activate the tighter MoH thresholds now** (they feed the binary mechanism about to be de-anchored; the 27 downward grade flips = churn de-anchor partly reverses). Track A parked behind TASK-395; **Track B (copy honesty fix) SHIPPED to master (65e6a33d)**. Owner decision pending: (i) resume TASK-395 staged de-anchor activation (tripwire-1)? (ii) confirm hold on 442 Track A? Prereq: BARI-INVERSION-TEST-001 not canonically landed (reframed on branch p277). EV-108↔EV-049 joint check before cereal/granola.

---

## OPEN OWNER DECISIONS (ranked)
1. **Live-line / consolidation** (THE blocker) — which branch to consolidate all gate fixes onto; authorize merge to master.
2. **Nutrition triage** of the 3 routed citations (TASK-454) — esp. the fermentation-bonus DOI that may force a tier downgrade (score move).
3. **Gate-enforcement program** (TASK-453 backlog) — greenlight to make the decorative gates actually fire (owner already said "go on" toward the gate-liveness sweep; the *fixes* are the next step, gated on #1).
4. **TASK-442 / TASK-395 de-anchor** — resume staged activation or hold.
5. **bari-pub-mag3 worktree** — ⚠️ 14,537 uncommitted changes incl. deletions of `.claude/agents/*.md`, LOCKED. Looks mangled (possible cloud-lane git-wipe). Untouched — needs owner call (investigate read-only, or discard).
6. **TASK-446 OCR build** — dispatch when ready (scope updated with the 40.7% baseline).

---

## GIT / TREE HYGIENE STATE (end of session)
- **Main tree `C:\Bari` (feature/homepage-mascots): CLEAN (0 uncommitted).** Mascots + all frontend committed; crackers committed (9b640dd).
- Removed scratch worktree `C:\bari_task442`. Remaining worktrees: `bari_phase2` (clean), `bari_p277` (2 trivial scratch files), `bari-pub-mag3` (the mangled/locked one — see decision #5).
- ⚠️ The WIP snapshot **6871d374 committed a lot of scratch** (`.tmp_*`, dumped HTML, one-off scripts) — tree is clean but history is junky; optional deliberate prune later.

## HAZARDS / GOTCHAS (carry forward)
- [[lane_dispatch_wipes_shared_tree]] — cloud CLI lanes at cwd=C:\Bari run git ops on the whole tree (the likely cause of the bari-pub-mag3 mess). Isolate agents in worktrees; verify tree after.
- The board (`DISPATCH_BOARD.md`) and some task/memory files were being externally modified mid-session (linter/user) — re-Read before Edit.
- **Memory index compaction DEFERRED** — `MEMORY.md` ~19.6KB approaching the 24.4KB read limit; harness asked to compact under 17.1KB. Do this carefully (merge/drop stale, don't lose content) when not mid-critical-thread.

## MEMORY ADDED THIS SESSION
- [[off_ban_enforcement_verify_by_census]] — prove OFF-clean by import-census + record-level trace, not commit messages or the detector alone.
- [[gates_designed_not_enforced]] — only G1-G8 auto-fires; verify gate WIRING not existence; fixes must land on the live line.
