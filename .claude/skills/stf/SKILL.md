---
description: STF (Strategy Task Force) — owner-invoked hard-strategy consultation between the two SST models (Claude Fable 5 in-session + GPT-5.6 Sol via read-only codex). Independent positions first, capped adversarial debate, verdict memo with honest dissent. Never implements.
argument-hint: <the strategic question — stakes, options if known, what a good answer unlocks>
---

# /stf — Strategy Task Force

**Owner-invoked only** (owner ruling 2026-07-11). This is the standing primitive for *very hard
strategy meetings*: the two SST-tier models (see the tier map in
`01_framework/operations/capability_router_v5.md`, invariant 9) debate to the best outcome.

**The two seats (owner ruling 2026-07-11, orchestrator-default edit):** the orchestrator default is
**Opus 4.8**, so the running session is NOT the Fable seat. `/stf` convenes both SST models
explicitly for the meeting:
- **Claude seat = Fable 5**, convened as a Fable-pinned subagent (`Agent` tool, `model: fable`) that
  writes its blind position and argues the debate rounds. The Opus orchestrator runs the meeting
  (frames, relays, records the memo) but does NOT itself hold the Claude seat — it is the chair, not
  a debater.
- **GPT seat = Sol 5.6**, reached via `strategist_consult()` in `03_operations/router/dispatch.py`
  (codex exec, READ-ONLY sandbox — consultations never write files; stdout is the deliverable).

**STF never implements.** No builds, no dispatches of build lanes, no file changes outside the memo
and scratchpad position files. Output = a verdict memo + owner decision points. Anything actionable
becomes a registered task only after the owner accepts the recommendation.

## Protocol (anti-anchoring is the whole design — do not shortcut it)

**0. FRAME.** Restate the question in one paragraph: stakes, constraints (Bari hard rules that
bound the answer — OFF ban, tripwires, two-gate, freeze states), the real options space, and the
decision criteria (what would make one answer *win*). If the owner's question is ambiguous, sharpen
it WITH the owner before convening — this is the one workflow where a clarifying question is the
right move, because the frame determines everything downstream.

**1. INDEPENDENT POSITIONS (blind).** As chair (Opus), dispatch BOTH seats with the frame ONLY —
never seed either with the other's take, and never with your own view:
- Fable seat: `Agent` tool `model: fable` — instruct it to write its full position to a scratchpad
  file (recommendation, reasoning chain, top 3 risks, kill-criteria) and return it.
- Sol seat: `strategist_consult()` with the same frame and the same required structure.
Fire them concurrently so neither can see the other. Two genuinely independent priors is what makes
this more than theater; a debate seeded with one model's take converges on that take. The chair does
NOT author a third position — it adjudicates.

**2. DEBATE ROUNDS (cap 3).** The chair relays each seat's position + the opposing critique to the
other and requires point-by-point defence or CONCESSION: send Fable → Sol's position and demand
Fable attack it; send Sol → Fable's position and demand the same. Each round must do one of:
converge a point (mark AGREED), kill a point (mark CONCEDED, by whom), or crystallize a **crux** —
the smallest testable claim that decides between positions, and what evidence would settle it. A
round that does none of these ends the debate (diminishing returns). Sequencing note: never run
`strategist_consult` while another dispatch.py lane is live (concurrent-dispatch hazard); resume the
Fable seat via SendMessage between rounds so its context persists.

**3. VERDICT MEMO.** Write to `01_framework/governance/stf_memos/YYYY-MM-DD_<slug>.md`:
- The frame (as debated, including anything the owner sharpened).
- **Converged recommendation** — or, if convergence failed honestly, the surviving cruxes with the
  evidence that would settle each. **Never fake consensus**; a recorded dissent is a deliverable,
  not a failure.
- Risks, reversibility class, and the owner decision points (tripwire-tagged where applicable).
- Appendix: both blind position files verbatim (provenance of the debate).
Then give the owner the memo's core in the chat reply — recommendation first, dissent explicit.

## Guardrails
- **SST seats only, both convened explicitly** — the Opus orchestrator chairs, it does not debate.
  Sol unavailable → Fable-seat-only analysis, EXPLICITLY marked "degraded: no cross-vendor seat";
  Fable subagent unavailable → do not substitute the Opus chair's own view as the Claude seat, say
  the meeting cannot convene.
- Read-only throughout: Sol runs sandboxed read-only; the Fable seat writes only its position file;
  the chair writes only the memo.
- Registry: an STF that spawns follow-up work registers tasks AFTER owner acceptance, citing the memo.
- This skill is not for routine calls (the decision-authority matrix already covers those) — if the
  question resolves with an in-lane expert call, say so in the FRAME step and offer to skip the ceremony.
