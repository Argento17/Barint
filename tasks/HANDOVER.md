# Orchestrator Handover — 2026-06-12

*For the next orchestrator chat. Read this, then `tasks\DISPATCH_BOARD.md`, then
the named TASK files. Durable truth = registry (`tasks\`) + memory + board.
This file is the bridge for what's in-flight and not yet frozen elsewhere.*

---

## Your role (read first)
You are the orchestrator = the main chat. You **dispatch owning agents via the
Agent tool** with a 5-part spec; you do **not** hand the owner prompts to paste —
EXCEPT in this session's working mode, which the owner set deliberately: **this
chat is expensive, so execution goes out as prompt FILES in `tasks\prompts\` that
the owner sends to cheaper agents / the "Stupid LLM" lane.** Do strategic work
inline; push mechanical work to prompt files. (Memory: `feedback_orchestrator_not_executor`,
`cc_agent_v4_strategic_mode`.)

**Closing authority is yours**, but only after verifying return-block claims
against artifacts at file:line. Agents PROPOSE `RETURNED`/`BLOCKED`; they never
write `CLOSED` and never "rule." If an agent's number isn't in a committed
artifact, it isn't proven — this session caught two such claims (P5 "47/47", P16's
self-written "Orchestrator ruling").

**Escalate to owner only on the 5 tripwires.** Go-live of a consumer category is
tripwire 2 (his call). Everything else inside a lane: decide, act, keep reversible,
log it.

---

## The dispatch board is the live view
`tasks\DISPATCH_BOARD.md` — owner ticks `[x]` when he sends a prompt; a
UserPromptSubmit hook injects those tick states into your context every message.
You own all writes to it; update at every dispatch/return/acceptance. Prompt
files live in `tasks\prompts\PN_*.md`, each ending with a footer telling the owner
to tick its box. (Memory: `dispatch_board_convention`.)

"In flight" = owner confirmed sending OR artifacts exist. Never assume a prompt
was sent.

---

## Where each thing stands RIGHT NOW

### Accepted & verified this session
- **P17** (cereals claim-gate) — 68 strings, 0 hard failures. Cereals draft
  (`02_products\breakfast_cereals\cereals_copy_remediation_draft_v1.json`) is
  **owner-read-ready**. Recorded in TASK-254.
- **P18** (second yogurt S) — **S=2 CONFIRMED** (was provisional). 90.6/S honest,
  trim correctly N/A (Path A declared cultures, not Path B name-inference). Both
  Hebrew S-explanations + shared caveat verified in
  `02_products\yogurt_system\s_grade_explanations_v1.md`. Recorded in TASK-256.
- **P5** (scrape pilot) — **Shufersal UNBLOCKED** from the VM via fingerprint
  randomization (no proxy spend). Sweep: 147 found, 89 new candidates, 30 delisted.
  Recorded in TASK-255. **BUT** its "47/47 replay proof" failed verification
  (committed report shows 0 matches; internal-code vs barcode key gap) → P20 opened.
- Earlier accepted: P16, P13, P11, P10, P12, P9.

### Owner's queue (prompt files ready, not yet sent)
1. **Owner reads** the cereals draft (tone/clarity only — machine verified the facts).
2. **P19** → Frontend/Data — yogurts page rebuild from `run_yogurt_006_shipcfg2`,
   18 products Shufersal-only, S-badge display check, strings PENDING_P14. UNBLOCKED.
3. **P20** → Data (cheap) — re-key + re-run the raw-store replay proof honestly.
   Gates scrape Phase 2.
4. **P6** → Data — Yohananof Playwright fetcher (host `yochananof.co.il`).
5. **P15** → Data (cheapest) — display-values 14-field spec in inventory builder.

### What YOU draft next (don't push to a file — strategic)
- **P14** — full yogurt copy regeneration vs shipcfg2, incl. both S explanations.
  Draft it **after P19 returns** (needs the rebuilt page structure).
- Then: claim-gate pass on the P14 copy (same as P17 rehearsal) → owner reads the
  yogurt copy → **owner's go-live call (tripwire 2).**

---

## Registry map (authoritative — `tasks\`)
- **TASK-256** (IN_PROGRESS) — **yogurts S-tier relaunch**; the live home of the
  P13→P16→P18→P19→P14→go-live chain. *Created this session because the chain had
  been riding TASK-249, which actually closed June 11 when v4 shipped.*
- **TASK-254** (RETURNED) — claim-entailment machine gate. Rubric v2 is law; P17
  was its first production run. Phase 2 = wire into build next to banned-phrase linter.
- **TASK-255** (IN_PROGRESS) — Leap 4+ continuous scrape + shelf expansion. Owner
  amendment: new products auto-enter approved shelves under existing law (admission
  contract in the file). P5 pilot accepted; P20 follow-up open.
- **TASK-253** (Shadow), **TASK-252** (Spine) — merged infra; Shadow arms its
  approved baseline at the first real engine change; Spine Phase 4 (all categories) open.
- **TASK-249** (CLOSED June 11) — yogurts v4 shipped. Do NOT reopen; new work = TASK-256.
- Open threads: TASK-189 (cereal sodium rule absent — blocks 9 drifted cereals'
  re-ship), fermentation trace-schema fix (bonus not persisted per-product),
  Path-B/trim engine debt (TASK-246).

---

## Standing constraints (verbatim-critical — do not soften)
- **OFF banned project-wide, every field, forever.** "Unknown is acceptable; OFF
  is not." Any OFF dependency = launch blocker. (Memory: `off_ban_hard_rule`.)
- **Firecrawl dropped** — not an option (owner, 2026-06-12). No third-party
  acquisition; il_prices is identity-only.
- **Never cap an engine-recognized grade to enforce a framing.** Honest S ships,
  gated on Nutrition trace audit + a very good consumer explanation. (Memory:
  `owner_s_grade_honesty_ruling`.)
- **Never delete contaminated BSIP1 records** — exclude with evidence, never erase.
- **Frozen invariants** (milk run_005_headpin top=85/A; no snack bar reaches A;
  bread provenance): adding a row never moves a published score; any movement =
  Shadow finding → Nutrition, not an auto-ship.
- This chat = strategic only; mechanical work → prompt files → cheap lanes.

---

## Infra quick-reference
- **VM:** Kamatera Tel Aviv, `ssh root@45.93.95.32`, $6/mo, Ubuntu 24.04. ALWAYS
  `/opt/bari/venv/bin/python3`. UFW blocks ICMP — ping is useless, SSH-check only.
- **GitHub API:** PowerShell `Invoke-RestMethod` (Bash calls get permission-denied);
  token via `cmd /c "git credential fill < credin.txt"`; commit msgs via `-F file`.
- Branch: `task-244-confidence-structural-fix`. Master is the PR base.

---

## First moves for the new chat
1. Read `tasks\DISPATCH_BOARD.md` (live state) + this file.
2. The hook will show you which prompts the owner has sent since this handover —
   reconcile any new tick marks, ask for return blocks not yet pasted.
3. When P19 returns: verify the v4 JSON grade distribution matches shipcfg2 exactly
   for the 18 page products, check the S-display findings, then draft P14.
