// Magnesium golden guide — /madrichim/magnesium (TASK-504B Wave 1; TASK-504C threshold
// infographic + hero mascot add-on; TASK-575 v2 REBUILD — descriptive 4-group model,
// gate-1 DRAFT copy pending gate-2).
//
// TASK-575 status: this is a GATE-1 DRAFT wire-through. Every consumer Hebrew string
// below is ported VERBATIM from
// C:\Bari\02_products\supplements\magnesium\mag_guide_v2_copy_package.md (Content
// Agent, gate-1) — nothing here is Frontend-authored. Structure (group model, gauge
// geometry, classifier badges, source links) follows
// C:\Bari\02_products\supplements\magnesium\mag_guide_v2_nutrition_spec.md §1-§9
// (Nutrition D6, Product D7 CONDITIONAL GO). gate-2 (Adversarial QA / Red-Team) has
// NOT run against this v2 copy — the page stays `noindex` (see page.tsx) until it does.
//
// Ground truth (used EXACTLY, nothing invented):
//   1. Copy — mag_guide_v2_copy_package.md, Slots 1-9. Every Hebrew string that is not
//      a structural label (heading key names, testids) is ported verbatim.
//   2. Bar-states — UNCHANGED from the prior (TASK-504) build. This task's copy
//      package + nutrition spec explicitly do NOT touch bar-state computation
//      (nutrition spec §0: "does not touch... bucket_logic... bar-threshold RUBRIC").
//      Only `bucket` (group) ASSIGNMENT and presentation change — see the group
//      precedence-rule mapping table, nutrition spec §2.
//   3. Grouping — nutrition spec §2's 18-row mapping table + precedence rule (a
//      known form/safety concern outranks a dose-only concern, which outranks a
//      label-insufficiency concern; default = meets all 4 assessed criteria). Result:
//      group (a) 0/18, group (b) 5/18, group (c) 12/18, group (d) 1/18.
//   4. Product identity (name/brand/imageUrl) — bari-web/src/lib/comparisons/
//      magnesium-page-data.ts, id/name/brand/imageUrl fields ONLY (unchanged, off-limits
//      to this task — its score/grade/insightLine/rowVerdict/expansion text are still
//      NOT used here).
//   5. Threshold-gauge/ladder geometry — the dose gauge is REBUILT per nutrition spec
//      §3 (neutral corpus-range presentation, no 300mg pass/fail zone); the safety
//      gauge and both ladders are UNCHANGED. Per-product doseMg/formHe are UNCHANGED
//      (still the same mechanically-sourced numbers/words as the prior build).
//
// Per-bar threshold placement (GuideThresholdPlacement) is product-vs-EXTERNAL-STANDARD
// only, never product-vs-field ranking (plan red-team RT-A3 / this task's guard).
//
// Pricing is null for all 18 (zero price data collected for magnesium — a
// data-completeness gap, not a product fact, per copy package Slot 3). buyUrl is null
// for all 18 (no retailer links collected yet) — GuideBuyButton already renders the
// dormant state for null.

import {
  GUIDE_BAR_ORDER,
  type GuideBarKey,
  type GuideBarState,
  type GuideBucket,
  type GuideGaugeGeometry,
  type GuideLadderGeometry,
  type GuideBarResult,
  type GuideCardVisibleFacts,
  type GuidePageVM,
  type GuideProductVM,
  type GuideV3Group,
} from "@/lib/view-models";
import { BAR_STATE_LABELS_HE } from "@/components/shared/bar-state-badge";
import { tierIndexFromState } from "@/components/guides/threshold-bar-row";
import { computeSuppressedBars } from "@/lib/guides/guide-suppression";
import { magnesiumProducts } from "@/lib/comparisons/magnesium-page-data";
import {
  MAG_V3_INTRO_HE,
  MAG_V3_WHAT_WE_FOUND_HE,
  MAG_V3_GROUP_LABELS_HE,
  MAG_V3_HOW_TO_READ_HE,
  MAG_V3_ONE_LINER_BY_BARCODE,
  MAG_V3_MARKET_GAPS_COMPACT_HE,
  MAG_V3_COLLAPSED_SECTION_TITLE_HE,
  MAG_V3_EXPANDER_LABELS_HE,
} from "@/lib/guides/magnesium-guide-copy-v3";

// ─── Product identity lookup (name/brand/imageUrl only — see header) ───────────────
function identity(id: string) {
  const p = magnesiumProducts.find((x) => x.id === id);
  if (!p) {
    throw new Error(`magnesium-guide-data: product id ${id} not found in magnesium-page-data.ts`);
  }
  return { id: p.id, name: p.name, brand: p.brand ?? null, imageUrl: p.imageUrl };
}

// Shorthand: build the 6 bars in GUIDE_BAR_ORDER from a compact state tuple.
function bars(
  d: GuideBarState,
  f: GuideBarState,
  t: GuideBarState,
  p: GuideBarState,
  s: GuideBarState,
  l: GuideBarState
) {
  const byKey: Record<GuideBarKey, GuideBarState> = {
    doseAdequacy: d,
    formAbsorption: f,
    thirdPartyVerification: t,
    priceFairness: p,
    safety: s,
    labelTransparency: l,
  };
  return GUIDE_BAR_ORDER.map((bar): GuideBarResult => ({ bar, state: byKey[bar] }));
}

// ─── Threshold geometry (TASK-504C spec §2/§3) — ONE object per bar, shared by every
// product row for that bar (the standard is a fact independent of any one product). ──
//
// TASK-575 (magnesium guide v2, nutrition spec §3 "gauge geometry — replacing the
// '300 (הסף)' tick") — REBUILT. The old geometry encoded the killed universal
// effective-dose floor (300mg) directly into pass/flag/fail zone colors; that framing
// is deleted, not softened (nutrition spec §3 kill instruction). Replacement is a
// NEUTRAL corpus-range presentation: one flat, un-toned zone spanning the reviewed
// range (76–520 mg, the actual observed min/max — domainMax is now the real corpus
// max, not a threshold+headroom value, so no product clamps/overflows), a plain
// reference tick at the median (190 mg, Product-Agent-corrected), and a separately
// labeled RDA all-sources context band (310–420 mg) that is NEVER rendered with
// zone-tone coloring (spec: "must never be rendered as 'your supplement should give
// you 310-420 mg'"). The min/max tick labels are bare numbers only (no explanatory
// Hebrew appended) — the copy package supplies exact wording only for the median tick
// and the mandatory RDA qualifier; nothing else is authored here.
const MAGNESIUM_DOSE_GAUGE: GuideGaugeGeometry = {
  anatomy: "gauge",
  domainMax: 520,
  hideZeroTick: true,
  zones: [
    // TWO zones, SAME neutral tone ("cannot_verify" — the system's only tone with no
    // pass/fail/flag connotation, spec: no zone tied to 300) — the split at 76 exists
    // only to give the corpus minimum a real visual boundary + short tick label ("76"),
    // not a color change. The corpus maximum (520) is the domain edge itself, labeled
    // via `maxTickLabel` below (fix: a first-pass version tried to render the median's
    // long sentence inline in this same short numeric row, which visually collided
    // with the "76" label — caught in this task's own screenshot verification and
    // moved to a below-track reference line + caption instead, see threshold-bar-row.tsx).
    { upTo: 76, tone: "cannot_verify", dividerStyle: "dashed", tickLabel: "76" },
    { upTo: 520, tone: "cannot_verify", dividerStyle: "solid" },
  ],
  maxTickLabel: "520",
  referenceTicks: [
    // Copy package Slot 9 gauge tick label — verbatim. Renders as a dashed reference
    // line + its own below-track caption line (never inline in the numeric tick row).
    { at: 190, label: "חציון בין 15 מוצרים עם מינון ברור" },
  ],
  contextBand: {
    from: 310,
    to: 420,
    label: "310–420",
    // Copy package Slot 9 — mandatory qualifier, verbatim, must render wherever the
    // band renders.
    qualifierLabel: "מכל המקורות יחד — לא רק תוסף",
  },
};

const MAGNESIUM_SAFETY_GAUGE: GuideGaugeGeometry = {
  anatomy: "gauge",
  // 350mg UL + headroom (spec §2) — same overflow rule as the dose gauge.
  domainMax: 400,
  zones: [
    // EFSA soft GI-tolerance caution line — advisory, dashed divider (spec §2).
    { upTo: 250, tone: "pass", dividerStyle: "dashed", tickLabel: "250" },
    // NIH/IOM hard UL veto line — solid divider (spec §2).
    { upTo: 350, tone: "flag", dividerStyle: "solid", tickLabel: "350" },
    { upTo: 400, tone: "fail", dividerStyle: "solid" },
  ],
};

// Tier order worst→best (index 0 = LOW/FAIL tone ... index 2 = HIGH/PASS tone) —
// matches tierIndexFromState's fail=0/flag=1/pass=2 mapping exactly, since the rubric
// defines this bar's STATE as its tier (not a separately-invented ranking).
// Design spec v2 §1.2 unifies this bar onto the same thin zoned-gauge anatomy as
// dose/safety, which has no room for the old per-tier chemical-name sublabel list —
// that mapping still lives verbatim in this guide's own educationSpine
// "הצורות הכימיות, מוסבר שוב בקצרה" section below (spec v2 §1.2 "content gap" note;
// not stranded, just relocated to its natural static-reference home).
const MAGNESIUM_FORM_LADDER: GuideLadderGeometry = {
  anatomy: "ladder",
  tiers: [
    { label: "נמוכה", tone: "fail" },
    { label: "בינונית", tone: "flag" },
    { label: "גבוהה", tone: "pass" },
  ],
};

const MAGNESIUM_TRANSPARENCY_LADDER: GuideLadderGeometry = {
  anatomy: "ladder",
  tiers: [
    { label: "לא גלוי כלל", tone: "fail" },
    { label: "חלקי", tone: "flag" },
    { label: "גלוי במלואו", tone: "pass" },
  ],
};

// TASK-575 gate-2 HIGH-1 ruling (nutrition spec §11, copy package Slot 11.1) — the
// SAME generic tooltip/expansion sentence for all 8 `evidence_limited` formAbsorption
// rows (#2, #4, #5, #6, #7, #8, #10, #15). Verbatim.
const EVIDENCE_LIMITED_FORM_NOTE_HE =
  "הצורה הכימית ידועה ומצוינת על התווית. הראיות לדירוג הספיגה שלה בביטחון, מול ציטראט, מוגבלות מדי כרגע.";

function ladderValueLabel(geometry: GuideLadderGeometry, tierIndex: number | null): string {
  if (tierIndex === null) return BAR_STATE_LABELS_HE.cannot_verify;
  return geometry.tiers[tierIndex].label;
}

// ─── Per-product builder ─────────────────────────────────────────────────────────────
// Computes `bars` once and derives `benchmarks` (the 4 discriminating-bar placements)
// MECHANICALLY from it — never a second, independently-typed source of truth for the
// same fact. `doseMg`/`doseValueLabel` are the SAME number/string already used for this
// product elsewhere in Bari's copy (nothing new); `formHe` is the SAME chemical-form
// word already named in the product's oneLinerHe below (null only for the two
// undisclosed-ratio blends, where form_absorption is itself cannot_verify).
function buildProduct(opts: {
  barcode: string;
  bucket: GuideBucket;
  isDefaultPick?: boolean;
  /** [doseAdequacy, formAbsorption, thirdPartyVerification, priceFairness, safety, labelTransparency] */
  states: [GuideBarState, GuideBarState, GuideBarState, GuideBarState, GuideBarState, GuideBarState];
  doseMg: number | null;
  doseValueLabel: string;
  formHe: string | null;
  oneLinerHe: string;
  /** TASK-575 (magnesium guide v2, copy package Slot 6) — per-row severity classifier,
   *  group-(c)/"fails" bucket only. Verbatim, optional. */
  classifierHe?: string;
  /** TASK-575 gate-2 HIGH-1 ruling (nutrition spec §11, copy package Slot 11.1's
   *  "longer tooltip/expansion variant") — the SAME generic sentence for all 8
   *  `evidence_limited` formAbsorption rows, rendered as `GuideBarResult.note` (the
   *  per-row expander's bar-detail caption, "· {note}"). Verbatim, optional. */
  formNote?: string;
}): GuideProductVM {
  const barsResult = bars(...opts.states);
  if (opts.formNote) {
    const formEntry = barsResult.find((b) => b.bar === "formAbsorption");
    if (formEntry) formEntry.note = opts.formNote;
  }
  const byKey = new Map(barsResult.map((b) => [b.bar, b] as const));
  const formTier = tierIndexFromState(byKey.get("formAbsorption")!.state);
  const transparencyTier = tierIndexFromState(byKey.get("labelTransparency")!.state);

  return {
    ...identity(opts.barcode),
    bucket: opts.bucket,
    isDefaultPick: opts.isDefaultPick ?? false,
    bars: barsResult,
    benchmarks: {
      doseAdequacy: {
        value: opts.doseMg,
        clamped: opts.doseMg !== null && opts.doseMg > MAGNESIUM_DOSE_GAUGE.domainMax,
        valueLabel: opts.doseValueLabel,
      },
      safety: {
        value: opts.doseMg,
        clamped: opts.doseMg !== null && opts.doseMg > MAGNESIUM_SAFETY_GAUGE.domainMax,
        valueLabel: opts.doseValueLabel,
      },
      formAbsorption: {
        tierIndex: formTier,
        valueLabel: opts.formHe ?? BAR_STATE_LABELS_HE.cannot_verify,
      },
      labelTransparency: {
        tierIndex: transparencyTier,
        valueLabel: ladderValueLabel(MAGNESIUM_TRANSPARENCY_LADDER, transparencyTier),
      },
    },
    pricing: null,
    buyUrl: null,
    oneLinerHe: opts.oneLinerHe,
    classifierHe: opts.classifierHe ?? null,
  };
}

// TASK-575 (magnesium guide v2) — the FOUR bucket constants are reused verbatim
// (GuideBucket's 4 enum values are unchanged — grep-verified: only this guide's own
// data/component files consume them, see the guide-product-table.tsx header comment),
// but their MEANING for this guide is now the nutrition-spec §2 descriptive-group
// model, not the retired ranked-tier model:
//   GROUP_A (clears_all)        — meets all 4 assessed criteria (0/18)
//   GROUP_B (passes_with_flag)  — lower elemental amount only, nothing else wrong (5/18)
//   GROUP_C (fails)             — form/tolerance concern (a KNOWN problem, ranked above
//                                 a dose-only concern per spec §2's precedence rule) (12/18)
//   GROUP_D (cannot_assess)     — label itself insufficient to know what's delivered (1/18)
// `states` tuples (bar-state computation) are UNCHANGED from the prior build — this
// task governs grouping/copy/gauge presentation only, never bar-state computation
// (nutrition spec §0: "does not touch... bucket_logic... bar-threshold RUBRIC").
// _GROUP_A: declared for parity/documentation with the other 3 group constants below
// (group (a) is genuinely 0/18 for this corpus, per spec §2 — it is never assigned to
// a product, by design, not an oversight).
const _GROUP_A: GuideBucket = "clears_all";
const GROUP_B: GuideBucket = "passes_with_flag";
const GROUP_C: GuideBucket = "fails";
const GROUP_D: GuideBucket = "cannot_assess";

const products: GuideProductVM[] = [
  // 1 — Supherb Citrate+B6 (250mg citrate) — Group (c), tolerance-note only
  buildProduct({
    barcode: "7290013464248",
    bucket: GROUP_C,
    states: ["flag", "pass", "cannot_verify", "cannot_verify", "flag", "pass"],
    doseMg: 250,
    doseValueLabel: '250 מ"ג',
    formHe: "ציטראט",
    classifierHe: "צורה נקייה, הערת סבילות בלבד",
    oneLinerHe:
      'מגנזיום ציטראט+B6, סופהרב נותן 250 מ"ג מגנזיום יסודי במנה היומית המצוינת על התווית, בצורת ציטראט: אחת הצורות שה-NIH ODS מונה במפורש כבעלות ספיגה טובה יותר מאוקסיד. הצורה והתיוג נקיים. המינון נמצא בדיוק בגובה סף 250 מ"ג ליום שמעליו EFSA ממליצה על תשומת לב לאי-נוחות עיכולית אפשרית.',
  }),
  // 2 — Altman Bisglycinate (250mg bisglycinate) — Group (c), tolerance-note only.
  // formAbsorption evidence_limited per TASK-575 gate-2 §11 ruling (was pass) — group
  // membership UNCHANGED (driven by safety=flag, never by form; §11 "do NOT change").
  buildProduct({
    barcode: "7290019444480",
    bucket: GROUP_C,
    states: ["flag", "evidence_limited", "cannot_verify", "cannot_verify", "flag", "pass"],
    doseMg: 250,
    doseValueLabel: '250 מ"ג',
    formHe: "ביסגליצינט",
    classifierHe: "צורה נקייה, הערת סבילות בלבד",
    formNote: EVIDENCE_LIMITED_FORM_NOTE_HE,
    oneLinerHe:
      'מגנזיום ביסגליצינט, אלטמן נותן אותו מינון: 250 מ"ג מגנזיום יסודי במנה היומית, בצורת ביסגליצינט. הצורה והתיוג נקיים כאן גם, והמינון נמצא באותו סף 250 מ"ג לתשומת לב עיכולית. ביסגליצינט נחשב בפועל צורה בעלת ספיגה טובה, אבל ה-NIH ODS לא מזכיר אותה בשמה בכלל, וההוכחה הישירה חלשה מכדי לדרג את הספיגה שלה בביטחון לצד ציטראט.',
  }),
  // 3 — Altman Citrate 120 (200mg citrate) — Group (b)
  buildProduct({
    barcode: "7290011899967",
    bucket: GROUP_B,
    states: ["flag", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 200,
    doseValueLabel: '200 מ"ג',
    formHe: "ציטראט",
    oneLinerHe:
      'מגנזיום ציטראט 120, אלטמן נותן 200 מ"ג מגנזיום יסודי במנה היומית, בצורת ציטראט. הצורה, הבטיחות והתיוג נקיים לגמרי. 200 מ"ג נמצא מעל החציון של 15 המוצרים עם מינון יסודי ברור (190 מ"ג), אך עדיין בחצי הנמוך של הטווח המלא (76 עד 520 מ"ג).',
  }),
  // 4 — Nutricare WELL (168mg bisglycinate) — Group (b). formAbsorption evidence_limited
  // per TASK-575 gate-2 §11 ruling (was pass) — group membership UNCHANGED (was already
  // dose-driven, never form-driven). No classifierHe (Slot 6/11.3: extension scoped to
  // the 4 MOVED rows only, not the 3 original Group-(b) bisglycinate rows).
  buildProduct({
    barcode: "7290018439043",
    bucket: GROUP_B,
    states: ["flag", "evidence_limited", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 168,
    doseValueLabel: '168 מ"ג',
    formHe: "ביסגליצינט",
    formNote: EVIDENCE_LIMITED_FORM_NOTE_HE,
    oneLinerHe:
      'מגנזיום WELL, נוטריקר נותן 168 מ"ג מגנזיום יסודי במנה היומית, בצורת ביסגליצינט: צורה שנחשבת בפועל בעלת ספיגה טובה, אבל ההוכחה הישירה לכך מוגבלת מכדי לדרג אותה בביטחון לצד ציטראט. הבטיחות והתיוג נקיים. 168 מ"ג נמצא מתחת לחציון של 15 המוצרים עם מינון יסודי ברור (190 מ"ג), באמצע-התחתון של הטווח המלא.',
  }),
  // 5 — NT L.C. Anti Leg Cramps (190mg hydroxide) — Group (b) (MOVED from Group (c)
  // per TASK-575 gate-2 §11 ruling: formAbsorption FLAG→evidence_limited, which is
  // neutral for §2 grouping purposes, so this row falls through Tier 1 to its own
  // determinate dose finding → Group (b)).
  buildProduct({
    barcode: "7290010207640",
    bucket: GROUP_B,
    states: ["flag", "evidence_limited", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 190,
    doseValueLabel: '190 מ"ג',
    formHe: "הידרוקסיד",
    classifierHe: "צורה ידועה, ראיות מוגבלות לדירוג",
    formNote: EVIDENCE_LIMITED_FORM_NOTE_HE,
    oneLinerHe:
      'אנטי לג קרמפס, NT L.C. נותן 190 מ"ג מגנזיום יסודי במנה היומית, בדיוק בחציון של 15 המוצרים עם מינון יסודי ברור, בצורת הידרוקסיד. הבטיחות והתיוג נקיים. הצורה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות. שם המוצר מתמקד בעוויתות שרירים: סקירת קוקריין משנת 2020 (Garrison et al., PMID 32956536) בדקה בדיוק את זה אצל מבוגרים עם עוויתות שרירים רגילות (שאינן קשורות להריון או לפעילות גופנית). הסקירה לא מצאה תמיכה קלינית משמעותית למגנזיום כתוסף מונע באוכלוסייה הזו.',
  }),
  // 6 — Full-Mag Hadas (122mg bisglycinate) — Group (b), the "600" correction.
  // formAbsorption evidence_limited per TASK-575 gate-2 §11 ruling (was pass) — group
  // membership UNCHANGED (was already dose-driven). No classifierHe (11.3 scope).
  buildProduct({
    barcode: "7290001943700",
    bucket: GROUP_B,
    states: ["fail", "evidence_limited", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 122,
    doseValueLabel: '122 מ"ג',
    formHe: "ביסגליצינט",
    formNote: EVIDENCE_LIMITED_FORM_NOTE_HE,
    oneLinerHe:
      'ביסגליצינט 600 כמוסות, פול-מג הדס נותן 122 מ"ג מגנזיום יסודי במנה היומית, בצורת ביסגליצינט: אותה צורה שנחשבת בפועל טובה לספיגה, אך ההוכחה הישירה לכך מוגבלת מכדי לדרג אותה בביטחון. ה-600 בשם המוצר הוא מספר הכמוסות באריזה בלבד. זה אינו מיליגרם מגנזיום, וזה מצוין בבירור על התווית. הצורה, הבטיחות והתיוג נקיים. 122 מ"ג נמצא ברבע התחתון של הטווח שנבדק (76 עד 520 מ"ג).',
  }),
  // 7 — Tink Malate (136mg malate) — Group (b) (MOVED from Group (c) per TASK-575
  // gate-2 §11 ruling — same fall-through-to-dose logic as #5).
  buildProduct({
    barcode: "7290015318532",
    bucket: GROUP_B,
    states: ["fail", "evidence_limited", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 136,
    doseValueLabel: '136 מ"ג',
    formHe: "מלאט",
    classifierHe: "צורה ידועה, ראיות מוגבלות לדירוג",
    formNote: EVIDENCE_LIMITED_FORM_NOTE_HE,
    oneLinerHe:
      'מגנזיום מלאט, טינק נותן 136 מ"ג מגנזיום יסודי במנה היומית, בצורת מלאט. הבטיחות והתיוג נקיים; 136 מ"ג נמצא בחלק התחתון של הטווח שנבדק (76 עד 520 מ"ג). הצורה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות.',
  }),
  // 8 — Nutricare Malate (~135mg malate) — Group (b) (MOVED from Group (c) per
  // TASK-575 gate-2 §11 ruling). Note: label-transparency FLAG (700mg compound mass,
  // no elemental conversion) stays a real, separate, unaffected finding.
  buildProduct({
    barcode: "7290001066973",
    bucket: GROUP_B,
    states: ["fail", "evidence_limited", "cannot_verify", "cannot_verify", "pass", "flag"],
    doseMg: 135,
    doseValueLabel: 'כ-135 מ"ג',
    formHe: "מלאט",
    classifierHe: "צורה ידועה, ראיות מוגבלות לדירוג; פער תיוג נוסף",
    formNote: EVIDENCE_LIMITED_FORM_NOTE_HE,
    oneLinerHe:
      'מגנזיום מלאט, נוטריקר נותן כ-135 מ"ג מגנזיום יסודי במנה היומית, גם הוא בצורת מלאט. הבטיחות תקינה. יש כאן גם פער תיוג: האריזה מציינת רק את משקל התרכובת (700 מ"ג מלאט), בלי לחשב את הכמות היסודית בעצמה. הצורה עצמה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות, כמו אצל מוצר המלאט הקודם.',
  }),
  // 9 — Solgar Ca+Mg+D3 (100mg oxide+citrate blend) — Group (b), dominant reason
  buildProduct({
    barcode: "0033984005181",
    bucket: GROUP_B,
    states: ["fail", "cannot_verify", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 100,
    doseValueLabel: '100 מ"ג',
    formHe: null, // undisclosed-ratio blend (oxide+citrate) — form_absorption is cannot_verify (blend_rule)
    oneLinerHe:
      'סידן ומגנזיום +D3, סולגר נותן 100 מ"ג מגנזיום יסודי במנה היומית, מספר שכן מצוין בבירור על התווית. 100 מ"ג נמצא בחלק התחתון של הטווח שנבדק. הצורה היא תערובת אוקסיד וציטראט ביחס שלא מפורסם, כך שאי אפשר לדרג את הספיגה של התערובת הספציפית הזו בנפרד.',
  }),
  // 10 — Nutricare Taurate (76mg taurate) — Group (b) (MOVED from Group (c) per
  // TASK-575 gate-2 §11 ruling).
  buildProduct({
    barcode: "7290018439579",
    bucket: GROUP_B,
    states: ["fail", "evidence_limited", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 76,
    doseValueLabel: '76 מ"ג',
    formHe: "טאוראט",
    classifierHe: "צורה ידועה, ראיות מוגבלות לדירוג",
    formNote: EVIDENCE_LIMITED_FORM_NOTE_HE,
    oneLinerHe:
      'מגנזיום טאוראט, נוטריקר נותן 76 מ"ג מגנזיום יסודי במנה היומית, המינון הנמוך ביותר בין 15 המוצרים עם מינון יסודי ברור, בצורת טאוראט. הבטיחות והתיוג נקיים. הצורה ידועה, אך הראיות לדירוג הספיגה שלה בביטחון מוגבלות, כמו אצל צורת המלאט.',
  }),
  // 11 — Nutricare Oxide-520 (520mg oxide) — Group (c), weaker form + crosses UL
  buildProduct({
    barcode: "7290001065662",
    bucket: GROUP_C,
    states: ["pass", "fail", "cannot_verify", "cannot_verify", "fail", "pass"],
    doseMg: 520,
    doseValueLabel: '520 מ"ג',
    formHe: "אוקסיד",
    classifierHe: "צורה בספיגה נמוכה, חוצה סף בטיחות",
    oneLinerHe:
      'מגנזיום אוקסיד 520, נוטריקר נותן 520 מ"ג מגנזיום יסודי במנה היומית, המינון הגבוה ביותר בין 18 המוצרים שנבדקו, בצורת אוקסיד. ה-NIH ODS מונה במפורש את אוקסיד כצורה עם ספיגה נמוכה יותר מציטראט, אספרטט, לקטט וכלוריד. 520 מ"ג חוצה גם את סף ה-350 מ"ג ליום שקבע המכון האמריקאי לרפואה (IOM/NASEM) למגנזיום מתוסף. זו אזהרת מינון גלויה על התווית, מעבר לממצא הספיגה.',
  }),
  // 12 — Altman Oxide-520 (520mg oxide) — Group (c), same as #11
  buildProduct({
    barcode: "7290017218564",
    bucket: GROUP_C,
    states: ["pass", "fail", "cannot_verify", "cannot_verify", "fail", "pass"],
    doseMg: 520,
    doseValueLabel: '520 מ"ג',
    formHe: "אוקסיד",
    classifierHe: "צורה בספיגה נמוכה, חוצה סף בטיחות",
    oneLinerHe:
      'מגנזיום 520, אלטמן נותן אותו מינון בדיוק כמו המוצר הקודם: 520 מ"ג מגנזיום יסודי במנה היומית, בצורת אוקסיד. אותם שני ממצאים חוזרים כאן: אוקסיד נספג פחות טוב לפי NIH ODS, והמינון חוצה את סף ה-350 מ"ג ליום.',
  }),
  // 13 — Altman Magnesium UP (450mg oxide) — Group (c)
  buildProduct({
    barcode: "7290013142894",
    bucket: GROUP_C,
    states: ["pass", "fail", "cannot_verify", "cannot_verify", "fail", "pass"],
    doseMg: 450,
    doseValueLabel: '450 מ"ג',
    formHe: "אוקסיד",
    classifierHe: "צורה בספיגה נמוכה, חוצה סף בטיחות",
    oneLinerHe:
      'מגנזיום UP, אלטמן נותן 450 מ"ג מגנזיום יסודי במנה היומית, גם הוא בצורת אוקסיד. המינון נמוך במקצת מהשניים הקודמים, אבל עדיין חוצה את סף ה-350 מ"ג ליום, ואותה מגבלת ספיגה של אוקסיד חלה כאן.',
  }),
  // 14 — Altman Magnesium Balance (450mg oxide) — Group (c)
  buildProduct({
    barcode: "7290019444206",
    bucket: GROUP_C,
    states: ["pass", "fail", "cannot_verify", "cannot_verify", "fail", "pass"],
    doseMg: 450,
    doseValueLabel: '450 מ"ג',
    formHe: "אוקסיד",
    classifierHe: "צורה בספיגה נמוכה, חוצה סף בטיחות",
    oneLinerHe:
      'מגנזיום באלאנס, אלטמן נותן 450 מ"ג מגנזיום יסודי במנה היומית, בצורת אוקסיד, עם אותו ממצא ספיגה ואותה חציית סף בטיחות כמו שני המוצרים הקודמים. אשווגנדה וולריאן מופיעים גם הם על התווית, אבל הם לא חלק מהבדיקה של המגנזיום עצמו.',
  }),
  // 15 — Nutricare Nano Liposomal (88mg bisglycinate base) — Group (b). formAbsorption
  // evidence_limited per TASK-575 gate-2 §11 ruling (was pass) — group membership
  // UNCHANGED (was already dose-driven). No classifierHe (11.3 scope).
  buildProduct({
    barcode: "7290001065594",
    bucket: GROUP_B,
    states: ["fail", "evidence_limited", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 88,
    doseValueLabel: '88 מ"ג',
    formHe: "ביסגליצינט",
    formNote: EVIDENCE_LIMITED_FORM_NOTE_HE,
    oneLinerHe:
      'נאנו מגנזיום ליפוזומלי, נוטריקר נותן 88 מ"ג מגנזיום יסודי במנה היומית, בצורת בסיס ביסגליצינט: צורה שנחשבת בפועל טובה לספיגה, אך ההוכחה הישירה לכך מוגבלת מכדי לדרג אותה בביטחון. הבטיחות והתיוג נקיים. 88 מ"ג הוא המינון השני הנמוך ביותר בין 15 המוצרים עם מינון יסודי ברור. הכיתוב "נאנו ליפוזומלי" על האריזה הוא טענת שיווק נפרדת: לא מצאנו במקורות שבדקנו עדות לשיפור ספיגה מעבר לצורת הבסיס עצמה.',
  }),
  // 16 — Tink Oxide-520, no elemental/compound qualifier — Group (c)
  buildProduct({
    barcode: "7290015318426",
    bucket: GROUP_C,
    states: ["cannot_verify", "fail", "cannot_verify", "cannot_verify", "cannot_verify", "cannot_verify"],
    doseMg: null,
    doseValueLabel: "לא ניתן לאימות",
    formHe: "אוקסיד", // form itself is known (oxide) even though the dose reading is ambiguous — not a blend (spec/rubric blend_rule distinction)
    classifierHe: "צורה בספיגה נמוכה, מינון לא ניתן לאימות",
    oneLinerHe:
      'מגנזיום אוקסיד 520, טינק (90 כמוסות) מציין 520 על האריזה, אבל התווית לא מבהירה אם זה מגנזיום יסודי או משקל התרכובת, כך שהמינון בפועל לא ניתן לאימות מהתווית. הצורה כן ידועה: אוקסיד, אותה צורה שה-NIH ODS מונה כבעלת ספיגה נמוכה יותר, ללא קשר לאיזו קריאה של "520" נכונה.',
  }),
  // 17 — Amorphicure pH Magnesium (carbonate, unresolved) — Group (c)
  buildProduct({
    barcode: "7290015429245",
    bucket: GROUP_C,
    states: ["cannot_verify", "fail", "cannot_verify", "cannot_verify", "cannot_verify", "cannot_verify"],
    doseMg: null,
    doseValueLabel: "לא ניתן לאימות",
    formHe: "קרבונט",
    classifierHe: "צורה בספיגה נמוכה, מינון לא ניתן לאימות",
    oneLinerHe:
      'pH מגנזיום, אמורפיקיור לא מפרט על התווית מהו המינון היומי בפועל, כך שהמינון לא ניתן לאימות. הצורה כן ידועה: קרבונט. קרבונט לא מוזכר בשמו במקור ה-NIH ODS, אבל מסווג יחד עם אוקסיד כצורה בעלת ספיגה נמוכה על סמך דמיון כימי בין המלחים בלבד. זה סיווג חלש יותר מציטוט ישיר, וההוכחה לכך חלשה יותר מזו של אוקסיד עצמו.',
  }),
  // 18 — TRIOMAG (undisclosed 3-form blend) — Group (d)
  buildProduct({
    barcode: "7290118816065",
    bucket: GROUP_D,
    states: [
      "cannot_verify",
      "cannot_verify",
      "cannot_verify",
      "cannot_verify",
      "cannot_verify",
      "cannot_verify",
    ],
    doseMg: null,
    doseValueLabel: "לא ניתן לאימות",
    formHe: null, // undisclosed 3-form blend — form itself unresolved (blend_rule)
    oneLinerHe:
      'TRIOMAG, סופהרב מציין על התווית תערובת של ציטראט, ביסגליצינט וטאוראט, בלי לפרט את היחס בין השלושה. בלי היחס הזה, אי אפשר לדעת כמה מגנזיום יסודי מגיע בפועל למנה, ואי אפשר לדרג את הספיגה של התערובת הספציפית הזו. זה המוצר היחיד מתוך 18 שנבדקו שבו גם הצורה הכימית עצמה אינה ניתנת לקביעה מהתווית, בנוסף למינון.',
  }),
];

// ─── TASK-577 wiring phase — SIGNED group mapping (supersedes the provisional table) ──
// Source of truth: mag_guide_v3_structure_spec.md §A.3 (the full 18/18 table),
// Nutrition D6 + Product D7 co-signed, sha256
// cc0cc76fc147955b802befbad64ab3a479d152a76d1915d38dfcfb3ea5ab6a84. This REPLACES the
// earlier provisional cascade this file shipped before the spec existed — the
// provisional table's own header comment predicted exactly this ("Expect this table
// to be replaced wholesale once Nutrition's real v3 spec lands").
//
// §A.2's precedence rule (Tier 1 known-poor-absorption-form checked before Tier 2
// nothing-knowable, before Tier 3 clean-citrate/bisglycinate, before Tier 4 default)
// moves #16 and #17 into Heading 3 ("מבוססי אוקסיד") — the provisional table had
// placed them in g4 because it prioritized dose-unclear over form-known; the signed
// spec's Tier 1 explicitly checks form first (§A.4 DEVIATION 4: "a precedence-
// resolution call, not a literal-text mismatch"). #17 is carbonate, not literally
// oxide — grouped under Heading 3 by chemical-class analogy only, weaker evidence
// basis than oxide's direct NIH ODS citation (§A.4 DEVIATION 3) — Product D7 made
// this a MANDATORY on-card disambiguation, fulfilled by #17's own one-liner (see
// MAG_V3_ONE_LINER_BY_BARCODE in magnesium-guide-copy-v3.ts).
//
// Signed distribution (§A.3): Heading 1 = 6/18 (#1,2,3,4,6,15), Heading 2 = 5/18
// (#5,7,8,9,10), Heading 3 = 6/18 (#11,12,13,14,16,17), Heading 4 = 1/18 (#18).
// Sum check: 6+5+6+1 = 18. ✓ Matched by barcode against the spec's own product table,
// not by array index.
const V3_GROUP_BY_BARCODE: Record<string, GuideV3Group> = {
  "7290013464248": "g1", // 1 — Supherb Citrate+B6 (citrate, clean label) — Heading 1
  "7290019444480": "g1", // 2 — Altman Bisglycinate (bisglycinate, clean label) — Heading 1
  "7290011899967": "g1", // 3 — Altman Citrate 120 (citrate, clean label) — Heading 1
  "7290018439043": "g1", // 4 — Nutricare WELL (bisglycinate, clean label) — Heading 1
  "7290010207640": "g2", // 5 — NT L.C. Anti Leg Cramps (hydroxide, low dose) — Heading 2
  "7290001943700": "g1", // 6 — Full-Mag Hadas (bisglycinate, clean label) — Heading 1
  "7290015318532": "g2", // 7 — Tink Malate (malate, low dose) — Heading 2
  "7290001066973": "g2", // 8 — Nutricare Malate (malate, low dose; extra label gap) — Heading 2
  "0033984005181": "g2", // 9 — Solgar Ca+Mg+D3 (blend, dominant fact = disclosed low elemental dose) — Heading 2, §A.4 DEVIATION 2
  "7290018439579": "g2", // 10 — Nutricare Taurate (taurate, lowest verifiable dose) — Heading 2
  "7290001065662": "g3", // 11 — Nutricare Oxide-520 (oxide, verifiable dose) — Heading 3
  "7290017218564": "g3", // 12 — Altman Oxide-520 (oxide, verifiable dose) — Heading 3
  "7290013142894": "g3", // 13 — Altman Magnesium UP (oxide, verifiable dose) — Heading 3
  "7290019444206": "g3", // 14 — Altman Magnesium Balance (oxide, verifiable dose) — Heading 3
  "7290001065594": "g1", // 15 — Nutricare Nano Liposomal (bisglycinate base, clean label) — Heading 1
  "7290015318426": "g3", // 16 — Tink Oxide-520 (form known = oxide; dose ambiguity ≠ grouping driver) — Heading 3, §A.4 DEVIATION 4 [MOVED from provisional g4]
  "7290015429245": "g3", // 17 — Amorphicure pH Magnesium (carbonate, grouped w/ oxide by chemical-class analogy) — Heading 3, §A.4 DEVIATION 3 [MOVED from provisional g4]
  "7290118816065": "g4", // 18 — TRIOMAG (the one product where nothing is knowable — form AND dose unresolved) — Heading 4
};

// `elementalDoseLabel`/`formLabel` stay a mechanical derivation — never a second,
// independently-authored source of truth for a fact already computed above (same
// discipline as `benchmarks` in buildProduct). `whatMattersHe` is now the SIGNED,
// gate-1 AUTHORED one-liner (mag_guide_v3_copy_package.md §2, wired verbatim via
// MAG_V3_ONE_LINER_BY_BARCODE) — no longer the v2 oneLinerHe placeholder. Fails loud
// (throws) if a product's barcode is missing from the signed map, matching the
// existing `identity()` fail-loud discipline above — a silent fallback to the old
// v2 string would ship unsigned-for-v3 copy without anyone noticing.
function visibleFactsV3For(product: GuideProductVM): GuideCardVisibleFacts {
  const dose = product.benchmarks?.doseAdequacy;
  const form = product.benchmarks?.formAbsorption;
  const whatMattersHe = MAG_V3_ONE_LINER_BY_BARCODE[product.id];
  if (!whatMattersHe) {
    throw new Error(
      `magnesium-guide-data: no signed v3 one-liner for product id ${product.id} in MAG_V3_ONE_LINER_BY_BARCODE`
    );
  }
  return {
    elementalDoseLabel:
      dose?.value != null ? `${dose.valueLabel} מגנזיום יסודי` : (dose?.valueLabel ?? "לא ניתן לאימות"),
    formLabel: form?.valueLabel ?? "לא ניתן לאמת",
    // TASK-577 — genuine data gap (spec §B / Product D7 amendment #4: fully absent
    // from the rendered card, never a placeholder). Never fabricated: absent for all
    // 18 products in this build.
    servingsPerDayLabel: null,
    whatMattersHe,
  };
}

for (const product of products) {
  product.groupV3 = V3_GROUP_BY_BARCODE[product.id] ?? null;
  product.visibleFactsV3 = visibleFactsV3For(product);
}

// ─── Display suppression (rubric display_suppression_rule) — computed fresh from the
// live `products` array above, never a hardcoded "hide these bars for magnesium" list
// (rubric re_evaluated_per_build clause). For the current 18-product corpus this
// resolves to [thirdPartyVerification, priceFairness] (both cannot_verify 18/18, per
// the Product Agent's premise check in magnesium_guide_bar_revision_call_v1.md) — but
// the value is DERIVED here, not asserted. ─────────────────────────────────────────
const suppressedBars = computeSuppressedBars(products, GUIDE_BAR_ORDER);
// Magnesium: bandExcludedBars stays [] per TASK-504 spec (creatine-only gating exclusion).
const bandExcludedBars: GuideBarKey[] = [];

export const magnesiumGuide: GuidePageVM = {
  slug: "magnesium",
  h1: "איך לבחור מגנזיום",
  subtitle: null,
  // TASK-504C add-on — hero mascot (owner-supplied asset, optimized + self-hosted,
  // see this task's return for the source/optimization chain). Alt text FINAL —
  // cleared QA gate-2 (2026-07-05, GO on record in this task's return, TASK-504
  // Wave 1); drafted per 03_operations/reports/content/magnesium_guide_slot_copy_v1.md
  // Slot 3.
  heroImage: {
    src: "/mascots/mascot-mg-magnesium-guide.webp",
    alt: "לומו, דמות בארי, בוחן דרך זכוכית מגדלת צורות שונות של תוסף מגנזיום, כשמסביבו בקבוקוני תוספים ומאכלים עתירי מגנזיום.",
    width: 1280,
    height: 1024,
  },
  // TASK-575 (magnesium guide v2) — copy package Slot 1, verbatim. Kills "מהמדף
  // הישראלי" as a market-completeness claim (nutrition spec §8), kills the retired
  // six-bars/"אף אחד לא עומד בכל שישה" framing, presents only the FOUR assessed
  // criteria, states the price/third-party gap once as a guide-level scope note.
  buyingRuleIntro:
    "בדקנו 18 תוספי מגנזיום הנמכרים בישראל, לפי ארבעה דברים שאפשר לקרוא ולבדוק ישירות מהתווית: כמה מגנזיום יסודי המוצר נותן במנה היומית המצוינת עליה, מה הצורה הכימית שלו, האם המינון מתקרב לסף שעלול לגרום לאי-נוחות עיכולית, והאם התווית בכלל מגלה את המידע הדרוש כדי לדעת מה קונים. אין צורך להבין כימיה כדי להשתמש בזה, רק לדעת מה לחפש לפני שמשלמים. שני דברים נוספים לא נבדקו בסבב הזה: מחיר למנה יומית, ובדיקת צד שלישי. שניהם מפורטים בהמשך כפער מידע ברמת המדריך כולו בלבד. הם אינם סיבה לשיוך של מוצר ספציפי לקבוצה כזו או אחרת.",
  // TASK-575 copy package Slot 2 — exactly the 4 ASSESSED-criteria cards (dose, form,
  // safety, label). Price + third-party LEAVE the assessed how-to-read grid (owner
  // directive) — they render only in the guide-level market-gaps box below, never as
  // an intro card. `bar` keys unchanged (GuideBarKey itself is untouched).
  buyingRule: [
    {
      bar: "doseAdequacy",
      explanation:
        "המינון היומי: כמה מגנזיום יסודי המוצר נותן במנה היומית המצוינת על התווית. משקל התרכובת (ציטראט, אוקסיד וכו') שלפעמים מודפס גדול יותר על האריזה הוא מספר אחר לגמרי.",
    },
    {
      bar: "formAbsorption",
      explanation: "הצורה הכימית: צורות מגנזיום שונות נספגות בגוף במידה שונה, וההבדל מתועד במקורות מקצועיים.",
    },
    {
      bar: "safety",
      explanation: "בטיחות: האם המינון היומי המוצהר מתקרב לסף שעלול לגרום לאי-נוחות עיכולית, או חוצה אותו.",
    },
    {
      bar: "labelTransparency",
      explanation:
        "שקיפות התיוג: האם התווית בכלל מאפשרת לדעת כמה מגנזיום יסודי מקבלים במנה, או שרק משקל התרכובת מצוין בלי חישוב.",
    },
  ],
  // TASK-575 copy package Slot 4 — replaces the retired empty-top-tier framing.
  // body[3]-body[7]'s five per-product paragraphs (duplicating each product's own
  // oneLinerHe) are DELETED per the package's explicit instruction ("product detail
  // now lives only in each product's own oneLinerHe, never duplicated here").
  // title/body[0] AMENDED per SLOT 11 / §11 MEDIUM-1 (gate-2 ruling, 2026-07-10):
  // "צורה כימית מומלצת" rescoped to citrate alone — citrate and bisglycinate no
  // longer share an evaluative adjective in the same clause (the old text incorrectly
  // paired them as equally "recommended"; only citrate has a direct NIH ODS citation
  // for better absorption, per nutrition spec §5 Bucket 1 vs Bucket 3).
  headlineFinding: {
    title:
      "בין 18 תוספי המגנזיום שבדקנו, אף אחד לא משלב מינון בחצי העליון של הטווח, צורת ציטראט ובטיחות ותיוג נקיים בו-זמנית.",
    body: [
      'כל מוצר שמגיע למינון הגבוה בטווח שנבדק (450 עד 520 מ"ג) עושה זאת בצורת אוקסיד, צורה שה-NIH ODS מונה במפורש כבעלת ספיגה נמוכה יותר מציטראט, אספרטט, לקטט וכלוריד. שני המוצרים היחידים בצורה עם עדות מבוססת לספיגה טובה יותר, ציטראט, נשארים מתחת ל-250 מ"ג. ביסגליצינט, הצורה הנפוצה השנייה בקטגוריה, מופיע במוצרים שנעים בין 88 ל-250 מ"ג, אך הראיות לדירוג הספיגה שלו בביטחון מוגבלות מדי כדי לצרף אותו לאותה קבוצה. אף אחד מ-18 המוצרים שנבדקו לא משלב בו-זמנית מינון בחצי העליון של הטווח, צורת ציטראט ובטיחות ותיוג נקיים. זה ממצא על השוק הנוכחי עצמו, מעבר לפערי הנתונים במחיר או בבדיקת צד שלישי.',
      'בגלל זה אין כאן קבוצה אחת שכל מוצר "טוב" צריך להימצא בה. המוצרים מחולקים לפי הממצא האמיתי שיש לגביהם: מוצרים שההסתייגות היחידה עליהם היא מינון יסודי נמוך יותר מתוך הטווח שנבדק, מוצרים עם הסתייגות קבועה על הצורה הכימית או על סבילות עיכולית, ומוצר אחד שאי אפשר לדעת עליו מספיק מהתווית כדי לשייך אותו לאחת משלוש הקבוצות האלה.',
      "מחיר למנה ובדיקת צד שלישי לא נכללים בשיוך הזה כלל. הם לא נבדקו לאף אחד מ-18 המוצרים, וזה מפורט בנפרד למטה.",
    ],
  },
  products,
  // TASK-504C — rubric display_suppression_rule. Computed above from the live product
  // array; NOT hardcoded. Currently resolves to [thirdPartyVerification, priceFairness].
  suppressedBars,
  bandExcludedBars,
  // TASK-575 copy package Slot 3 — same field (`suppressedBarsDisclosureHe`), copy
  // rewritten. Carries the owner's exact certification register and scopes every
  // market claim to "18 המוצרים שנבדקו" (nutrition spec §8), never "המדף הישראלי".
  // Rendering moved from a top-of-section amber line to a calm, AFTER-the-groups box
  // (see guide-product-table.tsx's useDescriptiveGroups branch) — task requirement C.
  suppressedBarsDisclosureHe:
    "שני דברים לא נבדקו במדריך הזה, אצל כל 18 המוצרים: מחיר למנה יומית, ובדיקת צד שלישי. מחיר הוא פער איסוף נתונים של בארי: עדיין לא נאספו נתוני מחיר לתוספי מגנזיום, ונוסיף אותם כשהנתונים ייאספו. בדיקת צד שלישי היא עובדה אחרת: לא מצאנו אישור או בדיקת צד שלישי הניתנים לאימות פומבי בקרב 18 המוצרים שנבדקו, נכון ליולי 2026. שני הפערים האלה לא משפיעים על השיוך של אף מוצר לאחת הקבוצות שלמטה. השיוך מבוסס רק על ארבעת הדברים שכן נבדקו.",
  // TASK-575 — the retired ranked-tier fields (recommendationTierCaptions /
  // veryRecommendedEmptyStateHe / cannotAssessSectionIntroHe) are DELETED for this
  // guide (copy package Slot 9 "retired fields" — no new copy authored for them; they
  // belong to the ranked-tier model this build removes end-to-end). Replaced by the
  // descriptive-group model below.
  useDescriptiveGroups: true,
  // TASK-575 copy package Slot 5 — the 4 group SECTION HEADERS, in GUIDE_BUCKET_ORDER
  // (clears_all / passes_with_flag / fails / cannot_assess = groups a/b/c/d). No
  // letters, no ranking language — descriptive section names only.
  groupLabelsHe: {
    clears_all: "עומדים בכל הקריטריונים שנבדקו",
    passes_with_flag: "מינון יסודי נמוך יותר",
    fails: "הסתייגות על הצורה הכימית או על סבילות עיכולית",
    cannot_assess: "מידע לא מספיק על התווית",
  },
  // TASK-575 copy package Slot 5 — the 4 group ONE-LINE captions. `clears_all`'s
  // caption doubles as its empty-state line (spec §2: "renders its empty-state
  // caption" — the group is always empty for this 18-product corpus today).
  // `passes_with_flag` REWRITTEN per SLOT 11.2 (gate-2 ruling, 2026-07-10): the old
  // caption made a blanket "form is clean" claim that was true for the original 5
  // members but is not true for 7 of the new 9 (only #3 is confirmed-good citrate;
  // #9 is an undisclosed blend, cannot_verify; the remaining 7 are evidence_limited).
  // `fails` caption text is UNCHANGED (still accurate for the remaining 8 — SLOT 11.2).
  groupCaptionsHe: {
    clears_all: "אף מוצר מתוך 18 שנבדקו לא נמצא כאן. זה עצמו הממצא המרכזי של המדריך — מפורט למעלה.",
    passes_with_flag:
      "מינון יסודי נמוך יותר מתוך הטווח שנבדק הוא המשותף לתשעת המוצרים האלה, ללא הסתייגות בטיחות אצל אף אחד מהם. שקיפות התיוג נקייה אצל שמונה מתוכם; מוצר אחד נושא פער תיוג, מפורט בשורה שלו. הצורה הכימית ידועה אצל כולם: ציטראט (מוצר אחד) נתמך בעדות מבוססת לספיגה טובה, אצל שאר הצורות הראיות לדירוג הספיגה בביטחון עדיין מוגבלות, ואצל מוצר אחד (תערובת שני רכיבים) היחס בתערובת אינו מפורסם כך שהספיגה שלו אינה ניתנת לדירוג כלל.",
    fails:
      "אצל המוצרים האלה יש ממצא קבוע על הצורה הכימית עצמה, או מינון שנמצא בגובה הסף לתשומת לב עיכולית. ממצא כזה לא משתנה כמה שלוקחים מהמנה המצוינת על התווית.",
    cannot_assess: "התווית של המוצר הזה לא מגלה מספיק כדי לדעת אילו מגנזיום, כמה, או שניהם.",
  },
  // Per-row expander toggle labels (Design spec v2 §3.3 progressive disclosure).
  // FINAL COPY — cleared QA gate-2 (2026-07-05, GO on record in this task's return,
  // TASK-504 Wave 1); drafted per magnesium_guide_tier_copy_v1.md Slot 4.
  expanderLabels: {
    collapsed: "הצג את הסולמות",
    expanded: "הסתר את הסולמות",
  },
  // TASK-504C — per-bar gauge/ladder geometry (Design spec §2/§3). Only the 4
  // discriminating bars have an anatomy defined today (spec §1) — thirdPartyVerification
  // and priceFairness are absent here (they are also suppressedBars for this build, so
  // this is moot for magnesium today, but stays correct if a future magnesium pricing
  // scrape un-suppresses priceFairness before an anatomy exists for it: it would then
  // render as a plain badge row, never crash on a missing geometry entry).
  thresholdGeometry: {
    doseAdequacy: MAGNESIUM_DOSE_GAUGE,
    formAbsorption: MAGNESIUM_FORM_LADDER,
    safety: MAGNESIUM_SAFETY_GAUGE,
    labelTransparency: MAGNESIUM_TRANSPARENCY_LADDER,
  },
  // TASK-575 copy package Slot 7 — consolidated from 11 education-spine sections to 5
  // content sections + 1 sources section. Removes the live duplication between
  // "בטיחות" and "מינון ובטיחות" (near-identical), folds "הצורות הכימיות, מוסבר שוב
  // בקצרה" into the absorption section instead of repeating it, and drops the
  // standalone "בדיקת צד שלישי" / "הוגנות המחיר" education sections (that content now
  // lives ONLY in the guide-level market-gaps box, never duplicated here). Every kill
  // instruction from nutrition spec §3/§4/§5/§6 (the 300mg floor, the capsule-stacking
  // suggestion, the oxide-cheap causal claim, the unscoped cramps claim) is applied.
  educationSpine: [
    {
      heading: "מגנזיום יסודי מול משקל התרכובת: המספר שבאמת חשוב",
      body: [
        "הספרה הרלוונטית היא כמות המגנזיום היסודי במנה היומית המצוינת על התווית. משקל התרכובת (ציטראט, אוקסיד, ביסגליצינט וכו') שלפעמים מודפס גדול יותר על האריזה הוא מספר אחר לגמרי. הוא לא מלמד ישירות על הכמות היסודית. כשאי אפשר לחשב את המינון היומי בכלל מהתווית, כמו אצל שלושה מהמוצרים שנבדקו, זהו פער מידע על אותו מוצר ספציפי בלבד. זה אינו ממצא על שאר הקטגוריה.",
      ],
    },
    {
      heading: "המינון בהקשר: איך להעריך מספר בלי סף יחיד",
      body: [
        'אין מחקר שקובע סף בודד שמפריד בין מינון משמעותי למינון שולי עבור תוסף מגנזיום באופן כללי. שני הקשרים כנים אפשר להשתמש בהם במקום זה. ראשית, ביחס לטווח שנמצא בפועל בין 18 המוצרים שנבדקו: מתוך 15 מוצרים עם מינון יסודי ברור על התווית, המינונים נעים בין 76 ל-520 מ"ג ליום, החציון 190 מ"ג. שנית, ביחס לצריכה היומית המומלצת הכללית (RDA) שקבע המכון הלאומי לבריאות האמריקאי (NIH ODS): 310 עד 420 מ"ג ליום, בהתאם לגיל ולמין, מכל המקורות יחד: מזון, משקאות ותוספים כאחד. תוסף בדרך כלל משלים רק חלק מהכמות הזו, וכמה בדיוק תלוי בתזונה של כל אחד. בארי אינה יכולה לדעת את זה מהתווית בלבד.',
      ],
    },
    {
      heading: "צורה כימית וספיגה: שלוש קבוצות ראיות במקום סולם אחד",
      body: [
        'לפי גיליון המידע המקצועי של המכון הלאומי לבריאות האמריקאי (NIH Office of Dietary Supplements) על מגנזיום, ציטראט, אספרטט, לקטט וכלוריד נספגים בגוף בצורה מלאה יותר מאוקסיד וגופרתי (סולפט). מתוך 18 המוצרים שנבדקו, ציטראט הוא הצורה היחידה מהקבוצה הזו שמופיעה בפועל, בשלושה מוצרים. אוקסיד, הצורה הפחות נספגת לפי אותו מקור, מופיע בשישה מוצרים; הוא גם זול לייצור כתרכובת תעשייתית נפוצה, אבל אלה שתי עובדות נפרדות בלבד, בלי יחס של סיבה ותוצאה ביניהן. קרבונט, שמופיע במוצר אחד, אינו מוזכר במקור הזה בשמו: הוא מסווג יחד עם אוקסיד לפי דמיון כימי בין המלחים בלבד, סיווג חלש יותר מציטוט ישיר. שאר הצורות שנמצאו בקטגוריה, ביסגליצינט, מלאט, טאוראט והידרוקסיד, אינן מוזכרות בשמן בגיליון של NIH ODS כלל. ביסגליצינט נחשב לרוב שווה-ערך לציטראט מבחינת ספיגה, אבל מחקרים קטנים שבדקו את זה ישירות נתנו תוצאות מעורבות וחלשות, וזה לא מספיק כדי לדרג אותו באותה רמת ביטחון. ההערכה הכנה לגבי ארבע הצורות האלה: הראיות מוגבלות מכדי לקבוע בביטחון אם הספיגה שלהן טובה או חלשה.',
      ],
    },
    {
      heading: "בטיחות: מתי מינון גבוה עלול להפריע",
      body: [
        'הסף העליון למגנזיום מתוסף (בשונה ממגנזיום שמקורו במזון) הוא 350 מ"ג יסודי ליום, לפי המכון האמריקאי לרפואה (IOM/NASEM). הרשות האירופית לבטיחות מזון (EFSA) קבעה סף רך יותר, 250 מ"ג ליום, במקור בחוות דעת של הוועדה המדעית למזון של האיחוד האירופי (SCF) משנת 2001, ואושרר מחדש בחוות דעת של פאנל התזונה של EFSA משנת 2015. שני הסכומים מתארים את אותה תופעה: מינון גבוה מדי של מגנזיום מתוסף עלול לגרום לשלשול קל וזמני. זו לא רעילות. אנשים עם מחלת כליות, או שנוטלים תרופות מסוימות, צריכים לדבר עם רופא לפני נטילת מינונים גבוהים, ללא קשר לצורה הכימית של המוצר. המדריך הזה מתאר את המנה היומית המצוינת על התווית של כל מוצר בלבד. הוא לא מציע לקחת יותר כמוסות ממה שהיצרן ממליץ.',
      ],
    },
    {
      heading: "מה מגנזיום עושה, ולמה זה לא כולל עוויתות שרירים אצל כולם",
      body: [
        "מגנזיום הוא מינרל חיוני שמעורב בתפקוד של שרירים, עצבים ובעצם. תוסף מגנזיום נותן ערך אמיתי כשהתזונה היומית לא מספקת מספיק, בהתאם למינון ולצורה הכימית שנספגת בפועל. הטענה השכיחה ביותר על תוספי מגנזיום, הקלה בעוויתות שרירים, נבדקה בסקירה שיטתית של קוקריין משנת 2020 (Garrison et al., PMID 32956536). אצל מבוגרים עם עוויתות שרירים רגילות (שאינן קשורות להריון או לפעילות גופנית), הסקירה לא מצאה תמיכה קלינית משמעותית למגנזיום כתוסף מונע. אצל נשים בהריון התמונה שונה: הראיות מעורבות, בלי מסקנה שלילית אחידה. משלושה מחקרים שנבדקו: אחד ללא יתרון מובהק, אחד עם יתרון בתדירות ובעוצמת ההתכווצויות, ואחד לא עקבי בתוצאותיו. לגבי עוויתות הקשורות לפעילות גופנית או למחלות שריר ועצב, כלל לא בוצעו מחקרים מבוקרים: זהו פער מחקר בלבד, מעבר לכל ממצא שלילי.",
      ],
    },
    {
      // TASK-575 copy package Slot 8 — structured, clickable sources (Task F). The
      // banned "אומת באמצעות ציטוטים משניים" framing is removed and NOT replaced with
      // any "verified/מאומת" language — each source simply states what it supports.
      // Only the 3 directly-fetched, verifiable sources ship (Open Questions 6/7:
      // the 3 unverifiable bisglycinate PMIDs and the Zhang/300mg BP citation are
      // deliberately NOT carried into this public list).
      heading: "מקורות",
      body: [
        "בארי קוראת תוויות. בארי אינה בודקת במעבדה. כל המינונים המוצגים הם מה שכתוב על האריזה הישראלית. המידע כאן הוא לצורך היכרות בלבד. הוא אינו תחליף לייעוץ רפואי.",
      ],
      sources: [
        {
          label:
            'המכון הלאומי לבריאות האמריקאי, המשרד לתוספי תזונה (NIH Office of Dietary Supplements) — גיליון מידע מקצועי על מגנזיום. מקור להיררכיית הספיגה בין הצורות הכימיות, ולטווח הצריכה היומית המומלצת (310–420 מ"ג ליום, מכל המקורות יחד) ולסף העליון של 350 מ"ג ליום למגנזיום מתוסף.',
          url: "https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/",
        },
        {
          label:
            'Garrison, S.R. et al., "Magnesium for skeletal muscle cramps," Cochrane Database of Systematic Reviews, 2020 (PMID 32956536). מקור לממצא שלא נמצאה תמיכה קלינית משמעותית להקלת עוויתות שרירים רגילות אצל מבוגרים, ולראיות הסותרות לגבי הריון.',
          url: "https://pubmed.ncbi.nlm.nih.gov/32956536/",
        },
        {
          label:
            'הוועדה המדעית למזון של האיחוד האירופי (SCF, חוות דעת 2001) ו-EFSA, פאנל NDA (חוות דעת 2015, אישרור מחדש); מרוכז בדוח הסיכום העדכני של EFSA על רמות עליון נסבלות (אוגוסט 2025). מקור לסף הרך של 250 מ"ג ליום למגנזיום מתוסף.',
          url: "https://www.efsa.europa.eu/sites/default/files/2024-05/ul-summary-report.pdf",
        },
      ],
    },
  ],
  // TASK-575 copy package Slot 9 — "דגלים" replaced with "השיוך לקבוצה" to match the
  // descriptive-group model instead of the retired flag-ladder vocabulary.
  buyLinkDisclosureLine: "קישור קנייה אינו משפיע על הכללה, על השיוך לקבוצה או על סדר ההצגה.",
  updatedLabel: "18 מוצרים · יולי 2026",

  // ─── TASK-577 (magnesium guide v3 STRUCTURAL rebuild) ──────────────────────────
  // Owner-dictated readability restructure, 2026-07-10. Every string below is either
  // (a) ported verbatim from the TASK-577 dispatch itself (the owner's own dictated
  // text — the dispatch IS the gate-1-equivalent source for this structural build;
  // final Hebrew still requires the real two-gate content package before this page
  // can go live/indexed — see page.tsx's noindex status, unchanged by this task), or
  // (b) the existing gate-2-approved v2 string, reused where the dispatch said to
  // keep the v2 string temporarily. Nothing here is newly authored prose.
  useV3Layout: true,

  // Item 1.1 — the ONE intro sentence under the H1. OWNER-DICTATED, verbatim, ships
  // as-is per instruction. FLAG (package §1.1, HIGH, unresolved — owner call, not
  // Frontend's to silently patch): "מהמדף הישראלי" reintroduces the exact
  // market-completeness phrase v2 spec §8 killed. Surfaced in this task's return.
  introSentenceHe: MAG_V3_INTRO_HE,

  // Item 1.2 — "מה גילינו" box, 4 bullets. OWNER-DICTATED, verbatim. FLAG (package
  // §1.2, MEDIUM, unresolved — owner call): bullet 3's "מוצרים רבים" is the exact
  // vague-count pattern spec §C's own wording-hazard note warned against for this
  // finding (precise count is 6/18). Surfaced in this task's return.
  whatWeFoundHe: MAG_V3_WHAT_WE_FOUND_HE,

  // Item 1.3 — the 4 v3 group section headers. OWNER-DICTATED, verbatim, matches
  // spec §A.1 exactly. Product MEMBERSHIP is on each product's own `groupV3` field —
  // see the SIGNED V3_GROUP_BY_BARCODE mapping above (spec §A.3, D6+D7 co-signed).
  groupV3LabelsHe: MAG_V3_GROUP_LABELS_HE,

  // Item 1.4 — "איך לקרוא תווית מגנזיום", 3 bullets. OWNER-DICTATED, verbatim.
  howToReadLabelHe: MAG_V3_HOW_TO_READ_HE,

  // Item 4 — compact market-information-gaps copy (package §4, AUTHORED, condenses
  // v2's 4-sentence `suppressedBarsDisclosureHe` to 3 sentences per the owner's
  // less-text direction). `suppressedBarsDisclosureHe` above stays byte-identical
  // for v2 rollback; this is the v3-only replacement, rendered in exactly one place
  // (the market-gaps box, after the groups) by GuideProductGroupsV3.
  marketGapsCompactHe: MAG_V3_MARKET_GAPS_COMPACT_HE,

  // Item 5 — collapsed education+sources accordion title (package §5, AUTHORED).
  collapsedEvidenceSectionTitleHe: MAG_V3_COLLAPSED_SECTION_TITLE_HE,

  // Item 5 — per-card `לפרטים` disclosure toggle labels (package §5, AUTHORED;
  // generic on purpose per the package's own note — whether the v2 gauge-specific
  // "הצג/הסתר את הסולמות" labels apply instead is an open Design/Frontend call this
  // package explicitly does not decide; keeping the generic pair since the v3 build
  // keeps the gauges inside the SAME disclosure as the badges/classifier, not a
  // gauge-only toggle).
  expanderLabelsV3: MAG_V3_EXPANDER_LABELS_HE,
};
