import { Heebo } from "next/font/google";

import { HomeCategories } from "@/components/home/home-categories";
import { HomeComparisons } from "@/components/home/home-comparisons";
import { HomeFinalCta } from "@/components/home/home-final-cta";
import { HomeFooter } from "@/components/home/home-footer";
import { HomeGuides } from "@/components/home/home-guides";
import { HomeHero } from "@/components/home/home-hero";
import { HomeMethodology } from "@/components/home/home-methodology";
import { HomeNewsletter } from "@/components/home/home-newsletter";
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
        "home-canvas relative text-zinc-900 antialiased selection:bg-emerald-500/20"
      )}
    >
      <main lang="he" className="relative">
        <HomeHero />
        <HomeCategories />
        <HomeComparisons />
        <HomeGuides />
        <HomeMethodology />
        <HomeTrust />
        <HomeNewsletter />
        <HomeFinalCta />
        <HomeFooter />
      </main>
    </div>
  );
}
