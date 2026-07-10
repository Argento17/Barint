// Magnesium golden guide — /madrichim/magnesium (TASK-504B, Wave 1; TASK-504C threshold
// infographic + hero mascot add-on).
//
// Ground truth (used EXACTLY, nothing invented):
//   1. Copy — 03_operations/reports/content/magnesium_guide_copy_v1.md (gate-1 approved
//      by the Content Agent; gate-2 / Adversarial QA sign-off CLEARED 2026-07-05 for
//      body + tier copy per the standing two-gate hard rule — GO on record in this
//      task's return, TASK-504 Wave 1. This does NOT make the page launch-ready: still
//      pending C3, Nutrition D7 co-sign, Design review, the C0 gate battery, and the
//      owner's index/robots flip — none of that is asserted here). Every Hebrew
//      string below that is not a structural label is ported VERBATIM from that file.
//      The only edit applied anywhere is stripping the source markdown's "**" bold
//      markers (pure markup, not content — this template renders plain <p> tags, not
//      markdown) and removing the numbered-list "N. " prefixes that only made sense in
//      a markdown list (their content is unchanged). No word was added, removed, or
//      reordered.
//   2. Bar-states — 01_framework/nutrition/supplement_guides_bar_rubric_companion_v1.md
//      §3 validation table (18 magnesium rows). D/F/T/P/S/L columns map 1:1 to
//      doseAdequacy/formAbsorption/thirdPartyVerification/priceFairness/safety/
//      labelTransparency; FLAG/PASS/FAIL/CANNOT-VERIFY map 1:1 to flag/pass/fail/
//      cannot_verify. Bucket column maps 1:1 to GuideBucket.
//   3. Mechanism — 03_operations/reports/product/supplement_guides_d7_cosign_v1.md §1/§2:
//      clears_all is empty (0/18) → headlineFinding leads the page, passes_with_flag
//      (5/18) is promoted as the practical shortlist, NO default pick anywhere.
//   4. Product identity (name/brand/imageUrl) — bari-web/src/lib/comparisons/
//      magnesium-page-data.ts, id/name/brand/imageUrl fields ONLY. Its score/grade/
//      insightLine/rowVerdict/expansion text are NOT used here — the copy doc's own
//      frontend note is explicit that this guide replaces all of that (including the
//      page's existing "EFSA (2021)" date defect, which this guide never repeats —
//      the correct EFSA (2001/2015) framing lives in the ported safety copy below).
//   5. Threshold-gauge/ladder geometry + per-product doseMg/formHe (TASK-504C) —
//      derived MECHANICALLY from data already in this file (the same mg numbers and
//      chemical-form words already shown in each product's oneLinerHe/benchmark
//      strings below), never a new fact. See
//      03_operations/reports/design/magnesium_guide_threshold_infographic_spec_v1.md
//      for the visual contract this section implements.
//
// Per-bar threshold placement (GuideThresholdPlacement) is product-vs-EXTERNAL-STANDARD
// only, never product-vs-field ranking (plan red-team RT-A3 / this task's guard): the
// doseAdequacy AND safety gauges both plot the SAME disclosed elemental-mg number
// against two different fixed standards (the 300 mg/day effective-dose floor vs the
// 250/350 mg/day GI-tolerance bands) — this is the same "single deciding number, two
// standards" relationship the old flat `benchmark` field approximated with a UL-vs-dose
// A/B switch; here both standards render simultaneously, honestly, per product.
//
// Pricing is null for all 18 (companion doc §3: zero price data collected for magnesium
// — a data-completeness gap, not a product fact). buyUrl is null for all 18 (no retailer
// links collected yet) — GuideBuyButton already renders the dormant state for null.

import {
  GUIDE_BAR_ORDER,
  type GuideBarKey,
  type GuideBarState,
  type GuideBucket,
  type GuideGaugeGeometry,
  type GuideLadderGeometry,
  type GuidePageVM,
  type GuideProductVM,
} from "@/lib/view-models";
import { BAR_STATE_LABELS_HE } from "@/components/shared/bar-state-badge";
import { tierIndexFromState } from "@/components/guides/threshold-bar-row";
import { computeSuppressedBars } from "@/lib/guides/guide-suppression";
import { magnesiumProducts } from "@/lib/comparisons/magnesium-page-data";

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
  return GUIDE_BAR_ORDER.map((bar) => ({ bar, state: byKey[bar] }));
}

// ─── Threshold geometry (TASK-504C spec §2/§3) — ONE object per bar, shared by every
// product row for that bar (the standard is a fact independent of any one product). ──
const MAGNESIUM_DOSE_GAUGE: GuideGaugeGeometry = {
  anatomy: "gauge",
  // 60mg headroom past the 300mg floor so the pass zone reads as a real zone (spec §2
  // domain+overflow rule) — outlier products (450-520mg) clamp at the end with "+".
  domainMax: 360,
  zones: [
    { upTo: 150, tone: "fail", dividerStyle: "solid", tickLabel: '150 (חצי סף)' },
    { upTo: 300, tone: "flag", dividerStyle: "solid", tickLabel: '300 (הסף)' },
    { upTo: 360, tone: "pass", dividerStyle: "solid" },
  ],
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
}): GuideProductVM {
  const barsResult = bars(...opts.states);
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
  };
}

const PW: GuideBucket = "passes_with_flag";
const FAILS: GuideBucket = "fails";
const CANNOT: GuideBucket = "cannot_assess";

const products: GuideProductVM[] = [
  // 1 — Supherb Citrate+B6 (250mg citrate) — PW
  buildProduct({
    barcode: "7290013464248",
    bucket: PW,
    states: ["flag", "pass", "cannot_verify", "cannot_verify", "flag", "pass"],
    doseMg: 250,
    doseValueLabel: '250 מ"ג',
    formHe: "ציטראט",
    oneLinerHe:
      "מגנזיום ציטראט+B6, סופהרב — 250 מ\"ג יסודי, ציטראט. עובר עם דגל: צורה ושקיפות מלאים, המינון (250 מ\"ג) עומד בסף חלקי מול 300 מ\"ג.",
  }),
  // 2 — Altman Bisglycinate (250mg bisglycinate) — PW
  buildProduct({
    barcode: "7290019444480",
    bucket: PW,
    states: ["flag", "pass", "cannot_verify", "cannot_verify", "flag", "pass"],
    doseMg: 250,
    doseValueLabel: '250 מ"ג',
    formHe: "ביסגליצינט",
    oneLinerHe:
      "מגנזיום ביסגליצינט, אלטמן — 250 מ\"ג יסודי, ביסגליצינט. עובר עם דגל: אותו פרופיל, מינון חלקי (250 מתוך 300), עם הסתייגות שראיות הספיגה לביסגליצינט חלשות יותר מציטראט.",
  }),
  // 3 — Altman Citrate 120 (200mg citrate) — PW
  buildProduct({
    barcode: "7290011899967",
    bucket: PW,
    states: ["flag", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 200,
    doseValueLabel: '200 מ"ג',
    formHe: "ציטראט",
    oneLinerHe:
      "מגנזיום ציטראט 120, אלטמן — 200 מ\"ג יסודי, ציטראט. עובר עם דגל: צורה נקייה, המינון (200 מ\"ג) עומד בסף חלקי בלבד.",
  }),
  // 4 — Nutricare WELL (168mg bisglycinate) — PW
  buildProduct({
    barcode: "7290018439043",
    bucket: PW,
    states: ["flag", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 168,
    doseValueLabel: '168 מ"ג',
    formHe: "ביסגליצינט",
    oneLinerHe:
      "מגנזיום WELL, נוטריקר — 168 מ\"ג יסודי, ביסגליצינט. עובר עם דגל: מינון צנוע (168 מ\"ג) הוא הדגל היחיד.",
  }),
  // 5 — NT L.C. Anti Leg Cramps (190mg hydroxide) — PW
  buildProduct({
    barcode: "7290010207640",
    bucket: PW,
    states: ["flag", "flag", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 190,
    doseValueLabel: '190 מ"ג',
    formHe: "הידרוקסיד",
    oneLinerHe:
      "אנטי לג קרמפס, NT L.C. — 190 מ\"ג יסודי, הידרוקסיד. עובר עם דגל: צורה בספיגה בינונית בלבד ומינון חלקי (190 מ\"ג); הטענה על עוויתות שרירים לא נתמכת בסקירת קוקריין 2020.",
  }),
  // 6 — Full-Mag Hadas (122mg bisglycinate) — fails
  buildProduct({
    barcode: "7290001943700",
    bucket: FAILS,
    states: ["fail", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 122,
    doseValueLabel: '122 מ"ג',
    formHe: "ביסגליצינט",
    oneLinerHe:
      'ביסגליצינט 600, פול-מג הדס — 122 מ"ג יסודי, ביסגליצינט. לא עובר: 122 מ"ג נמוך ממחצית הסף היומי (150 מ"ג), למרות שהצורה עצמה מעולה. המספר "600 כמוסות" על האריזה לא משנה שהמנה היומית קטנה מדי.',
  }),
  // 7 — Tink Malate (136mg malate) — fails
  buildProduct({
    barcode: "7290015318532",
    bucket: FAILS,
    states: ["fail", "flag", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 136,
    doseValueLabel: '136 מ"ג',
    formHe: "מלאט",
    oneLinerHe:
      "מגנזיום מלאט, טינק — 136 מ\"ג יסודי, מלאט. לא עובר: המינון (136 מ\"ג) נמוך ממחצית הסף היומי, והצורה (מלאט) עומדת רק בספיגה בינונית.",
  }),
  // 8 — Nutricare Malate (~135mg malate) — fails
  buildProduct({
    barcode: "7290001066973",
    bucket: FAILS,
    states: ["fail", "flag", "cannot_verify", "cannot_verify", "pass", "flag"],
    doseMg: 135,
    doseValueLabel: 'כ-135 מ"ג',
    formHe: "מלאט",
    oneLinerHe:
      "מגנזיום מלאט, נוטריקר — כ-135 מ\"ג יסודי, מלאט. לא עובר: המינון נמוך ממחצית הסף היומי, והתווית מציינת רק את משקל התרכובת (700 מ\"ג מלאט) בלי חישוב יסודי; שקיפות חלקית בנוסף למינון הנמוך.",
  }),
  // 9 — Solgar Ca+Mg+D3 (100mg oxide+citrate blend) — fails
  buildProduct({
    barcode: "0033984005181",
    bucket: FAILS,
    states: ["fail", "cannot_verify", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 100,
    doseValueLabel: '100 מ"ג',
    formHe: null, // undisclosed-ratio blend (oxide+citrate) — form_absorption is cannot_verify (blend_rule)
    oneLinerHe:
      "סידן ומגנזיום +D3, סולגר — 100 מ\"ג יסודי, תערובת אוקסיד וציטראט. לא עובר: המינון (100 מ\"ג) נמוך ממחצית הסף היומי, והצורה היא תערובת שני-רכיבים בלי יחס מפורסם, כך שגם הספיגה בפועל אינה ניתנת להערכה.",
  }),
  // 10 — Nutricare Taurate (76mg taurate) — fails
  buildProduct({
    barcode: "7290018439579",
    bucket: FAILS,
    states: ["fail", "flag", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 76,
    doseValueLabel: '76 מ"ג',
    formHe: "טאוראט",
    oneLinerHe:
      "מגנזיום טאוראט, נוטריקר — 76 מ\"ג יסודי, טאוראט. לא עובר: 76 מ\"ג נמוך משמעותית ממחצית הסף היומי.",
  }),
  // 11 — Nutricare Oxide-520 (520mg oxide) — fails, UL exceed
  buildProduct({
    barcode: "7290001065662",
    bucket: FAILS,
    states: ["pass", "fail", "cannot_verify", "cannot_verify", "fail", "pass"],
    doseMg: 520,
    doseValueLabel: '520 מ"ג',
    formHe: "אוקסיד",
    oneLinerHe:
      'מגנזיום אוקסיד 520, נוטריקר — 520 מ"ג יסודי, אוקסיד. לא עובר: הצורה (אוקסיד) נספגת הכי פחות מכל הצורות בקטגוריה, והמינון (520 מ"ג) חוצה את הסף הבטיחותי העליון (350 מ"ג); אזהרת מינון גלויה.',
  }),
  // 12 — Altman Oxide-520 (520mg oxide) — fails, UL exceed
  buildProduct({
    barcode: "7290017218564",
    bucket: FAILS,
    states: ["pass", "fail", "cannot_verify", "cannot_verify", "fail", "pass"],
    doseMg: 520,
    doseValueLabel: '520 מ"ג',
    formHe: "אוקסיד",
    oneLinerHe:
      "מגנזיום 520, אלטמן — 520 מ\"ג יסודי, אוקסיד. לא עובר: אותו ממצא בדיוק, אוקסיד בספיגה נמוכה, מינון שחוצה את הסף הבטיחותי.",
  }),
  // 13 — Altman Magnesium UP (450mg oxide) — fails, UL exceed
  buildProduct({
    barcode: "7290013142894",
    bucket: FAILS,
    states: ["pass", "fail", "cannot_verify", "cannot_verify", "fail", "pass"],
    doseMg: 450,
    doseValueLabel: '450 מ"ג',
    formHe: "אוקסיד",
    oneLinerHe:
      "מגנזיום UP, אלטמן — 450 מ\"ג יסודי, אוקסיד. לא עובר: אוקסיד בספיגה נמוכה, מינון (450 מ\"ג) שחוצה את הסף הבטיחותי.",
  }),
  // 14 — Altman Magnesium Balance (450mg oxide) — fails, UL exceed
  buildProduct({
    barcode: "7290019444206",
    bucket: FAILS,
    states: ["pass", "fail", "cannot_verify", "cannot_verify", "fail", "pass"],
    doseMg: 450,
    doseValueLabel: '450 מ"ג',
    formHe: "אוקסיד",
    oneLinerHe:
      "מגנזיום באלאנס, אלטמן — 450 מ\"ג יסודי, אוקסיד. לא עובר: אותו ממצא. אשווגנדה ווולריאן על התווית אינם משנים את חשבון המגנזיום עצמו.",
  }),
  // 15 — Nutricare Nano Liposomal (88mg bisglycinate base) — fails
  buildProduct({
    barcode: "7290001065594",
    bucket: FAILS,
    states: ["fail", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseMg: 88,
    doseValueLabel: '88 מ"ג',
    formHe: "ביסגליצינט",
    oneLinerHe:
      'נאנו מגנזיום ליפוזומלי, נוטריקר — 88 מ"ג יסודי, ביסגליצינט (צורת בסיס). לא עובר: 88 מ"ג נמוך משמעותית ממחצית הסף היומי. הטענה "נאנו ליפוזומלי" לא נתמכת בעדות מספקת לשיפור ספיגה מעבר לצורת הבסיס.',
  }),
  // 16 — Tink Oxide-520, no elemental/compound qualifier — fails
  buildProduct({
    barcode: "7290015318426",
    bucket: FAILS,
    states: ["cannot_verify", "fail", "cannot_verify", "cannot_verify", "cannot_verify", "cannot_verify"],
    doseMg: null,
    doseValueLabel: "לא ניתן לאימות",
    formHe: "אוקסיד", // form itself is known (oxide) even though the dose reading is ambiguous — not a blend (spec/rubric blend_rule distinction)
    oneLinerHe:
      "מגנזיום אוקסיד 520, טינק (90 כמוסות) — מינון לא ניתן לאימות, אוקסיד. לא עובר: הצורה עצמה ידועה בספיגה נמוכה (אוקסיד), גם אם התווית אינה מבהירה אם 520 מ\"ג הם המגנזיום היסודי או משקל התרכובת.",
  }),
  // 17 — Amorphicure pH Magnesium (carbonate, unresolved) — fails
  buildProduct({
    barcode: "7290015429245",
    bucket: FAILS,
    states: ["cannot_verify", "fail", "cannot_verify", "cannot_verify", "cannot_verify", "cannot_verify"],
    doseMg: null,
    doseValueLabel: "לא ניתן לאימות",
    formHe: "קרבונט",
    oneLinerHe:
      "pH מגנזיום, אמורפיקיור — מינון לא ניתן לאימות, קרבונט. לא עובר: הצורה עצמה ידועה בספיגה נמוכה (קרבונט), למרות שהמינון בפועל אינו ניתן לאימות מהתווית.",
  }),
  // 18 — TRIOMAG (undisclosed 3-form blend) — cannot_assess
  buildProduct({
    barcode: "7290118816065",
    bucket: CANNOT,
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
      "TRIOMAG, סופהרב — מינון לא ניתן לאימות, תערובת ציטראט/ביסגליצינט/טאוראט. לא ניתן להעריך: כאן גם הצורה עצמה אינה ידועה, שלושה רכיבים בתערובת בלי יחס מפורסם, כך שאין אפילו ממצא שלילי מוגדר להצביע עליו, רק חוסר מידע מוחלט.",
  }),
];

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
  buyingRuleIntro:
    "בדקנו 18 תוספי מגנזיום מהמדף הישראלי לפי שישה דברים שבאמת קובעים אם תוסף מגנזיום שווה את הכסף. אין צורך להבין כימיה כדי להשתמש בזה, רק לדעת מה לחפש על התווית לפני שמשלמים. שישה דברים קובעים תוסף מגנזיום טוב, ומוצר יכול להיראות מרשים מבחוץ (מספר גדול, שם מדעי, אריזה גדולה) ולהיכשל בכל שישה. זה בדיוק מה שקרה כשבדקנו את 18 המוצרים במדף הישראלי: אף אחד מהם אינו עומד בכל שישה הספים בבת אחת. הפירוט בהמשך.",
  buyingRule: [
    {
      bar: "doseAdequacy",
      explanation:
        "המינון היומי — המספר החשוב הוא כמה מגנזיום יסודי המוצר נותן ביום. משקל התרכובת שכתוב לפעמים באותיות גדולות על הקופסה הוא מספר אחר לגמרי.",
    },
    {
      bar: "formAbsorption",
      explanation: "הצורה הכימית — צורות מגנזיום שונות נספגות בגוף במידה שונה, וההבדל משמעותי.",
    },
    {
      bar: "thirdPartyVerification",
      explanation: "בדיקת צד שלישי — האם מישהו חוץ מהיצרן בדק שמה שכתוב באמת נכון.",
    },
    {
      bar: "priceFairness",
      explanation: "הוגנות המחיר — כמה משלמים על מנה יומית אפקטיבית, ביחס לשאר השוק.",
    },
    {
      bar: "safety",
      explanation: "בטיחות — האם המינון חוצה סף שגורם לאי-נוחות עיכולית.",
    },
    {
      bar: "labelTransparency",
      explanation: "שקיפות התיוג — האם התווית בכלל מאפשרת לדעת כמה מגנזיום יסודי מקבלים.",
    },
  ],
  // headlineFinding.body[0]/[2]/[8]: ROUND-3 rewrites, magnesium_guide_tier_copy_v1.md
  // Slot 5. STATUS: tier copy CLEARED QA gate-2 (2026-07-05) — RT-8
  // (magnesium_guide_tier_copy_redteam_v2.md) resolved: body[2]/body[8] carry zero
  // tier-label words in prose, verified by hebrew_readability.is_clean; GO on record
  // in this task's return (TASK-504 Wave 1). Retire the "הרשימה המעשית להתחיל ממנה"
  // shortlist framing (RT-6) and the RT-5 defect that lumped price-fairness (a Bari
  // collection gap) and third-party-verification (a market-wide fact) into one "data
  // gap" sentence. body[2]/body[8] name ZERO tier words (hebrew_readability.py's
  // `recommendation` HARD-leak kind fails a bare tier word in prose — EXCEPTION-003
  // sanctions the 4 tier words as GUIDE_RECOMMENDATION_TIER_LABELS_HE field values
  // ONLY, never inside a sentence); the two groups are named descriptively and the
  // tier HEADINGS rendered below supply the actual names. body[1] and body[3]-body[7]
  // (the five per-product paragraphs) are UNCHANGED.
  headlineFinding: {
    title: "אף מוצר מגנזיום במדף הישראלי לא עובר את כל ספי הקנייה.",
    body: [
      "מתוך 18 מוצרים שנבדקו, אף אחד לא עומד בכל שישה הספים בבת אחת. הסיבה המרכזית לכך אינה איכות ירודה של המוצרים עצמם. יש כאן שני דברים נפרדים: עדיין לא נאספו נתוני מחיר למוצרי מגנזיום, וזה פער של בארי שיתמלא כשהנתונים ייאספו. בנפרד מזה, אף מותג מגנזיום במדף לא פרסם טענת בדיקת-צד-שלישי כלל. זו עובדה על השוק כולו.",
      "בגלל זה אין היום בחירת ברירת מחדל למגנזיום. כשאף מוצר לא עומד בכל שישה הספים, הדרך ההוגנת היחידה היא להגיד את זה בפה מלא. בחירת מוצר עם הכי פחות דגלים והצגתו כברירת מחדל הייתה יוצרת רושם מטעה.",
      "מה כן אפשר להציג: המוצרים שאף סף לא נכשל אצלם, אבל לכל אחד לפחות דגל אחד לתשומת לב. הם נחלקים לשתי קבוצות שמופיעות בהמשך. אצל חלקם ההסתייגות היחידה היא מינון חלקי, שאפשר להשלים פשוט על ידי לקיחת כמות גדולה יותר. אצל האחרים ההסתייגות נוגעת גם לצורה הכימית או לסף הבטיחות, מעבר לכמות. הכותרות שלמטה מפרטות איזו קבוצה היא איזו, ואלה המוצרים:",
      "מגנזיום ציטראט+B6, סופהרב (250 מ\"ג יסודי, ציטראט). עומד בסף הצורה הכימית וסף שקיפות התיוג במלואם. הדגל: 250 מ\"ג נמוך מ-300 מ\"ג, כך שהמינון עומד בסף חלקי. בנוסף, 250 מ\"ג נמצא בדיוק בגובה הסף הרך המצריך תשומת לב עבור רגישים לאי-נוחות עיכולית.",
      "מגנזיום ביסגליצינט, אלטמן (250 מ\"ג יסודי, ביסגליצינט). אותו פרופיל בדיוק כמו הקודם: צורה כימית ושקיפות עומדות בסף במלואן, המינון עומד בסף חלקי (250 מתוך 300), ואותו סף רך לתשומת לב עיכולית. ביסגליצינט נחשב עדין יותר לקיבה עבור חלק מהאנשים, אבל הראיות שתומכות בכך חלשות יותר מהראיות התומכות בציטראט.",
      "מגנזיום ציטראט 120, אלטמן (200 מ\"ג יסודי, ציטראט). צורה, שקיפות ובטיחות עומדים בסף במלואם (200 מ\"ג נמצא מתחת לסף הרך לתשומת לב עיכולית). הדגל היחיד: המינון (200 מ\"ג) עומד בסף חלקי, רחוק יותר מ-300 מ\"ג מהשניים שלמעלה.",
      'מגנזיום WELL, נוטריקר (168 מ"ג יסודי, ביסגליצינט). צורה, שקיפות ובטיחות עומדים בסף במלואם. הדגל: מינון צנוע יותר (168 מ"ג), מתאים לתחזוקה שוטפת אבל מוגבל אם צריך לסגור פער תזונתי גדול.',
      "אנטי לג קרמפס, NT L.C. (190 מ\"ג יסודי, הידרוקסיד). שקיפות ובטיחות עומדים בסף. שני דגלים כאן: הצורה הכימית (הידרוקסיד) שייכת לרמת ספיגה בינונית בלבד, והמינון (190 מ\"ג) עומד בסף חלקי. חשוב גם לדעת: שם המוצר מבטיח הקלה בעוויתות שרירים, אבל סקירת קוקריין משנת 2020 לא מצאה לכך תמיכה קלינית משמעותית.",
      "אצל כל המוצרים בקבוצות שלמעלה, שני ספים נשארים מחוץ לתמונה: בדיקת צד שלישי והוגנות המחיר. אלה הסיבה שאף מוצר אינו עומד בכל ששת הספים במלואם. מדובר בשני סוגי פער שונים לגמרי: הוגנות המחיר היא פער נתונים של בארי, שיתמלא כשהמחירים ייאספו. בדיקת צד שלישי היא עובדה על השוק כולו: אף מותג מגנזיום לא פרסם טענת בדיקה כזו.",
    ],
  },
  products,
  // TASK-504C — rubric display_suppression_rule. Computed above from the live product
  // array; NOT hardcoded. Currently resolves to [thirdPartyVerification, priceFairness].
  suppressedBars,
  bandExcludedBars,
  // TASK-504C — guide-level disclosure line for the suppressed bars (owner fix #3 +
  // rubric honesty_constraint: "disclosed, never silently vanished"). FINAL COPY —
  // cleared QA gate-2 (2026-07-05, GO on record in this task's return, TASK-504
  // Wave 1); drafted per magnesium_guide_slot_copy_v1.md Slot 2 (RT-2 revised: dated
  // "יתעדכן בעדכון הבא" promise softened to open-timing "כשהנתונים ייאספו" — Product's
  // call A only characterizes Israeli pricing as a tracked fast-follow, not a
  // next-build commitment).
  suppressedBarsDisclosureHe:
    "שני דברים לא מוצגים כרגע בטבלה, אצל כל 18 המוצרים: הוגנות המחיר, כי עדיין לא נאספו נתוני מחיר למוצרי מגנזיום ונוסיף אותה כשהנתונים ייאספו, ובדיקת צד שלישי, כי אף מותג מגנזיום במדף לא פרסם טענת בדיקה כזו כלל.",
  // TASK-504 4-tier build — one caption per RANKED tier (replaces the retired
  // bucketSubCaptions/promotedShortlistLabel, RT-6).
  // STATUS: tier copy CLEARED QA gate-2 (2026-07-05) — RT-8
  // (magnesium_guide_tier_copy_redteam_v2.md) resolved; GO on record in this task's
  // return (TASK-504 Wave 1).
  // magnesium_guide_tier_copy_v1.md Slot 1. Captions are scoped to the DISPLAYED bars
  // only (gate-2 RT-1: neither claims "meets every bar," since price/third-party are
  // suppressed) and name zero raw counts (RT-1 lesson: a tier re-flows on rescore —
  // the live product count renders separately, in the tier header, via
  // GuideProductTable, never baked into a copy string).
  recommendationTierCaptions: {
    very_recommended: "מוצרים שעומדים בכל ספי הקנייה במלואם, בלי אף הסתייגות.",
    recommended:
      "מתוך הספים שהמדריך מציג, ההסתייגות היחידה אצל המוצרים האלה היא מינון שנמוך מהטווח האפקטיבי. אפשר להגיע לטווח הזה על ידי לקיחת כמות יומית גדולה יותר.",
    good: "מוצרים שנוסף על המינון הנמוך, נושאים גם הסתייגות על המוצר עצמו: הצורה הכימית, סף הבטיחות או שקיפות התיוג. הסתייגות כזו לא משתנה כמה שלוקחים.",
    not_recommended: "מוצרים שנכשלים בלפחות אחד מספי הקנייה.",
  },
  // very_recommended (מומלץ מאוד) renders unconditionally even when empty — rubric
  // empty_state_handling: an empty top tier IS the guide's own headline finding, not a
  // display bug to hide.
  // STATUS: tier copy CLEARED QA gate-2 (2026-07-05) — RT-8
  // (magnesium_guide_tier_copy_redteam_v2.md) resolved; GO on record in this task's
  // return (TASK-504 Wave 1). magnesium_guide_tier_copy_v1.md Slot 2.
  veryRecommendedEmptyStateHe:
    "אף מוצר מגנזיום לא עומד היום בכל ספי הקנייה במלואם. זה הממצא המרכזי שהמדריך הזה חושף.",
  // cannot_assess (TRIOMAG) renders in its own out-of-tier section (see
  // guide-product-table.tsx) — this is the section's intro line, DISTINCT from (not a
  // replacement for) the retired bucketSubCaptions.cannot_assess string; the two were
  // near-duplicates and RT-6 retires the bucket-caption field entirely, so only this
  // longer section-intro ships. FINAL COPY — cleared QA gate-2 (2026-07-05, GO on
  // record in this task's return, TASK-504 Wave 1); drafted per
  // magnesium_guide_tier_copy_v1.md Slot 3.
  cannotAssessSectionIntroHe:
    "מוצרים שאי אפשר לדעת אצלם כמה מגנזיום יסודי מגיע בפועל לא נכנסים לאף אחת מארבע הקבוצות למעלה. הסיבה: הצורה הכימית שלהם היא שילוב של כמה סוגי מגנזיום יחד, בלי לפרט את היחס ביניהם. בלי המספר הזה אי אפשר לבדוק אף אחד מהספים האחרים. זהו פער מידע על המוצר עצמו. הוא אינו ממצא שפוסל אותו.",
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
  educationSpine: [
    {
      heading: "התאמת המינון",
      body: [
        'הספרה הרלוונטית היא המגנזיום היסודי ליום. משקל התרכובת (ציטראט, אוקסיד וכו\') שמודפס לפעמים בגדול יותר על הקופסה הוא מספר אחר לגמרי. הספרות המדעית מצביעה על סביבות 300 מ"ג יסודי ליום כדי לקבל ערך משמעותי מתוסף. מוצר שנותן 300 מ"ג ומעלה עומד בסף הזה במלואו. מוצר שנותן פחות, אבל עדיין מעל מחצית הסף (בערך 150 עד 299 מ"ג), נותן ערך אמיתי אך חלקי; הכמות אינה מספיקה כדי לסמוך עליה כמקור עיקרי. מוצר שנותן פחות ממחצית הסף (מתחת ל-150 מ"ג) הוא בעיקר מחווה סמלית: הכמות קטנה מכדי לעשות הבדל אמיתי בתזונה, גם אם הצורה הכימית מצוינת. כשאי אפשר לחשב את המינון היומי בכלל (למשל: מינון לכמוסה בודדת בלי מספר כמוסות ליום), אי אפשר לדעת אם התוסף עומד בסף. זהו פער מידע. הוא אינו פסילה של המוצר.',
      ],
    },
    {
      heading: "צורה כימית וספיגה",
      body: [
        'זה החלק שהתוויות הכי אוהבות להסתיר. ציטראט, אספרטט, לקטט וכלוריד נספגים טוב יותר מאוקסיד: זו אמירה ישירה מגיליון המידע המקצועי של המכון הלאומי לבריאות האמריקאי (NIH ODS) על מגנזיום, שמפרט את ארבע הצורות האלו בשמן. ביסגליצינט (גליצינט) הוא צורה אורגנית שנחשבת נספגת היטב דרך מנגנון ספיגה שונה (כלציה של דו-פפטיד), ומעשית מסווגת יחד עם ציטראט בקבוצת הספיגה הגבוהה. חשוב לדייק: הגיליון המקצועי של NIH אינו מזכיר ביסגליצינט או גליצינט בשמו בכלל, ומחקרים קטנים שבדקו ספיגת ביסגליצינט ישירות נתנו תוצאות מעורבות וחלשות. זו אינה עדות שמאפשרת להציג את ביסגליצינט כשווה-ערך בעוצמת ההוכחה לציטראט, גם אם שתיהן מסווגות באותה קבוצת ספיגה. מלאט, טאוראט והידרוקסיד נספגים בצורה בינונית, טוב יותר מאוקסיד ופחות טוב מציטראט. אוקסיד, קרבונט וגופרתי (סולפט) הם הצורה שנספגת הכי פחות, ולכן גם הכי זולה לייצור; אותו גיליון NIH מונה במפורש את אוקסיד וסולפט כצורות פחות ביו-זמינות. זה הממצא המרכזי של המדריך הזה: מוצר יכול להכיל מינון גדול על הנייר ולתת בפועל ערך נמוך, כי חלק גדול מהמגנזיום פשוט אינו נספג.',
      ],
    },
    {
      heading: "בדיקת צד שלישי",
      body: [
        "יש הבדל בין מוצר שמישהו חיצוני בדק ואישר, מוצר שרק היצרן טוען עליו ועדיין איש לא בדק את הטענה, ומוצר שאין עליו טענה כזו בכלל. חוסר טענת אימות אינו פגם: יצרן שנמנע מלטעון הסמכה שאין לו הוגן יותר מיצרן שטוען הסמכה שלא קיימת. מבין 18 מוצרי המגנזיום שבדקנו, אף אחד לא נשא טענת בדיקת-צד-שלישי שניתן היה לאמת מול מרשם ציבורי. הסיבה לכך היא שאף מותג מגנזיום במדף לא פרסם טענה כזו כלל. זהו פער נתונים במדף כולו. הוא אינו ממצא על איכות המוצרים.",
      ],
    },
    {
      heading: "הוגנות המחיר",
      body: [
        "בודקים מחיר למנה יומית אפקטיבית (מחיר יחסית ל-300 מ\"ג יסודי ליום), מדד שונה ממחיר לאריזה. תוסף שנראה זול לאריזה יכול להיות יקר למנה בפועל אם המינון ליום נמוך. הבדיקה הזו דורשת נתוני מחירים אמיתיים שנאספו במדף. כרגע אין נתוני מחיר עבור אף אחד מ-18 מוצרי המגנזיום שנבדקו, כך שהסף הזה פשוט אינו ניתן להפעלה על הקטגוריה היום. זהו פער נתונים. הוא אינו ממצא על המוצרים עצמם.",
      ],
    },
    {
      heading: "בטיחות",
      body: [
        'הסף העליון שנקבע למגנזיום שמגיע מתוסף (לא ממזון) הוא 350 מ"ג יסודי ליום, לפי המכון הלאומי לבריאות האמריקאי (IOM/NASEM). מוצר שחוצה את הסף הזה מקבל אזהרה גלויה. זו אינה הערת שוליים חבויה. הרשות האירופית לבטיחות מזון קבעה סף רך יותר, 250 מ"ג ליום, במקור בחוות דעת של הוועדה המדעית למזון של האיחוד האירופי (SCF) משנת 2001, ואושרר מחדש בחוות דעת של הפאנל המדעי לתזונה של EFSA משנת 2015. חשוב להבין את שני הסכומים נכון: מדובר בסף לאי-נוחות עיכולית (שלשול קל, זמני). אין כאן רעילות. אנשים בריאים שחוצים את הסף עלולים לחוות אי-נוחות במערכת העיכול. אנשים עם מחלת כליות או שנוטלים תרופות מסוימות צריכים ייעוץ רפואי לפני נטילת מינונים גבוהים, ללא קשר לצורה הכימית.',
      ],
    },
    {
      heading: "שקיפות התיוג",
      body: [
        'זו שאלה שונה מהמינון עצמו: האם התווית בכלל מאפשרת לדעת מה המינון. תווית שקופה נותנת מספר ברור של מגנזיום יסודי, או נותנת את משקל התרכובת יחד עם חישוב יסודי מפורש. תווית פחות שקופה נותנת רק את משקל התרכובת (למשל "700 מ"ג מלאט") בלי לחשב את היסודי בעצמה. אפשר לחשב את זה חיצונית, אבל התווית עצמה לא עשתה את העבודה בשביל הצרכן. מוצר שמזכיר "מגנזיום" בלי שום מספר בשום מקום נכשל בשקיפות באופן מוחלט, בלי קשר אם המינון בפועל טוב או רע.',
      ],
    },
    {
      heading: "מה מגנזיום עושה בפועל",
      body: [
        "מגנזיום הוא מינרל חיוני שמעורב בתפקוד תקין של שרירים, עצבים ובעצם. תוסף מגנזיום נותן ערך אמיתי כשהתזונה אינה מספקת מספיק, בהתאם למינון ולצורה הכימית שנספגת בפועל. חשוב לדייק גם בכיוון ההפוך: הטענה הפופולרית ביותר על מגנזיום, הקלה בעוויתות שרירים, נבדקה בסקירה שיטתית של קוקריין משנת 2020. הסקירה בחנה את המחקרים הקיימים והתוצאה הייתה שלא נמצאה תמיכה קלינית משמעותית. הממצא הזה אינו פוסל את הערך הכללי של מגנזיום. הוא מצביע על כך שהטענה הספציפית הזו, הקלת עוויתות שרירים, אינה מבוססת מספיק כדי לסמוך עליה.",
      ],
    },
    {
      heading: "הצורות הכימיות, מוסבר שוב בקצרה",
      body: [
        "ציטראט, אספרטט, לקטט, כלוריד — הצורות עם ההוכחה החזקה ביותר לספיגה טובה. מקור: הגיליון המקצועי של NIH ODS, שמונה אותן בשמן.",
        "ביסגליצינט (גליצינט) — צורה אורגנית שנחשבת נספגת היטב דרך מנגנון כלציה שונה, ומעשית נכללת באותה קבוצת ספיגה גבוהה. חשוב: ההוכחה הישירה לכך חלשה יותר משל ציטראט, ומחקרים ספציפיים שבדקו את זה נתנו תוצאות מעורבות. זו אינה צורה שווה-ערך לציטראט בעוצמת ההוכחה, גם אם שתיהן נחשבות טובות לספיגה.",
        "מלאט, טאוראט, הידרוקסיד — ספיגה בינונית. טוב יותר מאוקסיד, פחות טוב מציטראט.",
        "אוקסיד, קרבונט, גופרתי (סולפט) — הספיגה הנמוכה ביותר. הצורה הזו זולה לייצור בדיוק בגלל שהגוף סופג ממנה פחות. הגיליון של NIH מונה את אוקסיד וסולפט במפורש כצורות פחות ביו-זמינות.",
      ],
    },
    {
      heading: "מינון ובטיחות",
      body: [
        'הסף העליון שנקבע למגנזיום מתוסף (לא ממזון) הוא 350 מ"ג יסודי ליום, לפי המכון הלאומי לבריאות האמריקאי (IOM/NASEM). מדובר בסף לאי-נוחות עיכולית. אין כאן רעילות. הרשות האירופית לבטיחות מזון (EFSA) קבעה סף רך יותר, 250 מ"ג ליום, שמקורו בחוות דעת של הוועדה המדעית למזון של האיחוד האירופי (SCF) משנת 2001, ואושרר מחדש בחוות דעת של EFSA משנת 2015. שני הסכומים מתארים את אותה תופעה: מינון גבוה מדי של מגנזיום מתוסף עלול לגרום לשלשול קל וזמני. הוא אינו פוגע במערכת הגוף לעומק. אנשים עם מחלת כליות, או שנוטלים תרופות מסוימות, צריכים לדבר עם רופא לפני נטילת מינונים גבוהים, ללא קשר לצורה הכימית של המוצר.',
      ],
    },
    {
      heading: "הממצא שכדאי לזכור",
      body: [
        'אוקסיד מגנזיום הוא הצורה הנפוצה ביותר על המדף הישראלי, וגם הזולה ביותר לייצור, בדיוק בגלל שהגוף סופג ממנה הכי פחות. מספר גדול על האריזה (450 מ"ג, 520 מ"ג) אינו מבטיח ערך גבוה יותר בפועל אם הצורה הכימית מגבילה כמה מגיע לגוף. זו הסיבה שהמדריך הזה מסתכל על מינון וצורה יחד. התייחסות לאחד מהם בנפרד הייתה מטעה.',
      ],
    },
    {
      heading: "מקורות",
      body: [
        "NIH Office of Dietary Supplements — Magnesium Health Professional Fact Sheet. מקור להיררכיית הצורות הכימיות: אספרטט, ציטראט, לקטט וכלוריד נספגים טוב יותר מאוקסיד וגופרתי (סולפט). אומת עצמאית מול ציטוטים משניים מהימנים.",
        'IOM/NASEM, Dietary Reference Intakes (1997). מקור לסף העליון של 350 מ"ג/יום מגנזיום מתוסף (לא ממזון), מבוסס על שלשול כתופעת הלוואי המגבילה.',
        "הוועדה המדעית למזון של האיחוד האירופי (SCF), חוות דעת 2001; EFSA, פאנל NDA, חוות דעת 2015 (אישרור מחדש). מקור לסף הרך של 250 מ\"ג/יום. התאריך שהופיע בעמוד הקודם עבור חוות דעת זו שגוי ותוקן כאן במפורש — התאריכים הנכונים הם 2001 ו-2015 בלבד.",
        "Garrison, S.R. et al., Cochrane Database of Systematic Reviews, 2020 (PMID 32956536). מקור לממצא שלא נמצאה תמיכה קלינית משמעותית להקלת עוויתות שרירים על ידי מגנזיום.",
        'בדיקת ראיות עבור טענת "ביסגליצינט נספג כמו ציטראט": נבדקו שלושה מחקרים קטנים שלעיתים מצוטטים לתמיכה בכך. אחד (מחקר אנושי, 2024) לא הראה עלייה מובהקת ברמות מגנזיום בזרוע הביסגליצינט שלו, וכלל מחברים המזוהים עם יצרן מסחרי של רכיב מתחרה. אחד (2019) הוא מחקר בעכברים בלבד; הוא אינו מחקר בבני אדם. אחד (1994, 12 חולים) הראה יתרון לביסגליצינט רק בתת-קבוצה של ארבעה חולים עם פגיעה חמורה בספיגה מראש; הוא אינו מראה יתרון כזה באוכלוסייה כללית. שלושת המחקרים האלה אינם משמשים כאן כהוכחה לעליונות ביסגליצינט. הם מוזכרים כדי להסביר למה ההוכחה לביסגליצינט חלשה יותר מזו של ציטראט.',
        "בארי קוראת תוויות. בארי אינה בודקת במעבדה. כל המינונים המוצגים הם מה שכתוב על האריזה הישראלית. המידע כאן הוא לצורך היכרות בלבד. הוא אינו תחליף לייעוץ רפואי.",
      ],
    },
  ],
  buyLinkDisclosureLine: "קישור קנייה אינו משפיע על הכללה, על דגלים או על סדר הצגה.",
  updatedLabel: "18 מוצרים · יוני 2026",
};
