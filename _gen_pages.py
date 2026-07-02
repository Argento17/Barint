import pathlib

base = pathlib.Path("C:/Bari/bari-web/src")

# -- 4. /hashvaot/page.tsx  (hub, 4 category boxes) ---------------------------
(base / "app/hashvaot/page.tsx").write_text("""\
import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { HashvaotCategoryBox } from "@/components/hashvaot/hashvaot-category-box";
import { HASHVAOT_CATEGORIES } from "@/lib/hashvaot/hashvaot-categories";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

export const metadata: Metadata = {
  title: "\u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea | Bari",
  description:
    "\u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea \u05d0\u05d9\u05e0\u05d8\u05e8\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9\u05d5\u05ea \u05de\u05d4\u05de\u05d3\u05e3 \u2014 \u05de\u05d6\u05d5\u05df, \u05ea\u05d5\u05e1\u05e4\u05d9\u05dd \u05d5\u05e2\u05d5\u05d3. \u05e0\u05d9\u05ea\u05d5\u05d7 \u05e8\u05d1-\u05e4\u05e8\u05de\u05d8\u05e8\u05d9 \u05e9\u05dc \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05d3\u05d5\u05de\u05d9\u05dd.",
};

export default function HashvaotIndexPage() {
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
          \u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea \u05de\u05d4\u05de\u05d3\u05e3
        </h1>
        <p className="mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]">
          \u05d7\u05d5\u05d5\u05d9\u05d5\u05ea \u05d4\u05e9\u05d5\u05d5\u05d0\u05d4 \u05d0\u05d9\u05e0\u05d8\u05e8\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9\u05d5\u05ea \u2014 \u05dc\u05d0 \u05de\u05d0\u05de\u05e8\u05d9\u05dd \u05e1\u05d8\u05d8\u05d9\u05e7\u05d9\u05d9\u05dd. \u05db\u05dc \u05d3\u05e3 \u05d1\u05d5\u05d7\u05df \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05d3\u05d5\u05de\u05d9\u05dd \u05dc\u05e4\u05d9 \u05e4\u05e8\u05de\u05d8\u05e8\u05d9\u05dd \u05d5\u05de\u05e6\u05d9\u05d2 \u05d8\u05e8\u05d9\u05d9\u05d3\u05d0\u05d5\u05e4\u05d9\u05dd \u05d1\u05d4\u05e7\u05e9\u05e8 \u05d4\u05e0\u05db\u05d5\u05df.
        </p>

        <div className="mt-12 grid gap-5 sm:grid-cols-2">
          {HASHVAOT_CATEGORIES.map((cat) => (
            <HashvaotCategoryBox key={cat.id} category={cat} />
          ))}
        </div>

        <Link
          href="/"
          className="mt-10 inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
        >
          <ArrowLeft className="size-4" aria-hidden />
          \u05d7\u05d6\u05e8\u05d4 \u05dc\u05d3\u05e3 \u05d4\u05d1\u05d9\u05ea
        </Link>
      </HomeContainer>
    </main>
  );
}
""", encoding="utf-8")
print("hashvaot/page.tsx written")

# -- 5. /hashvaot/supermarket/page.tsx ----------------------------------------
(base / "app/hashvaot/supermarket").mkdir(parents=True, exist_ok=True)
(base / "app/hashvaot/supermarket/page.tsx").write_text("""\
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
import Link from "next/link";

export const metadata: Metadata = {
  title: "\u05de\u05d5\u05e6\u05e8\u05d9 \u05e1\u05d5\u05e4\u05e8\u05de\u05e8\u05e7\u05d8 | Bari",
  description:
    "\u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea \u05de\u05d5\u05e6\u05e8\u05d9 \u05e1\u05d5\u05e4\u05e8\u05de\u05e8\u05e7\u05d8 \u2014 \u05d7\u05dc\u05d1, \u05dc\u05d7\u05dd, \u05d3\u05d2\u05e0\u05d9 \u05d1\u05d5\u05e7\u05e8, \u05d2\u05d1\u05d9\u05e0\u05d5\u05ea, \u05d7\u05d8\u05d9\u05e4\u05d9\u05dd \u05d5\u05e2\u05d5\u05d3. \u05e0\u05d9\u05ea\u05d5\u05d7 \u05e8\u05d1-\u05e4\u05e8\u05de\u05d8\u05e8\u05d9 \u05e9\u05dc \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05d3\u05d5\u05de\u05d9\u05dd.",
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

export default function SupermarketCategoryPage() {
  const cerealsDescription = `\u05e8\u05d5\u05d1 \u05d3\u05d2\u05e0\u05d9 \u05d4\u05d1\u05d5\u05e7\u05e8 \u05d1\u05de\u05d3\u05e3 \u05e0\u05d5\u05e9\u05d0\u05d9\u05dd \u05ea\u05d5\u05d5\u05d9\u05ea \u00ab\u05d3\u05d2\u05e0\u05d9\u05dd \u05de\u05dc\u05d0\u05d9\u05dd\u00bb \u2014 \u05d0\u05d1\u05dc \u05dc\u05d0 \u05db\u05d5\u05dc\u05dd \u05de\u05e6\u05d3\u05d9\u05e7\u05d9\u05dd \u05d0\u05d5\u05ea\u05d4. \u05d1\u05d3\u05e7\u05e0\u05d5 ${cerealsProducts.length} \u05de\u05d5\u05e6\u05e8\u05d9\u05dd: \u05d0\u05e3 \u05d0\u05d7\u05d3 \u05dc\u05d0 \u05d4\u05d2\u05d9\u05e2 \u05dc-A, \u05d4\u05e6\u05d9\u05d5\u05df \u05d4\u05d2\u05d1\u05d5\u05d4 \u05d1\u05d9\u05d5\u05ea\u05e8 \u05d4\u05d5\u05d0 75/B, \u05d5\u05d7\u05de\u05d9\u05e9\u05d4 \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05de\u05d9\u05d5\u05e2\u05d3\u05d9\u05dd \u05dc\u05d9\u05dc\u05d3\u05d9\u05dd. \u05d2\u05e8\u05e0\u05d5\u05dc\u05d4 \u05d5\u05de\u05d5\u05d6\u05dc\u05d9 \u05d4\u05d5\u05e4\u05e8\u05d3\u05d5 \u05dc\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d4 \u05de\u05e9\u05dc\u05d4\u05dd.`;
  const granolaDescription = `\u05d2\u05e8\u05e0\u05d5\u05dc\u05d4 \u05d5\u05de\u05d5\u05d6\u05dc\u05d9 \u05e0\u05e8\u05d0\u05d9\u05dd \u05db\u05de\u05d5 \u05d1\u05d7\u05d9\u05e8\u05ea \u05d4\u05d1\u05e8\u05d9\u05d0\u05d5\u05ea \u05e9\u05dc \u05d4\u05de\u05d3\u05e3 \u2014 \u05d0\u05d1\u05dc ${granolaProducts.length} \u05d4\u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05e9\u05d1\u05d3\u05e7\u05e0\u05d5 \u05e0\u05e2\u05d9\u05dd \u05d1\u05d9\u05df 76/B \u05dc-29/E, \u05e4\u05e2\u05e8 \u05e9\u05dc 47 \u05e0\u05e7\u05d5\u05d3\u05d5\u05ea. \u05d4\u05e6\u05d9\u05d5\u05df \u05ea\u05dc\u05d5\u05d9 \u05d1\u05db\u05de\u05d5\u05ea \u05d4\u05e1\u05d5\u05db\u05e8, \u05d4\u05e9\u05d5\u05de\u05df \u05d5\u05d4\u05e1\u05d9\u05e8\u05d5\u05e4 \u05d1\u05e4\u05e2\u05d5\u05dc, \u05dc\u05d0 \u05d1\u05ea\u05d3\u05de\u05d9\u05ea.`;
  const milkDescription = `\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4 \u05d1\u05d9\u05df ${milkProducts.length} \u05de\u05d5\u05e6\u05e8\u05d9 \u05d7\u05dc\u05d1 \u05d5\u05de\u05e9\u05e7\u05d0\u05d5\u05ea \u05d7\u05dc\u05d1 \u05e4\u05d5\u05e4\u05d5\u05dc\u05e8\u05d9\u05d9\u05dd \u05d1\u05d9\u05e9\u05e8\u05d0\u05dc \u2014 \u05db\u05d5\u05dc\u05dc \u05d7\u05dc\u05d1 \u05e4\u05e8\u05d4, \u05e1\u05d5\u05d9\u05d4, \u05e9\u05d9\u05d1\u05d5\u05dc\u05ea \u05e9\u05d5\u05e2\u05dc, \u05e9\u05e7\u05d3\u05d9\u05dd \u05d5\u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05e2\u05ea\u05d9\u05e8\u05d9 \u05d7\u05dc\u05d1\u05d5\u05df. Bari \u05de\u05e0\u05ea\u05d7\u05ea \u05e8\u05db\u05d9\u05d1\u05d9\u05dd, \u05e2\u05e8\u05db\u05d9\u05dd \u05ea\u05d6\u05d5\u05e0\u05ea\u05d9\u05d9\u05dd, \u05e8\u05de\u05ea \u05e2\u05d9\u05d1\u05d5\u05d3 \u05d5\u05ea\u05d5\u05e1\u05e4\u05d9\u05dd \u05db\u05d3\u05d9 \u05dc\u05d4\u05e6\u05d9\u05d2 \u05d0\u05ea \u05d4\u05d8\u05e8\u05d9\u05d9\u05d3\u05d0\u05d5\u05e4\u05d9\u05dd \u05d1\u05d9\u05df \u05d4\u05de\u05d5\u05e6\u05e8\u05d9\u05dd.`;
  const breadDescription = `\u05d3\u05d5\u05d7 \u05d4\u05e9\u05d5\u05d5\u05d0\u05d4 \u05de\u05d0\u05d5\u05d7\u05d3 \u05dc\u05dc\u05d7\u05dd, \u05e4\u05d9\u05ea\u05d5\u05ea \u05d5\u05e7\u05e8\u05e7\u05e8\u05d9\u05dd: 256 \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05e0\u05e1\u05e8\u05e7\u05d5, 81 \u05e7\u05d9\u05d1\u05dc\u05d5 \u05de\u05e1\u05e4\u05d9\u05e7 \u05e0\u05ea\u05d5\u05e0\u05d9\u05dd \u05dc\u05e0\u05d9\u05ea\u05d5\u05d7 \u05de\u05d4\u05d9\u05de\u05df, \u05d5-${breadProducts.length} \u05e0\u05d1\u05d7\u05e8\u05d5 \u05dc\u05d4\u05e6\u05d2\u05d4 \u05d4\u05e2\u05e8\u05d9\u05db\u05ea\u05d9\u05ea \u05d1\u05d3\u05e3.`;
  const snacksDescription = `\u05d3\u05d5\u05d7 \u05d4\u05e9\u05d5\u05d5\u05d0\u05d4 \u05dc\u05d7\u05d8\u05d9\u05e4\u05d9 \u05d4\u05d3\u05d2\u05e0\u05d9\u05dd: ${snacksProducts.length} \u05d7\u05d8\u05d9\u05e4\u05d9 \u05d3\u05d2\u05e0\u05d9\u05dd \u05d1\u05d3\u05e3 \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4, \u05de\u05ea\u05d5\u05da \u05de\u05d3\u05e3 \u05d4\u05d7\u05d8\u05d9\u05e4\u05d9\u05dd \u05e9\u05e0\u05e1\u05e7\u05e8 \u05d1\u05e9\u05d5\u05e4\u05e8\u05e1\u05dc.`;
  const proteinBarsDescription = `\u05d3\u05d5\u05d7 \u05d4\u05e9\u05d5\u05d5\u05d0\u05d4 \u05dc\u05d7\u05d8\u05d9\u05e4\u05d9 \u05d4\u05d7\u05dc\u05d1\u05d5\u05df: ${proteinBarsProducts.length} \u05d7\u05d8\u05d9\u05e4\u05d9\u05dd \u05e2\u05dd 25\u201334 \u05d2\u05e8\u05dd \u05d7\u05dc\u05d1\u05d5\u05df \u05dc-100 \u05d2\u05e8\u05dd \u2014 \u05d5\u05d4\u05de\u05d7\u05d9\u05e8 \u05d4\u05d4\u05e0\u05d3\u05e1\u05d9 \u05e9\u05de\u05d2\u05d9\u05e2 \u05d0\u05d9\u05ea\u05dd. \u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d4 \u05e0\u05e4\u05e8\u05d3\u05ea \u05de\u05d7\u05d8\u05d9\u05e4\u05d9 \u05d4\u05d3\u05d2\u05e0\u05d9\u05dd.`;
  const chocolateTabletsDescription = `\u05d1\u05d3\u05e7\u05e0\u05d5 ${chocolateTabletsProducts.length} \u05d8\u05d1\u05dc\u05d0\u05d5\u05ea \u05e9\u05d5\u05e7\u05d5\u05dc\u05d3: \u05de\u05e8\u05d9\u05e8 90% \u05e2\u05d3 \u05e9\u05d5\u05e7\u05d5\u05dc\u05d3 \u05dc\u05d1\u05df \u05de\u05de\u05d5\u05dc\u05d0. \u05d4\u05e6\u05d9\u05d5\u05df \u05d4\u05d2\u05d1\u05d5\u05d4 \u05d1\u05d9\u05d5\u05ea\u05e8 \u05d4\u05d5\u05d0 C \u2014 \u05db\u05dc \u05d4\u05e9\u05d5\u05e7\u05d5\u05dc\u05d3 \u05d4\u05d5\u05d0 \u05de\u05de\u05ea\u05e7, \u05d0\u05d1\u05dc \u05d4\u05e4\u05e2\u05e8 \u05d1\u05d9\u05df 2 \u05d2\u05e8\u05dd \u05e1\u05d5\u05db\u05e8 \u05dc-65 \u05d2\u05e8\u05dd \u05d4\u05d5\u05d0 \u05d0\u05de\u05d9\u05ea\u05d9.`;
  const chocolateBarsDescription = `\u05d1\u05d3\u05e7\u05e0\u05d5 ${chocolateBarsProducts.length} \u05d7\u05d8\u05d9\u05e4\u05d9 \u05e9\u05d5\u05e7\u05d5\u05dc\u05d3: \u05db\u05d5\u05dc\u05dd \u05e6\u05d9\u05d5\u05df E, 45\u201360 \u05d2\u05e8\u05dd \u05e1\u05d5\u05db\u05e8 \u05dc-100 \u05d2\u05e8\u05dd. \u05d4\u05d4\u05d1\u05d3\u05dc \u05d4\u05d9\u05d7\u05d9\u05d3\u05d9 \u05d4\u05d5\u05d0 \u05d1\u05d9\u05df \u05d7\u05d8\u05d9\u05e3 \u05e2\u05dd \u05d1\u05d5\u05d8\u05e0\u05d9\u05dd \u05dc\u05d7\u05d8\u05d9\u05e3 \u05e9\u05d4\u05d5\u05d0 \u05e8\u05e7 \u05e1\u05d5\u05db\u05e8 \u05d5\u05e9\u05de\u05df \u05de\u05ea\u05d7\u05ea \u05dc\u05e6\u05d9\u05e4\u05d5\u05d9.`;
  const hummusDescription = `${hummusPrologueSentences[0]} ${hummusProducts.length} \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05d1\u05d3\u05e3 \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4.`;
  const cheeseDescription = `${cheesePrologueSentences[0]} \u05de\u05de\u05e8\u05d7\u05d9 \u05d2\u05d1\u05d9\u05e0\u05ea \u05d4\u05e9\u05de\u05e0\u05ea \u05e0\u05d5\u05e4\u05dc\u05d9\u05dd \u05e0\u05de\u05d5\u05da \u05d9\u05d5\u05ea\u05e8 \u05d1\u05e8\u05d2\u05e2 \u05e9\u05e1\u05d5\u05e4\u05e8\u05d9\u05dd \u05d0\u05ea \u05d4\u05e9\u05d5\u05de\u05df \u05d4\u05d0\u05de\u05d9\u05ea\u05d9 \u05e9\u05d1\u05d4\u05dd \u2014 \u05e2\u05d3 30 \u05d0\u05d7\u05d5\u05d6. ${cheeseProducts.length} \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05d1\u05d3\u05e3 \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4.`;
  const juicesDescription = `\u05d1\u05d3\u05e7\u05e0\u05d5 ${juicesProducts.length} \u05de\u05d9\u05e6\u05d9\u05dd \u05d5\u05de\u05e9\u05e7\u05d0\u05d5\u05ea \u05e4\u05d9\u05e8\u05d5\u05ea: \u05de\u05d9\u05e5 100%, \u05e0\u05e7\u05d8\u05e8\u05d9\u05dd, \u05e9\u05d9\u05d9\u05e7\u05d9\u05dd \u05d5\u05e1\u05d7\u05d5\u05d8\u05d9 \u05e7\u05e8. \u05e8\u05e7 \u05de\u05d5\u05e6\u05e8 \u05d0\u05d7\u05d3 \u05d4\u05d2\u05d9\u05e2 \u05dc-A \u2014 \u05e1\u05d7\u05d5\u05d8 \u05ea\u05e4\u05d5\u05d6\u05d9\u05dd \u05d8\u05e8\u05d9. \u05d2\u05dd \u05de\u05d9\u05e5 100% \u05d4\u05d5\u05d0 \u05e1\u05d5\u05db\u05e8 \u05e0\u05d5\u05d6\u05dc\u05d9: 7\u201317 \u05d2\u05e8\u05dd \u05dc-100 \u05de\u201c\u05dc \u05dc\u05dc\u05d0 \u05e1\u05d9\u05d1\u05d9\u05d9\u05dd \u05d5\u05dc\u05dc\u05d0 \u05ea\u05d7\u05d5\u05e9\u05ea \u05e9\u05d5\u05d1\u05e2.`;
  const hardCheesesDescription = `\u05d1\u05d3\u05e7\u05e0\u05d5 ${hardCheesesProducts.length} \u05d2\u05d1\u05d9\u05e0\u05d5\u05ea \u05e7\u05e9\u05d5\u05ea \u05d5\u05e6\u05d4\u05d5\u05d1\u05d5\u05ea: 24 \u05e7\u05d9\u05d1\u05dc\u05d5 B, \u05e9\u05ea\u05d9\u05d9\u05dd \u05e7\u05d9\u05d1\u05dc\u05d5 C \u05d5\u05e9\u05ea\u05d9\u05d9\u05dd \u05e7\u05d9\u05d1\u05dc\u05d5 D \u2014 \u05d0\u05e3 \u05d2\u05d1\u05d9\u05e0\u05d4 \u05dc\u05d0 \u05d4\u05d2\u05d9\u05e2\u05d4 \u05dc-A. \u05ea\u05e7\u05e8\u05d9\u05ea \u05d4\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d4 \u05d4\u05d9\u05d0 B. \u05d2\u05d0\u05d5\u05d3\u05d4 \u05de\u05de\u05e8\u05db\u05d9\u05d1\u05d9\u05dd \u05de\u05d9\u05e0\u05d9\u05de\u05dc\u05d9\u05d9\u05dd \u05de\u05d5\u05d1\u05d9\u05dc\u05ea \u05d4\u05de\u05d3\u05e3; \u05d2\u05d1\u05d9\u05e0\u05d5\u05ea \u05dc\u05d9\u05d9\u05d8 \u05d5\u05de\u05e2\u05d5\u05d1\u05d3\u05d5\u05ea \u05e2\u05dd \u05de\u05d9\u05d9\u05e6\u05d1\u05d9\u05dd \u05de\u05e7\u05d1\u05dc\u05d5\u05ea \u05e6\u05d9\u05d5\u05df \u05e0\u05de\u05d5\u05da \u05d9\u05d5\u05ea\u05e8.`;
  const brinedCheesesDescription = `${brinedCheesesPrologueSentences[0]} ${brinedCheesesProducts.length} \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05d1\u05d3\u05e3 \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4.`;
  const cookiesCoffeeDescription = `\u05d1\u05d9\u05e1\u05e7\u05d5\u05d5\u05d9\u05d8\u05d9\u05dd \u05de\u05ea\u05d5\u05e7\u05d9\u05dd \u05de\u05e2\u05d5\u05d1\u05d3\u05d9\u05dd, \u05de\u05dc\u05d5\u05d5\u05d9 \u05d4\u05e7\u05e4\u05d4 \u05e9\u05dc \u05d4\u05de\u05d3\u05e3 \u05d4\u05d9\u05e9\u05e8\u05d0\u05dc\u05d9. ${cookiesCoffeeProducts.length} \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05e0\u05d1\u05d3\u05e7\u05d5 \u2014 \u05e6\u05d9\u05d5\u05df C \u05d4\u05d5\u05d0 \u05ea\u05e7\u05e8\u05d9\u05ea \u05d4\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d4. \u05d4\u05d4\u05d1\u05d3\u05dc\u05d9\u05dd: \u05e1\u05d5\u05d2 \u05d4\u05e9\u05d5\u05de\u05df, \u05db\u05de\u05d5\u05ea \u05d4\u05e1\u05d5\u05db\u05e8, \u05de\u05d5\u05e8\u05db\u05d1\u05d5\u05ea \u05e8\u05e9\u05d9\u05de\u05ea \u05d4\u05e8\u05db\u05d9\u05d1\u05d9\u05dd.`;
  const cCount = cakesHardCookiesProducts.filter((p) => p.grade === "C").length;
  const dCount = cakesHardCookiesProducts.filter((p) => p.grade === "D").length;
  const eCount = cakesHardCookiesProducts.filter((p) => p.grade === "E").length;
  const cakesTopScore = Math.max(...cakesHardCookiesProducts.map((p) => p.score ?? 0)).toFixed(1);
  const cakesDescription = `\u05d1\u05d3\u05e7\u05e0\u05d5 ${cakesHardCookiesProducts.length} \u05e2\u05d5\u05d2\u05d5\u05ea \u05de\u05d4\u05de\u05d3\u05e3 \u05d4\u05d9\u05e9\u05e8\u05d0\u05dc\u05d9 \u2014 \u05d0\u05e3 \u05de\u05d5\u05e6\u05e8 \u05dc\u05d0 \u05d4\u05d2\u05d9\u05e2 \u05dc-A \u05d0\u05d5 \u05dc-B. ${cCount} \u05e7\u05d9\u05d1\u05dc\u05d5 C (\u05d4\u05e6\u05d9\u05d5\u05df \u05d4\u05d2\u05d1\u05d5\u05d4 \u05d1\u05d9\u05d5\u05ea\u05e8 \u05d4\u05d5\u05d0 ${cakesTopScore}), ${dCount} \u05e7\u05d9\u05d1\u05dc\u05d5 D \u05d5-${eCount} \u05e7\u05d9\u05d1\u05dc\u05d5 E. \u05e6\u05d9\u05d5\u05df C \u05d4\u05d5\u05d0 \u05ea\u05e7\u05e8\u05d9\u05ea \u05d4\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d4, \u05dc\u05d0 \u05d4\u05d9\u05e9\u05d2.`;

  return (
    <HashvaotCategoryLanding
      eyebrow="Bari comparisons \xb7 \u05e1\u05d5\u05e4\u05e8\u05de\u05e8\u05e7\u05d8"
      title="\u05de\u05d5\u05e6\u05e8\u05d9 \u05e1\u05d5\u05e4\u05e8\u05de\u05e8\u05e7\u05d8"
      intro="\u05d7\u05d5\u05d5\u05d9\u05d5\u05ea \u05d4\u05e9\u05d5\u05d5\u05d0\u05d4 \u05d0\u05d9\u05e0\u05d8\u05e8\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9\u05d5\u05ea \u2014 \u05dc\u05d0 \u05de\u05d0\u05de\u05e8\u05d9\u05dd \u05e1\u05d8\u05d8\u05d9\u05e7\u05d9\u05d9\u05dd. \u05db\u05dc \u05d3\u05e3 \u05d1\u05d5\u05d7\u05df \u05de\u05d5\u05e6\u05e8\u05d9\u05dd \u05d3\u05d5\u05de\u05d9\u05dd \u05dc\u05e4\u05d9 \u05e4\u05e8\u05de\u05d8\u05e8\u05d9\u05dd \u05d5\u05de\u05e6\u05d9\u05d2 \u05d8\u05e8\u05d9\u05d9\u05d3\u05d0\u05d5\u05e4\u05d9\u05dd \u05d1\u05d4\u05e7\u05e9\u05e8 \u05d4\u05e0\u05db\u05d5\u05df."
    >
      <HashvaotComparisonCardGrid
        lead={
          <>
            <FeaturedMilkIntelligenceCard
              href={MILK_COMPARISON_HREF}
              description={milkDescription}
            />
            <p className="text-sm text-[#4E5663]">
              \u05e8\u05d5\u05e6\u05d9\u05dd \u05d0\u05ea \u05d4\u05e1\u05d9\u05e4\u05d5\u05e8 \u05de\u05d0\u05d7\u05d5\u05e8\u05d9 \u05d4\u05de\u05de\u05e6\u05d0\u05d9\u05dd?{" "}
              <Link
                href="/blog/milk-analysis"
                className="font-semibold text-[#1F8F6A] underline-offset-2 hover:underline"
              >
                \u05e7\u05e8\u05d0\u05d5 \u05d0\u05ea \u05d4\u05e0\u05d9\u05ea\u05d5\u05d7 \u05d1\u05d1\u05dc\u05d5\u05d2
              </Link>
              \u00a0\u2014 \u05d4\u05de\u05d0\u05de\u05e8 \u05de\u05e9\u05dc\u05d9\u05dd \u05d0\u05ea \u05de\u05e0\u05d5\u05e2 \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4, \u05dc\u05d0 \u05de\u05d7\u05dc\u05d9\u05e3 \u05d0\u05d5\u05ea\u05d5.
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
""", encoding="utf-8")
print("supermarket/page.tsx written")

# -- 6. /hashvaot/raw-foods/page.tsx ------------------------------------------
(base / "app/hashvaot/raw-foods").mkdir(parents=True, exist_ok=True)
(base / "app/hashvaot/raw-foods/page.tsx").write_text("""\
import type { Metadata } from "next";

import { HashvaotCategoryLanding } from "@/components/hashvaot/hashvaot-category-landing";
import { RAW_FOODS_COMING_SOON_SUBTEXT } from "@/lib/hashvaot/hashvaot-categories";

export const metadata: Metadata = {
  title: "\u05de\u05d6\u05d5\u05df \u05d2\u05d5\u05dc\u05de\u05d9 | Bari",
  description: "\u05de\u05d6\u05d5\u05df \u05d2\u05d5\u05dc\u05de\u05d9 \u2014 \u05d1\u05d1\u05e0\u05d9\u05d9\u05d4.",
  robots: { index: false, follow: false },
};

export default function RawFoodsCategoryPage() {
  return (
    <HashvaotCategoryLanding
      eyebrow="Bari comparisons \xb7 \u05de\u05d6\u05d5\u05df \u05d2\u05d5\u05dc\u05de\u05d9"
      title="\u05de\u05d6\u05d5\u05df \u05d2\u05d5\u05dc\u05de\u05d9"
      buildingSubtext={RAW_FOODS_COMING_SOON_SUBTEXT}
    />
  );
}
""", encoding="utf-8")
print("raw-foods/page.tsx written")

# -- 7. /hashvaot/personal-care/page.tsx --------------------------------------
(base / "app/hashvaot/personal-care").mkdir(parents=True, exist_ok=True)
(base / "app/hashvaot/personal-care/page.tsx").write_text("""\
import type { Metadata } from "next";

import { HashvaotCategoryLanding } from "@/components/hashvaot/hashvaot-category-landing";
import { PERSONAL_CARE_COMING_SOON_SUBTEXT } from "@/lib/hashvaot/hashvaot-categories";

export const metadata: Metadata = {
  title: "\u05d8\u05d9\u05e4\u05d5\u05d7 \u05d0\u05d9\u05e9\u05d9 | Bari",
  description: "\u05d8\u05d9\u05e4\u05d5\u05d7 \u05d0\u05d9\u05e9\u05d9 \u2014 \u05d1\u05d1\u05e0\u05d9\u05d9\u05d4.",
  robots: { index: false, follow: false },
};

export default function PersonalCareCategoryPage() {
  return (
    <HashvaotCategoryLanding
      eyebrow="Bari comparisons \xb7 \u05d8\u05d9\u05e4\u05d5\u05d7 \u05d0\u05d9\u05e9\u05d9"
      title="\u05d8\u05d9\u05e4\u05d5\u05d7 \u05d0\u05d9\u05e9\u05d9"
      buildingSubtext={PERSONAL_CARE_COMING_SOON_SUBTEXT}
    />
  );
}
""", encoding="utf-8")
print("personal-care/page.tsx written")

print("All page files written OK")
