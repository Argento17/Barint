# P269 / TASK-418 HC clean-refresh tripwire consult (route: C3)

You are the independent outside-the-family reviewer (ChatGPT). This is ADVICE ONLY — you do not decide,
build, or close. Pressure-test the reasoning below before the orchestrator brings a go/no-go to the owner.
A published-score change is a tripwire; your job is to find where this could be wrong or indefensible.

## Context (all independently verified by the orchestrator against artifacts + the scoring trace)
Bari scores Israeli grocery products. `hard_cheeses_frontend_v4` is live. TASK-429 pinned the canonical
scoring invocation that byte-reproduces all 31 published HC scores (drift 0.000). Some published scores rest
on a data-parsing defect: retailer-disclaimer lines ("אין להסתמך על הפירוט…", "יתכנו טעויות", "יש לקרוא…")
and nutrition-panel text ("ערכים תזונתיים 100 גרם 363 קל…") were scraped INTO the ingredient list and counted
as ingredients. Example: barcode 5384356 has ingredient_count=8 but the real list is 5 (milk, salt, calcium
chloride, lactic culture, rennet); items [5][6][7] are disclaimers and item [4] fused rennet with a nutrition
panel.

A deterministic clean rule (strip disclaimer lines + nutrition-panel bleed; keep the real ingredient head)
was applied to worktree COPIES and re-scored through the pinned invocation. **Nothing deployed.** Result
(verified: baseline reproduces, script deterministic, sha256-stable, mechanisms traced):

- **Only hard_cheeses is affected by the clean.** juices / cheese / cereals produce ZERO clean-rule-caused
  score changes — their baseline drift is the separate, already-known post-publication TASK-405 data-refresh
  set, not this pollution clean.
- **hard_cheeses: 8 products move (of 16 polluted live records), 2 grade moves.**
  - **5 move UP** (+2.0 to +6.0): the spurious extra "ingredients" had triggered small additive/count
    penalties; cleaning removes them. e.g. 4137311 70.8→76.8; 7290014760448 65.9→71.9.
  - **2 grade moves UP** (C→B): 4122270 and 7290110320850, both 62.6/C → 67.0/B.
  - **3 move DOWN** (−3.2 to −7.6), all landing exactly on the EV-104 HC-2 ceiling 67.0/B:
    5384356 74.6→67.0, 9150162 72.2→67.0, 7290116931524 70.2→67.0. **Traced mechanism:** in the polluted
    record the garbage text broke the "qualifying hard cheese" classification, so the EV-104 sodium/fat
    ceiling cap (fat≥25g → clamp to 67.0) did NOT fire and the score floated to 70–75. Cleaning restores the
    correct classification, the legitimate ceiling fires, and the score drops to the intended 67.0.
  - 8 already at the 67.0 ceiling → no change.

## The forks I need challenged
1. **Is this a legitimate data-hygiene correction or a disguised scoring change?** The engine/flags/shelf-stats
   are untouched; only obviously-non-ingredient scraped text is removed. Is "reproduces published exactly, but
   published rests on parsing garbage" sufficient grounds to refresh — or is there a reason to keep the
   published (defective) numbers?
2. **The 3 DOWN-moves are the sharp edge.** Restoring a legitimate ceiling that pollution had defeated *lowers*
   3 live scores by 3–8 pts. Is that defensible to publish? What's the failure mode if the clean rule
   OVER-strips (removes something that is actually a real ingredient/allergen statement) and wrongly triggers
   the ceiling? How should we bound that risk before deploy?
3. **Scope/consistency:** is it defensible to refresh only the pollution-clean HC moves now while the
   juices/cheese/cereals TASK-405 drift is a separate owner-gated refresh — or must they go together to avoid
   a half-clean corpus?
4. **Any reason this should NOT go to the owner as a go/no-go**, or any additional check you'd demand first.

## Return
Concise: for each of the 4 forks, your ruling + the single strongest reason. Then one line: SHIP-worthy as an
owner go/no-go? (yes / yes-with-conditions / no). End with the machine-readable return contract
(`01_framework/operations/return_contract_v1.md`). Advice only — do not close.
