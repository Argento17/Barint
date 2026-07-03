// Creatine supplement comparison route — TASK-492C.
// Data source: creatine-page-data.ts, ported verbatim from the two-gate-fixed content
// package (creatine_comparison_content_package_v2.md).
// Product ruling 1: NO A–E grade / no numeric score anywhere. 31 products total
// (18 Israeli shelf + 13 worldwide benchmark).
// DRAFT CONTENT — orchestrator gates (Content + Adversarial QA sign-off) before owner sees it.

import type { Metadata } from "next";

import { withComparisonOpenGraph } from "@/lib/seo/open-graph";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { CreatineComparisonPage } from "@/components/comparisons/creatine-comparison-page";
import {
  creatineHero,
  creatineMetadataLine,
  creatineMethodologyLines,
  creatinePrologueSentences,
  creatineIsraeliProducts,
  creatineWorldwideProducts,
  creatineProducts,
  creatineCategoryNote,
} from "@/lib/comparisons/creatine-page-data";

export const metadata: Metadata = withComparisonOpenGraph({
  title: "השוואת תוספי קריאטין | בארי",
  description:
    "השוואת 18 תוספי קריאטין מהמדף הישראלי מול 13 מותגי ייחוס עולמיים — דירוג בארי לפי שקיפות מינון, צורה, בדיקת צד-שלישי ומחיר לגרם אפקטיבי. כלי הכרה לפני קנייה.",
});

export default async function CreatineComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/creatine" products={creatineProducts} />
      <CreatineComparisonPage
        israeliProducts={creatineIsraeliProducts}
        worldwideProducts={creatineWorldwideProducts}
        metadataLine={creatineMetadataLine}
        hero={creatineHero}
        prologueSentences={creatinePrologueSentences}
        methodologyLines={creatineMethodologyLines}
        categoryNote={creatineCategoryNote}
        initialExpandedProductId={initialExpandedProductId}
      />
    </>
  );
}
