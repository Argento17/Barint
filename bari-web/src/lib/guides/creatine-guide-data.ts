// Creatine guide — /madrichim/creatine (TASK-504 Wave 2). Mirrors the shipped
// magnesium golden guide (magnesium-guide-data.ts), adapted for creatine's own
// bar-rubric application.
//
// Ground truth (used EXACTLY, nothing invented — Hard Rule 10 discipline):
//   1. Tier/bucket + per-product bar-state assignments — Product's
//      03_operations/reports/product/creatine_guide_recommendation_tiers_v1.md §4
//      (all 31 rows), CO-SIGNED by Nutrition D7 with ONE data correction in
//      01_framework/nutrition/creatine_guide_tier_cosign_v1.md §3: California Gold
//      Nutrition's price_fairness MUST display CANNOT-VERIFY (never the raw ₪0.97
//      figure — that figure answers "price per gram of active ingredient," not
//      "price per day's effective dose," because the daily capsule count is
//      undisclosed and price_fairness cascades from dose_adequacy's own
//      CANNOT-VERIFY per the rubric's own non-optional cascade rule). Applied here:
//      California Gold Nutrition's priceValueLabel is "לא ניתן לאימות", not a ₪
//      figure, and the Israeli price median used below is the corrected ₪0.96
//      (CGN excluded), not the as-filed ₪0.93.
//   2. Product identity (id/name/brand/imageUrl) + raw badge facts (form_label,
//      dose_label, cert_label, price_per_3g_label) — `creatine-page-data.ts`
//      (`creatineProducts`, the same file at the exact commit both the Product and
//      Nutrition docs pulled: origin/master @ 9546878cf90f069fe12c1467d8d12966b40221cf).
//      Every dose/form/cert/price value below is that file's own literal field,
//      never re-estimated.
//   3. Tier-layer copy (4 tier captions, headline finding, cannot-assess section
//      intro, expander labels) — Content's
//      03_operations/reports/content/creatine_guide_tier_copy_v1.md, GATE 1 ONLY
//      (Adversarial QA / gate 2 sign-off is PENDING, same status as the shipped
//      magnesium guide at its own Wave-1 ship point). Ported VERBATIM.
//
// TWO EXPLICIT GAPS this build does NOT paper over (both content-authorship gaps,
// not Frontend's to fill per the standing content sign-off hard rule — flagged in
// this task's return, not silently resolved):
//   (a) Per-product `oneLinerHe` — no guide-specific copy was authored for creatine's
//       31 products (creatine_guide_tier_copy_v1.md's own not_done list says so
//       explicitly). This file REUSES the existing `rowVerdict` string already
//       shipped (in DRAFT status, same two-gate-pending status) on the live
//       /hashvaot creatine comparison page for each product, verbatim — with ONE
//       exception: California Gold Nutrition's rowVerdict contains the banned
//       "₪0.97 ל-3 גרם (מחושב)" clause (Nutrition's §3 correction above), so that
//       clause is mechanically dropped here, nothing else reworded. This is a port,
//       not new authorship — but it is NOT guide-specific gated copy, and the
//       source page's own header states its content is unsigned draft.
//   (b) `buyingRule[].explanation` (layer-1 "what actually matters" blurbs) and the
//       hub-card `description` — no copy slot for these exists in the gate-1 doc
//       either. The six lines below are short, factual, non-evaluative bar
//       definitions restating already-settled facts (3-5g effective range, the
//       two-tier cert model, "no established UL" — all already established in
//       Nutrition-owned sources), written to the same register as the structural
//       GUIDE_BAR_LABELS_HE names, not narrative Tom-Bari voice. They are UNSIGNED
//       Frontend placeholders pending Content authorship, exactly like (a).
// Route ships `noindex: true` (see page.tsx) reflecting BOTH gaps, mirroring and
// extending the magnesium page's own gate-2-pending noindex treatment.
//
// `isDefaultPick` is deliberately unset on every product: unlike magnesium (empty
// clears_all, explicit no-default-pick headline), creatine's clears_all tier IS
// populated (Thorne/Momentous/BPN) and a "cheapest among all six-bar-clearers"
// claim is a comparative/superlative claim that needs its own sign-off — not
// decided by this build.

import {
  GUIDE_BAR_ORDER,
  type GuideBarKey,
  type GuideBarState,
  type GuideBucket,
  type GuideGaugeGeometry,
  type GuideLadderGeometry,
  type GuidePageVM,
  type GuideProductChannel,
  type GuideProductVM,
} from "@/lib/view-models";
import { tierIndexFromState } from "@/components/guides/threshold-bar-row";
import { computeBandExcludedBars, computeSuppressedBars } from "@/lib/guides/guide-suppression";
import { creatineProducts, creatineEvidenceSections } from "@/lib/comparisons/creatine-page-data";

// ─── Product identity lookup (id/name/brand/imageUrl only — see header) ────────────
function identity(id: string) {
  const p = creatineProducts.find((x) => x.id === id);
  if (!p) {
    throw new Error(`creatine-guide-data: product id ${id} not found in creatine-page-data.ts`);
  }
  return { id: p.id, name: p.name, brand: p.brand ?? null, imageUrl: p.imageUrl ?? null };
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

// ─── Threshold geometry — built for the 4 bars where a fixed external standard is
// scientifically uncontroversial (dose floor, verification-confidence tiers, price
// vs. same-currency median, disclosure completeness). Deliberately NOT built for:
//   - formAbsorption: the rubric/evidence co-sign (creatine_evidence_cosign_v1.md
//     §2.4; creatine_guide_tier_cosign_v1.md §4) explicitly BANS an
//     inferior/lower-quality framing for HCl/alternative forms ("evidence-orphaned
//     for a premium claim," never "lower absorption"). A worst→best ladder with
//     tier names like "low/medium/high" — the literal ask in one delegation
//     phrasing ("alt-forms=lower tier ladder") — would misstate that evidence in
//     exactly the banned direction. Flagged as a spec conflict in this task's
//     return; resolved here by showing form as a plain fact (product's own form
//     name) with NO ranked track, never a fabricated hierarchy.
//   - safety: uniform PASS across all 31 products (creatine has no established
//     upper limit) — a gauge/ladder where every product lands at the identical
//     point adds no information and would look like a broken control. Renders as
//     a plain badge only (the bar's PASS state already says everything there is
//     to say here).
const CREATINE_DOSE_GAUGE: GuideGaugeGeometry = {
  anatomy: "gauge",
  // Headroom past the typical 5g dose (not just past the 3g floor) — most products
  // in this corpus cluster at 5g, so headroom-past-floor-only (mirroring
  // magnesium's 20%-past-floor rule literally) would clamp the corpus's NORM, not
  // its outliers. 6g gives the common 5g dose clean headroom while still placing
  // the 0.75g HCl products deep in the fail zone.
  domainMax: 6,
  zones: [
    { upTo: 1.5, tone: "fail", dividerStyle: "solid", tickLabel: "1.5 (חצי סף)" },
    { upTo: 3, tone: "flag", dividerStyle: "solid", tickLabel: "3 (הסף)" },
    { upTo: 6, tone: "pass", dividerStyle: "solid" },
  ],
};

// Currency-agnostic by construction: the placed VALUE is price ÷ the product's OWN
// -currency median (₪0.96 Israeli / $0.225 worldwide — computed with the correct,
// Nutrition-ruled IL median, never mixed across currencies per the rubric's
// boundary_method and this task's explicit instruction). This is a mechanical unit
// transform of the rubric's own PASS ≤1.25× / FLAG ≤2.0× / FAIL >2.0× bands — not a
// new threshold — which is what lets ONE shared geometry object (the type system:
// GuidePageVM.thresholdGeometry is one entry per BAR, not per currency) serve both
// currencies honestly. At the IL median (₪0.96/3g): PASS ≤ ₪1.20 · FLAG ₪1.20–1.92 · FAIL > ₪1.92.
const CREATINE_PRICE_GAUGE: GuideGaugeGeometry = {
  anatomy: "gauge",
  domainMax: 2.5,
  zones: [
    { upTo: 1.25, tone: "pass", dividerStyle: "solid", tickLabel: "1.25×" },
    { upTo: 2.0, tone: "flag", dividerStyle: "solid", tickLabel: "2×" },
    { upTo: 2.5, tone: "fail", dividerStyle: "solid" },
  ],
};

const CREATINE_THIRD_PARTY_LADDER: GuideLadderGeometry = {
  anatomy: "ladder",
  tiers: [
    { label: "נבדק, ללא רישום תואם במאגר", tone: "fail" },
    { label: "מוצהר, טרם אומת מול מאגר", tone: "flag" },
    { label: "אומת מול מאגר", tone: "pass" },
  ],
};

const CREATINE_LABEL_LADDER: GuideLadderGeometry = {
  anatomy: "ladder",
  tiers: [
    { label: "בלי שום מספר", tone: "fail" },
    { label: "מספר חלקי בלבד", tone: "flag" },
    { label: "מינון יומי ברור", tone: "pass" },
  ],
};

// Note: unlike magnesium's `ladderValueLabel` helper (which falls back to the
// generic tier name for a cannot_verify tier), every product below supplies its own
// specific valueLabel (the actual cert_label / label-transparency fact, verbatim
// from the source data, e.g. "לא נמצאה טענה") for thirdPartyVerification/
// labelTransparency — a more informative, still-honest fact even on a
// cannot_verify row, so no generic-tier-name fallback helper is needed here.

// Same-currency price-fairness medians (Nutrition-ruled, corrected figures —
// creatine_guide_tier_cosign_v1.md §3 for IL; §1 for WW, both independently
// re-derived from the pulled creatine-page-data.ts price labels).
const IL_PRICE_MEDIAN_ILS = 0.96; // ₪/3g, California Gold Nutrition excluded (cascade rule)
const WW_PRICE_MEDIAN_USD = 0.225; // $/3g

// ─── Per-product builder ─────────────────────────────────────────────────────────────
function buildProduct(opts: {
  barcode: string;
  bucket: GuideBucket;
  /** [doseAdequacy, formAbsorption, thirdPartyVerification, priceFairness, safety, labelTransparency] */
  states: [GuideBarState, GuideBarState, GuideBarState, GuideBarState, GuideBarState, GuideBarState];
  doseGrams: number | null;
  doseValueLabel: string;
  formValueLabel: string;
  thirdPartyValueLabel: string;
  price: { currency: "ILS" | "USD"; amount: number } | null;
  priceValueLabel: string;
  labelValueLabel: string;
  oneLinerHe: string;
  channel?: GuideProductChannel | null;
}): GuideProductVM {
  const barsResult = bars(...opts.states);
  const byKey = new Map(barsResult.map((b) => [b.bar, b] as const));
  const thirdPartyTier = tierIndexFromState(byKey.get("thirdPartyVerification")!.state);
  const labelTier = tierIndexFromState(byKey.get("labelTransparency")!.state);
  const priceRatio = opts.price
    ? opts.price.amount / (opts.price.currency === "ILS" ? IL_PRICE_MEDIAN_ILS : WW_PRICE_MEDIAN_USD)
    : null;

  return {
    ...identity(opts.barcode),
    bucket: opts.bucket,
    bars: barsResult,
    benchmarks: {
      doseAdequacy: {
        value: opts.doseGrams,
        clamped: opts.doseGrams !== null && opts.doseGrams > CREATINE_DOSE_GAUGE.domainMax,
        valueLabel: opts.doseValueLabel,
      },
      // No geometry entry for this bar (see header) — valueLabel-only placement
      // still renders as an honest plain-text caption ("המוצר: {form}"), never a
      // ranked track.
      formAbsorption: {
        valueLabel: opts.formValueLabel,
      },
      thirdPartyVerification: {
        tierIndex: thirdPartyTier,
        valueLabel: opts.thirdPartyValueLabel,
      },
      priceFairness: {
        value: priceRatio,
        clamped: priceRatio !== null && priceRatio > CREATINE_PRICE_GAUGE.domainMax,
        valueLabel: opts.priceValueLabel,
      },
      labelTransparency: {
        tierIndex: labelTier,
        valueLabel: opts.labelValueLabel,
      },
      // safety: no benchmark entry — uniform PASS, no geometry (see header).
    },
    pricing: null,
    buyUrl: null,
    oneLinerHe: opts.oneLinerHe,
    channel: opts.channel ?? null,
  };
}


const DOMESTIC_CHANNEL_BY_BARCODE: Record<string, GuideProductChannel> = {
  "733739020383": "import_iherb",
  "5056555204153": "import_iherb",
  "631656705737": "import_iherb",
  "5055534302002": "import_myprotein",
  "7290019766223": "domestic_shelf",
  "748927023855": "import_iherb",
  "693749006350": "import_iherb",
  "898220022830": "import_iherb",
  "myprotein-creatine-gummies": "import_myprotein",
  "myprotein-creatine-elite": "import_myprotein",
  "myprotein-creatine-creapure": "import_myprotein",
  "850045966478": "import_iherb",
  "682676700646": "import_iherb",
  "myprotein-creapure-capsules": "import_myprotein",
  "7290014386006": "domestic_shelf",
  "7290016392005": "domestic_shelf",
  "7290010081288": "domestic_shelf",
  "myprotein-creatine-tablets": "import_myprotein",
  "7290122852677": "domestic_shelf",
  "7290014386013": "domestic_shelf",
  "7290120937000": "domestic_shelf",
  "7290014386396": "domestic_shelf",
  "7290122852837": "domestic_shelf",
  "7290001066775": "domestic_shelf",
  "7290018534427": "domestic_shelf",
  "810100920517": "domestic_shelf",
};

function withDomesticChannels(products: GuideProductVM[]): GuideProductVM[] {
  return products.map((product) => ({
    ...product,
    channel: product.channel ?? DOMESTIC_CHANNEL_BY_BARCODE[product.id] ?? null,
  }));
}

const CLEARS: GuideBucket = "clears_all";
const PW: GuideBucket = "passes_with_flag";
const FAILS: GuideBucket = "fails";
const CANNOT: GuideBucket = "cannot_assess";

const LABEL_CLEAR = "מספר גרם מדויק על התווית";
const LABEL_PARTIAL = "מספר לכמוסה, בלי כמות יומית";
const LABEL_NONE = "אין מספר גרם כלל";

// Sunwarrior (810100920517): barcode confirmed via bella-natura.net (independent Israeli retailer) + UPC-A checksum; added to the domestic array below.

const domesticProductsRaw: GuideProductVM[] = [
  // ═══ Israeli shelf (18) ═══
  // 1 — NOW Foods Sports Micronized Creatine — good (caveat: third-party)
  buildProduct({
    barcode: "733739020383",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 4.2,
    doseValueLabel: "4.2 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 0.52 },
    priceValueLabel: "₪0.52 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 4.2 גרם מונוהידראט. ₪0.52 ל-3 גרם, המחיר הנמוך ביותר במדף.",
  }),
  // 2 — ABE Creatine Monohydrate Micronized — good
  buildProduct({
    barcode: "5056555204153",
    bucket: PW,
    states: ["pass", "pass", "flag", "pass", "pass", "pass"],
    doseGrams: 4.25,
    doseValueLabel: "4.25 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed Sport)",
    price: { currency: "ILS", amount: 0.65 },
    priceValueLabel: "₪0.65 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 4.25 גרם מונוהידראט. Informed Sport מוצהר (לא אומת מול מאגר). ₪0.65 ל-3 גרם.",
  }),
  // 3 — MuscleTech Platinum 100% Creatine — good
  buildProduct({
    barcode: "631656705737",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה (רק בדיקת HPLC מוצהרת)",
    price: { currency: "ILS", amount: 0.77 },
    priceValueLabel: "₪0.77 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 5 גרם מונוהידראט. טענת HPLC בלבד. זו אינה בדיקת צד-שלישי מוסמכת. ₪0.77 ל-3 גרם.",
  }),
  // 4 — MyProtein Impact Creatine (250g) — good
  buildProduct({
    barcode: "5055534302002",
    bucket: PW,
    states: ["pass", "pass", "flag", "pass", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed Choice)",
    price: { currency: "ILS", amount: 1.03 },
    priceValueLabel: "₪1.03 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 3 גרם מונוהידראט, ברצפת הטווח שנחקר. Informed Choice מוצהר. ₪1.03 ל-3 גרם.",
  }),
  // 5 — All In אבקת קריאטין — good (caveat: third-party, price)
  buildProduct({
    barcode: "7290019766223",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 1.2 },
    priceValueLabel: "₪1.20 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 3 גרם מונוהידראט. ₪1.20 ל-3 גרם. ללא טענת בדיקת צד-שלישי.",
  }),
  // 6 — Optimum Nutrition Micronized Creatine Powder — good
  buildProduct({
    barcode: "748927023855",
    bucket: PW,
    states: ["pass", "pass", "flag", "pass", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed Choice)",
    price: { currency: "ILS", amount: 0.61 },
    priceValueLabel: "₪0.61 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 5 גרם מונוהידראט. Informed Choice מוצהר. ₪0.61 ל-3 גרם.",
  }),
  // 7 — Thorne (IL/iHerb) Creatine — good
  buildProduct({
    barcode: "693749006350",
    bucket: PW,
    states: ["pass", "pass", "flag", "pass", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (NSF Certified for Sport, הרישום הישראלי לא נבדק בנפרד)",
    price: { currency: "ILS", amount: 0.89 },
    priceValueLabel: "₪0.89 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport מוצהר (הרישום האמריקאי אומת בטבלת הייחוס העולמית; רישום ה-iHerb הישראלי לא נבדק בנפרד). ₪0.89 ל-3 גרם.",
  }),
  // 8 — California Gold Nutrition Sport Pure Creatine (capsules) — cannot_assess
  // Nutrition-ruled correction (cosign §3): price_fairness CANNOT-VERIFY, never
  // ₪0.97. oneLinerHe below is the source rowVerdict with that exact clause
  // mechanically dropped — see file header.
  buildProduct({
    barcode: "898220022830",
    bucket: CANNOT,
    states: ["cannot_verify", "pass", "flag", "cannot_verify", "pass", "flag"],
    doseGrams: null,
    doseValueLabel: "0.75 גרם לכמוסה",
    formValueLabel: "מונוהידראט (כמוסות)",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (iTested)",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_PARTIAL,
    oneLinerHe: "מוצהר, מתחת לרצפה — 0.75 גרם לכמוסה בודדת; כמות הכמוסות היומית לא מפורטת.",
  }),
  // 9 — MyProtein Creatine Gummies — good
  buildProduct({
    barcode: "myprotein-creatine-gummies",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3 גרם (3×1 גרם גומי)",
    formValueLabel: "מונוהידראט (גומי)",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מינון הוגן — 3 גרם מונוהידראט (3×1 גרם גומי). מחיר לגרם אפקטיבי לא חושב (סופר כמות חבילה לא מלאה בדוח המקור).",
  }),
  // 10 — MyProtein Creatine Monohydrate Elite (IL) — good
  buildProduct({
    barcode: "myprotein-creatine-elite",
    bucket: PW,
    states: ["pass", "pass", "flag", "cannot_verify", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3 גרם",
    formValueLabel: "מונוהידראט (כללי)",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed Choice)",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 3 גרם מונוהידראט כללי (לא Creapure). Informed Choice מוצהר.",
  }),
  // 11 — MyProtein THE Creatine Creapure (IL) — good
  buildProduct({
    barcode: "myprotein-creatine-creapure",
    bucket: PW,
    states: ["pass", "pass", "flag", "cannot_verify", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3 גרם",
    formValueLabel: "מונוהידראט (Creapure)",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed Choice)",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 3 גרם מונוהידראט Creapure. Informed Choice מוצהר.",
  }),
  // 12 — Kaged Creatine HCl — not_recommended (dose FAIL + price FAIL)
  buildProduct({
    barcode: "850045966478",
    bucket: FAILS,
    states: ["fail", "flag", "flag", "fail", "pass", "pass"],
    doseGrams: 0.75,
    doseValueLabel: "0.75 גרם",
    formValueLabel: "HCl",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed Sport)",
    price: { currency: "ILS", amount: 4.75 },
    priceValueLabel: "₪4.75 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מוצהר, מתחת לרצפה — 0.75 גרם HCl. ₪4.75 ל-3 גרם, פי כמה יקר יותר ממונוהידראט באותו מינון אפקטיבי.",
  }),
  // 13 — Con-Cret Creatine HCl — not_recommended
  buildProduct({
    barcode: "682676700646",
    bucket: FAILS,
    states: ["fail", "flag", "flag", "fail", "pass", "pass"],
    doseGrams: 0.75,
    doseValueLabel: "0.75 גרם",
    formValueLabel: "HCl",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (NSF Certified for Sport, ה-SKU הישראלי לא נבדק בנפרד)",
    price: { currency: "ILS", amount: 5.38 },
    priceValueLabel: "₪5.38 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מוצהר, מתחת לרצפה — 0.75 גרם HCl. ₪5.38 ל-3 גרם, המחיר הגבוה ביותר לגרם אפקטיבי במדף.",
  }),
  // 14 — MyProtein Creapure Micronised Capsules — good (caveat: dose, 3rd-party, price)
  buildProduct({
    barcode: "myprotein-creapure-capsules",
    bucket: PW,
    states: ["flag", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseGrams: 2.8,
    doseValueLabel: "2.8 גרם",
    formValueLabel: "מונוהידראט (Creapure, כמוסות)",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מוצהר, מתחת לרצפה — 2.8 גרם מונוהידראט Creapure, מתחת לרצפת ה-3 גרם.",
  }),
  // 15 — Super Effect קריאטין מונוהידראט ענבים — not_recommended (zero quantification)
  buildProduct({
    barcode: "7290014386006",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseGrams: 3.1,
    doseValueLabel: "3.1 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 3.1 גרם",
  }),
  // 16 — Super Effect קריאטין מונוהידראט פירות — not_recommended
  buildProduct({
    barcode: "7290016392005",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseGrams: 3.1,
    doseValueLabel: "3.1 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 3.1 גרם",
  }),
  // 17 — Sport GS אבקת קריאטין מונוהידראט — good (caveat: third-party, price)
  buildProduct({
    barcode: "7290010081288",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "cannot_verify", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 3.0 גרם",
  }),
  // 18 — MyProtein Creatine Monohydrate Tablets — not_recommended
  buildProduct({
    barcode: "myprotein-creatine-tablets",
    bucket: FAILS,
    states: ["cannot_verify", "pass", "cannot_verify", "cannot_verify", "pass", "fail"],
    doseGrams: null,
    doseValueLabel: "לא מפורט",
    formValueLabel: "מונוהידראט (טבליות)",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_NONE,
    oneLinerHe: "לא מפורט — התווית לא מציינת מספר גרם קריאטין למנה. מוצר טבליות מיובא.",
  }),


  // 19 — Life מונוהידראט (Super-Pharm) — recommended empty-caveat
  buildProduct({
    barcode: "7290122852677",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3.0 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 0.9 },
    priceValueLabel: "₪0.90 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 3.0 גרם",
  }),
  // 20 — Super Effect תפוח — recommended empty-caveat
  buildProduct({
    barcode: "7290014386013",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 3.1,
    doseValueLabel: "3.1 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 0.96 },
    priceValueLabel: "₪0.96 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 3.1 גרם",
  }),
  // 21 — Life ALL IN 80 — good (price flag)
  buildProduct({
    barcode: "7290120937000",
    bucket: PW,
    states: ["pass", "cannot_verify", "cannot_verify", "flag", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3.0 גרם",
    formValueLabel: "לא צוין מפורט על התווית",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 1.37 },
    priceValueLabel: "₪1.37 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 3.0 גרם",
  }),
  // 22 — Super Effect ללא טעם — recommended dose-only
  buildProduct({
    barcode: "7290014386396",
    bucket: PW,
    states: ["flag", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 2.5,
    doseValueLabel: "2.5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 0.96 },
    priceValueLabel: "₪0.96 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 2.5 גרם",
  }),
  // 23 — Life ALL IN ענבים 240 — cannot_assess
  buildProduct({
    barcode: "7290122852837",
    bucket: CANNOT,
    states: ["cannot_verify", "cannot_verify", "cannot_verify", "cannot_verify", "pass", "cannot_verify"],
    doseGrams: null,
    doseValueLabel: "לא ניתן לאימות",
    formValueLabel: "לא ניתן לאימות",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: "לא ניתן לאימות",
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט",
  }),
  // 24 — Nutri Care קריאטין מונוהידראט 250 גרם — recommended empty-caveat
  buildProduct({
    barcode: "7290001066775",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3.0 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 1.08 },
    priceValueLabel: "₪1.08 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 3.0 גרם",
  }),
  // 25 — Extreme Nutrition קריאטין מונוהידרט Badatz — recommended dose-only
  buildProduct({
    barcode: "7290018534427",
    bucket: PW,
    states: ["flag", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 2.5,
    doseValueLabel: "2.5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 0.57 },
    priceValueLabel: "₪0.57 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט, 2.5 גרם",
  }),
  // 26 — Sunwarrior אבקת קריאטין מונוהידראט טבעונית 300 גרם — recommended empty-caveat
  buildProduct({
    barcode: "810100920517",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "pass", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3.0 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "לא נמצאה טענה",
    price: { currency: "ILS", amount: 1.2 },
    priceValueLabel: "₪1.20 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    channel: "domestic_shelf",
    oneLinerHe: "מונוהידראט טבעוני, 3.0 גרם",
  }),
];

const benchmarkProducts: GuideProductVM[] = [
  // ═══ Worldwide benchmark (13) ═══
  // 19 — Thorne (worldwide) Creatine Micronized — very_recommended (clears all 6)
  buildProduct({
    barcode: "wb-thorne-creatine",
    bucket: CLEARS,
    states: ["pass", "pass", "pass", "pass", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "אומת מול מאגר (NSF, id 1204244)",
    price: { currency: "USD", amount: 0.27 },
    priceValueLabel: "~$0.27 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר. ~$0.27 ל-3 גרם.",
  }),
  // 20 — Momentous Creatine Monohydrate — very_recommended
  buildProduct({
    barcode: "wb-momentous-creatine",
    bucket: CLEARS,
    states: ["pass", "pass", "pass", "pass", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט (לא Creapure)",
    thirdPartyValueLabel: "אומת מול מאגר (NSF, id 1285010)",
    price: { currency: "USD", amount: 0.225 },
    priceValueLabel: "~$0.19–0.26 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מינון הוגן — 5 גרם מונוהידראט (לא Creapure, לפי דף המותג). NSF אומת מול מאגר. ~$0.19–0.26 ל-3 גרם.",
  }),
  // 21 — Klean Athlete Klean Creatine — good (caveat: price not collected)
  buildProduct({
    barcode: "wb-klean-athlete-creatine",
    bucket: PW,
    states: ["pass", "pass", "pass", "cannot_verify", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "אומת מול מאגר (NSF, id 1121640)",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר.",
  }),
  // 22 — BPN Creatine Monohydrate — very_recommended
  buildProduct({
    barcode: "wb-bpn-creatine",
    bucket: CLEARS,
    states: ["pass", "pass", "pass", "pass", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "אומת מול מאגר (NSF, id 1635096)",
    price: { currency: "USD", amount: 0.185 },
    priceValueLabel: "~$0.16–0.21 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר. ~$0.16–0.21 ל-3 גרם.",
  }),
  // 23 — MegaFood Micronized Creatine Monohydrate — good
  buildProduct({
    barcode: "wb-megafood-creatine",
    bucket: PW,
    states: ["pass", "pass", "pass", "cannot_verify", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "אומת מול מאגר (NSF)",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר.",
  }),
  // 24 — Sports Research Creatine Monohydrate Unflavored — good
  buildProduct({
    barcode: "wb-sports-research-creatine",
    bucket: PW,
    states: ["pass", "pass", "pass", "cannot_verify", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "אומת מול מאגר (NSF, id 1751614)",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר. מחיר לא נאסף בסבב זה.",
  }),
  // 25 — BioSteel Creatine (72 servings) — recommended (sole caveat: dose)
  buildProduct({
    barcode: "wb-biosteel-creatine",
    bucket: PW,
    states: ["flag", "pass", "pass", "pass", "pass", "pass"],
    doseGrams: 2.5,
    doseValueLabel: "2.5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "אומת מול מאגר (NSF, id 1292599)",
    price: { currency: "USD", amount: 0.205 },
    priceValueLabel: "~$0.17–0.24 ל-3 גרם (במנה בודדת)",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מוצהר, מתחת לרצפה — 2.5 גרם למדידה יחידה, מתחת לרצפת ה-3 גרם. NSF Certified for Sport אומת מול מאגר.",
  }),
  // 26 — Naked Nutrition Naked Creatine — not_recommended (3rd-party FAIL: checked, not found)
  buildProduct({
    barcode: "wb-naked-creatine",
    bucket: FAILS,
    states: ["pass", "pass", "fail", "pass", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: 'מוצהר על-ידי היצרן ("NSF-certified"). לא נמצא רישום תואם במאגר.',
    price: { currency: "USD", amount: 0.195 },
    priceValueLabel: "~$0.17–0.22 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מינון הוגן — 5 גרם מונוהידראט. טענת NSF מוצהרת. לא נמצא רישום תואם במאגר. ~$0.17–0.22 ל-3 גרם.",
  }),
  // 27 — Applied Nutrition Creatine Monohydrate 100% — good
  buildProduct({
    barcode: "wb-applied-nutrition-creatine",
    bucket: PW,
    states: ["pass", "pass", "flag", "pass", "pass", "pass"],
    doseGrams: 5.0,
    doseValueLabel: "5 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed-Sport, אתר הבודק חסם גישה לאימות)",
    price: { currency: "USD", amount: 0.165 },
    priceValueLabel: "~$0.14–0.19 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מינון הוגן — 5 גרם מונוהידראט. Informed-Sport מוצהר (לא ניתן לאימות — אתר הבודק חסם גישה). ~$0.14–0.19 ל-3 גרם.",
  }),
  // 28 — MyProtein (worldwide) Creatine Monohydrate Elite — good
  buildProduct({
    barcode: "wb-myprotein-elite",
    bucket: PW,
    states: ["pass", "pass", "flag", "flag", "pass", "pass"],
    doseGrams: 3.4,
    doseValueLabel: "3.4 גרם",
    formValueLabel: "מונוהידראט (כללי)",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed-Sport)",
    price: { currency: "USD", amount: 0.37 },
    priceValueLabel: "~$0.37 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מינון הוגן — 3.4 גרם מונוהידראט כללי (לא Creapure). Informed-Sport מוצהר. ~$0.37 ל-3 גרם.",
  }),
  // 29 — MyProtein THE Creatine (Creapure), worldwide — good
  buildProduct({
    barcode: "wb-myprotein-creapure",
    bucket: PW,
    states: ["pass", "pass", "flag", "flag", "pass", "pass"],
    doseGrams: 3.4,
    doseValueLabel: "3.4 גרם",
    formValueLabel: "מונוהידראט (Creapure)",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (Informed Choice)",
    price: { currency: "USD", amount: 0.44 },
    priceValueLabel: "~$0.44 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 3.4 גרם מונוהידראט Creapure. Informed Choice מוצהר. ~$0.44 ל-3 גרם.",
  }),
  // 30 — Switch Nutrition Perform Purest Creatine — good
  buildProduct({
    barcode: "wb-switch-nutrition-creatine",
    bucket: PW,
    states: ["pass", "pass", "flag", "cannot_verify", "pass", "pass"],
    doseGrams: 3.0,
    doseValueLabel: "3 גרם",
    formValueLabel: "מונוהידראט",
    thirdPartyValueLabel: "מוצהר על-ידי היצרן (HASTA, מאגר לא נבדק)",
    price: null,
    priceValueLabel: "לא ניתן לאימות",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe: "מינון הוגן — 3 גרם מונוהידראט, ברצפת הטווח שנחקר. HASTA מוצהר (מאגר לא נבדק).",
  }),
  // 31 — ESN Ultrapure Creatine Monohydrate — good
  buildProduct({
    barcode: "wb-esn-creatine",
    bucket: PW,
    states: ["pass", "pass", "cannot_verify", "flag", "pass", "pass"],
    doseGrams: 3.5,
    doseValueLabel: "3.5 גרם",
    formValueLabel: "מונוהידראט, מיקרופיין",
    thirdPartyValueLabel: "לא מוסמך (ללא טענה)",
    price: { currency: "USD", amount: 0.34 },
    priceValueLabel: "~$0.34 ל-3 גרם",
    labelValueLabel: LABEL_CLEAR,
    oneLinerHe:
      "מינון הוגן — 3.5 גרם מונוהידראט. ללא טענת בדיקת צד-שלישי (מוצג כהשוואה הוגנת. אין כאן חיסרון מוסתר). ~$0.34 ל-3 גרם.",
  }),
];

// ─── Display suppression — computed fresh, never hardcoded. Per the Product/
// Nutrition docs this resolves to [] for creatine (unlike magnesium's 2 of 6):
// no bar is CANNOT-VERIFY across all 31 products (safety is uniform PASS, not
// uniform CANNOT-VERIFY, so the guardrail correctly does not suppress it either).
const domesticProducts = withDomesticChannels(domesticProductsRaw);
const allProducts = [...domesticProducts, ...benchmarkProducts];
const suppressedBars = computeSuppressedBars(allProducts, GUIDE_BAR_ORDER);
const bandExcludedBars = computeBandExcludedBars(domesticProducts, GUIDE_BAR_ORDER);

export const creatineGuide: GuidePageVM = {
  slug: "creatine",
  h1: "איך לבחור קריאטין",
  subtitle: null,
  // Hero mascot asset is LIVE at the path below — a fitness scene (Lumo flexing in a
  // green cape beside a creatine tub, a dumbbell/kettlebell, and a scoop of powder).
  // The Slot-4 draft in creatine_guide_tier_copy_v1.md described a DIFFERENT scene
  // ("examining through a magnifying glass") that was never the actual image — that
  // was a placeholder written before the real asset existed. Re-authored here against
  // the real file (TASK-504 Content gate-1, 2026-07-05), verified by direct visual
  // inspection. Describes the physical scene only; does not restate the tub's printed
  // "STRENGTH/PERFORMANCE/POWER" text as a Bari claim, and makes no efficacy assertion.
  heroImage: {
    src: "/mascots/mascot-lumo-creatine-guide.webp",
    alt: "לומו, דמות בארי, לבוש גלימה ירוקה ומכופף את הזרוע בתנוחת כוח, יד אחת מונחת על קופסת אבקת קריאטין מונוהידראט. לצידו משקולת יד, קטלבל וכף מדידה עם אבקה לבנה.",
    width: 1280,
    height: 1024,
  },
  // No gate-1 copy exists for this slot (see file header gap (b)) — left null
  // rather than invented.
  buyingRuleIntro: null,
  // UNSIGNED Frontend placeholder (file header gap (b)) — short, factual,
  // non-evaluative bar definitions restating already-settled facts; pending
  // Content authorship + two-gate sign-off before this guide is indexable.
  buyingRule: [
    {
      bar: "doseAdequacy",
      explanation: "המינון היומי — כמה גרם קריאטין המוצר נותן במנה, מול הטווח שנחקר: 3 עד 5 גרם ליום.",
    },
    {
      bar: "formAbsorption",
      explanation:
        "הצורה הכימית — מונוהידראט היא הצורה שרוב המחקר נעשה עליה. צורות אחרות אינן מזיקות או נחותות, אך חסרה להן עדות אנושית ליתרון על פני המונוהידראט.",
    },
    {
      bar: "thirdPartyVerification",
      explanation: "בדיקת צד שלישי — האם מישהו חוץ מהיצרן בדק שמה שכתוב באמת נכון, ואם הבדיקה אומתה ישירות מול מאגר הבודק.",
    },
    {
      bar: "priceFairness",
      explanation: "הוגנות המחיר — כמה עולה גרם קריאטין אפקטיבי, ביחס לחציון המחירים באותו מטבע.",
    },
    {
      bar: "safety",
      explanation: "בטיחות — לא נקבע גבול עליון מבוסס לקריאטין.",
    },
    {
      bar: "labelTransparency",
      explanation: "שקיפות התיוג — האם התווית מציינת מספר גרם ברור למנה, או משאירה את המינון בפועל לא ידוע.",
    },
  ],
  products: domesticProducts,
  benchmarkProducts,
  bandExcludedBars,
  suppressedBars,
  // GATE-1 FINALIZED (Content Agent, TASK-504, 2026-07-05) — pending Adversarial QA
  // gate-2 sign-off. Finalizes Nutrition's structural draft: fixed a typo
  // ("בכטריס" -> "בכרטיס"), split the run-on sentence that used its em-dash as a
  // connector into two plain sentences (house rule: max one em-dash per paragraph,
  // never as a connector — this version uses zero), and standardized the term to
  // "מאגר בדיקת צד שלישי" throughout, matching headlineFinding's own exact wording
  // instead of the draft's inconsistent "מאגר בדיקה עצמאי".
  domesticBandsDisclosureHe:
    "מדף המוצרים הישראלי מדורג לפי ארבעה דברים: מינון, צורה כימית, הוגנות מחיר ושקיפות תיוג. אלה הדברים שאפשר לבדוק ולהשוות ישירות מהתווית ומהמחיר. אימות מול מאגר בדיקת צד שלישי אינו משפיע על הדירוג כאן, כי אף מוצר מהמדף הישראלי לא נושא היום רישום כזה. חלק מהמוצרים מציגים טענת בדיקה בעמוד היצרן, בלי אימות מול המאגר. הטענות עצמן עדיין מופיעות בכרטיס של כל מוצר. להשוואה מול מוצרים שכן אומתו מול מאגר בדיקת צד שלישי, אפשר לראות למטה את מוצרי הייחוס העולמיים.",
  benchmarkSectionHeadingHe:
    "מוצרי ייחוס עולמיים: תקן העולם שאומת מול מאגר עצמאי. מוצרים אלה לא נמכרים על מדף התוספים הישראלי.",
  // suppressedBars is empty for creatine, so no disclosure line is needed (the
  // guide-product-table only renders this when both a non-empty suppressedBars AND
  // this string are present).
  suppressedBarsDisclosureHe: null,
  // Slot 2 — headline finding. VERBATIM from creatine_guide_tier_copy_v1.md (gate 1
  // only; gate 2 pending, same as every other string on this page).
  headlineFinding: {
    title: "אף מוצר הזמין בישראל לא אומת מול מאגר בדיקת צד שלישי.",
    body: [
      "מתוך 26 תוספי קריאטין הזמינים בישראל (12 על מדפי הרשתות ו-14 בהזמנה מחו״ל דרך iHerb או MyProtein) ו-13 מותגי ייחוס עולמיים שנבדקו, שבעה מהמותגים העולמיים אומתו ישירות מול מאגר NSF Certified for Sport. אף אחד מ-26 המוצרים הזמינים בישראל לא אומת מול מאגר כזה. חלקם מציגים טענת בדיקה בדף המותג בלבד בלי אימות מול המאגר עצמו, וחלקם לא נושאים טענת בדיקה כלל.",
      "בדיקת צד שלישי היא רק אחד מששה דברים שהמדריך בודק. מוצר מהמדף הישראלי יכול להיות חזק מאוד במינון, בצורה הכימית ובשקיפות התיוג, ועדיין להישאר מחוץ לבדיקה העצמאית פשוט כי אף גוף הסמכה עדיין לא בדק אותו. זהו פער בתשתית הבדיקה של השוק הישראלי. הוא אינו ממצא על איכות המוצרים עצמם. ברגע שמוצר מהמדף הישראלי יעבור בדיקה כזו ויאומת מול מאגר עצמאי, הוא יוכל לעמוד באותם ספי קנייה כמו מותגי הייחוס העולמיים.",
    ],
  },
  // Slot 1 — 4 tier captions. VERBATIM.
  recommendationTierCaptions: {
    very_recommended: "מוצרים שעומדים בכל ספי הקנייה במלואם, בלי אף הסתייגות.",
    recommended:
      "ההסתייגות היחידה אצל המוצרים האלה היא מינון שנמוך מהטווח שנחקר. אפשר להגיע לטווח הזה על ידי לקיחת כמות יומית גדולה יותר.",
    good: "מוצרים שנושאים הסתייגות על המוצר עצמו, מעבר לשאלת המינון: בדיקת צד שלישי שטרם אומתה מול מאגר עצמאי, הוגנות המחיר, ולעיתים גם מינון חלקי לצידן. הסתייגות כזו לא משתנה כמה שלוקחים.",
    not_recommended: "מוצרים שנכשלים בלפחות אחד מספי הקנייה.",
  },
  // CORRECTION (TASK-504 Content gate-1, 2026-07-05): the comment this replaced said
  // very_recommended "is populated for creatine (3 products)" and left this field null
  // on that basis. That populated count (Thorne/Momentous/BPN) is the WORLDWIDE
  // benchmark group, rendered in the separate `benchmarkProducts` section below —
  // never through this domestic tier table. `GuideProductTable` receives `products:
  // domesticProducts` only (see guide-page-template.tsx), and zero of those 25 rows
  // carry the clears_all bucket (third_party_verification is never PASS on the
  // Israeli shelf, per headlineFinding above). So this tier renders EMPTY on the
  // actual page and was silently falling back to the generic very_recommended
  // caption with no explanation of why — flagged and fixed here, not left in place.
  veryRecommendedEmptyStateHe:
    "אף מוצר מהמדף הישראלי לא עומד היום בכל ספי הקנייה במלואם. הסיבה זהה אצל כולם: אף מוצר אינו מאומת מול מאגר בדיקת צד שלישי, גם אצל המוצרים שעומדים בכל שאר חמשת הספים במלואם.",
  // Slot 3 — cannot-assess section intro. VERBATIM.
  cannotAssessSectionIntroHe:
    "מוצרים שמפרטים כמות קריאטין לכמוסה או למנה בודדת, אבל לא מציינים כמה כמוסות או מנות לוקחים ביום. מוצרים כאלה לא נכנסים לאף אחת מארבע הקבוצות למעלה. בלי מספר הכמוסות היומי אי אפשר לדעת כמה קריאטין מגיע בפועל ביום, וגם אי אפשר לבדוק את הוגנות המחיר למנה יומית. זהו פער מידע על המוצר עצמו. הוא אינו ממצא שפוסל אותו.",
  // Slot 5 — expander labels. VERBATIM (identical to magnesium's shipped copy).
  expanderLabels: {
    collapsed: "הצג את הסולמות",
    expanded: "הסתר את הסולמות",
  },
  thresholdGeometry: {
    doseAdequacy: CREATINE_DOSE_GAUGE,
    thirdPartyVerification: CREATINE_THIRD_PARTY_LADDER,
    priceFairness: CREATINE_PRICE_GAUGE,
    labelTransparency: CREATINE_LABEL_LADDER,
    // formAbsorption, safety: no geometry (see header + gauge-const comments).
  },
  // Ported verbatim from creatineEvidenceSections (creatine-page-data.ts) — the same
  // reuse discipline as oneLinerHe above (a port of already-existing, DRAFT-status
  // text, not new authorship). {id, heading, paragraphs} -> {heading, body} is a
  // pure field rename, no wording touched.
  educationSpine: creatineEvidenceSections.map((section) => ({
    heading: section.heading,
    body: section.paragraphs,
  })),
  buyLinkDisclosureLine: "קישור קנייה אינו משפיע על הכללה, על דגלים או על סדר הצגה.",
  updatedLabel: "26 זמינים בישראל · 13 ייחוס עולמי · יולי 2026",
};
