# P277 / TASK-419 Stage-2 — continuous processing score behind a flag (route: C1 engine build)

## Charter (owner: "hold activation, BUILD Stage 2")
Build the Stage-2 de-chain increment: replace the rigid NOVA-class lookup's dominance in scoring with a
continuous, label-derivable **processing-burden** signal (P258 Design 1 "Refined Matrix Degradation Score"),
behind a NEW flag, OFF by default. This resolves the Petit-Beurre/Chokita inversion that Stage 0+D4 did not.
**Do NOT activate.** Score-moving ⇒ D6/D7 + owner-gated later. This task delivers a reviewable, score-neutral
(flag-off) build + a shadow measurement.

## Isolation
Worktree **C:\bari_p277** ONLY (off master 7733065a). NO git commands. Deploy nothing. Engine at
`03_operations/bsip2/proto_v0/src` (score_engine.py, nova_proxy.py, signal_extractor.py).

## Read first
- `C:\Bari\tasks\returns\P258_return.md` — the accepted feasibility + **Design 1** (continuous label-observable
  processing burden: refined-substrate markers penalized even at zero additives; whole-food complexity credited;
  additives contribute but do NOT duplicate D4; nutrition as corroboration; NOVA demoted to non-authoritative
  proxy) + the `BARI-INVERSION-TEST-001` fixture.
- `C:\Bari\tasks\TASK-419.md` (the 2026-07-01 orchestrator update with the accepted design).

## Deliverables (in priority order — partial-but-verified is acceptable; be honest about what's done)
1. **Flag scaffold + BYTE-IDENTICAL-OFF (the hard safety requirement).** Add a new flag (e.g.
   `BARI_PROC_CONTINUOUS_V1`), default OFF. With it OFF, the engine MUST be byte-identical to current. PROVE it:
   run `03_operations/page_generator/rescore_all.py` (or re-score every live category) OFF vs current HEAD and
   show **0 score/grade changes across all categories**. If any category moves with the flag off, it's a bug — fix
   until 0. This guarantee is non-negotiable.
2. **`BARI-INVERSION-TEST-001` as a machine test.** Encode the dominance invariant `score(PetitBeurre) <=
   score(Chokita)` (plain refined-starch cookie must not outrank the chocolate-filled one under the same config)
   as a runnable pytest/script fixture using their REAL direct-label data (locate the products in the
   corpus/comparison data; if absent, construct the fixture from documented label data — no invention beyond the
   real label). Add the generalized fixture families P258 lists if feasible.
3. **Design 1 implementation behind the flag (ON path).** Implement the continuous processing-burden signal per
   Design 1. Wire it so that ON, NOVA is demoted to a corroborating proxy and the refined-matrix burden drives the
   processing dimension.
4. **OFF/ON shadow.** Re-score the affected categories (esp. chocolate/cookies/snacks + a broad sample) OFF vs ON;
   report: does `BARI-INVERSION-TEST-001` PASS with the flag ON? per-category movement distribution, grade moves,
   any NEW inversions introduced, and inversion-invariant status. No deploy, no activation.

## Guards
- Flag OFF = byte-identical (hard gate). OFF-ban absolute. Do not change any published score (flag stays off).
- Do not close. Propose RETURNED.

## Return (`C:\bari_p277\tasks\returns\P277_return.md` + final message)
- Byte-identical-OFF proof: rescore_all OFF vs HEAD = 0 changes (paste the summary + command).
- The inversion machine-test: file path, and PASS/FAIL both OFF (baseline) and ON.
- Design-1 status: implemented / partial (what remains).
- Shadow table: OFF→ON movement per category (distribution + grade moves), inversion resolved? new inversions?
- Return contract (`01_framework/operations/return_contract_v1.md`): artifacts w/ sha256, counts w/ named
  denominators, distribution marker. Be honest about partial completion — a verified flag+test+byte-identical-off
  with a partial Design-1 is a good, safe increment; do not overstate.
