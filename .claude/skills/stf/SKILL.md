---
description: STF (Strategy Task Force) — owner-invoked hard-strategy consultation between the two SST models (Claude Fable 5 in-session + GPT-5.6 Sol via read-only codex). Independent positions first, capped adversarial debate, verdict memo with honest dissent. Never implements.
argument-hint: <the strategic question — stakes, options if known, what a good answer unlocks>
---

# /stf — Strategy Task Force

**Owner-invoked only** (owner ruling 2026-07-11). This is the standing primitive for *very hard
strategy meetings*: the two SST-tier models (see the tier map in
`01_framework/operations/capability_router_v5.md`, invariant 9) debate to the best outcome.
You (the session, Fable 5) are the Claude seat; GPT-5.6 Sol is the OpenAI seat, reached via
`strategist_consult()` in `03_operations/router/dispatch.py` (codex exec, READ-ONLY sandbox —
consultations never write files; stdout is the deliverable).

**STF never implements.** No builds, no dispatches of build lanes, no file changes outside the memo
and scratchpad position files. Output = a verdict memo + owner decision points. Anything actionable
becomes a registered task only after the owner accepts the recommendation.

## Protocol (anti-anchoring is the whole design — do not shortcut it)

**0. FRAME.** Restate the question in one paragraph: stakes, constraints (Bari hard rules that
bound the answer — OFF ban, tripwires, two-gate, freeze states), the real options space, and the
decision criteria (what would make one answer *win*). If the owner's question is ambiguous, sharpen
it WITH the owner before convening — this is the one workflow where a clarifying question is the
right move, because the frame determines everything downstream.

**1. INDEPENDENT POSITIONS (blind).** Write YOUR full position to a scratchpad file FIRST —
recommendation, reasoning chain, top 3 risks, kill-criteria (what evidence would change your mind).
Commit to it before reading anything from Sol. THEN dispatch Sol with the frame only (never your
position): same required structure. Two genuinely independent priors is what makes this more than
theater; a debate seeded with one model's take converges on that take.

**2. DEBATE ROUNDS (cap 3).** Exchange: attack Sol's position on its merits (counter-cases,
unstated assumptions, Bari-law conflicts); send Sol your position + your attack, require it to
attack yours and defend or CONCEDE point-by-point. Each round must do one of: converge a point
(mark AGREED), kill a point (mark CONCEDED by whom), or crystallize a **crux** — the smallest
testable claim that decides between positions, and what evidence would settle it. A round that does
none of these ends the debate (diminishing returns). Sequencing note: never run `strategist_consult`
while another dispatch.py lane is live (concurrent-dispatch hazard).

**3. VERDICT MEMO.** Write to `01_framework/governance/stf_memos/YYYY-MM-DD_<slug>.md`:
- The frame (as debated, including anything the owner sharpened).
- **Converged recommendation** — or, if convergence failed honestly, the surviving cruxes with the
  evidence that would settle each. **Never fake consensus**; a recorded dissent is a deliverable,
  not a failure.
- Risks, reversibility class, and the owner decision points (tripwire-tagged where applicable).
- Appendix: both blind position files verbatim (provenance of the debate).
Then give the owner the memo's core in the chat reply — recommendation first, dissent explicit.

## Guardrails
- SST models only. Sol unavailable → fable-only analysis, EXPLICITLY marked "degraded: no
  cross-vendor seat" — do not present it as an STF verdict.
- Read-only throughout: Sol runs sandboxed read-only; your writes are the position files + memo.
- Registry: an STF that spawns follow-up work registers tasks AFTER owner acceptance, citing the memo.
- This skill is not for routine calls (the decision-authority matrix already covers those) — if the
  question resolves with an in-lane expert call, say so in the FRAME step and offer to skip the ceremony.
