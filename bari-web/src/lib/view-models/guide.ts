// Bari Supplement Guides — View Model contract (TASK-504, Wave 0 skeleton).
//
// Source of truth: 01_framework/product/supplement_guides_concrete_plan_v1.md
// (owner-approved execution contract, §1 verdict layer / §2 six bars / §3 page shape /
// §4 buy button / §5 migration).
//
// This is a DELIBERATELY SEPARATE contract from BariProductVM (the food/supplement
// comparison-page VM). Guides retire ordinal ranking and score/grade display entirely —
// forcing guide data through BariProductVM would drag `score`/`grade` fields back onto
// the page. A guide's product is a bar-state record, nothing else.
//
// Hard constraints carried from the plan (do not relax without a plan amendment):
//   - No numeric score, no A–E letter grade, anywhere in a guide.
//   - Bar states are PASS / FLAG / FAIL / CANNOT_VERIFY only — never a 5th "graded" state.
//     AMENDED (TASK-575, Nutrition D6 + Product D7 co-sign, nutrition spec §11, gate-2
//     HIGH-1 ruling 2026-07-10): a 5th state, EVIDENCE_LIMITED, is added — but it is NOT
//     a graded/ordinal state (it never sits on the fail/flag/pass ladder; see
//     GuideBarState below). This is a scoped, ruled exception, not a silent relaxation.
//   - Buckets group products; they are NOT an ordinal ranking within a bucket.
//   - Benchmark placement is always product-vs-EXTERNAL-STANDARD (dose range, cert bar,
//     benchmark median price) — never product-vs-field ordering (that recreates ranking
//     by stealth per red-team RT-A3).
//   - verdict data (bars/bucket/defaultPick/benchmark) and `buyUrl` are separate fields
//     and must never be derived from one another (§4 mechanical separation). A missing
//     buyUrl must never hide or gate a product.
//   - The actual bar-threshold RUBRIC (what makes a given product's dose bar PASS vs FLAG)
//     is a versioned config file owned by Nutrition (plan §6 pre-build step) — it does not
//     exist yet. This file defines the SHAPE the rubric's output must be transformed into,
//     not the rubric itself. Nothing here computes a bar state from raw product data.

// ─── The six bars (plan §2 — Nutrition's amended attribute set) ────────────────────
export type GuideBarKey =
  | "doseAdequacy" // 1. vs literature-derived effective range, hedged as such
  | "formAbsorption" // 2. tier by form class; blend rule → cannot_verify for undisclosed blends
  | "thirdPartyVerification" // 3. two-tier: directory-confirmed / manufacturer-stated
  | "priceFairness" // 4. ₪ per effective unit / absorbed-mg
  | "safety" // 5. UL crossing = visible bar-level FAIL, never a tooltip
  | "labelTransparency"; // 6. dose disclosure honesty; undisclosed → cannot_verify, never assumed low

export const GUIDE_BAR_ORDER: readonly GuideBarKey[] = [
  "doseAdequacy",
  "formAbsorption",
  "thirdPartyVerification",
  "priceFairness",
  "safety",
  "labelTransparency",
] as const;

// Structural field labels (name the bar itself — not marketing copy). These are the
// vocabulary terms from the approved plan §2, not Content-authored narrative lines.
// Final on-page phrasing of the "buying rule" explanation for each bar is Content's job
// (GuideBuyingRuleBar.explanation below) — these are the short column/legend labels only.
export const GUIDE_BAR_LABELS_HE: Record<GuideBarKey, string> = {
  doseAdequacy: "מינון",
  formAbsorption: "צורה וספיגה",
  thirdPartyVerification: "בדיקת צד שלישי",
  priceFairness: "הוגנות מחיר",
  safety: "בטיחות",
  labelTransparency: "שקיפות תווית",
};

// ─── Bar state — the verdict-layer primitive (plan §1) ─────────────────────────────
// 4 ordinal states (pass/flag/fail/cannot_verify) + 1 non-ordinal state
// (evidence_limited, TASK-575 gate-2 HIGH-1 ruling). No numeric value ever attached.
//
// `evidence_limited` is a SEPARATE code path from `cannot_verify`, by design (nutrition
// spec §11): `cannot_verify` means the FACT itself is unknown/undisclosed (missing-data
// discard discipline — state why, never assume). `evidence_limited` means the fact IS
// known and disclosed (e.g. the chemical form), but the literature does not support
// ranking it with confidence against the forms that DO have a direct, named citation
// (spec §5 Bucket 3). Rendering requirement (behavioral, exact per the ruling): must
// render OFF the fail/flag/pass ordinal ladder entirely — not at "flag"/בינונית (that
// tier itself asserts a confident middle ranking) and not at "pass"/גבוהה — using a
// neutral treatment from the SAME family as `cannot_verify` (same non-ordinal
// footprint), but visually AND textually distinct from it: `cannot_verify`'s label
// asserts missing data ("לא ניתן לאמת"), which would be false here — the fact is not
// missing, only its ranking confidence is limited. Merging these two states into one
// code path or label is exactly the class of finding gate-2 would re-raise (spec §11
// "Unchanged" note).
export type GuideBarState = "pass" | "flag" | "fail" | "cannot_verify" | "evidence_limited";

export interface GuideBarResult {
  bar: GuideBarKey;
  state: GuideBarState;
  /** Short Hebrew note shown on hover/expand (e.g. why a bar FLAGged). Optional —
   *  CANNOT_VERIFY bars should generally carry a note explaining what is missing
   *  (missing-data discard discipline: state why, never assume). */
  note?: string | null;
}

// ─── Bucket (plan §1) — groups products; not a ranking ─────────────────────────────
export type GuideBucket =
  | "clears_all" // עובר את כל ספי הקנייה — unordered
  | "passes_with_flag" // עובר עם דגל
  | "fails" // לא עובר
  | "cannot_assess"; // לא ניתן להעריך

export const GUIDE_BUCKET_LABELS_HE: Record<GuideBucket, string> = {
  clears_all: "עובר את כל ספי הקנייה",
  passes_with_flag: "עובר עם דגל",
  fails: "לא עובר",
  cannot_assess: "לא ניתן להעריך",
};

/** Display order for bucket sections on the page (plan §1 order). */
export const GUIDE_BUCKET_ORDER: readonly GuideBucket[] = [
  "clears_all",
  "passes_with_flag",
  "fails",
  "cannot_assess",
] as const;

// ─── Per-bar threshold geometry (TASK-504C — threshold infographic spec v1) ─────────
// Static, per-BAR (not per-product) description of the "fixed external standard" a
// discriminating bar draws its gauge/ladder against (spec §2/§3: "the standard is a
// fact independent of this product"). ONE geometry object is shared by every product
// row for that bar — this is deliberately NOT duplicated per product. Populated only
// for the bars that have an anatomy defined (today: doseAdequacy, formAbsorption,
// safety, labelTransparency — spec §1); thirdPartyVerification/priceFairness carry no
// geometry until Product confirms an anatomy for them (spec §1 note).
export type GuideThresholdAnatomy = "gauge" | "ladder";

/** One contiguous zone of a Threshold Gauge, in ascending domain order. */
export interface GuideGaugeZone {
  /** Upper bound of this zone in the gauge's own numeric domain (mg). Zones are
   *  contiguous from 0; the LAST zone's `upTo` equals the geometry's `domainMax`. */
  upTo: number;
  /** Tone driving this zone's low-opacity background tint — reuses a bar-state tone
   *  (never a new hue), spec §2/§6. */
  tone: GuideBarState;
  /** Divider line style at this zone's UPPER boundary (WCAG 1.4.1 — never color-only,
   *  spec §7.1). "dashed" = an advisory line (e.g. EFSA soft-caution); "solid" = a hard
   *  boundary (e.g. UL veto, or the pass floor itself). */
  dividerStyle: "solid" | "dashed";
  /** Rendered directly under this boundary's tick, e.g. "150 (חצי סף)". Omit for a
   *  boundary that isn't a labeled anchor (spec §2: "only the meaningful anchors"). */
  tickLabel?: string;
}

export interface GuideGaugeGeometry {
  anatomy: "gauge";
  /** The gauge's numeric domain is 0..domainMax (spec §2 domain+overflow rule — chosen
   *  with headroom past the top zone boundary so the pass zone reads as a real zone). */
  domainMax: number;
  zones: GuideGaugeZone[];
  /**
   * TASK-575 (magnesium guide v2, nutrition spec §3 "gauge geometry") — suppress the
   * generic pct:0/label:"0" tick that `buildGaugeRender` otherwise always emits. Used
   * for a neutral corpus-range gauge where "0" is not a meaningful anchor (the
   * reviewed range starts at a real observed minimum, not zero) — the geometry
   * supplies its own boundary ticks via `referenceTicks` instead. Optional; default
   * (absent/false) preserves the existing "0" tick for every other gauge (e.g. the
   * unchanged safety gauge).
   */
  hideZeroTick?: boolean;
  /**
   * TASK-575 — a short numeric label at the domain max (e.g. "520"), rendered in the
   * same row as the zone-boundary ticks. Symmetric with the implicit "0"/zone
   * tickLabels — this is the one label that never has a natural zone boundary to
   * attach to (the domain max IS the last zone's edge).
   */
  maxTickLabel?: string;
  /**
   * TASK-575 — plain, tone-free reference points (e.g. a corpus median) marked on the
   * track as a thin dashed line, with their (Content-authored, verbatim) label
   * rendered on ITS OWN line below the track — never inline in the short numeric tick
   * row, which does not have room for a full sentence without colliding with an
   * adjacent boundary tick (a real layout defect caught in this task's own visual
   * verification pass). Carries no pass/fail/tone implication (spec §3).
   */
  referenceTicks?: { at: number; label: string }[];
  /**
   * TASK-575 — an additional overlay band on the track (e.g. the RDA all-sources
   * context range, 310–420 mg) that is NOT a pass/fail zone and must never reuse the
   * zone-tone system (spec §3: "must never be rendered as 'your supplement should
   * give you 310-420 mg'"). Rendered as a visually distinct, un-toned outline/bracket
   * with its own label + mandatory qualifier (both Content-authored, verbatim).
   */
  contextBand?: { from: number; to: number; label: string; qualifierLabel: string };
}

/** One tier of a Threshold Ladder, worst→best, left→right in the forced-LTR rail
 *  (spec §3 direction rule — stated once, shared by both ladder bars). */
export interface GuideLadderTier {
  /** e.g. "נמוכה" / "בינונית" / "גבוהה" — the tier name itself (spec §3 exact wording). */
  label: string;
  /** The 2–3 forms/values grouped into this tier, ported VERBATIM from already
   *  gate-1-approved copy (spec §3: "port those groupings verbatim, do not
   *  re-derive") — never newly authored here. Optional: not every ladder tier has a
   *  sub-grouping worth naming (labelTransparency's tiers do not, spec §3). */
  sublabel?: string;
  tone: GuideBarState;
}

export interface GuideLadderGeometry {
  anatomy: "ladder";
  /** Worst→best order, left→right in the forced-LTR rail. */
  tiers: GuideLadderTier[];
}

export type GuideThresholdGeometry = GuideGaugeGeometry | GuideLadderGeometry;

// ─── Per-product threshold placement (replaces the single flat `benchmark` field) ───
// One placement per DISCRIMINATING bar (spec §8: the old one-benchmark-per-product
// field "cannot carry 4 independent benchmarks as-is"). `value`/`tierIndex` of `null`
// means the underlying bar state is `cannot_verify` — the component renders the
// spec's honest no-marker/no-fill fallback, NEVER a fabricated position (spec §2/§3,
// the owner's explicit "keep it honest, no fake position" ask).
//
// Always product-vs-EXTERNAL-STANDARD only (plan red-team RT-A3, spec §8 non-goal) —
// never product-vs-field ranking. The caption's qualitative clause (spec §2 "· {short
// verdict clause}") is intentionally NOT a field here: it is sourced from the bar's
// own existing `GuideBarResult.note` at render time (spec §2: "Content's existing
// per-bar note field ... never invented here") rather than duplicated onto this type.
export interface GuideThresholdPlacement {
  /** Gauge bars only: the product's numeric value in the geometry's domain unit (mg).
   *  null = cannot_verify (render the hollow mid-track placeholder ring). Ignored for
   *  ladder bars. */
  value?: number | null;
  /** Gauge bars only: true when `value` exceeds the geometry's `domainMax` — clamp the
   *  marker at the domain end with a "+" glyph (spec §2 domain+overflow rule) instead
   *  of stretching the domain to fit an outlier. Ignored for ladder bars. */
  clamped?: boolean;
  /** Ladder bars only: 0-based index into the geometry's `tiers` array (worst→best)
   *  for this product's tier. null = cannot_verify (render every tier neutral, no
   *  fill, no caret — spec §3 CANNOT_VERIFY row). Ignored for gauge bars. */
  tierIndex?: number | null;
  /** Pre-rendered product value label, e.g. "250 מ״ג" / "ציטראט" / "לא ניתן לאימות" —
   *  never computed by the component. */
  valueLabel: string;
}

// ─── Pricing (plan §2.4 / §4) ───────────────────────────────────────────────────────
/** Factual retail channel tag (creatine domestic products only). */
export type GuideProductChannel = "domestic_shelf" | "import_iherb" | "import_myprotein";

export const GUIDE_PRODUCT_CHANNEL_LABELS_HE: Record<GuideProductChannel, string> = {
  domestic_shelf: "מדף בישראל",
  import_iherb: "הזמנה מחו״ל · iHerb",
  import_myprotein: "הזמנה מחו״ל · MyProtein",
};

export interface GuidePricing {
  /** Pre-rendered, e.g. "₪0.42 לגרם אפקטיבי". Backend computes; UI never derives. */
  pricePerEffectiveUnitLabel: string;
}

// ─── One product's guide record ─────────────────────────────────────────────────────
export interface GuideProductVM {
  id: string;
  name: string;
  brand?: string | null;
  imageUrl?: string | null;
  /** Exactly one result per GUIDE_BAR_ORDER entry (6 total). */
  bars: GuideBarResult[];
  bucket: GuideBucket;
  /** "הבחירה הפשוטה" (plan §1) — at most ONE product on the page carries this flag.
   *  Criterion (cheapest per effective unit among all-bar-clearers) is stated inline
   *  by the page, never implied by styling alone. */
  isDefaultPick?: boolean;
  /**
   * TASK-504C: one threshold placement per DISCRIMINATING bar (replaces the old
   * single `benchmark` field — see GuideThresholdPlacement header). Absent entry for
   * a bar → that bar renders without a gauge/ladder (either it has no geometry defined
   * yet, e.g. thirdPartyVerification/priceFairness, or it is suppressed entirely — see
   * GuidePageVM.suppressedBars). Optional at the VM level so non-discriminating bars
   * never need a placeholder entry.
   */
  benchmarks?: Partial<Record<GuideBarKey, GuideThresholdPlacement>>;
  pricing: GuidePricing | null;
  /** Plain retailer link, no affiliate params (plan §4). Separate from verdict data —
   *  never gate inclusion, bucket, or display order on whether this is set. */
  buyUrl: string | null;
  /**
   * TASK-504B — the product's one-line verdict, ported VERBATIM from the Content
   * Agent's gate-1-approved copy (חלק 4 of magnesium_guide_copy_v1.md, one line per
   * product). This is NOT computed or summarized by the frontend — it is pre-authored
   * prose stating the deciding bar(s) for that product. Rendered as-is, same
   * verbatim-render discipline as `rowVerdict` on BariProductVM.
   */
  oneLinerHe: string;
  /** Factual retail channel — routing tag, not marketing copy. */
  channel?: GuideProductChannel | null;
  /**
   * TASK-575 (magnesium guide v2) — a short, neutral-register sub-classification
   * phrase, Content-authored (copy package Slot 6), rendered as a small factual pill
   * on the product row. Used to keep severity visibly distinct WITHIN a single
   * descriptive group (e.g. group (c)'s "clean form, tolerance-note only" vs "known
   * weaker-absorption form" vs "weaker-absorption form + crosses the safety UL") —
   * this is NOT a ranking, letter, or score: it is a factual sub-label, optional, and
   * absent for products where no such distinction applies. Rendered verbatim, never
   * computed or paraphrased by the component.
   */
  classifierHe?: string | null;
}

// ─── Layer 1 — the buying rule (plan §3, item 1) ────────────────────────────────────
export interface GuideBuyingRuleBar {
  bar: GuideBarKey;
  /** One-line plain-Hebrew explanation of what this bar checks and why it matters.
   *  Content-authored; NOT present yet in this Wave 0 skeleton (mock fixture only). */
  explanation: string;
}

// ─── Layer 3 — the education spine (plan §3, item 3) ────────────────────────────────
export interface GuideEducationSection {
  heading: string;
  /** Paragraph blocks. Content-authored; mock fixture only in this skeleton. */
  body: string[];
  /**
   * TASK-575 — optional structured source list (Content copy package Slot 8),
   * rendered as clickable `target="_blank" rel="noopener"` links rather than bare
   * citation text. `label` is the descriptive sentence naming what the source
   * supports (Content-authored, verbatim); `url` is the canonical link. Absent for
   * every section except the guide's "מקורות" (sources) section.
   */
  sources?: { label: string; url: string }[];
}

// ─── Layer 2 headline (TASK-504B, Product D7 empty-shortlist ruling) ────────────────
// Rendered ONLY when the `clears_all` bucket is empty for this guide (0 products clear
// every bar). Content-authored (magnesium_guide_copy_v1.md חלק 3), rendered verbatim —
// the template never paraphrases or computes this text. Per the D7 ruling
// (supplement_guides_d7_cosign_v1.md §1), this leads the products section, BEFORE the
// bucket table, and the `passes_with_flag` bucket is then promoted below it as the
// practical shortlist — no new bucket, no default pick manufactured from a lower tier.
export interface GuideHeadlineFinding {
  /** The honest one-line finding (e.g. "אף מוצר ... לא עובר את כל ספי הקנייה."). */
  title: string;
  /** Supporting paragraphs — includes the no-default-pick statement and the
   *  passes_with_flag shortlist detail, ported verbatim from the approved copy. */
  body: string[];
}

// ─── Full guide page payload ─────────────────────────────────────────────────────────
export interface GuidePageVM {
  slug: string;
  /** "איך לבחור [X]" (plan §3 H1 frame). */
  h1: string;
  subtitle?: string | null;
  /**
   * TASK-504C add-on — optional hero mascot image shown beside the H1 (same placement
   * family as SeedOilsArticleHero / catalog's OLI). Self-hosted only under
   * `public/mascots/` (TASK-478 same-origin rule) — never a remote/hotlinked URL.
   * `alt` is a real, meaningful description (this mascot is not decorative filler —
   * it depicts the guide's own subject matter), so it is NOT rendered `aria-hidden`
   * like the purely decorative mascots elsewhere. null/absent → no hero image.
   */
  heroImage?: { src: string; alt: string; width: number; height: number } | null;
  buyingRuleIntro?: string | null;
  buyingRule: GuideBuyingRuleBar[];
  products: GuideProductVM[];
  educationSpine: GuideEducationSection[];
  /** Plan §4 on-page rule, verbatim, near the buy buttons: "קישור קנייה אינו משפיע על
   *  הכללה, על דגלים או על סדר הצגה." Rendered as-is — not re-authored by the template. */
  buyLinkDisclosureLine: string;
  updatedLabel?: string | null;
  /**
   * TASK-504B — the empty-clears-all headline (see GuideHeadlineFinding above).
   * null/absent when the `clears_all` bucket has at least one product — buckets then
   * render in their ordinary, un-promoted form.
   */
  headlineFinding?: GuideHeadlineFinding | null;
  /**
   * TASK-504C — per-BAR gauge/ladder geometry (see GuideThresholdGeometry header).
   * Keyed by the same GuideBarKey as `benchmarks` on each product. A bar absent from
   * this map renders as a plain badge (no infographic) wherever it appears — this is
   * how thirdPartyVerification/priceFailness degrade gracefully until an anatomy is
   * defined for them (spec §1).
   */
  thresholdGeometry?: Partial<Record<GuideBarKey, GuideThresholdGeometry>>;

  /**
   * TASK-504C — rubric `display_suppression_rule`
   * (supplement_guides_bar_rubric_v1.yaml): bars computed here, fresh per build, from
   * the live `products` array — NEVER a hardcoded per-guide exclusion list (the
   * rubric's own re_evaluated_per_build clause). See
   * `src/lib/guides/guide-suppression.ts:computeSuppressedBars`. A bar listed here is
   * DISPLAY-suppressed only: `GuideProductTable`/`GuideProductRow` skip rendering its
   * row entirely, but bucket_logic upstream (which produced `product.bucket`) already
   * evaluated all 6 bars unchanged — this field never feeds back into bucket math.
   */
  suppressedBars?: GuideBarKey[];

  /** Bars excluded from tier-GATING only (see computeBandExcludedBars). */
  bandExcludedBars?: GuideBarKey[];

  /**
   * TASK-504C — the ONE guide-level line disclosing which bar(s) were suppressed and
   * why (rubric honesty_constraint: "disclosed, never silently vanished"). Content-
   * authored, two-gate sign-off required — this Wave 1 build ships it as a literal
   * `"// TODO CONTENT (two-gate)"` placeholder string, not real copy. null/absent when
   * `suppressedBars` is empty (nothing to disclose).
   */
  suppressedBarsDisclosureHe?: string | null;

  /**
   * TASK-504 recommendation-tiers build (RT-6): one caption per RANKED tier
   * (`GuideRecommendationTier`, below) — replaces the retired `bucketSubCaptions`.
   * `very_recommended` never reads this field when empty — its empty state uses
   * `veryRecommendedEmptyStateHe` instead. Content-authored, both gates passed
   * (magnesium_guide_tier_copy_v1.md Slot 1).
   */
  recommendationTierCaptions?: Partial<Record<GuideRecommendationTier, string>>;

  /**
   * TASK-504 recommendation-tiers build — honest one-line state shown under the
   * `very_recommended` (מומלץ מאוד) tier header when it has zero products (rubric
   * `recommendation_tier_mapping.tiers[very_recommended].empty_state_handling`: render
   * the tier unconditionally, never hide it). Content-authored, both gates passed
   * (magnesium_guide_tier_copy_v1.md Slot 2).
   */
  veryRecommendedEmptyStateHe?: string | null;

  /**
   * TASK-504 recommendation-tiers build — intro line for the `cannot_assess` section,
   * which renders OUTSIDE the 4 ranked tiers (rubric
   * `recommendation_tier_mapping.tiers[cannot_assess].display_position`) — a genuine
   * data gap (e.g. TRIOMAG's undisclosed blend), never folded into `not_recommended`.
   * Content-authored, both gates passed (magnesium_guide_tier_copy_v1.md Slot 3).
   */
  cannotAssessSectionIntroHe?: string | null;

  /**
   * TASK-504 recommendation-tiers build — per-row expander toggle labels (Design spec
   * v2 §3.3: one expander per product row reveals the 4-bar threshold-gauge detail,
   * collapsed by default). Content-authored, both gates passed
   * (magnesium_guide_tier_copy_v1.md Slot 4).
   */
  expanderLabels?: { collapsed: string; expanded: string };

  /**
   * TASK-504 creatine — world-reference products rendered BELOW domestic A/B/C/D bands,
   * never interleaved into ranked tiers.
   */
  benchmarkProducts?: GuideProductVM[];

  /** Heading for the benchmark section (creatine only). */
  benchmarkSectionHeadingHe?: string | null;

  /**
   * TASK-504 creatine — non-collapsible disclosure at the TOP of domestic bands.
   * GATE-1 DRAFT — pending Content + Adversarial QA two-gate sign-off.
   */
  domesticBandsDisclosureHe?: string | null;

  /**
   * TASK-575 (magnesium guide v2) — renders `products` grouped by `GuideBucket` as
   * FOUR FLAT, DESCRIPTIVE sections (GUIDE_BUCKET_ORDER: clears_all / passes_with_flag
   * / fails / cannot_assess), with NO ranking, no tier ladder, no letters, no colored
   * good→poor palette on the section headers. This is ADDITIVE and opt-in: default
   * false/absent preserves the existing `GuideRecommendationTier` ranked-tier
   * rendering path unchanged for any other guide that still relies on it (none does
   * today — grep-verified at build time — but the old path is left intact rather than
   * deleted, per the "do not break other guide surfaces" constraint). When true,
   * `recommendationTierCaptions` / `veryRecommendedEmptyStateHe` /
   * `cannotAssessSectionIntroHe` are ignored in favor of `groupLabelsHe` /
   * `groupCaptionsHe` below.
   */
  useDescriptiveGroups?: boolean;

  /**
   * TASK-575 — per-bucket group SECTION HEADER text (copy package Slot 5 headers),
   * only consulted when `useDescriptiveGroups` is true. Falls back to
   * `GUIDE_BUCKET_LABELS_HE[bucket]` when a bucket is absent from this map.
   */
  groupLabelsHe?: Partial<Record<GuideBucket, string>>;

  /**
   * TASK-575 — per-bucket ONE-LINE caption rendered under the group header (copy
   * package Slot 5 second lines), only consulted when `useDescriptiveGroups` is true.
   * The `clears_all` bucket's caption doubles as its empty-state line (it is always
   * empty for magnesium today, and the section still renders per spec §2 — "renders
   * its empty-state caption").
   */
  groupCaptionsHe?: Partial<Record<GuideBucket, string>>;
}

// ─── Recommendation tiers (TASK-504 follow-on) ──────────────────────────────────────
// Display-layer relabeling of the existing bucket_logic buckets, PLUS one display-only
// split predicate (`dose_adequacy_sole_caveat`) applied only to `passes_with_flag`
// members — see 01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml
// `recommendation_tier_mapping`. Does NOT touch bucket_logic, bar states, or any
// computed field — `GuideProductVM.bucket` remains the authoritative source; tiers are
// derived from it (see src/lib/guides/guide-recommendation-tiers.ts), never hardcoded
// per-product. `cannot_assess` is deliberately NOT a member of this type — it renders
// in a separate, out-of-tier section (rubric: "never folded into לא מומלץ").
export type GuideRecommendationTier =
  | "very_recommended" // מומלץ מאוד — maps from clears_all_bars (all 6 bars PASS)
  | "recommended" // מומלץ — passes_with_flag, non-PASS displayed set is exactly {doseAdequacy}
  | "good" // טוב — passes_with_flag, non-PASS displayed set contains any other bar
  | "not_recommended"; // לא מומלץ — maps from fails (>=1 bar FAIL)

/** Ordered display: מומלץ מאוד → מומלץ → טוב → לא מומלץ. No sort within a tier — products
 *  render in their existing array order (stable, non-scored). `cannot_assess` renders
 *  separately below this ordered list, never interleaved. */
export const GUIDE_RECOMMENDATION_TIER_ORDER: readonly GuideRecommendationTier[] = [
  "very_recommended",
  "recommended",
  "good",
  "not_recommended",
] as const;

/**
 * EXCEPTION-003: these 4 Hebrew strings are sanctioned as tier-HEADING field values
 * ONLY. Never introduce "מומלץ"/"מומלץ מאוד"/"טוב"/"לא מומלץ" inside prose/body copy —
 * the hebrew_readability.py gate HARD-fails a bare tier word in a sentence (kind
 * `recommendation`); only this field-value usage is exempt.
 */
export const GUIDE_RECOMMENDATION_TIER_LABELS_HE: Record<GuideRecommendationTier, string> = {
  very_recommended: "מומלץ מאוד",
  recommended: "מומלץ",
  good: "טוב",
  not_recommended: "לא מומלץ",
};
