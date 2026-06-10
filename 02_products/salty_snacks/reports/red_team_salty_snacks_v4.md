# Red-Team Challenge Report — salty-snacks (run_salty_snacks_002 / v4)
Date: 2026-06-10
Scope: 41 products, /hashvaot/salty-snacks (frontend v4), git branch `salty-snacks-v4` @ e73f5d2f
Challenger: red-team-agent
Gate: satisfies QA Hard Rule 9 (pre-launch red-team challenge required before PASS)

## Opening Finding

**85% of the shelf (35/41 products) is scored with NO ingredient list — panel (nutrition table) only.**
Of the 32 products labeled NOVA-2, **31 carry that NOVA-2 label with `ingredientCount: 0`**. NOVA-2
here is therefore assigned by *absence of detectable additive markers in an absent ingredient string*,
not by confirmed composition. Under Hard Rule 6 (data-absent scoring) and Hard Rule 7 (no phantom
confidence) this is the structural headline and must be disclosed as such — it is NOT buried in
per-product notes.

Mitigating fact (why this is not, by itself, a launch blocker): the system already declares this
honestly. Every panel-only product carries `confidence: "partial"`, `confidence_label_he` = "דירוג
לפי הטבלה התזונתית בלבד", and a tooltip stating the ingredient list was unavailable. The NOVA group
is shown but the consumer-facing confidence state is correct. The finding is that the *internal
NOVA-2 distribution* (32/41) reads as a positive composition signal when it is largely a default
applied in the absence of contradicting data — and the engine itself flags this (`nova_confidence`
"low", "no_ingredient_list: NOVA inference unreliable"). Keep the consumer honesty; do not let the
NOVA-2 count be read as evidence of clean composition in any downstream copy or marketing.

## Product-by-Product Assessment

All 41 published scores were **independently recomputed** from the current BSIP1 records through the
frozen engine (`engine-baseline-2026-06-04` + TASK-216, `BARI_RECAL_P0=on`). **40/41 reproduce the
published score within rounding; 1/41 (Calbee, trivially) differs by <0.2 and rounds identically.**
No published score failed to reproduce. Reproducibility of the shelf is confirmed.

| ID (barcode) | Product | Pub | Grade | Recomputed | RT Assessment | Conf | Critical Notes |
|---|---|---|---|---|---|---|---|
| 7290110560317 | פריכיות משולשות מלח ים (Energy) | 77 | B | 77.2/B | Plausible | partial | Ceiling. Panel-only; 15g protein/8g fiber drive it. No ingredient list to confirm. |
| 7290000069364 | פריכונים אורז ללא מלח (אסם) | 76 | B | 75.7/B | Plausible | partial | 15mg sodium drives it; panel-only. |
| 7290000060071 | פריכונים אורז מלא (אסם) | 72 | B | 72.5/B | Plausible | partial | Same panel as 069364 but sodium 400 vs 15 → 4pt gap, proportionate. |
| 7290112967381 | פריכיות דגנים וקטניות (נסטלה) | 71 | B | 71.3/B | Plausible | partial | fiber 20g (implausibly high — see RT-6). |
| 7290111564291 | פריכיות קינואה (נסטלה) | 71 | B | 71.3/B | Plausible | partial | |
| 7290111564277 | פריכיות 3 דגנים (נסטלה) | 71 | B | 70.6/B | Plausible | partial | |
| 7290008745239 | תפוציפס קראנץ' | 70 | B | 70.0/B | Justified | verified | Real 3-ingredient list; 34.6g fat openly stated. Defensible. |
| 9322969000022 | פריכיות תירס סויה פשתן | 68 | B | 68.4/B | Plausible | partial | NOVA-3, panel-only. |
| 7702024074625 | קרקר פיטנס חיטה מלאה | 67 | B | 67.0/B | Plausible | partial | sugar 10g on a "cracker" — see RT-6. |
| 7290018198254 | קריספי צ'יפס תפוגן | 67 | B | 67.0/B | WEAK | partial | kcal 128/100g — implausible for a fried chip (see RT-5). |
| 7290119373345 | פריכיות תפו"א ואפונה (Energy) | 67 | B | 66.9/B | Plausible | partial | |
| 7290018198148 | קריספי צ'יפס קלאסי תפוגן | 66 | B | 66.3/B | WEAK | partial | kcal 139/100g — same implausibility as 198254. |
| 7290000066332 | אפרופו 50g (אסם) | 65 | C | 64.8/C | Plausible | verified | sodium NULL but scored 65 — see RT-4. Real 7-ingredient list. |
| 7290122782615 | קרקר כוסמין ודבש פיטנס | 64 | C | 64.4/C | Plausible | partial | |
| 7290004943738 | צ'יפס אמריקאי מילוטל | 63 | C | 63.4/C | WEAK | partial | sodium 17mg + kcal 145 — implausible fried-chip panel (RT-5). |
| 7290115679960 | ציטוס פופקורן (עלית) | 63 | C | 62.9/C | Plausible | partial | |
| 7290117035009 | פופקורן מיקרוגל יוחננוף | 62 | C | 61.5/C | Plausible | partial | trans 0.5 declared-threshold (no penalty — correct). |
| 7290000066318 | במבה קלאסי (אסם) | 61 | C | 61.2/C | CHALLENGED | verified | trans_status=high_concern on 0.625 = uncorrected 0.5g/80g artifact (RT-2). |
| 7290106574953 | בייגלה שטוחים שומשום | 60 | C | 60.0/C | Plausible | partial | sodium-capped cluster. |
| 7290018893654 | בייגלה צ'וקטה | 60 | C | 60.0/C | Plausible | partial | sodium 1120mg — highest on shelf, still floored at 60 (RT-3). |
| 7290017928364 | בייגלה XL מאיר | 60 | C | 60.0/C | Plausible | partial | |
| 7290000076133 | בייגלה שמיניות | 60 | C | 60.0/C | Plausible | partial | |
| 7290000071008 | בייגלה שטוחים מלח | 60 | C | 60.0/C | Plausible | partial | |
| 7290000070919 | בייגלה רשתות מלח | 60 | C | 60.0/C | Plausible | partial | |
| 7290112968807 | פיטנס קרקר דק סלק | 60 | C | 59.9/C | CHALLENGED | partial | The trans-correction rescue 0→60 (RT-1). NOVA contradiction (RT-7). |
| 7290106573314 | קריספי כפרי (אסם) | 59 | C | 59.0/C | Plausible | partial | sodium NULL, scored 59 (RT-4). |
| 7290017928661 | שברי בייגלה צ'דר (סמאש) | 58 | C | 57.7/C | Plausible | partial | |
| 7290112965684 | פיטנס מולטיגריין | 54 | C | 54.4/C | Plausible | partial | |
| 7290000420325 | פופקורן Pop Star | 54 | C | 54.0/C | Plausible | partial | trans 0.4 = "present" −10, also a likely artifact (RT-2). |
| 5701932026971 | פופקורן הוט פופ | 50 | C | 50.0/C | Plausible | partial | satfat 13.8g; trans 0.5 declared-threshold. |
| 7290104500572 | אפרופו איטליאנו | 42 | D | 41.8/D | CHALLENGED | partial | trans 0.6 = high_concern −20 on 0.3g/50g serving artifact (RT-2). |
| 7290000066141 | ביסלי גריל (אסם) | 41 | D | 41.3/D | Justified | verified | Real 16-ingredient list incl MSG/E627/E631; NOVA-4 defensible. |
| 7290110551926 | תפוצ'יפס גורמה בטטה | 36 | D | 36.1/D | Plausible | partial | sugar 25g panel-only. |
| 7290100850916 | דוריטוס חמוץ חריף | 36 | D | 35.8/D | Justified | verified | Real 20-ingredient list, NOVA-4, aspartame. Defensible. |
| 8851016002685 | מקלות צ'ילי קלבי | 33 | E | 33.0/E | Plausible | partial | sodium 836mg. |
| 7290000066295 | במבה מתוקה (אסם) | 30 | E | 29.9/E | Plausible | partial | sugar 43g. |
| 4011800528416 | קורני בוטנים | 30 | E | 29.6/E | Plausible | partial | sugar 22g/satfat 11g; trans 0.5 declared. |
| 7290112494313 | קליק קורנפלקס | 25 | E | 25.0/E | WEAK | partial | fiber 38g/100g — physically impossible (RT-6). |
| 7290118421603 | אפרופו קרמל | 18 | E | 18.2/E | RESOLVED | partial | trans corrected 1.25→0 (TASK-229). Published = 18/E, NOT 0/E (RT-1). |
| 4014400925319 | פופקורן קרמל Werther's | 17 | E | 16.7/E | Plausible | partial | sugar 53g. |
| 7290116537375 | קליק כריות נוגט | 16 | E | 15.5/E | Justified | verified | Real 24-ingredient list, sugar 48g. Defensible floor. |

## Summary Assessment

- **Justified (structural logic + inspectable evidence):** the 6 ingredient-resolved products
  (תפוציפס קראנץ' 70, אפרופו 50g 65, במבה קלאסי 61, ביסלי גריל 41, דוריטוס 36, קליק נוגט 16). These
  have real ingredient lists; their NOVA and additive findings are defensible.
- **Plausible but unverifiable:** the 29 panel-only products whose scores reproduce cleanly but rest
  entirely on a nutrition table with no ingredient confirmation. The numbers are internally correct;
  the *composition basis* is unconfirmable.
- **Weak confidence:** 7290018198254 / 7290018198148 / 7290004943738 — three "chips" with calorie
  density 128–145 kcal/100g, which is implausible for a fried potato chip and signals a per-serving /
  per-100g basis error in the source panel (RT-5).
- **Noise-level precision (indistinguishable):** the seven-product 60/C cluster (six pretzels +
  beet cracker) and the four-product 71/B cluster. Differences inside each are <2 pts — correctly
  presented as a tie band, not a rank.
- **Potentially incorrect:** none of the *published* scores. The one apparent 0/E (אפרופו קרמל) is a
  stale-trace artifact only; the published value is the correct 18/E.
- **Overriding structural problem:** none that blocks launch. The trans-fat artifact handling
  (RT-1/RT-2) is the sharpest systemic issue but does not move any published grade boundary.

## Findings by Severity

### CRITICAL — must resolve before launch
**None.** All 41 published scores reproduce from current data through the frozen engine. The
trans-correction did not produce an indefensible published score, and the one suspected
"unjustly-rescued 0/E" (אפרופו קרמל) is in fact published at 18/E, fully reproducible.

### HIGH — should resolve before launch (require explicit acknowledgment)

**RT-1 — The trans-fat data correction is defensible in mechanism, but the rescue it produced is
load-bearing for the beet cracker and must be acknowledged as such.**
  Evidence: `fix_beet_cracker_trans.py` + BSIP1 `data_corrections` (TASK-231) set
  `fat_trans_g 2.326→0.0`. Verified arithmetic: 2.326 × (21.5g serving / 100) = **exactly 0.5g** —
  i.e. the OFF 100g value was the Israeli "<1g" serving declaration (0.5g) divided by the serving
  fraction. The mechanism is real and the correction is *honest data repair*, not score
  engineering. BUT: the correction moves this product from 0/E to 59.9/C — a **4-grade swing that
  changes whether it appears on the shelf at all**. The same logic was correctly applied to אפרופו
  קרמל (TASK-229, 1.25 → 0; 1.25 × 40/100 = 0.5g). A skeptical reviewer's challenge: "you only
  discovered the artifact on products the veto sent to zero." That is defensible *only* if the same
  correction is applied consistently to the lower-trans artifacts that did NOT trigger the veto —
  which it currently is NOT (see RT-2).
  Implication: if a journalist reverse-engineers one corrected product and one uncorrected product
  carrying the identical 0.5g-serving signature, the selective application looks like outcome-driven
  data editing.
  Routes to: **data-agent** (apply the artifact correction consistently across the corpus, or
  document why only the >1.0 cases were corrected) + **nutrition-agent** (own the methodology call).

**RT-2 — The 0.5g serving-declaration artifact is corpus-wide and is being scored as a real
penalty on the products that fall *below* the veto threshold.**
  Evidence: 13 products carry nonzero trans; arithmetic shows the artifact signature on multiple:
  במבה קלאסי 0.625 = 0.5g/80g serving → `trans_status: high_concern` → **−20 penalty**;
  אפרופו איטליאנו 0.6 = 0.3g/50g → high_concern −20; Pop Star 0.4 → "present" −10. Yet `signal_extractor`
  only neutralizes the artifact when `fat_trans_g == 0.5` *exactly* (`trans_fat_threshold_artifact`).
  Any product where 0.5g was scaled by a serving size ≠ 100g lands at 0.4 / 0.6 / 0.625 / 1.25 and is
  penalized or vetoed as if measured. The engine's own comment (signal_extractor L1097) acknowledges
  0.5g is the declaration convention, but the guard is too narrow to catch the scaled values.
  Impact verified by re-scoring with trans=0: במבה +1.6, אפרופו איטליאנו +1.2 — small, no grade
  change today, but the logic is unsound and a future product could cross a boundary on a phantom.
  Implication: inconsistent trans handling; some products penalized for a labeling convention they
  share with two products that were exempted.
  Routes to: **nutrition-agent** (widen the threshold-declaration guard to detect the scaled 0.5g
  signature, e.g. flag when trans×plausible-serving ≈ 0.5 and no PHVO marker) + **data-agent**.

**RT-3 — `has_phvo: false` is derived from an absent ingredient list on 35/41 products, yet it is
the *only* gate standing between a trans value and a score-zero veto.**
  Evidence: `score_engine` L1709–1714: `trans_veto = trans > 1.0 and not _natural_dairy_trans_exempt`,
  where the dairy exemption requires `category == whole_food_fat`. For a salty snack there is **no
  exemption path at all** — a panel-only product with a >1.0 OFF artifact and no ingredient list
  (so PHVO can be neither confirmed nor ruled out) is vetoed to 0 purely on the OFF number. אפרופו
  קרמל would have been exactly this case had TASK-229 not manually intervened. The veto is a hard
  safety commitment (correct in spirit) but it currently trusts an unverified third-party 100g
  trans value over the absence of any PHVO source — the inverse of the precautionary logic the
  beet-cracker fix itself articulates.
  Implication: the category is one bad OFF panel away from publishing a 0/E that requires manual
  rescue. This is fragile and not auditable at scale.
  Routes to: **nutrition-agent** (add a snack-category guard: suppress the >1.0 veto to a
  high_concern penalty when ingredient list is absent AND no PHVO marker is present AND the value
  matches a serving-scaling artifact signature; keep the full veto only when PHVO is confirmed).

**RT-7 — Beet cracker NOVA contradiction between BSIP1 (4) and published (3), with a hidden
ingredient list.**
  Evidence: BSIP1 `bsip1_snack_7290112968807.json` has `nova_proxy: 4` and a *full 15-item English
  ingredient list*; the BSIP2 trace and frontend show **NOVA 3** and `ingredientCount: 0` /
  `ingredients: ""` (TASK-231 omitted the English list as panel-only). The consumer therefore sees a
  NOVA-3, "partial / table-only" product whose own upstream record both (a) contains a full
  ingredient list and (b) classifies it NOVA-4. The rescued 60/C product is the one with the most
  internally contradictory provenance on the shelf.
  Implication: the single most-scrutinized product (manually rescued from 0) is also the one whose
  NOVA and confidence labels contradict its own source record. A critic auditing the rescue will
  find this immediately.
  Routes to: **data-agent** (reconcile NOVA across BSIP1/trace/frontend) + **nutrition-agent**
  (decide whether an English-only ingredient list should drive NOVA even when omitted from display).

### MEDIUM — should document or monitor

**RT-4 — Two NULL-sodium products scored mid-shelf (65/C and 59/C) on incomplete panels.**
  אפרופו 50g (`sodium: null`, also null fiber/sugar/satfat) scores 65/C; קריספי כפרי (`sodium: null`)
  scores 59/C. Both are honestly flagged (`sodiumUnavailable: true`, sodium note). A salty snack
  scored without its sodium value is scoring around the single most relevant attribute of the
  category. Disclosure is correct; the score precision is overstated. Document as a known limitation.
  Routes to: **data-agent** / **content-agent** (consider a wider confidence haircut when the
  category-defining nutrient is missing).

**RT-5 — Three "chips" carry calorie densities (128/139/145 kcal/100g) that are physically
implausible for fried snacks and indicate a per-serving vs per-100g basis error in the OFF panel.**
  תפוגן 198254 (128), תפוגן 198148 (139), מילוטל 63 (145) — fried potato chips run ~500 kcal/100g.
  These three are almost certainly per-serving panels mis-tagged as per-100g, which inflates their
  scores (67/66/63) by suppressing calorie-density and fat penalties. `nutrition_consistency_status`
  passed them as "consistent" because the macros are internally proportional — the check cannot
  catch a uniform basis error. These are the three highest-ranked chips on the shelf and the ranking
  is likely an artifact.
  Routes to: **data-agent** (basis verification on these three EANs against the physical product).

**RT-6 — Implausible fiber values pass unchallenged.** קליק קורנפלקס fiber 38g/100g (physically
impossible for a corn-flake snack; >38% fiber by mass), נסטלה דגנים וקטניות fiber 20g/100g. Both
flow into satiety/nutrient-density scoring. קליק still lands 25/E so no harm today, but the fiber
signal is being trusted without a plausibility ceiling. Routes to: **data-agent**.

**RT-8 — NOVA-2 as default-by-absence (the opening finding, logged here for routing).** 31/32 NOVA-2
labels are assigned with zero ingredients. The engine flags `nova_confidence: low` internally and the
frontend confidence state is honest, so this is monitor-only — but no downstream copy may present the
"32 NOVA-2 products" distribution as evidence of clean composition. Routes to: **content-agent**
(guardrail) + **nutrition-agent** (consider showing NOVA only when ingredient-derived).

**RT-9 — Stale BSIP2 trace observed for אפרופו קרמל during review.** An initial read of
`bsip2_outputs/.../bsip1_snack_7290118421603/bsip2_trace.json` returned `final_score_estimate: 0`
with a trans-veto driver; the authoritative on-disk re-read and full recompute both yield 18.2/E with
`L1 trans=0.0`. The on-disk artifacts are consistent; flagging only so QA confirms no 0/E trace
ships in any export bundle. Routes to: **qa-agent** (confirm trace freshness in the baseline freeze).

## Routing Table

| Finding | Severity | Owning Agent | Recommended Action (no implementation by RT) |
|---|---|---|---|
| RT-1 | HIGH | nutrition-agent / data-agent | Acknowledge the beet-cracker rescue is load-bearing; document the correction rule |
| RT-2 | HIGH | nutrition-agent / data-agent | Widen the 0.5g threshold-declaration guard to catch serving-scaled values |
| RT-3 | HIGH | nutrition-agent | Add snack-category guard so >1.0 veto requires confirmed PHVO when ingredients absent |
| RT-7 | HIGH | data-agent / nutrition-agent | Reconcile beet-cracker NOVA (4 vs 3) and ingredient-list omission |
| RT-4 | MEDIUM | data-agent / content-agent | Wider confidence haircut when sodium (category-defining) is null |
| RT-5 | MEDIUM | data-agent | Verify per-100g basis on three low-kcal chips (128/139/145) |
| RT-6 | MEDIUM | data-agent | Add fiber plausibility ceiling |
| RT-8 | MEDIUM | content-agent / nutrition-agent | Guard against presenting NOVA-2 count as composition evidence |
| RT-9 | MEDIUM | qa-agent | Confirm no stale 0/E trace ships in export |

## Verdict

**CONDITIONAL PASS.**

No CRITICAL findings — the QA PASS is not blocked by this report. All 41 published scores
independently reproduce from current data through the frozen engine, the fabricated-identity v3 has
been genuinely replaced with real Yochananof EANs, and the data-absence reality is disclosed honestly
to the consumer. The trans-correction that the brief asked me to challenge is, on inspection, a
legitimate data repair (verified arithmetic: 0.5g serving-declaration ÷ serving fraction), and the
product the brief flagged as "still 0/E" (אפרופו קרמל) is in fact correctly published at 18/E.

Conditions for the launch to be defensible (HIGH findings requiring explicit acknowledgment, not
necessarily resolution, per Hard Rule 3):
1. **RT-1/RT-2/RT-3** — the trans-artifact handling is internally inconsistent (two products
   corrected, three structurally-identical ones penalized) and the veto is fragile against
   panel-only data. Acknowledge the correction rule publicly-defensibly, or apply it consistently.
2. **RT-7** — reconcile the beet-cracker NOVA contradiction before the rescued product is the one a
   critic audits first.

These are flagged, not fixed. Red-Team does not fix, approve, or close.
