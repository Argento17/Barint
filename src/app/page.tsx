import { Heebo } from "next/font/google";

import { HomeCategories } from "@/components/home/home-categories";
import { HomeCommunity } from "@/components/home/home-community";
import { HomeComparisons } from "@/components/home/home-comparisons";
import { HomeFinalCta } from "@/components/home/home-final-cta";
import { HomeFooter } from "@/components/home/home-footer";
import { HomeGuides } from "@/components/home/home-guides";
import { HomeHero } from "@/components/home/home-hero";
import { HomeIngredients } from "@/components/home/home-ingredients";
import { HomeMethodology } from "@/components/home/home-methodology";
import { HomeNewsletter } from "@/components/home/home-newsletter";
import { HomeRankings } from "@/components/home/home-rankings";
import { HomeTrust } from "@/components/home/home-trust";
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
        "relative min-h-screen bg-white text-zinc-900 antialiased selection:bg-emerald-500/20"
      )}
    >
      <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-gradient-to-b from-zinc-50 via-white to-emerald-50/25" />
      <div
        className="pointer-events-none fixed inset-0 -z-10 opacity-90"
        style={{
          backgroundImage:
            "radial-gradient(900px 520px at 85% -5%, rgba(16, 185, 129, 0.12), transparent 55%), radial-gradient(700px 420px at 0% 45%, rgba(224, 242, 254, 0.35), transparent 52%)",
        }}
      />

      <main lang="he">
        <HomeHero />
        <HomeCategories />
        <HomeComparisons />
        <HomeGuides />
        <HomeRankings />
        <HomeMethodology />
        <HomeIngredients />
        <HomeTrust />
        <HomeCommunity />
        <HomeNewsletter />
        <HomeFinalCta />
        <HomeFooter />
      </main>
    </div>
  );
}
