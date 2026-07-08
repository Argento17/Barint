# RT-2H1 modified-starch classifier fix — Nutrition + Product D7 co-sign record (TASK-515/515A)

Durable provenance for the classifier fix that corrects a modified-starch (E-1442) detection miss
found by the drinkable-yogurt terminal red-team (RT-2H1, round 2).

## The bug
`03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py:283-382` `resolve_structural()` matches
modified-starch synonyms by contiguous substring. The label "עמילן טפיוקה מעובד" (modified tapioca
starch, E-1442 = hydroxypropyl distarch phosphate) is not a contiguous match for the synonym
"עמילן מעובד" (the word טפיוקה sits between them) → falls through to the bare "עמילן" synonym →
mis-classified as `native_starch` (benign) instead of `modified_starch`. Consequence: the ECS-v1
`modified_starch_stabilizer` −3 penalty (`score_engine.py:1845`, medium-weight tier, `constants.py:358`)
never fires on affected products → final score ~3pts too high (before floor).

## Blast radius (Data Agent a2e82720, sandbox-measured, engine reverted byte-identical)
27 live-indexed products / 5 pages: yogurt_drinkable 3, yogurt_spoonable 13, hummus 3,
cakes_hard_cookies 7, crackers 1. 6 cross a published grade boundary, **all downward** (more accurate):
drinkable 7290110573737 B→C + 7290107938396 C→D; spoonable 7290010471669 D→E + 7290110578572 C→D +
7290119377404 B→C; crackers 7290011489595 C→D. additive_quality delta = 0 on all 27 (the move is
entirely the ECS penalty); 3 of 27 get +0 delta (fail the position≥4 gate — proof the fix is precise,
not blunt).

## C3 independent challenge (P509, `tasks/returns/P509_return.md`)
**fix-now-split ENDORSED.** Fix the classifier + rescore pre-launch yogurt now; HOLD live-category
(hummus/cakes/crackers) JSON regen+redeploy for explicit owner approval (published scores move there).
Do NOT reopen the ECS −3 weight in this bug fix (crossings prove the classifier mattered, not that the
penalty is wrong). Guardrails: phrase-boundary-safe regex (no comma-crossing), preserve `לא מעובד`
negative case, scan other source-qualified additive variants (pectin/gelatin/lecithin), full
cross-corpus baseline diff before merge.

## Nutrition co-sign (dispatch a15f130b, this session, verified against live code + corpus)
**YES, apply the fix**, contingent on 2 hardenings (both corpus-verified against real ingredient
strings, not hypothetical):
1. **Comma/clause-boundary guard** on the `{1,2}`-word window — demonstrated live hazard in
   `bsip1_yogurt_7290107938396/bsip2_trace.json:70`, a bundled stabilizer clause
   ("חומר מייצב (גואר גאם..., עמילן טפיוקה מעובד, ויטמין D...") where an unguarded window could
   cross a comma into an unrelated ingredient.
2. **Symmetric treatment of all 3 modified-starch synonyms** (`מעובד` / `מותמר` / `שעבר עיבוד`) —
   the same contiguous-match bug exists for `מותמר`/`שעבר עיבוד` in principle; fix all 3 or the same
   bug ships again under different label phrasing.
3. **`לא מעובד` negative-lookaround must be a pre-check on `מעובד` itself**, not scoped to
   "immediately after עמילן" — live corpus string `"עמילן תירס (לא מעובד)"`
   (`cakes_merged_bsip0_raw.json:3792`) has לא between the source word and מעובד, not between עמילן
   and מעובד. Required regression test: this string must keep resolving `native_starch`.

Penalty correctness: **CONFIRMED earned.** E-1442 is unambiguously modified (regulatory/Codex
definition, not a borderline call). The −3 medium-tier placement (grouped with mono/diglycerides,
DATEM, SSL, PGPR, carrageenan — one tier below CMC/P80 high-concern) is scientifically defensible,
consistent with the red-label de-anchor graduated-severity doctrine. No double-counting with
`additive_quality` (native_starch_relief=0, separate dimension).

Grade-move honesty: **CONFIRMED all 6, all downward-only** — corrects a real on-label additive that
was silently uncounted; matches the honest-data-over-grade-continuity doctrine and the same shape as
the "honest S-grades ship" ruling (a genuinely-earned grade isn't hidden one band up).

Ruled **NOT a scoring-philosophy tripwire** — a bug fix restoring the engine's own documented intent
(F1 exists to pull *native* starch out of additive burden; these 27 products are not native).

## Product D7 co-sign (dispatch af772bf1, this session, verified against Nutrition + C3 artifacts)
**YES, co-sign**, same 2 hardenings as a hard merge condition, plus: log C3's guardrail #3 (scan
pectin/gelatin/lecithin for the same contiguous-match defect) as an explicit follow-up task, not
silently dropped. Split confirmed sound (same precedent as `SPOONABLE_RESCORE_COSIGN.md`'s
whitespace-fragility fix — Product+Nutrition co-sign suffices for a pre-launch rescore; no published
score touched). Yogurt go-live impact: does NOT change go/no-go, changes what "go" is built on — both
pages ship, only on corrected grades; 938396's "שני מייצבים טבעיים" copy claim is a factual over-claim
independent of the fix (modified starch is on-label either way) and must be re-authored; all 6 crossed
products' copy needs re-authoring + re-gate (Content + Adversarial QA) since a score/grade change
invalidates prior sign-off.

**Owner-digest line (Product-drafted):** "A classifier bug undercounted a real on-label additive
(modified tapioca starch) on 3 live categories — fixing it drops hummus/cakes/crackers by up to one
grade on 4 products (all more accurate, none newly penalized unfairly); recommend approving
regen+redeploy once Nutrition's hardening lands, no rush, live pages are unaffected until you say go."

## Status
Both co-signs GRANTED (conditional on the 2 regex hardenings). Score_engine.py / constants.py /
ingredient_taxonomy.py remain byte-identical as of this record — no fix applied yet. Next: implement
the hardened fix (isolated worktree, C1 build lane) → cross-corpus baseline diff (C2) → re-score
pre-launch yogurt only → re-author affected copy (Content) → re-gate (Adversarial QA) → log the live
3-category re-flow as an owner-approval digest item (not blocking yogurt).
