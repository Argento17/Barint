---
document: w2_additive_copy_v1
task: TASK-179U
status: CONTENT_APPROVED
created_at: 2026-06-04
content_sign_off: 2026-06-04
blocks: [TASK-179T, TASK-179V]
contested_entries_signed_2026_06_21: [E330, E300, E202, E224]
contested_note: "EV-101 + EV-102 tier updates (TASK-369, 2026-06-21) — E330/E300/E202/E224 explanations revised to contested and CONTENT-SIGNED via the two-gate process (Nutrition authoring + Adversarial QA/Red-Team PASS on round 2). Staging-ready; live only when the D4 tooltip display surfaces (separate from BARI_D4_SCORE_V1 scoring activation). E224 = firmer regulatory basis; E330/E300/E202 = LOW-confidence (2028 revert). RT-M4 display-architecture perception gap routed to Product (open, non-blocking)."
---

# W2 Additive Copy — Hebrew Consumer Explanations (Canonical)

**Purpose:** Finalized Hebrew `explanation_he` strings for all 20 Glass Box W2 additives.
TASK-179T reads this file for component strings. This is the content record for future copy maintenance.

**Input source:** `01_framework/glass_box/additive_prototype_set_v1.md` (Nutrition Phase 3 + Product Phase 4 co-signed, 2026-06-04).

**Editorial standards applied:**
- `01_framework/editorial/insight_line_spec_v1.md`
- `01_framework/editorial/row_description_standard_v1.md`
- DEC-006 alarm-framing prohibition (binding across all tiers)

**Character limit:** ≤ 120 characters per line (strict). All 20 verified.

---

## Entries (E330-order, matching additive_prototype_set_v1.md)

---

### E330 — חומצת לימון (Citric acid)
**Tier:** contested (LOW confidence)
**Explanation (final):** חומצת לימון כתוסף שימור נקשרה במחקר תצפיתי לעלייה בלחץ דם; ממצא זה אינו נוגע ללימון עצמו ומוקדם ולא שוכפל.
**Change from draft (round 1):** tier functional → contested (LOW confidence). Copy updated: (1) establishes the additive-vs-intrinsic firewall ("כתוסף שימור" / scope-restriction clause) — the concern is citric acid used as a preservative additive, NOT the acid naturally present in citrus fruit; (2) frames the signal as observational association ("נקשרה") not causation; (3) flags low confidence / unreplicated ("מוקדם ולא שוכפל"). Evidence basis: EV-101 (NutriNet-Santé cohort, EHJ 2026).
**Change from draft (round 2 — RT-M1):** replaced "האחריות אינה בלימון עצמו" (liability/blame register) with "ממצא זה אינו נוגע ללימון עצמו" (neutral scope-restriction). De-duplicated "הממצא / הממצא" — second instance replaced with "ממצא זה". Same firewall, no liability tone. Character count: 106.
**Grammar gate (round 2):** one medium-confidence FLAG dismissed — subject_verb_gender_mismatch on 'נקשרה' vs anchor 'שימור'. False positive: gate's proximity-scan picks nearest bare NOUN (שימור, Masc) not the true Fem subject (חומצת לימון). Sentence is grammatically correct Hebrew.
**Status:** CONTENT-SIGNED — both gates cleared (Nutrition authoring + Adversarial QA/Red-Team PASS, round 2, 2026-06-21, TASK-369). Staging-ready; ships only when the D4 tooltip display is surfaced.

---

### E202 — פוטסיום סורבט (Potassium sorbate)
**Tier:** contested (LOW confidence)
**Explanation (final):** פוטסיום סורבט נקשר בניתוחים תצפיתיים לעלייה בלחץ דם — הממצא מוקדם ולא שוכפל.
**Change from draft (round 1):** tier likely-neutral → contested (LOW confidence). Copy updated to observational association framing. Evidence basis: EV-102 (NutriNet-Santé cohort + supporting analyses).
**Change from draft (round 2 — RT-H1):** prior string conflated two distinct evidence tracks under one "מוקדם" caveat: (1) the NutriNet observational blood-pressure association (genuinely preliminary/LOW-conf) and (2) the EFSA-2019 reaction-by-product genotoxicity question (a separate, still-open regulatory concern, not "preliminary" in the same sense). Merging both under one framing misrepresented track 2. Fix: dropped the by-product clause ("תוצרי לוואי פוטנציאליים נבחנים") entirely. The string now presents only the observational BP association accurately framed as preliminary and unreplicated ("מוקדם ולא שוכפל"). Track 2 (genotoxicity question) is the firmer regulatory concern and is NOT suppressed — it is accurately absent from this LOW-confidence consumer line until it reaches a promotable evidence tier. Character count: 76.
**Grammar gate (round 2):** CLEAN — 0 flags.
**Status:** CONTENT-SIGNED — both gates cleared (Nutrition authoring + Adversarial QA/Red-Team PASS, round 2, 2026-06-21, TASK-369). Staging-ready; ships only when the D4 tooltip display is surfaced.

---

### E224 — סולפיטים (תרכובת לא מפורטת) — sulphite group (was Potassium metabisulphite)
**Tier:** contested
**Explanation (final):** סולפיטים עלולים לעורר אסתמא אצל רגישים ומחייבים סימון אלרגן; EFSA הסירה ב-2022 את גבול הצריכה המאושר לסולפיטים.
**CH-1 change (2026-06-22, Nutrition DEC-CH-1):** this entry detects the sulphite GROUP (generic "סולפיט" + the "מטביסולפיט" substring), so the display was relabeled from the specific compound to the group ("סולפיטים (תרכובת לא מפורטת)", display E220–E228) and the explanation generalized from "פוטסיום מטביסולפיט" to "סולפיטים". Detection/tier/score_eligible unchanged — zero score move; EFSA-2022 group ADI withdrawal + allergen basis preserved. 108 chars.
**Change from draft (round 1):** explanation revised to reflect the STRONGER, more-confident basis established by EV-102: (1) leads with the allergen / asthma trigger and mandatory-declaration fact; (2) references EFSA 2022 action on sulphite group safety. Tier remains contested but confidence footing is firmer. Evidence basis: EV-102; EFSA 2022 sulphite re-evaluation; mandatory allergen legislation (EU 1169/2011, Israeli parallel).
**Change from draft (round 2 — RT-M2):** "עדכנה את הערכת הבטיחות שלו ב-2022" (understated — "updated") replaced with "הסירה ב-2022 את גבול הצריכה המאושר לסולפיטים". The 2022 EFSA action was a WITHDRAWAL of the sulphite group ADI (moved to margin-of-exposure approach because MOE fell below the safety threshold for most groups) — "withdrawal" not merely "update". The new verb "הסירה" is accurate and proportionate; does not assert consumer harm (DEC-006 compliant), but does not under-disclose the regulatory action. This is the firmest of the four entries — the firm regulatory ground is now accurately reflected. Character count: 117. Note: "אסתמא" is the medically standard Hebrew spelling (vs "אסתמה" in round 1 — corrected for consistency with standard medical Hebrew).
**Grammar gate (round 2):** one medium-confidence FLAG dismissed — subject_verb_number_mismatch on 'ומחייב' vs anchor 'רגישים'. False positive: gate's proximity-scan picks 'רגישים' (Plur) as the nearest noun, but the true subject of ומחייב is 'פוטסיום מטביסולפיט' (Sing Masc). Sentence is grammatically correct Hebrew.
**Status:** CONTENT-SIGNED — both gates cleared (Nutrition authoring + Adversarial QA/Red-Team PASS, round 2, 2026-06-21, TASK-369). Staging-ready; ships only when the D4 tooltip display is surfaced.

---

### E300 — חומצה אסקורבית (Ascorbic acid)
**Tier:** contested (LOW confidence)
**Explanation (final):** ויטמין C כתוסף שימור נקשר במחקר תצפיתי לסיכון קרדיווסקולרי מוגבר; הממצא מוקדם ואינו נוגע לוויטמין C הטבעי בפירות.
**Change from draft (round 1):** tier functional → contested (LOW confidence). Copy established the additive-vs-intrinsic firewall ("כתוסף שימור" / "אינו נוגע לוויטמין C הטבעי בפירות"); observational framing ("נקשר"); low-confidence flag ("מוקדם"). Evidence basis: EV-101 (NutriNet-Santé cohort, EHJ 2026).
**Change from draft (round 2 — RT-M3):** "שינויים בריאות הלב" (vague, non-directional — fails the one-read test) replaced with "סיכון קרדיווסקולרי מוגבר". EV-101 identifies E300 as the one additive individually linked to elevated cardiovascular risk in the NutriNet-Santé cohort (EHJ 2026) — the finding is specifically directional (elevated risk), not merely "changes." The new phrase is directional-but-hedged: "מוגבר" (elevated) names the direction; the full string still frames this as a preliminary observational finding ("נקשר במחקר תצפיתי... הממצא מוקדם") and preserves the additive-vs-intrinsic firewall. DEC-006 compliant: "סיכון קרדיווסקולרי מוגבר" names the observed direction without asserting a disease verdict or alarm. Character count: 113.
**Grammar gate (round 2):** CLEAN — 0 flags.
**Status:** CONTENT-SIGNED — both gates cleared (Nutrition authoring + Adversarial QA/Red-Team PASS, round 2, 2026-06-21, TASK-369). Staging-ready; ships only when the D4 tooltip display is surfaced.

---

### E1422 — עמילן מעובד (Modified starch)
**Tier:** likely-neutral
**Explanation (final):** עמילן מעובד הוא עמילן שעבר עיבוד כימי לשיפור יציבות המרקם; הוא עובר עיכול כפחמימה רגילה ואינו נספג ישירות.
**Change from draft:** unchanged

---

### E282 — פרופיונט סידן (Calcium propionate)
**Tier:** likely-neutral
**Explanation (final):** פרופיונט סידן הוא חומר משמר המונע עובש בלחם; חומצה פרופיונית דומה לו מיוצרת גם על ידי חיידקי המעיים שלנו באופן טבעי.
**Change from draft:** unchanged

---

### E481 — נתרן סטארויל לקטילט (Sodium stearoyl lactylate / SSL)
**Tier:** likely-neutral
**Explanation (final):** SSL (E481) הוא מרכיב עזר באפיית לחם המסייע לבצק לתפוח ולשמור על רכות; אושר לשימוש על ידי רשויות האיחוד האירופי.
**Change from draft:** unchanged

---

### E407 — קרגינן (Carrageenan)
**Tier:** contested
**Explanation (final):** קרגינן הוא מייצב שמקורו באצות ים; קיים דיון מדעי פעיל על השפעתו על מיקרוביום המעי, אם כי האיחוד האירופי אישר שימושו.
**Change from draft:** trimmed to meet 120-char limit (179→116). Removed "חומר" before "מייצב" and "לשמירה על מרקם חלק" (functional detail recoverable from context); tightened the regulatory clause from "רשות המזון האירופית אישרה את השימוש בו ברמות הנוכחיות" to "האיחוד האירופי אישר שימושו". Both the contested signal and the regulatory counter-position are preserved.

---

### E471 — מונו ודיגליצרידים (Mono- and diglycerides of fatty acids)
**Tier:** contested
**Explanation (final):** מונו ודיגליצרידים הם מתחלבים נפוצים; קיים דיון מדעי על בטיחות השימוש בהם, אם כי האיחוד האירופי אישר שימושם.
**Change from draft:** unchanged
**Change (EV-061):** tier likely-neutral → contested. Copy revised to the active-debate + EU-approved register (modeled on E407/E466). Evidence basis: EV-061 (Sellem et al., PLoS Medicine 2024, PMID 38349899 — E471 isolated, cancer HRs 1.15/1.24/1.46; emulsifier signal, same family as E407/E466). LOW-to-moderate, single cohort, no replication → contested, not confirmed-negative.
**CH-4 change (2026-06-22, Nutrition DEC-CH-4):** "השפעתם על מיקרוביום המעי" (microbiome — the hypothesised mechanism) replaced with "בטיחות השימוש בהם לאורך זמן" (safety of use over time). EV-061's primary finding was cancer HRs, not a microbiome outcome; naming "microbiome" mischaracterised what the study measured. New phrasing is accurate to an open safety question without adjudicating mechanism. 107 chars (gate-2 M-2 fix: trimmed from a 122-char draft that exceeded the 120 limit — removed "פעיל" + "לאורך זמן"), DEC-006-compliant.

---

### E472e — DATEM
**Tier:** likely-neutral
**Explanation (final):** DATEM הוא חומר עזר לאפייה המסייע לגלוטן להתפתח ולשמור על מרקם הלחם; שמו הטכני מופיע לעתים רחוקות על תוויות לחם ישראליות.
**Change from draft:** unchanged

---

### E415 — קסנטן (Xanthan gum)
**Tier:** functional
**Explanation (final):** קסנטן הוא מייצב טבעי המופק בתסיסה חיידקית, ומשמש לשמירה על מרקם אחיד ומניעת הפרדת מים.
**Change from draft:** unchanged

---

### E450/E451 — פוספטים (Phosphates)
**Tier:** dose-dependent
**Explanation (final):** פוספטים הם מלחי זרחן המשמשים לייצוב מרקם מוצרי חלב; הצריכה המצטברת מכלל המזון ראויה לתשומת לב.
**Change from draft:** trimmed to meet 120-char limit (124→94). Removed the parenthetical "מינרל חיוני לגוף" (recoverable from context; zרחן is the plain-language anchor); tightened "מכלל מקורות המזון" to "מכלל המזון". Dose-dependent signal ("צריכה מצטברת") preserved.

---

### E440 — פקטין (Pectin)
**Tier:** functional
**Explanation (final):** פקטין הוא סיב תזונתי מסיס שמקורו בפירות הדר ותפוחים, המשמש ליצירת מרקם ג'ל טבעי ומזין חיידקי מעיים מיטיבים.
**Change from draft:** unchanged

---

### E410 — לוקוסט-בין גאם (Locust bean gum)
**Tier:** functional
**Explanation (final):** לוקוסט-בין גאם הוא מייצב טבעי שמקורו בעץ החרוב, ומשמש לשמירה על מרקם קרמי ומניעת הפרדת נוזלים.
**Change from draft:** unchanged

---

### E412 — גואר (Guar gum)
**Tier:** functional
**Explanation (final):** גואר הוא חומר מסמיך טבעי המופק מזרעי גואר, ומשמש לשמירה על עקביות מרקם המוצר.
**Change from draft:** unchanged

---

### E955 — סוכרלוז (Sucralose)
**Tier:** dose-dependent
**Explanation (final):** סוכרלוז הוא ממתיק ללא קלוריות במוצרי ללא סוכר; מאושר ברמות הנוכחיות, אך מחקר על השפעות ארוכות טווח נמשך.
**Change from draft:** trimmed to meet 120-char limit (156→104). Removed the year reference "(2026)" and the phrase "הערכה האירופית האחרונה" — the approval fact is preserved without the citation detail, which belongs in methodology text rather than the per-additive explanation line. The key information (approved at current levels, ongoing long-term research) is fully retained.

---

### E950 — אצסולפאם K (Acesulfame potassium)
**Tier:** dose-dependent
**Explanation (final):** אצסולפאם K הוא ממתיק ללא קלוריות נפוץ במוצרים ללא סוכר; מאושר ברמות הנוכחיות, ונבדק להשפעתו על מיקרוביום המעי.
**Change from draft:** trimmed to meet 120-char limit (144→110). Removed "הנמצא בעיקר" and replaced with "נפוץ"; removed quotation marks around "ללא סוכר" (consistent with E955 treatment); tightened "וממשיך להיות נבדק בהקשר להשפעתו" to "ונבדק להשפעתו". Approved status and gut microbiome research signal preserved.

---

### E466 — CMC — קרבוקסי מתיל צלולוז (Carboxymethylcellulose)
**Tier:** contested
**Explanation (final):** CMC (E466) הוא חומר מייצב שנחקר בניסוי קליני שהראה שינויים בהרכב מיקרוביום המעי; הדיון המדעי בנושא פעיל ואינו מוכרע.
**Change from draft:** unchanged

---

### E150 — צבע קרמל (Caramel color)
**Tier:** disclosure-gap
**Explanation (final):** צבע קרמל הוא צבע מאכל חום; הסוג הספציפי אינו מצוין על התווית הישראלית ולכן לא ניתן לאפיין את פרופיל הבטיחות שלו.
**Change from draft:** trimmed to meet 120-char limit (160→112). The Nutrition-revised draft ("קיימים מספר סוגים שלו בעלי פרופיל בטיחות שונה, אך הסוג...") was further compressed: the fact that multiple subtypes exist with different safety profiles is conveyed implicitly by saying we cannot characterize the safety profile due to the missing subtype. The disclosure-gap logic is fully preserved in fewer words.

---

### E211 — נתרן בנזואט (Sodium benzoate)
**Tier:** dose-dependent
**Explanation (final):** בנזואט נתרן הוא חומר משמר; בצירוף ויטמין C עשויה להיווצר בנזן בכמויות קטנות, בעיקר במשקאות — פחות רלוונטי למוצרי חלב.
**Change from draft:** trimmed to meet 120-char limit (172→117). Removed "המאושר בישראל ובאירופה" (approval is default background; the specific concern here is the benzene interaction, which is what makes this line distinctive). "ובמוצרים חומציים" removed as redundant with "במשקאות" for the purpose of the consumer line. The benzene formation mechanism and dairy context-dependency are preserved.

---

### E320 — BHA — בוטילציאניזול (Butylated hydroxyanisole)
**Tier:** contested
**Explanation (final):** BHA הוא נוגד חמצון שמונע שמנים מהתקלקלות; נושא סיווג סיכון בינלאומי מנתוני בעלי חיים; הדיון לגבי הרלוונטיות לאדם פתוח.
**Change from draft:** trimmed to meet 120-char limit (167→118). Nutrition's revision already removed the alarm-word "מסרטן" (replaced with "סווג בסולם סיכונים בינלאומי"). Content further compressed: "הוא סווג בסולם סיכונים בינלאומי על בסיס נתוני בעלי חיים" → "נושא סיווג סיכון בינלאומי מנתוני בעלי חיים"; tail clause shortened by removing "ממשיך" (implicit in "פתוח"). DEC-006 posture maintained: no alarm framing, no intent attribution, contested signal conveyed accurately.

---

## W3 addendum (TASK-181E) — 14 additional shelf additives

**Added 2026-06-04** under TASK-181E (Glass Box W3). These 14 additives surface on the displayed
shelf and were wired by TASK-181D without copy. Authored against the **same** standards and the
≤120-char limit as the original 20, keyed by E-number for Data lookup.

**Input sources:** `additive_tiered_library_v1.md` (TASK-181B tiers) + `additive_library_expanded_v1.md`
(TASK-181A evidence). No claim beyond what the tier + 181A evidence support; no invented data.

**Tooling:** each line passed the offline `hebrew_readability` leakage gate (`is_clean = True`, no
Tier-4 framework term / raw score / recommendation language) and the ≤120-char limit.

---

### E960 — סטיביול גליקוזידים (Steviol glycosides)
**Tier:** dose-dependent
**Explanation (final):** סטיביול גליקוזידים (סטיביה) הוא ממתיק ללא קלוריות שמקורו בצמח; מאושר ברמות הנהוגות, וצריכה גבוהה במיוחד ראויה לתשומת לב.
**Grounding (181A N15 + 181B #35):** plant-derived NNS; EFSA/JECFA ADI 4 mg/kg + MODERATE over-exposure flag (children as high-consumer subgroup on the sweetener axis). Dose-dependent register mirrors W2 E955/E950: "approved at current levels; the consideration is high/cumulative intake" — no alarm, no health verdict. 120 chars.

---

### E141 — תרכובות נחושת של כלורופיל (Copper complexes of chlorophylls)
**Tier:** unclassified
**Explanation (final):** תרכובות נחושת של כלורופיל הוא צבע ירוק שמקורו בכלורופיל; רשם הראיות אינו מאפשר לאפיין במדויק את פרופיל הבטיחות שלו.
**Grounding (181A N5 + 181B #25, judgment call 3):** green colourant; no clean single numerical EFSA ADI (group eval with copper-release caveat) → the one additive the evidence record does not let us cleanly classify. States the evidence record (not the label) is incomplete — neutral, not a warning; no alarm word. US/EU divergence is a D5 note, not surfaced here. 115 chars.

---

### E500 — נתרן פחמתי (Sodium carbonates)
**Tier:** functional
**Explanation (final):** נתרן פחמתי (סודה לאפייה) הוא מלח נפוץ המשמש להתפחה ולאיזון חומציות; מאושר לשימוש ברמות הנהוגות.
**Grounding (181A N13 + 181B #33):** common leavening/buffer salt; EFSA 2013 "not specified"; no dose-response concern. Sodium contribution is a nutrition-axis matter, not stated as an additive concern (no double-count). 95 chars.

---

### E163 — אנטוציאנינים (Anthocyanins)
**Tier:** functional
**Explanation (final):** אנטוציאנינים הם פיגמנט צמחי המשמש כצבע אדום-סגול, ומופק כאן מרכז גזר שחור.
**Grounding (181A N2 + 181B #22):** plant pigment / colouring food; EFSA-SCF no ADI; no concern at colour-use exposure. 74 chars.

---

### E160a — בטא קרוטן (Beta-carotene)
**Tier:** functional
**Explanation (final):** בטא קרוטן הוא פיגמנט טבעי המשמש כצבע כתום-צהוב, ומקורו זהה לזה שבגזר ובירקות כתומים.
**Grounding (181A N1 + 181B #21):** provitamin-A carotenoid; no numerical ADI for colour use; the smoker/high-dose-supplement signal is a supplement context, not food-colour use — deliberately not surfaced. 84 chars.

---

### E333 — ציטרט סידן (Calcium citrate)
**Tier:** functional
**Explanation (final):** ציטרט סידן הוא מלח סידן של חומצת לימון, המשמש לאיזון ולהעשרה בסידן; הגוף מפרק אותו לציטרט ולסידן.
**Grounding (181A N6 + 181B #26):** citrate group "not limited" / FDA §184.1195; metabolized as citrate + calcium; no dose-response concern. 97 chars.

---

### E331 — ציטרט נתרן (Sodium citrate)
**Tier:** functional
**Explanation (final):** ציטרט נתרן הוא מלח נתרן של חומצת לימון, המשמש לאיזון חומציות; הגוף מפרק אותו לציטרט.
**Grounding (181A N7 + 181B #27):** citrate group "not limited" / FDA §184.1751; metabolized as citrate. Sodium contribution is nutrition-axis, not stated here as an additive concern (judgment call 4). 84 chars.

---

### E327 — לקטט סידן (Calcium lactate)
**Tier:** functional
**Explanation (final):** לקטט סידן הוא מלח סידן של חומצת חלב, המשמש לאיזון ולהעשרה בסידן; לקטט הוא תוצר טבעי בגוף.
**Grounding (181A N8 + 181B #28):** lactate group "not limited" / FDA §184.1207; lactate is a normal metabolite; no dose-response concern. 89 chars.

---

### E270 — חומצה לקטית (Lactic acid)
**Tier:** functional
**Explanation (final):** חומצה לקטית (חומצת חלב) היא תוצר טבעי של תסיסה, המשמשת לאיזון טעם ולשימור; הגוף מכיר אותה כמטבוליט רגיל.
**Grounding (181A N10 + 181B #30):** normal fermentation metabolite; JECFA "not limited" / FDA §184.1061; no concern at food-label exposure. 104 chars.

---

### E162 — אדום סלק (Beetroot red)
**Tier:** functional
**Explanation (final):** אדום סלק הוא פיגמנט המופק מסלק ומשמש כצבע אדום טבעי.
**Grounding (181A N3 + 181B #23):** beet-derived pigment; EFSA 2015 "not specified"; no safety concern at use levels. 52 chars.

---

### E296 — חומצה מאלית (Malic acid)
**Tier:** functional
**Explanation (final):** חומצה מאלית היא חומצה טבעית הקיימת גם בתפוחים ובפירות, ומשמשת לאיזון טעם.
**Grounding (181A N9 + 181B #29):** Krebs-cycle intermediate (L-malate); JECFA "not limited" / FDA §184.1069; no dose-response concern. 73 chars.

---

### E401 — אלגינט נתרן (Sodium alginate)
**Tier:** functional
**Explanation (final):** אלגינט נתרן הוא מסמיך שמקורו באצות חומות; הוא אינו נספג כמותו ומתנהג כמו סיב מסיס.
**Grounding (181A N11 + 181B #31):** brown-seaweed polysaccharide; EFSA 2017 "not specified"; not absorbed intact, soluble-fibre-like; no dose-response concern. 82 chars.

---

### E516 — גופרת סידן (Calcium sulphate)
**Tier:** functional
**Explanation (final):** גופרת סידן (גבס) הוא מלח סידן המשמש לחיזוק מרקם וכמקור סידן, ומשמש גם להקרשת טופו.
**Grounding (181A N12 + 181B #32):** gypsum; JECFA "not limited" / FDA §184.1230; common firming/coagulant (also tofu coagulant); no dose-response concern. 82 chars.

---

### E100 — כורכומין (Curcumin)
**Tier:** functional
**Explanation (final):** כורכומין הוא פיגמנט צהוב המופק מהכורכום, ומשמש כצבע מאכל טבעי.
**Grounding (181A N4 + 181B #24, judgment call 2):** EFSA/JECFA ADI 3 mg/kg, but the documented over-exposure is via concentrated supplements, not food-colour use → functional, not dose-dependent; the supplement-channel caveat is deliberately not surfaced on the shelf line. 62 chars.

---

---

## Wave 6 addendum — bar-shelf emulsifiers (2026-06-21)

**Added 2026-06-21.** E322 (lecithin) and E476 (PGPR) were present in real ingredient text
on the snack-bar and protein-bar shelves but absent from the D4 detection library.
This addendum adds their `explanation_he` entries. Same standards and ≤120-char limit as all
prior entries. Presentation-only — no score moved.

**Evidence basis:** EFSA ADIs (E322 "not specified"; E476 ADI 25 mg/kg, 2017 re-evaluation);
JECFA "not limited" (E322) / ADI 7.5 mg/kg (E476); scoring-taxonomy classification already
live in signal_extractor.py + ingredient_taxonomy.py (emulsifier_benign / emulsifier_medium).

---

### E322 — לציטין (Lecithin)
**Tier:** functional
**Explanation (final):** לציטין הוא חומר תחליב טבעי המופק מסויה, חמניות או זרעי קנולה; זהה כימית לפוספוליפידים הטבעיים בגוף.
**Change from draft:** new entry. Character count: 87. DEC-006 verified: no alarm word, no health verdict.

---

### E476 — פוליגליצרול PGPR (Polyglycerol polyricinoleate)
**Tier:** likely-neutral
**Explanation (final):** PGPR הוא חומר תחליב סינתטי להפחתת צמיגות בשוקולד; מאושר ברמות הנוכחיות, מותר גם ברטבים מתחלבים ותחליבי שומן.
**Change from draft:** new entry. Character count: 108. DEC-006 verified: no alarm word, no health verdict. "סינתטי" is accurate, not alarmist; "מאושר" provides the regulatory counter-position.
**TASK-366 correction round 1 (2026-06-21):** removed false tail clause "אינו מוכר בשאר שימושי המזון" — E476 is permitted outside chocolate per Reg. (EC) 1333/2008 Annex II and EFSA 2017 re-evaluation (EFSA Journal 2017;15(11):5049). First replacement tail: "מותר גם בממרחים דלי-שומן ורטבים".
**TASK-366 correction round 2 (2026-06-21, RT-M1):** Red-Team gate found "ממרחים דלי-שומן" (Cat 02.2.1, margarine-type) is the more challengeable element; "emulsified sauces" (Cat 12.6) and "fat emulsions" (Cat 02.2.2) are the better-documented non-chocolate permitted uses per the same Annex II. Tail revised to: "ברטבים מתחלבים ותחליבי שומן" — maps directly to Cat 12.6 + Cat 02.2.2; removes the challenged Cat 02.2.1 reference. Source: Reg. (EC) 1333/2008 Annex II; EFSA Journal 2017;15(11):5049. Content sign-off: APPROVED (Nutrition Agent, 2026-06-21). Pending independent Red-Team gate before category go-live.

### E414 — גומי ערבי (Acacia gum / gum arabic)
**Tier:** functional
**Explanation (final):** גומי ערבי הוא סיב טבעי מעץ השיטה המשמש לייצוב ולהסמכה; נחשב בטוח ונפוץ במזון.
**Change from draft:** new entry (chocolate scrape surfaced acacia gum in a Klik countline). DEC-006 verified: no alarm word, no health verdict; benign natural hydrocolloid stated plainly.

---

### E420 — סורביטול (Sorbitol) — **Wave-6 entry, TASK-366 round 3 (2026-06-21)**
**Tier:** functional
**Explanation (final — canonical tail, applies to all occurrences):** [prefix varies by product] + "נחשב בטוח ברמות הנהוגות; בכמות גדולה עלול להשפיע על מערכת העיכול."
**Full canonical string (long-prefix variant):** אלכוהול סוכר שומר לחות ומשמש כממס לתמציות; נחשב בטוח ברמות הנהוגות; בכמות גדולה עלול להשפיע על מערכת העיכול.
**Change from draft:** replaced "נחשב בטוח לחלוטין." (overclaim) with a dose-qualified tail. "לחלוטין" was unsupportable: sorbitol and other polyols (incl. glycerol E422) have dose-dependent osmotic/laxative effects; EU Reg. 1333/2008 and Dir. 94/35/EC require a "may have a laxative effect" advisory on foods containing polyols above 10 g per portion. The new tail is factual and proportionate — no alarm word, not alarmist. DEC-006 verified.
**Character count (long-prefix):** 108. **Short-prefix variant:** 83 chars. Both within 120-char limit.
**Evidence / source:** EFSA re-evaluation of sorbitol (E420) as food additive, EFSA Journal 2015;13(3):4037; EU Regulation (EC) No 1333/2008 Annex II polyol threshold; Directive 94/35/EC (sweeteners, laxative advisory). Applies equally to E422 (glycerol) which shares the polyol class and the same dose-effect profile.
**Scope of change:** cakes_hard_cookies_frontend_v1.json (35 occurrences, 2 prefix variants), cookies_coffee_frontend_v2.json (1 occurrence, E422 — same overclaim, same fix). No score moved. Presentation only.

---

## Wave 7 addendum — D4 display reconciliation (2026-06-22)

**Added 2026-06-22.** Seven additives surfaced on displayed shelves during the D4 display
reconciliation that lacked `explanation_he` tooltip strings: the EV-059 emulsifier/colour set
(E433, E124, E122, E129, E171), plus E392 (rosemary extract, EV-102) and E575 (GDL).
Authored against the **same** standards and the ≤120-char limit as all prior entries.
Presentation-only — no score moved. Tier values are authoritative from `additive_tiered_library_v1.md`
(E433/E124/E122/E129/E171 = §7.1 EV-059; E392/E575 = §10.3 EV-102 / §2.B #34).
**GATE-2 CLEARED (Adversarial-QA / Red-Team, 2026-06-22, CH-3):** all 7 assessed DEFENSIBLE —
DEC-006 clean, ≤120c, citations accurate (E171 EFSA-2021/EU-2022 ban; azo E124/E122/E129 EU
child-activity warning label; E433 emulsifier-microbiome RCT; E392 rosemary; E575 GDL),
proportional contested framing. Both gates now cleared.

**DEC-006 verified across all 7:** no alarm word (מסוכן/רעיל/נזק/מסרטן/מזיק/מסתיר/הוסתר); contested
entries framed as active scientific debate or regulatory-status fact, never proven harm; every
regulatory action paired with its counter-position.

---

### E433 — פוליסורבאט 80 (Polysorbate 80)
**Tier:** contested
**Explanation (final):** פוליסורבאט 80 הוא מתחלב סינתטי; קיים דיון מדעי פעיל על השפעתו על מיקרוביום המעי, אם כי האיחוד האירופי אישר שימושו.
**Grounding:** `additive_tiered_library_v1.md` §7.1 EV-059 #37 — Chassaing 2021 pre-registered RCT (n=32) + animal models, microbiome dysbiosis at food-achievable concentrations; EFSA "not specified" ADI predates evidence; named alongside CMC/E466 in same mechanistic pathway. Framed parallel to the E466 entry (active debate + EU-approved counter-position). Character count: 114.

---

### E124 — פונסו 4R (Ponceau 4R)
**Tier:** contested
**Explanation (final):** פונסו 4R הוא צבע אדום סינתטי (אזו); באיחוד האירופי נדרש סימון מחייב על השפעה אפשרית על קשב ופעילות אצל ילדים.
**Grounding:** `additive_tiered_library_v1.md` §7.1 EV-059 #43 — Southampton Mixes A+B (McCann 2007); EU Art. 24 mandatory warning re: effect on children's activity/attention (Reg 1333/2008). "אפשרית" preserves the regulatory-precaution (not proven-harm) register; EFSA/FDA split implicit in "באיחוד האירופי". Character count: 109.

---

### E122 — קרמואיזין (Carmoisine / Azorubine)
**Tier:** contested
**Explanation (final):** קרמואיזין הוא צבע אדום סינתטי (אזו); באיחוד האירופי נדרש סימון מחייב על השפעה אפשרית על קשב ופעילות אצל ילדים.
**Grounding:** `additive_tiered_library_v1.md` §7.1 EV-059 #42 — Southampton Mix A; EU Art. 24 mandatory warning; same EFSA/FDA split as E102. Same proportional framing as the E124 line. Character count: 110.

---

### E129 — אדום אלורה (Allura Red AC)
**Tier:** contested
**Explanation (final):** אדום אלורה הוא צבע אדום סינתטי (אזו); באיחוד האירופי נדרש סימון מחייב על השפעה אפשרית על קשב ופעילות אצל ילדים.
**Grounding:** `additive_tiered_library_v1.md` §7.1 EV-059 #44 — Southampton Mix B; EU Art. 24 mandatory warning; same EFSA/FDA split as E102. Same proportional framing as the E124 line. Character count: 111.

---

### E171 — טיטניום דיוקסיד (Titanium dioxide)
**Tier:** contested
**Explanation (final):** טיטניום דיוקסיד הוא צבע לבן; האיחוד האירופי אסר אותו ב-2022 לאחר ש-EFSA לא שללה חשש גנוטוקסי; ארה"ב וקנדה עדיין מתירות.
**Grounding:** `additive_tiered_library_v1.md` §7.1 EV-059 #39 — EFSA 2021 could not rule out genotoxicity, no safe ADI establishable → EU ban (Aug 2022); FDA/Health Canada/FSANZ maintained authorization (genuine regulatory schism). The line states the regulatory split factually — the EU action and the non-EU permission side by side — with no alarm word; "לא שללה חשש" mirrors EFSA's own could-not-rule-out language. Character count: 119.

---

### E392 — תמציות רוזמרין (Rosemary extract)
**Tier:** likely-neutral
**Explanation (final):** תמציות רוזמרין הן נוגד חמצון טבעי ממשפחת הפוליפנולים, המשמש לשמירה על רעננות; אושר לשימוש על ידי רשויות האיחוד האירופי.
**Grounding:** `additive_tiered_library_v1.md` §10.3 EV-102 #51 — natural polyphenol antioxidant; EFSA 2008/2018 benign, ADI 0.3 mg/kg, exposures 100–3000× below. Tier is `likely-neutral` (the EHJ naming carries a forward reassess flag but does NOT clear the contested bar — paradoxical directionality + clean independent safety record), so the line is stated plainly as benign; the open EHJ reassess flag is library-internal and not surfaced. Character count: 119.

---

### E575 — גלוקונו דלתא לקטון (Glucono-delta-lactone / GDL)
**Tier:** functional
**Explanation (final):** גלוקונו דלתא לקטון הוא מחמיץ ומקריש המתפרק בגוף לחומצה גלוקונית, מטבוליט רגיל; אין חשש תלוי-מינון ברמות הנהוגות.
**Grounding:** `additive_tiered_library_v1.md` §2.B #34 — hydrolyzes to gluconic acid (normal metabolite); JECFA "not limited" + FDA §184.1318; no dose-response concern. Stated plainly as benign acidulant/coagulant. Character count: 112.

### E414 — גומי ערבי (Acacia gum / gum arabic)
**Tier:** functional
**Explanation (final):** גומי ערבי הוא סיב טבעי מעץ השיטה המשמש לייצוב ולהסמכה; נחשב בטוח ונפוץ במזון.
**Change from draft:** new entry (chocolate scrape surfaced acacia gum in a Klik countline). DEC-006 verified: no alarm word, no health verdict; benign natural hydrocolloid stated plainly.

---

## W3 addendum sign-off (TASK-181E)

- All 14 lines authored against the same standards as the original 20 (insight_line_spec + row_description_standard + DEC-006 alarm-framing prohibition).
- DEC-006 verified: no forbidden words ("מסוכן", "מזיק", "רעיל", "מסרטן", "מסתיר", "הוסתר") and no recommendation language (מומלץ / בריא יותר / כדאי לקנות) in any line.
- No manufacturer intent attribution; no health verdict; no medical claim.
- Character limit ≤120: verified across all 14 (max = E960 at 120, E141 at 115).
- Offline `hebrew_readability` gate: all 14 `is_clean = True`, zero flags, readability 95–100.
- No-invent: every line traces to 181A evidence + the 181B tier; the two weighted-chip lines (E960 dose-dependent, E141 unclassified) carry their tier register honestly without alarm.
- Copy only — no score, JSON, or engine touched. Data re-wire (re-run the 181D wire by E-number lookup) is the remaining step to land these in the pilot JSONs.
- Content-agent: APPROVED 2026-06-04.

---

## Content sign-off

- All 20 lines reviewed against Bari editorial standards (insight_line_spec + row_description_standard).
- DEC-006 alarm-framing prohibition: verified across all 20 entries. No forbidden words ("מסוכן," "מזיק," "רעיל," "מסרטן," "מסתיר," "הוסתר") in any final line.
- No manufacturer intent attribution in any line: verified.
- Character limit (≤ 120 chars): verified across all 20 entries. Highest count: E472e at 120 chars (exact limit).
- 12 lines unchanged from Nutrition draft; 8 lines revised (E300, E407, E450, E955, E950, E150, E211, E320) — all revisions were character-limit trims, with no substantive information removed.
- Content-agent: APPROVED 2026-06-04.
