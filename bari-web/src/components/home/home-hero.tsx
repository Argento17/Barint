import Link from "next/link";
import { Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { HERO_COPY } from "@/lib/home/hero-copy";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

import { HeroProductStage } from "./hero-product-stage";
import { HomeContainer } from "./section-frame";

export function HomeHero() {
  return (
    <section
      className={cn(
        "relative overflow-hidden border-b border-black/[0.06] bg-[#F7F7F2]",
        siteHeaderOffsetClass
      )}
    >
      {/* Dual radial gradient atmosphere -- sage top-left, warm cream bottom-right */}
      <div
        className="pointer-events-none absolute inset-0 -z-10"
        aria-hidden
        style={{
          background:
            "radial-gradient(ellipse 65% 60% at 18% 38%, rgba(47,174,130,0.09) 0%, transparent 65%), radial-gradient(ellipse 55% 50% at 88% 78%, rgba(245,243,236,0.95) 0%, transparent 70%)",
        }}
      />

      <HomeContainer>
        <div
          className="hero-v5-grid py-14 md:py-[62px]"
          style={{
            direction: "ltr",
            display: "grid",
            gridTemplateAreas: "'visual copy'",
            gridTemplateColumns: "minmax(340px, 1.05fr) minmax(300px, 0.95fr)",
            gap: "4rem",
            minHeight: "580px",
            alignItems: "center",
          }}
        >
          {/* Visual column -- LEFT */}
          <div style={{ gridArea: "visual" }} className="flex items-center justify-center">
            <div className="w-full max-w-[560px]">
              <HeroProductStage />
            </div>
          </div>

          {/* Copy column -- RIGHT, reset to RTL for Hebrew */}
          <div
            style={{ gridArea: "copy", direction: "rtl" }}
            className="flex flex-col items-start gap-7 text-right"
          >
            {/* Eyebrow */}
            <p className="text-[0.78rem] font-bold uppercase tracking-widest text-[#167A58]">
              {HERO_COPY.heroEyebrow}
            </p>

            {/* H1 -- very large, clamp(48px, 6.5vw, 82px) per v5 spec */}
            <h1
              className="text-balance font-extrabold leading-[1.02] tracking-[-0.045em] text-[#111318]"
              style={{ fontSize: "clamp(2.75rem, 6.5vw, 5rem)" }}
            >
              <span className="block">{HERO_COPY.headline1}</span>
              <span className="block text-[#167A58]">
                בארי בודקת את
                <br />
                הרכיבים.
              </span>
            </h1>

            {/* Subline */}
            <p
              className="text-pretty leading-relaxed text-[#4E5663]"
              style={{ fontSize: "1.2rem", maxWidth: "36rem" }}
            >
              {HERO_COPY.subline}
            </p>

            {/* CTA block */}
            <div className="flex w-full max-w-[390px] flex-col items-stretch gap-3">
              <Button
                size="lg"
                className="rounded-2xl border border-[#1F8F6A]/10 bg-gradient-to-r from-[#167A58] to-[#1A9168] px-8 font-bold text-[#F7F7F2] shadow-[0_20px_48px_-16px_rgba(22,122,88,0.55)] transition-[box-shadow,transform] duration-500 ease-out hover:-translate-y-0.5 hover:shadow-[0_24px_56px_-16px_rgba(22,122,88,0.65)]"
                style={{ height: "70px", fontSize: "1.05rem" }}
                asChild
              >
                <Link href="/hashvaot" className="inline-flex items-center justify-center gap-2">
                  <Search className="size-5" aria-hidden />
                  {HERO_COPY.primaryCta}
                </Link>
              </Button>

              <p className="text-center text-sm font-semibold text-[#5E6560]">
                {HERO_COPY.secondaryCta}
              </p>
            </div>
          </div>
        </div>

        {/* Mobile override: stack copy first then visual */}
        <style>{`
          @media (max-width: 767px) {
            .hero-v5-grid {
              grid-template-areas: 'copy' 'visual' !important;
              grid-template-columns: 1fr !important;
              min-height: auto !important;
            }
          }
        `}</style>
      </HomeContainer>
    </section>
  );
}
