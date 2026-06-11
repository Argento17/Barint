import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { FeaturedBreakfastCerealsIntelligenceCard } from "@/components/hashvaot/featured-breakfast-cereals-intelligence-card";
import { FeaturedButterIntelligenceCard } from "@/components/hashvaot/featured-butter-intelligence-card";
import { FeaturedGranolaIntelligenceCard } from "@/components/hashvaot/featured-granola-intelligence-card";
import { FeaturedBreadIntelligenceCardLite } from "@/components/hashvaot/featured-bread-intelligence-card-lite";
import { FeaturedCheeseIntelligenceCard } from "@/components/hashvaot/featured-cheese-intelligence-card";
import { FeaturedHardCheesesIntelligenceCard } from "@/components/hashvaot/featured-hard-cheeses-intelligence-card";
import { FeaturedHummusIntelligenceCard } from "@/components/hashvaot/featured-hummus-intelligence-card";
import { FeaturedJuicesIntelligenceCard } from "@/components/hashvaot/featured-juices-intelligence-card";
import { FeaturedMaadanimIntelligenceCard } from "@/components/hashvaot/featured-maadanim-intelligence-card";
import { FeaturedMilkIntelligenceCard } from "@/components/hashvaot/featured-milk-intelligence-card";
import { FeaturedSaltySnacksIntelligenceCard } from "@/components/hashvaot/featured-salty-snacks-intelligence-card";
import { FeaturedSnacksIntelligenceCard } from "@/components/hashvaot/featured-snacks-intelligence-card";
import { FeaturedVegetableSpreadsIntelligenceCard } from "@/components/hashvaot/featured-vegetable-spreads-intelligence-card";
import { HomeContainer } from "@/components/home/section-frame";
import { BREAD_COMPARISON_HREF } from "@/lib/blog/bread-analysis-content";
import { SNACK_COMPARISON_HREF } from "@/lib/blog/snack-analysis-content";
import { breadProducts } from "@/lib/comparisons/bread-page-data";
import { SNACK_REPORT_STATS } from "@/lib/comparisons/snack-page-data";
import { snacksProducts } from "@/lib/comparisons/snacks-comparison-page-data";
import { hummusProducts, hummusPrologueSentences } from "@/lib/comparisons/hummus-comparison-page-data";
import { maadanimProducts } from "@/lib/comparisons/maadanim-page-data";
import { vegetableSpreadsProducts, vegetableSpreadsPrologueSentences } from "@/lib/comparisons/vegetable-spreads-comparison-page-data";
import { cheeseProducts, cheesePrologueSentences } from "@/lib/comparisons/cheese-comparison-page-data";
import { cerealsProducts } from "@/lib/comparisons/cereals-page-data";
import { butterProducts, butterPrologueSentences } from "@/lib/comparisons/butter-page-data";
import { granolaProducts } from "@/lib/comparisons/granola-page-data";
import { milkProducts } from "@/lib/comparisons/milk-page-data";
import { saltySnacksProducts } from "@/lib/comparisons/salty-snacks-page-data";
import { hardCheesesProducts } from "@/lib/comparisons/hard-cheeses-page-data";
import { juicesProducts } from "@/lib/comparisons/juices-page-data";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

export const metadata: Metadata = {
  title: "השוואות | Bari",
  description:
    "השוואות אינטליגנציית מזון אינטראקטיביות — ניתוח רב-פרמטרי של מוצרים דומים.",
};

const BUTTER_COMPARISON_HREF = "/hashvaot/butter";
const CEREALS_COMPARISON_HREF = "/hashvaot/breakfast-cereals";
const GRANOLA_COMPARISON_HREF = "/hashvaot/granola";
const HARD_CHEESES_COMPARISON_HREF = "/hashvaot/hard-cheeses";
const HUMMUS_COMPARISON_HREF = "/hashvaot/hummus";
const JUICES_COMPARISON_HREF = "/hashvaot/juices";
const MAADANIM_COMPARISON_HREF = "/hashvaot/maadanim";
const VEGETABLE_SPREADS_COMPARISON_HREF = "/hashvaot/vegetable-spreads";
const CHEESE_COMPARISON_HREF = "/hashvaot/cheese";
const MILK_COMPARISON_HREF = "/hashvaot/milk-comparison";

export default function HashvaotIndexPage() {
  const butterDescription = `${butterPrologueSentences[0]} ${butterProducts.length} מוצרים בדף ההשוואה.`;
  const cerealsDescription = `רוב דגני הבוקר במדף נושאים תווית «דגנים מלאים» — אבל לא כולם מצדיקים אותה. בדקנו ${cerealsProducts.length} מוצרים: אף אחד לא הגיע ל-A, הציון הגבוה ביותר הוא 75/B, וחמישה מוצרים מיועדים לילדים. גרנולה ומוזלי הופרדו לקטגוריה משלהם.`;
  const granolaDescription = `גרנולה ומוזלי נראים כמו בחירת הבריאות של המדף — אבל ${granolaProducts.length} המוצרים שבדקנו נעים בין 76/B ל-29/E, פער של 47 נקודות. הציון תלוי בכמות הסוכר, השומן והסירופ בפועל, לא בתדמית.`;
  const productCount = milkProducts.length;
  const milkDescription = `השוואה בין ${productCount} מוצרי חלב ומשקאות חלב פופולריים בישראל — כולל חלב פרה, סויה, שיבולת שועל, שקדים ומוצרים עתירי חלבון. Bari מנתחת רכיבים, ערכים תזונתיים, רמת עיבוד ותוספים כדי להציג את הטריידאופים בין המוצרים.`;
  const breadDescription = `דוח השוואה מאוחד ללחם, פיתות וקרקרים: 256 מוצרים נסרקו, 81 קיבלו מספיק נתונים לניתוח מהימן, ו-${breadProducts.length} נבחרו להצגה העריכתית בדף.`;
  const snacksDescription = `דוח השוואה לחטיפי המדף: ${SNACK_REPORT_STATS.scraped} נסרקו ב${SNACK_REPORT_STATS.retailer}, ${snacksProducts.length} מוצרים בדף ההשוואה.`;
  const hummusDescription = `${hummusPrologueSentences[0]} ${hummusProducts.length} מוצרים בדף ההשוואה.`;
  const maadanimDescription = `מעדן נראה כמו פינוק חלבי פשוט — אבל המדף מתפצל לשניים: קינוחים שהמרקם שלהם בנוי על מייצבים ועמילן, ומוצרים מועשרי חלבון שמתפקדים כחטיף. החלבון נע מ-0 גרם (פודינג וג'לי שאינם חלב) ועד כ-10 גרם, וזה המדד שמפריד ביניהם. ${maadanimProducts.length} מוצרים בדף ההשוואה.`;
  const vegetableSpreadsDescription = `${vegetableSpreadsPrologueSentences[0]} ${vegetableSpreadsProducts.length} מוצרים בדף ההשוואה.`;
  // TASK-152: reviewed & refined by Content Agent — 4 sub-pools; cream-cheese spreads fall
  // once real fat is counted (16–30%, EV-029).
  const cheeseDescription = `${cheesePrologueSentences[0]} ממרחי גבינת השמנת נופלים נמוך יותר ברגע שסופרים את השומן האמיתי שבהם — עד 30 אחוז. ${cheeseProducts.length} מוצרים בדף ההשוואה.`;
  const juicesDescription = `בדקנו ${juicesProducts.length} מיצים ומשקאות פירות: מיץ 100%, נקטרים, שייקים וסחוטי קר. רק מוצר אחד הגיע ל-A — סחוט תפוזים טרי. גם מיץ 100% הוא סוכר נוזלי: 7–17 גרם ל-100 מ"ל ללא סיבים וללא תחושת שובע.`;
  const hardCheesesDescription = `בדקנו ${hardCheesesProducts.length} גבינות קשות וצהובות מיוחננוף: 18 קיבלו B, 11 קיבלו C ואחד קיבל D — אף גבינה לא הגיעה ל-A. גאודה ממרכיבים מינימליים מובילת המדף; גבינות 'לייט' עם מייצבים מקבלות ציון נמוך יותר.`;
  const saltySnacksDescription = `בדקנו ${saltySnacksProducts.length} חטיפים מלוחים מהמדף הישראלי: צ'יפס, פופקורן, פצפוצי אורז, פרצלים וחטיפי קטניות. 7 קיבלו A, 16 B — חטיפי קטניות אפויים ופצפוצי אורז פשוטים; 18 C ו-13 D או E. חטיפים 'אפויים' ו'ללא גלוטן' לא בהכרח מגיעים גבוה.`;

  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="py-14 md:py-20">
        <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#1F8F6A]/80">
          Bari comparisons
        </p>
        <h1 className="mt-3 max-w-3xl text-balance text-4xl font-extrabold tracking-[-0.05em] md:text-5xl">
          השוואות אינטליגנציית מזון
        </h1>
        <p className="mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]">
          חוויות השוואה אינטראקטיביות — לא מאמרים סטטיים. כל דף בוחן מוצרים דומים לפי פרמטרים
          ומציג טריידאופים בהקשר הנכון.
        </p>

        <div className="mt-12 space-y-6">
          <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-[#7A817C]">
            השוואה מומלצת
          </h2>

          <FeaturedMilkIntelligenceCard href={MILK_COMPARISON_HREF} description={milkDescription} />

          <p className="text-sm text-[#4E5663]">
            רוצים את הסיפור מאחורי הממצאים?{" "}
            <Link
              href="/blog/milk-analysis"
              className="font-semibold text-[#1F8F6A] underline-offset-2 hover:underline"
            >
              קראו את הניתוח בבלוג
            </Link>
            — המאמר משלים את מנוע ההשוואה, לא מחליף אותו.
          </p>
        </div>

        <div className="mt-12 space-y-6">
          <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-[#7A817C]">
            ניתוח עדכני
          </h2>
          <FeaturedBreakfastCerealsIntelligenceCard
            href={CEREALS_COMPARISON_HREF}
            description={cerealsDescription}
          />
          <FeaturedGranolaIntelligenceCard
            href={GRANOLA_COMPARISON_HREF}
            description={granolaDescription}
          />
          <FeaturedButterIntelligenceCard
            href={BUTTER_COMPARISON_HREF}
            description={butterDescription}
          />
          <FeaturedMaadanimIntelligenceCard
            href={MAADANIM_COMPARISON_HREF}
            description={maadanimDescription}
          />
          <FeaturedBreadIntelligenceCardLite href={BREAD_COMPARISON_HREF} description={breadDescription} />
          <FeaturedSnacksIntelligenceCard href={SNACK_COMPARISON_HREF} description={snacksDescription} />
          <FeaturedHummusIntelligenceCard
            href={HUMMUS_COMPARISON_HREF}
            description={hummusDescription}
          />
          <FeaturedVegetableSpreadsIntelligenceCard
            href={VEGETABLE_SPREADS_COMPARISON_HREF}
            description={vegetableSpreadsDescription}
          />
          <FeaturedCheeseIntelligenceCard
            href={CHEESE_COMPARISON_HREF}
            description={cheeseDescription}
          />
          <FeaturedHardCheesesIntelligenceCard
            href={HARD_CHEESES_COMPARISON_HREF}
            description={hardCheesesDescription}
          />
          <FeaturedJuicesIntelligenceCard
            href={JUICES_COMPARISON_HREF}
            description={juicesDescription}
          />
          <FeaturedSaltySnacksIntelligenceCard
            href="/hashvaot/salty-snacks"
            description={saltySnacksDescription}
          />
        </div>

        <Link
          href="/"
          className="mt-12 inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
        >
          <ArrowLeft className="size-4" aria-hidden />
          חזרה לדף הבית
        </Link>
      </HomeContainer>
    </main>
  );
}
