# P104 — TASK-280 Phase-2: PHVO D7 Product Co-Sign (route: C1)
# Product Agent — Governance co-sign on PHVO detection corrections

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-280.md` (status: IN_PROGRESS)
**Depends on:** P103 D6 ruling (ACCEPTED by orchestrator)

---

## Context

Fix-B (signal_extractor.py PHVO markers) and Fix-C (score_engine.py fat_quality ceiling=40 when has_phvo=True) were committed to HEAD during TASK-275 without governance. TASK-280 Phase-1 (D6 ruling by Nutrition) has been completed and accepted. You are Product Agent providing the D7 co-sign to authorize implementation.

**Key facts:**
- PHVO changes are ALREADY COMMITTED to HEAD (not proposed, committed)
- The D6 ruling CORRECTS them, not approves them as-is
- Implementation = editing committed code to match the D6 ruling
- No published scores change yet; implementation produces a corrected committed engine
- Snacks re-score (where the live consumer impact would materialize) is a SEPARATE authorized step that does NOT happen here

---

## D6 Ruling Summary (P103, Nutrition Agent, accepted by orchestrator 2026-06-14)

Read the full ruling at `C:\Bari\tasks\returns\P103_return.md`. The key decisions:

**Q1: מחמאה REMOVED from `_PHVO_MARKERS`**
- מחמאה = clarified butter (ghee), animal fat, not PHVO
- The code COMMENT at signal_extractor.py:1167 misidentifies it as "margarine/shortening" — factually wrong
- The marker must be removed; sat_fat dimension already handles animal fat correctly

**Q2: Ceiling = 40 RETAINED + new position gate N ≤ 8**
- PHVO ceiling fires only if the PHVO marker appears within the first 8 ingredient positions
- Fallback: if product has no structured ingredient list (`ingredient_order` empty), current full-text search behavior is retained
- snk-019 מרגרינה at position #6 still fires (within gate)
- Q4 nuance: snk-019's מרגרינה = coconut oil composite (not hydrogenated vegetable oil); position gate fires but the chemical identity is borderline. Deferred to Data Agent after implementation.

**Q3: All-categories scope retained** (no category exclusion list; מחמאה removal eliminates the primary false-positive path)

**Q4: Patch deployed JSON only if grade changes (D→E or any grade boundary)**

**EV-086 designated** for this ruling.

---

## Your D7 Co-Sign Task

### Step 1: Ratify the D6 ruling

Review the D6 ruling from `C:\Bari\tasks\returns\P103_return.md` and co-sign or reject each question:
- Q1 (מחמאה REMOVE): ratify or override
- Q2 (ceiling=40 + N≤8 gate): ratify or add conditions
- Q3 (all-categories): ratify or add exclusion list
- Q4 (patch principle): ratify or override

If you reject any ruling → state the specific concern and propose a resolution; orchestrator decides.

### Step 2: Register EV-086

Add EV-086 to `C:\Bari\01_framework\operations\evidence_registry_v1.md`. EV entry must include:
- EV number: 086
- Title: PHVO Marker Correction + fat_quality Ceiling Ratification
- Summary: Four D6 rulings (Q1–Q4) — מחמאה removed, ceiling=40 ratified, position gate N≤8 added, patch principle stated
- Engine changes authorized: signal_extractor.py (remove מחמאה, fix code comment, add position gate), score_engine.py (position gate check integration)
- Category: All (PHVO detection fires cross-category)
- Evidence tier: Moderate (architectural + food chemistry reasoning; EV-050 extends)
- Links: References EV-050 (original PHVO concept)
- Status: D7 PENDING IMPLEMENTATION (set to D7-CO-SIGNED after your ratification)
- Owner: TASK-280

### Step 3: Authorize implementation spec

After ratification, specify what the Data Agent (P105 implementation dispatch) must implement:

**Implementation spec for signal_extractor.py:**
1. Remove `"מחמאה"` from `_PHVO_MARKERS` list
2. Fix the code comment on the removed entry (line 1167) to correctly state "clarified butter (ghee), animal fat — removed D6 Q1 ruling (TASK-280/EV-086)"
3. Fix the comment at line 1158 that also incorrectly references מחמאה as "margarine"
4. Add position gate: `has_phvo` should fire only if a PHVO marker appears in `ingredient_order` positions 0–7 (0-indexed, i.e., first 8 ingredients). Fallback to current full-text search when `ingredient_order` is empty or None.

**Implementation spec for score_engine.py:**
No changes required to score_engine.py. The ceiling logic (`min(fat_quality, 40) when has_phvo=True`) remains correct. The position gate enforcement lives in signal_extractor.py (where `has_phvo` is set).

**No-regression requirement:** After implementation:
1. Run `engine_invariants.py` — must PASS 342 cases
2. Run brined cheeses category through current engine with flag-off — must be byte-identical to run_brined_004
3. Run milk through current engine — must be byte-identical to run_005_headpin (frozen invariant)

### Step 4: snk-019 edge case decision

snk-019's מרגרינה = "(שמן קוקוס + E471)" (coconut oil composite, not hydrogenated). Under the corrected engine:
- The marker word "מרגרינה" is still in `_PHVO_MARKERS`
- מרגרינה is at position #6 ≤ 8 → PHVO ceiling fires
- BUT the actual fat is coconut oil (saturated, not trans) — the PHVO ceiling is designed for industrial trans fat

Product Agent must rule on this: should the Data Agent add a sub-check for coconut-oil/palm-oil-declared margarines (where the composition text shows no hydrogenation), or is the position gate + marker sufficient for now?

Options:
- (A) **Fire as-is** — "מרגרינה" label = industrial processing signal regardless of whether trans fats are present; the ceiling at 40 is appropriate for any industrial fat product labeled "מרגרינה"; Data Agent notes it but does not override
- (B) **Add a sub-exclusion** — if מרגרינה parenthetical lists only coconut/palm oil with no "מוקשה" qualifier, set has_phvo=False for this case; defers to Data Agent to implement

Rule with the simpler option that doesn't create audit complexity.

---

## Definition of Done

- [ ] D6 ruling ratified (Q1–Q4 explicit statement: "RATIFIED" or specific override)
- [ ] EV-086 written to evidence_registry_v1.md (verify line number, zero EV-086 duplicates)
- [ ] Implementation spec confirmed (signal_extractor.py spec, no score_engine.py edit needed)
- [ ] snk-019 edge case ruled (option A or B or alternative)
- [ ] D7 co-sign document written to `01_framework/bsip2_framework/phvo_governance/phvo_d7_cosign_v1.md`

---

## Constraints

- **Do NOT implement engine changes** — D7 is governance + spec only; implementation is a separate dispatch
- **Do NOT modify comparison JSON files** — no deployed scores patched yet
- **OFF ban absolute** — no Open Food Facts
- **EV-086 must be the first write** — before any other output; verify it's not already there
- **Agent does NOT decide go/no-go for snacks re-score** — orchestrator decides after this D7

---

## Return format

End with machine-readable contract:
```json
{
  "task_id": "TASK-280",
  "phase": "Phase-2 D7 co-sign",
  "status": "RETURNED",
  "return_date": "...",
  "agent": "product-agent",
  "d7_ratification": {
    "Q1_mchama": "RATIFIED|OVERRIDE",
    "Q2_ceiling_and_gate": "RATIFIED|CONDITIONS",
    "Q3_category_scope": "RATIFIED|OVERRIDE",
    "Q4_patch_principle": "RATIFIED|OVERRIDE"
  },
  "snk_019_ruling": "option_A|option_B",
  "ev_086_registered": true,
  "ev_086_line": <line number in registry>,
  "d7_doc_path": "01_framework/bsip2_framework/phvo_governance/phvo_d7_cosign_v1.md",
  "implementation_spec_confirmed": true,
  "not_done": []
}
```

**Do not close — propose RETURNED and let the orchestrator verify.**
