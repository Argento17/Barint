"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { ComparisonTable } from "@/components/shared/comparison-table";
import {
  filterButterProducts,
  BUTTER_SHELF_LENS_OPTIONS,
  type ButterShelfFilterId,
} from "@/lib/comparisons/butter-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";
import { cn } from "@/lib/utils";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";

// ---------------------------------------------------------------------------
// Section constants
// ---------------------------------------------------------------------------

// Pure butter: any product whose only ingredients are milk fat (cream), salt,
// and/or lactic cultures. Includes unsalted, salted, cultured/fermented, and
// ghee. Salt is the only permitted addition — it doesn't change the category.
const SECTION_HEADING_PURE = "חמאה טהורה";
const SECTION_SUBTITLE_PURE =
  "שמנת מפוסטרת בלבד — מלוחה, ללא מלח, מותססת או גהי. רכיב אחד. " +
  "כל הגרסאות מקבלות B/70 — זו תקרת הקטגוריה, לא פגם.";

// With additions: something beyond milk fat has been added — water, vegetable
// oil, thickeners, herbs, or preservatives. These are fundamentally different
// products sold under the butter name.
const SECTION_HEADING_ADDITIONS = "חמאה עם תוספות";
const SECTION_SUBTITLE_ADDITIONS =
  "כשמוסיפים שמן צמחי, מים, חומרי עיבוי, תבלינים או חומרים משמרים — " +
  "זה כבר לא שמנת בלבד. מוצרים אלה נמכרים \"כחמאה\" אבל הרכבם שונה לחלוטין.";

// ---------------------------------------------------------------------------
// Subtype grouping
// ---------------------------------------------------------------------------

/** Mirror of the ButterCorpusProduct interface in butter-shelf-filters.ts. */
interface ButterCorpusProduct extends BariProductVM {
  subtype?: string;
}

// Pure: cream ± salt ± cultures ± clarification. No non-dairy additions.
const PURE_SUBTYPES = new Set(["plain", "unsalted", "salted", "cultured_fermented", "ghee"]);
// With additions: non-dairy fat, water, thickeners, flavourings, preservatives.
const ADDITIONS_SUBTYPES = new Set(["additive_spread", "flavored"]);

function groupButterProducts(products: BariProductVM[]): {
  pure: BariProductVM[];
  additions: BariProductVM[];
} {
  const pure: BariProductVM[] = [];
  const additions: BariProductVM[] = [];

  for (const product of products) {
    const subtype = (product as ButterCorpusProduct).subtype ?? "";
    if (PURE_SUBTYPES.has(subtype)) {
      pure.push(product);
    } else if (ADDITIONS_SUBTYPES.has(subtype)) {
      additions.push(product);
    }
    // Unrecognised subtype → excluded (data issue, not a UI concern).
  }

  // Pure group: verified products sort before candidate, preserving order within tiers.
  const verifiedPure = pure.filter((p) => p.confidence === "verified");
  const candidatePure = pure.filter((p) => p.confidence !== "verified");

  return { pure: [...verifiedPure, ...candidatePure], additions };
}

// ---------------------------------------------------------------------------
// Section header component
// ---------------------------------------------------------------------------

interface SectionHeaderProps {
  heading: string;
  subtitle: string;
  isFirst: boolean;
  variant?: "default" | "additions";
}

function SectionHeader({ heading, subtitle, isFirst, variant = "default" }: SectionHeaderProps) {
  const isAdditions = variant === "additions";
  return (
    <div
      className={cn(
        "px-4",
        comparisonWebSectionPaddingClass(),
        isFirst ? "pt-4 pb-2" : "pt-8 pb-2"
      )}
      dir="rtl"
    >
      {!isFirst && (
        <hr className="mb-5 border-0 border-t-2 border-[#D8D8D0]" aria-hidden />
      )}
      {isAdditions ? (
        <div className="border-r-[3px] border-r-[#B07A28] bg-[#FEFBF4] rounded-sm pr-3 py-1.5 -mr-1">
          <p className="text-[10px] font-semibold uppercase tracking-widest text-[#B07A28] mb-0.5">
            שונה מחמאה טהורה
          </p>
          <h3 className="text-[15px] font-semibold leading-snug text-[#7A4F10]">
            {heading}
          </h3>
          {subtitle ? (
            <p className="mt-0.5 text-[12px] leading-normal text-[#8A7A5A]">
              {subtitle}
            </p>
          ) : null}
        </div>
      ) : (
        <>
          <h3 className="text-[15px] font-semibold leading-snug text-[#1A1A1A]">
            {heading}
          </h3>
          {subtitle ? (
            <p className="mt-0.5 text-[12px] leading-normal text-[#7A7A6A]">
              {subtitle}
            </p>
          ) : null}
        </>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

export interface ButterComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const butterShelfFilters = {
  lensOptions: BUTTER_SHELF_LENS_OPTIONS,
  filterProducts: filterButterProducts,
} as const;

// No single dominant numeric headline metric for butter — purity of ingredients
// is the signal, not a scalar nutrient. metricSpecs=[] keeps the row compact.
const BUTTER_METRIC_SPECS = [] as const;

// ---------------------------------------------------------------------------
// Grouped product renderer (module-level so react/display-name is satisfied)
// ---------------------------------------------------------------------------

function renderButterProducts(
  filteredProducts: BariProductVM[],
  expandedProductId: string | null
) {
  const { pure, additions } = groupButterProducts(filteredProducts);

  const sections = [
    { heading: SECTION_HEADING_PURE, subtitle: SECTION_SUBTITLE_PURE, products: pure, variant: "default" as const },
    { heading: SECTION_HEADING_ADDITIONS, subtitle: SECTION_SUBTITLE_ADDITIONS, products: additions, variant: "additions" as const },
  ].filter((s) => s.products.length > 0);

  return (
    <div>
      {sections.map((section, sectionIndex) => (
        <div key={section.heading}>
          <SectionHeader
            heading={section.heading}
            subtitle={section.subtitle}
            isFirst={sectionIndex === 0}
            variant={section.variant}
          />
          <ComparisonTable
            key={`${section.heading}-${expandedProductId ?? "none"}`}
            products={section.products}
            metricSpecs={BUTTER_METRIC_SPECS}
            showRail={false}
            showRank={false}
            initialExpandedProductId={
              section.products.some((p) => p.id === expandedProductId)
                ? expandedProductId
                : null
            }
            category="butter"
            suppressPartialBadges={false}
          />
        </div>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function ButterComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: ButterComparisonPageProps) {
  return (
    <ComparisonPage<ButterShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={butterShelfFilters}
      metricSpecs={BUTTER_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="butter"
      renderProducts={renderButterProducts}
    />
  );
}
