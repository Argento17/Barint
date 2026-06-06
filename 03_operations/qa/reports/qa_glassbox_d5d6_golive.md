**Task:** TASK-179O

# QA Go-Live Gate — Glass Box D5/D6 (frontend flag NEXT_PUBLIC_GLASSBOX_D5D6)

**Agent:** QA (Bari) · **Date:** 2026-06-04 · **Scope:** verification only (no code / score / data changes)
**Path verified:** engine D5/D6 gate output → glassBox JSON blocks (hummus_frontend_v4 / maadanim_frontend_v2) → code→Hebrew map (`glass-box-copy.ts`) → shared components (`comparison-row.tsx`, `expansion-section.tsx`, `glass-box-flag.tsx`) → rendered routes.

---

## VERDICT: **PASS** — clear to flip `NEXT_PUBLIC_GLASSBOX_D5D6=on`.

No hard fail. One non-blocking advisory (a co-mingled, unrelated maadanim content edit on a displayed product — scores/grades unchanged; see §6). It does not gate the flag flip; it routes to Content/Product for separate sign-off.

---

## 1. FLAG OFF = byte-identical on live routes — PASS

Default build (flag unset/OFF). Rendered static HTML grepped:

| Route | `ניתוח חלקי` | `לא נוקד` | `מה לא צוין בתווית` |
|---|---|---|---|
| /hashvaot/vegetable-spreads | 0 | 0 | 0 |
| /hashvaot/hummus | 0 | 0 | 0 |
| /hashvaot/maadanim | 0 | 0 | 0 |

- Flag actually gates the surface: `GLASSBOX_D5D6_ON` is read from `process.env.NEXT_PUBLIC_GLASSBOX_D5D6` (build-time, statically inlined → tree-shaken). `comparison-row.tsx` `glassBoxState()` returns `{isWithheld:false,isDemoted:false}` when OFF, and the `glassBox` prop to `ExpansionSection` is hard-gated `GLASSBOX_D5D6_ON && (isDemoted || isWithheld)`. 0 glass-box strings emitted on every comparison route with the flag OFF. **Confirmed at the rendered-HTML level.**

## 2. FLAG ON = correct on the REAL routes — PASS

Rebuilt with `NEXT_PUBLIC_GLASSBOX_D5D6=on`, re-grepped rendered HTML:

| Route | `ניתוח חלקי` (demote pill) | `לא נוקד` (withhold chip) | Result |
|---|---|---|---|
| /hashvaot/vegetable-spreads | 2¹ | 0 | ONE demote renders (the pepper spread) |
| /hashvaot/hummus | 0 | 0 | NO-OP (expected) |
| /hashvaot/maadanim | 0 | 0 | NO-OP (expected) |

¹ The 2 occurrences are the `aria-label` + the visible `<span>` text of the **same single pill** (the `title` carries the tooltip `הדירוג מבוסס על המידע שצוין בתווית…`). Exactly one demoted row.

- **hummus NO-OP is expected-correct, not broken.** hummus_v4 carries 3 non-unconstrained products: 2 `withhold` (`bsip1_1990261`, `bsip1_3643714`) and 1 `demote` (`bsip1_7290104721533`). The 2 withholds ARE the `EXCLUDED_RAW_CHICKPEA_IDS` set → filtered out of the hummus display. The 1 demote is a `pepper_spread` → excluded from hummus (vegetable-spread type). Net displayed gated products on hummus = 0. The no-op is because the gated ids are not in the displayed set, not because wiring is dead (wiring proven live on veg-spreads).
- **maadanim NO-OP is expected-correct.** maadanim_v2 carries exactly 1 demote (`bsip1_maadanim_7290018249123`, vanilla pudding powder), which IS in `EXCLUDED_MAADANIM_IDS` → filtered out. Net displayed gated = 0.
- **vegetable-spreads shows the ONE real displayed gated product.** `bsip1_7290104721533` (סלט פלפלים קלויים, pepper_spread): published `score:65 / grade:B`, `glassBox.gateState:"demote"`, `disclosureCodes:["missing_field"]`. Flag-ON it renders: grade chip **B** (unchanged) + the `ניתוח חלקי` pill + (on expand) the `מה לא צוין בתווית` section with the mapped line `חלק מהערכים התזונתיים לא הופיעו בתווית.` Code path verified in `expansion-section.tsx` `GlassBoxDisclosure` → `resolveDisclosureLines` (the expansion body renders client-side on row open, so it is correctly absent from the static collapsed HTML — not a failure).
- **null-render parity.** The withhold chip path (`GLASS_BOX_WITHHOLD_LABEL`) and the pre-existing unscored path both render the same neutral box: em-dash `—`, no number, no NaN, no error color (`#F7F7F2` bg, muted text). No displayed product across these routes is currently in `withhold` flag-ON, so no live `לא נוקד` renders — but the code path is correct and matches the existing `insufficient` chip.

## 3. Copy fidelity + leakage — PASS

- Every disclosureCode emitted by the live JSONs (`missing_field`, `proportions`, `generic_additive`) maps to an approved Hebrew line in `GLASS_BOX_DISCLOSURE_LINES` (`glass-box-copy.ts`), each verbatim against Content's FINAL doc `w1_disclosure_copy_v1.md` §1/§3. Unknown codes fail closed (skipped silently — no token leak).
- L411 withhold-reason unification IS in: `resolveWithholdReason` falls back to `GLASS_BOX_WITHHOLD_REASON = "אין מספיק מידע בתווית כדי לדרג את המוצר."` (canonical), used in `expansion-section.tsx` L421/428.
- Pill + tooltip strings: `ניתוח חלקי` / `הדירוג מבוסס על המידע שצוין בתווית. חלק מהפרטים לא פורטו.` — no number, no engine/internal term (no NOVA/BSIP/D5/D6/band/cap/floor/dimension/confidence), no intent attribution (Q2/Q4 clean). All strings sourced from the Content-owned map; the JSON carries codes only, no prose.

## 4. No regression + data integrity — PASS

- **Other category routes unchanged:** glassBox JSONs are consumed only by hummus, maadanim, and vegetable-spreads pages (vegetable-spreads reads hummus_v4). No other comparison route imports them. All other routes are flag-gated identically and render byte-identically OFF.
- **Published grades/scores UNCHANGED by glassBox.** The glassBox blocks live in the **uncommitted working tree**, not in any commit. Diff of working tree vs `HEAD` (last commit `fc8dd6a`):
  - hummus_frontend_v4: glassBox added to all 64 products; **0 score/grade changes; 0 other non-glassBox keys changed.** Purely additive.
  - maadanim_frontend_v2: glassBox added to all 84 products; **0 score/grade changes** (1 non-glassBox content edit — see §6, advisory).
  - Note: hummus_v4 already differs from the older hummus_v3 in 59/64 scores, but that delta is the **separately-shipped TASK-169 recalibration** (commit `8af14a2`), NOT glassBox. v3 is not the glassBox baseline; HEAD is. glassBox does not move scores.
- **Frozen invariants (engine-side) unaffected:** the FE flag is display-only; it does not touch the engine, BSIP2, or any published score. `gatedScore`/`gatedGrade` are carried for provenance only and are never rendered as a number.

## 5. Build health — PASS

- `npx tsc --noEmit` → exit 0, no errors.
- `npm run lint` → exit 0, 0 errors (10 pre-existing warnings: unused-var in 2 scripts + 8 `no-img-element` in legacy components; **none in glass-box files**).
- `npm run build` → exit 0, both OFF and `NEXT_PUBLIC_GLASSBOX_D5D6=on`; all 35 routes prerender (3 target routes static-OK). Working tree restored to the default flag-OFF build.

## 6. Advisory (non-blocking) — co-mingled content edit on a DISPLAYED maadanim product

The same uncommitted working set that adds glassBox also edits `insightLine` + `expansion.positiveSignals` on **`bsip1_maadanim_7290110321031`** (a displayed, non-excluded product). Verdict reframed: HEAD `"…הבסיס עדיין מעדן מתוק, לא מוצר חלבון."` → WORK `"…הבסיס בנוי על חלב ואבקת חלב מועשרים, לא על מבנה חלב שלם."` (TASK-169 whole-food-rubric framing).

- **score/grade: UNCHANGED.** This is a content/verdict edit, not a glassBox surface and not a score move.
- It does **not** gate the flag flip (glassBox is clean; this edit is independent and would render with the flag OFF too).
- It is outside the stated "additive glassBox only" premise, so it should be sign-off'd separately by Content (copy) / Product (positioning) as a TASK-169-adjacent verdict change. **Flagged, not fixed** (QA does not author copy). Owner can flip the glassBox flag without resolving this; this edit ships or reverts on its own track.

---

## Hard-fail check: NONE
- Leakage: PASS (no framework vocabulary in any rendered glass-box string).
- Score propagation discrepancy: NONE (glassBox additive; 0 grade/score deltas vs HEAD).
- Build: clean (OFF and ON).

## Condition attached to PASS
- The flag flip itself is unconditionally clear. The §6 maadanim verdict edit is a **separate** item for Content/Product sign-off and should not be bundled into the glassBox go-live commit without that sign-off.

*End of go-live QA report — TASK-179O.*
