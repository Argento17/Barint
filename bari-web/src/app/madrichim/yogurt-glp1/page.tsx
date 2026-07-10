// GLP-1 / suppressed-appetite high-protein yogurt guide — /madrichim/yogurt-glp1
// (TASK-504A). Reuses LIVE grade/score/image data from the yogurt-spoonable comparison
// corpus (see src/lib/guides/yogurt-glp1-guide-data.ts) — no new scores, no rescoring.
//
// noindex: this page has not yet had a Design Agent vision-critic pass, nor an owner
// index/robots approval (same pre-launch pattern used for the /madrichim/magnesium and
// /madrichim/creatine guide builds). Flip `robots.index` to true only after that
// approval — this is a reversible, non-consumer-facing technical default, not a content
// judgment (Frontend does not self-approve content for search visibility).

import type { Metadata } from "next";

import { YogurtGlp1GuidePage } from "@/components/guides/yogurt-glp1-guide-page";
import {
  yogurtGlp1CategoryNote,
  yogurtGlp1DrinkableCallout,
  yogurtGlp1FullListNote,
  yogurtGlp1Hero,
  yogurtGlp1HowToRead,
  yogurtGlp1Shortlist,
} from "@/lib/guides/yogurt-glp1-guide-data";

export const metadata: Metadata = {
  title: "יוגורט עתיר חלבון: מדריך לבחירה | Bari",
  description:
    "מדריך לבחירת יוגורט עתיר חלבון מתוך המדף הישראלי, ממוין לפי חלבון, נתרן וסוכר, מבוסס על הציונים שכבר פורסמו בהשוואת היוגורט.",
  robots: { index: false, follow: false },
};

export default function YogurtGlp1GuideRoute() {
  return (
    <YogurtGlp1GuidePage
      hero={yogurtGlp1Hero}
      howToRead={yogurtGlp1HowToRead}
      shortlist={yogurtGlp1Shortlist}
      fullListNote={yogurtGlp1FullListNote}
      drinkableCallout={yogurtGlp1DrinkableCallout}
      categoryNote={yogurtGlp1CategoryNote}
    />
  );
}
