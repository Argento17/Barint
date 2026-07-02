import type { Metadata } from "next";

import { FeaturedBreakfastCerealsIntelligenceCard } from "@/components/hashvaot/featured-breakfast-cereals-intelligence-card";
import { FeaturedGranolaIntelligenceCard } from "@/components/hashvaot/featured-granola-intelligence-card";
import { FeaturedBreadIntelligenceCardLite } from "@/components/hashvaot/featured-bread-intelligence-card-lite";
import { FeaturedCheeseIntelligenceCard } from "@/components/hashvaot/featured-cheese-intelligence-card";
import { FeaturedHardCheesesIntelligenceCard } from "@/components/hashvaot/featured-hard-cheeses-intelligence-card";
import { FeaturedHummusIntelligenceCard } from "@/components/hashvaot/featured-hummus-intelligence-card";
import { FeaturedJuicesIntelligenceCard } from "@/components/hashvaot/featured-juices-intelligence-card";
import { FeaturedMilkIntelligenceCard } from "@/components/hashvaot/featured-milk-intelligence-card";
import { FeaturedSnacksIntelligenceCard } from "@/components/hashvaot/featured-snacks-intelligence-card";
import { FeaturedProteinBarsIntelligenceCard } from "@/components/hashvaot/featured-protein-bars-intelligence-card";
import { FeaturedChocolateTabletsIntelligenceCard } from "@/components/hashvaot/featured-chocolate-tablets-intelligence-card";
import { FeaturedChocolateBarsIntelligenceCard } from "@/components/hashvaot/featured-chocolate-bars-intelligence-card";
import { FeaturedBrinedCheesesIntelligenceCard } from "@/components/hashvaot/featured-brined-cheeses-intelligence-card";
import { FeaturedCakesHardCookiesIntelligenceCard } from "@/components/hashvaot/featured-cakes-hard-cookies-intelligence-card";
import { FeaturedCookiesCoffeeIntelligenceCard } from "@/components/hashvaot/featured-cookies-coffee-intelligence-card";
import { FeaturedCrackersIntelligenceCard } from "@/components/hashvaot/featured-crackers-intelligence-card";
import {
  HashvaotComparisonCardGrid,
} from "@/components/hashvaot/hashvaot-group-section";
import { HashvaotCategoryLanding } from "@/components/hashvaot/hashvaot-category-landing";
import { BREAD_COMPARISON_HREF } from "@/lib/blog/bread-analysis-content";
import { SNACK_COMPARISON_HREF } from "@/lib/blog/snack-analysis-content";
import { breadProducts } from "@/lib/comparisons/bread-comparison-page-data";
import { snacksProducts } from "@/lib/comparisons/snacks-comparison-page-data";
import { proteinBarsProducts } from "@/lib/comparisons/protein-bars-comparison-page-data";
import { chocolateTabletsProducts } from "@/lib/comparisons/chocolate-tablets-comparison-page-data";
import { chocolateBarsProducts } from "@/lib/comparisons/chocolate-bars-comparison-page-data";
import { hummusProducts, hummusPrologueSentences } from "@/lib/comparisons/hummus-comparison-page-data";
import { cheeseProducts, cheesePrologueSentences } from "@/lib/comparisons/cheese-page-data";
import { cerealsProducts } from "@/lib/comparisons/cereals-page-data";
import { granolaProducts } from "@/lib/comparisons/granola-page-data";
import { milkProducts } from "@/lib/comparisons/milk-page-data";
import { hardCheesesProducts } from "@/lib/comparisons/hard-cheeses-page-data";
import { juicesProducts } from "@/lib/comparisons/juices-page-data";
import { brinedCheesesProducts, brinedCheesesPrologueSentences } from "@/lib/comparisons/brined-cheeses-page-data";
import { cakesHardCookiesProducts } from "@/lib/comparisons/cakes-hard-cookies-page-data";
import { cookiesCoffeeProducts } from "@/lib/comparisons/cookies-coffee-page-data";
import { crackersProducts } from "@/lib/comparisons/crackers-page-data";
import Link from "next/link";

export const metadata: Metadata = {
  title: "מוצרי סופרמרקט | Bari",
  description:
    "השוואות מוצרי סופרמרקט — חלב, לחם, דגני בוקר, גבינות, חטיפים ועוד. ניתוח רב-פרמטרי של מוצרים דומים.",
};

const CEREALS_COMPARISON_HREF = "/hashvaot/breakfast-cereals";
const CHOCOLATE_TABLETS_COMPARISON_HREF = "/hashvaot/chocolate-tablets";
const CHOCOLATE_BARS_COMPARISON_HREF = "/hashvaot/chocolate-bars";
const GRANOLA_COMPARISON_HREF = "/hashvaot/granola";
const HARD_CHEESES_COMPARISON_HREF = "/hashvaot/hard-cheeses";
const HUMMUS_COMPARISON_HREF = "/hashvaot/hummus";
const JUICES_COMPARISON_HREF = "/hashvaot/juices";
const CHEESE_COMPARISON_HREF = "/hashvaot/cheese";
const MILK_COMPARISON_HREF = "/hashvaot/milk-comparison";
const BRINED_CHEESES_COMPARISON_HREF = "/hashvaot/brined-cheeses";
const CAKES_COMPARISON_HREF = "/hashvaot/cakes";
const COOKIES_COFFEE_COMPARISON_HREF = "/hashvaot/cookies-coffee";
const CRACKERS_COMPARISON_HREF = "/hashvaot/crackers";

export default function SupermarketCategoryPage() {
  const cerealsDescription = `רוב דגני הבוקר במדף נושאים תווית «דגנים מלאים» — אבל לא כולם מצדיקים אותה. בדקנו ${cerealsProducts.length} מוצרים: אף אחד לא הגיע ל-A, הציון הגבוה ביותר הוא 75/B, וחמישה מוצרים מיועדים לילדים. גרנולה ומוזלי הופרדו לקטגוריה משלהם.`;
  const granolaDescription = `גרנולה ומוזלי נראים כמו בחירת הבריאות של המדף — אבל ${granolaProducts.length} המוצרים שבדקנו נעים בין 76/B ל-29/E, פער של 47 נקודות. הציון תלוי בכמות הסוכר, השומן והסירופ בפעול, לא בתדמית.`;
  const milkDescription = `השוואה בין ${milkProducts.length} מוצרי חלב ומשקאות חלב פופולריים בישראל — כולל חלב פרה, סויה, שיבולת שועל, שקדים ומוצרים עתירי חלבון. Bari מנתחת רכיבים, ערכים תזונתיים, רמת עיבוד ותוספים כדי להציג את הטריידאופים בין המוצרים.`;
  const breadDescription = `דוח השוואה ללחם ולפיתות: 256 מוצרים נסרקו, 81 קיבלו מספיק נתונים לניתוח מהימן, ו-${breadProducts.length} נבחרו להצגה העריכתית בדף. הקרקרים הופרדו לקטגוריה משלהם.`;
  const snacksDescription = `דוח השוואה לחטיפי הדגנים: ${snacksProducts.length} חטיפי דגנים בדף ההשוואה, מתוך מדף החטיפים שנסקר בשופרסל.`;
  const proteinBarsDescription = `דוח השוואה לחטיפי החלבון: ${proteinBarsProducts.length} חטיפים עם 25–34 גרם חלבון ל-100 גרם — והמחיר ההנדסי שמגיע איתם. קטגוריה נפרדת מחטיפי הדגנים.`;
  const chocolateTabletsDescription = `בדקנו ${chocolateTabletsProducts.length} טבלאות שוקולד: מריר 90% עד שוקולד לבן ממולא. הציון הגבוה ביותר הוא C — כל השוקולד הוא ממתק, אבל הפער בין 2 גרם סוכר ל-65 גרם הוא אמיתי.`;
  const chocolateBarsDescription = `בדקנו ${chocolateBarsProducts.length} חטיפי שוקולד: כולם ציון E, 45–60 גרם סוכר ל-100 גרם. ההבדל היחידי הוא בין חטיף עם בוטנים לחטיף שהוא רק סוכר ושמן מתחת לציפוי.`;
  const hummusDescription = `${hummusPrologueSentences[0]} ${hummusProducts.length} מוצרים בדף ההשוואה.`;
  const cheeseDescription = `${cheesePrologueSentences[0]} ממרחי גבינת השמנת נופלים נמוך יותר ברגע שסופרים את השומן האמיתי שבהם — עד 30 אחוז. ${cheeseProducts.length} מוצרים בדף ההשוואה.`;
  const juicesDescription = `בדקנו ${juicesProducts.length} מיצים ומשקאות פירות: מיץ 100%, נקטרים, שייקים וסחוטי קר. רק מיצים סחוטים ב-100% הגיעו ל-A. גם מיץ 100% הוא סוכר נוזלי, ללא סיבים וללא תחושת שובע.`;
  const hardCheesesDescription = `בדקנו ${hardCheesesProducts.length} גבינות קשות וצהובות: רוב המדף מתקבץ סביב B, כי השומן הרווי הוא הגורם הכובל שמשותף לכולן. גבינה דלת-שומן אחת בלבד יוצאת מהמקבץ ומגיעה ל-A; גבינות מעובדות עם מייצבים מקבלות ציון נמוך יותר.`;
  const brinedCheesesDescription = `${brinedCheesesPrologueSentences[0]} ${brinedCheesesProducts.length} מוצרים בדף ההשוואה.`;
  const cookiesCoffeeDescription = `ביסקוויטים מתוקים מעובדים, מלווי הקפה של המדף הישראלי. ${cookiesCoffeeProducts.length} מוצרים נבדקו — ציון C הוא תקרית הקטגוריה. ההבדלים: סוג השומן, כמות הסוכר, מורכבות רשימת הרכיבים.`;
  const cCount = cakesHardCookiesProducts.filter((p) => p.grade === "C").length;
  const dCount = cakesHardCookiesProducts.filter((p) => p.grade === "D").length;
  const eCount = cakesHardCookiesProducts.filter((p) => p.grade === "E").length;
  const cakesTopScore = Math.max(...cakesHardCookiesProducts.map((p) => p.score ?? 0)).toFixed(1);
  const cakesDescription = `בדקנו ${cakesHardCookiesProducts.length} עוגות מהמדף הישראלי — אף מוצר לא הגיע ל-A או ל-B. ${cCount} קיבלו C (הציון הגבוה ביותר הוא ${cakesTopScore}), ${dCount} קיבלו D ו-${eCount} קיבלו E. ציון C הוא תקרית הקטגוריה, לא הישג.`;
  const crackersAGrade = crackersProducts.filter((p) => p.grade === "A").length;
  const crackersBGrade = crackersProducts.filter((p) => p.grade === "B").length;
  const crackersTop = crackersProducts.find((p) => p.rank === 1);
  const crackersDescription = `בדקנו ${crackersProducts.length} קרקרים מהמדף הישראלי: ${crackersAGrade} הגיע ל-A ו-${crackersBGrade} קיבלו B. ${crackersTop ? `${crackersTop.name} מוביל את הדף` : "המוביל בדף"} — קטגוריה נפרדת מלחם, כי בקרקר היבש הקלוריות ל-100 גרם גבוהות מטבעו.`;

  return (
    <HashvaotCategoryLanding
      eyebrow="Bari comparisons · סופרמרקט"
      title="מוצרי סופרמרקט"
      intro="חוויות השוואה אינטראקטיביות — לא מאמרים סטטיקיים. כל דף בוחן מוצרים דומים לפי פרמטרים ומציג טריידאופים בהקשר הנכון."
    >
      <HashvaotComparisonCardGrid
        lead={
          <>
            <FeaturedMilkIntelligenceCard
              href={MILK_COMPARISON_HREF}
              description={milkDescription}
            />
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
          </>
        }
      >
        <FeaturedBreakfastCerealsIntelligenceCard
          href={CEREALS_COMPARISON_HREF}
          description={cerealsDescription}
        />
        <FeaturedGranolaIntelligenceCard
          href={GRANOLA_COMPARISON_HREF}
          description={granolaDescription}
        />
        <FeaturedBrinedCheesesIntelligenceCard
          href={BRINED_CHEESES_COMPARISON_HREF}
          description={brinedCheesesDescription}
        />
        <FeaturedCookiesCoffeeIntelligenceCard
          href={COOKIES_COFFEE_COMPARISON_HREF}
          description={cookiesCoffeeDescription}
        />
        <FeaturedCakesHardCookiesIntelligenceCard
          href={CAKES_COMPARISON_HREF}
          description={cakesDescription}
        />
        <FeaturedBreadIntelligenceCardLite
          href={BREAD_COMPARISON_HREF}
          description={breadDescription}
        />
        <FeaturedCrackersIntelligenceCard
          href={CRACKERS_COMPARISON_HREF}
          description={crackersDescription}
        />
        <FeaturedSnacksIntelligenceCard
          href={SNACK_COMPARISON_HREF}
          description={snacksDescription}
        />
        <FeaturedProteinBarsIntelligenceCard
          href="/hashvaot/protein-bars"
          description={proteinBarsDescription}
        />
        <FeaturedChocolateTabletsIntelligenceCard
          href={CHOCOLATE_TABLETS_COMPARISON_HREF}
          description={chocolateTabletsDescription}
        />
        <FeaturedChocolateBarsIntelligenceCard
          href={CHOCOLATE_BARS_COMPARISON_HREF}
          description={chocolateBarsDescription}
        />
        <FeaturedHummusIntelligenceCard
          href={HUMMUS_COMPARISON_HREF}
          description={hummusDescription}
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
      </HashvaotComparisonCardGrid>
    </HashvaotCategoryLanding>
  );
}
