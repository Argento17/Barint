import type { Metadata } from "next";

import rawCorpusV2 from "@/data/comparisons/frozen_vegetables_frontend_v2.json";
import shellCopyV2 from "@/data/comparisons/frozen_vegetables_shell_copy_v2.json";

import type { ComparisonCorpusMeta } from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import type { BariProductVM } from "@/lib/view-models";

// ---------------------------------------------------------------------------
// TASK-235 Phase 4 — score-free Frozen Vegetables v2.
//
// Frozen v2 is a self-contained, SCORE-FREE feature. It does NOT use the shared
// BariProductVM / corpus loader (those carry score/grade/confidence, none of which
// exist in v2). It reads its own v2 JSON schema directly and renders through the
// dedicated FrozenVegetablesComparisonPage composition (NOT the shared ComparisonPage,
// whose hardcoded methodology-footer note + partial-badge disclosure both mention
// "הציון" and would leak a score on a score-free page).
//
// The registry contract (getPageData / getCorpusPayload returning BariProductVM[])
// is satisfied with an empty stub so the registry stays type-sound and no generic
// tooling breaks — but nothing renders through it for frozen. The real data flows via
// the v2 exports below, consumed by the route and the (score-free) featured card.
// ---------------------------------------------------------------------------

export type FrozenVegetablesCorpusMeta = ComparisonCorpusMeta;

export interface FrozenVegetablesBand {
  id: string;
  title: string;
  standingMarker: string;
  order: number;
}

/** Label nutrition values. Only fields present on the label are set; an absent field
 *  is `undefined` and MUST NOT render as 0 (Phase 4 hard rule). */
export interface FrozenVegetablesNutrition {
  energyKcal?: number;
  protein?: number;
  fat?: number;
  satFat?: number;
  carbs?: number;
  sugar?: number;
  fiber?: number;
  sodium?: number;
}

export interface FrozenVegetablesExpansion {
  ingredients: string | null;
  nutrition: FrozenVegetablesNutrition;
  positiveFacts: string[];
  whatToKnowHeader: string;
  whatToKnow: string[];
  bottomLine: string;
  /** When true: identity/composition only — render no synthesized benefit/micronutrient claim. */
  notCharacterized: boolean;
}

export interface FrozenVegetablesProduct {
  id: string;
  bsip1_product_id: string;
  name: string;
  imageUrl: string;
  barcode: string;
  band: string;
  standingMarker: string;
  verdictLine1: string;
  verdictLine2: string;
  expansion: FrozenVegetablesExpansion;
}

interface FrozenVegetablesCorpusV2 {
  _meta: {
    generated: string;
    category: string;
    product_count: number;
    schema: string;
    version: string;
    scoreFree: boolean;
    source_run_id: string;
    provenance: string;
  };
  bands: FrozenVegetablesBand[];
  products: FrozenVegetablesProduct[];
}

interface FrozenVegetablesShellCopy {
  hero: { eyebrow: string; title: string };
  metadataLine: string;
  prologueSentences: string[];
  categoryNote: string;
  methodologyLines: string[];
  footerNote: string;
}

const corpusV2 = rawCorpusV2 as unknown as FrozenVegetablesCorpusV2;
const shell = shellCopyV2 as unknown as FrozenVegetablesShellCopy;

const corpusMeta: FrozenVegetablesCorpusMeta = {
  generated: corpusV2._meta.generated,
  category: corpusV2._meta.category,
  product_count: corpusV2._meta.product_count,
  schema: corpusV2._meta.schema,
  version: corpusV2._meta.version,
};

export { corpusMeta };

/** The 4 use-case bands, in render order (plain-veg → legumes → mixes-meals → seasoning). */
export const frozenVegetablesBands: readonly FrozenVegetablesBand[] = [...corpusV2.bands].sort(
  (a, b) => a.order - b.order
);

// TASK-235 Phase 4 UX note: artichoke-bottoms (frozen-veg-44 "תחתיות ארטישוק", frozen-veg-45
// "ארטישוק תחתיות") sit in band 4 (seasoning / תיבול) as authored upstream. Their banding is
// FLAGGED for UX review — left as-is here, NOT re-banded in this phase.
/** All v2 products in file order (cross-band ranking is intentionally absent — score-free). */
export const frozenVegetablesV2Products: readonly FrozenVegetablesProduct[] = corpusV2.products;

export const frozenVegetablesHero = shell.hero;
export const frozenVegetablesMetadataLine = shell.metadataLine;
export const frozenVegetablesPrologueSentences: readonly string[] = shell.prologueSentences;
export const frozenVegetablesCategoryNote = shell.categoryNote;
export const frozenVegetablesMethodologyLines: readonly string[] = shell.methodologyLines;
/** Score-free closing note — used INSTEAD of the shared "הציון מסכם…" METHODOLOGY_FOOTER_NOTE. */
export const frozenVegetablesFooterNote = shell.footerNote;

export const frozenVegetablesComparisonMetadata: Metadata = {
  title: "השוואת ירקות קפואים | Bari",
  description:
    "ירקות קפואים ממדף שופרסל לפי ארבעה שימושים במטבח — ירק בודד, קטנייה, תערובת ותיבול. בלי ציון: מה כל מוצר מביא לשימוש שלכם.",
};

// ---------------------------------------------------------------------------
// Registry contract — satisfied with a score-free, empty BariProductVM stub.
// Frozen renders through the v2 composition, NOT through these. Keeping them valid
// means the registry type-checks and any generic tooling that walks all categories
// (e.g. the dev corpus route) does not crash on frozen.
// ---------------------------------------------------------------------------

const FROZEN_REGISTRY_PRODUCTS: BariProductVM[] = [];

const frozenVegetablesShelfFilters = {
  lensOptions: [] as { id: string; label: string }[],
  filterProducts: (products: BariProductVM[]) => products,
};

export function getFrozenVegetablesPageData(): ComparisonCategoryPageData {
  return {
    products: FROZEN_REGISTRY_PRODUCTS,
    metadataLine: frozenVegetablesMetadataLine,
    hero: frozenVegetablesHero,
    prologueSentences: frozenVegetablesPrologueSentences,
    methodologyLines: frozenVegetablesMethodologyLines,
    corpusMeta,
    shelfFilters: frozenVegetablesShelfFilters,
  };
}

export function getFrozenVegetablesCorpusPayload(): {
  _meta: FrozenVegetablesCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: corpusMeta,
    products: FROZEN_REGISTRY_PRODUCTS,
  };
}
