import type { Metadata } from "next";

import { CakesHardCookiesComparisonPage } from "@/components/comparisons/cakes-hard-cookies-comparison-page";
import {
  cakesHardCookiesCategoryNote,
  cakesHardCookiesHero,
  cakesHardCookiesHighSugarIds,
  cakesHardCookiesLensOptions,
  cakesHardCookiesMetadataLine,
  cakesHardCookiesMethodologyLines,
  cakesHardCookiesPhvoIds,
  cakesHardCookiesPrologueSentences,
  cakesHardCookiesProducts,
} from "@/lib/comparisons/cakes-hard-cookies-page-data";

export const metadata: Metadata = {
  title: "השוואת עוגות | Bari",
  description:
    "השוואת 65 עוגות מהמדף הישראלי — ציון Bari, סוכר, שומן רווי ורשימת רכיבים. מידע, לא המלצה.",
};

export default function CakesComparisonRoute() {
  return (
    <CakesHardCookiesComparisonPage
      products={cakesHardCookiesProducts}
      metadataLine={cakesHardCookiesMetadataLine}
      hero={cakesHardCookiesHero}
      prologueSentences={cakesHardCookiesPrologueSentences}
      methodologyLines={cakesHardCookiesMethodologyLines}
      categoryNote={cakesHardCookiesCategoryNote}
      lensOptions={cakesHardCookiesLensOptions}
      phvoIds={cakesHardCookiesPhvoIds}
      highSugarIds={cakesHardCookiesHighSugarIds}
    />
  );
}
