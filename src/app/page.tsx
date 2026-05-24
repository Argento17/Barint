import { Heebo } from "next/font/google";

import { HomeAnalysisEngine } from "@/components/home/home-analysis-engine";
import { HomeComparisons } from "@/components/home/home-comparisons";
import { HomeFlagshipAnalysis } from "@/components/home/home-flagship-analysis";
import { HomeFinalCta } from "@/components/home/home-final-cta";
import { HomeFooter } from "@/components/home/home-footer";
import { HomeGuides } from "@/components/home/home-guides";
import { HomeHero } from "@/components/home/home-hero";
import { HomeMethodology } from "@/components/home/home-methodology";
import { HomeNewsletter } from "@/components/home/home-newsletter";
import { cn } from "@/lib/utils";

const heebo = Heebo({
  subsets: ["hebrew", "latin"],
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
});

export default function HomePage() {
  return (
    <div
      className={cn(
        heebo.className,
        "home-canvas relative text-[#111318] antialiased selection:bg-[#2FAE82]/20"
      )}
    >
      <main lang="he" className="relative">
        <HomeHero />
        <HomeFlagshipAnalysis />
        <HomeAnalysisEngine />
        <HomeMethodology />
        <HomeComparisons />
        <HomeGuides />
        <HomeNewsletter />
        <HomeFinalCta />
        <HomeFooter />
      </main>
    </div>
  );
}
