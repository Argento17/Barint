// Sweetener guide — FRONTEND-OWNED VISUAL LAYOUT DATA. NOT a copy module.
//
// Every string constant below is either (a) a byte-identical, contiguous substring of a
// paragraph already published in `sweetener-guide-data.ts` (verified programmatically at
// module load via `assertVerbatimSubstring`, not just eyeballed), or (b) a reused existing
// constant/label imported from that file. This module authors zero new consumer-facing
// words. It exists to answer purely presentational questions the data module has no
// opinion on: which icon illustrates which section, which real sentence gets pulled out
// as a pull-quote, which real product names get surfaced as tags on the "three groups"
// cards, and which existing sweetener names + existing statutory-warning text populate the
// chocolate-bar label-breakdown chips.
//
// If a future edit to sweetener-guide-data.ts removes or rewords one of these source
// sentences, `assertVerbatimSubstring` throws at build/import time (it is NOT gated behind
// NODE_ENV, specifically so `npm run build`'s prerender catches drift — the guide's own
// dev server was not available to verify this visually during the build).

import {
  SWEETENER_SECTIONS,
  SWEETENER_STATUTORY_WARNINGS,
  type SweetenerGuideSection,
} from "./sweetener-guide-data";

function findSection(id: string): SweetenerGuideSection {
  const section = SWEETENER_SECTIONS.find((s) => s.id === id);
  if (!section) {
    throw new Error(`[sweetener-guide-visuals] unknown section id "${id}"`);
  }
  return section;
}

/** Throws if `needle` is not a byte-identical contiguous substring of one of the section's
 *  real paragraphs (or its statutory warning). Runs unconditionally — cheap, and it is the
 *  only verification available since a dev server was not run for this build. */
function assertVerbatimSubstring(sectionId: string, needle: string, label: string): string {
  const section = findSection(sectionId);
  const haystacks = [...section.paragraphs, section.statutoryWarning ?? ""];
  const found = haystacks.some((h) => h.includes(needle));
  if (!found) {
    throw new Error(
      `[sweetener-guide-visuals] "${label}" is not a verbatim substring of section "${sectionId}". ` +
        `Value checked: ${JSON.stringify(needle)}`
    );
  }
  return needle;
}

// ── Section icon glyphs — purely visual, mapped by the section id already defined in the
// data module. Glyph choice reflects each section's real topic (verified by the heading/
// paragraph text at the given id), not new copy. ───────────────────────────────────────
export type SweetenerIconKey =
  | "opening"
  | "polyols"
  | "high-intensity"
  | "plant-derived"
  | "erythritol-headline"
  | "not-in-products"
  | "not-yet-known";

export const SWEETENER_SECTION_ICON: Record<string, SweetenerIconKey> = {
  opening: "opening",
  polyols: "polyols",
  "high-intensity": "high-intensity",
  "plant-derived": "plant-derived",
  "erythritol-headline": "erythritol-headline",
  "not-in-products": "not-in-products",
  "not-yet-known": "not-yet-known",
};

// ── Pull-quotes — each a verified verbatim substring of the named section. ──────────────
export interface SweetenerPullQuote {
  sectionId: string;
  /** Index into that section's paragraphs array, after which the quote is rendered. */
  afterParagraphIndex: number;
  quote: string;
}

export const SWEETENER_PULL_QUOTES: SweetenerPullQuote[] = [
  {
    sectionId: "polyols",
    afterParagraphIndex: 0,
    quote: assertVerbatimSubstring(
      "polyols",
      "הרכיב הראשון ברשימה שלה הוא סוכר, ובכל זאת מופיע בה גם סורביטול.",
      "cake-counter-example pull-quote"
    ),
  },
  {
    sectionId: "erythritol-headline",
    afterParagraphIndex: 0,
    quote: assertVerbatimSubstring(
      "erythritol-headline",
      "בתוך הקבוצה עצמה יש אחד שחמק מאי-הנוחות הזאת: אריתריטול.",
      "erythritol-escaped-the-cost pull-quote"
    ),
  },
  {
    sectionId: "not-in-products",
    afterParagraphIndex: 0,
    quote: assertVerbatimSubstring(
      "not-in-products",
      "רוב השמות שסביבם סובבת השיחה הציבורית כמעט לא נמצאים על המדף הזה.",
      "most-names-not-on-shelf pull-quote"
    ),
  },
];

// ── "Three groups on the shelf" cards — headings are looked up live from the data module
// by id (never re-typed here); only the per-card real product-name tags are declared here,
// each a verified verbatim substring of that section's own paragraphs. ─────────────────
export interface SweetenerGroupCard {
  sectionId: string;
  icon: SweetenerIconKey;
  /** Real product names mentioned in this section's paragraphs, verbatim. */
  productMentions: string[];
}

export const SWEETENER_GROUP_CARDS: SweetenerGroupCard[] = [
  {
    sectionId: "polyols",
    icon: "polyols",
    productMentions: [
      assertVerbatimSubstring("polyols", "עוגת הבית שיש אסם", "polyols group card product tag"),
    ],
  },
  {
    sectionId: "high-intensity",
    icon: "high-intensity",
    productMentions: [
      assertVerbatimSubstring(
        "high-intensity",
        'שוקולד מריר ללת"ס של שוקולד פרה',
        "high-intensity group card product tag (choc bar)"
      ),
      assertVerbatimSubstring(
        "high-intensity",
        'דנונה פרו לת"ס בננה טופי',
        "high-intensity group card product tag (danone)"
      ),
    ],
  },
  {
    sectionId: "plant-derived",
    icon: "plant-derived",
    productMentions: [
      assertVerbatimSubstring(
        "plant-derived",
        'גרנולה תותים ללת"ס של טרו',
        "plant-derived group card product tag (granola)"
      ),
      assertVerbatimSubstring(
        "plant-derived",
        "עוגיות קיטו שקד לוז",
        "plant-derived group card product tag (keto cookies)"
      ),
    ],
  },
];

// ── Chocolate-bar hero card (§3 / "high-intensity") — label breakdown. Sweetener names are
// the same verbatim label terms used in the glycemic table / prose; captions reuse the
// existing statutory-warning constant and a verified verbatim law-reach sentence. No new
// words. ──────────────────────────────────────────────────────────────────────────────
export interface SweetenerLabelBreakdownGroup {
  /** Section whose heading labels this group (looked up live, not re-typed). */
  headingSectionId: string;
  sweetenerNames: string[];
  /** Verbatim caption — either the statutory warning or a verified verbatim sentence. */
  caption: string;
  lawReaches: boolean;
}

export const SWEETENER_CHOC_BAR_IMAGE = "/products/7290107955782.webp";
export const SWEETENER_DANONE_IMAGE = "/products/7290119370177.webp";

export const SWEETENER_CHOC_LABEL_BREAKDOWN: SweetenerLabelBreakdownGroup[] = [
  {
    headingSectionId: "polyols",
    sweetenerNames: ["אריתריטול", "מלטיטול"],
    caption: SWEETENER_STATUTORY_WARNINGS.polyols,
    lawReaches: true,
  },
  {
    headingSectionId: "high-intensity",
    sweetenerNames: ["סוכרלוז"],
    caption: assertVerbatimSubstring(
      "high-intensity",
      "החוק לא מגיע אליהם כלל, בשום כמות",
      "sucralose label-breakdown caption"
    ),
    lawReaches: false,
  },
];

// ── Video embed slot — placed after the polyols section (§2), where the gut-warning /
// "what are polyols" ground is laid. Video ID is a single swappable constant. ──────────
export const SWEETENER_VIDEO_AFTER_SECTION_ID = "polyols";
export const SWEETENER_VIDEO_ID = "VIDEO_ID_PENDING";

/** Looks up a section's heading by id (used instead of duplicating heading text anywhere
 *  in this module). Throws on an unknown id — same fail-loud posture as the rest of the
 *  module. */
export function sectionHeadingById(id: string): string {
  return findSection(id).heading;
}
