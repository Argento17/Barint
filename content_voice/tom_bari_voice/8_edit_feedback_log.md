# 8 — Edit Feedback Log (Tom / Bari Hebrew)

**This is the engine of the whole system.** Every time Tom edits a draft, the diff
is the strongest possible signal of his voice. Capture it here as a before/after
pair. When a move repeats, promote it into `2_voice_fingerprint.md` and
`3_before_after_pairs.md`. The fingerprint only earns its way from PROPOSED (v0.1)
to confirmed (v1.0) through entries in this log.

---

## How to capture an edit (protocol)
1. When Tom edits Content-Agent copy, **before deleting the original**, paste both versions into a new entry below.
2. Tag the **fingerprint move(s)** the edit reveals (or "NEW — unmapped" if it doesn't fit an existing rule).
3. Note the **mode** (Critical / Balanced / Positive) and the **surface** (intro / insight line / benefit-limit bullet / takeaway / headline).
4. Once the **same move appears 2–3 times**, promote it:
   - add/sharpen the rule in `2_voice_fingerprint.md` (note the promotion + date),
   - add a canonical pair to `3_before_after_pairs.md`,
   - add any reusable phrase to `4_approved_phrases.md`.
5. If an edit **contradicts** a current fingerprint rule, that's a correction — update the rule and note that it was overturned by a Tom edit (highest authority, S5).

## Standing harvest cadence (Phase 4, TASK-374 — 2026-06-22)

The harvest was owner-burst (all of Harvests #1–#5 happened reactively). For a
content-first strategy it must be a **standing loop**, not a reaction to noticing bad
copy. Triggers — capture a harvest entry whenever ANY of these fire:

1. **Per category batch** — every time a shelf's copy is authored/regenerated, run the
   Naturalness Gate (`11_naturalness_gate.md`) and log the HIGH/MEDIUM distribution +
   any owner/judge rewrites as before/after pairs. (The protein-bars pilot is the
   template: `_phase1_pilot_report.md`.)
2. **Per owner redline** — any owner edit to shipped/draft copy is captured before the
   original is discarded (the original rule, step 1 above).
3. **Gate-miss** — any mediocre line that PASSED the gate but the owner/judge still
   flags = a calibration gap: add it to the gate's test set (`naturalness_gate.py`
   selftest / file 10) AND log why it slipped. This is how the gate gets sharper.

**Promotion threshold (unchanged):** a move repeated 2–3× promotes into files 2/3/4.
**Calibration threshold (new):** a tell that recurs across ≥2 shelves becomes a HIGH
detector in `naturalness_gate.py` (was MEDIUM) or a new T-row in file 10 §1.5 of file 5.

**Ownership:** the Content Agent runs triggers 1–2 in its self-check; the Adversarial QA
judge surfaces trigger 3. The orchestrator records the distribution at category close.
No separate scheduled job is required — the cadence rides the existing build-page /
two-gate flow.

## Entry template
```
### E### — <short title> · <YYYY-MM-DD> · <mode> · <surface>
**Agent draft:**
<original copy>
**Tom's edit:**
<edited copy>
**Move(s):** <fingerprint move, or NEW — unmapped>
**Promotion status:** captured | promoted → file 2/3/4 (date) | overturned rule X
**Notes:** <what changed and why it matters>
```

---

## Known gaps to fill first (priority for the first edit rounds)
These are the lowest-confidence parts of the PROPOSED fingerprint. Aim Tom's early
edits at them so v1.0 rests on real data:

1. **Positive-mode before/after pairs** — file 3 has none (only Critical/Balanced). Need 2–3 "generic over-praise → Tom's bounded praise" pairs.
2. **Em-dash latitude** (file 2 §7) — does Tom want one pivot per paragraph, or more? His edits decide whether this becomes a registered exception.
3. **Insight-line length** — do rhetorical questions belong in short product insight lines, or only in intros?
4. **How sharp Positive praise may get** — confirm the upper bound of enthusiasm before it reads as a recommendation.

---

## Log (most recent first)

---

### Harvest #7 — Gate COVERAGE gap caught by render-verify · 2026-06-22 · ALL-SHELF (methodology)

After the protein-bars copy passed the gate ("0 clean") and the judge (PASS), a
**render-verify** of the live page (`localhost:3000/hashvaot/protein-bars`) showed
`מזון שלם` ×19 still on screen. Root cause: the deterministic scanner + the pilot only
covered `insightLine/rowVerdict/comparisonContext`. They MISSED `positiveSignals[]`,
some `limitingFactors[]`, and ALL hardcoded `.ts/.tsx` copy — where `מזון שלם` ×16
(JSON) + ×2 (loader + dimension-bars.tsx) survived. **Lesson (hard):** a gate's
all-clear is only as wide as its field coverage; "0 HIGH" ≠ "page clean." RENDER-VERIFY
(fetch the real DOM) is mandatory before declaring any page done — it is the only check
that sees ALL consumer strings regardless of where they live. Two new owner editorial
rules also landed this session: **T8** ("מזון שלם" → "אוכל אמיתי"/"חומרי גלם אמיתיים")
and **T9** (gloss every named additive: "הממתיק מלטיטול"). Both encoded in the gate.

---

### Harvest #6 — Gate-miss on protein-bars refine (Phase-4 cadence trigger 3) · 2026-06-22 · ALL-SHELF

The protein-bars rewrite cleared Layer-1 (0 HIGH) but the **independent judge** caught
the Content Agent had traded the `X, לא Y` calque for a NEW one: the antithesis closer
**`עובד/נוח/מצוין כ-X; פחות/רחוק כ-Y`** ("works as X; less so as Y") on 4 products, plus
T4 metaphors that survived (`החלבון נושא אותו`, `נזקף לטובתו`) and a META opener
(`כדאי לקרוא לזה כמו שזה`). Per the standing cadence (gate-miss → harden), these became
new detectors in `naturalness_gate.py`: **T1b** (antithesis closer), **META**
(meta-narration opener), and **T4 promoted MEDIUM→HIGH** (specific known calques). The
selftest grew from 7 to 12 flagged lines. After a refine cycle the re-judge returned
**PASS (16/16, F1≥4 AND F2≥4)**. Lesson: removing one calque is not enough — agents
substitute a sibling calque; the gate must enumerate the family. The judge (not the
deterministic layer) is what caught it — the two-gate is load-bearing, not ceremony.

---

### Harvest #5 — Translationese taxonomy (Project Tom's Voice / TASK-374) · 2026-06-22 · ALL-SHELF

Source: owner provided **12 labeled live examples** (cereals + chocolate-tablet shelves)
+ **2 owner protein-bar rewrites**, flagging *naturalness* failures that pass every
existing gate. Full catalogue: `10_translationese_taxonomy.md` (T1–T7 + the closer
meta-finding). Two owner rulings promoted this round:

**H5-R1 — Repair the "X לא תמיד אומר Y" signature move (calque T2).**
**Failing:** `נקי לא תמיד אומר חזק` (#2 cereals) — owner: "weird phrasing."
**Ruling:** the move's *intent* stays; the calqued "...לא תמיד אומר..." phrasing is
retired. Repaired form: **`X הוא לא בהכרח Y`** (`מוצר נקי הוא לא בהכרח מוצר חזק`).
**Promotion status:** promoted → file 2 §2 (Balanced core sentence + closer) + §3
(workhorse construction) + file 4 §C (2026-06-22). "זה לא אומר Y" variant on watch.

**H5-R2 — Pro/con (יתרון/חיסרון) labels in the protein rewrites = editing shorthand, not a format.**
**Ruling:** final copy stays flowing prose (the #1-chocolate model). No frontend/design
change. The value in the rewrites is the *phrasing* (T1/T4/T7 fixes, jargon gloss,
discourse connectors), not the layout.
**Promotion status:** recorded → file 10 RESOLVED (2026-06-22).

**H5-R3 — The target register is "in-between"; two failure modes, not one.**
Owner ruling on the 8 gold rewrites: the fix is NOT "calm" — *"AI does not treat
'calm' nicely, it becomes too neutral that it doesn't write anything. Should be
somewhere in between."* **Target = opinionated substance in natural connected Hebrew.**
The gate must catch **F1 translationese-punch** (staccato calques, `X, לא Y`) AND
**F2 neutral-bland** (no stance, hedge-only, says nothing). Fingerprint keeps its
stance/verdict commitment (F2 guard) but moves default *texture* from staccato/"(!)"
to connected prose; punch becomes seasoning-when-earned. **Promotion status:** recorded
→ file 10 §D; drove Phase 1 (two-axis gate) + the fingerprint recalibration pass.
**APPLIED 2026-06-22 (Phase 1.5):** file 2 §0.5 added (default register = opinionated
substance in connected prose; F1+F2 failure modes; punch = seasoning-when-earned;
stance kept as F2 guard, supersedes conflicting punch-default rules); §1 step 1 opener
broadened to calm-orienting OR scene; §5 rhythm flipped to connected-prose default
(staccato chain = F1 failure); §3 "(!)" marked seasoning-only + gate-monitored.

**Meta-finding (owner):** the closer / "finish line" is the systematic failure zone —
`הקשר במדף` reliably collapses into T1 (`X, לא Y`) and T3 (dangling `גם`) calques. The
Phase 1 Naturalness Gate weights the final beat hardest. The full T1–T7 tell list is the
gate's calibration target; pending confirmation of screenshot transcriptions before
individual pairs promote to `3_before_after_pairs.md`.

---

### Harvest #4 — Batch-1 reconciliation · 2026-06-19 · ALL-SHELF CONFIRMED

Source: Owner batch-1 reconciliation on cereals + cross-shelf voice rules.
4 owner rulings. All are **promoted** this round into `2_voice_fingerprint.md`,
`5_banned_phrases_and_claims.md`, and `7_voice_match_gate.md`.

---

### H4-1 — No internal product-ID tokens in consumer copy · 2026-06-19 · ALL modes · ALL surfaces

**Agent draft (failing examples):**
> "כמו snk-001 — סוכר גבוה ורשימת רכיבים ארוכה."
> "השוואה ל-jc-042 בקטגוריה."

**Owner ruling:**
Internal slugs (jc-/snk-/hc-NNN), raw barcodes, and bsip1_* keys are pipeline identifiers — never consumer language. Siblings must be named by Hebrew product name or plain descriptor.

**Promotion status:** promoted → file 7 HF-8 (new hard fail) (2026-06-19)

---

### H4-2 — Intro originality: no cross-shelf opener cloning · 2026-06-19 · ALL shelves · intro/hero

**Agent draft (failing pattern):**
> Multiple shelves opening with the cereals "בוקר. ילד צריך לצאת…" scene verbatim.

**Owner ruling:**
Each category's intro/prologue + hero title must be framed to that category's shopping moment. Cereals "בוקר…" is a voice reference for tone, not a template.

**Promotion status:** promoted → file 2 §1 intro-originality principle (2026-06-19)

---

### H4-3 — Additive generalization in verdict prose · 2026-06-19 · ALL modes · rowVerdict/insightLine

**Agent draft (failing examples):**
> "E471, מונו- ודיגליצרידים של חומצות שומן, ושלושה חומרים משמרים…"

**Owner ruling:**
Verdict prose generalizes to "תוספי מזון"; contested-tier additives surface as "שחלקם שנויים במחלוקת". Per-additive detail lives only in the additive sub-dropdown.

**Promotion status:** promoted → file 5 §1 banned table + §4 P-4 (2026-06-19)

---

### H4-4 — Punch on the egregious · 2026-06-19 · ALL modes · verdict framing

**Owner ruling:**
Egregious products (near-zero real primary ingredient, deceptive naming, multiple red signals) get the sharpest honest framing first. Punch = sharper truth, never brand-attack, never fabrication.

**Promotion status:** promoted → file 2 §2 punch-on-egregious calibration (2026-06-19)

---

### Harvest #1 — Cakes shelf · 2026-06-19 · ALL-SHELF CONFIRMED

Source: Tom's Track Changes edits on the first real cakes category draft.
17 before/after pairs extracted and classified below. All substantive edits are
logged individually; trivial precision fixes (unit formatting, qualifier additions)
are grouped at E015–E017. All are **promoted** this round into `2_voice_fingerprint.md`
and/or `5_banned_phrases_and_claims.md`.

---

### E001 — Headline format: poetic two-beat → direct question + value promise · 2026-06-19 · Critical · headline

**Agent draft:**
> זה נראה כמו עוגה ביתית. ואז קוראים את הרכיבים.

**Tom's edit:**
> קונים עוגה ביתית בסופרמרקט? הנה מה שאתם צריכים לדעת

**Move(s):** NEW — Headline register. Tom replaces the poetic two-beat statement (situation → pivot) with a **direct second-person question + an explicit value promise** ("הנה מה שאתם צריכים לדעת"). The question anchors the reader in their real-world action; the value promise tells them why to keep reading. Neither existed in the agent draft.

**Promotion status:** promoted → file 2 §1 + §3 (2026-06-19)

**Notes:** This is a systematic reframe of what a headline does. The agent's draft relied on the "image-vs-contents" pivot as a standalone hook. Tom's version asks the reader a question about their actual buying moment, then makes a promise. The implication: headlines are not closers — they are entry points that establish relevance immediately.

---

### E002 — שורת בארי (punchy product): rhetorical dismissal replaces name-echo closer · 2026-06-19 · Critical · שורת בארי

**Agent draft (Dobosh):**
> שמו של הדובוש מוכר. המבנה שלו פחות.

**Tom's edit:**
> עוגת דובוש? תחשוב שוב.

**Move(s):** Overturns "image-vs-structure" pattern as default closer. Tom replaces the two-clause image-vs-structure beat (name/fame ↔ interior reality) with a **rhetorical-question dismissal** — three words, compressed irony. The product's name becomes the question; the verdict is immediate.

**Promotion status:** promoted → file 2 §3 + §6 (new "שורת בארי dual register" rule) (2026-06-19)

**Notes:** The image-vs-structure beat ("השם מוכר. המבנה פחות.") belongs in file 3 as a valid fingerprint move — but it is **not** the only valid closer. For products where the gap between name/fame and reality is the whole story, Tom prefers the compressed rhetorical question. This is the "clearly-bad product" register of the dual-register rule (see file 2 §6 new rule).

---

### E003 — שורת בארי (nuanced product): one-liner → substantive verdict with named positives + honest catch · 2026-06-19 · Balanced · שורת בארי

**Agent draft (Cheesecake):**
> מוצר סביר יותר — לא בגלל שהוא פשוט, אלא בגלל שהסוכר שם באמת.

**Tom's edit:**
> מוצר סביר יותר ביחס לקטגוריה. מעט סוכר, חלבון סביר, קלוריות לא גבוהות במיוחד. אבל גם כאן זוהה רמת עיבוד גבוהה שלא מאפשרת לנו לתת ציון גבוה.

**Move(s):** OVERTURNS "one sharp closer" rule. Tom **expands** the closer, not compresses it. For a nuanced product, the שורת בארי must (a) state relative standing, (b) name concrete positives, (c) state the honest catch, and (d) tie the catch to the score outcome — in plain consumer language ("שלא מאפשרת לנו לתת ציון גבוה" = why the grade is what it is, without mechanism leakage).

**Promotion status:** promoted → file 2 §6 (dual-register rule for שורת בארי) (2026-06-19)

**Notes:** The agent draft was "one sharp line." Tom's edit triples the length. This is not a case where the agent was wrong about the direction — "מוצר סביר יותר" is correct — but wrong about the scope. Nuanced products deserve a fuller verdict. The old "one sharp closer" instruction was over-compressed.

---

### E004 — De-escalation removed: "אין כאן דרמה" is the agent's restraint, not Tom's · 2026-06-19 · Critical · intro/framing

**Agent draft:**
> אין כאן דרמה. יש כאן פער בין הדימוי...

**Tom's edit:**
> יש כאן פער עצום בין הדימוי... מדובר במוצר תעשייתי לכל דבר.

**Move(s):** RETIRES default de-escalation. Tom deletes "אין כאן דרמה" entirely and raises the register: "פער" → "פער עצום"; "מוצר מדף" → "מוצר תעשייתי לכל דבר." The agent's reflex to pre-emptively soften is rejected when the product warrants a stronger finding. The product earns the word "עצום" — and Tom uses it.

**Promotion status:** promoted → file 2 §2 (retire "אין כאן דרמה" as default) + §5 (approved register) (2026-06-19)

**Notes:** "אין כאן דרמה / לא צריך להפוך את זה לדרמה" appeared in the agent draft as a pre-emption of consumer over-reaction. Tom's edit shows this is a misread of his voice: when the product warrants firmness, Tom is firm. The de-escalation was self-censorship by the agent, not an editorial choice.

---

### E005 — Throat-clearing deleted: "ברור ש..." concessions and self-narration removed · 2026-06-19 · Critical · body

**Agent draft (three separate deletions):**
> "זו עוגה — ברור שהיא מתוקה."
> "מובן."
> "צריך לומר מה הסיבה... ולא לייצר ציפייה שגויה."

**Tom's edit:** All three deleted entirely (no replacement).

**Move(s):** Throat-clearing cut. Three categories of clutter removed: (1) "ברור ש..." concessions — the reader already knows cakes are sweet; stating it apologizes for nothing; (2) the filler acknowledgment "מובן"; (3) meta-narration of editorial intent ("צריך לומר מה הסיבה").

**Promotion status:** promoted → file 2 §2 (new "trim throat-clearing" rule) (2026-06-19)

**Notes:** All three deletions share a structure: they narrate or excuse what the text is about to do, rather than doing it. Tom's voice is economical. It does not warm up, does not explain its method, does not apologize for directness.

---

### E006 — Register: category descriptor → firmer industrial classification · 2026-06-19 · Critical · body

**Agent draft (two instances):**
> "קינוחים תעשייתיים" (category label)
> "מוצר מדף מתועש" (product descriptor)

**Tom's edit:**
> "מוצרים אולטרא-תעשייתיים"
> "מוצר תעשייתי לכל דבר"

**Move(s):** Register elevation. "קינוחים תעשייתיים" is a neutral category name; "מוצרים אולטרא-תעשייתיים" is a finding. "מדף מתועש" is jargon; "לכל דבר" is consumer-immediate ("entirely / through and through"). Both edits move from a descriptor to a verdict, without crossing into scare language.

**Promotion status:** promoted → file 2 §5 (approved register vocabulary) (2026-06-19)

**Notes:** "אולטרא-תעשייתי" and "מוצר תעשייתי לכל דבר" are now the approved terms for this finding class. "מדף מתועש" is retired. These are not scare phrases — they are precise industrial-classification language that a consumer can understand directly.

---

### E007 — Emphasis: number + exclamation marker vs. bare count · 2026-06-19 · Critical · body

**Agent draft:**
> כאן יש 21 תוספי מזון

**Tom's edit:**
> בעוגה הזאת יש 21 (!) תוספי מזון

**Move(s):** Emphasis + product-anchor. Two changes: (1) "כאן" → "בעוגה הזאת" — grounds the count in this specific product rather than a vague location; (2) "(!) " after the number — Tom uses the parenthetical exclamation as a register signal that says "stop and notice this number" without editorializing in the prose.

**Promotion status:** promoted → file 2 §3 (new emphasis move: "(!)") (2026-06-19)

**Notes:** The "(!) " construction is a Tom fingerprint — it creates an arrested-breath effect in the reader without the agent making an evaluative claim. The number evaluates itself; the "(!) " just ensures the reader doesn't glide past it. This is appropriate for genuinely exceptional counts and should not be overused.

---

### E008 — Investigative structure added: simple-ideal → discovery → mechanism (WHY) · 2026-06-19 · Critical · body

**Agent draft:** No equivalent paragraph. The agent stated the finding without establishing the expected baseline or explaining the cause.

**Tom's edit (new paragraph added):**
> עוגה היא מוצר פשוט יחסית. קמח, סוכר, ביצים, שמן... מה שגילינו הוא שזה ממש לא המצב... יצרנים צריכים להשאיר את המוצר זמן רב על המדף → תיעוש גבוה.

**Move(s):** NEW — Investigative structure. Tom adds a three-part explanatory paragraph the agent had no template for: (1) the **simple ideal** — what the product *should* be ("עוגה היא מוצר פשוט יחסית. קמח, סוכר, ביצים, שמן..."); (2) the **discovery** — "מה שגילינו הוא שזה ממש לא המצב"; (3) the **mechanism / WHY** — the shelf-life/industrialization chain. Tom is not content to assert the finding — he shows the reader why it happens.

**Promotion status:** promoted → file 2 §4 (new investigative-structure rule) (2026-06-19)

**Notes:** This is the single largest structural addition Tom made. It implies a new spine beat between "the pivot" and "the evidence": establish the simple-ideal baseline, then introduce the discovery, then explain the mechanism. The agent's arc (§1 of file 2) did not include this. The spine needs updating.

---

### E009 — Constructive-alternative recommendation: Tom adds "our recommendation is..." · 2026-06-19 · Critical · closer

**Agent draft:** No equivalent passage. The agent's stance was description-only.

**Tom's edit (new paragraph added):**
> אנחנו לא אומרים ולעולם לא נאמר לכם מה לאכול. אבל המלצתנו היא שאם אתם בוחרים באכילת עוגה — תנסו לאפות אותה בבית.

**Move(s):** NEW — Constructive-alternative recommendation. Tom introduces a "our recommendation" framing that was previously treated as a file-5 violation. The structure: (1) explicit non-prescriptive disclaimer ("לא אומרים... מה לאכול"); (2) a bounded recommendation framed as "if you're choosing X, consider Y"; (3) a constructive alternative (bake at home) rather than "don't eat." This is a carve-out from the blanket "מומלץ/להימנע" ban.

**Promotion status:** promoted → file 5 §1 (carve-out) (2026-06-19)

**Notes:** This is an owner ruling on a previously prohibited category. The firewall still holds against "אסור לאכול", "להימנע", medical/disease claims. But constructive-alternative recommendations, when framed with the non-prescriptive disclaimer + if-clause + positive alternative, are now explicitly permitted. See file 5 §1 carve-out for the exact bounds.

---

### E010 — De-escalation language hardened: "פער" → "פער עצום" · 2026-06-19 · Critical · body

**Agent draft:**
> יש כאן פער בין הדימוי

**Tom's edit:**
> יש כאן פער עצום בין הדימוי

**Move(s):** Intensity upgrade. This pairs with E004 — Tom is willing to use strong adjectives ("עצום") when the product earns them. The agent's instinct to understate is not Tom's instinct.

**Promotion status:** promoted → file 2 §2 (firmer verdicts rule) (2026-06-19)

**Notes:** This is one of three intensity-upgrade edits in this harvest (see also E006, E007). Together they establish the pattern: the agent systematically understated; Tom corrects toward the earned intensity.

---

### E011 — Additive count phrasing: anchor to product ("בעוגה הזאת") · 2026-06-19 · Critical · body

**Agent draft:**
> כאן יש 21

**Tom's edit:**
> בעוגה הזאת יש 21

**Move(s):** Product-anchor precision. "כאן" is a location that does not name the product; "בעוגה הזאת" names the specific product. Swap-test alignment: the edited version cannot be copy-pasted across the shelf without feeling wrong.

**Promotion status:** promoted → file 2 §3 (precision rule) (2026-06-19)

**Notes:** Small edit, high signal. Tom grounds every claim in the specific product, not a shelf-level generalization. This is the HF-3 (swap-test) discipline at the micro-copy level — even when writing a count, the product name or "this product" must anchor it.

---

### E012 — "תוספי תזונה" → "תוספי מזון" (term fix) · 2026-06-19 · any · body

**Agent draft:** Used "תוספי תזונה" (dietary supplements) where food additives were meant.

**Tom's edit:** "תוספי מזון" (food additives).

**Move(s):** Term correction — not a voice move; a factual error. "תוספי תזונה" = dietary supplements (vitamins, minerals, etc.). "תוספי מזון" = food additives (emulsifiers, stabilizers, preservatives). Using the wrong term is a credibility failure in consumer copy.

**Promotion status:** promoted → file 5 §1 (existing ban on "תוספי תזונה" confirmed; reinforce guidance) (2026-06-19)

**Notes:** This term confusion already existed in file 5 §1 as a banned phrase. Tom's edit confirms the ban is correct and the agent must not use "תוספי תזונה" when meaning food additives in any consumer-facing copy.

---

### E013 — Firmer industrial verdict: named industrial-framing amplified · 2026-06-19 · Critical · body

**Agent draft:**
> מדובר במוצר מדף מתועש

**Tom's edit:**
> מדובר במוצר תעשייתי לכל דבר

**Move(s):** Register clarification. "מדף מתועש" combines two concepts (shelf product + processed) into a compound that is less clear than two separate words. "לכל דבר" is the amplifier — "through and through / in every sense." The phrase is stronger without scare vocabulary.

**Promotion status:** promoted → file 2 §5 (2026-06-19) [see also E006]

**Notes:** This is the second instance of the "לכל דבר" construction in this harvest. It is now a confirmed Tom register marker — an amplifier that works without hyperbole.

---

### E014 — On-shelf questioning introduced in תצוגת המוצר (rhetorical mirror for the category page) · 2026-06-19 · Critical · intro

**Agent draft:** Category intro framed as a neutral overview of what the comparison page contains.

**Tom's edit:** Intro recast with the "rhetorical mirror" move — surfaces the question the consumer should have been asking at the shelf ("אם על האריזה היה כתוב מראש 'עוגת מדף עם רשימת רכיבים ארוכה ותוספי מזון רבים' — האם הייתם מתייחסים אליה אותו דבר?").

**Move(s):** Rhetorical mirror (existing §3 fingerprint move). Confirmation that this move belongs in category intros, not just product-level copy. It forces the consumer to confront the delta between the shelf presentation and the real formulation.

**Promotion status:** captured (existing fingerprint move — promoted in the sense of confirmed; no new fingerprint entry needed) (2026-06-19)

**Notes:** The rhetorical mirror was listed in §3 as a fingerprint move but not yet confirmed by a real edit. This edit confirms it.

---

### E015–E017 — Precision / formatting group · 2026-06-19 · mixed · body

Grouped: three precision edits that confirm existing rules or fill detail gaps.

**E015 — Qualifier "על פניו" added (honesty qualifier):**
Agent draft omitted the qualifier on a visual-appearance claim. Tom added "על פניו" to signal "on the surface / at first glance" before a claim about appearance. Confirms: visual-appearance claims need a surface-level qualifier to distinguish them from structural findings.
Promotion status: captured (supports precision rule in §5) (2026-06-19)

**E016 — "בצורה שמחה" → "בצורה טובה" (no whimsy):**
"שמחה" (happy/cheerful) as an adverb describing how something performs is a whimsical register Tom does not use. "טובה" (well/good) is the plain word. Confirms: precise, plain language over cute adjectives.
Promotion status: promoted → file 2 §5 (no whimsy rule) (2026-06-19)

**E017 — "ל-100 גרם" added (unit precision):**
Tom added the per-100g unit specification where the agent stated a raw number without a referent. Confirms: every nutritional number must carry its unit and referent ("ל-100 גרם"). A bare number is incomplete.
Promotion status: promoted → file 2 §5 (precision rule confirmed) (2026-06-19)

---

## Harvest #2 — Cereals shelf · 2026-06-19 · ALL-SHELF CONFIRMED

Source: Tom's redline on the first real cereals category draft (cereals_draft_v0_AGENT.md).
4 owner rulings. All are **promoted** this round into `2_voice_fingerprint.md`,
`5_banned_phrases_and_claims.md`, and `7_voice_match_gate.md`.

---

### H2-R1 — No code language in consumer copy · 2026-06-19 · ALL modes · ALL surfaces

**Agent draft (failing examples):**
> "ללא תוספי מזון (d4_additives ריק)"
> "כמות מדויקת null"
> "מקור: `expansion.nutrition`"

**Owner ruling:**
A reader must NEVER see a field name, `null`, a backtick path, or `expansion.X` in any consumer-facing text. This is a first-order leakage failure.

**What to do instead:**
- Absent quantity: "לא צוין על האריזה" or "לא ידוע מהאריזה"
- Null ingredient list: "רשימת הרכיבים המלאה לא נקראה מהאריזה"
- No additives: "ללא תוספי מזון" — no source citation in consumer copy; source citations go in the separated internal notes block only

**Promotion status:** promoted → file 2 §6 (HARD RULE) + file 5 §1 (new banned row) + file 7 HF-6 (new hard fail) (2026-06-19)

**Notes:** The agent was leaking internal engine field names directly into consumer bullets. The fix is total: code tokens in consumer output are a hard fail, no exceptions, no "mostly clear."

---

### H2-R2 — שורת בארי retired as structural closer; הקשר במדף is the closing beat · 2026-06-19 · ALL modes · closer

**Agent draft (failing example):**
> The draft used "שורת בארי" as a named section heading and structural closing element for each product.

**Owner ruling:**
שורת בארי as a section/structural element is repetitive alongside הקשר במדף, which is "good and important." הקשר במדף becomes the sole closing beat. שורת בארי is removed from the spine (§1 step 7), signature moves (§3), and any structural checklist.

**What to do instead:**
הקשר במדף closes each review. It places the product in its real shelf context: how it ranks, what it beats, what it falls short of. The *voice quality* that Tom wants in a closer (sharp, earned, anchored in data) lives on inside הקשר במדף — only the label "שורת בארי" is retired.

**Promotion status:** promoted → file 2 §1 step 7 (replaced), §3 (שורת בארי closer removed), §6 (hard never) + file 7 Step 1.4 (updated) + file 7 HF-2B (updated closer language) (2026-06-19)

**Notes:** הקשר במדף was already in the v0 draft as a section. The owner confirmed it is sufficient and superior. No structural closer was needed in addition to it.

---

### H2-R3 — Sugar IS in the JSON; "null" claims about sugar are WRONG · 2026-06-19 · ALL modes · evidence

**Agent draft (failing examples):**
> "סוכר גבוה (מסומן בנתונים כ'סוכר גבוה', כמות מדויקת null)"
> (applied to ליון, נסקוויק, סיני מיניס)

**Owner ruling:**
Sugar values ARE present in `expansion.nutrition.sugar` for all three products:
- ליון: 24.7 גרם ל-100 גרם
- נסקוויק: 22.4 גרם ל-100 גרם
- סיני מיניס: 25.0 גרם ל-100 גרם

The agent claimed these were null/unknown — this was STALE and WRONG. Always state the real sugar number from the nutrition block. That is how the engine flagged them as high-sugar.

**What to do instead:**
State the actual value: "24.7 גרם סוכר ל-100 גרם — הגורם שמגביל את הציון."

**Promotion status:** captured as a data-verification lesson; reinforces HF-4 (unverified facts fail the gate) + the principle of reading the full JSON before writing (2026-06-19)

**Notes:** The agent apparently carried stale information from an earlier analysis rather than reading the live JSON. This is a verification failure, not a voice failure. The fix is protocol: always read `expansion.nutrition.sugar` from the JSON before declaring any value unknown.

---

### H2-R4 — Null ingredients: 3 products, honest handling · 2026-06-19 · ALL modes · evidence

**Agent draft (failing example):**
> "רשימת הרכיבים: לא זמינה בנתונים — מה שיש מאחורי 'שוקולד וקרמל' לא ניתן לבדיקה מלאה"

**Owner ruling:**
Exactly 3 products have genuinely null ingredient lists (ליון 5900020036407, נסקוויק 5900020012814, סיני מיניס 72968) — the scrape caught front-of-pack marketing text, not the real ingredient list. A separate re-scrape is underway. For these 3:
- Do NOT invent ingredients
- Do NOT write "null" or code-language
- Lean "מה מגביל" on the real nutrition facts (sugar, sodium, etc.) which ARE known
- If you must reference the list: "רשימת הרכיבים המלאה לא נקראה מהאריזה" — honest, not alarmist
- The framing is factual, not suspicious

**What to do instead:**
Write the מה מגביל section entirely from the nutrition block (sugar, sodium, energy, fiber, protein — all of which are present). The ingredient-list gap is an honest data limitation, not a sign of concealment.

**Promotion status:** promoted → file 2 §6 (HARD RULE zero code tokens) + file 5 §1 (correct handling of null ingredient lists) (2026-06-19)

**Notes:** The agent's handling in v0 was directionally correct (no invented ingredients) but used both an evasive framing and internal field language. The ruling clarifies both dimensions.

---

## Session H3 — Cereals v2, first `content_agent_v1` shelf · owner review 2026-07-10 (TASK-550)

First owner read of copy authored by the real LLM engine (not the deterministic placeholder).
Three rows reviewed; all three defects are systemic, not one-off.

---

### H3-R1 — Rank contradiction: the #1 product described as mediocre *relative to the shelf* · 2026-07-10 · ALL modes · HARD

**Agent draft (failing example):**
> "הפרופיל התזונתי הכולל של ויטביקס נשאר בינוני יחסית למדף, וזה נכון גם כשרשימת הרכיבים קצרה ונקייה מאוד."

**Owner ruling:**
> "the first fact is not true. weetbix is the first in the shelf and therefore הפרופיל התזונתי הכולל של ויטביקס נשאר בינוני יחסית למדף - not a true statement. other analysis is good enough."

**Verified:** ויטביקס (5010029000061) scores 74.7 — the **maximum** of all 20 products (range 32.2–74.7). It is rank 1/20. The claim "בינוני יחסית למדף" is therefore false by construction. The error repeats across FIVE fields: `insightLine`, `rowVerdict`, `consumerTakeaway`, `whyRated`, `watchOut` — and `context` compounds it with "בחלק הבינוני-עליון" (upper-middle) for a product that is first.

**Root cause:** the model read a *dimension* score (nutrient density = mid) and generalized it into a *shelf-relative standing* claim. Dimension ≠ rank. This is the Delifkan fat-contradiction failure class (Ruling 2) one level up: framing that contradicts the product's own trace.

**What to do instead:**
This is precisely where "best ≠ excellent" applies — and the draft inverted the reference frame. The honest construction names the frame explicitly:
- ✅ top of *this* shelf, while the shelf itself is unremarkable in absolute terms
- ⛔ "בינוני יחסית למדף" for the shelf leader — relative to the shelf, it is the best

**Promotion status:** to be enforced mechanically — a rank-aware framing guard (a product at rank 1 may not be framed as at-or-below shelf average on its OVERALL profile). Routed to content-agent (engine + prompt).

**Notes:** Owner explicitly approved the rest of the analysis for this row ("other analysis is good enough") — the protein/sugar findings stand. Only the reference frame is wrong.

---

### H3-R2 — "קל מבחינה תזונתית": wrong Hebrew, inverted valence · 2026-07-10 · ALL modes · HARD

**Agent draft (failing example):**
> "הסיבים נמוכים יחסית לקטגוריה, ובתור מקור לארוחת בוקר המוצר קל יחסית מבחינה תזונתית."

**Owner ruling:**
> "the ending is bad. 'ובתור מקור לארוחת בוקר המוצר קל יחסית מבחינה תזונתית' the קל יחסית מבחינה תזונתית is wrong hebrew and logically flawed."

**Owner's replacement (verbatim, use as the model):**
> "בתור מקור לארוחת בוקר, אתם לא מקבלים כאן הרבה ערכים תזונתיים."

**Verified:** the construction appears twice on 7297488098688 — in `rowVerdict` and again in `watchOut` ("מדובר במוצר קל מבחינה תזונתית").

**Why it fails:** "קל" carries a positive, diet-adjacent connotation while the intended meaning is *nutritionally poor* — the valence is inverted. It is also not idiomatic Hebrew. The owner's replacement is direct, second-person, and says the true thing plainly.

**What to do instead:**
Ban "קל מבחינה תזונתית" / "קל יחסית מבחינה תזונתית" and their variants. When a product is nutritionally thin, say so to the reader directly, in the second person, without euphemism.

**Promotion status:** → file 5 banned-phrase list; the owner's replacement sentence is an approved construction. Routed to content-agent.

---

### H3-R3 — THE WORST PATTERN: ingredient-list opener → recited nutrition values · 2026-07-10 · ALL modes · HARD

**Agent draft (failing example):**
> "רשימת הרכיבים של פצפוצי האורז כוללת שלושה מרכיבים בלבד, ואפס תוספי מזון. הסיבים, לעומת זאת, נמוכים משמעותית מרוב הדגנים במדף — פחות מגרם אחד ל-100 גרם. הנתרן עומד על 390 מיליגרם ל-100 גרם, גבוה משמעותית מהחציון."

**Owner ruling:**
> "this is the worst pattern that the writer does. The pattern is 'the ingredients list is X', 'the nutritional value repetition' here was the sodium. I get what its trying to say - but the flow is wrong, and also using here em dash. not the standard we strive for."

**The pattern, named:** open by stating what the ingredient list *is* → then recite one nutrition value → then recite another. Each sentence is individually legal (the numbers do comparison work, so the recite heuristic clears them), yet the whole reads as a spec sheet with connectors. The flow is wrong.

**Compounding:** em-dash used as the workhorse pivot. Present in BOTH `insightLine` and `rowVerdict` for this product. Per-paragraph the rule is satisfied; the owner's standard is to *minimize*, and the shelf overusesit.

**What to do instead:**
Lead with the finding, not with an inventory of the label. The ingredient list is evidence, not an opening. If two nutrition values must appear, they serve one point — not two consecutive recitations. Resolve contrasts in flowing prose, not on an em-dash.

**Promotion status:** highest-priority prompt + gate work. The existing recite heuristic does NOT catch this (each clause carries a comparison). Needs a structural check: ingredient-list opener followed by ≥2 recited nutrition values. Routed to content-agent.

**Notes:** Orchestrator-caused regression, logged honestly: this row was re-authored *at my instruction* to demote a thin "lowest sugar" superlative. The rewrite traded a superlative defect for the owner's most-disliked pattern. A fix directed at one gate can walk straight into another failure the gates do not measure.

---

## Session H4 — 30-row site-wide sample, owner review · 2026-07-10 (TASK-576)

Owner read 21 of 30 sampled live rows (stratified across all 19 shelves, un-annotated).
Verdicts verbatim, then the extracted pattern set and its site-wide measurement.

**Approved outright (6/21):** rows 12, 13, 15, 16, 17, 19.
**Approved except em-dash (2/21):** rows 1, 14 — "הכל מעולה חוץ מהאם-דש".
**Needs work (13/21).**

---

### H4-P1 — THE PRIMARY DEFECT: the copy scores the product, it does not DESCRIBE it

**Owner, row 3:** "לשכתב. האלגוריתם מבין את פרופיל המוצר אבל לא מתאר אותו כמו שצריך"
**Owner, row 7:** "לשכתב - תיאור גרוע מאוד"
**Owner, row 10:** "אין כאן תיאור מוצר"
**Owner, row 4:** "אין פה שום תיאור שאפשר להבין ממנו משהו על המוצר"

This is a NEW axis, orthogonal to every gate we run. Readability, naturalness, the
integrity battery, the antithesis rule and the recite heuristic all ask *is this true,
legal, well-formed?* **None asks: does this tell the reader what the product IS.** The
engine reasons correctly about the scoring profile and then reports that reasoning back
instead of describing the food. Highest-priority editorial fix; not mechanically detectable.

---

### H4-P2 — Ingredient counts are BANNED (hard)

**Owner, row 4:** "התבנית של 'שלושה רכיבים בלבד' - לא מקובלת."
**Owner, row 5:** "ראה הערה 4 לגבי ציון מספר הרכיבים. אני לא רוצה לראות את זה כתוב."

Never write the NUMBER of ingredients. "שלושה רכיבים בלבד" / "חמישה רכיבים" etc. tell the
reader nothing about the product. The short ingredient list may be *shown* as a structured
fact; it must not be narrated as an insight.
**Measured: 63/710 live rows (9%), 108 occurrences.**
Note: the cereals v2 copy authored under TASK-550 violates this (Vitabix "בזכות שלושה
רכיבים בלבד"; rice-apple "שלושה רכיבים, אפס תוספי מזון") — copy the orchestrator praised.

---

### H4-P3 — Nutritional values repeated across fields

**Owner, rows 6, 8, 11, 20:** "יש כאן חזרתיות על הערכים התזונתיים" / "חזרתיות יתר" /
"חזרתיות על כל הערכים התזונתיים שצריך לשנות"

The same figure restated in insightLine + rowVerdict + takeaway + whyRated.
**Measured (strict: identical number+unit in ≥2 distinct consumer fields): 239/710 rows
(34%), 378 distinct repeated values.** Worst: hummus 35, crackers 32, protein_combined 30,
hard_cheeses 29, cereals 17, cheese 17.

---

### H4-P4 — Em-dash

**Owner, rows 1 and 14:** "הכל מעולה חוץ מהאם-דש."
The ONLY defect in two otherwise-approved rows. Confirms the standing minimize-em-dash rule.
**Measured: 584/710 rows (82%), 1,801 occurrences.** Clean shelves prove it is reachable:
yogurt_drinkable 2, yogurt_spoonable 10, crackers 0.

---

### H4-P5 — Padding: stop when the sentence is done

**Owner, row 2:** "אפשר לסיים ב'חלה קלאסית'. התוספת מיותרת."
A trailing clause that earns nothing. End on the strong noun.

---

### H4-P6 — Vague stock phrase "עושים את רוב העבודה כאן"

**Owner, row 18:** "אני רואה הרבה פעמים תיאור של 'עושים את רוב העבודה כאן'. זה לא תמיד ברור
למה מתכוונים. אני מציע לשנות את הניסוח הזה"

**Measured — and the owner's impression overstates the frequency: 6/710 rows** carry the
phrase family (רוב העבודה / עושים את העבודה), not "many". Real, but small. Fix the six;
do not build a gate for it.

---

### H4-P7 — Ungrammatical sentence AND grade spelled in prose

**Owner, row 21:** "הכל בסדר חוץ מ'הם הפשרה שמשאירה אותו ב-B' זה לא משפט תקני"

Two defects in one clause. The owner flagged the grammar. The second is worse and he did not
name it: **"ב-B" spells the grade in prose**, which the standing rule forbids — the grade is
the badge, never the sentence.
**Measured: 142/710 rows (20%), 184 occurrences** of grade-in-prose, INCLUDING live copy that
writes "ציון S." (bread_v3) — directly against the owner's own S-grade ruling that consumer
copy never writes "S". Worst: cheese 45, bread_v3 32, hard_cheeses 29, bread_v4 25.

---

### Sizing implied by this review
Of 21 rows read: 6 clean, 2 em-dash-only, ~4 nutrition-repetition, ~3 no-description
(full rewrite), plus padding / phrase / grammar singles. Extrapolated to 710 rows, the
sweep splits roughly into a large TOUCH tier (em-dash, grade-in-prose, antithesis,
ingredient counts — all deterministic) and a REWRITE tier of order 25–30% driven by H4-P1,
which no gate can find and only the judge or the owner can.

---

## Session H5 — OWNER ANCHOR EXAMPLE for the description overhaul · 2026-07-10 (TASK-576)

After rejecting v1/v2 (cited nutrition values) and v3 (removed numbers but recited the
profile in corpus-ranked analyst-speak), the owner gave the target line himself. This is
the calibration anchor for ALL description copy — the voice the engine must match.

**Owner's model line (גאודה מאסדם, a plain product with no ingredient data):**
> גאודה הולנדית קלאסית, עשירה ומלוחה. היא מכילה חלבון גבוה אך גם שומן גבוה. מדובר במוצר יחסית נקי אבל יש לשים לב לכמות הנצרכת.

**What this teaches (the corrections to our prior attempts):**
1. **Naming nutrient QUALITIES in plain words is CORRECT, not a violation.** "חלבון גבוה",
   "שומן גבוה" is exactly what he wants. The ban is on cited VALUES (numbers: grams/mg/%),
   never on saying a nutrient is high or low. v3's mistake was NOT "high protein" — it was
   the clunky corpus-relative form "מהגבוהים בין הגאודות המלאות בסקירה".
2. **Plain and ABSOLUTE, not corpus-ranked.** Say "high protein but also high fat" — not
   "among the highest full-goudas in the review". The description is about the FOOD, not its
   rank. Rank lives in the score, not the prose.
3. **Three beats, short:**
   - (a) IDENTITY + sensory character: "גאודה הולנדית קלאסית, עשירה ומלוחה"
   - (b) NUTRITIONAL READ in plain words: "מכילה חלבון גבוה אך גם שומן גבוה"
   - (c) PRACTICAL TAKEAWAY / the catch: "יחסית נקי אבל יש לשים לב לכמות הנצרכת"
4. It is a genuine short ANALYSIS — the algorithm understands the profile and SAYS it like a
   person would, not a spec sheet and not a ranking. Owner: "Of course I would expect the
   engine to know better." The engine is meant to produce this unaided.

This anchor + the hard nutrition_value_citation gate ([[owner_no_cited_nutritional_values]])
together define the standard: no numbers, but a plain-language nutritional read with identity
and a takeaway. Apply corpus-wide (502 rows).
