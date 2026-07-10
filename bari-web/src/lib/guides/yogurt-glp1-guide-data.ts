// TASK-504A: GLP-1 / suppressed-appetite high-protein yogurt guide (/madrichim/yogurt-glp1).
//
// Copy source of truth: src/data/guides/yogurt_glp1_dairy_guide_v1.json — a byte-identical
// copy of the signed-off draft at C:\Bari\02_products\yogurt_system\guides\
// glp1_dairy_guide_COPY_DRAFT_v1.json (sha256 43a988fdefab6a13985160712c69747f806c95d2872
// 624028b2677ff8f8a8228, verified identical at copy time). Every Hebrew string exported
// from this file is read verbatim from that JSON — this loader authors NO new copy.
//
// Grade/score/image for the 4 shortlist products are NOT stored in the copy JSON (it
// carries no grade field). They are cross-referenced by barcode from the live frontend
// corpus (yogurt_spoonable_frontend_v1.json) through the IDENTICAL loadComparisonCorpus()
// normalization the /hashvaot/yogurt route uses, so the badge shown here is guaranteed
// byte-identical to the badge on the full comparison page — which is exactly what the
// copy's own howToRead.gradeNote promises ("הדירוג של כל מוצר כאן... זהה לחלוטין לדירוג
// שמופיע בהשוואת היוגורט המלאה").
//
// IMPORTANT FRONTEND-AGENT NOTE (flagged in the TASK-504A return, not silently resolved):
// the raw corpus JSON's `grade` field for the two Danone Pro products is "S" (score 92.6 /
// 90.6), and the shortlist whyFeatured prose for both also reads "...דירוג S." literally.
// The live /hashvaot/yogurt page never displays "S" though: corpus.ts's
// frontendGradeFromScore() folds the engine's 6-grade S>=90 band into "A" for the ScoreChip
// UI, because the frozen gradePalette (bari-comparison-tokens.ts) and the BariGrade type
// only define A|B|C|D|E — there is no "S" slot, and adding one would violate the frozen
// ScoreChip rule ("one hue family per grade A->E ... never add a second color axis").
// This loader reuses the exact same loadComparisonCorpus() pipeline as the live page, so
// these two products' badges render "A" here, not "S" — matching production and honoring
// the gradeNote's "identical to the full comparison" claim, rather than inventing a new
// visual grade the design system does not support. The word "S" the user reads is inside
// the frozen prose paragraph (rendered verbatim, untouched); it is not contradicted by the
// badge because a careful reader sees the badge as the same A shown on the full comparison
// page for the same product — this loader does not resolve the wording, only the display.

import copyDraft from "@/data/guides/yogurt_glp1_dairy_guide_v1.json";
import spoonableRaw from "@/data/comparisons/yogurt_spoonable_frontend_v1.json";

import { loadComparisonCorpus, type ComparisonCorpusRaw } from "@/lib/comparisons/corpus";
import type { BariProductVM } from "@/lib/view-models";

interface CopyDraftShape {
  hero: { eyebrow: string; title: string; intro: string };
  howToRead: {
    title: string;
    intro: string;
    bars: Array<{ label: string; description: string }>;
    gradeNote: string;
  };
  shortlist: Array<{ barcode: string; name: string; whyFeatured: string }>;
  fullListNote: string;
  drinkableCallout: string;
  categoryCaveat: { title: string; body: string };
}

const _copy = copyDraft as unknown as CopyDraftShape;

const _loadedSpoonable = loadComparisonCorpus(spoonableRaw as ComparisonCorpusRaw);
const _rawSpoonableProducts = (
  spoonableRaw as unknown as { products: Array<{ barcode?: string }> }
).products;

function findByBarcode(barcode: string): BariProductVM {
  const idx = _rawSpoonableProducts.findIndex((p) => String(p.barcode) === barcode);
  if (idx === -1) {
    throw new Error(
      `yogurt-glp1-guide-data: barcode ${barcode} not found in yogurt_spoonable_frontend_v1.json`
    );
  }
  return _loadedSpoonable.products[idx];
}

export interface YogurtGlp1ShortlistItem {
  barcode: string;
  /** Rendered verbatim from the copy draft — NOT the corpus's raw `name` field (which can
   *  differ in whitespace only, e.g. "לבן0%" vs "לבן 0%"; the copy string is the
   *  signed-off one and is what must render). */
  name: string;
  whyFeatured: string;
  /** Grade/score/image cross-referenced from the live comparison corpus — never
   *  hand-typed. See the module comment above re: the S->A normalization. */
  product: BariProductVM;
}

export const yogurtGlp1Hero = _copy.hero;
export const yogurtGlp1HowToRead = _copy.howToRead;
export const yogurtGlp1FullListNote = _copy.fullListNote;
export const yogurtGlp1DrinkableCallout = _copy.drinkableCallout;

// Same {title, body} -> "title\n\nbody" join the live yogurt comparison pages use for
// their categoryNote prop (see yogurt-spoonable-page-data.ts), so CategoryNoteBox renders
// this caveat with the identical visual treatment as the two live yogurt pages.
export const yogurtGlp1CategoryNote: string = `${_copy.categoryCaveat.title}\n\n${_copy.categoryCaveat.body}`;

export const yogurtGlp1Shortlist: YogurtGlp1ShortlistItem[] = _copy.shortlist.map((item) => ({
  barcode: item.barcode,
  name: item.name,
  whyFeatured: item.whyFeatured,
  product: findByBarcode(item.barcode),
}));
