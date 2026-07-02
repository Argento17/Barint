# P258 / De-chain Stage 2 — continuous NOVA-replacement feasibility challenge (route: C3)

Repo C:\Bari. You are C3 (independent challenge/consult) — advice only, you write NO files and make NO code changes. Read-only reasoning + a written verdict.

## Context
Bari's BSIP2 engine currently scores food processing via a rigid NOVA-class lookup. The de-chain program (TASK-395) wants to REPLACE that hard lookup with a CONTINUOUS, label-derivable processing assessment that also subordinates NOVA to outcome signals. A 2026-07-01 activation eval proved the ready stage (Stage 0 WFI-scaling + Stage 1A D4-additive) does NOT resolve the motivating inversion: Chokita (chocolate-filled cookie, 26.1/E) still outscores Petit-Beurre (plain refined-starch cookie, 21.4/E). Resolving that pair is exactly Stage 2's job (the D6 "Workstream 1" NOVA-lookup replacement), which the D6 proposal flagged as "not yet label-derivable."

Read for grounding (do not edit): `03_operations/bsip2/proto_v0/reports/dechain_d6_proposal_v1.md` and `d7_cosign_dechain_v1.md` (Stage 2 / Workstream 1 sections); `.claude/scoring.md`.

## The challenge — answer rigorously
1. **Feasibility:** Is a continuous, LABEL-DERIVABLE processing/NOVA signal actually achievable from the data Bari has (Israeli back-of-pack ingredient lists + nutrition panels, per the OFF-ban — no OFF, ever)? What is derivable from the label vs genuinely NOT derivable? Be concrete about the signal (e.g. count/type of refined markers, additive classes, structure-loss cues) and its ceiling.
2. **Approach options:** Propose 1–3 concrete designs for the continuous processing score that would let Petit-Beurre (refined starch, plain) score at/below Chokita rather than above it — WITHOUT hard NOVA lookups and WITHOUT manufacturing differentiation. State the mechanism, the label inputs, and the failure modes of each. Recommend one.
3. **Inversion guardrail:** How should BARI-INVERSION-TEST-001 be formalized as a machine-executable invariant (the pair(s) it must hold, the property it asserts, how it stays label-grounded and not overfit to two products)?
4. **Risks/traps:** shared-parser spillover across categories, endemic-food false positives, double-counting vs the existing D4 additive path, and any way this could invert OTHER pairs. What must the shadow prove before activation?

## Return
A crisp verdict: FEASIBLE / PARTIALLY-FEASIBLE / NOT-FEASIBLE-ON-CURRENT-LABELS, the recommended design, the inversion-test spec, and the top 3 risks. You do NOT decide or build — Nutrition owns the methodology, orchestrator brings it to owner. End with the machine-readable return contract (01_framework/operations/return_contract_v1.md).
