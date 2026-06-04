**Task:** TASK-179J

# Bari Glass Box — W1 Go-Live Threshold Lock + Blast-Radius Acceptance

**Author:** Product Agent · **Date:** 2026-06-04 · **Wave:** TASK-179, Wave 1
**Decision rights:** D4 (gate), D7 (scoring-rule approval, business/scope half), D10 (go-live).
**Reads:** `proof_B_flag_on_pilot_diff.md` + `_pilot_summary.json` (TASK-179G), `qa_glassbox_d5d6_w1.md` (TASK-179H, PASS-conditional).
**Locks against:** `d5_d6_rule_spec_v1.md` (179D, Nutrition) + my own starting-value co-sign `w1_product_cosign_numbers_v1.md` (179E), which explicitly held the four numbers "revisitable after the pilot." This memo closes that loop.
**Governance basis:** DEC-006 (owner-ratified 2026-06-04) — Q1 conservative-to-demote / reluctant-to-withhold; Q2 D5 annotates, never docks on its own axis.

---

## Verdict in one line

All four numbers **HOLD as final**. WARN-2 (consumer-facing grade removal) is **ACCEPTED on the record** as the shipped posture — it is the honest, intended behavior, not a defect. Pilot flag-ON go-live for hummus + maadanim = **GO-WITH-CONDITION** (two conditions, both pre-flip, both reversible). One item still needs the human owner's sign before the flip.

---

## Decision 1 — The four numbers: LOCKED (no adjustment)

`partial −10 / severe −20 / structural-only 0 · NULL_FLOOR=30 · DEMOTE_CEILING_BOUND=60`

**LOCKED as final. No number moves. The Nutrition co-sign does NOT re-open.**

The whole point of the pilot was to test the starting values against real shelf behavior before freezing the framing. The diff says the calibration is correct on every axis I co-signed it for:

- **Zero promotions** across 269 pilot products (hard invariant holds — D6 only demotes/withholds). The −20/−10 reductions never pushed anything *up* across a band edge, by construction. Confirmed against raw `_pilot_summary.json` (`_promotions_VIOLATION: []`).
- **The −10/−20 split behaves exactly as the asymmetry was designed.** Every one of the 5 maadanim demotes is a `partial`-band candy/jelly (jelly, 4× sugar-free סוכריות) taking −10 and crossing the legacy <40 insufficient gate — score unchanged, grade removed. Closable opacity eroded trust by a modest amount; structural-only gaps (the `minor` band) docked 0 and did not bleed the shelf. That is Q2 honored: D5 acts *through* confidence, never as a back-door quality penalty.
- **NULL_FLOOR=30 (severe-AND-conf<30, or panel-absent) is correctly the load-bearing reluctant-to-withhold valve, and it did NOT over-fire.** Of 36 total withholds, the overwhelming majority are products that were **already** `insufficient_data`/non-graded under OFF — Glass Box only relabels `insufficient_data → לא נוקד` (a more honest "we decline to rank" than a guessed middle-50). Verified in raw data: across the 32 maadanim withholds, only **one** (`בולגרית מעודנת 24%`, 45/D, conf 40→20, severe) was a genuinely graded product flipping to null; the other 31 were already non-graded. The floor reserved null for genuine floor-of-observability failures and did not withhold a single merely-thin-but-readable panel. The conjunction is deliberately hard to trip and it stayed hard to trip — that is on-posture (more reluctant, not less), exactly as my 179E forward-note anticipated.
- **EV-036 endemic-flavoring exclusion is load-bearing and confirmed.** Bare `חומרי טעם וריח` in 130/200 maadanim (~65%). Excluding it from band-raising is why only 5 demote + 32 withhold and **163/200 unchanged**. Without it ~65% of the shelf would demote — a DISTORTION-001-class category-blind error. The exclusion did its job; the numbers I locked sit on top of a shelf that is not over-demoting.
- **DEMOTE_CEILING_BOUND=60 proved out as the no-op restatement I conditioned it on in 179E.** All ON-vs-OFF score movement originated in the §2.1 reduction + the panel-absent null flip, both demote-or-null-only. The bound itself moved nothing. The single open condition on my starting-value co-sign is now retired by the pilot evidence.

**No number is adjusted. Therefore the Nutrition D6/D7 co-sign stands and is NOT re-opened.** (Per Hard Rule 8, a scoring-rule change needs both signatures; holding the numbers unchanged needs no new Nutrition signature — this is a lock of already-co-signed values, not a new proposal.)

---

## Decision 2 — WARN-2 (consumer-facing grade removal): ACCEPTED

**I formally ACCEPT WARN-2 as the shipped posture.**

Turning the flag ON removes a published-equivalent grade from **5 real consumer-facing products**:

| Product | Corpus | OFF | ON | Why |
|---|---|---|---|---|
| `חומוס` (`bsip1_1990261`) | hummus | 72.1/B | לא נוקד | panel-absent (severe, no ingredients_raw) |
| `חומוס` (`bsip1_3643714`) | hummus | 72.1/B | לא נוקד | panel-absent (severe) |
| `חומוס` (`bsip1_7296073733317`) | hummus | 75/B | לא נוקד | panel-absent (severe) |
| `חומוס ענק` (`bsip1_7296073733348`) | hummus | 75/B | לא נוקד | panel-absent (severe) |
| `בולגרית מעודנת 24%` (`bsip1_maadanim_2385455`) | maadanim | 45/D | לא נוקד | severe + conf 40→20 (floor failure) |

Plus 5 maadanim demotes (E/D → `insufficient_data`, score retained, grade removed).

**Why I accept rather than soften it:** these grades were never *earned* — they were guessed on top of a formulation the shelf does not disclose. A 72–75/B hummus with **no ingredient panel at all** is an A/B-shaped number built on an invisible recipe; publishing it is the exact dishonesty DEC-006 Q1 was ratified to stop. The product's response is not "downgrade it to a worse number we also can't justify" — it is `לא נוקד`: *we decline to rank because the label does not let us.* That is the honest posture, it is consistent with the spec §2.3 "tighten to לא נוקד," and the blast radius is small and surgical (5 grade removals + 5 demotes across 269 products), not a shelf-wide silencing. The clean single-ingredient hummus SKUs (`חומוס מוקפא`, `חומוס לבן ענק שופרסל`) correctly keep their 85/A via single-ingredient protection — so we are withholding *only* the genuinely opaque, not punishing whole foods. I accept it.

**Condition attached to the acceptance (consumer truthfulness, not a numbers change):** `לא נוקד` must read to a shopper as "not enough label info to rank," NOT as "bad / failed / low quality." A B-grade product disappearing into an unexplained blank is a worse consumer experience than the honest grade it replaces. See Decision 3, Condition 1.

---

## Decision 3 — Pilot flag-ON go-live (hummus + maadanim): **GO-WITH-CONDITION**

I authorize flag-ON go-live for the two pilot categories, conditional on two pre-flip items. Both are reversible (the flag is the rollback) and neither touches the locked numbers.

**Condition 1 — `לא נוקד` consumer wording + empty-state must be approved before the flip (Content + Design, D12/D13).**
The 5 withheld products will render with no grade. The shopper-facing string and the row/card empty-state must communicate *"not enough information on the label to score this"* — calm, non-pejorative, not a red "fail." This is the one place WARN-2 can do consumer harm if mishandled. Owner: **Content Agent** authors the line (positioning is D13, mine to approve); **Frontend Agent** confirms the withheld-row empty-state already renders cleanly for a null score (it does today for `insufficient_data`; confirm parity for `לא נוקד`). Blocking, but small.

**Condition 2 — Fix WARN-1 (Proof B §3 doc defect) before the proof is cited in the go-live packet.**
Proof B's example table wrongly names `חומוס לבן ענק שופרסל` as a withhold; in a fresh run that SKU is full-band / unchanged 85/A. The four actual hummus withholds are the plain `חומוס` / `חומוס ענק` SKUs listed in Decision 2. Counts (4 withholds, 0 promotions) are correct; only the named example is wrong. This is a documentation-integrity fix so the go-live evidence is clean. Owner: **Data Agent**, one-line correction. Not an engine change; does not affect the verdict or the lock.

**Not conditions, but tracked (do not block the flip):**
- **P3 token-aware deviation** — QA flagged the engine deviated from the literal spec §1.1 P3 text (panel-absent only when sub-threshold AND lacking a coherent ≥2-letter token) to avoid wrongly withholding clean single-ingredient whole foods. QA verified it sound and *more* conservative. I concur it is faithful to spec INTENT. **Action:** Nutrition Agent gives a one-line sign-off and amends spec §1.1 P3 text to the token-aware rule at the next co-sign pass (doc-vs-engine reconciliation). Governance tidy-up, not a gate.

---

## What still needs the human owner's sign before the flip

One item, and it is the only one that trips a strategic tripwire:

- **Flag-ON go-live is irreversible-in-spirit AND consumer-facing** — it changes published-equivalent grades on a live category (5 grade removals reach real shoppers). That is a DEC-006-class consumer-facing posture change. Per my autonomy mandate, removing published-equivalent grades from live consumer products crosses the "irreversible AND consumer-facing" wire. **I have locked the numbers, accepted the blast radius, and cleared the gate to GO-WITH-CONDITION — but the actual flip of `BARI_GLASSBOX_D5D6` to ON in production for hummus + maadanim is the owner's to authorize**, with my recommendation on the record: **flip it.** The honesty gain is real, the blast radius is small and surgical, and the flag is its own rollback.

Everything else (the four numbers, the WARN-2 acceptance, the two pre-flip conditions, the P3 tidy-up) is decided here and needs no further escalation.

---

## Ownership / next steps

| Owner | Action | Gate |
|---|---|---|
| **Content Agent** | Author the `לא נוקד` consumer line ("not enough label info to rank"). | Condition 1 (I approve positioning, D13) |
| **Frontend Agent** | Confirm withheld-row empty-state renders cleanly for `לא נוקד` (parity with `insufficient_data`). | Condition 1 |
| **Data Agent** | Fix WARN-1 (Proof B §3 example row). | Condition 2 |
| **Nutrition Agent** | One-line P3 token-aware sign-off + amend spec §1.1 P3 text. | Tracked, non-blocking |
| **Human owner** | Authorize the production flag flip for hummus + maadanim. | The one remaining sign |
| **Product (me)** | Hold D10; on owner sign + both conditions met, confirm GO and the flip proceeds. | — |

---

## What I am NOT deciding here

- I am not changing any locked number (this memo freezes the four; only a future tuning task with fresh evidence + dual co-sign reopens them).
- I am not extending the flag beyond the two pilot categories. Other categories (milk, bread, snack-bars, cheese, yogurt, cereals) are a separate Wave-2 rollout decision; their frozen invariants are protected and Glass Box ON is a no-op on the frozen milk corpus per QA Proof A.
- I am not approving any consumer-facing surfacing of `disclosure_profile` / `d5_completeness` beyond the `לא נוקד` label itself — that broader explainability surface is a later D11/D12 frontend-scope call.

*End of W1 go-live threshold lock. Decision + memo only — no engine, frontend, or governance file was modified by this task.*
